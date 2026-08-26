# Failed three-round stage

Verdict: **REJECT_WRAPPER_WALL_DURING_CACHE_PUBLICATION**.

The attempt started from the accepted round-1512 pair and logged arithmetic through round 1515, but the 115-second wrapper terminated it at 115.435948 seconds during output publication. No result or complete matching cache exists; the accepted frontier remains round 1512. The failed checkpoint is not resumable.

Recovery uses distinct directories and exact two-round caps 1514, 1516, 1518, 1520, 1522, and 1524, with native90/wrapper115 and all algebraic settings unchanged.
