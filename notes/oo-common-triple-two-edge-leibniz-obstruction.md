# The two-edge curvature identity has a nonzero lower-filtration obstruction

## 1. Outcome

The integral two-edge identity

\[
 M^{pq}_{pq\mid rs}-M^{pr}_{pr\mid qs}
 -D^{pq}_{pq\mid rs}+D^{pr}_{pr\mid qs}
   =\kappa X_2^D                                             \tag{1}
\]

does not admit a null-homotopy using the literal one-edge module plus the
two labelled diagonal rows.  Its four order-two columns are entirely
second-order Leibniz cross terms.  Their combined lower-filtration tail is
the right side of (1), and an explicit integral covector detects it.

For the fixed-`s` one-edge module, adjoining both labelled copies of the
three compatible `22` diagonal columns gives rank 10 in a 108-dimensional
feature space.  Adjoining the tail raises rank to 11.  Even after allowing
all 28 one-edge columns, the lower module has rank 24 and the tail raises it
to 25.  Therefore the obstruction is not caused by the fixed residual-site
choice.

The multiplication-safe Euler fallback closes only the trace part:

\[
 \sum_e e\partial_eH=4H,qquad
 \sum_{\substack{e<f\\s\in e\cup f}}
 ef\partial_e\partial_fH=3H,qquad
 \sum_{e<f}ef\partial_e\partial_fH=6H.                     \tag{2}
\]

The curvature difference is a traceless two-pair component and survives
these contractions.

The rank-two adjugate proposal also has a sharp guard.  The exact identity

\[
 B=uv^{\mathsf T}+qxy^{\mathsf T},\qquad
 \operatorname {adj}(B)
   =q(v\mathbin\times y)(u\mathbin\times x)^{\mathsf T},
 \qquad B\operatorname {adj}(B)=0                         \tag{3}
\]

is valid in residual degree six.  But any common-triple coefficient of
(3) whose displayed lead is

\[
                  M_{pq\mid rs}-M_{pr\mid qs}              \tag{4}
\]

must contain an additional remainder outside the one-edge/diagonal module.
The obstruction covector takes value (1) on (4), value zero on every
known lower row, and hence value (-1) on the unshown adjugate remainder.
Thus (3) does not bypass the obstruction using only the existing rows.  It
may instead identify the required new same-order/higher comparison row.

This freezes a precise nonzero obstruction class.  It does not prove that
no principal-parts or adjugate enlargement can kill it, and it does not
prove the anchored overlap-injectivity lemma or Krenn's conjecture.

## 2. Exact second-order product rule

For distinct physical edge variables (e,f), put

\[
                         J_{ef}=ef\partial_e\partial_f.       \tag{5}
\]

Its product rule is

