# k5 face `0:31:30`: A-open exact reduction and bounded gate

Status: **UNAUDITED exact source reduction; branch remains unresolved.**

## Exact reduction

The frozen raw row 7 is

```text
raw7 = A*a4+B,
A = -a0*d2*d4+b4*d2+d4.
```

On `A!=0`, substituting `a4=-B/A` and clearing denominators reduces the
other fifteen literal rows.  The audit removes only exact factors already
localized on this chart (`A` and `b4`).  All fifteen resulting rows are
distinct, including raw16 as the exact 25-term degree-six `R25` equation.

In raw-index order `6,8,9,...,21`, their `(terms,degree)` profiles are

```text
(11,4), (10,4), (47,9), (63,9), (41,7),
(26,8), (46,8), (14,5), (56,8), (25,6),
(51,7), (14,5), (13,4), (10,3), (78,8).
```

The selected-base and `a*d` antecedents reduce to the 16-term degree-17
product

```text
A*B*a1*a2*a3*a5*b3*b4*d2*d3*d4.
```

The additional transported `c`-product and `H` numerators have 48 and 253
terms (degree 11 before removal of their redundant live `b4` factors).  The
single full-live product has 25,230 terms and degree 37.  A logically
equivalent three-inverse input is only 12.5 KB, which controls for large
product parsing.

Canonical characteristic-zero input SHAs are:

```text
base only       109e9939a660f1cd1b18d9eb8b394961855dd4ea2b80900831c4cdb20f98695a
full product    aa326ac4a82425eac18fcdb475f7fc3dd3030bc04dbe59601f82b2a35aa720a8
split live      638d74a93b78be30cf48faaa0c6fae6ca3e60887f09b4cb57f33027609b911b2
core8 split     7f4ee6e36931d213a0e963b566d339d2c6d89b26cedc5faf1eae5154984fde03
```

Exporter logical digest:
`38882f87ad3c77f8031cdf8bdb446e7c05e32ff92a198e9be7e3ad60d1bc819d`.

## Omitted-row/core screen

The eight smallest reduced rows are raw

```text
6, 8, 12, 14, 16, 18, 19, 20.
```

They include `R25` and use all original live factors through the three exact
inverse equations.  Neither the one-prime discovery run nor the sole exact-Q
run returned a unit or positive-dimensional sentinel within its cap.

The natural literal second pivots worsen rather than shrink the interface:

| pivot | coefficient | residual | max row terms | max live terms |
|---|---:|---:|---:|---:|
| raw16, solve `a2` | 9 terms, degree 5 | 16 terms, degree 4 | 262 | 735 |
| raw20, solve `b3` | 2 terms, degree 1 | 8 terms, degree 3 | 425 | 1,103 |

Thus no compact fraction-field route emerged from the two literal pivots.
The next justified route is a component/slice calculation or a new sparse
linear combination, not another raw16/raw20 solve.

## Bounded solver ledger

Every entry below is a timeout and makes no algebraic claim:

```text
base-only modular, 120s
  b632089dd01538c15f1766b649e84a223dd45e894005ab583f9512b0c93c8c4e
full-product modular, 120s
  bc39bf866b210b46dbf8f5acfb879084a7c9260424f1b5c088986dbaf7e43f74
split-live modular, 120s
  8ea8b557c6f2b3b5f9a5e5b91ef45ba54357a64fbd88f73affdb9b8c5a31acc2
core8 modular, 60s
  ceaba1fd8f7e06a567591f673014690a666540b86ae44ee9aeeb5ba9727c73f2
core8 exact Q, 120s
  56c9b1120d7412ccecb71d5c1c0717736d107a4699d2ffeb615ea3f4219a9f4d
```

Because A-open did not close, the old full `A=B=0` gate was not repeated and
no new claim is made on that branch.

## Replay and precise blocker

`audit_face03130_aopen_status.py` independently checks all Q/modular input
pairs, strict coefficient-first syntax, the fifteen-row and core8 rankings,
the second-pivot growth profiles, and every bounded timeout manifest.  All
three modes pass:

```text
standard  9663532ff2112104878e32e1a5603ecb20a931f5ec85fb4cb7d355bfc4b51dad
-O        2a354f329369a4b6e2eac85c5e6eaea940b342f2e552e8e3deb0a78c2fb53234
-I-S      65926175cb0ab7c48c675c183b25d4cd2fc07e7bbdc2be8faedaa7533ce798df
```

The precise remaining blocker is that no bounded run produced a modular
unit, exact-Q unit, or positive-dimensional component description from
which the seven omitted rows could be reduced.  The exact sparse source
interface is frozen, but emptiness/nonemptiness of the A-open branch remains
open.

## Deterministic component/slice follow-up

The justified component route was attempted without another unsliced gate.
`export_face03130_core8_slices.py` derives three deterministic affine
hyperplanes from the frozen seed
`k5-face-0:31:30-Aopen-core8-affine-slices-v1`.  Their normals have rank
three modulo `1073741827`.  At depths one, two, and three the input consists
of the exact core8 rows, the first `d` affine slices, and the 16-term
degree-17 base-live product as the final F4SAT saturator.  The seven omitted
source rows and transported `c/H` numerators are reserved for component
replay rather than silently imposed.

The three input SHAs are

```text
depth 1  1c094986feae9bc49a847231d2d56793b2a6a222cae04b92d8e88e1eb27c8d05
depth 2  2498b046cfd679753c0270843a30ef470fa5bf7193c1ce145bb59dcbfa586de4
depth 3  f7f10671084c0bd5e9729485c57bbfc798e45a45387bd4bdc53153308ca46ef9
```

Slice-export logical digest:
`a89b1a13274c3bcec14bb7822cce0d056512b179385169c6618ac9c8ef0d3c39`.
Each F4SAT run timed out at its hard 120-second cap before producing a basis.
Consequently no finite residual, positive-dimensional basis, dimension,
degree, RUR, smallest source restriction, unit-slice discovery, or
leading/infinity statement exists to replay.  No second prime was used.

`audit_face03130_core8_slices.py` verifies every slice coefficient, input and
source hash, final-saturator position, F4SAT command, zero-byte output, and
timeout manifest.  Three modes pass:

```text
standard  6f9ca4b370bec71bfd199ebb2f1f70d90580f2905caf7b31b53d9b4a512baf8b
-O        3b6a0912bac9dc758d745586592088533c77032d8f09ab0d84a87eadaa10efc5
-I-S      6481284175efa9b9c634937adc4dc0f3290a95917a005e4e3411b13d8e95ef4f
```

This sharpens the blocker: even three generic affine slices do not expose a
bounded F4SAT basis for core8.  Future work needs a different component
representation or a new sparse source restriction, not more slices of this
presentation.
