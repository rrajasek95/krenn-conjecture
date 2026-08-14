# The uniform response deformation lands two of the three Gate-II charts

## Result

The centered occurrence projector gives a genuine presentation-safe
**relative** landing for the two endpoint charts in Gate II.  It does not
give the direct `Dq01` chart, so it does not yet construct the full carrier
orbit `(t_R,t_L,t_zprivate)`.

On the ninety endpoint occurrences put

\[
 c_f=90e_f-\mathbf1_{90},\qquad
 c_{01}=30b_{01}-\mathbf1_{90}.
\]

For the residual matching numerator `M=A+I`, the exact identity is

\[
                         M c_f=3c_{01}.                 \tag{1}
\]

The universal centered response deformation supplies the monic relative
graph

\[
                         d\beta_f=c_f-u_f.              \tag{2}
\]

Applying `M/3` to (2) gives

\[
 d(M\beta_f/3)=c_{01}-u_{01},
 \qquad u_{01}=Mu_f/3.                                 \tag{3}
\]

Combining (3) with the complete endpoint response generator reconstructs
only a relative selected fibre,

\[
 d\epsilon_{01}=b_{01}-t_B,
 \qquad t_B=u_{01}/30.                                 \tag{4}
\]

The graph keeps the old `H0`: its dimensions are `89 -> 89`.  Setting the
carrier to zero gives the raw centered boundary and changes them to
`89 -> 88`.  Thus (1)–(4) are the maximal presentation-preserving
consequence of the coefficient identity.  Endpoint reversal gives the
analogous carrier `t_C`.

Exact checker:
[`verify_h3_gate_ii_uniform_response_relative_carrier_landing_gate.py`](../computations/verify_h3_gate_ii_uniform_response_relative_carrier_landing_gate.py).

## Why this is not yet `R01` or `L01`

Write

\[
 A=Dq_{01}H,\qquad B=p_0s_1H,\qquad C=p_1s_0H,
\]

where

\[
 H=q_{23}q_{45}+q_{24}q_{35}+q_{25}q_{34}.
\]

Then

\[
 R_{01}=A+B+C,\qquad L_{01}=2A-B-C.                  \tag{5}
\]

The endpoint response deformation reaches the `B,C` plane.  In the literal
105-occurrence module that plane has rank two, while adjoining either
`R01` or `L01` raises the rank to three.  The normalized direct-chart
covector kills `B,C` and has values

```text
                       (B,C,R01,L01)=(0,0,1,2).
```

The missing third chart is exactly the already isolated augmentation-one
column

```text
U_C4[D,Q01;2345] -> H2345,
```

followed by a physical reinsertion by `D*q01`.  If three monic graphs

\[
 d\Gamma_A=t_A-A,
 \quad d\Gamma_B=t_B-B,
 \quad d\Gamma_C=t_C-C                              \tag{6}
\]

were available, the required top carrier would be automatic:

\[
 t_R=t_A+t_B+t_C,
 \qquad t_L=2t_A-t_B-t_C.                            \tag{7}
\]

Equations (6)–(7) are a change of basis among relative graph coordinates and
preserve `H0`.  The present machinery constructs the endpoint part of (6),
not the direct `A` part.  Introducing a universal coefficient parameter for
`A` would merely add another formal KS generator; it would not provide its
fixed physical comparison.

## The first product-rule face

There are two useful stopping points, depending on what is granted.

Without any new physical comparison, (3) stops at

\[
 dc_{01}=30,db_{01}-dR,                              \tag{8}
\]

where

\[
\begin{aligned}
 db_{01}=p_0s_1(&dq_{23}q_{45}+q_{23}dq_{45}
                +dq_{24}q_{35}+q_{24}dq_{35}\\
                &+dq_{25}q_{34}+q_{25}dq_{34}).       \tag{9}
\end{aligned}
\]

The old complete first-PP rows have rank two in the selected quotient;
adjoining (9) raises the rank to three.  Residual matching flips fix its
aggregate, so Maschke contraction does not remove it.  Thus the selected
six-term `db01` packet is the first currently ungranted physical face.

Now grant (9), its endpoint-reversed mate, and the same-grade lower `U_C4`
tail.  The full differential of `L01` has the exact split

```text
18 residual-tail derivatives + 18 direction-factor derivatives.
```

The normalized Gate-II covector is zero on the tail half and one on the
direction half.  The remaining six direction marginals are

\[
             (6,6,-3,-3,-3,-3)
             =3(2,2,-1,-1,-1,-1).                   \tag{10}
\]

For the direct chart these include the two independent cap faces

\[
 (\delta D)q_{01}U_{C4},\qquad D(\delta q_{01})U_{C4}. \tag{11}
\]

The `p0*s1` and `p1*s0` charts contribute their corresponding endpoint
factor derivatives.  Consequently the exact first face after the strongest
tail grant is the eighteen-term endpoint/direction packet, not zero.

## Downstream scope

Once that eighteen-term section is physically placed, the committed finite
labelled descent applies:

```text
(t_R,t_L)
    -> 18 direction terms
    -> word-0102 private carrier
    -> C*d=12*d
    -> dq23 / occurrence-labelled Q-ores
    -> labelled ores detector -35/72.
```

The scalar ordinary-residue value on the remaining labelled packet is zero.
The complete-response gauge and `d_even` remove it only after the physical
occurrence-to-`Q/ores` map and mixed-target square have been placed.

The universal response parameter has no fixed word/fine/repeated AugP2
image, and no physical `q`, `W`, or labelled ridge before that comparison.
Therefore the downstream calculation is conditional: it is neither a
closed carrier landing nor an accepted terminal.

## Shortest positive datum

Construct one source-labelled, termwise-PP-natural comparison for the
universal endpoint carrier whose selected face is (9), and the covariant
same-grade `U_C4[D,Q01;2345]` cap.  Totalize their eighteen direction-factor
faces in the existing labelled two-root square.  After that, the committed
`0102/dq/Q/ores` ladder is exhaustive; there is no new unlabelled recursive
Hasse problem.

This is exact for canonical `h=3` over characteristic zero.  It does not
identify a formal response-family parameter with a fixed physical source
chain.

Run normally, optimized, and isolated/no-site.  The checker prints its
frozen ledger digest.
