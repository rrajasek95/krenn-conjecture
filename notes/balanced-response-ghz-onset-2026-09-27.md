# Balanced responses and rank-free cofactor tests for GHZ onset

September 27, 2026. **Written proof with exact supporting checks; independent
audit pending.** The unrestricted square-root rate law remains open.

[Exact replay](../computations/balanced-response-ghz-2026-09-27/README.md) ·
[Illustrated guide](../explainers/CRITICAL-DIRECTION-GEOMETRY.md) ·
[GHZ project](../research/ghz-rates/README.md)

## 1. Two ground-cofactor tests, with no matrix-rank assumption

Let $A_0$ be a six-site single-ground-color source with all ground
entries $D_{ij}$ nonzero and zero hafnian. Write

$$
H(A)=\lambda(a^6+b^6+c^6)+E,\quad
\varepsilon=\|E\|,\quad \delta=\|A-A_0\|,\quad d=\delta^2.
$$

Let $T$ be the binary non-ground source, $t=\|T\|\le\delta$, and
$c_{ij}=\operatorname{haf}D[V\setminus\{i,j\}]$.
Call an edge **anchored** if $c_{ij}\ne0$.
All norms below are Hilbert or Frobenius norms.

**Theorem.** Fix $\eta>0$. Suppose $T=0$, or an edge $G=T_{01}$
has $\|G\|\ge\eta t$ and satisfies at least one of these conditions:

1. The edge $01$ is anchored.
2. There is an outside vertex $r$ such that both $0r$ and $1r$
   are anchored.
3. The four outside vertices have an anchored four-cycle:
   after relabelling, $24,25,34,35$ are anchored.

Then, uniformly near $A_0$,

$$
\boxed{|\lambda|\le C_1\varepsilon+C_2\delta^5.}
\tag{1}
$$

The matrix $G$ can have any rank. Its entries may include only one
different-color cell. All other blocks are unrestricted.
In particular, condition 3 always applies when **both endpoint
cofactor rows vanish**; see section 7.

The main new estimate is a balanced bilinear response lemma. Its
proof works in arbitrary finite local dimensions. The GHZ application
also needs refined bounds from actual mixed-color output equations.

## 2. A dimension-independent response gap

Let $x_i\in U=\mathbb C^p$, $y_i\in V=\mathbb C^q$, $1\le i\le m$.
Assume

$$
\sum_i\|x_i\|^2=\sum_i\|y_i\|^2=a^2>0.
$$

For a pair $(h,k)\in U\oplus V$ define

$$
M(h,k)=(x_i\otimes k+h\otimes y_i)_{i=1}^m,\qquad
K=\sum_i x_i y_i^*.
$$

The Hermitian Gram matrix is exactly

$$
M^*M=
\begin{pmatrix}a^2I_U&K\\K^*&a^2I_V\end{pmatrix}.
\tag{2}
$$

The singular values of $K$ obey

$$
\sum_j\sigma_j(K)=\|K\|_*
\le\sum_i\|x_i\|\|y_i\|\le a^2.
\tag{3}
$$

Here the nuclear norm is the sum of singular values; the first
inequality follows by its triangle inequality on rank-one terms.
Alternatively, write $K=XY^*$ and apply Cauchy--Schwarz to the
singular-vector expansion, giving $\|K\|_*\le\|X\|_F\|Y\|_F$.

The eigenvalues in (2) are $a^2\pm\sigma_j(K)$, with additional
copies of $a^2$ if the dimensions differ. At most one singular
value of $K$ exceeds $a^2/2$. Consequently there is a unit vector

$$
v=(p_0,q_0)/\sqrt2,\qquad \|p_0\|=\|q_0\|=1,
$$

such that

$$
\boxed{\|Me\|\ge a\|e\|/\sqrt2\quad\hbox{for every }e\perp v.}
\tag{4}
$$

Choose $v$ from a largest singular-vector pair of $K$, with the
relative sign giving the smallest Gram eigenvalue. If $K=0$, any
such equal-component vector works. The constant $1/\sqrt2$ is
sharp: $x_1=y_1=(1,0)$ and $x_2=y_2=(0,1)$ give $a^2=2$,
$K=I$, and Gram eigenvalues $1,1,3,3$.

Tensoring with an arbitrary outside color space $W$ preserves the
estimate. If $r_W=\|M(X_W,Y_W)\|$, orthogonal decomposition gives

$$
(X_W,Y_W)=v k_W+e_W,\qquad
\boxed{\|e_W\|\le\sqrt2\,r_W/a.}
\tag{5}
$$

The choice of $v$ depends only on the fixed pairs $(x_i,y_i)$,
not on $W$ or its attachments. Since $v$ is a Gram eigenvector,
$M(vk_W)$ and $Me_W$ are orthogonal, justifying the estimate in (5).
For two outside spaces $W,Z$,
the bilinear output therefore has the form

$$
X_WY_Z+X_ZY_W=P(k_Wk_Z)+R_{WZ},\qquad P=p_0q_0^{\mathsf T},
$$

$$
\|R_{WZ}\|\le
\|k_W\|\|e_Z\|+\|k_Z\|\|e_W\|+\|e_W\|\|e_Z\|.
\tag{6}
$$

