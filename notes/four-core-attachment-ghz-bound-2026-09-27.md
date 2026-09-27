# Four-site cores: control their attachments without resolving their singularities

September 27, 2026. **Written proof with exact supporting checks; independent
audit pending.** The unrestricted square-root rate law remains open.

[Exact replay](../computations/four-core-attachments-2026-09-27/README.md) ·
[Illustrated guide](../explainers/CRITICAL-DIRECTION-GEOMETRY.md) ·
[GHZ project](../research/ghz-rates/README.md)

## 1. A linear extension theorem for every palette

Let $C$ be a complex colored source on $K=\{0,1,2,3\}$ with
$H_4(C)=0$. Suppose all four sites are active and its support is not
contained in a star. No block-rank or smoothness hypothesis is imposed.
Write $q$ for the palette size.

For a new site $r$, let $X_i$ be the block joining $i$ to $r$.
Define the attachment response by

$$
(\mathcal M_C X)_{ijk}
=X_i\otimes C_{jk}+X_j\otimes C_{ik}+X_k\otimes C_{ij},
\qquad \{i,j,k\}\subset K,
\tag{1}
$$

where tensor factors are placed at their labelled sites, including $r$.
It is a linear map on the $4q^2$ attachment entries.

**Attachment theorem.** This map is injective except in the following case:

$$
C_{ij}=d_{ij}u_i u_j^{\mathsf T},\qquad
u_i\ne0,\quad d_{ij}\ne0,
\tag{2}
$$

and, writing

$$
a=d_{01}d_{23},\qquad b=d_{02}d_{13},\qquad c=d_{03}d_{12},
$$

we have

$$
a+b+c=0,\qquad a^2+b^2+c^2=0.
\tag{3}
$$

Thus $(a:b:c)=(1:\omega:\omega^2)$ or $(1:\omega^2:\omega)$,
where $\omega^2+\omega+1=0$. In this exceptional case the kernel has
dimension $q$. There are nonzero scalars $x_i$ such that it consists of

$$
X_i=x_i u_i v^{\mathsf T}\quad(i\in K),
\qquad v\in\mathbb C^q.
\tag{4}
$$

In particular, **specifying any one attachment block kills the entire
kernel**: for every $i$, the map $X\mapsto(\mathcal M_C X,X_i)$ is
injective. These exceptional cores are exactly the restrictions of
the complete five-site cube-root cores.

### Proof

First fix one color at the new site. A nonzero kernel element, added
to $C$, produces an exactly four-site-flat source on five active sites:
the old quartet vanishes by assumption and the other four vanish by
(1). Its support cannot be a star, because the original core is not
a star. The [all-size support theorem](four-site-flat-support-classification-2026-09-27.md)
and [colored five-clique theorem](flat-four-response-five-clique-2026-09-27.md)
force it to be the complete cube-root core. In particular $C$ has
form (2), and every attachment uses the same local direction $u_i$.

It remains to determine precisely when such attachments exist.
Their scalar coefficients solve $Mx=0$, where

$$
M_{ii}=0,\qquad
M_{ij}=d_{kl}\quad\text{if }\{k,l\}=K\setminus\{i,j\}.
\tag{5}
$$

Direct determinant expansion gives

$$
\det M=a^2+b^2+c^2-2(ab+ac+bc).
\tag{6}
$$

Since $H_4(C)=0$ says $a+b+c=0$, the determinant is
$2(a^2+b^2+c^2)$. Every three-by-three principal minor of $M$
is twice a product of three nonzero edge coefficients. Thus $M$
has rank at least three, and exactly three when (3) holds.
Every coordinate of its nonzero kernel vector is nonzero: if one
coordinate vanished, the complementary principal minor would force
the other three to vanish.

Repeating this argument independently for each new-site color gives
(4). Conversely (3)--(5) give a nonzero extension with all four new
blocks present; the five-clique theorem identifies it as the cube-root
core. The dimension and single-block assertion follow. ∎

This proof works even when the internal four-site zero set is singular.
It classifies only the attachment kernel; it does not assert an internal
normal form or a linear distance bound to that zero set.

