# The large isotropic-shore obstruction

Let `B` be an even vertex set, let every `V_v=C^3`, and attach an arbitrary
tensor `A_uv in V_u tensor V_v` to every pair.  Write

\[
 H_B(A)=\sum_{M\in\operatorname{PM}(B)}\bigotimes_{uv\in M}A_{uv}.
\]

This note records a uniform necessary condition for
`H_B(A)=Delta_(B,3)`.  It is elementary, but it is stronger than the
six-vertex three-versus-three torus-zero test because it applies to every
shore larger than its complement.

## 1. Large shores cannot be internally isotropic

Call a tuple of covectors `(x_v)_(v in L)` **toric** if every one of the
three coordinates of every `x_v` is nonzero.

**Lemma 1.1 (large isotropic shore).**  Suppose

\[
 H_B(A)=\sum_{r=0}^2 e_r^{\otimes B}.
\]

If `L` is a proper subset of `B` with

\[
                 |L|>|B\setminus L|,
\]

then there is no toric tuple `(x_v)_(v in L)` satisfying

\[
       (x_u\otimes x_v)(A_{uv})=0
       \qquad\text{for every }uv\in\binom L2.              \tag{1}
\]

**Proof.**  Contract the asserted tensor identity at every vertex of `L`
by the corresponding `x_v`.  A perfect-matching summand which contains an
edge internal to `L` vanishes by (1).  Any remaining summand would have to
match every vertex of `L` to a distinct vertex of `B\setminus L`, which is
impossible because the former shore is larger.  Thus the contraction of
the matching tensor is zero.

The contraction of the target is

\[
 \sum_{r=0}^2\left(\prod_{v\in L}x_v(e_r)\right)
                  e_r^{\otimes(B\setminus L)}.              \tag{2}
\]

The complement is nonempty because `L` is proper.  Its three displayed
constant tensors are linearly independent, and all three coefficients are
nonzero by toricity.  Hence (2) is nonzero, a contradiction. `QED`

For `|B|=6` and `|L|=3`, equality rather than strict inequality leaves
exactly the vector-permanent sector studied in
`notes/determinant-split-route.md`.  Lemma 1.1 starts one vertex beyond that
critical split and needs no vector-permanent classification.

## 2. A useful orientation certificate for rank-one systems

Suppose every nonzero internal matrix on `L` has rank one, and write

\[
                  A_{uv}=a_{uv,u}\otimes a_{uv,v}.          \tag{3}
\]

An endpoint `(v,uv)` is **killable** when `a_(uv,v)` is not a coordinate
vector.  Equivalently, its annihilator hyperplane meets `(C^*)^3`.

**Lemma 2.1 (one-demand orientation).**  If the nonzero internal edges of
`L` can be oriented so that

1. every edge is directed toward a killable endpoint, and
2. every vertex has indegree at most one,

then the internal forms have a simultaneous toric zero.

**Proof.**  At a vertex of indegree zero choose any toric covector.  At a
vertex with unique incoming edge `uv`, choose a toric covector in
`a_(uv,v)^perp`; this is possible by killability.  For every oriented edge,
its factor at the head is zero, so (3) vanishes regardless of the choice at
the tail. `QED`

Combining Lemmas 1.1 and 2.1 gives a finite combinatorial obstruction:
inside every proper shore of more than half the vertices, a rank-one exact
source admits no such orientation.  In particular, basis edges (rank-one
matrices supported on a single endpoint-color cell) are precisely the
rank-one edges with no killable endpoint, and every large shore whose
remaining edges have a one-demand orientation must contain a basis edge.

The indegree hypothesis is substantive.  Several noncoordinate factors at
one vertex need not have a common torus zero, so replacing it by a mere
``no basis edge'' condition would be invalid.

## 3. Scope

The obstruction is uniform in `|B|`, uses arbitrary asymmetric complex
matrices outside the rank-one corollary, and is unaffected by parallel
source aggregation.  It does not yet eliminate dense shores: a collection
of higher-rank bilinear forms, or several forced rank-one demands at one
vertex, can have no common toric zero.  Its intended role is as the exact
large-cut condition that a matching-theoretic or directed-anchor argument
must violate.
