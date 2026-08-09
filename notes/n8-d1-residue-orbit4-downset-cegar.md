# O4 downset CEGAR frontier

This checker applies only independently verified algebraic atoms to the full
`8,100`-fibre support shadow below the `193`-cell O4 chart.  It specializes
before Tseitin expansion and freezes a `225,759`-variable, `1,347,206`-clause
CNF.  The packets include the injective-tripod and six-site consequences,
four-star minor charts, target-alignment and boundary-star quotients, the
dimension-free one-site target-incidence theorem, D1 harm, and the checked
ordinary `U^k`/Laurent-character certificates through the 158-cell layer.

The exact cardinality replay still proves that 35 additional omissions are
impossible.  The first satisfiable bound is 36, so every support of size at
least 158 below O4 is closed by the promoted atoms.  A canonical maximum has
157 live cells, passes the complete support shadow, and yields 4,321 exact
coefficient generators under SHA-256
`00839fab040697522574a57f3529eb2968247eaa0b2ab49d2eadaf4795cf17d4`.
This checkpoint intentionally freezes that next coefficient input rather than
claiming that it is feasible.

The decisive new support mechanism is an upward repair chart.  Each of two
different coefficient identities remains valid after adding any cells except
for a checked nine-cell visible set; all symmetry transports of both charts
are present.  Together with the earlier finite atoms, these charts make the
entire 158-cell layer UNSAT.  The first 157-cell face is now also closed by a
third repair chart with the same nine visible cells and a new witness
localization.  The next maximum is the first face whose complete one- and
two-class character system is torus-consistent; its exact parametrization is
frozen separately.  This is not yet a proof for every deeper O4 downset face.

Reproduce with:

```bash
.venv/bin/python computations/verify_n8_d1_residue_orbit4_downset_cegar.py
.venv/bin/python -O computations/verify_n8_d1_residue_orbit4_downset_cegar.py
```

Frozen CNF SHA-256:
`f4e71a981d8c01299b94fe59fc518c0162b3c4d6b6d747114da6a79ad70a1c10`.
Frozen ledger SHA-256:
`8e6066422a0f8d4db41316868205a77bae1e359808d14b5482f9c33bf2fd5cc5`.
