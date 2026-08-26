# Independent audit of the fast single-pass K14 K24 charge engine

## Verdict

The fast computation is semantically cross-refereed on exact source interval `[0,1)`: both K14 sinks match the sealed physical consumer in source mass normalization, every stage count, terminal/full/irreducible occurrence counts, exact scaled charges, and every denominator-product histogram entry.  This is strong bounded evidence that the fast recurrence and the sealed physical recurrence agree.

An externally produced full result subsequently landed and passes this audit's structural/scalar checks, including independent replay of all 514 literal witnesses.  The raw output ledger by itself is nevertheless **not sufficient for full production acceptance**: its JSON omits the input/source/binary/result/sample hashes and independent RSS evidence required by the sealed charge-first contract.  Its legacy validator does not parse the sample TSV or enforce exact keysets and falsely accepts 11 of the hostile mutations below.  This audit did not launch or rerun the full computation.

## Frozen pins

Fast implementation:

- source `run_k24_charge_k14_source.rs`: `dd9510f3324b160a3b496ba6d0b5bdfb9335699a1fc99cd75c18dadaf8eeca6d`
- binary `run_k24_charge_k14_source`: `4049688d492ee604ead3b43e1bb3f42efb42e9da7758c8128b08f67377469853`
- legacy validator: `28bcd5552d43adaf800514ba6acdab89abb0ed143d3a598b6e84567c87bc891a`
- fast distributed-one diagnostic result: `1fd01ee42e4e0b8548794a58a8de7702791c59afeb8ad16e39ee0b5e37781083`
- fast distributed-eight diagnostic result: `2dbbd7c0633c0719336dbb8f2b164f6cec522afdbc04da879e58ac379f714013`
- fast full result: `f188ec896a6782cff185c91b369b9e71fcbe661bbafbe61d625cdc51e02ba442`
- fast full 514-witness ledger: `5d881350559aa3253e9aa60545bf6b8af62d9db7e8d5b9871f69ccea735554cf`
- legacy full validation: `dfcce3bb5c8aebf6b9f41245a3caa754bd6181b5917ac3a9556244b4daf5a747`

Independent strict interface:

- closed raw-result schema: `1eab6b6678f9a8f84381b113cb980f88949a1d65c63f388b23f67ceaabe9840d`
- independent audit: `32226639ee3ef177db6587d459d55c24b0f22f2452f8624e48660985a38706a1`
- hostile suite: `343a94af7f16ca328c5a9693f531d5aab68eb990bb176d4a8530e7be9e7f90ed`
- exact fast `[0,1)` result: `c976d3154334c7552e0722707bec0a96af9e20c917078de266a74f180dfd2d07`
- exact fast `[0,1)` samples: `0b94664381595e10422359f78ffb282d5411eda06c225e69791d4c9a8106c596`

Sealed physical reference:

- source: `10670f0687168d4383cfeb679ce8521d4c8b1b5621092b7600a3ef1b6ee79f51`
- binary: `21ef771613369867a4bb0bad7257cd7e04da11dffad68061b6f4c56dff231c8a`
- exact physical `[0,1)` result: `7e3533bac7eb87ba07af6d0238a13f06ade67aef59014a77724e40fe67f6ba5d`

Inputs re-hashed by the independent audit:

- physical structure/R8 source: `55e3823101f37f615f45ded7a3a4ca09c3d7ecd656c00f4bf3a9d5c33a5b260b`
- K17 auxiliary: `f8c78389c91498b625627f17429854178a0ee6c2c456288ddf108d97944d47ab`
- terminal K4 table: `4cec01e1695241c918f27625e79d767a8fb30fe5d1741b57f217f33712c35aa3`
- cycle auxiliary: `8213a3cbac99009ef71b5c055a977b440bc88979bb9119bbed022740d2397fc7`

## Exact source-record-zero crosscheck

The pinned fast binary was run only on contiguous source interval `[0,1)` with one worker.  For `D14:222|R:3-3-4` it produced scaled charge `261088457490432000`; for `D14:222|R:4-2-4` it produced `234863207730708480`.  These equal the sealed physical values exactly.

The following also agree exactly for both sinks:

