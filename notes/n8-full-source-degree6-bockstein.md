# The degree-six frontier is a filtered-syzygy problem

## Result of the fixed-tail calculation

The exact degree-five certificate proves

\[
H_0H_1H_2\in I_{\mathrm{mix}}+J^6,
\]

where `J` is the ideal of the 240 off-support coordinates.  Streaming the
chosen rational certificate one degree farther gives an exact degree-six
tail supported on 56,502 invariant row orbits.  Closing only this support
under mixed columns whose minimum off-support degree is six gives

- 590,739 degree-six row orbits;
- 1,425,600 minimum-degree-six column orbits;
- 2,445,960 nonzero invariant matrix entries;
- column support histogram `1:969846, 3:446652, 11:93, 15:9009`;
- entry size at most 4 and row frequency between 0 and 17.

Over `GF(1009)` the resulting fixed-tail matrix has rank 579,546, left
nullity 11,193, and a nonzero reduced target with 6,254 coordinates.  There
are 1,466 especially simple residual rows of frequency zero.  This proves
that the *chosen* degree-five lift cannot be continued using only new
minimum-degree-six columns.  It does **not** obstruct a different
degree-five lift: one may add an element of the kernel of the solved
degree-at-most-five system, and its degree-six tail changes the problem.

The closure and modular census are reproduced by
`analyze_n8_full_source_pure_product_degree6_lift.py` and
`analyze_n8_full_source_pure_product_degree6_modular.py`.  Their large
pickled matrices are temporary calculation checkpoints, not certificates
tracked by git.

## First Bockstein is killed by an exact two-column relation

Let `A` be the invariant mixed-column matrix through degree five and `T` its
degree-six tail.  For the first zero-frequency degree-six row `r`, the
functional `r*T` is supported on only six of the 224,153 earlier columns.
Appending it to `A` raises the rank over `GF(1009)` from 72,904 to 72,905.
Thus `r*T` is not in the row space of `A`, so `r` is not a true dual
obstruction.  Back substitution finds a kernel vector with only two terms.

In fact the relation is integral, not merely modular.  There are canonical
invariant columns `C_+` and `C_-`, both starting in filtration degree five
and both having orbit size four, such that

\[
\operatorname{in}_{\leq5}(C_+)=
\operatorname{in}_{\leq5}(C_-),
\qquad
\operatorname{in}_6(C_+-C_-)=
\sum_{i=1}^{12}\epsilon_i m_i,
\]

with six signs `+1` and six signs `-1`.  The coefficient at the selected
zero-frequency row is `+1`, so changing the degree-five lift by this exact
syzygy removes that apparent obstruction.  Only two of the twelve tail rows
lie outside the fixed-tail closure; closing them adds just four rows and
three minimum-degree-six columns.  The exact two-column identity is checked
without cached matrices or modular arithmetic by
`verify_n8_full_source_degree6_sparse_bockstein.py`.

## Adaptive Bockstein column generation

This suggests a substantially faster proof search than constructing the
full coupled degree-six Macaulay matrix.

1. Maintain a row set closed under the leading degree-six matrix `B`.
2. Choose a dual functional `lambda` that violates the current target.
3. Stream the sparse functional `lambda*T` on the already-built matrix `A`.
4. If `[lambda*T]` is nonzero modulo the row space of `A`, extract
   `z in ker(A)` with `lambda*T*z != 0`; change the lower lift by `z`, adjoin
   only the support of `T*z`, close it under `B`, and repeat.
5. If `lambda*T = mu*A`, then and only then test the genuine coupled pairing
   `lambda*c - mu*b`.

This is the Schur-complement calculation for the filtered system, performed
by dual-guided column generation.  It terminates because the degree-six row
universe is finite.  More importantly, it exposes the small exchange
relations that a conceptual proof should classify: the first apparent
obstruction is killed by a two-column move, whereas the raw degree-six
matrix has more than a million columns.

