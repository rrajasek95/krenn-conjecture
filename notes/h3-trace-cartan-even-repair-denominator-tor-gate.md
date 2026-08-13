# Denominator Tor sees exactly `B1+B4`, but the clean aggregate forbids it

## Result

The reduced-companion family contains an exact conditional realization of
the two tails needed by `tau_plus`:

```text
face 3, multiplier 34, matching 14|25  -> B4,
face 5, multiplier 45, matching 13|24  -> B1.
```

Both graphs have site profile `(1,1,1,2,1)`, so their repeated target site
is exactly the canonical site 4 created by the 13-of-15 collapse.  The
selected cycle matching on each face instead lands on `B0`.  Therefore,
conditional on selected denominator transgressions, ordinary matching-
Bianchi differences transport them to reduced companions with boundaries
`-B4` and `-B1`.  Negating half their sum gives the desired tail

\[
                         {B_1+B_4\over2}.              \tag{1}
\]

This is the strongest positive match so far.  It does not close the repair:
the required selected projection has aggregate one, which is impossible on
the exact clean normalized `C5` slice, and the reduced companion has the
wrong protected target/anchor/residue signature.

Checker:
[`verify_h3_trace_cartan_even_repair_denominator_tor_gate.py`](../computations/verify_h3_trace_cartan_even_repair_denominator_tor_gate.py).

## Literal six-route intersection

There are thirty adjacent-face denominator tails.  Exactly six lie in the
canonical faces-`(3,5)` complete target component.  In checker order their
targets are

```text
B0, B4, B5, B0, B1, B2.
```

For face 3 the cycle-selected matching is `12|45`; multiplying by `34`
gives `B0`.  The desired off-cycle matching `14|25` gives `B4`.  For face 5
the selected matching is `12|34`; multiplying by `45` gives `B0`, while the
off-cycle matching `13|24` gives `B1`.

Let the endpoint route be

\[
                 R_{v,N}=(-\Omega_v,+Q_{v,N};\operatorname{ores}=1)
\]

and suppose the selected reduced companion exists:

\[
                 A_{v,N_0}=(-Q_{v,N_0};\operatorname{ores}=-1).
\]

The matching-Bianchi difference has zero protected readouts, so

\[
 A_{v,N}=A_{v,N_0}-(R_{v,N}-R_{v,N_0})
         =(-Q_{v,N};\operatorname{ores}=-1).           \tag{2}
\]

Thus selected face-3 and face-5 transgressions would conditionally construct
the two exact off-cycle tails in (1).  No new matching-level transgression
type is needed after the selected cells.

## The clean reset-word coordinate forbids the selected projection

In face coordinates `(1,2,3,4,5)`, the direct selected projection needed by
the half-sum is

\[
                         y={e_3+e_5\over2}.             \tag{3}
\]

It has aggregate one.  Under the target involution `(2 5)`, its transformed
chart projection is `(e3+e2)/2`; averaging the two charts gives

\[
                  y_+={e_3\over2}+{e_2+e_5\over4},     \tag{4}
\]

which still has aggregate one.

Every literal denominator kernel satisfies the source-coordinate identity

\[
                          \sum_v h_vy_v=0.             \tag{5}

For (3), this asks `(h3+h5)/2=0`; for (4), it asks
`h3/2+(h2+h5)/4=0`.  On the clean normalized `C5` slice all `h_v=1`, so
both left sides equal one.  Hence neither the direct nor the rho-evenized
selected projection can be a denominator kernel there.  This is a literal
reset-word obstruction, not a rank heuristic.

Off the clean slice, equations (5) are necessary but not sufficient: the
full selected-column membership in the unselected denominator image is
still required.

## The protected readouts also differ

Use rows `(tail augmentation,target,ainc,ordinary residue)`.  Negating the
even reduced companion corrects its tail but has signature

```text
-A_even:       (1,0, 0,1),
required r0:   (1,1,-1,0),
difference:    (0,1,-1,-1).
```

Thus even where a denominator kernel exists, the same cell does not by
itself provide the pure-column `tau_plus` image.  A same-grade target/anchor/
residue cone correction remains necessary.  This is why the odd
labelled-ordinary-residue transgression and the even Rees repair cannot yet
be identified as one constructed cell.

## Frontier

The denominator approach has found the exact `B1/B4` tail geometry, but on
the clean `C5` branch it is forced into the separator side.  Away from that
slice it gives a conditional construction only if:

1. the weighted selected denominator membership holds;
2. source covariance supplies the transformed chart for rho-evenization;
3. a target/anchor/residue cone correction kills `(0,1,-1,-1)` in the same
   word, fine, repeated-site, and Rees grade.

The `beta=0` selected `D0` unary/complement branch is independent of all
three conditions.

## Verification

Run:

```text
python3 computations/verify_h3_trace_cartan_even_repair_denominator_tor_gate.py
python3 -O computations/verify_h3_trace_cartan_even_repair_denominator_tor_gate.py
python3 -I -S computations/verify_h3_trace_cartan_even_repair_denominator_tor_gate.py
```

Frozen ledger SHA-256:

```text
a980f6b0ee0054b418a97b3b3176ccc4977e0a3eee4c8ebec6ee0000b82e432c
```
