# A quantitative GHZ normal form near smooth critical directions

September 27, 2026. **Written proof with exact supporting checks; independent
audit pending.** The unrestricted square-root rate law remains open.

[Classification and stability theorem](flat-four-response-five-clique-2026-09-27.md) ·
[Binary cores and stars](star-response-identity-and-binary-flat-cores-2026-09-27.md) ·
[Replay](../computations/flat-core-rigidity-2026-09-27/README.md) ·
[Earlier full-support identities](full-support-single-color-jets-2026-09-27.md)

## 1. Scope and result

Let $A_0$ be a six-site source with only ground-color entries
$D_{ij}=A_{0,ij}(a,a)$, all nonzero, and $H(A_0)=0$.
Write

$$
A=A_0+\text{perturbation},\qquad
\delta=\|A-A_0\|,\qquad d=\min_{i<j}|D_{ij}|>0,
$$

$$
H(A)=\lambda(a^6+b^6+c^6)+E,\qquad
\varepsilon=\|E\|,\qquad E\perp(a^6+b^6+c^6).
$$

Let $X$ contain the entries with exactly one ground-color endpoint, and
let $T$ contain the entries with neither endpoint in the ground color.
Thus $\|X\|,\|T\|\le\delta$.

Fix a compact collection $\mathcal K$ of normalized four-site-flat sources
on the two non-ground colors, each belonging to one of these families:

- A complete five-site product core, with every core block nonzero.
- A complete four-site binary core, with every core block invertible.
- A spanning binary star, with every arm invertible.

The core families have all other sites isolated. The linked classification
and star estimates supply a local stability constant for each family,
uniform on the chosen compact collection. Rank-degenerate limits of these
families are excluded from the compact collection.

**Theorem.** For $\delta$ sufficiently small, if $T=0$ or the normalized
direction $T/\|T\|$ is sufficiently close to $\mathcal K$, then

$$
\boxed{|\lambda|\le C_1\varepsilon+C_2\delta^5.}
\tag{1}
$$

The constants are uniform for the chosen compact collection and base
$A_0$. This is a fifth-power bound in actual source distance on the stated
set of directions, not merely a statement about powers of an analytic
path parameter.

More precisely, there is an exactly four-site-flat source $Q$ in the
corresponding core or star family such that

$$
\boxed{
\|T-Q\|\le
\frac{2C_{\rm flat}}d
\left(\frac{\varepsilon}{\|T\|}+45\|X\|^2\right)
}
\quad(T\ne0).
\tag{2}
$$

Here $C_{\rm flat}$ is the scaled stability constant from the linked
theorems. Other critical support patterns and directions approaching a
degenerate core or star boundary are outside this statement.

## 2. Recover the four-site responses from mixed outputs

For each pair $ij$, take an output with color $a$ at exactly those two
sites and non-ground colors at the other four. Its coefficient is

$$
H_{a_i a_j w}
=A_{ij}(a,a)\,\bigl(H_4(T[V\setminus\{i,j\}])\bigr)_w
+\mathcal Q_{ij,w}.
\tag{3}
$$

Every term in $\mathcal Q$ uses two edges from $X$ and one from $T$.
There are fifteen matchings and three choices of the $T$ edge, so the
triangle inequality for their tensor products gives

$$
\|\mathcal Q\|\le45\|X\|^2\|T\|.
$$

All outputs on the left of (3) are off target; together they have norm at
most $\varepsilon$. If $\delta\le d/2$, then
$|A_{ij}(a,a)|\ge d/2$. Dividing the corresponding coordinates therefore gives

$$
\|\mathcal F_4(T)\|
\le \frac2d\left(\varepsilon+45\|X\|^2\|T\|\right).
\tag{4}
$$

Apply the scaled local stability theorem
$\|T-Q\|\le C_{\rm flat}\|\mathcal F_4(T)\|/\|T\|$.
This proves (2). No source jet has been fixed or discarded.

## 3. The fifth-power estimate

Set

$$
L=\frac{2C_{\rm flat}}d,\qquad K=46L.
$$

Shrink the source neighborhood so
$\delta\le\min(d/2,1,1/K)$, and put $t=\|T\|$.
If $T=0$, the pure $b$ coefficient is zero, so $|\lambda|\le\varepsilon$.
Otherwise there are two cases.

