# Triangle attachments: a fifth-power GHZ onset bound through rank loss

September 27, 2026. **Written proof with exact supporting checks; independent
audit pending.** The unrestricted square-root rate law remains open.

[Exact replay](../computations/triangle-ghz-onset-2026-09-27/README.md) ·
[Illustrated guide](../explainers/CRITICAL-DIRECTION-GEOMETRY.md) ·
[GHZ project](../research/ghz-rates/README.md)

## 1. Statement

Let $A_0$ be a six-site source using only the ground color $a$, with all
fifteen ground entries $D_{ij}\ne0$ and $\operatorname{haf}D=0$. Write

$$
H(A)=\lambda(a^6+b^6+c^6)+E,\qquad E\perp(a^6+b^6+c^6),\qquad
\varepsilon=\|E\|,\quad\delta=\|A-A_0\|.
$$

Let $T$ be the binary non-ground part of $A$, and $t=\|T\|$.
Fix a normalized binary source $S$ supported on a triangle
$K=\{0,1,2\}$, with all three blocks nonzero and the other sites isolated.

**Theorem.** There are neighborhoods of $A_0$ and $S$, and constants
$C_1,C_2$, such that

$$
\boxed{|\lambda|\le C_1\varepsilon+C_2\delta^5}
\tag{1}
$$

whenever $T=0$ or $T/t$ belongs to the chosen neighborhood of $S$.
No matrix-rank or triangle-response-rank hypothesis is imposed.
Constants are uniform on compact families of such normalized triangles.

The proof bounds a projection of the output. Bounding the entire
non-ground output by the fifth power from the auxiliary constraints
alone would be false; section 7 gives an exact example.

## 2. Response equations and ground anchors

Write $L=\{3,4,5\}$. Split $T$ into the actual triangle $C=T[K]$,
attachments $X_r=((T_{ir})_{i\in K})$ for $r\in L$, and outside edges
$Z_{rs}=T_{rs}$. Put $x_r=\|X_r\|$ and $z_{rs}=\|Z_{rs}\|$.
Tensor products below always place factors at their labelled sites.

Define the triangle attachment response

$$
U_CX_r=(X_r)_0C_{12}+(X_r)_1C_{02}+(X_r)_2C_{01},
\tag{2}
$$

and the three pair responses, one for each $\{i,j\}\subset K$,

$$
R(C,X_r,X_s,Z_{rs})_{ij}
=C_{ij}Z_{rs}+(X_r)_i(X_s)_j+(X_s)_i(X_r)_j.
\tag{3}
$$

They are exactly the four-site outputs on $K\cup\{r\}$ and on
$\{i,j,r,s\}$, respectively. The
[mixed-output bounds](four-arm-ghz-distance-bound-2026-09-27.md) give

$$
f:=\|\mathcal F_4(T)\|\le C(\varepsilon+\delta^2t),\qquad
\|T_{ij}\|\le C_{ij}'(\varepsilon+\delta^2)
\quad\text{if }c_{ij}:=\operatorname{haf}D[V\setminus\{i,j\}]\ne0.
\tag{4}
$$

Every five-site subset has an internal edge with $c_{ij}\ne0$; see
section 5 of the [normal-form note](ghz-critical-direction-normal-form-2026-09-27.md).
We call a block with $c_{ij}\ne0$ an anchored block.

The cases $T=0$, $\varepsilon>t\delta^2$, and $t\le L_0\delta^2$
for a fixed constant $L_0$ are immediate, since
$|H_{b^6}(T)|\le15t^3$ and $|H_{b^6}(T)-\lambda|\le\varepsilon$.
For $\delta\le1$ these give, respectively,
$|\lambda|\le\varepsilon$, $|\lambda|\le16\varepsilon$, and
$|\lambda|\le\varepsilon+15L_0^3\delta^6$.
Hence work in the regime

$$
\varepsilon\le t\delta^2,\qquad t>\delta^2,\qquad
f\le Ct\delta^2.
\tag{5}
$$

