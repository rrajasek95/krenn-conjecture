# Exact closure of the zero-tail `0,30,45` coefficient class

The smaller 86-orbit support class is empty over `Qbar`; no polynomial
Groebner basis or modular inference is used.

## Canonical Laurent interface

The lexicographically first support representative has

```text
Q cut pairs:       0,30,45
Q orientations:   {0000,1111}, {0011,1100}, {0101,1010}
X relation masks:  0,18,45 = 000000,010010,101101
support orbit size: 288
```

Twelve anchor entries are normalized.  Each of the eighteen sparse `2x2`
blocks has exactly one live diagonal or antidiagonal pair; solving its
permanent equation writes it as `(b,-1/b)`.  The residual clone gauge is a
Laurent section: for a star edge `0j`, take `t_j=b_0j^-1` on an equal-clone
block and `t_j=b_0j` on a crossed-clone block.  This sets
`b_c,01=b_c,02=b_c,03=1` without roots and leaves nine variables
`u_c,v_c,w_c`.

The exact exporter finds 12 literal triangle rows with five unique
numerators.  After substituting entry support, 440 of the 1,638 cross rows
remain structurally nonzero, with 32 unique numerators.  The full exact
minimal `Q,C` signature contributes 27 unique zero numerators; the combined
interface has only 34.

## Exhaustive coefficient closure

For an entry-relation mask `r`, a three-supervertex triangle has two live
cycle monomials exactly when its three relation bits have odd parity.  If the
parity is even, its literal normalized triangle row is exactly `t=-2`, hence
`(-1/2)t=1`.

Among the 86 support-orbit representatives, the number of colours satisfying
all four odd-parity tests has histogram

```text
0 colours: 64; 1 colour: 16; 2 colours: 4; 3 colours: 2.
```

Thus 84 representatives close by a one-row unit.  The only residual masks are
`(11,11,11)` and `(18,63,33)`, with support stabilizers of orders 6 and 12.
For either allowed one-colour mask the first three triangle equations give

```text
x^2 + 2*x - 1 = 0,
```

and the fourth retains six of the eight root-sign triples.  Therefore each
residual has exactly `6^3=216` combined branches over `Q(sqrt(2))`.  All 216
are H-live in both residuals.

A single literal row kills every branch in each case:

- `(11,11,11)`: `00011011 = Q0[0125]*Q1[3467]`;
- `(18,63,33)`: `00011110 = Q0[0127]*Q1[3456]`.

Both rows belong to the newly added `440/2110` orbit.  The branch check is
upgraded to exact sparse Laurent identities.  With
`g=s^2-2s-1=s*t1_123`:

```text
4 = -(u0+3)(s-3)(v1/w1) P + (2-g)f + 2g,
f = u0^2+2u0-1 = -u0*t0_012,
s = v1/(u1*w1),
```

and

```text
4 = -(v0+3)(s-1)v1 P + (2+g)f - 2g,
f = v0^2+2v0-1 = -v0*t0_013,
s = v1/(u1*w1).
```

The checker verifies both identities term-for-term in the integer Laurent
ring.  Covariance transports the triangle units and the two residual
identities through their full `B4 x S3` support orbits.  Hence no minimal
`0,30,45` support refinement realizes an H-live `e=t=0` solution of the full
1,638-row packet.

## Replay and digests

```text
PYTHONHASHSEED=19 python3 -O export_class_03045_laurent_interface.py --check-results
PYTHONHASHSEED=19 python3 -O solve_class_03045_exact_branches.py --check-results
```

- exporter: `329176ed4a325160e862fafaaf48bcb6f03189dd58de8add203cfdf539e6730c`
- interface result: `298b88acb5a63caa1aab555829470ae4f8ffe241c2cc0541221fa40fff309de3`
- solver: `3629c3ab0dad5742db1dca65aff70927c52999f318ffcaa6aca70619a3609d39`
- theorem result: `3f881dea3ef2db6e87340d715fdebdcdd418f8095b42f3b5628e188182d1f95f`
- interface logical: `00455f80b65b3b004c336b852a004f6373b3b7294a38493e212534fe9089764e`
- theorem logical: `6bdee0c2a402e1d30dae17ef2f769e7bfac6685883cc48bb157962b310454327`
