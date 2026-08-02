# The common-coloop polar dual closes the fixed missing diagonal

Research evidence only. Krenn's conjecture remains open, the dashed
clean-point implication is not proved, and the certified spine is
untouched.

## Outcome

The
[anchor--polar response quotient](common-coloop-anchor-polar-response-quotient.md)
reduces a common-coloop clean fibre at an attainable scalar \(z\) to

\[
 m_D(z)v=b_z,\qquad v\in\mathcal R_0,                        \tag{1}
\]

with diagonal values

\[
                   \kappa_i^z+\partial_i^A(v),
 \qquad i=0,1,2.                                             \tag{2}
\]

Here

\[
 m_D(z)v=vD_{\bar K}(z),\qquad
 vA=\sum_i\partial_i^A(v)X_i,\qquad A=q_0^{[h-1]}.           \tag{3}
\]

This note gives an exact dual classification of every remaining failure
in (1)--(2).

* The polar cokernel class survives exactly when a coefficient covector
  annihilates every \(vD_{\bar K}(z)\) but detects \(b_z\).
* On a consistent fibre, diagonal \(i\) is forced to zero exactly when a
  coefficient covector transports the \(X_i\)-coordinate of \(vA\)
  through \(D_{\bar K}(z)\), with the matching affine constant.
* In every singleton or binary one-corner branch, the fixed missing label
  \(t\) has \(\partial_t^A=0\) and \(\kappa_t^z=\kappa_t^0\ne0\).
  Therefore its forced-diagonal stratum is empty.

The last item closes one of the three forced-diagonal possibilities in
every one-corner branch. At any nonzero attainable scalar where (1) is
consistent, only the two nonmissing labels can still obstruct activity.
If neither of their transport covectors exists, an active clean
completion follows.

The two residual transport tests must be evaluated on the literal
singleton/binary arm responses before multiplication by \(A\). This
identifies exactly how the two rows omitted by the diagonal-complete
\(7/9\) guard can be used positively; it does not prove that they always
defeat the covectors.

## 1. Dual classification of the polar cokernel

Fix \(z\) and abbreviate

\[
 R=\mathcal R_0,\qquad
 M=m_D(z):R\longrightarrow E,\qquad b=b_z.
\]

Finite-dimensional duality gives

\[
 \boxed{\quad
 b\notin\operatorname{im}M
 \Longleftrightarrow
 \exists\,\Lambda\in E^*:
 \Lambda M=0,\quad\Lambda(b)\ne0.
 \quad}                                                       \tag{4}
\]

Thus a surviving polar cokernel is not merely a rank defect. It has one
exact coefficient witness which kills the polar image of every allowed
tangent response at the same scalar and detects the affine residual.
The response and scalar have not been freed.

In common-coloop notation, (4) is

\[
 \Lambda\bigl(vD_{\bar K}(z)\bigr)=0
       \quad(v\in\mathcal R_0),
 \qquad
 \Lambda(b_z)\ne0.                                          \tag{5}
\]

To close this stratum from the literal source, it is enough to show that
every covector detecting \(b_z\) also detects the polar image of at least
one full-nine arm response.

## 2. Dual classification of a forced diagonal

Assume now that (1) is consistent, and choose one solution \(v_0\). The
response-quotient theorem says that diagonal \(i\) is forced to zero
precisely when

\[
 \kappa_i^z+\partial_i^A(v_0)=0,
 \qquad
 \partial_i^A|_{\ker M}=0.                                  \tag{6}
\]

The second condition in (6) is equivalent to
\(\partial_i^A\in\operatorname{rowspan}M\). Hence there is a covector
\(\Lambda_i\in E^*\) with

\[
                       \Lambda_iM=\partial_i^A.              \tag{7}
\]

Since \(Mv_0=b\), the first condition becomes

\[
                       \Lambda_i(b)=-\kappa_i^z.             \tag{8}
\]

Conversely, (7)--(8) force (6). Therefore

\[
 \boxed{\quad
 i\text{ is forced zero}
 \Longleftrightarrow
 \exists\,\Lambda_i:
 \begin{cases}
 \Lambda_i(vD_{\bar K}(z))
       =\partial_i^A(v)=[X_i](vA)&(v\in\mathcal R_0),\\
 \Lambda_i(b_z)=-\kappa_i^z.&
 \end{cases}
 \quad}                                                       \tag{9}
\]

If two choices of \(\Lambda_i\) satisfy (7), their difference annihilates
\(\operatorname{im}M\). Because \(b\in\operatorname{im}M\), both have the
same value on \(b\). Thus the affine condition (8) is well defined.

Equation (9) is the exact \(A\)-to-\(D\) comparison which a forced
diagonal would require. It is source-faithful: the right side is the
literal \(X_i\)-coordinate of multiplication by the first common power
\(A\), the left side uses the polar difference, and both use the same
response \(v\) at the same scalar.

## 3. Closure of the fixed missing diagonal

Let \(t\) be the missing label in a singleton or binary one-corner
branch. By definition,

\[
                         c_t=d_t=0.                           \tag{10}
\]

For every tangent parameter
\(L=c\eta^{\mathsf T}+\xi d^{\mathsf T}\),

\[
              \delta_t(L)=c_t\eta_t+\xi_td_t=0.             \tag{11}
\]

Consequently

