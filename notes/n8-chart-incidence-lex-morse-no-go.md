# The 31-chart support incidence has seven lex-critical types

## Exact first-layer incidence

The 31 (S_8\times S_3) pure target-row orbits meet exactly 31 mixed
support-column orbits.  A row--column incidence means that a mixed support
one-factor can be removed from the target monomial to form that Macaulay
column.  Equivalently, filling the column's eight holes by a vertex perfect
matching recovers the target row.  The resulting (31\times31) integer
matrix has 111 nonzero entries.

This finite relation does not admit a matching with only charts 25 and 26
critical.  An exact Hall witness consists of the 13 row types

\[
 7,8,16,17,18,20,21,23,25,26,27,28,29
\]

and only the eight neighboring column types

\[
 13,14,17,22,24,25,27,30.
\]

Its deficiency is five, and the maximum ordinary support matching has size
26.  Thus at least five chart rows remain unmatched before any acyclicity
condition is imposed.  This refutes the proposed two-critical-type matching
independently of the choice of lexicographic order.

## Naive lex matching is cyclic

Order chart rows by their frozen canonical indices and support columns by
their canonical port-graph keys.  Matching each row to its smallest unused
incident column produces an alternating directed cycle

\[
 R_2\longrightarrow C_2\longrightarrow R_4
 \longrightarrow C_7\longrightarrow R_2.
\]

Hence raw greedy support matching is not a discrete-Morse contraction.

## Acyclic repaired-column replacement

The useful replacement is algebraic.  Process columns in canonical order;
whenever two columns have the same leading row, subtract the normalized
earlier column.  Every one of the 118 repairs strictly raises the leading
chart index.  After normalizing nonzero pivots, this gives a unit matching
over \(\mathbb Q\) whose gradient-path tails are supported strictly above
their matched rows.  It is therefore acyclic by the lex pivot statistic.

The exact rank is 24.  The unmatched row types are

\[
                 \boxed{25,26,27,28,29,30,31},
\]

and the zero repaired-column types are

\[
                 18,19,21,23,26,29,31.
\]

The 24 normalized pivot columns have 70 gradient-tail terms in total; the
checker freezes all rational coefficients and original-column provenance.
The extra critical charts have the following support types:

* chart 27: three mixed factors of type ((4,2,2)) with Hamiltonian
  complementary cycle;
* chart 28: six ((4,4)) Hamiltonian factors;
* chart 29: four ((4,4)) Hamiltonian factors;
* charts 30 and 31: mixtures of Hamiltonian and (4+4) complementary
  two-factors.

Thus charts 25/26 remain the uniquely *minimally coupled* charts, but they
are not the complete critical set of the first support-incidence
contraction.  Any two-chart proof needs five additional algebraic repairs
or a later filtered differential that kills charts 27--31.

## Laurent stability and scope

The pivot statistic uses only canonical target and support-column orbit
keys.  Multiplying a localized column by a support Laurent monomial
translates every exponent by the same unit and leaves this finite incidence
order unchanged.  This is the precise stability available for chartwise
Laurent contractions.

The statement is only the finite (n=8), first-layer
(S_8\times S_3)-orbit census.  It is not a uniform classification of
uniquely edge-coloured cubic graphs; infinite support families rule out such
a naive extrapolation.

## Reproduction

```sh
python3 computations/verify_n8_chart_incidence_lex_morse.py
```

All incidence counts, Hall data, rational repairs, zero-column syzygies,
and gradient tails are replayed exactly.
