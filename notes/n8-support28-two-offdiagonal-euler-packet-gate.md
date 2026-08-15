# Two-cell off-axis Euler packets still leave a permanent-triangle unit

## Result

The first off-axis packet capable of entering an even-parity diagonal row
consists of two ordered off-diagonal cells

\[
 z_1=A_{uv}[a,b],\qquad z_2=A_{rs}[a,b]
       \text{ or }A_{rs}[b,a],                              \tag{1}
\]

where the physical edges are disjoint and `a != b`.  The two cells have the
same unordered colour pair, so their mod-two colour-incidence defects cancel.

On each of the two unique affine support-28 target charts, every such packet
still leaves a literal permanent-triangle Laurent unit unchanged.  Therefore
it cannot repair the diagonal coefficient fibre.  An exact source containing
(1) must either drop one of the 48 affine diagonal units or contain a larger
off-axis packet.

The checker is
`computations/verify_n8_support28_two_offdiagonal_euler_packet_gate.py`.

## Exhaustive packet and orbit census

There are 210 unordered pairs of disjoint physical edges, three unordered
colour pairs, and four choices of endpoint orientation.  Thus each chart has

\[
                         210\cdot3\cdot4=2520              \tag{2}
\]

literal source-labelled packets.

The checker computes the actual automorphism group of the fixed affine
support inside the marked target stabilizer; it does not quotient by an
unmarked cube symmetry.  The exact orbit census is:

| target chart | support stabilizer | packet orbits | orbit sizes |
|---|---:|---:|---|
| pair target `12` | 4 | 652 | 44 of size 2, 608 of size 4 |
| full target `012` | 12 | 230 | 4 of size 3, 34 of size 6, 192 of size 12 |

The executable ledger freezes a SHA-256 registry of every canonical orbit
representative and keeps the physical edge and ordered endpoint-colour labels
in every representative.

## Literal two-cell row test

All permanent-triangle rows have even colour multiplicities.  A monomial
using only one of the two cells in (1) has nonzero parity defect and cannot
occur.  A new monomial can therefore occur only if

1. its perfect matching contains both marked physical edges;
2. the row word has the two prescribed ordered endpoint-colour pairs; and
3. the remaining four sites admit a supported diagonal matching.

The checker tests these conditions termwise against all three rows of all 96
permanent triangles, for all 2,520 packets in each chart.  Packets which meet
at least one triangle row number 680 in the `12` chart and 666 in the `012`
chart.  The other 1,840 and 1,854 packets, respectively, meet none.

Even the worst packet changes only 22 of the 96 triangle certificates.  Thus
every packet leaves at least 74 complete certificates unchanged.  The worst
literal packets are:

```text
pair target 12:
  01[01] + 56[01]
  06[01] + 15[10]

full target 012:
  05[02] + 17[02]
  07[02] + 15[02]
  45[12] + 67[12]
  47[12] + 56[21]
```

For every labelled packet the checker selects one untouched certificate,
computes the full augmented hafnian on its three words, and verifies exact
equality with the original two-term rows.  It then replays

\[
 cvwF_1+buwF_2-auvF_3=2bcduvw.                             \tag{3}
\]

The right side is twice a monomial in the localized diagonal support cells,
so the mixed source ideal remains the unit ideal in characteristic zero.

## Consequence and next atom

This closes the weakest Euler-even two-cell bridge without asking for a cap
selection or a cleanliness calculation.  The six endpoint-polarized
coordinates at pair `67` remain genuine physical coordinates, but no packet
consisting of one of them and one disjoint same-colour-pair mate can rescue
the affine diagonal orbit.

The next parity-minimal atom is a three-cell colour triangle: three disjoint
physical edges decorated by the three unordered colour pairs `01`, `12`, and
`20`, with arbitrary endpoint orientations.  Its colour-incidence graph is
Eulerian.  Larger possibilities are simultaneous even packets (four or more
cells).  Those are not classified here.

## Reproduction

```text
python3 computations/verify_n8_support28_two_offdiagonal_euler_packet_gate.py --mode structural
python3 -O computations/verify_n8_support28_two_offdiagonal_euler_packet_gate.py --mode full
python3 -I -S computations/verify_n8_support28_two_offdiagonal_euler_packet_gate.py --mode exhaustive
```

All modes return the same frozen ledger digest.
