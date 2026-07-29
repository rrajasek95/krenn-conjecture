# The third split layer is injective for distinct exceptional beta values

## 1. Outcome

Continue from
[live-three-zero-first-split-layers.md](live-three-zero-first-split-layers.md).
At the third split layer,

\[
                         t=r+4,\qquad r\ge5,                      \tag{1}
\]

there are \(2r-1\) live sites, \(t\) of them exceptional, and
\(r-3\) common-beta residual sites after the two type-\(10\) centres are
included.  There are no additional nonzero singular sites.

**Theorem 1.1 (distinct-beta third split).**  Suppose the \(t=r+4\)
exceptional live beta values are pairwise distinct.  Then the vanishing
cyclic response forces every residual nonzero-to-\(z_0\) block to
vanish.  Hence \(z_0\) is isolated in \(G_3(q)\), a contradiction.

The result is uniform in \(r\), has no generic-minor exception inside
the pairwise-distinct stratum, and treats the repeated common-beta
columns by a genuine confluent Borchardt quotient.  It does **not** infer
the collision strata by density.  Repeated exceptional beta values are
outside the scope of this note; they are treated separately by the
double-confluent/Hermite argument in
[live-three-zero-third-split-collision-beta.md](live-three-zero-third-split-collision-beta.md),
except at \(r=5,t=9\), where
[live-three-zero-all-exceptional-nine-live.md](live-three-zero-all-exceptional-nine-live.md)
already handles all repetitions.

## 2. Singleton-active pivots

Use the normalization and complete response formula of the preceding
notes.  Put

\[
                        p=r-1,\qquad k=r-4=p-3.                   \tag{2}
\]

Fix an exceptional triple \(R\).  Its complement among the exceptional
sites is

\[
                    N=E\setminus R,\qquad |N|=r+1=p+2.           \tag{3}
\]

For any \(p\)-subset \(L\subset N\), the complement
\(B=N\setminus L\) is a pair.  Give \(B\) colour \(2\), use it as the
unique marked pair for \(x_2z_2\), give \(L\) and one target active site
colour \(0\), and give \(R\) and the other \(k\) active sites colour
\(1\).

As before, this isolates the row-zero target star.  Let
\({\cal C}_{L\mid R}\) be the \(p\times p\) Cauchy matrix with row
parameters \(\{\nu_\ell:\ell\in L\}\) and column parameters

\[
                    \{\nu_c:c\in R\}\sqcup\{\mu^{[k]}\},         \tag{4}
\]

where \(\mu^{[k]}\) denotes \(k\) identical columns.  The exact pivot is

\[
                         C_{L\mid R}
                           =2h_{01}^{\,p}\operatorname {per}
                              {\cal C}_{L\mid R}.                 \tag{5}
\]

Equivalently, expanding the \(k\) common-beta columns gives the formula

\[
 C_{L\mid R}
 =2h_{01}^{\,p}k!
   \left(\prod_{\ell\in L}{1\over\nu_\ell+\mu}\right)
   \sum_{\substack{J\subset L\\|J|=3}}
       \operatorname {per}
       \left(
        {\nu_i+\mu\over\nu_i+\nu_c}
       \right)_{i\in J,\ c\in R}.                               \tag{6}
\]

Binary colour swapping gives row one.  Giving the target colour \(2\)
then gives row two after the already-vanishing binary rows are removed.
The direct coordinate-factor term is exactly zero in these equations
because \(B_{22}=0\).  Thus it is enough to prove that at least one
pivot (5) is nonzero.

## 3. The precise confluent Borchardt quotient

For a variable \(x\), define \(p\) denominator-kernel functions

\[
\begin{array}{ll}
 e_c(x)={1\over x+\nu_c},&
 a_c(x)={1\over(x+\nu_c)^2}
       \qquad(c\in R),\\[2mm]
 e_{\mu,j}(x)={(-1)^j\over(x+\mu)^{j+1}},&
 a_{\mu,j}(x)={(-1)^j(j+1)\over(x+\mu)^{j+2}}
       \qquad(0\le j<k).
\end{array}                                                       \tag{7}
\]

The last two expressions are the divided derivatives

\[
 {1\over j!}\partial_y^j{1\over x+y}\bigg|_{y=\mu},
 \qquad
 {1\over j!}\partial_y^j{1\over(x+y)^2}\bigg|_{y=\mu}.           \tag{8}
\]

Let \({\cal E}_L\) and \({\cal A}_L\) be their evaluation matrices on
the \(p\) row values in \(L\).  Start with distinct columns
\(\mu_1,\ldots,\mu_k\), apply Borchardt's identity

\[
 \operatorname {per}{\cal C}
                  ={\det({\cal C}^{\circ2})\over\det{\cal C}},
\]

and let all \(\mu_j\) tend independently to \(\mu\).  Dividing numerator
and denominator by the same column Vandermonde gives the exact finite
limit

\[
                  \operatorname {per}{\cal C}_{L\mid R}
                         ={\det{\cal A}_L\over\det{\cal E}_L}.    \tag{9}
\]

