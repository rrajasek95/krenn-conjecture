# First 157-cell O4 character holonomy

The first exact support-shadow frontier after closing the 158-cell layer has
157 localized cells and 4,105 coefficient generators.  Its 72 initial plus
binomials have exponent rank 25 and 47 character-consistent dependencies.
After exact reduction, the 244 two-class generators contribute 25 distinct
new character rows.  The augmented 97-row system has rank 39 and 58 integral
dependencies, exactly three of which have character `-1`.

All three odd dependencies are expanded back through the reduced relations to
ordinary source generators.  The selected smallest identity uses 13 source
records and 43 Laurent cofactor terms and clears to an ordinary `U^2`
certificate.  It proves emptiness in every characteristic except two; the
conjecture is over the complex numbers, so this is sufficient here.

The same source audit enumerates every newly admitted full-output monomial.
There are exactly nine inclusion-minimal repair masks, all singletons:

```
x01_10  x06_10  x06_11  x07_10  x14_01
x15_01  x16_01  x17_00  x37_00
```

Consequently the identity remains valid throughout the entire upward chart
where its 27 named source witnesses remain localized and those nine visible
cells remain absent.  The checker emits all eight O4 symmetry transports as
support-faithful clauses.  This visible set agrees with the earlier collision
chart, but its localization witnesses are different; it is therefore a new
chart below the 157-cell frontier, not a duplicate face certificate.

Reproduce with:

```bash
python3 computations/verify_n8_d1_residue_orbit4_157_character_holonomy.py
python3 -O computations/verify_n8_d1_residue_orbit4_157_character_holonomy.py
```

Frozen ledger SHA-256:
`a4e332f4f5562a97412742f2a86968b57a2b99f5c78d67fde9ee15f43c8abad0`.