If $\varepsilon>t\delta^2$, the elementary matching bound gives

$$
|H_{b^6}(A)|=|H_{b^6}(T)|
\le15t^3\le15\varepsilon,
$$

because $t\le\delta$. Hence $|\lambda|\le16\varepsilon$.

If $\varepsilon\le t\delta^2$, equation (2) gives
$\|Z\|:=\|T-Q\|\le K\delta^2$ and $\|Q\|\le2\delta$.
All four-site responses of $Q$ vanish, so $DH_6(Q)=0$ and $H_6(Q)=0$.
The cubic matching expansion has only terms with two or three factors
from $Z$:

$$
\begin{aligned}
\|H_6(T)\|
&\le45\|Q\|\|Z\|^2+15\|Z\|^3\\
&\le105K^2\delta^5.
\end{aligned}
$$

Since $|H_{b^6}(A)-\lambda|\le\varepsilon$, both cases yield the explicit
choice

$$
|\lambda|\le16\varepsilon+105K^2\delta^5.
$$

This proves (1).

## 4. What the result contributes to the rate problem

At a full-support single-color zero-output limit, the previous jet
identities constrain a first non-ground direction to have vanishing
four-site responses when the first two output orders vanish. Equation (2)
controls departures from the stated smooth families for actual nearby
sources, with all complex perturbation entries allowed.

At the explicit rank-25 example, the
[critical support classification](rank25-critical-directions-2026-09-27.md)
leaves supports on at most four sites or stars centered at one of two
vertices. Thus the invertible four-core and star families are the directly
relevant smooth branches there. A five-clique cannot be the nonzero
first non-ground jet at any full-support single-color limit, as the
following stronger estimate shows.

For a near-GHZ sequence, $\varepsilon=o(|\lambda|)$, equation (1) implies
$|\lambda|=O(\delta^5)$ in this class. It still does not give the lower
bound $\varepsilon\ge c|\lambda|^3$ required for the unrestricted
square-root rate law. The useful new ingredient is the quantitative
normal form, which constrains subsequent cancellation calculations.

## 5. A sixth-power estimate for quantitatively dense five-site support

Write $C_{ij}(D)=\operatorname{haf}D[V\setminus\{i,j\}]$.
For every set $K$ of five sites, at least one $C_{ij}(D)$ with $i,j\in K$
is nonzero. To prove this, suppose all ten were zero and let $r$ be the
remaining site. Expanding $\operatorname{haf}D=0$ at each $i\in K$ gives
$D_{ir}C_{ir}(D)=0$, hence every remaining cofactor is zero as well.
This says $\mathcal F_4(D)=0$. But the scalar six-site star estimate has
$\gamma=1$ and nonzero arms, so it forces every leaf edge to be zero,
contrary to full support.

Consequently

$$
\chi=\min_{|K|=5}\ \max_{\{i,j\}\subset K}|C_{ij}(D)|>0.
$$

Suppose some five-site set $K$ obeys
$\|T_{ij}\|_F\ge\eta\|T\|$ for all its ten edges, where $\eta>0$ is fixed.
Put $G_{ij}=A_{ij}(a,a)$ and $M=\|D\|+1$.
In a sufficiently small neighborhood of $A_0$, the selected nonzero
cofactor in each $K$ has modulus at least $\chi/2$.

The output sector with exactly two non-ground colors is
$\operatorname{diag}(C(G))T+\mathcal Q_2$, where every remainder term
uses two $X$ edges and one ground edge. Therefore

$$
a\|T\|\le\varepsilon+45M\delta^2,\qquad a=\chi\eta/2>0.
$$

Using $|H_{b^6}|\le15\|T\|^3$ and $(u+v)^3\le4(u^3+v^3)$, for
$\varepsilon\le1$ this yields

$$
\boxed{
|\lambda|\le (1+60a^{-3})\varepsilon
+60(45M/a)^3\delta^6.
}
\tag{5}
$$

This bound needs the dense-support condition, but not four-site flatness.
It also excludes a five-clique in the support of a nonzero first
non-ground jet lying in $\ker DH(A_0)$: its nonzero edge at the selected
cofactor would already produce a first-order off-target coefficient.
Neither (1) nor (5) compares the output error to $|\lambda|^3$.
