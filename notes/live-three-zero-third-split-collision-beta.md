# The third split layer is injective on every collision stratum

## 1. Outcome

Continue from
[live-three-zero-third-split-distinct-beta.md](live-three-zero-third-split-distinct-beta.md).
At the third split layer, put

\[
                 t=r+4,\qquad p=r-1,\qquad k=r-4=p-3.            \tag{1}
\]

There are \(p+5\) exceptional labels.  Their beta values may repeat,
but every structural sum \(\nu_i+\nu_j\) and \(\nu_i+\mu\) is nonzero.

**Theorem 1.1 (collision strata).**  For \(r\ge6\), if the exceptional
beta values are not pairwise distinct, then some singleton-active pivot
is nonzero.  Hence the vanishing cyclic response forces every residual
nonzero-to-\(z_0\) block to vanish, and \(z_0\) is isolated in
\(G_3(q)\), a contradiction.

Together with the distinct-beta theorem and the all-repetition
\(r=5,t=9\) result in
[live-three-zero-all-exceptional-nine-live.md](live-three-zero-all-exceptional-nine-live.md),
this closes the entire layer \(t=r+4\), with no restriction on beta
multiplicities.

The continuation to the first \(t=r+5\) case is
[live-three-zero-all-exceptional-eleven-live.md](live-three-zero-all-exceptional-eleven-live.md).

The proof has two parts.  A value of multiplicity at least three gives
a direct elementary-symmetric obstruction.  If every multiplicity is
at most two, the actual labeled pivots are initial-jet minors of a
double-confluent Cauchy matrix.  Their restricted Plücker support is
already enough: it would force a dependence inside a Vandermonde block.
Thus no density argument is used.

## 2. The common pivot

Fix three exceptional labels \(R\), put

\[
                         N=E\setminus R,\qquad |N|=p+2,           \tag{2}
\]

and choose a marked pair \(B\subset N\).  Then
\(L=N\setminus B\) has size \(p\).  The singleton-active construction
of the preceding note has pivot

\[
 C_{L\mid R}
 =2h_{01}^{\,p}k!
   \left(\prod_{\ell\in L}{1\over\nu_\ell+\mu}\right)
   G_{L\mid R},                                                  \tag{3}
\]

where

\[
 G_{L\mid R}
 =\sum_{\substack{J\subset L\\|J|=3}}
       \operatorname {per}H[J,R],\qquad
 H_{ic}={\nu_i+\mu\over\nu_i+\nu_c}.                            \tag{4}
\]

Every factor outside \(G_{L\mid R}\) is structurally nonzero.  Any one
nonzero pivot kills all three rows at every active site, exactly as in
Section 2 of the distinct-beta note.  Suppose henceforth, toward a
contradiction, that (3) vanishes for every \(R\) and \(B\).

## 3. A multiplicity-three class is already impossible

Suppose a beta value \(a\) occurs at least three times.  Choose three
such labels for \(R\).  The three columns of \(H[J,R]\) are identical.
Writing

\[
                         h_i={\nu_i+\mu\over\nu_i+a}\ne0,         \tag{5}
\]

equation (4) becomes

\[
                       G_{L\mid R}=6e_3(h_i:i\in L).             \tag{6}
\]

The following elementary lemma rules out the vanishing of (6).

**Lemma 3.1.**  If \(m\ge5\) and \(h_1,\ldots,h_m\) are nonzero, then
the quantities

\[
                         e_3(h_i:i\notin B),\qquad |B|=2,        \tag{7}
\]

cannot all vanish.

Indeed, if all \(h_i\) are equal, (7) is a nonzero binomial multiple
of their common cube.  Otherwise choose \(h_j\ne h_k\).  Comparing
(7) for \(B=\{i,j\}\) and \(B=\{i,k\}\) gives

\[
               (h_k-h_j)e_2(h_u:u\notin\{i,j,k\})=0.            \tag{8}
\]

Put \(W=[m]\setminus\{j,k\}\).  Thus
\(e_2(W\setminus\{i\})=0\) for every \(i\in W\).  Summing these
relations yields

\[
                         (|W|-2)e_2(W)=0,                        \tag{9}
\]

