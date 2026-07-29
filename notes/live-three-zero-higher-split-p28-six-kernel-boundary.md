# Higher splits: the first selected six-kernel boundary at \(p=28\)

## 1. Scope and result

Put

\[
                 p=h+k,\qquad h\geq13,\quad k\geq1.
\]

For a formal selection with \(d\) repeated role-two layers and
\(s=h+2-2d\) singleton role-one layers, let \(K\) be the selected-row
kernel.  The selected-row Wronskian inequality for
\(q=\dim K\) is

\[
 q^2-2q-h-2+\max(0,q-k)\leq0.                         \tag{1}
\]

This note identifies the first point at which (1) permits \(q=6\), gives
the exact collision-profile census there, and proves three common-lift
lemmas which force a return to a kernel of dimension at most five on most
of that boundary.  It is a frontier theorem, not a closure of the
collision stratum.

**Theorem 1.1 (first six-kernel boundary).**  A selected six-dimensional
kernel is impossible for \(p\leq27\).  At \(p=28\) it is possible in the
Wronskian count only for

\[
        (h,k)=(22,6),(23,5),(24,4),(25,3),(26,2),(27,1), \tag{2}
\]

and is exactly on equality there.  A seven-dimensional kernel is still
impossible, with Wronskian excess twelve.

The full exact profile census in the six-kernel branch contains

\[
\begin{array}{c|rrrrrr}
h&22&23&24&25&26&27\\ \hline
\text{profiles}&824&824&872&872&920&920.
\end{array}                                                \tag{3}
\]

Every one is still labelled \(R\) by the audited
\(H/S/C/L/Q/V\) route registry.  The older \(d\leq2\) equality-ledger
slice contains 344 profiles, independently of the split.

The common-lift lemmas below do not themselves rule out a profile.  They
prove that an explicit family of formal selections cannot consist
entirely of six-dimensional selected kernels.  Thus at least one member
of that family has dimension at most five, where the completed
\(p=18,19\) mechanisms become the relevant model.

## 2. Why the first boundary is \(p=28\)

At \(q=6\), the left side of (1) is

\[
                   22-h+\max(0,6-k).                       \tag{4}
\]

If \(k\leq6\), this equals \(28-p\).  If \(k\geq6\) and
\(p\leq27\), then \(h\leq21\), so it is again strictly positive.
Equality at \(p=28\) gives exactly (2).  At those six splits, the
\(q=7\) left side is

\[
                   33-h+(7-k)=40-p=12.                     \tag{5}
\]

Consequently every selected kernel has dimension at most six.

At equality, all gcd corrections in (1) vanish.  If the selected repeated
values are \(x\), the selected singleton values are \(r\), and the common
pole is \(-\mu\), then a six-space has the rigid Wronskian

\[
 \operatorname{Wr}(K)=C_K (z+\mu)^{6-k}
       \prod_x(z+x)^4\prod_r(z+r)^5.                       \tag{6}
\]

The relation-space theorem gives a four-space

\[
              {\cal S}\subseteq\mathbb C[z]_{\leq c-4}.    \tag{7}
\]

If the complementary multiplicities are \(m_1,\ldots,m_c\), its
truncated-mass inequality is

\[
                     \sum_i\min(m_i,4)\geq28.              \tag{8}
\]

The complementary mass itself is \(p=28\).  Hence equality is necessary,
every \(m_i\leq4\), and the relation Wronskian is also rigid:

\[
             \operatorname{Wr}({\cal S})=C_{\cal S}
                  \prod_i(z-a_i)^{4-m_i}.                  \tag{9}
\]

No original class of multiplicity at least five can be changed by a
formal role-one/role-two selection.  Therefore every six-kernel candidate
profile has the unique form

\[
          \boxed{4^e3^a2^b1^{h+u}},\qquad
                    4e+3a+2b+u=30.                         \tag{10}
\]

## 3. Exact census

