# Independent audit of defect-coefficient rank and defect-two sparsity

## 1. Verdict and scope

This note reconstructs independently the claims in
[the defect-coefficient note](defect-coefficient-rank-and-two-defect-sparsity.md).
The reconstruction confirms all five substantive points:

1. gauge rigidity makes every two-site complement matching-active and
   makes the vertex-gauge map faithful;
2. every off-diagonal product has a unique expansion in the defect
   directions, with the stated direct-entry balance;
3. an all-six-dense defect-two chart is excluded by the already completed
   abstract product geometry and cap theorem, without importing a hidden
   connectedness hypothesis on the rank-three graph;
4. an all-six-dense defect-three chart has coefficient span exactly three,
   and every named row and column pair is independent;
5. the five-site common-restriction model and its overlapping-order-eight
   residual are exact, including the coefficient `-6`.

There is one scope guard worth making explicit.  The five-site construction
is an odd common-complement, selected-row relaxation.  It is not by itself
an even pair chart, a good pair, a gauge-rigid Hessian chart, an exact
aggregate source, or a Krenn counterexample.  Its valid conclusion is that
the defect expansions and direct-entry balances alone do not imply
compatibility of two overlapping charts.

Throughout the genuine pair-chart argument, write `|W|=2t`.  In the active
application `|W|>=6`; the graph argument below only needs `|W|>=4`.

## 2. Pair-complement activity and faithfulness of the gauge map

Let

\[
 \mathcal H_q:\mathcal R_{W,2}\longrightarrow\mathcal R_{W,2t},
 \qquad Z\longmapsto Zq^{[t-1]},                       \tag{1}
\]

and assume that its kernel is exactly the gauge image

\[
 \{Z^\alpha:\textstyle\sum_i\alpha_i=0\},\qquad
 (Z^\alpha)_{ij}=(\alpha_i+\alpha_j)q_{ij}.            \tag{2}
\]

Fix distinct sites `i,j`.  If

\[
                 q_{W\setminus\{i,j\}}^{[t-1]}=0,      \tag{3}
\]

then every tensor in the nine-dimensional block
\(V_i\otimes V_j\) is killed by (1).  Indeed, after multiplication by a
tensor already occupying sites `i,j`, every term of `q^[t-1]` which also
uses either site vanishes in the site-square-zero algebra, and the only
remaining contribution is (3).  On the other hand, a gauge tensor
supported only on the block `ij` has that block in the line
\(\mathbb Cq_{ij}\), or is zero when `q_ij=0`.  Thus the gauge image meets this
nine-space in dimension at most one.  Gauge rigidity rules out (3), so

\[
             q_{W\setminus\{i,j\}}^{[t-1]}\ne0
             \qquad\text{for every }i\ne j.            \tag{4}
\]

Let `G_+(q)` have an edge precisely where `q_ij` is a nonzero block,
regardless of its rank.  A nonzero tensor in (4) contains at least one
supported perfect matching, so `G_+(q)-{i,j}` has a perfect matching for
every pair `i,j`.

This forces `G_+(q)` to be connected.  If it were disconnected, choose
two vertices in one nontrivial component.  A perfect matching after their
deletion forces that component and every untouched component to have even
order.  Deleting one vertex from each of two components would then leave
two odd components, which cannot be perfectly matched.  An isolated
component is already incompatible with the first deletion, and the
all-isolated graph is immediate.

It also forces `G_+(q)` to be nonbipartite.  If its shores were `L,R`, a
perfect matching after deleting one vertex from each shore would force
`|L|=|R|`.  Since `|W|>=4`, one shore contains two vertices; deleting two
vertices in that shore would instead require shore sizes differing by two.
The two requirements are inconsistent.

Finally, if `Z^alpha=0`, then

\[
                         \alpha_i+\alpha_j=0             \tag{5}
\]

on every edge of `G_+(q)`.  Alternation around an odd cycle gives zero on
that cycle, and connectedness propagates zero to every site.  Hence

