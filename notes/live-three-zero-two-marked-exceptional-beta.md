# Two marked exceptional sites remove the next three-zero boundary

## 1. Outcome

Continue from
[live-three-zero-minority-exceptional-beta.md](live-three-zero-minority-exceptional-beta.md).
The residual has \(2r-1\) live sites, two type-\(10\) centres, the shared
zero \(z_0\), and no additional nonzero singular sites.  The four centres
have beta value \(\mu\ne0\).  Let \(t\) be the number of live sites whose
beta value is different from \(\mu\).

**Theorem 1.1 (two-marked exceptional-star injectivity).**  If

\[
                         2\le t\le r+1,                            \tag{1}
\]

then the vanishing cyclic response \({\cal D}_0(x,z)=0\) forces

\[
                    q_{i z_0}=0
                    \quad\text{at every residual nonzero site }i. \tag{2}
\]

Thus \(z_0\) has no incident rank-three edge, contradicting the
connected-spanning hypothesis on \(G_3(q)\).

Together with the common-beta and one-exceptional arguments, Theorem 1.1
closes every no-extra-singular stratum with

\[
                              0\le t\le r+1.                       \tag{3}
\]

The first range not covered by a cancellation-free monomial coefficient
is consequently

\[
                         r+2\le t\le2r-1.                          \tag{4}
\]

This range is empty when \(r=2\).  When \(r=3\), its sole
all-exceptional case \(t=5\) is closed in
[live-three-zero-all-exceptional-five-live.md](live-three-zero-all-exceptional-five-live.md).

## 2. Normalization and the two sites to be marked

Normalize every live \(P_i\) to \(I\) and the two type-\(10\) matrices to

\[
                         D=\operatorname {diag}(1,1,0).
\]

Write the exceptional sites as \(E=\{y_1,\ldots,y_t\}\), with beta values
\(\nu_j\ne\mu\).  Their star blocks already vanish:

\[
                         (\nu_j-\mu)q_{y_jz_0}=0.                  \tag{5}
\]

The potentially nonzero star blocks are therefore indexed by

\[
 A=\{\text{common-beta live sites}\}
       \sqcup\{\text{two type-}10\text{ centres}\},\qquad
 |A|=2r+1-t.                                                       \tag{6}
\]

Fix a coordinate \(b\) at \(z_0\), and set
\(Z_{i,a}=q_{i z_0}[a,b]\).  For binary internal edges put

\[
 \kappa={h_{01}\over2\mu},\qquad
 \lambda_j={h_{01}\over\mu+\nu_j}.                                \tag{7}
\]

All these scalars are nonzero.  Choose any two exceptional sites,
say

\[
                              B=\{y_1,y_2\}.                       \tag{8}
\]

The new ingredient is to give precisely the sites in \(B\) local colour
\(2\) and to read the diagonal source coefficient \(x_2z_2\).  They are
then the unique marked pair: all other sites have binary colours, and
the type-\(10\) centres have zero third column in \(D\).

## 3. Fixed-cardinality equations for rows zero and one

Give every exceptional site in \(E\setminus B\) colour \(0\).  For a
subset \(T\subset A\), give the sites in \(T\) colour \(0\), the sites in
\(A\setminus T\) colour \(1\), and impose

\[
                              |T|=r+2-t.                           \tag{9}
\]

After removing the marked pair \(B\) and a zero-star site \(i\in T\),
the two binary shores both have size \(r-1\):

\[
 |(E\setminus B)\sqcup(T\setminus\{i\})|
       =t-2+(r+2-t)-1=r-1,
\]
\[
 |A\setminus T|=(2r+1-t)-(r+2-t)=r-1.                             \tag{10}
\]

Every unmarked exceptional site must be paired to a common-beta site.
All perfect matchings therefore have the same weight.  Their sum is the
single monomial

\[
 (r-1)!\left(\prod_{j=3}^{t}\lambda_j\right)
              \kappa^{\,r-t+1}.                                  \tag{11}
\]

The factor \(2\) from the ordered marked factors gives

\[
 C_B=2(r-1)!\left(\prod_{j=3}^{t}\lambda_j\right)
              \kappa^{\,r-t+1}\ne0.                              \tag{12}
\]