so \(e_2(W)=0\).  For each \(i\in W\),

\[
 0=e_2(W\setminus\{i\})
   =e_2(W)-h_i(e_1(W)-h_i)
\]

forces \(h_i=e_1(W)\).  All entries of \(W\) are therefore the same
nonzero value \(h\), but then \(h=|W|h\), a contradiction.  Here
\(|N|=p+2\ge7\), so the lemma applies.  Consequently every remaining
collision stratum has multiplicities only one or two.

## 4. Double confluence and the initial-jet minors

Assume every value has multiplicity at most two, and choose \(R\) from
three distinct value classes.  For \(c\in R\) and \(0\le j<k\), define

\[
\begin{array}{ll}
 e_c(x)={1\over x+\nu_c},&
 a_c(x)={1\over(x+\nu_c)^2},\\[2mm]
 e_{\mu,j}(x)={(-1)^j\over(x+\mu)^{j+1}},&
 a_{\mu,j}(x)={(-1)^j(j+1)\over(x+\mu)^{j+2}}.
\end{array}                                                       \tag{10}
\]

For a value \(x\) occurring \(q\in\{1,2\}\) times in \(L\), include
the \(q\) divided row jets

\[
             {1\over s!}\partial_x^s(e_\gamma(x))_\gamma,
 \quad
             {1\over s!}\partial_x^s(a_\gamma(x))_\gamma,
 \qquad 0\le s<q.                                                \tag{11}
\]

Call the resulting square matrices \({\cal E}^{H}_L\) and
\({\cal A}^{H}_L\).  Collide both the repeated row variables and the
\(k\) common-\(\mu\) column variables in Borchardt's identity.  Dividing
the numerator and denominator determinants by the same row and column
Vandermondes gives the exact double-confluent quotient

\[
 \operatorname {per}{\cal C}_{L\mid R}
             ={\det {\cal A}^{H}_L\over\det {\cal E}^{H}_L}.     \tag{12}
\]

The denominator is a double-confluent Cauchy determinant.  It is
nonzero because the distinct row classes and distinct column classes
are internally distinct and all cross sums are structurally nonzero.
Thus a zero pivot is exactly a zero numerator determinant in (12).

Now form the \((p+2)\times p\) global jet matrix
\({\cal A}^{H}_N\), using all multiplicities in \(N\).  Within each
value class designate its highest jet as the **top row**.  A singleton
has only its order-zero top row; a double class has an order-zero base
row and an order-one top row.  If \(B\) contains one label from each of
two distinct value classes \(u,v\), then \({\cal A}^{H}_L\) is exactly
the maximal submatrix obtained by deleting the two top rows \(t_u,t_v\).
Hence all those maximal minors vanish under the standing assumption.

Let \(d_N\) be the number of double classes remaining in \(N\).

**Lemma 4.1 (initial-jet rank).**  If \(d_N\le k\), the vanishing of all
the top-pair minors forces

\[
                         \operatorname {rank}{\cal A}^{H}_N<p.  \tag{13}
\]

Suppose instead that the rank were \(p\).  Its left kernel \(K\) would
be two-dimensional.  By maximal-minor duality, the deleted-pair minors
are, up to one common nonzero scalar and signs, the Plücker
coordinates of \(K\).  Their vanishing for every pair of top rows says
that the projection of \(K\) onto the top-row coordinates has dimension
at most one.  Some nonzero vector of \(K\) is therefore supported only
on the order-zero base rows of the \(d_N\) double classes.

Those base rows are independent.  Indeed, restrict them to the first
\(d_N\) common-\(\mu\) columns in (10), and put

\[
                              w_x={1\over x+\mu}.
\]

The resulting entries are

\[
                    (-1)^j(j+1)w_x^{\,j+2},\qquad
                    0\le j<d_N,                                 \tag{14}
\]

a nonsingular scaled Vandermonde matrix because the \(x\)'s, hence the
nonzero \(w_x\)'s, are distinct.  This contradicts the left-kernel
vector and proves (13).

## 5. A good triple forces a Hermite root polynomial

