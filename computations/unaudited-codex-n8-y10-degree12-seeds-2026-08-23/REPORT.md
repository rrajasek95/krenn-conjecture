# N8 chart-26: degree-12 nonmembership of the selected monomial

## Exact result

In the frozen normalized chart and t-last order, the homogeneous monomial

```text
m = 0111202020494f4f50f8 * t^2
```

does **not** belong to the normalized mixed ideal in total degree 12.

This is the terminal homogeneous degree for `m`.  No t-saturation or
degree-13 calculation was performed.

## Restricted-owner certificate

Degree 12 has one target divisor: `m` itself.  Modulo `t*M11`, the only new
columns are originals times t-free octic y-multipliers.  Exactly four such
columns touch `m`.

Taking all top `y^12` rows of those four seeds and every literal
original/octic factorization owner gives the complete restricted matrix

```text
244 seed rows
138 owner columns
579 incidences.
```

Private-row peeling removes 30 columns, including all four target seeds.
The 108-column induced residue contains zero seeds.  Hence restricting any
full degree-12 head relation to these rows forces the coefficients of all
new target-touching columns to vanish.

Every other degree-12 column has positive multiplier t-exponent and belongs
to `t*M11`.  Exact degree-11 standardness excludes its lower target pivot.
There is no higher generator degree that can occur in a homogeneous
degree-12 representation, so this proves `m` is not in the ideal.

## What this does—and does not—say about `C10`

The fixed deterministic residual

```text
C10 = R10 - R8*h2 + R7*S3 + R6*S4 + L(R9)
```

has 140,185,881 terms.  Its aggregate contains `m` with coefficient `-4`,
and `m` is the lex-first member of its minimum-PM4-dead subset.

The present result proves nonmembership of the **single monomial `m`**.  It
does **not** decide whether the full fixed polynomial `C10` belongs to the
ideal.  Other terms of `C10` can reduce into the same quotient class as `m`
and cancel its normal-form coefficient.  The aggregate does not compute the
full quotient normal form, nor does it certify `m` as an isolated quotient
coordinate or as the completed-order leading term of `C10`.

Even a future nonmembership proof for this fixed `C10` would retain the
frozen provenance warning: alternative lower-degree kernel/right-inverse
choices can change `C10`.

## Replay and scope

- Checker: `audit_degree12_restricted.py`.
- Logical digest:
  `8030714e1f1edaa844664c893bb28f6574e32cca7d3e88a3e1379cfc25d541bd`.
- Degree-11 authority:
  `98a5254238a87e79d7861640ee8b9cb4c88f68cdee57ca8251f9fe714df5e171`.
- Fixed aggregate authority:
  `3dd16ca8793cb5b435700fb90773dd1c4dae5a4b9166034feaef944740ffa75d`.
- Hard bounds: 300 seconds and 12 GiB.
- Discovery run: about 8.9 seconds and 363 MB peak RSS.

This report makes no claim about the full `C10` normal form, t-saturation,
degree 13, or the original unlocalized global ideal.
