# Middle-word rows leave exactly one response-cubic attaching class

## Outcome

Extend the exact through-Hamming-two fine-degree module from commit
`87304b5`.  For a selected off-diagonal row write

\[
 \alpha=d_{01}\ne0,\qquad Q_j=R^{[j]}q^{[3-j]},\qquad T=Q_3.
\]

Retain the two-chart static four-row block, whose determinant is \(-3\),
and the three response rows

\[
 e_0=\alpha Q_0+Q_1,\quad
 e_1=\alpha Q_1+2Q_2,\quad
 e_2=\alpha Q_2+3T.                                    \tag{1}
\]

Now adjoin every literal binary midpoint coefficient.  These are the 20
source-labelled words

\[
 m_S,\qquad S\subset\{0,\ldots,5\},\quad |S|=3,        \tag{2}
\]

where the word has colour 1 on \(S\) and colour 0 on its complement.
Each has count type \((3,3,0)\) and lies at Hamming distance three from
both binary pure words, so none was present in the Hamming-two block.

The honest dynamic module has coordinates

\[
                  (Q_0,Q_1,Q_2,T,(m_S)_{|S|=3})
\]

and rows \(e_0,e_1,e_2\) together with the 20 literal midpoint unit rows.
Its rank is 23 in dimension 24.  The exact cokernel separator is

\[
 k_\alpha=(-6,6\alpha,-3\alpha^2,\alpha^3,0,\ldots,0). \tag{3}
\]

It detects

\[
 [Q_3](k_\alpha)=\alpha^3,\qquad
 [4\chi](k_\alpha)=-8\alpha^3.                         \tag{4}
\]

Thus adding all literal middle rows does **not** kill the response cubic.
The static two-chart block remains a direct summand and leaves the same
one-dimensional cokernel.

## The exact missing attaching row

The primitive integral row which closes the module is

\[
                  A=16T+\sum_{|S|=3}m_S.              \tag{5}
\]

Modulo the already present row \(e_2\), this is the canonical twenty-cut
landing.  Indeed the committed normalization is
\(\sum_S\Theta_S=8\chi\), and the exact integral target identity is

\[
              \boxed{8\chi=8e_2-A+\sum_Sm_S.}         \tag{6}
\]

If the normalized middle aggregate is
\(M=-\frac1{16}\sum_Sm_S\), then (5) is simply
\(16(T-M)\).  This distinguishes the two objects which must not be
silently identified: \(T\) is the response-grade-three class, whereas
\(M\) is the readout of literal middle full-row coefficients.

Adjoining (5) raises the dynamic rank from 23 to 24; at \(\alpha=1\) the
24-by-24 determinant is \(16\).  Direct-summing the unchanged static
block raises the full rank from 27 to 28.  Hence (5), or an equivalent
source-provenant attaching relation, is both sufficient and minimal in
this bounded module.

## Source-label and scope guard

A starting full-nine row followed by three endpoint response tags reaches
fine degree \(4(e_0^L,e_1^R)\) only when the row and all three tags carry
the selected label pair \((0,1)\).  The checker exhausts all \(3^8\)
label choices and finds this single route.  No diagonal anchor or crossed
static row enters the terminal degree by a nonnegative label route.

Equation (5) is the **missing** row, not a proved physical identity.  The
calculation therefore returns an exact attaching obstruction, not a proof
that \(Q_3=0\).  It proves that raw middle-word vanishing and the complete
through-Hamming-two/two-chart static data are insufficient until a
source-faithful map identifies the normalized middle aggregate with the
response cubic.  Granting \(e_3=\alpha Q_3\) directly would assume that
missing map and make the calculation tautological.

## Verification

Run

```text
.venv/bin/python computations/verify_h3_h2_middle_attaching_obstruction.py
```

The checker enumerates all 20 literal midpoint labels and all endpoint
fine-degree routes; reproduces the static determinant; computes the exact
ranks, separator values, attaching closure, and integral identity at three
nonzero rational values of \(\alpha\); and freezes the complete ledger.
