# Representative 1 incidence-pivot quotient

Status: **exact contraction design PASS; representative 1 remains open.**

On a chart with `x_r != 0`, partner witness component `q_s != 0`, and outside entry `A47[pq] != 0`, normalize `x` and `q` by those components and set `alpha=1/x_r`, `beta=1/q_s`. The equations `A06*x=e_i` solve the three entries in column `r` of `A06`; `A13^T*y+A35*z=e_i` solves either row `s` of `A13` or column `s` of `A35`. The single equation `alpha*beta*A47[pq]*sat-1` enforces all three chart conditions. Conversely, divide the normalized witnesses by `alpha` and `beta` to recover an original incidence solution. Thus each localized quotient is exactly equivalent to its original open chart.

There are 486 raw choices `(i,p,q,r,kind,s)`. Exact simultaneous `S3` color action gives 82 orbits: 41 with a `y` pivot and 41 with a `z` pivot. Orbit sizes are two orbits of size 3 and 80 of size 6. This exhaustive ledger proves the chart union covers every original incidence obstruction because both witnesses are necessarily nonzero and the outside factor is in the already-saturated nonzero branch.

The quotient has 94 variables and 6,580 generators, compared with 100 and 6,586 previously. It removes six source entries and all six explicit incidence equations; the normalized witness/scale parameter counts equal the original witness counts. Full X5, the 18 stored guard equations, and the combined saturation remain exact. Only the all-equal `y` chart is materialized for a bounded modular diagnostic; no chart is claimed closed by the diagnostic.

## Tiny diagnostic outcome

After explicit resource clearance, the one sealed modular chart ran under the 15-second/4-GiB diagnostic gate. It reached `WALL_CAP_15` at 15.05 seconds with 1,978,114,048 bytes observed peak RSS. Singular confirmed `INPUT_GENERATORS=6580` but returned neither unit nor nonunit status. This is zero mathematical coverage; no other chart or exact-Q lane ran. The contraction design remains exact and useful, while representative 1 remains open.
