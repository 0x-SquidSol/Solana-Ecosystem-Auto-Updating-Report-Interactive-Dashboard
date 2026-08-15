"""Validator set health: stake distribution, delinquency, and clients.

Alongside the counts every explorer shows, this collector computes two
decentralization measures worth watching:

- the **superminority (Nakamoto) coefficient**: the smallest number of
  validators that together control more than a third of total stake —
  enough to halt the network if they colluded or failed together;
- the **stake-weighted client split** between Agave and Firedancer,
  joined from gossip node versions, since client diversity is its own
  form of resilience.

Version heuristic: Firedancer reports versions like ``0.505.20216``
(major version 0), while Agave-lineage clients report ``2.x``/``3.x``.
"""

from __future__ import annotations

from heliostat.rpc import RpcClient
from heliostat.util import error_envelope, lamports_to_sol, ok_envelope

SUPERMINORITY_THRESHOLD = 1.0 / 3.0

COMMISSION_BUCKETS = [
    ("0%", lambda c: c == 0),
    ("1-5%", lambda c: 1 <= c <= 5),
    ("6-10%", lambda c: 6 <= c <= 10),
    (">10%", lambda c: c > 10),
]


def _client_family(version: str | None) -> str:
    if not version:
        return "unknown"
    major = version.split(".", 1)[0]
    return "firedancer" if major == "0" else "agave"


def _short(pubkey: str | None) -> str:
    key = pubkey or ""
    return f"{key[:4]}..{key[-4:]}" if len(key) > 10 else key


def _nakamoto_coefficient(stakes_desc: list[int], total_stake: int) -> int | None:
    if not total_stake:
        return None
    cumulative = 0
    for count, stake in enumerate(stakes_desc, start=1):
        cumulative += stake
        if cumulative > total_stake * SUPERMINORITY_THRESHOLD:
            return count
    return None


def _concentration_pct(stakes_desc: list[int], total_stake: int, top: int) -> float | None:
    if not total_stake:
        return None
    return round(100.0 * sum(stakes_desc[:top]) / total_stake, 1)


def collect(rpc: RpcClient, top_n: int = 25, delinquent_alert_pct: float = 5.0) -> dict:
    """Gather validator metrics; returns the shared collector envelope."""
    try:
        vote_accounts = rpc.call("getVoteAccounts")
        current = vote_accounts.get("current", [])
        delinquent = vote_accounts.get("delinquent", [])

        active_stakes = sorted(
            (v.get("activatedStake", 0) for v in current), reverse=True
        )
        active_total = sum(active_stakes)
        delinquent_total = sum(v.get("activatedStake", 0) for v in delinquent)
        combined_total = active_total + delinquent_total

        delinquent_stake_pct = (
            round(100.0 * delinquent_total / combined_total, 2) if combined_total else None
        )
        # consensus halts if more than a third of stake stops voting;
        # express current delinquency as consumption of that margin
        stall_buffer_used_pct = (
            round(min(100.0, delinquent_stake_pct * 3.0), 1)
            if delinquent_stake_pct is not None
            else None
        )

        top_validators = sorted(
            current, key=lambda v: v.get("activatedStake", 0), reverse=True
        )[:top_n]
        top_list = [
            {
                "vote_pubkey": v.get("votePubkey"),
                "node_pubkey": v.get("nodePubkey"),
                "stake_sol": round(lamports_to_sol(v.get("activatedStake", 0))),
                "stake_pct": (
                    round(100.0 * v.get("activatedStake", 0) / active_total, 2)
                    if active_total
                    else None
                ),
                "commission_pct": v.get("commission"),
            }
            for v in top_validators
        ]

        commissions = [v.get("commission", 0) for v in current]
        histogram = {
            label: sum(1 for c in commissions if predicate(c))
            for label, predicate in COMMISSION_BUCKETS
        }
        weighted_commission = (
            round(
                sum(
                    v.get("commission", 0) * v.get("activatedStake", 0)
                    for v in current
                )
                / active_total,
                2,
            )
            if active_total
            else None
        )

        # stake-weighted client split, joined via gossip identity pubkeys
        nodes = rpc.call("getClusterNodes")
        version_by_pubkey = {
            n.get("pubkey"): n.get("version") for n in nodes or []
        }
        client_stake: dict[str, int] = {}
        for v in current:
            family = _client_family(version_by_pubkey.get(v.get("nodePubkey")))
            client_stake[family] = client_stake.get(family, 0) + v.get(
                "activatedStake", 0
            )
        client_split_pct = (
            {
                family: round(100.0 * stake / active_total, 1)
                for family, stake in sorted(client_stake.items())
            }
            if active_total
            else {}
        )

        # every active validator in compact form for distribution
        # charts and machine consumers: [stake_sol, commission,
        # short_vote_pubkey, client_family], largest stake first
        all_validators = [
            [
                round(lamports_to_sol(v.get("activatedStake", 0))),
                v.get("commission"),
                _short(v.get("votePubkey")),
                _client_family(version_by_pubkey.get(v.get("nodePubkey"))),
            ]
            for v in sorted(
                current, key=lambda v: v.get("activatedStake", 0), reverse=True
            )
        ]

        data = {
            "active_count": len(current),
            "delinquent_count": len(delinquent),
            "delinquent_stake_pct": delinquent_stake_pct,
            "stall_buffer_used_pct": stall_buffer_used_pct,
            "delinquency_alert": (
                delinquent_stake_pct is not None
                and delinquent_stake_pct >= delinquent_alert_pct
            ),
            "total_stake_sol": round(lamports_to_sol(combined_total)),
            "nakamoto_coefficient": _nakamoto_coefficient(
                active_stakes, active_total
            ),
            "top10_stake_pct": _concentration_pct(active_stakes, active_total, 10),
            "top20_stake_pct": _concentration_pct(active_stakes, active_total, 20),
            "top_validators": top_list,
            "all_validators": all_validators,
            "commission_histogram": histogram,
            "weighted_mean_commission_pct": weighted_commission,
            "client_stake_split_pct": client_split_pct,
        }
        return ok_envelope(data)
    except Exception as err:  # noqa: BLE001 - one source must never kill the report
        return error_envelope(err)
