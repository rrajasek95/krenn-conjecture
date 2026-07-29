# Cofactor quotients and the first collision Bianchi equation

## Outcome

There is a precise cross-pair compatibility equation, but it occurs at
third order and it cannot be written from the second-order output tensors
alone.

For a half-shift source

\[
                       q(t)=q_0+tK+t^2W,                  \tag{1}
\]

the pair equations first determine each active direct coefficient
`eta_ij` through the full deleted-pair cofactor quotient.  The vanishing
three-`z` target coefficient then imposes, for every triple `i,j,k`,

\[
 (\eta_{ij}k_k+\eta_{ik}k_j+\eta_{jk}k_i)
       {q_0^{m-2}\over(m-2)!}
 +k_ik_jk_k{q_0^{m-3}\over(m-3)!}=0.                     \tag{2}
\]

This is the first genuine Bianchi/Maurer--Cartan equation coupling
different pairs.  It is necessary for an exact ternary source, and the
complete-pure-normal-block countermodel violates it.  However, (2) is not
a consequence of the pair tensors `C_ij` and `B_ij`: a direct `W_ij`
direction can be invisible through second order and become visible after
multiplication by a third site tangent.  An exact Hamilton-cycle example
below exhibits that phenomenon.

Thus the useful hierarchy is:

1. full pair cofactor quotients at order two;
2. the connection coefficients `eta_ij`, including second-order-dormant
   ones;
3. triple Bianchi equations (2);
4. higher even/odd Maurer--Cartan equations.

A Pluecker relation involving only the scalar or tensor-valued pair
outputs skips item 2 and is not universal.

## 1. Normalized expansion

Work in the squarefree site algebra and put `n=2m`.  Decompose

\[
 K=\sum_i z_i k_i,
 \qquad W=\sum_{i<j}\eta_{ij}z_i z_j.                     \tag{3}
\]

Write

\[
 X_r=\sum_{|S|=r}\prod_{i\in S}z_i\prod_{v\notin S}x_v.
\]

The coefficient of `t^r` in `H(q(t))=q(t)^m/m!` is

\[
 \sum_{a+2b=r}
 {K^aW^bq_0^{m-a-b}\over a!b!(m-a-b)!}.                  \tag{4}
\]

The half-shift target is

\[
 Y+\prod_i(x_i-tz_i/2)+\prod_i(x_i+tz_i/2)
 =Y+\sum_{r\ {m even}}2^{1-r}t^rX_r.                  \tag{5}
\]

The first three nonconstant equations are therefore

\[
 {Kq_0^{m-1}\over(m-1)!}=0,                              \tag{6}
\]

\[
 {Wq_0^{m-1}\over(m-1)!}
 +{K^2q_0^{m-2}\over2(m-2)!}=\frac12X_2,                 \tag{7}
\]

and

\[
 {KWq_0^{m-2}\over(m-2)!}
 +{K^3q_0^{m-3}\over6(m-3)!}=0.                          \tag{8}
\]

Extracting the `z_i z_j z_k` sector of (8) gives (2); all factorials cancel
exactly as displayed.

## 2. Pair quotient followed by Bianchi

For a pair `i,j`, define

\[
 C_{ij}={q_0^{m-1}\over(m-1)!}\bigg|_{B\setminus\{i,j\}},
 \qquad
 B_{ij}=k_i k_j{q_0^{m-2}\over(m-2)!}.                   \tag{9}
\]

Then (7) in this sector is

\[
             \eta_{ij}C_{ij}+B_{ij}=\frac12X_{-ij}.      \tag{10}
\]

If `C_ij` is nonzero, (10) has a solution exactly when the full cofactor
wedge vanishes, and it then determines `eta_ij` uniquely.  For any
functional `phi_ij` nonzero on `C_ij`, one may write

\[
 \eta_{ij}=
 {\phi_{ij}(X_{-ij}/2-B_{ij})\over\phi_{ij}(C_{ij})}.     \tag{11}
\]

The value is independent of the chosen functional precisely because the
pair quotient equation holds.

Define the one-step descended tensors

\[
 L_{k\mid ij}=k_k{q_0^{m-2}\over(m-2)!},
 \qquad
 G_{ijk}=k_ik_jk_k{q_0^{m-3}\over(m-3)!}.                \tag{12}
\]

