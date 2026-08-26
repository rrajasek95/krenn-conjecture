# The 34-column packet attaches to the literal `F^h` cochain in bidegree `y^8 t^4`

## Exact result

The frozen 34-column correction is an exact **cochain** attachment.  After
multiplication by `t^4`, it sits in total degree twelve and preserves pairing
one with the literal normalized pure target `F^h`.  It changes the bounded
degree-eight boundary as follows:

```text
old nonzero boundary columns       252
old columns killed                  59
34-column antichain killed          34 / 34
new exterior columns                 0
remaining nonzero columns          193
```

All 193 survivors have at least one literal translated source leg in the
complete degree-five Buchberger packet.  No genuinely new cell appears in
this layer.

## Variance and target guards

The 23 leaf coefficients and 43 hard-block coefficients index output rows;
they extend the dual cochain.  They are not primal coefficients of mixed
generator columns.  The exact target statements are:

```text
dehomogenized 564-row residual pairing       -1 -> -1
constant pairing                              1 -> 1
literal F^h pairing after t^4 shift           1 -> 1
attachment-only F^h pairing                        0
```

Thus the reusable attachment lemma is:

> In the normalized chart-26 `y^8 t^4` layer, the invariant 66-row
> attachment preserves the literal `F^h` pairing, kills the complete
> 34-column complement, creates no new crossing, and leaves a coboundary
> supported entirely on translated legs of the complete degree-five source
> cells.

The result JSON exports all 564 target-residual rows, all 66 attachment
weights, all 193 surviving columns and exact pairings, word profiles,
matching skeletons, and degree-five source-leg multiplicities.

## Alignment with the direct `F^h` filtration

This packet has top bidegree `y^8 t^4`.  It therefore lies inside the
independently reported acyclic `y`-degrees six through nine.  The first
direct `F^h` core is two off-degrees later, at `y^10 t^2`, where the minimal
source columns have quadratic multipliers and three-term exchanges.

Consequently this theorem is a reusable lower attachment, not closure of
the `y^10 t^2` core.  Testing quadratic translates of the four gain-cell
interfaces against that core requires the literal core export; no inference
about it is made here.

## Replay

```text
python3 audit_antichain_attachment.py --check-results
python3 -O audit_antichain_attachment.py --check-results
python3 -I -S audit_antichain_attachment.py --check-results
python3 audit_antichain_attachment.py --mutate   # must fail
```

Logical digest:

```text
e94ed3e206b8652c0e20e662dc7f0a406e947406287d80719531d4d03a9550d3
```

This does not contract the 193 exchange-supported columns, decide the
`y^10 t^2` core, or make a degree-nine-and-higher saturation claim.

## PM4/PM6 translated-gain test

The four gain cells have minimum-layer types

```text
round 0: 4 unique-linear words
round 1: 4 unique-linear words
round 2: 1 PM4 word (degree2/support3) + 4 PM6 words (degree3/support15)
round 3: 22 unique-linear words.
```

Thus only round 2 can implement the proposed four-site/six-site bridge.  Its
literal unmatched sets do nest: on each of the four actual stabilizer
representatives,

```text
U6 = U4 union {2,5}.
```

The source labels do not nest.  The PM4 and restricted PM6 words induce
different colour-equality partitions on `U4`; equivalently, the three terms
obtained by slicing the PM6 coefficient on its `25` edge have zero literal
overlap with the three PM4 terms.  No global colour permutation repairs an
equality-partition mismatch.  Hence a common-unlabelled-vertex-set theorem
is true, but the needed common source-matrix theorem is false.

As a bounded core probe, the checker translates this bridge by the two
cells `(01;01),(23;00)` and by `t^2`, then performs the deterministic
unique-linear contraction through `y^8,y^9`.  It uses 101 literal pivots:

```text
initial:  y8:3, y9:84, y10:438
terminal: y10:1,064, y11:3,088, y12:6,664.
```

The 1,064 degree-ten coefficients are `556` plus ones and `508` minus ones.
Every row meets between 6 and 20 PM4 core columns; none is a leaf.  This
translate therefore lands inside the coupled PM4 incidence core but does
not close it.  Its degree-ten row digest is
`c790249778f988a2a0a0845b77848992a4d67765c9c382868494dc5179e89fec`.

Replay the separate checker:

```text
python3 audit_pm4_pm6_translated_bridge.py --check-results
python3 -O audit_pm4_pm6_translated_bridge.py --check-results
python3 -I -S audit_pm4_pm6_translated_bridge.py --check-results
python3 audit_pm4_pm6_translated_bridge.py --mutate   # must fail
```

Its logical digest is
`7b455d8d3c33408afbb72ef62c588332cd49f9126f092933279378f5a29f9c81`.
The producer-reported 63.6-million-row export is not used: it currently
propagates only the truncated `R6` tail and has not yet been audited as the
full direct-`F^h` degree-ten residual.
