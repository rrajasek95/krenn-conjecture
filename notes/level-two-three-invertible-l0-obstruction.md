# Binary L0 tangent incidence kills the displayed three-invertible guard

Research evidence only. Krenn's conjecture remains open,
**SP-CLEAN-BRIDGE** is untouched, and no certified dependency changes.

## 1. Exact outcome and scope

The integral residual packet in the
[three-invertible R2 guard](level-two-three-invertible-r2-guard.md) has no
completion to the full eight-vertex equation system. This is not a failure
of the particular zero values used in its R2 endpoint completion: the fixed
six-vertex binary packet $M$ alone is incompatible with the binary L0
target rows, no matter how every other ternary cell is chosen.

The argument gives a general necessary condition. For every endpoint pair
and binary colour pair in any full solution, both monochromatic six-bit basis
vectors must lie in the tangent image of the complementary six-site matching
tensor. At residual differential rank $55$, the restriction to the other
62 rows must consequently have rank exactly $53$.

This does **not** exclude the whole $3I+1R+2Z$ stratum. The eight
zero-multiplier residual blocks were free in the generic-kernel equation and
were assigned particular values in the displayed guard. Varying those blocks
changes the tangent image. What is proved is that this exact local guard
cannot be a partial global completion, and that any replacement must first
satisfy the tangent-incidence condition below.

## 2. Every binary endpoint slice lies in one tangent image

Let the residual sites be $R=\{0,\ldots,5\}$, let $p,q$ be two
endpoints, and restrict all residual colours to $a,b$. Write

\[
 H=\Psi(M)\in\mathbb C^{64},\qquad
 D=d\Psi_M:\mathbb C^{60}\longrightarrow\mathbb C^{64}.
\]

For fixed endpoint colours $s,t\in\{a,b\}$, put

\[
 U_r(i)=A_{pr}[s,i],\qquad V_r(i)=A_{qr}[t,i],\qquad
 W=A_{pq}[s,t].
\]

Partition the 105 perfect matchings on eight sites according to whether they
contain $pq$. The 15 containing $pq$ contribute $WH$. Each of the
other 90 matchings has $p$ matched to some $r$, $q$ matched to a
distinct $u$, and a matching on the remaining four residual sites.
Consequently the entire 64-coordinate L0 slice is

\[
 T_{s,t}=WH+D(N^{s,t}),                                      \tag{1}
\]

where, for $r<u$,

\[
 N^{s,t}_{ru}(i,j)=U_r(i)V_u(j)+V_r(i)U_u(j).                \tag{2}
\]

Formula (1) allows completely arbitrary endpoint blocks; no R2 zeros, star
ranks, or generic-kernel identities are used. Since the six-site matching
tensor is homogeneous of degree three, Euler's identity gives

\[
                         D(M)=3H.                            \tag{3}
\]

Thus, in characteristic zero,

\[
                         T_{s,t}\in\operatorname{im}D        \tag{4}
\]

for all four endpoint colour pairs.

## 3. A universal L0 rank screen

The full binary L0 equations require

\[
 T_{a,a}=e_{a^6},\qquad T_{b,b}=e_{b^6},\qquad
 T_{a,b}=T_{b,a}=0.                                         \tag{5}
\]

Combining (4) and (5) proves the universal incidence condition

\[
 \boxed{\quad e_{a^6},e_{b^6}\in\operatorname{im}d\Psi_M.\quad} \tag{6}
\]

Let $D_{\rm mix}$ be $D$ with the two monochromatic output rows deleted.
The kernel of the projection
$\operatorname{im}D\to\mathbb C^{62}$ is then exactly the plane spanned
by the two vectors in (6). Hence every full solution satisfies

\[
             \operatorname{rank}D_{\rm mix}
             =\operatorname{rank}D-2.                       \tag{7}
\]

The product-one vertex-rescaling torus gives the universal differential
rank cap $\operatorname{rank}D\le55$: it has five-dimensional orbits on a
dense open set, so every $56\times56$ minor vanishes identically. Therefore

\[
             \operatorname{rank}D_{\rm mix}\le53.           \tag{8}
\]

This is a necessary condition only. Equation (6) asks for arbitrary tangent
preimages, while a genuine endpoint completion must realize them in the
factored two-star form (2).

## 4. The rank screen is sharp

The bounds $55$ and $53$ in (7)--(8) occur simultaneously. The checker
constructs a second integral residual packet $M^\sharp$ with

