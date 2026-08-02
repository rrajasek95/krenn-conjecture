# The first nonsquarefree cell selects an exact geometric vertex split

Research target only.  The complete degree-five Buchberger layer and first
degree-six compatibility cell are exact.  This note records the rigorous
two-branch reduction suggested by the repeated coordinate; it does not claim
that either branch has already been closed.

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

## 4. Immediate exact tests

Let \(G\) be the frozen 546-term degree-six compatibility polynomial.

1. Reduce \(G|_{x=0}\) against the restrictions of the complete degree-four
   and degree-five basis.  Freeze its new leading monomial and whether it is
   squarefree.
2. In the Laurent branch, divide \(G\) by the largest common power of \(x\)
   allowed termwise after combining it with its opposite-order Bianchi mate;
   freeze the cleared polynomial identity.
3. Retest the homogenized pure target \(F^h\) separately in
   \(I^h+(x)\) and \(I^h:x^\infty\).  A bounded result on only one branch is
   not a chart certificate.

These tests use the actual source polynomials and preserve the distinction
between ideal membership, radical membership, and localization.
