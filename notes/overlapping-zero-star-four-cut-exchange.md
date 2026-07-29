# Overlapping zero-star triples: the exact four-cut exchange

## 1. Result

Let an exact ternary aggregate source live on an even set `B`, with
`|B|=2m>=8`, and choose four distinct sites `p,q,i,j`.  Suppose that `i`
and `j` are both literal zero-star sites for the same deleted pair `p,q`:

\[
 A_{pi}=A_{qi}=A_{pj}=A_{qj}=0.                         \tag{1}
\]

Put `D=B\setminus{p,q,i,j}` and write `z` for the quadratic internal to
`D`.  After contracting the displayed endpoint colours, write

\[
 a_{ab}=(A_{pq})_{ab},\qquad u_{cd}=(A_{ij})_{cd},       \tag{2}
\]

and let `x_a,y_b,t_c,v_d` be respectively the stars from `p,q,i,j` into
`D`.  All products below are in the site-square-zero algebra on `D`, and
`z^[r]=z^r/r!` is the unordered matching power.

**Theorem 1.1 (four-cut identity).**  The complete coefficient system on
the four exposed sites is

\[
\boxed{
\begin{aligned}
 &a_{ab}u_{cd}z^{[m-2]}
 +a_{ab}t_cv_dz^{[m-3]}
 +u_{cd}x_ay_bz^{[m-3]}\\
 &\hspace{31mm}+x_ay_bt_cv_dz^{[m-4]}
       =\delta_{a=b=c=d}X_a^D,
       \qquad 0\le a,b,c,d\le2 .                       \tag{3}
\end{aligned}}
\]

Thus the two common-complement 27-equation packets, one for
`{p,q,i}` and one for `{p,q,j}`, are not independent systems.  If their
target residuals are denoted by `E^i_(abc)` and `E^j_(abd)`, then

\[
 \boxed{\quad
 \iota_{j,d}E^i_{abc}=\iota_{i,c}E^j_{abd}
 \quad}                                                   \tag{4}
\]

for every `a,b,c,d`.  Both sides are (3) minus its target.  This is an
exchange regrading, valid coefficientwise over the integers before any
specialization of the aggregate blocks.

There is nevertheless new information in the *second literal zero-star*,
because the same isotropic pair for `A_pq` can be used in both triples.
Choose nonzero `xi,eta` with identical support `H`, `|H|<=2`, and

\[
                       \xi^{\mathsf T}A_{pq}\eta=0.       \tag{5}
\]

Put

\[
 P=\sum_a\xi_ax_a,\qquad S=\sum_b\eta_by_b,
 \qquad \kappa_h=(\xi_h\eta_h)^{-1}\quad(h\in H).       \tag{6}
\]

**Corollary 1.2 (shared row-and-column cap).**  For every `h in H`,

\[
 \boxed{
 \kappa_hPS\bigl(u_{hd}z^{[m-3]}+t_hv_dz^{[m-4]}\bigr)
       =\delta_{hd}X_h^D\quad(0\le d\le2),}             \tag{7}
\]

and

\[
 \boxed{
 \kappa_hPS\bigl(u_{ch}z^{[m-3]}+t_cv_hz^{[m-4]}\bigr)
       =\delta_{ch}X_h^D\quad(0\le c\le2).}             \tag{8}
\]

The direct `A_ij` entry, the common matching power, endpoint order, and
all complex cancellation remain in (7)--(8).  Only the `A_pq` terms have
disappeared, and they disappear by the explicit bilinear equation (5), not
by a support inference.

Equations (7)--(8) are a genuine lower-order cap packet, but they do not
by themselves produce an ordinary ternary source on `D`.  Section 5 gives
the smallest repeated-pair common-power model demonstrating this boundary.

## 2. Expansion of the first 27-equation packet

For the triple `C_i={p,q,i}`, its odd complement is `{j} disjoint-union D`.
The internal quadratic and the `i`-star on that complement are

\[
 z_i=z+\sum_de_d^{(j)}v_d,
 \qquad \tau_c=\sum_du_{cd}e_d^{(j)}+t_c.               \tag{9}
\]

Because of (1), equation (39) of the distinguished-span-two theorem has
only its direct `pq` and three-star terms:

\[
 a_{ab}\tau_cz_i^{[m-2]}
       +x_ay_b\tau_cz_i^{[m-3]}
       =\delta_{a=b=c}X_a^{\{j\}\cup D}.               \tag{10}
\]

Coefficient extraction at colour `d` of site `j` gives, for every `r`,

\[
 \iota_{j,d}(\tau_cz_i^{[r]})
       =u_{cd}z^{[r]}+t_cv_dz^{[r-1]}.                  \tag{11}
\]

This is a literal matching split: either `tau_c` occupies `j`, or `j` is
matched through `v_d` and `tau_c` occupies a distinct site of `D`.  There
is no binomial coefficient in divided-power notation.  Applying (11) to
the two terms of (10) gives exactly the left side of (3).  The coefficient
of the target is `delta_(a=b=c=d) X_a^D`, proving (3).

This derivation retains the direct product `a_ab u_cd`.  It also shows why
replacing the four terms by an ordinary product of two polarized
quadratics is generally incorrect: the four matching layers carry
different divided powers of `z`.

## 3. Expansion of the second packet and exchange

For `C_j={p,q,j}`, the odd complement is `{i} disjoint-union D`.  Now

\[
 z_j=z+\sum_ce_c^{(i)}t_c,
 \qquad \upsilon_d=\sum_cu_{cd}e_c^{(i)}+v_d.           \tag{12}
\]

The second packet is

