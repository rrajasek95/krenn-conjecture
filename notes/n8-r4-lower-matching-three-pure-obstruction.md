# The two lower all-flat `r=4` matching strata are empty

## Outcome

Continue in the sharp eight-site, four-reciprocal selected-witness packet
and assume that every adjacent rank-one-good transition is flat.  The graph
reduction in
[`n8-r4-flat-good-graph-reduction.md`](n8-r4-flat-good-graph-reduction.md)
left only

\[
       G=2K_2+4K_1,\qquad G=3K_2+2K_1,\qquad G=4K_2.       \tag{1}
\]

The last case was already excluded by
[`n8-r4-4k2-three-pure-support-obstruction.md`](n8-r4-4k2-three-pure-support-obstruction.md).
This note excludes the first two.  Neither lower matching stratum can
support all three nonzero pure target coefficients, even before mixed-fibre
equations or coefficient cancellations are imposed.

Consequently the entire maximum-degree-two all-flat `r=4` good-graph
frontier is empty.  This remains a local structural theorem: the curved
rank-one overlap gate and the shared-endpoint reciprocal branch are separate
parts of the global proof.

## 1. The four exhaustive essential profiles

Four reciprocal pairs make the 24 directed witnesses occupy twenty physical
selected pairs.  If `g=|E(G)|`, exactly `20-g` selected pairs are bad and
each needs an essential endpoint.  The refined count leaves the following
four profiles, where `t` is the number of cubic sites and `q` the number of
two-essential sites:

\[
\begin{array}{c|c|c|c|c}
G&(g,t,q)&\text{one-essential sites}&\text{bad pairs}
  &\text{essential incidences}\\ \hline
2K_2+4K_1&(2,2,6)&0&18&18\\
3K_2+2K_1&(3,1,7)&0&17&17\\
3K_2+2K_1&(3,2,5)&1&17&17\\
3K_2+2K_1&(3,2,6)&0&17&18.
\end{array}                                                   \tag{2}
\]

The first two are equality packets.  In the third, the unique remaining
site must use its one available essential incidence.  In the fourth, one
selected bad pair may be essential at both endpoints.  These alternatives
exhaust the one unit of slack in the `3K2+2K1` cap.

## 2. Why the three pure matchings are edge-disjoint

A nonzero pure coefficient contains at least one nonzero perfect-matching
monomial, regardless of complex weights or cancellations.  Choose one such
matching for each target colour.

No physical edge can occur in two chosen pure matchings.

* A selected witness block is rank one and target-aligned at at least one
  endpoint, so it supports at most one pure colour.
* An unselected edge at a cubic endpoint is zero: the cubic site's three
  selected neighbours are its whole nonzero star.
* Otherwise, (2) has at most one one-essential site.  Hence an unselected
  edge has a two-essential endpoint.  Equality in the essential-star lemma
  puts every nonessential endpoint factor on one common projective line.
  One line contains at most one of the three target axes.

Thus the union of any two chosen pure matchings is an alternating `C8` or
`C4+C4`.  The exact `S8` orbit census has sizes 5,040 and 1,260.  Freezing
one representative of each union type, with the third matching existential,
is exhaustive up to vertex and global-colour permutation.

For the `(3,2,5)` profile, the setwise stabilizer of either frozen pure pair
is vertex-transitive (orders 16 for `C8` and 64 for `C4+C4`).  After the
corresponding possible colour swap `0<->1`, the unique one-essential site
may therefore be fixed at vertex zero.  This is the only symmetry breaking
used in that profile.

The `(3,2,6)` profile has one surplus essential incidence.  It may lie on an
unselected pair, or be the second endpoint of one selected bad pair; both
possibilities are retained.  Vertex transitivity puts the surplus endpoint
at zero.  The stabilizer of zero has the following complete neighbour
orbits:

\[
\begin{array}{c|c}
C8&\{1,2\},\{3,4\},\{5,6\},\{7\}\\
C4+C4&\{1,2\},\{3\},\{4,5,6,7\}.
\end{array}                                                   \tag{3}
\]

