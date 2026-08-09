# D1 maximal residue orbits: profile split and binary closure

The six-orbit census in
`computations/verify_n8_d1_residue_maximal_orbits.py` is now coefficient-
complete on five of its six maximal supports.  The independent checker

```text
computations/verify_n8_d1_residue_maximal_orbits_binary_closure.py
```

uses the projection-profile theorem of `eeae4b3` and five ordinary polynomial
identities.  It does not call Singular or trust a solver verdict.

## The uniform branch split

Fix a residue vertex and let the color-0 and color-1 zero-target slices give
two tripod relations.  Write `K` for their span.  In O1, O2, O3, O5 and O6,
the two non-target rows have the same nonempty support on every incident
block, and that support contains a non-target coordinate.

If `dim K=2`, every nonzero projection of `K` has rank 1 or 2.  A rank-1
projected line cannot be the target line, because one of its localized
non-target coordinates is nonzero.  The exact classification `eeae4b3` then
closes every profile:

| profile | necessary condition for a pure target companion | result here |
|---|---|---|
| 222 | no nonzero decomposable companion | impossible |
| 122 | the rank-1 image line is the target line | impossible |
| 112 | one of three pairs of rank-1 lines is target-aligned | impossible |
| 111 | at least two rank-1 lines are target-aligned | impossible |

Profiles containing zero are already incompatible with three nonzero
opposite blocks.  Thus the only remaining branch has `dim K=1` at every
residue vertex (dimension zero is excluded by a localized row entry).

In that branch the two non-target tripod rows are proportional.  Their common
support makes the four proportionality factors units.  For every edge `uv`,

```text
x_uv(1,j) = rho_u x_uv(0,j),
x_uv(i,1) = rho_v x_uv(i,0).
```

Consequently every ternary residue coefficient is a Laurent-unit multiple of
the coefficient obtained by identifying colors 0 and 1.  It is therefore
enough to solve the binary K4 system on colors `{0,2}`.

## Finite orbit table

The arrows record the target-line digraph of the maximal support.  In the
five closed rows these arrows never rescue a rank-1 projection: every
non-target kernel row still has a localized non-target coordinate.

| orbit | size | target-line arrows | `dim K=2` | `dim K=1` binary system | verdict |
|---|---:|---|---|---|---|
| O1 | 45 | 4→7, 5→6, 6→5, 7→6 | no alignment choice | 14 generators; `x4602*x5600*x6720` in the ideal | residue-empty |
| O2 | 46 | 4→6, 5→7, 6→5, 7→4 | no alignment choice | 16 generators; `x4602*x5600*x6720` in the ideal | residue-empty |
| O3 | 46 | 4→7, 7→4, 5→6, 6→5 | no alignment choice | 16 generators; `x4602*x5600*x6720` in the ideal | residue-empty |
| O5 | 44 | 4→7, 5→6, 6→7, 7→6 | no alignment choice | 12 generators; `x4702*x5702*x6700` in the ideal | residue-empty |
| O6 | 45 | 4→7, 5→6, 6→7, 7→5 | no alignment choice | 14 generators; `x4702*x5700*x6702` in the ideal | residue-empty |
| O4 | 34 | 4→7, 5→7, 6→7, 7→6 | target-aligned compression exists | checked 14-parameter residue family | externally coupled |

For each closed orbit the displayed cubic is a product of localized active
cells.  The checker reconstructs the binary fibre generators over `Z`,
multiplies them by the frozen lift coefficients, and obtains that cubic
coefficient-by-coefficient.  Hence the localized ideal is the unit ideal over
every field, including characteristics 2 and 3.

## What remains

O4 is not residue-empty.  Its exact 14-parameter family and rational point
were frozen in `07f800a`.  Four six-site pure-fibre factors close the full
support unless all of

```text
x02_20, x02_21, x13_20, x13_21
```

are omitted.  Thus the six maximal residue supports have reduced to one
honest external-coupling case: O4 together with those four boundary
omissions.  No cardinality-layer or heuristic Gröbner verdict remains in the
other five cases.

## Reproduction

Run both interpreter modes:

```bash
.venv/bin/python computations/verify_n8_d1_residue_maximal_orbits_binary_closure.py
.venv/bin/python -O computations/verify_n8_d1_residue_maximal_orbits_binary_closure.py
```

The checker freezes its complete ledger hash after the first validated run.
