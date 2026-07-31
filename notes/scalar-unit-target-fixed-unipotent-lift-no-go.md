# A target-fixed unary unipotent lift contradicts support minimality

## 1. Outcome

Work at a good physical pair \(p,q\) of a minimum-entry-support exact
ternary aggregate source.  Let the residual set have size \(2h\), with
\(h\geq 3\), and suppose that the direct block is the intrinsic scalar
unit

\[
                         A_{pq}=\alpha E_{aa},\qquad \alpha\ne0.
\tag{1}
\]

Write the complete nine pair rows as

\[
 \alpha\delta_{ia}\delta_{ja}q^{[h]}
      +R_{ij}q^{[h-1]}=\delta_{ij}X_i,
 \qquad R_{ij}=p_i s_j.                                  \tag{2}
\]

The target-fixed unary version of the unipotent criterion cannot occur in
a surviving support-minimal counterexample.  Equivalently, constructing
it from the source rows would close the intrinsic scalar-unit branch
directly, by support descent rather than by an active cap.

> **Theorem 1 (unary lift no-go).**  There is no derivation \(\partial\)
> of the residual site algebra satisfying
> \[
>       \partial q=R_{aa},\qquad \partial R_{aa}=0,
>       \qquad \partial X_a=0.                            \tag{3}
> \]
> The same conclusion holds for an exact Hasse--Schmidt translation
> \(\Phi_t\) satisfying
> \[
>       \Phi_t(q)=q+tR_{aa},\qquad
>       \Phi_t(R_{aa})=R_{aa},\qquad
>       \Phi_t(X_a)=X_a.                                 \tag{4}
> \]

Indeed, either lift forces

\[
                         R_{aa}q^{[h-1]}=0.               \tag{5}
\]

Together with the two target-zero rows \(R_{ab}q^{[h-1]}=0\) and
\(R_{ac}q^{[h-1]}=0\), equation (5) says that every response slice whose
\(p\)-endpoint colour is \(a\) is zero.  Deleting the complete aggregate
star row \(p_a\) therefore preserves the exact matching tensor.  Goodness
makes \(p_a\ne0\), so this strictly decreases aggregate entry support,
contrary to the selected representative.

There are two consequences for the proposed proof route.

1. If the complete rows plus one adjacent source chart force (3), that is
   a valid branch-closing theorem: the resulting contradiction excludes
   the scalar-unit configuration from a minimal counterexample.  The
   impossibility of (3) on a surviving representative is the desired
   conclusion of such an argument, not an objection to constructing it.
2. The cap underlying the exceptional unary row is \(K=E_{aa}\).  It is
   clean under the criterion, but it is intrinsically **inactive**, since
   its two complementary diagonal target coordinates vanish.  Thus even
   without invoking the support contradiction, this unary lift would not
   by itself feed `SP-DESCENT` as an active clean cap.

If one insists on passing specifically through `SP-CLEAN-BRIDGE` and
`SP-DESCENT`, the genuinely active version is different.  One must first
choose a cap \(K\) with

\[
       s(K)K_{00}K_{11}K_{22}\ne0                       \tag{6}
\]

and solve

\[
 \partial q=r(K),\qquad \partial r(K)=0,
 \qquad \partial T(K)=0,                                \tag{7}
\]

where

\[
 s(K)=\alpha K_{aa},\quad
 r(K)=\sum_{i,j}K_{ij}R_{ij},\quad
 T(K)=\sum_iK_{ii}X_i.                                  \tag{8}
\]

Then the unipotent response-transgression theorem really does give an
active clean cap (and hence descent).  Equations (7)--(8) are the corrected
target for that particular route.  The unary system (3) remains an equally
valid, and formally stronger, direct scalar-unit branch exclusion if an
adjacent-chart theorem can force it.

This is a uniform invariant obstruction, not a support-case enumeration.

## 2. The triangular consequence forces the selected response to vanish

Put

\[
                   Q_j=R_{aa}^{[j]}q^{[h-j]}
                   \qquad(0\leq j\leq h).               \tag{9}
\]

Under (3), the divided-power product rule gives

\[
                         \partial Q_j=(j+1)Q_{j+1}.       \tag{10}
\]

The exceptional member of (2) is

\[
                         \alpha Q_0+Q_1=X_a.             \tag{11}
\]

Applying \(\partial^k\) to (11), and using target fixation, gives for
\(1\leq k<h\)

\[
                         \alpha Q_k+(k+1)Q_{k+1}=0,       \tag{12}
\]

after division by \(k!\), while the terminal equation is

\[
                         \alpha Q_h=0.                   \tag{13}
\]

Since \(\alpha\ne0\), descending from (13) through (12) yields

\[
                         Q_1=Q_2=\cdots=Q_h=0.           \tag{14}
\]

In particular \(Q_1=R_{aa}q^{[h-1]}=0\), proving (5).

The Hasse--Schmidt form makes the same obstruction coefficientwise and
does not assume that \(\Phi_t\) is the exponential of an ordinary
derivation.  Applying (4) to (11) gives

\[
 \alpha(q+tR_{aa})^{[h]}
   +R_{aa}(q+tR_{aa})^{[h-1]}=X_a.                       \tag{15}
\]

The coefficient of \(t^k\), for \(0\leq k<h\), is

\[
                         \alpha Q_k+(k+1)Q_{k+1},        \tag{16}
\]

