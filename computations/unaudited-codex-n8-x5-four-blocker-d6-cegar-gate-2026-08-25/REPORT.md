# Bounded X5 + 560-carrier four-blocker degree-six gate

## Outcome

The exact bounded gate is terminal and **diagnostic only**.  All four canonical
branches produced complete homogeneous degree-six duals over
`F_1073741827`; none produced the exact rational column combination replaying
to `t^6` that the frozen acceptance contract requires for a mathematical PASS.
Consequently this package does not close the blocker lemma or the conjecture.

| canonical branch | selected columns | final dual support | engine wall (s) | watchdog peak KiB | independently exhausted incident columns |
|---|---:|---:|---:|---:|---:|
| triangle endpoint colour | 439 | 14 | 0.735475 | 116,304 | 17 |
| cap endpoint colour | 445 | 13 | 0.868445 | 116,672 | 16 |
| third colour | 439 | 14 | 0.849501 | 116,752 | 17 |
| direct | 15 | 10 | 0.144326 | 320 | 12 |

Every run stayed below the per-branch limits of 120 seconds, 8 GiB RSS, and
50,000 selected columns.  No continuation above degree six occurred and no
D12 checkpoint or cache was read or modified.

## Frozen literal input

The source exporter and canonical-incidence manifest are pinned in
`SCHEDULE.json`.  Each generated provider has exactly 361 named variables and
6,571 equations:

- 6,558 X5 fibre equations plus three pure equations, homogenized to degree 4;
- nine membership/right-side equations, homogenized to degree 3;
- one live-cell inverse equation, homogenized to degree 2.

Thus each tested column is a monomial multiple of one of the literal 6,571
source equations, and the only target is homogeneous `t^6`.  The four complete
provider files have independent SHA-256 pins; no orbit or profile substitution
is used by the solver.

## Exact bounded computation

For each branch the engine begins from the target row and alternates:

1. solve the currently selected transpose system over the frozen prime with
   target dual value one;
2. enumerate source columns incident to the current sparse dual support;
3. append every column with nonzero pairing and repeat.

The independent validator reparses each literal provider, rematerializes every
selected column, and replays its pairing.  For a reported complete dual it also
independently enumerates every degree-2/3/4 generator term dividing every
supported degree-six row.  All such incident columns pair to zero.  Any other
column is support-disjoint, so its pairing is identically zero.  This proves the
reported global-dual statements over the one frozen finite field, not merely
over the selected CEGAR subset.

Standard Python and isolated `python3 -I -S` validation have identical output.
Optimized Python is rejected fail-closed because it disables the validator's
assertions.  Five hostile mutations (wrong degree, cap overrun, invented
rational replay, invented mathematical PASS, and a false global-dual flag) are
all rejected.

## Scope and interpretation

A finite-field dual at a single prime is not accepted here as a rational
nonmembership theorem: a rational certificate may have bad reduction at that
prime.  Conversely, no modular membership candidate arose for exact rational
lifting.  Therefore the exact acceptance count is zero:

```text
exact rational t^6 unit certificates: 0 / 4
mathematical blocker branches closed: 0 / 4
conjecture verdict: unchanged / open
```

The first attempted wrapper was rejected before arithmetic because it enforced
only the 36 GiB contract rather than the required 8 GiB contract.  The empty
attempts are represented by `rejected_wrapper_contract_runner_summary.json`.
All accepted runs use the separately pinned `watchdog8.py` and have atomic
result, selected-column, dual, and watchdog artifacts.

## Reproduction and audit

`run_gate.py` is the sequential runner.  `validate.py` is independent of the
Rust elimination code and writes `results_four_branch_gate_audit.json`.
`results_validation_selftest.json` records the hostile suite.  The authoritative
interpretation is
`PASS_EXACT_BOUNDED_GATE_DIAGNOSTIC_NO_MATHEMATICAL_CLOSURE`; “PASS” refers to
the bounded computation and audit, never to the conjecture.
