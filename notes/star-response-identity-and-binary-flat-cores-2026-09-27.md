# An exact star-response identity and rigidity of binary flat cores

September 27, 2026. **Written proofs with exact supporting checks; independent
audit pending.** No Lean verification or priority claim is made.

[Replay](../computations/flat-core-rigidity-2026-09-27/README.md) ·
[Five-clique classification](flat-four-response-five-clique-2026-09-27.md)

Write $\mathcal F_4(A)$ for the collection of all four-site matching
tensors. The following results describe two useful kinds of its zeros.

## 1. A sharp identity at an identity-matrix star

Use a center $0$ and $k$ leaves, with $q$ colors per site. Suppose every
star block is $A_{0i}=I_q$. Write $B_{ij}=A_{ij}$ for the leaf-to-leaf
blocks, with $B_{ji}=B_{ij}^{\mathsf T}$, and put

$$
T_\star=\sum_{1\le i<j<l\le k}\|H_4(A[\{0,i,j,l\}])\|^2.
$$

**Identity, for arbitrary complex leaf blocks:**

$$
\boxed{
T_\star=\bigl(q(k-2)-2\bigr)\sum_{i<j}\|B_{ij}\|_F^2
+\sum_i\left\|\sum_{j\ne i}B_{ij}\right\|_F^2.
}
\tag{1}
$$

**Proof.** Each four-site tensor has three terms, each pairing one leaf
with the center. A squared term contributes
$\|I_q\|_F^2\|B_{ij}\|_F^2=q\|B_{ij}\|_F^2$.
Each leaf edge occurs in $k-2$ of the triples.

In a cross term, contraction against the two identity matrices identifies
their color indices. The remaining inner product is that of two leaf
blocks sharing a vertex, both oriented away from that vertex. These are
exactly the cross terms in the row-sum squares on the right.
Those row-sum squares count each diagonal leaf-block norm twice. Subtract
these two copies from the diagonal coefficient $q(k-2)$ to obtain (1). ∎

If $\gamma=q(k-2)-2>0$, this gives

$$
T_\star\ge\gamma\sum_{i<j}\|B_{ij}\|_F^2.
\tag{2}
$$

For $q\ge2$, the coefficient is sharp: place any nonzero antisymmetric
matrix $J$ on an oriented three-cycle of leaves, with signs making all
row sums zero, and set the other leaf blocks to zero. For $q=1$ and
$k\ge4$, alternating signs on a four-cycle give the same sharpness for
$T_\star$. In particular:

| Palette and size | $\gamma$ |
| --- | --- |
| One color, six sites | $1$ |
| Two colors, five sites | $2$ |
| Two colors, six sites | $4$ |
| Three colors, six sites | $7$ |

The boundary values explain two exceptional cancellation families:
$q=1,k=4$ and $q=2,k=3$ have $\gamma=0$, so nonzero leaf blocks can
survive if their row sums cancel.

## 2. Arbitrary invertible star arms

Suppose instead that the star arms $G_i=A_{0i}$ are invertible. Define

$$
\alpha=\min_i\sigma_{\min}(G_i)>0,\qquad
M=\max_i\|G_i\|_{\rm op}.
$$

Apply $(G_i^{-1})^{\mathsf T}$ at leaf $i$, and the identity at the
center. Every star arm becomes $I_q$. A transformed leaf block has norm
at least $\|B_{ij}\|_F/M^2$, and a transformed observed four-site tensor
has norm at most its original norm divided by $\alpha^3$.
Thus, when $\gamma>0$,

$$
\boxed{
\|\mathcal F_4(A)\|^2\ge T_\star
\ge\frac{\gamma\alpha^6}{M^4}\sum_{i<j}\|A_{ij}\|_F^2.
}
\tag{3}
$$

Consequently an exactly four-site-flat source with this invertible
spanning star has no leaf-to-leaf edges. More generally, deleting those
edges gives an exactly flat star and the explicit distance bound