\[
                 \partial_t^A=0,\qquad
                 \kappa_t^z=\kappa_t^0
                 \quad\text{for every attainable }z.        \tag{12}
\]

The one-corner affine coset contains an active matrix only on the branch

\[
                         \kappa_t^0\ne0.                     \tag{13}
\]

Suppose the clean equation (1) is consistent. If \(t\) were forced zero,
(9) would give a left annihilator \(\Lambda_tM=0\) with

\[
                    \Lambda_t(b)=-\kappa_t^0\ne0.            \tag{14}
\]

But \(b=Mv_0\), so every left annihilator of \(M\) vanishes on \(b\).
This contradicts (14). Equivalently, (2) shows directly that the
\(t\)-diagonal is the fixed nonzero number \(\kappa_t^0\).

Hence:

> **Fixed-missing-diagonal theorem.**
> On every active singleton or binary one-corner affine coset, the missing
> diagonal is never forced to zero on a consistent clean response fibre.
> Only the two nonmissing diagonal loci remain.

The hypothesis (13) is sharp. If \(\kappa_t^0=0\), then the missing
diagonal is identically zero before cleanliness is imposed and is forced
on every consistent fibre, independently of \(D_{\bar K}(z)\).

## 4. Literal arm interpretation

In the disjoint singleton normalization

\[
                         c=e_r,\qquad d=e_s,\qquad r\ne s,
\]

the response before quotienting is

\[
 w(L)=u\,\bar S(\eta)+\bar P(\xi)\,v_{\mathrm{loc}},         \tag{15}
\]

while the only varying diagonal coordinates are

\[
                         \delta_r=\eta_r,\qquad
                         \delta_s=\xi_s,\qquad
                         \delta_t=0.                          \tag{16}
\]

After imposing the fixed-scalar equation, the literal left and right arm
responses in (15) span \(\mathcal R_0\). A forced \(r\)-diagonal requires
one covector \(\Lambda_r\) satisfying

\[
 \Lambda_r(wD(z))=[X_r](wA)
 \quad\text{on every left and right arm generator},          \tag{17}
\]

and similarly for \(s\). A polar cokernel witness must instead annihilate
the \(D(z)\)-image of every arm while detecting \(b_z\).

The binary one-corner branch has the same ledger after replacing the
singleton generators by its two-supported, locally aligned arm
responses. Its star-only anchor relations specify the \(A\)-coordinates
on those generators, so (17) must be checked before multiplying away the
common power.

This explains the exact role of the two arms absent from the
[diagonal-complete \(7/9\) guard](common-coloop-diagonal-arm-resultant-boundary.md).
That guard does not test (17) on both arm generators. Conversely, the
earlier
[missing-row \(A\)-to-\(D\) guard](common-coloop-a-to-D-overlap-attack.md)
shows that annihilation after multiplication by \(A\) alone cannot rule
out (5) or (17). The remaining proof must use the simultaneous literal
arm representatives.

## 5. Positive subcases and exact residue

At an attainable scalar \(z\ne0\) in a one-corner branch, an active clean
completion exists in either of the following exact situations.

1. The polar map is consistent and its kernel contains a response whose
   \(A\)-coordinate is nonzero for each nonmissing label.
2. More generally, the polar map is consistent and neither of the two
   interpolation systems (9) for the nonmissing labels has a solution.

The missing diagonal is already safe by the theorem above. Thus the
remaining bad locus at a fixed scalar is the union of only three dual
strata:

\[
\begin{array}{ll}
\text{polar cokernel:}&
 \Lambda M=0,\quad\Lambda(b)\ne0,\\[2mm]
\text{forced }r:&
 \Lambda_rM=\partial_r^A,\quad
 \Lambda_r(b)=-\kappa_r^z,\\[2mm]
\text{forced }s:&
 \Lambda_sM=\partial_s^A,\quad
 \Lambda_s(b)=-\kappa_s^z.
\end{array}                                                   \tag{18}
\]

This is strictly smaller than the four tests in the unrestricted response
quotient and retains the branch labels. Proving that one attainable
nonzero scalar avoids (18), using both literal arms or a nonflat
source-provenant overlap, remains open.

## 6. Exact audit and sharp guard

The dependency-free checker
[verify_common_coloop_polar_dual_forced_diagonal_boundary.py](../computations/verify_common_coloop_polar_dual_forced_diagonal_boundary.py)
uses an independent exact-rational row reducer. For each possible missing
label \(t=0,1,2\), it verifies:

* primal/dual equivalence of polar cokernel detection;
* primal/dual equivalence of forced-diagonal detection;
* a consistent positive kernel stratum;
* one forced nonmissing diagonal with its transport covector;
* impossibility of forcing the fixed nonzero missing diagonal; and
* sharpness when that fixed diagonal is set to zero.

The twelve-case ledger has SHA-256

    5384677b2b3f009baff38b05598cdea4271a3df4a34e66306e5b23a37f795a3d

The rational examples are sharp guards for the response-quotient linear
theorem, not synthetic Krenn sources. The closure of the missing diagonal
is source-level: it follows directly from the branch equations
(10)--(13), independently of the examples.

## 7. Scope

The result closes one forced-diagonal stratum on every singleton and
binary one-corner branch and dualizes all remaining failures. It does not
prove polar consistency, exclude the two labelled interpolation
covectors, or close the common-coloop boundary. Krenn's conjecture and the
dashed clean-point implication remain open.
