# Pfaffian supports reduce to a signed six-site problem, not the hafnian one

## Outcome

A Pfaffian orientation over characteristic zero does give a uniform Schur
reduction.  Starting from a hypothetical realization on any even number of
vertices whose aggregate support is Pfaffian, one obtains on six vertices
an alternating matrix of bilinear forms whose **Pfaffian** is a ternary GHZ
polynomial with three nonzero coefficients.

This does not yet contradict the proved six-site hafnian theorem.  The
six-vertex Pfaffian matching signs cannot be absorbed into edge matrices,
even by arbitrary nonzero complex scalars.  Moreover, an explicit planar,
3-connected, matching-covered eight-vertex support has a legal two-vertex
Schur pivot whose effective six-vertex support contains `K_(3,3)` and is
therefore non-Pfaffian.  Thus Pfaffianity of the original support is not
inherited by the response graph.

On the complementary graph-theoretic branch, non-Pfaffianity also does not
supply a clean six-site tensor minor.  In the bipartite case Little's theorem
supplies a `K_(3,3)` matching minor, but `K_(4,4)` shows that the conformal
minor can have unavoidable cross-edge contamination.  For general supports
there are even infinitely many matching-minor-minimal non-Pfaffian graphs.

## 1. Exact signed Schur reduction

Let `G` be a graph on `B={1,...,n}`, let `n` be even, and suppose `G` has a
Pfaffian orientation.  Equivalently, after fixing the vertex order there
are signs `epsilon_uv in {+1,-1}` and one global sign `sigma` such that

\[
 \operatorname{sgn}(M)\prod_{uv\in M}\epsilon_{uv}=\sigma
       \qquad(M\in\operatorname{PM}(G)),                  \tag{1}
\]

where `sgn(M)` is the sign of the matching term in the ordinary Pfaffian
expansion.

Let `A_uv` be arbitrary endpoint-ordered `3 by 3` matrices supported on
`G`, and introduce a three-vector `x_v` at each vertex.  Form the alternating
scalar matrix

\[
 B(x)_{uv}=\epsilon_{uv}x_u^TA_{uv}x_v\quad(u<v),
 \qquad B(x)_{vu}=-B(x)_{uv}.                              \tag{2}
\]

Equation (1) gives the polynomial identity

\[
                         \operatorname{Pf}B(x)
       =\sigma\,H_n(A)(x).                                 \tag{3}
\]

Assume hypothetically that `H_n(A)=Delta_(n,3)`.  Then `Pf B(x)` is a
nonzero polynomial.  Pfaffian expansion at one vertex proves the following
standard flag fact: a nonsingular alternating matrix over a field has a
nonsingular principal submatrix of every smaller even order.  Apply this
over the rational function field in the `x` variables and choose a principal
set `P` of cardinality `n-6` with

\[
                         \operatorname{Pf}B(x)[P]\ne0.     \tag{4}
\]

The coordinate torus is Zariski dense, so the variables at `P` may be
specialized to vectors `xi_p in (C^*)^3` while keeping (4) nonzero.  Let
`R=B setminus P`, `|R|=6`, and write the specialized matrix as

\[
 B=\begin{pmatrix}M&E\\-E^T&D\end{pmatrix},
 \qquad d=\operatorname{Pf}M\ne0.                         \tag{5}
\]

The Pfaffian Schur complement is

\[
                         N=D+E^TM^{-1}E.                  \tag{6}
\]

Since `M^(-1)` is alternating, `N` is alternating and has zero diagonal.
Every column `E_r` is linear in `x_r`; hence for `r ne s`, the entry `N_rs`
is still an arbitrary bilinear form in `x_r,x_s`.  Congruence by the block
unitriangular matrix with upper-right block `-M^(-1)E` gives

\[
                         \operatorname{Pf}B
                    =d\operatorname{Pf}N.                 \tag{7}
\]

Specializing the target in (3) therefore yields

\[
 \operatorname{Pf}N(x_R)
   =\sum_{i=0}^2\lambda_i\prod_{r\in R}x_{r,i},
 \qquad
 \lambda_i={\sigma\over d}\prod_{p\in P}\xi_{p,i}\ne0. \tag{8}
\]

One diagonal change of variables at one remaining vertex normalizes the
three `lambda_i` to one.  We have proved:

**Proposition 1.1 (Pfaffian-support reduction).**  A characteristic-zero
realization of `Delta_(n,3)` on a Pfaffian support, for any even `n>=6`,
would imply a six-site **transverse Pfaffian** realization of
`Delta_(6,3)`.

The conclusion is signed.  In (8), the fifteen matching terms carry their
Pfaffian permutation signs.  The arbitrary-complex six-site theorem proved
in `proofs/low-rank-graph-laurent-obstruction.md` concerns the unsigned
hafnian sum and therefore cannot be substituted at this point.

## 2. The six-site sign holonomy cannot be gauged away

The gap is not a choice of convention.  On vertices `0,...,5`, consider
the three positive-sign Pfaffian matchings

\[
\begin{aligned}
 A_1&=01|25|34,&A_2&=02|14|35,&A_3&=03|15|24,
\end{aligned}                                               \tag{9}
\]

