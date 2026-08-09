# D1 O4 157-cell affine/homogeneous fibre unit

`computations/verify_n8_d1_residue_orbit4_157_affine_homogeneous_unit.py`
closes the first nonlinear, torus-consistent 157-cell O4 frontier.  The
checker reconstructs every reduction from the committed 4,321-generator
coefficient input; it does not use the exploratory shape script or a solver
verdict.

## Collision

In the exact rank-39 Laurent quotient, source record 5 is

\[
 -1+R,\qquad
 R=x_{45,22}x_{67,22}+x_{46,22}x_{57,22}
   +x_{47,22}x_{56,22}.
\]

Record 2960 reduces to

\[
 \frac{x_{06,02}x_{13,22}x_{27,01}}{x_{67,22}}R.
\]

Thus the first equation forces the residue three-matching fibre to be one,
while the second forces the same fibre to vanish after multiplication by a
localized external factor.  The checker reconstructs both normal forms from
the 97 exact character rows, including the six checked resultant relations,
and subtracts their ordinary-source certificates.

After clearing Laurent denominators, the result is an integral ordinary
\(U^1\) certificate.  It uses 10 source generators, has 24 cofactor terms,
and has frozen certificate SHA-256

```
86e87bc812c60e75227504f5eca72b794cbd69adbf91538e6d080373ab0d5817
```

Because the final identity has integral coefficients and target \(U\), the
closure is valid in every characteristic.

## Upward support atom

The 10 sources use 24 localized witness cells.  The residue-purity source
already contains all three residue perfect matchings, so support additions
cannot alter it.  Exact enumeration of possible new matchings in the nine
full-output sources gives precisely five singleton repair masks:

```
x06_00, x07_01, x07_02, x26_10, x27_12.
```

Consequently, whenever the 24 witness cells remain live, every support face
on which all five displayed cells remain absent inherits the same unit
certificate.  Equivalently, coefficient feasibility under the witness
antecedent requires at least one of these five cells.  The checker also
transports this implication under the full eight-element D1 chart symmetry
group and freezes the transported clauses in its ledger.

## Reproduction

Run both interpreter modes:

```
python3 computations/verify_n8_d1_residue_orbit4_157_affine_homogeneous_unit.py
python3 -O computations/verify_n8_d1_residue_orbit4_157_affine_homogeneous_unit.py
```

Both must print ledger SHA-256
`ff7ae6d934617526f41c74baba29ba0d5a259670619dc28092e337ee2c8097cb`
and ordinary saturation `U^1`.
