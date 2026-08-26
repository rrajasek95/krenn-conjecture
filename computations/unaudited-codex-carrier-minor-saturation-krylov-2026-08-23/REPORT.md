# Multiplication by the pure amplitude does not close the carrier-minor Krylov block

Status: **UNAUDITED bounded exact negative result for the proposed all-`k`
saturation recurrence.**  The first two multiplication maps are nonzero, but
the frozen quotient data do not form an injective stable module.  The `k=3`
class is genuinely new.

## Quotient and frozen classes

Work in the homogeneous quotient

```text
Q = Q[A_e,ab] / (all mixed X5 amplitudes)
```

and write `F0=F_00000000`.  The preceding exact certificates give

```text
[Delta]       != 0,
[F0 Delta]    != 0,
[F0^2 Delta]  != 0,
```

with separator pairings `1,2,28`.  Consequently the two literal primal maps

```text
< [Delta] >       --F0--> < [F0 Delta] >,
< [F0 Delta] >    --F0--> < [F0^2 Delta] >
```

have rank one and are injective on their displayed one-dimensional source
lines.  This is only a two-step statement; it is not uniform injectivity.

## Exact dual multiplication map

For a quotient functional `lambda`, the transpose of multiplication is

```text
(m_F0^* lambda)(q) = lambda(F0 q).
```

The checker contracts the literal 44-term and 102-term integer separators by
all 105 pure matching terms.  Every resulting functional is replayed against
all mixed-X5 translates touching its support.  Ranks are computed exactly over
`Q`; the identical ranks at `32003` and `32009` are independent guards.

The frozen separator shells themselves are one-dimensional:

| degree | support columns | touching rows | rank over Q | nullity |
|---:|---:|---:|---:|---:|
| 13 | 44 | 52 | 43 | 1 |
| 17 | 102 | 177 | 101 | 1 |

However neither transpose transition preserves the preceding line:

| contraction | output support | touching rows | rank over Q | nullity | scalar previous separator? |
|---|---:|---:|---:|---:|---|
| degree 13 to 9 | 21 | 7 | 7 | 14 | no |
| degree 17 to 13 | 108 | 85 | 77 | 31 | no |

The second contraction overlaps the frozen degree-13 separator in only seven
coordinates.  It still annihilates every relevant row and pairs with
`F0 Delta` as `28`, so it is a valid new quotient-dual direction, not a failed
certificate.

The combined-support calculations rule out interpreting this as a hidden
two-line closed block:

```text
degree 9 union : support 22,  row rank 7,   nullity 15
degree13 union : support145, row rank109,  nullity 36.
```

Thus the known directions sit inside substantially larger exact annihilator
spaces.  There is no canonical finite endomorphism on which the two frozen
separators determine a minimal polynomial.

## Krylov conclusion

The three nonzero classes occupy distinct homogeneous degrees, so their
observed Krylov dimension is three.  Since `deg(F0)=4`, any scalar polynomial
annihilating `[Delta]` must reduce, grade by grade, to a monomial `t^m`.
The frozen data prove only

```text
m >= 3.
```

They do not decide whether `F0^3 Delta` vanishes.  Equivalently, the first two
line maps are injective, but no stable `F0`-torsion-free submodule has been
identified.  An exact degree-21 separator or membership calculation is needed;
`k=3` cannot be inferred from `k=1,2`.

## Replay and guards

```sh
python3 audit_saturation_krylov.py --check-results
python3 -O audit_saturation_krylov.py --check-results
python3 -I -S audit_saturation_krylov.py --check-results
```

The hostile `--mutate-lambda2` mode must fail because the contracted
functional ceases to annihilate a literal degree-13 mixed row.  Frozen logical
digest:

```text
a9eceb703c95fec67ea56d1ddf987137ebc9bcdea542eec31116097e378e040b
```

Scope is limited to the exact coordinate shells touched by the frozen
separators and their literal contractions.  This is not a full degree-21
Macaulay calculation and makes no radical or inhomogeneous-normalization
claim.
