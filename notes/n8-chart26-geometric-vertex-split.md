# The first nonsquarefree cell selects an exact geometric vertex split

The complete degree-five Buchberger layer and first degree-six compatibility
cell are exact.  This note records the rigorous two-branch reduction selected
by the repeated coordinate.  The first cell now has an exact branchwise
normal form, but neither branchwise target membership nor termination of an
iterated split is claimed.

## 1. General radical splitting lemma

Let \(A\) be a commutative ring, \(I\subset A\) an ideal, and \(x\in A\).
Then

\[
 \boxed{
   \sqrt I=\sqrt{I+(x)}\cap\sqrt{I:x^\infty}.}            \tag{1}
\]

One inclusion is immediate.  Conversely, suppose
\(f^a=i+xg\in I+(x)\) and \(x^Nf^b\in I\).  Modulo \(I\),

\[
 f^{aN+b}=(xg)^Nf^b=g^N(x^Nf^b)=0.
\]

Thus \(f\in\sqrt I\), proving (1) algebraically.  Geometrically the two
ideals describe the hyperplane part \(x=0\) and the closure of the open
part \(x\ne0\) of \(V(I)\).

For a target \(F\), formula (1) says

\[
 F\in\sqrt I
 \Longleftrightarrow
 \begin{cases}
  F\in\sqrt{I+(x)},\\
  F\in\sqrt{I:x^\infty}.
 \end{cases}                                             \tag{2}
\]

The second condition is equivalent to \(F\in\sqrt{IA[x^{-1}]}\).  In
certificate form, the two branches ask for integers \(r,s\geq1\) and
\(N\geq0\) such that

\[
             F^r\in I+(x),\qquad x^N F^s\in I.           \tag{3}
\]

Thus this is a finite algebraic cover, not a heuristic case distinction.

## 2. The coordinate selected by chart 26

For the normalized chart-26 ideal \(I^h\), the complete degree-five
Buchberger layer consists of 84,005 mutually reduced cells with distinct
squarefree leading monomials.  The first cross-word degree-six compatibility
cell has the minimal leading monomial

```text
0948cfcfebef
 = (02:00)(13:00)(46:00)^2(57:01)(57:12).
```

All five squarefree degree-five divisors were checked against the complete
84,005-cell leading set, and none occurs.  Hence this is a genuine minimal
nonsquarefree generator of the chosen initial ideal.  Put

\[
                         x=x_{46}^{00}.                   \tag{4}
\]

Applying (1) to \(I^h\) gives the exact next decomposition

