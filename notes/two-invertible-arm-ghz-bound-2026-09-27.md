# Two invertible arms suffice for fifth-power GHZ onset

September 27, 2026. **Written proof with exact supporting checks; independent
audit pending.** The unrestricted square-root rate law remains open.

[Exact replay](../computations/two-arm-ghz-onset-2026-09-27/README.md) ·
[Illustrated guide](../explainers/CRITICAL-DIRECTION-GEOMETRY.md) ·
[GHZ project](../research/ghz-rates/README.md)

## 1. Statement

Let $A_0$ be a six-site source using only the ground color $a$, with
all fifteen ground entries $D_{ij}\ne0$ and $\operatorname{haf}D=0$.
For a nearby ternary source write

$$
H(A)=\lambda(a^6+b^6+c^6)+E,\qquad E\perp(a^6+b^6+c^6),\qquad
\varepsilon=\|E\|,\quad\delta=\|A-A_0\|.
$$

Let $T$ be the binary non-ground part and $t=\|T\|$.

**Theorem.** Fix $\eta>0$. Near $A_0$ there are constants $C_1,C_2$
such that

$$
\boxed{|\lambda|\le C_1\varepsilon+C_2\delta^5}
\tag{1}
$$

whenever $T=0$, or two arms at a common vertex satisfy

$$
\sigma_{\min}(T_{01})\ge\eta t,\qquad
\sigma_{\min}(T_{02})\ge\eta t.
\tag{2}
$$

Here the blocks are binary $2\times2$ matrices, and
$\sigma_{\min}$ is the smaller singular value.
The other source blocks are unrestricted. No prior closeness to a
flat two-arm star is required, and the center's entire ground
cofactor row is allowed to vanish.

In particular, every normalized two-arm star with two invertible
blocks has a neighborhood on which (1) holds. This covers all such
stars, with constants uniform on compact families bounded away from
singular arm matrices. It does not cover arbitrary rank-one arms.

**Cofactor-sensitive refinement.** One may instead assume
$\sigma_{\min}(T_{01})\ge\eta t$ and $\|T_{02}\|_F\ge\eta t$,
provided at least one of the ground cofactor rows at sites $0,1$
is nonzero. Thus the second arm may have rank one when the ground
equations select an endpoint of the invertible arm.

## 2. A matrix-rank estimate for opposite pairings

Let $G\in L_0\otimes L_1$, $Y\in L_2\otimes L_r$,
$H\in L_0\otimes L_r$, and $B\in L_1\otimes L_2$.
All spaces are finite-dimensional complex Hilbert spaces. Form

$$
R=G_{01}Y_{2r}+H_{0r}B_{12}.
\tag{3}
$$

Define the singular-value tail

$$
\tau(G)^2=\|G\|_F^2-\sigma_{\max}(G)^2
=\sum_{j\ge2}\sigma_j(G)^2.
$$

It is positive exactly when $G$ has matrix rank at least two.
For binary blocks it equals $\sigma_{\min}(G)^2$.

**Separation lemma.** If $\tau(G)>0$, then

$$
\boxed{
\|Y\|_F\le\frac{\|R\|}{\tau(G)},\qquad
\|H\|_F\|B\|_F
\le\left(1+\frac{\|G\|_F}{\tau(G)}\right)\|R\|.
}
\tag{4}
$$

To prove it, flatten the tensor across $(0,r)\mid(1,2)$.
The second term in (3) is a rank-one matrix; the first, up to index
permutations, is a Kronecker product of $G$ and $Y^{\mathsf T}$.
Call this first matrix $M$. Then

$$
\|M\|_F=\|G\|_F\|Y\|_F,\qquad
\|M\|_{\mathrm{op}}=\sigma_{\max}(G)\sigma_{\max}(Y).
$$

Project on the $(0,r)$ side perpendicular to the vector representing $H$.
This kills the second term. A projection onto one row direction
can remove at most $\|M\|_{\mathrm{op}}^2$ of the squared Frobenius
norm. Hence

$$
\|R\|^2\ge\|G\|_F^2\|Y\|_F^2
-\sigma_{\max}(G)^2\sigma_{\max}(Y)^2
\ge\tau(G)^2\|Y\|_F^2.
\tag{5}
$$

If $H=0$, the same inequality is immediate.
The triangle inequality gives
$\|H\|_F\|B\|_F\le\|R\|+\|G\|_F\|Y\|_F$,
proving the second assertion.

The dependence on $\tau(G)$ is necessary. For
$G=\operatorname{diag}(1,s)$ with $0\le s\le1$, take $Y=e_0e_0^{\mathsf T}$,
$H=e_0e_0^{\mathsf T}$, and $B=-e_0e_0^{\mathsf T}$.
Their first components cancel, leaving $\|R\|=|s|$ and $\|Y\|=1$.
At $s=0$ the response vanishes with all four blocks nonzero.
This also proves sharpness of the first constant in (4).

