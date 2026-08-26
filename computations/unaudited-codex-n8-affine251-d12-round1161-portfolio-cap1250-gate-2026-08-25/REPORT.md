# Round 1161 portfolio and 1.25M cap gate: PASS

The independent Poincaré/round-1160 audit sealed the exact 959,506-column/support-990 input: checkpoint `23d91d21...`, vector cache `e622054e...`, and manifest `e56759b6...`. The launch interlock independently rehashed those artifacts before any clone or solve.

The six-way auto/best tree portfolio again selected cold/rare. Round 1161 has 961,803 columns (+2,297), support 998, and 522 newly incident support rows. The portfolio used 110.922 seconds and peaked at 25,618,272 KiB; the fixed replay used 58.075 seconds and 12,344,160 KiB. Both stayed below their independent 120-second/36-GiB watchdogs and produced byte-identical checkpoint and vector cache.

Because cold/rare remained selected, the conditional 1.25M-cap replay ran from the same input. It used 57.387 seconds and 12,339,120 KiB. After output-directory normalization, its command differs from the fixed control only at `--column-cap 1000000 -> 1250000`; its semantic round record and output checkpoint/cache are exact matches. The selected hashes are checkpoint `e7d53052997394ee...` and vector cache `0df2928faf351531...`.

Verdict: `PASS_EXACT_ROUND1161_PORTFOLIO_AND_CONDITIONAL_CAP_EQUIVALENCE`. This authorizes only a production command/config change to the 1.25M cap. Production source and prior production state were not mutated, and no round beyond 1161 ran.
