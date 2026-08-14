# The first mixed `K_Eq/AugP2` face remains the physical comparison obstruction

## Result

For the exact parents

\[
 M=01\,23\,45\,67,\qquad N=07\,12\,34\,56
\]

and the `q=01` Taylor--Spencer face, the common branch is

\[
 K=07\,23\,45\,67.
\]

Its two surviving restrictions are `q23` and `q45`.  In the centered
coefficient calculation these are exactly

```text
0112/q23 -> B1,       0121/q45 -> B4.
```

Thus the common parent module `V=Q^90` supplies the normalized top `R` and
the correct response-side restrictions.  It does not supply the displayed
word/fine/repeated/operation-labelled arrows into the cap packet.

Across the four oriented root paths `(AB-,AB+,AC-,AC+)` and the six selected
`B` labels, the objectwise `K_Eq`, `D4`, `P2`, and cap arrows give 24 square
boundaries.  Each edge skeleton has rank three and one cycle
`(1,-1,1,-1)`.  Therefore

```text
vertices = 96, edges = 96, edge rank = 72, H1 = 24.
```

All 24 cycles have zero target, zero Eq augmentation, and `d^2=0`.  No
existing physical two-cell fills them.  Even after imposing the strongest
label and root transport, those relations have rank 23 and leave one class,
detected by

\[
 \omega_{\rm mix}={1\over24}\sum_{r,j}D_r\,\mu_{r,B_j}^{*},
 \qquad D=(-1,1,-1,1).
\]

It vanishes on every pinned current augmented row and takes value one on the
full `D`-oriented mixed-square schema.

## Simultaneous totalization

In row order `(R, lower, Eq, ores)`, common `V` and the old correction give

\[
 (1,0,0,0)+(0,1,1,-1)=(1,1,1,-1),
\]

whereas the required comparison boundary is `(1,0,1,0)`.  The exact debt is

\[
                    (0,-1,0,+1).                 \tag{1}
\]

The pinned simultaneous `D4/P2/K_Eq/d_even` operator has rank 24 and
determinant 64.  Once the missing mixed section is supplied, it has the
unique characteristic-zero normalization

\[
                    K=(B_1+B_4)/2
\]

and cancels lower, Eq, ordinary residue, target, and anchor/incidence
readouts.  This is a conditional solve, not a construction of the section:
common `V` alone leaves (1).

## Endpoint-even cap quotient

The six cap cells have twelve ordered `P/S` parent candidates.  Endpoint
forgetting has rank six and odd kernel dimension six.  Passing to the
canonical rational even section

\[
 {1\over2}\bigl(M_{(p,s,N)}+M_{(s,p,N)}\bigr)
\]

therefore removes the orientation ambiguity without choosing either ordered
parent.  It does **not** remove the enriched comparison obstruction.  The
first retained boundary is still rank two:

```text
dG0 = (H-u)_response,       dr0 = (H-u)_Eq,cap.
```

After this degree-one obstruction come two independent mixed-target normals.
Modulo the two local diagonal lines their pairing with the protected word
detectors is

\[
 \begin{pmatrix}
 X_{00211122}^{*}\\ X_{00111222}^{*}
 \end{pmatrix}
 \begin{pmatrix}n_{0112}&n_{0121}\end{pmatrix}
 =\begin{pmatrix}2&0\\0&2\end{pmatrix}.             \tag{2}
\]

Hence their normalized rational detectors are one half of the displayed
word covectors.  Endpoint averaging acts on the `P/S` parent factor and
does not affect (2).  The cut/root involution exchanges the two normals, but
their invariant sum is nonzero.  The exact remaining obstruction dimensions
are consequently

```text
mixed Eq stage: 1,       protected target stage: 2.
```

The correction from commit `4373ae6` does not change this rank.  It is a
dual extension

\[
 target_j=W_j=-\mu_j,\qquad ores_j=\mu_j,\qquad
 ridge=-\sum_j\alpha_j\mu_j,
\]

with `q=ainc=Eq=0`; it adds no source column.  If a source-labelled placement
of a protected normal into those four corner rows is supplied, the formula
extends its detector through all known `r0,T,rho,K` columns.  It therefore
supports the terminal alternative and cannot itself fill either target
normal.

## Cyclic operator-module formulation

Let `A` denote the literal divided-Weyl/Hasse operation algebra and let the
TrigEulerSpencer packet be the cyclic module

\[
                 P_R=Ae_R/\operatorname{Ann}_A(e_R).
\]

If the physical cap packet `C_cap` is an `A`-module, an `A`-linear map with
`e_R -> r0` exists exactly when

\[
                  \operatorname{Ann}_A(e_R)\,r0=0.    \tag{3}
\]

The pinned full-star simplex, all 1,020 deleted-factor squares, the nine
ambiguous-lcm cylinders, and the ordinary objectwise `K_Eq/D4/P2` faces clear
every currently presented relation except the following tower:

1. the transported relation
   `(H-u)_response=(H-u)_Eq,cap`, represented by `omega_mix`;
2. the two protected mixed-target cone relations in (2).

Thus (3) is the right noncircular replacement for “adjoin an off-diagonal
arrow”: proving that `r0` is annihilated by these relations would construct
the comparison as an `A`-module homomorphism.  This is not yet an unconditional
existence theorem.  Two source statements remain unproved: that `C_cap`
really carries the literal `A`-action, and that the pinned full-star
presentation exhausts `Ann_A(e_R)`.  Without them, the exact result is the
normalized obstruction/terminal certificate above.

## Scope and verification

The checker covers the fixed `h=3` `M/N/q01` face, all six selected cap
labels, all four oriented root paths, the endpoint-even quotient, the pinned
1,020/9 protected presentation, and the complete currently modelled
augmented rows.  It does not construct the missing word-changing physical
operation or assert an unproved cap `A`-module structure.

Run:

```text
python3 computations/verify_h3_first_face_keq_augp2_mixed_square_totalization_gate.py
python3 -O computations/verify_h3_first_face_keq_augp2_mixed_square_totalization_gate.py
python3 -I -S computations/verify_h3_first_face_keq_augp2_mixed_square_totalization_gate.py
```

Frozen ledger SHA-256:

```text
70b908555076df66fce45d28d5ed97de92e2dd4ef83d246a464c23984a5009e1
```
