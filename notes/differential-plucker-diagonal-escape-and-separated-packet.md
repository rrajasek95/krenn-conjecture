# Differential Plücker closure kills the separated defect-three packet

## 1. Outcome

The Plücker--Hessian identities have a useful blockwise consequence which
does not require choosing target coordinates.  For a site pair `ij`, put

\[
 \ell_{ij}(\alpha)=\alpha_i+\alpha_j,
 \qquad h_{ij}(\alpha)=\sigma(\alpha)-\ell_{ij}(\alpha),
 \qquad \sigma(\alpha)=\sum_k\alpha_k.                 \tag{1}
\]

If the diagonal product `p_b s_b` is not proportional to `q` on that
block, then `h_ij` annihilates both reverse E2 primitives whose colours
avoid `b`.  Thus, when those primitives are independent, diagonal escape
is confined to a codimension-two defect condition.  The dependent
boundary includes the coincident-reverse packet treated below.

This closes the most natural coincident-reverse residual.  Suppose the
three colours occupy disjoint shores `P_0,P_1,P_2`, with `p_c=s_c`
supported on `P_c`, and the three unordered off-diagonal responses give
the three independent defect directions.  Differential Plücker closure
then forces

\[
 |P_c|-|M_c|=-2\qquad(c=0,1,2),                       \tag{2}
\]

where `P_c \sqcup M_c` is the corresponding bipartite rank-three
component.  Every `M_c` vertex can be joined by a nonzero `q` block only
to `P_c`.  Hence no supported perfect matching exists.  In particular,
this packet is impossible on a gauge-rigid chart.

An exact 24-site model shows sharpness: all six rows reach three sites,
the six responses span defect three, every differential Plücker
annihilator is already a response, and the response planes do not
propagate.  It fails the activity required by gauge rigidity through the
forced Hall deficit (2); no gauge-rigidity claim is made for the model.
Consequently the remaining gauge-rigid classification may assume genuine
overlap of the physical rows or a two-dimensional reverse-response plane;
the fully separated reciprocal-line packet is gone.

## 2. The diagonal-escape lemma

Let `W` be an even site set, let `q` be a quadratic, and let
`D \subseteq C^W`.  Write

\[
 \Gamma_q(\alpha)_{ij}=\ell_{ij}(\alpha)q_{ij},
 \qquad K_\alpha(R)_{ij}=h_{ij}(\alpha)R_{ij}.          \tag{3}
\]

Assume the six off-diagonal physical products have primitives in `D`,

\[
 Z_{cd}=p_cs_d=\Gamma_q(\alpha_{cd}),\qquad
 \alpha_{cd}\in D\quad(c\ne d),                       \tag{4}
\]

and that, for pairwise distinct `a,b,d`, the two differential Plücker
tensors

\[
\begin{aligned}
 K_{\alpha_{ab}}(Z_{bd})-K_{\alpha_{ad}}(Z_{bb}),\\
 K_{\alpha_{ab}}(Z_{dd})-K_{\alpha_{ad}}(Z_{db})
\end{aligned}                                         \tag{5}
\]

belong to `Gamma_q(D)`.  This is exactly the closure supplied by gauge
rigidity in
[`plucker-hessian-closure-and-defect-three-transition-guard.md`](plucker-hessian-closure-and-defect-three-transition-guard.md).
For a block, use the convention `C q_ij={0}` when `q_ij=0`.

**Lemma 2.1 (diagonal escape).**  Let `{a,d}` be the two colours other
than `b`, and set

\[
 R_b=\operatorname{span}\{\alpha_{ad},\alpha_{da}\}\subseteq D.
                                                               \tag{6}
\]

For every site pair `ij`,

\[
 (Z_{bb})_{ij}\notin\mathbb Cq_{ij}
       \quad\Longrightarrow\quad h_{ij}|_{R_b}=0.      \tag{7}
\]

**Proof.**  Reduce the first line of (5) modulo `C q_ij`.  Its first
term and its right-hand side vanish in the quotient, because both are
blockwise proportional to `q_ij`.  What remains is

\[
 h_{ij}(\alpha_{ad})[(Z_{bb})_{ij}]=0.                 \tag{8}
\]

Use (5) again with the ordered triple `(d,b,a)` to obtain the same
identity with `alpha_da`.  A nonzero quotient class gives (7).  \(\square\)

Two immediate consequences record exactly where closure can still be
blind.

* If two diagonals `b,c` escape on the same block and
  `R_b+R_c=D`, then `h_ij=0` on `D`.
* If all three diagonals escape there and the six primitives span `D`,
  then again `h_ij=0` on `D`.

The latter equality is the complement-sum identity

\[
             \sum_{k\in W\setminus\{i,j\}}\alpha_k=0
                         \qquad(\alpha\in D).           \tag{9}
\]

At such a block every first-order operator `K_alpha` vanishes.  This is
the exact residual, rather than an unspecified failure of plane
propagation.

## 3. The separated reciprocal packet is inactive

We now treat the coincident-reverse boundary without graph subcases.
Assume the rank-three graph has three bipartite components

\[
                  C_c=P_c\sqcup M_c\qquad(c=0,1,2),    \tag{10}
\]