Call a distinct-valued triple \(R\) **good** if \(d_N\le k\).  For a
good triple, Lemma 4.1 and the assumed vanishing of all pivots give a
nonzero column dependence among the functions in (10).  Let \(F_R(x)\)
be the corresponding rational function.  Its common denominator is

\[
                 D_R(x)=(x+\mu)^{k+1}
                         \prod_{c\in R}(x+\nu_c)^2,              \tag{15}
\]

of degree \(p+4\), while the numerator \(Q_R=F_RD_R\) has degree at
most \(p+2\).  The functions in (10) are independent by principal
parts, so \(Q_R\ne0\).

The jet equations say that \(F_R\), and hence \(Q_R\), vanishes at each
node in \(N\) with its full label multiplicity.  There are \(p+2\) such
zeros counting multiplicity.  Therefore

\[
 Q_R(x)=\lambda_R P_R(x),\qquad
 P_R(x)=\prod_{i\in N}(x-\nu_i),\qquad \lambda_R\ne0.            \tag{16}
\]

This is the collision analogue of the forced numerator in the
distinct-beta proof: ordinary roots at singleton classes and double
Hermite roots at double classes.

## 6. There are enough compatible good triples

Let \(d\) be the total number of double value classes and \(m\) the
total number of distinct value classes.  Since there are \(p+5\)
labels,

\[
                         d+m=p+5.                                \tag{17}
\]

If a distinct-valued triple \(R\) hits \(h\) double classes, those
classes become singletons in \(N\), so \(d_N=d-h\).  In view of
\(k=p-3\), the triple is good exactly when

\[
                         h\ge d-k=8-m.                           \tag{18}
\]

Every class has size at most two and \(p\ge5\), so \(m\ge5\), and the
positive part of \(8-m\) is at most three.  One can choose five distinct
value classes \(a,b,c,d,e\) such that each of

\[
                         \{a,b,c\},\quad
                         \{a,b,d\},\quad
                         \{a,b,e\}                               \tag{19}
\]

is good.  Explicitly: if \(m\ge8\), every triple is good; if \(m=7\),
choose \(a\) double; if \(m=6\), choose both \(a,b\) double.  If
\(m=5\), (17) and \(p\ge5\) force \(p=d=5\), so all five classes are
double and every triple in (19) hits three of them.

For each good triple, (16) has zero residue at the double pole belonging
to \(a\), because the span (10) contains no simple-pole term there.
For \(R=\{a,b,c\}\), logarithmic differentiation gives

\[
 -\sum_{i\notin R}{1\over a+\nu_i}
 = {k+1\over\mu-a}
    +{2\over b-a}+{2\over c-a}.                                 \tag{20}
\]

The sum is over labels, so repetitions carry their actual
multiplicity.  Comparing (20) for the first two triples in (19) still
cancels every repeated common term and gives

\[
 {1\over a+c}-{1\over a+d}
       =2\left({1\over c-a}-{1\over d-a}\right).                \tag{21}
\]

Thus

\[
 (c-a)(d-a)=2(a+c)(a+d),\qquad
 \rho_a(c)\rho_a(d)=2,\qquad
 \rho_a(x)={x-a\over x+a}.                                     \tag{22}
\]

The comparison with the third triple gives
\(\rho_a(c)\rho_a(e)=2\).  If \(a=0\), (22) says \(1=2\).  If
\(a\ne0\), the Möbius map \(\rho_a\) is injective away from its
structurally forbidden pole, so the two relations force \(d=e\).
Both alternatives contradict the choice of five distinct classes.

Therefore the pivots cannot all vanish.  Sections 3 and 4--6 cover all
multiplicity patterns and prove Theorem 1.1.

## 7. Exact audit

[verify_live_three_zero_third_split_collision_beta.py](../computations/verify_live_three_zero_third_split_collision_beta.py)
checks an exact five-square Borchardt quotient with simultaneous row and
column collisions, and the complementary-minor/left-kernel Plücker
duality in Lemma 4.1.  It verifies the elementary-symmetric identities
in Lemma 3.1 and audits every single/double multiplicity profile for
\(5\le p\le16\), including the five-class good-triple boundary and the
exact Vandermonde rank in (14).

It also checks the repeated-multiset residue subtraction (21) and its
equivalence to the Möbius obstruction (22).
