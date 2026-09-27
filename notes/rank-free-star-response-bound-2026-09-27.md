# A star-response bound that survives matrix rank loss

September 27, 2026. **Written proof with exact supporting checks; independent
audit pending.** The unrestricted square-root rate law remains open.

[Replay](../computations/flat-support-structure-2026-09-27/README.md) ·
[Complete support classification](four-site-flat-support-classification-2026-09-27.md) ·
[Earlier invertible-arm bound](star-response-identity-and-binary-flat-cores-2026-09-27.md)

## 1. The bound

Let a source have center $0$, $k\ge5$ leaves, and any finite palette.
All star arms $G_i=A_{0i}$ are nonzero; they need not be invertible.
Write $B_{ij}=A_{ij}$ for the leaf blocks, and set

$$
a=\min_i\|G_i\|_F>0,\qquad M=\max_i\|G_i\|_F.
$$

Let $R_{ijk}$ be the four-site matching tensor on $\{0,i,j,k\}$, and
$T_\star=\sum_{i<j<k}\|R_{ijk}\|^2$.

**Theorem.**

$$
\boxed{
T_\star\ \ge\
\frac{(k-2)a^6}{18M^4}\sum_{i<j}\|B_{ij}\|_F^2.
}
\tag{1}
$$

In particular, a four-site-flat source with a nonzero spanning star on
at least six sites has no leaf-to-leaf edges. Deleting the leaf blocks
gives the explicit estimate

$$
\boxed{
\operatorname{dist}(A,\{\text{stars centered at }0\})
\le \sqrt{\frac{18}{k-2}}\frac{M^2}{a^3}
\|\mathcal F_4(A)\|.
}
\tag{2}
$$

The constant involves Frobenius norms, not least singular values.
It remains finite when any arm loses matrix rank, provided no arm tends
to zero. The coefficient is deliberately coarse; no sharpness is claimed.
The invertible-arm identity can give a better constant in its own setting.

## 2. A three-vector estimate

Let $\operatorname{Sym}_3$ be the orthogonal projection onto symmetric
third-order tensors in a complex Hilbert space. For any three vectors,

$$
\|\operatorname{Sym}_3(u\otimes v\otimes w)\|^2
\ge \frac16\|u\|^2\|v\|^2\|w\|^2.
\tag{3}
$$

For unit vectors, six times the norm squared is the permanent of their
Gram matrix:

$$
1+|p|^2+|q|^2+|r|^2+2\operatorname{Re}(pqr),
$$

where $p=\langle u,v\rangle$, $q=\langle v,w\rangle$,
$r=\langle w,u\rangle$, using a consistent inner-product convention.
Since $|r|\le1$,
$2|pqr|\le |p|^2+|q|^2$. The displayed expression is at least one.
Scaling proves (3); a zero vector is immediate.

Suppose $G_1,G_2,G_3$ are matrices whose row index is in that same
Hilbert space, with separate column spaces. Symmetrize only their
three row indices. Applying (3) to each triple of columns and summing gives

$$
\|\operatorname{Sym}_3(G_1\otimes G_2\otimes G_3)\|^2
\ge \tfrac16\prod_{\ell=1}^3\|G_\ell\|_F^2.
\tag{4}
$$

No assumption on matrix ranks appears. The reverse upper bound with
coefficient one follows because an orthogonal projection contracts norm.

## 3. Lift the five-leaf equations to a common tensor space

First take exactly five leaves. All tensors in this paragraph live in
the common space consisting of three symmetric center copies and one
copy of each of the five leaves.

For each leaf edge $ij$, define $Z_{ij}$ by taking $B_{ij}$ and the
three arms $G_l$ at the other leaves, then symmetrizing the center
indices. For each leaf triple $ijk$, define $Y_{ijk}$ by taking
$R_{ijk}$ and the two arms at the other leaves, and symmetrizing the
three center indices.

The matching formula
$R_{ijk}=G_iB_{jk}+G_jB_{ik}+G_kB_{ij}$, with the tensor factors placed
at their labelled sites, gives the exact identity