\[
\begin{aligned}
 J_{ef}(AB)={}&J_{ef}(A)B+AJ_{ef}(B)+\Gamma_{ef}(A,B),\\
 \Gamma_{ef}(A,B)={}&ef\bigl(
   (\partial_eA)(\partial_fB)
  +(\partial_fA)(\partial_eB)\bigr).                       \tag{6}
\end{aligned}

Fix the distinct-head word

\[
                         w=(a,0,1,\ell,2,2,2,2).             \tag{7}
\]

Every hafnian monomial is squarefree in its four physical matching edges.
For either endpoint partial matching (m=\{e,f\}), split

\[
                         H_w=e\,\partial_eH_w+H_w^{\bar e}. \tag{8}
\]

The cofactor \(\partial_eH_w\) is independent of (e), and
\(H_w^{\bar e}\) contains no (e).  Consequently

\[
 J_{ef}(H_w)
 =\Gamma_{ef}(e,\partial_eH_w),                            \tag{9}
\]

while all three strict second-order terms on the first line of (6) vanish.
The left side of (9) is exactly the three-term mixed column (M_m).

For the diagonal base (G=H_D^{(2)}-X_2^D), factor

\[
                             mG=e(fG).                       \tag{10}
\]

Again the strict terms vanish and

\[
                         J_{ef}(e(fG))=\Gamma_{ef}(e,fG)=mG. \tag{11}
\]

Thus all four columns in (1) are pure cross terms.  Combining (9) and
(11) with the signs in (1) shows that the full Spencer/Leibniz tail is
exactly (kappa X_2^D), not zero.

The checker verifies (6), (9), and (11) in the universal sparse polynomial
ring for all three endpoint pairings and all nine \((a,\ell)\) types.  No
special source values are used.

## 3. Reduction against the lower module

Use the same 105 labelled matching features and three target features as in
the two-edge identity.  The lower generators are:

1. both source-labelled copies of every one-edge column
   (C_e=e\partial_eH_w); and
2. both labelled copies of
   (D_m=m(H_D^{(2)}-X_2^D)) for the three matchings
   (m) on `p,q,r,s`.

Exact rational elimination gives

\[
\begin{array}{l|r|r|r|r}
\text{lower module}&\text{columns}&\text{rank}&\text{cokernel}&
 \text{rank with tail}\\ \hline
\text{fixed-}s\text{ one-edge + anchors}&20&10&98&11\\
\text{all one-edge + anchors}&62&24&84&25.
\end{array}                                                \tag{12}
\]

The two chart copies are kept separate in the domains; their equality is
found by elimination rather than imposed in advance.

There is a small integral upper certificate for (12).  On source matching
features put

\[
\begin{aligned}
 \Lambda_{m src}={}&-\delta_{pr\mid qs\mid45\mid67}
 +\delta_{pr\mid q4\mid s5\mid67}
 +\delta_{ps\mid qr\mid45\mid67}\\
 &-\delta_{ps\mid q4\mid r5\mid67}
 -\delta_{p4\mid qr\mid s5\mid67}
 +\delta_{p4\mid qs\mid r5\mid67}.                       \tag{13}
\end{aligned}
\]

As in the one-edge calculation, every physical edge has total coefficient
zero in (13), so (Lambda_{m src}(C_e)=0) for all 28 edges.  Extend it
to the three target features by

\[
\begin{array}{c|ccc}
m&pq\mid rs&pr\mid qs&ps\mid qr\\ \hline
\Lambda(mX_2^D)&0&-1&1.
\end{array}                                                \tag{14}
\]

The entries in (14) are exactly
\(Lambda_{m src}(mH_D^{(2)})\).  Therefore

\[
                   \Lambda(D_m)=0                           \tag{15}
\]

for all three diagonal columns and both chart copies.  On the curvature
tail,

\[
 \Lambda\bigl((pq\mid rs-pr\mid qs)X_2^D\bigr)
                         =0-(-1)=1.                         \tag{16}
\]

Equations (13)--(16) prove the two rank jumps in (12) over
\(mathbb Z\), independently of Gaussian elimination.

## 4. Why Euler contraction does not repair the class

A degree-four matching monomial contains four edges, six unordered edge
pairs, and exactly one edge through `s`.  It follows term by term that

\[
 \sum_e C_e=4H_w,qquad
 \sum_{m\ni s}M_m=3H_w,qquad
 \sum_mM_m=6H_w.                                          \tag{17}
\]

These are integral identities; division by 3, 4, or 6 is unnecessary.
They show that the total coefficient contractions descend to ordinary
multiplication by the original mixed row.

However, the target in (1) is the difference of two individual endpoint
pairings.  The covector (13)--(14) kills every Euler total, since those
totals lie in the one-edge/original-row image, but detects the difference
by (16).  Hence averaging the second coefficients removes only the scalar
trace mode and cannot recover the curvature component.

## 5. The adjugate counterguard

The generic rank-two formula (3) is checked as an exact sparse polynomial
identity, including all entries of (B\operatorname {adj}(B)).  It is a
genuine multiplication-safe source identity in degree six, so it remains a
plausible source of an additional comparison cell.

What it cannot do is close (1) with only the already known lower rows.  Let
an extracted cross-chart coefficient of (3) have curvature lead (L) as in
(4), and write its remaining source tail as (R).  Since (3) is a source
identity,

\[
                              L+R=0.                         \tag{18}
\]

Direct matching expansion gives

\[
                         \Lambda_{m src}(L)=1.             \tag{19}
\]

Therefore (18) forces

\[
                         \Lambda_{m src}(R)=-1.            \tag{20}
\]

Every one-edge and diagonal correction has value zero.  Thus (R) is not
in their span.  This conclusion does not require guessing the rest of the
adjugate expansion: any exact expansion with lead (4) must carry the same
nonzero obstruction-grade remainder.

The adjugate route is therefore refined, not wholly discarded.  The next
useful calculation would identify (R) as a new literal row and show that
its own boundary cancels (20).  Merely citing (B\operatorname {adj}(B)=0)
does not supply the lower null-homotopy.

## 6. Consequence and scope

The two-edge module located the correct curvature--anchor associated class,
but the first attempted lift stops on the integral class (13)--(16).  A
proof now needs at least one of:

* a genuine second-principal-parts/Hasse cell whose extra boundary pairs
  (-1) with (Lambda);
* the explicit nonlower remainder from the cross-chart adjugate identity;
* a third-order operation whose (A_\infty) boundary cancels the cross
  term; or
* an independent source identity proving the obstruction class vanishes on
  the active/good-star localization.

No further unstructured rank enlargement at coefficient orders one or two
is useful: both images and the separating integral covector are exact.

## 7. Reproduction

Run

```text
python3 computations/verify_oo_common_triple_two_edge_leibniz_obstruction.py
python3 -O computations/verify_oo_common_triple_two_edge_leibniz_obstruction.py
```

The checker verifies the full Leibniz formula, all relevant factorizations,
the Euler identities, both lower-module ranks, the integral obstruction
covector, the generic rank-two adjugate formula, and the forced adjugate
remainder pairing for all nine normalized colour types.  Its frozen digest
is

```text
601df68efa257a52ab7096c91a555e5bb5447988e497915d19d066f17f1e5ae4
```
