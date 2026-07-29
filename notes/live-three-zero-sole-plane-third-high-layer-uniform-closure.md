# The third-high sole-plane layer \(t=r+5\) is injective

## 1. Outcome

Continue from the first point of this layer in
[live-three-zero-sole-plane-third-high-first-point-closure.md](live-three-zero-sole-plane-third-high-first-point-closure.md).
There is one extra singular site of eligible type \(M_e=\{2\}\), the live
shore has size \(2r\), and

\[
                         r\ge5,\qquad t=r+5.                    \tag{1}
\]

**Theorem 1.1 (uniform third-high-layer closure).**  For every \(r\ge5\),
every structurally admissible exceptional-beta multiset, every source-side
row plane at \(e\), and every direct \(B_{01}\) scale, the complete residual
response at the shared zero is injective.  Arbitrary beta repetitions and a
singleton beta value zero are allowed.  Hence the entire sole-plane layer
in (1) is impossible.

The proof for \(r\ge6\) is uniform.  Four equal special columns give an
elementary deletion descent.  Otherwise a one-deletion Hermite lemma turns
every four-special permanent into a rational relation whose residual degree
is the number of selected value classes minus two.  Collision profiles then
fail an affine Robin triangle compatibility, while the all-distinct profile
fails the universal quadratic Robin sextic from the preceding point.  The
case \(r=5\) is already closed in the cited note.

Consequently the exact remaining sole-plane frontier is

\[
                  r\ge7,\qquad r+6\le t\le2r,                  \tag{2}
\]

whose first point is \((r,t)=(7,13)\).

## 2. The uniform \(P_r/S_r\) response

Normalize the common beta value to \(1\), and put

\[
 H=\begin{pmatrix}0&1&1\\1&0&1\\1&1&0\end{pmatrix},\qquad
 P_i=I\ (i\text{ live}),\qquad
 P_c=P_d=D=\operatorname {diag}(1,1,0).                         \tag{3}
\]

Let \(E\) be the exceptional live set.  Under (1),

\[
                         |E|=r+5.                               \tag{4}
\]

There are \(r-5\) common-beta live sites.  Together with the two type-
\(10\) centres put

\[
 A=(U\setminus E)\sqcup\{c,d\},\qquad |A|=r-3.                \tag{5}
\]

The active response sites are \(A\sqcup\{e\}\).  For equal-length tuples,
write

\[
 \mathcal C_r(X\mid Y)
   =\operatorname {per}\left({1\over x_i+y_j}\right)_{i,j=1}^r. \tag{6}
\]

The noncoordinate pivot family is

\[
\begin{aligned}
 &m\in E,\qquad E\setminus\{m\}=L\sqcup R,\qquad
 |L|=r,\quad |R|=4,\\
 &P_{m;L\mid R}
   =\mathcal C_r\bigl(\nu_L\mid(1^{[r-4]},\nu_R)\bigr).       \tag{7}
\end{aligned}
\]

The coordinate and extra-block family is

\[
\begin{aligned}
 &B\subset E,\quad |B|=2,\qquad E\setminus B=L\sqcup R,
 \qquad |L|=r,\quad |R|=3,\\
 &S_{B;L\mid R}
   =\mathcal C_r\bigl(\nu_L\mid(1^{[r-3]},\nu_R)\bigr).       \tag{8}
\end{aligned}
\]

