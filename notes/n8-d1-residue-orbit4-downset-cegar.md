# O4 downset CEGAR frontier

This checker applies only independently verified algebraic atoms to the full
`8,100`-fibre support shadow below the `193`-cell O4 chart.  It specializes
before Tseitin expansion and freezes a `225,759`-variable, `1,347,070`-clause
CNF.  The algebraic packets are the injective-tripod/six-site consequences,
the 576 four-star minor-chart clauses, the 384 target-alignment clauses, the
boundary-star quotient, the global one-site target-incidence theorem, and the
support-faithful D1-harm equivalence.

The exact maximum-support model has 34 additional omissions and 159 live
cells.  Bound 33 is UNSAT and bound 34 is SAT.  There are no additional
residue holes: the residue tensor remains in the generic maximal O4 family,
all 24 checked tripod-minor charts remain live, and both `c,e` alignment flags
are non-target.

Thus the structural state is

The one-site incidence theorem forces an active target-only arc for every
site and every colour.  The canonical frontier has exactly one such arc per
`(site,colour)`.  Colours 0 and 1 both contain the mutual edge `0<->1`, while
colour 2 contains `6<->7`; every other arc feeds one of these directed cycles.
The checker freezes the complete 24-arc graph.

This is a finite incidence-graph frontier, not yet an O4-downset closure.  In
particular the successive maximum models need not form a single inclusion
chain, so the checker does not claim a global total termination order.  The
remaining structural task is the mutual target-only incidence / clean-pair
descent.  The exact coefficient input has 4,318 generators under SHA-256
`63b95d63ff5cbffdce8f2644dc58b65112b7af6d586d515decbb90664f507461`.

Reproduce with:

```bash
.venv/bin/python computations/verify_n8_d1_residue_orbit4_downset_cegar.py
.venv/bin/python -O computations/verify_n8_d1_residue_orbit4_downset_cegar.py
```

Frozen CNF SHA-256:
`96a0b4935c39c322d5dd56494f2d777df2a93910853c41c377cc6a0c1df07cac`.
Frozen ledger SHA-256:
`0aa7863835db16aaa949c8bcbc80eff44c51a835034ff24418e9f6e3aa6d6551`.
