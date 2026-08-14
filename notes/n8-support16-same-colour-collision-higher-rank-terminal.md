# Support 16: the sole same-colour two-face guard is not normalized

## Verdict

The only residual stabilizer orbit with two prototype cap faces is excluded
by the pure target rows.  Its exceptional same-colour chart requires
`w=(0,B,C)` with `B C != 0`; every one of its 232 full mutual-coordinate
anchor completions has **no** pure-colour-0 perfect-matching occurrence.
Consequently the colour-0 target coefficient is zero, contradicting the
normalized pure row.

This closes the single two-face collision left by the two-cap orbit
classifier.  The remaining 258 residual orbits all have at most one
prototype face, so they require a different response polynomial or a global
row argument; repeating the crossed `2 x 2` permanent construction cannot
close them.

The exact audit is

```text
python3 computations/verify_n8_support16_same_colour_collision_higher_rank_terminal.py
python3 -O computations/verify_n8_support16_same_colour_collision_higher_rank_terminal.py
python3 -I -S computations/verify_n8_support16_same_colour_collision_higher_rank_terminal.py
```

## Literal source-labelled representative

The unique orbit is graph index 10 in the 22 two-RRX representatives, has
orbit size one, and is the never-private directed incidence `0 -> 01` on

```text
01 03 05 06 07 12 13 14 15 24 25 27 34 37 46 56.
```

Its two prototype faces are caps `06` and `07`.  The canonical global
collision completion is

```text
01 = nonanchor
03=2, 05=1, 06=0, 07=0,
12=0, 13=0, 14=1, 15=2,
24=1, 25=0, 27=2,
34=0, 37=1, 46=2, 56=1.
```

The first new faces beyond the prototype have exact expanded splits

```text
cap03: 2 target terms + 8 residue terms
cap05: 2 target terms + 8 residue terms.
```

Thus these are the smallest available different response polynomials in this
orbit.

## Why the repeated prototype construction fails

Write the shared direct colour as `a=0` and the complementary colours as
`b,c`.  The exceptional chart is

```text
w=(0,B,C),  B C != 0.
```

The equation `w^T K=0` gives

```text
row_c = -(B/C) row_b.
```

For either crossed prototype residue,

```text
P_bc = K_bb K_cc + K_bc K_cb
     = -2 (B/C) K_bb K_bc.
```

Activity requires `K_bb,K_cc != 0`; the row relation and `B,C != 0` then
force `K_bc != 0`.  Hence `P_bc != 0`.  The checker verifies the exact
Laurent identity and its denominator-cleared form

```text
C P_bc = -2 B K_bb K_bc.
```

This is an actual negative stratum for the two-term-permanent method, not a
failure to choose sufficiently high rank.

## The eight-term faces do not rescue the chart

On the displayed completion, cap `03` has residue components

```text
000101 : K01 K10 + K00 K11
011101 : K01 K10 + K00 K11
020102 : 2 K00 K10
000000 : 2 K00^2.
```

Its target words are disjoint from all four residue words.  The last
component therefore prevents an active zero because activity includes
`K00 != 0`.

Cap `05` has residue components

```text
212110 : K01 K22 + K02 K21
202220 : K00 K22 + K02 K20
102110 : K01 K20 + K00 K21
200000 : 2 K00 K02.
```

Again the target words are disjoint.  If the residue vanished, the last two
displayed generators would imply the exact saturation identity

```text
2 K00^2 K22
  = 2 K00 (K00 K22 + K02 K20) - K20 (2 K00 K02) = 0,
```

contradicting active `K00 K22 != 0`.  Thus neither larger face supplies a
rank landing.  Also, `K03,K05,K06,K07` are independently typed cap
covectors, so imposing one common `K` would not be a source-valid repair.

## The normalization exit

The checker enumerates all 232 full anchor completions with

- `01` the sole nonanchor;
- caps `06` and `07` fixed to their common direct colour 0; and
- every vertex seeing all three coordinate colours.

For each completion it enumerates the perfect matchings of the support graph.
Because `w_0=0`, a pure-colour-0 occurrence cannot use edge `01`; it must be
an anchor-only colour-0 perfect matching.  None exists in any completion.
The exact histogram of `(pure0,pure1,pure2)` support counts is

```text
(0,0,0): 12
(0,0,1): 40
(0,1,0): 40
(0,1,1): 122
(0,1,2): 8
(0,2,1): 8
(0,2,2): 2.
```

The first coordinate is uniformly zero, so coefficient choices or
cancellations cannot repair the missing pure row.  This is a source-valid
normalization contradiction for the collision-completion branch.  It is not
a standalone GHZ counterexample and makes no claim about the 258 one-face or
zero-face residual orbits.
