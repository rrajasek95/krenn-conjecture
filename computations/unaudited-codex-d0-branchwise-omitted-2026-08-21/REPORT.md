# D0 branchwise omitted-cofactor audit

Status: **UNAUDITED**. This lane starts from the frozen exact degree-42
eliminant `E=F0*F1` and works only on the
`D0=0, C0!=0, selected-pivot!=0` chart. It does not claim that `E` exhausts
the saturated source projection.

## Exact literal-row restriction

The four omitted lower cofactors `Cof(e,3)`, `e=1..4`, were independently
restricted after the certified upper-cofactor, D0, endpoint, and two-row
Cramer solves. Substitution was performed inside `QQ(b0,d1,d4)`, rather than
by generic expression expansion. The primitive numerator profiles are:

- `Cof(1,3)`: 2,132 terms, total degree 38;
- `Cof(2,3)`: 2,294 terms, total degree 39;
- `Cof(3,3)`: 2,132 terms, total degree 37;
- `Cof(4,3)`: 2,294 terms, total degree 38.

Every cleared denominator factor is checked to divide the selected 320-term
pivot. Thus the numerator restrictions introduce no new localization. The
export logical digest is
`5b29fac1aa917b029df348adf3642891b7853ff6bd7c8442b6f26b09a6d396f1`.

## The hoped-for one-row gate is false

At `p=1073741827`, each of the eight branch-by-single-cofactor ideals is
NONUNIT. Every branch-by-pair ideal is also NONUNIT. Therefore no literal
omitted cofactor is individually a unit on either reconstructed degree-21
branch, and no such theorem is claimed.

The minimal discovered packets are three rows:

- factor 0: `{Cof(1,3),Cof(2,3),Cof(3,3)}` or
  `{Cof(1,3),Cof(2,3),Cof(4,3)}`;
- factor 1: `{Cof(1,3),Cof(3,3),Cof(4,3)}` or
  `{Cof(2,3),Cof(3,3),Cof(4,3)}`.

All four triples are UNIT at both `1073741827` and `536870909`. Modular
greedy deletion leaves one original Cramer compatibility in addition to the
branch factor, three omitted cofactors, and expanded pivot Rabinowitsch row:
compatibility index 1 for factor 0 and index 2 for factor 1.

## Exact characteristic-zero closure of both factors

The final strict msolve inputs have six rows each. They are coefficient-first,
fully expanded, contain no parentheses, and are source-selected byte-for-byte
from the exact packet export. Exact characteristic-zero msolve returned the
literal output `[-1]:`:

- factor 0: 17.17 seconds;
- factor 1: 32.52 seconds.

Hence, on the declared pivot-open chart, factor 0 is incompatible with
compatibility 1 plus literal `Cof(1,3),Cof(2,3),Cof(3,3)`, and factor 1 is
incompatible with compatibility 2 plus literal
`Cof(2,3),Cof(3,3),Cof(4,3)`.

The exact source/core/output replay is stable under `std`, `-O`, and `-I -S`
with logical digest
`4df338ae7dad51107c4fb2b1c52f9a0d6efd57938a97bb7cf6c5c5f33bb55e4c`.
The frozen census summary digest is
`8941672ffe96ecdcc7f4ff9b6ac3fcf392fa0342b5e2c3e3c38b7c939570da11`.

## Scope guard

This result closes the two reconstructed degree-21 resultant-factor branches.
It does **not** close the full `D0/C0` open chart: the prior exact computation
proves only that `F0*F1` divides one source resultant. It does not prove that
the 450-term eliminant exhausts the saturated source projection, and it does
not eliminate the large complementary resultant factor or pivot-zero chart.
