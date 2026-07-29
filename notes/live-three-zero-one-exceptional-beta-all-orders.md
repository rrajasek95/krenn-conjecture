# One exceptional live beta still leaves an injective three-zero star

## 1. Outcome

Continue from
[live-three-zero-common-beta-all-orders.md](live-three-zero-common-beta-all-orders.md).
The cyclic port orbit synchronizes the four centres at beta
\(\mu\ne0\) and the three zero sites at beta \(-\mu\). Let the residual
contain an arbitrary odd live shore

\[
                         |U|=2r-1\ge3,                              \tag{1}
\]

the two type-\(10\) centres, and the shared zero site \(z_0\), with no
additional nonzero singular sites. Suppose exactly one live site \(y\)
has beta value \(\nu\ne\mu\), while every other live site has beta
\(\mu\).

Then the vanishing cyclic response

\[
                              {\cal D}_0(x,z)=0                     \tag{2}
\]

again forces every residual block \(q_{i z_0}\) to vanish. The exceptional
site already has \(q_{y z_0}=0\) from

\[
                         (\nu-\mu)q_{y z_0}=0.                     \tag{3}
\]

The proof below kills all blocks at the common-beta sites. Consequently
\(z_0\) has no rank-three neighbour, contradicting the global
connected-spanning hypothesis on \(G_3(q)\).

Combining this result with the common-beta theorem, any cyclic \(s=3\)
escape for the two-coordinate-factor pattern must therefore contain at
least two different-beta live sites or an additional nonzero singular
site.

The same binary mechanism in fact handles every minority of exceptional
live beta values; see
[live-three-zero-minority-exceptional-beta.md](live-three-zero-minority-exceptional-beta.md).

## 2. Two binary edge weights

Normalize the common-beta live sites to \(P_i=I\), the two type-\(10\)
centres to \(P_i=D=\operatorname {diag}(1,1,0)\), and the exceptional live
site to \(P_y=I\). There are

\[
             2r\text{ common-beta residual sites},\qquad
             1\text{ exceptional site }y.                          \tag{4}
\]

Every possible zero-star block lies at one of the \(2r\) common-beta
sites. Fixing a coordinate \(b\) at \(z_0\), write its entries as
\(Z_{i,a}=q_{i z_0}[a,b]\).

On the binary local colours \(0,1\), internal \(q\)-edges have just two
nonzero values:

\[
 \kappa={h_{01}\over2\mu}
       \quad\text{between two common-beta sites},\qquad
 \lambda={h_{01}\over\mu+\nu}
       \quad\text{on an edge incident with }y.                     \tag{5}
\]

Both are nonzero. The first because
\(\mu h_{01}\ne0\), and the second because the structural left side on a
live--nonzero pair has nonzero rank, forcing \(\mu+\nu\ne0\).

A balanced binary cofactor on \(2t\) common-beta sites has value
\(t!\kappa^t\). If it contains \(y\), then \(y\) has \(t\) possible
opposite-colour partners, followed by a bijection on the remaining
sites, so its value is

\[
                         t!\lambda\kappa^{t-1}.                    \tag{6}
\]

No Cauchy-permanent cancellation remains in this one-exceptional-site
stratum: every matching contains exactly one edge at \(y\), and all such
edges have the same scalar \(\lambda\).

## 3. Weighted subset sums kill the binary star rows

Let \(T\) be an arbitrary \((r-1)\)-subset of the \(2r\) common-beta
sites. Give \(y\) colour \(0\), give the sites of \(T\) colour \(0\), and
give every other common-beta site colour \(1\). Use the diagonal source
coefficient \(x_1z_1\).

The two marked factors occupy colour-\(1\) sites. If the star uses a site
\(i\in T\), the remaining \(2r-2\) sites are balanced and include \(y\).
If it uses any other common-beta site, the remaining binary counts are
unbalanced. Using (6), the exact coefficient equation is

\[
 A_r\sum_{i\in T}Z_{i,0}=0,\qquad
 A_r=2\binom{r+1}{2}(r-1)!\lambda\kappa^{r-2}\ne0.       \tag{7}
\]

This holds for every \((r-1)\)-subset \(T\). Since
\(1\le r-1\le2r-1\), comparing two subsets which differ by one site and
then using one subset sum proves

\[
                              Z_{i,0}=0                              \tag{8}
\]

at every common-beta site.

Interchange colours \(0,1\): give \(y\) colour \(1\), give an arbitrary
\((r-1)\)-subset \(T\) colour \(1\), give the other common-beta sites
colour \(0\), and use \(x_0z_0\). The identical calculation gives

\[
                         A_r\sum_{i\in T}Z_{i,1}=0,
 \qquad                    Z_{i,1}=0.                              \tag{9}
\]

## 4. One ternary letter kills the final star row

Fix a common-beta site \(i\) and give it local colour \(2\). Give \(y\)
colour \(1\). Among the other \(2r-1\) common-beta sites use \(r+1\)
zeros and \(r-2\) ones, and take the source coefficient \(x_0z_0\).

When the star uses \(i\), the two marked zeros leave a balanced binary
cofactor containing \(y\), so \(Z_{i,2}\) has the same nonzero coefficient
\(A_r\) as in (7). Every term in which the star uses another site contains
a variable from (8)--(9). Hence the complete equation is

\[
                              A_rZ_{i,2}=0.                         \tag{10}
\]

Thus every row of every common-beta zero-star block vanishes. Repeating
for \(b=0,1,2\), and adjoining the already-zero exceptional block (3),
proves

\[
                  q_{i z_0}=0
                  \quad\text{for every residual nonzero site }i.   \tag{11}
\]

The zero--zero blocks at \(z_0\) vanish because all three zero betas equal
\(-\mu\), and its two blocks to the removed type-\(22\) centres are
singular coordinate ports. There are no other sites. Thus (11) leaves no
rank-three edge at \(z_0\), giving the required contradiction.

## 5. Exact audit

[verify_live_three_zero_one_exceptional_beta_all_orders.py](../computations/verify_live_three_zero_one_exceptional_beta_all_orders.py)
checks the fixed-size subset incidence rank and reconstructs the matching
coefficients (7)--(10) over
\(\mathbb Q(\kappa,\lambda)\) for \(r=2,\ldots,8\).

As a full ternary audit rather than only a binary count, it also constructs
the first nonminimal case \(r=3\): five live sites, two type-\(10\)
centres, and one zero site. Four live sites have beta \(\mu\), while the
fifth has beta \(\nu\). The map from the six arbitrary common-beta star
blocks has an explicit \(18\times18\) minor with determinant

\[
 -{2^{33}3^{18}h_{01}^{32}h_{02}h_{12}^{3}
       \over \mu^{18}(\mu+\nu)^{18}},                              \tag{12}
\]

which is nonzero throughout the admissible stratum.
