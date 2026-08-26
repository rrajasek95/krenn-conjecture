# Minimal S3 duals see only the support-unit carrier channel

Status: **UNAUDITED exact finite census**.

All 28 minimal three-row exact separators of the frozen residual-52
degree-five low-source component were reconstructed over `Z`.  Restricting
every row to its oriented response-half readings at the fixed carrier pair
`67` gives a subspace of `Mat_3^*` of rank exactly one:

```text
span = <K_00>.
```

There are 84 dual rows in total.  Forty-four have one fixed-`67` response
reading and forty have none; every one of the 44 readings has endpoint
colours `(0,0)`.  Of the 28 dual restrictions, 16 are nonzero and 12 cancel
to zero.  No restriction reaches any of the eight coordinates introduced by

```text
K_00 = <K,A_67> - sum_(ab != 00) A_67[ab] K_ab.
```

Thus the direct substitution is not closed by the minimal dual space alone.
Colour transport supplies the analogous support-unit diagonal channel in a
transported chart; it does not supply the eight corrections in this fixed
chart.

## Relation to the triangle pure quotient

The archived literal `15+90` identity proves, on an exact normalized `X5`
point, the quotient equations

```text
[K_cc] = H_c [<K,A_67>]  mod rowspan(L_T).
```

Consequently, on the simultaneous five-set rank-nine open and
`H_0 H_1 H_2 != 0`, any one of the four blocker memberships gives all four.
This is an actual localized row-space filler: rank nine and Cramer's rule
express the internal response rows in `L_T`, and the pure identity transports
between the direct and diagonal blocker forms.  Its exceptional divisors are
the chosen rank-nine minors and the three `H_c`.

This does **not** yet fill the S3 attachment.  The three-row object here is a
cokernel functional: it annihilates every frozen low-source column and pairs
nontrivially with residual S3.  Its carrier restriction keeps only one
oriented half of a response row.  Passing to a full response introduces the
crossed companion, and no chain producing/cancelling that companion is part
of the quotient theorem.  Hence the quotient collapses the blocker clause on
the open, but it does not convert this obstruction functional into a
source-labelled S3 preimage.  Besides the rank-drop and `H_c=0` boundaries,
the crossed-half/chain-coherence attachment remains to be proved.

## Replay

```sh
python3 computations/unaudited-codex-n8-s3-carrier-restriction-2026-08-23/audit_s3_carrier_restriction.py
python3 -O computations/unaudited-codex-n8-s3-carrier-restriction-2026-08-23/audit_s3_carrier_restriction.py
python3 -I -S computations/unaudited-codex-n8-s3-carrier-restriction-2026-08-23/audit_s3_carrier_restriction.py
```

The hostile `--mutate` mode must fail.

Frozen script SHA256:
`9d24490f9ef4b26bae2fd49432fb6dbdebbc45f85092ee33b67ff08ee51c78e9`.
Result SHA256:
`52f325e4d19769189a33ff4b04a0a9c8b6ebc1655ff58b460cedb2c4456d1948`.
Logical digest:
`24b3590e37a3ed115e9370904ed0f211c661d90e02ef7d738f4d47853d1ad8e9`.

Scope is exactly the 28 minimal size-three separators and fixed carrier pair
`67`; larger dual supports and higher HPL corrections are not classified.
