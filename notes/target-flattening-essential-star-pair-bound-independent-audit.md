# Independent audit: target flattening and essential pair stars

## 1. Verdict and exact scope

The theorem in
[target-flattening-essential-star-pair-bound.md](target-flattening-essential-star-pair-bound.md)
is sound.  Fix a three-colour coordinate projection of a monochromatic
decorated source system.  For every endpoint $u$, deletion of at most
three neighbors can make the resulting **aggregate projected** star
noninjective.  It follows that at least

\[
                 \binom N2-3N=\frac{N(N-7)}2
\]

physical pairs have injective projected stars at both endpoints, and some
endpoint lies in a fan of at least $N-7$ such pairs.  The bad-pair graph
is 4-degenerate, so the good-pair graph contains a clique of size at least
$\lceil N/5\rceil$.

The qualifications are substantive.  The conclusion concerns sums of all
parallel sources on a physical pair, not individual sources or individual
colour rows.  When the original palette has more than three colours, it
concerns one fixed ternary projection at a time.  The good pair supplied for
one chosen triple need not work for every other triple, and injectivity of a
ternary projected star does not assert full rank equal to the size of the
original palette.

## 2. Source aggregation, endpoint order, and projection

For $u<v$, aggregate every parallel decorated source on $\{u,v\}$ as

\[
 A_{uv}=\sum_{a:N(a)=\{u,v\}}w(a)
     e_{k(a,u)}^{(u)}\otimes e_{k(a,v)}^{(v)}.
\]

The block oriented from $v$ to $u$ is the transposed tensor.  Expanding
one product of aggregate blocks chooses one source on each pair of a
perfect matching, so distributivity proves source-level and block-level
matching tensors identical.  This remains true with repeated endpoint
colour pairs, exact cancellation between parallel sources, and zero
weights; no source is selected from a zero aggregate coefficient.

Let $P$ be coordinate projection onto any fixed three palette colours.
The perfect-matching polynomial is functorial:

\[
 H_B\bigl((P_u\otimes P_v)A_{uv}\bigr)
        =\left(\bigotimes_{u\in B}P_u\right)H_B(A).       \tag{1}
\]

Thus a palette target projects to exactly $\Delta_{B,3}$, including when
a selected colour occurs only on a zero-weight or otherwise inactive
source: monochromaticity still requires that colour's constant coefficient
to be one.  This discharges the larger-palette and zero-source edge cases
without deleting a palette colour.

## 3. The flattening argument

At a fixed endpoint $u$, orient every block with the $u$-slot first and
write

\[
 L_{u\leftarrow x}=\operatorname{im}
       (V_x^*\longrightarrow V_u),\qquad
 T_u=\sum_{x\ne u}L_{u\leftarrow x}.
\]

Partitioning perfect matchings by the unique neighbor paired with $u$
gives the coefficientwise identity

\[
 H_B(A)=\sum_{x\ne u}A_{ux}\otimes
                 H_{B\setminus\{u,x\}}(A),              \tag{2}
\]

with slots put back in physical order.  Consequently the left image of the
mode-$u$ flattening is contained in $T_u$.  On the target, that
flattening is

\[
 \sum_{i=0}^2 e_i^{(u)}\otimes e_i^{\otimes(B\setminus\{u\})}.
\]

The three right factors are independent, so its left image is all of
$V_u\cong\mathbb C^3$.  Hence $T_u=V_u$.  This inference is made after
the complete tensor identity and never promotes a vanishing sum to
termwise vanishing.

## 4. Essential subspaces and star kernels

Here is an independent proof of the linear lemma.  If subspaces $L_x$
span a $d$-space and deleting $L_x$ destroys spanning, choose
$\phi_x$ that annihilates all $L_y$ with $y\ne x$ but not $L_x$.
Choose $z_x\in L_x$ with $\phi_x(z_x)\ne0$.  The matrix
$(\phi_y(z_x))_{x,y}$ is diagonal with nonzero diagonal, so all such
$\phi_x$ are independent.  There are at most $d$ essential indices.

If there are exactly $d$, these covectors form a dual basis.  A
nonessential $L_y$ is annihilated by every one and is zero.  Each
essential $L_x$ is killed by the other $d-1$ covectors and is nonzero,
so it is the corresponding coordinate line.  In particular, the equality
case consists of $d$ independent lines plus any number of zero spaces.

