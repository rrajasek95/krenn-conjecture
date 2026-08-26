# K24 K16 R4-4 failed-full audit and support-aware witness contract

## Outcome

PASS failure audit: the attempted full K16 R4-4 fold exited with code 101 at the post-traversal `37 == 257` sample assertion, before either sample or result writing.  The intended result, result temporary, sample ledger, sample temporary, and validation artifact are all absent.  No scalar was accepted, and the rejection-evidence JSON is not a scalar result.

A deterministic support-aware 257-witness candidate set is independently validated and the sample-only repair preserves every scalar/count/histogram field on the 262,144-record distributed control.  However, full relaunch remains unauthorized: the repaired producer must first emit a full-traversal 257-bin support histogram and fail if its positive-bin set differs from the candidate manifest.

No heavy or full process was launched by this audit.

## Failed attempt

Frozen rejection evidence SHA-256: `4d78151f2326b93b629d5fd273016448008b4c659fc8779a6640e1e9faf79aea`.

The full traversal observed nonzero sample support in only 37 of the 257 equal global source-index bins.  Its old contract demanded one nonzero witness in every bin and panicked on `assert_eq!(ss.len(),257)` with left `37`.  The output order in the producer places this assertion before `sample.tmp`, sample rename, `result.tmp`, and result rename.

The audit independently confirmed the following paths are absent:

- `results_k16_r44_complete.json`
- `results_k16_r44_complete.json.tmp`
- `results_k16_r44_complete.json.samples.tsv`
- `results_k16_r44_complete.json.samples.tsv.tmp`
- `results_k16_r44_complete_validation.json`

The failed source/binary pins are `1ed9ef5a9b4450f55f2259a11a88a2f370259a6373af6b4b735361f928cdf1e1` / `3a1b5e716ff4f781a5e523e990d8f209975b34231faf55cce8e8dd72e4f88ef9`.  The repaired candidate-aware source/binary pins are distinct: `ca18746eb9368fe67d24e6cafc376b5e3f21530be0536313db9822efc2e58cd0` / `2d41110bcb5e3b608d045555a7b2cf22f5a4c7e9cb26d3d53d83f4e64d75b405`.  The failed binary lacks the candidate-manifest marker; the repaired source and binary contain it.  These pairs must never be interchanged in a manifest.

## Support-aware 257-witness contract

Support is defined occurrencewise: source record `i` supports global bin `floor(i*257/24097095)` iff at least one literal `(p1,t1,p2)` continuation has nonzero terminal K4 charge.

The certified candidate manifest contains exactly 257 distinct source records from the 37 observed support bins:

- bins 0 through 34: seven candidates each;
- bins 35 and 36: six candidates each.

This is the general balanced rule `floor(257/B)+1` in the first `257 mod B` positive bins and `floor(257/B)` in the rest, with `B=37`.  Within each bin, candidates are ordered by increasing source record and use that record's lexicographically first nonzero `(p1,t1,p2)` continuation.  Slots are exactly 0 through 256 in natural `(bin,record,p1,t1,p2)` order.

Candidate manifest SHA-256: `57b7f0cfa15b436b6b821922c426f19d15496eb7a1cd64e7e632acaa003d5fbf`.

The audit independently checked all 257 entries against checkpoint SHA-256 `93c1b21eaa1723b98eb4d3b59ada6d6a867c434573a255d2a48fcdeead0656d3`: exact source row and coefficient, unique record and slot, global-bin formula, quota, nonzero terminal charge, exact `U/(m1*m2)`, contribution arithmetic, degree 4, and natural ordering.  A separately executed literal referee replayed all 257 pivot/tail chains through every terminal K4 child without traversing a scalar shard; result SHA-256 `d0fd9bd271ba8842a1b74f27c226a7fc3b45e46eb68c265d40d1fa8045625319`.

The old distributed-262144 result SHA-256 `237c4c13...` and repaired result SHA-256 `f48edef8...` agree exactly in all source mass, pivot, child, terminal, full/irreducible, scalar, and `(m1,m2)` histogram fields.  Thus the bounded repair is sample-only.

## Required full-traversal certificate

The read-only census certified candidates in bins 0 through 36, but by itself did not prove bins 37 through 256 empty.  A fail-closed full producer must therefore accumulate, without changing its scalar recurrence:

- a 257-entry count of source records with at least one nonzero literal continuation;
- the exact positive-bin list; and
- the pinned candidate-manifest hash.

Before any file write, it must assert that the positive bins equal the candidate bins and that all 257 candidate slots were realized.  Any new positive bin must panic before output and force a new census/manifest supersession.  The sample and result hashes must then be pinned by an external acceptance envelope, and all candidate rows independently replayed.

The repaired producer currently pins the candidate ledger and can realize its 257 slots, but it does not emit the full support histogram.  Therefore it does not yet implement the complete fail-closed contract and is not cleared for a full relaunch.

## Hostile and mode checks

The support validator rejects ten mutations: duplicate slot, duplicate record, wrong bin, wrong source row, wrong coefficient, zero terminal charge, wrong unit, wrong contribution, wrong final degree, and non-natural order.

The independent audit is identical under standard Python, `-O`, and `-I -S`; stdout SHA-256 `5ebcf009237186b66cf15c10c36f1b9720903596b40af6a29fbf13d53fc1d2ba`.

Key package pins:

- support contract: `641e162cc27e6d44d99cb5b762499624e6d33fdf2dc8fb96aecb395c8876cf32`
- independent audit: `1eaf28c6f0b6d0e38b15fdda84c9829108e4c5feac88007c050799b144bd53a5`
- hostile suite: `81027e908b1769e284a85d6a14e74cc5653b49555943aa62199fc3911097c7f2`
- audit result: `2e4f47e1cee8ad4c7ef21fe740e43123f94f84ed288b3fe291a1bce086450f2a`