The slack formulas retain one marker from **every** orbit in (3).  No
surplus-neighbour type is discarded.

## 3. Source-relaxing Boolean model

For each pure-pair orbit and profile, the checker retains:

* the reciprocal perfect matching, the good matching, and all 24 selected
  directed witnesses;
* the literal head colour of each witness, one of each colour leaving every
  site;
* endpoint essential flags, cubic flags, and two-essential flags;
* the common line at a two-essential site, recorded as `e0`, `e1`, `e2`, or
  a line containing none of these axes; and
* the third pure perfect matching.

The clauses make the reciprocal pairs exactly the doubly selected pairs and
the good pairs exactly the selected pairs nonessential at both endpoints.
At a cubic site, every selected incidence is essential and every unselected
pure edge is forbidden.  At a two-essential site, all nonessential incoming
heads and all unselected/nonessential pure factors must lie on the one
common line.  At the possible one-essential site, unselected endpoint
support is deliberately unrestricted.

This admits arbitrary unselected pure edges.  That point is essential: the
selected-only restriction used in the `4K2` equality chart is not available
in the lower strata.  The model also forgets weights, mixed rows, and all
coefficient equalities.  It is therefore a support **relaxation** of every
actual packet in (2), not a coefficient ansatz.

The equality formulas have 420 variables and between 4,454 and 4,572
clauses.  The two slack formulas have 424/423 variables and 4,487/4,481
clauses after the complete symmetry reduction (3).  All eight formulas are
unsatisfiable.

## 4. Independently checked certificates

CaDiCaL was used only to generate proof candidates.  For the six equality
formulas, deletion records were discarded and every remaining clause was
independently replayed as a RUP addition by the separately pinned
two-watched-literal checker.  The two larger surplus formulas use
positive-hint LRAT: a local checker verifies every stated unit chain,
deletion, clause identifier, and final empty clause without invoking a SAT
solver.  Each frozen gzip payload and its decompressed proof are SHA-256
pinned.

\[
\begin{array}{c|c|r|r}
\text{pure union}&(g,t,q)&\text{proof additions}&\text{proof checks}\\ \hline
C8&(2,2,6)&11{,}889&1{,}671{,}761\\
C8&(3,1,7)&15{,}663&2{,}409{,}367\\
C8&(3,2,5)&16{,}354&2{,}697{,}088\\
C8&(3,2,6)&36{,}034&1{,}334{,}067\text{ LRAT hints}\\
C4+C4&(2,2,6)&11{,}696&1{,}774{,}820\\
C4+C4&(3,1,7)&20{,}429&2{,}651{,}093\\
C4+C4&(3,2,5)&18{,}993&3{,}106{,}168\\
C4+C4&(3,2,6)&31{,}951&1{,}114{,}292\text{ LRAT hints}.
\end{array}                                                   \tag{4}
\]

The combined audit has 163,009 proof additions and 16,758,656 checked
propagations/hints.  No external SAT solver is used in the normal
verification path.

## Scope

This closes exactly the two lower matching shapes left by the all-flat
`r=4` graph reduction.  Together with the committed `4K2` obstruction, it
closes all three matching-component cases in (1), as well as the previously
counted-out `C4+2K2` and `P3+2K2+K1` shapes.

It does **not** prove the full conjecture, the curved full-nine overlap
lemma, or the shared-endpoint/high-reciprocity branch.  It uses the sharp
four-reciprocal essential-count packet and the exact equality common-line
theorem at two-essential sites.

## Reproduction

```sh
python3 computations/verify_n8_r4_lower_matching_three_pure_rup.py
python3 -O computations/verify_n8_r4_lower_matching_three_pure_rup.py
```

Proof candidates can be regenerated with an explicit CaDiCaL path:

```sh
python3 computations/verify_n8_r4_lower_matching_three_pure_rup.py \
  --write-proofs --cadical /path/to/cadical
```
