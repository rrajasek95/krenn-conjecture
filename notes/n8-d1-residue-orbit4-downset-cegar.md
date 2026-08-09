# O4 downset CEGAR frontier

This checker applies only independently verified algebraic atoms to the full
`8,100`-fibre support shadow below the `193`-cell O4 chart.  It specializes
before Tseitin expansion and freezes a `225,759`-variable, `1,347,074`-clause
CNF.  The algebraic packets are the injective-tripod/six-site consequences,
the 576 four-star minor-chart clauses, the 384 target-alignment clauses, the
boundary-star quotient, the global one-site target-incidence theorem, and the
support-faithful D1-harm equivalence.  It now also contains the four distinct
automorphism transports of the checked 159-cell odd-circuit face clause.

The exact maximum-support model has 34 additional omissions and 159 live
cells.  Bound 33 is UNSAT and bound 34 is SAT.  There are no additional
residue holes: the residue tensor remains in the generic maximal O4 family,
all 24 checked tripod-minor charts remain live, and both `c,e` alignment flags
are non-target.

The one-site incidence theorem forces an active target-only arc for every
site and every colour.  The canonical frontier has exactly one such arc per
`(site,colour)`.  Colours 0 and 1 both contain the mutual edge `0<->1`, while
colour 2 contains `6<->7`; every other arc feeds one of these directed cycles.
The new canonical maximum after the odd-circuit clauses has the same three
mutual edges and a complete 24-arc graph, but is not in the killed face's
four-element clause orbit.

This is a finite incidence-graph frontier, not yet an O4-downset closure.  In
particular the successive maximum models need not form a single inclusion
chain, so the checker does not claim a global total termination order.  The
remaining task is a coefficient obstruction for this next incidence face.
The exact coefficient input has 4,321 generators under SHA-256
`44468c0d48b0afb2d23f383864ca76c85d4689d173fcb7ad95714268458d339d`.

Reproduce with:

```bash
.venv/bin/python computations/verify_n8_d1_residue_orbit4_downset_cegar.py
.venv/bin/python -O computations/verify_n8_d1_residue_orbit4_downset_cegar.py
```

Frozen CNF SHA-256:
`462754968bc95836a021d2b75d639b2eb89b85f73d60975606b44b4fb1ffa09f`.
Frozen ledger SHA-256:
`f7098bdf1092ac6e5bfd58e4af3402b852b47538a92eafef61d97c2d6053befe`.
