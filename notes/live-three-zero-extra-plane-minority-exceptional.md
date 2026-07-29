# A minority of exceptional live betas cannot rescue the extra plane

## 1. Outcome

Retain the sole-extra-plane configuration of
[live-three-zero-extra-plane-common-beta-all-orders.md](live-three-zero-extra-plane-common-beta-all-orders.md).
The live shore has size \(2r\), the residual coordinate centres are \(c,d\),
and the extra singular site \(e\) satisfies

\[
                  \operatorname {im}P_e=\langle e_0,e_1\rangle . \tag{1}
\]

Let \(t\) live sites have beta value different from the common centre value
\(\mu\).

**Theorem 1.1 (minority-exceptional extra-plane injectivity).**  If

\[
                         r\ge3,\qquad 1\le t\le r-2,              \tag{2}
\]

then the vanishing cyclic response forces every residual block at the
shared zero \(z_0\) to vanish.  Thus \(z_0\) has no rank-three neighbour,
a contradiction.

Together with the common-beta all-order theorem, this closes
\(0\le t\le r-2\) whenever there is exactly one extra plane.  The result
allows arbitrary repetitions among the exceptional beta values and every
admissible complex value; it uses no density or positivity argument.

## 2. Active sites and binary weights

Normalize the common beta value to \(1\), put every live matrix at \(I\),
put \(P_c=P_d=D=\operatorname {diag}(1,1,0)\), and normalize

\[
                    H=\begin{pmatrix}0&1&1\\1&0&1\\1&1&0\end{pmatrix}.
                                                                    \tag{3}
\]

Write \(E\) for the \(t\) exceptional live sites, with beta values
\(\nu_j\ne1\).  Their zero-star blocks vanish structurally:

\[
                         (\nu_j-1)q_{jz_0}=0.                     \tag{4}
\]

The active coordinate sites are

\[
 A=(U\setminus E)\sqcup\{c,d\},\qquad
                         |A|=n=2r+2-t.                           \tag{5}
\]

On binary rows put

\[
          \kappa={1\over2},\qquad
          \lambda_j={1\over1+\nu_j},\qquad
          \Lambda=\prod_{j\in E}\lambda_j.                       \tag{6}
\]

Every scalar in (6) is nonzero.  If all exceptional sites lie on one
binary shore, every one must pair with a common-beta site on the other
shore.  Consequently every surviving matching has the same weight
\(\Lambda\kappa^m\); repeated exceptional values introduce no cancellation.

As before, let

\[
                  R=\operatorname {row}P_e,\qquad
                  p=\eta^{\mathsf T}P_e=(p_0,p_1,p_2)\in R       \tag{7}
\]

after contracting the output at \(e\).  Fix a coordinate at \(z_0\) and
write \(Z_{i,a}\) for the corresponding star entry.  Define the nonzero
common factors

\[
\begin{aligned}
 K_{r,t}&=(r+1)r!\Lambda\kappa^{r-t},\\
 L_{r,t}&=(r+2)K_{r,t},\\
 M_{r,t}&=rK_{r,t}.                                              \tag{8}
\end{aligned}
\]

Only diagonal source rows will be used, so the direct \(01\)-quadratic
contributes zero.

## 3. Fixed-subset equations

Give every exceptional site colour \(0\).  For
\(S\subset A\) with

\[
                              |S|=r+1-t,                          \tag{9}
\]

give \(S\) colour \(0\), give \(A\setminus S\) colour \(1\), contract
\(e\) to \(p\), and use source \(11\).  The two marked ordinary sites and
the alternative in which \(e\) is marked combine to give

\[
 K_{r,t}\bigl((r+2)p_1+rp_2\bigr)
                         \sum_{i\in S}Z_{i,0}=0.                 \tag{10}
\]

For the second family, give every exceptional site colour \(1\), choose

\[
                              |S|=r+3,                            \tag{11}
\]

give \(S\subset A\) colour \(0\), and use source \(00\).  Exact expansion
gives

\[
                 L_{r,t}(p_1+p_2)\sum_{i\in S}Z_{i,0}=0.         \tag{12}
\]