Indeed, the map $B((X,Y),(X',Y'))=XY'+X'Y$ has norm at most the
product of its two input norms, by Cauchy--Schwarz. Expanding after
(5) proves (6).

This controls the response perpendicular to one common input
direction. It does **not** bound $k_W$ by the response; a true
kernel can remain. The GHZ proof bounds $k_W$ using additional
output equations.

If the two row norms initially differ, rescale all $x_i,X_W$ by
$\alpha>0$ and all $y_i,Y_W$ by $\alpha^{-1}$ to balance them.
This preserves every response and every bilinear output above.
The estimate (4) concerns the balanced input norm.

## 3. Mixed-output estimates retain the relevant edges

For any quartet $S$ of binary sites, with ground color at the
other two sites, the output equation has leading term
$D_{V\setminus S}(A)\mathcal F_S(T)$. Each remaining matching
uses two mixed ground/binary edges and one binary edge inside $S$.
Since the ground edge stays bounded away from zero,

$$
\boxed{\|\mathcal F_S(T)\|
\le C\left(\varepsilon+d\sum_{e\subset S}\|T_e\|\right).}
\tag{7}
$$

This is the quartet-specific version of the
[earlier mixed-output estimate](four-arm-ghz-distance-bound-2026-09-27.md).
In particular, $f=\|\mathcal F_4(T)\|\le C(\varepsilon+td)$.
An anchored edge has $\|T_e\|\le C_e(\varepsilon+d)$.

The cases $T=0$, $\varepsilon>td$, or $t=O(d)$ follow from
$|\lambda|\le\varepsilon+15t^3$. Henceforth assume

$$
0<t\le\delta\le1,\qquad \varepsilon\le td,\qquad f\le Ctd.
\tag{8}
$$

Anchored blocks are then $O(d)$. Condition 1 gives $t=O(d)$
and is already covered.

Write $X_r=T_{0r}$, $Y_r=T_{1r}$, $Z_{rs}=T_{rs}$ for
$r,s\in L=\{2,3,4,5\}$. Put

$$
C_{rs}=X_rY_s+X_sY_r,\qquad F_{rs}=GZ_{rs}+C_{rs}.
$$

The exact edge-removal identity and its projection perpendicular
to the core vector $G$ give

$$
H_6(T)=\sum_{\{r,s\}\subset L}F_{rs}Z_{L\setminus\{r,s\}}-GH_4(Z),
\qquad |\lambda|\le\varepsilon+f\|Z\|.
\tag{9}
$$

These identities need no invertibility. A projection perpendicular
to any one core vector retains at least squared binary GHZ norm
one, since the two outside GHZ words are orthogonal.
The identities were established in the
[single-edge package](single-invertible-edge-ghz-onset-2026-09-27.md).

## 4. A common anchored neighbor

Suppose $X_r,Y_r=O(d)$. For any other outside vertex $s$,

$$
\|G\|\|Z_{rs}\|
\le \|F_{rs}\|+\|X_r\|\|Y_s\|+\|X_s\|\|Y_r\|=O(td).
$$

Thus every block incident to $r$ is $O(d)$, including $Z_{rs}$.
Expand the full binary output at vertex $r$:

$$
H_6(T)=\sum_{j\ne r}T_{rj}\,
\mathcal F_{V\setminus\{r,j\}}(T).
$$

Every quartet on the right has norm at most $C(\varepsilon+td)$
by (7). Hence
$\|H_6(T)\|\le C(d\varepsilon+td^2)$, proving (1).
No projection or rank assumption is needed in this case.

## 5. A four-cycle of outside anchors

Assume $Z_{24},Z_{25},Z_{34},Z_{35}=O(d)$.
Put $U=Z_{23}$, $V=Z_{45}$, with $u=\|U\|\ge\|V\|=w$
after exchanging the pairs if necessary.
If $u\le L_0d$ for any fixed $L_0$, (9) proves (1).
Otherwise choose $L_0$ sufficiently large below.
Equation (7) on the outside quartet gives

$$
uw\le C(\varepsilon+d(u+w)+d^2),\qquad
w\le C(d+\varepsilon/u).
\tag{10}
$$

Let
$h_X^2=\|X_2\|^2+\|X_3\|^2$ and
$h_Y^2=\|Y_2\|^2+\|Y_3\|^2$.
From $C_{23}=F_{23}-GU$,

$$
\|C_{23}\|\ge\eta tu-Ctd\ge ctu,\qquad
\|C_{23}\|\le h_Xh_Y.
$$

Balance **all columns** of these four blocks with
$\alpha=(h_Y/h_X)^{1/2}$. Then

$$
a^2=h_Xh_Y\ge ctu,\qquad a\le t.
\tag{11}
$$

Use in section 2 the four pairs of columns indexed by site
$2$ or $3$ and its binary color. The response norm at $j=4,5$
is precisely the combined norm of $C_{2j},C_{3j}$.
All four outside cycle edges are small, so these responses are
$O(td)$. Equations (5)--(6) give

