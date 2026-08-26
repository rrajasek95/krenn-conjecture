# Corrected complete K19 immediate cycle charge

## Terminal result

`PASS_COMPLETE_K19_PATH_CHARGE_ASSEMBLY`.  This package contains no new
symbolic or charge computation: it adds the frozen hidden `[2,3]` component to
the prior exact K19 page and checks the result against the complete recurrence
DAG.

The corrected unscaled K19 totals are:

- full charge: `-790166942706596608/57955975`;
- irreducible charge: `-2117855228554753792/173867925`.

The irreducible charge remains nonzero.

## Exact arithmetic

The prior valid 23-path subtotal was

- full: `-25935229532575232/2258025`;
- irreducible: `-14857399077330176/1436925`.

The recovered `D14:222|R:2-3` component contributes

- full: `-74697630822299392/34773585`;
- irreducible: `-45729991456828928/24838275`.

These fractions are added over Q.  The old page's `k16_k14_k3=0` entry only
described retained nonpivotable K16 rows; it is a superseded placeholder, not
an additional lineage beside the repaired component.

## 321-node DAG coverage

The authoritative DAG has 321 reachable nodes and exactly 24 required K19
lineages.  The assembled component partition is disjoint and exhaustive:

| component | K19 DAG paths |
|---|---:|
| direct K19 packets `344,434,443` | 3 |
| K15 direct packets followed by `4` | 3 |
| K16 direct packets followed by `3` | 6 |
| K17 direct packets followed by `2` | 7 |
| K14 path `[3,2]` | 1 |
| K15 paths `[2,2]` | 3 |
| repaired K14 path `[2,3]` | 1 |
| **total** | **24** |

The assembly checker compares literal lineage IDs, not just counts:
`covered == required`, with no missing, duplicate, or extra path.

## K20 partial record

The repaired `D14:222|R:2-4` component is recorded only as a partial K20
component:

- full: `2220664522778112/11591195`;
- irreducible: `1850432653709056/10227525`.

The DAG requires 36 K20 paths.  This package covers one named path and makes no
complete K20 total claim.

## Scope and digests

All values are immediate 77-cycle charges under the frozen deterministic pivot
policy.  This is not row collection, downstream reduction, termination, ideal
membership, or a proof of the conjecture.

Assembly source SHA-256:
`888ee6d487d30548a2e6060aadaadf1508e179458f6c69765db15ec5040c56ec`.
Result SHA-256:
`d976b0a943ae3e1565054814882b2b280223a8f50dd0364e8fa1a8b01d8e055d`.
Logical digest:
`63afad8c0df8c034c7ba0cbf0a46012c1db834f2ff7f12229cad734dcee1c40d`.
