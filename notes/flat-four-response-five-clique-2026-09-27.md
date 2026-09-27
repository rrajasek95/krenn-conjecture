# Classifying a five-clique when every four-site response vanishes

September 27, 2026. **Written proof with exact supporting checks; independent
audit pending.** No literature-priority or Lean-verification claim is made.

[Replay](../computations/flat-core-rigidity-2026-09-27/README.md) ·
[GHZ application](ghz-critical-direction-normal-form-2026-09-27.md)

## 1. Statement

Let $A$ be a complex colored source on $n\ge5$ sites, with $q$ colors at
each site. Write

$$
\mathcal F_4(A)=\bigl(H_4(A[U])\bigr)_{|U|=4}
$$

for the collection of all four-site matching tensors. The support graph
has edge $ij$ when the whole block $A_{ij}$ is nonzero.

**Theorem 1.** Suppose $\mathcal F_4(A)=0$ and the support contains a
complete graph on five sites. Then:

1. All edges outside that five-site core, including edges incident to it,
   are zero.
2. After labelling its sites $0,1,2,3,4$, there are nonzero local vectors
   $v_i\in\mathbb C^q$ such that

$$
A_{ij}=c_{ij}v_i v_j^{\mathsf T},
\tag{1}
$$

where, for $\omega^2+\omega+1=0$,

$$
c_{01}=c_{23}=1,\quad
c_{02}=c_{13}=\omega,\quad
c_{03}=c_{12}=\omega^2,\quad
c_{i4}=1\quad(i<4).
\tag{2}
$$

Conversely every source (1)–(2), with all other sites isolated, has
$\mathcal F_4(A)=0$.

In particular every edge block has rank one, and all incident blocks use
the same color direction at a given site. The directions may differ
between sites. Scalar site factors are absorbed into $v_i$; this is a
classification, not a norm-preserving normalization.

**Theorem 2.** At every such source,

$$
\operatorname{rank}D\mathcal F_4(A)
=\binom n2q^2-5q.
\tag{3}
$$

The local zero set is a smooth complex manifold of dimension $5q$,
parameterized by its five local vectors. There are a neighborhood and a
constant $C$ such that

$$
\operatorname{dist}(B,\{\mathcal F_4=0\})
\le C\|\mathcal F_4(B)\|.
\tag{4}
$$

The constants can be chosen uniformly near any compact collection of
normalized sources of this type whose ten core blocks stay nonzero.

The five-clique hypothesis is essential. Four-site examples with all six
blocks invertible and zero matching tensor exist; the replay includes one.

## 2. In two colors, an invertible edge is impossible on the five-clique

For this part label the five sites $1,\ldots,5$. Put

$$
J=\begin{pmatrix}0&1\\-1&0\end{pmatrix}.
$$

We use the following elementary four-site calculation. If $A_{12}=A_{13}=I$
and $A_{14}=C\ne0$, the zero matching tensor says

$$
\delta_{ab}(A_{34})_{cd}
+\delta_{ac}(A_{24})_{bd}
+C_{ad}(A_{23})_{bc}=0.
$$

Its solutions are precisely

$$
A_{23}=tJ,\qquad A_{24}=-tJC,\qquad A_{34}=tJC.
\tag{5}
$$

For completeness, the choices $(a,b,c)=(0,1,1),(1,0,0)$ force the two
diagonal entries of $A_{23}$ to vanish whenever the corresponding row of
$C$ is nonzero. The choices with $a=b\ne c$ or $a=c\ne b$ express every row
of $A_{34},A_{24}$ in terms of $C$ and the off-diagonal entries. Substitution
into $a=b=c$ forces the remaining diagonal entries to vanish and the
off-diagonal entries to sum to zero. This also covers a zero row of $C$,
since its other row is nonzero. It gives (5), which directly satisfies all
sixteen coefficients.

Suppose two edges meeting at site 1 are invertible. Independent changes of
basis at sites 2 and 3 make $A_{12}=A_{13}=I$. Apply (5) to $1234$ and
$1235$. With $C=A_{14}$ and $D=A_{15}$, the same $t$ gives

$$
A_{24}=-tJC,\qquad A_{25}=-tJD.
$$

Now sum the coefficients of the $1245$ identity over equal colors at
sites 1 and 2. The last two terms cancel because $J^{\mathsf T}=-J$:

$$
2A_{45}+C^{\mathsf T}(-tJD)+(-tJC)^{\mathsf T}D=2A_{45}=0.
$$

