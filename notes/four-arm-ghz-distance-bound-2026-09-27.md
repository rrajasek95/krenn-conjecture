# A fifth-power GHZ onset bound through the loss of one star arm

September 27, 2026. **Written proof with exact supporting checks; independent
audit pending.** The unrestricted square-root rate law remains open.

[Four-arm response geometry](four-arm-star-response-2026-09-27.md) ·
[Replay](../computations/four-arm-ghz-boundary-2026-09-27/README.md) ·
[Previous five-arm estimate](rank-free-star-response-bound-2026-09-27.md)

## 1. Statement

Let $A_0$ be a six-site source using only the ground color $a$, with
all fifteen ground entries $D_{ij}$ nonzero and $H(A_0)=0$.
For a nearby ternary source write

$$
H(A)=\lambda(a^6+b^6+c^6)+E,\quad
\varepsilon=\|E\|,\quad
\delta=\|A-A_0\|,
$$

where $E$ is orthogonal to the GHZ target. Let $T$ be the binary
non-ground part of $A$, and $X$ the entries with exactly one ground
endpoint.

**Theorem.** Fix $\eta>0$. There are constants $C_1,C_2$ and a
neighborhood of $A_0$ such that

$$
\boxed{|\lambda|\le C_1\varepsilon+C_2\delta^5}
\tag{1}
$$

whenever $T=0$, or some vertex has four distinct non-ground arms with

$$
\|T_{0i}\|_F\ge\eta\|T\|
\quad\text{at each of those four neighbors}.
\tag{2}
$$

Labels may be permuted. The fifth arm may vanish, and all arm matrices
may have rank one. The normalized direction need not be assumed close
to a flat star. Constants depend on $A_0$ and $\eta$.

This extends the previous five-arm source-distance bound.
It is an onset estimate, not the lower bound
$\varepsilon\ge c|\lambda|^3$ needed for the square-root rate law.

## 2. Keep the leaf-only response separate

Fix a center and write $T=G+B$, where $G$ contains its five arms and
$B$ the edges between leaves. Put $t=\|T\|$ and $b=\|B\|$.
Let $\mathcal Q(B)$ collect the four-site responses entirely on leaves,
and $\mathcal R(G,B)$ those containing the center.
Set $d=\min|D_{ij}|>0$ and shrink the neighborhood so $\delta\le d/2$.

The earlier mixed-output identity gives

$$
\|\mathcal F_4(T)\|\le\frac2d
\left(\varepsilon+45\|X\|^2t\right).
\tag{3}
$$

There is a stronger estimate for the leaf-only part:

$$
\boxed{
\|\mathcal Q(B)\|\le\frac2d
\left(\varepsilon+45\|X\|^2b\right).
}
\tag{4}
$$

To see this, use only output words with ground color at the center and
one leaf. Their leading term is that ground edge times the four-site
response on the other leaves. In every remaining matching term, the
two ground sites use two mixed $X$ edges. The remaining non-ground
edge lies between leaves, so it belongs to $B$. The usual
15-matchings, three-edge-choice bound gives the coefficient 45.

Expansion of the entirely non-ground output at the center also gives

$$
H_6(T)=\sum_i G_i\otimes H_4(B[\text{leaves}\setminus i]),
$$

with factors at their labelled sites. Triangle and Cauchy–Schwarz
inequalities imply

$$
\boxed{\|H_6(T)\|\le\|G\|\,\|\mathcal Q(B)\|
\le\frac{2t}{d}\left(\varepsilon+45\delta^2b\right).}
\tag{5}
$$

The factor $b$ in (4) is essential. Replacing it by $t$ would lose
the improvement used below.

## 3. A nonzero ground cofactor supplies an extra constraint

Write $C_{ij}(D)=\operatorname{haf}D[V\setminus\{i,j\}]$.
Every five-site subset has a nonzero cofactor on an internal edge.
The proof is in section 5 of the
[earlier normal-form note](ghz-critical-direction-normal-form-2026-09-27.md):
otherwise the zero ground hafnian would force all cofactors to vanish,
contradicting the scalar six-site star bound and full support.

Whenever $C_e(D)\ne0$, the output sector with non-ground colors exactly
at the endpoints of $e$ gives, throughout a sufficiently small
neighborhood,

$$
\|T_e\|_F\le C_e'(\varepsilon+\delta^2).
\tag{6}
$$

