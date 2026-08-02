# The complete squarefree degree-five Buchberger layer in chart 26

## Exact result

Homogenize every normalized chart-26 mixed generator to degree four with
(t) last in the term order.  The 6,558 original leading monomials are
distinct squarefree (y)-monomials of degree four.  The product criterion
removes every disjoint pair.  An original-original S-pair has LCM degree
five exactly when its two leading matchings share three variables.

There are exactly 84,005 such labeled pairs.  Exhaustive exact expansion
splits them into

\[
 44{,}028\text{ Hamming-one star transports},\qquad
 39{,}977\text{ Hamming-two direct-double transports}.
\]

The two universal Laplace identities are derived in
`hafnian-star-minor-buchberger-identity.md`.  Every one of the 84,005 chart
instances has 180 terms, all coefficients are (pm1), and every monomial
is squarefree.  None of the 15,120,900 aggregate terms is divisible by an
original degree-four leading monomial.

The new leading monomials are also exceptionally clean:

* all 84,005 are distinct squarefree monomials of degree five;
* no new leading monomial occurs anywhere in the support of a different
  degree-five cell.

Consequently the cells are mutually reduced at this degree and may be
adjoined in any order.  They finish the entire homogeneous degree-five
Buchberger layer.  No new pair involving an adjoined cell can still have
total degree five: an old degree-four lead would have to divide its reduced
degree-five lead, or two distinct degree-five leads would have to coincide.

The aggregate off-support-degree census is

\[
\begin{array}{c|rrrrr}
\deg_y&1&2&3&4&5\\ \hline
\#&47&7{,}614&197{,}492&2{,}456{,}787&12{,}458{,}960.
\end{array}
\]

There are 39,703 source-pair representatives under the four-element chart
support stabilizer.  Because the lexicographic leading-term choice itself
is not invariant, this is a classification of the source pairs, while the
84,005-cell calculation is the actual term-order audit.

## Meaning for radicality

The first extension of the initial ideal remains squarefree on every
minimal generator through degree five.  This is strong evidence for a
determinantal straightening law: Hamming-one cells are star minors times
smaller hafnians, and Hamming-two cells are their direct-double companions.

It is not yet a radicality proof.  Cross-word and cross-vertex critical
pairs begin in degree six.  They must be reduced against this complete
84,005-cell layer before deciding whether a repeated-variable leading term
survives.  The earlier provisional degree-six cell intentionally predates
this completion and is not claimed to be globally minimal.

## Verification

Run

```text
python3 computations/verify_n8_chart26_complete_degree5_buchberger.py
```

The checker reconstructs every generator and all 84,005 labeled cells.  It
performs one pass for exact expansion, original reduction, squarefreeness,
and distinct leading terms, followed by an independent second pass for all
cross-leading incidences.  A streaming SHA-256 freezes the complete ordered
cell expansion without storing a 15-million-term certificate file.