For deletion of $v$, the star map at $u$ is the direct sum of the
contraction maps of $A_{ux}$ over $x\notin\{u,v\}$.  Therefore

\[
 \ker\sigma_u^{(v)}
 =\bigcap_{x\notin\{u,v\}}\operatorname{Ann}L_{u\leftarrow x}
 =\operatorname{Ann}\!\left(
       \sum_{x\notin\{u,v\}}L_{u\leftarrow x}\right).    \tag{3}
\]

The star is injective precisely when the sum in (3) is $V_u$.  Since all
neighbor supports together span $V_u$, deletion is deficient precisely
for an essential neighbor.  Dimension three gives the claimed budget of
three, including literal zero blocks.

## 5. Pair, fan, and good-clique arithmetic

Let $D_u$ be the set of globally deficient deleted neighbors at endpoint
$u$; then $|D_u|\le3$.  An unordered pair is bad only if one of its two
orientations belongs to the corresponding $D_u$.  Assign each bad pair
to one deficient endpoint.  This injection into directed deficiencies
gives at most $3N$ bad pairs and hence at least $N(N-7)/2$ good pairs.
Their average good degree is at least $N-7$, proving the fan bound.

There is a sharper hereditary consequence, and it is important here not to
recompute essentiality in a restricted support family.  If $u$ has three
globally essential neighbors, the equality case in Section 4 makes every
other $A_{uv}$ zero.  The reversed block is the same zero tensor, so $u$
cannot be essential at such a $v$, either.  Hence the entire bad degree of
$u$ is at most three.

Suppose an induced bad graph on $C$ had minimum degree at least five.  It
could contain no endpoint with three global essential neighbors.  Thus every
endpoint in $C$ witnesses at most two bad edges.  Assign every bad edge to
one endpoint witnessing its deficiency.  Then

\[
             |E_{\rm bad}(C)|\le2|C|,
   \qquad 2|E_{\rm bad}(C)|\ge5|C|,                       \tag{4}
\]

a contradiction.  The bad graph is therefore 4-degenerate and
5-colourable.  A largest colour class is independent in the bad graph,
hence a clique in the good graph, of size at least
$\lceil N/5\rceil$.  The first even $N$ for which this lower bound is six
is $N=26$.

The numerical pair/fan thresholds are

| $N$ | good pairs | forced fan degree |
|---:|---:|---:|
| 8 | 4 | 1 |
| 10 | 15 | 3 |
| 12 | 30 | 5 |
| 14 | 49 | 7 |

The crude local three-defect ledger is arithmetically sharp if the equality
structure is deliberately omitted: orient the cyclic differences
$+1,+2,+3$ as deficient at every endpoint.  For $N\ge8$, these are
$3N$ distinct unordered bad pairs and every vertex has good degree
$N-7$.  This ledger violates the three-essential support conclusion (its
bad degrees are six), so it is not realizable by a tensor satisfying all the
hypotheses.  It audits only the arithmetic of the earlier $3N$ union
bound, not sharpness of the complete theorem.

## 6. Equality case and the cubic-vertex upgrade

Suppose $u$ has three essential neighbors.  Section 4 shows that their
mode-$u$ supports are independent lines and every other incident aggregate
block is zero.  Each surviving matrix is nonzero of rank one.  Thus, after
discarding only zero **aggregate** pairs, $u$ is a cubic vertex.  Parallel
sources inside a surviving block have not been separated.

For completeness, the cubic upgrade can be reconstructed as follows at the
orders $N\ge8$ used here.  Name the three neighbors $j_0,j_1,j_2$.
For a covector $\lambda\in V_u^*$ whose three coordinates are nonzero,
contract the star expansion at $u$ by $\lambda$, and contract all sites
other than $u,j_0,j_1,j_2$ by

\[
 K_\lambda=\sum_{i=0}^2\lambda_i^{-1}
                 (e_i^*)^{\otimes(N-4)}.
\]

The target becomes the three-site diagonal tensor.  The right side is one
slice centered at each $j_s$, whose center is

\[
                  L_s(\lambda)=(\lambda\otimes\mathrm{id})A_{u j_s}.
\]

