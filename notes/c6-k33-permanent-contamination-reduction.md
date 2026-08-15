# Tail-free `C6` contamination reduces to one six-term permanent

## Result

The permanent-triangle recurrence of `eaff4ab` has an exact finite
contamination dichotomy.

* Every perfect-matching fine outside its `K3,3` uses one cross-shore edge
  and one edge internal to each shore.  It shares that cross edge with
  exactly two `K3,3` permutation fines, and each pair is a literal `C4`
  move with the cross edge retained as spectator tail.
* A genuinely tail-free three-channel family inside the `K3,3` is one of
  its two parity factorisations.  In any fixed endpoint-coloured word, its
  three occurrences cover all nine decorated cross-edge cells.  Occurrence
  closure therefore jumps immediately to all six permutation fines.

Thus there is no same-word three-, four-, or five-term tail-free
intermediate after a live factor triple.  The sole reduced coefficient
branch is the full six-term `3x3` permanent.

That branch is not a unit by coefficient algebra alone.  The all-nonzero
matrix

\[
 \begin{pmatrix}-2&1&1\\1&1&1\\1&1&1\end{pmatrix}           \tag{1}
\]

has permanent zero and all nine complementary `2x2` permanents nonzero.
Consequently the reduction returns the proof to pure normalization and mate
recursion; it does not itself exclude the full permanent guard.

The companion shared-star audit in `64e98dc` realizes the same permanent
fibre as a literal fifteen-cell physical guard, verifies all response-slice
rank identities, and shows that every minimum pure-witness completion exports
singleton debt.  The present note supplies the matching-topology interface
to that coefficient guard; it does not duplicate its cap census.

The exact checker is
`computations/verify_c6_k33_permanent_contamination_reduction.py`.

## Matching topology

Use the bipartition

```text
left  = {0,2,4}
right = {1,3,5}.
```

Six of the fifteen perfect matchings of `K6` are the permutation matchings
of this `K3,3`.  The other nine have type

```text
one left-shore edge + one right-shore edge + one cross edge.              (2)
```

Fix an outside fine `M` and let `e` be its unique cross edge.  Exactly two
permutation matchings contain `e`, corresponding to the two matchings of
the complementary `K2,2`.  For either such permutation fine `P`,

```text
M intersection P = {e},       |M symmetric-difference P| = 4.             (3)
```

So (3) is a source-labelled `C4` route with literal common tail `e`.  The
checker enumerates and records both mates for all nine outside fines.

## Endpoint-coloured closure

Among the six permutation fines there are exactly two triples whose members
are pairwise edge-disjoint.  They are the even- and odd-permutation classes.
Each triple partitions all nine cross edges.

This remains literal after word decoration.  For each of the two triples
and every one of the `3^6=729` endpoint-coloured words, the checker forms
the union of the three decorated occurrence-cell sets.  It then tests all
fifteen perfect matchings.  In all 1,458 cases, the supported occurrence
set is exactly the six `K3,3` permutation fines:

```text
closure-size histogram = {6:1458}.                                       (4)
```

Therefore a same-word live tail-free factor triple cannot acquire only one
or two parity mates.  All three complementary permutations become live at
once.  The contamination is the full permanent, not a partially filled
permanent triangle.

## Coefficient boundary

Let `x_ij` be the nine nonzero decorated cross-edge values.  The six
matching monomials sum to

\[
 \operatorname{per}(x)=\sum_{\sigma\in S_3}
 x_{0\sigma(0)}x_{1\sigma(1)}x_{2\sigma(2)}.                \tag{5}
\]

Substitution (1) makes (5) zero.  Its nine `2x2` permanental cofactors are
all nonzero (`-1` or `2`).  Hence the full permanent fibre can be exact on
the coefficient torus while avoiding the private-binomial hypothesis used
by the Laurent unit: the even and odd parity monomials now occur in the same
six-term row, not in three isolated binomial rows.

This is precisely the first contamination pattern that prevents the
permanent-triangle product argument.  It is a finite, physical coefficient
guard rather than a missing operation label.

## Scope and uniformity

The theorem classifies every perfect-matching fine relative to the fixed
six-site `K3,3` and replays every endpoint-coloured word.  It proves that
outside contamination returns to common-tail `C4` recursion and that the
tail-free support branch is the full permanent.

It does not prove that a full exact source can realize (1): pure target
normalizations are not supplied by this fifteen-cell core.  It also does
not close recursive mates of those pure witnesses.  A single
row-independent nonzero spectator perfect-matching tail tensors through
the reduction, but changing spectator tails remain outside its scope.

## Reproduction

```text
python3 computations/verify_c6_k33_permanent_contamination_reduction.py --mode structural
python3 -O computations/verify_c6_k33_permanent_contamination_reduction.py --mode full
python3 -I -S computations/verify_c6_k33_permanent_contamination_reduction.py --mode exhaustive
```

All modes return the same frozen ledger digest.
