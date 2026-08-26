# Round 1527 to 1538 continuation plan

This metadata-only plan starts from the cap2.75m candidate only after independent cap-gate acceptance. It performs no clone, cache read, or arithmetic.

The six planned stages have caps 1529, 1531, 1533, 1535, 1537, and 1538. Blocks are split 3+3, placing each block below 540 seconds even if all three stages consume the full 150-second wrapper limit. The final stage advances one round; all others advance two.

The initial column headroom is 349,663, comfortably above the deliberately conservative 107,070 projection. That projection is recomputed after every stage. Storage admission requires at least 50 GiB free after audit and approved compaction, with a 12 GiB running floor and 6 GiB scratch reserve.
