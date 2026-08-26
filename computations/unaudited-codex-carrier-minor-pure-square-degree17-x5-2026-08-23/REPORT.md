# First pure-normalization prolongation: minimal lift obstructed, full target bounded

Status: **UNAUDITED exact theorem on the minimal inverse-system shell; global
degree-17 membership remains bounded/unresolved**.

## Question and literal dual formulation

Let `lambda` be the exact 44-term degree-13 integer separator for
`F_00000000*Delta`, frozen in the
[preceding report](../unaudited-codex-carrier-minor-pure-amplitude-degree13-x5-2026-08-23/REPORT.md).
It annihilates every degree-9 mixed-X5 translate and pairs with
`F_00000000*Delta` as `2`.

A genuine degree-17 prolongation `Lambda` would satisfy

```text
F_00000000 . Lambda = lambda
```

under inverse-system contraction, annihilate every degree-13 translate of
the five compatible mixed X5 amplitudes, and consequently pair with
`F_00000000^2*Delta` as `2`.

## Exact minimal-shell obstruction

The smallest literal support shell is

```text
S0 = supp(lambda) * supp(F_00000000).
```

The exhaustive source census is

```text
supp(lambda)                         :    44
pure matching terms                  :   105
distinct S0 variables                : 4,559
contraction equations touching S0    : 4,457
mixed-X5 translate equations         :10,639
total affine rows                    :15,096

X5 rows by word:
  00000001 : 3,347
  00000010 :   802
  00000011 : 3,348
  00000020 :   845
  00000021 : 2,297.
```

There is no `Lambda` supported on `S0` with
`F_00000000.Lambda=lambda`.  The contradiction occurs already among the
contraction equations, before any X5 row is used.

An exact rational replay produces a 74-row certificate with coefficients
only `+/-1`:

```text
combined left-hand side : 0
combined right-hand side: 2
certificate SHA-256     : ce278f2e8387ac6bc2d97f02d8078012ac2544638cd42512c728fd85bbe3c5fa.
```

Thus the old 44-term obstruction does **not** prolong merely by adjoining
one pure matching factor.

## Mandatory enlargement and cap

In the unrestricted contraction space, the 74 certified quotient rows also
contain variables outside `S0`.  Their exact census is

```text
inside variables occurring in the certificate :   105
outside repair variables                       : 5,949
S0 plus all certificate repairs                 :10,508.
```

The frozen next-shell cap was 10,000, so the necessary repair layer already
exceeds it.  No inference about the full contraction map is made from the
minimal-shell contradiction.

## Direct degree-17 membership screen

Independently, a support-driven empty-seed CEGAR tested the target

```text
F_00000000^2 * Delta
```

without materializing it.  Target coefficients were evaluated on demand
from the 6,900-term `Delta` and the 5,250-term `F_00000000^2` factor.  It did
not terminalize before its frozen size cap:

```text
completed growth rounds : 109
rank                    : 5,711
tracked columns         : 391,585
basis nonzero entries   :12,135,624  (> 12,000,000 cap)
last dual support       :   106.
```

This is neither membership nor nonmembership.  In particular, pure
normalization is **not proved** to kill or preserve the obstruction at
degree 17.  What is proved is the sharper negative statement that the
canonical minimal inverse-system lift is impossible and any repair must
leave its 4,559-variable shell.

## Replay

The exact contraction certificate is deterministic in all modes:

```bash
python3 computations/unaudited-codex-carrier-minor-pure-square-degree17-x5-2026-08-23/screen_exact_separator_prolongation_shell.py
python3 -O computations/unaudited-codex-carrier-minor-pure-square-degree17-x5-2026-08-23/screen_exact_separator_prolongation_shell.py
python3 -I -S computations/unaudited-codex-carrier-minor-pure-square-degree17-x5-2026-08-23/screen_exact_separator_prolongation_shell.py
```

Frozen exact logical digest:
`c9ef83c02337abee12074a63f7f942e4574ac45759d1d3d8d98129da401915b4`.

The bounded direct-screen result SHA-256 is
`4e84b361dbb130197ec7fb5aa40e8072eb67f5ddc6b3d70c4ea1bc85f194ba5a`.
