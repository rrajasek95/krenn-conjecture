# D12 r1640 cap4.25m v3 resource-only amendment — HELD

Status: **HELD_AWAIT_INDEPENDENT_RESOURCE_AMENDMENT_REFEREE_AND_MANAGER_CLEARANCE**. This package authorizes no arithmetic.

The approved v2 cap-exhaustion proof remains unchanged: the independently accepted cap4.0m control returned `COLUMN_CAP` at r1639 with zero rounds and byte-unchanged input, and the frozen source audit proves `column_cap` is consulted only by the pre-arithmetic whole-next-set guard (apart from serialization). The v3 proposal changes only the failed candidate's resource bounds: solver native wall `150 -> 210` seconds and hard watchdog wall `180 -> 240` seconds.

## Failed attempt excluded

Attempt1 is sealed `REJECT_HARD_WALL_ZERO_COVERAGE`. Its watchdog terminated it at 181.729543 seconds; it produced no result or temporary output, and its checkpoint/cache remain the audited r1639 bytes. It contributes no r1640 coverage and cannot be resumed. Evidence is pinned by failure result `924da689...`, report `a2ca34fd...`, and manifest `8152ea7e...`.

Any approved v3 run must use a distinct fresh APFS clone named `candidate_cap4250_v3_attempt2`, made only from audited r1639 checkpoint `ab63c220...` and cache `4d342801...`. The failed `candidate_cap4250` directory is evidence only.

## Exact unchanged scope

Source `3139689f...`, binary `79410bc8...`, watchdog implementation `75bccbb6...`, prime 1073741827, cap4.25m, target r1640, cold/rare/hierarchical/16/nonincremental, no portfolio, and RSS36 are frozen. Relative to attempt1, the two wall literals are the entire diff. Relative to the already-run lower-cap control, the command differs in cap and these independently reviewable resource bounds, so v3 does **not** claim the old sole-cap-diff property.

Native210 is selected because attempt1 exceeded the prior hard wrapper180 and the observed round projects near 200 seconds. Wrapper240 leaves 30 seconds beyond the native cooperative bound for atomic publication. The wrapper implementation itself is unchanged and accepts this bound. A hard wrapper breach remains a rejection; there is no generic wall relaxation.

## Post-run obligations if separately cleared

The candidate must atomically publish exactly r1640, no r1641, with one r1640 record, no temporary output, watchdog PASS below 240 seconds and 36GiB, a checkpoint strict-descendant certificate, all 3,968,369 inherited cache records byte-identical in canonical order, and a full cache replay with normalized target 1 and zero failures. Independent post-run audit remains mandatory.

Free space was 163,314,344KiB while sealing this design, above the 88,080,384KiB floor, but it must be remeasured immediately before any fresh clone. Neither this measurement nor this design is launch clearance.
