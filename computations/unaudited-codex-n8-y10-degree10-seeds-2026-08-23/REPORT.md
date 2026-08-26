# N8 chart-26: exact target standardness through degree 10

## Result

For the normalized target

```text
C10 = 0111202020494f4f50f8 * t^2
```

and the frozen t-last order, `C10` is standard against every homogeneous
divisor of total degree at most 10.

This is one bounded degree-10 stage.  It makes no degree-11 claim.

## Exact restricted-owner certificate

Modulo `t*M9`, the only new degree-10 columns are normalized originals times
t-free sextic y-multipliers.  Exact target incidence gives:

| target slice | primitive new seeds | touched divisors |
|---|---:|---:|
| `y^9*t` | 16 | 6 / 7 |
| `y^8*t^2` | 68 | 23 / 23 |
| `y^10` | 0 | 0 / 1 |

The t-free target remains unreachable because every top `y^4` source term
is a perfect matching using site 5, while the target omits site 5.

For the 84 primitive seeds, take all their top `y^10` rows and every literal
original/sextic factorization owner of those rows.  The complete restricted
matrix has

```text
5,186 seed rows
1,303 owner columns
9,156 incidences.
```

Private-row peeling removes 558 columns, including all 84 target seeds.  The
745-column residue contains **zero** seeds.  Therefore restricting any full
top-head relation to these rows forces every primitive target-seed
coefficient to vanish.  Columns not enumerated have zero on the restricted
row set.

Every remaining degree-10 column has positive multiplier t-exponent and is
in `t*M9`; the exact degree-9 theorem excludes its lower target pivot.  This
proves the result.

## Replay and bounds

- Checker: `audit_degree10_restricted.py`.
- Logical digest:
  `d594eca45d977fae501602b8e2ee250d7ddabc9c4c4eb1e0f557d198b051a0fa`.
- Frozen degree-9 authority:
  `fee70f071e6123712a6d060c5dd2aadc4f9e7c79efc082b660343fb77d1238de`.
- Hard bounds: 300 seconds and 12 GiB.
- Discovery run: about 5.9 seconds and 356 MB peak RSS.

The checker audits only the exact target-rooted degree-10 restriction.  It
does not claim a full degree-10 Gröbner basis, global ideal completion, or
anything about degree 11.
