# Representative 1 guard-minor quotient

Status: **strictly smaller exact design PASS; no computation launched.**

Let `v=row_p(A47)` on an outside chart with `v_q=A47[pq] != 0`, and normalize the left incidence witness to `w_r=1`. The original equations give `A06*v=0` and `A06*w=alpha*e_i` with `alpha != 0`, so `v,w` are independent. Therefore at least one of the two minors `d(q,t)=w_q v_t-w_t v_q`, `t!=q`, is nonzero. These two minor subcharts cover the original chart.

On a selected minor chart, put `alpha=d*abar` and scale the third A06 column as `d*t`. Exact Cramer formulas then solve all nine A06 entries polynomially. They make both the incidence equations and the three guard equations against row `p` of A47 tautologies. The combined saturation `abar*beta*A47[pq]*d*sat-1` enforces every division used. Forward and reverse formulas are retained in the metadata.

This lowers the system from the original 100 variables/6,586 generators, through the first quotient's 94/6,580, to **91 variables/6,577 generators**. The full refined union has 972 raw charts and exactly 162 simultaneous-color orbits, 81 per partner-pivot kind; the all-equal-y lane has one minor orbit. No ideal was run.

The ten frozen two-sandwich stars were also re-audited. The only other common-A06 carrier is `A06^T*K*[A45|A47]`, whose partner space is full because `A45=I`; it cannot automatically eliminate the diagonal incidence. This is scoped to the frozen star ledger and is not a no-go theorem for other carrier types.
