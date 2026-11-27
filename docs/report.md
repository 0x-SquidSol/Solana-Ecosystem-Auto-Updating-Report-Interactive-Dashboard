# Solana Ecosystem Report

> Generated 2026-11-27T18:33:31Z - heliostat 0.1.0 - 6/8 sources ok - refreshes every 15 min

## Anomalies

- 🟡 **WARNING**: data source 'solana_com' failed this run

**Recently seen**

- 2026-11-26T15:58Z data source 'solana_com' failed this run
- 2026-11-27T00:17Z delinquent stake is 2.8 standard deviations above its recent mean (0.06 vs 0.0259091)
- 2026-11-27T00:17Z data source 'solana_com' failed this run
- 2026-11-27T08:52Z data source 'solana_com' failed this run
- 2026-11-27T18:33Z data source 'solana_com' failed this run

## Network

| Metric | Value |
|---|---|
| Health | healthy |
| True TPS (non-vote) | 2,115 |
| Total TPS (incl. votes) | 2,115 |
| Peak true TPS (30 min) | 3,207 |
| Mean slot time | 0.214 s |
| Slot | 474,652,110 |
| Block height | 452,664,764 |
| Epoch | 1098 - 73.17% complete, ~6.9 h remaining |

## Validators

| Metric | Value |
|---|---|
| Active validators | 654 |
| Delinquent | 34 (0.06% of stake) |
| Consensus stall buffer | 0.2% of the 33.3% halt threshold consumed |
| Total stake | 424,207,451 SOL |
| Nakamoto coefficient | 18 |
| Top-10 stake share | 25.0% |
| Top-20 stake share | 36.1% |
| Client stake split | agave 99.3% / firedancer 0.7% |
| Stake-weighted commission | 26.19% |

**Top validators by stake**

| # | Vote account | Stake | Share | Commission |
|---|---|---|---|---|
| 1 | `he1i..uBtk` | 16,815,245 SOL | 3.97% | 0% |
| 2 | `CcaH..oTN1` | 15,826,052 SOL | 3.73% | 7% |
| 3 | `3N7s..iD5g` | 12,437,388 SOL | 2.93% | 0% |
| 4 | `8Gbw..F8iD` | 10,238,108 SOL | 2.41% | 0% |
| 5 | `51JB..UNAm` | 9,920,637 SOL | 2.34% | 10% |
| 6 | `Catz..Diqb` | 9,617,109 SOL | 2.27% | 5% |
| 7 | `26pV..3dJx` | 9,296,651 SOL | 2.19% | 7% |
| 8 | `9QU2..29mF` | 8,037,877 SOL | 1.90% | 7% |
| 9 | `Dumi..Zk4a` | 6,972,141 SOL | 1.64% | 0% |
| 10 | `CvSb..wycB` | 6,741,351 SOL | 1.59% | 5% |

## Economy

| Metric | Value |
|---|---|
| SOL price | $71.71 (+0.8% 24h, +3.5% 7d) |
| Price sources | cross-checked, 0.068% apart |
| Market cap | $42.46B |
| TVL | $4.61B (+0.6% 24h) |
| Stablecoin supply | $12.77B |
| DEX volume (24h) | $870.58M |
| REV (24h) | $413.7K (network fees $332.6K + Jito tips $81.1K) |
| App fees (24h) | $6.15M |
| Median fee (user txs) | – lamports |
| Circulating supply | 592,238,160 SOL |

## Ecosystem Growth

| Metric | Value |
|---|---|
| Tokenized assets (RWA) on Solana | $544.05M across 11 protocols |
| Daily active addresses | available via optional DUNE_API_KEY |

**Largest tokenized-asset protocols**

- OnRe: $290.35M
- Huma: $244.47M
- International Stable Currency: $2.40M
- Mansory: $2.31M
- Exceed Finance exUSDC: $1.89M

## News & Upgrades


**Solana Status**

- [mb-020624](https://status.solana.com/incidents/n5kcgs8dl9pj) - 2024-02-06
- [Cluster Instability](https://status.solana.com/incidents/ymr0gyj9xqyz) - 2023-02-26
- [Public Endpoints and Explorer offline](https://status.solana.com/incidents/mf9plxrkjhnk) - 2023-01-08

**Agave Releases**

- [Release v4.5.0-rc.0](https://github.com/anza-xyz/agave/releases/tag/v4.5.0-rc.0) - 2026-11-26
- [Release v5.0.0-alpha.1](https://github.com/anza-xyz/agave/releases/tag/v5.0.0-alpha.1) - 2026-11-19
- [Release v4.5.0-beta.0](https://github.com/anza-xyz/agave/releases/tag/v4.5.0-beta.0) - 2026-11-26

**Firedancer Releases**

- [Firedancer Mainnet Release v26.11.1](https://github.com/firedancer-io/firedancer/releases/tag/v26.11.1) - 2026-11-25
- [Firedancer Testnet Release v26.11.0](https://github.com/firedancer-io/firedancer/releases/tag/v26.11.0) - 2026-11-11
- [Firedancer Mainnet Release v26.10.8](https://github.com/firedancer-io/firedancer/releases/tag/v26.10.8) - 2026-11-11

## Data Sources

| Source | Status | Fetched |
|---|---|---|
| network | ok | 2026-11-27T18:33:14Z |
| validators | ok | 2026-11-27T18:33:22Z |
| supply | ok | 2026-11-27T18:33:25Z |
| defillama | ok | 2026-11-27T18:33:14Z |
| price | ok | 2026-11-27T18:33:12Z |
| news | ok | 2026-11-27T18:33:31Z |
| solana_com | failed: HTTP 429 (https://solana.com/data) | 2026-11-27T18:33:16Z |
| dune | off (optional) | 2026-11-27T18:33:11Z |

_On-chain data served by `https://api.mainnet-beta.solana.com`._
