# The sharp all-flat `r=4, G=4K2` equality stratum is empty

## Outcome

Let an eight-site exact ternary source be in the sharp reciprocal equality
stratum with

* four reciprocal selected witness pairs forming a perfect matching `M`;
* exactly two essential deleted-star incidences at every site;
* sixteen selected bad pairs, each essential at exactly one endpoint; and
* four selected rank-one pairs good at both endpoints, forming a perfect
  matching `G=4K2`.

If every transition between adjacent rank-one good pairs is flat, then no
such source exists.  The reason is already visible at support level: the
selected twenty-block chart cannot support all three nonzero pure GHZ
coefficients.

This finishes the whole sharp all-flat `r=4,4K2` branch, not merely the
single labelled orbit closed in
[`n8-r4-selected20-full-source-empty.md`](n8-r4-selected20-full-source-empty.md).
It does not close other `r=4` good-graph strata or the curved-overlap branch.

## 1. Why only the selected twenty blocks remain

The sixteen bad selected pairs consume all sixteen essential incidences,
one at exactly one endpoint.  Hence every unselected nonzero block would be
nonessential at both endpoints.  The equality flag theorem places its two
endpoint spaces on the two common nonessential lines, making it a rank-one
good pair.

Such a pair is adjacent to the selected good matching edge through either
endpoint.  Every physical block in this equality packet has rank at most
one.  But the exact flat-wedge theorem says a flat wedge of two rank-one good
arms has opposite chord rank at least two.  Thus any unselected nonzero block
would produce a curved good overlap.  In the all-flat branch every
unselected block is zero, leaving exactly the twenty selected blocks.

## 2. The Boolean relaxation

The checker retains precisely the data needed by a pure matching term and
relaxes everything else.

For every physical pair `uv` it records:

* whether `uv` belongs to the reciprocal matching `M` or good matching `G`;
* the selected arc directions `u->v` and `v->u`;
* the unique target colour carried by every selected arc;
* which endpoint, if any, is deletion-essential; and
* whether the common nonessential endpoint line is a target axis or is
  treated as fully generic.

Every site has three outgoing arcs, one in each colour.  `M` and `G` are
disjoint perfect matchings.  A reciprocal pair has both orientations and a
nonreciprocal selected pair exactly one.  Consequently 24 arcs with four
reciprocal pairs occupy exactly twenty physical blocks.  `G` consists
exactly of the selected pairs nonessential at both endpoints; every other
selected pair is essential at exactly one endpoint, with two essential
incidences at each site.

If a selected arc `u->v` has colour `c`, its rank-one head factor at `v` is
the literal target axis `e_c`.  If that endpoint is nonessential, the common
line at `v` is therefore `e_c`.  An arbitrary common projective line with no
such incoming constraint is enlarged to a generic line supporting all three
colours.  Essential tail factors are also allowed to support every colour.
Thus the Boolean system is a **relaxation**: it never discards a pure term of
an actual source.  It ignores edge weights, mixed rows, cancellations,
minimum-reciprocity reselection, and all coefficient equalities.

A nonzero pure target coefficient contains at least one nonzero perfect-
matching monomial, so each of the three target colours chooses one perfect
matching in this relaxation.  This implication is valid with parallel
aggregate cells and arbitrary complex cancellations: a sum equal to one
cannot have all of its matching monomials zero.

## 3. There are exactly two pure-pair orbits

Every selected block has at least one witness head fixed to one target axis.
If that block occurs in a pure-`c` matching, the fixed head axis must be
`e_c`.  Hence the same physical block cannot occur in pure matchings of two
different colours.  The three chosen pure matchings are pairwise
edge-disjoint.

The checker independently enumerates all 105 perfect matchings of `K8` and
all 6,300 ordered disjoint pairs.  Under `S8` there are exactly two orbits,
of sizes 1,260 and 5,040.  Their alternating unions have cycle types

\[
                            C_4\sqcup C_4,
            \qquad	ext{or}\qquad C_8.                       \tag{1}
\]

It fixes one representative of each type for colours zero and one and adds
an existential perfect matching for colour two.  This exhausts all possible
three-pure support packets up to vertex permutation and global colour
permutation.

## 4. Independently checked UNSAT certificates

Each orbit gives a CNF with 396 Boolean variables and 2,972 clauses.  The
encoding uses only explicit pairwise/cardinality clauses and implications;
the exact-cardinality construction is exhaustively truth-table checked.

A deterministic in-repository CDCL generator produces deletion-free RUP
proofs.  The committed proof payloads are not trusted on generation: the
separate, pinned checker from
`verify_n8_d1_m10_first_core_rup.py` replays every addition by reverse unit
propagation and requires a final empty clause.

| pure-pair type | RUP additions | checked propagations |
|---|---:|---:|
| `C8` | 4,994 | 561,160 |
| `C4+C4` | 16,179 | 2,189,919 |

Both formulas are therefore unsatisfiable over literal Boolean semantics,
with no external SAT solver in the verification path.  Since they are
relaxations of the source data, every actual sharp all-flat `r=4,4K2` packet
is excluded.

## 5. Scope in the structural proof

Combining this result with the exact `r=3` response obstruction gives:

* the sharp all-flat three-reciprocal frontier is empty;
* the sharp all-flat four-reciprocal `4K2`-good equality frontier is empty;
* if this `r=4,4K2` equality packet occurs at all, it already has a curved
  adjacent rank-one/rank-one good overlap.

The missing local theorem is still the full-nine curved-overlap gate.  The
other `r=4` good graphs (`C4+2K2`, `P3+2K2+K1`, and lower-edge strata) and
the shared-endpoint `r>=4` reciprocal branch need their own equality/slack
reductions.  This note makes no claim that the complete conjecture or all of
`N=8` is proved.

## Reproduction

```sh
python3 computations/verify_n8_r4_4k2_three_pure_support_rup.py
python3 -O computations/verify_n8_r4_4k2_three_pure_support_rup.py
```

To regenerate the proof candidates before independent replay:

```sh
python3 computations/verify_n8_r4_4k2_three_pure_support_rup.py \
  --write-proofs --max-nodes 200000
```
