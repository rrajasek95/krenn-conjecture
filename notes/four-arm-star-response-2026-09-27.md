# Four-arm stars: hidden directions and quadratic response control

September 27, 2026. **Written proofs with exact supporting checks; independent
audit pending.** No Lean verification or priority claim is made.

[Replay](../computations/four-arm-ghz-boundary-2026-09-27/README.md) ·
[GHZ application](four-arm-ghz-distance-bound-2026-09-27.md) ·
[Five-arm estimate](rank-free-star-response-bound-2026-09-27.md)

## 1. The complete linear-kernel classification

Let $S$ be a star with center $0$ and exactly four nonzero arms
$G_i=S_{0i}$, $i=1,2,3,4$. Additional sites are isolated.
Allow any finite common palette, and write $B_{ij}$ for leaf-to-leaf
perturbation blocks. The center-containing four-site responses are

$$
(L_G B)_{ijk}=G_iB_{jk}+G_jB_{ik}+G_kB_{ij},
\tag{1}
$$

with tensor factors placed at their labelled sites. Missing arms are zero.

**Theorem.** The kernel of $L_G$ is one of the following:

| Arms | Kernel dimension |
| --- | ---: |
| At least one arm has rank at least two | 0 |
| All arms have rank one, with four common center directions | 2 |
| All arms have rank one, with exactly two distinct center directions, each occurring twice | 1 |
| Every other rank-one pattern | 0 |

Here a center direction means a line in the center's color space.
Scalar factors in a rank-one factorization can be absorbed into the
leaf vectors.

More explicitly, in the common-direction case write $G_i=u v_i^{\mathsf T}$.
Every kernel vector has

$$
B_{ij}=b_{ij}v_iv_j^{\mathsf T},
$$

where

$$
b_{12}=b_{34}=x,\quad b_{13}=b_{24}=y,\quad
b_{14}=b_{23}=z,\qquad x+y+z=0.
\tag{2}
$$

In the two-pair case, relabel so $G_1,G_2$ use center vector $u$ and
$G_3,G_4$ use a nonproportional center vector $v$. Then the kernel is

$$
b_{12}=b_{34}=0,\quad
b_{13}=b_{24}=\tau,\quad b_{14}=b_{23}=-\tau,
\tag{3}
$$

with the same leaf factors. Every kernel block incident to an additional
isolated site is zero.

Consequently, for $q$ colors and $n\ge5$ total sites,

$$
\operatorname{rank}D\mathcal F_4(S)
=q^2\binom{n-1}{2}-d,\qquad d\in\{0,1,2\},
\tag{4}
$$

where $d$ is the kernel dimension above. The other derivative-kernel
directions are exactly the $q^2(n-1)$ changes to star arms, including
the initially absent arms.

## 2. Proof by polynomial factorization

Represent each block by its bilinear polynomial in the local color
variables. Tensor vanishing is equivalent to polynomial vanishing.
The polynomial ring is an integral domain; work temporarily in its
fraction field and put

$$
f_{ij}=B_{ij}/(G_iG_j).
$$

The four center-containing quartet equations say
$f_{ij}+f_{ik}+f_{jk}=0$. Their solutions have equal opposite pairs
$f_{12}=f_{34}$, $f_{13}=f_{24}$, $f_{14}=f_{23}$,
whose sum is zero. In particular,

$$
G_3G_4B_{12}=G_1G_2B_{34},
\tag{5}
$$

and the two analogous opposite-pair identities hold.

A bilinear polynomial of matrix rank at least two is irreducible:
a factorization of its degree-two homogeneous polynomial into linear
factors would have to put all center variables in one factor and all
leaf variables in the other, giving rank one.
Suppose $G_1$ has rank at least two. In (5), it divides neither
$G_3G_4$ (which has no leaf-1 variables) nor a nonzero $B_{12}$
(which has no center variables). Unique factorization therefore
forces $B_{12}=0$. The other opposite-pair identities give
$B_{13}=B_{14}=0$, then all remaining blocks vanish.

Now suppose every $G_i=\ell_i m_i$ has rank one, where $\ell_i$
uses center variables and $m_i$ uses leaf-$i$ variables.
If $B_{12}\ne0$, (5) forces $m_1m_2$ to divide $B_{12}$, and
similarly $m_3m_4$ to divide $B_{34}$. Thus these blocks have the
claimed leaf factors, and
$\ell_1\ell_2$ is proportional to $\ell_3\ell_4$.
The same argument applies to every nonzero pair.

There must be at least two nonzero opposite pairs, because the three
$f$ values sum to zero. If, for example, the first two are nonzero,
unique factorization of the linear center forms gives

$$
\ell_1\ell_2\sim\ell_3\ell_4,\qquad
\ell_1\ell_3\sim\ell_2\ell_4.
$$

Their quotient implies $\ell_2\sim\ell_3$ and
$\ell_1\sim\ell_4$. Thus either all four lines coincide or they form
two equal pairs. Substitution into (1) gives (2) or (3).
The other choices of nonzero pairs differ only by relabeling.

