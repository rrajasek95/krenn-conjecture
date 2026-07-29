# Higher-split collision census after exchange and Wronskian closure

## 1. Status and scope

Put

\[
 h=t-r-1,\qquad p=r-1,\qquad k=p-h,
 \qquad h\ge8,\quad p\ge h+1.                              \tag{1}
\]

The exceptional multiset has

\[
                         M=p+h+2                             \tag{2}
\]

labels.  This note gives an exact combinatorial frontier for the
no-extra-singular collision strata after applying the presently proved
uniform tools:

1. the deleted-\(e_h\) obstruction for a class of multiplicity at least
   \(h\);
2. the short two-class Hermite contradiction;
3. the constant, linear, and quadratic moving-class root counts;
4. the value-core cubic exchange followed by the full-core residue and
   Wronskian count.

The result is a frontier, not a closure theorem.  In fact, Sections 8 and 9
exhibit large persistent residual families.  In particular, the exchange--
Wronskian argument which finishes the seventh split has only a very small
higher-split range.

Write the multiplicity profile as

\[
 \lambda=(\lambda _1\ge\lambda _2\ge\cdots\ge\lambda _c),
 \qquad \sum_i\lambda_i=M.                                  \tag{3}
\]

Let \(d\) be the number of parts equal to two and \(s\) the number equal
to one.  A repeated value is structurally nonzero; at most one singleton
value may be zero.

## 2. Uniform Hermite bookkeeping

Select \(h\) exceptional labels in a multiset \(R\), let \(m_R\) be the
number of value classes represented by \(R\), and put \(N=E\setminus R\).
Thus \(|N|=p+2\).  If \(N\) has a singleton value class, simultaneous row
and column confluence gives a nonzero rational column dependence

\[
 F_R(z)={Q_R(z)\over D_R(z)},\qquad
 D_R(z)=(z+\mu)^{k+1}\prod_{v\in R_{\rm cls}}
                         (z+v)^{r_v+1},                     \tag{4}
\]

where \(r_v\) is the number of selected labels of value \(v\).  Since
\(\sum r_v=h\),

\[
 \deg D_R=(k+1)+h+m_R=p+m_R+1,
 \qquad \deg Q_R\le p+m_R-1.                               \tag{5}
\]

All \(p+2\) complementary row jets are roots of \(Q_R\), counting
multiplicity.  Hence

\[
 Q_R=P_Nq_R,\qquad 0\ne q_R,qquad
                         \deg q_R\le m_R-3.                 \tag{6}
\]

In particular, \(m_R\le2\) is impossible.  Formula (6) is independent of
\(p\) and is the source of every route audited below.

## 3. The previously proved uniform routes

### 3.1 High multiplicity

If \(\max\lambda_i\ge h\), choose \(h\) equal-valued columns.  The
normalized pivot is \(h!e_h\) in the complementary Cauchy ratios.  The
deleted-pair subtraction

\[
 e_h(X\setminus\{i,j\})-e_h(X\setminus\{i,k\})
       =(x_k-x_j)e_{h-1}(X\setminus\{i,j,k\})               \tag{7}
\]

and the one-deletion identities descend from \(e_{h-1}\) to \(e_1\).
Here the remaining set has \(p\ge h+1\) elements, so every coefficient in
the descent is nonzero.  A Cauchy ratio would be forced to vanish, which is
structurally impossible.  Call this route **H**.

### 3.2 Short Hermite selections

Call a profile short if \(h\) labels can be selected in at most two value
classes while leaving a singleton in the complement.  Then (6) has
\(m_R\le2\), a contradiction.  Call this route **S**.

After H has been excluded, S has the following closed form:

\[
 \boxed{\lambda_1+\lambda_2\ge h+1
 \quad\hbox{or}\quad
 (s>0\ \hbox{ and }\ \lambda_1+\lambda_2\ge h).}           \tag{8}
\]

For the first alternative, select from the two leading classes and leave
one label in a selected class.  For the second, leave an untouched
singleton.  Conversely, any singleton left by a two-class selection is of
one of these two types, proving necessity.

### 3.3 Moving residuals of degree zero, one, and two

Choose \(a\in\{1,2,3\}\) distinct nonzero anchors once each, select \(f\)
labels from one fixed class, and select \(j\) labels from a moving class,
where

\[
                              a+f+j=h.                       \tag{9}
\]

