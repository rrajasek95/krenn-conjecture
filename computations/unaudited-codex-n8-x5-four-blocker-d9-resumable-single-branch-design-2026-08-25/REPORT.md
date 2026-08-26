# X5 degree-nine resumable single-branch recovery design

## Verdict

A source-pinned, restartable recovery lane is frozen for the incomplete
`triangle_endpoint_colour` branch at prime `1,073,741,827`.  It resumes from
exactly 15,273 selected columns, support 178, and round offset 434; it launches
only that branch and is held pending explicit resource clearance.  No literal
D9 continuation was run while D12 production was active.

The former engine spends 174.739622 of 175.758071 seconds (99.420539%) in
`solve_dual`; complete incident scans total only 0.764937 seconds.  The hot path
recomputes frequencies and rebuilds the entire selected linear system after
every CEGAR round.  This, rather than provider parsing or incident-column
enumeration, is the measured blocker.

## Exact resume and optimization

The isolated engine reparses the pinned selected TSV and dual TSV, rematerializes
all checkpoint columns from the pinned literal provider, and freezes the
checkpoint frequency/monomial pivot order.  It builds the echelon basis once.
Each later CEGAR round inserts only the newly exposed equations into that basis,
then back-substitutes and replays the candidate against every accumulated
column.

The fixed order makes incremental insertion exact: every normalized basis row
contains only rows later in the same total order, so inserting and reducing a
new equation preserves row-echelon form.  At startup the order and sorted
column sequence match the last full rebuild, and the reconstructed candidate
must equal the pinned 178-row dual byte-semantically before the first global
scan.  A mismatch fails before progress.

The synthetic engine selftest proves equality to the original full rebuild,
exact replay after an incremental equation, and detection of inconsistency.
It does not claim a literal-production speedup: that measurement is deliberately
held for the authorized one-branch slice.

## Control-flow repair

`run_single_resume.py` has no branch loop.  It launches one process and
classifies output semantically:

- a global modular dual or modular member is terminal diagnostic evidence;
- `INCOMPLETE_WALL_CAP` is accepted only as a restart checkpoint with zero
  mathematical coverage;
- every other status fails closed.

The runner requires progress beyond 15,273 columns and exact input/source/
binary/watchdog hashes.  Its six-case selftest rejects the former error mode:
an incomplete checkpoint cannot be relabelled terminal and cannot advance to
another branch.  Eight hostile contract mutations are independently rejected.

## Closure estimate

The prior triangle branch completed at:

| degree | rounds | selected columns | support | wall |
|---:|---:|---:|---:|---:|
| 6 | 210 | 439 | 14 | 0.735475 s |
| 7 | 217 | 1,943 | 23 | 3.328478 s |
| 8 | 225 | 4,309 | 52 | 41.277818 s |
| 9 partial | 434 | 15,273 | 178 | 175.758071 s |

D9 has changed regime.  In its final 25 recorded rounds it added 3,028 columns,
and every round still exposed 84--162 violations (median 118); there is no
observed approach to a zero-violation scan.  A low-confidence planning scenario
is 20,000--35,000 columns and 500--700 total rounds.  With the legacy repeated
rebuild, that corresponds roughly to 240--600 seconds total wall, but there is
no evidence-based finite upper bound.  The only hard wall statement is the
already measured 175.758071-second lower bound.

The optimized slice is capped at 175 native / 180 wrapper seconds and 8 GiB.
Its output is restartable, so failure to close no longer discards arithmetic.
No throughput or closure projection for the new path is promoted until this
single literal slice is measured under an explicit resource handoff.

## Scope

- frozen command: `python3 computations/unaudited-codex-n8-x5-four-blocker-d9-resumable-single-branch-design-2026-08-25/run_single_resume.py --run`;
- current status: held, never launched;
- no second prime, exact Q lift, other X5 branch, D10, or D12 cache read;
- the D6--D8 exact obstructions remain unchanged; D9 remains open.
