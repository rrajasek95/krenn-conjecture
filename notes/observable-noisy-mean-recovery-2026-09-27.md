# Observable certificates for mean directions from noisy tensors

Research note, 2026-09-27. Written finite-error bounds and exact rational
certificates at three, five, and seven sites. Not Lean formalized or
independently peer reviewed. The Krenn–Gu manuscript is unchanged.

## 1. Result and scope

The [two-kernel theorem](slice-commutator-mean-recovery-2026-09-27.md)
recovers generic mean directions from an exact tensor at every odd order
from three onward. This note gives a noisy-data initializer with a
certificate computed from the observation. It needs neither a supplied
source nor a starting guess near the true means.

The inputs are a full observed tensor `Y` and a stated Frobenius error
bound `epsilon`. If the certificate passes, **every** matching tensor
`T` within that error ball, and every source representation of each such
tensor, has nonzero means whose lines obey the recorded angle bounds.
No prior bound on source-parameter distance is assumed. Existence of a
compatible matching tensor is an assumption, not a conclusion of the
certificate; the measurement-error bound is supplied, not estimated.

The result also covers every nearby tensor admitting a **compression
center**: a tuple of local lines whose quotient maps annihilate it.
This is the broader model of Theorem 8 in the linked note.

The recovered objects are local mean lines. The certificate does not
recover mean magnitudes, align their magnitudes between shared
observations, or bound covariance errors. Those steps are needed before
applying the [full-source correction theorem](full-source-local-stability-2026-09-27.md).
The [covariance near-ambiguities](shared-calibration-and-near-ambiguity-2026-09-27.md)
remain obstructions to uniform full-source bounds.

## 2. Slice errors and approximate solves

Let `n=2m+1>=3`, with local spaces `C^3`. Vector and tensor norms
are Euclidean/Frobenius norms. Unsubscripted matrix norms are spectral
norms. Superscript `*` denotes conjugate transpose. The implementation
uses real rational data and ordinary transpose, but the proof also covers
complex compatible sources. For nonzero `u,v`, the line angle satisfies

$$
\sin\angle(u,v)=\sqrt{1-\frac{|u^*v|^2}{\|u\|^2\|v\|^2}}. \tag{1}
$$

Use the exterior matrix from the two-kernel note, with alternating
symbol `epsilon_012=1`:

$$
\mathcal A_s(D)_{r,t}=\sum_cD_c\prod_{i=1}^s\epsilon_{r_it_ic_i}.
$$

Separate the first site and define the observable slice matrices

$$
Y=\sum_{a=0}^2e_a\otimes Y_a,\qquad
B_a(Y)=\mathcal A_{n-1}(Y_a),\qquad N=3^{n-1}. \tag{2}
$$

The matrices have size `N` by `N`. Relabel the first site's coordinates
if necessary so that zero is the chosen reference slice.

**Lemma 1 (slice perturbation).** If `||T-Y||_F<=epsilon`, then

$$
\|B_a(T)-B_a(Y)\|\le\delta,\qquad \delta=2^m\epsilon. \tag{3}
$$

**Proof.** Each coefficient of an `s`-site tensor appears in exactly
`2^s` entries of its exterior matrix, with signs and with no overlap
between distinct coefficients. Hence
`||A_s(D)||_F^2=2^s ||D||_F^2`. Take `s=2m` and bound the spectral
norm by the Frobenius norm. QED.

Let `Q,A,B` be proposed approximations to
`B_0(Y)^(-1), B_0(Y)^(-1)B_1(Y), B_0(Y)^(-1)B_2(Y)`.
They may be computed numerically and rounded to rational entries.

**Lemma 2 (verified operator errors).** Suppose certified bounds give

$$
\|I-QB_0(Y)\|\le b_0<1,\qquad
\nu\ge\frac{\|Q\|}{1-b_0},\qquad
\|A\|\le a,\quad\|B\|\le b, \tag{4}
$$

$$
\|B_0(Y)A-B_1(Y)\|\le\rho_A,\qquad
\|B_0(Y)B-B_2(Y)\|\le\rho_B. \tag{5}
$$

If `nu delta<1`, every `B_0(T)` in the data-error ball is invertible.
For `A_T=B_0(T)^(-1)B_1(T)` and `B_T=B_0(T)^(-1)B_2(T)`,

