# The fifth split collision strata are uniformly injective

## 1. Outcome

Continue from
[live-three-zero-fifth-split-distinct-beta.md](live-three-zero-fifth-split-distinct-beta.md).
Put

\[
             t=r+6,\qquad p=r-1,\qquad k=r-6=p-5.              \tag{1}
\]

There are \(p+7\) exceptional live labels and \(k+1\) active star
sites in the standing residual with no additional nonzero singular sites.
This note treats every stratum on which at least two exceptional beta
values coincide.

**Theorem 1.1 (fifth split, collision strata).**  For every \(r\ge7\),
on every structurally admissible exceptional-beta collision stratum, some
isolated-star pivot is nonzero.  Hence the vanishing cyclic response kills
every residual nonzero-to-\(z_0\) block and isolates \(z_0\) in
\(G_3(q)\).

Together with the distinct-value theorem cited above, this closes the
entire no-extra-singular layer

\[
                              t=r+6.                              \tag{2}
\]

The proof does not pass to a collision divisor by density.  Repeated rows
and columns are treated by simultaneous Hermite confluence.

## 2. Pivots and the Hermite rank reduction

Fix five exceptional labels \(R\), let

\[
                         N=E\setminus R,\qquad |N|=p+2,          \tag{3}
\]

and delete a marked pair \(B\subset N\), leaving
\(L=N\setminus B\) of size \(p\).  The isolated-star pivot is

\[
 C_{L\mid R}=2h_{01}^{\,p}\operatorname {per}{\cal C}_{L\mid R}, \tag{4}
\]

where the \(p\times p\) Cauchy matrix has row parameters from \(L\) and
column parameters consisting of the five labels in \(R\) and \(k\) copies
of the common value \(\mu\).  Equivalently,

\[
 C_{L\mid R}=2h_{01}^{\,p}k!
 \left(\prod_{i\in L}{1\over\nu_i+\mu}\right)
 \sum_{\substack{J\subset L\\|J|=5}}
 \operatorname {per}
 \left({\nu_i+\mu\over\nu_i+\nu_c}\right)_{i\in J,c\in R}.     \tag{5}
\]

Every prefactor is structurally nonzero.  As in the preceding split
layers, one nonzero pivot kills row zero at every active star site; binary
colour exchange kills row one, and the marked-pair triangular cleanup
kills row two.  Suppose for contradiction that every pivot (4) vanishes.

For a fixed \(R\), let \(r_y\) be the number of its labels in exceptional
value class \(y\), and let \(q_x\) be the number of labels of \(N\) in row
class \(x\).  Use the divided mixed jets

\[
 {1\over s!j!}\partial_x^s\partial_y^j{1\over x+y},\qquad
 {1\over s!j!}\partial_x^s\partial_y^j{1\over(x+y)^2}.          \tag{6}
\]

Simultaneous row and column confluence in Borchardt's identity gives the
permanent as the quotient of the squared-kernel and Cauchy-kernel Hermite
determinants.  The denominator is nonzero: distinct value classes remain
distinct, and every row--column sum is structurally nonzero.  This remains
true when a value class has labels on both sides of the matrix, since then
the relevant sum is \(2x\ne0\).

Form the global \((p+2)\times p\) squared-kernel numerator jet matrix
\({\cal A}^{H}_N\).  In each row class call its highest jet the top row.
Deleting one label from each of two distinct row classes deletes the two
corresponding top rows.  Thus all such maximal minors vanish.

**Lemma 2.1 (singleton row class).**  If \(N\) has a singleton value
class, then

\[
                         \operatorname {rank}{\cal A}^{H}_N<p.  \tag{7}
\]

Indeed, otherwise the left kernel would be two-dimensional.  Vanishing of
all top--top complementary Plücker coordinates makes its projection to
the top rows at most one-dimensional.  A nonzero left-kernel vector is
therefore supported on the non-top rows.  It produces a nonzero rational
function

