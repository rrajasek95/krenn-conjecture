# Two-hole reduction of the five-site witness-union stratum

## 1. Outcome

Fix an invertible block `A_pq` in a hypothetical eight-site realization and
write

\[
 C_{u,r}=A_{pu}K_rA_{qu}^T,\qquad
 W_u=\{r:C_{u,r}=0\}.
\]

Assume that exactly five of the six outside sites have nonempty `W_u`.
There are 61 incidence orbits modulo permutations of sites and colors.
The hard-capacity rule leaves 49.  The two-hole correction gives a sharper
reduction than the exact-double minor used for the four-site boundary:

\[
\begin{array}{c|r}
\text{stage}&\text{orbits remaining}\\ \hline
\text{five-site incidence}&61\\
\text{hard capacity}&49\\
\text{two nontriple holes, one active color}&16\\
\text{binary target with a free annihilator plane}&13.
\end{array}
\]

The earlier exact-double version of the rank argument closes 18 of the 49
orbits.  Allowing arbitrary nontriple holes closes 33, fifteen more.  A
two-active-color monomial comparison closes three additional orbits after
hard assignments are taken into account.  The exact residual boundary is
13 incidence orbits and 36 labeled hard assignments.

This is a strict reduction, not yet an exclusion of witness-union size
five.  A full five-hole anchor audit leaves compatible charts on every
residual row, so a continuation must retain more than anchor incidence.
The later full-row square argument in
[`n8-011166-full-row-square-obstruction.md`](n8-011166-full-row-square-obstruction.md)
does retain that information and excludes the first row
`(0,1,1,1,6,6)`; the other 35 hard assignments in twelve rows remain.

## 2. The nontriple rank-two criterion

Work over

\[
 K=\operatorname{Frac}
 \bigl(\mathbb C[\alpha,\beta]/(\alpha^TA_{pq}\beta)\bigr)
\]

and put

\[
 x_u=A_{pu}^T\alpha,\qquad y_u=A_{qu}^T\beta,\qquad
 N_u=(\operatorname{span}_K\{x_u,y_u\})^\perp.
\]

Recall that `u` is hard for color `r` when
`N_u subset e_r^perp`.  Every color has at least two hard sites.  At a
nontriple site the hard colors are exactly `W_u`; at a triple-zero site
there is at most one hard color.

Leave two sites `u,v` open and contract the other four by arbitrary vectors
in their common annihilator spaces.  On the incidence quadric, the exact
two-hole identity is

\[
 \operatorname{diag}(t_0,t_1,t_2)=hR_{uv},\qquad
 R_{uv}=x_uy_v^T+y_ux_v^T.                              \tag{1}
\]

Here a target coefficient `t_r` is identically zero exactly when at least
one contracted site is hard for `r`; otherwise it is nonzero for generic
independent annihilator choices.

**Lemma 2.1 (nontriple rank-two obstruction).**  Suppose the only active
target color in (1) is `r`, and both holes are nontriple sites.  Then (1) is
impossible.

**Proof.**  Since `W_u` and `W_v` are proper subsets of the three colors,
their cross products `x_u cross y_u` and `x_v cross y_v` are nonzero over
`K`.  Thus both matrices

\[
 U=[x_u\ y_u],\qquad V=[x_v\ y_v]
\]

have column rank two.  But

\[
 R_{uv}=U\begin{pmatrix}0&1\\1&0\end{pmatrix}V^T,       \tag{2}
\]

so `R_uv` has rank exactly two.  For a generic annihilator choice, (1)
has nonzero left side `t_rE_rr`; it forces `h` nonzero and would equate a
rank-one matrix with a rank-two matrix. `QED`

Equivalently, the obstruction applies whenever the hard `r`-set consists
of two nontriple sites and every other color has a hard site outside that
pair.  The holes need not be exact double witnesses; exact singleton holes
work equally well.  This is the source of the fifteen new orbitwise
exclusions.

For reference, every selected minor of (2) factors as

\[
 \det R_{uv}[\{i,j\},\{k,l\}]
 =\det\!\begin{pmatrix}x_{u,i}&y_{u,i}\\x_{u,j}&y_{u,j}\end{pmatrix}
  \det\!\begin{pmatrix}y_{v,k}&x_{v,k}\\y_{v,l}&x_{v,l}\end{pmatrix}.
                                                                    \tag{3}
\]

## 3. The binary free-plane obstruction

There is one further two-hole use.  Suppose `u,v` are exact double sites
with the same witness colors `{r,s}`.  Their star spans are both the
coordinate plane `span(e_r,e_s)`, so the corresponding `2 by 2` block of
`R_uv` is invertible by (3).

Assume the active target colors in (1) are exactly `r,s`, and that a
contracted triple-zero site `w` is hard for the third color `t`.  Then

\[
                         N_w=e_t^\perp.
\]

