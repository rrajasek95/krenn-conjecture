# Blind source recovery with exact output verification and local conditioning

Research note, 2026-09-27. Numerical search, exact rational verification,
and written local analysis. Not Lean formalized or independently peer
reviewed. The Krenn–Gu paper is unchanged.

## 1. What is now implemented

The [previous inverse](quadratic-size-source-inverse-2026-09-27.md)
recovered a covariance and actual mean scales when the local mean lines
were supplied. The new program takes only the observed integer tensor. It searches
for those lines numerically, accepts them only after exact verification,
and then applies the covariance inverse.

On the recorded seven- and nine-site inputs it recovers complete sources
over the rational numbers. Every observed entry is verified exactly.
An eleven-site example verifies the mean lines only. A nine-site example
with larger covariance entries is also retained: the search fails to
find a verified tuple within its budget. Thus this is a blind search
with exact acceptance, not a globally convergent algorithm.

The distinction matters. A small floating-point residual is not an exact
solution, solver termination is not a zero residual, and a simple local
zero need not be the only zero on a particular input. The
[all-orders theorem](mean-direction-recovery-all-orders-2026-09-27.md)
establishes generic uniqueness separately. The certificates here do not
establish global mean-line uniqueness for each individual test input.

## 2. A normalized form of the mean-line equations

Let `T` be an odd-order tensor with three coordinates at each site.
A mean line is represented in a local chart by

$$
u_i=(1,h_{i,1},h_{i,2}),\qquad h_i\in\mathbb R^2.
$$

The position of the coordinate fixed to one can differ between sites.
The quotient matrix

$$
Q(h_i)=\begin{bmatrix}-h_{i,1}&1&0\\-h_{i,2}&0&1\end{bmatrix}
$$

kills `u_i`. The copy identity implies that the actual means satisfy
`(tensor_i Q(h_i))T=0`. This is a system of `2^n` equations in `2n`
chart coordinates. Changing coordinates does not require covariance data.

Using the raw quotient matrices makes the residual norm depend strongly
on chart coordinates. Instead put

$$
r_i=\sqrt{1+\|h_i\|^2},\qquad
W(h_i)=I_2-\frac{h_ih_i^t}{r_i(r_i+1)},\qquad
B(h_i)=W(h_i)Q(h_i). \tag{1}
$$

**Lemma 1 (orthonormal quotient).** The rows of `B(h_i)` are
orthonormal and their kernel is the candidate line. Consequently

$$
\left\|(\bigotimes_iB(h_i))T\right\|^2
 =\left\|(\bigotimes_i P_{u_i^\perp})T\right\|^2, \tag{2}
$$

where `P_(u_i perpendicular)` is the orthogonal projector onto the
plane perpendicular to the line. In particular the objective is
independent of the orthonormal bases chosen in these planes.

**Proof.** `QQ^t=I_2+hh^t`. The displayed `W` acts by `1/r` on
`h` and by one on its perpendicular direction, so it is the inverse
square root of `I_2+hh^t`. Hence `BB^t=I_2` and `B^tB` is the
stated projector. Tensor products preserve these identities. QED.

The program initializes each line with the leading left singular vector
of that site's tensor flattening. It then minimizes the normalized
residual with Levenberg–Marquardt and an analytic Jacobian. When a chart
coordinate becomes large, it changes the coordinate fixed to one and
restarts at the same projective line. This changes the chart without
changing the objective (2). Further attempts use seeded random starts.
Neither initialization nor chart changes supply the planted means.

## 3. Exact acceptance and rational source reconstruction

Near a numerical zero, the program reconstructs candidate rational chart
coordinates with a fixed denominator budget. It clears their denominators
in each row of `Q`, obtaining integer quotient matrices `Q_i^Z`, and
checks

$$
(\bigotimes_i Q_i^{\mathbb Z})T=0 \tag{3}
$$

in exact integer arithmetic. It also differentiates (3) in the `2n`
chart coordinates and records a nonzero maximal minor modulo `1000003`.
Because the matrix entries are integers, that minor proves full column
rank over the rationals, and therefore a reduced, isolated zero locally.
It gives no assertion about distant zeros.

For the seven- and nine-site cases, these verified lines are the sole
additional input to the covariance algorithm. That algorithm runs over
the field of order `1000003`. The recovered source is put into a fixed
site gauge, then reconstructed as bounded rationals. Rational lifting
can fail if the prime is too small; a modular answer is never silently
promoted to an answer over the rationals.

