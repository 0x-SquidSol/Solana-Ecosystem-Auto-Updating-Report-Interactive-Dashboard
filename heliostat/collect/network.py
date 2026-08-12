"""Core network performance metrics, straight from Solana RPC.

Covers node health, slot height, block time, epoch progress, and
throughput derived from recent performance samples. Throughput is
reported two ways on purpose:

- ``tps_total`` counts every transaction, including validator vote
  transactions, which are consensus overhead rather than user activity;
- ``tps_true`` counts non-vote transactions only — the honest measure
  of what users and programs are actually doing on the network.
"""

from __future__ import annotations

from heliostat.rpc import AllEndpointsFailed, RpcClient, RpcError
from heliostat.util import error_envelope, ok_envelope

# ~30 minutes of samples at one sample per minute
PERFORMANCE_SAMPLE_COUNT = 30


def _health(rpc: RpcClient) -> dict:
    try:
        rpc.call("getHealth")
        return {"ok": True, "detail": "ok"}
    except (RpcError, AllEndpointsFailed) as err:
        # an unhealthy answer is still an answer — report it, don't die
        return {"ok": False, "detail": str(err)}


def _throughput(samples: list[dict]) -> dict:
    usable = [s for s in samples if s.get("samplePeriodSecs")]
    total_secs = sum(s["samplePeriodSecs"] for s in usable)
    total_slots = sum(s.get("numSlots", 0) for s in usable)
    total_txs = sum(s.get("numTransactions", 0) for s in usable)

    non_vote_values = [
        s.get("numNonVoteTransactions")
        for s in usable
        if s.get("numNonVoteTransactions") is not None
    ]
    total_non_vote = sum(non_vote_values) if non_vote_values else None

    peak_total = 0.0
    peak_true = 0.0
    for s in usable:
        period = s["samplePeriodSecs"]
        peak_total = max(peak_total, s.get("numTransactions", 0) / period)
        if s.get("numNonVoteTransactions") is not None:
            peak_true = max(peak_true, s["numNonVoteTransactions"] / period)

    # per-sample series, oldest first (rpc returns newest first);
    # [minutes_ago, true_tps] pairs for minute-resolution charting
    tps_series = [
        [
            index,
            round(s["numNonVoteTransactions"] / s["samplePeriodSecs"], 1),
        ]
        for index, s in enumerate(usable)
        if s.get("numNonVoteTransactions") is not None
    ][::-1]

    return {
        "tps_series": tps_series,
        "tps_total": round(total_txs / total_secs, 1) if total_secs else None,
        "tps_true": (
            round(total_non_vote / total_secs, 1)
            if total_secs and total_non_vote is not None
            else None
        ),
        "tps_total_peak": round(peak_total, 1) if usable else None,
        "tps_true_peak": round(peak_true, 1) if non_vote_values else None,
        "mean_slot_time_secs": (
            round(total_secs / total_slots, 3) if total_slots else None
        ),
        "sample_window_minutes": round(total_secs / 60),
    }


def collect(rpc: RpcClient) -> dict:
    """Gather network metrics; returns the shared collector envelope."""
    try:
        health = _health(rpc)
        slot = rpc.call("getSlot")
        epoch = rpc.call("getEpochInfo")
        samples = rpc.call(
            "getRecentPerformanceSamples", [PERFORMANCE_SAMPLE_COUNT]
        )

        try:
            block_time = rpc.call("getBlockTime", [slot])
        except RpcError:
            # the newest slot may not have an available timestamp yet
            block_time = None

        throughput = _throughput(samples or [])

        slot_index = epoch.get("slotIndex", 0)
        slots_in_epoch = epoch.get("slotsInEpoch") or 1
        remaining_slots = slots_in_epoch - slot_index
        slot_time = throughput.get("mean_slot_time_secs")

        data = {
            "health": health,
            "slot": slot,
            "block_height": epoch.get("blockHeight"),
            "block_time_unix": block_time,
            "epoch": epoch.get("epoch"),
            "epoch_progress_pct": round(100.0 * slot_index / slots_in_epoch, 2),
            "epoch_slot_index": slot_index,
            "epoch_slots_total": slots_in_epoch,
            "epoch_remaining_hours": (
                round(remaining_slots * slot_time / 3600, 1)
                if slot_time
                else None
            ),
            **throughput,
        }
        return ok_envelope(data)
    except Exception as err:  # noqa: BLE001 - one source must never kill the report
        return error_envelope(err)
