# Common beta makes the cyclic three-zero obstruction uniform in the live size

## 1. Outcome

Retain the cyclic three-zero configuration and beta synchronization from
[live-three-zero-common-power-star-injectivity.md](live-three-zero-common-power-star-injectivity.md).
The two removed type-\(22\) centres and the two residual type-\(10\)
centres have beta value \(\mu\ne0\), while all three zero sites have beta
value \(-\mu\). Suppose there are no further nonzero singular sites, but
allow an arbitrary odd number

\[
                         |U|=2r-1\ge3                              \tag{1}
\]

of live sites. If every live site also has beta value \(\mu\), then the
vanishing mixed-port response

\[
                              {\cal D}_0(x,z)=0                     \tag{2}
\]

forces every block from the shared port site \(z_0\) to the residual
nonzero shore to vanish. As in the minimal proof, \(z_0\) then has no
incident rank-three edge, contradicting connectedness and spanning of
\(G_3(q)\).

Thus the cyclic three-zero boundary for the two-coordinate-factor
rank-two direct quadratic is excluded for **every** live-shore size on
the common-beta stratum. The remaining \(s=3\) escape must contain a live
site with beta different from \(\mu\), or an additional nonzero singular
site. This is a genuine restriction: such a different-beta live site has
zero block to \(z_0\) by the structural relation, but it still participates
in the internal common-power cofactors.

The case of exactly one such different-beta live site is also excluded,
uniformly in the live size, in
[live-three-zero-one-exceptional-beta-all-orders.md](live-three-zero-one-exceptional-beta-all-orders.md).

## 2. Normalized residual

After independent local changes of basis, the residual nonzero sites are

\[
 \underbrace{0,\ldots,2r-2}_{2r-1\ {\rm live}},\quad
 \underbrace{2r-1,2r}_{\text{two type-}10\text{ centres}},
                                                                    \tag{3}
\]

with

\[
 P_i=I\quad(i<2r-1),\qquad
 P_{2r-1}=P_{2r}=D:=\operatorname {diag}(1,1,0).                   \tag{4}
\]

There are \(m=2r+1\) nonzero residual sites and the one zero site \(z_0\).
Because every nonzero residual beta equals \(\mu\),

\[
 q_{ij}={1\over2\mu}P_iHP_j^{\mathsf T}.                          \tag{5}
\]

Put

\[
                         \kappa={h_{01}\over2\mu}\ne0.             \tag{6}
\]

On words using only local colours \(0,1\), all sites in (3) behave
identically: a \(q\)-edge has value \(\kappa\) when its endpoint colours
are opposite and value zero when they agree. A balanced binary word on
\(2t\) sites therefore has hafnian coefficient

\[
                              t!\,\kappa^t,                         \tag{7}
\]

because its perfect matchings are precisely the \(t!\) bijections between
the zero sites and the one sites.

Fix one coordinate \(b\) at \(z_0\), and denote

\[
                         Z_{i,a}=q_{i z_0}[a,b].                    \tag{8}
\]

The argument below proves that all \(3m\) values in (8) vanish. Repeating
it for the three choices of \(b\) kills every residual star block.

## 3. Binary subset sums kill the first two rows of every block

Take a binary word whose zero set \(S\) has size \(r+2\), and use the
diagonal source coefficient \(x_0z_0\). In a nonzero matching term, the
two marked factors occupy zero sites. If the star at \(z_0\) uses site
\(i\), balance of the remaining binary cofactor is possible exactly when
\(i\in S\). For each such \(i\), there are
\(\binom{r+1}{2}\) choices of the marked pair and the remaining
\(2r-2\) sites contribute (7) with \(t=r-1\). The coefficient equation is
therefore

\[
 A_r\sum_{i\in S}Z_{i,0}=0
 \quad\text{for every }|S|=r+2,\qquad
 A_r=2\binom{r+1}{2}(r-1)!\kappa^{r-1}\ne0.             \tag{9}
\]

Any two sites occur as the symmetric difference of two
\((r+2)\)-subsets: keep \(r+1\) common sites and exchange the last one.
Subtracting the corresponding equations in (9) shows that all \(Z_{i,0}\)
are equal. One equation in (9), together with characteristic zero, then
makes their common value zero. The inequalities needed here are
\(1\le r+2\le m-1\), which hold because \(r\ge2\).

Next take a binary word whose one set \(T\) has size \(r\), again using
the source coefficient \(x_0z_0\). The same balance calculation gives

\[
                         A_r\sum_{i\in T}Z_{i,1}=0
                         \qquad(|T|=r).                            \tag{10}
\]

Fixed-size subset sums with \(1\le r\le m-1\) again separate all sites,
so

\[
                         Z_{i,0}=Z_{i,1}=0
                         \qquad(0\le i<m).                         \tag{11}
\]

## 4. One ternary letter kills the last row

Fix a site \(i\). Give it local colour \(2\); among the other \(2r\)
sites use \(r+1\) zeros and \(r-1\) ones. Use the diagonal source
coefficient \(x_0z_0\). If the zero-star edge uses \(i\), the two marked
zeros leave a balanced binary cofactor and the coefficient of \(Z_{i,2}\)
is exactly the nonzero scalar \(A_r\) from (9).

If the zero-star edge instead uses another site, its local colour is
\(0\) or \(1\), so its contribution contains one of the already vanishing
variables in (11). The complete coefficient equation consequently reduces
to

\[
                              A_r Z_{i,2}=0.                         \tag{12}
\]

This holds for every site \(i\), proving that all variables in (8) vanish.
Notice that the argument retains arbitrary \(h_{02},h_{12}\): those
entries can occur in the discarded terms of (12), but their star
coefficients have already vanished.

## 5. Global contradiction and exact audit

The cyclic port pattern itself gives
\(\beta_{z_0}=\beta_{z_1}=\beta_{z_2}=-\mu\), so

\[
                         q_{z_0z_1}=q_{z_0z_2}=0.                  \tag{13}
\]

The two blocks from \(z_0\) to the removed type-\(22\) centres are
singular coordinate ports. There are no additional sites in the present
stratum. Equations (8)--(13) therefore leave \(z_0\) with no rank-three
neighbour, contradicting the global \(G_3(q)\) hypothesis.

[verify_live_three_zero_common_beta_all_orders.py](../computations/verify_live_three_zero_common_beta_all_orders.py)
checks over the rationals that the two fixed-size subset-incidence maps
have full column rank and audits the exact matching coefficients (9)--(12).
It runs through \(r=2,\ldots,8\), or residual nonzero shores of sizes
\(5,7,\ldots,17\); the proof above is independent of this finite audit.