## 2. Consequence for the six-site GHZ onset

Let $A_0$ be a six-site single-ground-color source with all fifteen
ground entries $D_{ij}$ nonzero and zero matching output.
For a nearby ternary source write

$$
H(A)=\lambda(a^6+b^6+c^6)+E,\quad E\perp(a^6+b^6+c^6),\qquad
\varepsilon=\|E\|,\quad \delta=\|A-A_0\|.
$$

Let $T$ be its binary non-ground part and $t=\|T\|$.

**Onset theorem.** Fix a normalized binary four-site-flat source $S$
on four active sites whose support is not a star, with both other
sites isolated. There are a neighborhood $U$ of $S$, a neighborhood
of $A_0$, and constants $C_1,C_2$ such that

$$
\boxed{|\lambda|\le C_1\varepsilon+C_2\delta^5}
\tag{7}
$$

whenever $T=0$ or $T/t\in U$.
This includes singular blocks, missing core edges, and singular internal
four-site response. Constants can be chosen uniformly for a compact
collection of such normalized cores.

### The output constraints we use

The [mixed-output estimates](four-arm-ghz-distance-bound-2026-09-27.md)
give, with constants depending on $A_0$,

$$
f:=\|\mathcal F_4(T)\|\le C(\varepsilon+\delta^2t).
\tag{8}
$$

For any ground cofactor
$C_{ij}(D)=\operatorname{haf}D[V\setminus\{i,j\}]\ne0$, they also give

$$
\|T_{ij}\|_F\le C_{ij}'(\varepsilon+\delta^2).
\tag{9}
$$

Every five-site subset contains an internal edge with nonzero ground
cofactor; see section 5 of the
[normal-form note](ghz-critical-direction-normal-form-2026-09-27.md).
These statements concern the original GHZ output, not just an
auxiliary response.

If $T=0$, then $|\lambda|\le\varepsilon$. If
$\varepsilon>t\delta^2$, the matching estimate
$|H_{b^6}(T)|\le15t^3\le15t\delta^2$ gives
$|\lambda|\le16\varepsilon$.
For each fixed $L$, the case $t\le L\delta^2$ also gives
$|\lambda|\le\varepsilon+15L^3\delta^6$ directly.
It therefore suffices to work with

$$
\varepsilon\le t\delta^2,\qquad t>\delta^2,
\qquad f\le Ct\delta^2.
\tag{10}
$$

Label the active core by $K=\{0,1,2,3\}$ and the outside sites by $r,s$.
Decompose $T$ into its actual internal source $B=T[K]$, the two
attachment collections $X_r,X_s$, and $Z=T_{rs}$.
Put $x_r=\|X_r\|$, $x_s=\|X_s\|$, and $z=\|Z\|$.
The source $B$ need not be flat.

### Both attachment collections are small

The four responses involving $r$ and three core sites are exactly
$\mathcal M_BX_r$. As $B/t$ is close to $S[K]$, injectivity of
$\mathcal M_{S[K]}$ implies a persistent linear lower bound:

$$
x_r\le C f/t\le C\delta^2,
\tag{11}
$$

and the same holds for $s$. This proves the claim for every
non-exceptional core.

Suppose $S[K]$ is exceptional. All its six blocks are nonzero.
If some nonzero ground cofactor lies inside $K$, its corresponding
block of $T$ has norm at least $ct$, and (9) implies
$t\le C(\varepsilon+\delta^2)$. Absorb the first term using (10)
and sufficiently small $\delta$. This gives $t\le L\delta^2$
for a fixed $L$, already handled above.

Otherwise every ground cofactor inside $K$ is zero. Apply the
five-site cofactor fact to $K\cup\{r\}$. It supplies an edge $ir$
with nonzero cofactor, so (9) controls the attachment block
$(X_r)_i$. The augmented injectivity in section 1 persists near
the fixed core and gives

$$
x_r\le C\bigl(f/t+\|(X_r)_i\|_F\bigr)
\le C\delta^2.
\tag{12}
$$

