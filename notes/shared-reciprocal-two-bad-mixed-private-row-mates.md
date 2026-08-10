# Minimal mates of both private bright rows kill the second kernel

## 1. Four simultaneous repair types

The minimal rank-13 packet from
[`the second-kernel gate`](shared-reciprocal-two-bad-mixed-second-kernel-gate.md)
has

```text
K2 = CCCC -2 CCAT +TACC.
```

Each private word has exactly two unused matching paths:

```text
CCAT:
  03:ca * 14:ct,       or       04:ct * 13:ca;

TACC:
  03:tc * 14:ac,       or       04:tc * 13:ac.
```

Consequently there are four simultaneous mate types.  Every minimal mate
uses four new endpoint-colour coordinates: two for each word.  If the first
pair has weights `x,y` and the second `p,q`, coefficient cancellation
requires

```text
xy=2,                 pq=-1.                            (1)
```

The checker works on the Laurent charts

```text
y=2/x,                q=-1/p,
```

so every nonzero coefficient is retained exactly.

## 2. Repair-invariant rank restoration

The old kernel

```text
U=e_t@0-e_a@1
```

survives every one of the four repairs.  The second kernel

```text
V=e_a@3-e_t@4
```

does not.  In each chart `Phi(V)` has four distinct private word
coordinates with Laurent-monomial coefficients; none can vanish when
`x,p` are nonzero.

More strongly, delete the duplicate column supplied by `U`.  For each of
the four types the checker extracts a literal `14x14` cofactor-map minor:

```text
det = -16/p^2    for a CCAT mate through 03/14,
det = +16/p^2    for a CCAT mate through 04/13.          (2)
```

The choice of TACC route does not change (2).  Thus over characteristic
zero, after localizing (1), every minimal simultaneous repair satisfies

```text
rank(Phi)=14,          ker(Phi)=<U>.                     (3)
```

This is a repair-invariant determinant lemma, not a coefficient sample.
It also excludes a hidden deformed second kernel: the nullity is exactly
one on the entire Laurent chart.

## 3. The missing pure class remains absent

No repaired support has a second `tt` physical edge, so every column of
`Phi` has zero `X_t` coordinate.  By (3), all kernel products reduce to
`P*U*U*q`; every nonzero term uses the `a` component of `U` at site `1`,
and hence also has zero `X_t` coordinate.  Therefore

```text
X_t notin im(Phi)+span{P*ker(Phi)*ker(Phi)*q}.           (4)
```

At unit Laurent representatives the exact rank summary is `(14,1,16,0)`:
even the augmented pure intersection is zero.  The mates repair the two
named `K2` coefficients but create further source-provenant mixed rows; no
bright pure class survives in the displayed representatives.

## 4. Scope and consequence

This closes all minimal simultaneous mate types for the two private rows
of the canonical second-kernel packet.  It is not a theorem about an
arbitrary larger path-switch network.  A true local seed must use a
non-minimal coupled repair whose extra cells both preserve a rank-13
cofactor map and restore the bright rows; independent minimal mates cannot
do so.

## 5. Reproduction

```sh
uv run python computations/verify_shared_reciprocal_two_bad_mixed_private_row_mates.py
uv run python -O computations/verify_shared_reciprocal_two_bad_mixed_private_row_mates.py
```

Both modes reproduce

```text
1eb4972f703b3567d62621f82c87a10b87f7200837306fa43e52fa0802b771fe
```
