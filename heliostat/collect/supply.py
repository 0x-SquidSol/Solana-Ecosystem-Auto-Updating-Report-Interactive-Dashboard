"""SOL supply, transaction fees, and liveness heartbeats.

Fee methodology: the commonly quoted "median fee" is misleading if it
includes validator vote transactions, which all pay the same base fee.
This collector samples one recent finalized block, filters votes out by
looking for the vote program in each transaction's account keys, and
reports the median fee of what remains — the fee a real user actually
paid. Recent prioritization fees are reported separately as the going
rate for priority inclusion.

The "heartbeat" reads the most recent transaction signature for a few
well-known, permanently busy addresses (configurable). Seconds since
their last activity is a simple, chain-native liveness signal for core
ecosystem infrastructure.
"""

from __future__ import annotations

from statistics import median

from heliostat.rpc import RpcClient, RpcError
from heliostat.util import error_envelope, lamports_to_sol, ok_envelope

VOTE_PROGRAM_ID = "Vote111111111111111111111111111111111111111"
INCINERATOR_ADDRESS = "1nc1nerator11111111111111111111111111111111"

# sample a block a little behind the tip so it is surely finalized
BLOCK_SAMPLE_OFFSET = 100


def _fee_sample(rpc: RpcClient) -> dict:
    """Median fee from one recent finalized block, votes excluded."""
    slot = rpc.call("getSlot", [{"commitment": "finalized"}])
    target = slot - BLOCK_SAMPLE_OFFSET
    block = rpc.call(
        "getBlock",
        [
            target,
            {
                "transactionDetails": "accounts",
                "rewards": False,
                "maxSupportedTransactionVersion": 0,
            },
        ],
    )
    user_fees: list[int] = []
    vote_count = 0
    for tx in block.get("transactions", []):
        meta = tx.get("meta") or {}
        fee = meta.get("fee")
        if fee is None:
            continue
        keys = tx.get("transaction", {}).get("accountKeys", [])
        pubkeys = {
            k.get("pubkey") if isinstance(k, dict) else k for k in keys
        }
        if VOTE_PROGRAM_ID in pubkeys:
            vote_count += 1
            continue
        user_fees.append(fee)

    return {
        "sampled_slot": target,
        "block_tx_count": len(block.get("transactions", [])),
        "block_vote_tx_count": vote_count,
        "median_fee_lamports": round(median(user_fees)) if user_fees else None,
        "mean_fee_lamports": (
            round(sum(user_fees) / len(user_fees)) if user_fees else None
        ),
    }


def _prioritization_fees(rpc: RpcClient) -> dict:
    fees = rpc.call("getRecentPrioritizationFees", [[]])
    values = [f.get("prioritizationFee", 0) for f in fees or []]
    if not values:
        return {"median_priority_fee_microlamports": None,
                "max_priority_fee_microlamports": None}
    return {
        "median_priority_fee_microlamports": round(median(values)),
        "max_priority_fee_microlamports": max(values),
    }


def _heartbeats(rpc: RpcClient, addresses: dict[str, str], now_unix: int) -> list[dict]:
    beats = []
    for label, address in addresses.items():
        entry: dict = {"label": label, "address": address}
        try:
            sigs = rpc.call(
                "getSignaturesForAddress", [address, {"limit": 1}]
            )
            block_time = sigs[0].get("blockTime") if sigs else None
            entry["last_activity_unix"] = block_time
            entry["seconds_since_activity"] = (
                max(0, now_unix - block_time) if block_time else None
            )
        except RpcError as err:
            entry["last_activity_unix"] = None
            entry["seconds_since_activity"] = None
            entry["error"] = str(err)
        beats.append(entry)
    return beats


def collect(rpc: RpcClient, heartbeat_addresses: dict[str, str], now_unix: int) -> dict:
    """Gather supply and fee metrics; returns the shared collector envelope."""
    try:
        supply = rpc.call("getSupply", [{"excludeNonCirculatingAccountsList": True}])
        value = supply.get("value", {})

        try:
            fees = _fee_sample(rpc)
        except Exception as err:  # noqa: BLE001 - getBlock is the heaviest call
            fees = {"error": f"block sample unavailable: {err}"}

        incinerator_lamports = rpc.call("getBalance", [INCINERATOR_ADDRESS])
        if isinstance(incinerator_lamports, dict):
            incinerator_lamports = incinerator_lamports.get("value", 0)

        data = {
            "total_supply_sol": round(lamports_to_sol(value.get("total", 0))),
            "circulating_supply_sol": round(
                lamports_to_sol(value.get("circulating", 0))
            ),
            "non_circulating_supply_sol": round(
                lamports_to_sol(value.get("nonCirculating", 0))
            ),
            "fees": fees,
            **_prioritization_fees(rpc),
            "incinerator_balance_sol": round(
                lamports_to_sol(incinerator_lamports), 4
            ),
            "heartbeats": _heartbeats(rpc, heartbeat_addresses, now_unix),
        }
        return ok_envelope(data)
    except Exception as err:  # noqa: BLE001 - one source must never kill the report
        return error_envelope(err)
