# The first axis-pure cancellation stratum is a literal coloop packet

## Result

The support-`17` coupled-circuit stratum isolated by `0ba6a00` is empty.  In
fact, no axis-purified support through `26` can satisfy even the necessary
no-singleton condition for the complete unary and four response rows.

The first possible supports occur at size `27`.  They have one structural
type, up to site relabelling and swapping bright colours:

```text
q:00 support: one perfect matching F0,
one bright q support: K2,2 on four sites,
the other bright q support: K2,4,
p_i and s_i: the corresponding four-site/two-site shores.
```

Every edge of `F0` belongs to every pure-zero matching—there is only one—so
all three are literal pure-colour coloops.  Thus

\[
\boxed{\text{the first coupled cancellation stratum enters the coloop branch}.}
\]

Checker:

```text
computations/verify_h3_axis_pure_singleton_mate_closure_coloop_gate.py
```

Frozen ledger digest:

```text
17c8da7536f8e9b01e4fb6a30da1313080b03603453d751356dabdf17a26c7e4
```

## The structural closure operation

Suppose an off-target matching fibre contains exactly one supported
monomial `M`.  Every occupied coordinate is nonzero, so the coefficient of
`M` cannot vanish.  An exact source must contain a second monomial `N` in
the same fibre.  Adjoin the coordinates of `N-M` and repeat.

This is a support-level form of the matching-circuit exchange.  Two
perfect matchings in one word fibre differ by alternating even cycles; the
new coordinates are the missing half of those cycles.  On six sites the
unary exchange costs are exactly:

```text
405 pairs requiring two new q coordinates,
180 pairs requiring three new q coordinates.
```

The unary fibre sizes are `90` singleton fibres, `90` three-matching fibres,
and the three monochromatic fibres of size `15`.

The recursive search chooses the current singleton with the fewest
available mates and explores every minimal mate.  This is exhaustive for a
fixed support budget: any no-singleton super-support must contain one of the
explored mates for that chosen singleton.

## Exact first-stratum census

Starting from the `185` target-skeleton orbits, monotonicity lets the checker
test the two boundary budgets:

```text
support budgets 17,...,26: no closure,
support budget 27:         12 labelled closures,
                           2 S6 orbits of size 45.
```

The two site orbits exchange under `1<->2`, so there is one type after
bright-colour symmetry.  The search visits `13,615` closure states at budget
`27`; no random sampling or coefficient genericity is used.

The graph description is intrinsic.  The `q:00` graph is `3K2`, one bright
graph is `K2,2` with degree profile `(2,2,2,2)`, and the other is `K2,4` with
degree profile `(4,4,2,2,2,2)`.  The corresponding endpoint shores have
sizes four and two, with `p_i` and `s_i` occupying the same shore.

## Consequence and remaining scope

At a maximum-anchor/minimum-support exact axis source:

* support is at least `27`;
* if equality holds, a literal pure-zero coloop is present.

This is the same matching-theoretic output used by the existing
four-good-or-coloop theorem.  It is **not** yet the normalized endpoint
target-coloop packet.  The separate arbitrary-coloop theorem must still
transport the internal `F0` coloop, common-`q` tail, response heads, and
four-hole rows into the committed target-coloop/Hall landing.

The size-`27` supports satisfy only a necessary support condition.  The
checker does not assert that coefficients exist which solve the complete
equations; coefficient incompatibility would only strengthen the result.
For supports above the first stratum, one may either continue the closure
or exploit the explicit `K2,2/K2,4` incidence to normalize the coloop.