Substitution of (11) into (2) gives the coordinate-free cross-pair
compatibility

\[
 \eta_{ij}L_{k\mid ij}
 +\eta_{ik}L_{j\mid ik}
 +\eta_{jk}L_{i\mid jk}
 +G_{ijk}=0.                                               \tag{13}
\]

Equation (13), rather than a tetrad among all-`x` pair entries, is the first
universal overlap identity.

There is an essential qualification.  If `C_ij=0`, equation (10) requires
literal equality `B_ij=X_-ij/2` but leaves `eta_ij` undetermined.  That
coefficient can still occur in (13) through `L_{k|ij}`.  Hence passing from
the source coefficient `eta_ij` to its second-order image
`eta_ij C_ij` loses data needed by the Bianchi equation.

## 3. Exact dormant-connection countermodel

Take the six-site alternating Hamilton base

\[
 q_0=2x_0x_1+x_2x_3+x_4x_5
       +y_1y_2+y_3y_4+y_0y_5.                             \tag{14}
\]

It realizes `2X+Y`.  Put

\[
                         K=z_1x_3,
 \qquad                  W=\eta z_0z_2.                  \tag{15}
\]

Vertices `1,3` lie on the same shore of the alternating cycle, so the
one-`z` cell in (15) is in the complete tangent kernel and (6) holds.
Likewise, deleting the same-shore pair `0,2` leaves no perfect matching, so

\[
                         C_{02}=0.                         \tag{16}
\]

Since `K` has only one `z`-site sector, `K^2=0`.  Thus every value of
`eta` gives exactly the same source output through order two.

At order three, however, the matching

\[
                         02\mid13\mid45                  \tag{17}
\]

uses `W`, `K`, and the `x_4x_5` base cell.  It is the unique contribution
to `z_0z_1z_2x_3x_4x_5`, and its coefficient is

\[
                              \eta.                       \tag{18}
\]

Therefore two arcs with identical `q_0`, identical `K`, and identical
second-order tensors `eta_ij C_ij` can have different Bianchi residuals.
No identity formed only from `C_ij=dH(W_ij)` and `B_ij` can recover (13).

## 4. The complete scalar normal countermodel fails Bianchi

For the exact rational data in
[`complete-normal-block-pluecker-countermodel.md`](complete-normal-block-pluecker-countermodel.md),
all fifteen pure pair coefficients agree with the target.  Its three
direct cells on `01,23,45` are invisible to those pure coordinates and
remain free at that stage.

Nevertheless the pure triple coloring

\[
                         x_0x_1x_2z_3z_4z_5               \tag{19}
\]

has third coefficient

\[
                            -\frac{255}{64}.               \tag{20}
\]

The coefficients of each of the three still-free direct cells in (20)
vanish (the possible contributions cancel exactly).  Thus no choice of
those cells repairs this Bianchi equation.  In fact thirty three-`z`
colorings have nonzero third residuals for that displayed scalar-normal
solution.

This does not prove a universal contradiction: the example already fails
twelve full pair quotient components.  It does show that adding the true
third-order overlap equations is strictly stronger than imposing all
scalar Pluecker blocks, and it gives the exact form a universal
compatibility proof would have to exploit.

## 5. Higher equations

For reference, the next coefficient is

\[
 {W^2q_0^{m-2}\over2(m-2)!}
 +{K^2Wq_0^{m-3}\over2(m-3)!}
 +{K^4q_0^{m-4}\over24(m-4)!}=\frac18X_4.                \tag{21}
\]

For six sites (`m=3`) the remaining equations terminate as

\[
 {W^2q_0\over2}+{K^2W\over2}=\frac18X_4,
 \qquad {KW^2\over2}=0,
 \qquad {W^3\over6}=\frac1{32}X_6.                       \tag{22}
\]

Together, (10), (13), and (21)--(22) are a finite Maurer--Cartan hierarchy
for a six-site collision.  The order-three equation is the first member
which genuinely couples different pair sectors.

[`verify_collision_cofactor_bianchi.py`](../computations/verify_collision_cofactor_bianchi.py)
audits the normalization on the exact four-site collision, verifies the
dormant connection (14)--(18), and checks (19)--(20) over the rationals.
