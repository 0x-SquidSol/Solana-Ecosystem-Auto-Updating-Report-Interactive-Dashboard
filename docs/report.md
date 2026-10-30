# Solana Ecosystem Report

> Generated 2026-10-30T20:47:20Z - heliostat 0.1.0 - 6/8 sources ok - refreshes every 15 min

## Anomalies

- 🔴 **ALERT**: TVL is 3.7 standard deviations below its recent mean (5.28B vs 5.70B)
- 🟡 **WARNING**: SOL price is 2.9 standard deviations below its recent mean (95 vs 101.059)
- 🟡 **WARNING**: data source 'solana_com' failed this run

**Recently seen**

- 2026-10-30T16:12Z SOL price is 3.4 standard deviations below its recent mean (94.81 vs 101.208)
- 2026-10-30T16:12Z data source 'solana_com' failed this run
- 2026-10-30T20:47Z TVL is 3.7 standard deviations below its recent mean (5.28B vs 5.70B)
- 2026-10-30T20:47Z SOL price is 2.9 standard deviations below its recent mean (95 vs 101.059)
- 2026-10-30T20:47Z data source 'solana_com' failed this run

## Network

| Metric | Value |
|---|---|
| Health | healthy |
| True TPS (non-vote) | 1,812 |
| Total TPS (incl. votes) | 1,812 |
| Peak true TPS (30 min) | 2,300 |
| Mean slot time | 0.214 s |
| Slot | 463,424,949 |
| Block height | 441,447,275 |
| Epoch | 1072 - 74.30% complete, ~6.6 h remaining |

## Validators

| Metric | Value |
|---|---|
| Active validators | 666 |
| Delinquent | 25 (0.65% of stake) |
| Consensus stall buffer | 2.0% of the 33.3% halt threshold consumed |
| Total stake | 435,357,093 SOL |
| Nakamoto coefficient | 18 |
| Top-10 stake share | 24.8% |
| Top-20 stake share | 36.0% |
| Client stake split | agave 99.4% / firedancer 0.6% |
| Stake-weighted commission | 26.98% |

**Top validators by stake**

| # | Vote account | Stake | Share | Commission |
|---|---|---|---|---|
| 1 | `CcaH..oTN1` | 16,965,456 SOL | 3.92% | 7% |
| 2 | `he1i..uBtk` | 16,678,000 SOL | 3.86% | 0% |
| 3 | `3N7s..iD5g` | 12,919,680 SOL | 2.99% | 0% |
| 4 | `8Gbw..F8iD` | 10,502,229 SOL | 2.43% | 0% |
| 5 | `Catz..Diqb` | 9,659,910 SOL | 2.23% | 5% |
| 6 | `51JB..UNAm` | 9,473,552 SOL | 2.19% | 10% |
| 7 | `26pV..3dJx` | 9,222,406 SOL | 2.13% | 7% |
| 8 | `9QU2..29mF` | 7,780,140 SOL | 1.80% | 7% |
| 9 | `CvSb..wycB` | 7,045,150 SOL | 1.63% | 5% |
| 10 | `Dumi..Zk4a` | 7,001,506 SOL | 1.62% | 0% |

## Economy

| Metric | Value |
|---|---|
| SOL price | $95.00 (-1.5% 24h, -8.8% 7d) |
| Price sources | cross-checked, 0.128% apart |
| Market cap | $56.06B |
| TVL | $5.28B (-7.2% 24h) |
| Stablecoin supply | $15.20B |
| DEX volume (24h) | $2.30B |
| REV (24h) | $689.2K (network fees $564.5K + Jito tips $124.7K) |
| App fees (24h) | $12.33M |
| Median fee (user txs) | – lamports |
| Circulating supply | 590,039,718 SOL |

## Ecosystem Growth

| Metric | Value |
|---|---|
| Tokenized assets (RWA) on Solana | $615.44M across 13 protocols |
| Daily active addresses | available via optional DUNE_API_KEY |

**Largest tokenized-asset protocols**

- OnRe: $307.49M
- Huma: $262.49M
- Plume Vaults: $35.07M
- Mansory: $2.56M
- International Stable Currency: $2.40M

## News & Upgrades


**Solana Status**

- [mb-020624](https://status.solana.com/incidents/n5kcgs8dl9pj) - 2024-02-06
- [Cluster Instability](https://status.solana.com/incidents/ymr0gyj9xqyz) - 2023-02-26
- [Public Endpoints and Explorer offline](https://status.solana.com/incidents/mf9plxrkjhnk) - 2023-01-08

**Agave Releases**

- [Release v4.4.0](https://github.com/anza-xyz/agave/releases/tag/v4.4.0) - 2026-10-30
- [Release v4.5.0-alpha.4](https://github.com/anza-xyz/agave/releases/tag/v4.5.0-alpha.4) - 2026-10-26
- [v4.5.0-alpha.3: Bump version to 4.5.0-alpha.3 (#16402)](https://github.com/anza-xyz/agave/releases/tag/v4.5.0-alpha.3) - 2026-10-26

**Firedancer Releases**

- [Firedancer Mainnet Release v26.10.5](https://github.com/firedancer-io/firedancer/releases/tag/v26.10.5) - 2026-10-27
- [Firedancer Mainnet Release v26.10.4](https://github.com/firedancer-io/firedancer/releases/tag/v26.10.4) - 2026-10-21
- [Firedancer Mainnet Release v26.10.3](https://github.com/firedancer-io/firedancer/releases/tag/v26.10.3) - 2026-10-20

**SIMD Activity**

- [docs: align SIMD-0550 with the integer inflation schedule (#704)](https://github.com/solana-foundation/solana-improvement-documents/commit/2be4cb0c0fd1025df8c037b19372f7346119b231) - 2026-10-29
- [Mark SIMDs as Activated (#710)](https://github.com/solana-foundation/solana-improvement-documents/commit/6cc17538e26601e65beca89bbfa761e755720956) - 2026-10-28
- [Amend SIMD-0607: Derive per-slot decay and increase intermediate prec…](https://github.com/solana-foundation/solana-improvement-documents/commit/2934dbeb1c8a7dfecc4f70a93a6b152e525b1698) - 2026-10-28

## Data Sources

| Source | Status | Fetched |
|---|---|---|
| network | ok | 2026-10-30T20:47:17Z |
| validators | ok | 2026-10-30T20:47:19Z |
| supply | ok | 2026-10-30T20:47:20Z |
| defillama | ok | 2026-10-30T20:47:09Z |
| price | ok | 2026-10-30T20:47:08Z |
| news | ok | 2026-10-30T20:47:13Z |
| solana_com | failed: HTTP 429 (https://solana.com/data) | 2026-10-30T20:47:12Z |
| dune | off (optional) | 2026-10-30T20:47:07Z |

_On-chain data served by `https://api.mainnet-beta.solana.com`._
