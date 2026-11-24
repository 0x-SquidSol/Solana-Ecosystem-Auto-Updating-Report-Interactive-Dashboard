# Solana Ecosystem Report

> Generated 2026-11-24T22:50:05Z - heliostat 0.1.0 - 6/8 sources ok - refreshes every 15 min

## Anomalies

- 🟡 **WARNING**: data source 'solana_com' failed this run

**Recently seen**

- 2026-11-23T15:30Z true TPS is 3.5 standard deviations above its recent mean (3,180 vs 1,729)
- 2026-11-23T15:30Z data source 'solana_com' failed this run
- 2026-11-24T02:29Z data source 'solana_com' failed this run
- 2026-11-24T12:48Z data source 'solana_com' failed this run
- 2026-11-24T22:50Z data source 'solana_com' failed this run

## Network

| Metric | Value |
|---|---|
| Health | healthy |
| True TPS (non-vote) | 1,738 |
| Total TPS (incl. votes) | 1,738 |
| Peak true TPS (30 min) | 2,044 |
| Mean slot time | 0.215 s |
| Slot | 473,517,879 |
| Block height | 451,530,998 |
| Epoch | 1096 - 10.62% complete, ~23.1 h remaining |

## Validators

| Metric | Value |
|---|---|
| Active validators | 660 |
| Delinquent | 27 (0.02% of stake) |
| Consensus stall buffer | 0.1% of the 33.3% halt threshold consumed |
| Total stake | 424,794,569 SOL |
| Nakamoto coefficient | 18 |
| Top-10 stake share | 25.0% |
| Top-20 stake share | 36.1% |
| Client stake split | agave 99.3% / firedancer 0.7% |
| Stake-weighted commission | 26.14% |

**Top validators by stake**

| # | Vote account | Stake | Share | Commission |
|---|---|---|---|---|
| 1 | `he1i..uBtk` | 17,003,542 SOL | 4.00% | 0% |
| 2 | `CcaH..oTN1` | 15,962,658 SOL | 3.76% | 7% |
| 3 | `3N7s..iD5g` | 12,418,812 SOL | 2.92% | 0% |
| 4 | `8Gbw..F8iD` | 10,242,949 SOL | 2.41% | 0% |
| 5 | `51JB..UNAm` | 9,885,209 SOL | 2.33% | 10% |
| 6 | `Catz..Diqb` | 9,615,269 SOL | 2.26% | 5% |
| 7 | `26pV..3dJx` | 9,283,847 SOL | 2.19% | 7% |
| 8 | `9QU2..29mF` | 8,016,085 SOL | 1.89% | 7% |
| 9 | `Dumi..Zk4a` | 6,968,432 SOL | 1.64% | 0% |
| 10 | `CvSb..wycB` | 6,779,378 SOL | 1.60% | 5% |

## Economy

| Metric | Value |
|---|---|
| SOL price | $69.88 (-2.6% 24h, -5.0% 7d) |
| Price sources | cross-checked, 0.023% apart |
| Market cap | $41.38B |
| TVL | $4.51B (0.0% 24h) |
| Stablecoin supply | $13.22B |
| DEX volume (24h) | $1.81B |
| REV (24h) | $531.0K (network fees $424.1K + Jito tips $106.9K) |
| App fees (24h) | $8.46M |
| Median fee (user txs) | – lamports |
| Circulating supply | 592,126,875 SOL |

## Ecosystem Growth

| Metric | Value |
|---|---|
| Tokenized assets (RWA) on Solana | $541.87M across 11 protocols |
| Daily active addresses | available via optional DUNE_API_KEY |

**Largest tokenized-asset protocols**

- OnRe: $289.80M
- Huma: $242.90M
- International Stable Currency: $2.40M
- Mansory: $2.24M
- Exceed Finance exUSDC: $1.89M

## News & Upgrades


**Solana Status**

- [mb-020624](https://status.solana.com/incidents/n5kcgs8dl9pj) - 2024-02-06
- [Cluster Instability](https://status.solana.com/incidents/ymr0gyj9xqyz) - 2023-02-26
- [Public Endpoints and Explorer offline](https://status.solana.com/incidents/mf9plxrkjhnk) - 2023-01-08

**Agave Releases**

- [Release v5.0.0-alpha.1](https://github.com/anza-xyz/agave/releases/tag/v5.0.0-alpha.1) - 2026-11-19
- [Release v4.5.0-beta.0](https://github.com/anza-xyz/agave/releases/tag/v4.5.0-beta.0) - 2026-11-06
- [Release v4.4.1](https://github.com/anza-xyz/agave/releases/tag/v4.4.1) - 2026-11-05

**Firedancer Releases**

- [Firedancer Testnet Release v26.11.0](https://github.com/firedancer-io/firedancer/releases/tag/v26.11.0) - 2026-11-11
- [Firedancer Mainnet Release v26.10.8](https://github.com/firedancer-io/firedancer/releases/tag/v26.10.8) - 2026-11-11
- [v26.10.7](https://github.com/firedancer-io/firedancer/releases/tag/v26.10.7) - 2026-11-11

**SIMD Activity**

- [SIMD-0706: Reject unknown syscalls and `sol_alloc_free_` (#706)](https://github.com/solana-foundation/solana-improvement-documents/commit/44a4406237de1597ce56c1d106161dda950cbc68) - 2026-11-23
- [Amend 0529: charge a flat cu first before execution (#707)](https://github.com/solana-foundation/solana-improvement-documents/commit/6cf17cb7138d3fac03f5b637c1fde91a00fb48fc) - 2026-11-20
- [SIMD-0701: Vote Account v5 (#701)](https://github.com/solana-foundation/solana-improvement-documents/commit/ae7b00f3287a614c5aa5d0a7ceb7bad0cdc4e022) - 2026-11-06

## Data Sources

| Source | Status | Fetched |
|---|---|---|
| network | ok | 2026-11-24T22:49:55Z |
| validators | ok | 2026-11-24T22:50:03Z |
| supply | ok | 2026-11-24T22:50:05Z |
| defillama | ok | 2026-11-24T22:49:58Z |
| price | ok | 2026-11-24T22:49:54Z |
| news | ok | 2026-11-24T22:50:00Z |
| solana_com | failed: HTTP 429 (https://solana.com/data) | 2026-11-24T22:49:58Z |
| dune | off (optional) | 2026-11-24T22:49:53Z |

_On-chain data served by `https://api.mainnet-beta.solana.com`._
