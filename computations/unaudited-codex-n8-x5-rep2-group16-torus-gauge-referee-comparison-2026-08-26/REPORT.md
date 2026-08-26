# Rep2 group16 torus-gauge independent referee and exact cover comparison

Status: **PASS_TORUS_19_EXACT_AND_SOUND_57_INTERSECTION_ZERO_SOLVES**.

The producer manifest and every pinned source replay.  The determinant-one character
matrix gives a root-free gauge fixing of `beta`, `abar`, and `a57_00`.  Independent
literal reconstruction reproduces all 19 sources byte-for-byte: nine 87-variable,
nine 78-variable, and one 70-variable source, each with 6,577 distinct nontrivial
generators and no removed variable token.  The 14 hostile outcomes pass.  The prior
group16 attempt remains a `NATIVE_WALL_CAP_240` with zero mathematical coverage and
explicit nonreuse.

The three guard-pivot quotients are equivariant after assigning their new inverse
variable weight `(0,-2,-1,0)`.  Since each `b_k` scales by the same nonzero
`lambda56` character, the two covers may be intersected exactly.  This yields 57
sources: 27 at 84/6574, 27 at 75/6574, and 3 at 67/6574.  The gain in per-source
size therefore costs a 57-chart cover; it is not a one-chart closure.

The deterministic smallest exact pilot is `rep2_group016_torus_A67zero_A12zero_guardpivot_k0_Q.sing` (SHA-256
`2403105f5c6bf4860525220d0d2d036099b79ace67297c864767ae71b9e97339`), the 67-variable/6,574-generator `A67=A12=0`, `D(b0)`
intersection.  A UNIT result would close only that localization.  Closing group16
by this combined decomposition requires all 57 intersections unless a separate
exact implication or symmetry reduction is proved.

No Singular process or ideal computation was launched.
