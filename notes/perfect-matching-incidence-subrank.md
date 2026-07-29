# Perfect-matching incidence tensors and the limits of tightness

This note isolates an exact tensor reformulation which is slightly finer
than aggregation by underlying vertex pair.  It also records two exact
counterexamples to an initially tempting, but false, general theorem about
tight tensors.

## 1. The incidence tensor

Let `G` be a finite loopless multigraph on the vertex set `B`; parallel
edge occurrences remain distinct.  For a vertex `v`, let `E(v)` be the set
of edge occurrences incident with `v`, and give

\[
                     U_v=\mathbb C^{E(v)}
\]

its occurrence basis `(f_{v,e})_(e in E(v))`.  Define

\[
 T_G=\sum_{M\in\operatorname {PM}(G)}
             \bigotimes_{v\in B}f_{v,M(v)}.                \tag{1}
\]

Here `M(v)` is the unique occurrence of `M` incident with `v`.  If an
edge occurrence `e=uv` has endpoint colors `(i,j)` and weight `w_e`, put

\[
 L_u f_{u,e}=w_e e_i,\qquad L_v f_{v,e}=e_j.               \tag{2}
\]

(The nonzero scalar can instead be split arbitrarily between the two
ends.)  Applying the maps (2) to one summand of (1) gives exactly its
decorated matching weight and endpoint coloring.  Therefore

\[
          (\bigotimes_vL_v)T_G=H_B(A).                     \tag{3}
\]

Conversely, split every nonzero aggregate cell `A_uv(i,j)` into one edge
occurrence with endpoint colors `(i,j)` and weight `A_uv(i,j)`.  Expanding
a product over a fixed underlying perfect matching is precisely the choice
of one such parallel occurrence on each pair, so (3) recovers the original
aggregate matching tensor.  Thus no parallel source, asymmetric endpoint
color, or complex cancellation is lost.

The local maps in (2) have an important special form: every input column
has exactly one nonzero output coordinate, but many columns may merge into
the same output row.  They are **row-monomial fiber maps**, not arbitrary
linear maps and not generalized subpermutation maps (the latter would also
forbid two columns in one row).  Any tensor argument which forgets this
distinction enlarges the problem substantially.

## 2. Strong tightness and alternating-cycle rectangles

Orient every edge occurrence once and assign it an independent formal
degree `gamma_e`.  Give its two incidence symbols degrees

\[
        \deg f_{u,e}=\gamma_e,\qquad
        \deg f_{v,e}=-\gamma_e.                            \tag{4}
\]

Every summand of (1) has total degree zero, edge by edge.  Composing (4)
with a sufficiently separated integer linear functional makes all local
degrees injective, so `T_G` is tight in the standard sense.  Its support is
also free: two distinct perfect matchings cannot differ at exactly one
vertex.

There is more structure than tightness or freeness.  If `M,N` are perfect
matchings, their symmetric difference is a disjoint union of alternating
even cycles (parallel occurrences may form a doubled two-cycle).  Switching
any subcollection of those cycles again gives a perfect matching.  If the
cycles are `C_1,...,C_k`, their `2^k` switchings form a Boolean rectangle,
and their edge-weight monomials obey all corresponding multiplicative
rectangle relations.

For a two-term mixed coloring fiber, write its two matching monomials as
`z^a,z^b`.  Since all used coordinates are nonzero, cancellation is
equivalent to

\[
                            z^{a-b}=-1.                    \tag{5}
\]

The exponent difference is a vertex-balanced alternating-cycle
circulation.  Consequently, if binomial fibers give circulations `d_j`
with an integer relation

\[
                   \sum_jm_jd_j=0,\qquad \sum_jm_j\text{ odd},\tag{6}
\]

then multiplying (5) to the powers `m_j` gives `1=-1`.  This is the exact
mechanism behind the odd-binomial certificates in the six-vertex audits.

## 3. Tight plus free does not force monomial diagonalization

The following two examples prevent replacing the incidence-specific
problem by a general theorem about tight tensors.

### 3.1 A row-monomial order-four example

Use local symbols `0,1,2,p` where they occur and take the five support
tuples

\[
 0000,\quad1111,\quad2222,\quad0101,\quad p1p1             \tag{7}
\]

with coefficients `1,1,1,1,-1`.  Map `0,1,2` to the three standard output
basis vectors and map `p` to `e_0`.  The last two terms become the same
mixed tensor with opposite coefficients, so the image is `Delta_(4,3)`.
The maps are row-monomial fiber maps.

This support is free and tight.  One choice of injective local weights,
listed in symbol order, is

\[
 (0,1,3,2),\quad(0,1,2),\quad(0,-1,3,-2),\quad(0,-1,-8),   \tag{8}
\]

and every tuple in (7) has total weight zero.  Its induced-matching
(monomial) subrank is only two: the three diagonal tuples are spoiled by
`0101`; a triple using `0101` fails with `0000` or `1111`; and the apparent
triple `{p1p1,0000,2222}` is again spoiled by `0101`.

It is not a perfect-matching incidence support.  The two independent local
switches implicit in the canceling pair would force the missing rectangle
corners, with multiplicatively related coefficients.

### 3.2 A positive order-three interpolation example

Let

\[
 T=\sum_{0\le i,j\le2}e_i\otimes e_j\otimes e_{4-i-j}
       \in\mathbb C^3\otimes\mathbb C^3\otimes\mathbb C^5.\tag{9}
\]

Its support is free and tight under the injective weights `i,j,k-4`.
For `r in {-1,0,1}`, let `L_r` be the quadratic Lagrange polynomial which
is one at `r` and zero at the other two points.  Use the coefficients of
the three `L_r` as the rows of the first and second local maps, and use
`r^(4-k)` as row `r`, column `k`, of the third map (with `0^0=1`).  The
output coefficient in rows `(a,b,c)` is

\[
                       L_a(r_c)L_b(r_c),                   \tag{10}
\]

so the image is exactly `Delta_(3,3)`.  On the other hand its monomial
subrank is two: a size-three restriction would use all three first and
second coordinates and three sum levels, but only the extreme levels
`i+j=0,4` have singleton fibers, leaving an extra selected cell.

This second example even has all source coefficients positive, but its
local maps are dense.  It shows that tightness plus freeness cannot by
itself supply an exact linear-to-monomial bridge.

## 4. Surviving incidence-specific question

For Krenn's problem the precise tensor statement is therefore:

> Can a perfect-matching incidence tensor (1), under nonzero row-monomial
> fiber maps of the edge-consistent form (2), map to `Delta_(B,3)` when
> `|B|>=6`?

The multigrading (4), rectangle completion, and circulation obstruction
(6) are genuine extra data.  The exact binary cancellation gadgets show
that they do not make every mixed fiber termwise zero, so a complete proof
still has to organize interactions among fibers of three or more terms or
derive enough odd circulation relations globally.