\[
                         \alpha\longmapsto Z^\alpha
                         \quad\text{is injective}.       \tag{6}
\]

This derivation uses no positivity and does not infer a nonzero matching
term from a vanishing sum: it uses the nonzero tensor (4), which necessarily
has at least one supported term.

## 3. Reconstruction of the unique defect expansion

For an oriented deleted pair `p,q`, the exact pair equations are

\[
 a_{cd}q^{[t]}+p_cs_dq^{[t-1]}=\delta_{cd}X_c^W.       \tag{7}
\]

Fix `c!=d`.  Since

\[
                         q q^{[t-1]}=tq^{[t]},          \tag{8}
\]

gauge rigidity gives a unique `alpha` with zero coordinate sum such that

\[
              p_cs_d+{a_{cd}\over t}q=Z^\alpha.       \tag{9}
\]

On a rank-three edge `ij`, (9) reads

\[
 (p_cs_d)_{ij}
   =\left(\alpha_i+\alpha_j-{a_{cd}\over t}\right)q_{ij}. \tag{10}
\]

The left side is a sum of two simple endpoint-ordered tensors and has
matrix rank at most two.  Since `q_ij` has rank three, its scalar in
(10) vanishes:

\[
                         \alpha_i+\alpha_j={a_{cd}\over t}.         \tag{11}
\]

Subtract the constant solution and put

\[
                  \gamma=\alpha-{a_{cd}\over2t}{\bf1}.             \tag{12}
\]

The vector `gamma` alternates on every rank-three edge.  On a nonbipartite
component it is zero; on a nontrivial bipartite component it is a multiple
of the shore-sign vector; and on an isolated site it is arbitrary.  Thus,
for the standard defect basis,

\[
 \alpha={a_{cd}\over2t}{\bf1}
             +\sum_{k=1}^{\nu}\beta_{cd,k}\zeta^{(k)}.             \tag{13}
\]

Writing `Delta_k=sum_i zeta_i^(k)`, the condition `sum_i alpha_i=0`
becomes

\[
                         a_{cd}+\sum_k\beta_{cd,k}\Delta_k=0.       \tag{14}
\]

Also

\[
                  Z^{(a_{cd}/(2t)){\bf1}}={a_{cd}\over t}q,        \tag{15}
\]

so (9) gives

\[
                         p_cs_d=\sum_k\beta_{cd,k}Z^{\zeta^{(k)}}.  \tag{16}
\]

The defect vectors in (13) are linearly independent because they have
disjoint component supports, and (6) makes their physical gauge tensors
linearly independent.  Therefore `beta_cd` is unique after choosing the
sign of each shore vector.  Reversing one shore convention reverses the
corresponding coefficient and imbalance, leaving (14)--(16) unchanged.
Equations (8)--(15) also confirm that no factor of `t`, `2`, or a divided
power factorial is missing.

## 4. Dense rows, coefficient rank, and the defect-two contradiction

In the site-square-zero algebra, multiplication by a linear element which
reaches at least three sites is injective on linear elements.  To see this
directly, suppose `p s=0` and choose three sites `i,j,k` on which `p` is
nonzero.  On two support sites the block equation is

\[
                         p_i\otimes s_j+s_i\otimes p_j=0.
\]

It either kills both corresponding components of `s`, or makes
`s_i=lambda_i p_i`, `s_j=lambda_j p_j` with
`lambda_i+lambda_j=0`.  Applying this to the triangle `ij,jk,ik` forces
all three scalars to vanish in characteristic zero.  Pairing any remaining
support site with these sites kills its component, while pairing a site
outside the support of `p` with one support site kills that component as
well.  Thus `s=0`.

Now fix a dense row `p_c`.  If its two off-diagonal coefficient vectors were dependent,
then for distinct `d,e!=c` there would be a nonzero pair `(mu,nu)` with

