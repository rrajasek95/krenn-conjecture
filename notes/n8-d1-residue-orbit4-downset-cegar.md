# O4 downset CEGAR frontier

This checker applies only independently verified algebraic atoms to the full
`8,100`-fibre support shadow below the `193`-cell O4 chart.  It specializes
before Tseitin expansion and freezes a `225,759`-variable, `1,347,210`-clause
CNF.  The packets include the injective-tripod and six-site consequences,
four-star minor charts, target-alignment and boundary-star quotients, the
dimension-free one-site target-incidence theorem, D1 harm, and the checked
ordinary `U^k`/Laurent-character certificates through the 158-cell layer.

The exact cardinality replay still proves that 35 additional omissions are
impossible.  The first satisfiable bound is 36, so every support of size at
least 158 below O4 is closed by the promoted atoms.  A canonical maximum has
157 live cells, passes the complete support shadow, and yields 4,321 exact
coefficient generators under SHA-256
`2541cf4aa31003a53496be25826d7be1089f10c9039ff14fbfd178aef930177f`.
This checkpoint intentionally freezes that next coefficient input rather than
claiming that the support-SAT model is coefficient-feasible.

The decisive new support mechanism is an upward repair chart.  Each of two
different coefficient identities remains valid after adding any cells except
for a checked nine-cell visible set; all symmetry transports of both charts
are present.  Together with the earlier finite atoms, these charts make the
entire 158-cell layer UNSAT.  The first 157-cell face is now also closed by a
third repair chart with the same nine visible cells and a new witness
localization.  The next maximum is the first face whose complete one- and
two-class character system was torus-consistent.  The later five-cell
affine/homogeneous atom from `d0aa9b5` is now promoted through its four
distinct transported clauses; it replaces the canonical 36-omission maximum
without increasing the minimum.  That replacement face is closed separately
by the generic affine-tail certificate documented in
`n8-d1-residue-orbit4-157-affine-tail-collision.md`.  This is not yet a proof
for every deeper O4 downset face.

Reproduce with:

```bash
.venv/bin/python computations/verify_n8_d1_residue_orbit4_downset_cegar.py
.venv/bin/python -O computations/verify_n8_d1_residue_orbit4_downset_cegar.py
```

Frozen CNF SHA-256:
`69e5da4b5866e5b2bcf8cb9bb80a19a8a4927c84a5bf4ce7235e2bd8f11fb11b`.
Frozen ledger SHA-256:
`df38068abd9b957303026fac1153736a688c65144ca390f21c6b205a634af57d`.
