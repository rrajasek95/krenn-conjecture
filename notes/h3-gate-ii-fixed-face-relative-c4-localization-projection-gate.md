# Fixed-face units leave the selected relative-C4 projection unsolved

## Sharp result

The factorwise shortcut is valid, but only for the coefficient-core part of
the Gate-II face.

On the fixed four-site window `2345`, the switch--Weyl product of `713b259`
leaves

\[
 -2\,d(DQ_{01})H+d(P_0S_1)H+d(P_1S_0)H,             \tag{1}
\]

where

\[
 H=q_{23}q_{45}+q_{24}q_{35}+q_{25}q_{34}.           \tag{2}
\]

At a fixed complex source, every partner coefficient in (1) is either zero
or a field unit:

```text
direction       partner coefficient
dD              q01
dq01            D
dp0             s1
ds1             p0
dp1             s0
ds0             p1
```

If the partner is zero, its three C4 matching terms vanish.  If it is
nonzero, it can be divided on that face.  Therefore the scalar common-core
colon from `4e2ff27` is not the obstruction for these six literal faces.

This does **not** construct the physical relative-C4 repair.  Scalar
normalization presupposes same-grade source columns with the selected C4
row.  The switch--Weyl cell supplies the selected row as the boundary which
must be repaired, together with its exact word/fine/Hasse labels; it is not a
second source preimage of that row.  Keeping all complete-response companion
occurrences leaves an independent affine projection problem.  A centered
`K2,2` is the smallest exact face-complete counterguard, and its primitive
dual survives every nonzero scalar normalization.

Exact checker:
[`verify_h3_gate_ii_fixed_face_relative_c4_localization_projection_gate.py`](../computations/verify_h3_gate_ii_fixed_face_relative_c4_localization_projection_gate.py).

Thus the present theorem is

\[
\boxed{
\begin{gathered}
\text{fixed-face scalar saturation: yes, pointwise;}\\
\text{literal relative DGA: yes, with a retained carrier;}\\
\text{physical selected-C4 landing: still not constructed.}
\end{gathered}}                                       \tag{3}
\]

## 1. The retained switch coordinate is still presentation-safe

Use degree-zero coordinates

```text
uA,uB,uC,zA,zB,zC,tB,tC
```

and the five monic graph columns

\[
\begin{aligned}
 d\theta_i&=z_i-u_i,\\
 d\phi_B&=t_B-(z_B-z_A),\\
 d\phi_C&=t_C-(z_C-z_A).
\end{aligned}                                        \tag{4}
\]

Their rank is five, so the degree-zero quotient has dimension `8-5=3`, the
original `A,B,C` fibre.  With

\[
 G_B=\phi_B+\theta_B-\theta_A,
 \qquad G_C=\phi_C+\theta_C-\theta_A,                 \tag{5}
\]

one has

\[
 d(G_B+G_C)=t_B+t_C+2u_A-u_B-u_C=T+L_{01}.            \tag{6}
\]

Hence `T=tB+tC` is retained.  Neither `T` nor `L01` has been set to zero.
The cell `T*H_W` is therefore legal and its direction boundary (1) is a
genuine source-labelled face.

## 2. The fixed-face scalar dichotomy

Let

\[
 s=(1,1,1),\qquad d_{01}=(1,-1,0),\qquad
 d_{12}=(0,1,-1).                                    \tag{7}
\]

The three vectors form a basis of the C4 occurrence module.  If a
same-grade physical repair map already contains

\[
                       a s,quad a d_{01},quad a d_{12},             \tag{8}
\]

and `a` is nonzero at the fixed source, the inverse from `4e2ff27` is
literal:

\[
\begin{aligned}
 m_0&=(s+2d_{01}+d_{12})/3,\\
 m_1&=(s-d_{01}+d_{12})/3,\\
 m_2&=(s-d_{01}-2d_{12})/3.                           \tag{9}
\end{aligned}
\]

Multiply (8) by `a^{-1}` and apply (9).  This proves the conditional
full-core unit construction in the exact fixed Hasse block.  All `64`
zero/nonzero patterns of the six partner coefficients obey the same rule:
each active coefficient accounts for three normalizable matching terms and
each zero coefficient removes three terms, for a total of eighteen.

The hypothesis in (8) is load-bearing.  It says that the selected source
rows already exist.  The codomain face in (1) supplies `a*s` as a repair
obligation, not as a new column in the repair map.  Dividing its coefficient
does not reverse the boundary map.

This is also the distinction between a pointwise coefficient unit and a
uniform polynomial operation.  On the open `D(a)`, division by `a` is
regular; on `V(a)`, the face vanishes.  This constructible split removes the
coefficient obstruction, but it says nothing about complete-row companion
projection on `D(a)`.

## 3. The minimal relative DGA is explicit

For any one of the three literal direction pairs, write the degree-zero
factors as `x,y`, with

\[
 dx=x',\qquad dy=y',\qquad dx'=dy'=0.                 \tag{10}
\]

Adjoin a tail-covariant relative graph on the fixed C4 window:

\[
                    dU=H-r,\qquad dr=0.               \tag{11}
\]

Here `r` is retained.  One old `H` coordinate has become the two coordinates
`H,r` modulo the single monic relation `H-r`, so `H0` remains
one-dimensional.  Repeating (11) in the three central blocks

