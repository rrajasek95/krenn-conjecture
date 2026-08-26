# D12 r1641 final retry3 — SUPPORT_CAP rejection

Status: **REJECT_SUPPORT_CAP_ZERO_COVERAGE_STOP_THIS_GEOMETRY**.

The final authorized retry3 ran under the exact frozen cap4.75m/support200k mathematics with native450/wrapper540/RSS36. The watchdog passed atomically with return code 0, no breach, 505.836726 seconds elapsed, and peak RSS 27,407,936KiB below 36GiB.

The solver did not reach r1641. It published `INCOMPLETE_SEARCH_CAP/SUPPORT_CAP`, retained `rounds_completed=1640`, and emitted no round record or dual. The fold exposed 4,293,039 columns: 223,328 beyond the 4,069,711-column audited input. Its computed next support was 464,887, exceeding support cap 200,000 by 264,887.

This failure leaves a quarantined hybrid: the checkpoint remains labeled round1640 with the old 76,616-entry candidate but now contains all 4,293,039 exposed columns, and the vector cache is extended correspondingly. Their hashes differ from audited r1640. Therefore the artifacts are neither the accepted r1640 input nor an accepted r1641 descendant and must not be resumed or reused.

No temporary output or r1642 exists. Retry3 contributes zero accepted coverage. Per the predeclared final-escalation contract, this geometry is stopped permanently: no fourth wall escalation, relaunch, or continuation is allowed.
