# Solana Ecosystem Report

> Generated 2026-11-12T02:30:16Z - heliostat 0.1.0 - 6/8 sources ok - refreshes every 15 min

## Anomalies

- 🟡 **WARNING**: data source 'solana_com' failed this run

**Recently seen**

- 2026-11-11T06:52Z data source 'solana_com' failed this run
- 2026-11-11T14:47Z data source 'solana_com' failed this run
- 2026-11-11T21:38Z true TPS is 2.7 standard deviations above its recent mean (2,754 vs 1,652)
- 2026-11-11T21:38Z data source 'solana_com' failed this run
- 2026-11-12T02:30Z data source 'solana_com' failed this run

## Network

| Metric | Value |
|---|---|
| Health | healthy |
| True TPS (non-vote) | 1,852 |
| Total TPS (incl. votes) | 1,852 |
| Peak true TPS (30 min) | 2,502 |
| Mean slot time | 0.215 s |
| Slot | 468,358,212 |
| Block height | 446,374,155 |
| Epoch | 1084 - 16.25% complete, ~21.6 h remaining |

## Validators

| Metric | Value |
|---|---|
| Active validators | 660 |
| Delinquent | 38 (0.60% of stake) |
| Consensus stall buffer | 1.8% of the 33.3% halt threshold consumed |
| Total stake | 433,416,361 SOL |
| Nakamoto coefficient | 17 |
| Top-10 stake share | 24.6% |
| Top-20 stake share | 36.2% |
| Client stake split | agave 99.6% / firedancer 0.4% |
| Stake-weighted commission | 25.83% |

**Top validators by stake**

| # | Vote account | Stake | Share | Commission |
|---|---|---|---|---|
| 1 | `he1i..uBtk` | 16,789,054 SOL | 3.90% | 0% |
| 2 | `CcaH..oTN1` | 16,119,194 SOL | 3.74% | 7% |
| 3 | `3N7s..iD5g` | 13,026,247 SOL | 3.02% | 0% |
| 4 | `8Gbw..F8iD` | 10,116,092 SOL | 2.35% | 0% |
| 5 | `51JB..UNAm` | 9,681,376 SOL | 2.25% | 10% |
| 6 | `Catz..Diqb` | 9,580,180 SOL | 2.22% | 5% |
| 7 | `26pV..3dJx` | 9,230,504 SOL | 2.14% | 7% |
| 8 | `9QU2..29mF` | 7,840,792 SOL | 1.82% | 7% |
| 9 | `Dumi..Zk4a` | 6,987,981 SOL | 1.62% | 0% |
| 10 | `CvSb..wycB` | 6,730,421 SOL | 1.56% | 5% |

## Economy

| Metric | Value |
|---|---|
| SOL price | $83.40 (+0.4% 24h, -13.3% 7d) |
| Price sources | cross-checked, 0.066% apart |
| Market cap | $49.33B |
| TVL | $5.03B (+0.1% 24h) |
| Stablecoin supply | $13.95B |
| DEX volume (24h) | $1.64B |
| REV (24h) | $633.8K (network fees $500.9K + Jito tips $132.9K) |
| App fees (24h) | $9.26M |
| Median fee (user txs) | – lamports |
| Circulating supply | 591,457,079 SOL |

## Ecosystem Growth

| Metric | Value |
|---|---|
| Tokenized assets (RWA) on Solana | $582.43M across 13 protocols |
| Daily active addresses | available via optional DUNE_API_KEY |

**Largest tokenized-asset protocols**

- OnRe: $309.39M
- Huma: $225.80M
- Plume Vaults: $36.90M
- International Stable Currency: $2.44M
- Mansory: $2.42M

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
| network | ok | 2026-11-12T02:30:04Z |
| validators | ok | 2026-11-12T02:30:15Z |
| supply | ok | 2026-11-12T02:30:16Z |
| defillama | ok | 2026-11-12T02:30:04Z |
| price | ok | 2026-11-12T02:30:07Z |
| news | ok | 2026-11-12T02:30:07Z |
| solana_com | failed: HTTP 429 (https://solana.com/data) | 2026-11-12T02:30:06Z |
| dune | off (optional) | 2026-11-12T02:30:02Z |

_On-chain data served by `https://api.mainnet-beta.solana.com`._