Every moving selection must leave a singleton in its complement.  It uses
\(a+2\) value classes, so (6) gives a residual of degree at most \(a-1\).
The established moving-anchor calculations give a nonzero cleared
polynomial in the moving value of degree at most \(2a\).  Therefore

\[
\begin{array}{c|c|c|c}
a&\deg q&\text{required candidates}&\text{route}\ \hline
1&0&3&\mathrm C\\
2&1&5&\mathrm L\\
3&2&7&\mathrm Q.
\end{array}                                                  \tag{10}
\]

These statements hold for every \(j\ge1\).  Their nonidentity proofs are
respectively the nonzero quadratic, the incompatible two-anchor endpoint
branches, and the three-anchor opposite-pole certificate.  No cubic or
higher residual is included in the census.

For completeness, the exact legality test used by the checker can be
written without class labels.  Let \(n_m\) be the number of classes of
multiplicity \(m\), and let \(A_m\) count the chosen anchors of that
multiplicity.  For each possible zero scenario,

\[
 \sum_m A_m=a,\qquad A_1\le n_1-\mathbf1_{\{\text{zero singleton}\}}. \tag{11}
\]

Choose a remaining fixed class of multiplicity \(u\), a count
\(1\le f\le u\), and put \(j=h-a-f\).  A remaining class of multiplicity
\(v\ge j\) is a legal moving candidate exactly when

\[
\begin{split}
 &n_1-A_1-\mathbf1_{u=1}-\mathbf1_{v=1}>0,\quad\hbox{or}\\
 &A_2>0,\quad\hbox{or}\quad u-f=1,quad\hbox{or}\quad v-j=1.
\end{split}                                                  \tag{12}
\]

The four alternatives say, respectively: an untouched singleton, a mate
of a double anchor, a fixed-class remainder, or a moving-class remainder.
After subtracting the anchor and fixed classes from the type counts, the
sum of legal candidates must be at least \(2a+1\).  Equations (11)--(12)
are an exact finite test for C, L, and Q, including a possible zero
singleton; they are not a heuristic sufficient condition.

## 4. Exactly when every \(h\)-value core is legal

Let \(V\) be the set of the \(c\) distinct exceptional values.  For an
\(h\)-set \(T\subset V\), select one label from every class in \(T\).  Its
complement has a singleton class precisely when

* \(T\) contains a double class, whose mate remains; or
* \(V\setminus T\) contains a singleton class.

Thus an illegal core contains every singleton and contains no double.  Such
a core exists exactly when \(s\le h\) and the number \(c-d\) of nondouble
classes is at least \(h\).  We have proved the exact criterion

\[
 \boxed{\text{every \(h\)-value core is legal}
 \iff c\ge h\ \text{ and }\bigl(s>h\ \text{ or }\ c-d<h\bigr).} \tag{13}
\]

The exchange--Wronskian route below requires the strict inequality
\(c\ge h+1\), because at least one cubic lift is needed to create a
three-dimensional final space.

## 5. Exchange to the full value set

Assume (13), with \(c\ge h+1\), and suppose all isolated-star pivots
vanish.  For every \(h\)-set \(T\subset V\), (6) gives

\[
                  0\ne q_T,\qquad \deg q_T\le h-3,          \tag{14}
\]

satisfying the Robin equations at the selected values.

Let \(m_v=\lambda_v\), and for any \(T\subset V\) define

\[
 B_T(z)=\prod_{v\in V}(z-v)^{m_v-\mathbf1_{v\in T}},
 \qquad
 \Delta_T(z)=(z+\mu)^{k+1}\prod_{v\in T}(z+v)^2.          \tag{15}
\]

For \(b\notin T\), the cubic gauge

\[
                         g_b(z)=(z-b)(z+b)^2                \tag{16}
\]

preserves the rational function exactly:

\[
 {B_{T\cup\{b\}}(z)g_b(z)q(z)\over\Delta_{T\cup\{b\}}(z)}
                  ={B_T(z)q(z)\over\Delta_T(z)}.           \tag{17}
\]

The three-lift lemma applies because the distinct value classes are
nonopposite; \(g_0=z^3\) handles a possible zero singleton.  Successively
cancelling the top two coefficients propagates (14) through every set size
below \(c\).  On the last step, retain the lift span rather than cancelling.
It gives

\[
                    K\subset\mathbb C[z]_{\le c-1},
                    \qquad \dim K\ge3,                      \tag{18}
\]

