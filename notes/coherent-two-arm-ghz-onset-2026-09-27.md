# Two comparable arms suffice for fifth-power GHZ onset

September 27, 2026. **Written proof with exact supporting checks; independent
audit pending.** The unrestricted square-root rate law remains open.

[Exact replay](../computations/coherent-two-arm-ghz-2026-09-27/README.md) ·
[Illustrated guide](../explainers/CRITICAL-DIRECTION-GEOMETRY.md) ·
[GHZ project](../research/ghz-rates/README.md)

## 1. Statement

Let $A_0$ be a six-site source using only ground color $a$, with all
fifteen ground entries nonzero and zero hafnian. For a nearby ternary
source write

$$
H(A)=\lambda(a^6+b^6+c^6)+E,\qquad
\varepsilon=\|E\|,\qquad \delta=\|A-A_0\|.
$$

Here $E$ is orthogonal to the displayed GHZ tensor. Let $T$ be the
binary non-ground part and $t=\|T\|$.

**Theorem.** Fix $\eta>0$. There are constants $C_1,C_2$ and a
neighborhood of $A_0$ such that

$$
\boxed{|\lambda|\le C_1\varepsilon+C_2\delta^5}
\tag{1}
$$

whenever $T=0$ or two edges at a common center satisfy

$$
\|T_{01}\|\ge\eta t,\qquad \|T_{02}\|\ge\eta t,
\tag{2}
$$

after relabelling sites. There is no matrix-rank hypothesis, no
specified nonzero ground cofactor row, and no restriction on the
other blocks.

The [previous two-arm result](transverse-two-arm-ghz-onset-2026-09-27.md)
proves this when the attachment map is uniformly injective. We now
handle neighborhoods of all its noninjective pairs: two rank-one
arms sharing a center line.

**Corollary.** Let $\mathcal E$ be the closed set of normalized binary
sources supported on one edge, with arbitrary matrix rank.
For every fixed $\rho_0>0$, (1) is uniform when $T=0$ or
$\operatorname{dist}(T/t,\mathcal E)\ge\rho_0$.

This is a source-distance onset bound at full-support single-color
limits. It does not prove the error-versus-signal inequality
$\varepsilon\ge c|\lambda|^3$ needed for the unrestricted rate law.

## 2. Retain the size of each outside arm

Write $K=\{0,1,2\}$, $L=\{3,4,5\}$, and

$$
G_i=T_{0i},\quad B=T_{12},\quad \beta=\|B\|,\quad
H_r=T_{0r},\quad Y_{ir}=T_{ir},\quad Z_{rs}=T_{rs}.
$$

Put $h_r=\|H_r\|$ and $d=\delta^2$. All source blocks have norm at
most $t\le\delta$. As in the previous proofs, the cases $T=0$,
$\varepsilon>td$, or $t\le L_0d$ for any fixed $L_0$ are immediate
from $|\lambda|\le\varepsilon+15t^3$. Hence assume

$$
\varepsilon\le td,\qquad t>d,\qquad
f:=\|\mathcal F_4(T)\|\le Ctd.
\tag{3}
$$

An edge with nonzero ground cofactor has block norm $O(d)$.
Call it anchored.

The four-site responses are

$$
F_r=G_1Y_{2r}+G_2Y_{1r}+H_rB,\qquad
R^i_{rs}=G_iZ_{rs}+H_rY_{is}+H_sY_{ir}.
\tag{4}
$$

Consider normalized arm pairs $(G_1/t,G_2/t)$ near any fixed pair
of nonzero rank-one matrices sharing a center line. The map
$\Phi(v_1,v_2)=(G_1/t)v_2+(G_2/t)v_1$ has one zero singular value
at that pair. Its other singular values stay bounded below.
Choose a unit smallest right singular vector $v=(v_1,v_2)$.
Both components stay bounded away from zero.

Orthogonal projection onto this one-dimensional input direction,
separately at each outside color, gives

$$
Y_{ir}=v_iw_r+e_{ir},\qquad
\|w_r\|\le t,\qquad
e_r:=\|(e_{1r},e_{2r})\|
\le C\left(d+\frac{\beta}{t}h_r\right).
\tag{5}
$$

The last inequality follows by applying the bounded inverse on the
other right singular directions to $F_r/t-H_rB/t$.
It does not require the smallest singular value to remain zero.
Unlike the earlier residual estimate, we retain $h_r$ rather than
replace it by $t$.

Set $\theta=\beta/t\le1$ and
$S_{rs}=H_rw_s+H_sw_r$. The complementary map

$$
(Z,W)\longmapsto
\bigl((G_1/t)Z+v_1W,\ (G_2/t)Z+v_2W\bigr)
\tag{6}
$$

