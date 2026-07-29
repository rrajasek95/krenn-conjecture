# The seventh split: collision closures and the exact residual frontier

## 1. Status and scope

Continue from the sixth-split notes.  Put

\[
 t=r+8,\qquad p=r-1,\qquad k=p-7,\qquad p\ge8.                \tag{1}
\]

There are \(p+9\) exceptional live labels.  Fix seven exceptional
columns \(R\); their complement \(N\) has \(p+2\) labels, and deleting a
marked pair leaves \(p\) row labels.

The lower bound in (1) is the feasibility condition
\(t=p+9\le2r-1=2p+1\).  The checker also retains \(p=7\) as a formal
one-step boundary diagnostic, but that row is not an admissible seventh
split.

This note treats every repeated-beta multiplicity profile by a uniform
exact census.  It proves all closures supplied by:

1. the deleted-\(e_7\) descent for a class of multiplicity at least seven;
2. the two-class Hermite degree contradiction;
3. constant, linear, and quadratic moving-class residuals.

The remaining profiles are listed exactly in Section 8.  They are an
honest frontier, not claimed closed.  In particular, a cubic-residual
argument with four fixed anchors does not automatically inherit the
sixth-split five-core closure: after two background labels and one moving
label are selected, only four fixed anchor slots remain.

## 2. The seven-column Hermite reduction

The isolated-star pivot has the same form as in the preceding splits:

\[
 C_{L\mid R}=2h_{01}^{p}\operatorname {per}{\cal C}_{L\mid R}, \tag{2}
\]

where the \(p\times p\) Cauchy matrix has row parameters from \(L\) and
column parameters consisting of the seven labels in \(R\) and \(k\)
copies of the common value \(\mu\).  Equivalently,

\[
 C_{L\mid R}=2h_{01}^{p}k!
 \left(\prod_{i\in L}{1\over\nu_i+\mu}\right)
 \sum_{\substack{J\subset L\\|J|=7}}
 \operatorname {per}
 \left({\nu_i+\mu\over\nu_i+\nu_c}\right)_{i\in J,c\in R}. \tag{3}
\]

Every displayed prefactor is structurally nonzero.  Suppose that all
pivots vanish.  If \(R\) represents \(m_R\) exceptional value classes,
the simultaneous-Hermite singleton-row lemma gives a nonzero column
dependence

\[
 F_R(z)={Q_R(z)\over D_R(z)},\qquad
 D_R(z)=(z+\mu)^{k+1}\prod_y(z+y)^{r_y+1}.                   \tag{4}
\]

Since \(\sum_y r_y=7\),

\[
 \deg D_R=(k+1)+7+m_R=p+m_R+1,
 \qquad \deg Q_R\le p+m_R-1.                                \tag{5}
\]

The \(p+2\) row jets are Hermite roots of \(Q_R\).  Thus
\(P_N(z)=\prod_{i\in N}(z-\nu_i)\), with repetitions, divides \(Q_R\),
and therefore

\[
\begin{array}{c|c}
 m_R&\text{consequence}\ \hline
 m_R\le2&\text{degree contradiction},\\
 m_R=3&Q_R=\lambda_RP_N,\\
 m_R=4&Q_R=P_N\ell_R,\quad\deg\ell_R\le1,\\
 m_R=5&Q_R=P_Nq_R,\quad\deg q_R\le2,\\
 m_R=6&Q_R=P_Nc_R,\quad\deg c_R\le3,\\
 m_R=7&Q_R=P_Nd_R,\quad\deg d_R\le4.
\end{array}                                                   \tag{6}
\]

Only the first four lines of (6) are used for the proved collision
closures below.

## 3. A class of multiplicity at least seven

Suppose a value \(a\) occurs at least seven times and choose seven copies
for \(R\).  Put

\[
                         h_i={\nu_i+\mu\over\nu_i+a}\ne0.    \tag{7}
\]

The normalized pivot is

\[
                              7!e_7(h_i:i\in L).              \tag{8}
\]

Let \(m=|N|=p+2\ge10\).  If all \(h_i\)'s are equal, (8) is the nonzero
quantity \(7!\binom p7h^7\).  Otherwise choose \(h_j\ne h_k\).  Subtracting
the deleted-pair equations for \(\{i,j\}\) and \(\{i,k\}\) gives

\[
 (h_k-h_j)e_6(h_\ell:\ell\notin\{i,j,k\})=0                 \tag{9}
\]

for every \(i\notin\{j,k\}\).  On \(W=N\setminus\{j,k\}\), all
one-deletion \(e_6\)'s vanish.  The identities

\[
 \sum_{i\in W}e_d(W\setminus\{i\})=(|W|-d)e_d(W),\qquad
 e_d(W)=e_d(W\setminus\{i\})+h_i e_{d-1}(W\setminus\{i\}) \tag{10}
\]

descend through \(d=6,5,\ldots,1\) and force some \(h_i=0\), a
contradiction.  Thus every profile of maximum multiplicity at least seven
is closed.

