# The fourth split layer is uniformly injective

## 1. Outcome

Continue from the first \(t=r+5\) case in
[live-three-zero-all-exceptional-eleven-live.md](live-three-zero-all-exceptional-eleven-live.md).
Put

\[
              t=r+5,\qquad p=r-1,\qquad k=r-5=p-4.              \tag{1}
\]

There are \(p+6\) exceptional live labels and \(k+1\) active star
sites, including the two type-\(10\) centres.

**Theorem 1.1 (fourth split layer).**  For every \(r\ge6\), on every
structurally admissible beta-multiplicity stratum, the vanishing cyclic
response forces every residual nonzero-to-\(z_0\) block to vanish.
Consequently \(z_0\) is isolated in \(G_3(q)\), a contradiction.

The proof is exact on collision strata.  It combines double-confluent
Borchardt quotients, complementary-minor Plücker support, primal and
dual rational degree bounds, and residue comparisons.  No collision
case is inferred by density.

Together with the preceding layers, this closes every no-extra-singular
stratum with

\[
                              0\le t\le r+5.                     \tag{2}
\]

## 2. Singleton-active pivots

Fix four exceptional labels \(R\), put

\[
                         N=E\setminus R,\qquad |N|=p+2,          \tag{3}
\]

choose a marked pair \(B\subset N\), and let
\(L=N\setminus B\), so \(|L|=p\).  Give \(B\) colour \(2\), give
\(L\) and one target active site colour \(0\), and give \(R\) and the
other \(k\) active sites colour \(1\).

Let \({\cal C}_{L\mid R}\) be the \(p\times p\) Cauchy matrix whose rows
are \(\{\nu_\ell:\ell\in L\}\) and whose columns are

\[
                         \{\nu_c:c\in R\}\sqcup\{\mu^{[k]}\}.    \tag{4}
\]

The exact isolated-star pivot is

\[
                         C_{L\mid R}
                           =2h_{01}^{\,p}
                              \operatorname {per}{\cal C}_{L\mid R}. \tag{5}
\]

Equivalently, with

\[
 a_\ell={1\over\nu_\ell+\mu},\qquad
 H_{\ell c}={\nu_\ell+\mu\over\nu_\ell+\nu_c},
\]

one has

\[
 C_{L\mid R}
 =2h_{01}^{\,p}k!
  \left(\prod_{\ell\in L}a_\ell\right)
  \sum_{\substack{J\subset L\\|J|=4}}
      \operatorname {per}H[J,R].                               \tag{6}
\]

All prefactors are structurally nonzero.  Binary colour swapping gives
row one, and the row-two cleanup is identical to the preceding split
layers.  Thus any one nonzero pivot kills all three rows at every active
site.  Suppose henceforth that every pivot (5) vanishes.

## 3. The uniform double-confluent framework

For a fixed possibly repeated-value \(R\), group its distinct values
\(y\) with multiplicities \(r_y\).  The \(k\) common columns form one
\(\mu\)-class.  If a row value \(x\) has multiplicity \(q_x\), use the
divided mixed jets

\[
 {1\over s!\,j!}
 \partial_x^s\partial_y^j{1\over x+y},
 \qquad
 {1\over s!\,j!}
 \partial_x^s\partial_y^j{1\over(x+y)^2}.                       \tag{7}
\]

Simultaneously colliding the row and column variables in Borchardt's
identity gives

\[
 \operatorname {per}{\cal C}_{L\mid R}
          ={\det{\cal A}^{H}_L\over\det{\cal E}^{H}_L}.          \tag{8}
\]

The double-confluent Cauchy denominator is nonzero because distinct
classes are internally distinct and every cross sum is structurally
nonzero.

Form the \((p+2)\times p\) global numerator jet matrix
\({\cal A}^{H}_N\).  In each row-value class, designate the highest jet
as its top row.  A marked pair containing one label from each of two
distinct classes deletes exactly those two top rows.  Hence every such
maximal minor vanishes.

**Lemma 3.1 (singleton initial-jet rank).**  If \(N\) has a singleton
value class, then

\[
                         \operatorname {rank}{\cal A}^{H}_N<p.  \tag{9}
\]

Indeed, if the rank were \(p\), its two-dimensional left kernel would
have zero Plücker coordinates on every pair of top rows.  Some nonzero
left-kernel vector would therefore be supported entirely on the
non-top rows.  Interpreting it as a rational function of the column
variable gives

\[
 G(y)=\sum_{\substack{x:q_x\ge2\\0\le s\le q_x-2}}
       z_{x,s}{1\over s!}\partial_x^s{1\over(x+y)^2}.            \tag{10}
\]

The column-jet equations give \(p\) zeros counting multiplicity.  If
\(q_{\rm rep}\) labels of \(N\) lie in repeated classes, a common
denominator for (10) has degree \(q_{\rm rep}\), and the nonzero
numerator has degree at most \(q_{\rm rep}-2\).  A singleton in the
\((p+2)\)-label set \(N\) gives

