# The actual order-four cube leaves a pure Eq face, not a forced curvature face

This audit starts from the literal denominator-marked faces of commit
ed60e2c and the shifted two-chart square of commit e7723de. It does **not**
declare an attaching chain or a new generator. Its purpose is to write the
complete cubical/Leibniz boundary and identify the first face that fails
after descent to the physical two-row complex.

## Exact boundary identity

Fix a deleted odd site \(v\), a matching \(N=\{e,f\}\) of its four-site
complement, and the four physical directions

\[
 I=\{a_{xv}^{0m_v},a_{pq}^{22},e,f\}.
\]

Put \(A=H_m\) and \(B=H_0-u\). For squarefree Hasse row copies, the
Leibniz differential is

\[
 d r_0[U]=B e_{\rm Eq}[U],\qquad
 d r_m[U]=\sum_{S\subseteq U}(\partial_S A)
                       e_{\rm Eq}[U\setminus S].       \tag{1}
\]

The actual full four-cube chain forced by (1) is

\[
 \boxed{
 s_I=\sum_{S\subseteq I}(\partial_S A)r_0[I\setminus S]
          -B r_m[I].}                                  \tag{2}
\]

It has sixteen \(r_0\) faces and one \(r_m\) correction. Every Leibniz
commutator is visible in

\[
\begin{aligned}
 d s_I
 &=\sum_{S\subseteq I}B(\partial_S A)e_{\rm Eq}[I\setminus S]
   -B\sum_{S\subseteq I}(\partial_S A)e_{\rm Eq}[I\setminus S]\\
 &=0.                                                   \tag{3}
\end{aligned}
\]

Thus no proper face may be omitted. The existing cap generator satisfies
\(dT=-Yw\), so, without naming or adjoining a new attaching generator,

\[
                         d(s_I-T)=Yw.                  \tag{4}
\]

This is an identity in the prolonged presentation cube.

## First uncancelled typed face

The selected directions form a perfect matching, hence
\(\partial_I A=1\). Diagonal descent forgets all positive Hasse copies and
retains only

\[
                         \pi_\Delta(s_I-T)=r_0-T.
\]

With the original physical differential,

\[
 d\pi_\Delta(s_I-T)=(H_0-u)e_{\rm Eq}+Yw,
 \qquad
 \pi_\Delta d(s_I-T)=Yw.
\]

Therefore the first uncancelled typed face is exactly

\[
 \boxed{[d,\pi_\Delta](s_I-T)=(H_0-u)e_{\rm Eq}.}      \tag{5}
\]

The type is load-bearing. The strict \(pq/pr\) comparison has zero global
Eq boundary. The proper denominator faces have support counts
\(5,3,3,1\) and live in the word/presentation-to-cap packet. The cap face
lives on \(w\). None cancels the pure Eq row in (5).

## Why curvature is not forced

The zero-endpoint denominator cube uses
\(a_{xv}^{00},a_{pq}^{00},e,f\), whereas (2) uses
\(a_{xv}^{0m_v},a_{pq}^{22},e,f\). Exact differentiation gives the same top
unit in both cubes. But the endpoint-\(22\to00\) bridge replaces **two**
directions; it is not deletion of one direction and hence is not one of the
eight facets of either four-cube.

Consequently the cubical identity \(D^2=0\), even with every Leibniz term in
(3), does not force a lower curvature face
\(\mathfrak C_{22\to00}\). Such a face would be an additional typed
comparison between the two endpoint cubes. The first equation that an
actual source-relative construction must solve is (5); merely inserting a
curvature symbol would assume the missing comparison.

## Verification

Run

    python3 computations/verify_h3_order4_denominator_cube_boundary.py
    python3 -O computations/verify_h3_order4_denominator_cube_boundary.py

The checker reconstructs all five deleted sites and all three complementary
matchings. For each of the fifteen cubes it verifies all sixteen paired
Leibniz cancellations, the seventeen-term lift, all sixteen strict-chart
face cancellations, all four external sector faces, the \(5,3,3,1\)
denominator ledger, equality of the two endpoint top units, and the typed
residual (5).

The frozen certificate digest is

    063f6306ef3e87c53903162cff6fdaca27e7fe41d03a36f01fff585666627486
