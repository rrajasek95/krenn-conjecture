# X5 four-blocker homogeneous degree-seven two-prime gate

## Verdict

All four frozen canonical branches have exact primitive integer dual
certificates at homogeneous degree seven.  Each dual has `L(t^7)=1`, pairs to
zero with every literal degree-seven source column, and reduces exactly to both
finite-field producer duals.  Therefore `t^7` is not in the degree-seven source
span over characteristic zero in any branch.

This is a mathematical PASS for the bounded degree-seven nonmembership claim,
not a conjecture proof.  No rational membership certificate arose, the blocker
branches remain open in higher degree, and degree eight was neither designed
nor launched.

| branch | selected columns at each prime | modular / integer support | exact equations / rank | exhaustive incident columns |
|---|---:|---:|---:|---:|
| triangle endpoint colour | 1,943 | 23 / 23 | 31 / 23 | 30 |
| cap endpoint colour | 1,939 | 17 / 17 | 25 / 17 | 24 |
| third colour | 1,945 | 17 / 17 | 25 / 17 | 24 |
| direct | 15 | 10 / 10 | 13 / 10 | 12 |

Every primitive integer coefficient is `+1` or `-1`, and every target
coefficient is exactly `1`.  The exact systems have full column rank on their
union supports.

## Bounded producers

The source-frozen 361-variable, 6,571-equation providers are reused byte for
byte from the sealed degree-six packages; only homogeneous target degree and
allowed multiplier degree change.  The isolated Rust engine accepts exactly
the primes `1,073,741,827` and `1,000,000,007`, degree seven, at most 100,000
selected columns, 115 native seconds, and 120 watchdog seconds / 8 GiB RSS.

All eight sequential runs return `COMPLETE_MODULAR_DUAL_DIAGNOSTIC`.  Engine
wall is at most 3.343 seconds and observed watchdog peak RSS is at most 133,600
KiB.  The two primes have identical selected-column counts and support sets for
each branch.

An initial eight-run attempt had correct degree-seven arithmetic and `t^7`
targeting but a stale JSON field `degree: 6`.  The validator rejected it before
acceptance.  Its exact source, binary, outputs, and attempted lift are retained
under `rejected_degree_metadata_v1/` with zero accepted coverage.  The source
was changed only to emit `DEGREE`; the engine was repinned and all eight runs
were repeated from scratch.

## Exact characteristic-zero lift

For each branch `lift_characteristic_zero.py` takes the union of both modular
supports and all literal source columns incident to it, then solves

```text
L(t^7) = 1
L(m * g_i) = 0
```

by exact rational RREF.  It primitive-normalizes the solution over the
integers, recomputes the incident set from its nonzero support, and replays
every pairing over `Z`.  Any remaining degree-seven source column is
support-disjoint and has pairing zero automatically.  Applying `L` to a
hypothetical rational identity for `t^7` gives the contradiction `1 = 0`.

`validate.py` independently reparses both providers, re-enumerates every
incident column, replays all integer pairings, verifies the two modular
reductions, and checks both watchdog contracts.  Standard and isolated Python
outputs agree.  Optimized Python is rejected fail-closed because assertions
would be disabled.  Five hostile mutations are rejected.

## Scope

- exact conclusion: four characteristic-zero homogeneous degree-seven
  nonmembership theorems;
- no prime-specific rank or target-pairing anomaly;
- no conclusion in degree eight or unrestricted degree;
- no D12 cache was read or modified;
- conjecture status remains open.
