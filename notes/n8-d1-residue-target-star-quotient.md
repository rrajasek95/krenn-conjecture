# N=8 D1: the residue target-star quotient

There is a division-free obstruction that closes the `31/54` residue
frontier and applies far beyond it.

Fix a residue center, say site `6`, and take the target-colour slices of its
three incident edge blocks.  On the other endpoints these are vectors

```text
b=B46[:,2],       d=D56[:,2],       f=F67[2,:].
```

If each vector has any localized non-target coordinate, it is not the target
line.  Choose colour `0` witnesses for notation.  The integral covectors

```text
q_b=(-b2,0,b0),   q_d=(-d2,0,d0),   q_f=(-f2,0,f0)
```

annihilate `b,d,f`, respectively, and take the value `b0,d0,f0` on `e2`.

The centre-colour-`2` residue equation on the other three sites is

```text
A45 tensor f + b tensor E57 + C47 tensor d = e2 tensor e2 tensor e2.
```

Contract it by `q_b tensor q_d tensor q_f`.  Each term on the left contains
one annihilated incident vector, so the left side is zero.  The right side is

```text
b0*d0*f0,
```

a unit after the three named localizations.  This is a polynomial identity
over `Z`, with no division, rank split, algebraic closure, or characteristic
assumption.  It therefore remains valid directly over a localized integral
domain and is particularly well suited to uniform descent.

For the canonical `31/54` frontier the residue blocks are

```text
45={01,10,11,12,21,22}       46={02,12,22}
47=all except 10             56={02,12,22}
57=full                      67={20,22}.
```

At center `6` both non-target projection rows are zero on all three incident
blocks.  More importantly for this lemma, the target vectors contain the
localized witnesses `x46_02,x56_02,x67_20`, so the quotient closes the whole
boundary subcube immediately.

The exact checker
[`verify_n8_d1_residue_target_star_quotient.py`](../computations/verify_n8_d1_residue_target_star_quotient.py)
freezes the maximal `194`-cell support with this residue pattern, verifies all
`8,100` support fibres, freezes its `7,237` coefficient generators under hash
`81ce07753287eb2c13138f9c8ecf8f1131c7623600b357d35327b2f061c1c647`,
records the four-center projection profile, and checks the contracted identity
coefficient by coefficient.