## 3. The two-arm attachment kernel

For two arbitrary nonzero arms $G_1\in L_0\otimes L_1$ and
$G_2\in L_0\otimes L_2$, define

$$
N_G(Y_1,Y_2)=G_1Y_2+G_2Y_1.
\tag{6}
$$

The map is injective except when both arms have rank one and use
the same center line. In that exceptional case, write
$G_i=u v_i^{\mathsf T}$ with $u,v_i\ne0$. Its kernel is exactly

$$
Y_1=v_1w^{\mathsf T},\qquad
Y_2=-v_2w^{\mathsf T},\qquad w\in L_r.
\tag{7}
$$

Thus for a common palette of size $q$, the kernel has dimension
$q$ in this case and zero otherwise.

If either arm has rank at least two, apply (4), with endpoints
relabelled as needed, to (6). It first forces one $Y$ to vanish
and then the other. If both arms have rank one with distinct
center lines, apply center linear functionals that kill one line
but not the other. This gives the same conclusion.
If the center lines agree, cancel their
common factor. The equation $v_1Y_2+v_2Y_1=0$, followed by projection
perpendicular to $v_1$ and $v_2$, gives precisely (7).

Under (2), the inverse estimate for (6) is uniform after dividing
the arms by $t$. In particular, for a constant depending only on
$\eta$,

$$
\|Y_1\|+\|Y_2\|\le C\|N_{G/t}(Y_1,Y_2)\|.
\tag{8}
$$

Injectivity alone is not our full GHZ theorem. Rank-one arms with
distinct center directions also have injective (6), but the proof
below needs (4) at whichever core vertex the ground equations select.
Condition (2) guarantees that step at both leaves.

## 4. Split off the three-site core

Set $K=\{0,1,2\}$ and let $L=\{3,4,5\}$ be the outside sites.
Write

$$
G_i=T_{0i}\ (i=1,2),\qquad B=T_{12},\qquad b=\|B\|.
$$

For each $\ell\in L$, let $H_\ell=T_{0\ell}$,
$Y_{i\ell}=T_{i\ell}$ for $i=1,2$,
$h_\ell=\|H_\ell\|$, and
$y_\ell=(\|Y_{1\ell}\|^2+\|Y_{2\ell}\|^2)^{1/2}$.
Put $Z_{\ell m}=T_{\ell m}$ and $z_{\ell m}=\|Z_{\ell m}\|$.

The response on $K\cup\{\ell\}$ is

$$
F_\ell=G_1Y_{2\ell}+G_2Y_{1\ell}+H_\ell B.
\tag{9}
$$

As in the [three-arm proof](three-arm-ghz-distance-bound-2026-09-27.md),
the elementary cases $T=0$ and $\varepsilon>t\delta^2$ already
satisfy (1). Otherwise the actual output constraints give

$$
\varepsilon\le t\delta^2,\qquad
f:=\|\mathcal F_4(T)\|\le Ct\delta^2,\qquad t\le\delta\le1.
\tag{10}
$$

Every edge with nonzero ground cofactor
$c_e=\operatorname{haf}D[V\setminus e]$ has
$\|T_e\|\le C_e\delta^2$. The constants depend on $D$.
We again call such an edge anchored.

By (8)--(10),

$$
y_\ell\le C\left(\delta^2+\frac{h_\ell b}{t}\right).
\tag{11}
$$

Also the quartet $0,1,\ell,m$ gives

$$
z_{\ell m}\le C\left(\delta^2+
\frac{h_\ell}{t}y_m+\frac{h_m}{t}y_\ell\right).
\tag{12}
$$

These hold for every outside site and pair. They do not yet say that
all $h_\ell$ or all $y_\ell$ are small.

## 5. Ground cofactors select two attachments

If either strong arm is anchored, (2) implies $t=O(\delta^2)$,
which gives $|\lambda|\le\varepsilon+15t^3=O(\varepsilon+\delta^6)$.
If $B$ is anchored, then $b=O(\delta^2)$.
Equations (11)--(12) then give every $y_\ell,z_{\ell m}=O(\delta^2)$.
The matching estimate in section 6 proves (1) directly.

We may therefore assume every ground cofactor inside $K$ is zero.
The following ground fact, also used in the
[triangle theorem](triangle-attachment-ghz-bound-2026-09-27.md),
then applies: there are a core site $i\in K$ and two distinct outside
sites $r,s$ with $c_{ir},c_{is}\ne0$.

For completeness, the cross-cofactor matrix cannot be zero.
Otherwise the identities
$\sum_{j\ne i}D_{ij}c_{ij}=\operatorname{haf}D=0$
at the three outside sites force their three mutual cofactors
to vanish as well. All cofactors would vanish, contradicting the
five-site cofactor fact. A nonzero cross row has at least two
nonzero entries, since its weighted sum is zero and every $D_{ij}\ne0$.
This proves the claimed selection.

