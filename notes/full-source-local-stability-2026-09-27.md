# Local stability of complete sources and shared mean spaces

Research note, 2026-09-27. Written proofs with exact certificates and an
independent computational replay. Not Lean formalized or independently
peer reviewed. The Krenn–Gu paper is unchanged.

## 1. Result and observation model

The [all-orders source theorem](single-cross-moment-all-orders-2026-09-27.md)
establishes generic exact recovery from one Gaussian cross moment at every
odd order at least seven. The present note gives **finite local error
bounds for all means and all cross-site covariance entries together**.
The bounds use the derivative of the complete forward map, so they do not
assume that an earlier mean-line or covariance-class reconstruction is
error-free. A second result shows that shared observations add covariance
information even when their means are unknown. A third transfers source
error to the span of the observed mean vectors.

These are local statements. They require an explicit neighborhood of a
source whose derivative has full rank after removing the scaling freedom.
The certificate checks that condition at supplied source points. It does
not locate those points from arbitrary noisy data or rule out distant
alternatives. The earlier
[near-ambiguity examples](shared-calibration-and-near-ambiguity-2026-09-27.md)
remain obstructions to uniform global bounds.

The later [observable noisy-mean certificate](observable-noisy-mean-recovery-2026-09-27.md)
locates the local mean directions directly from noisy full-tensor data
under checkable matrix conditions. Its bounds cover every compatible
source in the data-error ball, without assuming parameter proximity.
It supplies directions only. The subsequent
[full-source initializer](certified-full-source-initialization-2026-09-27.md)
now supplies covariance and mean-scale bounds and certifies entry into
this neighborhood for every compatible single-observation source. Its
exact seven-site example requires an extremely small error budget. The
later [shared-source note](certified-shared-source-alignment-2026-09-27.md)
also certifies alignment and entry into a joint correction neighborhood
and bounds the observed mean span. Useful noise thresholds remain open.

There are `n` labelled sites, indexed by `0,...,n-1`, and `p` labelled
observations. At first each site has three real coordinates. Observation
`s` has local mean vectors `mu_i^(s) in R^3`. Every observation uses the
same cross-site covariance blocks `R_ij in R^(3 by 3)`, for `i<j`.
Its tensor entry indexed by `a=(a_0,...,a_(n-1))` is

$$
F_s(\mu^{(s)},R)_a
=\sum_{M}\ \prod_{\{i,j\}\in M}(R_{ij})_{a_i a_j}
                 \prod_{i\notin V(M)}(\mu_i^{(s)})_{a_i}. \tag{1}
$$

Here `M` ranges over matchings: sets of edges with no repeated endpoint.
The set `V(M)` contains their endpoints; an empty product is one.
Equation (1) is the Gaussian matching formula, also meaningful purely as
a polynomial map. We write `F=(F_1,...,F_p)` for the stacked observations.
Within-site covariance never occurs in (1) and is not a recovered parameter.

All parameter norms are Euclidean norms of the listed free entries.
All data norms are Euclidean norms of all stacked tensor entries, or
equivalently Frobenius norms. No probabilistic model for measurement
error is assumed. Rescaling coordinates changes these numerical constants.

## 2. Fixing the scaling freedom using covariance alone

The product-one scaling

$$
\mu_i^{(s)}\longmapsto\lambda_i\mu_i^{(s)},\qquad
R_{ij}\longmapsto\lambda_i\lambda_jR_{ij},\qquad
\prod_i\lambda_i=1 \tag{2}
$$

preserves every output. A bound for raw source entries therefore needs
a fixed representative. Choose nonzero numbers `c_j`, for `1<=j<n`, and
impose the affine conditions

$$
(R_{0j})_{00}=c_j. \tag{3}
$$

This choice uses covariance alone, so it is common to all mean settings.
The free covariance vector has length

$$
q=9\binom n2-(n-1).
$$

The full parameter vector `theta` lists all `3np` mean entries, followed
by these `q` covariance entries. Its dimension is `d=3np+q`.

