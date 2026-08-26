# Independent referee — rep5 rank-stratified guard-pivot v2

Verdict: **PASS as a corrected design-only nine-stratum cover; zero solver runs and zero new mathematical coverage.**

The v2 package is bound to the prior rejection manifest `8a1c4e5f…`, whose defect was undeclared eliminated A37 names inside already-expanded A35/A36 expressions. The repaired generator constructs raw retained entries first, removes the four off-pivot A37 symbols at that layer, defines the proportional A37 accessor, and only then expands A35, A36, A06, A17, and the 6,561 amplitudes.

All six open sources independently parse as 84 variables and 6,562 distinct generators. Each contains zero occurrences anywhere of `a37_11`, `a37_12`, `a37_21`, and `a37_22`, and has no undeclared identifier. The three complementary sources parse as 86 variables and 6,570 generators and preserve their previously validated hashes.

Independent sparse-integer replay verifies the Cramer dot/cross identities and the cleared-denominator forward/reverse identities for the A17 and proportional-A37 substitutions. For each pivot `k=0,1,2`, the Boolean cases partition into `D(t1)`, `D(t2)`, or `V(t1,t2)`, giving exactly nine strata. This validates only the materialized algebraic design; it does not assert any ideal is unit or that rep5 is closed.
