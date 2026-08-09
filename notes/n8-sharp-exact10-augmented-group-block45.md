# Exact-ten augmented signed quotient: least-extra blocks 2--5

This is the second additive block theorem for the augmented signed group
defined in `notes/n8-sharp-exact10-augmented-group-block01.md`.  The checker
is

```text
computations/verify_n8_sharp_exact10_augmented_group_block45.py
```

The exact least-added-cell block census is

```text
block 2, 01;10:     0
block 3, 01;11:     0
block 4, 01;12:   136
block 5, 01;20: 1,442
```

Every one of the 1,578 nonempty-block supports has ten additions, is an
inclusion-minimal repair of the eleven seed singleton obligations, and is
replayed against the full 105 physical matchings in every supported word.
The complete augmented-HNF outcome is

\[
             1327\text{ sign units}+251\text{ one-class units},
\]

with no consistent all-multiclass third type.  The one-class checker prefers
the largest available fibre; its exact term-count census is

```text
3:88, 4:21, 5:19, 6:65, 7:9, 8:44, 9:3, 10:2.
```

The full signed certificate ledger digest is

```text
9916a56a1c33d90911cbde66abc67a032386cdbf9120ae7059a3d74a5fa96125
```

Together with blocks 0/1, the frozen exact-ten coverage is now **4,550**
supports:

\[
             3355\text{ sign units}+1195\text{ one-class units},
\]

again with no third type.  This remains a prefix theorem, not a complete
cap-26 proof.  Later least-cell blocks must be exhausted with the same full
signed quotient; an unsigned transfer cache is not sound.

Reproduce with

```bash
PYTHONPATH=computations .venv/bin/python \
  computations/verify_n8_sharp_exact10_augmented_group_block45.py
```
