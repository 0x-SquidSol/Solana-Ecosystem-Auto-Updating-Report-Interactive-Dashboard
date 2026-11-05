# Solana Ecosystem Report

> Generated 2026-11-05T10:12:13Z - heliostat 0.1.0 - 6/8 sources ok - refreshes every 15 min

## Anomalies

- 🟡 **WARNING**: data source 'solana_com' failed this run

**Recently seen**

- 2026-11-04T09:32Z data source 'solana_com' failed this run
- 2026-11-04T17:30Z data source 'solana_com' failed this run
- 2026-11-04T22:46Z data source 'solana_com' failed this run
- 2026-11-05T02:57Z data source 'solana_com' failed this run
- 2026-11-05T10:12Z data source 'solana_com' failed this run

## Network

| Metric | Value |
|---|---|
| Health | healthy |
| True TPS (non-vote) | 1,252 |
| Total TPS (incl. votes) | 1,252 |
| Peak true TPS (30 min) | 1,505 |
| Mean slot time | 0.213 s |
| Slot | 465,667,062 |
| Block height | 443,687,258 |
| Epoch | 1077 - 93.30% complete, ~1.7 h remaining |

## Validators

| Metric | Value |
|---|---|
| Active validators | 660 |
| Delinquent | 33 (0.51% of stake) |
| Consensus stall buffer | 1.5% of the 33.3% halt threshold consumed |
| Total stake | 433,017,789 SOL |
| Nakamoto coefficient | 17 |
| Top-10 stake share | 24.9% |
| Top-20 stake share | 36.3% |
| Client stake split | agave 96.5% / firedancer 0.4% / unknown 3.0% |
| Stake-weighted commission | 26.96% |

**Top validators by stake**

| # | Vote account | Stake | Share | Commission |
|---|---|---|---|---|
| 1 | `CcaH..oTN1` | 17,036,631 SOL | 3.95% | 7% |
| 2 | `he1i..uBtk` | 16,710,689 SOL | 3.88% | 0% |
| 3 | `3N7s..iD5g` | 13,012,272 SOL | 3.02% | 0% |
| 4 | `8Gbw..F8iD` | 10,433,406 SOL | 2.42% | 0% |
| 5 | `Catz..Diqb` | 9,524,736 SOL | 2.21% | 5% |
| 6 | `51JB..UNAm` | 9,439,186 SOL | 2.19% | 10% |
| 7 | `26pV..3dJx` | 9,217,930 SOL | 2.14% | 7% |
| 8 | `9QU2..29mF` | 7,826,697 SOL | 1.82% | 7% |
| 9 | `Dumi..Zk4a` | 6,981,457 SOL | 1.62% | 0% |
| 10 | `CvSb..wycB` | 6,980,105 SOL | 1.62% | 5% |

## Economy

| Metric | Value |
|---|---|
| SOL price | $96.81 (+4.0% 24h, -3.3% 7d) |
| Price sources | cross-checked, 0.030% apart |
| Market cap | $57.13B |
| TVL | $5.54B (+3.0% 24h) |
| Stablecoin supply | $14.88B |
| DEX volume (24h) | $2.22B |
| REV (24h) | $719.7K (network fees $579.8K + Jito tips $140.0K) |
| App fees (24h) | $10.83M |
| Median fee (user txs) | – lamports |
| Circulating supply | 590,262,012 SOL |

## Ecosystem Growth

| Metric | Value |
|---|---|
| Tokenized assets (RWA) on Solana | $566.71M across 13 protocols |
| Daily active addresses | available via optional DUNE_API_KEY |

**Largest tokenized-asset protocols**

- OnRe: $307.63M
- Huma: $212.70M
- Plume Vaults: $35.98M
- Mansory: $2.57M
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

- [SIMD-0685: Loader V3: Remove ExtendProgram (#685)](https://github.com/solana-foundation/solana-improvement-documents/commit/540f6ab4b9b71b584eae4f00c156194308d6650e) - 2026-11-02
- [rekey simd-0529 big int mod exp (#715)](https://github.com/solana-foundation/solana-improvement-documents/commit/0434aab3b2c6b596f607194bee44e94088ff2591) - 2026-11-01
- [SIMD-0567: CU-optimized ATA Program (`p-ATA`) (#567)](https://github.com/solana-foundation/solana-improvement-documents/commit/93cdf03a368a8bb2743a7f8d458a4cd36d2a904f) - 2026-11-01

## Data Sources

| Source | Status | Fetched |
|---|---|---|
| network | ok | 2026-11-05T10:12:03Z |
| validators | ok | 2026-11-05T10:12:12Z |
| supply | ok | 2026-11-05T10:12:13Z |
| defillama | ok | 2026-11-05T10:12:02Z |
| price | ok | 2026-11-05T10:12:01Z |
| news | ok | 2026-11-05T10:12:07Z |
| solana_com | failed: HTTP 429 (https://solana.com/data) | 2026-11-05T10:12:05Z |
| dune | off (optional) | 2026-11-05T10:12:01Z |

_On-chain data served by `https://api.mainnet-beta.solana.com`._
