# The chart-direction debt is one uniform Spencer packet

## The eighteen h=3 faces are rank one over the tail

Keep the four selected sites `X={0,1,P,S}` and write

\[
 A=01\,PS,\qquad B=0P\,1S,\qquad C=1P\,0S,
 \qquad L_h=(2A-B-C)H_Y .                            \tag{1}
\]

Here `H_Y` is the hafnian on the other `2h-2` sites.  Differentiate one
of the two `X`-edges.  In the order

```text
dD, dq01, dp0, ds1, dp1, ds0
```

the six coefficients are

\[
                  \kappa=(2,2,-1,-1,-1,-1).          \tag{2}
\]

Consequently the complete endpoint/direction face is

\[
                  S_h=\kappa\otimes H_Y .             \tag{3}
\]

The coefficient matrix, with six direction rows and the `(2h-3)!!` tail
occurrences as columns, has rank one.  It is fixed by both `0<->1` and
`P<->S`.  Thus it is one endpoint-even Spencer packet, not six independent
families.  For `h=3`, `H_Y` has three matchings, so (3) is exactly the
eighteen direction terms and the marginal

\[
                  3(2,2,-1,-1,-1,-1)
\]

computed in `2acaf90`.

Checker:
[`verify_uniform_response_h2_chart_direction_spencer_packet_gate.py`](../computations/verify_uniform_response_h2_chart_direction_spencer_packet_gate.py).

There is no new coefficient species as `h` grows.  The same six-vector is
only tensored with a larger lower hafnian.  It is nevertheless not killed
by the complete direction row: the constant vector and `kappa` have rank
two.  The useful identity

\[
 \kappa=3(1,1,0,0,0,0)-(1,1,1,1,1,1)               \tag{4}
\]

shows why a physical capped `A=Dq01` comparison together with the complete
chart row would be sufficient.  Equation (4) is a coefficient identity;
the capped source comparison and its complement remain the construction
isolated in `2acaf90`.

## Its next faces have exactly the known lower topologies

There are only two ways to differentiate (3) once more.

First, differentiate the other selected edge in the same cap.  The varied
pair is `D,Q` for `A`, or `P,S` for `B,C`.  What remains is the complete
hafnian `H_Y`.  At `h=3` these are three complete `C4` packets, with weights
`2,-1,-1`.

Second, differentiate a tail edge.  The first selected label determines
the lower coefficient:

| first selected label | varied pair | complete lower family |
|---|---|---|
| `D` | `D,Q` | pure hafnian / `C4` |
| `q01` | `Q,Q` | response `C2+` |
| `p0,p1` | `P,Q` | one-endpoint `P2` |
| `s0,s1` | `S,Q` | reversed `P2` |

This is exactly the pair-topology list proved by the committed second-Hasse
census.  There is no fourth compatible topology.

The fixed chart does **not**, however, contain the complete mixed lower
coefficient.  Fixing a selected direction and a tail edge leaves
`2h-2` vertices, so the complete response coefficient has `(2h-3)!!`
occurrences.  The zero-cross chart forces the complementary selected edge
and retains only `(2h-5)!!`.  Hence it contains the fraction

\[
                         {1\over 2h-3}.               \tag{5}
\]

At `h=3`, the 36 direction--tail faces are singleton summands of
three-term lower packets.  Their other 72 terms are cross-chart response
occurrences.  The exact split is

```text
fixed chart:       C4 6 + C2+ 6 + P2 12+12 = 36
cross companions:                                  72
complete packets:                                 108
```

So the optimistic induction in `03b5653` needs one correction: the
`C2+/C4/P2` theorems classify the next Hasse face only after the cross-chart
companions have been installed.  They do not directly make the first-PP
packet (3) a boundary.

## Uniform conclusion and physical frontier

The monoidal recursion has no growing list of algebraic obstructions.  Its
single proper-face family is

```text
endpoint-even Spencer packet  kappa tensor H_(h-1).
```

Its second faces are precisely spectator-extended `C2+`, `C4`, and `P2`
packets.  The remaining theorem is therefore one chart-complete physical
Spencer/cobar construction, not one theorem per direction occurrence:

> Construct a source-valid family with boundary `S_h`, including the
> cross-chart terms which complete every lower packet, while preserving the
> actual word, fine and repeated grade and the physical `q`, anchor, `W`,
> and labelled-ridge rows.

Before that family is placed, the coefficient packet is not an augmented
terminal and the named lower cells cannot be invoked on its singleton
fixed-chart summands.  This note proves the complete-matching and
first/second principal-parts classification only.

Run normally, optimized, and isolated/no-site.  The frozen ledger digest is
`b9811e3842bfeaf3e0760127a1e2f92565de01337cb6f6e673ccd83656143906`.
