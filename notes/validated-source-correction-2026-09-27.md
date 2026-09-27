# Exact validation of a numerical source-correction output

Research note, 2026-09-27. A conditional output theorem, saved binary64
corrections, and an exact computational audit. Not Lean formalized or
independently peer reviewed. The Krenn–Gu paper is unchanged.

## 1. The remaining numerical step

The [shared-source certificate](shared-source-recovery-visible-noise-2026-09-27.md)
places every compatible source in a correction neighborhood and proves
convergence of an exact-arithmetic iteration. A program using floating-point
arithmetic does not execute that iteration exactly. This note validates
the actual returned values instead.

Three ordinary binary64 correction steps are saved as exact hexadecimal
floating-point values. Each returned source is evaluated again with integers
and rational numbers. The first output has a certified distance at most
`4.289e-16` from the exact fixed point. Its error against every compatible
shared source is at most `4.308e-12`; the recovered rank-four mean space
has largest principal-angle sine at most `1.381e-11` in the common gauge.

This is an **a posteriori output certificate**: the numerical solver and
its intermediate rounding errors need not be trusted. It is not a proof
that arbitrary floating-point trajectories converge, or that later steps
improve the result. The three recorded outputs have different certified
errors, and the first has the smallest bound.

The synthetic starting candidate equals the source used to generate the
data. Moving toward a fixed point for noisy data therefore need not improve
its actual error against that planted source. The contribution here is
validated numerical correction and a conditional error bound for all
compatible sources, not an empirical accuracy improvement on this example.

## 2. A general output certificate

Let `F: C^d -> C^M` be twice continuously differentiable on the relevant
ball. For complex coordinates below, use a complex-linear derivative,
as for the matching polynomial. Norms are Euclidean, matrix norms are
spectral unless specified, and an asterisk denotes conjugate transpose.

The reference source is `theta_0`, the data are `Y`, and
`J=D F(theta_0)` has full column rank. Assume an earlier global argument
has established that **every** source compatible with
`||F(theta)-Y||<=epsilon` lies in the closed ball
`B(theta_0,R)`. Certify

$$
\|J^\dagger\|\le g,\qquad
\sup_{\theta\in B(\theta_0,R)}\|D^2F(\theta)\|\le L,
\qquad q=gLR<1.                                             \tag{1}
$$

Here `J^dagger=(J*J)^(-1)J*` is the left pseudoinverse. Define the
frozen-derivative correction map

$$
G(\theta)=\theta+J^\dagger(Y-F(\theta)).                    \tag{2}
$$

The derivative `J` is fixed at `theta_0`. A fixed point solves the
projected equations `J*(Y-F(theta))=0`. It need not minimize the full
squared data residual, whose first-order condition would involve the
derivative at the varying source. A full residual can remain nonzero
when the data do not lie on the source model.

For any numerical output `theta_tilde`, suppose exact arithmetic supplies

$$
\|\widetilde\theta-\theta_0\|\le R,\qquad
b(\widetilde\theta)\ge
\|J^\dagger(Y-F(\widetilde\theta))\|.                        \tag{3}
$$

Also require `b(theta_0)+qR<=R`.

**Theorem 1 (validated output and source error).** Under these conditions,
`G` has a unique fixed point `theta_infty` in the ball. Every output
satisfying (3) obeys

$$
\|\widetilde\theta-\theta_\infty\|
\le\frac{b(\widetilde\theta)}{1-q}.                         \tag{4}
$$

For every compatible source in the stated gauge,

$$
\|\widetilde\theta-\theta\|
\le\frac{b(\widetilde\theta)+g\epsilon}{1-q}.              \tag{5}
$$

**Proof.** Since `J^dagger J=I`,
`D G(theta)=J^dagger(J-D F(theta))`. Integrating the Hessian along a
segment gives `||D G(theta)||<=gLR=q`. The center displacement is at
most `b(theta_0)`, so the center test makes `G` a contraction of the
closed ball into itself. The Banach contraction theorem gives its
unique fixed point. For any output in the ball,

$$
\|\widetilde\theta-\theta_\infty\|
\le\|\widetilde\theta-G(\widetilde\theta)\|
      +q\|\widetilde\theta-\theta_\infty\|,
$$

which gives (4). For a compatible source, its own correction satisfies
`||G(theta)-theta||<=g epsilon`. The same comparison gives
`||theta-theta_infty||<=g epsilon/(1-q)`. Adding (4) proves (5).
The global hypothesis ensures that this comparison covers every compatible
source, rather than only those assumed close in advance. QED.

No condition in this theorem requires the output to have been produced
by a particular algorithm. Its exact stored coordinates and checked
residual determine acceptance.