\[
                    q_{\rm rep}\le p+1,\qquad
                    \deg\operatorname {num}G\le p-1,            \tag{11}
\]

contradicting the \(p\) zeros.

When (9) holds, a nonzero column dependence gives a rational function
\(F_R(x)\) with \(p+2\) row-jet zeros.  If \(m_R\) distinct exceptional
values occur in \(R\), its denominator has degree

\[
 \sum_y(r_y+1)+(k+1)
     =4+m_R+p-3=p+m_R+1,                                       \tag{12}
\]

and its nonzero numerator has degree at most

\[
                              p+m_R-1.                           \tag{13}
\]

In particular, if \(m_R\le2\), (13) is at most \(p+1\), impossible
for the \(p+2\) Hermite roots.

## 4. Collision strata with a short two-class split

### 4.1 Multiplicity at least four

If a value \(a\) occurs at least four times, choose four such labels for
\(R\).  The four columns in (6) are identical.  With

\[
                            h_i={\nu_i+\mu\over\nu_i+a}\ne0,
\]

the normalized pivot becomes

\[
                              4!\,e_4(h_i:i\in L).              \tag{14}
\]

For nonzero \(h_1,\ldots,h_m\), \(m\ge7\), the quantities
\(e_4(h_i:i\notin B)\), \(|B|=2\), cannot all vanish.  If all \(h_i\)
are equal this is immediate.  Otherwise choose \(h_j\ne h_k\);
subtracting the equations for \(\{i,j\}\) and \(\{i,k\}\) forces every
one-deletion \(e_3\) on
\(W=[m]\setminus\{j,k\}\) to vanish.  Summing and using
\[
 \sum_{i\in W}e_q(W\setminus\{i\})=(|W|-q)e_q(W)
\]
then descends successively through \(q=3,2,1\) and forces a nonzero
\(h_i\) to be zero.  Thus some pivot is nonzero.

### 4.2 Multiplicities at most three

Assume for now that the multiset is neither all distinct, all double,
nor one double plus singletons.

If a triple class and another repeated class exist, choose two labels
from each; the triple leaves a singleton in \(N\).  If the triple is
the only repeated class, choose all three of it and one singleton.  If
there is no triple, there are at least two doubles and at least one
singleton; choose both labels from two double classes.

In every case, \(R\) uses at most two value classes and \(N\) contains
a singleton.  Lemma 3.1 and the degree contradiction after (13) apply.
This closes every such multiplicity pattern uniformly in \(p\).

## 5. Exactly one double class

Let \(a\) be the repeated value and choose

\[
                            R=\{a,a,b,c\},                       \tag{15}
\]

where \(b,c\) are singleton values.  The complement \(N\) consists of
\(p+2\) distinct values, so all ordinary maximal minors vanish and the
global matrix has rank below \(p\).  Here \(m_R=3\), and (13) has degree
at most \(p+2\).  The \(p+2\) roots force

\[
                       Q_R(x)=\lambda_RP_R(x),\qquad
                       P_R(x)=\prod_{i\in N}(x-\nu_i).           \tag{16}
\]

The zero residue at the double pole \(-b\) is

\[
 -\sum_{i\in N}{1\over b+\nu_i}
 = {k+1\over\mu-b}+{3\over a-b}+{2\over c-b}.                  \tag{17}
\]

Replace \(c\) by distinct singleton values \(d,e\).  The repeated and
common terms cancel, leaving

\[
 {1\over b+c}-{1\over b+d}
       =2\left({1\over c-b}-{1\over d-b}\right),                \tag{18}
\]

and hence

\[
                 \rho_b(c)\rho_b(d)=2,\qquad
                 \rho_b(x)={x-b\over x+b}.                     \tag{19}
\]

The comparison with \(e\) either says \(1=2\) when \(b=0\), or forces
\(d=e\) by injectivity of \(\rho_b\).  Both are contradictions.  There
are \(p+4\ge9\) singleton classes, so the choices are available.

## 6. The all-double stratum

This stratum can occur only when \(p\) is even.  Let every exceptional
value occur twice, choose two distinct classes \(a,b\), and take both
copies of each for \(R\).  Then \(N\) consists entirely of double
classes.

If \(\operatorname {rank}{\cal A}^{H}_N<p\), the primal function in
(12)--(13) has \(m_R=2\), hence numerator degree at most \(p+1\), but
has \(p+2\) Hermite roots.  Therefore the rank must be \(p\).

The top-pair Plücker vanishing now gives a nonzero left-kernel relation
supported on the non-top rows, which are precisely the ordinary rows,
one for each double class in \(N\).  Thus

\[
                          G_{a,b}(y)
                            =\sum_{x\in N_{\rm cls}}
                              {z_x\over(x+y)^2}                  \tag{20}
\]