\[
 G(y)=\sum_{\substack{x:q_x\ge2\\0\le s\le q_x-2}}
 z_{x,s}{1\over s!}\partial_x^s{1\over(x+y)^2}.                 \tag{8}
\]

If \(q_{\rm rep}\) labels of \(N\) lie in repeated classes, the denominator
of (8) has degree \(q_{\rm rep}\) and its numerator has degree at most
\(q_{\rm rep}-2\).  A singleton among the \(p+2\) rows gives
\(q_{\rm rep}\le p+1\), while the column-jet equations give \(p\) zeros
counting multiplicity.  The bound

\[
                         q_{\rm rep}-2\le p-1                  \tag{9}
\]

is impossible.  This proves the lemma.

When Lemma 2.1 applies, a nonzero column dependence gives

\[
 F_R(z)={Q_R(z)\over D_R(z)},\qquad
 D_R(z)=(z+\mu)^{k+1}\prod_y(z+y)^{r_y+1}.                     \tag{10}
\]

Let \(m_R\) be the number of exceptional value classes represented in
\(R\).  Since \(\sum_y r_y=5\),

\[
 \deg D_R=p+m_R+1,\qquad \deg Q_R\le p+m_R-1.                  \tag{11}
\]

The \(p+2\) row jets are Hermite roots of \(Q_R\).  Consequently:

\[
\begin{array}{c|c}
 m_R&\text{consequence}\\ \hline
 m_R\le2&\text{immediate degree contradiction},\\
 m_R=3&Q_R=\lambda_RP_N,\\
 m_R=4&Q_R=P_N\ell_R,\quad\deg\ell_R\le1,
\end{array}                                                     \tag{12}
\]

where \(P_N(z)=\prod_{i\in N}(z-\nu_i)\), with repetitions, and every
displayed residual factor is nonzero.

## 3. A class of multiplicity at least five

Suppose a value \(a\) occurs at least five times and choose five such labels
for \(R\).  Put

\[
                         h_i={\nu_i+\mu\over\nu_i+a}\ne0
                         \qquad(i\in N).                        \tag{13}
\]

The normalized pivot in (5) is

\[
                             5!e_5(h_i:i\in L).                 \tag{14}
\]

Let \(m=|N|=p+2\ge8\).  These deleted-pair elementary symmetric functions
cannot all vanish.  If all \(h_i\) are equal, (14) is a nonzero multiple
of \(\binom p5h^5\).  Otherwise choose \(h_j\ne h_k\).  For every
\(i\notin\{j,k\}\), subtract the equations obtained by deleting
\(\{i,j\}\) and \(\{i,k\}\); this gives

\[
 (h_k-h_j)e_4(h_\ell:\ell\notin\{i,j,k\})=0.                  \tag{15}
\]

On \(W=N\setminus\{j,k\}\), all one-deletion \(e_4\)'s therefore vanish.
The identities

\[
 \sum_{i\in W}e_d(W\setminus\{i\})=(|W|-d)e_d(W),\qquad
 e_d(W)=e_d(W\setminus\{i\})+h_i e_{d-1}(W\setminus\{i\})   \tag{16}
\]

descend through \(d=4,3,2,1\) and finally force \(h_i=0\), a
contradiction.  Thus every profile with maximum multiplicity at least five
is closed.

## 4. The uniform multiplicity census

Assume henceforth that every multiplicity is at most four.

**Lemma 4.1 (two-class split).**  Apart from the following profiles, one
can choose five labels \(R\) in at most two value classes while leaving a
singleton class in \(N\):

1. all values distinct;
2. one triple class and all remaining classes singleton;
3. one triple class and all remaining classes double;
4. every class has multiplicity one or two, with at least one double.

