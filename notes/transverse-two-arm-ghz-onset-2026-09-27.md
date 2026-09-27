# Two-arm GHZ onset beyond matrix invertibility

September 27, 2026. **Written proof with exact supporting checks; independent
audit pending.** The unrestricted square-root rate law remains open.

[Exact replay](../computations/transverse-two-arm-ghz-2026-09-27/README.md) ·
[Illustrated guide](../explainers/CRITICAL-DIRECTION-GEOMETRY.md) ·
[GHZ project](../research/ghz-rates/README.md)

## 1. The sharper two-arm theorem

Let $A_0$ be a six-site, single-ground-color source with all fifteen
ground entries nonzero and zero hafnian. For a nearby ternary source write

$$
H(A)=\lambda(a^6+b^6+c^6)+E,\qquad
E\perp(a^6+b^6+c^6),\qquad
\varepsilon=\|E\|,\qquad \delta=\|A-A_0\|.
$$

Let $T$ be its binary non-ground part and $t=\|T\|$. Choose two arms
$G_1=T_{01}$ and $G_2=T_{02}$. On local color vectors define

$$
\Phi_G(v_1,v_2)=G_1v_2+G_2v_1,
\qquad
\Phi_G:L_1\oplus L_2\longrightarrow L_0\otimes L_1\otimes L_2.
\tag{1}
$$

All norms are Hilbert norms with the standard tensor-product convention.

**Theorem.** Fix $\eta>0$. Near $A_0$, there are constants $C_1,C_2$
such that

$$
\boxed{|\lambda|\le C_1\varepsilon+C_2\delta^5}
\tag{2}
$$

whenever $T=0$ or $\sigma_{\min}(\Phi_G)\ge\eta t$.
The other source blocks are unrestricted. No ground cofactor row is
required to be nonzero at a specified endpoint.