Indeed its leading term is $C_e(A_{aa})T_e$, and the remainder uses
two $X$ edges and one ground edge, of total norm at most
$45(\|D\|+1)\delta^2$. The selected cofactor stays bounded away from zero.

## 4. First prove the bound near each flat star with at least four arms

Fix a normalized flat star $S$ with at least four nonzero arms, and
suppose $T/t$ lies in a sufficiently small neighborhood of it.
If $T=0$ then $|\lambda|\le\varepsilon$.
If $\varepsilon>t\delta^2$, the elementary matching estimate
$|H_{b^6}|\le15t^3\le15t\delta^2$ already gives
$|\lambda|\le16\varepsilon$.
It remains to suppose

$$
0<t,\qquad \varepsilon\le t\delta^2.
\tag{7}
$$

By (3), $\|\mathcal R(G,B)\|/t\le C\delta^2$.

If the fixed star's leaf-response kernel is zero, its linear estimate
gives $b\le C\delta^2$. This includes every five-arm star, irrespective
of matrix rank.

For a four-arm star with the two-pair kernel, the refined response
estimate and (4) give

$$
b^2\le C\left(\varepsilon+\delta^2b+\delta^4\right).
$$

Young's inequality absorbs the middle term, yielding

$$
b\le C(\sqrt\varepsilon+\delta^2).
\tag{8}
$$

For the common-center two-dimensional kernel, take the five-site set
formed by the center and its four active leaves. Section 3 supplies a
nonzero cofactor edge inside this set.
If it is a star arm, that arm is bounded below by a fixed fraction of
$t$, so (6) gives $t\le C(\varepsilon+\delta^2)$.
The bound $|\lambda|\le\varepsilon+15t^3$ then gives the stronger
$|\lambda|\le C\varepsilon+C\delta^6$.

Otherwise the selected edge $e$ is between active leaves.
Equation (6), together with (7) and $\delta\le1$, gives
$\|B_e\|\le C\delta^2$.
The refined estimate with this edge term now gives exactly (8).
Thus the common-center five-core branches are removed by an actual
GHZ output constraint.

Finally insert (8) into (5), use $t\le\delta$, and
$\delta^3\sqrt\varepsilon\le(\varepsilon+\delta^6)/2$.
Since $|H_{b^6}-\lambda|\le\varepsilon$, this proves (1) near every
fixed star with at least four nonzero arms.

## 5. Remove the prior closeness-to-a-star assumption

Fix the four arms in (2), and consider normalized binary sources
$Z$ with those arm norms at least $\eta$. This is a compact set.
Its simultaneous zeros of

$$
\mathcal F_4(Z),\qquad
\mathcal C_D Z:=\bigl(C_{ij}(D)Z_{ij}\bigr)_{i<j}
\tag{9}
$$

are stars with at least four nonzero arms.
Indeed, the [flat-support classification](four-site-flat-support-classification-2026-09-27.md)
leaves only stars, at most four active sites, or complete five-cores.
Four arms already use five sites, and a complete five-core is excluded
by the nonzero cofactor from section 3.

Cover this compact zero set by finitely many star neighborhoods from
section 4. Outside their union, the continuous sum of the two residual
norms in (9) has a positive minimum. If the zero set is empty, the
same statement holds on the entire compact set.

Assume (7); otherwise the result is already proved.
For a sufficiently large fixed $M$, the case $t\le M\delta^2$ gives
$|\lambda|\le\varepsilon+15M^3\delta^6$ directly.
If $t>M\delta^2$, then (3) gives

$$
\|\mathcal F_4(T/t)\|\le C/M.
$$

The two-non-ground output equations, and
$C_{ij}(A_{aa})-C_{ij}(D)=O(\delta)$, also give

$$
\|\mathcal C_D(T/t)\|\le C(\delta+1/M).
$$

Choose $M$ large enough, then $\delta$ small enough, to put $T/t$
inside the finite union of star neighborhoods. Section 4 applies
with uniform constants. There are only finitely many choices of
center and four arms, so taking the largest constants proves the
stated theorem. ∎

Within the full-support single-color branch, the remaining uncontrolled
support patterns for this onset argument have at most four active sites.
The fifth-power estimate itself still does not compare error to the cube
of the GHZ signal, even on the star families controlled here.