whose shore-sign vectors `zeta^c` form a basis of `D`; allow in addition
vertices on which every vector of `D` is zero.  Put

\[
 \Delta_c=|P_c|-|M_c|,\qquad
 \alpha=\sum_ct_c\zeta^c.                             \tag{11}
\]

Assume `p_c=s_c=x_c`, where `x_c` is nonzero exactly on `P_c` and
`|P_c|>=2`.  Assume also that the three unordered products `x_cx_d` are
independent and span `Gamma_q(D)`.  Since `dim D=3`, this makes
`Gamma_q|_D` injective, so the two orientations use the same primitive.

**Theorem 3.1 (imbalance obstruction).**  If (5) holds, then
`Delta_0=Delta_1=Delta_2=-2`.  Neither `q` nor any restriction obtained
by deleting two sites has a supported perfect matching.

**Proof.**  On a pair in `P_c x P_d`, the product `x_cx_d` is nonzero,
so its response identity first implies `q_ij!=0`.  Every other unordered
product vanishes on that block.  Consequently `L_cd` kills the primitives
of the other two products, whereas it does not kill the primitive of
`x_cx_d`.  Thus the three
evaluation functionals

\[
       L_{01}(t)=t_0+t_1,quad L_{02}(t)=t_0+t_2,quad
       L_{12}(t)=t_1+t_2                              \tag{12}
\]

must distinguish the three independent products.  They are independent,
so, up to a nonzero scalar, the primitive of `x_ax_d` has coefficient
vector

\[
 (t_a,t_d,t_b)=\left(\frac12,\frac12,-\frac12\right), \tag{13}
\]

where `b` is the omitted colour.

Choose two sites in `P_b`.  Every off-diagonal product vanishes on that
block.  Since their primitives span `D` and `2t_b` is a nonzero
functional, (4) forces `q_ij=0`.  The diagonal block of `x_b^2` is
nonzero, so Lemma 2.1 and (13) give

\[
 0=h_{ij}(\alpha_{ad})
   ={1\over2}(\Delta_a+\Delta_d-\Delta_b)+1.           \tag{14}
\]

Doing this for all three omitted colours yields

\[
 \Delta_1+\Delta_2-\Delta_0=
 \Delta_0+\Delta_2-\Delta_1=
 \Delta_0+\Delta_1-\Delta_2=-2,                      \tag{15}
\]

whose unique solution is (2).

Finally, all off-diagonal products vanish at every pair incident with
`M_c`.  Their primitives span `D`, so (4) permits a nonzero `q` block
there only when every defect evaluation vanishes.  Among such pairs, the
only ones incident with `M_c` are `M_c x P_c`.  A supported perfect
matching would therefore have to match all `|M_c|=|P_c|+2` vertices of
`M_c` injectively into `P_c`, which is impossible.  More strongly, for
every two-site set `E`, at least one of the three strict inequalities

\[
                    |M_c\setminus E|>|P_c\setminus E|
\]

remains.  Deleting an `M_c` vertex reduces its shore deficit by one,
deleting a `P_c` vertex increases it by one, and the three initial
deficits are all two.  Thus the same Hall obstruction survives every
two-site deletion.  \(\square\)

Gauge rigidity implies every pair complement is active and therefore
excludes this persistent Hall deficit.  The theorem removes the exact
separated model that previously witnessed failure of plane propagation;
what remains is an overlapping or reverse-plane-rank-two problem.

## 4. Exact sharpness model

Take `|P_c|=3`, `|M_c|=5`, put `x_c=e_c` on `P_c` and zero elsewhere,
and define

\[
 q_{ij}=I_3\quad(i\in P_c,j\in M_c),\qquad
 q_{ij}=e_c\otimes e_d\quad(i\in P_c,j\in P_d,c<d),  \tag{16}
\]

with all other blocks zero.  Let `zeta^c` be `+1` on `P_c`, `-1` on
`M_c`, and zero elsewhere, and use

\[
 \alpha^{01}=(\zeta^0+\zeta^1-\zeta^2)/2,
 \quad\alpha^{02}=(\zeta^0-\zeta^1+\zeta^2)/2,
 \quad\alpha^{12}=(-\zeta^0+\zeta^1+\zeta^2)/2.       \tag{17}
\]

Then `sigma(alpha^cd)=-1` and

\[
 x_cx_d=\Gamma_q(\alpha^{cd}).                        \tag{18}
\]

For distinct `a,b,d`, direct block multiplication gives

\[
\begin{aligned}
 K_{\alpha^{ab}}(x_bx_d)-K_{\alpha^{ad}}(x_b^2)
     &=-x_bx_d,\\
 K_{\alpha^{ab}}(x_d^2)-K_{\alpha^{ad}}(x_dx_b)
     &= x_dx_b.                                       \tag{19}
\end{aligned}

Thus all six differential closures lie in the response space.  Yet the
planes from `x_0x_1` are zero on `P_2`, so they miss `x_0x_2`; and Hall's
inequality forbids a perfect matching.  The lightweight exact checker
[`verify_differential_plucker_diagonal_escape_and_separated_packet.py`](../computations/verify_differential_plucker_diagonal_escape_and_separated_packet.py)
audits (16)--(19), defect rank, row support, missed planes, and the Hall
deficit.
