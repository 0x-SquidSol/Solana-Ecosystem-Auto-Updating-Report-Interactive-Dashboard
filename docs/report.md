# Solana Ecosystem Report

> Generated 2026-11-25T23:46:44Z - heliostat 0.1.0 - 6/8 sources ok - refreshes every 15 min

## Anomalies

- 🔴 **ALERT**: delinquent stake is 3.8 standard deviations above its recent mean (0.06 vs 0.024)
- 🟡 **WARNING**: data source 'solana_com' failed this run

**Recently seen**

- 2026-11-24T22:50Z data source 'solana_com' failed this run
- 2026-11-25T05:08Z data source 'solana_com' failed this run
- 2026-11-25T15:31Z data source 'solana_com' failed this run
- 2026-11-25T23:46Z delinquent stake is 3.8 standard deviations above its recent mean (0.06 vs 0.024)
- 2026-11-25T23:46Z data source 'solana_com' failed this run

## Network

| Metric | Value |
|---|---|
| Health | healthy |
| True TPS (non-vote) | 1,482 |
| Total TPS (incl. votes) | 1,482 |
| Peak true TPS (30 min) | 1,841 |
| Mean slot time | 0.215 s |
| Slot | 473,935,520 |
| Block height | 451,948,453 |
| Epoch | 1097 - 7.30% complete, ~23.9 h remaining |

## Validators

| Metric | Value |
|---|---|
| Active validators | 655 |
| Delinquent | 33 (0.06% of stake) |
| Consensus stall buffer | 0.2% of the 33.3% halt threshold consumed |
| Total stake | 423,675,927 SOL |
| Nakamoto coefficient | 18 |
| Top-10 stake share | 25.0% |
| Top-20 stake share | 36.2% |
| Client stake split | agave 99.3% / firedancer 0.7% |
| Stake-weighted commission | 26.22% |

**Top validators by stake**

| # | Vote account | Stake | Share | Commission |
|---|---|---|---|---|
| 1 | `he1i..uBtk` | 16,805,000 SOL | 3.97% | 0% |
| 2 | `CcaH..oTN1` | 15,814,431 SOL | 3.73% | 7% |
| 3 | `3N7s..iD5g` | 12,430,859 SOL | 2.94% | 0% |
| 4 | `8Gbw..F8iD` | 10,236,589 SOL | 2.42% | 0% |
| 5 | `51JB..UNAm` | 9,910,258 SOL | 2.34% | 10% |
| 6 | `Catz..Diqb` | 9,615,394 SOL | 2.27% | 5% |
| 7 | `26pV..3dJx` | 9,281,563 SOL | 2.19% | 7% |
| 8 | `9QU2..29mF` | 8,032,075 SOL | 1.90% | 7% |
| 9 | `Dumi..Zk4a` | 6,971,305 SOL | 1.65% | 0% |
| 10 | `CvSb..wycB` | 6,740,287 SOL | 1.59% | 5% |

## Economy

| Metric | Value |
|---|---|
| SOL price | $70.41 (+0.9% 24h, -3.3% 7d) |
| Price sources | cross-checked, 0.153% apart |
| Market cap | $41.69B |
| TVL | $4.56B (-1.6% 24h) |
| Stablecoin supply | $12.92B |
| DEX volume (24h) | $1.46B |
| REV (24h) | $472.1K (network fees $366.0K + Jito tips $106.1K) |
| App fees (24h) | $7.15M |
| Median fee (user txs) | – lamports |
| Circulating supply | 592,183,384 SOL |

## Ecosystem Growth

| Metric | Value |
|---|---|
| Tokenized assets (RWA) on Solana | $525.96M across 11 protocols |
| Daily active addresses | available via optional DUNE_API_KEY |

**Largest tokenized-asset protocols**

- OnRe: $289.88M
- Huma: $226.88M
- International Stable Currency: $2.41M
- Mansory: $2.27M
- Exceed Finance exUSDC: $1.89M

## News & Upgrades


**Solana Status**

- [mb-020624](https://status.solana.com/incidents/n5kcgs8dl9pj) - 2024-02-06
- [Cluster Instability](https://status.solana.com/incidents/ymr0gyj9xqyz) - 2023-02-26
- [Public Endpoints and Explorer offline](https://status.solana.com/incidents/mf9plxrkjhnk) - 2023-01-08

**Agave Releases**

- [Release v4.5.0-rc.0](https://github.com/anza-xyz/agave/releases/tag/v4.5.0-rc.0) - 2026-11-25
- [Release v5.0.0-alpha.1](https://github.com/anza-xyz/agave/releases/tag/v5.0.0-alpha.1) - 2026-11-19
- [Release v4.5.0-beta.0](https://github.com/anza-xyz/agave/releases/tag/v4.5.0-beta.0) - 2026-11-06

**Firedancer Releases**

- [Firedancer Mainnet Release v26.11.1](https://github.com/firedancer-io/firedancer/releases/tag/v26.11.1) - 2026-11-25
- [Firedancer Testnet Release v26.11.0](https://github.com/firedancer-io/firedancer/releases/tag/v26.11.0) - 2026-11-11
- [Firedancer Mainnet Release v26.10.8](https://github.com/firedancer-io/firedancer/releases/tag/v26.10.8) - 2026-11-11

**SIMD Activity**

- [100M CUs Pt2 (#698)](https://github.com/solana-foundation/solana-improvement-documents/commit/e4d2b0e1c035385a65a96b3875e5b92af5df868e) - 2026-11-25
- [SIMD-0706: Reject unknown syscalls and `sol_alloc_free_` (#706)](https://github.com/solana-foundation/solana-improvement-documents/commit/44a4406237de1597ce56c1d106161dda950cbc68) - 2026-11-23
- [Amend 0529: charge a flat cu first before execution (#707)](https://github.com/solana-foundation/solana-improvement-documents/commit/6cf17cb7138d3fac03f5b637c1fde91a00fb48fc) - 2026-11-20

## Data Sources

| Source | Status | Fetched |
|---|---|---|
| network | ok | 2026-11-25T23:46:34Z |
| validators | ok | 2026-11-25T23:46:43Z |
| supply | ok | 2026-11-25T23:46:44Z |
| defillama | ok | 2026-11-25T23:46:34Z |
| price | ok | 2026-11-25T23:46:32Z |
| news | ok | 2026-11-25T23:46:37Z |
| solana_com | failed: HTTP 429 (https://solana.com/data) | 2026-11-25T23:46:36Z |
| dune | off (optional) | 2026-11-25T23:46:32Z |

_On-chain data served by `https://api.mainnet-beta.solana.com`._