and the coefficient of \(t^h\) is \(\alpha Q_h\).  The positive-degree
coefficients reproduce (12)--(14) exactly.

This also shows why a viable ``weaker Hasse--Schmidt chain'' cannot merely
be the same fixed-target translation in different notation.  It must
allow higher corrections, nontrivial response transport, or a filtered
operation that isolates the clean tail without forcing \(Q_1=0\).  Such
an operation is outside the hypotheses of the present no-go and outside
the current unipotent criterion.

## 3. Exact source deletion

Every perfect matching contributing to the source tensor either uses the
direct edge \(pq\), or sends \(p\) and \(q\) to two residual sites.  The
endpoint-colour \((i,j)\) response slice in the second class is exactly

\[
                         R_{ij}q^{[h-1]}.                \tag{17}
\]

Equation (5) kills (17) for \((i,j)=(a,a)\).  The two other entries in
the \(a\)-row of (2) have zero target, so

\[
                         R_{ab}q^{[h-1]}
                         =R_{ac}q^{[h-1]}=0.             \tag{18}
\]

Set the complete residual endpoint row \(p_a\) to zero, leaving the
direct block \(\alpha E_{aa}\), the internal quadratic \(q\), and every
other endpoint row unchanged.  The direct contribution is unchanged.
The only removed response slices are (17) with \(i=a\), and all three
are zero by (5) and (18).  Hence the modified aggregate array remains an
exact ternary source.

Goodness at \(p,q\) means, in particular, that the map

\[
               \mathbb C^3\longrightarrow
               \bigoplus_{x\ne p,q}V_x,
               \qquad e_i\longmapsto p_i                \tag{19}
\]

is injective.  Thus \(p_a\ne0\).  Zeroing it removes at least one nonzero
aggregate scalar entry and adds none, contradicting minimum entry support.
The transpose argument could instead delete \(s_a\).

No cancellation of a matching power and no termwise matching selection is
used in this argument.

## 4. Activity audit and the corrected active target

By the exact cap definitions in
[`clean-pair-cap-exact-descent-target.md`](clean-pair-cap-exact-descent-target.md),
the three target coordinates are
\(\kappa_i(K)=K_{ii}\), while in the scalar-unit chart

\[
                  s(K)=\langle K,\alpha E_{aa}\rangle
                      =\alpha K_{aa}.                    \tag{20a}
\]

Hence activity is exactly

\[
                    s(K)K_{00}K_{11}K_{22}\ne0.          \tag{20}
\]

At the unary cap \(E_{aa}\), one has \(s=\alpha\ne0\), but the other two
diagonal entries are zero, so (20) fails identically.  This conclusion is
coordinate-literal and uses no determinant proxy for activity.

For an active \(K\), contracting all nine rows gives

\[
                    s(K)q^{[h]}+r(K)q^{[h-1]}=T(K).      \tag{21}
\]

If (7) holds, the same triangular proof gives

\[
                    (s(K)q+r(K))^{[h]}
                       =s(K)^{h-1}T(K),                  \tag{22}
\]

which is precisely cleanliness of \(K\).  Now (6) supplies activity, so
the certified clean-pair descent applies.  This corrected formulation can
use an adjacent chart to construct the simultaneous edgewise system for
\(r(K)\).  The unary system for \(R_{aa}\) cannot substitute *as an
active cap*, although forcing it closes the scalar-unit branch by the
separate support argument above.

The stronger triangular conclusion also gives

\[
                    r(K)q^{[h-1]}=0,qquad
                    s(K)q^{[h]}=T(K).                    \tag{23}
\]

Because an active \(K\) has all three diagonal target coefficients
nonzero, (23) itself is an exact smaller ternary source after an explicit
local colour rescaling.  Indeed, put
\(c_i=s(K)^{-1}K_{ii}\ne0\), choose one residual site \(x\), and let the
diagonal automorphism at \(x\) send \(e_i^{(x)}\) to
\(c_i^{-1}e_i^{(x)}\), acting identically at every other site.  Applying
the induced site-algebra automorphism sends
\(q^{[h]}=\sum_i c_iX_i\) to \((q')^{[h]}=\sum_iX_i\).
Thus no extraction of roots or matching-power cancellation is hidden in
the rescaling.  This is consistent with (7) being sufficient for descent:
constructing it is already strong enough to produce the smaller source.

## 5. Scope and audit

This note does not modify the certified spine and does not prove
`SP-CLEAN-BRIDGE`.  It identifies two distinct possible closures: forcing
the unary system (3) excludes the scalar-unit branch by support minimality,
while forcing the active system (6)--(8) feeds the certified descent.  The
existing
scalar-unit moment-torsor and carrier-torsion guards remain compatible:
they already show that a source-faithful higher lift is extra data.  The
present theorem adds that the most rigid target-fixed unary lift is not
merely unproved; its existence is already a contradiction on the chosen
support-minimal source.  Thus an adjacent-chart derivation of (3) would be
a positive branch-closing result.

The dependency-free checker
[`verify_scalar_unit_target_fixed_unipotent_lift_no_go.py`](../computations/verify_scalar_unit_target_fixed_unipotent_lift_no_go.py)
audits the divided-power coefficient \(k+1\), the full triangular rank for
\(2\leq h\leq64\), the forced vanishing of \(Q_1\), the unary activity
failure, and guards showing that target fixation and the terminal
coefficient are both essential.  It uses explicit exceptions and runs
unchanged under optimized Python.
