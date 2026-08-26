# Rep5 second guard-pivot quotient: rank stratification

Status: **PASS exact nine-stratum design; zero solves**.

Let `v=row_0(A37)` and let `u_i=row_i(A06)` in the frozen p00 Cramer chart. The literal Cramer formulas give `u_0·v=0`, `u_0·w=d*abar`, and `u_m=t_m(w×v)` for `m=1,2`. Therefore

`u_0 × u_m = -t_m*d*abar*v`,

so on either open `t_m!=0` the already saturated factors make `A06` rank two with kernel exactly `span(v)`. Every other row of `A37` is forced proportional to `v`. Using the existing combined inverse eliminates four `A37` variables. All six remaining first guards become tautologies, and all six remaining second guards become multiples of the three pivot-row guards already removed by the `b_k` quotient. Each open system is therefore 84 variables and 6,562 generators: 6,561 full-X5 equations plus one combined saturation.

The complementary closed stratum is exactly `t1=t2=0`. Substitution removes those two variables and the four identically-zero first guards, leaving 86 variables and 6,570 generators. For each `b_k` chart, the two opens plus this closed quotient are exhaustive. Across `k=0,1,2`, nine exact Q inputs cover the original p00 chart.

The consumed modular k0 attempt is pinned only as zero-coverage evidence and is not reused. No source was executed, and there is no performance, closure, or rep5-completion claim.
