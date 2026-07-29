# A minority of exceptional live beta values cannot support the three-zero star

## 1. Outcome

Continue from the cyclic three-zero setup in
[live-three-zero-common-power-star-injectivity.md](live-three-zero-common-power-star-injectivity.md).
The four centres have beta value \(\mu\ne0\), the three literal zero sites
have beta value \(-\mu\), and the residual contains

\[
                         |U|=2r-1\ge3                              \tag{1}
\]

live sites, the two type-\(10\) centres, and the shared zero site \(z_0\).
Assume there are no additional nonzero singular sites. Call a live site
exceptional when its beta value differs from \(\mu\), and let \(t\) be the
number of exceptional live sites.

**Theorem 1.1 (minority-exceptional star injectivity).** If

\[
                              0\le t\le r-1,                        \tag{2}
\]

then the vanishing cyclic response \({\cal D}_0(x,z)=0\) forces

\[
                    q_{i z_0}=0
                    \quad\text{at every residual nonzero site }i. \tag{3}
\]

Consequently \(z_0\) has no incident rank-three edge, contradicting the
connected-spanning hypothesis on \(G_3(q)\).

This includes arbitrary repeated exceptional beta values and every
admissible complex value: there is no genericity assumption and no
positivity argument. In particular, it closes every two-exceptional-beta
case once \(|U|\ge5\); the remaining \(|U|=3\) cases were already closed
by the minimal symbolic star calculation.

For this first monochromatic construction, the provisional remaining
range is

\[
                              t\ge r.                              \tag{4}
\]

The continuation
[live-three-zero-two-marked-exceptional-beta.md](live-three-zero-two-marked-exceptional-beta.md)
uses the two marked factors to absorb two exceptional sites and closes
the larger range \(t\le r+1\).  Thus the combined argument leaves only
\(t\ge r+2\).

## 2. Active and exceptional sites

Normalize every live \(P_i\) to \(I\) and the two residual type-\(10\)
matrices to \(D=\operatorname {diag}(1,1,0)\) by independent local basis
changes. If an exceptional live site \(y_j\) has beta value
\(\nu_j\ne\mu\), then

\[
                         (\nu_j-\mu)q_{y_jz_0}=0,                   \tag{5}
\]

so its zero-star block already vanishes. The possible nonzero star blocks
are at the common-beta sites

\[
 A=\{\text{live sites of beta }\mu\}
       \sqcup\{\text{two type-}10\text{ centres}\},\qquad
 |A|=2r+1-t.                                                       \tag{6}
\]

Fix a coordinate \(b\) at \(z_0\), and put
\(Z_{i,a}=q_{i z_0}[a,b]\) for \(i\in A\). On binary local colours define

\[
 \kappa={h_{01}\over2\mu},\qquad
 \lambda_j={h_{01}\over\mu+\nu_j}.                                \tag{7}
\]

Every scalar in (7) is nonzero. In particular,
\(\mu+\nu_j\ne0\), because the structural left side between the live site
\(y_j\) and either type-\(10\) centre has rank two.

## 3. Monochromatizing the exceptional sites removes cancellation

Give all \(t\) exceptional sites colour \(0\). Let \(T\subset A\) have

\[
                              |T|=r-t,                              \tag{8}
\]

give the sites of \(T\) colour \(0\), give the other sites of \(A\)
colour \(1\), and take the diagonal source coefficient \(x_1z_1\).

In a surviving term the two marked factors occupy colour-\(1\) sites.
If the zero-star edge uses \(i\in T\), the remaining cofactor has
\(r-1\) zeros and \(r-1\) ones. Every exceptional zero must use a distinct
common-beta one. There are

\[
 { (r-1)!\over(r-t-1)!}
\]

ways to choose and assign those partners, followed by
\((r-t-1)!\) bijections between the remaining common-beta zeros and
ones. Thus the cofactor is the single nonzero monomial

\[
                  (r-1)!\left(\prod_{j=1}^t\lambda_j\right)
                     \kappa^{r-t-1}.                               \tag{9}
\]

There is no cancellation among different perfect matchings: all of them
have exactly the same weight. If the star uses a site outside \(T\), the
binary counts are unbalanced and the cofactor vanishes. The marked pair
has \(\binom{r+1}{2}\) choices, so the exact coefficient equation is

\[
 C_{r,t}\sum_{i\in T}Z_{i,0}=0,\qquad
 C_{r,t}
   =2\binom{r+1}{2}(r-1)!
      \left(\prod_{j=1}^t\lambda_j\right)
      \kappa^{r-t-1}\ne0.                              \tag{10}
\]

