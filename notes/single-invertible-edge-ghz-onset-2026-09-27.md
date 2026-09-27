# One uniformly invertible edge suffices for fifth-power GHZ onset

September 27, 2026. **Written proof with exact supporting checks; independent
audit pending.** The unrestricted square-root rate law remains open.

[Exact replay](../computations/single-invertible-edge-ghz-2026-09-27/README.md) ·
[Illustrated guide](../explainers/CRITICAL-DIRECTION-GEOMETRY.md) ·
[GHZ project](../research/ghz-rates/README.md)

## 1. Statement and the remaining directions

Let $A_0$ be a six-site single-ground-color source with all fifteen
ground entries nonzero and zero hafnian. Write

$$
H(A)=\lambda(a^6+b^6+c^6)+E,\qquad
\varepsilon=\|E\|,\qquad \delta=\|A-A_0\|,
$$

where $E$ is orthogonal to the ternary GHZ tensor. Let $T$ be the
binary non-ground part and $t=\|T\|$.

**Theorem.** Fix $\eta>0$. Near $A_0$ there are constants $C_1,C_2$
such that

$$
\boxed{|\lambda|\le C_1\varepsilon+C_2\delta^5}
\tag{1}
$$

whenever $T=0$ or one edge block $G=T_{01}$, after relabelling, satisfies

$$
\sigma_{\min}(G)\ge\eta t.
\tag{2}
$$

All other blocks are unrestricted. In particular, every other edge
may become arbitrarily small relative to $G$.

Combined with the
[two-comparable-arm theorem](coherent-two-arm-ghz-onset-2026-09-27.md),
this gives a uniform onset bound away from normalized sources
supported on a single **rank-one** edge. Those are the remaining
directions for this onset argument at full-support single-color
limits. The error-versus-signal estimate required for the unrestricted
square-root law remains open, including on the controlled families.

The proof uses a bilinear response lemma and a sharp projection gap
for a plane tangent to the rank-one matrix locus.

## 2. Remove one edge from the matching output

Let $L=\{2,3,4,5\}$. Write $X_r=T_{0r}$, $Y_r=T_{1r}$,
$Z_{rs}=T_{rs}$, and

$$
C_{rs}=X_rY_s+X_sY_r,\qquad F_{rs}=GZ_{rs}+C_{rs}.
$$

Products always place factors at their labelled sites.
Let $z^2=\sum_{r<s}\|Z_{rs}\|^2$ and
$f=\|\mathcal F_4(T)\|$, the norm of all four-site responses.
The fifteen six-site matchings give the exact identity

$$
\boxed{H_6(T)=\sum_{\{r,s\}\subset L}F_{rs}Z_{uv}-G H_4(Z),}
\qquad \{u,v\}=L\setminus\{r,s\}.
\tag{3}
$$

Each outside perfect matching occurs twice in the sum, explaining
the subtraction.

Project the two-site space at $0,1$ perpendicular to the matrix $G$,
viewed as a vector. This removes the last term. For
$\Delta_2=b^6+c^6$, the retained squared norm is

$$
2-\frac{|G_{bb}|^2+|G_{cc}|^2}{\|G\|^2}\ge1.
$$

Cauchy--Schwarz in the sum of six terms therefore gives, for any
nonzero $G$ regardless of matrix rank,

$$
\boxed{|\lambda|\le\varepsilon+fz.}
\tag{4}
$$

Put $d=\delta^2$. The actual mixed-output equations and ground
cofactors give

$$
f\le C(\varepsilon+td),\qquad
\|H_4(Z)\|\le C(\varepsilon+dz),\qquad
\|T_e\|\le C_e(\varepsilon+d)\quad\text{if }c_e\ne0.
\tag{5}
$$

Here $c_e$ is the ground hafnian cofactor at $A_0$.
The second bound keeps only ground color at sites $0,1$.
Each of the twelve remainder terms has two mixed edges and a
binary edge entirely in $L$; its size involves $z$, not $t$.
These are the same mixed-output and anchored-edge arguments used
in the [earlier onset proof](four-arm-ghz-distance-bound-2026-09-27.md).

