# Three different orbit counts, reconciled

Research evidence only.  Krenn's conjecture remains open, `SP-CLEAN-BRIDGE`
is untouched, and no certified dependency changes.  Nothing here is a partial
case of the conjecture.

## 1. Why this note exists

Three numbers for "the matching-triple orbits" are in circulation and were
being compared to each other:

* the external Lean proof that closes \((6,3)\) branches on **8** cases;
* this repository's `search_parallel_binomial_nonzero_constants_cegar`
  indexes target orbits up to at least **56** at \(n=8\), and
  [`n8-full-support-sat.md`](n8-full-support-sat.md) names "orbit 39";
* `search_monomial_triple_cancellation_sat` produces a much shorter list.

They count **different objects**, so none of the comparisons was valid.  Here
they all are.

## 2. The table

Ordered triples of perfect matchings, by set and by group:

| set | group | \(n=6\) | \(n=8\) |
|---|---|---|---|
| arbitrary | \(S_n\) | 16 | 86 |
| arbitrary | \(S_n\times S_2\) (last two slots) | 12 | **57** |
| arbitrary | \(S_n\times S_3\) | **8** | **31** |
| pairwise edge-disjoint | \(S_n\) | 2 | 18 |
| pairwise edge-disjoint | \(S_n\times S_2\) | 2 | **13** |
| pairwise edge-disjoint | \(S_n\times S_3\) | 2 | 8 |

So:

* the external proof's **8** branches are *arbitrary* triples modulo
  \(S_6\times S_3\);
* this repository's **57** target orbits are *arbitrary* triples modulo
  \(S_8\times S_2\).  The reason is an implementation choice, not a
  constraint: `canonical_pair` extends the stabilizer only by the \(1\!\leftrightarrow\!2\)
  swap.  Pinning the first matching does **not** preclude the full \(S_3\) —
  the checker here pins it too and still reaches \(31\);
* `search_monomial_triple_cancellation_sat`'s **13** are *pairwise
  edge-disjoint* triples modulo \(S_8\times S_2\);
* "orbit 39" of `n8-full-support-sat.md` is
  \(01|23|45|67,\ 02|13|46|57,\ 03|14|27|56\), which **is** pairwise
  edge-disjoint — which is exactly why the two indexings were confusable.

## 3. The two consequences

**The right scaling comparison is \(8\to31\).**  Both endpoints are arbitrary
triples modulo the full symmetric group on vertices and colours, so this is
like against like.  The case structure of the architecture that closed
\((6,3)\) grows by a factor under four at \(n=8\), not by orders of magnitude.
Where the cost actually grows is inside each branch: the support-only SAT
encoding goes from \(10{,}890\) to \(688{,}590\) term variables, a factor of
\(63\), per [`n8-full-support-sat.md`](n8-full-support-sat.md).  That is a
statement about the branch *count* only; it prices nothing.

**A factor of about \(1.8\) is available, and it has now been checked.**  This
repository enumerates \(57\) orbits where \(31\) classify the same set.  The
full \(S_3\) is legitimate — the GHZ target \(\sum_ce_c^{\otimes n}\) is
symmetric under permuting colours — and an independent audit confirmed the
encoding is too: the \(57\) representatives merge into exactly \(31\) classes
(\(29\) merged pairs), and for **all \(29\)** the base CNF is *literally
identical* to its image under the induced cell renaming, with the lazily added
mixed-fibre constraints corresponding \(145/145\).  Negative controls: \(36\)
of \(40\) wrong colour permutations disagree, and \(4\) of \(4\) wrong vertex
permutations do.  No colour-\(0\)-specific code exists in the \(n=8\) path.

Corroborating argument: \(57\) *already* presupposes invariance under the
colour transposition \((1\,2)\), or \(86\) would be required.  The only way
\(57\) could be right and \(31\) wrong is if colour \(0\) alone were special.

Two caveats.  The saving is **prospective**, not currently-wasted work: no
\(57\)-orbit sweep at \(n=8\) exists, since the \(n=8\) scripts run one orbit
at a time.  And under `--symmetry-lex` the two CNFs are equisatisfiable rather
than isomorphic, because lex-leader depends on cell order — sound, but the
invariance is semantic rather than textual.

## 4. What this does not say

1. Nothing about whether \((8,3)\) has a solution, and nothing about whether
   the branch architecture closes it.
2. It prices no branch.  Branch *count* and branch *cost* are different
   quantities and only the first is computed here.
3. It does not establish that the external proof's steps survive at \(n=8\);
   it establishes only that its case structure grows \(8\to31\).
4. The \(1.8\) is prospective, not currently-wasted work; see section 3.

## 5. Audit

The dependency-free checker
[`verify_matching_triple_orbit_counts.py`](../computations/verify_matching_triple_orbit_counts.py)
verifies that \(K_n\) has \((n-1)!!\) perfect matchings, that \(S_n\) is
transitive on them and that \(\operatorname{Stab}\) of the canonical matching
has order \(2^{n/2}(n/2)!\); computes every entry of the table by pinning the
first matching and acting by that stabilizer, with the \(S_3\) merge done by
union-find on the resulting representatives; and confirms "orbit 39" is a
pairwise-disjoint triple whose first element is canonical.

The stabilizer route is **cross-checked at \(n=6\) against brute force with the
full \(S_6\times S_3\) acting** — over all \(3375\) triples for the arbitrary
row and all \(480\) for the pairwise-disjoint row — agreeing on all three group
columns.  Independently reconfirmed by union-find over the full \(105^3\)
triple set and by Burnside, both at \(n=8\): every one of the twelve cells
agrees.

Negative controls: the counts must be monotone in the group and the \(S_3\)
quotient must strictly reduce, or the group action is not being applied at all.

Standard library only, exact integer arithmetic, about three seconds, passing
normal, `-O` and `-I -S`, byte-identical across hash seeds \(0,1,42,12345\).

**Mutation-tested.**  Five injected faults — a wrong expected count, a
disabled slot swap, an \(S_3\) reduced to the identity, a non-canonicalizing
permutation, and a corrupted disjointness test — each raise, with exit code
\(1\), under **both** `python3` and `python3 -O`.
