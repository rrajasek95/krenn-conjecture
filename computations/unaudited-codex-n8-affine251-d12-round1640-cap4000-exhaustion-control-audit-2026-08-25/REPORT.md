# Independent r1640 lower-cap control referee

Status: **PASS_LOWER_CAP_EXHAUSTION_CONTROL**.

The cap-4.0m lane returned `COLUMN_CAP` at the unchanged r1639 state: 3,968,369 columns, support 32,704, zero round records, all 3,968,369 cached vectors loaded, no vectors materialized on restore, and zero cache-write time. The independently hashed checkpoint and 8.58 GB cache are byte-identical to the sealed r1639 inputs (`ab63c220...` and `4d342801...`). No temporary or dual output exists and both logs are empty.

The exact command is the frozen cold/rare/16 hierarchical nonincremental engine with `--column-cap 4000000 --round-cap 1640`. The watchdog passed atomically in 72.368616 seconds at 20,924,976 KiB, below 180 seconds/36 GiB, with no breach. Together with the approved static source theorem, this proves the deterministic whole r1640 incident set exceeds the 31,631 remaining cap-4.0m slots and that the control returned before column arithmetic without changing state.

The cap-4.25m candidate directory remained absent throughout this referee. This package validates only the lower-cap witness; it does not itself authorize candidate arithmetic, accept an r1640 state, or authorize r1641.
