# K24 direct D17/D18 residual gate

## Verdict

**The literal H-row materialization is rejected. The exact replacement is a weighted H-column-orbit interface; no K24 production result was accepted.**

The requested source scope is exactly:

- `source_D17_R3_4`: seven IDs `D17:{234,243,324,333,342,423,432}|R:3-4`;
- `source_D18_R2_4`: six IDs `D18:{244,334,343,424,433,442}|R:2-4`.

Both paths reconstruct a K20 parent, average occurrencewise over its selected mixed K0 pivots, and emit the 60 K4 tails. Every K24 child has anchor mass zero and is terminal.

## Materialized prefix rejection

The prefix-only producer `run_k24_residual_direct_d17_d18_gate.rs` exact-collects labelled rows, retains sorted raw runs, H-canonicalizes only after exact labelled cancellation, retains canonical runs, and would derive the charge from the exact merged row masses. It accepts only source counts 1, 8, or 61 and never accepts a full 485-slice request.

The one-slice run was stopped at 442.68 seconds during incomplete D17 H-canonicalization. At that point it had retained 6,167,729,927 bytes:

| Diagnostic stage | Files | Stored records | Bytes |
|---|---:|---:|---:|
| D17 sorted labelled-row runs | 130 | 103,093,823 | 4,123,752,920 |
| D18 sorted labelled-row runs | 33 | 27,579,406 | 1,103,176,240 |
| partial D17 H-canonical runs | 224 | 22,400,000 | 940,800,000 |
| D18 H-canonical runs | 0 | 0 | 0 |

No canonical merge, row TSV, result JSON, or charge was produced. The partial runs are explicitly incomplete diagnostics and cannot be assembled or paired. Peak RSS is unavailable because sandboxed `/usr/bin/time -l` failed its system query; that missing measurement independently prevents resource clearance.

Linear disk projections from the retained bytes are 49.34 GB for eight slices, 376.23 GB for 61 slices, and 2.991 TB for all 485 slices. The 61-slice projection exceeded the 232.65 GB available at the gate, and the full projection violates the sealed 1 TiB materialization limit. Prefixes 8 and 61 and full production were therefore not launched.

`results_prefix1_materialized_rejection.json` is the machine-readable hostile guard. The producer source SHA-256 is `d85163c6ab1845a3daa6353ec52843036d72491b6143ddbe6be80759d1992459`; the stopped binary SHA-256 is `c0f2fae63808f1b68f18fb8427a53d6a5b175d652cc6b5e657c7bf80ebbdec6e`.

## Exact factorized replacement

The final 60-row response fan for a selected K20 pivot is exactly one multiplier-aware literal K24 top column:

```text
C = (mixed word w, multiplier U20 = K20_parent - pivot_anchor)
top(C) = sum of the 60 K4 tails [U20 + tail].
```

Thus the producer need not materialize 60 rows for every selected pivot. It emits one exact record `(w,U20,weight)` per selected K20 pivot occurrence, exact-collects labelled columns, then H-canonicalizes and exact-collects column orbits. A final column-orbit record stores:

```text
canonical column C
column orbit size o_C
orbit-total exact mass W_C
per-labelled-column coefficient alpha_C = W_C / o_C
```

The division by `o_C` is load-bearing and must be exact; it is the H-invariance guard. Sorted labelled-column runs remain until the canonical column merge is independently accepted.

The prior exact source fold fixes 842,301,440 selected pivots for D17 R3-4 and 230,937,600 for D18 R2-4. At 37 raw bytes per record, the factorized full raw upper bound is 39,709,844,480 bytes, before exact cancellations—about a 75-fold reduction from the rejected row projection. Production remains unlaunched: it must pass new 1/8/61 factorized gates and the 540-second, 8 GiB family-RSS, 16 GiB aggregate-RSS, and measured-disk rules. The planned production partition is eight balanced half-open intervals over `[0,485)`.

## Compatibility with the frozen Gram provider

The stopped producer preserved one complete literal witness for each strict group. The audit reconstructs the selected multiplier from the K20 parent and pivot, then replays the existing multiplier-aware provider:

| Group | Canonical column | Column orbit | Top outputs | Provider row coordinates |
|---|---|---:|---:|---:|
| D17 R3-4 | `00000022:0d0d11222e44505f616d90a3a7b8c5cfdfe9eaed` | 384 | 60 | 60 |
| D18 R2-4 | `00000011:090d0d112244484c5061b8c5cfd2d7dfe9eaedf2` | 384 | 60 | 60 |

For both, the producer literal K24 row occurs in `top_outputs(C)`, every output is K24, the producer H-canonical row and action witness replay exactly, and the provider orbit vector has exact orbit-size divisibility. This is the sound part of the existing K24 provider; its older 1,757 decorated-matching index is not used.

For a factorized residual `R = sum_C alpha_C v_C`, the exact derived interfaces are:

```text
H-row mass:       m_R(r) = sum_C alpha_C m_C(r)
target pairing:   <v_D,R> = sum_C alpha_C G(D,C)
target norm:      ||R||^2 = sum_C,E alpha_C alpha_E G(C,E)
77-charge:        Q(R) = sum_C alpha_C sum_r m_C(r) q(r)
```

These formulas allow row masses, charge, and target-rooted pairings to be evaluated on demand without a global row file. Moreover, the accepted weighted column ledger is itself a constructive rational source vector `x` with `R=A*x` for this fragment; any assembled constructive-span claim still requires complete, independently accepted source coverage and exact column-orbit coefficients for all required fragments.

`factorized_k24_residual_interface.schema.json` freezes the record and shard provenance. It requires the strict group, exact source interval, all input/engine/content hashes, selected-pivot count, zero cancellations, orbit-division guard, and literal source/factor/pivot/tail/multiplier witnesses. A charge scalar never substitutes for a column record.

## Scope

`results_k24_factorized_residual_gate.json` accepts only the interface design and the two literal/provider proof witnesses. It makes no factorized production, complete K24 residual, K24 charge, terminal-span, or conjecture claim. The multi-terabyte partial row directory is diagnostic and intentionally omitted from `MANIFEST.sha256`.

Replay:

```sh
python3 computations/unaudited-codex-orbit0-k24-residual-direct-d17-d18-gate-2026-08-24/audit_k24_factorized_gate.py
```
