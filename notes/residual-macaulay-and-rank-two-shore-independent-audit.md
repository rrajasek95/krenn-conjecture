# Independent audit: residual Macaulay rank and rank-two shores

## 1. Verdict

The formal algebraic statements in both audited notes are correct, subject
to the ambient hypotheses stated below.

* Proposition 1.1 in
  [the residual Macaulay note](residual-macaulay-quotient-is-the-common-divisor.md)
  is **PASS**:
  \(\operatorname{rank}\mu_{f,L'}=h-\deg\gcd(f,L')\).
* Lemma 4.1 there is **PASS** as a two-axis flag statement.
* Lemma 2.1 and Theorem 1.1 in
  [the rank-two shore note](full-nine-rank-two-shore-coordinate-support.md)
  are **PASS**.
* The common-exceptional-site identity and its two alternatives are
  **PASS**, with the alternatives understood inclusively and with the first
  allowing \(q^{[h]}=0\).

There is no counterexample to any boxed formal conclusion.  There are four
actionable scope/wording corrections:

1. state \(h\geq1\) explicitly in both notes;
2. split off the case \(d=h\) in the proof of the Macaulay proposition,
   because calling two degree-zero units a complete intersection is not
   standard;
3. replace the claim that an annihilating covector must additionally be
   proved point-supported: a nonzero element of
   \((\operatorname{coker}\mu)^*\) already implies a common root by
   Proposition 1.1;
4. keep “two anchors are the threshold” qualified as a threshold only for
   **partial flag alignment**.  Lemma 4.1 does not transport the needed
   coefficient equations and therefore does not establish sufficiency for
   the active overlap/gluing problem.

## 2. Residual Macaulay proposition