This is not a substitution into the singular distinct-column formula:
the derivative columns in (7) are the confluent limit.

Because the row beta values are distinct, the three values in \(R\) are
distinct, and none equals \(\mu\), the confluent Cauchy determinant
\(\det{\cal E}_L\) is nonzero.  Hence a pivot (5) vanishes exactly when
\(\det{\cal A}_L=0\).

## 4. Rank loss produces one forced numerator polynomial

Suppose every pivot for a fixed \(R\) vanished.  Since every
\(p\)-subset \(L\subset N\) occurs, all maximal minors of the
\((p+2)\times p\) evaluation matrix \({\cal A}_N\) vanish.  Therefore
its columns are dependent.  A nonzero linear combination of the
functions \(a_c,a_{\mu,j}\) in (7) vanishes at all \(p+2\) distinct
values \(\nu_i\), \(i\in N\).

Give that rational function the common denominator

\[
 D_R(x)=(x+\mu)^{k+1}\prod_{c\in R}(x+\nu_c)^2.                  \tag{10}
\]

Its degree is

\[
                           \deg D_R=k+7=p+4.
\]

Every numerator has degree at most

\[
                           \deg D_R-2=p+2=|N|.                   \tag{11}
\]

The functions in (7) are linearly independent by their distinct
principal parts, so the numerator is not zero.  Its \(p+2\) distinct
roots and (11) force it to be

\[
                         \lambda P_R(x),\qquad
 P_R(x)=\prod_{i\in N}(x-\nu_i),\qquad \lambda\ne0.              \tag{12}
\]

Thus the only possible rank-loss function is
\(\lambda P_R(x)/D_R(x)\).

## 5. Zero residues give an impossible Möbius relation

Write \(R=\{a,b,c\}\), using the same letters for the beta values.
The span in (7) contains a double-pole term at \(-a\) but no simple-pole
term there.  Consequently the residue of \(P_R/D_R\) at \(-a\) must
vanish.  Taking the logarithmic derivative of the factor remaining
after \((x+a)^2\) gives

\[
 -\sum_{i\notin R}{1\over a+\nu_i}
 = {k+1\over\mu-a}
    +{2\over b-a}+{2\over c-a}.                                 \tag{13}
\]

Now replace \(c\) by a fourth distinct exceptional value \(d\), keeping
\(a,b\) fixed, and subtract the two instances of (13).  All common
terms cancel:

\[
 {1\over a+c}-{1\over a+d}
       =2\left({1\over c-a}-{1\over d-a}\right).                 \tag{14}
\]

Since \(c\ne d\), equation (14) is equivalent to

\[
 (c-a)(d-a)=2(a+c)(a+d),                                        \tag{15}
\]

or

\[
                \rho_a(c)\rho_a(d)=2,\qquad
                \rho_a(x)={x-a\over x+a}.                       \tag{16}
\]

All denominators in (13)--(16) are structurally nonzero.  Fix
five distinct exceptional values \(a,b,c,d,e\).  Applying (16) to
\((c,d)\) and \((c,e)\) gives

\[
                         \rho_a(d)=\rho_a(e).                    \tag{17}
\]

If \(a=0\), equation (16) already reads \(1=2\).  If \(a\ne0\),
\(\rho_a\) is an injective Möbius transformation, so (17) says
\(d=e\), again a contradiction.  There are at least nine distinct
exceptional values in the present stratum, so the five choices are
available.

Thus the pivots cannot all vanish even for one fixed-\(R\) family across
all choices of \(R\).  Some pivot (5) is nonzero, proving Theorem 1.1.

## 6. Collision scope

If exceptional beta values collide, the ordinary row determinant in
(9) also becomes confluent.  One must then use Hermite evaluation rows,
and vanishing of the labeled cofactor pivots does not automatically say
that every arbitrary maximal minor of one fixed jet matrix vanishes.
Rank can drop on a collision divisor, so the pairwise-distinct theorem
cannot be extended by density.

This continuation is carried out in
[live-three-zero-third-split-collision-beta.md](live-three-zero-third-split-collision-beta.md).
There the particular initial-jet minors obtained by deleting two labeled
sites force a dependence among ordinary rows; a common-\(\mu\)
Vandermonde block excludes that dependence.  No collision conclusion is
drawn from density.

## 7. Exact audit

[verify_live_three_zero_third_split_distinct_beta.py](../computations/verify_live_three_zero_third_split_distinct_beta.py)
checks the repeated-column expansion (6) for \(4\le p\le9\), verifies
the five-square collision limit in (9) exactly, and audits the degree
count (11) through \(p=12\).

It also checks the sign in the residue subtraction:

\[
\begin{aligned}
 &{1\over a+c}-{1\over a+d}
 -2\left({1\over c-a}-{1\over d-a}\right)\\
 &\quad=
 { (c-d)\bigl(a^2+3a(c+d)+cd\bigr)\over
   (a-c)(a+c)(a-d)(a+d)},
\end{aligned}
\]

and verifies that (15) has the same obstruction numerator.
