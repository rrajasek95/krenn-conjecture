# O4 downset CEGAR frontier

This checker applies only independently verified algebraic atoms to the full
`8,100`-fibre support shadow below the `193`-cell O4 chart.  It specializes
before Tseitin expansion and freezes a `225,759`-variable, `1,347,110`-clause
CNF.  The algebraic packets are the injective-tripod/six-site consequences,
the 576 four-star minor-chart clauses, the 384 target-alignment clauses, the
boundary-star quotient, the global one-site target-incidence theorem, and the
support-faithful D1-harm equivalence.  It now also contains the four distinct
automorphism transports of the checked 159-cell odd-circuit face clause.
It additionally contains all eight transports of the second incidence face's
explicit ordinary `U^1` coefficient certificate.
The third and fourth 159-cell faces contribute eight integral `U^2` clauses
and four odd-circuit `U^3` clauses.  Finally, a two-face batch contributes 16
integral `U^1` clauses on the 158-cell layer.

The entire 159-cell layer is now closed: bounds 33 and 34 are UNSAT.  The
exact maximum-support model has 35 additional omissions and 158 live cells;
bound 35 is SAT.  The first two 158-cell maxima are also coefficient-empty,
but a third exact 158-cell frontier remains after their transported clauses.

The one-site incidence theorem forces an active target-only arc for every
site and every colour.  The canonical frontier has exactly one such arc per
`(site,colour)`.  Colours 0 and 1 both contain the mutual edge `0<->1`, while
colour 2 contains `6<->7`; every other arc feeds one of these directed cycles.
The current canonical maximum passes the full support shadow.  Its direct
signed-Laurent oracle has 54 unique plus rows of rank 20, 34 even-character
dependencies, and no one-class generator.  This is a frozen open coefficient
frontier, not a claimed point.

This is a finite incidence-graph frontier, not yet an O4-downset closure.  In
particular the successive maximum models need not form a single inclusion
chain, so the checker does not claim a global total termination order.  The
remaining task is an iterated two-class or transfer/holonomy obstruction for
this next incidence face.
The exact coefficient input has 4,321 generators under SHA-256
`7097b288a7a41be1fe4abb42ee8de20f49c5e69a2a1f720268ac7568b02aa9ce`.

Reproduce with:

```bash
.venv/bin/python computations/verify_n8_d1_residue_orbit4_downset_cegar.py
.venv/bin/python -O computations/verify_n8_d1_residue_orbit4_downset_cegar.py
```

Frozen CNF SHA-256:
`f96facf2be0ebbffcb05fff17128bf98d9dd62228b18a1bcf28e70ae014c3cea`.
Frozen ledger SHA-256:
`b00199e9eab9b0ffa3a9698411a0cc8469d470c629f06548011cf359793d65d0`.
