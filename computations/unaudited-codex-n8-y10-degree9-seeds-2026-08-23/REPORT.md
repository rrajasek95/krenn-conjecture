# N8 chart-26: exact target standardness through degree 9

## Theorem

For the frozen normalized target

```text
C10 = 0111202020494f4f50f8 * t^2
```

and the frozen t-last order, `C10` is standard against every homogeneous
divisor of total degree at most 9.

This advances the exact degree-8 terminal.  It makes no degree-10 claim.

## Why only 160 new columns matter

Modulo `t*M8`, the only new degree-9 columns are normalized originals times
t-free quintic y-multipliers.  Exhaustive literal incidence with target
divisors gives:

| target slice | primitive columns | touched divisors | exchange pairs in seed top rows |
|---|---:|---:|---|
| `y^8*t` | 40 | 17 / 23 | `C4`: 453; decoration-only: 1,335 |
| `y^7*t^2` | 120 | 48 / 48 | `C4`: 2,118; `C6`: 332; decoration-only: 4,629 |
| `y^9` | 0 | 0 / 7 | none |

Every seed top row has exactly one cell incident to physical site 5.  Thus
all alternative source matchings reuse that decorated cell: physical `C8`
and `C4+C4` exchange are impossible.

## Target-rooted triangular certificate

Take all top `y^9` rows of the 160 primitive target-touching columns.  Add
every literal original/quintic factorization owner of those rows.  This is
the exact restriction of the full top Macaulay matrix to the seed-row set:

```text
1,689 columns x 9,976 rows.
```

Private-row peeling removes 945 columns, including **all 160 target seeds**.
The induced 744-column residue contains zero seeds.  Therefore any vector in
the kernel of the full degree-9 head has coefficient zero on every new
target-touching column: restricting a full relation to the seed rows gives
this exact matrix, and columns not enumerated have zero on those rows.

All remaining degree-9 columns have a positive multiplier t-exponent and lie
in `t*M8`.  Frozen exact degree-8 standardness excludes their lower target
pivots.  These two facts prove the theorem.

## First apparent core and why it is harmless

In the priority `y^8*t` slice, a restricted one-shell 2-by-2
decoration-only square appears:

```text
columns:
  (2327, 0105114fa7)
  (3785, 01051149a7)

rows:
  01051120494f91a7ec
  01051120494f9ba7e2
```

It lies entirely in the nonseed frontier, so it cannot carry a target
relation.  As a further guard, both columns have globally private outside
top rows; in fact all 744 frontier columns have such a row, and a bounded
second-shell augmentation peels the entire residue.  The first witness is

```text
(86, 1120204b4f) -> 111320204b4f5a7ef8.
```

This also shows why a physical-cycle-only statistic is insufficient:
decoration squares occur before a target obstruction, but the exact
source-labelled private row restores the descent.

## Provenance and scope

- Checker: `audit_degree9_seeds.py`.
- Logical digest:
  `fee70f071e6123712a6d060c5dd2aadc4f9e7c79efc082b660343fb77d1238de`.
- Degree-8 authority:
  `../unaudited-codex-n8-orbit26-direct-target-2026-08-23/results_y10_d8_staged_blocks.json`,
  raw logical digest
  `a4ca3979e466a18eeea2603382d6d86a61e4ccb6837a8be95b507361df9bb0e5`,
  current file SHA-256
  `f049bafcee14c588362aebd87c06653ebfbd4658196e750a5aa42fbb71dd6390`.

The exchange numbers are pair-incidence counts, not symmetry-orbit counts.
The second-shell guard is not used to prove standardness; the zero residual
seed count in the exact first-shell restriction is already decisive.
