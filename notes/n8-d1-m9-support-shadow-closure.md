# N=8 D1: exact closure of the nine-cell support frontier

The checker
`computations/verify_n8_d1_m9_support_shadow_closure.py` proves that a D1
packet cannot have exactly nine nonzero aggregate cells outside Sigma.  The
certificate is finite, solver-free, and pins the committed `m=8` checker.

The one-colour census now runs through size six.  It finds 34,657 valid
six-cell supports, but every one contains one of the already known 72
minimal three-cell or 27 minimal four-cell anchors.  There are no new minimal
normal forms at sizes five or six.  The four two-colour distributions are
therefore `3+3+3`, `3+4+2`, `4+3+2`, and `4+4+1`, with the same 312
anchor-unit orbits as at `m=8`.

Those orbit representatives have 39,907,200 raw choices for the remaining
cells.  Exact unique-fibre repair requirements reduce them to 483,402.  Once
the chosen cells are made mandatory, a second unique-fibre pass kills
481,642 choices: 235,008 residue, 185,187 six-site, and 61,447 full-fibre
certificates.  The remaining 1,760 branch candidates form 1,315 state orbits
over 1,071 support orbits.

Every residual support is then fixed exactly.  The 78-word fibre palette
frozen by the `m=7` closure unit-refutes 442 support orbits.  Deterministic
unit propagation on the complete 8,100-fibre shadow refutes the other 629.
No SAT solver or numerical ideal computation is trusted by this conclusion.

Together with the `m=6`, `m=7`, and `m=8` closures, D1 now requires at least
ten nonzero off-Sigma aggregate cells.  The `m >= 10` strata remain open.

Frozen ledger SHA-256:
`a57e3f9dc2d826b30190897c3cf6c1e84298f2ae47805e6a6fc9cc4a975f5811`.

Run:

```text
python3 computations/verify_n8_d1_m9_support_shadow_closure.py
python3 -O computations/verify_n8_d1_m9_support_shadow_closure.py
```