Every anchored block is then $O(\delta^2)$.
If any internal triangle edge is anchored, its norm is at least a
fixed positive multiple of $t$. Equation (4), followed by absorption
of $O(t\delta^2)$, gives $t\le L_0\delta^2$, already treated.
We may therefore assume

$$
c_{01}=c_{02}=c_{12}=0.
\tag{6}
$$

## 3. Pair control from the impossibility of a missing edge

Let $A_rX$ select the attachment blocks at edges $ir$ with $c_{ir}\ne0$.
For a fixed outside pair $r,s$, put $e_{rs}=1$ if $c_{rs}\ne0$ and
$e_{rs}=0$ otherwise. By the five-site cofactor fact on $K\cup\{r,s\}$
and (6), at least one of $A_r,A_s,e_{rs}$ specifies an anchored edge.

**Pair lemma.** For $B$ sufficiently close to $S[K]$, there is a
uniform constant $M$ such that

$$
\begin{aligned}
\|X\|\|Y\|+\|Z\|\le M\bigl(&\|R(B,X,Y,Z)\|\\
&+(\|U_BX\|+\|A_rX\|)\|Y\|\\
&+\|X\|(\|U_BY\|+\|A_sY\|)+e_{rs}\|Z\|\bigr).
\end{aligned}
\tag{7}
$$

This lemma permits any fixed finite palette. To prove it first take
$B=S[K]$ and $\|X\|=\|Y\|=1$. If its right side vanished, the source
$S+X+Y+Z$ on five sites would have every four-site output zero:
the five quartets are precisely the two equations (2) and the three
equations (3). All five sites are active, because $X,Y\ne0$.
The triangle prevents a star support. The
[flat-support classification](four-site-flat-support-classification-2026-09-27.md)
therefore forces a complete five-site support. But at least one
specified anchored edge is zero, a contradiction.

This nonvanishing gives a quantitative bound by compactness.
Indeed $\|(S_{ij}Z)_{i<j}\|=\|S\|\|Z\|$, while the remaining
quadratic terms in (3) are bounded for unit $X,Y$. For large $\|Z\|$,
the first term on the right side of (7) controls $1+\|Z\|$.
For bounded $Z$, the continuous right side has positive minimum.
Separate rescaling of $X,Y$, and rescaling $Z$ by their product,
proves (7) for nonzero $X,Y$; when either is zero the linear term in
$Z$ proves it directly. Perturbing $S$ to $B$ changes the response
terms by at most $O(\|B-S\|)(\|X\|\|Y\|+\|Z\|)$.
Absorption proves the neighborhood assertion.

Apply (7) with $B=C/t$, $X=X_r$, $Y=X_s$, and $Z=tZ_{rs}$.
The first response is the actual quartet collection (3).
Moreover $\|U_{C/t}X_r\|\le f/t=O(\delta^2)$,
$\|A_rX_r\|=O(\delta^2)$, and $x_r\le t$.
If $e_{rs}=1$, then $tz_{rs}=O(t\delta^2)$ by (4).
Consequently, for all three outside pairs,

$$
\boxed{x_rx_s\le Ct\delta^2,\qquad z_{rs}\le C\delta^2.}
\tag{8}
$$

Individual attachment norms need not be $O(\delta^2)$.

## 4. Two attachments share an anchored core component

The cross-cofactor matrix $(c_{ir})_{i\in K,r\in L}$ is not zero.
Otherwise the ground matching identity

$$
\sum_{j\ne i}D_{ij}c_{ij}=\operatorname{haf}D=0
\tag{9}
$$

at the three outside sites would give
$D_{rs}c_{rs}+D_{rh}c_{rh}=0$ and its two companions.
Adding two equations and subtracting the third makes each outside
edge product zero. Since $D$ has full support, all outside cofactors
would be zero. Together with (6) this would make all cofactors zero,
contrary to the five-site cofactor fact.

Choose a nonzero cross row, at core site $i$. Equation (9) and (6)
show that this row has at least two nonzero entries, say at distinct
outside sites $r,s$. Thus

$$
\|(X_r)_i\|+\|(X_s)_i\|\le C\delta^2.
\tag{10}
$$