and every member of \(K\) satisfies the full-core Robin equations at all
\(c\) value nodes.

## 6. The high-order common-pole residue

Put

\[
 B(z)=\prod_{v\in V}(z-v)^{m_v-1},\qquad
 P(z)=\prod_{v\in V}(z+v),\qquad
 F_q(z)={B(z)q(z)\over(z+\mu)^{k+1}P(z)^2}.                \tag{19}
\]

The full-core Robin equations say exactly that \(F_q\) has zero residue at
each pole \(-v\), \(v\in V\).  Since

\[
 \deg B=M-c,\qquad \deg q\le c-1,
\]

the decay at infinity is

\[
 (k+1)+2c-\bigl((M-c)+(c-1)\bigr)=2(c-h)\ge2.              \tag{20}
\]

There is no residue at infinity.  The residue theorem therefore makes the
residue at the only remaining pole, \(-\mu\), vanish.  Its regular cofactor
is structurally nonzero, so this is a differential functional of exact
order \(k\):

\[
 \left.\left({d\over dz}\right)^k
       \left({B(z)q(z)\over P(z)^2}\right)\right|_{z=-\mu}=0
                         \qquad(q\in K).                    \tag{21}
\]

For \(k=1\), (21) is the extra Robin node used in the final seventh-split
proof.  For \(k>1\), it is not a Robin equation and must not be counted as
one.  The next section records its exact, weaker Wronskian contribution.

## 7. The generalized Wronskian criterion

Let \(r=\dim K\ge3\), let \(H=\gcd K\), and set \(e=\deg H\).  Let \(b\)
be the number of value nodes at which \(H\) vanishes, and let
\(t=\operatorname{ord}_{-\mu}H\).  A common root at a value-node Robin
condition is automatically double.  Hence

\[
                              e\ge2b+t.                     \tag{22}
\]

After division by \(H\), every one of the \(c-b\) remaining value nodes
has Wronskian weight at least \(r-1\).

If \(t\le k\), equation (21) becomes a differential functional of exact
order \(\kappa=k-t\) on the reduced, base-point-free space.  The vanishing
sequence at \(-\mu\) cannot contain \(\kappa\): a section of exact order
\(\kappa\) kills all lower derivatives but not the leading derivative of
the functional.  Omitting \(\kappa\) contributes at least

\[
                         w_t=\max(0,r-k+t)                  \tag{23}
\]

to the Wronskian weight.  If \(t>k\), the pole has been cancelled and we
put \(w_t=0\).

The reduced polynomials have degree at most \(c-1-e\).  The polynomial
Wronskian bound would therefore require

\[
 (c-b)(r-1)+w_t
          \le r(c-r-e)
          \le r(c-r-2b-t).                                 \tag{24}
\]

The leftmost side minus the rightmost side is

\[
                     r^2-c+b(r+1)+rt+w_t.                  \tag{25}
\]

For every \(t\ge0\), the last two terms are at least
\(\max(0,r-k)\); the remaining expression increases with \(b\) and with
\(r\ge3\).  Thus (24) is impossible whenever

\[
                     9-c+\max(0,3-k)>0.                    \tag{26}
\]

Equivalently, the proved value-core route **V** is

\[
\boxed{
\begin{array}{c|c}
k=p-h&\text{Wronskian range}\ \hline
1&c\le10,\\
2&c\le9,\\
k\ge3&c\le8.
\end{array}}                                                \tag{27}
\]

This must be combined with \(c\ge h+1\) and (13).  Since \(h\ge8\), the
last line of (27) is empty.  The only parameter triples on which V can add
anything are

\[
 (h,p,c)=(8,9,9),(8,9,10),(8,10,9),(9,10,10).              \tag{28}
\]

The strictness in (26) matters.  Equality is not a contradiction and is
left open by this method.

## 8. The exact incremental V list and low-base census

Apply the routes in the order H, S, C, L, Q, V.  The profiles newly closed
by V are exactly the following.  Exponential notation records numbers of
value classes, so \(3^4 2^2 1^3\) means four triple classes, two double
classes, and three singleton classes.