## 4. Short two-class splits

Call a profile **short** if seven labels can be selected from at most two
value classes while leaving a singleton value class in \(N\).  For that
selection, the singleton-row lemma applies and \(m_R\le2\), contradicting
the first line of (6).

This definition is deliberately algorithmic.  If a profile is
\(\lambda=(\lambda_1,\ldots,\lambda_c)\), it asks for one or two indices
and integers \(0<r_i\le\lambda_i\) with total seven such that

\[
                         \lambda_h-r_h=1                     \tag{11}
\]

for at least one class \(h\), where an unselected class has \(r_h=0\).
The census checker tests exactly (11), not a heuristic surrogate.

## 5. Three moving-class lemmas

The following setup packages all remaining proved closures.  Select
\(a\) distinct fixed anchors once each, select \(f\ge1\) labels from one
additional fixed value class, and select \(j\ge1\) labels from a moving
class \(x\), where

\[
                              a+f+j=7.                        \tag{12}
\]

Assume that every member of the moving family leaves a singleton class in
\(N_x\).  A simple-selected anchor \(s\) contributes

\[
 Y_s(x)=U_s+\chi_j(s,x),\qquad
 \chi_j(s,x)={j\over s+x}-{j+1\over x-s}
             =-{x+(2j+1)s\over x^2-s^2}.                    \tag{13}
\]

All fixed anchors used below are nonzero.  This is always part of the
legal-witness test: structural admissibility permits at most one zero
value, and a repeated value cannot be zero.
The candidate moving classes have distinct values, and no candidate is a
pole of (13), by distinctness of the classes and the structural pair-sum
condition.

### 5.1 One anchor: constant residual

For \(a=1\), exactly three value classes occur in \(R_x\), and (6) gives
\(Q=\lambda P_N\).  The anchor condition is

\[
                         U+\chi_j(s,x)=0.                     \tag{14}
\]

After clearing the denominator this is

\[
                    U(x^2-s^2)-x-(2j+1)s=0,                 \tag{15}
\]

a nonzero quadratic.  Hence at most two moving values are possible.  A
family with at least three candidates is closed.

### 5.2 Two anchors: linear residual

For \(a=2\), the residual has degree at most one.  Two anchor rows have a
common nonzero kernel only if

\[
 Y_b-Y_a+(b-a)Y_aY_b=0.                                     \tag{16}
\]

Writing \(\gamma=2j+1\), clearing the two quadratic denominators gives a
polynomial of degree at most four.  If it were identically zero, its two
top coefficients would give

\[
 V=-U,qquad U((a-b)U-2)=0.                                 \tag{17}
\]

The two branches reduce to nonzero quadratics with leading factors
\(\gamma-1\) and \(\gamma+1\), respectively.  Since \(j\ge1\), neither
factor vanishes.  Thus at most four moving values are possible, and five
candidates close the family.

### 5.3 Three anchors: quadratic residual

For \(a=3\), the residual has degree at most two.  The determinant of the
three anchor rows is the polynomial \(\Phi(A,B,C)\) from (14) of
[live-three-zero-fifth-split-distinct-beta.md](live-three-zero-fifth-split-distinct-beta.md).
After substituting \(U_s+\chi_j(s,x)\), its cleared degree is at most six.

The opposite-pole proof from that note extends to every \(j\ge1\).  Put
\(\gamma=2j+1\).  The three opposite-pole subtractions give

\[
\begin{split}
 L_a={}&(a^2-b^2)V+(a^2-c^2)W+2a+(2-\gamma)(b+c),\\
 L_b={}&(a^2-b^2)U+(c^2-b^2)W+(\gamma-2)(a+c)-2b,\\
 L_c={}&(a^2-c^2)U+(b^2-c^2)V+(\gamma-2)(a+b)-2c.
\end{split}                                                   \tag{18}
\]

If the cleared determinant were the zero polynomial, evaluation at the
two opposite poles \(x=\pm a\) would force both corresponding
\(\Phi_A\)-values to vanish; their difference is a structurally nonzero
factor times \(L_a\).  The same argument at \(\pm b\) and \(\pm c\)
forces \(L_a=L_b=L_c=0\).  This is impossible, because

\[
 -(b^2-c^2)L_a-(a^2-c^2)L_b+(a^2-b^2)L_c
 =\gamma(a-b)(a-c)(b-c)\ne0.                                \tag{19}
\]

Thus the degree-six determinant is not identically zero.  It has at most
six moving roots, so seven candidates close the family.

## 6. Exact legal-witness census

For a multiplicity profile \(\lambda\), the checker applies the following
classes in order.

1. **H:** \(\max\lambda_i\ge7\), Section 3.
2. **S:** a short witness (11).
3. **C:** a legal one-anchor family (12) with at least three moving
   candidates.
4. **L:** a legal two-anchor family with at least five candidates.
5. **Q:** a legal three-anchor family with at least seven candidates.

