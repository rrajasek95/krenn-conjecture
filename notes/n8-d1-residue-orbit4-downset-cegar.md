# O4 downset CEGAR frontier

This checker applies only independently verified algebraic atoms to the full
`8,100`-fibre support shadow below the `193`-cell O4 chart.  It specializes
before Tseitin expansion and freezes a `225,759`-variable, `1,347,198`-clause
CNF.  The packets include the injective-tripod and six-site consequences,
four-star minor charts, target-alignment and boundary-star quotients, the
dimension-free one-site target-incidence theorem, D1 harm, and the checked
ordinary `U^k`/Laurent-character certificates through the 158-cell layer.

The exact cardinality replay proves that 35 additional omissions are
impossible.  The first satisfiable bound is 36, so every support of size at
least 158 below O4 is closed by the promoted atoms.  A canonical maximum has
157 live cells, passes the complete support shadow, and yields 4,105 exact
coefficient generators under SHA-256
`45f70f0cb4b3e9e322861b220e2ff4290469ac4bdfe87808f2a0a45df6d8fd27`.
This checkpoint intentionally freezes that next coefficient input rather than
claiming that it is feasible.

The decisive new support mechanism is an upward repair chart.  Each of two
different coefficient identities remains valid after adding any cells except
for a checked nine-cell visible set; all symmetry transports of both charts
are present.  Together with the earlier finite atoms, these charts make the
entire 158-cell layer UNSAT.  This is an exact finite cover at that layer, not
yet a proof for every deeper O4 downset face.

Reproduce with:

```bash
.venv/bin/python computations/verify_n8_d1_residue_orbit4_downset_cegar.py
.venv/bin/python -O computations/verify_n8_d1_residue_orbit4_downset_cegar.py
```

Frozen CNF SHA-256:
`c3c9d31ced2d0befc451bae5818c6a1dc671d20c4ec6cfb8a51f80f30ce1d9aa`.
Frozen ledger SHA-256:
`f6e05bdb27569b2f8c997d72db016983200696de45ec996a3bd6578b35d246df`.
