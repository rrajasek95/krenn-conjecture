# Failed cap-4.25m candidate attempt 1

Verdict: `REJECT_HARD_WALL_ZERO_COVERAGE`.

The approved candidate was killed by the hard 180-second watchdog at
181.729543 seconds (`WALL_CAP`, return code -15). No result or temporary output
exists, stdout/stderr are empty, and the checkpoint/cache remain byte-identical
to the audited round-1639 input. Therefore the attempt contributes zero accepted
coverage and no round-1640 state.

The watchdog's `atomic_outputs_clean` field is false because no final result was
published; the stronger abort guard `abort_final_output_absent=true` holds and no
partial final output was accepted. The unchanged clone is not resumable as a
candidate result. Any retry requires a separately approved resource-only
contract and a distinct fresh clone. No relaunch or round 1641 is authorized by
this seal.
