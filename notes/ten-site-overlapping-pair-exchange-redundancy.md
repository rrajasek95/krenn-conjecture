# The ten-site overlapping pair system is an exchange reindexing

## 1. Outcome

For arbitrary ten-site edge data, the full nine equations for one deleted
physical pair already contain the full nine equations for every overlapping
deleted pair.  The exact compatibility identity behind this fact is the
triple-slice exchange

\[
 \boxed{
 \iota_{0,\alpha}
 \left(a_{ij}q^{[4]}+p_i s_jq^{[3]}\right)
 =
 \iota_{t,j}
 \left(b_{i\alpha}(q^{(0)})^{[4]}
       +\widetilde p_i\widetilde s_\alpha(q^{(0)})^{[3]}
 \right).}                                               \tag{1}
\]

Both sides are the \((i,j,\alpha)\) triple contraction of the same top
matching tensor.  In particular, once all nine first-pair tensor equations
hold, imposing the nine overlapping-pair tensor equations is not an
additional filter.  Their coefficient residuals are literally the same
polynomials with their indices permuted.

This closes a tempting but false interpretation of equations (27)--(29) in
[`polarized-eight-site-shared-pair-cap-countermodel.md`](polarized-eight-site-shared-pair-cap-countermodel.md):
the substitution is a useful second coordinate chart on the same equations,
but it does not supply new equations.  Any useful overlap argument must
extract a source-variable consequence from the exchange syzygies; it cannot
count the second full-nine system as independent information.

## 2. Arbitrary ten-site source and its first pair slice

Work in the commutative site-square-zero algebra.  Aggregate all parallel
sources on a physical pair into their endpoint-ordered \(3\times3\) block
before doing any calculation.  Let the ten sites be

\[
                       \{r,t,0,1,\ldots,7\}
\]

and decompose an arbitrary quadratic as

\[
 h=q+\sum_i e_i^{(r)}p_i+\sum_j e_j^{(t)}s_j
       +\sum_{i,j}a_{ij}e_i^{(r)}e_j^{(t)}.             \tag{2}
\]

Here \(q\) is internal to \(U=\{0,\ldots,7\}\).  Put

\[
                         H=h^{[5]},\qquad
                         Q=q^{[4]},\qquad F=q^{[3]}.
\]

Let \(\iota_{u,c}\) mean coefficient contraction at site \(u\) and color
\(c\).  Splitting a perfect matching according to whether it uses the
direct edge \(rt\), or sends \(r,t\) to two distinct sites of \(U\), gives

\[
 R^{rt}_{ij}:=\iota_{t,j}\iota_{r,i}H
              =a_{ij}Q+p_i s_jF.                       \tag{3}
\]

This is the raw pair equation.  There are \(105\) direct-edge matchings and
\(8\cdot7\cdot15=840\) two-star matchings, accounting once each for all
\(9!!=945\) perfect matchings of ten labeled sites.  Terms with coincident
star endpoints vanish in the site-square-zero algebra; no support or
noncancellation assumption is used.

The full ternary GHZ equation is equivalent to the nine tensor equations

\[
                    R^{rt}_{ij}=\delta_{ij}X_i^U
                    \qquad(0\leq i,j<3).               \tag{4}
\]

Indeed, a top-degree tensor has one mode at every site.  Its coefficient at
an arbitrary coloring is a coefficient of exactly one row in (4), selected
by the colors at \(r,t\).  Thus one complete pair slice already specifies
all \(3^{10}\) coefficients of \(H\).

## 3. The overlapping decomposition

