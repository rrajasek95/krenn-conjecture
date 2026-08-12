# H3 C6 E14 mixed-10 companion-row unit

## Result

The seven anchor-contained mixed-10 guards left by `8f58910` are ordinary
two-row source units.  In fact, the same statement closes every first
mixed-10 internal extension of the nine minimal E14 bright charts: all
135 chart/cell records are units, coefficientwise in the complete E14
formal family and in arbitrary core `p1,s1` entries.

The exact checker is
`computations/verify_h3_c6_e14_mixed10_companion_row_unit.py`.

## Common identity

Let

```text
T = G11[111111]
```

denote the complete target coefficient, so its source generator is
`F_target=T-1`.  For 120 of the 135 mixed-10 extensions the zero word already
used in `8fe3f8b` still satisfies

```text
G11[zero_i] = T,
F_zero - F_target = 1.
```

The remaining 15 extensions have one of only two literal companion rows:

```text
X1-tail 1:  G11[110011] = -T       (6 records),
X1-tail 2:  G11[110101] = -T       (9 records).
```

Thus in both cases

```text
-F_companion - F_target = 1.
```

These are identities of the full endpoint-polynomial rows, not selected
monomial cancellations.  They remain true for every value of the E14
parameters and the new mixed-10 coefficient.  No localization is used.

## Closure of the seven guards

The checker replays and pins the complete 1,020-record classification from
`8f58910`.  Its seven literal `anchor_contained_two_tail_guard` keys are all
members of the 15 companion-row records.  Therefore the earlier distinction
between eight nonanchor mixed attachments and seven anchor-contained guards
is unnecessary at this one-cell level: all fifteen are already source units.

This is stronger than a typed-attachment or reselection landing, and no
deleted-star rank conclusion is needed.  Rank landing remains logically
separate for later, simultaneous contaminations.  This theorem makes no
claim about adding two new internal cells at once.

## Exact audit

The checker enumerates all `9 * 15 = 135` first mixed-10 extensions and
asserts the full complete-row identities above.  It also verifies that all
seven pinned guards occur in the companion-unit set.

```text
extensions=135
routes={'companion_antiparallel_unit': 15,
        'original_parallel_unit': 120}
companion_words={'110011': 6, '110101': 9}
closed_previous_anchor_guards=7
ledger_sha256=bca83e2c4ae4acc529a0a8d18e989576ea31b56cf066c36e8a2efc5a8aa23476
```

The checker passes under normal Python, `python -O`, and `python -I -S`.
