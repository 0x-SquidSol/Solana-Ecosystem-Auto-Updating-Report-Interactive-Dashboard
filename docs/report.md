# Solana Ecosystem Report

> Generated 2026-11-23T15:30:18Z - heliostat 0.1.0 - 6/8 sources ok - refreshes every 15 min

## Anomalies

- 🔴 **ALERT**: true TPS is 3.5 standard deviations above its recent mean (3,180 vs 1,729)
- 🟡 **WARNING**: data source 'solana_com' failed this run

**Recently seen**

- 2026-11-22T18:48Z data source 'solana_com' failed this run
- 2026-11-22T23:56Z data source 'solana_com' failed this run
- 2026-11-23T04:52Z data source 'solana_com' failed this run
- 2026-11-23T15:30Z true TPS is 3.5 standard deviations above its recent mean (3,180 vs 1,729)
- 2026-11-23T15:30Z data source 'solana_com' failed this run

## Network

| Metric | Value |
|---|---|
| Health | healthy |
| True TPS (non-vote) | 3,180 |
| Total TPS (incl. votes) | 3,180 |
| Peak true TPS (30 min) | 3,904 |
| Mean slot time | 0.215 s |
| Slot | 472,993,324 |
| Block height | 451,006,786 |
| Epoch | 1094 - 89.20% complete, ~2.8 h remaining |

## Validators

| Metric | Value |
|---|---|
| Active validators | 660 |
| Delinquent | 25 (0.04% of stake) |
| Consensus stall buffer | 0.1% of the 33.3% halt threshold consumed |
| Total stake | 425,691,542 SOL |
| Nakamoto coefficient | 18 |
| Top-10 stake share | 25.0% |
| Top-20 stake share | 36.0% |
| Client stake split | agave 98.7% / firedancer 1.3% |
| Stake-weighted commission | 26.10% |

**Top validators by stake**

| # | Vote account | Stake | Share | Commission |
|---|---|---|---|---|
| 1 | `he1i..uBtk` | 16,918,440 SOL | 3.98% | 0% |
| 2 | `CcaH..oTN1` | 16,346,959 SOL | 3.84% | 7% |
| 3 | `3N7s..iD5g` | 12,401,889 SOL | 2.91% | 0% |
| 4 | `8Gbw..F8iD` | 10,243,005 SOL | 2.41% | 0% |
| 5 | `51JB..UNAm` | 9,842,253 SOL | 2.31% | 10% |
| 6 | `Catz..Diqb` | 9,612,896 SOL | 2.26% | 5% |
| 7 | `26pV..3dJx` | 9,269,555 SOL | 2.18% | 7% |
| 8 | `9QU2..29mF` | 7,998,895 SOL | 1.88% | 7% |
| 9 | `Dumi..Zk4a` | 6,987,495 SOL | 1.64% | 0% |
| 10 | `CvSb..wycB` | 6,775,083 SOL | 1.59% | 5% |

## Economy

| Metric | Value |
|---|---|
| SOL price | $76.51 (+8.8% 24h, +7.9% 7d) |
| Price sources | cross-checked, 0.124% apart |
| Market cap | $45.29B |
| TVL | $4.76B (+3.6% 24h) |
| Stablecoin supply | $13.44B |
| DEX volume (24h) | $975.74M |
| REV (24h) | $369.8K (network fees $287.1K + Jito tips $82.7K) |
| App fees (24h) | $5.92M |
| Median fee (user txs) | – lamports |
| Circulating supply | 592,016,624 SOL |

## Ecosystem Growth

| Metric | Value |
|---|---|
| Tokenized assets (RWA) on Solana | $521.91M across 11 protocols |
| Daily active addresses | available via optional DUNE_API_KEY |

**Largest tokenized-asset protocols**

- OnRe: $289.69M
- Huma: $223.64M
- International Stable Currency: $2.41M
- Mansory: $2.20M
- Exceed Finance exUSDC: $1.34M

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
| network | ok | 2026-11-23T15:30:07Z |
| validators | ok | 2026-11-23T15:30:18Z |
| supply | ok | 2026-11-23T15:30:17Z |
| defillama | ok | 2026-11-23T15:30:07Z |
| price | ok | 2026-11-23T15:30:09Z |
| news | ok | 2026-11-23T15:30:11Z |
| solana_com | failed: HTTP 429 (https://solana.com/data) | 2026-11-23T15:30:09Z |
| dune | off (optional) | 2026-11-23T15:30:05Z |

_On-chain data served by `https://api.mainnet-beta.solana.com`._