A formal selection chooses \(x\) exact doubles and
\(t\in\{0,1\}\) exact triples in role two.  Put \(d=x+t\).  It is legal
at the level used here exactly when

\[
\begin{gathered}
 0\leq x\leq b,\qquad 0\leq t\leq\min(1,a),\\
 0\leq h+2-2d\leq h+u.                                  \tag{11}
\end{gathered}
\]

Equations (10)--(11), with the already separated all-singleton profile
deleted, give the counts in (3).  The count changes every two values of
\(h\), because the largest allowed \(d\) is
\(\lfloor(h+2)/2\rfloor\).

If one retains the \(d\leq2\) restriction of the \(p=18,19\) equality
ledger, (11) reduces to

\[
\begin{array}{ll}
u\geq2;&\text{or}\\
u\geq0\ \text{and}\ a+b\geq1;&\text{or}\\
u\geq-2\ \text{and}\bigl(b\geq2\ \text{or}\ (a\geq1,b\geq1)\bigr).
\end{array}                                                \tag{12}
\]

There are exactly 344 solutions, with the following quartic-count
distribution:

\[
\begin{array}{c|rrrrrrrr}
e&0&1&2&3&4&5&6&7\\ \hline
\#&101&79&60&44&29&18&10&3.
\end{array}                                                \tag{13}
\]

## 4. A moving-singleton active-count lemma

The numerical phenomenon is parameter-uniform.  Put \(r=q-2\), and
consider the first row-relation mass threshold

\[
                         p=r(r+3).                           \tag{14a}
\]

Assume every complementary multiplicity is at most \(r\), as equality in
the truncated-mass bound requires.  The moving-singleton transport carries
an \(r\)-dimensional relation space into a common baseline of mass
\(p+1\) and polynomial degree \(P+C-2\).  A hypothetical
\((r+1)\)-space in that common kernel has forced weight minus Wronskian
cap

\[
 (r+1)(P+C)-(p+1)
 -(r+1)(P+C-r-2)=1.                                      \tag{14b}
\]

Thus the common kernel has dimension at most \(r\).  If \(m\) moving
selections have the maximal selected-kernel dimension \(r+2\), their
transported \(r\)-spaces all fill the common kernel, so its gcd contains
their \(m\) coprime cubics.  The quotient must still contain an
\(r\)-space.  Consequently

\[
                    \boxed{3m\leq P+C-r-1}.                 \tag{14c}
\]

The case below is \(r=4\).  Besides explaining the otherwise isolated
one-unit excess in (16)--(17), (14b)--(14c) recover the same dimension
shift behind the completed \(p=18\) five-kernel ledger when \(r=3\).

Fix all selected repeated layers and all but one selected original
singleton layer.  Let the remaining selected singleton range over a pool
\(P\) of distinct original singleton values.  Let \(C\) be the number of
fixed complementary value classes.  For each \(q\) in the pool whose
selected kernel is six-dimensional, its relation four-space transports
by

\[
                      f_q=(z-q)^2(z+q)                       \tag{14}
\]

to a four-space

\[
 f_q{\cal S}_q={\cal T}_q\subseteq{\cal K}
       \subseteq\mathbb C[z]_{\leq P+C-2}.                 \tag{15}
\]

The common baseline has mass \(29\): it has all \(P\) pool singletons
and the \(C\) fixed classes, each of multiplicity at most four.  A
hypothetical five-space in \({\cal K}\) has forced weight

\[
 4P+\sum_{i=1}^C(5-m_i)
       =5(P+C)-29,                                        \tag{16}
\]

while its degree cap is

\[
             5\bigl((P+C-2)+1-5\bigr)=5(P+C)-30.          \tag{17}
\]

