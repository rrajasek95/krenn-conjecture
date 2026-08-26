# X5 four-blocker staged homogeneous degree-nine gate

## Verdict

The degree-nine gate is terminal **fail closed with zero mathematical
coverage**.  The first coloured branch reached its sealed 175-second native
wall cap after 15,273 selected columns and 434 CEGAR rounds.  Its emitted
178-entry vector annihilates the selected subsystem, but the producer did not
finish the global incident-column test.  It is therefore neither a modular
degree-nine obstruction nor a characteristic-zero certificate.

No second-prime run, direct branch, rational lift, or degree-ten computation
was launched.  The established exact D6--D8 obstructions are unaffected; this
package establishes no D9 theorem and does not close the conjecture.

| role | branch | status | selected | support | engine wall | peak RSS | accepted coverage |
|---|---|---|---:|---:|---:|---:|---:|
| authoritative staged attempt | triangle endpoint colour | `INCOMPLETE_WALL_CAP` | 15,273 | 178 | 175.758071 s | 528,656 KiB | 0 |
| rejected control-flow overrun | cap endpoint colour | `INCOMPLETE_WALL_CAP` | 10,117 | 87 | 175.843385 s | not retained | 0 |

## Fail-closed control-flow audit

The initial watchdog treated process return code zero plus an atomic result as
success without checking the result's semantic status.  Consequently the
initial staged runner began the cap-colour branch after the triangle branch
had returned `INCOMPLETE_WALL_CAP`.  The runner was interrupted, but that
engine was in its own process session and reached its native cap before the
approved termination could act.

Both historical scripts and their schedule are retained in
`rejected_control_flow_v1/`.  The cap-colour output is retained there as
rejected diagnostic evidence and contributes zero coverage.  The superseding
watchdog accepts only the two explicit terminal modular statuses; the
superseding runner also checks this semantic status before advancing.  Nothing
was relaunched after the defect was found.

## Independent literal audit

`validate_failure.py` reparses the separately pinned literal provider for each
attempt.  It reconstructs and replays all 15,273 authoritative selected
columns and all 10,117 rejected selected columns against the respective
finite-field vector; all 25,390 selected pairings vanish.  It also proves that
the remaining two first-prime directories, all four second-prime directories,
all exact-lift directories, and the lift result are absent.

The audit passes under standard and isolated Python with identical output,
fails closed under optimized Python, and rejects five hostile attempts to
invent completion, globality, exact replay, the wrong degree, or the wrong
prime.  These checks validate the diagnostic records only: a selected-system
dual is not a global dual.

## Feasibility conclusion

At D8 the slowest complete branch required 41.411 seconds, 4,309 selected
columns, and 227,824 KiB.  At D9 the very first coloured branch was still
incomplete after 175.758 seconds with 15,273 columns and support 178.  Thus the
observed D9 work already exceeds D8 by more than 4.2 times in wall and 3.5
times in selected columns, without supplying a completion-time projection.
The direct branch was correctly withheld because the coloured phase did not
pass its bound.

Any D9 continuation needs a separately authorized algorithmic or resource
gate; simply widening this staged run is not justified by the present data.
D10 remains explicitly out of scope.