The likely missing lemma is therefore not another large rank computation.
It is a structural statement that these local exchange syzygies generate
enough of the lower-degree kernel tails to remove every associated-graded
obstruction (or else isolate the first surviving coupled dual).  In
spectral-sequence language, the fixed-tail cokernel is only the `E_1` page;
the sparse relations compute its differentials.

## Exact endpoint: exponent-one nonmembership

The adaptive calculation eventually isolates a surviving coupled dual.  To
avoid cycling, every degree-six row of zero leading frequency is kept as a
cumulative constraint, including rows whose current residual is already
zero.  Dual separation then adds only columns on which the current dual has
nonzero pairing.  After eight separation rounds the final modular dual has
support on 80 lower rows and 20 degree-six rows, and exhaustive separation
finds no omitted column.

The modular coefficients lift canonically to the half-integers

\[
\{-2,-3/2,-1,-1/2,1/2,1,3/2,2\}.
\]

Over `Q`, the resulting functional has the following properties.

- Its 20 degree-six rows have no incident mixed column of minimum degree
  six, so it annihilates the entire leading block `B`.
- The union of rows in its support has 180 incident canonical mixed columns,
  or 706 actual columns after orbit expansion.
- After dividing invariant row weights by their row-orbit sizes, it
  annihilates every one of those 706 actual columns exactly.  Every other
  column pairs to zero trivially because it is not incident to the support.
- Its exact pairing with `H_0 H_1 H_2` is `-1`.

Thus

\[
H_0H_1H_2\notin I_{\mathrm{mix}}
\]

at exponent one.  The frozen certificate and independent exact replay are
`n8_full_source_degree6_exact_dual.json` and
`verify_n8_full_source_degree6_exact_dual.py`.

This is deliberately **not** stated as a counterexample to the localized
Krenn claim.  The chart permits multiplication by support monomials (or,
equivalently, sets the twelve support variables to units).  Such Laurent
translations change the balanced port multidegree and are absent from this
degree-12 Macaulay component.  The exact dual therefore proves unsaturated
exponent-one nonmembership and identifies a critical class; the next test is
whether that class survives in the normalized full chart with all twelve
support variables set to one.

The census also suggests a conceptual model.  Of the original 1,425,600
leading columns, 969,846 have singleton support.  Choosing unit columns as a
lexicographic matching gives an algebraic discrete-Morse contraction;
alternative columns create the two-column diamonds and longer gradient paths
seen by the Bockstein repairs.  The exact 100-row dual is a small critical
class left after those cancellations, not a mysterious vector arising only
from a million-column rank computation.

## What localization does to the critical class

Dropping the twelve support variables sends the 100 balanced dual rows to
100 distinct monomials in the 240 normalized variables.  The target pairing
is still `-1`, but the annihilation property collapses:

- all 6,558 mixed words give 688,059 distinct normalized generator terms;
- the critical support has 1,091 incident normalized column orbits;
- 903 of those columns pair nontrivially with the old dual;
- the restricted 100-row matrix has 889 singleton columns and full rank.

More concretely, six invariant columns with coefficients `+/-1/2` have
critical projection exactly equal to the constant monomial.  Their full
image is the constant plus a positive-degree tail on 564 invariant monomial
orbits (2,240 actual monomials), in degrees two through seven.  This exact
calculation is frozen in `verify_n8_normalized_critical_contraction.py`.

Thus the exponent-one obstruction is genuinely a port-grading artifact and
does not survive the first localized contraction.  The remaining issue is
also sharply identified: because two normalized mixed generators have
constant terms, the ideal is inhomogeneous and naive degree truncation can
hide an infinite degree-raising tail.  A localized proof now needs either an
explicit finite certificate or a well-founded graded-lex/discrete-Morse
orientation showing that the 564-orbit tail reduces to zero.  This is a much
smaller and more structural problem than the original full Macaulay rank.
