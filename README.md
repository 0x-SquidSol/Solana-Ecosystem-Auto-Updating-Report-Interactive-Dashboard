# Solana Ecosystem Report

[![tests](https://github.com/0x-SquidSol/Solana-Ecosystem-Auto-Updating-Report-Interactive-Dashboard/actions/workflows/tests.yml/badge.svg)](https://github.com/0x-SquidSol/Solana-Ecosystem-Auto-Updating-Report-Interactive-Dashboard/actions/workflows/tests.yml)
[![report](https://github.com/0x-SquidSol/Solana-Ecosystem-Auto-Updating-Report-Interactive-Dashboard/actions/workflows/report.yml/badge.svg)](https://github.com/0x-SquidSol/Solana-Ecosystem-Auto-Updating-Report-Interactive-Dashboard/actions/workflows/report.yml)

**A self-updating report and interactive dashboard on the state of the
Solana network — pure Python standard library, zero API keys, zero
third-party dependencies.**

**Live dashboard:**
<https://0x-squidsol.github.io/Solana-Ecosystem-Auto-Updating-Report-Interactive-Dashboard/>

Every 15 minutes, the engine (`heliostat`) collects on-chain data over
public Solana RPC alongside public off-chain sources, detects anomalies
against its own accumulated history, and renders three outputs:

| Output | Live | Frozen sample |
|---|---|---|
| Interactive HTML dashboard (dark) | [dashboard](https://0x-squidsol.github.io/Solana-Ecosystem-Auto-Updating-Report-Interactive-Dashboard/) | — |
| Human-readable Markdown | [docs/report.md](docs/report.md) | [samples/report.md](samples/report.md) |
| Machine-readable JSON | [docs/report.json](docs/report.json) | [samples/report.json](samples/report.json) |

## Quick start

```bash
git clone https://github.com/0x-SquidSol/Solana-Ecosystem-Auto-Updating-Report-Interactive-Dashboard.git
cd Solana-Ecosystem-Auto-Updating-Report-Interactive-Dashboard
python -m heliostat --once
```

Then open `docs/index.html` in a browser. That's the entire setup:
no `pip install`, no API keys, no build step — any Python 3.10+
installation is sufficient. `python -m heliostat --loop` keeps
regenerating on the configured interval instead of exiting.

## What it reports

- **Network performance** — true (non-vote) and total TPS with a
  minute-resolution 30-minute chart, peak throughput, mean slot time,
  slot height with a live client-side estimate, block height, epoch
  progress with a countdown to the boundary.
- **Validators** — active/delinquent counts and stake, the Nakamoto
  (superminority) coefficient, top-10/20 stake concentration, a stake
  "skyline" of every active validator (hover to inspect each one),
  stake-weighted client split between Agave and Firedancer, commission
  distribution and stake-weighted mean, top validators table.
- **Economy** — SOL price cross-checked between two independent
  sources, market cap, stablecoin supply, DEX volume, REV (network
  fees + Jito MEV tips, kept strictly separate from application fees),
  and the median fee of real user transactions from a sampled block —
  votes excluded — expressed in lamports, USD, and transactions-per-dollar.
- **Ecosystem growth** — tokenized real-world assets on Solana by
  protocol (BlackRock BUIDL, xStocks, …), plus headline figures
  published on solana.com/data including monthly active addresses.
- **News & upgrades** — the Solana blog, status-page incident history,
  Agave and Firedancer releases, and recent SIMD (protocol proposal)
  activity, where upgrades like Alpenglow surface first.
- **Anomalies** — statistical and rule-based detection with a
  persistent log of recent alerts (details below).

## Data sources and how they are integrated

| Source | What | How |
|---|---|---|
| Solana JSON-RPC | network, validators, supply, fees, heartbeats | direct calls to public endpoints with automatic failover; no key |
| DeFiLlama | TVL + 30-day series, stablecoins, DEX volume, fees, RWA | free public API; no key |
| CoinGecko | SOL price, market cap, changes | free public endpoint; no key |
| Jupiter | second, on-chain-derived SOL price | free public endpoint; no key; cross-checked against CoinGecko |
| solana.com/data | headline ecosystem figures incl. monthly active addresses | the page server-renders its stats; fetched and parsed directly, each figure labelled with provenance |
| GitHub feeds | Agave/Firedancer releases, SIMD activity | public Atom feeds; no key |
| status.solana.com | incident history | public RSS |
| Dune Analytics | optional enrichment (e.g. daily active addresses) | activates only when `DUNE_API_KEY` is set; see below |

RPC methods used: `getSlot`, `getBlockTime`, `getEpochInfo`,
`getRecentPerformanceSamples`, `getVoteAccounts`, `getBalance`,
`getSignaturesForAddress`, `getHealth`, `getSupply` — plus
`getClusterNodes` (client versions), `getBlock` (fee sampling), and
`getRecentPrioritizationFees`.

**About Twitter:** deliberately not used. Twitter has no keyless API,
and scraping it is fragile and against its terms of service. The
primary sources above — the Foundation's own blog, status page, and
the client repositories — cover announcements and incidents without a
scraper that breaks the week after submission.

**About the price cross-check:** CoinGecko aggregates exchange order
books; Jupiter derives price from on-chain liquidity. When two
independent methodologies agree within tolerance the number is
trustworthy; divergence beyond 1% raises a flag, and either source
alone can carry the headline if the other is down.

## Automation strategy

A GitHub Actions workflow runs the generator every 15 minutes,
commits the refreshed outputs, and GitHub Pages serves `docs/` as the
live dashboard. Because each run commits a compact snapshot of
selected metrics under `data/`, **the repository's git history is the
time-series database** — no external storage, and anyone who clones
the repo gets the full measurement history. Recent days keep per-run
snapshots; older days are compacted into daily min/mean/max rollups
so history stays rich while the repository stays small.

The refresh interval is one setting (`refresh_interval_minutes` in
`config.json`, mirrored by the workflow cron), and the dashboard
reads it for its auto-reload and staleness indicator, which turns
amber if data stops arriving.

### Run your own

1. Fork this repository.
2. Enable **Actions** (Actions tab → enable workflows).
3. Enable **Pages** (Settings → Pages → deploy from branch → `main`,
   `/docs`).

That's a personal, self-updating Solana dashboard in about two
minutes, refreshing on schedule with zero servers and zero keys.

## Anomaly detection

Two complementary layers run on every refresh:

- **Statistical.** For each watched metric — true TPS, slot time,
  delinquent stake, TVL, SOL price — the rolling mean and standard
  deviation of accumulated snapshots define "normal", and the current
  value's z-score flags unusual moves: |z| ≥ 2.5 warns, ≥ 3.5 alerts.
  There are no hard-coded thresholds to go stale; the baseline is
  measured. Detection stays disarmed until enough history exists
  (12 samples), so a fresh clone never fires false alarms, and each
  metric only alerts in the direction that is actually bad — slot
  time far *below* normal is fast, not broken.
- **Rule-based.** Conditions that are wrong at any z-score: RPC health
  failing, delinquent stake above the configured limit, price sources
  diverging, a data source failing.

Every alert is appended to a rolling 14-day log, so the dashboard
shows recently *resolved* incidents alongside active ones — a
detector whose work stays visible.

This is not theoretical. On 2026-08-12 at 04:16 UTC the detector
caught a delinquency spike to **21.2% of all stake** — roughly
two-thirds of the way to the 33.3% threshold at which Solana halts —
and recorded its recovery within the following half hour. The
validators panel carries a dedicated **consensus stall buffer** gauge
so events like this read at a glance: it shows how much of the halt
margin current delinquency is consuming.

## Configuration

Everything lives in `config.json`; environment variables override.

| Key | Default | Meaning |
|---|---|---|
| `rpc_endpoints` | two public endpoints | ordered failover list; `HELIOSTAT_RPC_URL` prepends a preferred endpoint |
| `refresh_interval_minutes` | 15 | loop cadence, dashboard auto-reload, staleness threshold |
| `top_validators` | 25 | table depth |
| `history_days` | 7 | per-run snapshot retention before rollup compaction |
| `http_timeout_seconds` | 10 | per-request timeout |
| `delinquent_stake_alert_pct` | 5.0 | rule-based delinquency alert level |
| `heartbeat_addresses` | USDC mint, Jupiter v6 | accounts probed for last-activity liveness |
| `dune_query_ids` | `{}` | optional: label → public Dune query id |

**Dune (optional):** set `DUNE_API_KEY` in the environment and map
labels to query ids in `dune_query_ids`. Queries should return a
single row whose first column is the value to display (e.g. a daily
active addresses query). Without a key the section reports itself
`off` — never `failed` — and the rest of the report is unaffected.
The key travels only in a request header and is never written to disk.

## Design notes

- **Zero dependencies, zero keys** — runs on a clean Python 3.10+
  install, works identically on a laptop and a CI runner, and has no
  supply chain to audit. The dashboard is a single self-contained HTML
  file: inline CSS, a small amount of inline JavaScript, hand-rolled
  SVG charts, no external requests of any kind.
- **Failure containment** — every collector returns a status envelope;
  a dead source renders as an "unavailable" note in its section while
  everything else stays live. Sub-fetches degrade independently, and
  the run only fails if *everything* fails.
- **Honest presentation** — every metric shows its source and fetch
  time; live-updating figures (slot height, epoch countdown) are
  labelled as estimates and re-anchor to measured values each refresh;
  marketing-tier figures from solana.com are labelled with provenance
  rather than blended into measured data.
- **Trusted feeds only for XML** — feed parsing uses the standard
  library and is limited to a fixed set of primary sources.

## Tests

```bash
python -m unittest discover -s tests
```

The suite runs entirely offline against recorded fixtures — no
network access — covering collectors, storage, anomaly detection,
renderers (including escaping of externally sourced text), and the CLI.

## License

[MIT](LICENSE)
