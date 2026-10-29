# Solana Ecosystem Report

> Generated 2026-10-29T23:42:11Z - heliostat 0.1.0 - 6/8 sources ok - refreshes every 15 min

## Anomalies

- 🔴 **ALERT**: SOL price is 3.7 standard deviations below its recent mean (96.18 vs 101.968)
- 🟡 **WARNING**: data source 'solana_com' failed this run

**Recently seen**

- 2026-10-29T14:31Z data source 'solana_com' failed this run
- 2026-10-29T19:50Z slot time is 3.0 standard deviations above its recent mean (0.215 vs 0.212386)
- 2026-10-29T19:50Z data source 'solana_com' failed this run
- 2026-10-29T23:42Z SOL price is 3.7 standard deviations below its recent mean (96.18 vs 101.968)
- 2026-10-29T23:42Z data source 'solana_com' failed this run

## Network

| Metric | Value |
|---|---|
| Health | healthy |
| True TPS (non-vote) | 2,102 |
| Total TPS (incl. votes) | 2,102 |
| Peak true TPS (30 min) | 3,228 |
| Mean slot time | 0.214 s |
| Slot | 463,069,803 |
| Block height | 441,092,973 |
| Epoch | 1071 - 92.08% complete, ~2.0 h remaining |

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
| Client stake split | agave 99.8% / firedancer 0.1% / unknown 0.1% |
| Stake-weighted commission | 26.92% |

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
| SOL price | $96.18 (-6.0% 24h, -6.5% 7d) |
| Price sources | cross-checked, 0.100% apart |
| Market cap | $56.74B |
| TVL | $5.55B (-2.6% 24h) |
| Stablecoin supply | $15.16B |
| DEX volume (24h) | $1.73B |
| REV (24h) | $673.1K (network fees $527.1K + Jito tips $145.9K) |
| App fees (24h) | $10.35M |
| Median fee (user txs) | – lamports |
| Circulating supply | 589,983,547 SOL |

## Ecosystem Growth

| Metric | Value |
|---|---|
| Tokenized assets (RWA) on Solana | $596.44M across 13 protocols |
| Daily active addresses | available via optional DUNE_API_KEY |

**Largest tokenized-asset protocols**

- OnRe: $304.10M
- Huma: $246.31M
- Plume Vaults: $35.56M
- Mansory: $2.59M
- International Stable Currency: $2.41M

## News & Upgrades


**Solana Status**

- [mb-020624](https://status.solana.com/incidents/n5kcgs8dl9pj) - 2024-02-06
- [Cluster Instability](https://status.solana.com/incidents/ymr0gyj9xqyz) - 2023-02-26
- [Public Endpoints and Explorer offline](https://status.solana.com/incidents/mf9plxrkjhnk) - 2023-01-08

**Agave Releases**

- [Release v4.4.0](https://github.com/anza-xyz/agave/releases/tag/v4.4.0) - 2026-10-29
- [Release v4.5.0-alpha.4](https://github.com/anza-xyz/agave/releases/tag/v4.5.0-alpha.4) - 2026-10-26
- [v4.5.0-alpha.3: Bump version to 4.5.0-alpha.3 (#16402)](https://github.com/anza-xyz/agave/releases/tag/v4.5.0-alpha.3) - 2026-10-26

**Firedancer Releases**

- [Firedancer Mainnet Release v26.10.5](https://github.com/firedancer-io/firedancer/releases/tag/v26.10.5) - 2026-10-27
- [Firedancer Mainnet Release v26.10.4](https://github.com/firedancer-io/firedancer/releases/tag/v26.10.4) - 2026-10-21
- [Firedancer Mainnet Release v26.10.3](https://github.com/firedancer-io/firedancer/releases/tag/v26.10.3) - 2026-10-20

**SIMD Activity**

- [docs: align SIMD-0550 with the integer inflation schedule (#704)](https://github.com/solana-foundation/solana-improvement-documents/commit/2be4cb0c0fd1025df8c037b19372f7346119b231) - 2026-10-29
- [Mark SIMDs as Activated (#710)](https://github.com/solana-foundation/solana-improvement-documents/commit/6cc17538e26601e65beca89bbfa761e755720956) - 2026-10-28
- [Amend SIMD-0607: Derive per-slot decay and increase intermediate prec…](https://github.com/solana-foundation/solana-improvement-documents/commit/2934dbeb1c8a7dfecc4f70a93a6b152e525b1698) - 2026-10-28

## Data Sources

| Source | Status | Fetched |
|---|---|---|
| network | ok | 2026-10-29T23:42:01Z |
| validators | ok | 2026-10-29T23:42:11Z |
| supply | ok | 2026-10-29T23:42:11Z |
| defillama | ok | 2026-10-29T23:42:01Z |
| price | ok | 2026-10-29T23:41:59Z |
| news | ok | 2026-10-29T23:42:05Z |
| solana_com | failed: HTTP 429 (https://solana.com/data) | 2026-10-29T23:42:03Z |
| dune | off (optional) | 2026-10-29T23:41:59Z |

_On-chain data served by `https://api.mainnet-beta.solana.com`._
