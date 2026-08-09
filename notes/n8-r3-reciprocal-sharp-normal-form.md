# The sharp three-reciprocal frontier has two isolated cubic sites

## Outcome

Continue the selected rank-one witness census at `N=8` with exactly three
reciprocal physical pairs.  The earlier flat-wedge audit leaves two possible
graphs for the **good selected edges**:

\[
                 3K_2\sqcup2K_1,\qquad 4K_2.              \tag{1}
\]

The essential-star equality case eliminates the second graph and rigidifies
the first.  In every surviving sharp packet:

1. the good selected graph is `3K2+2K1`;
2. its two isolated vertices have three essential neighbours and hence are
   literal coordinate-cubic sites;
3. the two cubic sites have zero direct block between them;
4. all fifteen pairs among the other six sites are selected rank-one pairs;
5. the three good edges form a perfect matching on those six outer sites.

Thus the `r=3` counting frontier is not a diffuse reciprocal problem.  It is
a **two-cubic-zero-pair plus outer-K6** normal form.  It is still not closed by
the adjacent-cubic descent, because the two forced cubic sites are necessarily
nonadjacent.  Complete mixed-fibre equations, not another incidence count, are
needed to eliminate or descend this residual chart.

## Essential-incidence equality

The 24 selected directed witnesses occupy `24-r=21` physical pairs.  If the
good graph has `g` edges, all other `21-g` selected pairs are bad and must be
covered by endpoint-essential incidences.  A vertex with three essential
neighbours has total nonzero degree three by the equality case of the
essential-subspace lemma.  All three of its selected incident pairs are then
bad, so such a vertex must be isolated in the good graph.  Every other vertex
contributes at most two essential incidences.

For `4K2`, there is no isolated vertex.  Hence there are no three-essential
sites, while the essential budget is at most `8*2=16`.  But `21-4=17` bad
selected pairs must be covered.  This is impossible.

For `3K2+2K1`, the eighteen bad pairs require

\[
                   18\le 16+t,\qquad t\le2,               \tag{2}
\]

where `t` is the number of three-essential sites.  Equality holds throughout:
`t=2`, the two sites are exactly the isolated vertices of the good graph, all
other sites have two essential neighbours, and no bad edge is charged twice.
The cubic-vertex theorem upgrades each equality site to three literal
same-colour coordinate cells, one for each target colour.

Each cubic site has selected degree three, hence degree four in the
seven-edge complement of the selected graph.  The union of two four-edge
complement stars has size eight if the cubic pair is selected and size seven
if it is absent.  Since the entire complement has size seven, the cubic pair
is absent and the complement is exactly the union of those two stars.  It
follows at once that every outer-outer pair is selected, proving the announced
normal form.

## Sharp incidence counterguard

This normal form is feasible at the complete witness/essential-incidence
level.  Take cubic sites `0,1`, outer sites `2,...,7`, all outer edges, and

\[
  N(0)=\{2,3,4\},\qquad N(1)=\{5,6,7\}.                    \tag{3}
\]

Declare `25,36,47` good.  Charge the six cubic arms at their cubic endpoints.
The remaining twelve outer edges form `K6` minus that perfect matching; a
cyclic Euler orientation charges two at every outer endpoint.  This realizes
eighteen distinct bad-edge charges with essential degrees

\[
                         (3,3,2,2,2,2,2,2).                \tag{4}
\]

The checker also orients the 21 selected pairs as 24 witness arcs of
outdegree three, with the three disjoint reciprocal pairs `23,45,67`, and
assigns one arc of each colour at every tail.  It realizes the full endpoint
line flags: the cubic arms are same-colour coordinate cells, the two
essential outer lines are independent, and every other line at an outer site
is their common complementary axis.  In this representative all three
reciprocal units are diagonal.  Therefore neither a reciprocal hub, an
off-diagonal reciprocal selector, nor an adjacent cubic pair follows from
graph, endpoint-essential, and witness-label data alone.

This counterguard is not an exact source: it does not assign arbitrary block
coefficients or satisfy the nine GHZ tensor equations.  Its purpose is to
locate the next honest gate.  The configurations in (3) must now be tested using the diagonal and
off-diagonal target rows together with the two cubic pure completions.

## Consequence for the structural split

The current `N=8` structural alternatives can now be stated more sharply.

* For at most two reciprocal witness pairs, the curved adjacent good
  rank-one overlap is forced.
* For three reciprocal pairs, an all-flat obstruction can survive the local
  count only in the two-cubic-zero-pair/outer-K6 chart above.
* The previously listed `4K2` frontier was an artefact of not feeding the
  equality clause back into endpoints incident to a good edge.

This is a genuine reduction, not a proof of the conjecture.  Closing the
remaining chart requires a source-faithful mixed-fibre identity.  In
particular, the reciprocal cap/permanent insertion guards show that support
or quadratic insertion data by itself cannot supply that identity.

## Reproduction

```sh
python3 computations/verify_n8_r3_reciprocal_sharp_normal_form.py
python3 -O computations/verify_n8_r3_reciprocal_sharp_normal_form.py
```

The checker independently verifies the two shape budgets, constructs the
sharp normal form and essential assignment, finds a three-reciprocal
outdegree-three witness orientation, and audits the source colour labels.