## 3. Computing the projected residual without an exact pseudoinverse

Forming a dense exact pseudoinverse is unnecessary. Let `P` be a square
matrix proposed as an inverse square root of the Gram matrix `J*J`.
Certify

$$
H=P^*J^*JP,\qquad \|H-I\|\le\eta<1,\qquad \|P\|\le p.
                                                                    \tag{6}
$$

This also proves that `P` is invertible and `J` has full column rank.
For a residual vector `r=Y-F(theta_tilde)`, compute

$$
w=P^*J^*r,\qquad a=Pw.                                    \tag{7}
$$

Both matrix-vector products can be performed exactly when the reference
Jacobian, proposed preconditioner, data, and output are rational.

**Lemma 2 (retained preconditioned vector).** A valid correction bound is

$$
b(\widetilde\theta)=\min\left\{
 \|a\|+\frac{p\eta}{1-\eta}\|w\|,
 \frac{p}{1-\eta}\|w\|\right\}.                            \tag{8}
$$

Moreover, the exact correction differs from the computed vector `a`
by at most `p eta ||w||/(1-eta)`.

**Proof.** Equation (6) implies

$$
J^\dagger r=P H^{-1}w
           =Pw+P(H^{-1}-I)w.
$$

The Neumann-series bounds give `||H^(-1)||<=1/(1-eta)` and
`||H^(-1)-I||<=eta/(1-eta)`. Applying them proves both bounds in (8)
and the error estimate for `a`. QED.

The first bound retains cancellation inside the actual vector `Pw`.
Replacing it by `p||w||` can lose considerable accuracy. On the selected
output, taking norms before this multiplication would give a fixed-point
distance bound about `2.39e-14`; retaining the vector gives `4.29e-16`.
This changes the certificate, not the numerical output.