\[
 0=\mu p_cs_d+\nu p_cs_e=p_c(\mu s_d+\nu s_e).          \tag{17}
\]

Injectivity would give `mu s_d+nu s_e=0`, contrary to independence of the
good star `(s_0,s_1,s_2)`.  Hence the two coefficient vectors in every
dense named row are independent.  Interchanging the two stars proves the
same statement for every dense named column.

Suppose now that `nu=2` and all six star rows are dense.  The six products
in (16) span exactly a two-space `E`, and every named row pair and column
pair is a basis of `E`.  Equivalently, the map from the six-dimensional
zero-diagonal matrix space to `E` has a four-dimensional kernel which
meets no coordinate row plane or coordinate column plane.

These are the abstract starting hypotheses of
[the corank-two product geometry](all-dead-corank-two-product-geometry.md)
and
[the aligned boundary closure](aligned-two-plane-boundary-closure.md).
The connected, spanning, nonbipartite rank-three graph used in Section 2
of
[the product-reduction note](all-dead-corank-two-product-reduction.md)
was one way to *derive* these product relations in the original E1 branch.
It is not used by the subsequent product geometry.  Here (16) supplies the
relations directly, so that provenance is bypassed rather than assumed.

For completeness, the cap side can also be checked directly.  Put

\[
 V=\operatorname{span}\{p_cs_d:0\le c,d\le2\},
 \qquad Q=q^{[t]}.                                      \tag{18}
\]

The six off-diagonal equations give
\(\mathcal H_q(E)\subseteq\mathbb CQ\).  Modulo \(\mathbb CQ\),
the three diagonal equations make the classes of the three independent
targets `X_0,X_1,X_2` lie in the image of `V/E`.  Their quotient span has
dimension three when `Q=0` or `Q` is outside their span, and dimension two
when `0!=Q` belongs to their span.  Consequently

\[
 \dim V\ge5\quad\text{in the first cases},\qquad
 \dim V\ge4\quad\text{in the second}.                  \tag{19}
\]

The completed abstract product geometry and its zero-boundary analysis
say that the dense two-plane configuration is impossible or has
`dim V<=3`.  This contradicts (19) for every value and target position of
`Q`.  Thus an actual defect-two chart has a star row supported on at most
two sites.

The same reasoning audits the defect-three claim.  When all six rows are
dense, every named row and column pair of coefficient vectors is
independent, so their total span has dimension at least two.  If it had
dimension two, the preceding abstract contradiction would apply verbatim.
It must therefore have dimension at least three.  For `nu=3` it has
dimension exactly three.  This is a coefficient-rank statement, not a
closure of the dense defect-three branch.

## 5. Exact five-site common-restriction model

Let `K={1,2,3,4,5}`, take `V_i=C^3`, and write `x_i=e_0` in the copy at
site `i`.  Define the endpoint-ordered blocks

\[
 q_{12}=q_{34}=I_3,
 \qquad q_{ij}=x_i\otimes x_j
       \quad\text{for all other }i<j.                  \tag{20}
\]

Thus the rank-three graph consists of the two edges `12`, `34` and the
isolated site `5`.  Its defect vectors and imbalances are

\[
\begin{aligned}
 \zeta^{(1)}&=(1,-1,0,0,0),&\Delta_1&=0,\\
 \zeta^{(2)}&=(0,0,1,-1,0),&\Delta_2&=0,\\
 \zeta^{(3)}&=(0,0,0,0,1),&\Delta_3&=1.
\end{aligned}                                           \tag{21}
\]

Put

\[
 P=\sum_i x_i,
 \qquad
 L(b)_i=\lambda_i x_i,
 \qquad
 (\lambda_1,\ldots,\lambda_5)
       =(b_1,-b_1,b_2,-b_2,b_3).                       \tag{22}
\]

On an ordinary pair `ij` other than `12,34`, both sides of

\[
                         P L(b)=\sum_{k=1}^3b_kZ_q^{\zeta^{(k)}}    \tag{23}
\]

