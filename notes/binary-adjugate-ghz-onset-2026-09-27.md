# Binary adjugate responses and the remaining thirty onset directions

September 27, 2026. **Written proof with exact supporting checks; independent
audit pending.** The unrestricted square-root rate law remains open.

[Exact replay](../computations/binary-adjugate-ghz-2026-09-27/README.md) ·
[Illustrated guide](../explainers/CRITICAL-DIRECTION-GEOMETRY.md) ·
[GHZ project](../research/ghz-rates/README.md)

The identity below is the binary, six-site instance of the determinant
mechanism in the repository's earlier
[cap-adjugate note](cap-adjugate-six-boundary-identity.md).
The contribution here is its explicit norm certificate and its use in
the current onset problem. No priority claim is made for the underlying
rank-one determinant identity.

## 1. A same-color edge component suffices

Let $A_0$ be a six-site single-ground-color source with all ground
entries nonzero and zero hafnian. For a nearby ternary source write

$$
H(A)=\lambda(a^6+b^6+c^6)+E,\qquad
\varepsilon=\|E\|,\qquad \delta=\|A-A_0\|.
$$

Let $T$ be the binary non-ground source and $t=\|T\|$.
All norms are Hilbert or Frobenius norms.
For a binary edge block $G$, put

$$
\gamma(G)=\sqrt{|G_{bb}|^2+|G_{cc}|^2}.
$$

**Theorem.** Fix $\eta>0$. Near $A_0$, the estimate

$$
\boxed{|\lambda|\le C_1\varepsilon+C_2\delta^5}
\tag{1}
$$

holds if $T=0$ or any edge satisfies $\gamma(G)\ge\eta t$.
No matrix-rank or ground-cofactor condition is imposed on that edge.
All other blocks are unrestricted.

Together with the
[two-arm theorem](coherent-two-arm-ghz-onset-2026-09-27.md)
and [single-invertible-edge theorem](single-invertible-edge-ghz-onset-2026-09-27.md),
this gives a uniform estimate away from sources supported on one
different-color cell: $b$ at one endpoint and $c$ at the other.
There are $15\cdot2=30$ such complex lines in binary source space.
They are thirty projective directions, rather than thirty normalized
vectors: each line still allows arbitrary complex phase.

This remains an onset estimate at full-support single-color limits.
It is not the error-versus-signal inequality
$\varepsilon\ge c|\lambda|^3$ needed for the unrestricted rate law.

## 2. The response identity

Distinguish sites $0,1$ and put $L=\{2,3,4,5\}$.
Use binary colors $0=b$, $1=c$ at the distinguished sites.
Let $G=T_{01}$ and let $H_{ij}$ be the $i,j$ core slice of $H_6(T)$,
a tensor on $L$.

For $\{r,s\}\subset L$, let $F^{ij}_{rs}$ be the corresponding
four-site matching output on $\{0,1,r,s\}$ with core colors $i,j$.
Define the adjugate contraction

$$
\mathcal B(G,H)
=G_{00}H_{11}+G_{11}H_{00}
-G_{01}H_{10}-G_{10}H_{01}.
$$

Then, for every source,

$$
\boxed{
\mathcal B(G,H_6(T))
=\sum_{\{r,s\}\subset L}
\left(F^{00}_{rs}F^{11}_{uv}
-F^{01}_{rs}F^{10}_{uv}\right),
\quad \{u,v\}=L\setminus\{r,s\}.
}
\tag{2}
$$

The sum has six terms. Each partition into two pairs appears in
both orders. Products place factors at their labelled outside sites.
The outside palette may be any fixed finite palette.
No invertibility assumption or division by an edge entry is needed.

Here is a compact proof. Work in the commutative algebra where products
using a site twice are zero. Let $x$ collect outside edges, and let
$\ell_i,m_j$ collect the two root rows with the indicated core colors.
The pair-family response and the full-output slice are

$$
F_{ij}=G_{ij}x+\ell_i m_j,\qquad
H_{ij}=G_{ij}\frac{x^2}{2}+\ell_i m_j x.
$$

Thus $F=xG+\ell m^{\mathsf T}$.
The two-by-two rank-one determinant identity gives

$$
\det F=x^2\det G+x\,
\bigl(G_{00}\ell_1m_1+G_{11}\ell_0m_0
-G_{01}\ell_1m_0-G_{10}\ell_0m_1\bigr).
$$

This is exactly $\mathcal B(G,H)$.
Extracting the part using all four outside sites gives (2).
Equivalently, in a direct matching expansion, the terms using four
root attachments occur in both products and cancel.

## 3. A sharp quadratic response bound

