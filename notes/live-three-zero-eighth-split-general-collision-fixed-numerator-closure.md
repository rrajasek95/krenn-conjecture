# The eighth split: a fixed-numerator closure for general collision profiles

## 1. Result

Work on the no-extra-singular live-three-zero stratum at the eighth
split.  Thus

\[
             h=8,\qquad p=8+k,\qquad k\geq1,\qquad
             \sum_{v\in V}\lambda_v=k+18.                    \tag{1}
\]

Distinct value classes are distinct and pairwise nonopposite, every
repeated value is nonzero, and at most one singleton value is zero.  A
**formal double layer** at a class of multiplicity at least two means that
two of its labels are assigned selected role two; any excess labels at that
value remain complementary.

Call a set \(U\subseteq V\) a **legal seven-universe** if

* \(|U|=7\) and every class in \(U\) is repeated; and
* for every five-set \(T\subset U\), all ten cores obtained by lowering
  two different formal double layers in \(T\) from role two to role one
  leave a nonzero singleton class in the complement.

The nonzero qualification makes the definition uniform over the possible
zero singleton orbit.

**Theorem 1.1 (general-collision fixed numerator).**  A collision profile
with a legal seven-universe is impossible.

The theorem is uniform in \(k\) and in all multiplicities outside the two
labels donated by each formal layer.  In particular, it is not restricted
to the stable profiles \(2^m\) and \(2^m1\).

Here is a count-only sufficient criterion.  Let \(n_j\) be the number of
parts equal to \(j\), and put

\[
                       \rho=\sum_{j\geq2}n_j.                    \tag{2}
\]

**Corollary 1.2.**  A legal seven-universe exists if

\[
 \boxed{\quad
 \rho\geq7\quad\hbox{and}\quad
 \bigl(n_1\geq2\ \hbox{ or }\ n_2\geq6\ \hbox{ or }\ n_3\geq5\bigr).
 \quad}                                                       \tag{3}
\]

Applied after the exact `H/S/C/L/Q/V` frontier and after removing every
profile with a mixed-role selection, (3) has the following exact effect:

\[
\begin{array}{c|rrrr}
k&\text{baseline R}&\text{selection-free}&\text{closed by (3)}&
       \text{left by (3)}\\ \hline
1&35&11&1&10\\
2&42&10&4&6\\
3&46&12&8&4\\
4&46&11&8&3\\
5&44& 6&5&1\\
6&44& 6&5&1\\
7&40& 3&3&0\\
8&39& 2&2&0\\
9&39& 2&2&0\\
10&39&1&1&0.
\end{array}                                                  \tag{4}
\]

There is no hidden later tail: every selection-free baseline profile with
\(k\geq7\) satisfies (3).  Section 8 proves a uniform finite bound before
the exact enumeration is invoked.

## 2. The formal-five input with fixed excess

Fix five repeated classes \(T\).  Regard two labels at every member of
\(T\) as a formal double layer.  If all ten pair drops are legal, the
all-order formal-five duality theorem gives an injective two-plane of
relation multipliers.  More explicitly, after subtracting two labels at
each \(t\in T\), put

\[
 A_T(z)=\prod_{v\in V}(z-v)^{\lambda_v-2\mathbf1_{v\in T}},
 \qquad c_T=\#\{v:\lambda_v-2\mathbf1_{v\in T}>0\}.             \tag{5}
\]

Then there is a two-plane

\[
                 {\cal S}_T\subseteq\mathbb C[z]_{\leq c_T-4} \tag{6}
\]

such that every \(S\in{\cal S}_T\) occurs in the exact rational
derivative

\[
 { (z+\mu)^k\displaystyle\prod_{t\in T}(z+t)^2 S(z)
   \over
   \displaystyle\prod_{\lambda_v-2\mathbf1_{v\in T}>0}
       (z-v)^{\lambda_v-2\mathbf1_{v\in T}+1}}.                 \tag{7}
\]

This is exactly the formal-five theorem with the fixed excess
\((z-t)^{\lambda_t-2}\) retained in the complementary polynomial.  No
full-double assumption has entered.

## 3. Put all fifth choices in one common kernel

Fix four values \(R\subset U\).  Define

\[
 m_v=\lambda_v-2\mathbf1_{v\in R},\qquad
 P_R=\{v:m_v>0\},\qquad c_R=|P_R|,                              \tag{8}
\]

and

\[
 \begin{aligned}
 Q_R(z)&=\prod_{r\in R}(z+r),\\
 D_R(z)&=\prod_{v\in P_R}(z-v)^{m_v+1},\\
 D_0(z)&=\prod_{v\in P_R}(z-v)^{m_v},\\
 H_R(z)&={ (z+\mu)^kQ_R(z)^2\over D_R(z)}.
 \end{aligned}                                                \tag{9}
\]

The degree which matters is