and the three negative-sign matchings

\[
\begin{aligned}
 B_1&=01|24|35,&B_2&=02|15|34,&B_3&=03|14|25.
\end{aligned}                                               \tag{10}
\]

The two triples use exactly the same edge multiset:

\[
                         A_1\sqcup A_2\sqcup A_3
                    =B_1\sqcup B_2\sqcup B_3.             \tag{11}
\]

If nonzero complex edge scalars `t_e` could turn Pfaffian signs into
unsigned signs, multiplying the three equations
`prod_(e in M)t_e=sgn(M)` for (9) would give `+1`, while multiplying them
for (10) would give `-1`.  Equation (11) makes the two left sides equal, a
contradiction.  Thus not even roots of unity or arbitrary complex phases
remove the sign pattern.

This is the smallest exact obstruction that a signed six-site theorem has
to overcome.  It is the multiplicative sign holonomy absent in the
characteristic-two Schur reduction.

## 3. A planar pivot can create a non-Pfaffian response

There is also no graph-level inheritance statement for the effective
support.  Let `R={0,...,5}` span the cycle `C_6`.  Add vertices `p,q`, the
edge `pq`, the edges from `p` to `0,1,2`, and the edges from `q` to `3,4,5`.
Call the resulting graph `G_8`.

The graph is planar, 3-connected, matching-covered, and has minimum degree
three.  A planar rotation is

\[
\begin{array}{c|c}
0&1,p,5\\1&0,2,p\\2&1,3,p\\3&2,4,q\\4&3,5,q\\5&4,0,q\\
p&q,0,1,2\\q&5,p,3,4.
\end{array}                                                 \tag{12}
\]

Its seven perfect matchings cover every edge.

Give `pq` scalar weight one, every star edge scalar weight one, and every
edge of the boundary cycle weight two.  Pivot on `P={p,q}`.  In the order
`p,q`,

\[
 M=\begin{pmatrix}0&1\\-1&0\end{pmatrix}.                 \tag{13}
\]

The boundary column at `r` is `(1,0)^T` for `r in {0,1,2}` and `(0,1)^T`
for `r in {3,4,5}`.  Therefore the Schur term in (6) is nonzero on every
pair joining these two triples.  The effective support contains the
spanning `K_(3,3)`.

That support is non-Pfaffian.  Indeed, its six bipartite perfect matchings
split into the three even and three odd permutations.  The product of the
three even matching monomials and the product of the three odd matching
monomials both use every `K_(3,3)` edge exactly once, but their determinant
sign products are opposite.  This is the bipartite analogue of (9)--(11).

Thus a perfectly good planar Pfaffian support can acquire a non-Pfaffian
six-vertex response after the principal pivot required by Proposition 1.1.
The signs in (8) are essential Schur data, not an orientation which can be
forgotten.

## 4. Why the non-Pfaffian branch has no clean graph reduction

For a bipartite graph, Little's theorem says that non-Pfaffianity is
equivalent to containing `K_(3,3)` as a matching minor: a central even
subdivision is selected and its degree-two vertices are bicontracted.  Both
operations are graph operations.  Selecting the subgraph deletes all other
active edges, which is not a valid operation on a Krenn tensor.

`K_(4,4)` is the sharp eight-vertex warning.  Delete one vertex from each
shore.  The remaining six vertices span a central `K_(3,3)` and the two
deleted vertices have their complementary edge.  Nevertheless there are
six support edges crossing between the minor and the complementary pair.
The pair-cap formula therefore has a full two-cross-edge boundary sector;
the conformal perfect matching does not isolate the minor.  Moreover
`K_(4,4)` has no nontrivial tight cut, so tight-cut contraction cannot
remove this contamination.  These facts are independent of matrix values.

For nonbipartite supports even the fixed-minor statement fails.  Norine and
Thomas, *Minimally non-Pfaffian graphs*, exhibit an infinite family of
non-Pfaffian graphs minimal under the matching-minor relation; the Petersen
graph is already a ten-vertex minimal example.  Hence no theorem saying
that every general non-Pfaffian support contains one fixed six-vertex
non-Pfaffian matching minor can hold.

The exact finite audit
`computations/verify_pfaffian_support_obstructions.py` checks (9)--(11),
the planarity, 3-connectivity, matching coverage, and Schur support of
`G_8`, and all odd shores and conformal six-sets of `K_(4,4)`.

## 5. Precise remaining lemma

The Pfaffian-support route would close if one proved either of the following
genuinely algebraic statements:

1. no six-site alternating matrix of arbitrary inter-site bilinear forms
   has transverse Pfaffian equal to `Delta_(6,3)` over `C`; or
2. the particular Schur complement in Proposition 1.1 admits an unsigned
   edge realization despite the holonomy (11).

The second statement is false as a graph/sign assertion by Section 3 and
would have to use special coefficient cancellations forced by the target.
The first is a new signed six-site obstruction, not a consequence of the
current hafnian theorem.  On the non-Pfaffian branch, a matching minor is
likewise insufficient unless its edge deletions and bicontractions are
implemented by a contamination-free tensor identity.