The cases $T=0$, $\varepsilon>td$, or $t=O(d)$ are immediate from
$|\lambda|\le\varepsilon+15t^3$ and $t\le\delta$.
Hence assume $\varepsilon\le td$ and $t>d$.
Then $f\le Ctd$, and every anchored edge is $O(d)$.
Equation (4) already proves (1) whenever $z=O(d)$.

## 3. A conditioned bilinear response leaves only one product term

We first prove a lemma independent of the ground source.
Let $x_1,x_2\in U=\mathbb C^2$ and $y_1,y_2\in V=\mathbb C^2$.
Suppose

$$
C=x_1y_2^{\mathsf T}+x_2y_1^{\mathsf T},\qquad
c=\|C\|>0,\qquad \sigma_{\min}(C)\ge\kappa c.
\tag{6}
$$

For an outside color space $W$, let
$X_W\in U\otimes W$, $Y_W\in V\otimes W$ and define

$$
L_i(X_W,Y_W)=x_iY_W+X_Wy_i,\qquad
r_W^2=\|L_1(X_W,Y_W)\|^2+\|L_2(X_W,Y_W)\|^2.
$$

**Bilinear response lemma.** One can choose $i\in\{1,2\}$, depending
only on the four fixed vectors, with $P=x_i y_i^{\mathsf T}\ne0$,
such that for any two outside spaces $W,Z$,

$$
X_WY_Z+X_ZY_W=P M_{WZ}+R_{WZ},\qquad
\|R_{WZ}\|\le C_\kappa\,\frac{r_Wr_Z}{c},
\tag{7}
$$

for some tensor $M_{WZ}$ on $W,Z$. Moreover

$$
\det(C+sP)=\det C,\qquad
\operatorname{tr}(\operatorname{adj}C\,P)=0.
\tag{8}
$$

To prove it, scale all $x$ and $X$ vectors by a positive factor
and all $y$ and $Y$ vectors by its reciprocal. This preserves
$C$, both responses, $P$, and the output in (7).
First make
$\sum_i\|x_i\|^2=\sum_i\|y_i\|^2=a^2$.
Put $\alpha_i=\|x_i\|/a$, $\beta_i=\|y_i\|/a$, and
$p=\max_i\alpha_i\beta_i$. The reverse triangle inequality and
Hadamard's determinant inequality give

$$
\frac{c^2}{a^4}\ge
(\alpha_1\beta_2-\alpha_2\beta_1)^2
=1-(\alpha_1\beta_1+\alpha_2\beta_2)^2
\ge1-4p^2,
$$

$$
p^2\ge\frac{|\det C|}{a^4}
\ge\kappa^2\frac{c^2}{a^4}.
$$

Thus $p\ge\kappa/\sqrt{1+4\kappa^2}\ge\kappa/2$.
Here $\kappa\le1/\sqrt2$ whenever (6) is nonvacuous.
Choose the index attaining $p$, relabel it 1, and rebalance once
more so $\|x_1\|=\|y_1\|=b$.
The other two vector norms are at most $K_\kappa b$ for a constant
depending only on $\kappa$; for example $K_\kappa=2/\kappa$ suffices.
Consequently $c\le2K_\kappa b^2$.

The map $(X,Y)\mapsto x_1Y+Xy_1$ has kernel
$\mathbb C(x_1,-y_1)$ on local vectors.
Its nonzero singular values are $b,b,\sqrt2b$.
Writing $v=(x_1,-y_1)/(\sqrt2b)$, we may therefore decompose

$$
(X_W,Y_W)=v k_W+e_W,\qquad \|e_W\|\le r_W/b.
$$

The second response on $v$ is
$(x_1y_2^{\mathsf T}-x_2y_1^{\mathsf T})/(\sqrt2b)$.
Its numerator $D$ satisfies $\det D=-\det C$, so

$$
\|L_2(v)\|=\frac{\|D\|}{\sqrt2b}
\ge\frac{\sqrt{|\det C|}}b\ge\frac{\kappa c}b.
$$

Using the bound on $x_2,y_2$ now gives
$\|k_W\|\le C_\kappa b r_W/c$.
Expand the left side of (7) using this decomposition at $W,Z$.
Its leading term has factor $P$, and the remainder is bounded by

$$
C\bigl(\|k_W\|\|e_Z\|+\|k_Z\|\|e_W\|+\|e_W\|\|e_Z\|\bigr)
\le C_\kappa r_Wr_Z/c.
$$

