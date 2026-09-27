# Three arms suffice for fifth-power GHZ onset

September 27, 2026. **Written proof with exact supporting checks; independent
audit pending.** The unrestricted square-root rate law remains open.

[Exact replay](../computations/three-arm-ghz-onset-2026-09-27/README.md) ·
[Illustrated guide](../explainers/CRITICAL-DIRECTION-GEOMETRY.md) ·
[GHZ project](../research/ghz-rates/README.md)

## 1. The three-arm theorem

Let $A_0$ be a six-site source using only the ground color $a$, with
all fifteen ground entries $D_{ij}\ne0$ and $\operatorname{haf}D=0$.
For a nearby ternary source write

$$
H(A)=\lambda(a^6+b^6+c^6)+E,\qquad
E\perp(a^6+b^6+c^6),\qquad
\varepsilon=\|E\|,\quad \delta=\|A-A_0\|.
$$

Let $T$ be its binary non-ground part and $t=\|T\|$.

**Theorem.** Fix $\eta>0$. Near $A_0$ there are constants $C_1,C_2$
such that

$$
\boxed{|\lambda|\le C_1\varepsilon+C_2\delta^5}
\tag{1}
$$

whenever $T=0$, or one vertex has three distinct non-ground arms with
norm at least $\eta t$. The other two arms may have any size, including
zero. All matrices may have rank one, and the center's entire ground
cofactor row may vanish. No prior closeness to a star is required.

In the nontrivial regime of the proof, we control the whole binary
output, $\|H_6(T)\|\le C(\varepsilon+\delta^5)$.
Combined with the triangle and four-core results, this leaves only
stars with at most two arms for the full-support single-color onset
argument. Equation (1) is not the error-versus-signal estimate needed
for the unrestricted rate law.

## 2. A weighted five-site extension estimate

This auxiliary result works over any fixed finite palette.
Use center $0$, active leaves $1,2,3$, and one new site $r$.
Let $G_i$ be the three center arms. Assume

$$
\|G\|\le1,\qquad \|G_i\|\ge\eta>0.
$$

Let $B=(B_{12},B_{13},B_{23})$ be the internal leaf edges,
$H$ the new arm $0r$, and $Y=(Y_1,Y_2,Y_3)$ the edges $ir$.
Write $b=\|B\|$, $h=\|H\|$, and $y=\|Y\|$.
The five four-site responses are

$$
F=G_1B_{23}+G_2B_{13}+G_3B_{12},
\tag{2}
$$

$$
R_{ij}=G_iY_j+G_jY_i+HB_{ij}\quad(1\le i<j\le3),
\qquad
Q=B_{12}Y_3+B_{13}Y_2+B_{23}Y_1.
\tag{3}
$$

Tensor factors are placed at their labelled sites throughout.
Select any one of the seven edges other than $01,02,03$, and define
its weighted residual by

$$
\alpha_e=
\begin{cases}
h\|B_{ij}\|,&e=ij\subset\{1,2,3\},\\
b\|H\|,&e=0r,\\
\|Y_i\|,&e=ir.
\end{cases}
\tag{4}
$$

**Weighted extension lemma.** There is a constant $M$, depending only
on $\eta$ and the palette, such that, whenever $b>0$,

$$
\boxed{
bh+y\le M\left(\|R\|+h\|F\|+\frac{\|Q\|}{b}+\alpha_e\right).
}
\tag{5}
$$

The same constant may be used for every choice of the selected edge.
When $b=0$ or $h=0$, the simpler bound
$y\le M\|R\|$ holds.

### Proof

First the map

$$
(N_GY)_{ij}=G_iY_j+G_jY_i
\tag{6}
$$

is injective for any three nonzero arms. Represent blocks by their
bilinear polynomials in local color variables. If (6) vanishes, then

$$
2G_1G_2Y_3=G_1(N_GY)_{23}+G_2(N_GY)_{13}
-G_3(N_GY)_{12}=0.
$$

The polynomial ring is an integral domain, so $Y_3=0$ and then
$Y_1=Y_2=0$. On the stated compact set of arm triples, injectivity
gives a uniform positive least singular value. In particular
$\|Y\|\le M_0\|N_GY\|$ without any matrix-rank hypothesis.

For $b,h>0$, replace $B,H,Y$ by $B/b,H/h,Y/(bh)$.
Every term in (5) is multiplied by $1/(bh)$.
It is enough to prove the assertion when $\|B\|=\|H\|=1$.
For large $\|Y\|$, the term $R=N_GY+HB$ controls $1+\|Y\|$
by the uniform lower bound for (6).

