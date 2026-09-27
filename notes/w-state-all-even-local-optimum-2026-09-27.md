# Unrestricted local W optimality at every even site count

September 27, 2026. **Written proof with exact supporting checks; independent
audit pending.** This is a local theorem. Global unrestricted W optimality
remains open.

[Replay](../computations/w-all-even-local-optimum-2026-09-27/README.md) ·
[Exceptional four-site argument](w-state-four-site-local-obstruction-2026-09-27.md) ·
[Earlier six-site certificate](w-state-unrestricted-local-optimum-2026-09-26.md)

## 1. The theorem

Let $n=2m\ge4$, $N=n-1$, and $g=N^2+1$. Label the root $0$ and the
core sites $1,\ldots,N$. Define $A_*$ by

$$
(A_*)_{ij}(a,a)=\sqrt g\quad(1\le i<j\le N),\qquad
(A_*)_{0i}(a,b)=N,\qquad (A_*)_{0i}(b,a)=1,
$$

with all other entries zero. Then

$$
H(A_*)=\Lambda W_n,\qquad
\Lambda=g^{(m-1)/2}N!!,\qquad S_*:=S(A_*)=gNm,
$$

and its rate is

$$
R_*=\frac{n(N!!)^2}{(N^2+1)(Nm)^m}
=\frac{nB_n}{(n-1)^2+1}.
$$

**Theorem.** In a neighborhood of $A_*$, every complex colored source
with exact nonzero output proportional to $W_n$ satisfies $R\le R_*$.
All source cells and any finite palette are allowed.

After fixing the output amplitude to $\Lambda$, equality holds precisely
on the local site-phase orbit

$$
A_{ij}(h,k)\longmapsto e^{i(\theta_i+\theta_j)}A_{ij}(h,k),
\qquad \sum_{i=0}^N\theta_i=0.
$$

More quantitatively, there are a neighborhood and $c_n>0$ such that,
for exact output $\Lambda W_n$,

$$
S(A)-S_*\ge c_n\operatorname{dist}(A,\mathcal O_*)^2,
\tag{1}
$$

where $\mathcal O_*$ is that phase orbit. With output amplitude free,
overall nonzero complex scaling is an additional equality symmetry.
No numerical radius or uniform-in-$n$ constant is asserted.

The proof below gives explicit positive second-variation formulas for
every even $n\ge6$. Four sites require the higher output constraints
proved in the linked companion note.

## 2. Rational coordinates and stationarity

Rescale every core cell, including initially zero cells, by writing
$A_{ij}(h,k)=\sqrt g\,z_{ij}(h,k)$ for $i,j>0$.
Keep root cells unchanged. Each matching has exactly $m-1$ core edges,
so

$$
H(A)=g^{(m-1)/2}H(z),\qquad S(A)=z^*Gz,
$$

where $G$ is diagonal with weight $g$ on core cells and weight one on
root cells. The base $z_*$ has core ground entries one and root mixed
entries $N,1$.

Put $c=(N-2)!!$. A Lagrange multiplier $y$ on output words has value
$N/c$ for an excitation at a core site and $1/c$ for an excitation
at the root; it is zero on all other words. Counting complementary
matchings gives

$$
J^{\mathsf T}y=Gz_*,\qquad J=DH(z_*).
\tag{2}
$$

For a root mixed cell, the derivative is $c$, proving its component
of (2). For a core ground edge, its derivatives in the weighted W
outputs sum to $N^2+1=g$. Every other cell contributes only to output
sectors on which $y=0$, and its base value is zero.

Define

$$
B=\sum_w y_wD^2H_w(z_*),\qquad V=\ker J.
$$

For a complex tangent displacement $u+iv$ with real $u,v\in V$, the
quadratic norm Lagrangian is

$$
Q_R(u)+Q_I(v),\qquad
Q_R=G-B,\quad Q_I=G+B.
\tag{3}
$$

This corresponds to the Lagrangian
$z^*Gz-2\operatorname{Re}\sum_w y_wH_w(z)$.

## 3. Describe the whole binary tangent space

Use the following names for a tangent displacement:

| Cells | Coordinates |
| --- | --- |
| Core ground entries | $d_{ij}=d_{ji}$ |
| Root ground entries | $\zeta_i$ |
| Root $ab$ and $ba$ entries | $x_i,y_i$ |
| Core entry exciting $i$ and grounding $j$ | $U_{ij}$ |
| Root $bb$ entries | $V_i$ |
| Core $bb$ entries | $Y_{ij}$ |

