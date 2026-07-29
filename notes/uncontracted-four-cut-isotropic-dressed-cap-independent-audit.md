# Independent audit of the isotropic dressed-cap export

## Verdict

The dressed-cap and double-isotropic formulas in
[`uncontracted-four-cut-isotropic-dressed-cap.md`](uncontracted-four-cut-isotropic-dressed-cap.md)
are correct, including the smallest case `m=4`.  The colour-retention
classification is sharp.  The two consistency guards are also correct,
but neither is a solution of the full dressed packet: the binary guard
checks only the final four-star identity, and the twelve-site ternary guard
uses one specially chosen unstructured multiplier which is not proved to be
a divided power of a quadratic.

No theorem currently registered in this repository excludes the general
dressed packet.  Several existing theorems exclude narrower factorizable,
pure-lift, coherent-field, or repeated-star strata, but none has all the
hypotheses needed to consume the export below.

## 1. Clean-room contraction

Use the complete four-cut identity

\[
\begin{aligned}
 &a_{ab}u_{cd}Z_0+a_{ab}t_cv_dZ_1
   +u_{cd}x_ay_bZ_1+x_ay_bt_cv_dZ_2\\
 &\hspace{38mm}=\delta_{a=b=c=d}X_a^D,
\end{aligned}                                             \tag{A1}
\]

where

\[
 Z_0=z^{[m-2]},\qquad Z_1=z^{[m-3]},\qquad
 Z_2=z^{[m-4]}.
\]

Choose covectors `alpha,beta` and abbreviate

\[
 \mu=\sum_{c,d}\alpha_cu_{cd}\beta_d,
 \qquad T=\sum_c\alpha_ct_c,
 \qquad V=\sum_d\beta_dv_d.
\]

Multiplying (A1) by `alpha_c beta_d` and summing in `c,d` gives, for
each still-uncontracted pair `(a,b)`,

\[
 a_{ab}\mu Z_0+a_{ab}TVZ_1
       +\mu x_ay_bZ_1+x_ay_bTVZ_2
   =\delta_{ab}\alpha_a\beta_aX_a^D.                    \tag{A2}
\]

If `alpha^T U beta=mu=0`, precisely the first and third terms vanish.
Divided powers obey

\[
                         zZ_2=(m-3)Z_1.                  \tag{A3}
\]

Therefore, with `F=TVZ_2`, equation (A2) is exactly

\[
 \boxed{
 F\left(x_ay_b+\frac{a_{ab}}{m-3}z\right)
       =\delta_{ab}\alpha_a\beta_aX_a^D.}              \tag{A4}
\]

At `m=4`, one has `Z_2=z^[0]=1`, `Z_1=z`, and `m-3=1`.
Thus (A3)--(A4) have no negative divided power, zero denominator, or
exceptional normalization at the eight-site boundary.

Now choose `xi,eta` with `xi^T A eta=0`, multiply (A4) by
`xi_a eta_b`, and sum in `a,b`.  The common direct term vanishes by this
single bilinear equation, while the target diagonal retains only equal
indices.  Hence

\[
 \boxed{
 x(\xi)y(\eta)t(\alpha)v(\beta)z^{[m-4]}
   =\sum_{h=0}^2\xi_h\eta_h\alpha_h\beta_hX_h^D.}       \tag{A5}
\]

This calculation uses all four matching layers.  In particular, (A4)
retains the direct `A` block; it is discarded only in the optional second
contraction (A5).

## 2. Torus zeros and the exact retention maximum

Call a nonzero scalar multiple of one matrix unit a *scalar matrix unit*.
For `M in Mat_3(C)`, the bilinear form

\[
                         f_M(X,Y)=\sum_{r,s}M_{rs}X_rY_s \tag{A6}
\]

is a Laurent polynomial on `(C^*)^6`.  A Laurent polynomial is a unit
exactly when it is a nonzero scalar monomial.  Thus:

* if `M` is a scalar matrix unit, (A6) has no torus zero;
* if `M` has at least two nonzero entries, (A6) is a nonunit and lies in
  a maximal ideal of the torus coordinate ring, so it has a torus zero;
* if `M=0`, every torus pair is a zero.

This also has an elementary row-wise proof.  If all nonzero entries occupy
one row, two of them can be cancelled by a full-support `Y`.  If at least
two rows are nonzero, choose a torus `Y` away from their row hyperplanes;
then `MY` has at least two nonzero entries and admits a full-support
orthogonal `X`.

For `M=lambda E_rs`, isotropy says

\[
                         X_rY_s=0.                       \tag{A7}
\]

