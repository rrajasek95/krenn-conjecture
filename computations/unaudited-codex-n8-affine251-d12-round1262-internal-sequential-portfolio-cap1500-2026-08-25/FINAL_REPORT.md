# Round 1262 internal sequential portfolio: PASS

The built-in sequential six-task portfolio passed in 258.220 seconds at peak 19,403,696 KiB and selected cold/rare. Round 1262 has 1,240,851 columns (+2,310), support 1,098, and 567 new support rows.

The fixed replay passed in 74.150 seconds at 14,575,808 KiB; the 1.5M-cap candidate passed in 74.131 seconds at 14,575,920 KiB. All three semantic round records, checkpoints, and vector caches agree exactly. The accepted checkpoint is `2d9f65c9...`; the accepted vector cache is `00437f95...`.

After output-directory normalization, the fixed/candidate commands differ only at `--column-cap 1250000 -> 1500000`. Both failed parallel attempts remain zero-coverage artifacts. No round beyond 1262 ran and production was not mutated.
