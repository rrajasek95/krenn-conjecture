# Grouped D15 R4-2 K21 charge

Status: `PASS_INDEPENDENT_TERMINAL_REFEREE_GROUPED_D15_R4_2_K21_CHARGE`.

The retained `K15CHK1` checkpoint gives the strict grouped scalar for exactly
`D15:{223,232,322}|R:4-2`. Full equals irreducible charge is
`-105580126744994119680/U = -2333827745792/8855`, with
`U=400591699200`. The source checkpoint aggregates the three lineages, so no
individual-ID scalar is claimed.

Eleven atomic intervals cover `[0,5311211)` with no gap or overlap. They check
44,342,881 first pivots, 2,660,572,860 K4 candidates, 972,495,600 retained
pivotable K19 children, 1,549,305,840 second pivots, and 18,591,670,080 K2
tails. Every division by `m1*m2` is exact. The two response signs give
`w19=-w15*U/m1` and `w21=-w19/m2`.

All K21 outputs are terminal: anchor sum `9-4+0-4+2=3`, while every K0 pivot
has sum 4. An independent evenly distributed 257-parent replay checked 889,920
literal K21 children, including literal/abstract cycle keys and terminal child
signatures. Missing, duplicate, and reordered grouped-ID interfaces are
rejected.

The maximum shard took 67.003 seconds. The largest sampled live RSS was
4,430,144 KiB, below the 180-second/8-GiB shard guard. Scope excludes all
other K21 paths and any conjecture verdict.
