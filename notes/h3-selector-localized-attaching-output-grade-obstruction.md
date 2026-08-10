# Selector localization erases endpoint fine degree but not the attaching output grade

> **Scope correction (commit `9dac232`).**  This note localizes the
> separately internal `(C_S,D_S)` presentation inherited from `87ee2bf`.
> Its `sum_S D_S=0` target is not the attaching relation of a genuine common
> full-nine row.  Such a row has a response companion `M_S`, so its literal
> aggregate is `alpha(C+D)+M=0`; even `D=0` leaves the terminal class free.
> The corrected source-relative target is
> `K=sum_S(M_S+alpha D_S)=0`, as proved in
> [`h3-full-nine-middle-companion-normalization-guard.md`](h3-full-nine-middle-companion-normalization-guard.md).
> The selector/output-grade calculation below and its checker are unchanged;
> only the formerly proposed common-packet normalization is retracted.

## Outcome

Localizing the two good-star selector determinants does remove the endpoint
fine-degree obstruction isolated in
[`h3-two-chart-h2-tagged-reinsertion-cokernel.md`](h3-two-chart-h2-tagged-reinsertion-cokernel.md).
Indeed, a selector inverse has the exact adjugate character needed to shift
any diagonal anchor into the selected off-diagonal endpoint degree.  This is
a genuine new route through the old fine grading.

It still does **not** normalize the grade-three attaching array of
[`h3-grade3-middle-attaching-target-obstruction.md`](h3-grade3-middle-attaching-target-obstruction.md).
Selector and adjugate coefficients are scalars on the residual output-word
module.  The diagonal anchors remain in the three pure residual summands,
whereas the attaching array lies in the twenty binary `3+3` midpoint
summands.  Localization does not connect those summands.

Consequently the exact localized midpoint presentation still has one row

\[
                         C_S+D_S=0                     \tag{1}
\]

for every three-set \(S\), where \(C_S\) is the canonical attaching cell
and \(D_S\) its physical normalization defect.  The desired augmentation

\[
                         \sum_S C_S=0                  \tag{2}
\]

is independent even after adjoining all three transported diagonal rows.
The exact separator from commit `87ee2bf` survives on the selector open set:

\[
        (C_S,D_S)=(\Theta_S,-\Theta_S),\qquad
        \sum_S C_S=-224.                               \tag{3}
\]

Thus determinant localization can solve the **endpoint character** problem,
but not the **source attaching** problem.  A proof still needs an
output-grade-changing, source-provenant Bianchi/attaching map.  More selector
rank, Cramer inversion, or scalar localization cannot supply it.

This is an exact localized-module obstruction, not a full ternary Krenn
counterexample.  In particular (3) retains the exact binary diagonal source
and canonical response array from `87ee2bf`, but it does not assert that the
independently localized third target grade is realized by one common physical
source.

## 1. The selector character really shifts the fine degree

Let \(P=(P_{i\mu})\) be a left selector matrix.  With the literal endpoint
grading

\[
                         \deg P_{i\mu}=e_i^L,
\]

every term of \(\det P\) has degree
\(\mathbf1^L=e_0^L+e_1^L+e_2^L\), while

\[
 \deg (\operatorname {adj}P)_{\mu i}=\mathbf1^L-e_i^L,
 \qquad
 \deg(P^{-1})_{\mu i}=-e_i^L.                         \tag{4}
\]

For two charts, the transition entry

\[
             T^L_{ai}=\sum_\mu \widetilde P_{a\mu}
                                      (P^{-1})_{\mu i}
\]

therefore has degree \(\widetilde e_a^L-e_i^L\).  The analogous right
transition has degree \(\widetilde e_b^R-e_i^R\).  Starting from diagonal
row \((i,i)\), multiplying by the two transition entries and two selected
response tags gives

\[
 (e_i^L+e_i^R)
 +(\widetilde e_a^L-e_i^L+\widetilde e_b^R-e_i^R)
 +2(\widetilde e_a^L+\widetilde e_b^R)
 =3(\widetilde e_a^L+\widetilde e_b^R).               \tag{5}
\]

So all three diagonal rows reach the selected terminal fine degree after
localization.  The checker exhibits the determinant-two selector

\[
 P=\begin{pmatrix}1&1&0\\0&1&1\\1&0&1\end{pmatrix},
 \qquad \widetilde P=I,
\]

on both ends.  For selected pair \((a,b)=(0,1)\), the three diagonal
transport coefficients are

\[
                         (1/4,-1/4,-1/4),              \tag{6}
\]

all nonzero.  The obstruction is therefore not caused by a vanishing
transition coefficient.

## 2. The residual output grading survives localization

Let \(A\) be the source-cell ring and invert the two selector determinants.
The residual coefficient module is still a direct sum

\[
 A[(\det P\det S)^{-1}]\langle e_w:w\in\{0,1,2\}^6\rangle.
                                                               \tag{7}
\]

Adjugate entries and transition coefficients belong to the localized scalar
ring.  They can change source-cell/endpoint characters as in (5), but
scalar multiplication preserves the basis vector \(e_w\).  The diagonal
anchors occupy

\[
                         e_{0^6},e_{1^6},e_{2^6},       \tag{8}
\]

whereas the attaching array occupies

\[
            e_{1^S0^{S^c}},\qquad |S|=3.              \tag{9}
\]

The three words in (8) and the twenty words in (9) are disjoint.  Thus a
transported diagonal row cannot add a relation inside the midpoint direct
summand.  This is exactly the limitation observed earlier for ordinary
good-star Cramer transport: inversion separates or relabels endpoint
channels; it does not manufacture the missing source-grade comparison.

## 3. Exact localized cokernel

Work just in the midpoint summand and retain one pair of formal coordinates
\((C_S,D_S)\) for every three-set.  The twenty physical mixed rows have
matrix

\[
                         [\ I_{20}\ I_{20}\ ].         \tag{10}
\]

The three transported pure rows form a disjoint three-column block, with
the nonzero coefficients (6).  Hence the retained localized matrix has rank
\(23\).  Adjoining (2) raises the rank to \(24\).  This calculation is
unchanged over any selector open set: localization is flat, and the output
direct-sum decomposition (7) remains literal.

The source-labelled values from `87ee2bf` give the stronger exact separator
(3).  Every row (1) and every transported pure row annihilates it, while
(2) evaluates to \(-224\).  Therefore even granting nonzero routes from all
three diagonal anchors does not normalize the attaching array.

The dependency-free checker
[`verify_h3_selector_localized_attaching_output_grade_obstruction.py`](../computations/verify_h3_selector_localized_attaching_output_grade_obstruction.py)
verifies the adjugate characters, the three active localized routes, the
pure/midpoint output-grade separation, the rank jump, and the exact
`87ee2bf` separator.  It uses runtime failures and runs unchanged under
normal, optimized, isolated, and optimized-isolated Python.

## 4. Sharp remaining interface

Selector localization has done everything its algebra allows: it erases the
old endpoint fine-degree separation.  The missing identity must additionally
change the residual output grade and retain common source provenance.  In
the notation of `87ee2bf`, the exact target remains

\[
                         \boxed{\sum_S D_S=0}.          \tag{11}
\]

Such a row could arise from a genuine two-chart Bianchi/attaching map or a
source syzygy coupling the pure and midpoint coefficient summands.  It
cannot arise from determinant inversion, adjugate/Cramer transport, or a
further rank statement about the same selector matrices alone.
