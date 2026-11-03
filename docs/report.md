# Solana Ecosystem Report

> Generated 2026-11-03T22:00:24Z - heliostat 0.1.0 - 6/8 sources ok - refreshes every 15 min

## Anomalies

- 🟡 **WARNING**: data source 'solana_com' failed this run

**Recently seen**

- 2026-11-02T19:52Z data source 'solana_com' failed this run
- 2026-11-03T01:54Z data source 'solana_com' failed this run
- 2026-11-03T08:47Z data source 'solana_com' failed this run
- 2026-11-03T16:42Z data source 'solana_com' failed this run
- 2026-11-03T22:00Z data source 'solana_com' failed this run

## Network

| Metric | Value |
|---|---|
| Health | healthy |
| True TPS (non-vote) | 2,184 |
| Total TPS (incl. votes) | 2,184 |
| Peak true TPS (30 min) | 2,687 |
| Mean slot time | 0.215 s |
| Slot | 465,058,793 |
| Block height | 443,079,418 |
| Epoch | 1076 - 52.50% complete, ~12.3 h remaining |

## Validators

| Metric | Value |
|---|---|
| Active validators | 666 |
| Delinquent | 27 (0.42% of stake) |
| Consensus stall buffer | 1.3% of the 33.3% halt threshold consumed |
| Total stake | 434,699,177 SOL |
| Nakamoto coefficient | 18 |
| Top-10 stake share | 24.8% |
| Top-20 stake share | 36.1% |
| Client stake split | agave 97.2% / firedancer 0.7% / unknown 2.2% |
| Stake-weighted commission | 26.92% |

**Top validators by stake**

| # | Vote account | Stake | Share | Commission |
|---|---|---|---|---|
| 1 | `CcaH..oTN1` | 17,030,641 SOL | 3.93% | 7% |
| 2 | `he1i..uBtk` | 16,704,340 SOL | 3.86% | 0% |
| 3 | `3N7s..iD5g` | 13,043,664 SOL | 3.01% | 0% |
| 4 | `8Gbw..F8iD` | 10,431,126 SOL | 2.41% | 0% |
| 5 | `Catz..Diqb` | 9,561,007 SOL | 2.21% | 5% |
| 6 | `51JB..UNAm` | 9,435,905 SOL | 2.18% | 10% |
| 7 | `26pV..3dJx` | 9,232,746 SOL | 2.13% | 7% |
| 8 | `9QU2..29mF` | 7,814,810 SOL | 1.81% | 7% |
| 9 | `Dumi..Zk4a` | 7,008,986 SOL | 1.62% | 0% |
| 10 | `CvSb..wycB` | 6,979,031 SOL | 1.61% | 5% |

## Economy

| Metric | Value |
|---|---|
| SOL price | $93.63 (+1.7% 24h, -7.2% 7d) |
| Price sources | cross-checked, 0.043% apart |
| Market cap | $55.27B |
| TVL | $5.43B (-0.5% 24h) |
| Stablecoin supply | $14.65B |
| DEX volume (24h) | $1.85B |
| REV (24h) | $605.6K (network fees $482.2K + Jito tips $123.4K) |
| App fees (24h) | $11.21M |
| Median fee (user txs) | – lamports |
| Circulating supply | 590,265,855 SOL |

## Ecosystem Growth

| Metric | Value |
|---|---|
| Tokenized assets (RWA) on Solana | $584.45M across 13 protocols |
| Daily active addresses | available via optional DUNE_API_KEY |

**Largest tokenized-asset protocols**

- OnRe: $307.43M
- Huma: $230.82M
- Plume Vaults: $35.93M
- Mansory: $2.53M
- International Stable Currency: $2.42M

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
| network | ok | 2026-11-03T22:00:14Z |
| validators | ok | 2026-11-03T22:00:22Z |
| supply | ok | 2026-11-03T22:00:24Z |
| defillama | ok | 2026-11-03T22:00:14Z |
| price | ok | 2026-11-03T22:00:21Z |
| news | ok | 2026-11-03T22:00:19Z |
| solana_com | failed: HTTP 429 (https://solana.com/data) | 2026-11-03T22:00:17Z |
| dune | off (optional) | 2026-11-03T22:00:12Z |

_On-chain data served by `https://api.mainnet-beta.solana.com`._
