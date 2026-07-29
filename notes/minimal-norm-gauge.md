# Minimal-norm gauges: exact consequences and their limit

Let (B) have even cardinality (n), let (V_v=mathbb C^q), and put

\[
 W=\bigoplus_{u<v}V_u\otimes V_v,
 \qquad
 \Phi(A)=H_B(A)=\sum_{M\in\operatorname {PM}(B)}
                     \bigotimes_{uv\in M}A_{uv}.
\tag{1}
\]

All norms and adjoints below are for the standard Hermitian structures.
This note records what minimizing the Frobenius norm really adds to the
target-torus reduction.  There are two useful additions:

* every star is the least-norm solution of an exact linear system, with no
  regularity assumption on the fiber; and
* after allowing the target to range over its closed local-(GL) orbit,
  one obtains a fully isotropic representative and hence positive-definite
  operator-scaling equations on an exact representative.

Neither conclusion by itself forces individual edges to have rank one.  An
exact binary active-rank-two example tests the first warning, and a uniform
three-color Fourier model tests the second.

## 1. A minimum exists, but ordinary Lagrange multipliers are unsafe

The exact fiber

\[
                  \mathcal F=\Phi^{-1}(\Delta_{B,q}),
 \qquad \Delta_{B,q}=\sum_{i=0}^{q-1}e_i^{\otimes B},
\tag{2}
\]

is closed.  If it is nonempty, the continuous proper function
(A\mapsto\lVert A\rVert^2) therefore attains a minimum on it.

At a singular point of a polynomial fiber, a vector in
(\ker D\Phi_A) need not integrate to a curve in the fiber.  Thus it is not
legitimate, without a constraint qualification, to assert that a closest
point is orthogonal to the entire Zariski tangent space.  The matching map
does, however, have large blocks on which it is *exactly linear*.  Those
blocks give unconditional normal equations.

Call a family (E_0\subseteq\binom B2) intersecting if no two of its edges
are vertex-disjoint.  No perfect matching contains two members of (E_0).
With all edges outside (E_0) fixed, (1) consequently has the affine form

\[
 \Phi(A)=R_{E_0}+L_{E_0}((A_e)_{e\in E_0}),
 \qquad
 L_{E_0}((Z_e))=\sum_{e\in E_0}Z_e\otimes H_{B\setminus e}(A),
\tag{3}
\]

where tensor slots are restored to their positions.  The cofactors in (3)
do not involve an edge of (E_0), because every such edge meets (e).

**Lemma 1.1 (exact block normal equation).**  If (A) minimizes the norm
on (2), then, for every intersecting edge family (E_0),

\[
        (A_e)_{e\in E_0}\perp\ker L_{E_0},
 \qquad
        (A_e)_{e\in E_0}\in\operatorname {ran}L_{E_0}^*.
\tag{4}
\]

Equivalently, the displayed block of (A) is the unique least-norm point
among all blocks giving the same value in (3).

**Proof.**  If (Z\in\ker L_{E_0}), then (A+tZ) remains in the exact
fiber for every (t\in\mathbb C), not merely to first order.  Minimality of
the quadratic norm gives (A_{E_0}\perp Z).  In finite dimensions
((\ker L)^perp=\operatorname {ran}L^*), and strict convexity of the norm
on an affine space gives uniqueness.  (square)

The most useful case is the full star at (v).  Every perfect matching uses
exactly one star edge, so (R_{E_0}=0).  Define

\[
 L_v:\bigoplus_{u\ne v}V_v\otimes V_u\longrightarrow
       \bigotimes_{x\in B}V_x,
 \qquad
 L_v((Z_{vu}))=\sum_{u\ne v}Z_{vu}\otimes H_{B\setminus\{v,u\}}(A).
\tag{5}
\]

Then a minimum satisfies

\[
 L_v(A_{v*})=\Delta_{B,q},
 \qquad A_{v*}=L_v^*\Lambda_v                         \tag{6}
\]

