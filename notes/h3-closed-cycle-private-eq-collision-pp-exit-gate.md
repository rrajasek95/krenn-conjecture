# Private-minus-`Eq` kills the closed cycle, but not each possible PP comparison

## Verdict

The private-minus-`Eq` character completely terminalizes the **internal**
24-switch cycle guard.  It does not yet terminalize the exhaustive physical
source.

For each labelled four-corner component, order the vertices as

```text
A0, A1 | B0, B1
```

and put

\[
                    \delta=(1,1,-1,-1),\qquad
                    \Psi=\delta\cdot(B-\operatorname{Eq}).                \tag{1}
\]

The six two-switch/all-pure components give 48 private/`Eq` coordinates.
Their 24 cap diagonals and 24 internal switches have rank 42.  The cokernel
has dimension six, with one copy of (1) per literal component.  Every one of
the 24 switches has value zero.

The strongest hoped-for exit statement is false: an individual absolute
one-hole landing or collision matching repair also has value zero.  Before
the physical shore gauge it is `e_A-e_endpoint`; after the gauge it is the
signless shore-crossing edge `e_A+e_endpoint`, already one of the `K2,2`
columns annihilated by (1).  Such a landing can close its local 24-flag
first-PP residual without changing the global balanced quotient.

The balanced `L01` face is different.  Its projection is

\[
                         (B,\operatorname{Eq})=(\delta,0),                 \tag{2}
\]

so `Psi(L01)=4`.  It raises the six-block rank from 42 to 48.  If its
private and `Eq` packets are tied instead, `(delta,delta)`, its value is zero
and the rank remains 42.

The exact first undecided exit is earlier than the completed `L01` top: it is
the selected six-term vertical `db01` PP comparison.  The committed source
has no map from that PP summand to the private/`Eq` block.  Its deciding
scalar

\[
              m_{db01}=\delta\cdot(B-\operatorname{Eq})
                         \bigl(\Pi_{B/Eq}(db01)\bigr)                      \tag{3}
\]

is therefore genuinely uncomputed.  If (3) is zero, the next family is the
eighteen endpoint/direction terms of `dL01`; if it is nonzero, `db01` is the
first physical exit and rank raiser.

Exact checker:
[`verify_h3_closed_cycle_private_eq_collision_pp_exit_gate.py`](../computations/verify_h3_closed_cycle_private_eq_collision_pp_exit_gate.py).

## 1. Identifying the physical cycle with the private square

The full-site cycle checker uses cyclic object order

```text
state 00, state 10, state 11, state 01.
```

Even states carry the ordered direct chart and odd states the endpoint
chart.  Reorder these as

```text
state 00, state 11 | state 10, state 01.
```

Then its physical site edges are exactly

\[
             (A_0,B_0),\ (A_0,B_1),\ (A_1,B_0),\ (A_1,B_1),               \tag{4}
\]

and its alternating charge becomes `(1,1,-1,-1)`.  Thus the site/root
closed square and the private/`Eq` square are literally the same `K2,2`
block after a fixed relabelling, not merely isomorphic abstract graphs.

There are six blocks:

```text
three pure colours x two switch families A<->B and A<->C.
```

In each block include the four cap columns

\[
                          (B,Eq)=(e_i,e_i)                                  \tag{5}
\]

and the four internal switch faces

\[
                          (B,Eq)=(e_a+e_b,0),
                  \qquad a\in\{A_0,A_1\},\ b\in\{B_0,B_1\}.              \tag{6}
\]

Equations (5)--(6) have rank seven in every eight-dimensional block.  Their
sixfold direct sum has

```text
coordinates  48,
columns      48,
rank         42,
cokernel      6.
```

The six primitive cokernel rows are exactly the six copies of (1).

## 2. Why internal relative switches have zero mismatch

For a shore-crossing edge in (6),

\[
             \Psi(e_a+e_b,0)=\delta_a+\delta_b=1-1=0.                    \tag{7}
\]

The retained mapping-cylinder carrier of a presentation-safe chart bar is
outside the private/`Eq` projection, so it does not alter (7).  Hence all 24
internal site/root comparisons, including their flat cycle transport, are
annihilated.

This is compatible with the pure normalization point.  Normalized target
values live outside (1), while the physical cap dressing is diagonal as in
(5).  Neither changes the six mismatch characters.

## 3. Collision and one-hole exits

The signed first collision residual has the exact ladder