Let $D=\sum_{i<j}d_{ij}$, $t_i=\sum_{j\ne i}d_{ij}$,
$a_i=D-t_i$, and $s_i=\sum_{j\ne i}U_{ij}$.
Separating the derivative by the number and position of excitations gives
exactly these equations:

$$
\sum_i\zeta_i=0,\qquad
x_i=-\frac{N}{N-2}a_i,\qquad
\sum_i y_i=-D,
\tag{4}
$$

$$
U_{ij}+U_{ji}=s_i+s_j,\qquad V_i=-s_i,\qquad Y_{ij}=0.
\tag{5}
$$

For example, the derivative in a core excitation pair $i,j$ is
$N(N-4)!!(s_i+s_j-U_{ij}-U_{ji})$.
In the root-and-core pair $0,i$ it is $c(s_i+V_i)$.
In the triple $0,i,j$ it is $cY_{ij}$, which forces $Y=0$;
the other triple equations then vanish too. No higher-excitation word
can occur in the derivative.

Summing (5) gives

$$
\sum_i s_i=0,\qquad \sum_{j\ne i}U_{ji}=(N-3)s_i.
\tag{6}
$$

The free variables consist of $d$, a zero-sum part of $y$, the
zero-sum vector $\zeta$, and an arbitrary antisymmetric part of $U$.
Indeed, if $K_{ij}=(U_{ij}-U_{ji})/2$, then
$\sum_jK_{ij}=(4-N)s_i/2$ determines $s$ from $K$ since $N$ is odd.
Consequently

$$
\dim_{\mathbb C}V=N(N+1)-2,\qquad
\operatorname{rank}J=N(N+1)+2.
\tag{7}
$$

These are statements about all $2N(N+1)$ binary source coordinates.

## 4. Split the core and mixed-entry coordinates

Decompose the symmetric core perturbation as

$$
d_{ij}=\alpha+u_i+u_j+h_{ij},\qquad
\sum_i u_i=0,\quad \sum_{j\ne i}h_{ij}=0.
\tag{8}
$$

Explicitly $\alpha=2D/[N(N-1)]$ and
$u_i=[t_i-(N-1)\alpha]/(N-2)$.
Write $y_i=-(N-1)\alpha/2+v_i$ with $\sum_i v_i=0$.
Then $x_i=N[u_i-(N-1)\alpha/2]$.

The three summands in (8) are orthogonal for the edge norm, and

$$
\|d\|^2=\binom N2\alpha^2+(N-2)\|u\|^2+\|h\|^2
$$

for real tangent coordinates. The $h$ space has dimension
$N(N-3)/2$; at $N=3$ it is zero.

Similarly, decompose the antisymmetric part of $U$ as

$$
K_{ij}=\frac{4-N}{2N}(s_i-s_j)+(K_0)_{ij},
\qquad K_0^{\mathsf T}=-K_0,\quad \sum_j(K_0)_{ij}=0.
$$

The symmetric and antisymmetric parts are orthogonal, as are the two
displayed parts of $K$. Therefore

$$
\|U\|_F^2=\left(N-5+\frac8N\right)\|s\|^2+\|K_0\|_F^2.
\tag{9}
$$

The norms of $U,K_0$ count ordered pairs; the norms of $d,h$ count
unordered edges. This distinction accounts for the factors in (9).

## 5. Universal sums of squares

Put

$$
A_N=N^2(N-1)+N-2,\qquad
\kappa_N=(N^2+1)\left(N-5+\frac8N\right)-(N^2-1).
$$

On the real tangent coordinates from (8)–(9), the exact forms are

$$
\begin{aligned}
Q_R={}&
\frac{gN(N^2-1)}2\,\alpha^2
+\|u+v\|^2+(2A_N-2)\|u\|^2
+\frac{g(N-3)}{N-2}\|h\|^2\\
&+\|\zeta+Ns\|^2+\kappa_N\|s\|^2+g\|K_0\|_F^2,
\end{aligned}
\tag{10}
$$

$$
Q_I=
\|u-v\|^2+\frac{g(N-1)}{N-2}\|h\|^2
+\|\zeta-Ns\|^2+\kappa_N\|s\|^2+g\|K_0\|_F^2.
\tag{11}
$$

Here (10) applies to the real part of a complex displacement, and
(11) to its imaginary part.

