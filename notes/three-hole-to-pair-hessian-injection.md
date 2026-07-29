# Three-hole excess injects into pair-Hessian excess

## 1. Outcome

The exceptional branch in the fixed-star three-hole dichotomy is not
independent of the source-Hessian branch.  Let `J` have odd size
`2m-1`, fix a site `j`, and put `W=J\{j}`.  If the rank-three graph of
the quadratic restricted to `W` is connected and nonbipartite, contraction
of the barred `j` slot gives a canonical injection

\[
 \boxed{
 {\ker\Psi_{j,r}\over\operatorname {im}\mathcal G_{j,r}}
 \hookrightarrow
 \operatorname {Hom}\!\left(
    \bar V_j^*,{\ker\mathcal H_{q_W}\over\mathcal G_{q_W}}
                         \right).}                       \tag{1}
\]

Here `Psi_(j,r)` and its expansion gauges are those of
[`fixed-star-three-hole-gauge-dichotomy.md`](fixed-star-three-hole-gauge-dichotomy.md),
while `H_(q_W)` and `G_(q_W)` are the two-deletion Hessian and its
vertex-expansion gauges.  Consequently

\[
 \dim\ker\Psi_{j,r}-\dim\operatorname {im}\mathcal G_{j,r}
 \le 2\dim(\ker\mathcal H_{q_W}/\mathcal G_{q_W}).        \tag{2}
\]

In particular, pair-Hessian gauge rigidity forces three-hole gauge
rigidity.  Conversely, every genuine extra `Psi` direction forces a
genuine extra Hessian direction after some contraction of the quotient
slot.  This retains the actual common powers; it is false for unrelated
one-hole and three-hole tensors.

## 2. The two maps and their normalizations

Work in the site-square-zero algebra on

\[
                         J=W\mathbin{\dot\cup}\{j\},
 \qquad |W|=2m-2=2s,
 \qquad s=m-1.                                           \tag{3}
\]

Let `q_W` be the quadratic internal to `W`.  The one-hole and three-hole
common cofactors are

\[
 C_j={q_W^s\over s!},\qquad
 D_{ijk}={q_{W\setminus\{i,k\}}^{s-1}\over(s-1)!}
 \quad(i,k\in W).                                       \tag{4}
\]

Fix a color `r`, put `bar V_j=V_j/Ce_r`, and recall

\[
 \Psi_{j,r}\bigl(u,(T_{ik})\bigr)
  =u^{(j)}\otimes C_j+
    \sum_{i<k}T_{ik}^{(i,j,k)}\otimes D_{ijk}.            \tag{5}
\]

The expansion gauge associated with vectors `w_i in bar V_j` is

\[
 \mathcal G_{j,r}(w)=
 \left(\sum_iw_i,
       \bigl(-(w_i+w_k)^{(j)}\otimes(q_W)_{ik}\bigr)_{i<k}
                                                        \right).     \tag{6}
\]

On the even set `W`, use the factorial-normalized Hessian

\[
 \mathcal H_{q_W}(Z)={Zq_W^{s-1}\over(s-1)!}.
                                                               \tag{7}
\]

For scalars `beta_i` with `sum_i beta_i=0`, its vertex gauge is

\[
 (Z^\beta)_{ik}=(\beta_i+\beta_k)(q_W)_{ik}.             \tag{8}
\]

Notice the exact Euler normalization

\[
                         \mathcal H_{q_W}(q_W)=sC_j.     \tag{9}
\]

## 3. Slot contraction produces a Hessian kernel

Let

\[
                         v=(u,(T_{ik}))\in\ker\Psi_{j,r}
\]

and take `phi in bar V_j^*`.  Contract the barred `j` factor and define

\[
 a_\phi=\phi(u),\qquad
 (Z_\phi)_{ik}=(\operatorname{id}\otimes\phi\otimes
                    \operatorname{id})(T_{ik}).          \tag{10}
\]

Contracting (5) gives

\[
                         a_\phi C_j+\mathcal H_{q_W}(Z_\phi)=0.
                                                               \tag{11}
\]

By (9),

\[
 K_\phi:=Z_\phi+{a_\phi\over s}q_W
                         \in\ker\mathcal H_{q_W}.        \tag{12}
\]

The assignment is linear in `phi`, so (12) defines a linear map

\[
 \Theta(v):\bar V_j^*\longrightarrow
          \ker\mathcal H_{q_W}/\mathcal G_{q_W},
 \qquad \phi\longmapsto[K_\phi].                        \tag{13}
\]

It kills every expansion gauge.  Indeed, for (6) put

\[
 \alpha_i=\phi(w_i),\qquad a=\sum_i\alpha_i.
\]

Then the `ik` block of (12) is

\[
 \left(-\alpha_i-\alpha_k+{a\over s}\right)(q_W)_{ik}
       =(\beta_i+\beta_k)(q_W)_{ik},                     \tag{14}
\]

