# The switch-Weyl product constructs the top decoration but exports a relative-C4 face

## Sharp theorem

Let

\[
 T=t_B+t_C=(B-A)+(C-A)=-L_{01}
\]

be the retained endpoint-even carrier in the presentation-safe chart-switch
DGA, and let `H_W` be the all-pair signed-Weyl telescope.  Then `T*H_W` is a
legal cell in the extended source DGA.  Its top Weyl boundary is target-safe
and has the required centered matching factor.  Thus the construction
genuinely removes the earlier matching-constant/circular-projector objection.

It does not close Gate II.  The full total differential is

\[
 D(T H_W)=(d_{PP}T)H_W+T(W-1).                    \tag{1}
\]

The first term in (1) is mandatory.  Its exact support is

```text
18 residual-edge faces + 18 direction-factor faces.
```

The residual-edge half has the known `C2+/P2` formal reduction.  The other
eighteen faces lie in the `C4` objects

```text
Hasse[2](D,Q01), Hasse[2](P0,S1), Hasse[2](P1,S0),
```

six in each.  Signed Weyl/Cartan action recolours literal factors but
preserves the Hasse direction-pair and repeated-edge tags.  Therefore these
faces have zero projection to the existing labelled `P2` square, which lies
in the `PQ/SQ` repeated-`P3+K2` idempotent.

The first surviving typed face is exactly one tail-covariant, same-grade,
protected relative-`C4` restriction/insertion primitive.

Exact checker:
[`verify_h3_gate_ii_switch_weyl_product_rule_idempotent_gate.py`](../computations/verify_h3_gate_ii_switch_weyl_product_rule_idempotent_gate.py).

## Why the product is presentation-safe

The relative graph retains `T`; it does not declare `T=0`.  In the canonical
three-chart model the graph has eight degree-zero coordinates, five monic
boundary columns, and `H0` dimension three—the original `A,B,C` fibre.
Multiplying a retained degree-zero coordinate by the physical Cartan
homotopy adds no equation to that fibre.

Write `K=W-1`.  The PP/Cartan tensor-product signs give

\[
\begin{aligned}
 D(T H_W)&=(dT)H_W+TK,\\
 D((dT)H_W)&=-(dT)K,\\
 D(TK)&=(dT)K.
\end{aligned}
\]

Hence `D^2=0`.  Keeping only `T(W-1)` would fail this totalization by the
uncancelled `(dT)(W-1)` face.

The positive content is important.  The bare telescope has matching factor
`1_105` and is killed by every centered occurrence detector.  Here `T` is
the source-provenant switch coordinate satisfying `T=-L01` modulo the monic
graph boundary.  Thus `T(W-1)` has the desired centered matching factor and
the target-safe `chi_w` decoration without inserting an illicit projector.

## Exact product-rule inventory

For

\[
 A=Dq_{01}H,\qquad B=p_0s_1H,\qquad C=p_1s_0H,
\]

we have `dT=-dL01`.  The chartwise census is:

| source chart | coefficient in `dT` | tail faces | direction faces |
|---|---:|---:|---:|
| `DQ` | `-2` | 6, type `C2+` | 6, type `C4` |
| `PS01` | `+1` | 6, type `P2` | 6, type `C4` |
| `PS10` | `+1` | 6, type `P2` | 6, type `C4` |

The six direction marginals are

\[
 (-6,-6,3,3,3,3)=3(-2,-2,1,1,1,1),                \tag{2}
\]

in the order

```text
dD, dq01, dp0, ds1, dp1, ds0.
```

The first eighteen faces can be routed formally through the committed
`C2+ -> P2` reduction.  This does not claim their physical augmented landing:
the selected `t_zprivate` line in the P2 relative graph remains open.

The second eighteen are not `P2` faces at all.  They retain the three
original `DQ/PS` direction-pair labels and the residual three-matching `C4`
tail.

## The first central-idempotent failure

In the relevant labelled output category, take the central blocks

```text
C4:DQ, C4:PS01, C4:PS10, P2:PQ, P2:SQ.
```

Then

\[
 e_{C4}=(1,1,1,0,0),\qquad e_{P2}=(0,0,0,1,1),
 \qquad e_{C4}e_{P2}=0.                              \tag{3}
\]

The direction charge is

\[
                 (-2,1,1,0,0),                     \tag{4}
\]

so `e_C4` fixes it and `e_P2` kills it.  The signed Weyl telescope is block
diagonal for this decomposition: it changes colour words but does not turn a
`DQ/PS` operation into `PQ/SQ` or change its repeated type.  Consequently no
choice of telescope pairing or prefix order moves (4) into the P2 square.

This obstruction remains even when word, endpoint head, and coarse fine
labels coincide.  The exact mixed-word counterguard at word `001122` has
nonzero second-Hasse values in all four `DQ`, `PS`, `PQ`, and `SQ` packets,
but they occupy distinct direction-pair components of the repeated source
grade.  Equality of the output word therefore does not identify their
central idempotents.

## Consequence for the proof

The construction advances the proof by one real step:

```text
retained switch carrier T
    x signed-Weyl telescope H_W
    -> source-provenant, target-safe, matching-centered top chi_w face.
```

The remaining lower boundary is now sharper:

```text
(dT)H_W
    -> C2+/P2 tail arm (formal relative graph exists)
    + 18 DQ/PS relative-C4 direction faces
    -> one same-grade relative-C4 restriction/insertion primitive.
```

Thus the shortest next attack is not another Weyl telescope and not a larger
P2 square.  It is the four-site same-grade relative-`C4` landing, natural for
the switch graph and the Weyl word orbit.  Once that cell is supplied, the
existing P2 relative square and the committed word-`0102`/`dq`/`Q`/ores
descent become the relevant downstream route.

No accepted terminal, physical P2 carrier landing, or new `q/W/ridge`
promotion is asserted here.

## Reproduction

```bash
python3 computations/verify_h3_gate_ii_switch_weyl_product_rule_idempotent_gate.py
python3 -O computations/verify_h3_gate_ii_switch_weyl_product_rule_idempotent_gate.py
python3 -I -S computations/verify_h3_gate_ii_switch_weyl_product_rule_idempotent_gate.py
```

Frozen ledger digest:

```text
d9cb04b3aa0bba20b225776edf73f8142b0f88286e00b1c79f962ed774bce58a
```

Checker digest:

```text
fbd4815eb5c6d46b8dbcd018f6e75237f004e3f52b1ccf47631479b698f9db35
```
