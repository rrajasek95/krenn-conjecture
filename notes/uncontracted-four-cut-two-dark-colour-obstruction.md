# The uncontracted four-cut system forbids two dark colours

## 1. Result

Let the notation and hypotheses be those of
[the overlapping zero-star four-cut exchange](overlapping-zero-star-four-cut-exchange.md).
Thus `p,q,i,j` are distinct sites,

\[
 A_{pi}=A_{qi}=A_{pj}=A_{qj}=0,
\]

`D` is their common complement, and the complete 81-row system is

\[
\begin{aligned}
 &a_{ab}u_{cd}z^{[m-2]}
 +a_{ab}t_cv_dz^{[m-3]}
 +u_{cd}x_ay_bz^{[m-3]}\\
 &\hspace{31mm}+x_ay_bt_cv_dz^{[m-4]}
       =\delta_{a=b=c=d}X_a^D.                         \tag{1}
\end{aligned}
\]

All products of stars in this note are products in the site-square-zero
algebra on `D`.  In particular, a statement such as `t_c v_c=0` concerns
the full product after all complex cancellation; it does not assert that
either star vanishes.

**Theorem 1.1 (two-dark-colour obstruction).**  In every solution of
(1),

\[
 \#\{c:t_cv_c=0\}\le1,
 \qquad
 \#\{c:x_cy_c=0\}\le1.                                \tag{2}
\]

Equivalently, at least two of the three diagonal products are nonzero in
each of the two star pairs.  The conclusion is uniform in the size and
structure of `D`, including every common-power degeneration of `z`.

This immediately proves that the repeated-pair `K4` selected-cap model in
Section 5 of the four-cut note cannot extend to the full 81 rows: that
model has `t_1v_1=t_2v_2=0`.

## 2. The matrix projection of all 81 rows

It is useful first to retain every uncontracted `(a,b)` direction.  Put

\[
 Z_0=z^{[m-2]},\qquad Z_1=z^{[m-3]},\qquad
 Z_2=z^{[m-4]}.                                        \tag{3}
\]

For an arbitrary matrix functional `M=(M_ab)`, define

\[
 \lambda_M=\sum_{a,b}M_{ab}a_{ab},
 \qquad Q_M=\sum_{a,b}M_{ab}x_ay_b.                   \tag{4}
\]

Multiplying (1) by `M_ab` and summing over `a,b` gives the exact projected
row

\[
\boxed{
 \lambda_M(u_{cd}Z_0+t_cv_dZ_1)
 +Q_M(u_{cd}Z_1+t_cv_dZ_2)
 =\delta_{cd}M_{cc}X_c^D.}                            \tag{5}
\]

No rank or support inference enters (5).  In particular, taking a matrix
unit `M=E_ab` recovers the corresponding nine rows of (1), including the
direct term `a_ab u_cd Z_0` that the selected cap discarded.

## 3. Three rows rule out two dark colours at `i,j`

Suppose, for distinct colours `r,s`, that

\[
                         t_rv_r=t_sv_s=0.               \tag{6}
\]

For every `a,b` set

\[
                         R_{ab}=a_{ab}Z_0+x_ay_bZ_1.     \tag{7}
\]

The rows `(a,b;c,d)=(r,r;r,r)`, `(s,s;s,s)`, and
`(r,r;s,s)` of (1) are, respectively,

\[
 u_{rr}R_{rr}=X_r^D,
 \qquad u_{ss}R_{ss}=X_s^D,
 \qquad u_{ss}R_{rr}=0.                                \tag{8}
\]

The middle equality forces the complex scalar `u_ss` to be nonzero,
because `X_s^D` is a nonzero basis monomial.  The last equality therefore
forces `R_rr=0`, contradicting the first.  This proves the first bound in
(2).  Notice that (8) keeps `a_rr Z_0` inside `R_rr`; no individual source
or matching summand has been declared zero.

## 4. The symmetric three-row argument at `p,q`

Now suppose instead that

\[
                         x_ry_r=x_sy_s=0                \tag{9}
\]

for distinct `r,s`, and put

\[
                         S_{cd}=u_{cd}Z_0+t_cv_dZ_1.     \tag{10}
\]

The rows `(r,r;r,r)`, `(s,s;s,s)`, and `(s,s;r,r)` become

\[
 a_{rr}S_{rr}=X_r^D,
 \qquad a_{ss}S_{ss}=X_s^D,
 \qquad a_{ss}S_{rr}=0.                                \tag{11}
\]

Here the second equality gives `a_ss != 0`; the third then gives
`S_rr=0`, contrary to the first.  This proves the second bound in (2).

## 5. Scope and next gate

The theorem closes the explicit repeated-pair common-power escape left by
the five selected cap rows.  More generally, it turns the full 81-row
compatibility problem into a concrete support requirement: both exposed
zero-star pairs must have at least two live diagonal colour products.

It does **not** yet eliminate the whole E1 chart.  The remaining dense
four-cut case has two or three live diagonal products in each pair.  The
[isotropic dressed-cap theorem](uncontracted-four-cut-isotropic-dressed-cap.md)
uses the same 81 rows more globally: it contracts one direct block along a
bilinear zero and exports all nine opposite rows with their direct terms
and one common-power multiplier.  That is now the stronger dense-case
target.  Sparse deleted-star rows, distinguished span at least three, and
graph-degenerate rank-three charts remain separate E1 residuals.

## 6. Audit

The dependency-free checker
[`verify_uncontracted_four_cut_two_dark_colour_obstruction.py`](../computations/verify_uncontracted_four_cut_two_dark_colour_obstruction.py)
enumerates every matrix-unit projection of (1), checks the three decisive
target-index patterns for every ordered pair of distinct colours, and
confirms that the repeated-pair selected-cap boundary contains a forbidden
two-dark pair.  It does not search source parameters.