For bounded $Y$, use compactness in $G,B,H,Y$.
If the right side of (5) vanished, (2)--(3) would say that every
four-site response of the five-site source $G+B+H+Y$ is zero.
All five sites are active: the three arms are nonzero and $H\ne0$.
Its support is not a star, since $B\ne0$ and the three center arms
are present. The [flat-support theorem](four-site-flat-support-classification-2026-09-27.md)
therefore forces a complete five-site support.
But $\alpha_e=0$ makes the selected edge zero, a contradiction.
The continuous right side consequently has positive minimum on the
bounded compact set. Combining the two regions proves (5).

If $b=0$ or $h=0$, then $HB=0$, so the lower bound for (6)
directly gives the asserted simpler estimate. There are only seven
choices of $e$, so a maximum of their constants is uniform. ∎

The division by $b$ and the factors in (4) respect the two separate
scalings of $B$ and $H$. An unweighted compactness argument would
not give the estimate needed below.

## 3. Apply the actual GHZ output constraints

Relabel the three arms as $G_i=T_{0i}$, $i=1,2,3$.
Take core $K=\{0,1,2,3\}$ and outside sites $r,s$.
Inside the core, retain the leaf triangle $B$ and its norm $b$.
For each outside site $\ell$, write $H_\ell=T_{0\ell}$,
$Y_\ell=(T_{i\ell})_{i=1}^3$, $h_\ell=\|H_\ell\|$, and
$y_\ell=\|Y_\ell\|$. Finally let $Z=T_{rs}$ and $z=\|Z\|$.
These symbols describe pieces of $T$, not the mixed ground/non-ground
entries of the original source.

The [mixed-output estimates](four-arm-ghz-distance-bound-2026-09-27.md) give

$$
f:=\|\mathcal F_4(T)\|\le C(\varepsilon+\delta^2t),\qquad
\|T_e\|\le C_e(\varepsilon+\delta^2)
\quad\text{if }c_e:=\operatorname{haf}D[V\setminus e]\ne0.
\tag{7}
$$

Every five-site subset contains an edge with $c_e\ne0$, by section 5
of the [normal-form note](ghz-critical-direction-normal-form-2026-09-27.md).

As before, $T=0$ gives $|\lambda|\le\varepsilon$.
If $\varepsilon>t\delta^2$, then
$|\lambda|\le\varepsilon+15t^3\le16\varepsilon$.
We may assume

$$
\varepsilon\le t\delta^2,\qquad f\le Ct\delta^2,\qquad
t\le\delta\le1.
\tag{8}
$$

Every anchored block, meaning one with $c_e\ne0$, is $O(\delta^2)$.
If any of the three strong arms is anchored, its lower bound
$\eta t$ implies $t=O(\delta^2)$, and the direct bound
$|\lambda|\le\varepsilon+15t^3$ gives (1).
Thus assume all three strong arms have zero ground cofactors.

For each outside site $\ell$, the five-site subset $K\cup\{\ell\}$
therefore has an anchored edge of type $B$, $H_\ell$, or $Y_\ell$.
This is precisely one of the seven choices allowed in the lemma.

Apply that lemma with arms $G/t$, internal leaf source $B$,
new arm $H_\ell/t$, and attachments $Y_\ell$.
The responses $F$ and $R$ of the lemma become their actual values
divided by $t$, while $Q_\ell$ stays the actual response on
$\{1,2,3,\ell\}$. Since $b,h_\ell\le t$ and the selected actual
block is $O(\delta^2)$, all three possible expressions (4) are
$O(\delta^2)$. Equations (5), (7), and (8) give

$$
\frac{b h_\ell}{t}+y_\ell
\le C\left(\delta^2+\frac{q_\ell}{b}\right),
\qquad q_\ell:=\|Q_\ell\|,\quad b>0.
\tag{9}
$$

This argument also covers $h_\ell=0$, using (6).

## 4. A response bound that only sees the relevant leaf edges

For the quartet $\{1,2,3,r\}$, use output words with ground color
at $0$ and $s$. Their leading term is $A_{aa,0s}Q_r$.
Every other matching uses two mixed ground/non-ground edges and
one non-ground edge inside that quartet. The latter belongs to
$B$ or $Y_r$.

Since $D_{0s}\ne0$, its nearby ground entry stays bounded away
from zero. The other twelve matching terms give

$$
\boxed{q_r\le C\bigl(\varepsilon+\delta^2(b+y_r)\bigr),}
\tag{10}
$$

and the same holds for $s$. For example, the earlier coefficient
bound 45 with the minimum ground-edge modulus gives a valid
constant. There is no contribution from the three strong arms,
the other outside site's attachments, or the edge $rs$ in this
remainder.

Insert (10) into (9). For a sufficiently large fixed $L_0$, if
$b>L_0\delta^2$, absorb the term $C\delta^2y_\ell/b$ to get

$$
\boxed{
y_\ell\le C\kappa,\qquad b h_\ell\le Ct\kappa,\qquad
\kappa=\delta^2+\frac{\varepsilon}{b}.
}
\tag{11}
$$

