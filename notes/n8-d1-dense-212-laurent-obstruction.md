# N=8 D1: a dense 212-cell Laurent obstruction

The three-binomial certificates on the sparse D1 frontier are not the whole
mechanism.  A valid complete support shadow with 212 of the 217 E1-admissible
cells has no monomial full-output equation and no odd three-binomial circuit,
but its localized coefficient ideal is still empty by a compact Laurent
lattice calculation.

The support omits only

```text
x_67_02, x_67_10, x_67_12, x_67_20, x_67_21.
```

The checker
[`verify_n8_d1_dense_212_laurent_obstruction.py`](../computations/verify_n8_d1_dense_212_laurent_obstruction.py)
reconstructs all 8,100 support fibres and all 8,101 distinct coefficient
generators.  Among 720 plus binomials, nine consecutive full-output equations
have independent Laurent exponent differences.  Exact integer Gaussian
elimination records every basis exponent as an integral combination of those
nine differences and carries the associated `-1` character.

Modulo those nine binomials, full-output generator 5351 reduces from

```text
x_02_20 x_13_20 (
    x_45_00 x_67_00
  + x_46_00 x_57_00
  + x_47_00 x_56_00)
```

to the single Laurent monomial

```text
x_02_20 x_13_20 x_45_00 x_67_00.
```

Every displayed variable is localized nonzero, so the ten equations have no
common torus point.  This argument works in every characteristic, including
two.  No numerical solver, SAT verdict, or Groebner-basis verdict is used:
the checker independently rebuilds all exponent combinations, sign
characters, and the target-monomial normal form.

This closes one dense support rather than all subsets of the 140-cell upward
cube.  Its importance is structural: the sparse odd circuit has enlarged to
a nine-binomial lattice certificate, suggesting that an extension-robust D1
theorem should permit bounded Laurent lattice reductions, not only literal
three-binomial circuits.

The frozen ledger SHA-256 is
`b08106c08267a8e530e2330e80bac0b00de0169087faf702aa3f46e53b869e71`.
