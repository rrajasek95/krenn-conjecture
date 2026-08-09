# N=8 D1: four additional checked ten-cell support cores

The checker `computations/verify_n8_d1_m10_additional_core_rups.py`
rigorously closes four more complete `m=10` support-base families.  They are
the lex-first `3+4`, lex-first `4+3`, and first two `4+4` support-pair orbits,
with exactly three, three, two, and two further off-Sigma cells respectively.
Each CNF is the exact 16-fibre relaxation frozen at the first frontier: UNSAT
for this weaker support-only system closes every anchor-unit branch over the
given base.

Glucose 4.2 only generates candidate traces.  The committed certificates are
deletion-free DRUP streams with 931, 717, 345, and 172 additions.  The
standard-library checker reconstructs each input, pins its DIMACS and proof
hashes, checks every addition by reverse unit propagation using the already
pinned independent two-watch implementation, and requires a final checked
empty clause.  Normal and optimized Python execute the same checks:

```text
python3 computations/verify_n8_d1_m10_additional_core_rups.py
python3 -O computations/verify_n8_d1_m10_additional_core_rups.py
```

The checker also maps the four support bases back into the structural
audit's anchor-state quotient and reruns the exact repair-DNF classifier.
The `3+4` and first `4+4` bases were already closed there.  The `4+3` and
second `4+4` bases were genuine symbolic survivors, so these certificates
close two additional branches.  Combined with the first `3+3+4`
certificate, three of the original 271 repair-DNF survivors are now closed;
the conservative remaining `m=10` frontier is at most 268 branches.

The optional deterministic generator requires `python-sat`:

```text
.venv/bin/python computations/generate_n8_d1_m10_additional_core_drups.py
```

Frozen checked-ledger SHA-256:
`bf4a7452e2da1e3b4815b240cec961c1485205ed33609a27fe65434abd7fd00b`.