For completeness, these formulas can be obtained without diagonalizing
a size-dependent matrix. The nonzero Hessian blocks are:

- Between disjoint core ground edges: $g/(N-2)$.
- Between a core ground edge and $x_i$, when $i$ is outside that edge:
  $N/(N-2)$; the analogous entry for $y_i$ is $1/(N-2)$.
- Between $\zeta_i$ and $U_{jk}$ with $i\notin\{j,k\}$:
  $N/(N-2)$.

These follow by counting the matchings left after the two varied edges.
All other Hessian entries are zero because the multiplier sees only
single-excitation outputs.

The disjoint-edge adjacency operator on $d$ acts by
$\binom{N-2}{2}$ on the constant part, by $-(N-3)$ on the $u$ part,
and by $1$ on $h$. These identities follow by summing over edges
disjoint from a fixed pair, using the zero-sum and zero-row conditions.
For $N=3$, the $h$ space is absent. Substitution into the listed Hessian
blocks gives (10)–(11). In the second group, the Hessian cross term is
$-2N\sum_i\zeta_i s_i$ by (6); completing its square and using (9)
gives $\kappa_N$.

For every $N\ge5$, $\kappa_N$ is strictly positive. With $r=N-5\ge0$,

$$
\boxed{\kappa_N=\frac{r^4+14r^3+69r^2+136r+88}{N}>0.}
\tag{12}
$$

All other displayed coefficients on nonzero spaces are positive.
Thus $Q_R$ is positive definite on $V$. The kernel of $Q_I$ consists
exactly of arbitrary $\alpha$ and $u=v$, with $h,\zeta,s,K_0$ zero.
It has dimension $1+(N-1)=N$.

These are precisely the fixed-output site phases: choose
$\theta_i=\alpha/2+u_i$ at core sites and $\theta_0=-N\alpha/2$.
Then $\sum_i\theta_i=0$ and the tangent source is
$i(\theta_i+\theta_j)(z_*)_{ij}$. There are no other zero modes.

At $N=3$, $\kappa_3=-4/3$. The companion
[four-site obstruction proof](w-state-four-site-local-obstruction-2026-09-27.md)
shows that every actual nearby feasible displacement has
$s=O(\|\delta z\|^{4/3})$. The potentially negative term is therefore
of smaller order than the positive quadratic terms. It proves the same
strict local conclusion at four sites.

## 6. From the forms to a local theorem

Fix the output to $H(z_*)=N!!W_n$.
Use the $N$ independent site phases to place a nearby source on the
slice where its imaginary displacement is $G$-orthogonal to the
phase tangents. This slice exists by the implicit function theorem:
the derivative of its phase conditions is the positive definite
Gram matrix of those tangents.

For a feasible displacement $\delta z$,
$J\delta z=O(\|\delta z\|^2)$.
Its component normal to $V$ is therefore $O(\|\delta z\|^2)$, using
a bounded inverse of $J$ on a fixed complement of its kernel.
No smoothness or independence of the complete output constraints
is assumed. The $G$-orthogonal projection onto $V$ retains the phase
conditions.

For $N\ge5$, (10)–(12) are coercive on this phase-fixed tangent slice.
The stationary Lagrangian and the fixed output give

$$
S(z)-S(z_*)=Q_R(\operatorname{Re}\delta z)
+Q_I(\operatorname{Im}\delta z)+O(\|\delta z\|^3).
$$

Replacing $\delta z$ by its tangent projection changes the right side
by $O(\|\delta z\|^3)$. The positive quadratic term absorbs the
remainder. The four-site argument gives the same conclusion with an
additional $O(\|\delta z\|^{8/3})$ error.
This proves (1), since the phase-slice displacement bounds distance
to the orbit and the coordinate change is invertible.

For nearby output $\mu W_n$, multiply the physical source by the
branch of $(\Lambda/\mu)^{1/m}$ near one. This fixes the amplitude
and preserves rate. For extra colors, project each edge onto the
two target colors: all binary outputs are unchanged, and the source
norm only decreases. Equality requires every discarded entry to be zero.
This proves the theorem for every finite palette. ∎

## 7. Scope of the progress

The earlier local certificate covered six sites. This theorem covers
every even count from four onward and every complex colored perturbation.
It supplies a quadratic cost for moving away from the local equality
orbit, after normalizing the output.

A remote component or distant region of the exact-W source set could
still have a better rate. The all-even global design theorem still
requires a global bound or a reduction of those remaining sources.