**Lemma 1 (a common local gauge).** For odd `n>=3`, every real source
with all `(R_0j)_00` nonzero has a unique representative satisfying (3).
This representative depends smoothly on the source on the stated open
set. The affine slice (3) is transverse to the scaling directions.

**Proof.** Put `r_j=(R_0j)_00`. The required scaling satisfies

$$
\lambda_j=\frac{c_j}{\lambda_0r_j},\qquad
\lambda_0^{n-2}=\prod_{j=1}^{n-1}\frac{c_j}{r_j}. \tag{4}
$$

The exponent is odd, so there is a unique nonzero real root. Its
derivative is finite on each component where the right side is nonzero.
For transversality, write an infinitesimal scaling as `tau_i`, with
`sum_i tau_i=0`. Preserving (3) requires `tau_0+tau_j=0` for every
`j>0`, hence `(2-n)tau_0=0`, and then all `tau_i=0`. QED.

The real root in (4) is not claimed to be rational. Over the complex
numbers the same slice is a local gauge, with finitely many global
choices. For the real local bounds below there is no such discrete choice.

**Corollary 2 (generic full derivative rank at all odd orders).** For
every odd `n>=7` and every fixed finite `p`, the derivative
`J=D F(theta)` on (3) has full column rank on a nonempty generic set.
The same conclusion holds with local dimensions at least three.

**Proof.** The earlier single-output theorem gives an inverse modulo
(2), rational on suitable quotient charts. Compose that inverse with
the smooth gauge (4). Differentiating the resulting local identity
shows that the single-output derivative is injective on (3).
For several observations, a vector in the kernel of the stacked
derivative restricts, for each observation, to a zero single-output
variation of its means and the common covariance. Each such variation
is zero. The necessary single-output generic conditions hold
simultaneously on a nonempty open set: their defining nonzero
polynomials, in the common covariance and separately labelled means,
have nonzero product. The same argument uses the earlier theorem for
larger local dimensions. QED.

The concrete certificates below prove full rank directly at their
particular sources; they do not rely on those sources being generic.

## 3. Smaller matching responses give the derivatives

For a subset `S` of sites, let `T_S` denote the matching tensor (1) on
those sites only; set `T_empty=1`. Inserting a coordinate vector at
removed sites means fixing the corresponding tensor indices to that
coordinate and setting the other entries to zero.

**Lemma 3 (first and second derivatives).** The column for a mean entry
`mu_i[a]` is `T_(all sites except i)` with the coordinate vector `e_a`
inserted at site `i`. The column for `(R_ij)[a,b]` is the analogous
tensor with sites `i,j` removed and `e_a,e_b` inserted. A mixed second
partial is zero if the two parameter entries use a common site.
Otherwise it is the matching tensor on the remaining sites with all
four, three, or two specified coordinate vectors inserted.

**Proof.** Differentiate the matching sum. A matching term uses exactly
one mean or edge factor at any given site, so two factors sharing that
site never occur together. For disjoint supports, removing the selected
factors leaves each matching on the complementary sites exactly once.
In particular, differentiating an edge entry introduces no factor of
two: the independent edge blocks in (1) are indexed by `i<j`. QED.

This is the smaller-response identity behind the full-source Jacobian.
It also supplies a finite bound on how quickly the derivative changes.
Fix a source `theta_c`. For each observation define

$$
m_i=1+\max_a |\mu_i[a]|,\qquad
c_{ij}^{+}=1+\max_{a,b}|R_{ij}[a,b]|.
$$

On the unit parameter ball around `theta_c`, these bound every relevant
entry, including the fixed entries harmlessly overestimated by one.
For a subset of sites define a positive scalar matching sum by

$$
h(\varnothing)=1,\qquad
h(S)=m_i h(S\setminus\{i\})+
\sum_{j\in S\setminus\{i\}}c_{ij}^{+}h(S\setminus\{i,j\}). \tag{5}
$$

Use the unordered edge block in (5). The resulting value is independent
of the chosen `i in S`. Every entry of `T_S` has absolute value at
most `h(S)`.

**Lemma 4 (a computable curvature bound).** Assign weight `w_{ {i} }=3`
to a singleton support, weight `w_{ {0,j} }=8` to a fixed-star edge,
and weight nine to every other edge support. For one observation set