```text
45-term symmetric collision sector
    -> 180 labelled first-PP flags
    -> 30 distinct-direction C2+/C4/P2 packets
    -> J_E01, the 24 same-cell one-hole anti-diagonal.
```

The collision top is in a nonsquarefree augmented-vertex degree, and the PP
flags are in a vertical principal-parts summand.  No committed comparison
sends either summand to private/`Eq`; their current direct-sum projection is
zero.  The distinct packets are old, centered, or outside the selected
private block, so they do not alter (1).

The local one-hole theorem shows that one absolute cofactor split fills
`J_E01`.  Its coefficient type is an oriented direct-to-endpoint switch

\[
                              e_A-e_B.                                    \tag{8}
\]

The shore gauge which turns the root return into the physical switch changes
(8) into

\[
                              e_A+e_B.                                    \tag{9}
\]

Equation (9) is one of (6), so its private-minus-`Eq` value is zero.  The
checker verifies all 24 placements.  Adding them does not raise rank 42.

This resolves a useful ambiguity:

```text
absolute one-hole landing
    -> can kill the local first-PP anti-diagonal;
    -> need not kill the global balanced chart charge.
```

The same statement applies to the squarefree matching repair of a collision:
its two endpoints are exactly one `A/endpoint` switch edge.

## 4. `L01` is the first known nonzero private/`Eq` type

The balanced chart face is not one switch edge.  It is the four-corner
charge itself.  With projection (2),

\[
                            \Psi(L01)=\delta\cdot\delta=4.                 \tag{10}
\]

Adding one such face in each component supplies all six missing private/
`Eq` ranks.  This is the exact positive control.

The negative control is equally important.  A more fully decorated column
with projection

\[
                       (B,Eq)=(\delta,\delta)                              \tag{11}

has value zero.  Thus the word “absolute” is not sufficient: the physical
cell must have an **untied** balanced private/`Eq` readout.  This is precisely
the criterion isolated by the private-minus-`Eq` theorem.

## 5. The first untyped breaker is `db01`

The selected endpoint fibre has a literal six-term vertical face `db01`.
Its known local coordinates are

```text
db01, private graph carrier dz01, normalized all-D endpoint.
```

The graph and all-D columns have rank two; adjoining `db01` raises rank to
three.  The all-D endpoint is not `db01`: their fine colours, module roles,
and vertical PP degrees differ.

None of these facts defines `Pi_BEq(db01)`.  In particular, pure
normalization of the all-D endpoint cannot force (3).  Both outcomes remain
compatible with the committed local rank data:

```text
Pi_BEq(db01) is centered/tied   -> m_db01=0;
Pi_BEq(db01) has balanced B-only part -> m_db01=4.
```

Therefore `db01` is the exact first family that can break the internal
cycle detector.  If its mismatch vanishes, the next proper face is the
eighteen-term `dL01` direction packet with primitive marginal profile

\[
                          (2,2,-1,-1,-1,-1).                              \tag{12}

Its private/`Eq` comparison must then be tested by the same scalar.

## 6. Sharp remaining fork

The current conclusion is:

```text
all internal chart/root switches                         Psi=0
all individual shore-gauged one-hole/collision repairs  Psi=0
absolute balanced L01 private face                       Psi=4
selected db01 physical B/Eq comparison                   UNKNOWN
```

Hence the internal closed-cycle counterguard is terminal under (1), but the
full-source terminal theorem needs exactly one more compatibility result:

> Construct the private/`Eq` readout of the selected `db01` source cell.  If
> its mismatch is nonzero, it is the first exit and filler.  If it is zero,
> prove the same law for the eighteen `dL01` faces and all later collision
> carriers; the six copies of `Psi` then extend to the accepted terminal.

This is shorter than asking whether arbitrary collision exits are active.
Most of them are rigorously invisible to the deciding character; only the
vertical PP comparison can first change it.

## Verification

Run

```text
python3 computations/verify_h3_closed_cycle_private_eq_collision_pp_exit_gate.py
python3 -O computations/verify_h3_closed_cycle_private_eq_collision_pp_exit_gate.py
python3 -I -S computations/verify_h3_closed_cycle_private_eq_collision_pp_exit_gate.py
```

The checker identifies the literal physical-cycle vertex order, constructs
the six 8-coordinate private/`Eq` blocks, verifies all ranks and dual values,
tracks the one-hole shore gauge, and pins the collision, one-hole, `db01`,
and `dL01` boundary audits.
