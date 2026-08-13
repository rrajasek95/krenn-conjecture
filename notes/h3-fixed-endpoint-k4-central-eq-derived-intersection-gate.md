# The selected K4 / central-Eq square needs one pointed source equation

## Exact verdict

Let

\[
 b_{ps}=p_ps_s\sum_{M\in\operatorname{PM}([6]\setminus\{p,s\})}q_M,
 \qquad R=\sum_{p\ne s}b_{ps}.                         \tag{1}
\]

The physical mixed response source contains the **complete** equation `R`,
not thirty independent equations `b_ps`.  At the marked ordered endpoints
`(p,s)=(0,1)`, its K4 fibre is

\[
 b_{01}=p_0s_1(q_{23}q_{45}+q_{24}q_{35}+q_{25}q_{34}), \tag{2}
\]

whose first principal-parts face is

\[
\begin{aligned}
 db_{01}=p_0s_1(&dq_{23}q_{45}+q_{23}dq_{45}
               +dq_{24}q_{35}+q_{24}dq_{35}\\
               &+dq_{25}q_{34}+q_{25}dq_{34}).        \tag{3}
\end{aligned}
\]

There are thirty ordered endpoint fibres and 180 endpoint-tagged first
faces.  In both the coefficient and first-PP modules, the complete row has
rank one and adjoining the marked fibre raises rank to two.  The primitive
covectors

```text
b_01^* - b_10^*,
(01,dq23*q45)^* - (10,corresponding face)^*
```

kill the complete rows and read one on the marked rows.  Thus (3) is a
literal formula but is not the derivative of a separately available source
equation.

Checker:
[`verify_h3_fixed_endpoint_k4_central_eq_derived_intersection_gate.py`](../computations/verify_h3_fixed_endpoint_k4_central_eq_derived_intersection_gate.py).

## The aggregate square is canonical

Write

\[
 E=(H_0-u)e_{\rm Eq}.
\]

Grant a clean central Tate edge `theta` with `d(theta)=E`, and let the actual
complete response generator satisfy `d(epsilon_R)=R`.  Their natural mixed
Koszul cell is

\[
 \kappa_R=\epsilon_R\wedge\theta,
 \qquad d\kappa_R=R\theta-\epsilon_RE.                \tag{4}
\]

The two second-boundary terms cancel: `d^2 kappa_R=RE-RE=0`.  Hence the
aggregate complete-response / central-Eq derived intersection has one
canonical square cell, conditional only on the already open physical
promotion of the clean `theta`.

Equation (4) does not select the marked K4 fibre.  It has `dR=sum db_ps` as
its first response face.

## The selected square is conditional on exactly one new source datum

Formally, if a pointed generator existed with

\[
 d\epsilon_{01}=b_{01},                               \tag{5}
\]

then one cell would suffice:

\[
 \kappa_{01}=\epsilon_{01}\wedge\theta,
 \qquad d\kappa_{01}=b_{01}\theta-\epsilon_{01}E,     \tag{6}
\]

and again `d^2 kappa_01=0`.  Its first principal-parts packet is exactly

\[
 (db_{01})\theta+b_{01}\,d\theta
 -(d\epsilon_{01})E
 -\epsilon_{01}\big((dH_0-du)e_{\rm Eq}
                    +(H_0-u)d e_{\rm Eq}\big).        \tag{7}
\]

The first term of (7) is the six-term face (3); the last two terms record
the central Eq product-rule faces.  Therefore the required central incidence
*is* the fundamental class of a `2 x 2` derived intersection only after (5)
is part of the source presentation.  In the current complete-row
presentation it is an excess/cokernel class.  Declaring (6) without (5)
would be a formal free-occurrence square, not a physical source chain.

The weakest positive input is a source-labelled pointed response section
equivalent to (5) modulo the complete row, natural under endpoint/matching
transport.  It need not be phrased as thirty unrelated equations, but it
must split the selected fibre in the physical presentation.

## Target and augmented faces

The word `110000` is mixed.  Consequently (2) and (3) have target readout
zero.  This does not remove the endpoint-Cartan target normal.  The eight
marked endpoint moves carry the already pinned eighteen-word packet

\[
 N_f=\sum_{x\in\{0,1\},\ t\in\{2,3,4,5\}}
 (X_{\{x,t\}=1}+X_{\{x,t\}=0})
 -8X_{000000}-8X_{111111},                            \tag{8}
\]

and `X_101000^*` kills the GHZ line but reads one on (8).  Thus the moving
target correction remains a separate proper face of any physical
totalization.

There is also a logically prior augmentation issue: the ordinary derived
intersection contains `theta`, but the nearest old physical realization of
the clean target-zero central edge has forced labelled ordinary residue
`+Y`.  So even the aggregate cell (4) is conditional on the physical
central-Tate comparison; selecting (6) then additionally needs (5).

## Consequence for the proof frontier

The central Eq incidence is not a mysterious second scalar condition.  It
is exactly the mixed face of a Koszul square.  What is missing is source
provenance for one side of that square:

1. construct a physical target-zero central `theta`;
2. construct a pointed response section `epsilon_01` (or an equivariant
   family giving it modulo `R`);
3. use the canonical mixed cell (6), carrying (7), the endpoint normal (8),
   and the separately typed cap/ridge/q rows.

After that cell lands, the old unary row closes `T12`; no separate unary
companion theorem is needed.  The fibre and mixed-incidence covectors here
are local source-cokernel classes, not yet Fredholm terminals, because their
extension across every word/fine/target/anchor/q/ridge/`W`/eta/sigma row has
not been proved.

## Verification

```text
python3 computations/verify_h3_fixed_endpoint_k4_central_eq_derived_intersection_gate.py
python3 -O computations/verify_h3_fixed_endpoint_k4_central_eq_derived_intersection_gate.py
python3 -I -S computations/verify_h3_fixed_endpoint_k4_central_eq_derived_intersection_gate.py
```

Frozen ledger SHA-256:

```text
57c9c27575b4c08b66cf9132d6014beaeacf810c1e1ee420b5a6e7c20c001737
```
