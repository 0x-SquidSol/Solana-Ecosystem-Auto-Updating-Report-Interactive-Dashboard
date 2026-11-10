# Solana Ecosystem Report

> Generated 2026-11-10T19:59:34Z - heliostat 0.1.0 - 6/8 sources ok - refreshes every 15 min

## Anomalies

- 🔴 **ALERT**: delinquent stake is 5.5 standard deviations above its recent mean (1.34 vs 0.304)
- 🟡 **WARNING**: data source 'solana_com' failed this run

**Recently seen**

- 2026-11-09T22:15Z data source 'solana_com' failed this run
- 2026-11-10T04:12Z data source 'solana_com' failed this run
- 2026-11-10T12:36Z data source 'solana_com' failed this run
- 2026-11-10T19:59Z delinquent stake is 5.5 standard deviations above its recent mean (1.34 vs 0.304)
- 2026-11-10T19:59Z data source 'solana_com' failed this run

## Network

| Metric | Value |
|---|---|
| Health | healthy |
| True TPS (non-vote) | 1,938 |
| Total TPS (incl. votes) | 1,938 |
| Peak true TPS (30 min) | 2,518 |
| Mean slot time | 0.214 s |
| Slot | 467,846,722 |
| Block height | 445,863,911 |
| Epoch | 1082 - 97.85% complete, ~0.6 h remaining |

## Validators

| Metric | Value |
|---|---|
| Active validators | 655 |
| Delinquent | 43 (1.34% of stake) |
| Consensus stall buffer | 4.0% of the 33.3% halt threshold consumed |
| Total stake | 434,984,472 SOL |
| Nakamoto coefficient | 17 |
| Top-10 stake share | 24.9% |
| Top-20 stake share | 36.3% |
| Client stake split | agave 97.9% / firedancer 2.1% |
| Stake-weighted commission | 26.00% |

**Top validators by stake**

| # | Vote account | Stake | Share | Commission |
|---|---|---|---|---|
| 1 | `CcaH..oTN1` | 16,898,208 SOL | 3.94% | 7% |
| 2 | `he1i..uBtk` | 16,746,254 SOL | 3.90% | 0% |
| 3 | `3N7s..iD5g` | 13,034,244 SOL | 3.04% | 0% |
| 4 | `8Gbw..F8iD` | 10,280,950 SOL | 2.40% | 0% |
| 5 | `51JB..UNAm` | 9,598,549 SOL | 2.24% | 10% |
| 6 | `Catz..Diqb` | 9,553,851 SOL | 2.23% | 5% |
| 7 | `26pV..3dJx` | 9,233,159 SOL | 2.15% | 7% |
| 8 | `9QU2..29mF` | 7,813,316 SOL | 1.82% | 7% |
| 9 | `Dumi..Zk4a` | 6,987,971 SOL | 1.63% | 0% |
| 10 | `CvSb..wycB` | 6,712,231 SOL | 1.56% | 5% |

## Economy

| Metric | Value |
|---|---|
| SOL price | $82.83 (-4.2% 24h, -11.1% 7d) |
| Price sources | cross-checked, 0.025% apart |
| Market cap | $48.96B |
| TVL | $5.00B (-1.9% 24h) |
| Stablecoin supply | $14.65B |
| DEX volume (24h) | $1.49B |
| REV (24h) | $530.1K (network fees $408.0K + Jito tips $122.1K) |
| App fees (24h) | $9.38M |
| Median fee (user txs) | – lamports |
| Circulating supply | 591,148,922 SOL |

## Ecosystem Growth

| Metric | Value |
|---|---|
| Tokenized assets (RWA) on Solana | $582.05M across 13 protocols |
| Daily active addresses | available via optional DUNE_API_KEY |

**Largest tokenized-asset protocols**

- OnRe: $309.37M
- Huma: $225.57M
- Plume Vaults: $36.89M
- Mansory: $2.42M
- International Stable Currency: $2.40M

## News & Upgrades


**Solana Status**

- [mb-020624](https://status.solana.com/incidents/n5kcgs8dl9pj) - 2024-02-06
- [Cluster Instability](https://status.solana.com/incidents/ymr0gyj9xqyz) - 2023-02-26
- [Public Endpoints and Explorer offline](https://status.solana.com/incidents/mf9plxrkjhnk) - 2023-01-08

**Agave Releases**

- [Release v4.5.0-beta.0](https://github.com/anza-xyz/agave/releases/tag/v4.5.0-beta.0) - 2026-11-06
- [Release v4.4.1](https://github.com/anza-xyz/agave/releases/tag/v4.4.1) - 2026-11-05
- [Release v4.4.0](https://github.com/anza-xyz/agave/releases/tag/v4.4.0) - 2026-10-30

**Firedancer Releases**

- [Firedancer Mainnet Release v26.10.6](https://github.com/firedancer-io/firedancer/releases/tag/v26.10.6) - 2026-11-10
- [Firedancer Mainnet Release v26.10.5](https://github.com/firedancer-io/firedancer/releases/tag/v26.10.5) - 2026-10-27
- [Firedancer Mainnet Release v26.10.4](https://github.com/firedancer-io/firedancer/releases/tag/v26.10.4) - 2026-10-21

**SIMD Activity**

- [SIMD-0701: Vote Account v5 (#701)](https://github.com/solana-foundation/solana-improvement-documents/commit/ae7b00f3287a614c5aa5d0a7ceb7bad0cdc4e022) - 2026-11-06
- [SIMD-0602: Disallow Nonce Account as Program ID (#602)](https://github.com/solana-foundation/solana-improvement-documents/commit/809a97a0b0e0f2190fa5d494bcc5856a06907969) - 2026-11-06
- [SIMD-0685: Loader V3: Remove ExtendProgram (#685)](https://github.com/solana-foundation/solana-improvement-documents/commit/540f6ab4b9b71b584eae4f00c156194308d6650e) - 2026-11-02

## Data Sources

| Source | Status | Fetched |
|---|---|---|
| network | ok | 2026-11-10T19:59:24Z |
| validators | ok | 2026-11-10T19:59:33Z |
| supply | ok | 2026-11-10T19:59:34Z |
| defillama | ok | 2026-11-10T19:59:26Z |
| price | ok | 2026-11-10T19:59:23Z |
| news | ok | 2026-11-10T19:59:28Z |
| solana_com | failed: HTTP 429 (https://solana.com/data) | 2026-11-10T19:59:27Z |
| dune | off (optional) | 2026-11-10T19:59:22Z |

_On-chain data served by `https://api.mainnet-beta.solana.com`._