is nonzero and vanishes on the column multiset: twice at \(a\), twice
at \(b\), and \(k\) times at \(\mu\).  Its denominator has degree
\(p+2\), its numerator has degree at most \(p\), and it has exactly
\(p\) zeros counting multiplicity.  Consequently

\[
 \operatorname {num}G_{a,b}(y)
       =\lambda_{a,b}(y-a)^2(y-b)^2(y-\mu)^k.                   \tag{21}
\]

The absence of a simple pole at \(-x\), for \(x\in N_{\rm cls}\),
gives

\[
 -{2\over x+a}-{2\over x+b}-{k\over x+\mu}
       =2\sum_{\substack{z\in N_{\rm cls}\\z\ne x}}
              {1\over z-x}.                                    \tag{22}
\]

Choose four distinct value classes \(a,b,c,x\).  Compare (22) for the
two choices \(R=\{a,a,b,b\}\) and \(R=\{a,a,c,c\}\), retaining the pole
\(-x\).  Every common term cancels, leaving

\[
 0=-{2\over x+b}+{2\over x+c}
       -{2\over c-x}+{2\over b-x}
   ={-4x(b-c)(b+c)\over
      (x-b)(x+b)(x-c)(x+c)}.                                   \tag{23}
\]

All factors in the final numerator are nonzero: \(x\ne0\) because its
class is doubled, \(b\ne c\), and \(b+c\ne0\) structurally.  This is a
contradiction.  Since there are at least six double classes, the four
choices are available.

## 7. The all-distinct stratum

Let all exceptional values be distinct and fix a four-set \(R\).  Every
maximal minor of the \((p+2)\times p\) numerator evaluation matrix
vanishes.  Its columns are dependent, producing

\[
 D_R(x)=(x+\mu)^{k+1}\prod_{c\in R}(x+\nu_c)^2,\qquad
 \deg D_R=p+5.                                                  \tag{24}
\]

The numerator has degree at most \(p+3\) and the \(p+2\) roots in \(N\),
so

\[
                    Q_R(x)=P_R(x)\ell_R(x),\qquad
                    \deg\ell_R\le1,\quad \ell_R\ne0.            \tag{25}
\]

Fix three values \(a,b,c\), set \(R_x=\{a,b,c,x\}\), and write

\[
 A_a=-\sum_{i\ne a}{1\over a+\nu_i}-{k+1\over\mu-a},\qquad
 \psi(a,x)={1\over a+x}-{2\over x-a}
           =-{x+3a\over x^2-a^2}.                              \tag{26}
\]

Absorb the two fixed-core contributions into \(U_a\), so that
\(Y_a(x)=U_a+\psi(a,x)\).  If
\(\ell_{R_x}(z)=u_xz+v_x\), the zero-residue equations at \(-a\) and
\(-b\) have a common nonzero solution only if

\[
                         Y_b(x)-Y_a(x)
                           +(b-a)Y_a(x)Y_b(x)=0.                 \tag{27}
\]

Clearing \((x^2-a^2)(x^2-b^2)\) gives a polynomial of degree at most
four.  It vanishes at all \(p+3\ge8\) exceptional values outside the
fixed core and hence would be identically zero.

Writing \(U=U_a,V=U_b\), its \(x^3,x^4\) coefficients are

\[
                    (a-b)(U+V),\qquad UV(b-a)-U+V.              \tag{28}
\]

They force \(V=-U\), followed by \(U=0\) or
\(U=-2/(b-a)\).  The resulting polynomials are respectively

\[
 2(a-b)\bigl(x^2-(a+b)x-3ab\bigr),\qquad
 -4(a-b)\bigl(x^2+(a+b)x+3ab\bigr),                             \tag{29}
\]

neither of which is zero.  This contradiction closes the distinct
stratum and completes Theorem 1.1.

## 8. Scope and the first unclosed layer

No multiplicity pattern remains open at \(t=r+5\).  The next split is

\[
                              t=r+6,\qquad r\ge7.                \tag{30}
\]

Its first instance is \(r=7,t=13\), with all thirteen live sites
exceptional.  The quadratic residual factor on its all-distinct stratum
is treated in
[live-three-zero-fifth-split-distinct-beta.md](live-three-zero-fifth-split-distinct-beta.md).
The collision strata of this next split remain outside the present
theorem.

## 9. Exact audit

[verify_live_three_zero_fourth_split_layer.py](../computations/verify_live_three_zero_fourth_split_layer.py)
checks the repeated-common-column expansion for \(5\le p\le10\), an
exact six-square simultaneous row/column confluent Borchardt quotient,
and the multiplicity-four deletion identities.

It exhausts all \(7199\) integer multiplicity profiles for
\(5\le p\le18\), routing every one into the five cases above and
auditing all primal and dual degree counts.  It also verifies the
one-double Möbius subtraction, the all-double pair-swap identity (23),
and the distinct quartic coefficients (28)--(29).