Let \(n=2h-1\) and \(I=(f,L')\).  In degree \(n\),

\[
 I_n=fS_{h-1}+L'S_{h-1}.
\]

Therefore the image of multiplication modulo \(fS_{h-1}\) is
\(I_n/fS_{h-1}\), and hence

\[
 \operatorname{coker}\mu_{f,L'}=(S/I)_n. \tag{A1}
\]

Write \(g=\gcd(f,L')\), \(d=\deg g\), and
\(f=g\bar f\), \(L'=g\bar L'\).  Suppose first that
\(d<h\) and \(L'\ne0\).  For every linear factor \(\ell\) of
\(\bar f\), the subspace

\[
 \{e\in\bar L':\ell\mid e\}
\]

is proper; otherwise \(\ell\) would divide the gcd of \(\bar f\) and
all of \(\bar L'\).  Over the infinite field \(\mathbb C\), finitely
many proper linear subspaces cannot cover \(\bar L'\).  Thus one may
choose \(\bar e\in\bar L'\) with
\(\gcd(\bar f,\bar e)=1\).

Put \(m=h-d>0\).  The quotient by the coprime degree-\(m\) binary forms
\(\bar f,\bar e\) has Hilbert series

\[
 \frac{(1-t^m)^2}{(1-t)^2}
\]

and vanishes in every degree at least \(2m-1\).  The needed normalized
degree is

\[
 n-d=2h-1-d=(2m-1)+d\geq2m-1. \tag{A2}
\]

Consequently

\[
 (\bar f,\bar L')_{n-d}=S_{n-d},
 \qquad I_n=gS_{n-d}. \tag{A3}
\]

It follows that

\[
 \dim(S/I)_n=(n+1)-(n-d+1)=d. \tag{A4}
\]

Since \(\dim Q_f=\dim S_n-\dim fS_{h-1}=2h-h=h\),
(A1)--(A4) give

\[
 \operatorname{rank}\mu_{f,L'}=h-d. \tag{A5}
\]

The omitted boundary cases are harmless but should be explicit:

* if \(L'=0\), the map has rank zero and the convention gives \(d=h\);
* if \(L'\ne0\) and \(d=h\), every member of \(L'\) is a scalar
  multiple of \(f\), so the map modulo \(fS_{h-1}\) again has rank zero.

Thus the proposition is fully correct.  I also checked (A5) by exact
coefficient-matrix elimination for every \(h=1,\ldots,6\) and every
\(d=0,\ldots,h\), using

\[
 g=v^d,\qquad f=v^d(u^{h-d}+v^{h-d}),\qquad e=v^h
\]

for \(d<h\), and \(e=f=v^h\) for \(d=h\).  Every computed quotient
rank was \(h-d\).  This is only a sanity check; the Hilbert-function
argument above proves the general statement.

### Consequence at \(h=3\)

For \(h=3\), rank at most two is equivalent to \(d\geq1\).  Over
\(\mathbb C\), that is equivalent to a common linear factor, hence to a
projective point at which \(f\) and every member of \(L'\) vanish.  This
also covers \(L'=0\), because every nonzero cubic has a projective root.

The dual interpretation needs one wording correction.  Merely choosing an
arbitrary nonzero covector in \(Q_f^*\) proves nothing, but constructing

\[
 0\ne\lambda\in Q_f^*,
 \qquad \lambda(eg)=0
 \quad(e\in L',\ g\in S_{h-1}) \tag{A6}
\]

is already sufficient.  Equation (A6) says
\(\lambda\in(\operatorname{coker}\mu)^*\), so the rank is deficient and
Proposition 1.1 supplies the common point.  One need not separately prove
that this particular \(\lambda\) is an evaluation functional at a single
root.  The genuinely hard source-provenant step is producing (A6), not a
second support theorem for \(\lambda\).

For squarefree \(f\), the displayed decomposition into three evaluation
fibres is correct after choosing fibre trivializations.  For nonreduced
\(f\), principal-part functionals occur, but (A5) still turns any nonzero
cokernel into a common linear factor.

## 3. Transported diagonal anchors

For \(c\in\{r,s\}\), put

\[
 x_c=A^{-\mathsf T}e_c,
 \qquad y_c=B^{-\mathsf T}e_c.
\]

Then

\[
 A^{-\mathsf T}E_{cc}B^{-1}=x_cy_c^{\mathsf T}. \tag{A7}
\]

The right side is nonzero and rank one.  A nonzero diagonal rank-one
matrix has exactly one nonzero diagonal cell.  Therefore there is a label
\(k_c\) such that both \(x_c\) and \(y_c\) are nonzero multiples of
\(e_{k_c}\).  Since \(A^{-\mathsf T}\) is invertible,
\(x_r,x_s\) are independent, so \(k_r\ne k_s\); the same conclusion also
follows from \(B^{-\mathsf T}\).  This proves Lemma 4.1 exactly as stated.

It additionally implies that all four transported matrix units on the
\(r,s\) block land in the corresponding \(k_r,k_s\) coordinate block:

\[
 A^{-\mathsf T}E_{cd}B^{-1}
   =(A^{-\mathsf T}e_c)(B^{-\mathsf T}e_d)^{\mathsf T},
 \qquad c,d\in\{r,s\}. \tag{A8}
\]

What it does **not** imply is that the source equations provide all four
units with the coefficient factorizations needed downstream.  The note
acknowledges this immediately after the lemma.  Accordingly, “local
threshold” is proved only for aligning a two-label flag.  The claim that
two anchors plus a crossed zero row will construct the desired Macaulay
annihilator remains a well-motivated target, not a theorem in this note.
The one-anchor guard proves necessity of more than one anchor under its
stated hypotheses; the cited two-dark-colour pattern makes the three-row
interaction plausible, but does not by itself prove sufficiency in the
active selector chart.

## 4. The one-row tensor lemma

Let \(\pi:V\to V/\mathbb Cu\) and
\(\bar Q=(\pi\otimes1)Q\).  Projecting the three equations gives

\[
 b_j\bar Q=c_j\pi(e_j)\otimes Y_j. \tag{A9}
\]

If \(\bar Q=0\), every active \(j\) satisfies
\(\pi(e_j)=0\), because \(Y_j\ne0\).  The line \(\mathbb Cu\) contains
at most one of the three independent coordinate vectors, so there is at
most one active index.

If \(\bar Q\ne0\), an active index with \(\pi(e_j)\ne0\) forces
\(b_j\ne0\) and makes \(\bar Q\) a pure tensor whose second-factor line
is \(\mathbb CY_j\).  Two such indices are impossible because distinct
\(Y_j\) are nonproportional (the stated linear independence is stronger
than needed).  There is at most one active index with
\(\pi(e_j)=0\), again because \(\mathbb Cu\) contains at most one
coordinate axis.  Thus there are at most two active indices.  If there are
two, exactly one has zero projection, and \(u\) lies on that active
coordinate axis.  Lemma 2.1 is therefore correct.

## 5. Application to a rank-two shore

This argument uses the following ambient assumptions, which should be
restated in the note for self-containment:

* \(h\geq1\), \(|W|=2h\);
* multiplication is in
  \(\bigotimes_{y\in W}(\mathbb C\oplus V_y)\), with
  \(V_yV_y=0\) and fixed ternary bases;
* \(X_i=\bigotimes_{y\in W}e_i^{(y)}\);
* all nine equations hold literally in top degree; and
* \(P:\mathbb C^3\to\bigoplus_yV_y\) is injective.

If \(\operatorname{rank}P_{\bar x}=2\), its kernel is a line.  For
\(0\ne c\) in that kernel,

\[
 P(c)=P_x(c)=u\in V_x,
\]

and global injectivity gives \(u\ne0\).  Top degree identifies

\[
 ({\cal R}_W)_{2h}=V_x\otimes
        \bigotimes_{y\ne x}V_y. \tag{A10}
\]

When \(P(c)\) multiplies \(s_jq^{[h-1]}\), every term containing an
\(x\)-factor vanishes by \(V_xV_x=0\).  The terms avoiding \(x\) are
exactly

\[
 u\otimes
 \left((s_j|_{W\setminus\{x\}})
       (q|_{W\setminus\{x\}})^{[h-1]}\right). \tag{A11}
\]

There is no missing binomial or factorial coefficient: the surviving term
is precisely the all-off-\(x\) term in the divided-power expansion.  The
\(c\)-weighted sum of column \(j\) is therefore

\[
 (c^{\mathsf T}a)_jQ+u\otimes h_j
   =c_j e_j^{(x)}\otimes
       \bigotimes_{y\ne x}e_j^{(y)}. \tag{A12}
\]

The three off-\(x\) monochromatic tensors are nonzero and independent, so
Lemma 2.1 applies and proves the claimed coordinate-support classification.
The transposed proof is valid provided the second endpoint map \(S\) is
injective.

No rootlessness, genericity, invertibility of \(a\), or support condition
on \(q\) is used.  Conversely, the complete nine literal equations and
global injectivity are essential hypotheses; the theorem should not be
quoted for a contracted packet or for a merely formal response identity.

## 6. Both shores exceptional at the same site

Let \(c,d\) span the kernels of \(P_{\bar x},S_{\bar x}\).  Then
\(P(c),S(d)\in V_x\), so their product is zero.  Taking the \((c,d)\)
bilinear combination of the full nine equations gives exactly

\[
 (c^{\mathsf T}ad)q^{[h]}
       =\sum_i c_id_iX_i. \tag{A13}
\]

If \(c^{\mathsf T}ad\ne0\), the right side is supported on
\(\operatorname{supp}(c)\cap\operatorname{supp}(d)\), a set of size at
most two.  Hence \(q^{[h]}\) lies in the span of at most two
monochromatic targets.  This includes the possibility that
\(q^{[h]}=0\); if “unary/binary power” is intended to mean nonzero, the
note must add \(q^{[h]}\ne0\) or say “supported on at most two targets,
possibly zero.”

If \(c^{\mathsf T}ad=0\), independence of \(X_0,X_1,X_2\) gives
\(c_id_i=0\) for every \(i\), equivalently

\[
 \operatorname{supp}(c)\cap\operatorname{supp}(d)=\varnothing. \tag{A14}
\]

The two alternatives are logically correct but are not necessarily
exclusive.  They also require the exceptional site to be the same for the
two endpoint stars and both off-site ranks to be exactly two.  Subject to
those conditions, (A13)--(A14) are a genuine proved reduction of the
common-coloop chart, not a heuristic.  Closing either resulting branch by
the scalar-zero packet or by transported anchors remains future work.