$$
\|A_T-A\|\le d_A=\frac{\nu}{1-\nu\delta}
 [\rho_A+\delta(1+a)],\qquad
\|B_T-B\|\le d_B=\frac{\nu}{1-\nu\delta}
 [\rho_B+\delta(1+b)]. \tag{6}
$$

**Proof.** The geometric-series inverse of `QB_0(Y)` proves
`||B_0(Y)^(-1)||<=nu`. A second such argument bounds
`||B_0(T)^(-1)||` by `nu/(1-nu delta)`. Put
`Delta_a=B_a(T)-B_a(Y)`. The identity

$$
A_T-A=B_0(T)^{-1}[\Delta_1-\Delta_0A-(B_0(Y)A-B_1(Y))]
$$

gives (6); the other operator is identical. QED.

Thus the bound includes solve residuals. It never silently treats a
floating-point inverse or solve as exact.

## 3. Stack the two equations

Form the proposed and true commutators and stacked matrices:

$$
C=AB-BA,\quad D=\begin{bmatrix}C\\CA\end{bmatrix},\qquad
C_T=A_TB_T-B_TA_T,\quad
D_T=\begin{bmatrix}C_T\\C_TA_T\end{bmatrix}. \tag{7}
$$

**Lemma 3 (stack perturbation).** With `c>=||C||`, define

$$
d_C=2(bd_A+ad_B+d_Ad_B),\qquad
d_{CA}=c\,d_A+d_C(a+d_A),\qquad
\eta=\sqrt{d_C^2+d_{CA}^2}. \tag{8}
$$

Then `||D_T-D||<=eta` throughout the data-error ball. A certified
upper bound on the square root may replace `eta`.

**Proof.** Expand the commutator difference using
`A_T=A+Delta_A`, `B_T=B+Delta_B`. The two terms linear in each
increment contribute `2b d_A` and `2a d_B`; the mixed terms contribute
`2d_A d_B`. Next expand
`C_TA_T-CA=C Delta_A+(C_T-C)A+(C_T-C)Delta_A`.
The norm of the vertical stack is bounded by the square root of the sum
of the squared block norm bounds. QED.

Stacking avoids a numerical decision about how many singular values of
`C` should be regarded as zero. Its exact kernel can be much larger
than one and vary between sources; the stack has a simple kernel at
every exact tensor covered by the two-kernel theorem.

Let `z` be any proposed unit vector in `C^N` and set

$$
H=D^*D+zz^*,\qquad r\ge\|Dz\|. \tag{9}
$$

**Lemma 4 (approximate kernel vector).** If `H` is positive definite
and `g>=sqrt(||H^(-1)||)`, then

$$
\|w\|\le g\|Dw\|\quad(z^*w=0). \tag{10}
$$

For every unit vector `v in ker D_T`,

$$
\sin\angle(z,v)\le q:=g(\eta+r). \tag{11}
$$

**Proof.** On `z`'s orthogonal complement, `w^*Hw=||Dw||^2`,
proving (10). Write `v=(z^*v)z+w`. Since `D_Tv=0`,
`||Dv||<=eta`, hence `||Dw||<=eta+|z^*v|r<=eta+r`.
Now `||w||=sin angle(z,v)`. QED.

An approximate smallest singular vector is a convenient proposal, but
the proof uses only its checked residual. The program stores an integer
vector `x`, and uses `zz^*=xx^t/(x^tx)`, a rational matrix.

**Lemma 5 (integer preconditioner).** Write a real rational symmetric
matrix as `H=G/s`, with integer `G` and positive integer `s`. Suppose
an integer square matrix `M`, integer `d>0`, and integer `b_H` satisfy

$$
\|M^tGM-d^2sI\|_F\le b_H<d^2s. \tag{12}
$$

Then `H` is positive definite, and an admissible bound is

$$
g^2\ge\frac{s\|M\|_F^2}{d^2s-b_H}. \tag{13}
$$

**Proof.** Put `alpha=d^2s-b_H`. Then `M^tGM>=alpha I`, so
`M,G` are invertible. Inverting gives `H^(-1)<=s MM^t/alpha` in
the positive-semidefinite order. Bound its norm by the trace. QED.

