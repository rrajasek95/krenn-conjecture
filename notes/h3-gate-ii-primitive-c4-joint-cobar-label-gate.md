# The Gate-II primitive-C4 joint carrier fails first at the mixed chart label

## Result

Grant the two strongest missing tail data isolated in the uniform-response
landing audit:

1. a termwise-PP-natural selected `db01` carrier and its endpoint mate; and
2. the same-grade direct cap `U_C4[D,Q01;2345]`.

These data have a canonical **coefficient-level** primitive-C4 completion.
However, its eighteen direction-factor faces cannot be realized as one
source-labelled two-root cobar orbit.  The first failure is literal: every
required mate edge changes the physical operation tag from `DQ` to `PS`,
whereas a site-root cobar edge preserves the structural occurrence tag and
the `D/P/S/Q` operation profile.

Exact checker:
[`verify_h3_gate_ii_primitive_c4_joint_cobar_label_gate.py`](../computations/verify_h3_gate_ii_primitive_c4_joint_cobar_label_gate.py).

## The eighteen faces

Put

\[
 A=Dq_{01}H,\qquad B=p_0s_1H,\qquad C=p_1s_0H,
\]

where `H` is the three-term residual `C4` sum on sites `2345`.  Then

\[
                         L_{01}=2A-B-C.
\]

After the residual-tail derivatives have been granted, the remaining part
of `dL01` consists of six direction derivatives in each chart:

| chart | physical profile `(D,P,S,Q)` | terms | coefficient |
|---|---:|---:|---:|
| `A=D*q01` | `(1,0,0,1)` | `3 tails x 2 direction factors = 6` | `2` |
| `B=p0*s1` | `(0,1,1,0)` | `3 x 2 = 6` | `-1` |
| `C=p1*s0` | `(0,1,1,0)` | `3 x 2 = 6` | `-1` |

The six labelled marginals are exactly

\[
 (dD,dq_{01},dp_0,ds_1,dp_1,ds_0)
   =(6,6,-3,-3,-3,-3),
\]

with primitive profile `(2,2,-1,-1,-1,-1)`.

## The strongest formal primitive-C4 shadow

Duplicate the direct chart according to the two root orders and use the four
vertices

```text
A_[a|b], A_[b|a], B, C.
```

There are two total same-character mate involutions

```text
tau_a = (A_[a|b] B)(A_[b|a] C),
tau_b = (A_[a|b] C)(A_[b|a] B).
```

Their signless incidence rows form a face-complete flat `C4`, of rank three.
Its centered alternating charge is

\[
                     (1,1,-1,-1).
\]

Under the projection which identifies the two ordered direct copies, this
charge becomes

\[
                     (1,1,-1,-1)\longmapsto(2,-1,-1).
\]

The four mate rows project to precisely two row types, `A+B` and `A+C`.
Thus the coefficient algebra has found the right object: its relative Tate
charge is exactly `L01`, and differentiating it gives the required eighteen
faces.

This does **not** yet construct a physical top cell.  In the flat-component
theorem the alternating charge is the surviving centered cokernel class.  A
source-labelled Tate generator would still have to kill it.

## Why it is not a two-root cobar orbit

The pinned literal Hasse/cobar square has four words

```text
0112 -> {1112,0102} -> 1102
```

and realizes the two ordered paths with cubical boundary

```text
A0 + B1 - A1 - B0.
```

At every vertex, root action preserves the marked occurrence tag

```text
(p_site, s_site, residual_sites)
```

and changes only the colour on the literal factor at the root site.  In
particular, it cannot turn a `D*q` factorization into a `p*s` factorization.

Every edge in the formal square above is instead one of

```text
DQ <-> P0S1,
DQ <-> P1S0.
```

All four proposed mate edges therefore violate the literal operation-profile
invariant.  Zero of them is an existing two-root cobar edge.  The virtual
`K8` matching notation makes `A,B,C` look like three charts of one local
perfect-matching packet, but the physical source category remembers that
`A` has profile `(1,0,0,1)` and `B,C` have profile `(0,1,1,0)`.

## Smallest complete-row counterguard

Take the four words of a two-root square and three physical chart tags
`A,B,C`, giving twelve coordinates.  Include:

- every tag-preserving root edge in the square; and
- the complete response row `A+B+C` at every word.

The root-edge rank is nine.  Adding all complete response rows raises it to
ten.  The `L01` charge at one word raises it again:

```text
root edges                              rank 9
+ all complete response rows            rank 10
+ (2A-B-C) at one word                  rank 11
```

The explicit dual is constant across the word square and has chart values

\[
                            (A,B,C)=(2,-1,-1).
\]

It kills every tag-preserving root edge and every complete response row.  Its
value on `2A-B-C` is `6`, so division by six gives a normalized detector.

Adding only the projected mate row `A+B` leaves the candidate independent;
the same is true for only `A+C`.  Adding both row types fills the entire
twelve-dimensional module and makes the candidate dependent:

```text
base + only (A+B): rank 11 -> 12 after candidate
base + only (A+C): rank 11 -> 12 after candidate
base + both:       rank 12 -> 12 after candidate
```

So the smallest missing physical packet consists of **two independent chart
switches**, not another complete matching row or another tag-preserving root
square.

## Why signed boundary completion does not supply them

The exact primitive-C4 identity is

\[
                         LR=BD=-BF.
\]

A cancelling top binomial therefore exports nonzero `L` and `R` boundary
fibres and requires signed mates.  But the top binomial alone has exponent
rank one and no closed holonomy circuit.  More importantly, the pinned exact
boundary-complete packet shows that unique same-character mates can rotate
their retained tail and physical window:

```text
retained tail: 01 -> 23 -> 45
C4 window:     2345, 0145, 0123
common sites:  none
```

Thus primitive boundary completion certifies the coefficient mate relations;
it does not certify that the mates live over one common action-site window,
one endpoint pair, or one physical source object.  It cannot be used to
silently promote `A+B` and `A+C` to the missing chart-switch arrows.

## Shortest positive datum

The shortest remaining construction is a source-provenant chart-switch
bicomplex containing both

\[
 DQ\leftrightarrow P_0S_1,
 \qquad
 DQ\leftrightarrow P_1S_0,
\]

natural for the two site-root PP operators.  Its four mixed commutator faces
and its signed primitive boundary mates must remain on one fixed residual
tail and one fixed physical `C4` window.  With that datum, the formal flat
charge projects to `L01`, the eighteen direction faces close, and the
already committed descent can start:

```text
word 0102 -> private carrier -> C*d=12*d
          -> dq23 / occurrence-labelled Q-ores -> -35/72.
```

No accepted terminal is reached here.  The obstruction occurs before the
word-`0102` private face, so no new `q`, `W`, ridge, target, residue, or ores
claim is made.

## Reproduction

```bash
python3 computations/verify_h3_gate_ii_primitive_c4_joint_cobar_label_gate.py
python3 -O computations/verify_h3_gate_ii_primitive_c4_joint_cobar_label_gate.py
python3 -I -S computations/verify_h3_gate_ii_primitive_c4_joint_cobar_label_gate.py
```

The frozen ledger digest is

```text
595771f49fd81aa9ce0dfaa29d03a848905f10f976b96fd3cf6107b6ecc642e2
```

and the checker file digest is

```text
d77f4fd853673c434d4a0bb4027bf9ba046f1bb7ea4d752028a609e832255f44
```
