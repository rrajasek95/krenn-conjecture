# Independent rep1 guard-minor quotient referee

Status: **PASS exact design only; representative 1 remains open.**

The localized equivalence is exact.  From `A06*v=0`, `A06*w=alpha*e_i`, and nonzero `alpha`, the vectors `v,w` are independent.  Since the chart already has `v_q != 0`, the two minors involving `q` cover it.  On either minor chart, coefficient-wise polynomial replay confirms all nine Cramer formulas give `A06*v=0` and `A06*w=d*abar*e_i`; the separate `y` and `z` partner substitutions each solve exactly three entries.  The saturation `abar*beta*A47[pq]*d*sat-1` is precisely the product of every denominator used.  Exactly the three guard equations for row `p` become tautologies.

An independent simultaneous-color census gives 972 raw refined charts and 162 free `S3` orbits, split 81/81 by partner kind, with one all-equal-y minor orbit.  The independent ledger gives 91 variables (`78+13`) and 6,577 generators (`6561+6+9+1`).  The producer manifest replays exactly.  No ideal was run, no representative was closed, and no D12 artifact was read.

`RESOURCE_PLAN.json` is held, not launched.  It permits at most the single materialized all-equal-y lane over `F_32003`, under 300-second native / 310-second wrapper / 8-GiB RSS caps.  Every terminal outcome remains diagnostic only; no second modular lane or exact-Q lane is authorized.