It therefore kills target colour `r` or target colour `s`, and three
active diagonal products are impossible.  Conversely, omitting `r` or
omitting `s` and taking both covectors nonzero on the complementary
two-set gives two active products.  Equal two-coordinate supports are a
convenient witness, not a necessary form of every isotropic pair.

Apply this independently to `A=lambda E_rs` and `U=mu E_kl`.  If
`I_A={r,s}` and `I_U={k,l}`, with repetitions removed, then the exact
maximum number of nonzero coefficients on the right of (A5) is

\[
\begin{array}{c|c}
\text{direct-block types}&\text{maximum active colours}\\ \hline
\text{neither is a scalar matrix unit}&3\\
\text{exactly one is a scalar matrix unit}&2\\
\text{both units and }I_A\cap I_U\ne\varnothing&2\\
\text{both units and }I_A\cap I_U=\varnothing&1.
\end{array}                                               \tag{A8}
\]

For the upper bound in the third and fourth rows, retaining two common
colours means omitting one common colour, and (A7) forces that omitted
colour to belong to both endpoint-index sets.  For the converse, omit an
index in their intersection.  If the sets are disjoint, omit one index
from each; their two complementary active sets meet in exactly one colour.
This proves both attainability and sharpness in every case.

## 3. The two consistency guards

### 3.1 Binary four-star guard

On four cyclic sites define

\[
                         L_j=e_0^{(j)}+e_1^{(j+1)}.
\]

A choice of one summand from every `L_j` is encoded by a cyclic binary
word.  If that word is nonconstant, it has a cyclic `1`-to-`0` transition.
The two factors bordering that transition occupy the same site, so their
product is zero in the site-square-zero algebra.  The two constant choices
survive once each, proving

\[
                         L_0L_1L_2L_3=X_0+X_1.          \tag{A9}
\]

Thus a binary output in (A5) is not contradictory even when `m=4`.
Equation (A9) does not specify the other eight dressed rows in (A4).

### 3.2 Twelve-site unstructured-multiplier guard

Partition twelve sites into four-sets `S_c={s_(c,0),...,s_(c,3)}` and
put

\[
 L_j=\sum_c e_c^{(s_{c,j})},\qquad
 R=\sum_c\bigotimes_{u\notin S_c}e_c^{(u)}.             \tag{A10}
\]

Fix the `c`-summand of `R`.  It already occupies every site outside
`S_c`.  Square-freeness therefore forces each `L_j` to choose its unique
component at `s_(c,j)`.  The resulting word is `X_c`, and summing over
`c` gives

\[
                         L_0L_1L_2L_3R=X_0+X_1+X_2.     \tag{A11}
\]

Here `R` is one deliberately chosen unstructured degree-eight multiplier.
The construction neither says that (A11) works for every multiplier nor
realizes `R=z^[4]` for a quadratic `z`.  Its exact conclusion is that
factor count and target support alone cannot rule out the ternary
four-star shape.

## 4. Repository-scope audit

The closest registered results do not close (A4):

* the pure-lift common-power theorems require a codimension-two multiplier
  in the target-pure lift span, together with its next-power provenance;
  `F=TVz^[m-4]` need not be target-pure;
* the sitewise response filtration and the coherent-line-field theorems
  use responses factored as `p_a s_b F`, or assume a resolution into at
  most two common line fields; the dressed quadratic
  `x_a y_b+a_ab z/(m-3)` has neither property in general;
* the coordinate-free diagonal square ideal uses one repeated marked star
  family, whereas (A4) has two independent families `x_a,y_b`;
* the source-Hessian rank-drop theorems require a pure Hessian multiplier,
  gauge rigidity, and rank-graph hypotheses not inherited by `F`;
* the arbitrary-complex six-site theorem excludes an ordinary quadratic
  matching tensor, not a quadratic dressed response times a higher-degree
  common multiplier.

These theorems remain applicable after additional hypotheses place (A4)
in one of their special strata.  They do not furnish a universal
contradiction to the exported packet.  Even the fully contracted ternary
boundary at `m=4` is a restriction of the four-way permanent tensor to a
three-term diagonal tensor; the repository records the corresponding
`Per_4` subrank problem as unresolved in
[`permanent-subrank-and-incidence-gap.md`](permanent-subrank-and-incidence-gap.md).

The usable new leverage is therefore the whole synchronized system (A4):
one actual multiplier `TVz^[m-4]`, six target-zero dressed quadratics,
three diagonal targets, and one shared tuple `(A,x,y,z)`.  Contracting it
again to (A5) loses precisely the synchronization that the consistency
guards show is necessary.