Finally, with $A=[x_1,x_2]$, $B=[y_1,y_2]$,

$$
C+s x_1y_1^{\mathsf T}
=A\begin{pmatrix}s&1\\1&0\end{pmatrix}B^{\mathsf T}.
$$

Its determinant is independent of $s$. The other choice of index
has the same property, proving (8).

## 4. A sharp GHZ gap for a determinant-tangent plane

**Projection lemma.** Let $P=uv^{\mathsf T}$ be a nonzero rank-one
binary matrix, and let $C$ be independent of $P$, with
$\operatorname{tr}(\operatorname{adj}C\,P)=0$.
Let $Q$ be the orthogonal projection perpendicular to
$\operatorname{span}\{P,C\}$ on two selected sites. Then

$$
\boxed{\|Q(b^6+c^6)\|^2\ge\tfrac12.}
\tag{9}
$$

The constant is sharp.

Normalize $u,v$ to unit vectors, and write
$x=|u_b|^2$, $y=|v_b|^2$.
For two-by-two matrices the determinant's polarized form is symmetric,
so the trace condition also reads
$\operatorname{tr}(\operatorname{adj}P\,C)=0$.
Thus $C$ lies in the tangent space

$$
\operatorname{span}\{uv,\ u^\perp v,\ uv^\perp\}.
$$

After removing its component along $P$, the second unit vector
of the plane lies in the last two-dimensional span.
The diagonal-coordinate squared norm of $P$ is
$p=xy+(1-x)(1-y)$.
On the orthonormal basis $u^\perp v,uv^\perp$, the diagonal-coordinate
compression has diagonal entries $1-p$ and off-diagonal modulus
$2\sqrt{x(1-x)y(1-y)}$.
The total diagonal mass removed by the plane is therefore at most

$$
p+(1-p)+2\sqrt{x(1-x)y(1-y)}\le\tfrac32.
$$

The two GHZ words are orthogonal on the other four sites.
Their original squared norm is two, so (9) follows.
Equality holds for $P$ proportional to the all-ones matrix and
$C=\operatorname{diag}(1,-1)$.

This lemma controls a specific target even when the norm of the
discarded product output is large.

## 5. A nonzero endpoint cofactor row

Return to $G=T_{01}$ satisfying (2).
If $c_{01}\ne0$, then $t=O(d)$, already treated.
Suppose an endpoint cofactor row is nonzero, say at 0.
The ground identity

$$
\sum_{j\ne0}D_{0j}c_{0j}=\operatorname{haf}D=0
$$

and $c_{01}=0$ give two distinct outside sites $r,s$ with
$X_r,X_s=O(d)$. Call the remaining sites $u,v$.

For $a\in\{r,s\}$ and any other outside site $b$,

$$
GZ_{ab}+X_bY_a=F_{ab}-X_aY_b=O(td).
$$

