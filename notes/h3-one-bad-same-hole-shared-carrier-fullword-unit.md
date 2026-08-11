# The canonical shared-carrier packet has a literal two-row unit

Date: 2026-08-11

Checker: `computations/verify_h3_one_bad_same_hole_shared_carrier_fullword_unit.py`

## Verdict

The exact `17`-cell shared C/A carrier packet reached in `f057798` is empty.
There is no coefficient-consistent rational guard on this support and no
need to invoke the still-open general curved-OO transport theorem.

The checker constructs all `3^8=6561` literal full-output generators.  On
the pinned support, `29` words have physical tails containing `31` distinct
matching monomials; the remaining `6532` rows are literal zeros.  There are
already `24` mixed words whose coefficients are single monomials in the
localized carrier/star units.

## Ordinary two-row certificate

An especially transparent certificate uses the pure and mixed words

```text
00000000,  00000001.
```

Both have the unique physical matching

```text
01 | 27 | 34 | 56.
```

Put

```text
M  = q01:00*q34:00*A56:00,
ra = A27:00,
rc = A27:01.
```

The two exact full-source generators are

```text
Gpure  = ra*M - 1,
Gmixed = rc*M.
```

Therefore the determinant-cleared identity is

```text
ra*Gmixed - rc*Gpure = rc.
```

The same-hole `R_c` coefficient `rc` is one of the forced localized units,
so the localized full-word ideal contains one.  On the fixed normalization
used in `f057798`, `ra=1` and `rc=-2`, giving the ordinary polynomial-row
identity over `Q`

```text
1 = (-1/2)*Gmixed - Gpure.
```

This is source-valid: both generators are literal original eight-site
coefficient rows and the checker reconstructs their unique matchings from
the physical cells.

## Scope

This closes the canonical carrier-only residue packet, not every completion
with extra support.  Adding arbitrary residue cells can add matchings to the
two selected words and destroy their unique-tail equality; that larger
support stratum is intentionally outside this bounded test.  Extra endpoint
stars and the general active curved-doubly-good overlap also remain separate.