The three-slice center lemma says these centers are nonzero multiples of
three distinct coordinate vectors.  A short proof of that lemma is useful
for auditing degeneracies.  For a decomposition

\[
 \Delta_{3,3}=x\otimes P+y\otimes Q+z\otimes R,
\]

let $U_x\subseteq\mathbb C^3$ be the evaluation vectors on the three
diagonal basis vectors of covectors annihilating $x$, and similarly for
$y,z$.  Each has dimension at least two.  Triple contraction gives
$\sum_i a_i b_i c_i=0$ for every
$a\in U_x,b\in U_y,c\in U_z$, so
$\operatorname{span}(U_x\odot U_y)$ has dimension at most one.  Two
subspaces of $\mathbb C^3$ of dimension at least two can have such a
product span only when they are two distinct coordinate hyperplanes: a
vector with all coordinates nonzero would make coordinatewise
multiplication invertible, while a vector space contained in the union of
the three coordinate hyperplanes lies in one of them.  The third space is
the remaining coordinate hyperplane.  Their annihilators make $x,y,z$
three distinct coordinate centers.

Apply this for every $\lambda$ in the Zariski-dense torus.  Pairwise
products of distinct output coordinates of each linear map $L_s$ vanish
on that torus, hence identically.  Since a polynomial ring is a domain,
the image of $L_s$ lies in one fixed coordinate line.  Thus
$A_{u j_s}=a_s\otimes e_{t_s}$.  The center never vanishes on the torus.
A linear form involving at least two coordinates has a zero there (choose
two nonzero coordinates to cancel, avoiding at most one value when a third
term is present), so $a_s$ is itself a nonzero coordinate vector.  The
three $u$-colours are distinct.  Finally, slicing the full target at $u$
leaves one nonzero term and forces $t_s$ to equal its $u$-colour.

This proof allows arbitrary complex cancellation before contraction.  A
zero one of the three surviving blocks would leave only two slices and
contradict the slice rank three of the diagonal tensor.

## 7. Independent exact checker

Frozen audited artifacts:

```text
94fc773a552589c4321cc9aa71c9bb4ec6bbf8759ca93bb25432e420507aca64  notes/target-flattening-essential-star-pair-bound.md
56598490ae2868b35c1e73da7d543c61b4c071effc9798e83705cb255a298ad0  computations/verify_target_flattening_essential_star_pair_bound.py
f6dbeebd0ec6a19a47c8cf7aaaab7aa74dfbfc590f5e1a4cdde331b625a8f5a6  computations/audit_target_flattening_essential_star_pair_bound_independent.py
```

The clean-room checker
[audit_target_flattening_essential_star_pair_bound_independent.py](../computations/audit_target_flattening_essential_star_pair_bound_independent.py)
uses different finite certificates from the primary script.  It

* compares source-level and aggregate-block matching tensors for exact
  rational parallel sources with endpoint-asymmetric colours, zero weights,
  cancelling duplicates, a five-colour palette, and a reordered ternary
  projection;
* verifies the endpoint recursion and flattening containment at both block
  orientations coefficient by coefficient;
* enumerates 231,987 spanning multisets of subspaces of
  $\mathbb F_3^3$ through five neighbors, finding 702 equality families
  and checking the independent-lines-plus-zeros classification;
* checks the star-rank/support-rank identity on exact rational eight-site
  aggregate families;
* exhausts all $13^3$ projective center triples over $\mathbb F_3$ and
  finds exactly the six permutations of the three coordinate axes that can
  support a three-slice decomposition of the diagonal tensor; and
* checks the cyclic directed-defect arithmetic, all induced subsets at
  $N=8,10$, the four displayed pair/fan thresholds, the min-degree-five
  contradiction, and the $N=26$ six-site threshold.

The finite-field checks are adversarial certificates for the displayed
identities; the characteristic-zero conclusions come from the proofs above.

## 8. Remaining gate

This theorem is a strong incidence input, not a proof of Krenn's
conjecture.  It does not force a rank-three individual pair block, a clean
cap, connected internal rank-three graphs, or simultaneous goodness across
all colour triples.  Even the six-site good clique at $N\ge26$ supplies
only mutually injective aggregate projected stars.  A continuation must
still use the mixed target equations to eliminate the disconnected and
extra-kernel Hessian escapes or to force a source-specific cap
factorization.
