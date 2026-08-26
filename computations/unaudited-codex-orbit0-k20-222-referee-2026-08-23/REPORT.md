# Independent referee: K20 `[2,2,2]` immediate charge

## Verdict

**PASS for the single lineage `D14:222|R:2-2-2`; no complete K20 charge
exists yet.**  The exact 36-path DAG has only two certified paths and 34
missing paths, so the two-path subtotal must not be presented as a K20 total.

The terminal component reads all `158,439,965` `H18PIV2` parent orbits of
scaled signed mass `724159651336720220160`.  It selects `399,275,484` third
pivots, emits `4,791,305,808` representative K2 tails, and finds
`4,221,024,490` immediately irreducible tails.  The independently checked
charges are

- full: `2274118864523560648704 / U`;
- irreducible: `2180843458743050600448 / U`
  = `2839639920238347136/521603775`.

## Arithmetic and source audit

For all 33 realized `(m2,m3)` types, the provenance ledger satisfies
`p3_uses=m3*parents`, `children=12*p3_uses`, and all component sums reproduce
the terminal totals.  Every type has `m2*m3 | U`; the production loop also
asserts `w2 % m3 == 0` on every parent before applying the cancellation sign
`w3=-w2/m3`.  The upstream `m1` is already incorporated into the signed K18
mass; no extra division is silently performed here.

All 257 production sample parents were independently replayed from literal
cell data.  Their `p2/t2` witness landing, `m2`, `m3`, every third-pivot K2
tail, cycle charge, and immediate pivotability agreed exactly.  The cached
path-profile formula is source-faithful: it records the four open endpoint
paths and closed cycles, and endpoint completion determines precisely the
same cycle partition used by the literal 77-cycle evaluator.

## Global K20 scope

The exact recurrence DAG contains 36 reachable K20 paths.  Certified here are
only `[2,2,2]` and the earlier `[2,4]` path.  Their partial scaled subtotal is

- full `2350865030430772199424`;
- irreducible `2253321204923526905856`.

The remaining 34 paths require unrecorded pivotable K17/K18 intermediates or
new regeneration from the source structure.  Thus there is no authoritative
36-path aggregation, terminal K20 residual, or K20 membership claim.

Replay: `audit_k20_222.py`; result logical SHA-256
`68a14362375ba273f1905435e5cca6976de4ff52e4a74bc8a5b6661f94e5c04d`.