- `source_heads = 1728`, source mass magnitude `663552`;
- all three selected-pivot counts;
- all three tail counts and both pivotable-child counts;
- terminal, full, and irreducible occurrences;
- full and irreducible scaled charge; and
- the complete denominator-product histogram.

The apparent sign difference in source fields is intentional and equivalent: the sealed physical engine starts from the direct D14 coefficient `-M` and applies three response sign flips, while the fast engine folds those signs into a positive `M` before the same exact `U/(m1*m2*m3)` division.

The fast run took 3.217920 seconds versus 30.286253 seconds for the retained physical control.  The existing fast eight-record gate took 4.115902 seconds and projects about 250 seconds linearly, but it is a distributed diagnostic over the whole 485-record index range, not a contiguous acceptance interval.  This audit makes no full-wall or RSS claim.

## Full-result structural and literal audit

The externally landed result covers the exact non-distributed interval `[0,485)`, consumes all 485 declared records, and completed in an engine-reported 180.344244 seconds.  Its two exact scaled charges are:

- `D14:222|R:3-3-4`: `104945403010833285120`
- `D14:222|R:4-2-4`: `64033288812772392960`

The strict auditor reconstructs the source mass of every interval directly from the pinned R8 ledger and checks all recurrence/histogram identities.  It then independently replays all 514 samples (257 bins for each sink): source-record and factor indices reconstruct the literal K14 row; each recorded pivot belongs to the independently recomputed pivot set; each exact divisor is reproduced; both intermediate literal rows match; all 60 terminal K4 children are nonpivotable; and their independently recomputed cycle charge equals the recorded terminal response.  There are 413 nonzero terminal-charge witnesses.

This establishes structural/scalar PASS for the two full K14 charge fragments.  Resource acceptance remains withheld because no independent external RSS record accompanied the run; the raw engine's peak-cache field is not a substitute for process RSS.

## Strict raw-result schema and hostile tests

`k24_fast_k14_result.schema.json` closes the top level, both named sinks, caches, sample guard, and resource guard with `additionalProperties: false`.  The executable auditor mirrors and crosschecks all schema keysets without `assert`, reconstructs exact source masses directly from the pinned 485-record source, enforces exact interval/distributed semantics, checks all recurrence identities and histogram cardinalities, reads the adjacent sample TSV, and verifies its exact header/counts/ranges/flags.

All 15 hostile mutations are rejected by the independent validator:

1. extra top-level key;
2. wrong status;
3. duplicate lineage ID;
4. interval/count mismatch;
5. wrong source-head count;
6. wrong source mass;
7. full/irreducible scalar mismatch;
8. product-histogram cardinality mismatch;
9. inexact `U` division;
10. false abstract/literal guard;
11. wrong sample count;
12. detached sample ledger;
13. negative terminal-cache-clear count;
14. resource peak above cap; and
15. elapsed time at or above the gate.

The legacy validator falsely accepts 11 of these: extra key, wrong status, interval/count mismatch, wrong source mass, product-histogram cardinality mismatch, false abstract/literal guard, wrong sample count, detached sample ledger, negative cache-clear count, resource peak above cap, and elapsed time above the gate.  Its semantic predicates use `assert`; under `python -O` those checks disappear and the CLI terminates only because its embedded hostile selftest then detects that mutations were accepted.

The independent audit output is identical in standard, `-O`, and `-I -S` modes (stdout SHA-256 `2d10778b42c87264236af188bc92a4d918b233ec303ec76f6eaa415789f88726`).

## What a full acceptance still requires

A future full fast result may be considered only through a superseding external acceptance envelope that pins:

- all four retained inputs, the fast source and binary, the raw result, and its sample TSV;
- exact non-distributed interval `[0,485)` with 485 consumed records;
- the strict two-ID/two-sink schema and all scalar/count/histogram invariants;
- independently measured wall/RSS evidence under the production gate; and
- independently replayed distributed literal witnesses, with nonzero continuations represented rather than relying solely on the engine's current earliest-per-bin sample policy.

The independent integrity and literal replay supplied here is sufficient for the mathematical structure/scalar portion of that envelope.  Until independent resource evidence is attached, the result should be recorded as a structurally accepted K24 charge fragment with production-resource acceptance explicitly withheld.