is bounded below near the limiting pair. Indeed, at the limit
$G_1/t=uv_1$, $G_2/t=-uv_2$, and its two components are
$v_1(uZ+W)$ and $v_2(-uZ+W)$, which determine both $Z,W$.
This remains true after tensoring with the outside color spaces.

Insert (5) into (4), and apply (6) to $(Z_{rs},S_{rs}/t)$.
Since $h_r,h_s\le t$, we obtain the refined estimates

$$
\boxed{
\|Z_{rs}\|\le C\left(d+\frac{\theta h_rh_s}{t}\right),\qquad
\|S_{rs}\|\le C(td+\theta h_rh_s).
}
\tag{7}
$$

In particular, for
$J_{rs}=H_rY_{2s}+H_sY_{2r}$,

$$
J_{rs}=v_2S_{rs}+H_re_{2s}+H_se_{2r},\qquad
\|J_{rs}\|\le C(td+\theta h_rh_s).
\tag{8}
$$

All constants are uniform on a sufficiently small neighborhood of
the fixed normalized arm pair. The argument needs no assumption
that the other normalized source blocks vanish.

## 3. The projection and the small-attachment alternative

Let $P$ be the orthogonal projection perpendicular to $v_1$ at
leaf 1. It has binary rank one and
$\|P(b^6+c^6)\|=1$.
Every six-site matching belongs to

$$
H_6(T)=\sum_{\{r,s\}\subset L}Z_{rs}F_u+
\operatorname{Perm}_3(H,Y_1,Y_2),
\qquad \{u\}=L\setminus\{r,s\}.
\tag{9}
$$

In the permanent, group terms by the outside site $u$ assigned to
leaf 1. Equation (5) gives the exact identity

$$
P\operatorname{Perm}_3(H,Y_1,Y_2)
=\sum_{u\in L}(Pe_{1u})J_{rs}.
\tag{10}
$$

The direct cases below bound (9) after this projection by $Ctd^2$.
The remaining case uses a rescaled triangle and may use a different
local projection.

