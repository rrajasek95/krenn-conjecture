# The active-fan recurrence moves the double-collision debt but does not kill its endpoint-odd jet

## Outcome

The six `P4+K2` and three `4K2` faces left by the localized `db01`
attempt do **not** enter an unconditional outside-support, four-good, or
closed coloop exit.

There are two distinct statements:

1. The committed complete unary/response theorem is genuinely exhaustive
   on its ordinary `K6` coefficient-support packet: after all of its word
   rows are imposed, the old closed support shadows force strict Hall growth
   and hence active-fan entry.
2. The nine current faces are not ordinary coefficient occurrences.  They
   are endpoint-oriented first-PP faces of the repeated-site top
   `p0*s1*q01*H2345`, of type `P4+2K2`.  The support theorem explicitly
   stops before the pointed occurrence comparison, and the termwise
   complete-row pivot preserves endpoint orientation.  No committed theorem
   prolongs that recurrence to this jet/operation block.

A literal local tangent makes the gap concrete.  It satisfies the normalized
pure-coloop target row, the complete two-orientation response row, and their
first differentials, while its selected `db01` value is one.  Its tail holes
form the closed matching/rectangle Hall concept and its pure support returns
the literal-coloop branch.  A finite full-labelled rank model then leaves a
nine-dimensional endpoint-odd survivor even after every face is given its
own recurrence graph and complete source/exit pair.

Checker:
[`verify_h3_double_collision_active_fan_hall_prolongation_gate.py`](../computations/verify_h3_double_collision_active_fan_hall_prolongation_gate.py).

## 1. A trapped complete-row tangent

Use the residual pure-`q` point

```text
q01=q23=q45=1,
every other residual q=0.
```

Then

\[
 H_{2345}=q_{23}q_{45}+q_{24}q_{35}+q_{25}q_{34}=1,
 \qquad q_{01}H_{2345}=1.                            \tag{1}
\]

Choose the two opposite endpoint orientations with

```text
p0*s1= 1,
p1*s0=-1.
```

Thus the complete local response row is

\[
                         b_{01}+b_{10}=1-1=0.         \tag{2}
\]

Now take the tangent

```text
dq01=-1,  dq23=1,
all other dq=0.
```

It has `dH2345=1`.  Therefore

\[
 d(q_{01}H_{2345})=(-1)\cdot1+1\cdot1=0             \tag{3}
\]

and

\[
 db_{01}=1,qquad db_{10}=-1,qquad
 d(b_{01}+b_{10})=0.                                 \tag{4}
\]

The two inserted double-collision relations also close individually:

\[
 q_{01}db_{01}+b_{01}dq_{01}=1-1=0,
 \qquad
 q_{01}db_{10}+b_{10}dq_{01}=-1+1=0.                \tag{5}
\]

So neither the complete response row nor the normalized target first-PP row
forces the selected orientation to vanish.  They see only the endpoint-even
sum.

This is a local fixed-window coefficient/tangent point, not a claimed full
GHZ tensor.  Its role is exact: it refutes an implication from the named
local complete rows and scalar localization alone.

## 2. Hall and active-fan image of the tangent

The nonzero pure matching support is the singleton

\[
                         01\mid23\mid45.              \tag{6}
\]

For the two tail holes put

\[
 A=\{23,45\}.
\]

Its transversal is the rectangle

\[
 T(A)=\{24,25,34,35\},
 \qquad T(T(A))=A.                                   \tag{7}

Hence this is the exact closed matching/rectangle Hall concept.  There is
no outside tail hole in the tangent.  Moreover every edge of the singleton
support (6) is a literal coloop.  If the coefficient shadow is fed into the
active-fan alternative, it reaches

```text
four-good or literal coloop  ->  literal coloop.
```

Restarting the special mate recurrence at that coloop is not a proved
decrease: the pinned recurrence theorem already shows that arbitrary
coloop recurrence is one-shot until the fan-grade pointed comparison is
constructed.

The later closed-shore complete-row census is not contradicted.  It adds
all three mixed unary words and four ordinary response blocks, tests 4,736
completed seeds, and forces strict Hall growth in that coefficient-support
problem.  Its stated scope deliberately does not identify the resulting
cross-word occurrence with the pointed covector.  In particular, it does
not supply a boundary in the new `P4+2K2` PP operation block.

## 3. Why termwise transport does not repair the jet

The complete-row pivot transports a literal occurrence with the same

```text
matching skeleton,
P/S partners and endpoint orientation,
remote q tail,
word and response head.
```

That is exactly the right source provenance for a relative graph.  It is
also why the endpoint-odd class persists: the transport does not mix or
absolutely normalize the `p0*s1` and `p1*s0` orientations.

For each orientation, the localized product has nine live faces:

```text
6 tail faces:  P4+K2, carrying q01*db,
3 q01 faces:   4K2, carrying ps*H2345*dq01.
```

The checker forms a 36-coordinate packet

```text
(source B, source C, exit B, exit C),
```

with nine coordinates in each block.  For every fine/removed-edge label it
grants all four favorable rows:

```text
exit_B-source_B,
exit_C-source_C,
source_B+source_C,
exit_B+exit_C.
```

The last two are stronger than the actual aggregate complete rows: they
give an absolute complete pair separately in every fine label.  The four
rows have rank three per face, hence total rank `27`.  Adjoining the selected
nine-face `B` packet raises the rank to `28`.

The exact dual is

```text
+1 on B at source and exit,
-1 on C at source and exit.
```

It kills all granted rows and reads `9` on the selected `B` packet.  There
is one such odd line for every face, so the full survivor dimension is nine.
The recurrence can transport these lines to retained coloop carriers, but
cannot make them absolute.

## First missing typed row

The next positive datum is not another ordinary support lemma.  It is one
of the following equivalent physical upgrades:

* an endpoint-orientation-asymmetric `P4+2K2` first-jet Hall prolongation
  whose boundary contains the named `P4+K2` and `4K2` faces; or
* an absolute coloop-exit row in that same word, fine, removed-edge,
  repeated-site, and operation block.

Either row would break the endpoint-odd detector.  Complete coefficient
rows, orientation-preserving recurrence graphs, and the ordinary
four-good-or-coloop alternative do not.

## Verification

Run the three theorem views under all interpreter modes:

```text
python3 computations/verify_h3_double_collision_active_fan_hall_prolongation_gate.py --mode tangent
python3 computations/verify_h3_double_collision_active_fan_hall_prolongation_gate.py --mode recurrence
python3 computations/verify_h3_double_collision_active_fan_hall_prolongation_gate.py --mode survivor
python3 -O computations/verify_h3_double_collision_active_fan_hall_prolongation_gate.py --mode tangent
python3 -O computations/verify_h3_double_collision_active_fan_hall_prolongation_gate.py --mode recurrence
python3 -O computations/verify_h3_double_collision_active_fan_hall_prolongation_gate.py --mode survivor
python3 -I -S computations/verify_h3_double_collision_active_fan_hall_prolongation_gate.py --mode tangent
python3 -I -S computations/verify_h3_double_collision_active_fan_hall_prolongation_gate.py --mode recurrence
python3 -I -S computations/verify_h3_double_collision_active_fan_hall_prolongation_gate.py --mode survivor
```

Frozen ledger SHA-256:

```text
cd768a1041dec8bbe13d58e53cc56269bdba0f32ac3a8b2e85fd2f26128afc32
```
