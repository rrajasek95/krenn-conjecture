# Root/Weyl–Reynolds–`K_Eq` has zero response-to-cap component

## Outcome

On the minimal shared-site collision quotient, the positive coefficient
chain is as large as it can be:

```text
shared-site coordinates before minimalization       148
shared-P3 response rank                             146
two root copies                                     292
two ordered endpoint lifts                           584
endpoint-even Reynolds image                         292
endpoint-even rank per root                          146
```

The target-corrected root/Weyl operations and endpoint Reynolds projector
lose none of these 146 directions.  Nevertheless their composite with the
existing objectwise `K_Eq` and target cone has

\[
             \operatorname {rank}(e_C\,K_{Eq}P_+W\,e_R)=0.       \tag{1}
\]

The reason is categorical, not numerical:

\[
 W,P_+\in e_RAe_R,\qquad K_{Eq},T_{23},T_{45}\in e_CAe_C,
 \qquad e_Ce_R=0.                                      \tag{2}
\]

Thus this positive composition does not construct a nonzero
response-to-cap component.

Exact checker:
[`verify_h3_rank146_root_weyl_reynolds_keq_composite_gate.py`](../computations/verify_h3_rank146_root_weyl_reynolds_keq_composite_gate.py).

## 1. Word transport is relative and preserves the response tags

The two response words in the order-six block are

```text
11111111       5 changed sites to 01211222,
11211211       3 changed sites to 01211222.
```

Their normalized local-`GL3` word intervals have cube data

```text
pure:   vertices 32, edge-incidence rank 31, H0 dimension 1,
mixed:  vertices  8, edge-incidence rank  7, H0 dimension 1.
```

In both cases the bar boundary is `all-L - all-D`; the desired all-`L`
endpoint is not an absolute boundary.  The signed-Weyl companion gives a
physical target correction inside the response object.  It changes colour
words but preserves the underlying matching, matching index, repeated-edge
label, and second-Hasse direction tag.

Consequently the literal projection to the cap `Gamma*` summand is already
zero after the word stage.  Its first grade mismatch is the selected
`t*q_(v,N)` fine/window and full `P3+K2` parent placement.  A shared-P3 pair
coordinate is the correct collision topology but is not itself a selected
cap parent or occurrence idempotent.

To isolate the load-bearing obstruction, the checker then grants the
strongest possible diagonal repair:

> grant a monic target-safe word endpoint and every diagonal
> fine/repeated/window placement on all 146 response directions.

The result below therefore cannot be blamed on the normalized-bar endpoint
or on a choice of fine label.

## 2. Reynolds preserves the entire quotient

On every oriented endpoint pair,

\[
 P_+=\frac12\begin{pmatrix}1&1\\1&1\end{pmatrix}
\]

has rank one and satisfies

\[
P_+^2=P_+,qquad sP_+=P_+s=P_+.
\]

Tensoring with the rank-146 collision quotient and the two root labels gives
rank 292.  Hence the endpoint-even reduction is lossless on the desired
coefficient packet.  It does not, however, change its operation object.

## 3. The exact root-labelled operation dual

Even after independently granting every diagonal word, head, fine,
repeated, window, and same-object operation repair, the two-root section
ledger is

```text
strong diagonal base                              rank 24
+ AB response-to-cap section                      rank 25
+ AC response-to-cap section alone                rank 25
+ one root-forgetting AB+AC aggregate             rank 25
+ both separately labelled sections               rank 26.
```

Thus the absent operation quotient is two-dimensional, with primitive
duals

\[
                 \omega_{AB}^{Hom},\qquad
                 \omega_{AC}^{Hom}.                  \tag{3}
\]

One root-forgetting sum leaves

\[
       (\omega_{AB}^{Hom}-\omega_{AC}^{Hom})/2.       \tag{4}
\]

These are root-operation characters, constant and natural over the
rank-146 occurrence quotient; the 292 coefficient directions do not create
292 new operation generators.

## 4. `K_Eq` and the target cone occur one stage later

Conditionally after a cap landing, the target cone has rank two:

\[
dT_{23}=N_{23},\qquad dT_{45}=N_{45}.
\]

It changes target `H1` from two to zero and the relative protected `H1`
from three to one.  The survivor is

\[
                         \omega_{Eq}=(1,-1).           \tag{5}
\]

But this cone is a cap-internal proper-face completion.  It cannot be
postcomposed with a response vector before an `e_CAe_R` map exists.  If both
root Hom units are formally granted, the next boundary is exactly

```text
dG0_response = (1,0),
dr0_Eq,cap   = (0,1),
rank          2,
dual          (1,-1).
```

This orders the obstructions sharply:

1. literally, selected fine/window placement fails after word transport;
2. after granting every diagonal placement, the two root-natural
   `e_CAe_R` matrix units fail;
3. after granting those units, the single Eq excess class remains and the
   existing target cone supplies its target proper faces.

## Shortest positive datum

The next construction must be a genuinely operation-changing map, not a
further colour or parity projector.  The most economical candidate is one
root-natural, endpoint-even Beck–Chevalley/excess map from the shared-site
collision groupoid to `AugP2`, with excess boundary

\[
                         (H_0-u)e_{Eq}.                \tag{6}
\]

Its `AB` and `AC` instances would kill (3); equation (6) would then feed the
already constructed `K_Eq`/target-cone completion.

## Verification

```bash
python3 computations/verify_h3_rank146_root_weyl_reynolds_keq_composite_gate.py --mode structural
python3 computations/verify_h3_rank146_root_weyl_reynolds_keq_composite_gate.py --mode full
python3 computations/verify_h3_rank146_root_weyl_reynolds_keq_composite_gate.py --mode exhaustive
```

Frozen ledger SHA-256:
`6bd3f79a2b8f493ac5736dfcc6c2f385a6118b9f8a6f2ec91db4e520d5532abe`.
