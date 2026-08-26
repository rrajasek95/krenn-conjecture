# Exact degree-12 dual and fixed-C10 nonmembership

## Result

There is an explicit 20-row rational functional `lambda` on the full
homogeneous total-degree-12 normalized row space such that

```text
lambda(original mixed generator * every degree-8 multiplier) = 0
lambda(0111202020494f4f50f8 * t^2) = 1
lambda(fixed C10) = -4.
```

Therefore the **fixed deterministic 140,185,881-term `C10` residual is not
in the full homogeneous degree-12 normalized mixed ideal**.

## The functional

The exact support is stored literally in
`results_degree12_full_dual_fixed_c10.json`.  Its profile is

```text
y-degree 10:  1 row
y-degree 11:  3 rows
y-degree 12: 16 rows
total:        20 rows.
```

All coefficients are `+1` or `-1`.  The sole y-degree-10 row is the selected
monomial, with coefficient `+1`.

## Construction and exhaustive ideal replay

Start in total degree 10 with the delta functional on the selected t-free
`y^10` row.  No degree-10 original column meets it because the row omits
physical site 5, while every top source term is a perfect matching.

Lift through the t-filtration:

| stage | crossing primitive columns | top owner rows | owner columns | peeled | correction rows |
|---|---:|---:|---:|---:|---:|
| D11 | 3 | 200 | 25 | 9 | 3 |
| D12 | 16 | 1,148 | 292 | 156 | 16 |

Reverse triangular substitution on the private-row pivot ledger gives the
three then sixteen correction coefficients.  At D12, 19 primitive octic
columns touch the lifted support before correction; exhaustive primitive
replay gives zero afterward.

As an independent stronger guard, the checker enumerates **every** original
column of the relevant total degree that touches the functional support,
including positive-t multipliers:

```text
D11:  3 incident columns, all pair to zero
D12: 22 incident columns, all pair to zero.
```

Every omitted original column is nonincident and hence pairs to zero
tautologically.  This is a full degree-12 ideal functional, not merely a
restricted-row separator.

## Fixed-C10 streaming evaluation

The exact circuit is

```text
C10 = R10 - R8*h2 + R7*S3 + R6*S4 + L(R9).
```

Because `lambda` has only one y-degree-10 support row, evaluation can be
performed coefficient-first: stream the five frozen residual packets and
retain only kernel factors capable of emitting that row.  This scans
3,476,885 source residual rows and is algebraically identical, by
distributivity, to streaming all 142,520,100 emitted contributions.

The exact pairing is

```text
lambda(R10)   =  0
lambda(-R8h2) =  0
lambda(R7S3)  =  0
lambda(R6S4)  = -4
lambda(L(R9)) =  0
-------------------
lambda(C10)   = -4.
```

This independently matches the frozen full disk aggregation, logical digest
`3dd16ca8793cb5b435700fb90773dd1c4dae5a4b9166034feaef944740ffa75d`.
Every streamed input packet is SHA-256 pinned by the checker.

## Lower-kernel referee: no quotient upgrade

The earlier 90-column lower-kernel witness changes the coefficient of the
selected `y10*t2` row by `+1`, but all 90 columns are literal homogeneous
degree-12 original-generator multiples.  Exact full replay against `lambda`
gives

```text
y10 contribution to lambda:  +1
y11 contribution to lambda:  -1
y12 contribution to lambda:   0
--------------------------------
full contribution:             0.
```

Individually, each of the 90 source columns pairs to zero.  The witness has
714 nonzero y10 rows, 2,492 y11 rows, and 5,772 y12 rows; the old lex-only
calculation omitted the y11 cancellation.

This does **not** make `C10` right-inverse invariant.  The deterministic
`C10` packet retains the y10 transfer layer.  A lower-kernel mutation changes
that layer by `pi10(M12(k))`, whereas `lambda` annihilates only the complete
source image with its y11/y12 tail:

```text
lambda(M12(k)) = 0,       but lambda(pi10(M12(k))) can be nonzero.
```

The 90-column witness gives the latter value `+1`.  Thus the fixed-`C10`
certificate cannot be promoted to a lower-right-inverse-invariant residual
class or to the full `F^h` class.  Direct full-`F^h` evaluation supplies the
same guard: all 1,157,625 normalized `F^h` terms have zero intersection with
the 20-row functional, so `lambda(F^h)=0`.  Since `lambda(C10)=-4`, the
omitted y11/y12 residual tail pairs by `+4` and cancels it exactly.

The exact truncation referee is `audit_lower_kernel_invariance.py`; result
`results_lower_kernel_dual_invariance.json`, logical digest
`87e2d04986ec22147d39b5d5783c82d53a3eedcb627ef92d7a13d553e21037dc`.

## Replay and scope

- Checker: `audit_degree12_full_dual.py`.
- Frozen result: `results_degree12_full_dual_fixed_c10.json`.
- Logical digest:
  `cde136aef242841bc78bc9b7da8e56323ab0b273bb637a30253902e9b2729aed`.
- Discovery/replay: about 13 seconds, under 450 MB peak RSS.
- Hard bounds: 300 seconds and 12 GiB.

This proves nonmembership only for the fixed deterministic `C10` attached to
the frozen lower right inverse.  It does **not** prove invariance under
alternative lower-kernel choices, nonmembership of full `F^h`, t-saturation,
degree 13, or a global unlocalized source theorem.
