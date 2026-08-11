# Cubic anchor-union matchings have three multiply-used web types

## Result

Let `Q_0,Q_1,Q_2` be the three selected pure target matchings on six
residual sites, and let `R` be the physical perfect matching supporting a
cubic ordered-`01/10` decoration.  Assume

\[
                         R\subset Q_0\cup Q_1\cup Q_2. \tag{1}
\]

There is a complete incidence dichotomy.

1. `R` has a multiplicity-one edge `e`, used by exactly one `Q_c`.  At
   either endpoint of `e`, the other two selected matchings block at most
   two companion neighbours.  Hence at least `N-4=2` possible active sites
   are free.  Once the target-preserving alternating repair of `Q_c` is
   selected, `c78fc9b` gives the distinct-head four-good landing unless all
   nonzero `Delta C` products are concentrated on the one or two blocked
   neighbours.
2. Every edge of `R` has multiplicity at least two.  Then at least two of
   `Q_0,Q_1,Q_2` equal `R`.  The third selected matching shares exactly
   `0`, `1`, or `3` edges with `R`.  Up to `S_6 x S_3`, these are exactly
   the three webs

   \[
                    (222),\qquad(223),\qquad(333).     \tag{2}
   \]

Thus the finite source-identity input is not an arbitrary cubic support
family: it is the three fully multiply-used webs (2), together with the
multiplicity-one states whose active products are trapped on at most two
anchor neighbours.

Checker:
`computations/verify_uniform_cubic_anchor_union_incidence_dichotomy.py`.

## Hand proof of the multiply-used classification

Suppose every edge of `R` occurs in at least two selected matchings.  The
three edges of `R` then have at least six incidences among `Q_0,Q_1,Q_2`.
By pigeonhole, some `Q_c` contains at least two edges of `R`.  Two perfect
matchings on six vertices which share two edges necessarily share the third,
so `Q_c=R`.

After removing that copy, the two remaining selected matchings must together
cover every edge of `R`.  One of them contains at least two edges of `R` and
hence is also equal to `R`.  The last matching can share neither exactly
two edges nor any number larger than three; its intersection size is
`0`, `1`, or `3`.  These give (2), respectively.

Canonical representatives, writing `R=01|23|45`, are

```text
222: Q0=R, Q1=R, Q2=02|14|35
223: Q0=R, Q1=R, Q2=01|24|35
333: Q0=R, Q1=R, Q2=R.
```

This argument is coefficient-free and does not depend on a support
cardinality layer.

## The multiplicity-one landing and its exact guard

Let `e=vu` be used only by `Q_c`.  The alternating pure-`c` repair `Q_c'`
avoids `e`, so `(Q_c',Q_d,Q_f)` makes both deleted stars of `e` rank three.
At endpoint `v`, the two other target matchings have only the neighbours
`Q_d(v),Q_f(v)`.  Every other site `s` outside `e` gives a companion edge
`vs` absent from both, and `(Q_c,Q_d,Q_f)` makes both deleted stars of `vs`
rank three.

The target-augmented identity

\[
             q_u+\sum_s\Delta_{us}C_s=0              \tag{3}
\]

therefore lands as soon as one nonzero product in (3) uses a free `s`.
The nonzero determinant supplies distinct centre heads and the cofactor
supplies activity.  Failure is exactly concentration of every nonzero term
of (3) on the one or two blocked neighbours.  This is the trapped branch
already isolated by `c78fc9b`; the cubic matching introduces no new
incidence failure for a multiplicity-one edge.

## Exact finite audit

The checker enumerates only the finite matching-incidence object: all
`15^3` selected matching triples and every physical perfect matching `R`
contained in their union.  The `10,185` states have multiplicity histogram

```text
111  3600       112  4320       113   540
122  1080       222   360       223   270       333  15
```

Exactly `9,540` states have a multiplicity-one edge, and every such edge
has at least two free active sites at either endpoint.  The `645` fully
multiply-used states split as `360/270/15` across (2).  Canonicalization
under all site and target-colour permutations finds exactly one orbit for
each of `222`, `223`, and `333`.

The census audits the hand proof.  It is not a source-support search.

## Coefficient closure in the concentrated chart

The exact cubic aggregate theorem `2cbdffb` is the coefficient endpoint for
this finite residual.  Its bounded inventory is all `15*2^3=120`
ordered-`01/10` decorated perfect matchings.  They form `32` stabilizer
orbits, and every orbit has an ordinary source-row unit.  Thus every
orientation of (2) and every trapped multiplicity-one state is empty in the
concentrated-spoke fine-degree module.

With the fixed response holes restored as physical anchor edges, that
module has `245` anchor-union physical configurations, or `1,960` after the
eight endpoint-colour decorations.  Its multiplicity signatures are

```text
111:132   112:80   113:4   122:24   222:4   223:1.
```

The general `333` incidence orbit cannot occur in this particular
concentrated normalization because the two response matchings contain the
distinct restored hole edges `01` and `23`; it remains part of the uniform
arbitrary-selected-matching theorem.  No further incidence subdivision is
needed for the concentrated cubic chart.

This closure is scoped to the concentrated ordered-`01/10` fine-degree
module.  It does not identify arbitrary multisite-star packets with that
module, cover other ordered colour sectors, or prove compatibility of the
orbitwise units when several decorated perfect matchings are simultaneously
supported.

## Verification

Run

```text
python3 computations/verify_uniform_cubic_anchor_union_incidence_dichotomy.py
python3 -O computations/verify_uniform_cubic_anchor_union_incidence_dichotomy.py
python3 -I -S computations/verify_uniform_cubic_anchor_union_incidence_dichotomy.py
```

The checker pins `c78fc9b` and the quadratic/cubic aggregate closures,
verifies the hand pigeonhole argument state-by-state, freezes the three
canonical web types, and audits the complete normalized incidence census.

Frozen ledger SHA-256:

```text
fc2232f6fac0f896a7c70da2a557fdbb924c3be857cc6b3bd860450be4241336
```
