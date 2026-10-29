# Solana Ecosystem Report

> Generated 2026-10-29T01:21:33Z - heliostat 0.1.0 - 6/8 sources ok - refreshes every 15 min

## Anomalies

- 🟡 **WARNING**: data source 'solana_com' failed this run

**Recently seen**

- 2026-10-28T17:22Z delinquent stake is 3.4 standard deviations above its recent mean (0.9 vs 0.156667)
- 2026-10-28T17:22Z data source 'solana_com' failed this run
- 2026-10-28T21:46Z delinquent stake is 2.9 standard deviations above its recent mean (0.89 vs 0.172826)
- 2026-10-28T21:46Z data source 'solana_com' failed this run
- 2026-10-29T01:21Z data source 'solana_com' failed this run

## Network

| Metric | Value |
|---|---|
| Health | healthy |
| True TPS (non-vote) | 1,630 |
| Total TPS (incl. votes) | 1,630 |
| Peak true TPS (30 min) | 2,231 |
| Mean slot time | 0.214 s |
| Slot | 462,693,708 |
| Block height | 440,717,477 |
| Epoch | 1071 - 5.03% complete, ~24.4 h remaining |

## Validators

| Metric | Value |
|---|---|
| Active validators | 666 |
| Delinquent | 23 (0.74% of stake) |
| Consensus stall buffer | 2.2% of the 33.3% halt threshold consumed |
| Total stake | 436,776,187 SOL |
| Nakamoto coefficient | 18 |
| Top-10 stake share | 24.7% |
| Top-20 stake share | 36.1% |
| Client stake split | agave 99.9% / firedancer 0.1% / unknown 0.1% |
| Stake-weighted commission | 26.91% |

**Top validators by stake**

| # | Vote account | Stake | Share | Commission |
|---|---|---|---|---|
| 1 | `CcaH..oTN1` | 17,028,574 SOL | 3.93% | 7% |
| 2 | `he1i..uBtk` | 16,665,444 SOL | 3.84% | 0% |
| 3 | `3N7s..iD5g` | 12,878,826 SOL | 2.97% | 0% |
| 4 | `8Gbw..F8iD` | 10,762,073 SOL | 2.48% | 0% |
| 5 | `Catz..Diqb` | 9,705,356 SOL | 2.24% | 5% |
| 6 | `51JB..UNAm` | 9,466,646 SOL | 2.18% | 10% |
| 7 | `26pV..3dJx` | 9,218,110 SOL | 2.13% | 7% |
| 8 | `9QU2..29mF` | 7,761,555 SOL | 1.79% | 7% |
| 9 | `Dumi..Zk4a` | 6,998,037 SOL | 1.61% | 0% |
| 10 | `CvSb..wycB` | 6,646,428 SOL | 1.53% | 5% |

## Economy

| Metric | Value |
|---|---|
| SOL price | $101.48 (+0.3% 24h, -4.8% 7d) |
| Price sources | cross-checked, 0.107% apart |
| Market cap | $59.87B |
| TVL | $5.72B (0.0% 24h) |
| Stablecoin supply | $15.41B |
| DEX volume (24h) | $1.63B |
| REV (24h) | $661.8K (network fees $527.1K + Jito tips $134.7K) |
| App fees (24h) | $10.46M |
| Median fee (user txs) | – lamports |
| Circulating supply | 589,984,073 SOL |

## Ecosystem Growth

| Metric | Value |
|---|---|
| Tokenized assets (RWA) on Solana | $605.18M across 13 protocols |
| Daily active addresses | available via optional DUNE_API_KEY |

**Largest tokenized-asset protocols**

- OnRe: $305.55M
- Huma: $254.05M
- Plume Vaults: $35.03M
- Mansory: $2.64M
- International Stable Currency: $2.41M

## News & Upgrades


**Solana Status**

- [mb-020624](https://status.solana.com/incidents/n5kcgs8dl9pj) - 2024-02-06
- [Cluster Instability](https://status.solana.com/incidents/ymr0gyj9xqyz) - 2023-02-26
- [Public Endpoints and Explorer offline](https://status.solana.com/incidents/mf9plxrkjhnk) - 2023-01-08

**Agave Releases**

- [Release v4.4.0](https://github.com/anza-xyz/agave/releases/tag/v4.4.0) - 2026-10-28
- [Release v4.5.0-alpha.4](https://github.com/anza-xyz/agave/releases/tag/v4.5.0-alpha.4) - 2026-10-26
- [v4.5.0-alpha.3: Bump version to 4.5.0-alpha.3 (#16402)](https://github.com/anza-xyz/agave/releases/tag/v4.5.0-alpha.3) - 2026-10-26

**Firedancer Releases**

- [Firedancer Mainnet Release v26.10.5](https://github.com/firedancer-io/firedancer/releases/tag/v26.10.5) - 2026-10-27
- [Firedancer Mainnet Release v26.10.4](https://github.com/firedancer-io/firedancer/releases/tag/v26.10.4) - 2026-10-21
- [Firedancer Mainnet Release v26.10.3](https://github.com/firedancer-io/firedancer/releases/tag/v26.10.3) - 2026-10-20

**SIMD Activity**

- [Mark SIMDs as Activated (#710)](https://github.com/solana-foundation/solana-improvement-documents/commit/6cc17538e26601e65beca89bbfa761e755720956) - 2026-10-28
- [Amend SIMD-0607: Derive per-slot decay and increase intermediate prec…](https://github.com/solana-foundation/solana-improvement-documents/commit/2934dbeb1c8a7dfecc4f70a93a6b152e525b1698) - 2026-10-28
- [SIMD-0690: Hash validation in program migrations and upgrades (#690)](https://github.com/solana-foundation/solana-improvement-documents/commit/eac20f2994dd064482d96f178a4bbc0f4e358fd0) - 2026-10-26

## Data Sources

| Source | Status | Fetched |
|---|---|---|
| network | ok | 2026-10-29T01:21:24Z |
| validators | ok | 2026-10-29T01:21:32Z |
| supply | ok | 2026-10-29T01:21:33Z |
| defillama | ok | 2026-10-29T01:21:23Z |
| price | ok | 2026-10-29T01:21:22Z |
| news | ok | 2026-10-29T01:21:27Z |
| solana_com | failed: HTTP 429 (https://solana.com/data) | 2026-10-29T01:21:26Z |
| dune | off (optional) | 2026-10-29T01:21:22Z |

_On-chain data served by `https://api.mainnet-beta.solana.com`._