Fix the other annihilators generically and let
`z_w=z_re_r+z_se_s` vary freely.  The active part of (1) has the form

\[
 \operatorname{diag}(c_rz_r,c_sz_s)=h(z_r,z_s)
       R_{uv}|_{\langle e_r,e_s\rangle},                 \tag{4}
\]

where `c_r,c_s` are nonzero.  For generic `(z_r,z_s)`, both sides have
rank two.  The off-diagonal entries make the fixed correction block
diagonal, with two nonzero diagonal entries `R_rr,R_ss`.  Eliminating `h`
from the diagonal equations gives

\[
                 c_rR_{ss}z_r=c_sR_{rr}z_s,             \tag{5}
\]

an impossible identity in two independent coordinates.

This criterion closes all hard assignments left by Lemma 2.1 in exactly
three incidence orbits:

\[
 (0,1,1,6,6,7),\qquad
 (0,1,6,6,7,7),\qquad
 (0,3,3,7,7,7).                                        \tag{6}
\]

The mask convention is

\[
\begin{array}{c|rrrrrrrr}
\text{mask}&0&1&2&3&4&5&6&7\\ \hline
W&\varnothing&0&1&01&2&02&12&012.
\end{array}                                             \tag{7}
\]

## 4. Structure when one hole is triple

The only way a one-active-color pair can escape Lemma 2.1 is for at least
one hole to be triple-zero.  This failure has a useful exact normal form.
Suppose `u` is triple and hard for `r`, while `v` is nontriple and hard for
`r`.  Write

\[
 A_{pu}=a e_r^T,\qquad A_{qu}=b e_r^T,                  \tag{6a}
\]

where `a,b` are not both zero.  For a column index `s!=r`, write
`p_s=A_{pv}e_s` and `q_s=A_{qv}e_s`.  The `(r,s)` entry of the correction
in (1) is the class of

\[
 \alpha^T(aq_s^T+p_sb^T)\beta.                          \tag{6b}
\]

It must vanish.  Its coefficient matrix has rank at most two, so it cannot
be a nonzero scalar multiple of the invertible matrix `A_pq`.  Here is the
quotient-domain step explicitly.  The off-diagonal equation is

\[
             0=h\,[\alpha^T(aq_s^T+p_sb^T)\beta]
\]

in the domain generated by the arbitrary annihilator coordinates over
`K`.  The active diagonal entry makes `h` nonzero, so the bracket vanishes
in `K`.  A bidegree `(1,1)` form in the principal ideal
`(alpha^T A_pq beta)` is a scalar multiple of its generator.  Since the
displayed coefficient matrix has rank at most two while `A_pq` has rank
three, that scalar is zero.  Hence the form vanishes before quotienting:

\[
                         aq_s^T+p_sb^T=0\qquad(s\ne r). \tag{6c}
\]

If `a,b` are both nonzero, rank-one factor uniqueness gives scalars
`lambda_s` with

\[
             p_s=\lambda_sa,\qquad q_s=-\lambda_sb.     \tag{6d}
\]

If `a=0`, then all `p_s=0` for `s!=r`; nontriplality of `v` makes its
remaining column nonzero, so `A_pv` is a directed `r`-anchor.  Symmetrically,
if `b=0`, then `A_qv` is a directed `r`-anchor.

The two-sided locks also remember which columns are nonzero.  After
permuting colors take `r=0`, and abbreviate

\[
 A=\alpha^Ta,\quad B=\beta^Tb,\quad
 C=x_{v,0},\quad D=y_{v,0}.
\]

Writing the two scalars in (6d) as `lambda_1,lambda_2` gives

\[
 x_v=(C,\lambda_1A,\lambda_2A),\qquad
 y_v=(D,-\lambda_1B,-\lambda_2B),
\]

and hence

\[
 x_v\mathbin\times y_v
 =(0,\lambda_2F,-\lambda_1F),\qquad
 F=AD+BC=(R_{uv})_{00}\ne0.                              \tag{6e}
\]

Thus an exact singleton `W_v={r}` locks both off-`r` columns to the triple
endpoint lines, and an exact double `W_v={r,s}` locks precisely its
nonzero off-`r` column `s`; the missing-color column is zero.

Thus every residual active-one identity is either one-sided-anchor forcing
or a paired-column alignment.  This statement has not yet been coupled
across enough hole choices to eliminate an additional incidence row, but
it removes the unconstrained rank-one-correction ambiguity.

## 5. Exact residual boundary

The following table lists the thirteen residual incidence representatives.
For each row, `all` is the number of hard-capacity assignments before the
two-hole tests and `left` is the number not covered by Sections 2--3.  A
triple-label such as `(1,2)` records the hard colors assigned, in site
order, to the entries `7`.  Nontriple hard masks are fixed by (7).

