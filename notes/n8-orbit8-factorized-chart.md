# The factorized 36-cell orbit-8 chart

This note records an exact characteristic-zero obstruction on the most
structured completion presently found above the pairwise-Hamiltonian
orbit-8 boundary.  It is a chart theorem, not a proof of Krenn's full
conjecture.  The solver-independent audit is

```text
computations/verify_n8_orbit8_factorized_chart.py
```

and the reusable finite branch engine is

```text
computations/factorized_laurent_branches.py
```

## 1. Support

Start with the twelve diagonal cells in the three prescribed matchings of
`sparse_seed(orbit=8)`.  Add the following twelve cells:

```text
26;21 26;22 27;21
36;12 37;11 37;12
46;21 47;21 47;22
56;11 56;12 57;12
```

The resulting 24-cell support has 22 mixed binomial fibres and twelve odd
unit Laurent triangles.  An exact minimum-cover calculation shows that at
least four further cells are needed to break those twelve triangles.  The
balanced minimum cover used here is

```text
04;11 05;22 12;11 13;22.
```

Finally add

```text
02;21 03;12 04;21 05;12
12;21 13;12 14;21 15;12.
```

This gives 36 cells.  Direct enumeration of all 105 perfect matchings and
all `3^8` colourings gives pure fibre sizes `(1,4,4)` and the complete mixed
histogram

\[
  \#\{|F_c|=2\}=16,\qquad \#\{|F_c|=4\}=94.
\]

Thus there are no mixed singletons.

## 2. Exact Laurent quotient

The sixteen mixed binomials have thirteen independent signed HNF rows and
are consistent over the complex torus.  Reduce the remaining 94 mixed
four-term polynomials in this signed quotient.  Thirty-two vanish
identically.  Each of the other 62 has four Laurent classes and factors
exactly as a Laurent monomial times two signed binomials.  Their coefficient
patterns are

\[
  30\text{ copies of }(-1,-1,-1,-1),\qquad
  32\text{ copies of }(-1,-1,1,1).
\]

After deduplication there are sixteen possible binomial factors, arranged
as opposite sign choices for eight exponent vectors:

\[
 L_i^+,L_i^-\ (1\le i\le4),\qquad
 R_j^+,R_j^-\ (1\le j\le4).
\]

Here `+` means `x^d=+1` and `-` means `x^d=-1` for the same normalized
exponent `d`.  The 62 factorizations reduce to exactly the following 32
distinct Boolean clauses:

\[
 (L_i^+\lor R_j^+),\qquad (L_i^-\lor R_j^-)
 \quad(1\le i,j\le4).                                  \tag{1}
\]

Every zero of all mixed coefficients must choose at least one zero factor
in every clause of (1).  Opposite signs for the same exponent are Laurent
inconsistent.  Exact branch enumeration has only four minimal covers:
two contain an immediate opposite-sign inconsistency, while the two
consistent covers are

\[
 \{L_1^+,\ldots,L_4^+,R_1^-,\ldots,R_4^-\},\qquad
 \{L_1^-,\ldots,L_4^-,R_1^+,\ldots,R_4^+\}.             \tag{2}
\]

The signed HNF is consistent on both branches in (2).  In each quotient,
however, the complete pure-colour-1 sum and the complete pure-colour-2 sum
both reduce identically to zero.  Hence neither branch can realize a
nonzero target coefficient.  Adding more zero factors cannot repair an
identically zero pure polynomial, so the four minimal covers exhaust all
branches.

Consequently the 36-cell support has no nonzero complex weighting whose
mixed coefficients all vanish and whose three pure coefficients are all
nonzero.

## 3. Audit

Run

```sh
.venv/bin/python computations/verify_n8_orbit8_factorized_chart.py
```

The checker reconstructs the support and every fibre, verifies the initial
signed HNF, rederives all 62 rectangle factorizations, constructs the sixteen
factor relations and 32 clauses, and exhausts the four branches with exact
integer HNF and group-algebra reductions.  Its expected terminal line is

```text
PASS cells=36 mixed={2:16,4:94} residuals=62 factors=16 clauses=32 branches=4 inconsistent=2 pure_zero=2
```