Let $j,k$ be the other core sites. For $B=C/t$, consider the map on
two local color vectors

$$
N_B(v_j,v_k)=v_j B_{ik}+v_k B_{ij}.
\tag{11}
$$

At $B=S[K]$ its kernel has dimension at most one. Here is an elementary
proof valid for any palette. A nonzero relation must have both
$v_j,v_k\ne0$, since both edge blocks are nonzero. Projecting at
site $j$ perpendicular to $v_j$ shows $B_{ij}=u_i v_j$ for some
nonzero $u_i$. Substitution gives $B_{ik}=-u_i v_k$.
Any other relation must use the same one-dimensional local factors
and the same ratio. It is therefore a scalar multiple of the first.

If $N_S$ is injective, it remains bounded below nearby. For each
outside color, (2), (5), and (10) imply that (11) applied to the
remaining two attachment components is $O(\delta^2)$. Hence
$x_r+x_s=O(\delta^2)$ in this case.

If $N_S$ has a one-dimensional kernel, all but the smallest singular
value remain bounded below nearby. Choose a unit right singular
vector $v=(v_j,v_k)$ for the smallest singular value of $N_B$.
The same map is used for both outside sites and all outside colors.
Projection onto the other right singular vectors, followed by (10),
therefore gives

$$
X_r=K_r+e_r,\qquad X_s=K_s+e_s,\qquad
\|e_r\|+\|e_s\|\le C\delta^2,
\tag{12}
$$

where, for some outside color vectors $u_r,u_s$,

$$
(K_\ell)_i=0,\qquad
(K_\ell)_j=v_j u_\ell^{\mathsf T},\qquad
(K_\ell)_k=v_k u_\ell^{\mathsf T}
\quad(\ell=r,s).
\tag{13}
$$

Both $v_j,v_k$ are nonzero after shrinking the neighborhood, since
both are nonzero at the limiting kernel line. This argument allows
$N_B$ to become injective: it does not assume persistence of its kernel.

## 5. Projecting the six-site output

Let $\operatorname{Perm}_3(X_r,X_s,X_h)$ denote the sum of the six
matching tensors that join each outside site to a distinct core site.
Every six-site matching either has exactly one outside edge or has
three cross edges. Thus

$$
H_6(T)=\sum_{\{r,s\}\subset L}Z_{rs}\,U_CX_h
+\operatorname{Perm}_3(X_r,X_s,X_h),
\qquad \{h\}=L\setminus\{r,s\}
\tag{14}
$$

in each summand of the first sum. Its norm is at most
$3\max z_{rs}\,f\le Ct\delta^4$ by (5) and (8).

In the injective case of section 4, the last term also has norm at
most $6x_rx_sx_h\le Ct\delta^4$. Suppose instead (12)--(13) hold.
In $\operatorname{Perm}_3(K_r,K_s,X_h)$, the first two attachments
must occupy core sites $j,k$, leaving site $i$ to $X_h$.
The tensor therefore has the fixed local factor $v_j$ at site $j$.
Let $P_j$ be the orthogonal projection onto $v_j^\perp$ at that site,
acting as the identity elsewhere. It kills this tensor exactly.

Trilinearity and the pair estimates give

$$
\begin{aligned}
&\|\operatorname{Perm}_3(X_r,X_s,X_h)
-\operatorname{Perm}_3(K_r,K_s,X_h)\|\\
&\quad\le6\|e_r\|x_sx_h+6\|K_r\|\|e_s\|x_h\\
&\quad\le C\delta^2\bigl(t\delta^2+(x_r+C\delta^2)x_h\bigr)
\le Ct\delta^4.
\end{aligned}
\tag{15}
$$

Thus $\|P_jH_6(T)\|\le Ct\delta^4\le C\delta^5$.
The two binary GHZ words remain orthogonal after the local projection,
because their other five factors are orthogonal. Since a rank-one
projection in the binary space has trace one,

$$
\|P_j(b^6+c^6)\|^2=\|P_jb\|^2+\|P_jc\|^2=1.
\tag{16}
$$

