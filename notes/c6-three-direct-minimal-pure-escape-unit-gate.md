# Minimum pure escapes from the seven-cell three-direct guard hit a source unit

## Result

Start with the labelled diagonal `C6` packet

```text
cap 34:       34;0, 34;1, 34;2
core fine:    05;1, 12;1
mate fine:    01;1, 25;1
window/tail:  0125 / T.
```

Its only supported words are

```text
111001 : 2 terms, operation coefficient:111001
111111 : 2 terms, operation coefficient:111111
111221 : 2 terms, operation coefficient:111221.
```

The two mixed rows force the common residual `H` to vanish.  Pure
normalization then forces a cap-avoiding colour-one escape `E1=1`.

There are exactly eight support-minimum first escapes, each adding two cells.
They form two orbits under the order-eight stabilizer retaining cap `34`, the
core fine, and the mate fine.  Every first escape gives the same nine-cell
local guard:

```text
111001 : 2 terms
111111 : 3 terms
111221 : 2 terms,
```

with no mixed singleton and localized equations `H=0, E1=1`.  Thus the first
repair is genuinely locally consistent; a unit does not appear one step too
early.

However, every support-minimum attempt to supply either missing pure colour
next creates a literal mixed singleton.  There are 96 labelled second-step
realizations for colour zero and 96 for colour two, and all 192 are source
units.  Hence the support-minimal escape chain cannot recur.

The checker is
`computations/verify_c6_three_direct_minimal_pure_escape_unit_gate.py`.

## 1. The eight first escapes

A cap-avoiding perfect matching can contain at most one of the four old
residual edges.  Indeed, the only disjoint old pairs are

```text
05|12 and 01|25,
```

and both leave `34` as the third edge.  Therefore a cap-avoiding colour-one
matching must add at least two decorated cells.  Exactly eight matchings
attain the bound:

```text
01|23|45   01|24|35
03|12|45   03|14|25
04|12|35   04|13|25
05|13|24   05|14|23.
```

The labelled stabilizer has two orbits of size four.  Canonical
representatives are

```text
mate-edge orbit:  01|23|45
core-edge orbit:  03|12|45.
```

The distinction is load-bearing because the core and mate fine matchings are
retained, rather than quotienting the two coefficient terms.

For any such escape, write

\[
 H=q^1_{05}q^1_{12}+q^1_{01}q^1_{25},
 \qquad E_1=\prod_{e\in M_1}q^1_e.                         \tag{1}
\]

The complete local equations are

\[
 q^0_{34}H=0,\qquad q^2_{34}H=0,\qquad
 q^1_{34}H+E_1=1.                                         \tag{2}
\]

All three cap cells are live, so (2) is equivalent to

\[
                              H=0,qquad E_1=1.             \tag{3}
\]

This Laurent system is proper over the intended complex field: the two
terms of `H` can cancel while the two new escape weights normalize `E1`.
The nine-cell packet is therefore the smallest exact **local** guard, though
it is not a full GHZ source because pure colours zero and two are still
missing.

## 2. Every next minimum pure escape is a singleton unit

For colour `c=0` or `c=2`, none of the old residual cells has colour `c`.
A cap-avoiding pure matching therefore needs exactly three new decorated
cells.  All twelve cap-avoiding physical matchings attain this minimum.
Pairing them with the eight first escapes gives `8*12=96` labelled
realizations per colour.

Their mixed-singleton histograms are identical:

```text
singleton rows  1  2  3  4  6  7
realizations   16 16  8 24  8 24.
```

The fixed-colour orbit census has 16 orbits per missing colour: eight of
size four and eight of size eight.

A sharp one-singleton representative is

```text
first colour-1 escape:  01|23|45
next colour-0 escape:   02|14|35
singleton word/fine:    101101 / 05|14|23
singleton cells:        05;1, 14;0, 23;1.
```

For colour two the same geometry gives

```text
singleton word/fine:    121121 / 05|14|23
singleton cells:        05;1, 14;2, 23;1.
```

Every singleton coefficient is a monomial in live localized weights.  Its
target is zero because the word is mixed.  Thus its source equation is a
literal Laurent unit, independently of all coefficient signs elsewhere.

## 3. Full minimum completions

For completeness, the checker chooses both missing-colour escapes.  There
are

\[
                         8\cdot12\cdot12=1152             \tag{4}
\]

fifteen-cell minimum completions.  Every one has a mixed singleton; their
singleton counts range from six to 26.  The exact histogram is

```text
6:32, 7:144, 8:112, 9:112, 10:128, 11:160, 12:160,
13:48, 14:104, 16:24, 18:48, 19:48, 20:8, 24:16, 26:8.
```

So simultaneous completion of the last two pure colours cannot cancel the
second-step unit within the support-minimum class.

## 4. Terminal-ear potential

Define

\[
 \mu=\#\{c:\text{the colour-}c\text{ support has no cap-avoiding pure
 matching}\}.                                             \tag{5}
\]

On the seven-cell guard, `mu=3`: even colour one has only cap-containing
pure terms, and those are killed by the mixed equations.  A minimum
colour-one escape gives `mu=2`.  Any next minimum decrease of `mu` emits a
mixed singleton immediately.  Hence along support-minimum escape moves,

```text
mu=3 -> mu=2 -> source unit.
```

This is a strict, well-founded terminal-ear potential for the requested
local class.  The nine-cell guard records the only nonterminal intermediate;
there is no exact recurrent minimum packet after it.

## Scope

The theorem is exhaustive for support-minimum cap-avoiding pure escapes from
the fixed seven-cell diagonal guard, with cap/window/tail/word/fine/operation
labels retained.  A nonminimum repair may add cancellation mates at the same
time as a missing-colour escape; those larger simultaneous packets are not
classified here.

## Reproduction

```text
python3 computations/verify_c6_three_direct_minimal_pure_escape_unit_gate.py --mode structural
python3 -O computations/verify_c6_three_direct_minimal_pure_escape_unit_gate.py --mode full
python3 -I -S computations/verify_c6_three_direct_minimal_pure_escape_unit_gate.py --mode exhaustive
```

All modes return the same frozen ledger digest.
