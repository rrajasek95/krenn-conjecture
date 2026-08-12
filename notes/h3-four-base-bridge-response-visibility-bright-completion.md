# Fixed-port bright rows type every silent four-base bridge

## Result

The eleven-monomial source identity of `c44d784` forces one of nine
pure-zero physical `C4` bridges or two `C6` separators.  Among the nine
bridges, exactly five already contain a selected response-hole edge:

```text
01|25|34: G11 and G22,
02|13|45, 05|13|24: G21,
04|12|35, 04|15|23: G12.
```

Thus these five give six literal nonzero matching occurrences in the
selected zero-target response coefficients.  The remaining four bridges
are response-silent at all four selected holes:

```text
02|14|35, 03|12|45, 03|15|24, 05|14|23.              (1)
```

Fix the minimum endpoint ports

```text
p1@0:1, s1@1:1, p2@3:2, s2@4:2,
```

and adjoin arbitrary selected bright cofactor matchings: one of the three
pure-`11` matchings behind hole `01` and one of the three pure-`22`
matchings behind hole `34`.  For every one of the `4 x 3 x 3=36` choices,
a complete literal response coefficient gives exactly one selected-support
monomial.  Every one of its two alternative residual matchings contains a
nonanchor offdiagonal cell:

```text
36 charts: both alternatives contain a nonanchor offdiagonal q cell.
```

Consequently the fixed-port silent-bridge branch has no new guard.  After
localizing the selected unary and bright matching factors, exactness gives
an ordinary source unit if neither mate occurs; otherwise the pinned
nonanchor active-carrier input occurs.

Checker:
`computations/verify_h3_four_base_bridge_response_visibility_bright_completion.py`.

## Why the five visible bridges really lift

The selected response holes are

```text
G11:01, G12:04, G21:13, G22:34.
```

If a nonzero pure-zero matching contains one of these edges, remove that
edge and replace it by the corresponding selected endpoint pair.  The two
remaining pure-zero cells and both endpoint entries are nonzero, so the
result is a literal nonzero monomial in that response coefficient.  This
is stronger than physical `C4` adjacency: it is an occurrence in the
actual source row with its fine word and endpoint labels fixed.

The overlap `01|25|34` lifts in both diagonal rows.  Each of the other four
visible bridges lifts in the indicated crossed row.  The checker enumerates
all nine bridges and verifies the exact `5+4` split and six occurrences.

## Private-row argument for the four silent bridges

Write `Q0` for one matching in (1), `Q1=01|A_i` for a selected bright
pure-`1` matching, and `Q2=34|B_j` for a selected bright pure-`2` matching.
On the selected support retain

```text
q^00 on the complete old A/B/K/L union and Q0,
q^11 on A_i, q^22 on B_j,
```

together with the four fixed endpoint cells.  For each of the 36 choices,
the checker expands every fixed-port coefficient of `G11,G12,G21,G22` and
chooses a non-target fine word with exactly one supported monomial.

There are exactly two other perfect matchings on its four residual sites.
Their decorations are prescribed by the same fine word.  Every one has an
offdiagonal cell.  If such a cell lies outside

```text
Q0 union Q1 union Q2,
```

the nonanchor theorem pinned by the checker supplies the certified active
carrier interface.  The checker verifies this for both alternate
matchings in all 36 charts.  Retaining the full old pure-zero support is
load-bearing in this audit: it is the genuine extension of the four-base
packet, rather than a three-edge formal bridge packet.

In general, an anchor-contained alternative would still share the two
identically decorated endpoint factors with the selected term and differ
by one residual `C4`, hence would be a genuine typed same-tail response
edge.  No such fallback is needed here: the exact full-old-support census
has route profile `36 x (two nonanchor alternatives)`.

## Consequence and scope

This closes the fixed-port response-typing question for all nine physical
bridges:

1. five are visible in a selected response row immediately;
2. all four silent bridges become unit/offanchor after arbitrary
   selected bright cofactor matchings are imposed.

The result does **not** claim that a typed edge already has nonzero Fitting
minor or deleted-star rank three.  A flat typed edge enters the connected
flat/source-exhaustivity theorem; a nonflat edge is the active carrier.
Nor does the 36-chart calculation classify additional endpoint components
on the four core sites.  It is the exact concentrated fixed-port theorem,
not an arbitrary-star concentration result.

## Verification

```text
python3 computations/verify_h3_four_base_bridge_response_visibility_bright_completion.py
python3 -O computations/verify_h3_four_base_bridge_response_visibility_bright_completion.py
python3 -I -S computations/verify_h3_four_base_bridge_response_visibility_bright_completion.py
```

Frozen ledger SHA-256:

```text
e5991dfb5af90ecd42d0a81f295facb6027404dbf32193f06501a71b0e615d2b
```