for some output tensor (Lambda_v).  In particular, if
(H_{B\setminus\{u,v\}}(A)=0), then (A_{uv}=0): deleting that edge leaves
the output unchanged and strictly lowers the norm unless the edge was
already zero.  Thus every nonzero edge at a minimum is tensor-active.

The same argument applies to a triangle, the other maximal type of
intersecting edge family in a complete graph.  It is stronger than a formal
KKT equation precisely because the kernel directions in (4) are genuine
lines in the fiber even at a singular point.

## 2. The exact-target stabilizer gives only diagonal balance

For (n\ge3), the Lie algebra of the local-(GL) stabilizer of
(\Delta_{B,q}) contains no off-diagonal directions.  Indeed, if

\[
                         \sum_v X_v^{(v)}\Delta_{B,q}=0,
\tag{7}
\]

then the coefficient having color (j\ne i) at (v) and color (i) at
every other vertex is ((X_v)_{ji}), so every off-diagonal entry vanishes.
The all-(i) coefficient then gives

\[
                         \sum_v(X_v)_{ii}=0\quad(i=0,\ldots,q-1).
\tag{8}
\]

Conversely, diagonal tuples satisfying (8) annihilate the target.  Hence
minimizing along the local group orbit *inside the exact fiber* gives
exactly the already-known target-torus moment equations

\[
 \sum_{u\ne v}\sum_j|A_{v|u}(i,j)|^2=c_i
       \quad(v\in B),                                      \tag{9}
\]

where (A_{v|u}) is the matrix with its (v)-slot as the row slot.  There
is no hidden non-diagonal Kempf--Ness equation in the exact-target
stabilizer.  Any additional equation must use the nonlinear geometry of
the fiber, such as (4), or permit the target itself to move in its orbit.

## 3. A fully isotropic representative over the GHZ orbit

The latter option gives a stronger existence normal form.  Let

\[
 \mathcal G=left\{(g_v)\in\prod_{v\in B}GL(V_v):
                         \prod_v\det g_v=1\right\}.          \tag{10}
\]

Its Lie algebra consists of tuples ((X_v)) with
(sum_v\operatorname {tr}X_v=0).  The orbit

\[
                         \mathcal O=\mathcal G\Delta_{B,q}   \tag{11}
\]

is closed.  One quick proof is Kempf--Ness: the one-site reduced Gram
matrix of (Delta_{B,q}) is (I_q) at every site, and hence

\[
 \left.\frac d{dt}\right|_{t=0}
 \left\lVert(e^{tX_v})_v\Delta_{B,q}\right\rVert^2
 =2\sum_v\operatorname {tr}X_v=0                           \tag{12}
\]

for every Hermitian element of the Lie algebra.  Thus the target is a
minimal vector and its complex reductive orbit is closed.  Equivalently,
(mathcal O) is the usual (prod_vSL(V_v))-orbit: decomposing each
(g_v) into a scalar and an (SL) matrix leaves a product scalar which is
a (q)-th root of unity, and that scalar matrix belongs to (SL(V_v)) at
one site.

The map (Phi) is (mathcal G)-equivariant, so

\[
                         \mathcal Z=\Phi^{-1}(\mathcal O)   \tag{13}
\]

is closed and (mathcal G)-invariant.  It is nonempty whenever the exact
fiber is nonempty.

For (C_{uv}\in V_u\otimes V_v), let

\[
 \rho_v(C_{uv})=\operatorname {Tr}_{V_u}
                         |C_{uv}\rangle\langle C_{uv}|
\tag{14}
\]

denote the reduced Gram operator in the (v)-slot, and put

\[
                         R_v(C)=\sum_{u\ne v}\rho_v(C_{uv}).\tag{15}
\]

**Theorem 3.1 (full isotropic-orbit normal form).**  If
(Phi^{-1}(\Delta_{B,q})\ne\varnothing), there is (C\in W) such that

\[
 \Phi(C)\in\mathcal G\Delta_{B,q},
 \qquad
                         R_v(C)=cI_q\quad\hbox{for every }v,\tag{16}
\]