For an additional site $r$, the equations are
$G_iB_{jr}+G_jB_{ir}=0$ for distinct active leaves.
Three such equations imply $2G_iG_jB_{kr}=0$, hence all these blocks
vanish. A quartet consisting of the center, one active leaf, and two
additional sites then forces their mutual block to vanish.
This proves the kernel classification and (4). ∎

## 3. What the leaf-only response sees

Let $\mathcal Q(B)$ collect the four-site tensors using only leaves.
For a kernel vector in (2), its only possible nonzero component is
on leaves $1,2,3,4$ and equals

$$
(x^2+y^2+z^2)\,v_1\otimes v_2\otimes v_3\otimes v_4.
\tag{6}
$$

For (3), this is
$2\tau^2\,v_1\otimes v_2\otimes v_3\otimes v_4$.
Thus, in the two-pair case, for some fixed $C$,

$$
\|K\|^2\le C\|\mathcal Q(K)\|\qquad(K\in\ker L_G).
\tag{7}
$$

In the common-direction case, fix any one edge $e$ between the four
active leaves. Then

$$
\|K\|^2\le C\bigl(\|\mathcal Q(K)\|+\|K_e\|_F^2\bigr).
\tag{8}
$$

Indeed, if its selected coefficient is zero, the other two opposite-pair
coefficients are negatives, and their squared sum vanishes only when
both are zero. On the unit sphere in this two-dimensional kernel,
the right side of (8) therefore has a positive minimum.
Both sides are homogeneous of degree two under complex scaling.

For unit leaf vectors and $e=12$, one elementary estimate is
$\|K\|^2\le6|x^2+y^2+z^2|+24|x|^2$.
It follows from $z=-x-y$ and
$|y|^2\le|x^2+y^2+z^2|+3|x|^2$.

## 4. A refined estimate for nearby sources

Normalize the fixed star $S$ to norm one. Let a nonzero source $T$
have $T/\|T\|$ sufficiently close to $S$, put $t=\|T\|$, and split
$T=G+B$ into its star arms and its leaf blocks.
Write $\mathcal R(G,B)$ for the responses containing the center.

In the two-pair case, there is a constant $C$ such that

$$
\boxed{
\|B\|^2\le C\left(
\|\mathcal Q(B)\|+\frac{\|\mathcal R(G,B)\|^2}{t^2}
\right).
}
\tag{9}
$$

In the common-direction case, for any fixed active leaf edge $e$,

$$
\boxed{
\|B\|^2\le C\left(
\|\mathcal Q(B)\|+\|B_e\|_F^2
+\frac{\|\mathcal R(G,B)\|^2}{t^2}
\right).
}
\tag{10}
$$

In the zero-kernel case the stronger linear estimate
$\|B\|\le C\|\mathcal R(G,B)\|/t$ holds.

**Proof.** Project $B=K+Z$ onto $\ker L_S$ and its orthogonal complement.
On the complement, $L_S$ has a positive least singular value.
If the normalized arms differ from those of $S$ by at most $\eta_0$,

$$
\|Z\|\le C\left(\|\mathcal R(G,B)\|/t+\eta_0\|B\|\right).
$$

Use (7) or (8) on $K$. Since $\mathcal Q$ is quadratic,
$\mathcal Q(B)-\mathcal Q(K)$ is bounded in norm by a constant times
$\|K\|\|Z\|+\|Z\|^2$. Also $\|K_e\|\le\|B_e\|+\|Z\|$.
Young's inequality absorbs the mixed term and gives

$$
\|B\|^2\le C\bigl(\|\mathcal Q(B)\|+\|B_e\|^2+\|Z\|^2\bigr),
$$

with the edge term omitted in the two-pair case. Substituting the
$Z$ estimate and choosing $\eta_0$ small enough proves (9)–(10).
The zero-kernel case follows directly from the singular-value bound.
The same linear conclusion holds near a star with five nonzero arms
by the earlier rank-independent star theorem. ∎

## 5. A sharp square-root obstruction in the two-pair case

Use two colors, six sites, and unit vectors $e_0,e_1$. Set

$$
G_1=G_2=e_0e_0^{\mathsf T},\qquad
G_3=G_4=e_1e_0^{\mathsf T},\qquad G_5=0.
$$

Add the kernel vector (3) with every leaf vector $e_0$.
Every center-containing response remains zero, while the only leaf
response is $2\tau^2 e_0^{\otimes4}$. Thus

$$
\|\mathcal F_4(S+\tau K)\|=2|\tau|^2,\qquad
\|\tau K\|=2|\tau|.
$$

Equation (9) shows that all nearby flat sources are stars with this
center. Their distance is therefore $2|\tau|$ for sufficiently small
$\tau$. A linear bound by $\|\mathcal F_4\|$ is impossible here;
the square-root distance exponent is optimal.

This does not contradict the GHZ rate conjecture. Its extra mixed-output
constraints are absent from this response-only example.
In the common-direction case, (6) instead permits actual five-core
branches with $(x,y,z)$ proportional to $(1,\omega,\omega^2)$.
The edge term in (10) is essential for excluding those branches.
