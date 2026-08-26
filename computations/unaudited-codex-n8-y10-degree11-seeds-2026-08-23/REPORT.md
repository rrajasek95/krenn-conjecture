# N8 chart-26: exact target standardness through degree 11

## Result

For the normalized target

```text
C10 = 0111202020494f4f50f8 * t^2
```

and the frozen t-last order, `C10` is standard against every homogeneous
divisor of total degree at most 11.

This is exactly one bounded degree-11 stage.  Degree 12 was not tested.

## Restricted-owner certificate

Modulo `t*M10`, the only new degree-11 columns are originals times t-free
septimic y-multipliers.  Literal target incidence gives:

| target slice | primitive seeds | touched divisors |
|---|---:|---:|
| `y^10*t` | 3 | 1 / 1 |
| `y^9*t^2` | 24 | 7 / 7 |
| `y^11` | 0 | 0 / 0 |

Take every top `y^11` row of those 27 target-touching columns and every
literal original/septimic factorization owner of those rows.  The exact
restricted matrix has

```text
1,656 seed rows
613 complete owner columns
3,328 incidences.
```

Private-row peeling removes 185 columns, including all 27 seeds.  The
428-column induced residue contains zero target seed columns.  Consequently
the restriction of any full degree-11 head relation forces every primitive
target-seed coefficient to vanish.  Columns absent from the restriction have
zero entries on all seed rows.

Every other degree-11 column has positive multiplier t-exponent and lies in
`t*M10`; exact degree-10 standardness excludes its lower target pivot.  This
proves the result.

## Replay and scope

- Checker: `audit_degree11_restricted.py`.
- Logical digest:
  `98a5254238a87e79d7861640ee8b9cb4c88f68cdee57ca8251f9fe714df5e171`.
- Frozen degree-10 authority:
  `d594eca45d977fae501602b8e2ee250d7ddabc9c4c4eb1e0f557d198b051a0fa`.
- Hard bounds: 300 seconds and 12 GiB.
- Discovery run: about 7.4 seconds and 367 MB peak RSS.

This is target-rooted triangular standardness, not a full degree-11
Gröbner-basis computation or a degree-12 membership statement.
