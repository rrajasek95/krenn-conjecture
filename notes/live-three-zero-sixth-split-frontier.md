# The sixth split: determinant reduction and collision closure

## 1. Status and scope

Continue from
[live-three-zero-fifth-split-collision-beta.md](live-three-zero-fifth-split-collision-beta.md).
Put

\[
             t=r+7,\qquad p=r-1,\qquad k=r-7=p-6.              \tag{1}
\]

There are $p+8$ exceptional live labels, $k+1$ active star sites,
and $p\ge7$.  Fixing six exceptional columns leaves $p+2$ possible
row labels.  This note gives two principal outcomes.

1. On the all-distinct stratum, vanishing of all isolated-star pivots is
   reduced to an explicit four-anchor rational determinant identity of
   degree eight.  The companion note
   [live-three-zero-sixth-split-distinct-closure.md](live-three-zero-sixth-split-distinct-closure.md)
   extracts a linear endpoint certificate from that identity and closes
   the stratum by an invertible five-core Cauchy system.
2. All collision strata are closed.  The proof combines a deleted $e_6$
   descent, short Hermite splits, constant-residual moving classes,
   inherited linear and quadratic moving determinants, and a
   second-derivative argument for the last double/single profile.

The stronger pointwise determinant-rigidity implication DR4 stated in
Section 5 is not needed and is not claimed here.  Its weaker linear
consequence is proved exactly in the companion note.  Together with the
collision result below, this closes the entire sixth-split layer.

## 2. The sixth isolated-star pivot

Let $E$ be the exceptional multiset, choose six labels $R\subset E$, put

\[
                         N=E\setminus R,\qquad |N|=p+2,         \tag{2}
\]

and delete a marked pair $B\subset N$.  With $L=N\setminus B$, the
isolated-star pivot is

\[
 C_{L\mid R}=2h_{01}^{\,p}\operatorname {per}{\cal C}_{L\mid R}, \tag{3}
\]

where the $p\times p$ Cauchy matrix has row parameters from $L$ and
column parameters consisting of the six labels in $R$ and $k$ copies
of the common value $\mu$.  Equivalently,

\[
 C_{L\mid R}=2h_{01}^{\,p}k!
 \left(\prod_{i\in L}{1\over\nu_i+\mu}\right)
 \sum_{\substack{J\subset L\\|J|=6}}
 \operatorname {per}
 \left({\nu_i+\mu\over\nu_i+\nu_c}\right)_{i\in J,c\in R}.     \tag{4}
\]

Every prefactor is structurally nonzero.  As in the preceding split
layers, one nonzero pivot completes the row-zero cleanup at all active
stars; binary colour exchange gives row one and the marked-pair
triangular cleanup gives row two.  Thus it is enough to contradict the
assumption that every pivot (3) vanishes.

## 3. Hermite rank and degree bookkeeping

For a possibly repeated-value $R$, let $r_y$ be the number of its labels
in value class $y$, and let $q_x$ be the number of labels of $N$ in row
class $x$.  Simultaneously confluence rows and columns using the divided
mixed jets

\[
 {1\over s!j!}\partial_x^s\partial_y^j{1\over x+y},\qquad
 {1\over s!j!}\partial_x^s\partial_y^j{1\over(x+y)^2}.         \tag{5}
\]

The confluent Cauchy determinant is nonzero: distinct value classes
remain distinct, every row--column sum is structurally nonzero, and a
class occurring on both shores contributes $2x\ne0$.

The singleton-row-class lemma from the fourth and fifth splits applies
without change.  If $N$ has a singleton value class, all top--top
complementary maximal minors vanish, and the global $(p+2)\times p$
squared-kernel jet matrix has rank below $p$.  A nonzero column
dependence gives

\[
 F_R(z)={Q_R(z)\over D_R(z)},\qquad
 D_R(z)=(z+\mu)^{k+1}\prod_y(z+y)^{r_y+1}.                    \tag{6}
\]

If $m_R$ distinct exceptional values occur in $R$, then

