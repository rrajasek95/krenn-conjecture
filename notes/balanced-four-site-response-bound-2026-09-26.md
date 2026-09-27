# A sharp norm identity for four-site matching responses

September 26, 2026. **Written proof with exact supporting checks; independent
audit pending.** No formal verification or literature-priority claim is made.

[Replay](../computations/site-balancing-2026-09-26/README.md) ·
[Global normalization](site-balancing-rate-reduction-2026-09-26.md) ·
[Illustrated guide](../explainers/SITE-BALANCING.md)

## 1. Identity and sharp six-site bound

Allow arbitrary complex edge blocks and any fixed finite color dimension.
For $i\ne j$, orient the blocks by $A_{ji}=A_{ij}^{\mathsf T}$, and set

$$
 w_{ij}=\|A_{ij}\|_F^2,\quad S=\sum_{i<j}w_{ij},\quad
 d_i=\sum_{j\ne i}w_{ij},\quad \rho_{ij}=A_{ij}A_{ij}^{\dagger}.
$$

Let $M$ be the symmetric matrix whose off-diagonal site blocks are $A_{ij}$
and whose diagonal site blocks are zero. Define

$$
 \begin{aligned}
 T_4&=\sum_{|U|=4}\|H_4(A[U])\|^2,\\
 L&=\sum_i\sum_{\substack{j<k\\j,k\ne i}}
       \bigl(w_{ij}w_{ik}-\operatorname{tr}(\rho_{ij}\rho_{ik})\bigr),\\
 O&=\sum_{i<j}\|(MM^\dagger)_{ij}\|_F^2.
 \end{aligned}
$$

Here $H_4$ is the four-site matching tensor, with three pairings, and the
subscript $ij$ on $MM^\dagger$ means a whole site block.

**Exact identity, any number of sites:**

$$
 \boxed{T_4=\frac{S^2}{2}-\frac34\sum_i d_i^2
               +\sum_{i<j}w_{ij}^2+\frac L2+\frac O2.}          \tag{1}
$$

Both $L$ and $O$ are nonnegative. For the former, positive semidefinite
matrices satisfy
$\operatorname{tr}(\rho\sigma)\le
\operatorname{tr}(\rho)\operatorname{tr}(\sigma)$: for example,
$\rho\le\operatorname{tr}(\rho)I$.

At **six sites**, write

$$
 V_d=\sum_i(d_i-S/3)^2,\qquad
 V_w=\sum_{i<j}(w_{ij}-S/15)^2.
$$

Equation (1) becomes the sum-of-nonnegative-terms identity

$$
 \boxed{T_4+\frac34V_d=\frac{S^2}{15}+V_w+\frac L2+\frac O2.}    \tag{2}
$$

In particular a balanced source, $d_i=S/3$, satisfies the sharp bound

$$
                              T_4\ge S^2/15.                    \tag{3}
$$

Even without balance, (2) quantifies the necessary imbalance for a small
response. Complete four-site cancellation implies $V_d\ge4S^2/45$.

## 2. Elementary proof by separating site collisions

Use ordinary commuting variables $z_{i,a}$, one for each site and color.
Give monomials the orthogonal inner product
$\|z^\alpha\|^2=\alpha!=\prod_r\alpha_r!$. Write

$$
 P(z)=\tfrac12z^{\mathsf T}Mz
     =\sum_{i<j}z_i^{\mathsf T}A_{ij}z_j.
$$

We first claim

$$
 \left\|\frac{P^2}{2}\right\|^2
          =\frac{S^2}{2}+\frac14\operatorname{tr}((MM^\dagger)^2). \tag{4}
$$

To check this, expand $P^2/2=\frac18\sum M_{ab}M_{cd}z_a z_b z_c z_d$.
The monomial inner product is the sum over all 24 bijections between the
four unbarred and four barred indices; this remains true when indices repeat,
because the number of matching bijections is precisely the factorial norm.
Eight bijections keep each unbarred pair together and give
$8\|M\|_F^4/64$. The other sixteen split both pairs and give
$16\operatorname{tr}((MM^\dagger)^2)/64$, using symmetry of $M$.
Since $\|M\|_F^2=2S$, this is (4).

Now split the left side into orthogonal groups according to site
multiplicities. No site can occur more than twice, since each factor of
$P$ joins distinct sites. There are three possibilities:

| Site multiplicities | Contribution |
|---|---|
| Four distinct sites | $T_4$ |
| Site $i$ twice, distinct $j,k$ once | $w_{ij}w_{ik}+\operatorname{tr}(\rho_{ij}\rho_{ik})$ |
| Sites $i,j$ twice each | $\frac12(w_{ij}^2+\operatorname{tr}(\rho_{ij}^2))$ |

For the middle row, contracting the two indices at site $i$ has two
possibilities: they stay paired or cross. These give the two displayed terms.
For the last row, contract the two indices at each endpoint in the square
of $\frac12(z_i^{\mathsf T}A_{ij}z_j)^2$. Two of the four contractions give
$w_{ij}^2/4$, and two give $\operatorname{tr}(\rho_{ij}^2)/4$.

For transparent algebra, abbreviate

$$
 \begin{aligned}
 E_w&=\sum_{i<j}w_{ij}^2,& E_\rho&=\sum_{i<j}\operatorname{tr}(\rho_{ij}^2),\\
 W&=\sum_i\sum_{j<k;,j,k\ne i}w_{ij}w_{ik}
       =\tfrac12\sum_i d_i^2-E_w,&
 V&=\sum_i\sum_{j<k;,j,k\ne i}\operatorname{tr}(\rho_{ij}\rho_{ik}).
 \end{aligned}