If the selected core site is the center, then
$h_r+h_s=O(\delta^2)$.
Equation (11) gives $y_r+y_s=O(\delta^2)$, since $b\le t$.
We also have $bh_r+bh_s=O(t\delta^2)$.

If the selected core site is leaf $1$, then
$\|Y_{1r}\|+\|Y_{1s}\|=O(\delta^2)$.
Move these terms to the right side of (9):

$$
\|G_1Y_{2\ell}+H_\ell B\|\le Ct\delta^2
\qquad(\ell=r,s).
$$

Apply (4) with $\tau(G_1)\ge\eta t$ and $\|G_1\|\le t$.
It gives $\|Y_{2\ell}\|=O(\delta^2)$ and
$bh_\ell=O(t\delta^2)$.
The selected-leaf-$2$ case is identical using $G_2$.
Thus every selection yields

$$
\boxed{
y_r+y_s\le C\delta^2,\qquad bh_r+bh_s\le Ct\delta^2.
}
\tag{13}
$$

Let $u$ be the third outside site. Equation (11) gives

$$
y_u\le C\left(\delta^2+\frac{h_ub}{t}\right).
\tag{14}
$$

Insert (13)--(14) into (12). For example,
$(h_r/t)y_u\le C\delta^2+
(h_u/t)(bh_r/t)\le C\delta^2$.
Therefore all three outside edges satisfy

$$
z_{\ell m}\le C\delta^2.
\tag{15}
$$

## 6. Every matching is controlled

The exact six-site split is

$$
H_6(T)=\sum_{\{\ell,m\}\subset L}Z_{\ell m}F_k
+\sum_{(\ell,m,k)\text{ a permutation of }L}
H_\ell Y_{1m}Y_{2k},
\quad \{k\}=L\setminus\{\ell,m\}
\tag{16}
$$

in each term of the first sum. The first sum contains nine matchings;
the second contains six. Factors always occupy their labelled sites.

The first sum has norm at most $3\max z_{\ell m}\,f\le Ct\delta^4$.
For a term with center attachment $H_u$, (13) gives
$h_uy_ry_s\le Ct\delta^4$.
For a term with center attachment $H_r$, (13)--(14) give

$$
h_ry_sy_u
\le C\delta^2\left(h_r\delta^2+\frac{h_u}{t}bh_r\right)
\le Ct\delta^4.
$$

The $H_s$ case is identical. Hence
$\|H_6(T)\|\le Ct\delta^4\le C\delta^5$ in this case.
When $B$ was anchored, all $y_\ell,z_{\ell m}=O(\delta^2)$
and (16) gives the same bound immediately.

Since the entirely non-ground output is
$H_6(T)=\lambda(b^6+c^6)+E_{\rm bin}$ with
$\|E_{\rm bin}\|\le\varepsilon$, these estimates and the elementary
cases prove (1). Constants are uniform under (2), and there are only
finitely many label choices. ∎

For the refinement, the inverse estimate (8) still holds: apply
(4) using $G_1$, then use $\|G_2\|\ge\eta t$ to bound the other
attachment. The cases of an anchored internal core edge are
unchanged. Otherwise all three internal cofactors are zero, and
the assumed nonzero cofactor row at site $0$ or $1$ has at least
two nonzero outside entries. Select this row in section 5.
Only the center case or the leaf-$1$ case is then needed, so the
argument never uses a lower bound for $\tau(G_2)$.
All remaining estimates are identical.

## 7. The remaining onset set

Let $\mathcal S$ be the closed set of normalized binary six-site
sources supported on a star with at most two arms, such that at
least one of the two arm blocks has rank at most one.
A missing arm has rank zero, so this set includes every single edge,
whether its block has rank one or two.

For each fixed $\rho>0$, (1) now holds uniformly near $A_0$
whenever $T=0$ or

$$
\operatorname{dist}(T/t,\mathcal S)\ge\rho.
\tag{17}
$$

Use the compactness argument from section 6 of the
[three-arm note](three-arm-ghz-distance-bound-2026-09-27.md).
The remaining simultaneous critical zeros outside $\mathcal S$
are triangles, non-star four-site cores, stars with at least three
arms, or two-arm stars with two invertible blocks.
Each has a neighborhood covered by an established theorem.
A finite cover and the same two residual bounds give (17).

The remaining shapes for this onset estimate are single edges and
two-arm stars with a rank-one arm, with some further cases covered
by the cofactor-sensitive refinement. For a two-arm star with
exactly one invertible arm, the refinement leaves only the case
where both ground cofactor rows at that arm's endpoints vanish.
This statement concerns
full-support single-color zero-output limits only.
The universal rate question still needs
$\varepsilon\ge c|\lambda|^3$ across every relevant boundary;
a fifth-power source-distance estimate does not imply it.
