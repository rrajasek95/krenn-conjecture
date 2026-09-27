# Higher output constraints restore four-site W local optimality

September 27, 2026. **Written proof with exact supporting checks; independent
audit pending.** This proves the exceptional four-site case of the
[all-even local theorem](w-state-all-even-local-optimum-2026-09-27.md).

[Replay](../computations/w-all-even-local-optimum-2026-09-27/README.md).

## 1. Why a second-variation test alone is insufficient

Use the rational coordinates of the all-even theorem at $N=3$.
The base has three core ground entries one, root $ab$ entries three,
and root $ba$ entries one. Its physical rate is $1/10$.

The full linear output kernel has complex dimension ten.
Its second-variation formulas have $\kappa_3=-4/3$, so the
Lagrangian is genuinely indefinite on that linear space.

For example, let the core mixed-entry row sums be
$(s_1,s_2,s_3)=(1,\omega,\omega^2)$, put

$$
U_{ij}=(2s_i+s_j)/3,\quad
\zeta_i=-3\overline{s_i},\quad V_i=-s_i,
$$

and set the other tangent coordinates to zero.
This lies in $\ker J$ and its real Lagrangian quadratic value is $-4$.
It is not a proof of a better exact W design: the linear kernel can
contain directions that no feasible curve follows.

## 2. Two polynomial identities in the tangent coordinates

For a general binary tangent at this base, $\sum_i s_i=0$ and

$$
U_{ij}=(2s_i+s_j)/3+K_{ij},
$$

where $K$ is antisymmetric with zero row sums.
On three sites, $K$ has the form
$K_{12}=K_{23}=K_{31}=\tau$, with reversed entries negated.

For each pair $i,j$ and the remaining core site $k$, put

$$
P_{ij}=s_iU_{jk}+s_jU_{ik}.
$$

Direct expansion gives the exact identities

$$
\boxed{\sum_{i<j}P_{ij}=-\sum_i s_i^2,\qquad
\sum_i s_iP_{jk}=3s_1s_2s_3.}
\tag{1}
$$

The cyclic $K$ terms cancel in both sums. For example,
$P_{ij}=4s_is_j/3-s_k^2/3+s_iK_{jk}+s_jK_{ik}$;
use $\sum_i s_i=0$ and $\sum_i s_i^3=3s_1s_2s_3$.
These are complex polynomial identities, not identities of squared norms.

## 3. Apply the exact higher-excitation equations to nearby feasible points

Let $z=z_*+\delta z$ have exactly the same W output as the base, and
write $\rho=\|\delta z\|$. Take the $G$-orthogonal tangent projection
$T\in V$ of $\delta z$.
Since $J\delta z=O(\rho^2)$, we have

$$
\delta z=T+O(\rho^2).
$$

Use $s,U$ for the tangent coordinates of $T$. All are $O(\rho)$.
Let $\widehat Y_{ij}$ be the actual core $bb$ entries of $z$;
their tangent values are zero, so $\widehat Y=O(\rho^2)$.
The actual root mixed entries are
$\widehat x_i=3+O(\rho)$ and $\widehat y_i=1+O(\rho)$;
the actual root $bb$ entries satisfy $\widehat V_i=-s_i+O(\rho^2)$.

The output exciting the root and core sites $i,j$, while grounding $k$,
is exactly

$$
0=\widehat y_k\widehat Y_{ij}
+\widehat V_i\widehat U_{jk}
+\widehat V_j\widehat U_{ik}.
$$

Therefore

$$
\widehat Y_{ij}=P_{ij}+O(\rho^3).
\tag{2}
$$

The output exciting all three core sites, with the root grounded, is
$0=\sum_i\widehat x_i\widehat Y_{jk}$.
Thus $\sum_{i<j}\widehat Y_{ij}=O(\rho^3)$.
Combining this with (1)–(2) gives

$$
\sum_i s_i^2=O(\rho^3).
\tag{3}
$$

The all-excited output is exactly
$0=\sum_i\widehat V_i\widehat Y_{jk}$.
Using (1)–(2), including their error orders, gives

$$
s_1s_2s_3=O(\rho^4).
\tag{4}
$$

No source jets have been set to zero in this argument. It holds for
every sufficiently close feasible source.

## 4. The dangerous row-sum modes are smaller than first order

Since $\sum_i s_i=0$, each $s_i$ satisfies

$$
s_i^3-\tfrac12\left(\sum_j s_j^2\right)s_i-s_1s_2s_3=0.
$$

Together with $s_i=O(\rho)$, (3)–(4) imply

$$
\boxed{s_i=O(\rho^{4/3}),\qquad \|s\|^2=O(\rho^{8/3}).}
\tag{5}
$$

This estimates complex absolute values. Although (3) alone permits
nonzero isotropic vectors such as $(1,\omega,\omega^2)$, adding the
cubic condition forces every limiting first-order row-sum vector to zero.

On the phase-fixed tangent space with $s=0$, the all-even
second-variation formulas are positive definite: the $h$ space is
absent, the core terms are positive modulo the three site phases,
and the other terms are $\|\zeta\|^2+10\|K_0\|_F^2$.
Finite-dimensional quadratic-form estimates therefore give constants
$c,C>0$ such that on the full phase-fixed tangent space,

$$
Q_R+Q_I\ge c\|T\|^2-C\|s\|^2.
$$

For instance, decompose into the subspace $s=0$ and a fixed complement,
and absorb their cross terms by the positive quadratic form on the
first subspace. Equation (5) controls the complement for feasible
points.

The fixed-output Lagrangian now yields

$$
S(z)-S(z_*)\ge c'\rho^2-O(\rho^{8/3})-O(\rho^3)>0
$$

for every sufficiently small nonzero phase-fixed feasible displacement.
This proves strict local optimality modulo phases at four sites.
Amplitude normalization and projection away from additional colors
work as in the all-even theorem.

## 5. An exact rejected extension

The negative direction from section 1 can be extended so that every
second-order output error cancels: choose the second core $bb$ jet
from (2), and adjust the root $ab$ entries to remove the second-order
W coefficients. Here $\sum_i s_i^2=0$.

Nevertheless its all-excited coefficient at third order is
$-3s_1s_2s_3=-3$. It cannot be changed by a third source jet,
because the corresponding row of the base Jacobian is zero.
The second core $bb$ jet was already fixed by the triple outputs;
adding a second-jet tangent vector does not change it.

The replay verifies this full complex jet fixture and checks both
polynomial identities (1) coefficient by coefficient.
The result illustrates a general optimization issue at singular
constraints: an indefinite Lagrangian on the linearized kernel need
not give an improving feasible direction. Higher equations can remove
the dangerous modes.
