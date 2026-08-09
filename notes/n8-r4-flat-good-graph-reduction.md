# The all-flat `r=4` graph frontier has only matching components

## Outcome

The previously listed `C4+2K2` and `P3+2K2+K1` cases do not survive the
sharp essential-incidence count.  Once the rank-at-least-two chord forced by
each flat good wedge is charged at its endpoints, their selected bad-edge
requirements exceed their essential budgets:

\[
\begin{array}{c|c|c}
G&\text{selected bad pairs}&\text{selected essential cap}\\ \hline
C_4+2K_2&14&12\\
P_3+2K_2+K_1&16&15.
\end{array}                                                   \tag{1}
\]

The only all-flat four-reciprocal graph shapes left are

\[
             2K_2+4K_1,\qquad3K_2+2K_1,\qquad4K_2.          \tag{2}
\]

The `4K2` equality case is already excluded by the independently checked
three-pure RUP certificate in
[`n8-r4-4k2-three-pure-support-obstruction.md`](n8-r4-4k2-three-pure-support-obstruction.md).
Thus the remaining all-flat frontier consists only of the two lower matching
strata in (2).

## The refined essential cap

Four reciprocal witness pairs mean that the 24 directed witnesses occupy
twenty physical selected pairs.  Hence the complement of the selected graph
has eight edges.  A coordinate-cubic site has selected physical degree three
and therefore complement degree at least four.  The exact extremal table for
the minimum number of complement edges supporting `t` such vertices is

\[
                 0,4,7,9,10,10,12,14,16\qquad(t=0,\ldots,8). \tag{3}
\]

With only eight complement edges, at most two sites can be cubic.

Let `G` be the graph of selected rank-one pairs good at both endpoint stars,
under the assumption that every adjacent transition is flat.  The flat-wedge
theorem forces every distance-two chord of `G` to have rank at least two.
At an endpoint of such a chord, three essential neighbours are impossible.
If there are two, the chord itself is essential, leaving at most one
essential incidence among the selected bad pairs.  Thus:

* every vertex covered by a forced chord contributes at most one selected
  essential incidence;
* every other noncubic vertex contributes at most two; and
* only isolated vertices of `G` can be cubic, with at most two cubic sites
  globally by (3).

If `c(G)` vertices are covered by forced chords and `i(G)` are isolated, the
selected essential cap is therefore

\[
       c(G)+2(8-c(G))+\min(i(G),2).                           \tag{4}
\]

Every selected bad pair needs at least one essential endpoint.  Applying
(4) to all maximum-degree-two path/cycle decompositions on eight vertices,
discarding triangles and shapes whose forced chords exceed the eight-edge
complement, leaves exactly the three matching graphs in (2).

For `C4+2K2`, all four cycle vertices are chord-covered and no vertex is
isolated, giving cap `4+2*4=12<14`.  For `P3+2K2+K1`, the two path endpoints
are chord-covered, five other nonisolated vertices contribute at most two,
and the sole isolate may contribute three, giving `2+10+3=15<16`.

## Exact lower frontier

The two remaining unclosed shapes have very small cubic profiles.

* `2K2+4K1` has eighteen selected bad pairs and cap eighteen.  It is an
  equality packet: exactly two isolated sites are cubic, all six others have
  exactly two essential neighbours, and every bad pair is essential at
  exactly one endpoint.
* `3K2+2K1` has seventeen selected bad pairs.  It has either one cubic
  isolate with equality throughout, or two cubic isolates with exactly one
  unit of essential slack.

These are finite source-labelled support problems.  The appropriate next
test retains the reciprocal matching, the good matching, the cubic sites,
the common-line equality at every two-essential site, and all three pure
perfect matchings.  A head-only relaxation is insufficient: it admits
spurious packets whose two-essential sites receive incompatible incoming
head colours.

## Scope

This is an exact structural reduction, not a coefficient feasibility claim
for the two lower matching strata.  It uses the global all-flat hypothesis.
The curved rank-one/rank-one full-nine gate and shared-reciprocal full-span
branch remain separate.

## Reproduction

```sh
python3 computations/verify_n8_r4_flat_good_graph_reduction.py
python3 -O computations/verify_n8_r4_flat_good_graph_reduction.py
```