$$
(\widetilde X_j,\widetilde Y_j)=v k_j+e_j,\qquad
\|e_j\|\le Ctd/a.
\tag{12}
$$

Using all columns is essential: the row norms in the next output
estimate are the full norms $h_X,h_Y$, not norms of selected columns.

Apply (7) to the quartet $\{0,2,3,j\}$:

$$
\mathcal F_{\{0,2,3,j\}}=X_jU+X_2Z_{3j}+X_3Z_{2j}.
$$

Since the two cycle blocks are $O(d)$,

$$
u\|X_j\|\le C\varepsilon+Cd(h_X+\|X_j\|+u+d).
$$

Absorb the term $Cd\|X_j\|$ using $u>L_0d$. The corresponding
quartet rooted at 1 gives

$$
\|X_j\|\le C(\varepsilon/u+dh_X/u+d),\qquad
\|Y_j\|\le C(\varepsilon/u+dh_Y/u+d).
\tag{13}
$$

After balancing, the two components of $v$ have the same norm.
Thus (12)--(13), and $\min(\alpha,\alpha^{-1})\le1$, imply

$$
\begin{aligned}
\|k_j\|&\le
C\left(ad/u+\varepsilon/u+d+td/a\right)\\
&\le C(ad+\varepsilon)/u.
\end{aligned}
\tag{14}
$$

For the last step, (11) and $u\le t$ give
$a\ge\sqrt c\,u$ and $td/a\le c^{-1}ad/u$.
No lower bound on the smallest singular value of $G$ was used.

By (6), there is a unit rank-one core matrix $P$ such that

$$
C_{45}=P(k_4k_5)+R,\qquad
\boxed{u\|R\|\le Ctd^2+C\varepsilon.}
\tag{15}
$$

Indeed the left side is at most a constant times

$$
td^2+(td/a)\varepsilon+ut^2d^2/a^2.
$$

The last term is at most $c^{-1}td^2$ by (11).
Also $(td/a)^2\le c^{-1}td^2/u\le c^{-1}td\le c^{-1}$
because $u>d$ and $t,d\le1$. This proves (15).

## 6. Remove one output factor and keep the GHZ signal

Use the exact cancellation of the potentially large $GUV$ term:

$$
\begin{aligned}
H_6(T)={}&F_{23}V+C_{45}U\\
&+\sum_{\{r,s\}\in\{24,25,34,35\}}
F_{rs}Z_{L\setminus\{r,s\}}\\
&-G(Z_{24}Z_{35}+Z_{25}Z_{34}).
\end{aligned}
\tag{16}
$$

Project the core space perpendicular to $P$.
The $P(k_4k_5)U$ term vanishes, leaving $O(td^2+\varepsilon)$
by (15). The last two lines are $O(td^2)$. The first term is
at most $Ctd(d+\varepsilon/u)\le Ctd^2+C\varepsilon$.

For any unit core vector $P$,

$$
\|Q_P(b^6+c^6)\|^2
=2-|P_{bb}|^2-|P_{cc}|^2\ge1.
$$

Therefore $|\lambda|\le C\varepsilon+Ctd^2
\le C\varepsilon+C\delta^5$.
Only this one-dimensional projection is needed; the earlier
determinant-tangent plane estimate is not needed for this application.
This completes the theorem.

## 7. A ground-dependent reduction of the remaining axes

If both endpoint cofactor rows vanish, the outside weights
$w_{rs}=D_{rs}c_{rs}$ have zero row sums. Consequently

$$
w_{23}=w_{45},\quad w_{24}=w_{35},\quad w_{25}=w_{34},
\qquad w_{23}+w_{24}+w_{25}=0.
$$

At least one is nonzero by the
[ground cofactor fact](ghz-critical-direction-normal-form-2026-09-27.md).
Thus either all six outside edges are anchored or four form an
anchored cycle. This proves the stated zero-row corollary.

Let $B_D$ consist of ground edges $ij$ for which:

- $c_{ij}=0$;
- the endpoints have no common anchored neighbor;
- their four outside vertices have no anchored four-cycle.

Combine the theorem with the
[same-color, invertible-edge, and two-arm criteria](binary-adjugate-ghz-onset-2026-09-27.md).
The onset estimate is uniform when the normalized direction stays
a fixed positive distance from the $2|B_D|$ projective directions
given by one pure $bc$ or $cb$ cell on an edge in $B_D$.
The compactness argument is the same: cover every normalized
four-site-flat source outside this finite set by a controlled
neighborhood; away from the flat set, (7) and the cubic bound suffice.

Every remaining edge has at least one nonzero endpoint cofactor row.
For the exact ground fixture in the replay, the cofactor support is
the cycle $02,03,12,13$. Four edges are anchored, two have common
anchored neighbors, and one has an outside anchored cycle.
The eight other edges leave sixteen projective directions.
This count concerns that fixture, not every ground source.

The uncontrolled directions still have zero output themselves.
Their perturbations remain to be treated. More broadly, (1) is a
source-distance onset bound at full-support single-color limits;
it does not supply $\varepsilon\ge c|\lambda|^3$ or handle every
zero-output boundary relevant to the unrestricted rate law.
