# Generic affine-tail collision and the next O4 maximum

Promoting the five-cell upward atom from `d0aa9b5` leaves the exact O4
downset minimum at 36 omissions.  The replacement maximal support has 157
localized cells, passes all 8,100 support fibres, and has 4,321 coefficient
generators with SHA-256

```
2541cf4aa31003a53496be25826d7be1089f10c9039ff14fbfd178aef930177f
```

The updated downset checker freezes this support and the strengthened CNF.

## Affine-tail oracle

`computations/verify_n8_d1_residue_orbit4_157_affine_tail_collision.py`
implements a generic signed-group-algebra test.  For every pair of nonzero
reduced Laurent rows it looks for

\[
 f=c m+S,\qquad S=\lambda x^a g.
\]

Then \(f-\lambda x^a g=cm\), a Laurent unit on the localized torus.  The
test canonicalizes every possible one-term deletion of every residual row
up to Laurent translation and nonzero rational scaling, so it exhausts all
such affine-tail/homogeneous-tail pairs.  This criterion is independent of
the O4 input and can be reused in other quotient-character charts.

For the replacement face, the initial signed character system has 55 rows,
rank 21, 34 consistent dependencies, and no one-class residual.  The generic
oracle nevertheless finds exactly 36 affine-tail collisions, all pairing a
three-class row with a two-class row.  Their frozen census hash is

```
31e9b9ee4e85356b5016e6ae22434baaf5a02d2af59752770bc4f526beb22cc8
```

## Selected ordinary certificate

The lexicographically first collision pairs records 2475 and 2474.  Their
tails align by the Laurent multiplier `x06_11/x06_10`; subtraction leaves
one localized monomial.  Expanding the rank-21 character reductions to the
original coefficient equations and clearing denominators gives an integral,
all-characteristic ordinary `U^2` certificate:

- 8 source generators;
- 18 Laurent and ordinary cofactor terms;
- certificate SHA-256
  `1b62944c9ae68c40d81b1ceb5a479f73b5a7f2b39a903d217a1297fbfcd17575`.

The source identity uses 22 localized witness cells.  Exhaustive matching
repair gives nine singleton repair cells:

```
x01_10, x04_10, x07_11, x12_01, x16_00,
x16_01, x17_01, x26_10, x27_11.
```

Thus the same identity closes the entire upward subcube retaining the 22
witnesses and omitting those nine cells.  The checker freezes all eight D1
symmetry transports of this implication.

## Reproduction

```
python3 computations/verify_n8_d1_residue_orbit4_157_affine_tail_collision.py
python3 -O computations/verify_n8_d1_residue_orbit4_157_affine_tail_collision.py
/Users/rishi/.venv/bin/python3 computations/verify_n8_d1_residue_orbit4_downset_cegar.py
/Users/rishi/.venv/bin/python3 -O computations/verify_n8_d1_residue_orbit4_downset_cegar.py
```

The affine-tail ledger is
`a3b5bfe09405a21f20c00ba2605f175d69af49531579c3ebbc5e0190e15e1533`;
the strengthened CEGAR ledger is
`df38068abd9b957303026fac1153736a688c65144ca390f21c6b205a634af57d`.