$$
Y_{ijk}=Z_{ij}+Z_{ik}+Z_{jk}.
\tag{5}
$$

For arbitrary vectors $Z_{ij}$ in any Hilbert space, expansion of the
squares on the complete graph with five vertices gives

$$
\sum_{i<j<k}\|Z_{ij}+Z_{ik}+Z_{jk}\|^2
=\sum_{i<j}\|Z_{ij}\|^2+
\sum_i\left\|\sum_{j\ne i}Z_{ij}\right\|^2.
\tag{6}
$$

Indeed, a diagonal edge term occurs in three triples and twice in the
row sums; two adjacent edges occur together once on each side.
All other cross terms are absent. Thus $\sum\|Y\|^2\ge\sum\|Z\|^2$.

The independent leaf indices let (4) factor out $\|B_{ij}\|_F^2$, giving

$$
\sum\|Z\|^2\ge \frac{a^6}{6}\sum\|B\|_F^2.
$$

The upper norm bound for symmetrization gives
$\sum\|Y\|^2\le M^4\sum\|R\|^2$.
Combining these proves (1) for five leaves.

For $k>5$, sum this five-leaf bound over all five-element leaf subsets.
Each response triple is counted $\binom{k-3}{2}$ times and each leaf
edge $\binom{k-2}{3}$ times. Their ratio is $(k-2)/3$.
This proves (1), and deleting the leaf blocks proves (2). ∎

## 4. Smooth stars without an invertibility hypothesis

At a flat spanning star on $n=k+1\ge6$ sites, changes to the arms alone
produce no four-site output. The derivative in the leaf blocks is the
linear map $B\mapsto(R_{ijk})$ controlled by (1).
It is injective. Hence, for $q$ colors,

$$
\operatorname{rank}D\mathcal F_4
=q^2\binom{n-1}{2},\qquad
\ker D\mathcal F_4=\{\text{changes to the star arms}\}.
\tag{7}
$$

The local flat family is exactly the star family. The constants are
uniform when the arm norms stay in a compact interval bounded away
from zero, regardless of their matrix ranks.

Five leaves are necessary for this rank-independent statement.
A scalar four-leaf star has two undetected leaf-block directions in
the derivative. In particular, the cube-root five-core supplies
nonzero leaf blocks with all four-site outputs zero while retaining
all four star arms.

## 5. Consequence for the GHZ distance bound

Use the notation of the
[GHZ normal-form theorem](ghz-critical-direction-normal-form-2026-09-27.md):
a full-support single-color zero $A_0$, ground-edge lower bound $d>0$,
$H(A)=\lambda\Delta+E$, $\varepsilon=\|E\|$,
$\delta=\|A-A_0\|$, and non-ground part $T$.

Suppose some vertex has all five non-ground arms satisfying

$$
\|T_{0i}\|_F\ge\eta\|T\|,\qquad i=1,\ldots,5,
\tag{8}
$$

where $\eta>0$ is fixed. No matrix-rank condition or prior closeness to
a flat star is needed. If $T=0$, then $|\lambda|\le\varepsilon$.
Otherwise, by (2), deleting its non-star blocks gives a
flat star $Q$ with

$$
\|T-Q\|\le \frac{\sqrt6}{\eta^3\|T\|}\|\mathcal F_4(T)\|.
$$

Substitution into the mixed-output identity gives

$$
\|T-Q\|\le L\left(\frac{\varepsilon}{\|T\|}+45\|X\|^2\right),
\qquad L=\frac{2\sqrt6}{d\eta^3}.
$$

The same cubic remainder argument as the normal-form theorem, with
$K=46L$ and $\delta\le\min(d/2,1,1/K)$, proves

$$
\boxed{|\lambda|\le16\varepsilon+105K^2\delta^5.}
\tag{9}
$$

This extends that theorem across matrix rank loss in every spanning-star
direction satisfying (8). It does not control constants as an arm
disappears, or prove the needed inequality
$\varepsilon\ge c|\lambda|^3$.
