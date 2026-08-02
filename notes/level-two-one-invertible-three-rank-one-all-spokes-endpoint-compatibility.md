# Endpoint compatibility excludes the exact 1I+3R+2Z all-spokes guard

Research evidence only. Krenn's conjecture remains open and the certified
spine is unchanged.

## Outcome

The potential-boundary analysis leaves one `1I+3R+2Z` support envelope,
with potentials

\[
(\nu_0,\ldots,\nu_5)
   =(\lambda,\lambda,\lambda,\lambda,-\lambda,-\lambda),
\qquad \lambda\ne0.                                         \tag{1}
\]

The exact rank-55/R2 guard displayed there does **not** extend through the
missing endpoint equations. In fact:

1. neither pure L0 target lies in the unrestricted differential image;
2. the overlapping L1 equations leave only two genuine endpoint-star
   modes on the four-site core and kill all zero-site star vectors; and
3. even the full linear span of the four products of those modes, enlarged
   by the direct endpoint term, misses both pure targets.

The same obstruction holds on the full nonzero local diagonal torus
through the guard. This closes the displayed guard and a justified
covariant family, but it does not yet close the entire all-spokes support
envelope. Any remaining survivor must lie on the special rank-55,
mixed-rank-53 incidence locus outside that torus.

The companion checker is
[`verify_level_two_one_invertible_three_rank_one_all_spokes_endpoint_compatibility.py`](../computations/verify_level_two_one_invertible_three_rank_one_all_spokes_endpoint_compatibility.py).

## 1. The exact selected guard

Use the endpoint matrices and residual packet from the potential-boundary
guard. Sites `0,1,2,3` have endpoint ranks `2,1,1,1`, sites `4,5` vanish,
all eight core-to-zero blocks are invertible, and `M_45=0`. The checker
rebuilds the packet rather than importing an opaque constant, and rechecks:

\[
X_rJX_u^{\mathsf T}=(\nu_r+\nu_u)M_{ru},                    \tag{2}
\]

all 64 selected level-two rows, exact differential rank 55 over
`Q`, `F_101`, and `F_1000003`, and literal R2 at all six roots.

## 2. Linear L0 already excludes the guard

For either binary endpoint-colour pair `(s,t)`, every full eight-site L0
slice has the universal form

\[
T_{st}=W_{st}\Psi(M)+d\Psi_M(N^{st}),                         \tag{3}
\]

where

\[
N^{st}_{ru}
 =U_r^s(V_u^t)^{\mathsf T}+V_r^t(U_u^s)^{\mathsf T}.          \tag{4}
\]

Euler's identity places the first term in the differential image, so the
two pure GHZ targets must both belong to `im(dPsi_M)` even before the
factorization (4) or any L1 overlap is imposed. The exact incidence ranks
are

\[
\begin{array}{c|ccccc}
&D&D_{\rm mixed}&[D\mid e_0]&[D\mid e_1]&[D\mid e_0,e_1]\\ \hline
\operatorname{rank}&55&55&56&56&57.
\end{array}                                                   \tag{5}
\]

All five values agree over the three audited fields. Thus neither pure
target is in the differential image. The 192 cells outside the fixed
60-cell residual binary block cannot repair (3).

For comparison, a rank-55 packet that passes both linear L0 incidences
must have the exact profile

\[
\operatorname{rank}D=55,\qquad
\operatorname{rank}D_{\rm mixed}=53,\qquad
\operatorname{rank}[D\mid e_0]
=\operatorname{rank}[D\mid e_1]
=\operatorname{rank}[D\mid e_0,e_1]=55.                     \tag{6}
\]

Equation (6) is the first exact description of the only locus on which a
continuation of this all-spokes envelope is necessary.

## 3. Overlapping L1 endpoint-star systems

The checker also imposes the missing L1 equations rather than stopping at
(5). For one P/V star family, introduce vectors `V_r` and edge scalars
`rho_ru` and solve

\[
P_rV_u^{\mathsf T}+V_rP_u^{\mathsf T}=\rho_{ru}M_{ru}        \tag{7}
\]

on all fifteen residual edges. The Q/U system is the analogous equation

\[
Q_rU_u^{\mathsf T}+U_rQ_u^{\mathsf T}=\rho'_{ru}M_{ru}.      \tag{8}
\]

Each is a `60 x 27` rational linear system of rank 24 and nullity 3. One
null direction is the vacuous scalar on the forced block `M_45=0`; it has
no endpoint-star component. The star projection therefore has dimension
two in each system. Every mode satisfies

\[
U_4=U_5=V_4=V_5=0,                                          \tag{9}
\]

as forced by the invertible core-to-zero spokes. The ordinary aligned
modes `U_r=P_r` and `V_r=Q_r` are present, together with one rank-one-core
mode in each system.

Take all four products of the two U modes and two V modes in (4). Their
differential outputs are independent, of rank four. Adding the direct
vector `Psi(M)` does not increase that rank. However,

\[
\begin{array}{c|cccc}
&\text{four products}&+\Psi(M)&+e_0&+e_1&+e_0,+e_1\\ \hline
\operatorname{rank}&4&4&5&5&6.
\end{array}                                                   \tag{10}
\]

Thus even the *linear enlargement* of every L1-compatible factored slice
misses both pure targets. The genuine bilinear endpoint-star image is a
subset of that enlargement, so (10) is a fortiori a shared factored
endpoint-star obstruction.

## 4. Covariant diagonal family

For arbitrary nonzero diagonal matrices

\[
D_r=\operatorname{diag}(d_{r0},d_{r1}),
\]

put

\[
X'_r=D_rX_r,\qquad M'_{ru}=D_rM_{ru}D_u.                    \tag{11}
\]

The generic-kernel equations, endpoint ranks, literal column-pure R2
witnesses, and nonzero cofactors are preserved. For a binary word `w` and
a tangent cell `ru(a,b)`, the differential transforms exactly as

\[
D'_{w,ru(a,b)}
 =\frac{\prod_k d_{k,w_k}}{d_{r,a}d_{u,b}}
    D_{w,ru(a,b)}.                                           \tag{12}
\]

Both row and column factors are invertible. Pure coordinate targets only
rescale, so all incidence ranks in (5) and the endpoint obstruction in
(10) persist on this torus. The checker audits every one of the `64*60`
identities (12) at a nontrivial rational torus point.

## 5. Remaining frontier

The displayed exact rank-55/R2 guard is excluded twice: already by linear
L0 incidence, and again after explicitly enforcing L1 and shared factored
endpoint-star compatibility. Its whole diagonal covariant family is also
excluded.

This is not a proof that every all-spokes packet fails. A future closure
only needs to study packets satisfying the exceptional incidence profile
(6), together with the nonlinear factored equations and the overlapping
L1 systems. Generic rank-55 members, including the committed sharp guard,
are no longer candidates.

## Exact audit

The standard-library checker:

- rebuilds and hashes the exact packet;
- rechecks generic kernel, selected rows, rank 55, and all R2 witnesses;
- verifies the universal 256 endpoint-slice identities;
- computes all five incidence ranks in (5) over three fields;
- row-reduces both complete L1 systems over `Q`;
- constructs all four L1-compatible factored tangent outputs and verifies
  (10) over three fields;
- audits the full diagonal covariance identity (12); and
- records the exact necessary survivor profile (6).

The SHA-256 digest of the exact 60-cell residual packet serialization is

```text
135afa073bda1bf11a4e423696c141138e116f0e19722b9787bed5b7df39d8b8
```

It uses no external CAS.