The residual in (12) is checked by integer sums of squares. Matrix
norms in (4)–(8) use `||M||^2<=||M||_1 ||M||_infinity` with exact
row and column sums. Square roots are rounded upward to rational
bounds. Numerical eigenvalues only propose `M`; no floating-point
singular value is accepted as a rigorous lower bound.

## 4. Every compatible mean tuple obeys the bounds

**Theorem 6 (observable global mean-line control).** Suppose Lemmas
2–5 are certified and `q<1`. Any tensor `T` in the data-error ball
that has a compression center has exactly one such center. Its unit
tail product `v` satisfies (11). If `T` is a matching tensor, every
source representation has nonzero means and these same lines.

Define the site-zero estimate by

$$
\widehat\alpha=z^*Az,\quad\widehat\beta=z^*Bz,\quad
\widehat u_0=(1,\widehat\alpha,\widehat\beta). \tag{14}
$$

At each other site choose any nonzero estimate `hat u_i`. Reshape `z`
as a `3` by `3^(n-2)` matrix `Z_i` with that site as its row index.
Let `P_i` be the orthogonal projection onto `C hat u_i` and put
`t_i=||(I-P_i)Z_i||_F`. The compatible mean lines satisfy

$$
\sin\angle(\mu_0,\widehat u_0)
 \le\sqrt{(d_A+2aq)^2+(d_B+2bq)^2}, \tag{15}
$$

$$
\sin\angle(\mu_i,\widehat u_i)\le t_i+2q\quad(i>0). \tag{16}
$$

The bounds also apply to compression lines without a matching
representation.

**Proof.** Equation (10) bounds the second-smallest singular value of
`D` below by `1/g`, by restricting to a codimension-one subspace.
Since `g eta<=q<1`, Lemma 3 implies `rank D_T>=N-1`. A compression
center supplies a product vector in `ker D_T`, by the block equations
of the two-kernel theorem. Its nullity is therefore exactly one, and
that theorem proves unique compression lines. Its zero-mean perturbation
argument excludes zero means in every matching representation.

Write the true site-zero line as `(1,alpha,beta)`. The same block
equations give `A_Tv=alpha v`, `B_Tv=beta v`. The trace norm of
`zz^*-vv^*` is `2 sin angle(z,v)`. Consequently

$$
|\widehat\alpha-\alpha|\le d_A+2aq,\qquad
|\widehat\beta-\beta|\le d_B+2bq.
$$

Project the difference of the two first-site vectors perpendicular to
the true line, and divide by `||hat u_0||>=1`, to obtain (15).
Choose the phase of `v` aligned with `z`; then
`||z-v||<=sqrt(2)q<=2q`. Its site-`i` flattening is a rank-one
unit matrix whose left factor is the true local line. Projecting that
matrix perpendicular to `hat u_i`, then adding and subtracting `Z_i`,
proves (16). QED.

The program requires the stronger threshold `q<1/4` and requires all
local-line bounds to be below one. Tail directions are proposed by
leading left singular vectors of `Z_i`, rounded to rational coordinates.
The residuals `t_i` check their quality directly.

**Corollary 7 (generic initialization from data alone).** At every
exact tensor satisfying the two-kernel theorem, certificates of this
form pass for all sufficiently small observation errors when the
proposals have sufficient precision. Mean-line errors tend to zero
linearly with data error, with constants depending on the exact tensor
and chosen chart. No nearby mean guess is required.

**Proof.** At the exact tensor, `D` has a simple zero singular value
and an invertible reference slice. With exact operator solves,
`eta=O(epsilon)`. A smallest right singular vector of the observed
stack has `r<=eta`, because it does no worse than the true kernel
vector. The positive eigenvalues of `H` stay bounded away from zero,
so `g` stays bounded. The best left singular vector of each `Z_i`
does no worse in its projection residual than the true factor, giving
`t_i=O(epsilon)`. Choose rational proposal errors of order `epsilon`
or smaller, and apply (11), (15), and (16). There is no fixed-precision
assertion as `epsilon` tends to zero. QED.

This is conditional on sufficiently small errors at a good exact
tensor. It supplies neither a uniform threshold across all sources
nor a full covariance initializer.

