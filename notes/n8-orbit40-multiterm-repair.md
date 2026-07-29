# The orbit-40 multi-term repair chart

This note records an exact attempt to repair the 28-cell orbit-40 monomial
boundary without imposing the artificial condition that every nonempty mixed
fibre be binomial.  The accompanying program is

```
computations/search_n8_orbit40_multiterm_completion.py
```

All statements below concern aggregate cells `uv;ab` with nonzero complex
weights.  A selected support is therefore a torus chart; no sign or
unit-weight restriction is made.

## 1. The 30-cell repaired seed

Let `S0` be the diagonal orbit-40 support from
`verify_n8_toric_orbit40_boundary.py`, and put

\[
 S_+=S_0\cup\{02;00,13;00\}.
\]

Direct enumeration of the 105 perfect matchings and all `3^8` colourings
gives

\[
 \#S_+=30,
 \qquad
 \#\{\hbox{mixed fibres of sizes }1,2,3\}=(2,51,1).
\]

Thus the two new cells do turn one old binomial into a trinomial, but they do
not remove the Laurent obstruction.  In fact the 51 remaining binomials
contain 136 unit-coefficient odd triangles.  One especially small certificate
uses the following three complete fibres (common nonzero factors have already
been cancelled):

\[
\begin{array}{c|c}
00001010&x_{05}^{00}x_{27}^{00}+x_{07}^{00}x_{25}^{00}=0,\\
00021012&x_{01}^{00}x_{25}^{00}+x_{05}^{00}x_{12}^{00}=0,\\
00021210&x_{01}^{00}x_{27}^{00}+x_{07}^{00}x_{12}^{00}=0.
\end{array}
\]

The first two equations imply

\[
 \frac{x_{01}^{00}x_{27}^{00}}
      {x_{07}^{00}x_{12}^{00}}=+1,
\]

whereas the third says that the same ratio is `-1`.  Consequently `S+`
itself admits no nonzero complex weighting.  This certificate uses only six
variable cells; the factors `13;00`, `37;22`, `35;22`, and `46;11` cancelled
from the displayed complete matching coefficients.

## 2. Sound unrestricted-multiterm completion SAT

The completion search has one Boolean variable `X_e` for every one of the 252
aggregate cells, fixes every cell in `S+`, and optionally imposes a cardinality
cap.  It never imposes an upper bound on the size of a mixed fibre.

For a currently singleton term `M` in colouring `c`, it adds selectors
`s_N`, one for every other perfect matching `N`, with

\[
 s_N\Longrightarrow X_e\quad(e\in N\setminus M),
 \qquad
 \bigwedge_{e\in M}X_e\Longrightarrow\bigvee_{N\ne M}s_N.
\]

Hence, whenever `M` remains supported, some genuine distinct mate is
supported.  This is an equisatisfiable encoding in the support variables of
the necessary no-singleton condition.

There is a second, equally important lazy constraint.  Suppose currently
binomial fibres `c_i` have exponent differences `d_i` and an exact odd
integer dependency

\[
 \sum_i a_i d_i=0,
 \qquad \sum_i a_i\equiv1\pmod2.
\]

Their equations `x^{d_i}=-1` are inconsistent.  A future support can escape
only by deleting one of the guarded pair terms or by adding a genuine third
term to at least one of those fibres.  The seed is fixed, so only the latter
is possible for the 136 seed triangles.  The program encodes exactly this
disjunction with one-way term selectors.  It re-enumerates all fibres after
every SAT model and checks the full integer Laurent lattice, so a reported
survivor has neither a singleton nor an inconsistent binomial subsystem.

The four vertex permutations

```
01234567, 10325476, 23016745, 32107654
```

are precisely the seed-preserving subgroup used for optional lex leaders.
Every completion orbit has a lexicographically least representative, so this
does not remove any support orbit.

## 3. Certified sparse obstruction

With at most 38 total cells, even the weaker no-singleton condition is
impossible.  The generated formula has 61,900 variables and 215,846 clauses.

