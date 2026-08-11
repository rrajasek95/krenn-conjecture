# Every explicit two-cell private-row frontier preserves the same unit

Date: 2026-08-11

Checker: `computations/verify_h3_one_bad_same_hole_private_two_qcell_units.py`

## Verdict

All six first two-cell contamination supports listed in `dae10d3` are empty.
No replacement identity is needed and no coefficient-feasible carrier packet
survives: the original private-row unit remains exact.

The audited supports are

```text
shared C/A:
  + {q03:00,q14:00}
  + {q04:00,q13:00}

middle A/T right:
  + {q01:00,q34:00}
  + {q04:00,q13:00}

middle A/T left+secondary:
  + {q01:00,q34:00}
  + {q04:00,q13:00}.
```

## Coefficient identity

In each enlarged support, the private words `00000000` and `00000001`
have two physical matchings rather than one.  Crucially, the matching lists
are identical for the pure and mixed words.  Factoring the edge-`27` cells
gives one common two-term polynomial `H`:

```text
Gpure  = ra*H - 1,
Gmixed = rc*H.
```

Consequently the determinant-cleared identity is unchanged:

```text
ra*Gmixed - rc*Gpure = rc.
```

Since `rc` is the forced localized same-hole star, every localized ideal is
the unit ideal.  At the fixed normalization `ra=1,rc=-2`, all six supports
again have the ordinary source identity

```text
1 = (-1/2)*Gmixed - Gpure.
```

The checker exports every literal full word on each support.  Their sizes
range from `19` to `21` physical cells, `27` to `51` nonzero word tails, and
`31` to `57` collected matching monomials.

## Scope

This audit stops exactly at the six requested two-cell supports.  It does not
add a third common-`q` cell, enlarge the endpoint stars, or infer a theorem
for arbitrary residue support.