This controls a product involving each outside arm. It does not claim
that $b$ or $h_\ell$ is individually small.

## 5. Bound the whole binary output

The linear estimate (6), before using the weighted lemma, always gives

$$
y_\ell\le C\left(f/t+(h_\ell/t)b\right)
\le C(\delta^2+b).
\tag{12}
$$

The quartet on $0,i,r,s$ is
$G_iZ+H_r(Y_s)_i+H_s(Y_r)_i$.
Using any strong arm gives

$$
z\le C\left(f/t+(h_r/t)y_s+(h_s/t)y_r\right).
\tag{13}
$$

Every six-site matching has one of three forms:

| Form | Bound for its summed contribution |
| --- | --- |
| The outside sites join each other | $zf$ |
| Both outside sites join distinct active leaves | $6t\,y_ry_s$ |
| One outside site joins the center, the other an active leaf | $3b(h_ry_s+h_sy_r)$ |

These are all fifteen matchings: respectively three, six, and six.
The first row uses the actual four-site output of the core.
Thus

$$
\|H_6(T)\|\le zf+6t\,y_ry_s+3b(h_ry_s+h_sy_r).
\tag{14}
$$

If $b\le L_0\delta^2$ or $b^2\le\varepsilon$, (12)--(14) yield

$$
\|H_6(T)\|\le Ct(\delta^2+b)^2
\le C(\delta^5+\varepsilon).
\tag{15}
$$

Otherwise (11) holds and $\varepsilon/b<\sqrt\varepsilon$.
Equations (11) and (13) give $z\le C\kappa$; insert these estimates
and $bh_\ell\le Ct\kappa$ into (14):

$$
\|H_6(T)\|\le Ct\kappa^2
\le Ct(\delta^2+\sqrt\varepsilon)^2
\le C(\delta^5+\varepsilon).
\tag{16}
$$

The entirely non-ground output satisfies
$H_6(T)=\lambda(b^6+c^6)+E_{\rm bin}$ with
$\|E_{\rm bin}\|\le\varepsilon$, proving (1).
All constants were uniform for $\|G/t\|\le1$ and
$\|G_i/t\|\ge\eta$. A finite choice of centers and three arms
completes the stated uniformity. ∎

## 6. The remaining onset shapes have at most two arms

Let $\mathcal B_2$ be the closed set of normalized binary six-site
sources supported on a star with at most two nonzero arms.
For each fixed $\rho>0$, near every $A_0$ above, (1) holds uniformly
whenever $T=0$ or

$$
\operatorname{dist}(T/t,\mathcal B_2)\ge\rho.
\tag{17}
$$

The compactness proof is the same as section 6 of the
[triangle note](triangle-attachment-ghz-bound-2026-09-27.md).
Simultaneous normalized zeros of $\mathcal F_4$ and
$(c_eT_e)_e$ outside $\mathcal B_2$ are triangles, non-star
four-site cores, or stars with at least three arms.
The triangle theorem, four-core theorem, and the present theorem
cover neighborhoods of these directions.
Outside a finite cover, the two residual norms have positive sum;
the mixed-output bounds force a normalized source into the cover
unless $t=O(\delta^2)$ or $\varepsilon>t\delta^2$.
Both exceptions already satisfy (1).

The unresolved shapes for this onset estimate are now a single edge
and a two-arm star, with arbitrary colored blocks. The unrestricted
square-root law still requires $\varepsilon\ge c|\lambda|^3$
through all relevant limits. The source-distance estimate (1) does
not supply that comparison.

## 7. Both extra terms in the extension estimate matter

For a two-pair four-arm kernel, take unit leaf factors,
$G_1=G_2=e_0e_0^{\mathsf T}$, $G_3=e_1e_0^{\mathsf T}$,
and $H=h e_1e_0^{\mathsf T}$. Put

$$
B_{12}=0,\quad B_{13}=\tau e_0e_0^{\mathsf T},\quad
B_{23}=-\tau e_0e_0^{\mathsf T},\qquad
(Y_1,Y_2,Y_3)=\tau h(-1,1,0)e_0e_0^{\mathsf T}.
$$

Then $F=R=0$, and the selected edge $12$ is zero, but
$Q=2\tau^2h\,e_0^{\otimes4}$. Without the term $\|Q\|/b$,
the right side of (5) would vanish when $\tau h\ne0$.

Conversely, take all three arms in a common color direction, and
use scalar coefficients

$$
(B_{12},B_{13},B_{23})=\tau(1,\omega,\omega^2),\quad H=h,\quad
(Y_1,Y_2,Y_3)=\tau h(\omega^2,\omega,1),
$$

where $\omega^2+\omega+1=0$ and $\omega\ne1$.
Now $F=R=Q=0$, with every edge nonzero when $\tau h\ne0$.
This is the complete five-site cube-root branch.
The selected-edge residual in (5) is essential to exclude it.