## 5. Exact certificates and reproduction

The examples use the all-orders paired witness, applying the same
orthogonal matrix to both sites of each pair:

$$
O_k=I-\frac23w_kw_k^t,\qquad
w_k=(1,(-1)^k,(-1)^{\lfloor k/2\rfloor}). \tag{17}
$$

Since `||w_k||^2=3`, the matrices are orthogonal. The tail mean
directions have three nonzero coordinates. The clean tensor has
denominator nine. Seeded noise `+/-2^(-40)` is added to **every**
entry, including the reference slice. The error budget is
`ceil(sqrt(3^n))/2^40`. Only the noisy tensor, budget, and numerical
proposals enter certificate acceptance; the clean source is used later
for comparisons.

| Sites | Data-error bound | Tail-product sine bound | Largest local-line sine bound | Largest actual local-line error in this test |
| ---: | ---: | ---: | ---: | ---: |
| 3 | `5.46e-12` | `3.81e-9` | `2.65e-8` | below `1.18e-12` |
| 5 | `1.46e-11` | `7.26e-7` | `1.50e-5` | below `8.91e-13` |
| 7 | `4.28e-11` | `9.12e-5` | `5.55e-3` | below `8.50e-13` |

Displayed bounds are rounded upward. The
[certificate](../computations/matching-tensor-recovery-2026-09-26/slice-noise-recovery-certificate.json)
stores rational bounds and integer witnesses. The bounds are conservative;
they cover every compatible tensor, whereas the actual-error column
compares only the planted source. These examples are not statistical
accuracy estimates.

The [replay](../computations/matching-tensor-recovery-2026-09-26/verify_slice_noise_recovery.py)
rebuilds every exterior entry separately, the clean tensor by scalar
matching sums, and the augmented Gram directly from the stacked matrix.
It checks noise norms and line errors exactly, with numerical solvers
disabled. Zero inverse and preconditioner proposals and an excessive
noise budget are rejected. The
[saved audit](../computations/matching-tensor-recovery-2026-09-26/slice-noise-recovery-audit.json)
passes all three sizes. It shares the exact bound-acceptance function
and integer matrix library with the generator; it is not an independent
implementation of every inequality.

From the repository root:

```sh
OPENBLAS_NUM_THREADS=1 .venv/bin/python computations/matching-tensor-recovery-2026-09-26/slice_noise_recovery.py
OPENBLAS_NUM_THREADS=1 .venv/bin/python computations/matching-tensor-recovery-2026-09-26/verify_slice_noise_recovery.py
```

The generator's `--quick` omits seven sites. The seven-site proposal
and acceptance took about eight seconds in the recorded run, using
dense matrices of order 729. Storage and arithmetic grow exponentially
with the number of sites; this is not compressed-data initialization.

## 6. Attribution and remaining work

Singular-subspace perturbation bounds are classical; see Wedin,
[Perturbation bounds in connection with singular value decomposition](https://link.springer.com/article/10.1007/BF01932678),
*BIT* 12 (1972), 99–111. The elementary residual argument in Lemma 4
is proved here with the hypotheses actually used. Its application
depends on the specific observable stack and its all-orders rank theorem.

Numerical proposals followed by rigorous residual acceptance are standard
verification methods; see Rump,
[Verification methods: rigorous results using floating-point arithmetic](https://www.tuhh.de/ti3/paper/rump/Ru10.pdf),
*Acta Numerica* (2010), Section 1.6 and Part 2. Lemma 5 uses the same
preconditioner principle as the earlier full-source local-stability note.
The contribution here is the propagation from raw tensor errors and
imperfect solves to observable bounds covering all nearby compression
centers and mean tuples.

The subsequent [full-source initialization note](certified-full-source-initialization-2026-09-27.md)
now propagates direction errors through the covariance solves and scalar
calibration and certifies entry into the existing local correction ball.
It covers every compatible source under explicit acceptance conditions;
the saved seven-site error budget is extremely small, about `3.4e-41`.
Useful noise thresholds remain open. The subsequent
[shared-source certificate](certified-shared-source-alignment-2026-09-27.md)
uses the common covariance to certify consistent scales across observations
and gives a finite bound for the observed global mean span. Compressed-data
initialization and nongeneric classification remain open.
