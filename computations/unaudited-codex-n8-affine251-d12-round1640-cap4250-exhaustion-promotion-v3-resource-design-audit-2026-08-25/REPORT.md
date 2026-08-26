# Independent referee: r1640 v3 resource-only amendment

Status: **PASS_PRELAUNCH_RESOURCE_ONLY_AMENDMENT_APPROVED_HELD**.

The v3 proposal changes exactly two resource literals relative to the failed cap-4.25m candidate: native wall 150→210 seconds and hard wrapper 180→240 seconds. Source `3139689f...`, binary `79410bc8...`, watchdog implementation `75bccbb6...`, prime, cap 4.25m, round 1640, RSS 36 GiB, cold/rare/16 hierarchical nonincremental mode, and the approved v2 proof/control bindings are unchanged. The wrapper’s sealed upper bound accepts 240 seconds; a hard wrapper breach remains rejection and this is not a generic wall relaxation.

Attempt 1 is independently classified `REJECT_HARD_WALL_ZERO_COVERAGE`: watchdog `WALL_CAP`/SIGTERM at 181.729543 seconds, no result or temporary output, empty logs, and checkpoint/cache pinned to the audited r1639 bytes. It made no accepted mathematical state and is evidence only. Resume, copy, or reuse is forbidden.

Any separately cleared attempt 2 must be a distinct fresh clone directly from audited r1639, and its solver command may differ from attempt 1 only at native wall 150→210; the wrapper invocation may differ only at hard wall 180→240. The full inherited-byte, strict-descendant, target-1/all-column replay, atomicity, r1640-only, and independent postrun requirements remain unchanged. This referee does not authorize arithmetic: manager clearance, an immediate 88,080,384-KiB storage gate, and a frozen launch record are still required.
