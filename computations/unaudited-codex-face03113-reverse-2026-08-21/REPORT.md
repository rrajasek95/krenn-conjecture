# Face `(0,31,13)` exact reverse gate

Status: **closed on the selected-base/remaining-C open set by a canonical
characteristic-zero empty sentinel with independent literal source replay**.
This is the sole proper boundary type left open in the preceding recursive
face audit.

## Degree-nine routing, now terminal

The frozen degree-nine dual for the 12-row discovery subsystem was
transported back to the complete monomial universe and evaluated on every
multiple of the four omitted rows.  The numbers of dual-breaking columns
were:

```
raw 6  t_012          1885
raw 9  t_123           193
raw 10 Cof(0,0)         23
raw 11 Cof(0,3)       1411
```

The audit independently replays both the generator ledger and the 135,659-row
monomial ledger before pairing.  Logical digest:
`cc1d905a89471539dfb97c2681485b8a08ecaaa21ee50ee8c19ec50217cc3856`.

The two cheapest rows were tested separately, using complete homogeneous
multipliers and sound zero-target leaf peeling:

- base12 + raw10 leaves a `31,847 x 22,429` target core.  At `p=1009` its
  rank is 20,911, the target is outside, and the left dual has 6,862 terms
  with target pairing 572.  Core SHA-256:
  `a44099a42dabb33bff215c0475baad5aa30c84b897c5331745b0e3960e643ea5`;
  solve SHA-256:
  `5131cd0a6efbb0048e7a3c30efa6d13efcd9872152127220f84691e1e5e4bf0c`.
  Standard, `-O`, and `-I-S` replays have logical digests
  `0afb9b8af1d0b9ad96e4bfbbfc2ff49beb98655113b36bf953d4d12a1a416494`,
  `24d8ceac83699aa608f91e34e4436a8b1e055705296ee721d9bb308c13e7a37d`,
  and `1b204cc0d7d3cc3ff9050a69c47ffa91bce005c9c265b0cfc8404d990a7e4730`.
- base12 + raw9 leaves a `32,103 x 22,671` target core.  At `p=1009` its
  rank is 21,151, the target is outside, and the left dual has 6,687 terms
  with target pairing 916.  Core SHA-256:
  `926a20243ad08b183399095d4800a41371eda23c738ba3ce8c0dcc292d18be1e`;
  solve SHA-256:
  `9593204edaee51daa61f3c1b2e4719fa10cecdb65ba90e5ec9b5513c78036d07`.
  Standard, `-O`, and `-I-S` replay digests are
  `8b2db857f8d0d0c7594835307ddb8ee5df4e63e2e611f17448a431c1ee1ca040`,
  `1a5edcd0149e42f8d6392f7b9d087292939d3305773f567d00a0fd9ea0bef1f8`,
  and `ab4483f33ea213a4699653acc211d4da4ae312f7edc96650424cf4c51e546fbd`.

These are only `F_1009`, degree-nine obstructions.  They do not prove affine
or characteristic-zero nonmembership.  They show that degree nine remains
structurally insufficient even after either cheapest omitted row is restored.
No higher-degree ladder was launched.

## Canonical characteristic-zero input

`export_face03113_base12_char0.py` rebuilds raw rows

```
7, 8, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21
```

from `results_recursive_face_charts.json`.  Every polynomial is expanded over
`Z` and printed coefficient-first.  The thirteenth row is the explicit
Rabinowitsch equation

```
s*a5*b3*b4*(1+a0)*(1+a2*d2)*(1+a3*d3) - 1.
```

Thus only `a5`, `b3`, `b4`, `1+a0`, `1+a2*d2`, and `1+a3*d3` are localized.
Neither the pure Hafnian `H` nor `a0*a2*a3*d2*d3` is localized.  The strict
toolkit parser rejects parentheses, `**`, and coefficient-after-symbol terms
after export.  The canonical input SHA-256 is
`652183de1427c09053bdb5aeb1fbd67c619321f88c0da5fbb418acd3d1159f9e`;
the source/export logical digest is
`ec9dc5653a7b3f75657072b68fa751588197350459078ba0c8521e4e37a3736f`.

## Characteristic-zero verdict

The one authorized characteristic-zero msolve 0.10.1 run completed in
11.15 seconds and returned exactly

```
[-1]:
```

The toolkit parses this as `kind=empty`, degree zero, in twelve variables.
Output SHA-256:
`0333251e6ebb3890ef547f522ec55f27f0cef9a860998757e31f3e1b819e7490`;
manifest logical digest:
`091f7f6545494efaffb2291a63c83263b578d3b599bc9974f634449070369138`.

`audit_face03113_char0_empty.py` independently compares every input row with
both the literal source strings and the rational term ledger, reconstructs the
expanded Rabinowitsch row, requires the exact empty sentinel, and rejects the
positive-dimensional `[1,5,-1,[]]:` sentinel.  Standard, `-O`, and `-I-S`
logical digests are
`48617e0ab6931d9481eaee55fddaca57fc6efe0263d881426e531cffdda5470c`,
`fc5bc8b436cb637d36c4e7c246b097212137f1ba17a6cb073a159db999af2ba4`,
and `b442419864ad0e2b322c3ea976d5df1265509b35fdfd6b5e978eb1cca8ec5483`.

Therefore the localized 12-row subsystem is empty over characteristic zero.
Since those rows are a subset of the full literal source, the canonical face
`(0,31,13)` is closed on the required selected-base/remaining-C open set.