Delete instead \(\{r,0\}\), with boundary
\(U'_0=\{t,1,\ldots,7\}\).  Sorting the same literal edge cells by their new
roles gives

\[
\begin{aligned}
 q^{(0)}
   &=q|_{\{1,\ldots,7\}}
     +\sum_{v=1}^7\sum_{j,\beta}
        s_{j,v,\beta}e_j^{(t)}e_\beta^{(v)},\\
 b_{i\alpha}&=p_{i,0,\alpha},\\
 \widetilde p_i
   &=\sum_j a_{ij}e_j^{(t)}
     +\sum_{v=1}^7\sum_\beta p_{i,v,\beta}e_\beta^{(v)},\\
 \widetilde s_\alpha
   &=\sum_j s_{j,0,\alpha}e_j^{(t)}
     +\sum_{v=1}^7
       \left(e_\alpha^{(0)*}\mathbin{\lrcorner}q_{0v}\right).
                                                               \tag{5}
\end{aligned}
\]

The named-endpoint contraction in the last line is essential: if the stored
orientation of the physical block is reversed, its two color indices are
reversed with it.  Formula (5) assigns each of the \(45\cdot9=405\)
endpoint-ordered edge cells to exactly one new role.

The corresponding raw row is

\[
 R^{r0}_{i\alpha}:=\iota_{0,\alpha}\iota_{r,i}H
 =b_{i\alpha}(q^{(0)})^{[4]}
   +\widetilde p_i\widetilde s_\alpha(q^{(0)})^{[3]}.
                                                               \tag{6}
\]

## 4. Exchange theorem

**Proposition 4.1 (pair-slice exchange).**  For every \(i,j,\alpha\), the
two tensors on the seven remaining sites satisfy (1).

**Proof.**  Coefficient contractions at three distinct sites commute.
Using (3) and (6),

\[
\begin{aligned}
 \iota_{0,\alpha}R^{rt}_{ij}
   &=\iota_{0,\alpha}\iota_{t,j}\iota_{r,i}H\\
   &=\iota_{t,j}\iota_{0,\alpha}\iota_{r,i}H\\
   &=\iota_{t,j}R^{r0}_{i\alpha}.
\end{aligned}                                           \tag{7}
\]

The argument is polynomial over \(\mathbb Z\) in the aggregated edge-cell
coefficients.  It therefore remains valid after arbitrary complex
specialization, including zero blocks, degeneracies, and cancellation among
many perfect matchings.  No coefficient is divided by anything.  \(\square\)

There is also a literal matching proof.  For either deleted pair, the direct
and two-star cases partition the same set of \(945\) perfect matchings.
After fixing the colors \((i,j,\alpha)\) at \((r,t,0)\) and an arbitrary
color word \(\omega\) on \(\{1,\ldots,7\}\), both sides of (1) sum the same
\(945\) edge-cell monomials, each with coefficient one.

## 5. Exact redundancy of the second full-nine system

Define the target residuals

\[
\begin{aligned}
 E^{rt}_{ij}&=R^{rt}_{ij}-\delta_{ij}X_i^U,\\
 E^{r0}_{i\alpha}&=R^{r0}_{i\alpha}
                     -\delta_{i\alpha}X_i^{U'_0}.
                                                               \tag{8}
\end{aligned}
\]

The target terms obey the same exchange identity, because

\[
 \iota_{0,\alpha}(\delta_{ij}X_i^U)
 =\iota_{t,j}(\delta_{i\alpha}X_i^{U'_0})
 =
 \begin{cases}
   X_i^{\{1,\ldots,7\}},&i=j=\alpha,\\
   0,&\text{otherwise}.
 \end{cases}                                             \tag{9}
\]

Hence

\[
       \boxed{\quad
       \iota_{0,\alpha}E^{rt}_{ij}
       =\iota_{t,j}E^{r0}_{i\alpha}\quad}               \tag{10}
\]

for every triple of colors.  After taking a coefficient at a word
\(\omega\) on the remaining seven sites, (10) reads

\[
 [e_\alpha^{(0)}e_\omega]E^{rt}_{ij}
   =[e_j^{(t)}e_\omega]E^{r0}_{i\alpha}.                \tag{11}
\]

As \((i,j,\alpha,\omega)\) ranges over its \(3^{10}=59{,}049\) values,
(11) is a bijection between the complete coefficient lists of the two
systems.  Consequently their generated ideals in the ring of the \(405\)
edge-cell coefficients are equal; in fact, the two generator lists are
the same list of top-tensor residual polynomials under reindexing.

It follows immediately that (4) implies

\[
                    R^{r0}_{i\alpha}
                    =\delta_{i\alpha}X_i^{U'_0}         \tag{12}
\]

for all \(i,\alpha\), and conversely.  The same statement holds for a
disjoint second pair, not only an overlapping one: every complete pair
slice is simply a coordinate chart for the entire top tensor.

## 6. Factor-four audit

For an eight-site internal quadratic,

\[
             q^{(0)}(q^{(0)})^{[3]}=4(q^{(0)})^{[4]}.
                                                               \tag{13}
\]

Every internal four-edge matching occurs four times on the left, once for
each choice of distinguished edge.  Therefore the polarized row is exactly
four times the raw row:

\[
\begin{aligned}
 &(b_{i\alpha}q^{(0)}
       +4\widetilde p_i\widetilde s_\alpha)
       (q^{(0)})^{[3]}\\
 &\hspace{35mm}=4R^{r0}_{i\alpha}.
                                                               \tag{14}
\end{aligned}
\]

Thus the targets are respectively

\[
 4\delta_{i\alpha}X_i^{U'_0}
 \quad\text{(polarized)},\qquad
 \delta_{i\alpha}X_i^{U'_0}
 \quad\text{(raw)}.                                    \tag{15}
\]

The same \(4{:}1\) relation holds for the first pair.  There is no hidden
factor depending on which pair is deleted.

## 7. Consequence for the conjecture attack

This result is negative about one proposed source of leverage, but positive
about the exact structure to use next.

1. A search that solves all nine tensor equations for one deleted pair has
   already solved the ten-site top GHZ equation.  Applying (5) and then
   “imposing” the second nine equations cannot remove any survivor.
2. Lower cap-minor identities from another pair may be useful rewritten
   consequences for elimination, but they are not additional hypotheses
   once the first full-nine tensor system is retained.
3. A genuine overlap step must use (10) as a syzygy among the different
   source-variable presentations and prove a new elimination consequence,
   such as the desired clean internal cap.  Dimension counts which simply
   add the two full-nine systems double-count the same \(3^{10}\) residuals.
4. If one works with a projected or aggregated equation instead of all nine
   rows, then a second chart can add information; that is a different,
   explicitly weakened system.

The standalone checker
[`verify_ten_site_overlapping_pair_exchange_redundancy.py`](../computations/verify_ten_site_overlapping_pair_exchange_redundancy.py)
independently enumerates all \(945\) perfect matchings, audits both
\(105+840\) pair partitions, redecomposes all \(405\) endpoint-ordered
cells through (5), compares the universal matching polynomials, verifies
the polarized/raw factors \((4,1)\), and checks all \(59{,}049\) target
coordinate reindexings.
