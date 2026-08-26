# Independent rep1 group-13 exact-Q referee

Status: **PASS exact-Q unit ideal for canonical group 13 only.**

The producer manifest replays and its exact-Q source is pinned at SHA `336bc28a4affecb31ce32fa468eadb1317efea5fb3ee2d5acbd24fc5f320790a`. Independent parsing finds 91 distinct variables and 6,577 ideal generators. Singular returned normally with basis size one, literal remainder zero, and `STATUS=UNIT_IDEAL` in `24.033887499943376` seconds at `497,045,504` bytes peak RSS.

The single-lane scope and resource clearance are correctly bound to the prior terminal rectangle seal. The output was atomic, no temporary output remains, and the package records no second lane, optional three-lane batch, or relaunch. No later group-specific exact-Q package exists in the frozen naming scope.

This closes group 13 only. Together with previously closed group 0, exactly 2 of 162 canonical common-S3 groups are closed; representative 1 is not closed.

`NEXT3_EXACT_Q_HELD_PLAN.json` selects groups 15, 17, and 25 by the previously sealed rule: remaining maximum-source-size groups in canonical group-ID order. It is sequential, at most three lanes, requires fresh materialization and explicit resource clearance per lane, stops on the first non-unit/resource/process failure, and authorizes no launch or relaunch.