have block \((\lambda_i+\lambda_j)x_i\otimes x_j\).  On `12`, the left
block is zero because `lambda_1+lambda_2=0`, while every defect-vector
sum on the right is zero; hence the full-rank block `q_12=I_3` is also
multiplied by zero.  The same check applies on `34`.  This proves (23)
on every block, with both endpoint terms in the product retained.

The imbalance calculation gives the direct scalar

\[
                         a+\sum_kb_k\Delta_k=0
                         \quad\Longleftrightarrow\quad a=-b_3.     \tag{24}
\]

Thus (20)--(24) exactly realize the displayed defect-coordinate and
direct-balance identities on the common restriction.

## 6. The order-eight overlap residual

Add three boundary sites `r,u,v` and choose **pairwise distinct** boundary
colors

\[
                         (c,d,e)=(0,1,2),               \tag{25}
\]

or any relabelling.  Pairwise distinctness is the clean hypothesis here:
it makes each selected boundary pair off-diagonal, so all three selected
cells are in the regime audited by (14)--(16), and it makes the triple
target zero.

Use the common restrictions

\[
                         p_c=P,qquad s_d=S=L(e_3)=x_5,qquad
                         t_e=T=L(e_3)=x_5,              \tag{26}
\]

Here `e_3` denotes the third standard vector in the defect-coordinate
space of (21), not a fourth physical color.  Use the selected direct
entries

\[
 A_{r\mid u}(c,d)=-1,qquad
 A_{r\mid v}(c,e)=-1,qquad
 A_{u\mid v}(d,e)=0.                                  \tag{27}
\]

For `|B|=8`, the endpoint-ordered common-complement equation in this row
is

\[
 \bigl(A_{r\mid u}(c,d)t_e+A_{r\mid v}(c,e)s_d
          +A_{u\mid v}(d,e)p_c\bigr)q^{[2]}
       +p_cs_dt_eq
       =\delta_{c=d=e}X_c^K.                           \tag{28}
\]

Because a site may occur only once, `S T=x_5^2=0`.  The left side of
(28) is therefore

\[
                         -2x_5q^{[2]}.                  \tag{29}
\]

The coefficient of the all-`e_0` tensor on sites `1,2,3,4` in `q^[2]`
is the sum of the three perfect matchings

\[
                         12|34,qquad13|24,qquad14|23. \tag{30}
\]

Each contributes one: the first uses the `(0,0)` entries of the two
identity blocks, and the other two use rank-one
\(e_0\otimes e_0\) blocks.
The divided power `q^[2]=q^2/2!` counts each unordered matching once, so
the coefficient is exactly three, not six.  After (29), the all-`e_0`
coefficient on all five common sites is

\[
                              -2\cdot3=-6.              \tag{31}
\]

The right side of (28) is zero by (25).  Hence this selected-row common
restriction cannot extend through the full overlap equation.  Endpoint
orientation causes no sign or transpose change in the selected scalars;
the two exceptional internal blocks are identities and are transpose
invariant as well.

## 7. What is and is not certified

The genuine even-chart conclusions are the unique formula (14)--(16),
the existence of a sparse row at defect two, and full coefficient rank for
an all-six-dense defect-three chart.  They allow arbitrary complex blocks,
endpoint asymmetry, zero entries, and cancellation.

The five-site model certifies a limitation of those conclusions.  Its
common set has odd cardinality; only selected rows and direct cells are
specified; independent three-row stars, the full aggregate blocks, gauge
rigidity of an even pair chart, and the remaining overlap rows are not
asserted.  The nonzero residual (31) shows precisely why those omitted
equations matter.  It must not be promoted to a chart-level or source-level
counterexample.

As a mechanical cross-check, the companion dependency-free verifier
[checks the model blockwise](../computations/verify_defect_coefficient_rank_and_two_defect_sparsity.py).
The uniform conclusions above are supplied by the hand argument and the
previously completed abstract product theorem, not by that finite check.
