# Reduced K17 structural census

## Verdict

The exhaustive read-only Rust pass completed in 24.088 seconds.  Exactly
`18,369,804 / 55,191,349` H-orbits (`33.28%`) admit the proved mixed
four-distinct-cycle Morse pivot.  The contraction would leave `36,821,545`
rows, only a `1.50x` support reduction, so it does **not** materially compress
the target for a broad follow-on closure or rank computation.

The input checkpoint was not changed and no pivot tail was emitted.

## Exact structural census

The balanced row is viewed as a 2-regular multigraph on the 24 site-colour
ports.  Its cycle partition records component sizes.  Its colour-content type
records, for each cycle, the triple `(number of colour-0, colour-1, colour-2
ports)`, with cycles unordered and the whole packet canonicalized under the
global `S3` colour action.

- input H-orbits: `55,191,349`;
- cycle partitions: `184`;
- global-S3 colour-content types: `6,800`;
- pivotable: `18,369,804`;
- unpivotable: `36,821,545`.

The exact failure split is:

- fewer than four cycles: `30,812,520`;
- at least four cycles but no physical perfect matching across four distinct
  cycles: `4,791,728`;
- eligible physical matchings exist, but every such word is pure:
  `1,217,297`.

| cycle count | H-orbits | pivotable | unpivotable |
|---:|---:|---:|---:|
| 1 | 1,324,640 | 0 | 1,324,640 |
| 2 | 11,255,816 | 0 | 11,255,816 |
| 3 | 18,232,064 | 0 | 18,232,064 |
| 4 | 14,719,350 | 9,350,365 | 5,368,985 |
| 5 | 6,951,582 | 6,345,346 | 606,236 |
| 6 | 2,183,337 | 2,149,956 | 33,381 |
| 7 | 449,584 | 449,163 | 421 |
| 8 | 67,808 | 67,806 | 2 |
| 9 | 6,641 | 6,641 | 0 |
| 10 | 513 | 513 | 0 |
| 11 | 14 | 14 | 0 |

Thus even the high-cycle boundary is not empty: 423 rows with seven or eight
cycles remain outside this Morse pivot.

## Coefficient denominators

The checkpoint coefficients use the frozen clearing factor `281,801,520`.
After reducing each H-orbit coefficient separately, the exact denominator
histogram is:

| denominator | H-orbits |
|---:|---:|
| 1 | 20,848,739 |
| 5 | 10,406,708 |
| 7 | 6,453,754 |
| 11 | 12,442,642 |
| 17 | 1,895,682 |
| 35 | 785,696 |
| 55 | 1,178,368 |
| 77 | 786,208 |
| 187 | 393,552 |

The total signed mass replays as `-12,732,235,776/7`, and total L1 mass as
`132,066,403,328/7`, matching the frozen K17 result.  Pivotable signed mass is
`-98,930,099,152/119`; its L1 mass is `44,768,563,398,128/6,545`.

## Scope and artifacts

The Morse criterion is source-faithful: deleting a mixed physical perfect
matching whose four edges lie on distinct cycles produces four paths, and each
different completion strictly lowers cycle count.  This pass counts only where
that pivot exists.  It does not construct source columns, emit K19+ tails,
compute closure, or prove any row outside the criterion irreducible.

- input checkpoint SHA-256:
  `c1f4184bba99f4440ea1dafe2da93a90dcea815b104052967dfd64647bea5c05`;
- census source SHA-256:
  `e1004802010a85fbfd2eb54a702c729098313cfc16f7ed17339b9e4d6466ffc0`;
- result byte SHA-256:
  `bc56c96a7c59bb4f1444b9b6238de72a55d39e9dd51eff4846885ab911d92a6b`;
- result logical SHA-256:
  `cc1a6ef8f3e4061a87b0b851c1f402e85be82b6b50f353ceca035f0e9bf0126c`.

The complete 184-partition and 6,800-content ledgers are stored in
`results_reduced_k17_census.json`.