The entirely non-ground part of the original output is exactly
$H_6(T)=\lambda(b^6+c^6)+E_{\rm bin}$, with
$\|E_{\rm bin}\|\le\varepsilon$. Applying $P_j$ proves
$|\lambda|\le\varepsilon+C\delta^5$.
In the injective case the full output bound gives the same conclusion.
Together with the elementary cases in section 2 this proves (1).
A finite cover gives the compact-family assertion. ∎

## 6. Only stars with at most three arms remain for this onset estimate

Let $\mathcal B_\star$ be the closed set of normalized binary six-site
sources supported on a star with at most three nonzero arms, allowing
arbitrary colored blocks.

**Corollary.** For every fixed $\eta>0$, estimate (1) holds uniformly
near each $A_0$ above whenever $T=0$ or

$$
\operatorname{dist}(T/t,\mathcal B_\star)\ge\eta.
\tag{17}
$$

Combine this theorem with the
[four-core theorem](four-core-attachment-ghz-bound-2026-09-27.md)
and the [four-arm theorem](four-arm-ghz-distance-bound-2026-09-27.md).
The simultaneous normalized zeros of $\mathcal F_4(S)$ and
$(c_{ij}S_{ij})_{i<j}$ outside $\mathcal B_\star$ are triangles,
non-star four-site cores, or stars with at least four arms.
The support theorem and the five-site cofactor fact exclude the
complete five-site alternative. These three theorems provide a
neighborhood of each remaining direction.

For completeness, restrict to the compact set in (17), and take a
finite cover of its simultaneous zero set by such neighborhoods.
Outside their union the sum of the two residual norms has a positive
minimum. In the regime $\varepsilon\le t\delta^2$ and $t>L_0\delta^2$,
the original output equations give

$$
\|\mathcal F_4(T/t)\|\le C/L_0,\qquad
\|(c_{ij}T_{ij}/t)_{i<j}\|\le C(\delta+1/L_0).
$$

These are the same residual bounds as in section 3 of the four-core
note. Choosing $L_0$ large and then $\delta$ small puts the direction
in the finite cover. The other regimes are elementary as before.
This proves (17), also if the simultaneous zero set is empty.

This is a source-distance onset result at full-support single-color
limits. The estimate $\varepsilon\ge c|\lambda|^3$ needed for the
unrestricted square-root rate law is still open, including on the
families whose onset is now controlled. Other boundary classes also
remain.

## 7. Why the projection is necessary for these auxiliary bounds

Let $\omega^2+\omega+1=0$, with $\omega\ne1$. Take the full-support
ground source

$$
(D_{01},D_{02},D_{12})=(1,1,-2),\quad
D_{34}=D_{35}=D_{45}=1,
$$

and cross rows, in outside order $(3,4,5)$,

$$
(D_{0r})=(1,\omega,\omega^2),\qquad
(D_{1r})=(D_{2r})=(1,\omega^2,\omega).
$$

Its hafnian is zero and its nonzero cofactors occur exactly at
$04,05,34,35$. For real $\tau>0$, use only one non-ground color and set
all three triangle edges to $\tau^2$, set outside edges to zero, and set

$$
X_4=X_5=\tau^3(0,1,-1),\qquad
X_3=\tau^3(-2,1,1).
$$

Then all anchored non-ground blocks vanish, $U_CX_r=0$ for every $r$,
and

$$
\mathcal F_4(T(\tau))=\tau^6\mathcal F_4(T(1)),\qquad
H_6(T(\tau))=4\tau^9 b^6,\qquad
\|T(\tau)\|^2=3\tau^4+10\tau^6.
$$

In particular $f=O(t^3)$ and every anchor constraint holds exactly,
yet $\|H_6(T)\|$ is of order $t^{9/2}$, not $O(t^5)$.
The large term has a fixed local color and the projection in section 5
removes it. This auxiliary example is not a GHZ counterexample: its
output has no $c^6$ component and hence cannot have small error
relative to a nonzero binary GHZ signal.