where

\[
                         \beta_i=-\alpha_i+{a\over2s}.
\]

Because `|W|=2s`, the `beta_i` sum to zero.  Thus (14) is precisely the
Hessian gauge (8), and `Theta` descends to the quotient in (1).

## 4. Injectivity after quotienting the gauges

Assume now that `G_3(q_W)` is connected and nonbipartite.  Then the gauge
parameterization (8) is injective: if

\[
                         (\beta_i+\beta_k)(q_W)_{ik}=0
\]

on every rank-three edge, connectedness makes the `beta_i` alternate and
an odd cycle makes them all zero.

Suppose `Theta(v)=0`.  For every `phi`, there is therefore a **unique**
zero-sum tuple `beta(phi)` such that

\[
 K_\phi=Z^{\beta(\phi)}.                                 \tag{15}
\]

Uniqueness and linearity of `K_phi` imply that every `beta_i(phi)` is a
linear functional of `phi`.  Since `bar V_j` is finite-dimensional, there
are unique vectors `b_i in bar V_j` with

\[
                         \beta_i(\phi)=\phi(b_i),
 \qquad                         \sum_i b_i=0.             \tag{16}
\]

Comparing the `ik` blocks in (12) and (15), for every `phi`, gives

\[
 \phi\!\left(T_{ik}+{1\over s}u^{(j)}\otimes(q_W)_{ik}
       -(b_i+b_k)^{(j)}\otimes(q_W)_{ik}\right)=0.
\]

The covectors `phi` separate `bar V_j`, hence

\[
 T_{ik}=\left(b_i+b_k-{u\over s}\right)^{(j)}
                                      \otimes(q_W)_{ik}. \tag{17}
\]

Set

\[
                         w_i=-b_i+{u\over2s}.             \tag{18}
\]

Equations (16) and `|W|=2s` give `sum_iw_i=u`, while (17) becomes

\[
                         T_{ik}=-(w_i+w_k)^{(j)}
                                      \otimes(q_W)_{ik}. \tag{19}
\]

Equations (18)--(19) say exactly that `v=G_(j,r)(w)`.  Thus the kernel of
the descended map is zero, proving (1).  Since `dim bar V_j=2`, (2)
follows immediately.

## 5. Consequences for a hypothetical full source

Let a fixed full-source star have odd internal set `J`, and let `j in J`.
The quadratic `q_W` above is exactly the source obtained after deleting
the star center `p` and `j`.  In fact, on the distinguished `Psi`-kernel
vector furnished by a full row equation, the injection has a particularly
concrete meaning.

Write `p_r` for the color-`r` row from `p` to `W`, and for
`phi in bar V_j^*` write

\[
 s_\phi=\sum_{i\in W}(\phi\otimes\operatorname{id})q_{ji},
 \qquad a_{r,\phi}=\phi(z_{j,r}).                         \tag{20}
\]

Contracting the tensor in equation (7) of the fixed-star note gives,
block by block,

\[
                         Z_\phi=p_rs_\phi.               \tag{21}
\]

Consequently (12) is exactly the off-diagonal two-deletion kernel vector

\[
                         K_{r,\phi}
       =p_rs_\phi+{a_{r,\phi}\over s}q_W.                \tag{22}
\]

For the coordinate covector `phi=e_d^*`, `d!=r`, this is the usual
`K_rd` from the nine pair equations.  The restriction `phi(e_r)=0` is
precisely why its target right side vanishes.  Thus the three row-derived
`Psi` classes package the six distinguished off-diagonal pair-Hessian
classes, two at a time; the bridge (1) is not merely an abstract map
between unrelated kernels.

Therefore:

* if that two-deletion Hessian is gauge-rigid and its rank-three graph is
  connected and nonbipartite, then every `Psi_(j,r)` is gauge-rigid;
* if a fixed-star row falls into the extra-`Psi` branch while the graph
  condition holds, some two-deletion Hessian has excess corank at least
  one;
* by the dense-pair propagation theorem in
  [`extra-hessian-corank-two-propagation.md`](extra-hessian-corank-two-propagation.md),
  the latter excess jumps to at least two whenever the corresponding two
  deleted stars satisfy its row-support hypotheses.

Thus the two apparent determinantal escapes form one hierarchy.  What
remains is the higher-corank/low-rank-component locus, not an unrelated
three-hole singularity.

## 6. Exact audit

[`verify_three_hole_hessian_injection.py`](../computations/verify_three_hole_hessian_injection.py)
checks the factorial identity (9), contracts random exact `Psi` gauges on
`|W|=4,6,8`, verifies (14), and reconstructs (18)--(19) from random
vector-valued zero-sum Hessian gauges over the rationals.  The verifier is
an audit of the tensor and normalization bookkeeping; injectivity for all
orders is the linear argument in Section 4.