This contradicts the five-clique support. Thus at most one invertible edge
can meet any site.

Suppose instead that $A_{12}$ is invertible and is the only invertible edge
at site 1. Set it to $I$. For $j=3,4,5$, write
$A_{1j}=x_j y_j^{\mathsf T}$, with both vectors nonzero.
For distinct $j,k$, the vectors $x_j,x_k$ must be independent: otherwise
the last two terms of the $12jk$ identity have rank one across site 1,
whereas $I\otimes A_{jk}$ has rank two.

Contract that identity with the two linear forms dual to $x_j,x_k$.
It follows that

$$
A_{jk}=t_{jk}y_jy_k^{\mathsf T},\qquad
A_{2j}=b_j(Jx_j)y_j^{\mathsf T}.
$$

The coefficients $b_j$ are nonzero because $A_{2j}\ne0$. Removing the
nonzero factors $y_j,y_k$ from the same identity gives

$$
t_{jk}I+b_kx_j(Jx_k)^{\mathsf T}
             +b_jx_k(Jx_j)^{\mathsf T}=0.
$$

Multiply on the right by $J$ and take the symmetric part. Since
$x_jx_k^{\mathsf T}+x_kx_j^{\mathsf T}\ne0$, this gives $b_j+b_k=0$.
Three nonzero numbers cannot each be the negative of the other two.
This is a contradiction.

Every nonzero two-by-two block therefore has rank one.

For any larger palette, a block of rank at least two would survive as an
invertible two-by-two block under suitable local linear projections.
The projections can simultaneously keep all ten blocks nonzero: each
requirement excludes the zero set of a nonzero polynomial, and a finite
product of nonzero polynomials is nonzero over $\mathbb C$. Four-site
vanishing is preserved by these projections. The two-color result rules
this out. Thus every block has rank one for every palette.

## 3. Rank-one blocks must share their local directions

Three nonzero decomposable tensors whose sum is zero can differ in their
local directions at at most one site. Indeed, if two terms differ at two
sites, their sum has matrix rank two across either of those sites and
cannot equal the third decomposable tensor. If two terms are proportional,
all three are proportional and there is no exceptional site.

Apply this observation to the three matching terms on each four-clique.
At least three of its vertices therefore have all three incident local
directions proportional.

Suppose site 1 has different directions toward sites 2 and 3. The
four-cliques $1234$ and $1235$ force sites 2 and 3 to have a common
direction on all their incident edges. They also align the directions at
site 4 toward $1,2,3$, and at site 5 toward $1,2,3$.
At least one of $1245$ and $1345$ is still exceptional at site 1, so it
aligns the remaining directions on edge $45$ at both endpoints.
All sites except possibly site 1 now have a single local direction.

Write the four edges at site 1 as $x_j\otimes u_j$, and all edges among the
other four sites as $d_{jk}u_j\otimes u_k$, with $d_{jk}\ne0$. The four-site
equations involving site 1 become

$$
d_{kl}x_j+d_{jl}x_k+d_{jk}x_l=0
\quad\text{for every triple }j,k,l.
$$

These are the kernel equations of the symmetric four-by-four matrix with
zero diagonal and off-diagonal entry $d_{kl}$ complementary to its two
indices. Every three-by-three principal minor is twice the product of
three nonzero entries, so its rank is at least three. Its kernel has
dimension at most one. Applying the equations to each coordinate of the
$x_j$ forces all $x_j$ to be proportional, a contradiction.

Every site consequently has a single local direction. The problem reduces
to nonzero scalar weights $d_{ij}$.

## 4. The remaining scalar solution is the cube-root core

Return to labels $0,\ldots,4$. Scalar site factors make $d_{i4}=1$ for
$i<4$. The four-site equations containing site 4 say that the sum of the
three weights on each triangle among $0,1,2,3$ is zero. Solving those four
linear equations gives opposite pairs

$$
d_{01}=d_{23}=a,\quad d_{02}=d_{13}=b,\quad
d_{03}=d_{12}=c,\qquad a+b+c=0.
$$

The remaining four-site equation is $a^2+b^2+c^2=0$. Since $a\ne0$,
$(b/a)^2+b/a+1=0$. Thus $(a,b,c)$ is proportional to
$(1,\omega,\omega^2)$, up to exchanging two core labels.
A final scalar site change sets $a=1$ while retaining $d_{i4}=1$.
Absorbing all site factors into the local vectors proves (1)–(2).

