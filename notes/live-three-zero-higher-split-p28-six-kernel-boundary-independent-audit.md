# Independent audit: the \(p=28\) selected six-kernel boundary

## 1. Audit verdict and scope

The claims in
[the primary frontier note](live-three-zero-higher-split-p28-six-kernel-boundary.md)
pass an independent reconstruction.  In particular:

* \(p=28\) is the first numerical boundary at which a selected kernel can
  have dimension six;
* the six equality splits, all six census totals, the uniform 344-profile
  \(d\leq2\) subledger, and the nine residual parameter tuples are exact;
* every candidate is presently labelled \(R\), and every individual
  \(H/S/C/L/Q/V\) test in the underlying route classifier fails;
* the cubic, quartic, and quintic common-lift arguments have the claimed
  Wronskian gaps and pair-intersection thresholds; and
* the reduction table counts profiles for which one explicitly exhibited
  formal selection has kernel dimension at most five.

The last item is only a **dimension-drop frontier**.  Neither a
five-dimensional selected kernel nor any of the counts below rules out its
collision profile.  No \(p=18\) or \(p=19\) closure theorem is silently
transported to \(p=28\).

## 2. Selected and relation Wronskians

For \(d\) role-two layers and

\[
                  s=h+2-2d
\]

role-one layers, a hypothetical \(q\)-space has forced selected-row weight

\[
 d(q-2)+s(q-1)+\max(0,q-k),
\]

and degree cap

\[
 q\bigl((h+3-d)+1-q\bigr).
\]

Their difference is independent of \(d\):

\[
 q^2-2q-h-2+\max(0,q-k).                       \tag{1}
\]

At \(q=6\), (1) is (22-h+\max\(0,6-k\)).  It is positive for
every \(p=h+k\leq27\).  At \(p=28\), it vanishes precisely at

\[
 (h,k)=(22,6),(23,5),(24,4),(25,3),(26,2),(27,1).
\]

At each of these splits the \(q=7\) excess is

\[
 33-h+(7-k)=40-p=12.
\]

The gap is strictly increasing for all larger \(q\), so this really gives
the upper bound six, not merely the exclusion of dimension seven.

Equality for \(q=6\) gives selected local weights four at every role-two
value, five at every role-one value, and \(6-k\) at the common pole.  Their
sum equals the complete Wronskian degree cap, which verifies the rigid
Wronskian displayed in the primary note.

The relation space has dimension \(6-2=4\) and lies in
\(\mathbb C[z]_{\leq c-4}\).  Its truncated-mass condition is

\[
                  \sum_i\min(m_i,4)\geq28.               \tag{2}
\]

Because the actual complementary mass is exactly 28, (2) holds exactly
when every complementary part is at most four.  Its forced relation
Wronskian weight is then

\[
 \sum_i(4-m_i)=4c-28=4\bigl((c-4)+1-4\bigr),
\]

again the full cap.  The standard exact-jet correction was checked for
every relevant row dimension, multiplicity, and possible gcd order; it is
always nonnegative.  Thus common factors cannot weaken any of these gap
arguments.

Since a formal role-one/role-two selection changes only original parts of
sizes one, two, or three, an original part of size at least five would
remain in the complement and violate (2).  The candidates therefore have
exactly the form

\[
 4^e3^a2^b1^{h+u},\qquad 4e+3a+2b+u=30.                 \tag{3}
\]

## 3. Literal census and route status

The independent checker enumerates every multiplicity-count solution of
(3), constructs every literal choice of \(x\) exact doubles and
\(t\in\{0,1\}\) exact triples, and retains it exactly when

\[
        0\leq h+2-2(x+t)\leq h+u.                       \tag{4}
\]

The already separated all-singleton \(D\)-profile is deleted.  This gives

\[
\begin{array}{c|rrrrrr}
h&22&23&24&25&26&27\\ \hline
\#&824&824&872&872&920&920.
\end{array}
\]

For every choice, the checker reconstructs the actual complementary
multiset, verifies mass 28 and maximum part four, and checks equality in
both Wronskian caps above.  It then evaluates the route classifier branch
by branch: the profile is not \(D\) or \(H\), has no \(S\) witness, fails
each \(C,L,Q\) moving-family test, and fails the \(V\) value-core test.
The final status counter at every split is therefore exactly