\[
\begin{array}{c|c|r|r}
\text{masks}&\text{residual triple labels}&\text{all}&\text{left}\\ \hline
(0,1,1,1,6,6)&-&1&1\\
(0,1,3,3,6,7)&(2)&1&1\\
(0,1,3,5,6,6)&-&1&1\\
(0,1,3,5,7,7)&(1,2),(2,1)&2&2\\
(0,1,6,6,6,7)&(0)&1&1\\
(0,1,6,7,7,7)&\operatorname{Perm}(0,1,2)&6&6\\
(0,3,3,3,5,7)&(2)&1&1\\
(0,3,3,3,7,7)&(2,2)&1&1\\
(0,3,3,5,5,6)&-&1&1\\
(0,3,3,5,6,7)&(2)&4&1\\
(0,3,3,5,7,7)&(1,2),(2,1)&7&2\\
(0,3,5,7,7,7)&\operatorname{Perm}(0,1,2)&18&6\\
(0,3,7,7,7,7)&\operatorname{Perm}(0,1,2,2)&12&12
\end{array}                                             \tag{8}
\]

In particular, every nonempty site is hard for some color in every one of
the 36 residual assignments.  This explains why no three-hole contraction
can retain the full ternary diagonal: contracting any witness site kills a
target color.

## 6. Full five-hole anchor audit

Contract only the unique nonwitness site.  All three target coefficients
remain nonzero, so this is a legitimate use of the one-slice covering
lemma.  It forces a directed anchor of every color from each endpoint among
the five open sites.

The checker enumerates all anchor labels subject to the exact local rules:

* an anchor color at `u` belongs to `W_u`;
* two distinct endpoint labels at one site force that exact double mask;
* two equal endpoint labels force a triple-zero mask;
* at a triple site hard for `c`, each nonzero star block is a `c`-anchor
  and at least one of the two blocks is nonzero.

Before using the row locks, every row of (8) has compatible full endpoint
coverage.  The numbers of incidence-shadow charts are, in table order,

\[
 24,212,334,132,240,85,708,336,1070,582,362,235,119.    \tag{9}
\]

Even imposing the additional exploratory requirement that each color's
chosen `p`- and `q`-anchors occur at distinct sites leaves respectively

\[
 24,148,334,64,192,32,504,336,1070,518,224,104,56       \tag{10}
\]

charts.  The distinct-site filter is stronger than what is needed here;
(10) is recorded only to show that endpoint collision bookkeeping alone
does not shrink the thirteen-row boundary.

The row-lock lemma makes this finite shadow substantially smaller.  At a
triple site hard for `c`, record one of three types:

* `P`: the `p`-star is nonzero and the `q`-star is zero;
* `Q`: the `q`-star is nonzero and the `p`-star is zero;
* `B`: both stars are nonzero.

For an active pair consisting of this triple and a nontriple site, type
`P` forces a `q`-side `c`-anchor at the nontriple site, type `Q` forces the
`p`-side analogue, and type `B` installs the nonzero column-line locks from
(6d)--(6e) at both endpoints.  The checker enumerates these types, forced
anchors, line sources, optional compatible anchors, and full endpoint
coverage.  It leaves the following exact chart counts:

\[
\begin{array}{c|r|r}
\text{masks}&\text{row-lock charts}&\text{distinct-site subcharts}\\ \hline
(0,1,1,1,6,6)&24&24\\
(0,1,3,3,6,7)&138&74\\
(0,1,3,5,6,6)&334&334\\
(0,1,3,5,7,7)&56&16\\
(0,1,6,6,6,7)&144&96\\
(0,1,6,7,7,7)&21&4\\
(0,3,3,3,5,7)&456&252\\
(0,3,3,3,7,7)&336&336\\
(0,3,3,5,5,6)&1070&1070\\
(0,3,3,5,6,7)&582&518\\
(0,3,3,5,7,7)&236&112\\
(0,3,5,7,7,7)&97&26\\
(0,3,7,7,7,7)&49&14
\end{array}                                             \tag{11}
\]

Counts in rows with several residual hard assignments are the same for
each assignment, after the corresponding site/color relabeling.  Every row
still survives, but the most triple-heavy cases have fallen from `85,235,
119` basic charts to `21,97,49` row-lock charts.  These explicit line-lock
signatures are the input for a higher-hole symmetric-slice test; unlike
bare anchor labels, they retain which triple endpoint vector controls each
nonzero column.

No partial-diagonal slice-cover inference is used: after contracting any
hard witness, one or more colors disappear and the one-slice lemma is no
longer available.

## 7. Exact audit

Run

```text
.venv/bin/python computations/verify_n8_witness_union_five_stages.py
```

The checker enumerates all 61 orbits, all 147 labeled hard-capacity
assignments on the 49 surviving representatives, the `18 -> 33 -> 36`
orbitwise obstruction stages, the thirteen rows and 36 assignments in
(8), the minor factorizations (3), the monomial comparison (5), the
ordinary row-lock identities (6c)--(6e), and the basic and row-locked
anchor-chart counts (9)--(11).
