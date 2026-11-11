# Solana Ecosystem Report

> Generated 2026-11-11T21:38:32Z - heliostat 0.1.0 - 6/8 sources ok - refreshes every 15 min

## Anomalies

- 🟡 **WARNING**: true TPS is 2.7 standard deviations above its recent mean (2,754 vs 1,652)
- 🟡 **WARNING**: data source 'solana_com' failed this run

**Recently seen**

- 2026-11-11T00:26Z data source 'solana_com' failed this run
- 2026-11-11T06:52Z data source 'solana_com' failed this run
- 2026-11-11T14:47Z data source 'solana_com' failed this run
- 2026-11-11T21:38Z true TPS is 2.7 standard deviations above its recent mean (2,754 vs 1,652)
- 2026-11-11T21:38Z data source 'solana_com' failed this run

## Network

| Metric | Value |
|---|---|
| Health | healthy |
| True TPS (non-vote) | 2,754 |
| Total TPS (incl. votes) | 2,754 |
| Peak true TPS (30 min) | 3,364 |
| Mean slot time | 0.216 s |
| Slot | 468,276,871 |
| Block height | 446,292,985 |
| Epoch | 1083 - 97.42% complete, ~0.7 h remaining |

## Validators

| Metric | Value |
|---|---|
| Active validators | 659 |
| Delinquent | 40 (0.22% of stake) |
| Consensus stall buffer | 0.7% of the 33.3% halt threshold consumed |
| Total stake | 433,423,964 SOL |
| Nakamoto coefficient | 18 |
| Top-10 stake share | 24.6% |
| Top-20 stake share | 36.1% |
| Client stake split | agave 99.2% / firedancer 0.8% |
| Stake-weighted commission | 25.83% |

**Top validators by stake**

| # | Vote account | Stake | Share | Commission |
|---|---|---|---|---|
| 1 | `he1i..uBtk` | 16,764,485 SOL | 3.88% | 0% |
| 2 | `CcaH..oTN1` | 16,564,685 SOL | 3.83% | 7% |
| 3 | `3N7s..iD5g` | 13,031,625 SOL | 3.01% | 0% |
| 4 | `8Gbw..F8iD` | 10,117,254 SOL | 2.34% | 0% |
| 5 | `51JB..UNAm` | 9,644,051 SOL | 2.23% | 10% |
| 6 | `Catz..Diqb` | 9,571,015 SOL | 2.21% | 5% |
| 7 | `26pV..3dJx` | 9,231,999 SOL | 2.13% | 7% |
| 8 | `9QU2..29mF` | 7,814,330 SOL | 1.81% | 7% |
| 9 | `Dumi..Zk4a` | 6,987,248 SOL | 1.62% | 0% |
| 10 | `CvSb..wycB` | 6,729,845 SOL | 1.56% | 5% |

## Economy

| Metric | Value |
|---|---|
| SOL price | $84.76 (+1.7% 24h, -10.1% 7d) |
| Price sources | cross-checked, 0.079% apart |
| Market cap | $50.13B |
| TVL | $5.09B (+0.8% 24h) |
| Stablecoin supply | $13.89B |
| DEX volume (24h) | $1.34B |
| REV (24h) | $565.0K (network fees $444.5K + Jito tips $120.5K) |
| App fees (24h) | $8.41M |
| Median fee (user txs) | – lamports |
| Circulating supply | 591,401,603 SOL |

## Ecosystem Growth

| Metric | Value |
|---|---|
| Tokenized assets (RWA) on Solana | $582.31M across 13 protocols |
| Daily active addresses | available via optional DUNE_API_KEY |

**Largest tokenized-asset protocols**

- OnRe: $309.24M
- Huma: $225.83M
- Plume Vaults: $36.89M
- Mansory: $2.43M
- International Stable Currency: $2.42M

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

- [Firedancer Testnet Release v26.11.0](https://github.com/firedancer-io/firedancer/releases/tag/v26.11.0) - 2026-11-11
- [Firedancer Mainnet Release v26.10.8](https://github.com/firedancer-io/firedancer/releases/tag/v26.10.8) - 2026-11-11
- [v26.10.7](https://github.com/firedancer-io/firedancer/releases/tag/v26.10.7) - 2026-11-11

**SIMD Activity**

- [SIMD-0701: Vote Account v5 (#701)](https://github.com/solana-foundation/solana-improvement-documents/commit/ae7b00f3287a614c5aa5d0a7ceb7bad0cdc4e022) - 2026-11-06
- [SIMD-0602: Disallow Nonce Account as Program ID (#602)](https://github.com/solana-foundation/solana-improvement-documents/commit/809a97a0b0e0f2190fa5d494bcc5856a06907969) - 2026-11-06
- [SIMD-0685: Loader V3: Remove ExtendProgram (#685)](https://github.com/solana-foundation/solana-improvement-documents/commit/540f6ab4b9b71b584eae4f00c156194308d6650e) - 2026-11-02

## Data Sources

| Source | Status | Fetched |
|---|---|---|
| network | ok | 2026-11-11T21:38:22Z |
| validators | ok | 2026-11-11T21:38:30Z |
| supply | ok | 2026-11-11T21:38:32Z |
| defillama | ok | 2026-11-11T21:38:23Z |
| price | ok | 2026-11-11T21:38:20Z |
| news | ok | 2026-11-11T21:38:26Z |
| solana_com | failed: HTTP 429 (https://solana.com/data) | 2026-11-11T21:38:24Z |
| dune | off (optional) | 2026-11-11T21:38:20Z |

_On-chain data served by `https://api.mainnet-beta.solana.com`._
