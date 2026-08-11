# The first normal/Rees correction gives a full-rank invisible boundary

This is the exact first-normal calculation requested after `5462b2a`.  It is
positive at the associated-graded level: there is no primitive normal
separator.  The remaining issue is an all-order physical lift, not another
set-theoretic face-zero test.

## The cyclotomic stratum is transverse in all five face directions

Normalize the five cycle edges of (q_m) to one and write

\[
 A=q_{13},\quad B=q_{14},\quad C=q_{24},\quad
 D=q_{25},\quad E=q_{35}.
\]

At the cyclotomic point (A=B=C=D=E=\zeta), the Jacobian of
((h_1,\ldots,h_5)) with respect to these five chord coordinates is

\[
J=
\begin{pmatrix}
0&0&\zeta&1&\zeta\\
1&\zeta&0&0&\zeta\\
0&\zeta&1&\zeta&0\\
\zeta&0&0&\zeta&1\\
\zeta&1&\zeta&0&0
\end{pmatrix},
\qquad
\det J=-4-8\zeta\ne0.                                  \tag{1}
\]

Thus the five face equations are regular normal coordinates on this chart.
Let (n^{(v)}) be the chord direction given by the (v)-th column of
(J^{-1}).  Then

\[
                         dh_w(n^{(v)})=\delta_{wv}.      \tag{2}
\]

The checker constructs (J) from the literal three-matchings face formulas,
computes its inverse over
(\mathbb Q[\zeta]/(\zeta^2+\zeta+1)), and verifies (2) by expanding every
quadratic (h_w), including its order-two remainder.

## Honest first Rees quotient

Along the normal arc

\[
                         q(\tau)=q_0+\tau n^{(v)},       \tag{3}
\]

the exact expansion is

\[
 h_w(q(\tau))=\tau\delta_{wv}+\tau^2R_{wv}.             \tag{4}
\]

The composed two-chart Schur tail is

\[
             \bigl(h_w(q(\tau)),-h_w(q(\tau))\bigr).
\]

Divide by the Rees parameter and set (\tau=0).  Equations (2)--(4) give

\[
                  \bigl(\delta_{wv},-\delta_{wv}\bigr). \tag{5}
\]

Reading the chart-odd half-difference, the five normal directions therefore
have boundary matrix

\[
                                I_5.                    \tag{6}
\]

This is not a set-theoretic evaluation of (h=0): it is the divided first
normal class in the Rees/normal cone.

## Target and ordinary residue

Every complete face word remains mixed throughout (3), so the physical
target is identically zero.  In the old split-cap landing, the two tagged
sectors have the same ordinary-residue reading.  Their signs in (5) are
opposite, hence

\[
                         \operatorname {ores}(5)=0       \tag{7}
\]

for every normal direction.  Thus the first-normal boundary is nonzero and
full rank, while target and old ordinary residue both vanish.

After localizing the selected curvature scalar, (6) becomes

\[
                              \kappa I_5.               \tag{8}
\]

Its determinant is (\kappa^5), a unit.  Therefore there is no nonzero
primitive normal covector separating the available boundaries: the normal
separator dimension is zero.

## Exact consequence and scope

At the associated-graded normal level, the desired phenomenon occurs:
the composed covariance/Schur construction supplies five independent
nonzero (\kappa)-localized chart-odd boundaries with

\[
                         \mathrm{tgt}=\mathrm{ores}=0.   \tag{9}
\]

This removes the first-normal obstruction exposed by `5462b2a`.

It is not yet the full Component-IV theorem.  Two load-bearing promotions
remain:

1. lift the normal/Rees classes through higher order to an honest
   source-provenant chain in the completed physical quotient; and
2. identify the chart-odd boundary (6), with its normalization and chart
   labels retained, with the final physical cap (w)-coordinate used by the
   target-augmented attaching theorem.

The calculation proves that neither promotion can fail for a first-normal
rank reason; a failure must occur in higher compatibility or in the physical
boundary-identification map.

## Verification

Run

```text
.venv/bin/python computations/verify_h3_component_iv_cyclotomic_normal_rees_boundary.py
.venv/bin/python -O computations/verify_h3_component_iv_cyclotomic_normal_rees_boundary.py
```

The checker uses exact quadratic-field arithmetic, reconstructs the Jacobian
and its inverse from matching formulas, expands the full quadratic Rees arcs,
and verifies the boundary, target, ordinary-residue, and
(\kappa)-localized ranks.