\[
                         R^{\#}.
\]

Restricting the literal selections in (4) to \(x+t\leq2\) independently
reproduces the three applicability alternatives in the primary note.  It
gives 344 profiles at every split, with quartic-count distribution

\[
\begin{array}{c|rrrrrrrr}
e&0&1&2&3&4&5&6&7\\ \hline
\#&101&79&60&44&29&18&10&3.
\end{array}
\]

## 4. Common-lift arithmetic

### 4.1 Moving singleton

Restoring the moving singleton produces \(P+C\) baseline classes of mass
29 and degree \(P+C-2\).  A hypothetical five-space has forced weight

\[
                    5(P+C)-29
\]

and cap

\[
                    5(P+C-6)=5(P+C)-30.
\]

The excess is exactly one, so the common kernel has dimension at most
four.  If \(m\) active transported four-spaces fill it, every member is
divisible by \(m\) pairwise coprime cubics

\[
                     f_q=(z-q)^2(z+q).
\]

After division, a four-space needs residual degree at least three.  Hence

\[
                    3m\leq P+C-5.                         \tag{5}
\]

Putting \(m=P\) shows that not all pool choices can be active when
\(C\leq2P+4\).

All legal moving-singleton choices were exhaustively compared.  Selecting
one more exact double changes \(2P-C\) by \(+5\), while selecting the one
allowed exact triple changes it by \(+4\).  Thus the primary greedy choice
really maximizes the test, including both parities of \(h\); it is not just
a convenient heuristic.

### 4.2 Moving triple and double

Restoring either a moving triple or a moving double raises the baseline
mass to 30.  In the triple case the quartic transport

\[
                    B_x=(z-x)^2(z+x)^2
\]

puts every transported four-space in degree at most \(c\).  A common
six-space is on equality, while a seven-space has excess 12, so the common
kernel has dimension at most six.  Two active four-spaces must intersect
in dimension at least two.  Exact coefficient-space rank calculations for
two coprime quartics give

\[
 \dim\left(B_x\mathbb C[z]_{\leq c-4}
       \cap B_y\mathbb C[z]_{\leq c-4}\right)
                    =\max(c-7,0).
\]

This is at most one exactly when \(c\leq8\).

For a moving double, the quintic transport

\[
                    g_i=(z-i)^3(z+i)^2
\]

has common degree \(c+1\).  The analogous exact rank calculation is

\[
 \dim\left(g_i\mathbb C[z]_{\leq c-4}
       \cap g_j\mathbb C[z]_{\leq c-4}\right)
                    =\max(c-8,0),
\]

so the contradiction range is exactly \(c\leq9\).

The local transports were also checked directly: a square kills a full
first jet and satisfies

\[
 \left((z-x)^2R\right)'''(x)=6R'(x),
\]

while a cube kills the complete two-jet.  Structural nonopposition makes
the transports for distinct moving values coprime, including the possible
zero member of a singleton pool.

For applying the last two tests, “legal choice” includes the conditions
implicit in the primary reduction table: a moving-triple pool has
\(a\geq2\), a moving-double pool has \(b-x\geq2\), and the selected
singleton count is nonnegative and available.  The independent enumeration
uses all and only such choices.

## 5. Reduction ledger and residual cores

Applying the tests sequentially reproduces the full table:

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
\end{array}
\]

On the \(d\leq2\) subledger, the singleton test supplies 333 explicit
dimension drops and the triple test supplies two more.  The double test
adds none.  The nine unreduced tuples are exactly

\[
\begin{aligned}
 &(0,10,0,0),(0,10,1,-2),\\
 &(2,7,0,1),(2,7,1,-1),\\
 &(3,6,0,0),(3,6,1,-2),\\
 &(7,0,0,2),(7,0,1,0),(7,0,2,-2).
\end{aligned}
\]

Restoring the harmless selected-double variants gives exactly the four
natural common baselines

\[
                  3^{10},\qquad 4^2 3^7 1,\qquad
                  4^3 3^6,\qquad 4^7 1.
\]

These are the correct next equality configurations to study, but their
appearance is not itself a contradiction.

## 6. Reproducible audit

[verify_live_three_zero_higher_split_p28_six_kernel_boundary_independent_audit.py](../computations/verify_live_three_zero_higher_split_p28_six_kernel_boundary_independent_audit.py)
does not import the primary \(p=28\) checker.  It performs the independent
enumeration, branch-level classifier audit, exact Wronskian arithmetic,
greedy optimization check, symbolic local-jet checks, coefficient-rank
intersection checks, complete reduction ledger, and residual-baseline
reconstruction.

The only issue found in the primary note is editorial: equation (20) has
the TeX text `,quad` where `,\quad` was intended.  It does not affect any
definition or computation.
