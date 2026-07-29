# Common-factor transfer from a mixed binomial to a pure zero

## Lemma

Work in a binomial support chart and let every selected aggregate cell have a
nonzero complex weight.  Fix a palette colour `a`.  Suppose the pure-`a`
fibre consists of exactly two matching monomials

\[
  P=g u,\qquad Q=g v,
\]

where `g,u,v` are Laurent monomials.  Suppose some mixed colouring has exactly
two matching monomials

\[
  R=h u,\qquad T=h v

\]

with the same ordered pair `u,v` after common factors are canceled.  Then the
support cannot realize the monochromatic tensor.

Indeed, the mixed coefficient equation is

\[
  0=R+T=h(u+v).

\]

Every selected cell weight is nonzero, hence `h` is nonzero and `u+v=0`.
The pure coefficient is therefore

\[
  P+Q=g(u+v)=0,

\]

whereas monochromaticity requires it to equal one.  Equivalently, the mixed
and pure exponent-difference rows are identical (up to sign); the equation
`x^d=-1` makes the two pure terms opposite.

The same proof works whenever the two exponent-difference rows agree, without
requiring literal monomial factorizations to be displayed.

## The n=8 representative

For the captured representative, the mixed colouring is `12121212`.  Its two
terms are

\[
\begin{aligned}
R&=(02;11)(15;22)(37;22)(46;11),\\
T&=(04;11)(15;22)(26;11)(37;22),
\end{aligned}
\]

while the exact pure-colour-1 fibre is

\[
\begin{aligned}
P&=(02;11)(13;11)(46;11)(57;11),\\
Q&=(04;11)(13;11)(26;11)(57;11).
\end{aligned}
\]

Thus `h=(15;22)(37;22)`, `g=(13;11)(57;11)`,
`u=(02;11)(46;11)`, and `v=(04;11)(26;11)`.

Under arbitrary vertex and global colour relabeling this incidence schema has
7,560 distinct images.  Each gives a sound hybrid clause with six negated
support literals, the two negated present pure-term indicators, and the 103
positive absent pure-term indicators.  The exact orbit and exponent identity
are checked independently by
`computations/verify_n8_toric_one_row_pure_zero_orbit.py`.

## Complete fixed-target classification at n=8

The single orbit above is only a small part of the one-row family relevant to
a search with prescribed pure target matchings.  Fix a pure colour `a`, let
`P` be its forced target matching, and suppose the exact pure fibre is
`{P,Q}`.  If a mixed row equals the pure exponent-difference row up to sign,
orient its two matchings `R,T` so that

\[
 R-T=P-Q.
\]

Equality of aggregate-cell coordinates gives

\[
 R\setminus T=P\setminus Q,\qquad
 T\setminus R=Q\setminus P.
\]

Every vertex on those alternating-cycle edges therefore has colour `a` in
the mixed colouring.  The remaining vertices are precisely those covered by
the common pure edges $P \cap Q$; on them `R` and `T` share an arbitrary
perfect matching, and their vertex colours are arbitrary except that they
cannot all equal `a`.  Conversely, every choice of this form gives the same
exponent-difference row and hence the common-factor obstruction.  This proves
completeness, not merely soundness, of the enumeration.

Relative to a fixed perfect matching on eight vertices, 32 other matchings
share one edge and 12 share two edges.  In the first case the two common
vertices have one possible shared mixed matching and `3^2-1=8` nonconstant
colour assignments.  In the second case the four common vertices have three
possible shared matchings and `3^4-1=80` assignments.  Thus there are

\[
 3\bigl(32(3^2-1)+12\cdot3(3^4-1)\bigr)=9,408
\]

two-term schemas over the three pure colours.  Of these, 8,640 have six-cell
guards and 768 have seven-cell guards.  Only 144 belong to the previously
preloaded 7,560-element global orbit, so 9,264 of these pair schemas are new.

This also classifies larger pure fibres killed by one mixed row.  Modulo a
fixed matching-difference row, pure matching monomials occur in disjoint
opposite-sign pairs: a difference of two squarefree matching exponent vectors
cannot be a multiple of the row of absolute value greater than one.  For a
six-cycle difference there is only the target's
pair.  For a four-cycle difference there are three pairs, corresponding to
the three perfect matchings on the four complementary vertices.  A pure
polynomial with coefficient one is identically zero under this row exactly
when its selected terms are a union of complete pairs.  Since the forced
target belongs to one distinguished pair, the other two pairs may be included
independently.  Thus each four-cycle guard permits exact pure fibres of sizes
2, 4, 4, or 6.

The resulting complete one-row family has 35,328 schemas: 9,408 with two pure
terms, 17,280 with four, and 8,640 with six.  Their guard-size distribution is
34,560 of size six and 768 of size seven.  After removing forced target cells
all remain distinct, with reduced-guard counts 96 of size two, 3,840 of size
three, and 31,392 of size four.

Only 204 distinct exact pure-fibre assignments occur (132 of size two and 36
each of sizes four and six).  Production gives each one a shared existential
trigger: a single long clause forces the trigger when that exact fibre occurs,
and each associated schema is `guard -> not trigger`.  Eliminating the trigger
recovers every original long clause exactly.  Hence the 35,328 guard clauses
have lengths only 3--5; compared with direct term-status clauses this removes
3,617,364 literal occurrences.

`computations/verify_n8_toric_all_target_one_row.py` first inverts the pair
enumeration from mixed matchings, then independently reconstructs all pure
quotient pairs from each row signature.  It checks exact equality with both
production generators and all counts above.  The generalized trigger
projection is exhausted in `verify_n8_toric_zero_product_nogood.py`.

## Scope of a possible hitting statement

A useful structural theorem would say that prescribed n=8 target matchings,
the zero-or-two mixed-fibre condition, and Laurent phase consistency force one
of these common-factor configurations.  The current SAT/CEGAR test installs
the complete 35,328-element target-specific family and then searches for a
phase-consistent support.  A surviving support disproves that proposed hitting
statement; an UNSAT certificate would prove it only for the stated target
orbit and cell cap unless those restrictions were separately removed.
