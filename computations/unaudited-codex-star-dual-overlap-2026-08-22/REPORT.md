# Least-star dual overlap audit

Status: **exact acyclicity no-go on every injective-star chart**.

Let `T_pq` be the edge residual-Hafnian map and

```text
L_v = direct_sum_{q != v} T_vq.
```

At a norm minimum, choose the least Hermitian dual in `im L_v`,

```text
Lambda_v = L_v (L_v^* L_v)^(-1) A_v*,
A_v* = L_v^* Lambda_v.
```

The two endpoint equations on a shared edge give the literal compatibility

```text
T_pq^* (Lambda_p - Lambda_q) = A_pq - A_pq = 0.       (1)
```

This looks like a Cech cocycle, but it carries no new equation on an
injective-star chart.  Define

```text
D(Lambda)_pq = T_pq^*(Lambda_p-Lambda_q).
```

If `z=(z_pq)` is a row syzygy, then at vertex `v`

```text
(D^*z)_v = sum_{q != v} +/- T_vq z_vq = 0.
```

The displayed sum is precisely `L_v` applied to the signed tuple of incident
`z` values.  Injectivity of `L_v` forces every incident `z_vq=0`; hence
`ker D^*=0` and `D` is surjective.  In particular, neither a triangle nor a
four-cycle supports a Koszul class.  This proof works both on the full dual
spaces and after restricting each dual to `im L_v`.

## Exact controls

For the exact `n=4` ternary GHZ minimum:

```text
star ranks                    4 x 27
edge residual ranks           6 x 9
restricted overlap rank       54 / 54 rows
restricted domain/kernel      108 / 54
full dual domain/kernel        324 / 270
triangle / four-cycle ranks   27/27, 36/36
```

Every star matrix has orthonormal one-hot columns.  The four literal least
duals can therefore be evaluated without inversion, and all four equal the
ternary GHZ output tensor.

For the phased block-injective `n=6` non-GHZ source:

```text
star ranks                    6 x 45
edge residual ranks           15 x 9
restricted overlap rank       135 / 135 rows
restricted domain/kernel      270 / 135
full dual domain/kernel        4374 / 4239
triangle / four-cycle ranks   27/27, 36/36
```

The ranks are exact over `F_7` under the valid specialization
`Q(omega) -> F_7`, `omega -> 2`; attaining the row-count upper bound proves
the characteristic-zero cyclotomic ranks.  Canonical exact algebraic duals
were solved independently at all six stars and pass all fifteen overlap
equations.  Their span has dimension greater than one, so compatibility does
not mean the local dual representatives coincide.  The least Hermitian duals
obey (1) for the same formal reason.

Thus overlap compatibility cannot distinguish GHZ from the phased non-GHZ
control and cannot manufacture a clean-cap covector or cycle identity on the
generic chart.  New information can occur only on a vanishing star determinant,
where `A_v* orthogonal ker L_v` becomes a genuine condition.  That boundary is
already the block-normal/support stratification, not a new generic proof lane.
