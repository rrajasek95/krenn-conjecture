# Exact seven-block rank/activity referee

Status: **the finite rank problem has been reduced exactly, and the matrix-unit subclass is closed on all six full-family representatives; the general dense-block lemma remains open.** No conjecture counterexample or full seven-block closure is claimed.

## Cap-67 determinant reduction

For each full-family representative, let `L_67` be the forbidden-response map for cap `67` and triangle `012`. The formal guard is literally

```text
L_67 vec(I3)=0.
```

Consequently `rank(L_67)<=8`. Moreover the same kernel vector `I3` evaluates to one under each of `K00,K11,K22`, so all three diagonal activity functionals are automatically nonzero on the kernel. The only remaining cap-67 activity test is

```text
rank([L_67; vec(A67)]) = rank(L_67)+1.
```

Failure is exactly `vec(A67) in Row(L_67)`; paired with the guard it also forces `trace(A67)=0`. Thus the earlier four-activity/minor obligation collapses to one rowspace incidence.

On the canonical support the three nonstructural guard equations are

```text
A06 A57^T = 0,
A17 A56^T + A57^T = 0,
A26 A57^T + A56^T = 0.
```

They imply `A56^T=-A26 A57^T`, `(I-A17 A26)A57^T=0`, `Col(A56)<=Col(A57)`, and—because `A06` is nonzero—`rank(A57)<=2`.

## Two-sandwich reduction for all 64 strata

The referee reconstructed every unresolved support directly from the sealed seven-block ledger. Each of the 64 strata has a star whose forbidden map consists of two supported products sharing one block. The deterministic census exactly matches the independently sealed two-sandwich producer: thirteen labeled patterns with counts summing to 64.

For a left-common factor the map is `K -> (U K B1, U K B2)` and has rowspace `P tensor Q`, where `P=Row(U)` and `Q=ColSpan(B1,B2)`; the right-common case is transposed. Therefore:

- `Kii` fails exactly when `e_i` belongs to both `P` and `Q`;
- the cap pairing fails exactly when its coefficient matrix lies in `P tensor Q`;
- if all four restrictions are live, four-hyperplane avoidance over `Q` produces one active clean covector.

For canonical cap `45`, star center `2`, the map factors exactly as

```text
K -> A04 K [A35^T | A56 | A57].
```

Its active-star criterion is: `P=Row(A04)` and `Q=ColSpan(A35^T,A56,A57)` are not both full, no coordinate vector lies in both, and the trace pairing is live. The guard simplifies `Q` to `Col(A35^T)+Col(A57)`.

## Exact negative control and matrix-unit closure

The sealed integer witness was independently replayed from literal entries. It satisfies the guard and pure normalization, has zero active triangles, but has exactly two active stars (`16/star2` and `45/star2`). Its six distinguished residuals are `(1,1,1,1,1,2)`, and 114 mixed amplitudes are nonzero. Hence it refutes a triangle-only lemma but not the corrected triangle-or-star-or-full-X5-residual dichotomy.

There is also a rigorous new finite closure. If every nonidentity block is an arbitrary nonzero scalar multiple of one matrix unit, the fixed matching contributes to 78 mixed words. Across the six representatives, all alternative graph matchings can contribute to at most

```text
56, 53, 52, 43, 47, 41
```

word occurrences, respectively. Each bound is below 78, so some fixed-matching mixed amplitude cannot cancel. Thus full X5 is impossible throughout this entire exact subclass, independently of scalar choices.

## Remaining dense locus

The unresolved general locus is now explicit: all fifteen named blocks are nonzero; the formal guard and every mixed-amplitude equation hold; `vec(A67)` lies in `Row(L_67)`; and every candidate triangle/star fails at least one rank/activity augmentation. Equivalently, for each chosen two-sandwich star, either its response space is full or a diagonal/cap coefficient lies in the corresponding `P tensor Q` incidence.

No pinned identity proves that this dense determinantal-amplitude locus is empty, and the matrix-unit occurrence bound does not extend to dense blocks. This is the exact first unproved subclaim. The remaining 52 non-full-family strata are reduced to the same thirteen incidence patterns, but are not closed merely by transport from the six full-family representatives.

All calculations are exact integer/rational algebra, bounded to the six representatives and 64 recorded strata. The referee independently reconstructed 2,340 symbolic triangle/star maps, replayed all 728 carriers and all `3^8` amplitudes for the negative control, used no D12 data, and ran no broad solve.