If $\beta=O(d)$, the earlier shared-center estimate
$|\lambda|\le C\varepsilon+Ct(\beta+d)^2$ already proves (1).
If a strong arm is anchored, (2) forces $t=O(d)$.
An anchored closing edge also has $\beta=O(d)$.
Thus we may assume $\beta>L_0d$ for a sufficiently large fixed
$L_0$, and all three internal ground cofactors vanish.
The ground selection argument then supplies a core vertex $i$ and
two distinct outside sites $r,s$ with anchored edges $ir,is$.
See [the triangle proof](triangle-attachment-ghz-bound-2026-09-27.md#4-two-attachments-share-an-anchored-core-component).

We also use the following direct consequence of the
[rescaled-triangle argument](transverse-two-arm-ghz-onset-2026-09-27.md#3-rescale-the-weak-triangle-edge):

**Small-attachment criterion.** In the remaining case with zero internal
ground cofactors, under (2)--(3), if $\beta>L_0d$
and all three $\|(Y_{1r},Y_{2r})\|\le C_0\beta$, then (1) holds.

For clarity, the earlier argument uses two-arm injectivity only to
derive precisely this attachment bound. Once it is supplied,
rescale the sites with $\theta=\beta/t$ so that

$$
\widetilde B=B/\theta,\quad
\widetilde H_r=\theta H_r,\quad
\widetilde Y_{ir}=Y_{ir},\quad
\widetilde Z_{rs}=\theta Z_{rs},
$$

and the two arms stay unchanged. The normalized triangle has all
three edges bounded below, and its attachments have size $O(\beta)$.
The leaf-sensitive mixed-output bound and the triangle pair lemma
give

$$
\|\widetilde X_r\|\|\widetilde X_s\|\le
C\beta(d+\varepsilon/\beta),\qquad
\|Z_{rs}\|\le C(d+\varepsilon/\beta).
$$

The shared-anchor projection in that proof gives
$\|P'H_6(\widetilde T)\|\le C\beta d(d+\varepsilon/\beta)$
for a suitable local projection $P'$.
Since $H_6(\widetilde T)=\theta H_6(T)$,

$$
|\lambda|\le\varepsilon+Ctd^2+C(td/\beta)\varepsilon
\le C\varepsilon+C\delta^5.
$$

This proves the criterion without an attachment-injectivity hypothesis.

## 4. When the selected anchors are at the center

Suppose $i=0$, so $h_r,h_s=O(d)$; let $u$ be the third outside site.
Every outside pair includes at least one of $r,s$, and (7) therefore
gives $\|Z_{ab}\|=O(d)$ for all three pairs. The first sum in (9)
has norm $O(td^2)$.

Equation (5) gives $e_r,e_s=O(d)$.
By (8), $J_{ru},J_{su}=O(td)$, so their contributions to (10)
are $O(td^2)$.

For the last contribution, the direct expression for $J_{rs}$ gives

$$
\|J_{rs}\|\le Cd(\|w_r\|+\|w_s\|+d).
\tag{11}
$$

The potentially large $h_u$ can be paired with the hidden vectors:

$$
\begin{aligned}
h_u\|w_r\|
&\le\|H_uw_r+H_rw_u\|+h_r\|w_u\|\\
&\le C(td+\theta h_uh_r)+h_rt
\le Ctd,
\end{aligned}
\tag{12}
$$

and likewise for $s$. Multiplying (11) by
$e_u\le C(d+\theta h_u)$ and using (12), $\|w_r\|,\|w_s\|\le t$,
$h_u\le t$, and $d<t$ gives $e_u\|J_{rs}\|\le Ctd^2$.
This completes the center-anchor case.

## 5. When the selected anchors are at a leaf

Suppose $i=1$ or $2$. Since $\|v_i\|$ stays bounded below, its two
anchored components and (5) imply

$$
\|w_r\|\le C(d+\theta h_r),\qquad
\|w_s\|\le C(d+\theta h_s).
\tag{13}
$$

In particular both are $O(\beta)$. Let $u$ be the remaining site,
and choose a sufficiently large fixed constant $L$.
If $\|w_u\|\le L\beta$, (5) makes all leaf attachments $O(\beta)$;
the small-attachment criterion applies.

Otherwise put $w=\|w_u\|>L\beta$. The pair equation controls the
center arm to each anchored outside site:

$$
\begin{aligned}
h_rw
&\le \|S_{ru}\|+h_u\|w_r\|\\
&\le C(td+\theta h_rh_u)+Ch_u(d+\theta h_r)\\
&\le Ctd+C\beta h_r.
\end{aligned}
\tag{14}
$$

For large enough $L$, absorb the last term to obtain

$$
h_r,h_s\le Ctd/w,\qquad
\theta h_r,\theta h_s=O(d),\qquad
e_r,e_s,\|w_r\|,\|w_s\|=O(d).
\tag{15}
$$

Again every outside pair touches $r$ or $s$. Equations (7), (15),
and $\beta/w<1/L$ give $\|Z_{ab}\|=O(d)$ for all pairs.
The outside-edge sum in (9) is $O(td^2)$.

For (10), equation (8) bounds $J_{ru},J_{su}$ by $Ctd$;
their factors $e_s,e_r$ are $O(d)$.
For the remaining term, use the direct expression instead:

$$
\|J_{rs}\|\le C(h_r+h_s)d\le Ctd^2/w,\qquad
e_u\le C(d+\beta)\le C'\beta.
$$

Its product is at most $C(\beta/w)td^2\le Ctd^2$.
This completes the leaf-anchor case.

Since a local binary rank-one projection retains unit GHZ norm,
the direct bounds, together with the small-attachment criterion,
give $|\lambda|\le C\varepsilon+Ctd^2$.
As $t\le\delta$ and $d=\delta^2$, this proves (1) near every
shared-center arm pair.

## 6. Uniformity and the single-edge frontier

The normalized arm pairs with norms at least $\eta$ and combined
squared norm at most one form a compact set. At an injective pair,
the previous theorem applies in a neighborhood. At every other
pair, the proof above applies in a neighborhood. A finite cover
proves (1) uniformly under (2).

The corollary needs only an elementary support observation. A
nonzero four-site-flat source whose support has no two adjacent
edges has at most one edge: its support is a matching, and any
two of those edges would produce their nonzero tensor product on
their four endpoints, without any other term to cancel it.

On the compact set of normalized sources at distance at least
$\rho_0$ from $\mathcal E$, each zero of $\mathcal F_4$ consequently
has two nonzero adjacent edges. A finite cover gives neighborhoods
with a common positive arm threshold $\eta$, where the theorem
applies. On the remaining compact set,
$\|\mathcal F_4(T/t)\|\ge c>0$. Equations (3) and the mixed-output
bound before the reduction give

$$
ct^2\le C(\varepsilon+td).
$$

Thus either $t=O(d)$ or $t^2=O(\varepsilon)$.
The elementary bound $|\lambda|\le\varepsilon+15t^3$ proves (1)
in either case. This proves the corollary.

The closing-edge contribution in the earlier residual estimate is
therefore controlled by the full collection of output and ground
equations near every two-arm direction. Single-edge directions
remain outside this uniform onset theorem. The unrestricted
square-root rate law, including its other boundary branches,
remains open.
