# N=8 D1: exact closure of the seven-cell support frontier

The anchor-normal-form audit in commit `6558cbf` reduced every D1 support
with exactly seven nonzero cells outside Sigma to 22 support orbits.  None of
those orbits passes the necessary Boolean support shadow.

The checker
`computations/verify_n8_d1_m7_support_shadow_closure.py` imports and hashes
that committed normal-form audit, reconstructs its 22 representatives, and
specializes the matching equations to each fixed off-Sigma support.  For
each representative it freezes a core of 7--14 full eight-site fibres.  A
monochrome fibre must contain a supported matching; a mixed fibre may contain
zero or at least two, but never exactly one.  These are necessary conditions
for the corresponding integer polynomial coefficients to have the required
target values.

The checker independently rebuilds every matching conjunction and every
``not exactly one`` constraint.  Its Tseitin clauses are exact equivalences.
The resulting cores use 42--71 variables and 98--214 clauses.  Deterministic
unit propagation derives a conflict in every case (35--63 propagation steps),
so the empty clause is RUP for each core.  This verification uses only the
Python standard library; the native SAT solver used to discover the small
cores is not part of the certificate or the trusted runtime.

Consequently all 22 support orbits, hence all 26 surviving anchor-unit
branches, are empty before any numerical coefficient ideal is considered.
Together with the exact six-cell closure in commit `f5c43d3`, D1 now requires
at least eight nonzero aggregate cells outside Sigma.  This closes the
`m = 7` stratum only; the D1 loci with `m >= 8` remain open.

Run:

```text
python3 computations/verify_n8_d1_m7_support_shadow_closure.py
python3 -O computations/verify_n8_d1_m7_support_shadow_closure.py
```

Frozen ledger SHA-256:
`4474bb261b5ff2581e7f50df3883faa8c432cc1f85064e047a210432d8ff98a7`.
