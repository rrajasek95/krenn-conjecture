# The six-site W design is locally optimal among unrestricted complex sources

September 26, 2026. **Written local proof with an exact rational
second-variation certificate; independent audit pending.**

[Replay](../computations/w-state-local-optimum-2026-09-26/README.md) ·
[All-even two-root optimum](w-state-two-root-optimum-2026-09-26.md) ·
[Illustrated guide](../explainers/BOUNDARY-STRUCTURE.md)

## 1. An unrestricted local theorem

Use sites 0 through 4 as the core and site 5 as the distinguished root.
Define the source \(A_*\) by

\[
 (A_*)_{ij}(a,a)=\sqrt{26}\quad(0\le i<j<5),
\]
\[
 (A_*)_{i5}(b,a)=5,\qquad (A_*)_{i5}(a,b)=1\quad(i<5),
\]

with every other cell zero. Then
\(H(A_*)=390W_6\), \(S(A_*)=390\), and \(R(A_*)=1/65\).

**Theorem.** In some neighborhood of \(A_*\), every arbitrary complex
matching source with exact nonzero output proportional to \(W_6\) satisfies

\[
                              R\le1/65.
\]

No scalar-core or two-root restriction is imposed on the perturbation.
All 135 ternary source cells are allowed; any larger finite palette is
covered by projection onto the target colors. After fixing the output
amplitude, equality holds locally precisely on the vertex-phase orbit

\[
 A_{ij}(h,k)\mapsto e^{i(\theta_i+\theta_j)}A_{ij}(h,k),
                  \qquad\sum_i\theta_i=0.
\]

These phases preserve the full output tensor and every source-cell magnitude.
With the amplitude free, overall nonzero complex scaling is also allowed.
The proof gives existence of a neighborhood, not a numerical radius.
It does not exclude a better design far from this orbit.

## 2. Rational coordinates for every binary source cell

For this calculation only, rescale **all** non-root cells by \(\sqrt{26}\):
write \(A_{ij}(h,k)=\sqrt{26}\,z_{ij}(h,k)\) when \(j<5\), and
\(A_{i5}(h,k)=z_{i5}(h,k)\). This is an invertible coordinate change,
including cells that vanish at the displayed design.

Every perfect matching contains two non-root edges and one root edge, so

\[
                    H(A)=26H(z),\qquad S(A)=z^*Gz,
\]

where \(G\) is diagonal, equal to 26 on the forty non-root binary cells
and 1 on the twenty root cells. The base \(z_*\) has only integer entries:
core \(aa\) entries 1, incident \(ba\) entries 5, and incident \(ab\)
entries 1. Its output is \(H(z_*)=15W_6\).

Thus all derivatives and norm forms below have rational coefficients.

## 3. Exact first and second variations

Let \(J=DH(z_*)\), a 64-by-60 real rational matrix. Choose an output
multiplier \(y\) supported on the six W words: weight \(5/3\) for an
excitation at a core site and \(1/3\) for an excitation at the root.
The exact stationarity identity is

\[
                              J^T y=Gz_* .              \tag{1}
\]

Put \(B=\sum_w y_w D^2H_w(z_*)\), a symmetric rational matrix, and let
\(V=\ker J\). The checker computes \(\operatorname{rank}J=32\), so
\(V\) has real dimension 28. It checks the two restricted quadratic forms

\[
                  Q_R=(G-B)|_V,\qquad Q_I=(G+B)|_V.
\]

Exact rational elimination gives:

| Form | Positive directions | Zero directions |
|---|---:|---:|
| \(Q_R\), real perturbations | 28 | 0 |
| \(Q_I\), imaginary perturbations | 23 | 5 |

Every positive pivot is recorded in the replay receipt. The checker verifies
that any zero-diagonal Schur remainder is the zero matrix, so this is a
positive-semidefinite certificate, not a floating-point eigenvalue test.

For \(j=0,\ldots,4\), take vertex phases with \(\theta_j=1\),
\(\theta_5=-1\), and all others zero. Their real coefficient vectors are

\[
                  (g_j)_{uv}(h,k)=(\theta_u+\theta_v)
                                             (z_*)_{uv}(h,k).
\]

The actual tangent perturbations are \(ig_j\). The checker verifies
\(Jg_j=0\), \(Q_I(g_j)=0\), and independence of these five vectors.
They therefore span the **entire** nullspace of \(Q_I\). There is no
additional zero direction in the unrestricted binary tangent space.

## 4. Why the certificate proves a local minimum

Consider the real-valued Lagrangian

\[
 \mathcal L(z)=\tfrac12 z^*Gz-\operatorname{Re}\sum_w y_wH_w(z).
\]

Equation (1) makes its first derivative zero at \(z_*\). For
\(z=z_*+u+iv\), its quadratic part is

\[
                    \tfrac12 u^T(G-B)u+
                    \tfrac12 v^T(G+B)v.                 \tag{2}
\]

First fix the harmless vertex phases. In a neighborhood of the base, a
unique small phase adjustment places the imaginary displacement in the
\(G\)-orthogonal complement of \(g_0,\ldots,g_4\). This follows from
the implicit function theorem: the derivative of the five phase conditions
is their positive definite \(G\)-Gram matrix. The adjustment preserves
both the output and the source norm.

For an exact feasible displacement \(\delta=u+iv\), the polynomial
constraint \(H(z)=H(z_*)\) gives

\[
                      Ju=O(\|\delta\|^2),\qquad
                      Jv=O(\|\delta\|^2).
\]

Hence the components normal to \(V\) are \(O(\|\delta\|^2)\).
This uses a bounded inverse on the fixed orthogonal complement of \(V\);
it does **not** assume the output constraints are independent or that the
feasible set is smooth. The \(G\)-orthogonal projection of \(v\) onto
\(V\) retains the phase-fixing conditions because each \(g_j\in V\).

On this phase-fixed tangent space, (2) is positive definite. Taylor expansion
and the exact output constraint therefore give constants \(c>0\) and a
sufficiently small neighborhood such that

\[
                         S(A)-S(A_*)\ge c\|\delta\|^2.
\]

The cubic remainder is absorbed by the positive quadratic term. This proves
a strict minimum on the phase slice and therefore a local minimum modulo
the phase orbit. The singularity of the constraint variety causes no gap
in this sufficiency argument.

## 5. Amplitude normalization and additional colors

If a nearby source has output \(\mu W_6\), \(\mu\ne0\), multiply it by
the branch of \((390/\mu)^{1/3}\) near one. This fixes the output at
\(390W_6\) and leaves \(R=\|H\|^2/S^3\) invariant.

For a source with additional endpoint colors, discard every cell using a
color outside \(a,b\). All binary output coefficients are unchanged, and
all other outputs of the projected source vanish. It is therefore still an
exact W source, while its source norm cannot increase. Apply the binary
local minimum and then restore the discarded nonnegative source energy.
Equality forces that additional energy to be zero.

This completes the unrestricted local theorem. The global problem remains:
another component of the exact-W source set could have a better rate.
