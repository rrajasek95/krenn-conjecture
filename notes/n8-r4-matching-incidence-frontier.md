# The four-reciprocal matching frontier needs one coefficient theorem

## Outcome

After the exact `r=3` closure, four reciprocal selected witness pairs are
the first new matching-shaped case.  The local incidence data do **not**
permit a reduction to three reciprocals: there is a rational endpoint-line
packet for which exhaustive reselection among all target-aligned carrier
blocks still has minimum reciprocity four.

The packet has

\[
 M_{\rm rec}=\{01,23,45,67\},\qquad
 G_{\rm sel}=\{03,16,25,47\},                            \tag{1}
\]

where `G_sel` is the graph of selected rank-one pairs good at both deleted
stars.  The matchings in (1) are disjoint.  Every vertex has exactly two
essential incidences, every one of the sixteen selected bad pairs is
essential at exactly one endpoint, and there is no cubic site or adjacent
pair in `G_sel`.  Four common nonessential lines are target axes and four
are genuine generic projective lines.  This is the exact boundary missed by
the axis-purified termwise cover theorem: a generic line can carry several
target coefficients.

The new arbitrary-direct sitewise four-cover theorem does not eliminate
this packet.  On deleting any of the four reciprocal pairs, every target
axis belongs to at least four of the six residual incident spaces, and every
residual site contains at least one target axis.  Thus purification of the
four generic lines requires more than the `|D_i|>=4` and site-cover counts.

There is nevertheless a sharp positive reduction.  The selected twenty
physical blocks alone miss the pure colour-zero and colour-one supports.
Adding the two generic/generic blocks `02,46` gives explicit pure matching
terms in all colours:

\[
\begin{array}{c|c}
0&02|17|35|46\\
1&02|13|46|57\\
2&05|14|27|36.
\end{array}                                               \tag{2}
\]

Those two repairs are automatically rank-one good pairs.  Together with
`G_sel` they form the two paths

\[
                         3-0-2-5,\qquad1-6-4-7.          \tag{3}
\]

Every length-two wedge in (3) has a nonzero rank-one opposite chord:

\[
 (3,0,2)\mapsto23,quad(0,2,5)\mapsto05,quad
 (1,6,4)\mapsto14,quad(6,4,7)\mapsto67.                \tag{4}

The exact flat-wedge theorem says a flat rank-one good wedge has opposite
chord rank at least two.  Hence an exact source on the repaired packet would
already have a curved rank-one/rank-one overlap.  The repair is therefore
not a counterexample to the desired structural split; it exhibits how pure
support can force that split.

## Exact packet

The checker stores the 24 labelled arcs explicitly.  Each tail uses one
distinct neighbor in each colour.  Their physical support has twenty edges
and the reciprocal graph is the first matching in (1).  The essential
endpoint incidences are

```text
01 07 | 13 14 | 21 23 | 35 36 |
43 45 | 50 57 | 65 67 | 71 72.
```

At sites `0,2,4,6` the common nonessential line is `(1,1,1)`.  At sites
`1,3,5,7` it is respectively `e0,e1,e0,e1`.  Incoming witness arcs fix
their endpoint axes; a free essential tail factor is also taken as
`(1,1,1)`.  Exact row reduction verifies that deletion drops the endpoint
span precisely for the sixteen displayed incidences and for no others.

The two extra blocks in (2) use the common generic line at both endpoints.
They create no new target-aligned carrier arc.  There are two admissible
local carrier triples at each of the four generic-head sites and one at each
of the four axis-head sites.  Across all `16` global choices, respecting
distinct neighbors at a site, the reciprocal count is never below four.
Thus simply choosing the witnesses more carefully cannot return this packet
to the closed `r<=3` case.

There is also a uniform consequence in the sharp `4K2` equality stratum.
The sixteen bad selected pairs consume all sixteen allowed essential
incidences, one at exactly one endpoint; every unselected nonzero block is
therefore nonessential at both endpoints.  The equality flag theorem puts
its two endpoint spaces on the two common lines, so it is a rank-one good
pair.  It is adjacent to the selected good matching edge through either
endpoint.  Since every possible opposite chord has rank at most one, the
flat-wedge rank theorem makes this adjacent wedge curved.  Consequently an
all-flat sharp `4K2` source has **no unselected nonzero block at all**.  The
remaining all-flat question is thus not an open-ended repair census: it is
the coefficient-complete GHZ system on the selected twenty-block support.

## What remains

This is a structural packet, not a solution of the GHZ matching equations.
It proves three useful scope facts.

1. `r_min<=3` is not a consequence of endpoint line incidence and carrier
   availability.
2. The full-direct four-cover/site-cover theorem does not by itself purify
   the remaining four lines.
3. In the displayed sharp orbit, the first termwise pure-support repair
   already supplies the desired curved rank-one overlap; uniformly in the
   `4K2` equality stratum, every nonzero unselected block does so.

The unresolved all-flat `r=4,4K2` task is now finite and source-faithful:
test the coefficient-complete pure/mixed system on the selected twenty
blocks.  Other `r=4` good-graph strata still require their own equality or
slack analysis.  A support or incidence argument which ignores the four
generic projective lines cannot finish them.

For `r>=5`, the reciprocal graph has a shared endpoint, but this observation
alone is also selection-dependent: a common line can require a duplicate
non-carrier block to avoid the three-essential/cubic equality case.  The
same coefficient theorem should therefore be formulated at minimum
reciprocity, rather than for an arbitrary chosen witness system.

## Reproduction

```sh
python3 computations/verify_n8_r4_matching_incidence_frontier.py
python3 -O computations/verify_n8_r4_matching_incidence_frontier.py
```

The checker verifies the endpoint flags, the minimum-reciprocity census,
the three pure-support terms, the four flat-wedge rank contradictions, and
the full-direct four-cover/site-cover ledger on all four reciprocal
deletions.