The exact-row gcd correction is nonnegative, so
\(\dim{\cal K}\leq4\).  If even one pool selection has dimension six,
its transported four-space fills \({\cal K}\).  If \(m\) pool selections
have dimension six, every member of \({\cal K}\) is divisible by the
product of their \(m\) pairwise coprime cubics.  A four-space remaining in
degree \(P+C-2-3m\) requires that degree to be at least three.  Thus:

**Lemma 4.1 (active singleton bound).**

\[
                      \boxed{3m\leq P+C-5}.                \tag{18}
\]

In particular, not all \(P\) moving selections can have dimension six
whenever

\[
                          C\leq2P+4.                        \tag{19}
\]

For (10), choose as many selected exact doubles as possible while keeping
one selected singleton, then select one triple if a role remains.  More
precisely, put

\[
 d_{\max}=\left\lfloor{h+1\over2}\right\rfloor,\quad
 x=\min(b,d_{\max}),\quad
 t=\mathbf1_{\{a>0,\ x<d_{\max}\}},                       \tag{20}
\]

and

\[
                 P=u-1+2(x+t),\qquad C=e+a+b-x.            \tag{21}
\]

Whenever \(P\geq1\), this is the optimal choice for (19): an additional
selected double improves \(2P-C\) by five and a selected triple improves
it by four.

## 5. The shifted quartic and quintic intersection lemmas

There is a uniform form here as well.  For \(r\geq3\), at the threshold
\(p=r(r+3)\), restoring a moving triple or double raises the common
baseline mass to

\[
                         p+2=(r+1)(r+2).                     \tag{21a}
\]

The transported relation spaces have dimension \(r\).  The common
kernel has dimension at most \(r+2\): an \((r+2)\)-space is on exact
Wronskian equality, while an \((r+3)\)-space has excess \(2(r+2)\).
Hence two transported spaces meet in dimension at least \(r-2\).
The coprime-quartic pair ambient has dimension
\(\max(c-7,0)\), and the coprime-quintic pair ambient has dimension
\(\max(c-8,0)\).  Therefore at most one moving selection can have maximal
dimension whenever

\[
 \boxed{\begin{array}{c|c}
 \text{quartic triple transport}&c\leq r+4,\\
 \text{quintic double transport}&c\leq r+5.
 \end{array}}                                               \tag{21b}
\]

For \(r=4\), these thresholds are eight and nine.

The moving-triple lift from the completed \(p=19\) ledger becomes even
simpler on the six-kernel boundary.  Let \(c\) be the number of classes
in a selected complement.  For an active moving triple \(x\), the exact
quartic transport gives

\[
 B_x=(z-x)^2(z+x)^2,\qquad
 B_x{\cal S}_x={\cal T}_x\subseteq{\cal K}
                    \subseteq\mathbb C[z]_{\leq c}.        \tag{22}
\]

The common baseline restores the selected simple class to a triple and
has mass thirty.  A seven-space exceeds its Wronskian cap by twelve, so
\(\dim{\cal K}\leq6\).  Two active transported four-spaces must therefore
meet in dimension at least two.  On the other hand, coprimality gives

\[
 B_x\mathbb C[z]_{\leq c-4}\cap
 B_y\mathbb C[z]_{\leq c-4}
       =B_xB_y\mathbb C[z]_{\leq c-8},                    \tag{23}
\]

whose dimension is at most one for \(c\leq8\).

**Lemma 5.1 (moving-triple dimension drop).**  If \(c\leq8\), at most one
member of a moving-triple pool can have a six-dimensional selected
kernel.

There is a direct shifted version of the \(p=19\) singleton pair-line
construction.  For an active moving double \(i\), transport by

\[
 g_i=(z-i)^3(z+i)^2,qquad
 g_i{\cal S}_i={\cal T}_i\subseteq{\cal K}
                  \subseteq\mathbb C[z]_{\leq c+1},        \tag{24}
\]

where \(c\) is again the selected-complement class count.  The restored
baseline has mass thirty, so \(\dim{\cal K}\leq6\).  Two active
four-spaces meet in dimension at least two, whereas

