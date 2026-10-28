# Solana Ecosystem Report

> Generated 2026-10-28T17:22:27Z - heliostat 0.1.0 - 6/8 sources ok - refreshes every 15 min

## Anomalies

- 🟡 **WARNING**: delinquent stake is 3.4 standard deviations above its recent mean (0.9 vs 0.156667)
- 🟡 **WARNING**: data source 'solana_com' failed this run

**Recently seen**

- 2026-10-28T00:14Z delinquent stake is 7.8 standard deviations above its recent mean (0.89 vs 0.104286)
- 2026-10-28T05:42Z delinquent stake is 4.9 standard deviations above its recent mean (0.89 vs 0.122558)
- 2026-10-28T11:38Z delinquent stake is 3.9 standard deviations above its recent mean (0.89 vs 0.14)
- 2026-10-28T17:22Z delinquent stake is 3.4 standard deviations above its recent mean (0.9 vs 0.156667)
- 2026-10-28T17:22Z data source 'solana_com' failed this run

## Network

| Metric | Value |
|---|---|
| Health | healthy |
| True TPS (non-vote) | 2,136 |
| Total TPS (incl. votes) | 2,136 |
| Peak true TPS (30 min) | 2,686 |
| Mean slot time | 0.213 s |
| Slot | 462,559,167 |
| Block height | 440,583,637 |
| Epoch | 1070 - 73.88% complete, ~6.7 h remaining |

## Validators

| Metric | Value |
|---|---|
| Active validators | 660 |
| Delinquent | 31 (0.90% of stake) |
| Consensus stall buffer | 2.7% of the 33.3% halt threshold consumed |
| Total stake | 437,290,026 SOL |
| Nakamoto coefficient | 18 |
| Top-10 stake share | 24.8% |
| Top-20 stake share | 36.0% |
| Client stake split | agave 99.9% / firedancer 0.1% / unknown 0.1% |
| Stake-weighted commission | 26.95% |

**Top validators by stake**

| # | Vote account | Stake | Share | Commission |
|---|---|---|---|---|
| 1 | `CcaH..oTN1` | 17,006,422 SOL | 3.92% | 7% |
| 2 | `he1i..uBtk` | 16,661,096 SOL | 3.84% | 0% |
| 3 | `3N7s..iD5g` | 12,791,931 SOL | 2.95% | 0% |
| 4 | `8Gbw..F8iD` | 10,815,143 SOL | 2.50% | 0% |
| 5 | `Catz..Diqb` | 9,718,548 SOL | 2.24% | 5% |
| 6 | `51JB..UNAm` | 9,464,443 SOL | 2.18% | 10% |
| 7 | `26pV..3dJx` | 9,208,877 SOL | 2.13% | 7% |
| 8 | `9QU2..29mF` | 7,757,994 SOL | 1.79% | 7% |
| 9 | `CvSb..wycB` | 7,041,146 SOL | 1.62% | 5% |
| 10 | `Dumi..Zk4a` | 6,997,044 SOL | 1.61% | 0% |

## Economy

| Metric | Value |
|---|---|
| SOL price | $100.93 (+0.0% 24h, -6.8% 7d) |
| Price sources | cross-checked, 0.048% apart |
| Market cap | $59.55B |
| TVL | $5.70B (+0.7% 24h) |
| Stablecoin supply | $15.19B |
| DEX volume (24h) | $1.58B |
| REV (24h) | $680.2K (network fees $538.0K + Jito tips $142.2K) |
| App fees (24h) | $10.91M |
| Median fee (user txs) | – lamports |
| Circulating supply | 589,928,302 SOL |

## Ecosystem Growth

| Metric | Value |
|---|---|
| Tokenized assets (RWA) on Solana | $603.04M across 13 protocols |
| Daily active addresses | available via optional DUNE_API_KEY |

**Largest tokenized-asset protocols**

- OnRe: $301.39M
- Huma: $254.00M
- Plume Vaults: $37.12M
- Mansory: $2.63M
- International Stable Currency: $2.40M

## News & Upgrades


**Solana Status**

- [mb-020624](https://status.solana.com/incidents/n5kcgs8dl9pj) - 2024-02-06
- [Cluster Instability](https://status.solana.com/incidents/ymr0gyj9xqyz) - 2023-02-26
- [Public Endpoints and Explorer offline](https://status.solana.com/incidents/mf9plxrkjhnk) - 2023-01-08

**Agave Releases**

- [Release v4.5.0-alpha.4](https://github.com/anza-xyz/agave/releases/tag/v4.5.0-alpha.4) - 2026-10-26
- [v4.5.0-alpha.3: Bump version to 4.5.0-alpha.3 (#16402)](https://github.com/anza-xyz/agave/releases/tag/v4.5.0-alpha.3) - 2026-10-26
- [Release v4.4.0-rc.1](https://github.com/anza-xyz/agave/releases/tag/v4.4.0-rc.1) - 2026-10-27

**Firedancer Releases**

- [Firedancer Mainnet Release v26.10.5](https://github.com/firedancer-io/firedancer/releases/tag/v26.10.5) - 2026-10-27
- [Firedancer Mainnet Release v26.10.4](https://github.com/firedancer-io/firedancer/releases/tag/v26.10.4) - 2026-10-21
- [Firedancer Mainnet Release v26.10.3](https://github.com/firedancer-io/firedancer/releases/tag/v26.10.3) - 2026-10-20

**SIMD Activity**

- [Amend SIMD-0607: Derive per-slot decay and increase intermediate prec…](https://github.com/solana-foundation/solana-improvement-documents/commit/2934dbeb1c8a7dfecc4f70a93a6b152e525b1698) - 2026-10-28
- [SIMD-0690: Hash validation in program migrations and upgrades (#690)](https://github.com/solana-foundation/solana-improvement-documents/commit/eac20f2994dd064482d96f178a4bbc0f4e358fd0) - 2026-10-26
- [SIMD-0670: ABIv1 invoke signed v2 syscall (#670)](https://github.com/solana-foundation/solana-improvement-documents/commit/c9ec366af14dd32a74259f5d9f5772249188bd25) - 2026-10-24

## Data Sources

| Source | Status | Fetched |
|---|---|---|
| network | ok | 2026-10-28T17:22:16Z |
| validators | ok | 2026-10-28T17:22:26Z |
| supply | ok | 2026-10-28T17:22:27Z |
| defillama | ok | 2026-10-28T17:22:16Z |
| price | ok | 2026-10-28T17:22:14Z |
| news | ok | 2026-10-28T17:22:20Z |
| solana_com | failed: HTTP 429 (https://solana.com/data) | 2026-10-28T17:22:18Z |
| dune | off (optional) | 2026-10-28T17:22:14Z |

_On-chain data served by `https://api.mainnet-beta.solana.com`._
