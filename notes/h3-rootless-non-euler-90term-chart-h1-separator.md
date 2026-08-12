# The non-Euler 90-term Hasse row has a primitive chart-H1 marked separator

## Outcome

Fix one of the five non-Euler faces constructed in
[the diagonal-stabilizer jet theorem](h3-rootless-non-euler-diagonal-stabilizer-jet.md).
In its selected mixed fine degree, the complete corrected Hasse coefficient
has 90 physical matching terms, each with coefficient one.  Its two literal
chart decompositions have the same source boundary, zero target, and zero on
all fifteen ordinary-residue companions.  Their primitive difference is
therefore a correction-kernel class.

The normalized marked-sector cochain does not vanish on that class: it reads
one.  Consequently the non-Euler polar does **not** define a
zero-indeterminate (P(e_v)) through the literal two-chart module.  The
smallest missing datum is now exact: a source-valid higher comparison whose
boundary kills this chart-difference class and whose terminal value cancels
its marked readout.

This is a sparse separator in the literal chart presentation, not a no-go
for every larger source resolution.  In particular, the chart difference is
a presentation-kernel class, not a second physical coordinate correction.

## 1. The augmented two-chart correction complex

Use the direct-free eight-site chart with

\[
 x=0,\quad D=\{1,2,3,4,5\},\quad p=6,\quad q=7,
 \quad A_{p3}=0.
\]

For (v=1), the selected mixed word is

\[
                         w=00211200.                  \tag{1}
\]

The non-Euler site-weight pair of `da53697` has corrected mixed-Hasse
coefficient

\[
  J_A Z_{\lambda,\mu}+H_A(X_\lambda,X_\mu)
                    =H_w(A)=0.                        \tag{2}
\]

Term by term, its coefficient on every direct-free perfect matching is
one.  Thus its physical matching vector is

\[
                         B_w=\sum_{M\not\ni p3} M,     \tag{3}
\]

with 90 terms.

Let (c_{pq}) and (c_{pr}) denote the two literal chart lifts.  The first
splits (3) into 15 direct and 75 two-star terms; the second has zero direct
and 90 two-star terms.  After forgetting the tags both are exactly (B_w).

Form the augmented boundary

\[
 \widehat d:\mathbb Q c_{pq}\oplus\mathbb Q c_{pr}
       \longrightarrow
       E_{\rm match}^{90}\oplus E_{\rm tgt}^{3}
                         \oplus E_{\rm ores}^{15}.     \tag{4}
\]

Because (1) is mixed, both target components vanish.  Both weight systems
are supported only in colour zero, while every endpoint of every residual
four-site companion has colour one or two.  Hence the two first weights,
the diagonal correction, and the mixed Hessian all vanish termwise on all
fifteen ordinary-residue matching companions.  Therefore

\[
       \widehat d(c_{pq})=(B_w,0,0)
                         =\widehat d(c_{pr}).           \tag{5}
\]

The matrix in (4) has rank one and primitive kernel

\[
                         k_w=c_{pq}-c_{pr}.             \tag{6}
\]

This is exactly the selected-word kernel row in
[the all-word connecting-class rigidity theorem](h3-full-nine-connecting-class-rigidity.md).
With no additional higher comparison supplied, it generates the correction
(H_1) of the literal two-column complex.

## 2. The six-entry separator

Differentiate the two chart decompositions by the marked edges

\[
                     a_{01}^{00},\qquad a_{67}^{00}.   \tag{7}
\]

In the (pq) chart all three surviving monomials lie in the direct sector;
in the (pr) chart the same three monomials lie in the two-star sector.
They are precisely the deletion-face hafnian

\[
 h_1=q_{23}^{21}q_{45}^{12}
       +q_{24}^{21}q_{35}^{12}
       +q_{25}^{22}q_{34}^{11}.                       \tag{8}
\]

Let (T) be this tagged marked-tail map and define the normalized chart-odd
cochain

\[
 \Lambda_1((pq,{\rm direct}),M)=\frac16,qquad
 \Lambda_1((pr,{\rm two\ star}),M)=-\frac16
                         \quad(M\in\operatorname{supp}h_1). \tag{9}
\]

It has only six nonzero entries.  Direct calculation gives

\[
 \Lambda_1T(c_{pq})=\frac12,\qquad
 \Lambda_1T(c_{pr})=-\frac12,
 \qquad \boxed{\Lambda_1T(k_w)=1}.                   \tag{10}
\]

Thus

\[
       \ker\widehat d\not\subseteq\ker(\Lambda_1T). \tag{11}
\]

The marked readout cannot descend independently of the choice of literal
chart lift.  This is the requested sparse separator for correction (H_1).

## 3. Exact scope and next map

Equation (11) does not contradict the existence of a larger physical
overlap--jet complex.  It says what such a complex must add.  There must be
a source-valid higher cell (b_w) with

\[
                 d b_w=k_w,                            \tag{12}
\]

together with a compatible terminal component whose boundary cancels the
unit in (10).  Merely choosing one chart lift is not source-provenant, and
regarding (k_w) as a physical tangent is forbidden by the
[presentation/physical jet distinction](h3-rootless-presentation-jet-physical-polar-obstruction.md):
its physical forgetful image is zero.

So the result is simultaneously stronger and narrower than saying that the
marked map is undefined.  The complete literal augmented module is defined,
and its first obstruction is the primitive unit (10).  What remains
undefined is precisely the new higher comparison differential (12).

## Verification

Run

    python3 computations/verify_h3_rootless_non_euler_90term_chart_h1_separator.py
    python3 -O computations/verify_h3_rootless_non_euler_90term_chart_h1_separator.py
    python3 -I -S computations/verify_h3_rootless_non_euler_90term_chart_h1_separator.py

The checker pins the non-Euler physical jet, the direct-free full-nine row,
and the all-word connecting-class rigidity theorem.  It reconstructs all 90
corrected matching coefficients, both literal chart partitions, the three
target and fifteen ordinary-residue rows, the primitive correction kernel,
the three marked terms in each chart, and the six-entry rational separator.
The frozen ledger digest is

    000871fd19267809d25b89a4c9ab01ab9d491996e978cb875d97b304ae383376

