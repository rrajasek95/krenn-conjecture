# The shifted denominator face has a derived filler; its first underived commutator is $h_v(H_0-u)e_{\rm Eq}$

## Outcome

The unique candidate from
[the first comparison gate](h3-non-euler-chart-h1-first-comparison-gate.md)
can be completed across target, ordinary residue, and both chart sectors in
the indexed Hasse/Koszul presentation.

Let $u=u_v$, $t=a_{pq}^{00}$, $H_m$ be the mixed source row, and
$F_0=H_0-u_{\rm hom}$. The complete two-direction Hasse companion is

\[
\begin{aligned}
s_{ut}={}&H_m r_0[ut]
 +(\partial_uH_m)r_0[t]+(\partial_tH_m)r_0[u]\\
 &+h_vr_0[\varnothing]-F_0r_m[ut].                    \tag{1}
\end{aligned}
\]

Its indexed source boundary is zero. With the shifted cap generator $T$,

\[
n_v=s_{ut}-h_vT                                             \tag{2}
\]

satisfies

\[
\boxed{(d,\operatorname{tgt},\operatorname{ores})(n_v)
       =(h_vYw,0,0).}                                      \tag{3}
\]

Thus the initial chain $dn_v=h_vY_0$ forced by `f872900` has a positive
filler in the derived presentation. It does **not** yet construct the source
cell $b_v$ with $db_v=k_v$ in the underived physical two-chart source.

The chart sign also works. The strict chart difference of (1) has external
face $+S_v$; subtracting the correcting filler therefore contributes exactly
$-S_v$, whose marked readout is $-1$. Target and ordinary residue vanish
before this subtraction.

The earliest obstruction is source descent, not augmentation. If the
diagonal coefficient $h_v(r_0-T)$ is isolated and evaluated with the original
underived differential, then

\[
d\bigl(h_v(r_0-T)\bigr)
 =h_vYw+h_v(H_0-u_{\rm hom})e_{\rm Eq}.                    \tag{4}
\]

The four companion terms in (1) cancel the second summand in the indexed
Hasse differential. At the $q$-zero top, $h_v$ contracts to $1$, so diagonal
projection leaves the primitive commutator

\[
(H_0-u_{\rm hom})e_{\rm Eq}.                              \tag{5}
\]

Consequently the remaining theorem is a comparison from the prolonged
derived Hasse/Koszul presentation to the underived physical source which
kills (5) while preserving (3) and the $-S_v$ chart face. The later
$\kappa Yw_v$ curvature-cap landing is a separate step.

## 1. Fine degree and shifted cap row

The initial face $h_vY_0$ has coefficient/output weight $9$. The strict
EqSystem degree has weight $12$, and their unique difference is

\[
\sigma=e_{x,0}+e_{p,0}+e_{q,0}.                           \tag{6}
\]

Equation (2) realizes this shift: $r_0$ and the shifted $h_vT$ term have the
same homological and fine degrees. Both have target $h_v$, so their difference
has target zero. Neither $r_0$, $r_m$, nor $T$ carries ordinary residue, hence
(2) has residue zero without a stipulated cancellation.

This sharpens the earlier degree statement. The shift is no longer the
obstruction inside the derived presentation; its physical realization in an
underived source comparison remains open.

## 2. Complete differential and first commutator

For square-zero Hasse parameters $\epsilon_u,\epsilon_t$, the indexed row
differential is

\[
dr_m[S]=\sum_{A\subseteq S}(\partial_AH_m)
 e_{\rm Eq}[S\setminus A],\qquad
dr_0[S]=F_0e_{\rm Eq}[S].                                \tag{7}
\]

Substitution of (1) into (7) cancels every Eq component coefficientwise.
The five source terms in (1) are forced by the Hasse product rule; omitting
any proper face leaves a Leibniz commutator.

The diagonal coefficient alone is

\[
h_v(r_0-T).                                                \tag{8}
\]

Its target and residue already vanish, but (4) shows it is not a chain. The
residual $h_vF_0e_{\rm Eq}$ is nonzero and has 273 distinct labelled monomials
in the universal direct-free ring. The lower Hasse companion terms cancel it
exactly. Thus (4) is the earliest nonzero residual, not a support artefact or
an omitted target row.

## 3. Chart placement and correction sign

Every external coefficient containing $u,t$ lies in the $pq$-direct sector.
The same matching cannot contain $pr$, and the direct-free presentation
empties the $pr$-direct sector, so its other copy lies in the $pr$-two-star
sector. This holds on all four internal Boolean faces.

Writing the translated copies as $\mathcal N^{pq}$ and $\mathcal N^{pr}$,
their common $T$ term cancels and

\[
\mathcal N^{pq}-\mathcal N^{pr}
=\tau(H_m)(r_0^{pq}-r_0^{pr})
-F_0(r_m^{pq}-r_m^{pr})                                  \tag{9}
\]

is closed, target-zero, and residue-zero coefficientwise. Its external
order-two face is

\[
(h_v)_{pq}-(h_v)_{pr}=S_v.                                \tag{10}
\]

The homotopy correcting the original connecting class is subtracted, so it
contributes $-S_v$. This derives the chart-odd decoration that older
denominator-face audits could only stipulate.

## 4. Internal faces and surviving physical gate

Retain two internal matching directions $e,f$. The complete four-way
translation is

\[
\mathcal N=\tau(H_m)(r_0-T)-\tau(F_0)r_m,
\qquad d\mathcal N=\tau(H_m)Yw.                          \tag{11}
\]

All fifteen denominator columns are present. Their selected-column counts on
the internal faces $\varnothing,\epsilon_e,\epsilon_f,
\epsilon_e\epsilon_f$ are

\[
5,3,3,1.                                                  \tag{12}
\]

Thus the proper-face leakage is real, but (11) cancels it exactly. The top
face is Kronecker-supported at $d_{v,m_v}$ and has

\[
r_0-T\longmapsto Yw,qquad
\operatorname{tgt}=\operatorname{ores}=0.                \tag{13}
\]

However, $[\epsilon_u\epsilon_t\epsilon_e\epsilon_f]\tau(H_m)=1$ although
$H_m=0$ on the underived source. Diagonal projection of (13) therefore has
commutator (5). The derived filler is complete; a physical comparison map is
still missing.

This constructs the initial layer (3), not the final active cap class
$(\kappa Yw_v,0,0)$. Curvature normalization may be applied only after the
source descent represented by (5) is solved.

## Verification

Run:

```text
python3 computations/verify_h3_shifted_denominator_chart_filler_augmented_commutator.py
python3 -O computations/verify_h3_shifted_denominator_chart_filler_augmented_commutator.py
python3 -I -S computations/verify_h3_shifted_denominator_chart_filler_augmented_commutator.py
```

The checker pins `f872900` and the complete Hasse/Koszul/cap totalization. It
reconstructs (1), checks its indexed differential, constructs (2)--(3), and
verifies the unique shift, all target and ordinary-residue rows, every chart
sector on all internal faces, the $-S_v$ correction sign, the 15-column
support census, and the exact residuals (4)--(5). The frozen digest is

```text
bdcc6a2734c3bd31f060d56fd88f8f5344f39e43aed03f70f18cfa65eef74b92
```
