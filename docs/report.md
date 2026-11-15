# Solana Ecosystem Report

> Generated 2026-11-15T01:08:55Z - heliostat 0.1.0 - 6/8 sources ok - refreshes every 15 min

## Anomalies

- 🟡 **WARNING**: TVL is 3.2 standard deviations below its recent mean (4.61B vs 5.01B)
- 🟡 **WARNING**: SOL price is 2.6 standard deviations below its recent mean (69.29 vs 82.67)
- 🟡 **WARNING**: price sources diverge by 1.078% (CoinGecko vs Jupiter)
- 🟡 **WARNING**: data source 'solana_com' failed this run

**Recently seen**

- 2026-11-14T21:25Z data source 'solana_com' failed this run
- 2026-11-15T01:08Z TVL is 3.2 standard deviations below its recent mean (4.61B vs 5.01B)
- 2026-11-15T01:08Z SOL price is 2.6 standard deviations below its recent mean (69.29 vs 82.67)
- 2026-11-15T01:08Z price sources diverge by 1.078% (CoinGecko vs Jupiter)
- 2026-11-15T01:08Z data source 'solana_com' failed this run

## Network

| Metric | Value |
|---|---|
| Health | healthy |
| True TPS (non-vote) | 2,013 |
| Total TPS (incl. votes) | 2,013 |
| Peak true TPS (30 min) | 3,021 |
| Mean slot time | 0.215 s |
| Slot | 469,539,823 |
| Block height | 447,554,869 |
| Epoch | 1086 - 89.77% complete, ~2.6 h remaining |

## Validators

| Metric | Value |
|---|---|
| Active validators | 662 |
| Delinquent | 37 (0.09% of stake) |
| Consensus stall buffer | 0.3% of the 33.3% halt threshold consumed |
| Total stake | 429,651,631 SOL |
| Nakamoto coefficient | 18 |
| Top-10 stake share | 24.7% |
| Top-20 stake share | 35.9% |
| Client stake split | agave 99.1% / firedancer 0.8% / unknown 0.0% |
| Stake-weighted commission | 25.91% |

**Top validators by stake**

| # | Vote account | Stake | Share | Commission |
|---|---|---|---|---|
| 1 | `he1i..uBtk` | 16,955,905 SOL | 3.95% | 0% |
| 2 | `CcaH..oTN1` | 16,374,909 SOL | 3.81% | 7% |
| 3 | `3N7s..iD5g` | 12,611,498 SOL | 2.94% | 0% |
| 4 | `8Gbw..F8iD` | 10,140,468 SOL | 2.36% | 0% |
| 5 | `51JB..UNAm` | 9,736,890 SOL | 2.27% | 10% |
| 6 | `Catz..Diqb` | 9,574,439 SOL | 2.23% | 5% |
| 7 | `26pV..3dJx` | 9,199,377 SOL | 2.14% | 7% |
| 8 | `9QU2..29mF` | 7,914,792 SOL | 1.84% | 7% |
| 9 | `Dumi..Zk4a` | 6,990,062 SOL | 1.63% | 0% |
| 10 | `CvSb..wycB` | 6,707,745 SOL | 1.56% | 5% |

## Economy

| Metric | Value |
|---|---|
| SOL price | $69.29 (-10.5% 24h, -22.5% 7d) |
| Price sources | DIVERGING 1.08% |
| Market cap | $40.99B |
| TVL | $4.61B (-0.0% 24h) |
| Stablecoin supply | $13.96B |
| DEX volume (24h) | $1.59B |
| REV (24h) | $555.5K (network fees $448.8K + Jito tips $106.7K) |
| App fees (24h) | $8.65M |
| Median fee (user txs) | – lamports |
| Circulating supply | 591,573,599 SOL |

## Ecosystem Growth

| Metric | Value |
|---|---|
| Tokenized assets (RWA) on Solana | $592.25M across 13 protocols |
| Daily active addresses | available via optional DUNE_API_KEY |

**Largest tokenized-asset protocols**

- OnRe: $305.45M
- Huma: $239.05M
- Plume Vaults: $37.02M
- International Stable Currency: $2.43M
- Mansory: $2.26M

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
| network | ok | 2026-11-15T01:08:54Z |
| validators | ok | 2026-11-15T01:08:55Z |
| supply | ok | 2026-11-15T01:08:53Z |
| defillama | ok | 2026-11-15T01:08:44Z |
| price | ok | 2026-11-15T01:08:43Z |
| news | ok | 2026-11-15T01:08:48Z |
| solana_com | failed: HTTP 429 (https://solana.com/data) | 2026-11-15T01:08:47Z |
| dune | off (optional) | 2026-11-15T01:08:43Z |

_On-chain data served by `https://api.mainnet-beta.solana.com`._