\[
 \deg D_R=(k+1)+6+m_R=p+m_R+1,\qquad
 \deg Q_R\le p+m_R-1.                                        \tag{7}
\]

The $p+2$ row jets are Hermite roots of $Q_R$.  In particular,

\[
                   m_R\le2\quad\Longrightarrow\quad
                   \deg Q_R\le p+1<p+2,                       \tag{8}
\]

which is an immediate contradiction.

## 4. The all-distinct cubic residual

Assume all exceptional beta values are distinct.  For a fixed six-set
$R$, every maximal minor of the global numerator evaluation matrix
vanishes.  Its columns are dependent, and

\[
 D_R(z)=(z+\mu)^{k+1}\prod_{c\in R}(z+\nu_c)^2,\qquad
 \deg D_R=p+7.                                                \tag{9}
\]

The nonzero numerator has degree at most $p+5$ and vanishes at the
$p+2$ distinct values in $N$.  Hence

\[
 Q_R(z)=P_N(z)q_R(z),\qquad
 0\ne q_R,\qquad \deg q_R\le3.                               \tag{10}
\]

At an anchor $a\in R$, absence of a simple pole at $-a$ gives

\[
                    q_R'(-a)+Y_a(R)q_R(-a)=0,                 \tag{11}
\]

where

\[
 \begin{split}
 A_a&=-\sum_{i\in E\setminus\{a\}}{1\over a+\nu_i}
       -{k+1\over\mu-a},\\
 \psi(a,x)&={1\over a+x}-{2\over x-a}
            =-{x+3a\over x^2-a^2},\\
 Y_a(R)&=A_a+\sum_{c\in R\setminus\{a\}}\psi(a,c).
 \end{split}                                                  \tag{12}
\]

No denominator in (12) vanishes on the structurally admissible
all-distinct stratum.

## 5. The exact four-anchor frontier

Choose five distinct nonzero exceptional values

\[
                            C=\{a,b,c,d,e\},                   \tag{13}
\]

and let $x$ range over $E\setminus C$.  Put $R_x=C\cup\{x\}$.
For $s\in C$, absorb the fixed core into

\[
 U_s(C)=A_s+\sum_{v\in C\setminus\{s\}}\psi(s,v),\qquad
 Y_s(x)=U_s(C)+\psi(s,x).                                     \tag{14}
\]

Write a cubic as $q(z)=u z^3+v z^2+wz+h$.  Its residue row at
anchor $s$ is

\[
 \bigl(3s^2-s^3Y_s(x),\ -2s+s^2Y_s(x),\
       1-sY_s(x),\ Y_s(x)\bigr).                              \tag{15}
\]

For any four anchors $s_1,s_2,s_3,s_4\in C$, the determinant of the
four rows (15) vanishes at every allowed exceptional value $x\notin C$,
because the nonzero cubic (10) lies in their common kernel.  Multiplying
row $i$ by $x^2-s_i^2$ gives the polynomial row

\[
 (x^2-s_i^2)D_{s_i}
 +\bigl(U_{s_i}(x^2-s_i^2)-(x+3s_i)\bigr)E_{s_i},              \tag{16}
\]

where $D_s$ and $E_s$ are derivative and evaluation at $-s$.  The
cleared determinant has degree at most eight.  It has

\[
                         |E|-5=p+3\ge10                       \tag{17}
\]

distinct roots, none a pole, and is therefore the zero polynomial.

This leaves the following purely algebraic statement.

**Determinant-rigidity problem DR4.**  Let $s_1,\ldots,s_4$ be distinct
nonzero complex numbers with $s_i+s_j\ne0$.  If the determinant of the
four rows (16) is identically zero in $x$, must

\[
                              U_{s_1}=\cdots=U_{s_4}=0?         \tag{18}
\]

For $U_{s_i}=0$, the identity is explained by the explicit kernel

\[
                         g_x(z)=(z-x)(z+x)^2,                  \tag{19}
\]

because

