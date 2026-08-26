# Rep1 groups 88--137 exact-Q terminal referee

Verdict: **PASS_ALL_50_EXACT_Q_UNIT_IDEALS**.

The frozen dependency adapter independently reconstructs the exact closed union 0--87. The strict batch then closes groups 88--137 in order: every one of the 50 rational lanes has 91 variables and 6,577 generators, returns a one-element Groebner basis, reduces 1 to zero, exits normally, and stays below the frozen 240-second native and 8 GiB RSS limits. There was no skip, reorder, relaunch, overlap, or group beyond 137.

The promoted exact scope is therefore rep1 groups 0--137 (138 of 162 canonical groups). Groups 138--161 remain open. This does not close the rep1 representative, the seven-block family, or the conjecture.

Aggregate lane wall time was 1,460.356265 seconds; the maximum single-lane wall time was 50.779107 seconds and maximum peak group RSS was 797,458,432 bytes.
