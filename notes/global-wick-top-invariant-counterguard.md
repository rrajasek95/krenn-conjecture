# Global Wick top invariants do not separate ternary GHZ

## Outcome

There is no contraction-stable polynomial identity of the **top multilinear
Wick tensor alone** that can prove the ternary Krenn obstruction.  For every
even (n\geq6), the tensor

\[
                   \Delta_{n,3}=\sum_{c=0}^2e_c^{\otimes n}
\]

is in the ordinary and Zariski closure of top moments of centered Wick
systems with pairwise (3\times3) cross-covariances.  The degenerating
covariances can simultaneously be chosen

* rank one and same-colour on every nonzero pair block, and
* globally nonsingular, with determinant exactly
  ( (-1)^{3n/2}\in\{1,-1\}) for every finite parameter value.

Consequently the no-go includes every polynomial obtained after fixed local
linear maps, flattenings, tensor products, permutations, symmetrizations,
antisymmetrizations, and contractions.  It also includes rational identities
whose denominator is nonzero at the target.

Allowing arbitrary endpoint-dependent block projections makes the route even
less rigid: at every arity at least three, ternary GHZ is an **exact** local
image of a product of two Bell-pair Gaussian/matchgate signatures per link.
Thus an invariant stable under arbitrary block projections cannot distinguish
the target at all.  This exact image is not a Krenn realization, because its
internal block maps accept several incidences rather than exactly one.  The
special one-hot incidence condition is precisely the information that a
viable source-relative argument must retain.

The result is a counterguard, not a proof of Krenn's conjecture.  It rules out
the proposed fast route unless the invariant detects non-closed finite-source
membership, uses lower Wick sectors together with the actual covariance, or
exploits the one-hot incidence maps.

## 1. The top moment is the matrix-hafnian tensor

Let (V_v=\mathbb C^3) and let (A_{uv}\in V_u\otimes V_v) be arbitrary
for (u<v).  Make a symmetric global covariance (Z(A)) on
(\bigoplus_vV_v) by putting (A_{uv}) in its (uv) block and
(A_{uv}^{T}) in its (vu) block; the same-site blocks are zero.  Algebraic
Wick expansion of the centered variables gives

\[
 \mathbb E_Z[X_{1,c_1}\cdots X_{n,c_n}]
   =\sum_{M\in\operatorname {PM}([n])}
       \prod_{uv\in M}A_{uv}(c_u,c_v).                    \tag{1}
\]

No positivity or conjugation is used here: (1) is the polynomial Wick
functional for an arbitrary complex symmetric covariance.  Equivalently,
the complete top tensor is

\[
 H_n(A)=\sum_{M\in\operatorname {PM}([n])}
               \bigotimes_{uv\in M}A_{uv}.                \tag{2}
\]

This is exactly the aggregate Krenn tensor.  Arbitrary endpoint colours and
parallel-source cancellation are already included in the arbitrary matrices
(A_{uv}).

## 2. A nonsingular Laurent boundary at six sites

On sites (0,\ldots,5), use the following nine rank-one diagonal blocks.
An entry (uv:c,t^a) means
(A_{uv}=t^a e_c\otimes e_c):

\[
\begin{array}{c|ccc}
c=0&03:t&12:t^{-1}&45:1\\
c=1&14:1&02:1&35:1\\
c=2&25:1&01:1&34:1.
\end{array}                                                  \tag{3}
\]

The uncoloured support is a triangular prism.  Its complete list of perfect
matchings consists of the three displayed colour classes and

\[
                             03\mid14\mid25.                \tag{4}
\]

The colour-class products are one.  Matching (4) has product (t) and
word (012012).  Therefore, for every (t\ne0),

\[
                 H_6(A(t))=\Delta_{6,3}+t e_{012012}.       \tag{5}
\]

The covariance is nonsingular despite the pole in (3).  After the ports are
ordered by colour, it is the direct sum of the weighted adjacency matrices
of the three colour-class perfect matchings.  A weighted matching on six
ports has determinant ((-1)^3) times the square of its edge product.
All three products are one, so

\[
                              \det Z(A(t))=-1.              \tag{6}
\]

Thus covariance nonsingularity, even with determinant bounded away from
zero, does not turn the output image into a closed set.

## 3. Uniform vertex-to-triangle propagation

The preceding boundary propagates by two sites at a time.  Suppose a cubic
graph is properly edge-coloured by (0,1,2), with the colour classes as
perfect matchings.  Give its edges integer valuations (\nu(e)), normalize
each colour class to total valuation zero, and suppose every other perfect
matching has positive valuation.

At a vertex (v), write (e_i=vu_i) for its incident colour-(i) edge.
Replace (v) by a triangle with vertices (s_0,s_1,s_2).  Join (u_i) to
(s_i) by a colour-(i) external edge, and colour the internal edge
(s_js_k) by the missing colour (i).  For arbitrary integers (a_i), set

\[
 \nu(u_is_i)=\nu(e_i)+a_i,
 \qquad \nu(s_js_k)=-a_i.                                  \tag{7}
\]

Every perfect matching of the expanded graph uses either one or three
external edges.

* In the one-external case, (u_is_i) is accompanied by its opposite
  internal edge.  Contracting the triangle gives one old matching containing
  (e_i), and (7) preserves its valuation exactly.
* In the three-external case, no internal edge is used and the valuation is
  shifted by (a_0+a_1+a_2).

There are finitely many three-external matchings.  Take (a_0=a_1=0) and
choose (a_2=L) large enough that all of them have valuation at least one.
The three colour classes use the first case, remain normalized, and are the
only zero-valuation matchings.  All other matchings have positive valuation.
The proper three-edge-colouring is also preserved.