To prove the claim, first suppose a class has multiplicity four.  A double
class supplies the fifth label and leaves a singleton; a second class of
multiplicity three or four can instead be used in a \(3+2\) split, leaving
one label of the four-class; and if all remaining classes are singleton,
the total size \(p+7\ge13\) leaves an untouched singleton.  Now suppose the
maximum is three.  Two triple classes admit a \(3+2\) split.  With exactly
one triple, the presence of both a double and a singleton permits the
\(3+2\) split using the double while leaving the singleton.  The only
failures are therefore a triple with homogeneous singleton or double
remainder.  With no triple, all multiplicities are one or two.

For every profile supplied by Lemma 4.1, Lemma 2.1 applies and \(m_R\le2\),
contradicting the first line of (12).  The all-distinct exception is already
closed by the preceding note.  It remains to treat the last three collision
families explicitly.

## 5. Constant residuals and moving value classes

The following observation handles all residuals with \(m_R=3\).

**Lemma 5.1 (moving-class quadratic).**  Suppose \(R_x\) contains one
fixed anchor label of value \(a\), contains \(j\in\{1,2\}\) labels of a
moving class \(x\), and has a fixed remaining part.  Suppose also that
\(N_x\) has a singleton class and that exactly three exceptional value
classes occur in \(R_x\).  If all pivots vanish, then at most two distinct
values can be used for \(x\).

By (12), \(Q_{R_x}=\lambda_xP_{N_x}\).  At the anchor pole \(-a\), the
column span has a double pole and no simple pole.  The zero-simple-residue
condition is

\[
                              Y_a(x)=0.                          \tag{17}
\]

More explicitly, for any such \(R\),

\[
 Y_a(R)=
 -\sum_{i\in N}{1\over a+\nu_i}
 -{k+1\over\mu-a}
 -\sum_{\substack{y\in R_{\rm cls}\\y\ne a}}
       {r_y+1\over y-a}.
\]

Use the full exceptional multiset as a fixed baseline.  Selecting \(j\)
labels of value \(x\) removes their \(j\) row-logarithmic-derivative terms,
and the corresponding column cluster contributes a pole of order \(j+1\).
Thus all \(x\)-dependence in (17) is

\[
 Y_a(x)=U+\chi_j(a,x),\qquad
 \chi_j(a,x)={j\over a+x}-{j+1\over x-a}
             =-{x+(2j+1)a\over x^2-a^2}.                       \tag{18}
\]

Every denominator is nonzero by distinctness of the value classes and the
structural pair-sum condition.  Clearing it gives

\[
                    U(x^2-a^2)-x-(2j+1)a=0.                    \tag{19}
\]

This is a nonzero polynomial of degree at most two: its coefficient of
\(x\) is \(-1\).  Three distinct moving values are impossible.

## 6. The one-triple homogeneous profiles

Let a value \(\tau\) occur three times, and suppose all other classes have
one common multiplicity \(h\in\{1,2\}\).  Fix one other class \(a\), and
for each further class \(x\) choose

\[
                         R_x=\{\tau,\tau,\tau,a,x\}.             \tag{20}
\]

Only one label is selected from \(a\) and \(x\).  When \(h=1\), untouched
singleton classes remain in \(N_x\); when \(h=2\), the unselected copies of
\(a\) and \(x\) are singleton row classes.  Thus Lemma 2.1 applies,
\(m_{R_x}=3\), and Lemma 5.1 applies with \(j=1\).

There are at least ten remaining classes when \(h=1\), and at least five
when \(h=2\), because the total number of labels is at least thirteen.
After fixing \(a\), at least three choices of \(x\) remain.  Lemma 5.1 is a
contradiction in both cases.

## 7. Profiles made from singles and doubles

Let there be \(d\ge1\) double classes and \(s\) singleton classes, so

\[
                              2d+s=p+7\ge13.                    \tag{21}
\]

### 7.1 At most three double classes

If \(d\le3\), then \(s\ge7\).  Fix a double class \(u\), take both of its
labels, fix two singleton anchors \(a,b\), and let \(x\) range over every
other singleton class:

\[
                         R_x=\{u,u,a,b,x\}.                     \tag{22}
\]