**Proposition 2 (exact final-output check).** Let a rational candidate
source be lifted from any finite-field calculation. Choose a positive
integer `D` that clears its mean and covariance denominators. Then
`D mu_i` and `D^2 R_ij` are integers and their tensor is `D^n G(mu,R)`.
If every entry of that tensor and of `D^n T` has absolute value at
most an integer `H`, equality modulo `2H+1` of every entry proves
`G(mu,R)=T` over the rationals.

**Proof.** Each difference is an integer of absolute value at most
`2H`, so the only possible multiple of `2H+1` is zero. QED.

The program computes such a bound recursively using absolute values of
all means and edge entries. A separate matching recurrence checks every
entry modulo `2H+1`. This last modulus need not be prime: it is an
integer equality check, not a field calculation.

The inverse functions do not read the source generator's parameters.
Only after reconstruction does a separate comparison check every
recovered mean and covariance entry against the planted source, allowing
product-one site scalings. Forward equality certifies the candidate even
without access to those planted parameters.

## 4. A local noise bound from the direction Jacobian

Fix a nonzero exact tensor `T_0` and a zero `h_0` of its line equations.
Keep `C=||T_0||` fixed and define

$$
F(T,h)=C^{-1}(\bigotimes_i B(h_i))T,\qquad
J=\partial_h F(T_0,h_0).
$$

**Theorem 3 (local mean-line conditioning).** Suppose `J` has full
column rank, and write `sigma` for its least singular value. For
sufficiently small real perturbations `E`, the least-squares objective
`||F(T_0+E,h)||^2/2` has a unique stationary point near `h_0`, which
is a strict local minimum. This point satisfies

$$
h(E)-h_0
 =-C^{-1}(J^tJ)^{-1}J^t(\bigotimes_i B(h_{0,i}))E
   +O(\|E\|^2), \tag{4}
$$

and therefore

$$
\|h(E)-h_0\|\le\frac{\|E\|}{C\sigma}+O(\|E\|^2). \tag{5}
$$

At the exact tensor, undamped Gauss–Newton converges quadratically from
a sufficiently close starting point.

**Proof.** The stationarity equations are
`partial_h F(T,h)^t F(T,h)=0`. At `(T_0,h_0)` their derivative in
`h` is `J^tJ`, because the residual is zero. This matrix is positive
definite. The implicit function theorem gives the unique nearby
stationary point; continuity of the Hessian makes it a strict local
minimum. Differentiating the stationarity equations gives (4).
The tensor product of the orthonormal quotient matrices has operator
norm one, which proves (5).

For the exact zero, write `h=h_0+e`. Smoothness gives
`F(T_0,h)=partial_h F(T_0,h)e+O(||e||^2)`. The Jacobian remains
injective nearby and its left inverse is bounded. The Gauss–Newton
update therefore cancels `e` and leaves `O(||e||^2)`. QED.

The full-rank condition holds generically at all the orders in the
earlier mean-direction theorem. This is a local consequence of that
result and standard least-squares analysis. It does not prove that the
implemented search reaches the relevant neighborhood, bound that
neighborhood uniformly, or establish a statistical sample complexity.

**Corollary 4 (an exact computable conditioning bound).** At an
accepted rational tuple, let `J_Z` be the integer Jacobian of (3).
For site `i`, let `d_i` be the larger of the two denominators used to
clear its quotient rows, and keep the line representative `u_i` with
its chart coordinate equal to one. Then

$$
K^2=\|T_0\|^2\left(\prod_i\|u_i\|^2d_i^2\right)
       \mathrm{tr}\left((J_Z^tJ_Z)^{-1}\right) \tag{6}
$$

is a positive rational number with `sigma^2 >= 1/K^2`. Thus the
first-order amplification of relative tensor error is at most `K` in
the chosen line coordinates.

**Proof.** If `D_i` is the diagonal matrix of row denominators,
then `Q_i^Z=D_i Q_i`. At a zero, differentiating the matrices `W_i`
adds no term because the full quotient residual is zero. Hence

$$
J=C^{-1}(\bigotimes_i W_iD_i^{-1})J_Z.
$$

The least singular value of `W_i D_i^-1` is at least
`1/(||u_i|| d_i)`. For the positive definite Gram matrix `G=J_Z^tJ_Z`,
`lambda_min(G) >= 1/tr(G^-1)`. Combine these inequalities to obtain
(6). The Gram inverse and its trace are computed over the rationals.
QED.

The stored floating-point singular values are estimates. The rational
bound (6) is the certified statement; it can be quite conservative.
It controls the first-order local behavior, not arbitrary finite noise.