It also proves that **no real colored source with $\mathcal F_4=0$ can
have a five-clique in its support**. Real rank-one blocks can be factored
over the reals, but the scalar equations would give three nonzero real
numbers with $a^2+b^2+c^2=0$.

## 5. A scalar minor excludes every outside edge

Let $M$ be the derivative of the five scalar four-site hafnians with
respect to the ten core edges, at (2). Its rows are indexed by the
omitted site. On columns $01,02,03,12,13$, its minor is

$$
\begin{pmatrix}
0&0&0&1&1\\
0&1&1&0&0\\
1&0&1&0&1\\
1&1&0&1&0\\
1&\omega&\omega^2&\omega^2&\omega
\end{pmatrix},
\qquad \det=-4-8\omega\ne0.
\tag{6}
$$

In particular $\operatorname{rank}M=5$. The map

$$
(x_i)_{i=0}^4\longmapsto
\bigl(x_i c_{jk}+x_j c_{ik}+x_k c_{ij}\bigr)_{i<j<k}
\tag{7}
$$

is $M^{\mathsf T}$, after relabelling each triple by its complementary
pair. It is injective.

Change local bases on the core so its five local directions are the first
basis vectors. Fix an outside site $r$ and one of its colors. In the
equation on $r,i,j,k$, any non-first color at core site $i$ occurs only
in $A_{ri}$ multiplied by $c_{jk}\ne0$. Thus those entries of $A_{ri}$
vanish. The entries using the first core colors then satisfy (7), and
vanish too. All outside-to-core blocks are zero.
An equation on two outside sites and two core sites now forces their
outside-to-outside block to vanish. This proves the isolation assertion
without a support enumeration.

## 6. The derivative kernel consists exactly of changes to the five vectors

At the canonical source, use color 0 for each core direction.
Internal perturbations separate into three disjoint output sectors:

| Perturbed core colors | Derivative rank |
| --- | --- |
| Both are 0 | $5$, by (6) |
| Exactly one is nonzero | $15(q-1)$ |
| Both are nonzero | $10(q-1)^2$ |

For the middle row, fix its site and nonzero color. The four incident
entries are acted on by the four-by-four complementary-edge matrix from
section 3. It has rank at least three, and it has the nonzero kernel
vector $(c_{ij})_{j\ne i}$ because each four-site hafnian vanishes.
Its rank is exactly three.

For the last row, fixing its two nonzero colors singles out the varied
edge, multiplied by a nonzero complementary core edge.
The internal rank is therefore $10q^2-5q$.

For each outside site, the same separation as in section 5 makes all
$5q^2$ outside-to-core directions independent. Every outside-to-outside
block contributes a further $q^2$ independent directions, distinguished
by its two outside positions. These output sectors are disjoint, giving (3).

Varying the five vectors in (1) supplies $5q$ kernel directions.
This parameter map has injective derivative: its non-first colors are
detected on the incident edges, and its remaining scalar kernel would
require $t_i+t_j=0$ on every core edge, forcing every $t_i=0$.
Thus these variations are the whole kernel.

## 7. Why the classification is stable

The five-vector parameterization is a smooth local manifold of zeros.
Its tangent space is exactly the derivative kernel. On the orthogonal
normal space, the derivative therefore has a positive least singular
value. This remains bounded below in a sufficiently small neighborhood.

Choose a nearest point $P$ on this local manifold and write $B=P+Z$,
where $Z$ is normal to it. Taylor expansion gives

$$
\mathcal F_4(B)=D\mathcal F_4(P)[Z]+O(\|Z\|^2).
$$

For sufficiently small $\|Z\|$, the linear lower bound dominates the
remainder, so $\|\mathcal F_4(B)\|\ge c\|Z\|$. This proves (4) and also
shows that there are no additional nearby zeros outside the manifold.
Compactness gives the stated uniformity.

Since $\mathcal F_4$ is homogeneous of degree two, the scaled version is

$$
\operatorname{dist}(T,\{\mathcal F_4=0\})
\le C\frac{\|\mathcal F_4(T)\|}{\|T\|}
\tag{8}
$$

whenever $T\ne0$ and its normalized direction lies in the specified
neighborhood of a compact collection of normalized five-clique cores.
The nearest zero may be chosen from the corresponding five-clique
manifolds. The [GHZ application](ghz-critical-direction-normal-form-2026-09-27.md)
uses this conclusion; it does not assume a global error bound on other
support strata.
