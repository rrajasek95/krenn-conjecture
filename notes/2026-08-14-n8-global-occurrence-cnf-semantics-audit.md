# Exact semantic audit of the global N=8 occurrence CNF

## Verdict

At source SHA-256
`0b8ca774d5a2dcf6571d9fd29a84e7cc0938331117351cb23a187be6629f80b7`,
`computations/search_n8_global_occurrence_cnf.py` is an exact Boolean encoding
of the nonsymmetric core of the literal QF_LIA occurrence model.  I found no
overconstraint in the support, nonanchor, coordinate-anchor, pure-row, or
mixed-no-singleton clauses.

The qualification “nonsymmetric core” is important.  With no degree sequence
argument the CNF contains no degree variables or degree-order clauses, and it
also omits the QF_LIA model's residual colour-1/colour-2 lexicographic
inequality in the pair-target chart.  Thus the raw CNF is a relaxation of the
symmetry-reduced QF_LIA formula, not literally the same formula.  This is safe
for an UNSAT proof and cannot manufacture UNSAT.

The independent replay is
`computations/verify_n8_global_occurrence_cnf_semantics_audit.py`.
It pins the constants, `CNF`, `occurrence_inventory`, and `build_instance`
source to semantic SHA-256
`5c72f7d2ada2214737e53bef97712ba718cce3b124d35f5731ddd17b8e81b97c`;
changes confined to CLI output do not invalidate the semantic audit.

## Clause-by-clause comparison

For each edge (e), the three variables (y_{e,c}) have the same meaning as
the QF_LIA Boolean support bits.

* `live_e` is biconditional to the disjunction of the three support bits.  The
  exact-support and minimum-support automata therefore count live edges, not
  coloured entries.  The latter is the same saturated counter used for the
  nonanchor lower bound and implements support at least the requested value.
* Each pair auxiliary is biconditional to (y_{e,a}\wedge y_{e,b}), and
  `nonanchor_e` is biconditional to the disjunction of the three pairs.  It is
  true exactly when the support of (e) has size at least two.  The saturated
  automaton implements “at least four,” including supports of size three.
* `coordinate_e_c` has all four directions needed for
  (y_{e,c}\wedge\neg y_{e,c'}\wedge\neg y_{e,c''}).  The 24 vertex-colour
  cover clauses consequently require literal singleton-support edges; a
  multicolour edge cannot masquerade as an anchor.
* The independently rebuilt inventory agrees exactly: 105 perfect matchings,
  8,505 decorated matching rows, and 1,641 words.  The word row-count
  histogram is

  ```text
  3:1260, 9:210, 15:168, 105:3.
  ```

  Every occurrence variable is biconditional to its four selected edge-colour
  bits.  The three pure clauses say that at least one of the 105 monochromatic
  matching occurrences is present.
* For a mixed word with occurrence variables (o_1,\ldots,o_k), the clauses
  (o_i\Rightarrow\bigvee_{j\ne i}o_j) exclude exactly multiplicity one:
  zero satisfies them; one violates the clause belonging to its unique true
  occurrence; two or more satisfy all of them.  Since the occurrence
  auxiliaries are biconditionals, this is neither an upper nor a lower
  relaxation of the QF_LIA sum constraint.
* The exact and saturated counters use one-hot states at every layer.  For
  each current one-hot state and input bit, one of the two transition clauses
  forces the unique correct next state.  The terminal unit clause therefore
  has exactly the intended equality or lower-bound semantics.

The executable audit assigns every one of the 9,383 variables its direct
semantic value and replays all 57,011 clauses.  It also checks twelve seeded
support assignments against an independently computed defect set.  Any
Tseitin implication missing in either direction shows up either as a failed
definition clause or as a mismatch between violated top-level clause families
and literal defects.

## Positive controls

Two explicit relaxed SAT witnesses make the audit sensitive to accidental
overconstraint.

1. Give every edge of (K_8) support \(\{0,1,2\}\), use target chart 012,
   support 28, and nonanchor lower bound four.  It satisfies the target,
  support, nonanchor, all three pure, and every mixed-no-singleton clause.  It
  violates exactly the 24 coordinate-cover clauses.  Deleting only those 24
   clauses makes the intended full variable assignment a CNF witness, both
   for exact support 28 and for minimum support 18.
2. The following 16-edge support uses three disjoint singleton perfect
   matchings and four two-colour edges:

   ```text
   01:12  02:01  03:01  04:01  05:2  06:1  07:0  12:2
   14:1   16:0   23:1   25:0   34:0  37:2  46:2  57:1
   ```

   Its degree sequence is `(7,4,4,4,4,3,3,3)`.  It satisfies the pair target,
   exact support and degree, the four-nonanchor bound, all 24 coordinate
   covers, and all three pure clauses.  It violates exactly 14 mixed
   no-singleton clauses.  Deleting only those clauses makes the intended
   assignment a CNF witness.  Swapping colours 1 and 2 gives the same result,
   confirming that no hidden residual-colour lex condition entered the CNF.

These are controls for the translation, not counterexamples to the full
occurrence system.

## Degree branches and unlabeled symmetry

An unbranched instance has no degree restriction at all.  Passing an exact
degree sequence creates eight independent counting automata; inspection and
the executable audit show that no clause contains state variables for two
different vertices.  In particular, the CNF does not secretly encode
`d0 >= d1` or `d2 >= ... >= d7`.

The external list of 182 support-22 degree sequences is nonetheless
exhaustive after the genuine occurrence-level stabilizer

\[
S_{\{0,1\}}\times S_{\{2,\ldots,7\}}.
\]

Swapping target endpoints preserves the undirected target edge and all
occurrence clauses; permuting vertices 2 through 7 does likewise.  Therefore
every labelled support has a representative whose first two degrees and last
six degrees are separately nonincreasing.  Fixing one such degree tuple still
searches all labelled graph structures with those per-vertex degrees; it is a
degree-orbit partition, not a graph-isomorphism quotient.

There is harmless redundancy in the 182 jobs.  Exhaustively choosing the six
missing edges of a 22-edge support, while retaining edge 01, gives only 121
realizable canonical degree tuples of minimum degree at least three.  Thus 61
of the declared tuples are structurally empty even before colours are added.
The relationship is

```text
realizable 121  ⊆  declared 182; omitted realizable tuples 0.
```

The minimum-degree-three cutoff is itself forced by the coordinate clauses:
at a vertex, the three required singleton colours must occur on three distinct
incident edges.  Hence it removes no model of the literal occurrence system.

This symmetry statement is limited to the occurrence model.  A later
source-labelled or directed-cap predicate must be checked for the same
stabilizer before reusing the degree quotient.

## Reproduction

```bash
python3 computations/verify_n8_global_occurrence_cnf_semantics_audit.py
python3 -O computations/verify_n8_global_occurrence_cnf_semantics_audit.py
python3 -I computations/verify_n8_global_occurrence_cnf_semantics_audit.py
```

All three modes must print `CNF semantic equivalence: PASS` and the audited
semantic digest above.
