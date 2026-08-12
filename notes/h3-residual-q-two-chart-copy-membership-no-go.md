# Primitive chart differences do not realize the residual-q fiber cell

## Verdict

The literal difference between the `pq` and `pr` chart copies cancels every
private full-nine pivot, but it does so by cancelling the **entire physical
column**.  In the physical word

\[
                         01211222
\]

(word `1211222` after deleting the distinguished site), its boundary,
residue, eta terminal, and sigma terminal are all zero.  The only surviving
quantity is a chart-odd presentation readout.  Before the marked top is
taken, that readout has the three-term tail

\[
 h_1=q_{23}^{21}q_{45}^{12}
       +q_{24}^{21}q_{35}^{12}
       +q_{25}^{22}q_{34}^{11},
\]

not the required endpoint-odd correction

\[
                         -q_{00}+q_{11}.
\]

Thus the primitive chart class cannot be the one-cell lift required by the
residual/eta/sigma fiber-product criterion.  This is an exact no-go for
primitive chart-copy differences and their common monomial multiples, not
for a new chart-nondiagonal higher comparison.

## The physical-word calculation

The direct-free full-nine row at `01211222` has 90 distinct matching terms.
Its two literal presentations split as

```text
pq chart: 15 direct + 75 two-star
pr chart:  0 direct + 90 two-star.
```

After forgetting chart and sector tags, each presentation is the identical
90-term polynomial.  Therefore

\[
 d(c_{pq}-c_{pr})=0
\]

coefficientwise, including all word-private matching coordinates.  Every
physical linear readout, and every physical derivation followed by such a
readout, factors through this forgotten polynomial.  Consequently

\[
 (D,\operatorname{ores},\eta,\sigma)(c_{pq}-c_{pr})=(0,0,0,0).
\]

This already excludes the required fiber target

\[
 \operatorname{ores}=-\delta=(-1,1,1,-1),\qquad
 \eta_z=1+\delta_{vz}u_z/t,\qquad
 \sigma=-q_{pq}^{22}.
\]

Retaining chart tags explains why the difference nevertheless looks useful.
Removing the physical endpoint cells `(pq:22,xv:0m)` puts the same `h_1`
above in the `pq` direct sector and in the `pr` two-star sector.  Their
chart-odd difference forgets to zero.  It contains the selected mixed corner

\[
 q_{11}=q_{24}^{21}q_{35}^{12}
\]

with coefficient one, but contains no pure corner

\[
 q_{00}=q_{24}^{11}q_{35}^{11}.
\]

It is therefore not even the two-term endpoint-odd shadow
`-q00+q11` of `-delta`.

Adding the aligned internal matching `((2,4),(3,5))` makes each chart top a
unit.  The normalized chart-odd cochain reads one on their difference.  The
four marked edges have site profile `(1,1,1,1,1,1,1,1)`: this is the
squarefree `4K2` comparison cube already found in the third-cofactor gate.
Its unit is presentation H1, not a physical residue, eta, or sigma terminal.

## The repeated `P3+K2` grade

The five complete first rootless repeated components have endpoint colour
slots

```text
p: colour 0 only
q: colour 0 only.
```

Hence the physical word `01211222`, which has colour 2 at both endpoints,
is absent from all five components.  The zero-endpoint chart word
`00211200` is present in every component.  Its multiplier census is

```text
component:                 0   1   2   3   4
selected multiplier hits: 12  12   6  12  12
private pivots/column:   45-46 45-46 45-46 42 45-46
```

For each of these 54 selected columns, the `pq-pr` copy difference cancels
all 90 boundary terms, including the 42--46 private pivots.  But the complete
rank calculation is sharper: each component has 576 doubled columns, rank
288, and kernel dimension 288.  Since the one-chart map is injective, those
288 pairwise differences are the entire kernel.  It contains no further
combination with a different physical landing.  Moreover the complete
two-chart kernel has

\[
   (\operatorname{anchor},\operatorname{target},W,
     \operatorname{ores})=(0,0,0,0).
\]

Thus the repeated component supplies the same presentation-kernel mechanism
at the wrong endpoint word; it does not transport the physical-word chart
unit into the residual-q packet.

No pairwise difference has an intrinsic physical terminal meaning.  A
physical terminal must be invariant under changing the chart presentation,
so it assigns the same value to the two copies and vanishes on their
difference.  A chart-odd terminal can be nonzero—this is exactly the marked
Hasse unit—but it is presentation data until an additional comparison cell
and differential make it descend.  The `576/288/288` census therefore
confirms rather than evades the obstruction.

## Common-multiplier guard and remaining interface

If two chart copies present the same literal polynomial, multiplication by
the same monomial preserves that equality coefficientwise.  It preserves
the zero physical boundary and every descended zero readout, and it does not
change the source word.  Therefore no common repeated `P3+K2` tail can turn
the primitive chart difference into the desired fiber cell.

The remaining positive theorem must introduce a genuinely
**chart-nondiagonal relative differential**: a higher source cell whose
physical landing is nonzero and whose three projections are simultaneously
`-delta`, the eta primitive, and the sigma correction.  Cancelling private
pivots by subtracting identical chart copies is insufficient because it also
cancels precisely those physical projections.

## Verification

Run

```text
python3 computations/verify_h3_residual_q_two_chart_copy_membership_no_go.py
python3 -O computations/verify_h3_residual_q_two_chart_copy_membership_no_go.py
python3 -I -S computations/verify_h3_residual_q_two_chart_copy_membership_no_go.py
```

The frozen ledger SHA-256 is

```text
2c1187a432a461efaab2868729126f7ca1b931cff8ed9440ecae90939738de08
```
