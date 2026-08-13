# The 140 H2 direction tags have one structural coinvariant

## Exact quotient

The literal second-Hasse incidence from `8c3dafb` has 210 nonzero response
direction pairs, partitioned into seventy three-element fibres by their
common complementary lower tail.  The centered direction-tag module is

\[
 K=\bigoplus_{C\in\mathcal C}
 \ker\bigl(\mathbb Q^{\{e_1,e_2,e_3\}_C}\to\mathbb Q\bigr),
 \qquad \dim K=70(3-1)=140.                         \tag{1}
\]

Let

\[
 G=S_6\times\langle\theta\rangle,
 \qquad \theta(p_i)=s_i,\quad\theta(s_i)=p_i,\quad
 \theta(q_{ij})=q_{ij},\quad\theta(D)=D.             \tag{2}
\]

The checker constructs the complete integral action of the five adjacent
site transpositions and `theta` on the basis
`(e_1-e_0,e_2-e_0)` in every fibre.  The resulting 840 action-relation rows
have rank 139 modulo each of `1000003` and `1000033`.  An integral invariant
functional exhibited below kills every relation, so the rational rank is
exactly 139, not merely bounded by the modular calculation.  Therefore

\[
                       \dim_{\mathbb Q}K_G=1.          \tag{3}
\]

Checker:
[verify_h3_h2_direction_tag_maschke_c4_coinvariant_gate.py](../computations/verify_h3_h2_direction_tag_maschke_c4_coinvariant_gate.py).

## Orbit and sector decomposition

There are four pair orbits:

| size | pair types |
|---:|---|
| 15 | `DQ` |
| 30 | `PS-distinct` |
| 45 | `QQ-disjoint` |
| 120 | `PQ-disjoint`, `SQ-disjoint` |

There are three component orbits:

| size | component types |
|---:|---|
| 15 | `C2+` |
| 15 | `C4` |
| 40 | `P2`, reversed `P2` |

Thus the trivial multiplicity in
`Q[pairs]-Q[components]` is already forced to be `4-3=1`.  The direct
action matrices refine this orbit count sectorwise:

\[
\begin{array}{c|c|c|c}
\text{sector}&\dim&\operatorname{rank}\langle g-1\rangle&\dim\text{ coinvariants}\\
\hline
C2^+&30&30&0\\
C4&30&29&1\\
P2\oplus P2^T&80&80&0.
\end{array}                                             \tag{4}
\]

In each `C4` fibre there is one `DQ` direction and two endpoint-pair
directions.  The surviving invariant vector and dual can be chosen as

\[
 v_{C4}=\sum_{C4\ {m fibres}}
       \bigl(2e_{DQ}-e_{PS,1}-e_{PS,2}\bigr),
 \qquad
 \lambda_{C4}=\sum_{C4\ {m fibres}}e_{DQ}^{*}.       \tag{5}
\]

The checker verifies `lambda_C4(gx-x)=0` for every generator and
`lambda_C4(v_C4)=30`.  The other natural line
`e_PS,1-e_PS,2` is `theta`-odd and is contracted over characteristic zero by
`(1-theta)/2`.

This identifies the irreducible content relevant to the quotient: exactly
one copy of the trivial representation survives.  All other irreducible
summands are nontrivial action modules.

## What one equivariant PP schema would prove

If the physical Cartan/Hasse/PP comparison is defined **termwise** on every
literal direction tag and is natural under (2), the characteristic-zero
action-groupoid bar contracts every nontrivial summand of `K`.  Hence it
simultaneously removes the complete `C2+` sector, the complete
`P2/P2^T` tag sector, the `theta`-odd `C4` line, and every nontrivial site
representation.  It does not remove (5), because (5) is invariant.

Root-colour permutations transport the corresponding fine-grade copies but
do not change this uncoloured pair/component orbit difference.  Likewise,
the formal coefficient-level Hasse restriction is not itself the required
termwise physical comparison.  These are typing guards, not extra
coinvariant directions.

The known `P2` word-`0102` endpoint-even private carrier is separate from
(5).  Equation (4) says that no `P2` class remains *inside the original
140-dimensional tag module*.  The `0102` carrier appears downstream, after
restriction and word/fine-grade promotion; its detectors remain `-13/6`
before reinsertion and `35/72` on the labelled `dq23` preimage.  Thus the
shortest physical schema has two differently typed invariant faces:

1. the `C4` direct-`DQ` versus endpoint-pair average (5);
2. after restriction, the already known `P2` word-`0102` private landing.

This prevents the false conclusion that the one-dimensional quotient has
somehow constructed or eliminated the downstream `P2` carrier.

## Promotion of a failure dual

The augmented extension theorem `4373ae6` applies after a local face is
placed in the literal same word/fine/direction and repeated physical grade.
It extends any nonzero local dual through the known
`q/ainc/target/W/ores/ridge` packet.  Exact finite-dimensional duality then
gives only two branches:

\[
 \text{protected-zero physical filler}
 \quad\text{or}\quad
 \text{accepted augmented terminal};                 \tag{6}
\]

there is no third branch.  Consequently a failed physical filler for (5),
or for the downstream `0102` carrier, promotes to a terminal once the
literal same-grade placement exists.  `4373ae6` does not manufacture that
placement, so (6) is intentionally conditional.

## Shortest remaining theorem

Construct one termwise equivariant PP comparison schema.  Maschke then
contracts every nontrivial direction-tag representation automatically.
Only the invariant `C4` line (5) and the downstream `P2` word-`0102` carrier
require physical landing; each lands in the existing filler-or-terminal
fork.  This note proves the exact quotient and reduction, not either missing
landing.

The result is canonical h=3 and characteristic zero.  The checker was run
normally, optimized, and isolated/no-site, with a frozen ledger digest.