with one common constant (c>0).  The point (C) may simultaneously be
chosen to satisfy all block normal equations (4), with its own output in
place of (Delta).

**Proof.**  Minimize (lVert C\rVert^2) on the nonempty closed set
(mathcal Z).  For Hermitian (X=(X_v)) with
(sum_v\operatorname {tr}X_v=0), the curve (e^{tX}C) remains in
(mathcal Z).  Differentiating at the minimum gives

\[
                         0=2\sum_v\operatorname {tr}(X_vR_v(C)).\tag{17}
\]

Taking one (X_v) traceless at a time shows (R_v(C)=c_vI_q).  Taking
(X_v=t_vI_q) with (sum_vt_v=0) shows all (c_v) are equal.  Since
(Phi(C)\ne0), also (C\ne0), so (c>0).  Finally, the fixed-output
block variations used in Lemma 1.1 stay inside (mathcal Z), proving the
last assertion.  (square)

Thus the incident matrices form a tight operator frame at every vertex:

\[
 \sum_{u\ne v}\lVert C_{v|u}^*x\rVert^2=c\lVert x\rVert^2,
 \qquad
 \lVert C\rVert^2=\frac{nqc}{2},
 \qquad
 \lVert C_{uv}\rVert_{\rm op}^2\le c.                     \tag{18}
\]

The target in (16) can be pulled back to the coordinate GHZ tensor at the
price of non-Euclidean local metrics.  Write
(Phi(C)=g\Delta_{B,q}) with (g=(g_v)\in\mathcal G), set
(A=g^{-1}C), and put (P_v=g_v^*g_v>0).  Orient every edge matrix so its
(v)-slot is the row slot.  Then

\[
 \Phi(A)=\Delta_{B,q},\qquad \prod_v\det P_v=1,
\tag{19}
\]

and (16) is exactly

\[
 \boxed{\displaystyle
 \sum_{u\ne v} A_{v|u}P_u^{\mathsf T}A_{v|u}^*
                         =cP_v^{-1}\quad(v\in B).}
\tag{20}
\]

Equation (20) is a genuine strengthening of diagonal target-torus balance:
it includes all off-diagonal Gram equations, but in unknown positive local
metrics.  It is also invariant under arbitrary asymmetric endpoint
decorations and already works with the aggregated edge matrices.

## 4. Exact and support-level adversarial tests

First, exactness and tensor activity do not make individual matrices rank
one.  The binary six-vertex source

\[
\begin{array}{c|c@{\qquad}c|c}
01&E_{00}&23&I_2\\
02&-e_0e_1^{\mathsf T}&13&e_0e_1^{\mathsf T}\\
45&E_{00}&05&E_{11}\\
12&E_{11}&34&E_{11}
\end{array}                                                   \tag{21}
\]

has matching tensor (Delta_{6,2}), every displayed edge has a nonzero
four-site cofactor, and (A_{23}) has rank two.  It is not a norm minimum,
which shows that the word "minimum" in Lemma 1.1 is substantive.  With all
non-star edges fixed, the original star at vertex (2) has squared norm
four.  Replacing it by

\[
                         A_{12}=E_{11},\qquad A_{23}=E_{00},\tag{22}
\]

and setting its other edges to zero preserves the output exactly and has
star norm two.  The remaining (A_{13}) is then inactive and can be
deleted, leaving the standard two-perfect-matching realization of norm
squared six.

Second, even the full isotropy equations (16), coordinate anchors, lack of
singleton fibers, and full-rank non-anchor edges are mutually compatible
for every even (n\ge6).  Choose five edge-disjoint one-factors

\[
                         P,P',Q_0,Q_1,Q_2\subset K_n.        \tag{23}
\]

