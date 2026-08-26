# Orbit26 direct pure-target transfer through y10

## Exact result

The complete original residual of the frozen degree-five certificate was
contracted through y9 with the frozen deterministic monic providers.  Its
exact y10 circuit is

`C10 = R10 - R8*h2 + R7*S3 + R6*S4 + L(R9)` (scale 4).

The circuit emits 142,520,100 contributions and aggregates to **140,185,881**
nonzero y10 rows.  Against all 2,206 literal N4/PM4 three-term leading blocks,
**12,195** rows have no quadratic divisor and
**113,790** have exactly one.  The lex-first dead row is
`0111202020494f4f50f8` with coefficient -4.

Thus this particular right inverse is exactly dead at y10.  This is not a
full-Macaulay nonmembership statement: changing the lower-degree kernel
choices may change the terminal y10 class.

## Transfer structure

The small exact kernels have support 66 (cubic S3) and 244 (quartic S4).
S3 has physical profile 28 `3P2`, 28 `P3+P2`, and 10 `P4`, spanning 65
uncoloured skeletons.  Only 14 of the 28 matching-skeleton rows are literal
normalized Hafnian terms; the other 52 rows are endpoint-colour or physical
product/collision terms.  The unrelated archived 66-row attachment lives in
degree 8 and has literal intersection zero with S3.

The 52-row nonliteral class is not closed under the twelve source-labelled
linear contractions used to construct S3.  Five contractions have all six
tails in the 52 rows, while seven also meet literal `h3` rows.  The unique
tail collision is `05c0d5`, reached from the two distinct `h2` source rows
`30c0` and `72d5`; this is the smallest exact obstruction to treating the
52 rows as an autonomous contraction class.

## Replay

Run:

```text
python3 computations/unaudited-codex-n8-orbit26-direct-target-2026-08-23/audit_factored_y10_transfer.py
python3 computations/unaudited-codex-n8-orbit26-direct-target-2026-08-23/audit_s3_physical_skeleton.py
python3 computations/unaudited-codex-n8-orbit26-direct-target-2026-08-23/audit_s3_source_closure.py
python3 computations/unaudited-codex-n8-orbit26-direct-target-2026-08-23/package_full_y10_aggregate.py
```

The 140-million-row aggregation itself is replayed by the Rust binary
`aggregate-full-y10` using a disposable partition directory.  Its compact
raw result has SHA-256 `f623fa82320d70550518721dbb90d34b7df865662227a33c94bbf619f8328c03`.

The old file `r6_lex_correction_y10_tail.txt` is an isolated R6 correction
control only and is not the scope-correct terminal residual.
