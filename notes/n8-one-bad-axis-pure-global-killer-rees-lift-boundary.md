# The global killer order is not a target-compatible Rees landing

Date: 2026-08-11

Checker:
`computations/verify_n8_one_bad_axis_pure_global_killer_rees_lift_boundary.py`

## Exact boundary

`1aec4da` gives a sound common **source initial order**: its 54 literal rows
have 54 distinct unit-linear carrier initials, and the 36 other carrier rays
are strictly separated.  This order is not itself a target-compatible
cocharacter.  Indeed, the selected and contaminating terms in every literal
row have the same target character; their strict source-order comparison is
an algebraic standard-basis device, not a source symmetry.

The obstruction persists if one uses the standard basis first and then asks
for a target-compatible landing.  Require

```text
the 54 selected carrier weights >= 0,
the 36 surviving carrier weights >= 1,
all 72 endpoint-star correction weights >= 0,
all 4 binary-direct correction weights >= 0.
```

Together with the 18 chart/target equations of `9913c00`, this rational
system is infeasible.

## Primitive three-inequality certificate

Two literal source-character identities suffice.  The first is one of the
already-eliminated opposing pairs:

```text
chi(03:01) + chi(35:01)
  = chi(03:00) + chi(35:11) = 0
```

in the chart quotient.  The second is carried by the actual response row

```text
11 @ 111011
  = A*s1*(p0*m35:01 + p5*m03:10 + ...),
```

and hence

```text
chi(35:01) + chi(p0) = chi(03:10) + chi(p5).
```

The retained cells `03:00`, `35:11`, and `p0` have weight zero.  Eliminating
`35:01` gives

```text
wt(03:01) + wt(03:10) + wt(p5) = 0.
```

Here `03:01` is one of the 54 selected carriers, `03:10` is one of the 36
survivors, and `p5` is an endpoint-star correction.  The augmented landing
inequalities require

```text
wt(03:01) >= 0,   wt(03:10) >= 1,   wt(p5) >= 0.
```

Adding these three primitive inequalities gives `0 >= 1`.  This is an
integral Farkas certificate with multipliers `(1,1,1)`; no numerical LP is
used.  The separator recorded in `1aec4da` reaches the boundary exactly:
all 54 selected carriers have weight zero, the survivors have weights 1 or
2, and `p5` is forced to weight `-1`.

## Consequence

Thus `1aec4da + 260bb94 + 9070e22` does **not** yet prove emptiness of the
full mixed chart.  `260bb94/9070e22` prove emptiness after a source has
landed in the positive mixed completion of the pure chart; the certificate
above shows that the common standard-basis order does not supply that
landing while keeping the endpoint data finite.

The exact missing step is an equivariant Rees/Weierstrass lift which either
proves `p5=0` from the full source equations before applying the separator,
or replaces the 54-variable graph by source-valid coordinates in which all
endpoint/direct parameters have nonnegative target-compatible weights.
Only after that step may the pure-chart unit be promoted by Nakayama.

No new carrier row, higher Hilbert circuit, or support search enters this
countercertificate.
