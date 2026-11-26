# Solana Ecosystem Report

> Generated 2026-11-26T05:52:14Z - heliostat 0.1.0 - 6/8 sources ok - refreshes every 15 min

## Anomalies

- 🟡 **WARNING**: data source 'solana_com' failed this run

**Recently seen**

- 2026-11-25T05:08Z data source 'solana_com' failed this run
- 2026-11-25T15:31Z data source 'solana_com' failed this run
- 2026-11-25T23:46Z delinquent stake is 3.8 standard deviations above its recent mean (0.06 vs 0.024)
- 2026-11-25T23:46Z data source 'solana_com' failed this run
- 2026-11-26T05:52Z data source 'solana_com' failed this run

## Network

| Metric | Value |
|---|---|
| Health | healthy |
| True TPS (non-vote) | 1,487 |
| Total TPS (incl. votes) | 1,487 |
| Peak true TPS (30 min) | 2,017 |
| Mean slot time | 0.215 s |
| Slot | 474,037,519 |
| Block height | 452,050,411 |
| Epoch | 1097 - 30.91% complete, ~17.8 h remaining |

## Validators

| Metric | Value |
|---|---|
| Active validators | 657 |
| Delinquent | 31 (0.03% of stake) |
| Consensus stall buffer | 0.1% of the 33.3% halt threshold consumed |
| Total stake | 423,675,927 SOL |
| Nakamoto coefficient | 18 |
| Top-10 stake share | 25.0% |
| Top-20 stake share | 36.1% |
| Client stake split | agave 99.3% / firedancer 0.7% |
| Stake-weighted commission | 26.21% |

**Top validators by stake**

| # | Vote account | Stake | Share | Commission |
|---|---|---|---|---|
| 1 | `he1i..uBtk` | 16,805,000 SOL | 3.97% | 0% |
| 2 | `CcaH..oTN1` | 15,814,431 SOL | 3.73% | 7% |
| 3 | `3N7s..iD5g` | 12,430,859 SOL | 2.93% | 0% |
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
| SOL price | $70.97 (+3.5% 24h, -4.2% 7d) |
| Price sources | cross-checked, 0.058% apart |
| Market cap | $42.03B |
| TVL | $4.59B (+1.5% 24h) |
| Stablecoin supply | $13.00B |
| DEX volume (24h) | $1.47B |
| REV (24h) | $523.3K (network fees $415.3K + Jito tips $107.9K) |
| App fees (24h) | $7.49M |
| Median fee (user txs) | – lamports |
| Circulating supply | 592,183,289 SOL |

## Ecosystem Growth

| Metric | Value |
|---|---|
| Tokenized assets (RWA) on Solana | $526.05M across 11 protocols |
| Daily active addresses | available via optional DUNE_API_KEY |

**Largest tokenized-asset protocols**

- OnRe: $290.02M
- Huma: $226.86M
- International Stable Currency: $2.37M
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

- [Withdraw SIMD-0506 (#738)](https://github.com/solana-foundation/solana-improvement-documents/commit/1536c3eceda1779de191453246f939e53d8d7c94) - 2026-11-26
- [100M CUs Pt2 (#698)](https://github.com/solana-foundation/solana-improvement-documents/commit/e4d2b0e1c035385a65a96b3875e5b92af5df868e) - 2026-11-25
- [SIMD-0706: Reject unknown syscalls and `sol_alloc_free_` (#706)](https://github.com/solana-foundation/solana-improvement-documents/commit/44a4406237de1597ce56c1d106161dda950cbc68) - 2026-11-23

## Data Sources

| Source | Status | Fetched |
|---|---|---|
| network | ok | 2026-11-26T05:52:04Z |
| validators | ok | 2026-11-26T05:52:13Z |
| supply | ok | 2026-11-26T05:52:14Z |
| defillama | ok | 2026-11-26T05:52:04Z |
| price | ok | 2026-11-26T05:52:02Z |
| news | ok | 2026-11-26T05:52:07Z |
| solana_com | failed: HTTP 429 (https://solana.com/data) | 2026-11-26T05:52:06Z |
| dune | off (optional) | 2026-11-26T05:52:01Z |

_On-chain data served by `https://api.mainnet-beta.solana.com`._