The CNF includes only the fixed seed, the at-most-38 cardinality encoding,
three sound lex leaders, and 576 witnessed singleton-mate gadgets.  Thus its
UNSAT conclusion proves that every no-singleton extension of `S+` uses at
least 39 cells.  A separate run at cap 39 is also UNSAT, although the smaller
cap-38 instance is the one for which the portable proof trace was retained.

The initial CaDiCaL proof export omitted the terminal contradiction, so its
raw trace is not claimed as a portable certificate.  A complete-trace export
must pass `verify_drup_certificate.py` before this bounded UNSAT result is
called independently certified.

## 4. First no-singleton completion and its exact failure

The first directed sparse completion found has 46 cells.  Besides `S+`, its
cells are

```
13;01  13;02  13;10  13;12
15;01  15;11  17;21  26;21
35;02  35;12  37;01  37;02
37;11  37;12  37;21  57;12.
```

Its three pure fibre sizes are `(26,2,4)`, and its mixed fibre census is

\[
 \#\{\hbox{sizes }2,4\}=(224,19).
\]

So this is a genuine no-singleton completion, not a boundary artefact.
Nevertheless its 224 exact binomials have 7,968 unit odd triangles.  It is
therefore excluded over the full complex torus before the nineteen
four-term equations or the pure sums need to be considered.

Moreover, if these 46 cells are fixed, breaking just the 136 original seed
triangles requires at least seven additional cells.  The exact core formula
is UNSAT with four additional cells (cap 50); a separate focused enumeration
finds no circuit cover of sizes one through six and finds one at size seven.
One size-seven cover creates 79 new singleton fibres and still leaves 790
unit odd triangles, illustrating why merely hitting the original circuits is
not enough.

The shared-witness cap-50 core formula has 6,226 variables and 19,709 clauses.
A complete Glucose 4.2 trace has 4,677 deletion-free DRUP additions and passes the
independent unit-propagation checker with both Glucose 4.2 and CaDiCaL 1.9.5,
including the terminal empty clause:

```
computations/cert_n8_orbit40_base46_cap50_shared_g42.cnf
computations/cert_n8_orbit40_base46_cap50_shared_g42.drup
```

The earlier incomplete CaDiCaL exports have an `.incomplete` suffix and are
not certificates.  The independent structural checker
`computations/verify_n8_orbit40_multiterm_repair.py` additionally verifies the
displayed seed triangle, both fibre censuses, all 7,968 base triangles, the
exact minimum-seven focused cover, and the residual 790 triangles after the
displayed cover.

The portable proof is checked by

```
.venv/bin/python computations/verify_drup_certificate.py \
  computations/cert_n8_orbit40_base46_cap50_shared_g42.cnf \
  computations/cert_n8_orbit40_base46_cap50_shared_g42.drup \
  --solver glucose42
```

The stronger directed completion formula is UNSAT through cap 54: after the
136 seed-core gadgets are preloaded, only 173 singleton-mate gadgets are
needed before contradiction.  That final instance has 61,354 variables and
201,241 clauses.  Therefore no extension of the displayed base 46 by at most
eight cells can both avoid mixed singleton fibres and break even the original
seed triangles.  This is still a bounded chart statement, not a global
obstruction to denser repairs.

## 5. Quotient reduction for a genuine survivor

For every support that survives the preceding tests, the program forms the
row-HNF of the lattice generated by `(d_i,1)` and `(0,2)`.  Each monomial in
every remaining multi-term or pure fibre is reduced to its exact class in

\[
 \mathbb Z^{252}\oplus\mathbb Z\varepsilon
 \big/\langle(d_i,1),(0,2)\rangle.
\]

Terms in the same exponent class and opposite epsilon class are combined
with opposite signs.  The output reports every nonzero reduced multi-term
polynomial and the reduced support size of all three pure sums.  Thus a
future `SURVIVOR` line is already the requested exact binomial-Laurent
reduction; only the residual quotient equations, and then an independent
coefficient audit, remain.

At present no quotient-consistent survivor has appeared on this chart.  The
results above are therefore a certified sparse obstruction and a warning
against treating the two-cell repair as an algebraic completion, not a
counterexample to Krenn's conjecture.
