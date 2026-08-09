# O4 158-cell initial odd dependency

This maximum-support O4 face is decided at the first tier of the exact
quotient-character oracle.  Its 74 unique plus binomials have exponent rank
26.  Of the 48 integral dependencies, exactly one has character `-1`; it uses
only three rows with coefficients `(1,-1,1)`.

Expanding that dependency through the three original binomials gives the
Laurent constant `2`.  The checker clears all denominators and verifies an
ordinary `U^1` identity with three source generators.  The certificate is
valid in characteristic not two, in particular over `C`.  Its support clause
has four distinct O4 transports, each with stabilizer multiplicity two.

A second maximum-support face has the same three-row shape, now with dependency
coefficients on rows `(36,72,73)`.  Its Laurent constant `2` expands to a
different three-generator ordinary `U^1`.  It contributes four more O4
transports, again with multiplicity two.

This face is therefore still inside the exact `<=2`-class character criterion
and is substantially cheaper than the later parallel-edge collision.

Reproduce with:

```bash
python3 computations/verify_n8_d1_residue_orbit4_158_initial_odd_dependency.py
python3 -O computations/verify_n8_d1_residue_orbit4_158_initial_odd_dependency.py
```