These are standard verified-residual and contraction principles. See
S. M. Rump, *Verification methods: Rigorous results using floating-point
arithmetic*, Acta Numerica **19** (2010), 287–449, particularly the
preconditioned residual bounds of Section 10.3 and the nonlinear verification
methods of Section 13 ([corrected author text](https://www.tuhh.de/ti3/paper/rump/Ru10.pdf)).
No new general fixed-point or interval-arithmetic machinery is claimed.
The application here connects those principles to the global source
enclosures supplied by the copy and response identities.

## 4. Application to the shared matching source

The source and data are those of the
[four-observation visible-noise certificate](shared-source-recovery-visible-noise-2026-09-27.md).
There are seven sites of local dimension three, four sets of means,
and one shared collection of edge matrices. The parameter vector contains
78 free mean coordinates and 189 edge entries, for a total of 267.
The output stacks four tensors, with 8,748 entries.

The first observation fixes the common product-one site-scaling gauge:
its first mean coordinate is held fixed at each site except the last.
The later means and all shared edges are free. Every compatible source
has already been enclosed in this gauge. All parameter distances and
mean-space angles below refer to it.

The earlier certificate supplies an outer correction radius about
`5.48e-7`, but subsequently sharpens the global source error to
`R=1.71858e-11`. Use this much smaller, already verified ball in (1).
Its Hessian bound is inherited from the same certified unit ball.
The new contraction factor is then about `1.5688e-5`, rather than using
the earlier upper bound of one half. The center test in Theorem 1 is
checked again on this smaller ball.

The integer Gram preconditioner from the input certificate is checked
again against the exact joint Jacobian. Its rational entries give
`eta<=1.31109e-10`. The implementation bounds `p` by the Frobenius norm
of `P`, and computes the two products (7) using integers with common
denominators. All square roots are rounded upward with rational bounds.

**Corollary 3 (validated means and common edges).** Each accepted output
has common-edge error and total mean error at most the source bound (5).
Let `V_tilde` be its `21 by 4` matrix of concatenated mean columns, and
certify a lower bound `sigma_0>0` on its smallest singular value. If the
source bound `E` is less than `sigma_0`, every compatible mean space has
rank four and largest principal-angle sine at most `E/sigma_0`.
Replacing `E` by the fixed-point distance (4) gives the corresponding
statement relative to the exact correction fixed point.

**Proof.** Mean and edge entries are subvectors of the full parameter
error, so each inherits (5). The mean-matrix Frobenius error is bounded
by the total mean error. The rank and angle estimates follow from
Corollary 3 of the shared-source note, whose elementary projection proof
is stated there. The same argument applies to the means of the fixed
point. QED.

The target mean space is the span of the four **observed global mean
vectors**, not an unobserved latent space. The exact fixed point is a
well-defined data-dependent estimate; it is not identified with the true
source in the presence of noise.

## 5. Numerical proposal and exact acceptance

The proposal constructs the reference Jacobian in binary64, freezes its
Gram matrix, and takes three steps

$$
x_{k+1}=x_k+\mathrm{solve}(J^tJ,\ J^t(Y-F(x_k)))
$$

using ordinary floating-point operations. Here `solve` denotes the
numerical linear-system solver; this display describes the implementation,
not an exact identity accepted by the proof. Each output is stored using
`float.hex()`, which specifies its binary64 coordinates exactly.

Acceptance converts these coordinates into exact dyadic rationals.
To evaluate the matching tensor, choose a common denominator `s` for
all mean and edge entries, scale means by `s` and edges by `s^2`, and
evaluate the matching recurrence with arbitrary-size integers. Every
term at seven sites has denominator `s^7`. This avoids trusting a
floating evaluation of a residual near machine resolution.

For each stored output the verifier checks the source-ball membership,
recomputes the tensor and projected residual, applies (8), and computes
the source and mean-space bounds. It selects the output with the smallest
certified fixed-point distance. All three outputs and their checks remain
in the certificate.

| Output | Certified distance to exact fixed point | Certified error to every compatible source |
| --- | ---: | ---: |
| Starting candidate, with the new tighter analysis | `6.56369e-14` | `4.37291e-12` |
| Numerical step 1 | `4.28822e-16` | `4.30771e-12` |
| Numerical step 2 | `9.32712e-16` | `4.30821e-12` |
| Numerical step 3 | `1.43360e-15` | `4.30871e-12` |

For the selected first output, the mean-space angle-sine bound is
`1.38047e-11` relative to a compatible source and `1.37422e-15` relative
to the exact fixed point. Its displacement from the starting candidate
is about `6.56e-14`. The full tensor residual is about `9.47e-13`, within
the stacked budget of about `9.63e-13` for this example.

The table lists rounded descriptive decimals. Acceptance uses rational
inequalities. The later outputs have larger certified bounds; this does
not by itself prove that their actual distances to the fixed point are
larger. The recorded run provides no claim of monotone floating-point
convergence.

The previous published source-error bound was `1.719e-11`. Most of the
reduction to the new bounds comes from shrinking the certified ball and
using its smaller contraction factor. The first table row separates that
improvement from the additional effect of numerical correction. In this
synthetic test, the starting candidate was already the planted source,
so the correction's nonzero displacement is an actual error relative to
that known source. All conditional error bounds continue to hold.

## 6. Replay and separate checks

From the repository root, with the existing NumPy, SciPy, SymPy, and
python-flint research environment:

```sh
OPENBLAS_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 .venv/bin/python \
  computations/matching-tensor-recovery-2026-09-26/verify_validated_source_correction.py
```

The default replay first rechecks the complete global shared-source chain,
including all four observation certificates. It then disables the numerical
correction solver and verifies the saved binary64 values. It separately
checks reference derivative entries and corrected tensor entries through
scalar matching recursions.

The normal residual `J*r` is independently assembled column by column.
A mean derivative inserts one coordinate vector and the matching tensor
on the complementary sites. An edge derivative inserts two coordinate
vectors and the complementary matching tensor, summed over observations
for a shared edge. Contracting these tensors directly with residual
slices checks the dense Jacobian multiplication and parameter layout.
The two preconditioner products are also checked by scalar integer sums.

A separate `3 by 2` rational linear example has a nonzero Gram-preconditioner
defect. Its analytic pseudoinverse checks (8) on 27 residual vectors.
A zero residual must yield zero correction bound, and an output outside
the certified source ball must be rejected.

The implementation and artifacts are:

- [Generator and acceptance code](../computations/matching-tensor-recovery-2026-09-26/validated_source_correction.py).
- [Saved binary64 outputs and certificate](../computations/matching-tensor-recovery-2026-09-26/validated-source-correction-certificate.json).
- [Replay](../computations/matching-tensor-recovery-2026-09-26/verify_validated_source_correction.py)
  and [audit](../computations/matching-tensor-recovery-2026-09-26/validated-source-correction-audit.json).

The numerical proposal may vary across numerical-library builds. Replay
uses the stored exact output values and requires no numerical solve.
This is an exact computational audit with separate constructions; it
shares the inequality code and arithmetic libraries with the generator,
and is not an independent mathematical review.

## 7. Boundary of the result

The earlier gap between an exact convergence theorem and an actual
computed output is now closed for this shared-source example, through
a posteriori validation. There is still no guarantee for every floating
trajectory or source, and no experimental-noise threshold. The certificate
remains conditional on the input error budgets and existence of a common
compatible source. Larger noise, compressed observations, and nongeneric
source classification remain open. No additional claim about the
Krenn–Gu paper or its Lean formalization follows from this research artifact.
