# Lazy all-X5 joint-semigroup CEGAR

Status: **exact finite-field implementation PASS; bounded decision runs are
nonterminal and the computation lane is retired at the current memory
budget.**  Nothing below proves target membership or nonmembership.

## Exact interface

The dependency-light Rust executable
`rust-fine/src/bin/closure23_joint_cegar.rs` now supports a lazy pool of all
6,558 non-pure three-colour words.  It starts from the frozen 22-word,
128,516-row basis of rank 124,368 over `F_32003`.  At each round it computes a
separator `lambda`, enumerates every translated X5 row with nonzero pairing,
adds a deterministic batch of independent crossing rows, recomputes the
separator, and rescans the whole pool.

The lazy construction is logically equivalent to eager closure for deciding
this fixed degree-13 module.  A row with `lambda(row)=0` cannot invalidate the
current separation.  Every row with nonzero pairing lies outside the current
span.  Within a batch, later crossing rows can become dependent on earlier
ones, so `--crossing-cap N` continues through the sorted candidate list until
it has inserted `N` independent rows or exhausted the list.  A no-crossing
terminal therefore gives a separator against the complete pool; zero target
remainder gives membership.  A round or resource cap gives neither.

The indexed divisor scanner enumerates physical perfect-matching divisors and
degree-four colour-histogram divisors of the live dual columns.  Its complete
round-one candidate list is asserted equal to the original direct 6,558-word
convolution.  The guard passes with exactly 12,708 candidates.

## Preserved bounded runs

| pivot/batch | completed rounds | last rank | added rank | wall/closure | terminal reason |
|---|---:|---:|---:|---:|---|
| forward / 256 | 256 | 189,904 | 65,536 | 264.47 s | round cap |
| forward / 2,048 | 161 | 454,096 | 329,728 | 1,202.72 s | hard 20-minute gate |
| forward / 8,192 | 24 | 320,976 | 196,608 | 206.42 s | RSS exceeded 16 GiB |
| reverse / 8,192 | 3 | 141,018 | 16,650 | 110.83 s | next round exceeded 120 s |

Every completed forward batch inserted its full independent-row cap and the
target remainder stayed at 13,636 terms.  The fully serialized 256-round run
ends with a modular dual of support 5,347, still crossed by 3,609,752
translations from 5,904 words; its cheapest crossing word is `10222210` with
one translation.  It is therefore explicitly not a terminal separator.

The cap-2,048 run provided the best rank progress below 16 GiB.  Its last
completed round had 26,673,009 candidates and dual support 52,252.  The
cap-8,192 forward run reached RSS 17,089,952 KiB after round 23; round 24
completed before SIGINT.  Both interrupted runs have compact stopped ledgers
and carry an explicit `inference: none` guard because the full result is
serialized only at normal termination.

## Pivot-order benchmark

Reverse lex is decisively worse.  At the common third-round checkpoint,
forward lex has rank 148,944, 20,951,696 stored nonzeros, and 7.06 seconds of
closure time.  Reverse lex has rank 141,018, 128,306,549 nonzeros, and 110.83
seconds: 6.12 times the fill and 15.7 times the time while gaining less rank.
Reverse round four exceeded the 120-second per-round gate and was stopped.
No reverse or larger-batch continuation is justified by this benchmark.

## Global column-interner prototype

The executable also has a bounded `--intern-columns` prototype.  Basis rows
store `(u32 column_id, u16 coefficient)` while all merge and pivot comparisons
dereference the ID to the original `Key`; insertion order is never used as a
monomial order.  The key table is authoritative and stores each 37-byte key
once.  A 64-bit fingerprint table maps to IDs and checks literal keys on every
hit; the bounded run has zero fingerprint collisions.  A round-one
inline/interner replay is algebraically identical:
both see 12,708 crossings, inspect 261 candidates to insert 256 independent
rows, reach rank 124,624 with 12,939,819 stored nonzeros, and produce the same
remainder digest and terminal dual.

The prototype fails the predeclared speed guard.  Inline storage takes 610 ms
end to end, while the interner takes 1,877 ms, a 3.077-fold slowdown.  The
interner already contains 4,585,601 distinct keys, 35.44% as many as the row
nonzeros, so the hash/interner overhead is substantial.  Sandboxed
`/usr/bin/time -l` could not expose peak RSS.  Because slowdown exceeded 2x,
the prescribed r8/r16 benchmark and any long decision run were not performed.
The exact negative-prototype digest is
`576835b37ca520130dce9bd48ae8c5d339a08fc700b9b719f54a99cb3b0adace`.

## Artifacts and replay

Primary serialized artifact:

```text
results_lazy_all_mixed_x5_cap256_joint_cegar_rust_p32003.json
sha256 0afdf5d644a7040e9ddf837fc4c5a6603e5857211dee8c2dceb16fb11cf7e985
```

Stopped-run and fill ledgers:

```text
results_lazy_all_mixed_x5_cap2048_timeout.json
sha256 82ac95b8ff1798b54d4b8c79cc51290f7782a6a3bea4044a6d023c4045d64a44

results_lazy_all_mixed_x5_cap8192_memory_stop.json
sha256 335934becac4132781d06c10b892b4386bd9c8709eda1a42c667dd8ab5186cae

results_lazy_all_mixed_x5_cap8192_reverse_pivot_stop.json
sha256 b698e9269d188be65f748a1c1e443a4236560da779973e0411562f90b8108294

results_lazy_all_mixed_x5_cap8192_forward_r3_fill.json
sha256 d9313681f6636cc95a43e787152eeb8a8e84cc22bfaf52ce6ce5cde5c4a84415
```

Current source SHA-256 is
`5ea7659b135c24c171a3ddf3b1f4aa7414e2218fd04ebbe3fe615cb827c7097e`.
The finite unit guards replay with:

```sh
cargo test --release --bin closure23_joint_cegar
python3 check_closure23_joint_cegar_rust.py --check-results
python3 check_lazy_all_x5_cegar.py --check-results
python3 check_joint_cegar_column_interner.py --check-results
```

The lazy-run checker logical digest is
`bb7df46fb072807a6abe0b5533af458d4aa5d8d3e16f1e733681fea63b9e8657`.

For a short independent-row guard rather than a long decision attempt:

```sh
target/release/closure23_joint_cegar \
  --prime 32003 --max-rounds 1 --lazy-pool-all --crossing-cap 256 \
  --output ../results_lazy_all_forward_pivot_r1_guard.json
```

It must report the 12,708-candidate indexed/direct equality and rank increase
124,368 to 124,624.  Python standard, optimized, and isolated replay modes
are part of the terminal package audit.

## Scope

This is exact linear algebra only in the frozen degree-13 joint edge/colour
semigroup.  The result establishes that lazy complete-pool CEGAR is sound and
that forward capped elimination scales farther than the eager and reverse
variants.  Because every bounded run stopped with nonzero remainder and live
crossings, it supplies no characteristic-zero claim and no ideal-membership
or conjecture theorem.
