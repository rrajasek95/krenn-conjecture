# All three exact same-hole carrier packets have the same private-row unit

Date: 2026-08-11

Checker: `computations/verify_h3_one_bad_same_hole_three_carrier_fullword_units.py`

## Three-packet verdict

The canonical shared C/A packet, the middle A/T right-repair packet, and the
forced-secondary middle-left packet are all empty on their exact carrier
supports.  Their support sizes are respectively `17,17,19` cells.  No
coefficient-consistent rational guard survives.

The complete literal full-word ledgers are:

```text
packet                    nonzero rows  monomials  row sizes
shared C/A                         29          31  27x1 + 2x2
middle A/T right                   21          23  19x1 + 2x2
middle A/T left+secondary          34          38  30x1 + 4x2
```

## Uniform literal certificate

In every packet, the pure word `00000000` and mixed word `00000001` have
the same unique physical matching within that packet.  For shared C/A it is

```text
01 | 27 | 34 | 56.
```

For both middle A/T packets it is

```text
03 | 14 | 27 | 56.
```

For the shared packet the three-factor common tail is
`q01:00*q34:00*A56:00`; for both middle packets it is
`q03:00*q14:00*A56:00`.  In every case, writing the common tail as `M`,

```text
Gpure  = ra*M - 1,
Gmixed = rc*M,
```

where `ra=A27:00` and `rc=A27:01`.  Thus

```text
ra*Gmixed - rc*Gpure = rc.
```

The forced same-hole `R_c` cell is localized and nonzero.  At the pinned
normalization `ra=1, rc=-2`, the identity is the ordinary rational source
unit

```text
1 = (-1/2)*Gmixed - Gpure.
```

This closes the two remaining `f057798` carrier packets without invoking
the general curved-doubly-good OO route.

## Scope

The conclusion is exactly the requested carrier-support verdict.  It does
not allow additional residue cells: such cells can add physical matchings to
the two private words.  It also does not address arbitrary extra endpoint
stars or prove the general curved-OO transport theorem.
