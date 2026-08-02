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