$$
\operatorname{dist}(A,\{\text{stars centered at }0\})
\le\frac{M^2}{\sqrt\gamma\,\alpha^3}\|\mathcal F_4(A)\|.
\tag{4}
$$

This estimate does not require the other blocks to be small. It applies
to any source with the stated invertible arms.

For a binary star on $n\ge5$ sites, the derivative of $\mathcal F_4$ is
injective on the non-star blocks by (3). Its kernel consists exactly of
the $4(n-1)$ star entries, so its rank is
$4\binom n2-4(n-1)$. At six sites this is 40.

## 3. The other binary exception: an invertible four-site core

For two colors, define

$$
I=\begin{pmatrix}1&0\\0&1\end{pmatrix},\qquad
J=\begin{pmatrix}0&1\\-1&0\end{pmatrix}.
$$

On four sites $0,1,2,3$, put

$$
A_{01}=A_{02}=A_{03}=I,\qquad
A_{12}=J,\quad A_{13}=-J,\quad A_{23}=J.
\tag{5}
$$

Its four-site tensor is zero. All six blocks are invertible.

**Classification.** Every binary four-site-flat source with all six blocks
invertible is equivalent to (5) under invertible local changes of basis.
If it sits inside a larger four-site-flat source, all other sites are isolated.

**Proof on four sites.** Normalize the three blocks incident to site 0
to identities by separate changes of basis at sites 1, 2, and 3.
The elementary four-site calculation in section 2 of the
[five-clique proof](flat-four-response-five-clique-2026-09-27.md) gives
the other blocks as $tJ,-tJ,tJ$. Here $t\ne0$.
A scalar change $cI$ at site 0 and $c^{-1}I$ at each leaf preserves the
three identities and replaces $t$ by $t/c^2$. Choosing $c^2=t$ gives (5).

**Isolation.** Fix one color at an outside site and let $X_i\in\mathbb C^2$
be its four incident rows into the core. The equation on that outside site
and core triple $0,1,2$ gives

$$
X_1=-JX_0,\qquad X_2=JX_0.
$$

The equation with triple $0,1,3$ gives

$$
X_1=JX_0,\qquad X_3=-JX_0.
$$

These formulas follow by reading the eight binary coefficients of each
three-site tensor. Together they force all $X_i=0$.
This applies to every outside color. A four-site equation with two outside
sites and two core sites then forces their outside-to-outside block to be
zero as well. ∎

## 4. Derivative rank and local stability of the four-site core

The core zero set has dimension 13. Indeed, the three invertible star
blocks give 12 free coordinates. After normalizing them, the remaining
12 coordinates must lie on the one-dimensional line
$(tJ,-tJ,tJ)$. In these normalized coordinates the four-site output is
linear in those 12 coordinates and has kernel exactly that line, hence
rank 11.

For each outside site, the two triangle calculations above make all eight
outside-to-core variables independent for each outside color, contributing
16 to the derivative rank. Each outside-to-outside block contributes four
independent coordinates. Therefore on $n\ge4$ binary sites,

$$
\boxed{\operatorname{rank}D\mathcal F_4=4\binom n2-13.}
\tag{6}
$$

At six sites the rank is 47. The kernel is exactly the 13-dimensional
tangent space to the local-basis orbit of (5).

The derivative is injective normal to this smooth family. The
nearest-point and Taylor argument in section 7 of the five-clique proof
therefore gives a local bound

$$
\operatorname{dist}(T,\{\mathcal F_4=0\})
\le C\|\mathcal F_4(T)\|.
$$

By scaling, the bound becomes
$C\|\mathcal F_4(T)\|/\|T\|$ near a compact collection of normalized
nondegenerate four-site cores. Together with (4), this supplies two
quantitative critical families for the GHZ rate investigation.

The hypotheses on invertibility matter. These estimates do not provide
uniform constants as a star arm or a core block loses rank.