\[
                       \deg D_0=\sum_vm_v=k+10.                \tag{10}
\]

Define the common exactness kernel

\[
 {\cal K}_R=\{F\in\mathbb C[z]_{\leq c_R}:
                  H_RF\text{ has zero residue at every finite pole}\}.
                                                                    \tag{11}
\]

For \(a\in U\setminus R\), use the formal selection \(R\cup\{a\}\).
Put

\[
 \chi_a=\mathbf1_{\{\lambda_a=2\}},\qquad
 B_a(z)=(z+a)^2(z-a)^{2+\chi_a}.                               \tag{12}
\]

The derivative (7) is \(H_RB_aS\).  Moreover,

\[
 c_{R\cup\{a\}}=c_R-\chi_a,
 \qquad
 \deg(B_aS)\leq(4+\chi_a)+(c_R-\chi_a-4)=c_R.          \tag{13}
\]

Thus every fifth choice supplies a two-plane

\[
               B_a{\cal S}_{R\cup\{a\}}\subseteq{\cal K}_R.
                                                                    \tag{14}
\]

The calculation in (13) is where exact doubles and higher-multiplicity
formal layers differ.  The difference cancels: an exact double removes a
pole class and has a degree-five lift, while a class with fixed excess has
a degree-four lift and leaves the class present.

## 4. Exact normalization of the primitive

We now prove the fixed-numerator statement, including the integration
constant.  Put

