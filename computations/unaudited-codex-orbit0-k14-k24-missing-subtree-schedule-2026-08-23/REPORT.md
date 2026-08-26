# Minimal execution schedule for the discarded K16 subtree

## Verdict

Exactly five pivotable parent pages are needed for an independently replayable
completion of the 15 missing descendants:

| parent checkpoint | children |
|---|---|
| `D14:222|R:2` (recovered K16 root) | `[2,2]`, `[2,3]`, `[2,4]` |
| `D14:222|R:2-2` (K18) | `[2,2,2]`, `[2,2,3]`, `[2,2,4]` |
| `D14:222|R:2-3` (K19) | `[2,3,2]`, `[2,3,3]`, `[2,3,4]` |
| `D14:222|R:2-4` (K20) | `[2,4,2]`, `[2,4,3]`, `[2,4,4]` |
| `D14:222|R:2-2-2` (K20) | `[2,2,2,2]`, `[2,2,2,3]`, `[2,2,2,4]` |

The remaining 11 response nodes have degree at least 21.  Their anchor sum is
at most three, so no four-cell mixed K0 head can divide them.  For the frozen
77-cycle charge program, they may therefore be accumulated directly as exact
77-bin profiles/scalars.  The irreducible normals left at the four K18--K20
parents may be handled the same way.  This compression is not enough for a
literal residual or a different quotient; those goals require retaining the
full H-row pages.

## Dependency- and disk-minimal order

1. Replay the K14 `222` cancellation, but retain and exactly merge the branch
   formerly discarded at the `if pivots(row_signature)` test.  This produces
   the K16 root checkpoint.
2. Traverse each complete K16 H-orbit once and emit all K2/K3/K4 children
   together.  Merge the K18 `[2,2]`, K19 `[2,3]`, and K20 `[2,4]` pages
   separately, preserving their lineage IDs.
3. Consume K19 and K20 `[2,4]` into terminal profiles and delete their accepted
   parent pages.  Doing these first prevents them from overlapping on disk
   with the extra K20 page created next.
4. Reduce K18 `[2,2]`, accumulating its K21/K22 terminal profiles and
   materializing only K20 `[2,2,2]`.
5. Reduce that final K20 parent to its K22/K23/K24 profiles.  Accept the page
   only when the DAG verifier sees all 15 evidence-bearing lineage IDs.

A full parent file can be elided only by a transactionally journaled
source-linear stream whose upstream cursor, exact pivot histogram, child
manifests, and digests independently replay the same page.  A scalar alone can
never replace one of the five pivotable parents.

## Known work and storage

The first replay has exact frozen counts:

- `838,080` factored H-slice/head pairs;
- `6,619,280` valid K14 pivot uses;
- `79,431,360` K2 tail evaluations;
- `75,691,040` pivotable K16 occurrences to retain; and
- `3,740,320` simultaneous irreducible-control occurrences.

At the certified scale `U=400591699200`, a compact checkpoint record is a
24-byte canonical row plus a signed i128 coefficient, or 40 bytes.  Before
collection, the K16 raw payload is therefore at most `3,027,641,600` bytes
(`2.820 GiB`); a two-generation external merge needs at most `5.640 GiB` of
record payload, excluding indexes and allocator overhead.  The collected
checkpoint can only be smaller.

Later exact costs cannot be inferred from signature reachability because the
discarded coefficients were never collected.  After merging a parent, record

```text
L = sum orbit_size
V = sum orbit_size * dividing_pivot_count.
```

Its exact K2/K3/K4 evaluation counts are `12V`, `32V`, and `60V`, and a
collected child with `N` nonzero H-orbits occupies `40N` bytes.  The pivot-count
ceilings are 16 at K16, 4 at K18, 2 at K19, and 1 at K20.  The JSON includes a
rigorous but intentionally hostile K16 upper bound; it must not be treated as
an expected cost.  No child expansion should begin until the actual `L,V`
census is atomically accepted.

## Exact stop and replay gates

Every page pins all upstream hashes and must satisfy degree, H-canonicality,
signed-zero cleanup, lineage, sign, and denominator-product checks.  The root
must replay the exact `75,691,040 + 3,740,320` split.  Every parent publishes
its orbit count, labelled support, pivot histogram, `V`, child-evaluation
counts, mass/L1 totals, byte cursor, and run hashes.  Denominator products must
belong to the corresponding DAG node and divide `U`; the sign rule is
`child=-parent/pivot_count`.

K21+ outputs and retained K18--K20 normals must scan with zero dividing K0
pivots.  Incomplete runs are never accepted as parents, and no full K18, K19,
or cumulative charge claim may be restored until every one of the 15 lineage
manifests passes replay.  The hostile guard deletes `[2,2,2]` and must fail.

This was a read-only scheduling audit; no residual, profile, or charge run was
launched.  Result logical digest:
`47ef89cee9a47a7293006543c904e2042fb95a68c2dd9a8d43dfdbb47fc74b33`.

