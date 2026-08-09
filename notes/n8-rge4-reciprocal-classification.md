# N=8 classification of four-or-more reciprocal witnesses

This note isolates the exact content of the selected-witness graph and the
endpoint essential-incidence axioms for `r>=4`.  Its main negative conclusion
is load-bearing: those local axioms do **not** force an adjacent cubic packet,
even at the maximum reciprocal count.  Matching-coefficient or cofactor
provenance is needed.

## 1. Reciprocal-graph dichotomy

Each of the eight sites chooses three directed, colour-labelled witness arcs,
so there are 24 arcs.  Let `r` be the number of physical pairs used in both
directions.  The reciprocal physical pairs form a simple graph of maximum
degree three, and the selected arcs occupy

\[
                         24-r
\]

physical blocks.

If no two reciprocal pairs share an endpoint, the reciprocal graph is a
matching and hence has at most four edges.  At `r=4` it is a perfect matching
on all eight sites (105 labelled possibilities).  Therefore the exhaustive
split is

\[
 \boxed{r=4\text{ reciprocal perfect matching}}
 \quad\text{or}\quad
 \boxed{\text{two reciprocal pairs share an endpoint}}.       \tag{1}
\]

The second alternative is automatic for every `r>=5`.

## 2. Why high reciprocity does not itself make cubic sites

There are `24-2r` singly selected arcs.  A site receiving no such arc has
degree three in the **selected witness graph**, so at least

\[
             \max(0,8-(24-2r))=\max(0,2r-16)                  \tag{2}
\]

sites have selected degree three.  In particular the lower bounds at
`r=9,10,11,12` are `2,4,6,8`.

It is not valid to call these sites literal coordinate-cubic sites.  The
three chosen witness blocks need not be all the nonzero incident blocks;
unselected blocks can remain nonzero.  This is exactly the distinction
already warned about in the reciprocal census of
[`n8-oriented-rankone-curvature-full-nine-frontier.md`](n8-oriented-rankone-curvature-full-nine-frontier.md).
Consequently the majority-cubic theorem and adjacent-cubic descent cannot be
invoked from (2).

## 3. Exact local-incidence counterguards

The checker freezes one coordinate endpoint-line model for each reciprocal
count `4<=r<=12`.  At `r=4` it freezes both branches of (1).  In every model:

1. every site has three outgoing witnesses whose head axes are exactly
   colours `0,1,2`;
2. the reciprocal and underlying physical-pair counts are exact;
3. every one of the 28 physical blocks is declared nonzero rank one, including
   blocks outside the selected witness graph;
4. the seven endpoint lines at each site span all three target axes; and
5. deletion-essential neighbors are recomputed literally as the unique
   occurrences of an endpoint axis, giving at most two at every noncubic
   complete star.

The replayed census is:

| branch | selected blocks | sites of selected degree 3 | literal cubic sites |
|---|---:|---|---:|
| `r4_matching` | 20 | none | 0 |
| `r4_shared` | 20 | none | 0 |
| `r5_shared` | 19 | `6` | 0 |
| `r6_shared` | 18 | `2` | 0 |
| `r7_shared` | 17 | `0,2` | 0 |
| `r8_shared` | 16 | `6` | 0 |
| `r9_shared` | 15 | `2,6` | 0 |
| `r10_shared` | 14 | `0,1,4,5` | 0 |
| `r11_shared` | 13 | `0,1,3,4,5,7` | 0 |
| `r12_shared` | 12 | all sites | 0 |

These are not matching sources and do not satisfy the full pure/mixed
coefficient system.  They are exact counterguards to any deduction using
only the selected-witness, coordinate-head, rank-one, local-span, and
essential-deletion data.  In particular neither a reciprocal hub nor even a
three-regular reciprocal graph termwise forces an adjacent-cubic packet.

## 4. The sharp `r=4` pure-row refinement

The two frozen `r=4` guards realize the equality profile `e(u)=2` at every
site.  Each site has one common nonessential coordinate line, and no physical
edge is essential at both endpoints.  Thus the independently checked
[`axis-purified one-sided pure-cover theorem`](axis-purified-one-sided-essential-pure-cover.md)
excludes these particular packets once all three nonzero pure coefficient
rows are imposed: a pure-`c` perfect matching needs four sites labelled `c`,
so three colours would need twelve sites.

This does not close arbitrary `r=4`.  It gives the precise surviving guard:
an exact `r=4` source must escape at least one of the inputs needed for that
pure-cover reduction—most importantly, axis purification of every common
nonessential line or the one-sided/no-double-essential condition.  A generic
projective common line can have nonzero coordinates in several colours.

## 5. Consequence for the proof program

The graph-theoretic part of the `r>=4` reciprocal branch is finished by (1).
There is no honest incidence-only route from the shared-endpoint branch to
adjacent-cubic descent.  The next useful lemma must use an exact coefficient
packet.  Natural targets are:

- prove that a shared reciprocal hub purifies the common endpoint lines;
- force a double-essential/four-site cancellation packet and close it by the
  existing mixed equations; or
- obtain a source-faithful cap/Schur modification from the reciprocal
  coordinate blocks.

Any claimed high-`r` cubic shortcut must explicitly prove that the
unselected incident blocks vanish; selected degree three is insufficient.

## Reproduction

```sh
python3 computations/verify_n8_rge4_reciprocal_classification.py
python3 -O computations/verify_n8_rge4_reciprocal_classification.py
```

The checker pins the essential-count and axis-purified pure-cover
dependencies, enumerates all 105 labelled four-edge reciprocal matchings,
and replays every endpoint-line counterguard without a SAT solver.
