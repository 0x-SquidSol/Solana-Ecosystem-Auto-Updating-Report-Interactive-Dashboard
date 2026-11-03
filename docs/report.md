# Solana Ecosystem Report

> Generated 2026-11-03T01:54:43Z - heliostat 0.1.0 - 6/8 sources ok - refreshes every 15 min

## Anomalies

- 🟡 **WARNING**: data source 'solana_com' failed this run

**Recently seen**

- 2026-11-01T23:13Z data source 'solana_com' failed this run
- 2026-11-02T02:29Z data source 'solana_com' failed this run
- 2026-11-02T09:47Z data source 'solana_com' failed this run
- 2026-11-02T19:52Z data source 'solana_com' failed this run
- 2026-11-03T01:54Z data source 'solana_com' failed this run

## Network

| Metric | Value |
|---|---|
| Health | healthy |
| True TPS (non-vote) | 1,570 |
| Total TPS (incl. votes) | 1,570 |
| Peak true TPS (30 min) | 1,868 |
| Mean slot time | 0.214 s |
| Slot | 464,720,973 |
| Block height | 442,742,049 |
| Epoch | 1075 - 74.30% complete, ~6.6 h remaining |

## Validators

| Metric | Value |
|---|---|
| Active validators | 665 |
| Delinquent | 28 (1.01% of stake) |
| Consensus stall buffer | 3.0% of the 33.3% halt threshold consumed |
| Total stake | 434,160,766 SOL |
| Nakamoto coefficient | 17 |
| Top-10 stake share | 25.0% |
| Top-20 stake share | 36.3% |
| Client stake split | agave 97.1% / firedancer 0.7% / unknown 2.2% |
| Stake-weighted commission | 27.11% |

**Top validators by stake**

| # | Vote account | Stake | Share | Commission |
|---|---|---|---|---|
| 1 | `CcaH..oTN1` | 17,034,354 SOL | 3.96% | 7% |
| 2 | `he1i..uBtk` | 16,710,199 SOL | 3.89% | 0% |
| 3 | `3N7s..iD5g` | 13,037,180 SOL | 3.03% | 0% |
| 4 | `8Gbw..F8iD` | 10,429,501 SOL | 2.43% | 0% |
| 5 | `Catz..Diqb` | 9,580,109 SOL | 2.23% | 5% |
| 6 | `51JB..UNAm` | 9,453,055 SOL | 2.20% | 10% |
| 7 | `26pV..3dJx` | 9,226,805 SOL | 2.15% | 7% |
| 8 | `9QU2..29mF` | 7,803,392 SOL | 1.82% | 7% |
| 9 | `Dumi..Zk4a` | 7,001,891 SOL | 1.63% | 0% |
| 10 | `CvSb..wycB` | 6,978,080 SOL | 1.62% | 5% |

## Economy

| Metric | Value |
|---|---|
| SOL price | $92.41 (-2.6% 24h, -8.5% 7d) |
| Price sources | cross-checked, 0.069% apart |
| Market cap | $54.54B |
| TVL | $5.40B (-1.0% 24h) |
| Stablecoin supply | $15.22B |
| DEX volume (24h) | $1.40B |
| REV (24h) | $599.6K (network fees $482.2K + Jito tips $117.4K) |
| App fees (24h) | $10.69M |
| Median fee (user txs) | – lamports |
| Circulating supply | 590,206,288 SOL |

## Ecosystem Growth

| Metric | Value |
|---|---|
| Tokenized assets (RWA) on Solana | $597.77M across 13 protocols |
| Daily active addresses | available via optional DUNE_API_KEY |

**Largest tokenized-asset protocols**

- OnRe: $307.44M
- Huma: $244.38M
- Plume Vaults: $35.67M
- Mansory: $2.52M
- International Stable Currency: $2.44M

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
| network | ok | 2026-11-03T01:54:32Z |
| validators | ok | 2026-11-03T01:54:42Z |
| supply | ok | 2026-11-03T01:54:43Z |
| defillama | ok | 2026-11-03T01:54:32Z |
| price | ok | 2026-11-03T01:54:31Z |
| news | ok | 2026-11-03T01:54:36Z |
| solana_com | failed: HTTP 429 (https://solana.com/data) | 2026-11-03T01:54:35Z |
| dune | off (optional) | 2026-11-03T01:54:30Z |

_On-chain data served by `https://api.mainnet-beta.solana.com`._