\[
\begin{array}{c|l}
(h,p)&\text{profiles newly routed by V}\ \hline
(8,9)&
3^4 2^2 1^3,\ 3^3 2^4 1^2,\ 3^3 2^3 1^4,\
3^2 2^6 1,\ 3^2 2^5 1^3,\ 3 2^8,\ 3 2^7 1^2,\ 2^9 1;\\
(8,10)&3^4 2^3 1^2,\ 3^3 2^5 1,\ 3^2 2^7;\\
(9,10)&
4^3 2^2 1^5,\ 4^2 3 2^3 1^4,\ 4^2 2^5 1^3,\
4 3^3 2^2 1^4,\ 4 3^2 2^4 1^3,\ 4 3 2^6 1^2,\
4 2^8 1,\ 3^4 2^3 1^3,\ 3^3 2^5 1^2,\ 3^2 2^7 1,\ 3 2^9.
\end{array}                                                  \tag{29}
\]

There is no incremental V profile at any other \((h,p)\).

For orientation, the exact category counts in the first four rows
\(p=h+1,\ldots,h+4\) are:

\[
\begin{array}{cc|rrrrrrr|r}
h&p&H&S&C&L&Q&V&R&D\\ \hline
8&9 &190&218&17&10&11&8 &35 &1\\
8&10&263&270&22&14&12&3 &42 &1\\
8&11&356&338&22&16&13&0 &46 &1\\
8&12&480&411&28&21&15&0 &46 &1\\
9&10&267&355&28&14&12&11&104&1\\
9&11&364&452&30&16&13&0 &126&1\\
9&12&491&555&38&22&15&0 &133&1\\
9&13&656&689&44&27&20&0 &138&1\\
10&11&368&593&33&16&13&0&231&1\\
10&12&499&741&43&22&15&0&254&1\\
10&13&667&923&49&27&20&0&271&1\\
10&14&887&1137&59&36&26&0&290&1\\
11&12&503&912&49&22&15&0&456&1\\
11&13&675&1151&58&27&20&0&504&1\\
11&14&898&1426&71&36&26&0&552&1\\
11&15&1184&1769&83&44&36&0&601&1\\
12&13&679&1427&61&27&20&0&795&1\\
12&14&906&1785&76&36&26&0&888&1\\
12&15&1195&2224&89&44&36&0&976&1\\
12&16&1569&2739&111&56&47&0&1081&1.
\end{array}                                                  \tag{30}
\]

Here D is the all-distinct profile, already closed by the uniform
all-distinct theorem, and R means genuinely residual after the routes of
this note.  The large R column is the important conclusion of the census.

There is also a finite-base description for each fixed \(h\).  H, S, C,
L, and Q persist after adjoining a new value class.  For a newly adjoined
zero singleton, use the old no-zero moving witness and leave the new class
untouched; all old anchors remain nonzero.  Therefore any residual
collision profile can be reduced, while preserving one repeated class, to
a profile of total size

\[
                         2h+3\le M\le3h+1.                  \tag{31}
\]

Indeed, outside this window a whole class of size at most \(h-1\) can be
removed while remaining feasible.  If the smaller profile had an H/S/C/L/Q
witness, that witness would lift back, a contradiction.  V is deliberately
not used in this persistence argument: its class bound (27) is not stable
under adjoining a class.

Let \({\cal B}_h\) be the collision profiles in (31) not routed by the five
persistent methods H/S/C/L/Q.  The numbers of base seeds at successive
\(k=1,\ldots,h-1\) are

\[
\begin{array}{c|l}
h& |{\cal B}_h|\text{ for }k=1,\ldots,h-1\\ \hline
8&43,45,46,46,44,44,40\\
9&115,126,133,138,140,140,140,140\\
10&231,254,271,290,302,318,332,349,363\\
11&456,504,552,601,650,704,757,815,872,930\\
12&795,888,976,1081,1182,1299,1412,1540,1665,1804,1931.
\end{array}                                                  \tag{32}
\]

The V profiles in (29) are included in these base-seed counts because V
does not persist upward.  Equations (11)--(12) give an exact enumerator for
\({\cal B}_h\) at every \(h\), rather than only the displayed rows.

## 9. Persistent method gaps

Two exact families make clear why the present tools do not close the
higher collision layers.

### 9.1 Every double/single profile

For \(h\ge8\), a selection using three anchors and two further classes can
take at most \(3+2+2=7<h\) labels.  Thus no double/single profile can use C,
L, or Q.  Two classes take at most four labels, so H and S also fail.
The V range contains exactly one such profile.  Consequently the exact
double/single frontier is