\[
 g_i\mathbb C[z]_{\leq c-4}\cap
 g_j\mathbb C[z]_{\leq c-4}
       =g_ig_j\mathbb C[z]_{\leq c-9}                     \tag{25}
\]

has dimension at most one for \(c\leq9\).

**Lemma 5.2 (moving-double dimension drop).**  If \(c\leq9\), at most one
member of a moving-double pool can have a six-dimensional selected
kernel.

This is precisely the dimension-shifted p=19 pair-line mechanism: the
lower intersection bound rises from one to two, so the low-degree cases
contradict coprimality before a clique interpolation is needed.

For parameter bookkeeping, selecting one moving triple and \(x\) fixed
doubles gives

\[
       u+2x\geq0,\qquad c=e+a+b+u+x.                       \tag{26}
\]

Selecting one moving double, \(x\) fixed doubles, and
\(t\in\{0,1\}\) fixed triples gives

\[
 u+2x+2t\geq0,qquad
 c=e+a+b+u+x+2t-1.                                       \tag{27}
\]

The corresponding pool sizes are \(a\) and \(b-x\), respectively.

## 6. Exact reduction table and remaining equality cores

Apply Lemma 4.1 using (20)--(21), then Lemmas 5.1--5.2 using every legal
choice in (26)--(27).  The exact sequential counts are

\[
\begin{array}{c|r|r|r|r|r|r}
h&\text{candidates}&\text{singleton}&\text{new triple}&
 \text{new double}&\text{union}&\text{remain}\\ \hline
22&824&676&12&17&705&119\\
23&824&719&12& 7&738& 86\\
24&872&719&13&17&749&123\\
25&872&762&13& 7&782& 90\\
26&920&762&14&17&793&127\\
27&920&805&14& 7&826& 94.
\end{array}                                                \tag{28}
\]

Again, the union column counts profiles for which an explicit selected
kernel has dimension at most five; it is not a profile closure count.

On the uniform \(d\leq2\) subledger, Lemma 4.1 reduces 333 of the 344
profiles.  Lemma 5.1 reduces two more.  The nine profiles not reduced by
these common-lift inequalities are

\[
\boxed{\begin{aligned}
 &(e,a,b,u)=(0,10,0,0),(0,10,1,-2),\\
 &(2,7,0,1),(2,7,1,-1),\\
 &(3,6,0,0),(3,6,1,-2),\\
 &(7,0,0,2),(7,0,1,0),(7,0,2,-2).
\end{aligned}}                                             \tag{29}
\]

Their natural saturated common baselines are, respectively, the
all-triple, quartic--triple, and all-quartic Schubert configurations.  The
next concrete algebraic targets are therefore the six-spaces with
baseline profiles

\[
                 3^{10},\qquad 4^2 3^7 1,qquad
                 4^3 3^6,\qquad 4^7 1,                    \tag{30}
\]

The first three have mass thirty and arise from moving-triple transport;
the last has mass twenty-nine and is the one-point moving-singleton
baseline.  The harmless selected-double variants restore to the same
displayed baselines.  These are a much smaller equality frontier than an
order-by-order \(p=28\) census.

## 7. Exact audit

[verify_live_three_zero_higher_split_p28_six_kernel_boundary.py](../computations/verify_live_three_zero_higher_split_p28_six_kernel_boundary.py)
checks (1)--(13), reconstructs every formal selection and all census
counts, confirms that every candidate is still \(R\) in the current route
classifier, audits the three common-kernel Wronskian gaps and coprime
intersection thresholds, reproduces (28), and verifies the nine-profile
frontier (29).

The
[independent audit](live-three-zero-higher-split-p28-six-kernel-boundary-independent-audit.md)
reconstructs the gap formula, every census and route-classifier branch,
the transport and intersection arithmetic, the complete reduction ledger,
and the scope guard that a dimension drop is not a profile closure.
