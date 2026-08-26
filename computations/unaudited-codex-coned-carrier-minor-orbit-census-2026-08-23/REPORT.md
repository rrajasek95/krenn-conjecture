# A coned carrier-minor certificate has 124 inequivalent same-colour orbits

Status: **UNAUDITED exact finite `S8 x S3` orbit census**.

## Verdict

Fix the canonical carrier `(cap,triangle)=(67,012)`, residual colour zero,
and the target

```text
M = 01|23|45|67 in pure colour 0,
Delta = det C_0[{01,11,21},{01,02,12}].
```

One certificate for `M*Delta` does **not** transport to all 105 pure
matching charts and all 56 maximal minors of every `C_c`.  On any fixed
carrier and colour its orbit reaches only

```text
9 matching charts x 4 row minors = 36 target pairs.
```

The four minors are

```text
{01,11,21}, {02,12,22}, {10,11,12}, {20,21,22}.
```

The nine matchings have the same block incidence as the base matching:
one edge inside the triangle, one triangle--outside edge, one edge inside
the outside triple, and the cap edge itself.

## Exact orbit count

After fixing the carrier and residual colour, the stabilizer is

```text
S3(triangle) x S3(outside) x S2(cap)
  x S2(the two nonresidual colours),                  order 144.
```

It has:

```text
matching-chart orbits                         6
minor-rowset orbits                          17
joint (matching,rowset) orbits              124.
```

The 124 joint orbit sizes are

```text
size 12: 6       size 18: 6       size 24: 11
size 36: 51      size 72: 50.
```

They exceed `6*17=102` because the cap transposition acts simultaneously on
the matching and on the ordered cap-colour row labels; the two marginal
classifications cannot be chosen independently.

Restoring all 560 `(cap,triangle)` carriers and all three residual colours
gives `9,878,400` same-colour coned-minor targets.  They still form exactly
124 full `S8 x S3` orbits, with sizes

```text
20,160 (6), 30,240 (6), 40,320 (11),
60,480 (51), 120,960 (50).
```

The canonical target has full orbit size `60,480` and stabilizer order four.
Its intersection with any fixed carrier/colour is the 36-pair family above.
Determinant signs from column permutations are immaterial for ideal
membership and are quotiented in this census.

## Proof-spine consequence

On a pure-normalized exact source, for each colour at least one of the 105
pure matching monomials is live, but its incidence type is not known.  To
deduce every maximal minor by summing over the pure matching cover, the
same-colour coned strategy therefore needs one certificate for each of the
124 joint orbit representatives—not one canonical certificate, and not
merely `6+17` marginal representatives.

If the cone colour is allowed to differ from the carrier residual colour,
colour equality is itself invariant.  The different-colour family has 236
more orbits, for 360 total.  The natural strategy should keep cone colour
equal to carrier colour and target the smaller 124-orbit packet.

This is an orbit-counting obstruction, not a polynomial nonmembership
result.  It says exactly how large an orbit-complete coned carrier-minor
certificate family must be before the rank-drop bridge can be claimed.

## Replay

```bash
python3 computations/unaudited-codex-coned-carrier-minor-orbit-census-2026-08-23/audit_coned_carrier_minor_orbits.py --check-results
python3 -O computations/unaudited-codex-coned-carrier-minor-orbit-census-2026-08-23/audit_coned_carrier_minor_orbits.py --check-results
python3 -I -S computations/unaudited-codex-coned-carrier-minor-orbit-census-2026-08-23/audit_coned_carrier_minor_orbits.py --check-results
```

Frozen logical digest:
`d6fde3a28b9814848aead1185e9d40ac590facd3e9ddd3528e8a6ae6e861f085`.