\[
 \sqrt{I^h}
   =\sqrt{I^h+(x)}\cap\sqrt{I^h:x^\infty}.               \tag{5}

The same statement may be combined with the existing \(t\)-saturation by
localizing or adjoining \(t\) in either order.

## 3. Why this is better aligned with the cell

On the closed branch \(x=0\), the repeated leading term disappears and the
compatibility polynomial exposes its next surviving term.  Combinatorially,
one off-support decorated edge has been deleted.  This branch should be
compared with the neighboring support charts and with chart 25's Hamilton
complement.

On the open branch \(x\ne0\), the repeated factor is a Laurent unit.  The
same compatibility cell can be divided by a power of \(x\), so its
multiplicity is not an obstruction to a localized contraction.  Any finite
certificate in this branch clears denominators to the second identity in
(3).

This does not prove that either branch is radical or that the pure target is
in its radical.  Its advantage is structural: the first failure of the
global squarefree degeneration chooses the branching coordinate
canonically.  Repeating (5) at later repeated cells would build a
source-labelled geometric vertex decomposition.  Termination would amount
to a well-founded statistic on deleted/inverted decorated edges, precisely
the missing acyclicity datum in the filtered Morse approach.

## 4. Exact closed-branch reduction

Let \(G\) be the frozen 546-term degree-six compatibility polynomial.
Setting \(x=0\) kills 258 terms and leaves

\[
 \#\operatorname{supp}(G|_{x=0})=288,
 \qquad
 \#_{\deg_y=3,4,5,6}=(1,18,77,192).
\]

Its 288 coefficients consist of 144 copies of each of \(+1\) and \(-1\).
The restriction is already reduced by all restricted degree-four generators.
The exact restricted degree-four census is

\[
 6558=5830+728,
\]

where 5830 generators retain 105 terms and 728 retain 90 terms.  None
vanishes, and their 6558 leading monomials remain distinct squarefree
monomials of degree four.

Restricting the complete 84,005-cell degree-five layer gives the exact term
census

\[
\begin{array}{c|rrrrr}
\#\text{ terms}&90&150&156&165&180\\ \hline
\#\text{ cells}&436&681&4731&5688&72469.
\end{array}
\]

All 84,005 raw restrictions are nonzero and have distinct squarefree
degree-five leads.  Exactly 653 expose a term reducible by the changed
degree-four leads.  Exact division sends every one of those 653 cells to
zero: 436 use one degree-four column and 217 use two, for 870 columns total.
Thus 83,352 degree-five restrictions survive unchanged.  No surviving lead
divides any monomial of \(G|_{x=0}\).

Consequently exact division by the entire restricted degree-four/degree-five
generating layer uses zero columns.  The next lead is

```text
0951acd9e1f5
 = (02:00)(14:00)(35:01)(47:01)(56:00)(67:02),
```

which is squarefree.  This is a genuine improvement of the first cell on the
closed branch.  It does not assert that the restricted layer is a complete
Groebner basis in all later degrees.

## 5. Exact Laurent branch and the Bianchi mate

Use the notation of the cross-vertex Bianchi note.  The source S-polynomial
whose reduction is \(G\) is exactly

\[
 S=x\,\mathtt{eb}\,H_{11}-B'R_v(0).
\]

The four-corner identity gives the opposite-order expression

\[
 S=x\,\mathtt{eb}\,H_{11}
      -B R_v(1)-A'R_q(1)+A R_q(2).                     \tag{6}
\]

The difference of these two displayed expressions expands to zero before
any reduction.  Hence the Bianchi mate is not a second polynomial which can
be subtracted to improve divisibility: it is literally the same source
polynomial, and the same three original-generator reductions return the
same \(G\).

The exact \(x\)-exponent census of \(G\) is

\[
\begin{array}{c|rrr}
\nu_x\text{ of a term}&0&1&2\\ \hline
\#\text{ terms}&288&228&30.
\end{array}
\]

In particular \(\nu_x(G)=0\), so neither one nor two powers of \(x\) can be
removed while staying in the polynomial ring merely by this Bianchi rewrite.
On the Laurent branch that is not required.  Put

\[
                         \widehat G=x^{-2}G.
\]

Its distinguished pivot is

```text
0948ebef = (02:00)(13:00)(57:01)(57:12),
```

a squarefree degree-four Laurent pivot.  The \(x\)-exponents in
\(\widehat G\) are \(-2,-1,0\), with respective term counts 288, 228, 30.
The exact denominator-clearing identity is simply

\[
                         x^2\widehat G=G\in I^h.        \tag{7}
\]

Thus the repeated factor disappears from the selected pivot after
localization, although negative powers occur in the lower terms.  Equation
(7) is the precise open-branch gain; it is not a polynomial factorization of
\(G\).

## 6. Meaning and next obstruction

The first geometric split repairs the first repeated pivot in complementary
ways:

1. on \(x=0\), deletion exposes a new squarefree degree-six lead which is
   untouched by every known restricted reducer through degree five;
2. on \(x\ne0\), Laurent division removes both selected copies of \(x\) from
   the pivot and gives a squarefree degree-four pivot, with denominator two.

The Bianchi packet supplies no stronger polynomial representative.  A full
argument still needs either later branchwise Groebner cells or a well-founded
Morse/vertex-decomposition statistic proving that repeated splitting
terminates and transports the pure target.

## 7. Verification

Run

```text
python3 computations/verify_n8_chart26_geometric_vertex_split.py
```

The checker reconstructs the 546-term cell, streams all 84,005 completed
degree-five cells, performs all 653 newly exposed exact reductions, verifies
the zero-column closed reduction, expands the Bianchi mate, and freezes the
Laurent support and clearing identity by SHA-256.
