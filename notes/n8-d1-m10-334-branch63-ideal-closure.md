# N=8 D1: m=10 branch 334:63 ideal closure

The complete-shadow support frozen for branch `334:63` has no coefficient
point over ℚ, ℂ, or any field of characteristic other than two.  The
checker `computations/verify_n8_d1_m10_334_branch63_ideal_closure.py` proves
this with three of the 523 frozen full-output generators; no solver or
Gröbner-basis verdict is used.

Write

```text
a = x_01_11    b = x_03_11
c = x_14_11    d = x_15_11
e = x_34_11    f = x_35_11
u1 = x_24_00 x_67_00
u2 = x_25_00 x_67_00
u3 = x_02_00 x_67_00.
```

Artifact generators 78, 91, and 109 are respectively

```text
g1 = u1 (a f + b d),
g2 = u2 (a e + b c),
g3 = u3 (c f + d e).
```

All displayed variables are among the 77 cells localized nonzero.  In the
Laurent ring the exact identity

```text
a (c f + d e) - c (a f + b d) + d (a e + b c) = 2 a d e
```

therefore gives a contradiction in characteristic not two.  The checker also
clears the three unit factors and constructs an ordinary polynomial
Nullstellensatz certificate.  If `U` is the product of all 77 localized
variables, it verifies exact sparse-polynomial equality showing `U^3` lies in
the original 523-generator ideal.  Hence saturation by `U` is the unit ideal.

The checked ledger SHA-256 is
`d000761d34787891a1020f2c4cbddc7173ee39b780e15fcd908d09b083e79c01`.
Both normal and optimized replays first reconstruct the complete candidate
artifact and all 523 equations, then independently verify the three-generator
certificate.

This closes the first complete-shadow survivor at coefficient level.  It does
not yet close every remaining `3+3+4` support branch: the same compact
binomial template should be searched across subsequent Boolean survivors,
while branches without a complete-shadow model remain support-level closures.