Here $\varepsilon\le t\delta^2\le\delta^3$ and $\delta\le1$.
Using $K\cup\{s\}$ gives the same estimate for $x_s$.
Thus both attachment collections are $O(\delta^2)$ in every case
that remains.

### Control the last edge and then the output

Choose any nonzero block $S_{ij}$, so $\|B_{ij}\|_F\ge ct$
in a sufficiently small normalized neighborhood. The quartet
$i,j,r,s$ has response

$$
B_{ij}\otimes Z+(X_r)_i\otimes(X_s)_j
+(X_s)_i\otimes(X_r)_j.
$$

Consequently

$$
ctz\le f+2x_rx_s\le C(t\delta^2+\delta^4).
$$

Since $t>\delta^2$, this implies $z\le C\delta^2$.

Every six-site perfect matching now either joins $r$ to $s$, or
joins them to two distinct core sites. Hence the exact identity

$$
H_6(T)=Z\otimes H_4(B)
+\sum_{\substack{i,j\in K\\i\ne j}}
(X_r)_i\otimes(X_s)_j\otimes
B_{K\setminus\{i,j\}},
\tag{13}
$$

again with labelled tensor factors. It follows that

$$
\|H_6(T)\|\le zf+12t x_rx_s
\le Ct\delta^4\le C\delta^5.
\tag{14}
$$

The entirely non-ground output coordinate satisfies
$|H_{b^6}(T)-\lambda|\le\varepsilon$. Combining all cases proves
(7). A finite cover proves uniformity over compact collections of
the specified cores. ∎

## 3. A uniform statement away from triangles and small stars

Let $\mathcal B$ be the following closed set of normalized binary
six-site sources:

- sources supported on at most three sites;
- stars with at most three nonzero arms.

This is a finite union of unit spheres in coordinate subspaces.
It contains all triangles, edges, and three-arm stars, with arbitrary
colored blocks.

**Corollary.** Fix $\eta>0$. Near each full-support single-color zero
$A_0$, estimate (7) holds uniformly whenever $T=0$ or

$$
\operatorname{dist}(T/t,\mathcal B)\ge\eta.
\tag{15}
$$

To prove this, consider the compact set of normalized directions
satisfying (15). Its simultaneous zeros of

$$
\mathcal F_4(S),\qquad
\mathcal C_D S:=\bigl(C_{ij}(D)S_{ij}\bigr)_{i<j}
$$

are, by the support theorem and cofactor exclusion, either non-star
four-active-site cores or stars with at least four arms.
The present theorem handles the first class. The
[four-arm onset theorem](four-arm-ghz-distance-bound-2026-09-27.md)
handles a neighborhood of every star in the second class.
Cover this compact zero set by finitely many such neighborhoods.

Outside their union, the sum of the two residual norms has a positive
minimum. In the regime $\varepsilon\le t\delta^2$ and $t>L\delta^2$,
the output equations give

$$
\|\mathcal F_4(T/t)\|\le C/L,\qquad
\|\mathcal C_D(T/t)\|\le C(\delta+1/L).
$$

For the second estimate, divide the two-non-ground output sector by
$t$ and use $C_{ij}(A_{aa})-C_{ij}(D)=O(\delta)$.
Choose $L$ sufficiently large and then $\delta$ sufficiently small.
The direction must belong to one of the selected neighborhoods.
The other regimes were handled directly in section 2. This proves
the corollary, including the case of an empty simultaneous zero set. ∎

## 4. What is gained, and what is still missing

Internal singularities of a non-star four-site core no longer obstruct
this fifth-power onset estimate. The reason is structural: a six-site
matching must use both outside sites, so controlling their attachments
is enough. The only hidden attachment is the cube-root extension,
and one ground-cofactor constraint removes it.

Within the full-support single-color boundary branch, the remaining
critical shapes not covered by this onset argument are triangles and
stars with at most three arms. The constants above need not stay
bounded when approaching those shapes.

The unrestricted rate problem still needs
$\varepsilon\ge c|\lambda|^3$, uniformly over all relevant boundaries.
An upper bound involving source distance $\delta$ does not provide that
comparison, even on the families now controlled. Other zero-output
boundary classes also remain to be handled.