\[
 a_{ab}\upsilon_dz_j^{[m-2]}
       +x_ay_b\upsilon_dz_j^{[m-3]}
       =\delta_{a=b=d}X_a^{\{i\}\cup D}.               \tag{13}
\]

Taking the coefficient at colour `c` of `i` again gives (3).  Equivalently,
if `H=A^[m]` is the complete top matching tensor, then contractions at
distinct sites commute:

\[
 \iota_{j,d}\iota_{i,c}\iota_{q,b}\iota_{p,a}H
 =\iota_{i,c}\iota_{j,d}\iota_{q,b}\iota_{p,a}H.       \tag{14}
\]

The diagonal target obeys the same equality.  Subtracting it proves (4).
As `(a,b,c,d)` and a word on `D` vary, either packet lists all `3^(2m)`
coefficients of the same top residual.  Consequently a proof must not add
the ranks or equation counts of the two packets.  Their value is as two
source-variable presentations of (3), together with the additional
literal zeros in (1).

## 4. Isotropic contraction gives both a row and a column

Multiply (3) by `kappa_h xi_a eta_b` and sum over `a,b`, first with
`c=h` fixed.  The two terms containing `a_ab` vanish by (5).  The other
two become

\[
 \kappa_hPS\bigl(u_{hd}z^{[m-3]}+t_hv_dz^{[m-4]}\bigr).
\]

On the right, only `a=b=c=d=h` can survive, and (6) normalizes its
coefficient to one.  This proves (7).  Repeating the calculation with
`d=h` fixed proves (8).

For one selector colour, (7)--(8) comprise five tensor rows: three entries
in row `h`, three in column `h`, with the diagonal counted once.  They are
only five linear combinations of the 81 rows in (3).  In particular they
discard the eight-dimensional complement of `xi tensor eta` in the
`(a,b)` response indices.  That discarded complement is not cosmetic; the
next section shows it is exactly where a false localization can hide.

## 5. Exact contracted countermodel: the repeated-pair `K4`

This model satisfies the complete selected row-and-column cap
(7)--(8), including one common quadratic and its literal powers.  It is
not a solution of (3), and hence is not a Krenn counterexample.  The
[uncontracted two-dark-colour theorem](uncontracted-four-cut-two-dark-colour-obstruction.md)
now proves directly that no extension to (3) exists.

Take `m=5` and let `D={0,1,2,3,4,5}`.  On the first four sites put the
three one-factors of `K4`, in their three coordinate colours:

\[
\begin{aligned}
 z={}&e_0^{(0)}e_0^{(1)}+e_0^{(2)}e_0^{(3)}\\
    &+e_1^{(0)}e_1^{(2)}+e_1^{(1)}e_1^{(3)}\\
    &+e_2^{(0)}e_2^{(3)}+e_2^{(1)}e_2^{(2)}.            \tag{15}
\end{aligned}
\]

Then, exactly,

\[
 z^{[2]}=E_0(45)+E_1(45)+E_2(45),\qquad z^{[3]}=0,      \tag{16}
\]

where `E_c(45)=tensor_(r=0)^3 e_c^(r)`.  Thus all three pure lifts have
the same missing pair `45`, the sharp repeated-pair power boundary.

Use the singleton selector `H={0}`, `kappa_0=1`, and set

\[
 P=e_0^{(4)},\quad S=e_0^{(5)},\quad
 t_0=e_0^{(0)},\quad v_0=e_0^{(1)},                     \tag{17}
\]

with

\[
 t_1=t_2=v_1=v_2=0,qquad
 u_{0d}=u_{c0}=0\quad(0\le c,d\le2).                   \tag{18}
\]

The edge `01` meets every cell of (15) except its colour-zero mate `23`.
Therefore

\[
 t_0v_0z=E_0(45),\qquad
 PS\,t_0v_0z=X_0^D.                                    \tag{19}
\]

Equations (17)--(19) give (7)--(8) for `h=0`: the diagonal is (19), and
every other selected row or column is zero.  Yet `z^[2]` still contains
all three repeated-pair lifts in (16).  Hence the selector-contracted
system alone neither localizes the multiplier to one physical pair nor
produces a lower ternary matching source.

The model deliberately leaves the uncontracted `x_a,y_b` rows unspecified.
It cannot be promoted to a countermodel of (3) merely by naming them.  In
fact, its two dark colours satisfy `t_1v_1=t_2v_2=0`, and three of the full
81 rows already contradict such a pair by the theorem linked above.

## 6. Resolved gate and remaining dense case

The direct-sensitive complement requested by the first version of this
note is supplied by the
[uncontracted two-dark-colour theorem](uncontracted-four-cut-two-dark-colour-obstruction.md).
It retains the direct `A_pq` term and uses two diagonal rows plus one mixed
target-zero row to prove

\[
 \#\{c:t_cv_c=0\}\le1,
 \qquad \#\{c:x_cy_c=0\}\le1.                          \tag{20}
\]

This excludes the repeated-pair filtering in Section 5 uniformly, without
any hypothesis on the common powers.  It does not yet close the entire E1
chart: the remaining dense four-cut case has at least two live diagonal
products in each star pair.  A second full 27-packet still adds nothing by
(4); the next step must couple those surviving diagonal products to the
zero-star construction or export a genuine lower-order cap.

## 7. Audit

The dependency-free checker
[`verify_overlapping_zero_star_four_cut_exchange.py`](../computations/verify_overlapping_zero_star_four_cut_exchange.py)

* enumerates the four matching layers in (3) at the first relevant order
  and checks that they partition every matching compatible with (1);
* checks the target-index exchange in (4); and
* expands (15)--(19) exactly over the integers, including `z^[2]`,
  `z^[3]`, the selected diagonal cap, and all off-diagonal selected rows
  and columns.