At least one singleton remains in \(N_x\), so Lemma 2.1 applies.  Here
\(m_{R_x}=4\), and (12) gives a nonzero linear residual

\[
                              \ell_x(z)=A_xz+B_x.                \tag{23}
\]

At the two singleton anchor poles, the residue equations are

\[
 \bigl(1-aY_a(x),Y_a(x)\bigr)\binom{A_x}{B_x}=0,
 \qquad
 \bigl(1-bY_b(x),Y_b(x)\bigr)\binom{A_x}{B_x}=0,               \tag{24}
\]

where

\[
             Y_a(x)=U+\chi_1(a,x),\qquad
             Y_b(x)=V+\chi_1(b,x).                              \tag{25}
\]

The vector in (24) is nonzero, so

\[
                  Y_b(x)-Y_a(x)+(b-a)Y_a(x)Y_b(x)=0.            \tag{26}
\]

After multiplication by
\((x^2-a^2)(x^2-b^2)\), the left side is a polynomial of degree at most
four.  There are \(s-2\ge5\) distinct allowed moving values, none a pole;
hence the polynomial would be identically zero.

Its coefficients of \(x^3,x^4\) are respectively

\[
                  (a-b)(U+V),\qquad UV(b-a)-U+V.                \tag{27}
\]

They force \(V=-U\) and then either \(U=0\) or
\(U=-2/(b-a)\).  In the two cases the cleared polynomials reduce to

\[
 2(a-b)\bigl(x^2-(a+b)x-3ab\bigr),\qquad
 -4(a-b)\bigl(x^2+(a+b)x+3ab\bigr),                            \tag{28}
\]

both nonzero because \(a\ne b\).  This contradiction closes
\(1\le d\le3\), including the sole-one-double profile.

### 7.2 Four double classes

Now let \(d=4\).  Equation (21) gives \(s\ge5\).  Fix a singleton anchor
\(a\), take both labels from one fixed double class \(u\), and take both
labels from a moving double class \(x\):

\[
                            R_x=\{a,u,u,x,x\}.                   \tag{29}
\]

There are three possible moving double classes, and untouched singleton
classes remain in \(N_x\).  Lemma 5.1 applies with \(j=2\), contradicting
those three choices.

### 7.3 At least five double classes

Finally let \(d\ge5\).  Choose distinct double classes \(a,u\), put one
label of \(a\) and both labels of \(u\) in \(R\), and again put both labels
of a moving double class \(x\) in \(R\):

\[
                            R_x=\{a,u,u,x,x\}.                   \tag{30}
\]

The unused copy of \(a\) is a singleton row class of \(N_x\).  There are
\(d-2\ge3\) possible moving classes \(x\).  Lemma 5.1 with \(j=2\) again
gives a contradiction.  This includes the all-double profile and the
all-double-plus-one-singleton boundary; no dual full-rank branch remains.

## 8. Completion and exact audit

Sections 3--7 exhaust every collision partition.  Therefore some pivot
(4) is nonzero.  The inherited singleton-active cleanup kills all three
rows of every common-beta live and type-`10` star, while exceptional stars
already vanish from

\[
                         (\nu_i-\mu)q_{i z_0}=0.                 \tag{31}
\]

Repeating for every coordinate at \(z_0\), and using the standing facts
that zero--zero blocks vanish and the removed type-`22` ports are singular,
isolates \(z_0\) in \(G_3(q)\).  This proves Theorem 1.1.

[verify_live_three_zero_fifth_split_collision_beta.py](../computations/verify_live_three_zero_fifth_split_collision_beta.py)
checks the repeated-common-column expansion, an exact simultaneous
row/column confluent Borchardt quotient in which one value occurs on both
shores, the complete deleted-\(e_5\) descent, and all primal and singleton-
dual degree counts.  It enumerates 35,199 multiplicity profiles for
\(6\le p\le24\) and routes every profile into exactly the cases above.  It
also proves the one- and two-label moving-class quadratics and the
few-double quartic obstruction symbolically.