Let

$$
f_{01}^2=\sum_{\{r,s\}\subset L}\sum_{i,j=0}^1
\|F^{ij}_{rs}\|^2.
$$

This is the squared norm of the four-site responses containing
both distinguished sites. If $f=\|\mathcal F_4(T)\|$, then $f_{01}\le f$.
For each core color pair write
$a_{ij}^2=\sum_{r<s}\|F^{ij}_{rs}\|^2$.
By (2), Cauchy--Schwarz and the complementary-pair bijection give

$$
\begin{aligned}
\|\mathcal B(G,H_6(T))\|
&\le a_{00}a_{11}+a_{01}a_{10}\\
&\le\frac12\sum_{i,j}a_{ij}^2.
\end{aligned}
$$

Consequently

$$
\boxed{\|\mathcal B(G,H_6(T))\|\le\tfrac12 f_{01}^2.}
\tag{3}
$$

The constant $1/2$ is sharp for this response norm.
Take $G=I$, put one $bb$ cell of weight one on each of edges $23,45$,
and set all other cells to zero. Then $f_{01}^2=4$ and the
contraction is $2b^4$, of norm two.
This fixture establishes sharpness of (3), not of the GHZ rate law.

The binary target satisfies

$$
\mathcal B(G,b^6+c^6)=G_{11}b^4+G_{00}c^4,
\qquad
\|\mathcal B(G,b^6+c^6)\|=\gamma(G).
$$

The linear contraction $H\mapsto\mathcal B(G,H)$ has operator norm
$\|\operatorname{adj}G\|_F=\|G\|_F$.
Therefore any approximation
$H_6(T)=\lambda(b^6+c^6)+E_{\rm bin}$ with
$\|E_{\rm bin}\|\le\varepsilon$ obeys the exact certificate

$$
\boxed{
|\lambda|\gamma(G)\le\|G\|\varepsilon+\tfrac12 f_{01}^2.
}
\tag{4}
$$

This certificate is independent of the ground source. It can be
computed directly from a proposed binary source.

## 4. Fifth-power onset

At the full-support ground limit, the
[mixed-output estimate](four-arm-ghz-distance-bound-2026-09-27.md)
gives

$$
f\le C(\varepsilon+t\delta^2),\qquad t\le\delta.
$$

If $T=0$, then $|\lambda|\le\varepsilon$.
If $\varepsilon>t\delta^2$, the elementary bound
$|\lambda|\le\varepsilon+15t^3\le16\varepsilon$ suffices.
In the remaining case, $f\le2Ct\delta^2$.
Apply (4) at an edge with $\gamma(G)\ge\eta t$ and use $\|G\|\le t$:

$$
|\lambda|\le\eta^{-1}\varepsilon+
\frac{f^2}{2\eta t}
\le\eta^{-1}\varepsilon+\frac{2C^2}{\eta}t\delta^4
\le C_1\varepsilon+C_2\delta^5.
$$

This proves (1). The constants are uniform under the stated
relative same-color strength hypothesis.

## 5. Why only thirty projective directions remain

Let $\mathcal A$ be the set of normalized sources supported on one
cell $T_{ij}(b,c)$ or $T_{ij}(c,b)$.
For every fixed $\rho_0>0$, (1) is uniform when $T=0$ or
$\operatorname{dist}(T/t,\mathcal A)\ge\rho_0$.

Consider the zeros of $\mathcal F_4$ in that compact normalized set.
A zero with two adjacent nonzero edges is covered by the two-arm
theorem. Otherwise its support is a matching. Two disjoint
nonzero edges have a nonzero tensor-product quartet with no
other term to cancel it, so a flat source of this type has only
one edge.

For that edge, any nonzero diagonal component is covered by the
present theorem. If both diagonal entries vanish, the matrix is

$$
\begin{pmatrix}0&u\\v&0\end{pmatrix}.
$$

When $uv\ne0$, the single-invertible-edge theorem applies.
When $uv=0$, nonzeroness leaves exactly one different-color cell,
which belongs to $\mathcal A$ and has been excluded.

A finite cover of the normalized zero set gives uniform constants
and positive relative thresholds for these three theorems.
On the remaining compact set the normalized four-site response
has a positive lower bound. The mixed-output estimate forces either
$t=O(\delta^2)$ or $t^2=O(\varepsilon)$, and the elementary cubic
output bound proves (1) there as well.

The remaining axes are genuine blind directions of the present
tests: they have zero four-site response, zero same-color edge
strength, no two-arm support, and no invertible edge.
Their six-site output is also zero. They are not counterexamples
to the rate law; perturbations near them still need analysis.