$$

We have $L=W-V$ and
$\operatorname{tr}((MM^\dagger)^2)=2E_\rho+2V+2O$.
Subtracting the last two rows of the table from (4) gives

$$
 \begin{aligned}
 T_4&=S^2/2+(E_\rho+V+O)/2-(W+V)-(E_w+E_\rho)/2\\
    &=S^2/2-\tfrac34\sum_i d_i^2+E_w+(L+O)/2.
 \end{aligned}
$$

This proves (1). Expanding $V_d,V_w$, using $\sum_i d_i=2S$ and
$\sum_{i<j}w_{ij}=S$, proves (2) and (3). ∎

The replay independently expands $P^2/2$ on a dense complex fixture and
checks (4), both collision formulas, and the four-distinct-site matching
sum. Further colored, unbalanced, and cancellation examples check (1).
These finite calculations support the universal written argument above.

## 3. Sharpness and equality structure

Use just one color. Label the sites $0,1,2,3,4,\infty$, and define a real
symmetric zero-diagonal matrix $C$ by

$$
 C_{i\infty}=1,\qquad
 C_{ij}=\begin{cases}
    1,&i-j\equiv1,4\pmod5,\\
   -1,&i-j\equiv2,3\pmod5,
 \end{cases}\quad (i,j<5).
$$

Direct multiplication gives $CC^{\mathsf T}=5I$. With $A_{ij}=C_{ij}$,
every edge has $w_{ij}=1$, every site has $d_i=5$, and $S=15$.
The local Gram slack and off-diagonal Gram blocks both vanish. Hence
$T_4=15=S^2/15$. Equivalently, all fifteen four-site hafnians are (1) or
(-1). The constant in (3) cannot be improved, even over real scalar sources.
This construction is a symmetric conference matrix; its properties here
are directly checkable from the displayed entries.

There is also an equality description for $S>0$. Equality in (3) forces
every $w_{ij}=S/15>0$, every local Gram slack to vanish, and $O=0$.
At any site, normalize each incident density matrix to trace one. Equality
$\operatorname{tr}(\rho\sigma)=1$ forces both to be the same rank-one
projection: the largest eigenvalue must be one, and the other density matrix
must be supported on that eigenspace. It follows that there are unit site
vectors $u_i$ such that

$$
                      A_{ij}=c_{ij}u_i u_j^{\mathsf T}.
$$

The symmetric scalar matrix $C=(c_{ij})$ has zero diagonal,
$|c_{ij}|^2=S/15$, and $CC^\dagger=(S/3)I$. Conversely these conditions
give equality. Thus equality reduces to uniform-modulus complex symmetric
conference matrices after fixing one color direction at each site. This
does not assert a classification of all such conference matrices.

## 4. What this controls in the six-site derivative

For a source entry on edge $ij$ with endpoint colors $a,b$, differentiation
of the six-site tensor fixes those two colors and leaves the four-site
matching tensor on the complementary sites. Thus the corresponding column
of $DH_6(A)$ has norm exactly
$\|H_4(A[V\setminus\{i,j\}])\|$.

There are fifteen such cofactor norms. Equations (2)--(3) imply that for a
balanced source at least one column obeys

$$
                      \|\text{column of }DH_6(A)\|\ge S/15.      \tag{5}
$$

In particular $DH_6(A)\ne0$ whenever the balanced source is nonzero.
If the palette has $q$ colors, $\|DH_6(A)\|_F^2=q^2T_4$.

This bounds an individual column and hence the largest singular value from
below. It gives **no positive lower bound on the smallest singular value**,
and no guarantee of response in the GHZ direction. A balanced source can
still have a large kernel. Consequently this result does not establish the
unrestricted square-root rate law.

## 5. A support consequence for complete cancellation

**Corollary.** If every colored four-site matching tensor of a complex source
vanishes, its support graph has matching number at most two.

**Proof.** Otherwise restrict to the six endpoints of three disjoint nonzero
edge blocks. All four-site tensors still vanish, and the six-site support
contains a perfect matching. Consider the closure of its product-one positive
site-scaling orbit, *without deleting any edges*. Along this orbit the
product of the block norms on the chosen matching is a fixed positive number.
By continuity it has the same value throughout the closure, so the closure
does not contain the zero source.

The squared norm attains a positive minimum in this closed set: intersect
with any bounded nonempty sublevel set and use finite-dimensional compactness.
The orbit closure is invariant under every fixed positive site scaling.
Differentiating the norm along such scalings at a minimizer gives balance,
exactly as in the normalization theorem.

Under a finite site scaling, each four-site tensor is multiplied by the
product of its four site factors. Its vanishing is therefore preserved by
scaling and by limits. The balanced nonzero minimizer would have $T_4=0$,
contradicting (3). ∎

The orbit-closure step matters: pruning preserves the full six-site output,
but need not preserve every four-site tensor. We do not use pruning in this
corollary. The proof applies to any number of sites by the six-site restriction,
and to any finite palette over the complex numbers.

## 6. A higher-site consequence

For balanced $n\ge6$, (1) and Cauchy--Schwarz on the
$\binom n2$ edge weights give

$$
 T_4\ge\left(\frac12-\frac3n+\frac{2}{n(n-1)}\right)S^2
       =\frac{(n-5)(n-2)}{2n(n-1)}S^2.
$$

Only at six sites are these four-site tensors the columns of the first
derivative of the full matching map. We claim sharpness here only for the
six-site bound; higher-site equality requires additional constructions.