The \(S_r\) family is inherited from the already closed layer \(t=r+4\).
Indeed, omit any label \(q\in E\).  On the \((r+4)\)-label set
\(E'=E\setminus\{q\}\), the preceding theorem supplies a nonzero
three-special \(P_r\) pivot with marked label \(m\).  Taking
\(B=\{q,m\}\) gives exactly the same permanent in (8).  Therefore

\[
                         \boxed{\text{some }S_{B;L\mid R}\ne0}. \tag{9}
\]

It remains to prove the analogous statement for (7).

## 3. The one-deletion Hermite lemma

Fix a four-label set \(R\), put

\[
                         N=E\setminus R,\qquad |N|=r+1,        \tag{10}
\]

and suppose every one-label deletion in (7) vanishes.  Group the values in
\(R\) into distinct classes \(y\), of multiplicities \(r_y\), and group
the row labels in \(N\) into classes \(x\), of multiplicities \(q_x\).
Use the divided mixed jets

\[
 {1\over s!j!}\partial_x^s\partial_y^j{1\over x+y},\qquad
 {1\over s!j!}\partial_x^s\partial_y^j{1\over(x+y)^2}.        \tag{11}
\]

Simultaneous row and column confluence in Borchardt's identity expresses
every permanent as the quotient of the corresponding squared-Cauchy and
Cauchy Hermite determinants.  The denominator is nonzero: different beta
classes are distinct, every opposite sum is structurally nonzero, and a
class occurring on both shores has self-sum \(2x\ne0\).

Form the global \((r+1)\)-by-\(r\) squared-Cauchy numerator jet matrix
\({\cal A}_N^H\).  In each row class call its highest jet the top row.
Deleting one labelled row before confluence deletes precisely the top row
of its class.  Hence every maximal minor obtained by deleting a top row
vanishes.

**Lemma 3.1 (one-deletion initial-jet rank).**

\[
                         \operatorname {rank}{\cal A}_N^H<r.   \tag{12}
\]

If the rank were \(r\), its left kernel would be one-dimensional.  The
vanishing top-row complementary minors would force its generator to be
supported entirely on non-top rows.  It would give a nonzero rational
function

\[
 G(y)=\sum_{\substack{x:q_x\ge2\\0\le s\le q_x-2}}
 z_{x,s}{1\over s!}\partial_x^s{1\over(x+y)^2}.                \tag{13}
\]

Let \(q_{\rm rep}\) be the number of labels of \(N\) in repeated classes.
A common denominator of (13) has degree \(q_{\rm rep}\), so its numerator
has degree at most \(q_{\rm rep}-2\le r-1\).  The \(r\) column-jet
equations say that it has \(r\) zeros counting multiplicity, away from its
poles.  Thus \(G=0\), and uniqueness of partial fractions forces every
\(z_{x,s}=0\), a contradiction.  This proves (12).  Notice that no
singleton row class is needed; the saving comes from having only one
deleted label.

Let \(m_R\) be the number of distinct exceptional values represented in
\(R\).  A nonzero column dependence supplied by (12) is

\[
 F_R(z)={Q_R(z)\over D_R(z)},\qquad
 D_R(z)=(z+1)^{r-3}\prod_y(z+y)^{r_y+1}.                       \tag{14}
\]

The denominator and numerator degrees satisfy

\[
 \deg D_R=r+m_R+1,\qquad \deg Q_R\le r+m_R-1.                 \tag{15}
\]

All \(r+1\) row jets are Hermite roots of \(Q_R\).  With

\[
                         P_N(z)=\prod_{i\in N}(z-\nu_i),       \tag{16}
\]

the residual factor has degree at most \(m_R-2\).  In particular,

\[
\begin{array}{c|c}
m_R&\text{consequence}\\ \hline
1&\text{immediate degree contradiction},\\
2&Q_R=\lambda_RP_N,\\
3&Q_R=P_N\ell_R,\quad\deg\ell_R\le1,\\
4&Q_R=P_NH_R,\quad\deg H_R\le2.
\end{array}                                                     \tag{17}
\]

Every displayed residual is nonzero, because principal parts at distinct
poles are linearly independent.

## 4. A class of multiplicity at least four

Suppose \(a\) occurs at least four times and use four copies in \(R\).  Put

\[
                         h_i={\nu_i+a\over\nu_i+1}\ne0.        \tag{18}
\]

Expansion along the four equal columns gives, with \(j=r-4\),

\[
 P_{m;L\mid R}
 =4!j!\left(\prod_{i\in L}{1\over\nu_i+a}\right)
                         e_j(h_i:i\in L).                      \tag{19}
\]

Suppose all \(r+1\) one-deletion values vanished.  On the set \(N\),

\[
 \sum_{m\in N}e_j(N\setminus\{m\})=(|N|-j)e_j(N)=5e_j(N),   \tag{20}
\]

so \(e_j(N)=0\).  The identity

\[
 e_j(N)=e_j(N\setminus\{m\})+h_m e_{j-1}(N\setminus\{m\})  \tag{21}
\]

and \(h_m\ne0\) make every one-deletion \(e_{j-1}\) vanish.  Repeating
(20)--(21) descends to the impossible equation \(e_0=0\).  Thus every
profile with maximum multiplicity at least four is closed uniformly.

## 5. Affine Robin compatibility

Assume henceforth that every multiplicity is at most three and that some
value \(u\) repeats.  Select two copies of \(u\) and one label from each of
two other value classes \(b,c\):

\[
                         R=\{u,u,b,c\}.                         \tag{22}
\]

Here \(m_R=3\), so (17) supplies a nonzero affine factor \(\ell_{bc}\).
At the selected simple pole \(-b\), the missing simple principal part is
the undivided Robin equation

\[
 \ell_{bc}'(-b)=Y_b(c)\ell_{bc}(-b),\qquad
 Y_b(c)=A_b+{c+3b\over c^2-b^2},                              \tag{23}
\]

where \(A_b\) is independent of \(c\).  This equation also covers the
boundary \(\ell_{bc}(-b)=0\): it would then force the affine polynomial and
its derivative to vanish, contrary to \(\ell_{bc}\ne0\).  The analogous
equation holds at \(-c\).

Eliminating the two coefficients of \(\ell_{bc}\) gives

\[
                  Y_b(c)-Y_c(b)+(c-b)Y_b(c)Y_c(b)=0.           \tag{24}
\]

After clearing its structural denominators, (24) is

\[
 K_{bc}:=A_bA_c(b-c)(b+c)^2+2A_b c(b+c)
          -2A_c b(b+c)+(b-c)=0.                               \tag{25}
\]

For three distinct candidate values \(a,b,c\), eliminate \(A_b,A_c\)
from \(K_{ab},K_{ac},K_{bc}\).  The exact undivided resultant is

\[
 -(a-b)(a-c)(b-c)
 \bigl[A_a(a^2+a(b+c)+bc)-(2a+b+c)\bigr]^2.                  \tag{26}
\]

Thus every candidate triangle obeys

\[
                         A_a(a+b)(a+c)=2a+b+c.                 \tag{27}
\]

If there are four distinct candidate classes \(a,b,c,d\) besides \(u\),
subtract (27) for \((a,b,c)\) and \((a,b,d)\).  Since \(c\ne d\),

\[
                         A_a(a+b)=1.                           \tag{28}
\]

Substitution in the first equation gives \(a+b=0\), contradicting the
structural pair-sum condition.  Therefore every collision profile having
at least five value classes is closed.

## 6. Exactly four value classes

For \(r\ge6\), four classes of multiplicity at most three contain at most
ten labels if one class is a singleton.  Since \(|E|=r+5\ge11\), every
one of the four classes is repeated.  Denote their distinct values by
\(a,b,c,d\).

Fix the anchor value \(b\).  When two copies of a selected value \(u\) are
used in (22), a direct logarithmic-derivative calculation in (23) gives

\[
 A_b^{(u)}=C_b+{3\over u-b}-{2\over u+b},\qquad
 C_b=\sum_{i\in E}{1\over b+\nu_i}
       +{r-3\over1-b}-{1\over2b}.                             \tag{29}
\]

Here \(b\ne0\), because its class repeats.  For \(u=a\), the remaining
candidate triangle is \(\{b,c,d\}\); equation (27) says

\[
 C_b={2b+c+d\over(b+c)(b+d)}-{3\over a-b}+{2\over a+b}.       \tag{30}
\]

The choices \(u=c\) and \(u=d\) give the two analogous expressions.
Equating the \(u=a,c\) expressions and clearing only structural factors
gives

\[
                         2ab+ac+b^2+2bc=0.                    \tag{31}
\]

Equating the \(u=a,d\) expressions gives

\[
                         2ab+ad+b^2+2bd=0.                    \tag{32}
\]

Subtracting yields \((c-d)(a+2b)=0\), hence \(a=-2b\).  Equation (31)
then reduces to \(-3b^2=0\), contradicting \(b\ne0\).  Thus the four-
class boundary is also impossible.

This identifies exactly what was special at \(r=5\).  With ten labels the
profile \(3^3 1\) has four classes but one may be the allowed singleton
zero, so the last contradiction need not apply.  The fixed-special
deletion argument in the preceding \((5,10)\) note closes precisely that
finite boundary.  Every other branch above is already uniform.

## 7. The all-distinct quadratic

It remains to suppose all exceptional values are distinct.  Fix three
values \(a,b,c\), let \(d\) vary, and take

\[
                         R_d=\{a,b,c,d\}.                      \tag{33}
\]

The last line of (17) gives \(Q_d=P_NH_d\), \(\deg H_d\le2\).  At each
fixed selected pole \(-y\), \(y\in\{a,b,c\}\), the undivided residue
condition is

\[
 H_d'(-y)+Z_y(d)H_d(-y)=0,\qquad
 Z_y(d)=A_y-{d+3y\over d^2-y^2}.                              \tag{34}
\]

For \(H=h_0+h_1x+h_2x^2\), the corresponding row is

\[
                  \bigl(Z_y,\ 1-yZ_y,\ -2y+y^2Z_y\bigr).      \tag{35}
\]

After clearing
\((d^2-a^2)(d^2-b^2)(d^2-c^2)\), the determinant of the three rows is a
polynomial of degree at most six in \(d\).  It is never identically zero on
the structural locus.  If \(F_0,\ldots,F_6\) are its coefficients and

\[
 \Delta=\prod_{y\in\{a,b,c\}}(y-1)(y+1)
          (a-b)(a+b)(a-c)(a+c)(b-c)(b+c),                     \tag{36}
\]

the universal exact certificate is

\[
               \langle F_0,\ldots,F_6,1-s\Delta\rangle
                              =\langle1\rangle                 \tag{37}
\]

over \(\mathbb Q[a,b,c,A_a,A_b,A_c,s]\).  This is the same universal
lemma audited at \((5,10)\); the checker reruns it rather than merely citing
the earlier output.

There are \(|E|-3=r+2\ge7\) allowed, distinct values of \(d\), none at a
cleared pole.  They cannot all be roots of a nonzero sextic.  The all-
distinct profile is impossible, completing the proof that some pivot (7)
is nonzero.

## 8. Literal response and row-plane cover

Suppose first that the row plane at \(e\) is noncoordinate and choose
\(p=(p_0,p_1,p_2)\) in it with \(p_2\ne0\).  Give \(m\) colour two,
contract \(e\) to \(p\), and use source \(22\).  For a target \(v\in A\),
put \(v\sqcup L\) on one binary shore and
\((A\setminus\{v\})\sqcup R\) on the other.  Removing the target leaves
two shores of size \(r\), whereas every off-target star is unbalanced.
Thus a nonzero (7) gives

\[
                         2p_2P_{m;L\mid R}Z_{v,j}=0            \tag{38}
\]

for both binary rows.  At \(c,d\), replacing the target by its zero local
third row kills the third row literally.

Choose a nonzero (8), give \(B\) colour two, put \(L\) on one binary shore
and \(A\sqcup R\) on the other, and contract \(e\) by an arbitrary output
covector.  The star at \(e\) has coefficient \(2S_{B;L\mid R}\); all
contamination lands in binary rows of \(A\) already killed by (38).  This
kills the complete extra block.  Finally replace each common-beta live
target by its genuine third row in (38).  The target coefficient remains
unchanged, and every additional marked-pair term is triangular into an
already-vanishing active column.

If the row plane is coordinate, put \(P_e=D\).  The active set
\(A\sqcup\{e\}\) has size \(r-2\).  For any target, put the target and
\(L\) on one shore and the other \(r-3\) active sites together with the
three labels of \(R\) on the other.  A nonzero \(S_r\) pivot isolates both
binary target rows.  The zero local third rows at \(c,d,e\) are literal
singletons, and the common-live third rows follow by the same triangular
cleanup.

All selected equations use source \(22\), so the arbitrary direct
\(B_{01}\) scale has coefficient zero.  The standard three-chart cover of
\(\operatorname {Gr}(2,3)\) separates the coordinate plane from the charts
containing a vector with nonzero third coordinate.  Singleton zero beta is
retained throughout.  This proves Theorem 1.1.

## 9. Exact audit

[verify_live_three_zero_sole_plane_third_high_layer_uniform.py](../computations/verify_live_three_zero_sole_plane_third_high_layer_uniform.py)
checks the complete \(r=6\) partition census

\[
                         56=40+1+14+1,                         \tag{39}
\]

routing respectively to the heavy, four-class, at-least-five-class
collision, and all-distinct branches.  It repeats the routing through
\(r=30\), verifies the equal-column permanent and deletion descent, audits
all Hermite degree counts, reconstructs the pair polynomial and the
undivided triangle resultant, and checks the two four-class exchange
factorizations.  It reruns the universal localized unit certificate (37),
checks the \(S_r\) embedding combinatorially, and evaluates the literal
\(r=6\) response with a singleton zero beta, a repeated nonzero beta,
direct scale \(17\), all active sites, and both row-plane regimes.

No finite census is used to infer the theorem: the census tests the routing,
while Sections 3--7 prove each routed family uniformly.
