# Bianchi cycle mixing preserves the selector sum obstruction

## 1. Outcome

The [cycle-span repair](k6-cycle-span-hessian-mixing.md) and the
[selector sum-channel guard](two-chart-selector-provenance-sum-channel-guard.md)
fit together without tension.  Mixing the two cross orientations can
remove an aggregate Hessian-kernel pairing, but a Bianchi difference cannot
remove the selector-family provenance class while retaining cap detection,
provided the aggregate normals and physical curvature tables are combined
coefficientwise as in Section 4.

Let

\[
 \mathcal Q_d=\operatorname {Mat}_2/(\Delta+\mathbb C d)
\]

be the completed-square selector quotient.  At one coefficient write

\[
 H=R_{\bullet k}F_{\bullet l}^{\mathsf T},\qquad
 G=E_{\bullet l}T_{\bullet k}^{\mathsf T},\qquad B=H+G,
\]

and let the two oriented curvature tables be

\[
                         K_H=ud-H,\qquad K_G=ud-G.       \tag{1}
\]

If the Bianchi difference is class-zero,

\[
                              [H-G]=0,                   \tag{2}
\]

then

\[
             \boxed{[K_H]=[K_G]=-\tfrac12[B].}           \tag{3}
\]

Consequently every mixture satisfies

\[
                   [aK_H+bK_G]=-\frac{a+b}{2}[B].       \tag{4}
\]

For a pure cap-edge coefficient cut, the two four-cycle orientations have
the same cap evaluation \(c\ne0\).  Their corresponding mixture detects
the cap by

\[
                         (a\lambda_H+b\lambda_G)(\beta)
                              =(a+b)c.                   \tag{5}
\]

If \([B]\ne0\), equations (4)--(5) give the exact lock:

> every mixture which retains cap detection has nonzero selector
> provenance class, while every mixture in the Bianchi-difference
> direction has zero cap detection.

Thus adding orientation differences may repair the aggregate Hessian
equation, as it does in the corank-one guard, but cannot by itself produce
the required filtered source lift.

## 2. Proof

Modulo \(\Delta+\mathbb C d\), equation (1) gives

\[
                         [K_H]=-[H],\qquad [K_G]=-[G].
\]

Equation (2) says \([H]=[G]\), whereas \(B=H+G\) says
\([B]=2[H]\).  Characteristic zero now gives (3), and linearity gives (4).

For the pure coefficient direction
\(\beta=\beta_{rs}\mathbf e_{rs}\), both oriented cycle polynomials have
the same direct-matching term

\[
                         q_{rs}q_{uv}.
\]

Their different cross terms do not meet \(\beta\), so both differentials
take the value \(c=\beta_{rs}q_{uv}\).  This proves (5).  When the
coefficient cut has been normalized by the dark matching, \(c\ne0\).
Equations (4)--(5) prove the lock.

## 3. The exact integral guard

In the integral triangle packet from the sum-channel note, at the
\((\alpha,\alpha)\) coefficient,

\[
 d=\begin{pmatrix}1&1\\1&2\end{pmatrix},\qquad
 H=G=\begin{pmatrix}0&1\\0&1\end{pmatrix},\qquad u=0.
\]

With

\[
 \omega_d(X)=d_{21}X_{12}-d_{12}X_{21},
\]

one has

\[
 \omega_d(B)=2,\qquad
 \omega_d(K_H)=\omega_d(K_G)=-1.                         \tag{6}
\]

For the formal common-evaluation vector \((c,c)=(1,1)\), the mixture
\((a,b)=(2,-1)\), matching the coefficients of the explicit Hessian
repair, has evaluation \(a+b=1\) and provenance value \(-1\).  The pure
Bianchi difference \((1,-1)\) has both values zero.  This is not a
numerical coincidence; it is (4)--(5).

The triangle guard itself specifies only endpoint block tables.  It supplies
no scalar base \(q\), cap direction \(\beta\), complementary dark matching,
or common-evaluation vector, and therefore has no dark cap of its own.  It
audits the quotient half of the lock exactly; the common-evaluation half is
the separate pure coefficient-cut calculation in Section 2.

## 4. Exact scope and next lemma

The argument assumes that the two aggregate orientation normals and the
two physical curvature tables are compared linearly with the same
coefficients.  It proves an obstruction under that natural
grade-preserving comparison; it does not construct the comparison map.
Nor is the integral triangle a complete full-nine source.

The remaining positive input must either force \([B]=0\) using extra physical
equations, or supply an additional grade-preserving row with class
proportional to \([B]\).  In the displayed guard
\((d_{12},d_{21})\ne(0,0)\), so \(\mathcal Q_d\) is one-dimensional and any
new nonzero class can be normalized to represent the assignment-sum class.
A differently labelled diagonal anchor or a crossed full-nine row transported
through the second chart is the available source of such a grade split.  More
class-zero Bianchi differences at this coefficient cannot provide it.

The dependency-free
[checker](../computations/verify_cycle_mixing_selector_sum_lock.py) audits
(3)--(6) for every small integral mixture in the exact guard.
