# Every two-cell torus obstruction is killed by literal source rows

Date: 2026-08-11

Checker:
`computations/verify_n8_one_bad_axis_pure_all_opposing_pair_elimination.py`

## Exact pair census

The pure-chart character quotient contains `90` off-diagonal residual q
cells and exactly `22` opposing pairs.  The full site/colour stabilizer of
the three coloured pure matchings has order `4`; its action splits the pairs
into seven orbits of sizes

```text
4, 4, 2, 4, 2, 4, 2.
```

The first four-element orbit is exactly the chart-stabilizer transport of
the `c821e58` canonical pair and its two private top-row eliminations.  The
other `18` pairs occupy six genuinely different chart orbits, so they are
not being declared symmetric copies of that calculation.

This is an exact character calculation with the three target weights and
the degree-four source gauge retained, as in `9913c00`.

## Complete symbolic elimination

For each of the `22` pairs, independently adjoin symbolic carriers `x,y` to
the arbitrary fifteen-cell pure-zero form, retain the old coloured q and
endpoint-star coefficients, and expand

```text
q^[3],  p1*s1*q^[2], p1*s2*q^[2],
        p2*s1*q^[2], p2*s2*q^[2].
```

After imposing the target word in each sector, the checker finds a literal
zero row containing exactly one carrier times chart units.  It sets that
carrier to zero, specializes the complete expansion, and finds a second
such row for the mate.  Every pair closes in exactly two steps.

The allowed units are source-provenant:

```text
A,B,C,D and p0,p2,s1,s2   from the two diagonal response anchors,
z03,z12,z45               from the exact 260bb94 pure-chart ideal.
```

The 44 killing rows fall into four unordered factor-pattern classes:

```text
old-q + stars       / pure-unit + stars : 12 pairs
old-q pair          / old-q + stars      :  4 pairs
old-q + stars       / old-q + stars      :  4 pairs
old-q pair          / pure-unit + stars  :  2 pairs
```

Some killers are top rows and some are response rows.  An arbitrary binary
direct coefficient cannot spoil a response killer: its additional term is
the same residual coefficient of `q^[3]`, already zero in the top ideal.

## Consequence and frontier

Axis purification alone did not guarantee toric access, because the weight
system admits the 22 pairwise circuits.  The complete source equations now
remove every one of those minimal circuits.  Thus no **two-cell** mixed
carrier obstruction to the pure chart survives.

This is not an arbitrary mixed-support theorem.  Three carriers can supply
cancellation mates for a row which was unique in the pair calculation.
The checker intentionally stops before that layer; no support CEGAR or
three-cell census is inferred from the pairwise result.