Condition (2) is exactly what makes

\[
                       1\le |T|=r-t\le |A|-1.                      \tag{11}
\]

The incidence matrix of fixed-size proper nonempty subsets versus points
has full column rank in characteristic zero: subtracting two rows which
exchange one point shows all coordinates are equal, and one row sum then
kills the common value. Applying this to (10) gives

\[
                              Z_{i,0}=0\qquad(i\in A).              \tag{12}
\]

Colour-swapping the construction and using \(x_0z_0\) gives

\[
                              Z_{i,1}=0\qquad(i\in A).              \tag{13}
\]

## 4. One ternary letter kills the last row

Fix \(i\in A\), give \(i\) local colour \(2\), and give every exceptional
site colour \(1\). Among the other sites of \(A\), use \(r+1\) zeros and
\(r-t-1\) ones, and take the source coefficient \(x_0z_0\).

When the star uses \(i\), the marked pair has
\(\binom{r+1}{2}\) choices and leaves a balanced cofactor with all
exceptional sites on its one side. Its coefficient is exactly
\(C_{r,t}\). Every term whose star uses another common-beta site contains
a variable from (12)--(13), while every exceptional star is zero by (5).
The full equation therefore reduces to

\[
                              C_{r,t}Z_{i,2}=0.                     \tag{14}
\]

This proves (3) after repeating the argument for all three coordinates
\(b\) at \(z_0\). The two zero--zero blocks at \(z_0\) vanish because all
three zero beta values are \(-\mu\), and the two blocks to the removed
type-\(22\) centres are singular coordinate ports. Hence no rank-three
edge is incident with \(z_0\), completing the proof of Theorem 1.1.

## 5. The apparent majority-exceptional Cauchy boundary

The threshold (4) is sharp for the monochromatization argument. If all
\(t\) exceptional sites are put on one binary side, a star term needs
\(r-t\) common-beta sites on that side. This is a nonempty subset exactly
when \(t\le r-1\). For \(t\ge r\), every usable balanced coefficient must
split the exceptional sites between the two binary colours or allow some
of them to carry marked factors.

For any fixed marked pair and star site, let \(X,Y\) be the two colour
classes in the remaining balanced cofactor. Its exact value is

\[
 h_{01}^{\,r-1}
   \operatorname {per}
      \left({1\over\beta_x+\beta_y}\right)_{x\in X,\ y\in Y}.
                                                                    \tag{15}
\]

Without changing the marked-factor pattern, the next stratum is a finite
weighted fixed-cardinality incidence system whose entries are sums of
the Cauchy permanents (15).
Individual entries can vanish over \(\mathbb C\); discarding that
possibility would reintroduce the forbidden generic-weight assumption.

When the beta values on each side are pairwise distinct, Borchardt's
identity rewrites (15) as

\[
 \operatorname {per}(C)
      ={\det(C^{\circ2})\over\det C},
 \qquad C_{xy}={1\over\beta_x+\beta_y}.                            \tag{16}
\]

Repeated beta values must be handled by the original permanent or by a
confluent limit, because both determinants in (16) can vanish. Poles
\(\beta_x+\beta_y=0\) do not form an escape: the structural left side is
invertible for two live sites and has rank two for a live/type-\(10\)
pair, so every such denominator is nonzero.

Equations (15)--(16) isolate the apparent cancellation locus for this
particular word family without asserting that it is empty.  The
two-marked continuation cited above postpones the genuine unresolved
range to \(t\ge r+2\).  No counterkernel occurs in the
minority-exceptional range: equations (10)--(14) give injectivity there
identically.

## 6. Exact audit

[verify_live_three_zero_minority_exceptional_beta.py](../computations/verify_live_three_zero_minority_exceptional_beta.py)
checks the fixed-subset incidence rank and reconstructs (9)--(14) over
\(\mathbb Q(\kappa,\lambda_1,\ldots,\lambda_t)\) for every
\(2\le r\le8\) and \(0\le t\le r-1\).

For the first new two-exceptional case \(r=3,t=2\), it also constructs the
full ternary response with five live sites and two type-\(10\) centres.
Ordering the five common-beta star sites by coordinate rows, the proof's
fifteen equations form a \(15\times15\) minor with determinant

\[
 \left(
 {24h_{01}^{\,2}\over
   (\mu+\nu_1)(\mu+\nu_2)}
 \right)^{15}\ne0.                                                \tag{17}
\]