$$
L_s^2=\sum_{A\cap B=\varnothing}
 w_Aw_B\,3^{n-|A\cup B|}\,h((A\cup B)^c)^2, \tag{6}
$$

where the sum is over ordered pairs of singleton or edge supports.
Then `L=sqrt(sum_s L_s^2)` bounds the bilinear operator norm of
`D^2 F` throughout the unit ball. Consequently

$$
\|D F(\theta)-D F(\theta')\|\le L\|\theta-\theta'\| \tag{7}
$$

whenever their joining segment is in that ball.

**Proof.** There are `w_Aw_B` free coordinate pairs with disjoint
supports `A,B`. By Lemma 3 each corresponding second partial has
squared norm at most `3^(n-|A union B|) h((A union B)^c)^2`.
Summing bounds the squared Frobenius norm of the full Hessian array,
which bounds its bilinear operator norm. For shared outputs, the
Hessian arrays occupy separate output blocks. Their squared norms add;
mixed derivatives involving means from different observations are zero.
Integration along the segment proves (7). QED.

For larger local dimensions replace the support weights by `d_i` and
`d_i d_j`, subtracting one on each fixed-star edge, and replace
`3^|S|` by `product_(i in S) d_i`. The remaining statements are unchanged.

## 4. Exact conditioning certificates

Put `J_c=D F(theta_c)` and `G=J_c^t J_c`. Superscript `t` denotes
transpose. At an integer source all entries of these matrices are
integers. The program uses a floating-point eigensolver only to propose
an approximate inverse square root of `G`. The following exact test
accepts or rejects that proposal.

**Lemma 5 (integer preconditioner certificate).** Let `M` be a square
integer matrix of order `d`, let `D` be a positive integer, and suppose
an integer `b` satisfies

$$
\|M^tGM-D^2I\|_F\le b<D^2.
$$

Put `alpha=D^2-b`. Then `G` is positive definite and

$$
G^{-1}\preceq\frac{MM^t}{\alpha},\qquad
\|J_c^\dagger\|^2\le\frac{\|M\|_F^2}{\alpha}. \tag{8}
$$

Here `A preceq B` means `B-A` is positive semidefinite, and
`J_c^dagger=(J_c^t J_c)^(-1) J_c^t` is the left pseudoinverse.
For a chosen parameter block, restricting the row sum `||M||_F^2`
to that block bounds the squared norm of the corresponding rows of
`J_c^dagger`.

**Proof.** The residual bound implies `M^t G M >= alpha I`, so `M`
and `G` are invertible. Inverting this inequality and conjugating gives
the first inequality in (8). The identity
`J_c^dagger (J_c^dagger)^t=G^(-1)` and the bound of a positive
semidefinite matrix's spectral norm by its trace prove the rest. QED.

The program uses `D=2^48` and the exact integer upper bound

$$
b=\left\lceil\sqrt{\sum_{i,j}
 [(M^tGM)_{ij}-D^2\delta_{ij}]^2}\right\rceil.
$$

The saved `M` is compressed only for storage. The replay decompresses
it and performs the matrix products and inequalities with integers.
No reported floating singular value is used to certify a lower bound.

## 5. Finite source-error bounds and a local iteration

Choose rational or integer upper bounds
`g>=||J_c^dagger||` and `ell>=L`, both positive, and set

$$
r=\min\left\{1,\frac{1}{2g\ell}\right\}. \tag{9}
$$

**Theorem 6 (finite local source stability).** Any two parameter
vectors in the closed ball `B(theta_c,r)` satisfy

$$
\|F(\theta)-F(\theta')\|
\ge\frac{\|\theta-\theta'\|}{2g}. \tag{10}
$$

In particular, take `theta_c` to be the true source and
`Y=F(theta_c)+E`, where `||E||<=epsilon`. Every source estimate in
this ball with data residual at most `epsilon` satisfies

$$
\|\widehat\theta-\theta_c\|\le4g\epsilon. \tag{11}
$$

If `epsilon<=r/(8g)`, a minimizer of the squared data residual over
the closed ball exists, lies in its interior, and satisfies (11).

**Proof.** On the ball, `||D F(theta)-J_c||<=ell r`. Subtract
the constant derivative `J_c` inside the integral along the segment
from `theta'` to `theta`. The integral of the derivative difference
has norm at most `ell r ||theta-theta'||`, while
`||J_c(theta-theta')||>=||theta-theta'||/g`. Equation (9) gives
(10). This argument controls vector cancellation along the segment;
a pointwise singular-value bound alone would not suffice.
For (11), the distance between the two fitted output tensors is at
most `2 epsilon`. A minimizer exists by compactness. At the center
the residual is at most `epsilon`; on the boundary it is at least
`r/(2g)-epsilon>epsilon` under the stated threshold. Thus every
minimizer is interior and has residual at most `epsilon`. QED.

No uniqueness of a noisy least-squares minimizer is asserted.

**Corollary 7 (a posteriori comparison).** If `theta_c` is a proposed
source, `delta=||F(theta_c)-Y||`, and another source in the certified
ball fits `Y` to error at most `epsilon`, their distance is at most
`2g(delta+epsilon)`.

**Proof.** Apply (10) and the triangle inequality. QED.

This corollary still requires the other source to lie in the ball.
A small residual alone does not establish that global fact.

There is also a constructive local consequence using a fixed derivative.
It should be distinguished from the earlier blind mean-line optimizer.

**Proposition 8 (convergence of a frozen left-inverse iteration).** Put
`B=J_c^dagger`. If `||Y-F(theta_c)||<=r/(2g)`, the map

$$
\Phi_Y(\theta)=\theta+B(Y-F(\theta)) \tag{12}
$$

maps the closed ball in (9) to itself and is a contraction of factor at
most one half. From every point of that ball, repeated application of
(12) converges to its unique fixed point `theta_*`. If a true source
`theta_0` is in the same ball and `Y=F(theta_0)+E`, then

$$
\|\theta_*-\theta_0\|\le2g\|E\|. \tag{13}
$$

**Proof.** Since `B J_c=I`,
`D Phi_Y(theta)=B(J_c-D F(theta))` has norm at most
`g ell r<=1/2`. The image of the center is at distance at most
`g ||Y-F(theta_c)||<=r/2` from the center, proving invariance of
the ball. The contraction mapping theorem gives existence, uniqueness
and convergence. Finally `Phi_Y(theta_0)=theta_0+B E`; comparison
with the fixed point gives
`||theta_*-theta_0||<=||theta_*-theta_0||/2+g||E||`. QED.

The iteration solves the projected equations `B(F(theta_*)-Y)=0`.
For noisy data this need not be a zero of the entire data residual or
a least-squares stationary point. The theorem concerns exact arithmetic;
no floating-point iteration error guarantee is claimed. The saved
certificates verify its radius and residual threshold. They do not
constitute a run of the iteration or a method of globally reaching its
ball from an arbitrary initialization.

## 6. Shared covariance information with unknown means

For observation `s`, split its derivative on the same slice (3) as

$$
J_s=[A_s\ B_s],
$$

where `A_s` has the mean columns and `B_s` has the common covariance
columns. Here `B_s` is unrelated to the pseudoinverse `B` in (12).
Assume each `J_s` has full column rank. Define the orthogonal projection

$$
P_s=I-A_s(A_s^tA_s)^{-1}A_s^t,
\qquad I_s=B_s^tP_sB_s. \tag{14}
$$

The matrix `P_s` removes output changes that can be explained by
varying that observation's unknown means. Thus `I_s` measures the
remaining sensitivity to covariance. It is an ordinary least-squares
information matrix, with no statistical noise interpretation required.

**Theorem 9 (additive covariance information).** Each `I_s` is positive
definite. In the stacked linearized least-squares problem with separate
unknown means and a common covariance, the covariance information is

$$
I_{\rm shared}=\sum_{s=1}^p I_s. \tag{15}
$$

The operator norm of the linear map from stacked data errors to the
estimated covariance increment is exactly
`1/sqrt(lambda_min(I_shared))`. If `c_s^2` bounds the squared norm
of the covariance rows of `J_s^dagger`, then

$$
\|\hbox{covariance error map}\|^2
\le\left(\sum_{s=1}^p\frac{1}{c_s^2}\right)^{-1}. \tag{16}
$$

**Proof.** For a proposed covariance increment `v`, minimizing over
the mean increment in output `s` leaves the residual
`P_s(B_s v-e_s)`. The mean parameters belong to separate outputs,
so the profiled objective is the sum of these squared norms, giving
(15). If `P_s B_s v=0`, then `B_s v` is in the column space of
`A_s`; injectivity of `J_s` forces `v=0`. Thus `I_s` is positive
definite. The covariance error map is

$$
e\longmapsto I_{\rm shared}^{-1}
          \sum_s B_s^tP_s e_s.
$$

Multiplying this map by its transpose gives `I_shared^(-1)`.
For a single output, the covariance block of `(J_s^t J_s)^(-1)`
is `I_s^(-1)`, by the same elimination. Hence
`I_s >= c_s^(-2) I`; sum and invert to obtain (16). QED.

Lemma 5 supplies exact rational `c_s^2` without calculating an exact
Schur complement. The bound is first order, whereas (11) controls
finite perturbations of the complete source. Both use the same covariance
coordinates; no known mean frame or pre-recovered covariance class is
assumed. A full joint certificate can be stronger than the bound obtained
by combining separate certificates in (16).

The improvement in (16) compares errors at a fixed **total stacked**
noise norm. If each additional observation comes with its own arbitrary
error of unchanged size, that total norm grows. Equation (16) by itself
does not imply cancellation of coherent errors or a statistical averaging
rate.

## 7. Stability of the observed mean space

Flatten each observation's local means into a vector in `R^(3n)`, and
let `U` be the matrix with those vectors as its `p` columns. The space
of interest is the column space of `U`, of rank `r_mu`. This concerns
the span actually sampled by the observations, not latent directions
that no setting uses. Its Euclidean geometry is measured in the fixed
covariance gauge (3).

**Corollary 10 (observed mean-span error).** Suppose
`s_0<=sigma_(r_mu)(U)` is positive. Under Theorem 6, form the mean
matrix `U_hat` from an estimate satisfying (11), and take its leading
`r_mu` left singular vectors. If also `epsilon<=s_0/(8g)`, the sine
of the largest angle between the estimated and true subspaces is at most

$$
\|\sin\Theta\|\le\frac{8g}{s_0}\epsilon. \tag{17}
$$

**Proof.** The operator norm of `U_hat-U` is bounded by its Frobenius
norm, hence by the full source error `delta=4g epsilon`.
Project the leading left singular-vector equation for `U_hat` onto
the orthogonal complement of the column space of `U`. The projected
right side has norm at most `delta`, while the retained singular
values are at least `sigma_(r_mu)(U)-delta` by the singular-value
perturbation inequality. Thus
`||sin Theta||<=delta/(sigma_(r_mu)(U)-delta)<=2 delta/s_0`.
This proves (17), including for any choice of leading subspace if
the boundary case has a tie. QED.

This is a standard singular-subspace perturbation argument, in the
setting of [Wedin's perturbation bounds](https://link.springer.com/article/10.1007/BF01932678).
If `U` has full column rank, an elementary exact lower bound is

$$
\sigma_{\min}(U)^2\ge
\frac{1}{\mathrm{tr}((U^tU)^{-1})}. \tag{18}
$$

The certificate evaluates the right side rationally and rounds its
square root down. The general corollary does not require full column
rank; that assumption is used only by this particular certificate for
`s_0`.

## 8. Exact examples and reproduction

The sources and every preconditioner witness are saved in the
[certificate](../computations/matching-tensor-recovery-2026-09-26/source-local-stability-certificate.json).
All means and covariance entries are chosen from `{-2,-1,1,2}`.
The seven-site example has four observations sharing all covariance
blocks. Their global mean vectors have rank four, while the means at
each individual site span only three dimensions. Thus the mean-span
bound does not require local dimension greater than the global number
of observed directions.

The following numbers are rounded descriptions of exact rational
constants in the certificate. `r` is a parameter radius, and `epsilon_0`
is the data-noise threshold `r/(8g)` used in Theorem 6.

| Sites | Outputs | Free parameters | Certified upper bound `g` | Radius `r` (approximately) | Threshold `epsilon_0` (approximately) |
| --- | --- | --- | --- | --- | --- |
| 7 | 4 | 267 | `0.041008055211` | `1.27414e-5` | `3.88381e-5` |
| 9 | 1 | 343 | `0.007458746434` | `1.14139e-6` | `1.91283e-5` |

These radii are conservative. The unit-ball matching majorant and
Frobenius trace bounds prioritize verifiability over sharp constants.
They are absolute, coordinate-dependent bounds, not relative errors or
claims of practical performance at those noise levels.

For the seven-site family, (16) gives a covariance derivative bound
smaller than `0.051155` in norm; the numerical estimate is about
`0.01618`. Only the rational bound is certified. The sharper full joint
certificate is separately retained. There are six exact matrix witnesses
in total: four separate seven-site outputs, their joint source, and the
nine-site output.

Generate the certificates from the repository root:

```sh
OPENBLAS_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 .venv/bin/python computations/matching-tensor-recovery-2026-09-26/source_local_stability.py
```

Verify the saved witnesses without using a numerical eigensolver:

```sh
OPENBLAS_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 .venv/bin/python computations/matching-tensor-recovery-2026-09-26/verify_source_local_stability.py
```

The [generator](../computations/matching-tensor-recovery-2026-09-26/source_local_stability.py)
constructs the derivative from Lemma 3 and checks one directional
derivative against a separate differentiated matching recurrence.
The [replay](../computations/matching-tensor-recovery-2026-09-26/verify_source_local_stability.py)
checks **every forward and Jacobian entry** using a separate scalar
matching recurrence. An absolute integer bound makes the modular
forward check a characteristic-zero equality check. Integer overflow
guards cover the tensor and Gram operations; all residual certificate
products use arbitrary-precision integers. A second implementation
enumerates matchings directly to verify the curvature majorant.
The replay also checks every block of the joint Gram matrix, the exact
information-combination bound, and the rational radius, noise and
observed-span constants. It ignores floating-point estimates when
deciding whether the certificate is valid.

## 9. Attribution and remaining scope

Gaussian moment and derivative formulas are established tools; see
[Pereira–Kileel–Kolda](https://arxiv.org/abs/2202.06930).
Numerical proposals followed by rigorous residual tests are standard
verified numerics; see Rump,
[*Verification methods: rigorous results using floating-point arithmetic*](https://www.tuhh.de/ti3/paper/rump/Ru10.pdf),
especially Section 1.6. Our elementary integer test is stated and proved
explicitly in Lemma 5. The contraction argument, elimination of nuisance
mean parameters by orthogonal projection, and singular-subspace bound
are also classical. No new general perturbation theory is claimed.

The contribution here is their application to the complete matching
source: a covariance-only gauge valid across unknown mean settings,
all-orders generic derivative rank from the preceding copy-based inverse,
matching-response curvature certificates, and local control of the shared
source and its observed mean space without treating intermediate inverse
steps as exact.

The remaining tasks include global initialization, more useful certified
neighborhood sizes, analysis of the retained blind-search failure, and
classification of singular or nongeneric sources. Uniform global
conditioning is already excluded by the prior near-ambiguity examples.
The written all-orders proofs and these local certificates remain
separate from the Lean formalization of the original conjecture.

The subsequent [product-measurement result](product-measurement-source-recovery-2026-09-27.md)
applies established algebraic measurement theory to reduce the exact
scalar data requirement to a quantity quadratic in the number of sites
at fixed local dimension. Direct scalar matching responses give local
certificates through eleven sites without constructing the full tensor.
The finite-error theorem here applies to that compressed forward map as
well, with its own certified Jacobian and curvature bounds. Global
initialization and certification of specific probe lists remain separate
problems.
