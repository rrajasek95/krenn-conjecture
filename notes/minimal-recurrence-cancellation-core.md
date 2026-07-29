# Minimal recurrence cancellation cores need not have tight cuts

This note sharpens the perfect-matching unfolding lemma and records the
smallest obstruction to turning its alternating cycle into a
Gallai--Edmonds, Kotzig-bridge, or tight-cut induction.

Let `F` be a family of even subsets of a finite set `V`, with
`emptyset in F`, satisfying the per-pivot recurrence rules.  Write

\[
 E=\{uv:\{u,v\}\in F\},
\qquad
 L_F(S)=\{uv\in E[S]:S\setminus\{u,v\}\in F\}.          \tag{1}
\]

Thus the degree of `u` in `L_F(S)` is exactly the number of nonzero
recurrence terms at pivot `u`.

## 1. The minimal-core theorem

**Theorem 1.**  Suppose `S` is inclusion-minimal among the even sets which
are matchable in `E` but do not belong to `F`.  Then:

1. every proper even matchable subset of `S` belongs to `F`;
2. `L_F(S)` is exactly the allowed-edge subgraph

   \[
   H(S)=\{uv\in E[S]:E[S\setminus\{u,v\}]
                         \text{ has a perfect matching}\};              \tag{2}
   \]

3. every vertex of `H(S)` has degree at least two;
4. every connected component of `H(S)` is matching-covered and has no edge
   common to all of its perfect matchings.  In particular every vertex is
   contained in an alternating cycle between two supported perfect
   matchings.

**Proof.**  Assertion 1 is the definition of inclusion-minimality.  If
`uv` belongs to (2), then `S-{u,v}` is a proper matchable set and hence is
feasible by assertion 1, so `uv in L_F(S)`.  Conversely, if
`uv in L_F(S)`, perfect-matching unfolding at the feasible remainder gives
a perfect matching of `E[S-{u,v}]`.  This proves assertion 2.

Because `S` is matchable, every vertex is incident with at least one
allowed edge.  Since `S` is infeasible, its recurrence-term count at each
pivot is not one.  By assertion 2 this count is the degree in `H(S)`, so it
is at least two.  This proves assertion 3.

Every edge of `H(S)` extends to a perfect matching of `S`, by (2).  A
perfect matching cannot use edges between distinct connected components,
so its restriction makes each component matching-covered.  If an edge
`uv` occurred in every perfect matching of its component, no other edge at
`u` could be allowed, contrary to the degree bound.  Hence an allowed edge
can be compared with a perfect matching omitting it; the symmetric
difference supplies an alternating cycle through its incident vertex.
This proves assertion 4. `QED`

The theorem is field-free and is the strongest conclusion supplied by
minimality plus the recurrence alone.  It does **not** imply the presence
of a reducible cut.

## 2. The smallest dense countermodule

Take `V={0,1,2,3,4,5}`.  Let `A` be the symmetric zero-diagonal scalar
matrix whose every upper-triangular entry is one except

\[
                              a_{01}=-2.                 \tag{3}
\]

Put

\[
                   F=\{T:|T|\text{ is even and }
                              \operatorname{haf}A[T]\ne0\}.             \tag{4}
\]

This is an actual characteristic-zero hafnian-support family, so it
satisfies the recurrence rules exactly.  On
`S={0,1,2,3}` one has

\[
 \operatorname{haf}A[S]
   =a_{01}a_{23}+a_{02}a_{13}+a_{03}a_{12}
   =-2+1+1=0.                                           \tag{5}
\]

Every edge is nonzero, so `S` is matchable and all of its proper even
matchable subsets are feasible.  It is therefore a minimal cancellation
core.  Moreover

\[
                              H(S)=K_4,                  \tag{6}
\]

not a graph with a unique-matching bridge.  It has three perfect matchings,
minimum degree three, and no nontrivial tight cut.

The ambient support is `K_6`, and

\[
                         \operatorname{haf}A[V]=6\ne0.  \tag{7}
\]

Thus both `emptyset` and the ambient full set are feasible, as required in
the diagonal recurrence setting.  The ambient matching-covered graph also
has no nontrivial tight cut: every `3|3` cut is crossed once by some perfect
matchings and three times by others.  Its Gallai--Edmonds decomposition is
the single perfect core `C=V`, with `D=A=emptyset`.

Equation (7) is entirely a boundary-coupling effect.  Perfect matchings
using the outside edge `45` contribute

\[
                 a_{45}\operatorname{haf}A[S]=0,         \tag{8}
\]

whereas the twelve matchings crossing from `S` to `{4,5}` twice have total
weight `6`.  Consequently neither the canceled shore nor any alternating
cycle in it can be contracted while retaining the full hafnian support.

This example is order-minimal for the failed reduction.  A proper even
matchable infeasible set has size at least four, and an even ambient ground
set properly containing it has size at least six.

## 3. Exact boundary for a prospective induction

The following implication is therefore false, even for genuine rational
hafnians:

> a minimal matchable infeasible class forced by a failed three-colour
> cover has a Kotzig bridge or a nontrivial tight cut along which the class
> and the ambient recurrence can be reduced.

Theorem 1 gives an alternating cancellation core, but (3)--(8) show that
the core can be dense, tight-cut-free, and coupled to the complement only
through multi-crossing matchings.  A valid uniform induction needs an
additional *three-family* invariant that controls these crossing terms; no
one-family Gallai--Edmonds or tight-cut statement follows from recurrence
accessibility.

The dependency-free exact audit is
`computations/verify_minimal_recurrence_cancellation_core.py`.