Let (F=(\omega^{ij})_{0\le i,j<3}), where
(omega^2+\omega+1=0).  Put (F) on every edge of (P\cup P'), put
(E_{ii}) on every edge of (Q_i), and put zero elsewhere.  Since

\[
                         FF^*=F^*F=3I_3,                    \tag{24}
\]

each vertex has

\[
                         R_v=2(3I_3)+\sum_iE_{ii}=7I_3.     \tag{25}
\]

Every coloring has a nonzero matching monomial on each of (P,P'), every
vertex/color port has a same-color coordinate anchor, and the two (F)
edges at a vertex are invertible.  This model is deliberately not claimed
to have matching tensor (Delta_{n,3}); rather, it proves that neither the
isotropic moment equations nor their usual Boolean support companions can
yield a rank-one conclusion or a three-color contradiction without using
the exact cancellation equations.  Scaling all five families also shows
that (16) alone permits arbitrary positive values of (c).

There is also a uniform variant satisfying all three *complete*
constant-color equations.  Let \(S\) be the cyclic \(3\times3\)
permutation matrix.  Put \(S\) on \(P\), \(S^2\) on \(P'\), and retain
\(E_{ii}\) on \(Q_i\).  Then

\[
 R_v=SS^*+S^2(S^2)^*+\sum_iE_{ii}=3I_3.
\]

Both permutation matrices have zero diagonal.  Therefore, in constant
color \(i\), the only supported perfect matching is \(Q_i\), and its
coefficient is exactly one.  This works for every even \(n\ge6\).
It may have singleton mixed fibers; the Fourier model supplies the
complementary stronger support test.

For (n=6), take

\[
\begin{aligned}
 P&=\{01,23,45\},&P'&=\{05,12,34\},\\
 Q_0&=\{02,14,35\},&Q_1&=\{03,15,24\},&
 Q_2&=\{04,13,25\}.
\end{aligned}                                                \tag{26}
\]

There is a useful strengthening at six vertices.  Multiply the matrices on
edges \(05,34,04,25\), respectively, by

\[
                         \omega^2,\ \omega^2,\ \omega^2,\ \omega, \tag{26a}
\]

and leave all other edge phases equal to one.  Unit phases preserve
(24)--(25) and every support assertion.  Moreover the product of the
phases on \(P,P',Q_0,Q_1,Q_2\) is respectively
\(1,\omega,1,1,1\).  Each constant-color fiber has four supported
matchings.  Besides its anchor \(Q_i\), their three contributions are
\(1,\omega,\omega^2\), in some order.  Consequently the *complete*
constant coefficient is exactly

\[
                         1+(1+\omega+\omega^2)=1            \tag{26b}
\]

for every color.  Thus full isotropy, three exactly normalized constant
fibers, coordinate anchors, at least two terms in every mixed fiber, and
invertible non-anchor matrices are all simultaneously feasible.  Only the
vanishing of the mixed coefficient sums is absent.

The exact audit `computations/verify_minimal_norm_gauge.py` checks (21)--
(22), all binary coefficients and cofactors, the phased cyclotomic Gram
identities (24)--(26b), every constant coefficient, and the support
assertions for (26).

## 5. Consequence for the uniform route

The minimal-norm method gives the rigorous simultaneous normal form
(4), (16), or equivalently (4), (19)--(20).  What remains is not a further
formal moment-map calculation: one would need a theorem combining the
least-star adjoint equations with the *matching coefficient cancellations*
to contradict a tight operator frame when (q=3,n\ge6).  The Fourier model
shows why an argument using only ranks, anchors, support multiplicity, and
the moment matrices cannot do so.

Finally, border degenerations do not evade the minimum.  If
(A(t)) is a family with (Phi(A(t))\to\Delta_{B,q}) but the exact fiber is
empty, then (lVert A(t)\rVert\to\infty) along every such convergent-output
sequence: a bounded subsequence would have a convergent source subsequence,
and continuity of (Phi) would produce an exact preimage.  This explains
the norm blow-up in the known prism border family, but supplies no finite
norm bound capable of excluding a hypothetical exact point.

## 6. All exact-linear blocks, and the nonlinear square-move barrier

There are no missing edge blocks on which the matching polynomial is
*structurally* affine-linear, independently of the values on the other
edges.  Indeed, such a block has matching number at most one, and hence is
pairwise intersecting.  (At a special point, vanishing cofactors can of
course create additional accidental affine directions.)  If all the
block's edges share a vertex it lies in a star.
Otherwise it contains \(ab,ac\), and an edge avoiding \(a\); that edge must
be \(bc\).  Every edge meeting all three of \(ab,ac,bc\) belongs to this
triangle.  Thus the maximal blocks are exactly

\[
 \{vu:u\ne v\}
 \quad\text{and}\quad
 \{ab,bc,ca\}.                                             \tag{27}
\]

This classification makes it possible to test the complete collection of
block equations, rather than only selected stars.  In the phased
six-vertex Fourier/anchor model (26)--(26a), every one of the six star
maps has rank \(45\), and every one of the twenty triangle maps has rank
\(27\).  These ranks
are certified over \(\mathbf F_7\): specialize
\(\mathbf Z[\omega]\to\mathbf F_7\) by \(\omega\mapsto2\), which is valid
because \(2^2+2+1=0\pmod 7\).  A full-rank minor after specialization is a
nonzero cyclotomic minor over \(\mathbf C\).  Hence every equation (4) is
automatic in this fully isotropic model, because every relevant kernel is
zero.

There is an even sharper infinitesimal check.  For arbitrary \(X\),

\[
 D\Phi_A[X]
   =\sum_e X_e\otimes H_{B\setminus e}(A).                 \tag{28}
\]

The exact same finite-field computation gives rank \(130\) for (28) in
that model; its domain has dimension \(15\cdot9=135\).
The five-dimensional kernel is exactly the universal scalar vertex gauge

\[
 X_{uv}=(p_u+p_v)A_{uv},\qquad \sum_vp_v=0.                \tag{29}
\]

The inclusion of (29) in the kernel follows term by term, since every
perfect matching uses each vertex once.  The rank computation proves
equality.  In particular this isotropic point has no additional
fixed-output infinitesimal square move.

In fact the phased model (26a) is an exact smooth local minimum on the
fiber of its own output.  Let

\[
 \mathcal S=\{(\lambda_v)\in(\mathbf C^*)^6:
                         \prod_v\lambda_v=1\}.
\]

The action \(A_{uv}\mapsto\lambda_u\lambda_vA_{uv}\) fixes every matching
tensor term by term.  Its orbit through the model has dimension five and,
by the rank-\(130\) computation, its tangent space is the entire kernel of
\(D\Phi_A\).  Choose \(130\) output coordinates whose differentials are
independent.  Their common level set is a smooth five-dimensional
manifold near \(A\).  The \(\mathcal S\)-orbit is contained in it and has
the same tangent dimension, so the inverse function theorem makes the
orbit an open neighborhood of \(A\) in that level set.  Hence the full
fixed-output fiber agrees locally with this orbit.

Writing \(|\lambda_v|=e^{p_v}\), with \(\sum_vp_v=0\), its norm is

\[
 f(p)=\sum_{u<v}e^{2(p_u+p_v)}\|A_{uv}\|^2.
\]

Every vertex is incident to two Fourier matrices of squared norm \(9\)
and three anchors of squared norm \(1\), so every weighted degree is
\(21\).  Therefore \(\nabla f(0)\) vanishes on \(\sum_vp_v=0\), and

\[
 D^2f(0)[p,p]
 =4\sum_{u<v}(p_u+p_v)^2\|A_{uv}\|^2>0
\]

for nonzero real \(p\) in that hyperplane.  Phase directions preserve the
norm.  Thus \(A\) is a local norm minimum of
\(\Phi^{-1}(\Phi(A))\), modulo its compact phase orbit.  This supplies an
explicit stationary configuration satisfying full isotropy, all three
exact constant-coefficient equations, and every block normal equation.
Its mixed coefficient at coloring \(010000\), for example, is
\(1+\omega\ne0\).  The GHZ zero equations are exactly what separates this
local minimum from a putative counterexample.

This is not merely a numerical rank claim.  The verifier performs exact
Gaussian elimination in \(\mathbf F_7\), so the same nonzero-minor
argument proves the asserted complex ranks.  The model does not have GHZ
output, and therefore it does not rule out a theorem that uses the GHZ
cancellation equations.  It does show that full isotropy, all block
normal equations, and nondegenerate cofactors do not by themselves imply
the existence of a norm-decreasing direction.

There is a sharper warning about using only one cancellation cycle.  In
the same phased model, select (P) as the color-zero constant monomial,
(Q_1) as the color-one monomial, and (Q_2) as the color-two monomial.
Their decorated union contains the fourth matching

\[
                    M=\{04,15,23\},
\qquad c=(2,1,0,0,2,1).                                  \tag{29a}
\]

The selected term has value \(\omega^2\).  The complete nonzero list in
this mixed fiber is

\[
 \begin{array}{c|c}
 \{01,23,45\}&\omega\\
 \{04,15,23\}&\omega^2\\
 \{05,12,34\}&1,
 \end{array}
 \qquad \omega+\omega^2+1=0.                             \tag{29b}
\]

Thus the selected-three-factors theorem, an actual vanishing mixed
coefficient, and two external cancellation mates all occur at the smooth
strict local minimum just described.  In particular, a single vanishing
selected-factor cycle does not force an extra tangent direction, an
integrable square move, or norm descent.  Any variational contradiction
specific to GHZ must use the *simultaneous* vanishing of every mixed
fiber (or a consequence coupling several such fibers), not merely the
existence of the cycle supplied by one choice of three constant terms.

The corresponding general local barrier is worth isolating.  Let
(T_Delta) be the diagonal local torus fixing (Delta_{B,3}), and let
(mathfrak t_Delta A) denote its tangent space at an exact source (A).
Suppose (A) is a smooth point of its fixed-output fiber and

\[
                     \ker D\Phi_A=\mathfrak t_\Delta A.    \tag{29c}
\]

If (A) satisfies the target-torus moment equations (9), then (A) is a
local norm minimum on that fiber, modulo the compact phase torus.  Indeed,
smoothness and (29c) make the torus orbit an open neighborhood in the
fiber.  On its real part write the diagonal parameters as (x_{v,i}),
where (sum_vx_{v,i}=0).  Its norm is

\[
 f(x)=\sum_{u<v}\sum_{i,j}|A_{uv}(i,j)|^2
                         e^{2(x_{u,i}+x_{v,j})}.           \tag{29d}
\]

Equation (9) makes (0) a critical point, and (f) is convex.  The
kernel of its Hessian consists exactly of parameters acting trivially on
every supported source coordinate; after quotienting by that point
stabilizer and by phases, the minimum is strict.  Consequently a general
GHZ variational proof cannot merely invoke balance plus the mixed
cancellations: it must prove that (29c) fails and that an additional
tangent actually integrates, or construct a global branch not visible in
the local tangent space.  A hypothetical smooth balanced GHZ preimage
with (29c) would have no norm-decreasing exact curve.

For completeness, an alternating-cycle deformation first appears at
second order.  If

\[
 A(t)=A+tX+\tfrac12t^2Y+O(t^3),\qquad \Phi(A(t))=\Phi(A),
\]

then necessarily

\[
 D\Phi_A[X]=0,\qquad
 D\Phi_A[Y]+D^2\Phi_A[X,X]=0,                              \tag{30}
\]

where

\[
 D^2\Phi_A[X,X]
 =2\!\!\sum_{\substack{e<f\\e\cap f=\varnothing}}
 X_e\otimes X_f\otimes H_{B\setminus(e\cup f)}(A).         \tag{31}
\]

At a norm minimum the same curve must satisfy

\[
 \operatorname {Re}\langle A,X\rangle=0,\qquad
 \|X\|^2+\operatorname {Re}\langle A,Y\rangle\ge0.         \tag{32}
\]

For a four-cycle \(12,23,34,41\), the quadratic obstruction (31) has the
two opposite-edge terms

\[
 2\bigl(
 X_{12}\otimes X_{34}
 +X_{23}\otimes X_{41}
 \bigr)\otimes H_{B\setminus\{1,2,3,4\}}(A),              \tag{33}
\]

with tensor slots restored in the evident order.  Thus a first-order
cycle cancellation is not an exact move: an acceleration \(Y\) exists
only if the tensor in (33) lies in \(\operatorname {ran}D\Phi_A\), and it
must additionally beat the positive \(\|X\|^2\) term in (32).  A straight
square move requires (33) itself to vanish.  Neither condition follows
from the star/triangle normal equations.

Finally, the obvious termwise-preserving edge scalings cannot provide the
desired strict decrease.  If numbers \(\beta_{uv}\) obey

\[
 \sum_{uv\in M}\beta_{uv}=0
 \quad\text{for every perfect matching }M,                 \tag{34}
\]

then comparison of matchings differing on four vertices gives the
four-point relations

\[
 \beta_{ab}+\beta_{cd}
 =\beta_{ac}+\beta_{bd}
 =\beta_{ad}+\beta_{bc}.
\]

For \(n\ge6\), these relations imply
\(\beta_{uv}=p_u+p_v\), with \(\sum_vp_v=0\); conversely these are all
solutions.  Hence (34) is precisely (29), not an urban-renewal symmetry.
Along its real one-parameter subgroup,

\[
 \|A(t)\|^2
 =\sum_{u<v}e^{2t(p_u+p_v)}\|A_{uv}\|^2.
\]

At a fully isotropic point its first derivative is
\(2qc\sum_vp_v=0\), while its second derivative is

\[
 4\sum_{u<v}(p_u+p_v)^2\|A_{uv}\|^2\ge0.                  \tag{35}
\]

The color-dependent diagonal target stabilizer has the same
sum-of-squares convexity.  More explicitly, suppose a universal
coordinatewise rescaling has exponents
\(\beta_{uv}^{ij}\), and suppose that for every coloring and every two
perfect matchings the sums of the selected exponents agree.  Comparing
the three pairings on four arbitrarily colored vertices gives

\[
 \beta_{ab}^{ij}+\beta_{cd}^{k\ell}
 =\beta_{ac}^{ik}+\beta_{bd}^{j\ell}
 =\beta_{ad}^{i\ell}+\beta_{bc}^{jk}.                     \tag{36}
\]

The four-point equations imply

\[
 \beta_{uv}^{ij}=x_{u,i}+x_{v,j}.                         \tag{37}
\]

For example, choose two auxiliary vertices and define \(x_{u,i}\) as
one half the sum of its two incident \(\beta\)'s minus the \(\beta\)
between the auxiliaries; (36) proves independence of the auxiliaries and
then (37).  Preserving the three nonzero constant coefficients requires

\[
 \sum_vx_{v,i}=0\qquad(i=0,1,2),                          \tag{38}
\]

so this entire class is exactly the diagonal target stabilizer.  If
\(d_{v,i}=\sum_{u,j}|A_{uv}(i,j)|^2=c_i\), its norm along this real
rescaling has

\[
\begin{aligned}
 f'(0)&=2\sum_{v,i}x_{v,i}d_{v,i}=0,\\
 f''(0)&=4\sum_{u<v}\sum_{i,j}
 |A_{uv}(i,j)|^2(x_{u,i}+x_{v,j})^2\ge0.                 \tag{39}
\end{aligned}
\]

Likewise, in the moving-output normal form (16), every Hermitian local
\(\mathcal G\)-direction has a convex norm profile.  Diagonalizing each
local generator turns that profile into a positive sum of exponentials;
isotropy makes its first derivative zero.  Thus local group directions
cannot supply a descent either.

Therefore a successful no-critical-point argument must extract a
genuinely nonlinear integrable direction from the exact GHZ cancellations,
change relative matching terms inside at least one zero fiber, and verify
both conditions (30)--(32).  There is no universal strict
norm-decreasing alternating-cycle variation.