\[
 R_0(z)=\prod_{v\in P_R}(z-v),\qquad
 S_0(z)={D_0(z)\over R_0(z)},\qquad
 D_1(z)={D_0'(z)\over S_0(z)}.                                  \tag{15}
\]

All three expressions are polynomials.  For \(n\in\mathbb C[z]\), set

\[
 {\cal E}_R(n)=
 R_0\bigl((z+\mu)n'+(k+1)n\bigr)-(z+\mu)D_1n.                  \tag{16}
\]

**Lemma 4.1.**  There is an exact linear isomorphism

\[
 \boxed{
 {\cal K}_R\simeq
 {\cal W}_R:=\{n\in\mathbb C[z]_{\leq9}:
                         Q_R^2\mid{\cal E}_R(n)\}.}             \tag{17}
\]

Under it, \(F={\cal E}_R(n)/Q_R^2\).

**Proof.**  If \(F\in{\cal K}_R\), then

\[
 \deg\operatorname{num}(H_RF)-\deg D_R
 \leq(k+8+c_R)-(k+10+c_R)=-2.                                 \tag{18}
\]

Hence \(H_RF\) has a unique rational primitive \(G\) which vanishes at
infinity.  Its pole at \(v\) has order at most \(m_v\), so

\[
                  G={M\over D_0},\qquad \deg M\leq k+9.        \tag{19}
\]

Let \(c=G(-\mu)\).  The derivative \(G'=H_RF\) has a zero of order at
least \(k\) at \(-\mu\), which is not a pole.  Therefore \(G-c\) has a
zero of order at least \(k+1\).  The numerator of \(G-c\), written over
\(D_0\), has degree at most \(\deg D_0=k+10\).  Consequently there is a
unique \(n\in\mathbb C[z]_{\leq9}\) such that

\[
                 G-c={ (z+\mu)^{k+1}n(z)\over D_0(z)}.           \tag{20}
\]

The subtraction of \(c\) is essential: it raises the numerator cap in
(19) by one and gives degree nine, not eight.

Differentiating (20) gives

\[
 G'={ (z+\mu)^k\over D_R}{\cal E}_R(n).                        \tag{21}
\]

Indeed the unreduced numerator is

\[
 D_0\bigl((z+\mu)n'+(k+1)n\bigr)-(z+\mu)D_0'n,
\]

which has the common factor \(S_0\), and
\(D_R=R_0^2S_0\).  Comparison with \(H_RF\) proves
\({\cal E}_R(n)=Q_R^2F\).

Conversely, for \(j=\deg n\leq9\), the nominal leading coefficient in
(16) is

\[
                 j+(k+1)-\deg D_0=j-9.                          \tag{22}
\]

It cancels at \(j=9\), and hence
\(\deg{\cal E}_R(n)\leq c_R+8\).  Dividing by \(Q_R^2\) gives a
polynomial \(F\) of degree at most \(c_R\), and (21) proves exactness.
If \({\cal E}_R(n)=0\), the left side of (20) is constant; its value at
\(-\mu\) is zero, so \(n=0\).  This proves bijectivity. \(\square\)

## 5. Fixed-anchor and moving-anchor jets

Write

\[
                 {\cal E}_R(n)=A(z)n'(z)+B(z)n(z),
                 \qquad A(z)=(z+\mu)R_0(z).                    \tag{23}
\]

At \(t=-r\), \(r\in R\), structural admissibility gives \(A(t)\ne0\).
The condition \((z+r)^2\mid{\cal E}_R(n)\) is the two-row system

\[
 \begin{pmatrix}
 B(t)&A(t)&0\\
 B'(t)&A'(t)+B(t)&A(t)
 \end{pmatrix}
 \begin{pmatrix}n(t)\\n'(t)\\n''(t)\end{pmatrix}=0.           \tag{24}
\]

The two rows are independent.  Thus a \(d\)-space in \({\cal W}_R\)
has Wronskian weight at least \(2(d-1)\) at each of the four fixed
anchors.

There is a second, reflected condition which is just as important.  For
\(a\in U\setminus R\), the primitive belonging to the relation plane in
(14) has denominator

\[
                  {D_0(z)\over(z-a)^2}.                         \tag{25}
\]

Putting it over the common denominator \(D_0\) shows that its normalized
numerator is \((z-a)^2N(z)\).  Therefore (14) pulls back under (17) to a
two-plane

\[
              {\cal V}_a\subseteq
              {\cal W}_R\cap(z-a)^2\mathbb C[z]_{\leq7}.
                                                                    \tag{26}
\]

This double zero is independent of whether \(a\) is an exact double or
has fixed excess.

## 6. The normalized space is exactly four-dimensional

Put \(d=\dim{\cal W}_R\).  The four fixed anchors and the degree-nine
Wronskian cap give

\[
                         8(d-1)\leq d(10-d).                     \tag{27}
\]

Thus \(d\leq4\).  Since \(U\setminus R\) contains three values, (26)
also rules out the lower dimensions.

If \(d=2\), every \({\cal V}_a\) is the whole space.  At each moving
value the vanishing sequence is at least \((2,3)\), of weight four.
Together with the four fixed weights this gives

\[
                         4\cdot2+3\cdot4=20>2(10-2)=16.          \tag{28}
\]

If \(d=3\), the two-plane in (26) gives vanishing sequence at least
\((0,2,3)\), of weight two.  Hence

\[
                         4\cdot4+3\cdot2=22>3(10-3)=21.          \tag{29}
\]

Dimension one cannot contain (26).  Consequently

\[
                         \boxed{\dim{\cal W}_R=4}.               \tag{30}
\]

Every inequality in (27) is now an equality.  At each \(t_i=-r_i\) the
vanishing sequence is exactly

\[
                              (0,3,4,5),                         \tag{31}
\]

and there is no other Wronskian weight.  Intersecting the three
hyperplanes of sections divisible by \((z+r_j)^3\), \(j\ne i\), gives

\[
 R_i(z)=\prod_{j\ne i}(z+r_j)^3\in{\cal W}_R.                   \tag{32}
\]

The four \(R_i\)'s are independent by evaluation at the four points
\(-r_i\).  Therefore

\[
                         {\cal W}_R=\langle R_1,R_2,R_3,R_4\rangle.
                                                                    \tag{33}
\]

## 7. Core swaps cancel every collision multiplicity

Apply the first row of (24) to \(R_i\) at \(t_i=-r_i\).  Since
\(D_1/R_0=D_0'/D_0\), division by structural units gives

\[
 3\sum_{j\ne i}{1\over r_j-r_i}
 +{k+1\over\mu-r_i}
 +\sum_{v\in V}{\lambda_v-2\mathbf1_{v\in R}\over r_i+v}=0.
                                                                    \tag{34}
\]

This is the only place where the arbitrary collision multiplicities
appear.

Fix three values \(r,b,c\in U\), and in (34) take

\[
                         R=\{r,b,c,x\},qquad
                         x\in U\setminus\{r,b,c\}.               \tag{35}
\]

All terms independent of \(x\) cancel into one constant.  The remaining
term is

\[
 g_r(x)={3\over x-r}-{2\over x+r}
        ={x+5r\over x^2-r^2}.                                  \tag{36}
\]

Thus all four values in \(U\setminus\{r,b,c\}\) must lie in one fibre
of \(g_r\).  But \(g_r(x)=\gamma\) is the nonzero quadratic equation

\[
                 \gamma x^2-x-(\gamma r^2+5r)=0;                \tag{37}
\]

its coefficient of \(x\) is \(-1\), so the equation is never identically
zero and every fibre has size at most two.  This contradiction proves
Theorem 1.1.

## 8. Count criterion and the uniform tail audit

For a selected five-set \(T\), put

\[
 e_T=\#\{t\in T:\lambda_t=2\},\qquad
 q_T=\#\{t\in T:\lambda_t=3\}.                                \tag{38}
\]

After lowering a pair, a nonzero singleton is supplied by a lowered exact
double, an unlowered exact triple, or an untouched nonzero singleton.
If \(n_1\geq2\), the last source is always present.  If \(n_1\leq1\),
the possible singleton must be treated as zero, and literal enumeration of
the lowered pair says that every five-subset of a seven-universe is legal
exactly in either of the two cases

\[
                 \#\{u\in U:\lambda_u=2\}\geq6,
       \qquad\hbox{or}\qquad
                 \#\{u\in U:\lambda_u=3\}\geq5.               \tag{39}
\]

Indeed a bad pair contains no exact double and contains every selected
exact triple.  If a seven-set has at least six doubles, every five-subset
has at least four doubles.  If it has at least five triples, every
five-subset has at least three triples.  Conversely, with at most five
doubles and at most four triples one can choose a bad five-subset; the
finite type enumeration in the checker verifies all (36) triples of
type counts.  This proves (3).

It remains to justify that the last assertion after (4) is uniform.  A
selection-free profile has \(n_1\leq9\).  Failure of route `S` gives

\[
 \lambda_1+\lambda_2\leq7\quad(n_1>0),\qquad
 \lambda_1+\lambda_2\leq8\quad(n_1=0).                          \tag{40}
\]

If (3) fails and \(n_1>0\), either there are at most six repeated
classes, or \(n_1=1,n_2\leq5,n_3\leq4\).  Equation (40) bounds the total
size by \(28\), hence \(k\leq10\).

If \(n_1=0\), at most six repeated classes give total size at most \(24\).
With at least seven repeated classes, failure of (3) again gives
\(n_2\leq5,n_3\leq4\).  If one part is at least five, (40) bounds the
total size by \(28\).  Otherwise all parts are at most four.  Eleven
four-classes trigger the exact quadratic-moving route `Q`: choose three
four-class anchors, take two labels from a fixed four-class, and three
labels from each of seven moving four-classes; the moving remainder is a
nonzero singleton.  Thus a baseline residual has at most ten four-classes,
and its total size is at most

\[
                         10\cdot4+4\cdot3+5\cdot2=62.            \tag{41}
\]

Consequently every theorem-open baseline profile has \(k\leq44\).
Exact partition enumeration through that rigorously bounded range shows
that theorem-open profiles occur only for \(1\leq k\leq6\), giving (4)
and proving the uniform \(k\geq7\) tail statement.

## 9. The arbitrary-\(h\) normalization and its exact limit

The normalization itself is not special to \(h=8\).  Suppose a common
formal selection at a general split has total role \(h+2\).  Fix anchors
whose selected roles sum to \(A\), and restore every prospective moving
class to the common complement.  The common primitive denominator then
has degree

\[
                    (2h+k+2)-A.                                \tag{42}
\]

After subtracting the value at \(-\mu\) and dividing by
\((z+\mu)^{k+1}\), the normalized numerator has degree at most

\[
                         \boxed{2h+1-A}.                         \tag{43}
\]

If one moving layer has role \(b\), then \(A=h+2-b\), so (43) is
\(h-1+b\).  A fixed anchor of role \(r\) imposes \(r\) independent jets
on the first-order operator and contributes \(r(d-1)\) Wronskian units.
If a moving relation plane has dimension two, its normalized numerators
are divisible by \((z-a)^b\); at a \(d\)-space this contributes at least

\[
                         2\max(0,b-d+2)                         \tag{44}
\]

additional units.  Thus \(q\) moving candidates must satisfy

\[
 (h+2-b)(d-1)+2q\max(0,b-d+2)
                       \leq d(h+b-d).                           \tag{45}
\]

For the formal-double case \(b=2,d=4\), the slack in the fixed-anchor
part of (45) is exactly

\[
                  4(h-2)-3h=h-8.                               \tag{46}
\]

This explains both the strength and the limit of Theorem 1.1.  At the
eighth split the slack is zero and gives the rigid basis (33).  For
\(h>8\) it is positive, while a two-plane of double-zero sections is an
ordinary condition in a four-space and contributes no Wronskian weight.
Therefore the \(h=8\) core-swap closure must not be credited at the
higher-split \(p=18\) saturated five-space boundary.  The normalized
degree formula (43) remains exact there, but an additional cofactor,
multi-drop, or reflected-jet compatibility is required.

## 10. Exact audit

[verify_live_three_zero_eighth_split_general_collision_fixed_numerator_closure.py](../computations/verify_live_three_zero_eighth_split_general_collision_fixed_numerator_closure.py)
checks the rational derivative identity with nonuniform pole
multiplicities, the integration-constant and degree formulas, the local
jet ranks, every Wronskian inequality and equality, the equality basis and
multiplicity-cancelling swap, all seven-universe type counts, the complete
bounded census (4), and the arbitrary-\(h\) formulas (42)--(46).

The theorem closes a uniform part of the unrelated eighth-split
no-selection frontier.  It does not close the finitely many
selection-free cases at \(k\leq6\), the higher-\(h\) saturated branches,
the additional-singular strata, or the missing global all-even reduction.