\[
 \boxed{(2^d,1^{M-2d}),\qquad
 1\le d\le\lfloor M/2\rfloor,}                              \tag{33}
\]

all residual except

\[
                    (h,p;d,s)=(8,9;9,1),                   \tag{34}
\]

which is the final profile in the first row of (29).  The all-singleton
case \(d=0\) is not a collision and is already closed separately.

### 9.2 A broader top-two cone

Suppose a collision profile satisfies

\[
                         \lambda_1+\lambda_2\le h-4.        \tag{35}
\]

Then H fails, S fails, and even the largest possible moving selection has

\[
                a+f+j\le3+\lambda_1+\lambda_2\le h-1.      \tag{36}
\]

Thus C, L, and Q cannot apply.  Every such profile is residual unless it
lies in the isolated V list (29).  In particular, for \(k\ge3\), where V
has empty range, (35) is an unconditional persistent gap for every audited
method.  Appending further low-multiplicity classes while preserving (35)
produces arbitrarily large residual families.

The three boundary bands
\(\lambda_1+\lambda_2\in\{h-3,h-2,h-1\}\), together with the no-singleton
edge at sum \(h\), are governed exactly by the candidate test (11)--(12).
They are not declared closed.

## 10. Legal Hermite cores inside every residual

Although not every residual has \(h\) distinct value classes, every
residual does have a legal selection of \(h\) labels with a sharply bounded
number \(m\) of represented classes.  If \(m_{\min}(\lambda)\) denotes the
least such number, then

\[
                 \boxed{3\le m_{\min}(\lambda)\le h-1}      \tag{37}
\]

for every profile in R.

The lower bound is exact: a legal selection represented in one or two
classes would be route S.  To prove the upper bound, first suppose there is
a singleton class.  Leave one singleton untouched, take two labels from a
repeated class, and fill the other \(h-2\) selected slots without using the
guard singleton.  This represents at most \(h-1\) classes.  If there is no
singleton, choose two distinct repeated classes \(A,B\), take two labels
from \(A\), and take \(\lambda_B-1\) labels from \(B\), leaving a singleton
mate.  Fill the remaining slots arbitrarily.  Since
\(2\le\lambda_B\le h-1\), the resulting number of represented classes is
at most

\[
                 2+(h-\lambda_B-1)=h-\lambda_B+1\le h-1.   \tag{38}
\]

Both ends of (37) occur.  The sparse profile \((2,1^{M-2})\) has
\(m_{\min}=h-1\), so there is no uniform improvement to \(h-2\).  At the
first unresolved parameter pair \((h,k)=(8,1)\), the distribution of
\(m_{\min}\) among the 35 residual profiles is

\[
\begin{array}{c|rrrrr}
m_{\min}&3&4&5&6&7\\ \hline
\#\text{ profiles}&19&11&2&2&1.
\end{array}                                                  \tag{39}
\]

The smallest profile left by the routes audited in this note, measured
first by \((h,k)\) and then by the number of value classes, is uniquely

\[
             \boxed{(h,k;\lambda)=(8,1;(4,3,3,3,3,3)).}    \tag{40}
\]

It has only six value classes, so the value-core exchange cannot start.
Nevertheless it has a legal three-class Hermite selection: take three
labels from the four-class, three from one triple, and two from another
triple.  The four-class leaves the required singleton row and (6) gives a
nonzero constant residual.  The companion
[common-pole closure](live-three-zero-eighth-split-433333-common-pole-closure.md)
now eliminates (40) by comparing the fully selected triple role at the
common pole.  It is retained here to make the baseline census and the
checker category R reproducible.  At the opposite extreme,
\((2,1^{17})\) at the same \((h,k)\) witnesses the sharp upper edge
\(m_{\min}=7\).

## 11. Audit

[verify_live_three_zero_higher_split_collision_frontier.py](../computations/verify_live_three_zero_higher_split_collision_frontier.py)
checks the Hermite degrees, the exact value-core legality equivalence, the
type-compressed C/L/Q witness search against literal indexed searches, the
possible zero singleton, the high-order common-pole vanishing-sequence
weight, the gcd-corrected Wronskian inequality, every profile in (29), all
counts in (30)--(32), the persistent families (33)--(36), the sharp core
bound (37), and the smallest baseline profile (40).  Its output labels R as
unresolved by exactly the route set audited here; later companion notes may
and do shrink that baseline frontier.