For two nonzero arms, $\Phi_G$ is injective except when both arms
have rank one and share the same center line. This was proved in the
[two-arm kernel classification](two-invertible-arm-ghz-bound-2026-09-27.md#3-the-two-arm-attachment-kernel).
Consequently (2) holds in a neighborhood of every normalized two-arm
star with either an invertible arm or distinct rank-one center lines.
Constants are uniform on compact families avoiding the exceptional
shared-line pairs.

This strengthens the earlier invertible-arm theorem: a single invertible
arm now suffices without an endpoint-cofactor hypothesis, and neither
arm needs to be invertible when their rank-one center lines differ.

There is also a quantitative estimate at the exceptional pairs.
Let $S$ be a normalized two-arm star with two nonzero rank-one arms
sharing a center line, and put $B=T_{12}$, $\beta=\|B\|$.
In a neighborhood of this direction,

$$
\boxed{
|\lambda|\le C\varepsilon+C\,t(\beta+\delta^2)^2
\le C'\varepsilon+C'\delta^5+C't\beta^2.}
\tag{3}
$$

In particular, (2) also holds there if $\beta=O(\delta^2)$ or
$\beta^2=O(\varepsilon)$. The constants in these conditional statements
may depend on the constants in the $O$ assumptions.

## 2. Actual output constraints

Let $K=\{0,1,2\}$ and $L=\{3,4,5\}$. Write
$H_r=T_{0r}$, $Y_{ir}=T_{ir}$ for $i=1,2$, and $Z_{rs}=T_{rs}$.
Put $h_r=\|H_r\|$, $y_r^2=\|Y_{1r}\|^2+\|Y_{2r}\|^2$, and
$z_{rs}=\|Z_{rs}\|$.

The previous mixed-output argument gives

$$
f:=\|\mathcal F_4(T)\|\le C(\varepsilon+t\delta^2),\qquad
\|T_e\|\le C_e(\varepsilon+\delta^2)
\quad\text{if the ground cofactor }c_e\ne0.
\tag{4}
$$

Call these latter edges anchored. Every five-site subset has an
internal anchored edge. If $T=0$ or $\varepsilon>t\delta^2$, (2)
follows immediately from $|\lambda|\le\varepsilon+15t^3$ and
$t\le\delta\le1$. Hence assume

$$
\varepsilon\le t\delta^2,\qquad f\le Ct\delta^2.
\tag{5}
$$

All anchored blocks are now $O(\delta^2)$.
The attachment and pair responses are

$$
F_r=G_1Y_{2r}+G_2Y_{1r}+H_rB,
\tag{6}
$$

$$
R^i_{rs}=G_iZ_{rs}+H_rY_{is}+H_sY_{ir},\quad i=1,2,
\tag{7}
$$

$$
Q_{rs}=BZ_{rs}+Y_{1r}Y_{2s}+Y_{1s}Y_{2r}.
\tag{8}
$$

Their norms are bounded by $f$. Equation (8) has the sharper bound

$$
\boxed{\|Q_{rs}\|\le
C\bigl(\varepsilon+\delta^2(\beta+y_r+y_s+z_{rs})\bigr).}
\tag{9}
$$

Indeed, the corresponding output words have ground color at $0$ and
the third outside site. Their leading three matching terms are the
nonzero nearby ground edge times $Q_{rs}$. Each of the other twelve
terms has two mixed ground/non-ground edges, each $O(\delta)$, and
one binary edge inside $\{1,2,r,s\}$. Only $B,Y_r,Y_s,Z_{rs}$ can be
that binary edge. Divide by the ground edge, which stays bounded away
from zero. This proves (9) without using either strong arm in the remainder.

## 3. Rescale the weak triangle edge

Assume the lower singular-value hypothesis of section 1.
The map (1), tensored with the outside color space, and (6) give

$$
y_r\le C\left(\delta^2+\frac{h_r\beta}{t}\right)
\le C(\delta^2+\beta).
\tag{10}
$$

If $\beta\le L_0\delta^2$, for a fixed constant $L_0$, all $y_r$ are
$O(\delta^2)$. Equation (7), using either arm, then makes every
$z_{rs}=O(\delta^2)$. The six-site matching split in section 5 yields
$\|H_6(T)\|\le Ct\delta^4$.
If a strong arm is anchored, its norm is at least $\eta t$, forcing
$t=O(\delta^2)$ and giving the stronger elementary sixth-power bound.

Choose $L_0$ sufficiently large and consider $\beta>L_0\delta^2$.
If $B$ were anchored this inequality would be impossible. Thus all
three internal ground cofactors vanish in the remaining case.
Set $\rho=\beta/t\in(0,1]$ and define a rescaled binary source:

$$
\widetilde G_i=G_i,\quad
\widetilde B=B/\rho,\quad
\widetilde H_r=\rho H_r,\quad
\widetilde Y_{ir}=Y_{ir},\quad
\widetilde Z_{rs}=\rho Z_{rs}.
\tag{11}
$$

These are site scalings with factors
$\sqrt\rho$ at $0,3,4,5$ and $1/\sqrt\rho$ at $1,2$. Therefore

$$
H_6(\widetilde T)=\rho H_6(T).
\tag{12}
$$

The normalized triangle $\widetilde T[K]/t$ has all three edge norms
bounded below uniformly: the first two by $\eta$, the third by one.
It belongs to a compact family of nonzero triangles.
Its attachment vector is
$X'_r=(\rho H_r,Y_{1r},Y_{2r})$; by (10),

$$
x'_r:=\|X'_r\|\le C\beta.
\tag{13}
$$

The transformed responses on $K\cup\{r\}$ remain $F_r$.
For a pair of outside sites, the transformed responses at core edges
$01,02$ are $\rho R^1_{rs},\rho R^2_{rs}$, while the response at $12$
remains $Q_{rs}$. These unequal scaling factors are essential.

## 4. A weighted pair bound with the correct small scale

Apply the [triangle pair lemma](triangle-attachment-ghz-bound-2026-09-27.md#3-pair-control-from-the-impossibility-of-a-missing-edge)
to the normalized rescaled triangle, the two attachments $X'_r,X'_s$,
and the outside-edge variable $t\widetilde Z_{rs}=\beta Z_{rs}$.
Its constant is uniform over the compact family above.
The lemma uses an anchored edge in $K\cup\{r,s\}$, whose existence
follows from the five-site cofactor fact and the vanishing internal
cofactors.

The two arm-containing pair responses are $O(\beta\delta^2)$ by (5).
Equations (9)--(10) bound the remaining response by
$C(\varepsilon+\beta\delta^2+\delta^2z_{rs})$.
The single-attachment response divided by $t$ is $O(\delta^2)$,
as is every selected anchored component of $X'_r$.
Their contributions multiplied by another attachment are
$O(\beta\delta^2)$ by (13). If the selected anchor is $rs$, its
contribution is $\beta z_{rs}=O(\beta\delta^2)$.

The pair lemma consequently gives

$$
x'_rx'_s+\beta z_{rs}
\le C(\varepsilon+\beta\delta^2+\delta^2z_{rs}).
$$

Increasing $L_0$ absorbs the last term. With
$\kappa=\delta^2+\varepsilon/\beta$, this yields

$$
\boxed{x'_rx'_s\le C\beta\kappa,\qquad z_{rs}\le C\kappa.}
\tag{14}
$$

Using only the coarser $f$ bound in the leaf quartet would replace
$\beta$ by $t$ and lose the desired fifth power after undoing (11).

## 5. Shared anchors and one local projection

Since all internal ground cofactors vanish, a core vertex $i$ has
nonzero ground cofactors to two distinct outside sites, say $r,s$.
This is the ground selection argument in
[section 4 of the triangle proof](triangle-attachment-ghz-bound-2026-09-27.md#4-two-attachments-share-an-anchored-core-component).
Thus the $i$ components of $X'_r,X'_s$ are $O(\delta^2)$.

Let $j,k$ be the other core sites and $C=\widetilde T[K]/t$.
The two-vector map
$N_C(v_j,v_k)=v_jC_{ik}+v_kC_{ij}$ has kernel dimension at most one
whenever both edges are nonzero.
On our compact family, every singular value except possibly the
smallest is uniformly positive.
Choose a unit right singular vector $v=(v_j,v_k)$ for the smallest
singular value. Equations (5)--(6) give

$$
X'_r=K_r+e_r,\qquad X'_s=K_s+e_s,\qquad
\|e_r\|+\|e_s\|\le C\delta^2,
\tag{15}
$$

where $(K_\ell)_i=0$, $(K_\ell)_j=v_jw_\ell$, and
$(K_\ell)_k=v_kw_\ell$ for some outside vectors $w_\ell$.
This decomposition is valid even when the smallest singular value
is positive; no kernel persistence is assumed.

Choose a nonzero component of $v$ and project perpendicular to it
at that one core site. Call the projection $P$.
The six-cross-edge permanent
$\operatorname{Perm}_3(K_r,K_s,X'_u)$ is killed exactly:
the first two attachments must occupy $j,k$.
If one component of $v$ is zero, this permanent is already zero.

Every six-site matching is accounted for by

$$
H_6(\widetilde T)
=\sum_{\{r,s\}\subset L}\widetilde Z_{rs}F_u
+\operatorname{Perm}_3(X'_3,X'_4,X'_5),
\qquad \{u\}=L\setminus\{r,s\}.
\tag{16}
$$

The first sum is bounded by $C\beta\kappa\delta^2$.
Using (14)--(15), the error on replacing two attachments by $K_r,K_s$
is at most

$$
C\delta^2\bigl(x'_sx'_u+(x'_r+C\delta^2)x'_u\bigr)
\le C\beta\kappa\delta^2.
$$

Here (13) bounds the extra $\delta^4x'_u$ term.
It follows that $\|PH_6(\widetilde T)\|\le C\beta\kappa\delta^2$.
For every rank-one local orthogonal projection in the binary palette,

$$
\|P(b^6+c^6)\|^2=1.
\tag{17}
$$

Apply (12) and use the actual binary target equation.
Dividing the resulting estimate by $\rho$ gives

$$
|\lambda|\le\varepsilon+Ct\delta^4+
C\frac{t\delta^2}{\beta}\varepsilon
\le C_1\varepsilon+C_2\delta^5.
$$

The last inequality uses $\beta>L_0\delta^2$ and $t\le\delta\le1$.
Together with the elementary cases, this proves (2).

## 6. A residual estimate at the shared-center rank-one pairs

Now let the normalized arms approach a fixed exceptional pair.
The normalized map $\Phi_{G/t}$ has exactly one zero singular value
at that pair; all the others stay bounded below nearby.
Its smallest right singular vector $v=(v_1,v_2)$ has both components
bounded away from zero. Applying the same decomposition to (6) gives

$$
Y_{ir}=v_iw_r+e_{ir},\qquad
\|e_r\|\le C(\beta+\delta^2)=:C h.
\tag{18}
$$

Consider the complementary map

$$
\mathcal M_{G/t,v}(Z,W)=
\bigl((G_1/t)Z+v_1W,\ (G_2/t)Z+v_2W\bigr).
\tag{19}
$$

At the limiting kernel, the relation
$G_1v_2+G_2v_1=0$ gives
$G_1/t=u v_1$, $G_2/t=-u v_2$ for some nonzero $u$.
Then the two equations in (19) are
$v_1(uZ+W)$ and $v_2(-uZ+W)$.
Their simultaneous vanishing forces $Z=W=0$.
The map is consequently bounded below uniformly nearby, also after
tensoring with the two outside color spaces.

Insert (18) into the pair responses (7). The map (19) acts on

$$
Z=Z_{rs},\qquad W=(H_rw_s+H_sw_r)/t.
$$

The remainder is bounded by
$C\delta^2+(h_r/t)\|e_s\|+(h_s/t)\|e_r\|\le Ch$.
Hence

$$
z_{rs}\le Ch,\qquad
\|H_rw_s+H_sw_r\|\le Cth.
\tag{20}
$$

Project at leaf 1 perpendicular to $v_1$.
For each fixed outside site $s$ assigned to leaf 1, the permanent
contribution after projection is

$$
(Pe_{1s})\bigl(H_rY_{2u}+H_uY_{2r}\bigr),
\qquad \{r,u\}=L\setminus\{s\}.
$$

Its bracket is
$v_2(H_rw_u+H_uw_r)+H_re_{2u}+H_ue_{2r}$, with norm $O(th)$
by (18)--(20). Thus the projected permanent is $O(th^2)$.
The outside-edge sum is at most $Chf\le Cth\delta^2\le Cth^2$.
Equation (17) now proves (3). This argument does not require a
nonzero ground cofactor at a particular vertex.

## 7. The remaining onset shapes

Let $\mathcal S_{\rm coh}$ be the closed set of normalized binary
six-site sources that are either supported on a single edge, with
arbitrary matrix rank, or on two rank-one arms with a common center line.

For every fixed $\rho_0>0$, (2) holds uniformly near $A_0$ when $T=0$
or $\operatorname{dist}(T/t,\mathcal S_{\rm coh})\ge\rho_0$.
Combine the present theorem with the previous triangle, four-core,
and three-arm theorems. The flat-support classification leaves no
other normalized simultaneous critical zero. The same finite-cover
and residual argument used in the earlier onset notes proves uniformity.

Near a shared-center pair, (3) further shows that a sequence violating
the fifth-power estimate must have $t\beta^2$ large relative to
$\varepsilon+\delta^5$. In particular the closing edge cannot remain
of order $\delta^2$, nor can its squared norm be controlled by
$\varepsilon$.

These are source-distance estimates at full-support single-color limits.
The error-versus-signal inequality $\varepsilon\ge c|\lambda|^3$ needed
for the unrestricted square-root law is still open, including on the
families whose onset is controlled here.

## 8. Why the local projection matters

There is an exact auxiliary family with transverse rank-one arms for
which the whole binary output is larger than the fifth power.
Use binary colors $b=e_0,c=e_1$, outside sites $3,4,5$, and

$$
\begin{aligned}
G_1&=\tau^4 e_0e_0^{\mathsf T},&
G_2&=\tau^4 e_1e_0^{\mathsf T},&
B&=\tau^6 e_0e_0^{\mathsf T},\\
H_3=H_4&=\tau^5 e_0e_0^{\mathsf T},&
H_5&=\tau^5 e_1e_0^{\mathsf T},\\
Y_{23}=Y_{24}=Y_{15}&=-\tau^7e_0e_0^{\mathsf T}.
\end{aligned}
$$

All other blocks vanish. Direct matching expansion gives

$$
\|T\|^2=2\tau^8+3\tau^{10}+\tau^{12}+3\tau^{14},\qquad
\|\mathcal F_4(T)\|^2=8\tau^{24}+2\tau^{28},
$$

$$
F_r=0\quad(r=3,4,5),\qquad H_6(T)=2\tau^{19}b^6.
$$

The normalized two-arm map stays uniformly injective.
The exact replay supplies a full-support zero ground with cofactor
support $\{13,14,35,45\}$, so every anchored binary block is zero.
The leaf-sensitive responses in (9) are of order $\tau^{14}$ or zero.
Thus the auxiliary bounds hold with $\delta$ comparable to $\tau^4$,
but the full output has order $\delta^{19/4}$, not $\delta^5$.
Projection at leaf 1 kills it while retaining unit binary GHZ norm.

This is not a GHZ counterexample: the output has no $c^6$ component.
It explains why a full-output norm estimate cannot replace the
target-sensitive projection in the auxiliary argument.
