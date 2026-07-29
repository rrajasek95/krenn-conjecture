# Independent audit of the uncontracted four-cut two-dark-colour obstruction

## Verdict

The two-dark-colour obstruction is correct.  It is a direct consequence of
three rows of the complete 81-row four-cut identity, and it is insensitive to
complex cancellation inside the tensors on the common complement.  The only
cancellation performed in the proof is division by a scalar already forced to
be nonzero by a pure target row.

The conclusion is conditional on having two literal zero-star sites for the
same deleted pair and on vanishing of the full star product in the
site-square-zero algebra.  Vanishing merely after multiplication by one common
power is not the stated hypothesis.

## Clean-room setup

Let `B` have size `2m>=8`, let `p,q,i,j` be distinct, and assume

\[
 A_{pi}=A_{qi}=A_{pj}=A_{qj}=0.
\]

Put `D=B\setminus\{p,q,i,j\}`.  Write `z` for the internal quadratic on
`D`, and abbreviate

\[
 Z_0=z^{[m-2]},\qquad Z_1=z^{[m-3]},\qquad Z_2=z^{[m-4]}.
\]

The accompanying star factors in (1) make each of its four summands top
degree on `D`; at the smallest order, `m=4`, the last divided power is
`Z_2=1`.  Let

\[
 a_{ab}=(A_{pq})_{ab},\qquad u_{cd}=(A_{ij})_{cd},
\]

and let `x_a,y_b,t_c,v_d` be the stars from `p,q,i,j`, respectively, into
`D`.  Resolving the four named sites gives exactly four possible matching
layers: both direct edges, only `pq`, only `ij`, or four crossings into `D`.
Consequently the row with exposed colours `(a,b;c,d)` is

\[
\begin{aligned}
 a_{ab}u_{cd}Z_0+a_{ab}t_cv_dZ_1
 +u_{cd}x_ay_bZ_1+x_ay_bt_cv_dZ_2
   =\delta_{a=b=c=d}X_a^D.                    \tag{1}
\end{aligned}
\]

The two other direct pairings of the four named sites vanish by the four
literal zero blocks.  Divided powers enumerate the residual matchings without
extra binomial factors.  Each `X_c^D` is a nonzero basis monomial of the
site-square-zero algebra.

Here a colour `c` is *dark for the `i,j` star pair* when the complete product
`t_cv_c` is zero in that algebra.  This need not mean that either factor is
zero individually.  Define darkness for the `p,q` star pair analogously using
`x_cy_c`.

## The `t,v` obstruction

Suppose two distinct colours `r,s` are dark for the `i,j` star pair:

\[
                         t_rv_r=t_sv_s=0.              \tag{2}
\]

Set

\[
                         R_h=a_{hh}Z_0+x_hy_hZ_1.
\]

In (1), the rows `(r,r;r,r)`, `(s,s;s,s)`, and `(r,r;s,s)` become,
respectively,

\[
 u_{rr}R_r=X_r^D,\qquad
 u_{ss}R_s=X_s^D,\qquad
 u_{ss}R_r=0.                                          \tag{3}
\]

The middle equality and `X_s^D\ne0` force the scalar `u_{ss}\ne0`.  Cancelling
that scalar in the last equality gives `R_r=0`, contradicting the first
equality.  No tensor factor, common power, star form, or aggregate block was
cancelled.  Hence at most one of

\[
                         t_0v_0,\ t_1v_1,\ t_2v_2
\]

can vanish.  The diagonal row also records the useful pointwise implication

\[
                         t_cv_c=0\quad\Longrightarrow\quad u_{cc}\ne0.
                                                               \tag{4}
\]

## The symmetric `x,y` obstruction

Now suppose instead that `x_ry_r=x_sy_s=0` for distinct `r,s`, and put

\[
                         T_h=u_{hh}Z_0+t_hv_hZ_1.
\]

The rows `(r,r;r,r)`, `(s,s;s,s)`, and `(s,s;r,r)` of (1) give

\[
 a_{rr}T_r=X_r^D,\qquad
 a_{ss}T_s=X_s^D,\qquad
 a_{ss}T_r=0.                                          \tag{5}
\]

The second equality forces the scalar `a_{ss}\ne0`; the third then forces
`T_r=0`, contradicting the first.  Thus at most one of

\[
                         x_0y_0,\ x_1y_1,\ x_2y_2
\]

can vanish, and likewise

\[
                         x_cy_c=0\quad\Longrightarrow\quad a_{cc}\ne0.
                                                               \tag{6}
\]

This is genuinely the symmetric argument: its mixed target-zero row is
`(s,s;r,r)`, rather than `(r,r;s,s)`, so that the nonzero scalar forced by
the `s` diagonal row multiplies `T_r`.

## Exact scope at the proof frontier

Every solution of the full 81-row system therefore has at least two nonzero
diagonal products among the `t_c v_c`, and independently at least two among
the `x_c y_c`.  In particular, the repeated-pair `K_4` cap model in the
four-cut exchange note, which fixes
`t_1=t_2=v_1=v_2=0`, cannot be extended to all 81 rows while retaining those
stars.  The mixed target-zero row is precisely the uncontracted information
that its five selector-contracted cap equations omitted.

This does not yet close the overlapping E1 branch.  It leaves all cases with
zero or one dark colour, says nothing comparable about off-diagonal products
`t_cv_d` or `x_ay_b`, and does not turn the nonzero products into a localized
pair or a lower-order ternary source.  It also assumes, rather than proves,
the existence of two literal zero-star sites for one pair.  Consequently it
does not address the sparse-row, distinguished-span-at-least-three, or
graph-degenerate E1 strata, nor does it exclude a repeated-pair filter whose
uncontracted stars have the required two-colour activity.
