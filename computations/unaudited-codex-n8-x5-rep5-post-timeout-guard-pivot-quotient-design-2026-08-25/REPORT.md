# Rep5 post-timeout exact guard-pivot quotient

The consumed 91-variable/6,577-generator p00 chart is not relaunched. Its
remaining guard equations imply a strict three-chart cover. Put
`b_h = row_h(A26)·row_p(A37)` and
`P = abar*beta*A37[p,q]*d`. The `j=p,i=q` guard and `A37[p,q] != 0` force at
least one `b_k != 0`.

On chart `b_k != 0`, all three entries `A17[i,k]` are eliminated by
`A17[i,k] = (A37[p,i] - sum_{h!=k} A17[i,h]b_h) P sat`, with combined
saturation `P*b_k*sat-1`. The three removed guards equal
`N_i(1-P*b_k*sat)`, so they are redundant exactly. Forward and reverse maps
are obtained by `sat_new=sat_old/b_k` and `sat_old=b_k*sat_new`.

Each of the three Q design inputs has 88 variables and 6,574 generators. The
three `k` charts cover the parent without assuming a symmetry transport. No
Singular run, order-performance claim, parent relaunch, or closure claim occurs.
