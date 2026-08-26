# Exact K19–K24 denominator and restart arithmetic plan

## Verdict

A single fixed integer scale suffices through K24:

```text
U = 400,591,699,200
  = 2^8 · 3^3 · 5^2 · 7^2 · 11^2 · 17 · 23.
```

This is the exact LCM of all pivot-count products reachable in the literal source-lineage anchor-signature recurrence before coefficient cancellation.  Big integers and general rational arithmetic are not required: signed `i128` is rigorously sufficient.

The old one-page scale `281,801,520` is not sufficient for nested pages.  K19 already has a reachable two-step product `5·5=25`, while that scale contains only one factor of 5.

## Pivot arithmetic by layer

A balanced degree-24 monomial has each of the 12 disjoint anchor cells with multiplicity `0,1,2`; a Kd row has anchor sum `24-d`.  Consequently K20 is the last pivotable parent, and every pivotable K20 signature has exactly one dividing pivot.

| parent degree | exact policy-count LCM |
|---:|---:|
| K14 frozen valid policy | 3,612,840 |
| K15 all pivots | 21,677,040 |
| K16 all pivots | 55,440 |
| K17 all pivots | 840 |
| K18 all pivots | 12 |
| K19 all pivots | 2 |
| K20 all pivots | 1 |

The exact source-lineage DP starts from the literal direct signature sets at K14–K20, uses the frozen valid-pivot policy at K14, and then applies every literal dividing pivot with K2/K3/K4 increments `+2,+3,+4`.

| output | distinct products | maximum product | product LCM |
|---:|---:|---:|---:|
| K19 | 84 | 560 | 33,382,641,600 |
| K20 | 175 | 2,240 | 400,591,699,200 |
| K21 | 183 | 2,240 | 400,591,699,200 |
| K22 | 183 | 2,240 | 400,591,699,200 |
| K23 | 178 | 2,240 | 400,591,699,200 |
| K24 | 146 | 2,240 | 400,591,699,200 |

Every individual product is listed in `results_k19_k24_arithmetic.json`.  This is an exact pre-cancellation source-lineage census; cancellation may reduce denominators but cannot enlarge them.

### Hidden higher-tail re-audit

The depth ledger explicitly retains pivotable intermediate children.  In
particular it contains the previously easy-to-miss path

```text
K14 --K2--> K16 --K2--> K18 --K2--> K20,
```

so K20 has denominator depth three, not two.  That depth-three slice has 142
distinct pivot-count products, maximum `2,240`, and LCM exactly
`400,591,699,200`.  Continuing all K2/K3/K4 children gives maximum denominator
depth four at K24; its depth-four slice has 119 products and the same LCM.
Thus the earlier DP did not omit these hidden pages and the recommended scale
`U` remains unchanged.  The result JSON now freezes the product lists by
pivot depth as a must-fire regression guard.

## Coefficient bound

Pivot averaging does not increase L1 mass beyond the tail count: a parent of mass `M` emits at most `12M`, `32M`, and `60M` into its K2/K3/K4 pages because summing the `m` chosen pivots cancels the `1/m` average.

Assuming every parent pivots and every term in a bucket collides gives:

- maximum K24 coefficient magnitude: `4,186,210,293,964,800`;
- maximum scaled labelled numerator: `1,676,961,094,867,890,736,988,160,000`;
- maximum transient scaled H-orbit mass, including `|H|=384`: `643,953,060,429,270,043,003,453,440,000`;
- signed-i128 safety margin: more than `264,213,642`.

Thus `i128` is sufficient even for hostile total collision.  Modular residues can be maintained as audit shadows, but they are not the authoritative representation.

## Restartable representation

Store each record as:

```text
(K-degree, canonical 24-byte H-row, i128 numerator at scale U)
```

The numerator represents the coefficient **per labelled row**, not the orbit mass.  For one canonical parent:

1. Expand its complete H orbit.
2. For each labelled image with `m` dividing pivots, emit every tail with scaled coefficient `-c/m`; assert exact divisibility by `m`.
3. Canonicalize and collect signed child contributions.
4. For each child orbit, exact-divide the collected scaled orbit mass by the child orbit size; equivariance of the complete parent-orbit packet proves divisibility.
5. Drop zeros only after exact signed addition.

This avoids introducing spurious factors of 384 from orbit compression.  Existing scaled checkpoints must be parsed as reduced rationals and rescaled to `U`; their raw numerator at the old scale must not be converted by integer ratio because `U` deliberately omits the unused prime 13.

Flush sorted per-degree runs and checkpoint the input SHA, byte offset, record count, run counts/hashes, scale, sign convention, policy hash, and pending child degrees.  Merge every input degree completely before reducing the next degree.

## Replay and scope

Standard, `-O`, and `-I -S` modes agree with logical digest `f77bc67518a2bf8611e88a4eaa7995b1896c96a5882d29d55647f1a7e0605610`; the hostile scale mutation fails.

This is an exact arithmetic/source-lineage plan only.  No K19+ residual, row collection, charge, or membership computation was run.