To see the common factor directly, consider a star at \(i\in S\).
In (10), after the marked pair and star are removed, \(e\) pairs with
one of \(r\) zero sites.  Pairing it with an exceptional or a common site
gives the same product
\(\Lambda\kappa^{r-t}\), and the remaining bijection contributes \(r!\).
In (12), the same count holds with \(e\) forced onto a common zero.
Every star outside \(S\), and the star at \(e\), has unbalanced binary
shores and contributes zero.  This proves (10)--(12), including the
absence of hidden cancellation.

Both subset sizes are proper and nonempty precisely in the range needed
here; for (11), condition \(r+3\le n-1\) is equivalent to \(t\le r-2\).
As in the common-beta proof, the two linear forms

\[
                         (r+2)p_1+rp_2,\qquad p_1+p_2             \tag{13}
\]

cannot both vanish on the two-plane \(R\).  Choose the corresponding
family.  Fixed-size subset incidence has full column rank, so

\[
                              Z_{i,0}=0\qquad(i\in A).             \tag{14}
\]

Swapping binary colours gives the forms
\((r+2)p_0+rp_2\) and \(p_0+p_2\), and hence

\[
                              Z_{i,1}=0\qquad(i\in A).             \tag{15}
\]

## 4. The extra block and the centre third rows

Give every exceptional site colour \(0\), give \(r-t\) active sites
colour \(0\), give the remaining \(r+2\) active sites colour \(1\), and
use source \(11\).  Contract \(e\) by an arbitrary \(\eta\).  The star at
\(e\) has balanced binary cofactor, while every active off-star term
contains (14) or (15), and every exceptional star is zero by (4).  Thus

\[
                         L_{r,t}\eta^{\mathsf T}q_{e z_0}=0.      \tag{16}
\]

This kills the entire extra block.

For row \(2\) at \(c\), give \(c\) that zero row and choose
\(0\ne p\in R\cap\{p_0=0\}\).  Put every exceptional site on the
colour-\(1\) shore and use source \(00\).  With \(r+2\) active zeros among
\(A\setminus\{c\}\), the singleton coefficient is

\[
                              L_{r,t}(p_1+p_2).                   \tag{17}
\]

If this vanishes, then \(p_2\ne0\); using \(r+1\) active zeros instead
gives the nonzero coefficient

\[
                              M_{r,t}p_2.                         \tag{18}
\]

All off-star terms contain the zero row of \(P_c\), so (17)--(18) kill
\(Z_{c,2}\).  They kill \(Z_{d,2}\) identically.

## 5. Live third rows

Suppose first that some \(p\in R\) has \(p_2\ne0\).  Choose any two
common-beta live sites \(i,j\), give them colour \(2\), give every
exceptional site colour \(0\), and split the remaining active sites into
\(r-t\) zeros and \(r\) ones.  Use source \(22\) and contract \(e\) to
\(p\).  The only surviving unknowns are the two live third rows, and

\[
        2r!\Lambda\kappa^{r-t}p_2
                         (Z_{i,2}+Z_{j,2})=0.                    \tag{19}
\]

There are \(2r-t\ge r+2\ge5\) common-beta live sites.  All pair sums
therefore force every live \(Z_{i,2}\) to vanish.

If \(p_2=0\) throughout \(R\), then \(R=\langle e_0,e_1\rangle\), and an
output change makes \(P_e=D\).  It joins the active binary-coordinate
sites.  Give one common live site colour \(2\), give every exceptional
site colour \(0\), split the other active sites into \(r-t\) zeros and
\(r+2\) ones, and use source \(11\).  The unique remaining third-row
coefficient is \(L_{r,t}\ne0\).  The same one-ternary-letter row kills the
third row at each singular active site.

Repeating the argument for every coordinate at \(z_0\), and adjoining the
structurally zero exceptional blocks (4), kills the entire residual star.
The removed type-\(22\) ports are singular and the zero--zero blocks vanish
by beta parity.  This proves Theorem 1.1.

## 6. Exact audit

[verify_live_three_zero_extra_plane_minority_exceptional.py](../computations/verify_live_three_zero_extra_plane_minority_exceptional.py)
constructs the complete marked response over the rational function fields
in \(p_0,p_1,p_2,\nu_1,\ldots,\nu_t\).  It checks (10)--(19), every claimed
zero support, both subset-incidence ranks, and the coordinate-plane branch
at \((r,t)=(3,1),(4,1),(4,2)\).  The factorial proof above is uniform in
\(r,t\).