```text
Hasse[2](D,Q01), Hasse[2](P0,S1), Hasse[2](P1,S0)
```

preserves the three old local `H0` dimensions exactly.

The two Leibniz arrows totalize without an extra mixed face.  Put

\[
                         K=-d(xy)U=-(x'y+xy')U.        \tag{12}
\]

Then

\[
                         dK=d(xy)(H-r).                \tag{13}
\]

Indeed,

\[
\begin{aligned}
 d(-x'yU)&=x'y(H-r)+x'y'U,\\
 d(-xy'U)&=xy'(H-r)-x'y'U.                            \tag{14}
\end{aligned}
\]

The two `x'y'U` faces cancel termwise.  This is the literal
PP/reinsertion square, not just a support count.

Applying (12)--(14) to (1) exports precisely

\[
\begin{aligned}
 &-2\bigl((dD)q_{01}+D(dq_{01})\bigr)r_{DQ},\\
 &\phantom{-2}\bigl((dp_0)s_1+p_0(ds_1)\bigr)r_{PS01},\\
 &\phantom{-2}\bigl((dp_1)s_0+p_1(ds_0)\bigr)r_{PS10}.                \tag{15}
\end{aligned}
\]

Thus (11) is the exact minimal relative-C4 construction and (15) is its
first augmented face.  It transports the obstruction to a retained carrier;
it does not erase it.  Setting `r=0` would turn (11) into an absolute
attachment and change the old `H0`.  A physical source column whose boundary
has nonzero `r` component is still required.

## 4. Scalar inversion does not project a complete row

The independent source-role obstruction already appears in the normalized
face-complete rows

\[
\begin{aligned}
 F_{A0}&=C+z_{00}+z_{01},\\
 F_{A1}&=C+z_{10}+z_{11},\\
 F_{B0}&=C+z_{00}+z_{10},\\
 F_{B1}&=C+z_{01}+z_{11}.                            \tag{16}
\end{aligned}
\]

Every companion occurs twice and every row has two companions.  The only
row relation is centered:

\[
                  F_{A0}+F_{A1}-F_{B0}-F_{B1}=0.      \tag{17}
\]

It cancels `C` together with the companions; it does not project `C`.  The
exact dual

\[
             \eta=(1,-\tfrac12,-\tfrac12,-\tfrac12,-\tfrac12)       \tag{18}
\]

on `(C,z00,z01,z10,z11)` kills all four rows and reads one on `C`.  Their
rank is three and rises to four after adjoining `C`.

For every nonzero scalar `a`, the scaled rows `a*F_v` have the same span.
The dual still kills them and reads `a` on `a*C`.  Therefore inverting
`q01`, `D`, `p_i`, or `s_i` normalizes (16) but cannot remove its affine
companion class.

The actual three-chart Gate-II shadow says the same thing before the
face-complete abstraction.  The endpoint charts `B,C` have rank two;
adjoining either

\[
 R=A+B+C,\qquad L=2A-B-C                              \tag{19}
\]

raises the rank to three.  The direct-chart covector has values

```text
(B,C,R,L)=(0,0,1,2).
```

Nonzero coefficient rescaling preserves these ranks and values up to a
unit.  The switch--Weyl construction fixes the earlier word/fine/Hasse
typing failure by placing the desired codomain face.  It does not supply an
extra complete-response column with which to cancel the endpoint/direct or
companion cokernel.

The `K2,2` in (16) is an exact implication counterguard, not a claim that a
full ternary decorated hafnian source realizes this abstract component.
Consequently the conclusion is a sharp boundary on the proposed shortcut,
not an accepted physical terminal.

## 5. Shortest positive datum

The scalar split, C4 coherence, switch labels, product-rule signs, and
presentation-safe relative graph are now explicit.  The shortest remaining
positive datum is one source-labelled column in each fixed DQ/PS block—or
one covariant combined column—whose complete boundary has nonzero component
on the retained `r_j` of (11), after every companion occurrence is kept.

Equivalently, the next calculation should evaluate the transported charge
on the common-core coefficient row of the **actual first physical complete
companion component**:

```text
uncentered charge  -> explicit selected-C4 projector;
centered charge    -> extend eta through its higher boundary or land a terminal.
```

Another factor localization or Weyl telescope cannot decide this affine
projection.

## Verification

Run

```text
python3 computations/verify_h3_gate_ii_fixed_face_relative_c4_localization_projection_gate.py
python3 -O computations/verify_h3_gate_ii_fixed_face_relative_c4_localization_projection_gate.py
python3 -I -S computations/verify_h3_gate_ii_fixed_face_relative_c4_localization_projection_gate.py
```

The checker pins the switch--Weyl product rule, presentation-safe switch
DGA, Gate-II response-carrier landing, C4 unit/colon theorem, and uniform
complete-row projection boundary.  It verifies the switch graph rank, all
64 scalar zero/unit patterns, the conditional C4 inverse, the exact two-arrow
relative DGA, preservation of `H0`, the first retained faces (15), the
direct-chart rank detector, and the scalar-stable centered `K2,2` dual.

Frozen ledger digest:

```text
e62422ac6e684636a46f4d011062bd9d1e5120d0d97f540ec7cd1719eaecd592
```