\[
 {g_x'(-s)\over g_x(-s)}=-\psi(s,x).                          \tag{20}
\]

Exact rational Groebner computations for many admissible anchor
quadruples, and exhaustive finite-field computations, find no other
translation vector $U$.  These checks are evidence only: they do not
replace a symbolic complex proof of DR4.

## 6. Why full DR4 is unnecessary

If DR4 is proved, apply it to the five four-subsets of $C$.  Equation
(18) then gives $U_s(C)=0$ for every $s\in C$.  Fix a nonzero anchor
$a$, hold three companion values fixed, and vary the fourth companion
$y$.  Comparing the resulting equations $U_a(C)=0$ forces

\[
                              \psi(a,y)=\text{constant}.       \tag{21}
\]

There are more than three eligible moving values.  But a fibre of
$y\mapsto\psi(a,y)$ has size at most two, since

\[
 \psi(a,c)-\psi(a,d)
 ={(c-d)\bigl(a^2+3a(c+d)+cd\bigr)\over
   (a^2-c^2)(a^2-d^2)},                                      \tag{22}
\]

or, equivalently, $\psi(a,y)=\lambda$ is the nonzero quadratic

\[
                         \lambda(y^2-a^2)+y+3a=0.              \tag{23}
\]

Thus DR4 would close the entire all-distinct sixth-split stratum.  The
companion closure does not prove (18): instead it derives one exact linear
relation from each four-anchor determinant, assembles the five relations
on a five-core into a hollow Cauchy system, and proves that sufficiently
many such cores are invertible.  This already forces the repeated fibre
contradiction (23), so DR4 is no longer a proof obligation.

## 7. A class of multiplicity at least six

Suppose a value $a$ occurs at least six times and choose six such labels
for $R$.  Put

\[
                         h_i={\nu_i+\mu\over\nu_i+a}\ne0
                         \qquad(i\in N).                       \tag{24}
\]

The normalized pivot (4) is

\[
                              6!e_6(h_i:i\in L).               \tag{25}
\]

Let $m=|N|=p+2\ge9$.  The deleted-pair values in (25) cannot all
vanish.  If all $h_i$ are equal, this follows from
$\binom{m-2}{6}h^6\ne0$.  Otherwise choose $h_j\ne h_k$.
Subtracting the equations obtained by deleting $\{i,j\}$ and
$\{i,k\}$ gives

\[
 (h_k-h_j)e_5(h_\ell:\ell\notin\{i,j,k\})=0                  \tag{26}
\]

for every $i\notin\{j,k\}$.  On $W=N\setminus\{j,k\}$, all
one-deletion $e_5$'s vanish.  The identities

\[
 \sum_{i\in W}e_d(W\setminus\{i\})=(|W|-d)e_d(W),\qquad
 e_d(W)=e_d(W\setminus\{i\})+h_i e_{d-1}(W\setminus\{i\})     \tag{27}
\]

descend through $d=5,4,3,2,1$ and force $h_i=0$, a contradiction.
Hence some pivot is nonzero, closing every profile of maximum
multiplicity at least six.

## 8. The two-class singleton sector

Suppose one can select six labels $R$ from at most two exceptional
value classes while leaving at least one singleton value class in
$N=E\setminus R$.  The simultaneous-Hermite singleton lemma applies,
and $m_R\le2$.  Equation (8) is impossible, closing the profile without
further residue analysis.

This criterion is deliberately a checkable selection property, not a
claim that it exhausts the remaining collision partitions.  For
orientation, among the integer partitions of $p+8$, the exact counts are

\[
\begin{array}{c|rrrrrr}
p&7&8&9&10&11&12\\ \hline
\text{all profiles}&176&231&297&385&490&627\\
\max\ge6&92&130&178&244&326&435\\
\text{two-class singleton}&66&81&99&118&142&167\\
\text{residual}&18&20&20&23&22&25
\end{array}                                                    \tag{28}
\]

The residual line includes the all-distinct partition and collision
families made mostly from singleton, double, and triple classes.  The
next sections close every one of those collision families.

## 9. Two inherited moving-class lemmas

The following two observations will finish the multiplicity census.

**Lemma 9.1 (constant residual).**  Suppose a family $R_x$ uses exactly
three value classes, includes exactly one selected label at a fixed
anchor $a$, selects $j\ge1$ labels from a moving value class $x$, and
leaves a singleton row class in $N_x$.  There are at most two possible
moving values $x$.

Indeed, (7) and the $p+2$ Hermite roots force
$Q_{R_x}=\lambda_xP_{N_x}$.  Absence of a simple pole at the fixed
anchor gives

\[
 Y_a(x)=U+\chi_j(a,x)=0,\qquad
 \chi_j(a,x)={j\over a+x}-{j+1\over x-a}
             =-{x+(2j+1)a\over x^2-a^2}.                     \tag{29}
\]

After clearing the denominator this is

\[
                      U(x^2-a^2)-x-(2j+1)a=0,                 \tag{30}
\]

a nonzero quadratic because its coefficient of $x$ is $-1$.

**Lemma 9.2 (linear residual).**  Suppose a family $R_x$ uses exactly
four value classes, leaves a singleton row class, has two fixed
single-selected anchors $a,b$, and selects $j\ge1$ labels from the
moving class $x$.  At most four moving values are possible.

Here $Q=P_N\ell_x$ with $\deg\ell_x\le1$.  The two anchor rows have a
common nonzero kernel only if

\[
 Y_b(x)-Y_a(x)+(b-a)Y_a(x)Y_b(x)=0,                           \tag{31}
\]

where $Y_a=U+\chi_j(a,x)$ and $Y_b=V+\chi_j(b,x)$.  Put
$\gamma=2j+1$.  Clearing
$(x^2-a^2)(x^2-b^2)$ gives a polynomial of degree at most four.
If it were identically zero, its $x^3,x^4$ coefficients would give

\[
 V=-U,\qquad U\bigl((a-b)U-2\bigr)=0.                         \tag{32}
\]

For the two branches, the cleared polynomial reduces respectively to

\[
 \begin{split}
 &(a-b)(\gamma-1)
       \bigl(x^2-(a+b)x-\gamma ab\bigr),\\
 &-(a-b)(\gamma+1)
       \bigl(x^2+(a+b)x+\gamma ab\bigr).
 \end{split}                                                  \tag{33}
\]

Both are nonzero because $a\ne b$, $j\ge1$, and their quadratic leading
coefficients are one.

We will also reuse the three-anchor quadratic determinant proved in
[live-three-zero-fifth-split-distinct-beta.md](live-three-zero-fifth-split-distinct-beta.md):
if $Q=P_Nq_x$, $\deg q_x\le2$, and three fixed distinct nonzero
single-selected anchors have coefficients
$U_s+\psi(s,x)$, at most six moving values are possible.  Its proof is
the degree-six determinant and incompatible opposite-pole residues
(18)--(20) of that note; the fixed part of $R_x$ is irrelevant.

The last collision profile needs one more observation which uses the
full confluent pole condition rather than only the simple-anchor rows.

**Lemma 9.3 (three full doubles).**  A profile containing at least five
distinct double classes and at least one singleton class is impossible.

Fix one double value $u$ and four other double values
$v_1,\ldots,v_4$.  For every pair $v,w$ among the latter four, select

\[
                         R_{vw}=\{u,u,v,v,w,w\}.              \tag{34}
\]

An exceptional singleton remains in $N_{vw}$, while $m_{R_{vw}}=3$.
Thus the Hermite roots and (7) force
$Q_{R_{vw}}=\lambda_{vw}P_{N_{vw}}$ with $\lambda_{vw}\ne0$.
At the selected double anchor $u$, write

\[
 W_{u;v,w}(z)=
 {P_{N_{vw}}(z)\over
  (z+\mu)^{k+1}(z+v)^3(z+w)^3}.
                                                                    \tag{35}
\]

Locally, $F=\lambda_{vw}W_{u;v,w}(z)/(z+u)^3$.  The confluent
squared-kernel columns at $u$ have pole orders three and two but no
simple pole.  Consequently

\[
 W_{u;v,w}''(-u)=0,\qquad
 \bigl((\log W_{u;v,w})'(-u)\bigr)^2
       +(\log W_{u;v,w})''(-u)=0.                              \tag{36}
\]

All values in (36) are defined and nonzero where required by the
structural denominator hypotheses.  Absorb into constants $C,K$ the
terms independent of $v,w$.  Moving a double value $v$ from the
numerator factor $(z-v)^2$ to the selected denominator factor
$(z+v)^3$ changes the two logarithmic derivatives at $-u$ by

\[
 A_v={2\over u+v}-{3\over v-u},qquad
 B_v={2\over(u+v)^2}+{3\over(v-u)^2}.                         \tag{37}
\]

Hence (36), for every pair $i<j$, is

\[
                 (C+A_i+A_j)^2+K+B_i+B_j=0.                  \tag{38}
\]

For distinct indices $i,j,k,\ell$, subtract the $(i,k)$ equation from
the $(i,j)$ equation, do the same with $\ell$ in place of $i$, and
subtract once more.  This gives

\[
                         2(A_j-A_k)(A_i-A_\ell)=0.             \tag{39}
\]

Applying (39) to the three partitions of four indices into two pairs
forces at least three of $A_1,A_2,A_3,A_4$ to be equal.  On the other
hand, $A_v=\lambda$ is

\[
                       \lambda(v^2-u^2)+v+5u=0,               \tag{40}
\]

a nonzero polynomial of degree at most two because the coefficient of
$v$ is one.  Its fibre contains at most two distinct values, a
contradiction.

## 10. The legal multiplicity census

Call a profile **short** if Section 8 applies, and **constant-movable**
if it has a Lemma 9.1 family with at least three moving classes.  The
single-selected-anchor hypothesis in Lemma 9.1 is essential.

**Lemma 10.1 (partition census).**  Every partition of $M=p+8\ge15$
which has a repeated part belongs to one of the following classes:

1. maximum multiplicity at least six;
2. short;
3. legally constant-movable;
4. one triple, $d\in\{0,1,2\}$ doubles, and singleton remainder;
5. $d\ge1$ doubles and singleton remainder;
6. all classes double.

Here is a direct proof.  Assume the maximum is at most five.

- A five-class is short: take $4+2$ if another repeated class exists,
  and otherwise take the whole five-class and one singleton, leaving
  another singleton.
- With maximum four, two four-classes or a four- and a triple-class give
  a short $3+3$ split; a double and singleton give a short $4+2$ split.
  The remaining one-four-class profiles are legally constant-movable by
  \[
       4_{\rm fixed}+1_{\rm anchor}+1_{\rm moving},\qquad
       3_{\rm fixed}+1_{\rm anchor}+2_{\rm moving},             \tag{41}
  \]
  for singleton and double remainders respectively.
- With maximum three, two triples and an untouched singleton give a
  short $3+3$ split.  For exactly one triple and at least three doubles,
  use
  \[
       3_T+1_{D,\rm anchor}+2_{D_x};
  \]
  when there are exactly three doubles and the first template has too
  few candidates, $M\ge15$ supplies at least six singletons and
  $3_T+1_{S,\rm anchor}+2_{D_x}$ works.  Thus only one triple with at
  most two doubles remains.  If there are at least two triples but no
  singleton, the legal templates
  \[
  \begin{array}{c|c}
  \text{number of triples}&\text{fixed and moving counts}\\ \hline
  2&3_T+1_{D,\rm anchor}+2_x\\
  3&3_T+1_{D,\rm anchor}+2_x\\
  4&2_T+1_{D,\rm anchor}+3_{T_x}\\
  \ge5&1_{T,\rm anchor}+2_T+3_{T_x}
  \end{array}                                                   \tag{42}
  \]
  have at least three candidates by $M\ge15$.  This exhausts the
  maximum-three case.
- With maximum two, the profile is precisely doubles plus singletons,
  including the all-double boundary.

Every constant template displayed above has a fixed count-one anchor
and leaves a singleton row class.  This proves the lemma.

## 11. Closing the remaining collision profiles

First take class 4 of Lemma 10.1.  Let $\tau$ be the triple value and
choose two distinct nonzero singleton anchors $a,b$.  For every other
singleton value $x$, take

\[
                         R_x=\{\tau,\tau,\tau,a,b,x\}.          \tag{43}
\]

The complement has singleton classes, $m_{R_x}=4$, and the residual is
linear.  If there are $d\le2$ doubles, the number $s$ of singletons
satisfies $s=M-3-2d\ge8$, so there are at least six moving values.
Lemma 9.2 with $j=1$ allows at most four.  Thus class 4 is closed.

Now consider $d$ doubles and $s>0$ singletons.  Fix a double class $u$
and three distinct nonzero value classes $a,b,c$, selecting one label
at each.  For every other value class $x$, also select one label and put

\[
                         R_x=\{u,u,a,b,c,x\}.                  \tag{44}
\]

The three anchors leave singleton row classes whenever they were
double; untouched singleton classes handle the other cases.  Thus
$m_{R_x}=5$ and the residual is quadratic.  There are $d+s-4$ moving
classes.  The inherited three-anchor degree-six obstruction closes the
profile whenever

\[
                              d+s\ge11.                         \tag{45}
\]

A second route uses a moving double class.  Fix a double class $u$,
two single-selected anchors $a,b$, and put

\[
                         R_x=\{u,u,a,b,x,x\}.                  \tag{46}
\]

The residual is linear.  If $s\ge3$, take $a,b$ singleton and retain an
untouched singleton in $N$; there are $d-1$ moving double values.  If
$s\in\{1,2\}$, take one anchor singleton and the other from a double
class, whose unused copy is a singleton in $N$; there are $d-2$ moving
double values.  Thus Lemma 9.2 with $j=2$ closes

\[
   s\ge3,\ d\ge6,\qquad\text{or}\qquad
   s\in\{1,2\},\ d\ge7.                                      \tag{47}
\]

For the all-double profile take both anchors from double classes.  There
are $d-3\ge5$ moving values because $d=M/2\ge8$, so it is closed as
well.

For $s>0$, the only integer pairs not covered by (45) or (47) satisfy

\[
        2d+s\ge15,\qquad d+s\le10
\]

and fail both alternatives in (47).  The unique pair is

\[
                              (d,s)=(5,5).                     \tag{48}
\]

It has five distinct double classes and singleton classes, so Lemma 9.3
closes it.

**Theorem 11.1 (sixth-split collision closure).**  Every sixth-split
collision stratum is closed.

Combining Theorem 11.1 with
[live-three-zero-sixth-split-distinct-closure.md](live-three-zero-sixth-split-distinct-closure.md)
gives the full conclusion: every no-extra-singular sixth-split stratum at
(t=r+7) is closed.  The independent audit in
[live-three-zero-sixth-split-five-core-cauchy-audit.md](live-three-zero-sixth-split-five-core-cauchy-audit.md)
checks the endpoint signs, the hollow-Cauchy conversion, the possible zero
exceptional value, and the strict root counts.

## 12. Exact audit

[verify_live_three_zero_sixth_split_frontier.py](../computations/verify_live_three_zero_sixth_split_frontier.py)
checks the degree bookkeeping, constructs (15)--(16), verifies the
degree-eight bound and explicit kernel (19), runs exact rational and
finite-field diagnostics for DR4, checks the deleted-$e_6$ descent,
proves (29)--(33) and the three-full-double identities (36)--(40)
symbolically, and enumerates the short, constant-movable, and final
profile classes through a wide exact range.  DR4 remains diagnostic in
that checker; the two companion checkers certify the weaker five-core
argument which closes the all-distinct stratum.