The [opposite-pairing singular-value estimate](two-invertible-arm-ghz-bound-2026-09-27.md#2-a-matrix-rank-estimate-for-opposite-pairings)
and (2) give

$$
\|Z_{ab}\|=O(d),\qquad \|X_b\|\|Y_a\|=O(td).
\tag{10}
$$

Thus only $Z_{uv}$ may exceed order $d$.
Multiply
$\|G\|\|Z_{uv}\|\le f+\|X_u\|\|Y_v\|+\|X_v\|\|Y_u\|$
by $\|Y_a\|$ and use (10). Since all blocks have norm at most $t$,

$$
\|Z_{uv}\|\|Y_r\|+\|Z_{uv}\|\|Y_s\|=O(td).
$$

In (3), project perpendicular to $G$.
All terms except $F_{rs}Z_{uv}$ are $O(td^2)$.
The remaining term equals the projection of
$(X_rY_s+X_sY_r)Z_{uv}$ and is also $O(td^2)$.
This proves (1) when either endpoint row is nonzero.

## 6. Zero endpoint rows leave a four-cycle of anchors

Suppose both endpoint cofactor rows vanish.
For the four outside vertices put $w_{rs}=D_{rs}c_{rs}$.
Their row sums vanish. Solving the four linear equations gives

$$
w_{23}=w_{45},\quad w_{24}=w_{35},\quad w_{25}=w_{34},
\qquad w_{23}+w_{24}+w_{25}=0.
\tag{11}
$$

Not all cofactors vanish: every five-site subset has an internal
nonzero cofactor, by the
[ground cofactor fact](ghz-critical-direction-normal-form-2026-09-27.md).
Because all $D_{rs}\ne0$, either all six outside edges are anchored,
or four form an anchored cycle and the remaining opposite pair
may be unanchored.
In the first case $z=O(d)$ and (4) finishes the proof.

Relabel the second case so the potentially large edges are
$U=Z_{23}$, $V=Z_{45}$, with $u=\|U\|\ge v=\|V\|$.
The other four $Z$ blocks are $O(d)$.
If $u\le Ld$, (4) applies again.
Otherwise choose $L$ sufficiently large depending on $\eta$ and
the preceding constants.
The outside quartet equation in (5) gives

$$
uv\le C(\varepsilon+dz+d^2),\qquad
v\le C(d+\varepsilon/u).
\tag{12}
$$

Here $z\le u+v+Cd\le2u+Cd$.

Choose an entry $\zeta=U_{\alpha\beta}$ with $|\zeta|\ge u/2$.
Fix these colors at outside sites 2,3, and let $x_1,y_1$ be the
corresponding columns of $X_2,Y_2$, and $x_2,y_2$ those of $X_3,Y_3$.
Their two-by-two core matrix satisfies

$$
C=x_1y_2^{\mathsf T}+x_2y_1^{\mathsf T}
=-\zeta G+(F_{23})_{\alpha\beta}.
$$

By (2), $f=O(td)$, and $u>Ld$, this matrix has
$c=\|C\|\asymp tu$ and $\sigma_{\min}(C)\ge\kappa c$
for some fixed $\kappa>0$.

All four cross-cycle $Z$ blocks are $O(d)$.
The corresponding equations $C_{ab}=F_{ab}-GZ_{ab}$,
restricted to the chosen colors at sites 2,3,
give $r_4,r_5=O(td)$ in the bilinear response lemma.
It follows that

$$
C_{45}=P M+R,\qquad
\|R\|\le Ctd^2/u,\qquad
\operatorname{tr}(\operatorname{adj}C\,P)=0,
\tag{13}
$$

where $P$ is nonzero and rank one.

Use the projection $Q$ from section 4 for this $C,P$.
It need not annihilate $G$.
Instead rewrite (3), cancelling the $GUV$ term exactly:

$$
\begin{aligned}
H_6(T)={}&F_{23}V+C_{45}U\\
&+\sum_{\{a,b\}\in\{24,25,34,35\}}F_{ab}Z_{L\setminus\{a,b\}}\\
&-G(Z_{24}Z_{35}+Z_{25}Z_{34}).
\end{aligned}
\tag{14}
$$

After projection, the second term is $O(td^2)$ by (13).
The last two lines are $O(td^2)$ because their outside edges are
anchored. The first term is at most

$$
Ctd(d+\varepsilon/u)
\le Ctd^2+C\varepsilon,
$$

using $u>Ld$ and $t\le1$.
Equation (9) retains at least squared GHZ norm $1/2$, so
$|\lambda|\le C\varepsilon+Ctd^2\le C\varepsilon+C\delta^5$.
This completes the theorem.

## 7. The remaining onset directions are single product edges

Let $\mathcal E_1$ be the closed set of normalized sources supported
on a single rank-one edge.
For every fixed $\rho_0>0$, the fifth-power estimate is uniform
when $T=0$ or $\operatorname{dist}(T/t,\mathcal E_1)\ge\rho_0$.

To see this, consider zeros of $\mathcal F_4$ on that compact set.
A zero with two adjacent nonzero edges is covered by the
two-comparable-arm theorem. Otherwise its support is a matching;
four-site flatness forces it to have just one edge.
That edge must have rank two and is covered by the present theorem.
A finite cover gives uniform constants. On the remaining compact
set the four-site response is bounded below; (5) forces either
$t=O(d)$ or $t^2=O(\varepsilon)$, and the elementary cubic bound
finishes the argument.

This narrows the onset problem, but does not identify every zero-output
boundary relevant to the rate law or prove the required lower bound
on error relative to GHZ amplitude.