"Legal" means that the fixed classes and moving class are distinct, every
selection count is available, every moving complement has a singleton,
and the required anchors can be chosen nonzero even if the unique possible
zero value is a singleton class.  Since classes of the same multiplicity
are interchangeable, it is enough to test the no-zero case and one
representative zero singleton.

For \(p=8,\ldots,13\), the exact counts, including the all-distinct profile
\(D\), are shown below.  The daggered \(p=7\) row is the formal diagnostic
mentioned after (1), not a feasible stratum.

\[
\begin{array}{c|rrrrrrr|r}
p&H&S&C&L&Q&R&D&\text{total}\ \hline
7^\dagger&95&96&11&4 &6 &18&1&231\\
8 &134&119&13&7&9 &14&1&297\\
9 &186&151&14&10&11&12&1&385\\
10&255&182&18&13&12&9&1&490\\
11&345&226&19&14&13&9&1&627\\
12&461&269&22&16&14&9&1&792\\
13&611&325&25&17&16&7&1&1002.
\end{array}                                                   \tag{20}
\]

No profile containing a part four, five, or six occurs in column \(R\).
Thus every residual collision profile consists only of triples, doubles,
and singletons.

## 7. The double/single boundary in closed form

Write a double/single profile as

\[
                             (2^d,1^s),\qquad 2d+s=p+9.       \tag{21}
\]

Neither a short, constant, nor linear family can use seven labels from
classes of size at most two.  A quadratic family must have the unique
count pattern

\[
                  1+1+1+2+2=7:                              \tag{22}
\]

three simple anchors, one fixed full double, and one moving full double.
Let \(a\) of the three anchors come from double classes.  Then the number
of moving double candidates is \(d-1-a\).  Requiring seven candidates,
nonzero anchors in the possible presence of one zero singleton, and a
singleton in every complement gives exactly

\[
\boxed{
\begin{array}{ll}
 d\ge8,&s\ge4,\\
 d\ge9,&s\ge3,\\
 d\ge10,&s\ge2,\\
 d\ge11,&s\ge0.
\end{array}}                                                  \tag{23}
\]

Here the four lines correspond to \(a=0,1,2,3\).  These conditions are
both sufficient and exhaustive for the methods of Sections 3--5 on a
double/single profile.

## 8. Exact residual profiles

Let \((q,d,s)\) denote \(q\) triple classes, \(d\) double classes, and
\(s\) singleton classes.  The residual triple-containing profiles are

\[
\begin{array}{c|l}
p& (q,d,s)\ \hline
7^\dagger&(3,3,1),(3,2,3),(3,1,5),(3,0,7),
   (2,5,0),(2,4,2),(2,3,4),(2,2,6),(1,6,1),(1,4,5)\\
8&(3,4,0),(3,3,2),(3,2,4),(3,1,6),(2,5,1),(2,3,5)\\
9&(6,0,0),(3,4,1),(3,2,5)\\
12&(7,0,0).
\end{array}                                                   \tag{24}
\]

There are no other triple-containing residuals.  For feasible
\(p=8,\ldots,12\),
the residual double/single profiles are precisely the pairs \((d,s)\)
with \(d\ge1\), \(2d+s=p+9\), which fail (23).  For every \(p\ge13\), this simplifies
to the seven uniform families

\[
                  \boxed{(2^d,1^{p+9-2d}),\qquad1\le d\le7.} \tag{25}
\]

The uniform assertion uses only a finite reduction.  For profiles with
all parts at most six, every proved witness remains valid after a new value
class is appended.  This also respects the possible zero value.  An appended
class of size at least two is necessarily nonzero, so the old zero-robust
witness persists.  If an appended singleton is nonzero, the same is true;
if it is the unique zero, use the old no-zero witness and leave the new
singleton untouched.  Its anchors remain nonzero, and the new complement
even supplies a singleton row class.

If a profile of total at least 29 contains a part at least three, remove
whole other classes, preserving such a part, until its total lies between
22 and 28.  Since every removed part is at most six, the first total below
29 is still at least 23.  The exact base census in that interval has no
residual with a part at least three, and the persistence just proved lifts
its witness back through the removed classes.  Double/single profiles are
governed directly by (23).  This proves (24)--(25) for every feasible
\(p\), rather than only for the displayed numerical range.

These residuals require a new ingredient: a confluent treatment of the
linear/cubic residual on the small triple profiles, or a four-anchor
identity strong enough to handle a fixed four-core whose translation
changes when the moving label is replaced.  Neither step is asserted here.

## 9. Exact audit

[verify_live_three_zero_seventh_split_collision_frontier.py](../computations/verify_live_three_zero_seventh_split_collision_frontier.py)
checks the degree formulas, deleted-\(e_7\) subtraction and descent,
constant/linear moving polynomials, the generalized quadratic
opposite-pole certificate (18)--(19), every legality condition including a
possible zero singleton, the counts (20), the residual table (24), the
double/single criterion (23), and the finite-to-uniform reduction behind
(25).  It reports the residuals as open.
