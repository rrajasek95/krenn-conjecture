# Independent terminal referee: rep1 next25 exact-Q

Verdict: **PASS_ALL_25_EXACT_Q_UNIT_IDEALS**.

The exact scheduled IDs `[11,12,14,16,...,37]` ran once, sequentially, and in the frozen order. Every lane independently replays as a 91-variable, 6577-generator exact-Q computation with `GROEBNER_SIZE=1`, `UNIT_REMAINDER=0`, wrapper return code zero, empty stderr, and no termination event. There were no skips, relaunches, parallel lanes, temporary outputs, or groups beyond 37.

Aggregate lane wall time was 666.516905 seconds; the maximum lane wall time was 46.787682 seconds and maximum observed RSS was 773,996,544 bytes, below the frozen 240-second and 8-GiB per-lane gates.

Scope is deliberately narrow: these 25 refined rep1 orbits are closed. This does not close the rep1 representative, the seven-block family, or the conjecture.