Starting from (3), induction gives, for every even (n\geq6), a Laurent
family

\[
 H_n(A^{(n)}(t))=\Delta_{n,3}+\sum_{k\geq1}t^kT_k.          \tag{8}
\]

At every stage, every port ((v,c)) lies on exactly one colour-(c) edge.
The global covariance is therefore a weighted perfect-matching matrix in
each colour, and the normalized colour products give

\[
             \det Z(A^{(n)}(t))
                 =\prod_{c=0}^2(-1)^{n/2}
                    \left(\prod_{e\in P_c}t^{\nu(e)}\right)^2
                 =(-1)^{3n/2}.                             \tag{9}
\]

This proves the claimed nonsingular boundary uniformly.

## 4. No top-tensor polynomial or regular rational separator

Let (\mathcal W_n) be the image of the polynomial map
(A\mapsto H_n(A)).  Let (P) be a polynomial in the coordinates of the
top tensor and suppose (P(T)=0) for every (T\in\mathcal W_n).  Substitute
(8).  Although its source entries are Laurent monomials, its output has only
nonnegative powers, so

\[
                    P\!\left(H_n(A^{(n)}(t))\right)         \tag{10}
\]

is an ordinary polynomial in (t).  It vanishes for every (t\ne0), hence
also at zero.  Therefore

\[
                              P(\Delta_{n,3})=0.             \tag{11}
\]

Now let (F) be any construction from the top tensor using finitely many
fixed local linear maps, tensor products, permutations, contractions, and
linear symmetrizations.  Every coordinate of (F(T)) is polynomial in the
coordinates of (T).  A polynomial identity on (F(H_n(A))) therefore
pulls back to a polynomial (P(T)), and (11) applies.  This covers
flattening minors, exterior-power equations, polynomial rank tests, and
Grassmann--Pluecker or matchgate equations after eliminating all auxiliary
coordinates and retaining only fixed contractions of the top signature.

The same argument excludes a rational identity (P/Q=0) regular at the
target.  If (Q(\Delta_{n,3})\ne0), then
(Q(H_n(A^{(n)}(t)))\ne0) for generic nonzero (t).  Its numerator
vanishes on those points, so (11) again gives (P(\Delta_{n,3})=0).  A
rational invariant can escape only by having a pole on the target or by
retaining source data whose Laurent blow-up is visible.

## 5. Arbitrary blockwise local projections are even too expressive

There is a second, exact obstruction to importing a matchgate identity
through endpoint-dependent projections.  For any arity (r\geq3), place
two independent Bell pairs between each consecutive pair of blocks.  If
(d\in\{0,1\}^2) denotes their two common bits, the unprojected chain
signature is

\[
 \Gamma_r=
 \sum_{d_1,\ldots,d_{r-1}\in\{0,1\}^2}
 |d_1\rangle\otimes|d_1,d_2\rangle\otimes\cdots\otimes
 |d_{r-2},d_{r-1}\rangle\otimes|d_{r-1}\rangle.            \tag{12}
\]

This is a product of disjoint two-leg Gaussian/matchgate signatures.  Choose
three codewords

\[
                    d_0=00,\qquad d_1=01,\qquad d_2=10.     \tag{13}
\]

At an endpoint, send (|d_c\rangle\) to (e_c) and kill the fourth word.
At every internal block, set

\[
 P_j|d,d'\rangle=
 \begin{cases}
 e_c,&d=d'=d_c,\\
 0,&\text{otherwise}.
 \end{cases}                                                \tag{14}
\]

Only assignments with
(d_1=\cdots=d_{r-1}=d_c) survive, once for each (c).  Hence exactly

\[
                    (P_1\otimes\cdots\otimes P_r)\Gamma_r
                         =\sum_{c=0}^2e_c^{\otimes r}.       \tag{15}
\]

It follows formally that no identity possessed by Gaussian/matchgate
signatures and preserved under **arbitrary** blockwise local linear maps can
be violated by ternary GHZ.  Endpoint- or site-dependent choices do not
help; (14) already permits different maps at every block.

Equation (15) is deliberately not claimed as a Krenn counterexample.  A
Krenn site projection accepts configurations retaining exactly one incident
edge occurrence.  An internal map in (14) accepts four virtual half-edges,
two on each neighboring link.  Forgetting this one-hot constraint enlarges
the category enough to contain GHZ exactly.

## 6. Exact audit and surviving route

Run

```text
python3 computations/verify_global_wick_top_invariant_counterguard.py
```

The dependency-free checker independently enumerates every perfect matching
in the expansion through (n=18), represents all weights by integral
Laurent valuations, verifies that the constant term is exactly ternary GHZ,
and checks every other matching has positive valuation.  It constructs the
full (3n\times3n) covariance at (t=2) and computes its determinant by
exact rational elimination.  It also enumerates the Bell-chain projection
through arity ten.  Normal, optimized, and isolated standard-library runs
all produce digest

```text
d5d3199b39bfa81cfba33ebaf38144846488e6cc051cc6a6be12d5ac649bd07c
```

The fast Wick/matchgate route therefore leaves one narrow possibility: an
identity of the **pair** ((A,H_n(A))), involving lower Wick sectors or
nontransversal coordinates, that remains meaningful only on the exact
one-hot Krenn incidence chart and controls the Laurent pole in (3).  Such an
identity is source-relative and non-closed; it is not a contraction-stable
identity of the top tensor.
