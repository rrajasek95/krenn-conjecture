# A fixed-zero bright fibre evades the private-row normalization

## Verdict

The whole-kernel site-flag theorem does not by itself put branch (iii) into
one of the four zero-free private-row mate charts.  The first exact evasion
is the rational seven-cell common quadratic already underlying the
common-radical provenance audit.

It has

\[
 \operatorname{rank}\Phi=11,\qquad
 \dim\ker\Phi=4,\qquad
 X_a,X_c\in\operatorname{im}\Phi,\qquad
 X_t\notin\operatorname{im}\Phi,                       \tag{1}
\]

and

\[
                  \dim\pi_t(\ker\Phi)=2               \tag{2}
\]

on the minimal target pair ({0,3}).  Nevertheless every preimage of
both bright tensors vanishes at site (2).  No change of representatives
by a kernel row enters the zero-free flag branches.

The exact replay is
`computations/verify_shared_reciprocal_two_bad_bright_fixed_zero_counterguard.py`.

## Literal source and affine fibres

The nonzero endpoint-colour cells are

```text
12:aa=3/5, 02:aa=4/5, 34:aa=1,
01:cc=1,   23:cc=1,
02:ca=1,   02:ta=1.
```

Bright preimages are

\[
 A_0={5\over3}e_a@0,\qquad C_0=e_c@4.                \tag{3}
\]

A complete kernel basis is

\[
\begin{aligned}
 &-{4\over3}e_a@0-{5\over3}e_c@0-{5\over3}e_t@0+e_a@1,\\
 &e_a@3,\qquad e_c@3,\qquad e_t@3.
\end{aligned}                                         \tag{4}
\]

Every vector in (4) evaluates to zero at sites (2) and (4).  Therefore

\[
 \operatorname{ev}_2\bigl(\Phi^{-1}(X_a)\bigr)=0,
 \qquad
 \operatorname{ev}_2\bigl(\Phi^{-1}(X_c)\bigr)=0.     \tag{5}
\]

In fact the (X_a) fibre also vanishes identically at site (4).  Equation
(5) is an affine-fibre statement, stronger than exhibiting one sparse
bright representative.  It proves that the zero branch of the site-flag
trichotomy is genuine and cannot be removed by generic choice in the
preimage coset.

## Why this does not survive the full common-hafnian rows

The counterguard contains no pair of disjoint (tt) cells.  Hence every
pure-target four-site cofactor vanishes:

\[
                         K_z(t,t,t,t)=0\quad(0\le z<5). \tag{6}
\]

For every controller row (P), its all-target response is therefore

\[
                  R=\sum_zP_{z,t}K_z(t,t,t,t)=0.       \tag{7}
\]

But the full ((t,t)) common-hafnian row in the normalized common-radical
branch gives the exact source-ideal equation

\[
                              D_{tt}R=1.                \tag{8}
\]

Thus this literal (q) cannot extend to a point of the full branch-(iii)
ideal.  Its role is narrower and load-bearing: bright images, the odd-star
kernel equations, the target-pair theorem, and the whole-kernel site flags
still do **not** derive the four canonical private-row charts.  The pure
target chord (or another full-row consequence) must first eliminate the
fixed-zero affine-fibre branch.

## Consequence for the chart-cover strategy

The proposed matching filtration remains viable only after a full-row
preprocessing split:

1. eliminate fixed-zero bright fibres using (D_{tt}R=1) together with
   the other diagonal/off-diagonal rows;
2. enter the zero-free whole-kernel line-flag branches;
3. normalize leading cofactor matchings there and derive the four private
   mate charts;
4. resolve later critical pairs by a rank-14 pivot or Laurent holonomy.

The canonical first critical pair already has the latter form:

\[
 W=\pm2r/x-s+t,\qquad Z=-s+t,
\]

so (W=Z=0) forces the localized switch weight (r=0).  The counterguard
above occurs strictly before that odd-holonomy stage; it is not a failure
of the holonomy invariant.