If the star site lies in \(A\setminus T\), the remaining binary shores
are unbalanced, so its cofactor is zero.  The exact response equation is
therefore

\[
                         C_B\sum_{i\in T}Z_{i,0}=0.                \tag{13}
\]

Condition (1) is exactly what guarantees

\[
                    1\le |T|=r+2-t<|A|.                          \tag{14}
\]

The incidence matrix of fixed-size proper nonempty subsets against
points has full column rank in characteristic zero.  Hence (13), for
all \(T\) of size (9), gives

\[
                              Z_{i,0}=0\qquad(i\in A).             \tag{15}
\]

Swapping binary colours \(0\) and \(1\), while leaving the marked sites
in colour \(2\), gives

\[
                              Z_{i,1}=0\qquad(i\in A).             \tag{16}
\]

Repeated exceptional beta values cause no problem: only the visibly
nonzero factors in (12) occur.

## 4. The same marked pair kills row two

Fix \(i\in A\).  Give \(i,y_1,y_2\) colour \(2\), give every site in
\(E\setminus B\) colour \(1\), and among \(A\setminus\{i\}\) give
\(r-1\) sites colour \(0\) and the remaining \(r+1-t\) sites colour
\(1\).  The latter number is nonnegative precisely in the range (1).
Again read \(x_2z_2\).

For the coefficient of \(Z_{i,2}\), the marked pair must be \(B\).
After removing \(B\) and the star site \(i\), the zero shore has
\(r-1\) common-beta sites, while the one shore consists of \(t-2\)
exceptional and \(r+1-t\) common-beta sites.  The cofactor is (11), and
the coefficient is \(C_B\).

If \(i\) is a common-beta live site, it can itself participate in other
marked pairs.  Such terms cannot use \(i\) as the star and consequently
contain only a row-zero or row-one active star variable, or an
exceptional star variable.  They vanish by (5), (15), and (16).  If
\(i\) is a type-\(10\) centre, its third marked factor is already zero.
The response equation thus reduces exactly to

\[
                              C_B Z_{i,2}=0.                       \tag{17}
\]

This proves (2) after repeating the argument for every coordinate \(b\)
at \(z_0\).  The zero--zero blocks at \(z_0\) vanish because the three
zero beta values are all \(-\mu\), while its blocks to the removed
type-\(22\) centres are singular coordinate ports.  Therefore \(z_0\)
is isolated in \(G_3(q)\), completing the proof.

## 5. What remains

The two marked factors have absorbed exactly two exceptional sites.
For \(t\ge r+2\), the subset size in (9) is nonpositive and the
monochromatic cofactor cannot be balanced.  Any continuation must split
the \(t-2\) unmarked exceptional sites across the two binary shores, or
use response rows in which the marked pair is not forced.

For a fixed split, the cofactor is a Cauchy permanent

\[
 h_{01}^{\,r-1}
 \operatorname {per}
 \left({1\over\beta_x+\beta_y}\right)_{x\in X,\ y\in Y}.          \tag{18}
\]

Unlike (11), this need not be a single monomial over \(\mathbb C\).
Thus (4), rather than \(t\ge r\), is the first range requiring a
Cauchy-cancellation argument.  Its first case \(r=3,t=5\) is closed by
the three-minor cover cited above; no counterkernel occurs in the range
(1).

## 6. Exact audit

[verify_live_three_zero_two_marked_exceptional_beta.py](../computations/verify_live_three_zero_two_marked_exceptional_beta.py)
checks (9)--(17) over
\(\mathbb Q(\kappa,\lambda_1,\ldots,\lambda_t)\) for every
\(2\le r\le8\) and \(2\le t\le r+1\).  It also reconstructs the full
ternary response in the first endpoint case \(r=3,t=4\), retaining the
off-block terms caused when a common-beta live site participates in a
marked pair.

If \(B=\{y_1,y_2\}\), the proof rows form a \(9\times9\) minor with

\[
 \det M=
 \left(
 {4h_{01}^{\,2}\over
  (\mu+\nu_3)(\mu+\nu_4)}
 \right)^9\ne0.                                                   \tag{19}
\]