\[
 \operatorname{rank}d\Psi_{M^\sharp}=55,\qquad
 \operatorname{rank}(d\Psi_{M^\sharp})_{\rm mix}=53.        \tag{9}
\]

The construction is transparent. On vertices $\{2,3,4,5\}$, two
rank-one matching products cancel and leave the four-site tensor
$e_{0^4}$. On vertices $\{0,1,2,3\}$, the analogous cancellation leaves
$e_{1^4}$. It follows literally that the differential column indexed by
the cell $(01,00)$ is $e_{0^6}$, while the column indexed by $(45,11)$
is $e_{1^6}$. Exact elimination proves (9) over $\mathbb Q$ and the two
audit primes.

Thus tangent incidence at maximal residual rank is nonempty. This sharpness
packet is only a guard for the linear screen: it is not claimed to realize
the four tangent directions simultaneously in the factored endpoint form
(2), nor to satisfy L1 or the ternary equations.

The first follow-up now settles that question for this packet:
[the factored L0 obstruction](level-two-l0-sharp-factor-obstruction.md)
proves that $M^\sharp$ has no simultaneous endpoint completion. A weakened
four-edge ideal is already the unit ideal over $\mathbb Q$, while an
[independent standard-library audit](level-two-l0-sharp-factor-obstruction-independent-audit.md)
verifies an explicit three-slice rational Nullstellensatz certificate.
This does not make (8) non-sharp: $M^\sharp$ still attains the exact linear
ranks $55/53$; it fails only at the stronger shared-factor stage.

## 5. The displayed guard fails the screen by two dimensions

For the displayed integral $M$, exact elimination gives the following
ranks. Each tuple records the rank over $\mathbb Q$, modulo $101$, and
modulo $1{,}000{,}003$:

\[
\begin{array}{c|c}
\text{matrix}&(\operatorname{rank}_{\mathbb Q},
\operatorname{rank}_{101},\operatorname{rank}_{1000003})\\ \hline
D&(55,55,55)\\
D_{\rm mix}&(55,55,55)\\
[D\mid e_{a^6}]&(56,56,56)\\
[D\mid e_{b^6}]&(56,56,56)\\
[D\mid e_{a^6}\mid e_{b^6}]&(57,57,57).
\end{array}                                                  \tag{10}
\]

Thus both pure target vectors miss $\operatorname{im}D$, their cokernel
classes are independent, and the mixed restriction has rank 55 rather than
the required 53. Equations (4) and (5) contradict (10). This contradiction
precedes L1 and overlapping L2.

Equivalently, every future choice of the eight zero-multiplier blocks that
could occur in a full solution must lie on the exact incidence locus

\[
 \operatorname{rank}[D\mid e_{a^6}\mid e_{b^6}]
 =\operatorname{rank}D.                                    \tag{11}
\]

The displayed guard lies two cokernel dimensions away from this locus.

## 6. Fixed cells and machine audit

The minimal selected-block guard fixes 85 of the 252 ternary edge cells:

* 60 binary residual cells comprising $M$, including the 32 cells on the
  zero-multiplier cut $\{0,1,2,3\}\mid\{4,5\}$;
* 24 selected endpoint-star cells; and
* the direct cell $A_{pq}[c,c]=-1$.

It leaves 167 cells free. If the optional binary endpoint blocks used in the
literal R2 completion are also counted, 133 cells are fixed and 119 are
free. The obstruction uses only $M$, so either interpretation is covered.

[verify_level_two_three_invertible_l0_obstruction.py](../computations/verify_level_two_three_invertible_l0_obstruction.py)
checks exactly:

* the $15+90$ matching partition and its two-star parametrization;
* formula (1) as a formal endpoint-monomial identity on all $4\cdot64=256$
  binary slices;
* Euler identity (3);
* all five obstruction rank triples in (10), the sharp $55/53$ rank pair,
  and the two literal pure columns of $d\Psi_{M^\sharp}$; and
* the two fixed/free cell counts.

The checker is standard-library only, raises explicitly, and remains live
under normal, optimized, and isolated Python. The local R2 guard retains its
original logical force: selected-block equations plus residual R2 do not
exclude its pattern. It is now known not to survive the first global L0
screen. The live $3I+1R+2Z$ problem is to classify or exclude
zero-multiplier spoke choices satisfying (11), then impose the factorization
(2) and the L1/overlapping-L2 rows.
