# Nine-added-block induction census

Status: **PASS exact source/guard census; zero solver runs; no theorem promotion**.

The classifier is imported byte-for-byte from the corrected eight-block
interface (`43348045...`), including the source-labelled family, fixed caps,
formal guard reduction, nonidentity hyperplane carriers, and the order-two
guard permutation.  The corrected 616-record eight-block ledger is the sole
authority for deletion parents.

## Enumeration and deletion boundary

Among all `C(20,9)=167,960` nine-added supports, 57,308 have a fixed identity
cap and 110,652 evade that first filter.  Formal guard reduction leaves 2,329
stable nine-supports and 37,264 variable-family strata.  Exact structural
classification gives

```text
fixed identity cap             26,380
nonidentity hyperplane cap      7,408
unresolved coefficient locus    3,476
```

Of the 3,476 unresolved records, **2,556** delete at least one added edge to
an unresolved corrected eight-block record, while **920** have no such parent
and are the genuinely new minimal records for this induction relation.  The
exact parent-count histogram is `0:920, 1:732, 2:1412, 3:364, 4:48`.
This is only a source-labelled parent relation: no deletion-monotonicity
conclusion is made.

## Essential skeletons and symmetry

The matching-essential edge histogram is

```text
12: 224
13: 472
14: 358
15: 780
16: 1,108
17: 534
```

There are 2,628 distinct labelled essential skeletons, 191 exhaustive
unlabelled graph-isomorphism classes, and 1,778 literal guard orbits (80
singletons and 1,698 pairs).  Graph isomorphism is computed exhaustively
inside invariant degree cells; it is not conflated with the much smaller
formal guard symmetry.

Exactly 3,472 records have a degree-four vertex.  Four exact-16 records have
degree sequence `(3,3,3,3,5,5,5,5)` and therefore lie outside the degree-four
frontier theorem premise.  All four have unresolved eight-block deletion
parents; the 920 genuinely new records all have a degree-four vertex.

## Conditional frontier coverage

No external theorem is promoted here.  If the fresh current-CNF max-15 proof
receives terminal independent DRAT verification and a pinned seal, it covers
1,834 records.  A separately fresh/pinned max-16 theorem then covers 1,104
additional records, for **2,938/3,476** total.  The exact remainder is:

- 534 degree-four records with 17 essential edges;
- 4 exact-16 records with no degree-four vertex.

Within the genuinely new 920 records, max-15 would cover 598 and max-16 an
additional 242, leaving 80 exact-17 records.  The historical max-16/max-17
interfaces are not imported or replayed by this package.

Validation performs a full deterministic regeneration, and 14 hostile
mutations are rejected.  There was no Singular, SAT, DRAT, or other heavy
solver invocation and no nine-block or conjecture-level closure claim.