**Observation 5 (no uniform conditioning for these line equations).**
Normalize the actual means to the first coordinate and replace all
covariance blocks by `epsilon R_ij`, for a fixed generic source. If
`n=2m+1`, the direction Jacobian before tensor normalization is exactly
`epsilon^m` times its value at `epsilon=1`. Indeed, its entries pair
all `n-1` other sites after projecting outside the mean lines. Meanwhile
the tensor tends to a nonzero product tensor as `epsilon` tends to zero.
Thus the normalized Jacobian's least singular value tends to zero at
order `|epsilon|^m`. Generic nondegeneracy alone cannot give a uniform
bound in (5). This concerns the quotient-equation estimator; it is not
a minimax lower bound for every possible source-recovery method.

## 5. Recorded outcomes and reproduction

Run from the repository root:

```sh
OPENBLAS_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 .venv/bin/python computations/matching-tensor-recovery-2026-09-26/blind_mean_search.py
```

The [program](../computations/matching-tensor-recovery-2026-09-26/blind_mean_search.py)
and [certificate](../computations/matching-tensor-recovery-2026-09-26/blind-mean-search-certificate.json)
record the input sources and hashes, every search attempt, exact line
checks, tangent minors, conditioning bounds, and recovered rational
sources. The numerical runs use SciPy 1.18.0 and deterministic seeds.

Means are chosen from `{-2,-1,1,2}`. Edge entries are chosen independently
from the integer interval shown below. The search receives neither.

| Sites | Edge-entry interval | Search result | Exactly verified output |
| --- | --- | --- | --- |
| 7 | `[-3,3]` | First start | All means and 189 covariance entries over `Q`; all 2187 tensor entries |
| 9 | `[-3,3]` | First start | All means and 324 covariance entries over `Q`; all 19683 tensor entries |
| 11 | `[-3,3]` | First start, with one chart change | Mean lines and rank-22 tangent minor; no covariance inverse attempted |
| 9 | `[-30,30]` | No accepted result in 16 starts | No recovered source claimed |

The successful tangent minors have residues `631283`, `993552`, and
`328365`, respectively, modulo `1000003`. Their ranks are `14`, `18`,
and `22`. The exact values of (6) give conservative relative first-order
amplification bounds `4327`, `9722`, and `10372`, respectively; the
certificate retains the full rational squares. These bounds do not
include the subsequent covariance step.

The failed case's best normalized residual is approximately `0.03080`.
It is recorded as a failure even though a numerical optimizer can
successfully terminate at a nonzero local minimum. It is not evidence
against the generic algebraic uniqueness theorem. A separate postmortem
uses the planted means only after the search has failed: their quotient
residual is exactly zero and their tangent minor has rank 18 and residue
`742683` modulo `1000003`. Thus the search missed a locally regular zero.
Those supplied means are never fed back into the search or counted as
a blind recovery.

## 6. Attribution and next work

The initialization is the standard mode-wise singular-vector construction;
see De Lathauwer–De Moor–Vandewalle,
[*A Multilinear Singular Value Decomposition*](https://epubs.siam.org/doi/10.1137/S0895479896305696).
The nonlinear optimizer is the established Levenberg–Marquardt method
as implemented by MINPACK and exposed through
[SciPy's least-squares interface](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.least_squares.html).
Its documentation explicitly describes a local least-squares solution.
Orthonormal quotient coordinates, the implicit function theorem, and
Gram-matrix bounds are standard tools, not new mathematical machinery.

The application here is to the mean-line equations supplied by the copy
identity, followed by the covariance corrections and Gaussian calibration
proved in the preceding notes. Exact acceptance and the retained failure
keep the practical search separate from the generic uniqueness theorem.
No exhaustive priority claim is made.

The remaining computational problem is a reliable global mean-line
algorithm or a proved useful basin for this optimizer. It should explain
the failure with stronger covariance. Arbitrary-order identifiability,
an exact successful reconstruction, and uniform numerical reliability
are different claims.

The subsequent [shared-calibration analysis](shared-calibration-and-near-ambiguity-2026-09-27.md)
now gives explicit gauge-invariant obstructions for full covariance
recovery and sharp conditional bounds for shared calibration. It also
connects mean-setting design to classical tight frames. It does not
resolve the failed nonlinear search or propagate noise through every
stage of the blind inverse.

The later [full-source stability note](full-source-local-stability-2026-09-27.md)
now gives finite local error bounds for all means and covariance entries
using the joint forward derivative. It proves a convergence neighborhood
for a separate frozen left-inverse iteration and controls the observed
mean span. Exact seven- and nine-site certificates verify those bounds.
The neighborhoods are conservative and do not supply global initialization
or a convergence proof for the blind search used here.
