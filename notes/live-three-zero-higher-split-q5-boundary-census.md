# Higher splits: exact \(q=5\) boundary census

## 1. Uniform profile test

Let \(h\geq13\), \(p=h+k\), and let

\[
 \lambda=(\lambda_1,\ldots,\lambda_C),\qquad
 \sum_i\lambda_i=p+h+2                                  \tag{1}
\]

be a no-extra-singular collision profile which admits a formal selection
with \(d\in\{0,1,2\}\).  The exact applicability test is

\[
\boxed{\begin{aligned}
&n_1\geq h+2;\quad\text{or}\\
&n_1\geq h\quad\text{and}\quad(n_2\geq1\ \text{or}\ n_3\geq1);
   \quad\text{or}\\
&n_1\geq h-2\quad\text{and}\quad
 (n_2\geq2\ \text{or}\ (n_2\geq1,n_3\geq1)),
\end{aligned}}                                           \tag{2}
\]

where \(n_j\) counts parts equal to \(j\).  The last line reflects the
rule that at most one selected role-two class may be an exact triple.

Define the high-multiplicity excess

\[
                         E(\lambda)
                    =\sum_{\lambda_i\geq4}(\lambda_i-3). \tag{3}
\]

Selecting singleton, double, or triple classes does not change any part
of size at least four.  Hence every \(d\leq2\) selection has complementary
profile \(A\) satisfying

\[
          \sum_{a\in A}\min(\operatorname{mult}_A(a),3)
                              =p-E(\lambda).             \tag{4}
\]

Assume also that the selected-row kernel has dimension at most five.
Pair drops give dimension at least four.  The four-dimensional branch is
impossible by
[the low-role incidence theorem](live-three-zero-higher-split-low-role-selected-lift-incidence-closure.md),
while the five-dimensional branch requires the capped complementary mass
to be at least eighteen by
[the row-relation bound](live-three-zero-higher-split-row-relation-truncated-mass-bound.md).
Therefore

\[
             \boxed{E(\lambda)>p-18\quad\Longrightarrow\quad
                    \lambda\text{ is impossible}.}      \tag{5}
\]

This is an exact consequence for every profile satisfying (2), not a
heuristic selection score.

## 2. The first boundary \(p=18\)

At

\[
             (h,k)=(13,5),(14,4),(15,3),(16,2),(17,1), \tag{6}
\]

the \(q=5\) selected-row Wronskian bound is at equality.  The \(q=6\)
bound is still strict, so the kernel has dimension four or five.  Formula
(5) eliminates every applicable profile containing a part at least four.

Applied after the exact \(H/S/C/L/Q/V\) frontier, the finite census is

\[
\begin{array}{c|c|r|r|r|r}
h&k&R&\text{applicable }d\leq2&
 \text{closed by (5)}&\text{survive}\\ \hline
13&5&2174&467&417&50\\
14&4&3255&542&492&50\\
15&3&4836&612&562&50\\
16&2&6752&656&606&50\\
17&1&9365&699&649&50
\end{array}                                               \tag{7}
\]

Here \(R\) has exactly the meaning used by the frontier checker:
unresolved by its audited route set.  The new column is sequentially
relative to that baseline.

The fifty survivors have a uniform symbolic description.  They are

\[
                         3^a2^b1^{\,h+u},\qquad
                         3a+2b+u=20,                     \tag{8}
\]

subject to at least one of

\[
\begin{array}{ll}
u\geq2;&\\
u\geq0\ \text{and}\ a+b\geq1;&\\
u\geq-2\ \text{and}\ (b\geq2\ \text{or}\ (a\geq1,b\geq1)).
\end{array}                                               \tag{9}
\]

The all-singleton solution \((a,b,u)=(0,0,20)\) is the already separated
\(D\) profile, not an \(R\) profile.  Equations (8)--(9), with that one
deletion, contain exactly fifty triples \((a,b,u)\).

## 3. Equality rigidity at \(p=18\)

Every survivor in (8) is on equality in both Wronskian estimates.  Fix
one of its formal selections, with \(d\) repeated and
\(s=h+2-2d\) singleton layers.  All gcd corrections in the selected
five-space \(K\) must vanish, and its Wronskian is fixed up to a nonzero
scalar:

\[
 \operatorname{Wr}(K)=C_K
 (z+\mu)^{\,5-k}
 \prod_{\text{selected repeated }x}(z+x)^3
 \prod_{\text{selected singleton }r}(z+r)^4.            \tag{10}
\]

Indeed, the forced degree is

\[
 3d+4s+(5-k)=5(h-d-1)
       =5\bigl((h+3-d)+1-5\bigr),                        \tag{11}
\]

which is the full polynomial Wronskian cap.

The complementary relation three-space \(\mathcal S\) is equally rigid.
If its complementary profile has \(n_1,n_2,n_3\) parts of sizes one,
two, and three, then

\[
 \operatorname{Wr}(\mathcal S)=C_{\mathcal S}
 \prod_{m_i=1}(z-a_i)^2
 \prod_{m_i=2}(z-a_i),                                  \tag{12}
\]

because

\[
 2n_1+n_2=3c-18=3\bigl((c-4)+1-3\bigr).                 \tag{13}
\]

Thus the fifty symbolic families are not featureless leftovers: any
escape must realize two simultaneously saturated, gcd-free linear series,
linked by the exact differential operator in the row-relation theorem.
This is the concrete equality branch on which a multi-drop or
Wronski-map attack should focus.

## 4. The next boundary \(p=19\)

The same calculation at

\[
 (h,k)=(13,6),(14,5),(15,4),(16,3),(17,2),(18,1)        \tag{14}
\]

gives

\[
\begin{array}{c|c|r|r|r|r}
h&k&R&\text{applicable }d\leq2&
 \text{closed by (5)}&\text{survive}\\ \hline
13&6&2407&548&454&94\\
14&5&3626&643&549&94\\
15&4&5446&737&643&94\\
16&3&7625&807&713&94\\
17&2&10654&858&764&94\\
18&1&14247&901&807&94
\end{array}                                               \tag{15}
\]

Now (5) permits high excess at most one.  Thus the ninety-four survivors
are exactly the \(R\) profiles of the two forms

\[
 3^a2^b1^{\,h+u},\qquad
 4\,3^a2^b1^{\,h+u},                                    \tag{16}
\]

with respectively

\[
 3a+2b+u=21,\qquad 4+3a+2b+u=21,                        \tag{17}
\]

and the applicability alternatives (9).  Again the sole all-singleton
solution is \(D\), not \(R\).

More generally, at \(p=18+e\), a \(q=5\) survivor can have only

\[
                         E(\lambda)\leq e.               \tag{18}
\]

Thus the first new high parts enter in the transparent sequence: no high
part at \(e=0\), at most one \(4\) at \(e=1\), and at \(e=2\) either one
\(5\) or at most two \(4\)'s.

## 5. Warning about \(q\geq6\)

For \(h\leq21\), the selected-row \(q=6\) deficit is

\[
                         22-h+\max(0,6-k)>0,             \tag{19}
\]

so the kernel really is at most five and (5) is a closure theorem.  From
\(h=22\) onward a six-dimensional kernel may survive the selected-row
bound.  The \(q=5\) capped-mass test must not then be credited by itself.
The general relation theorem instead requires, for the actual kernel
dimension \(q\),

\[
             \sum_i\min(m_i,q-2)\geq(q-2)(q+1).          \tag{20}
\]

For example, \(q=6\) uses cap four and threshold twenty-eight, not cap
three and threshold eighteen.  A higher-\(q\) census must branch on the
kernel dimension or obtain a separate upper bound.

## 6. Exact audit

[verify_live_three_zero_higher_split_q5_boundary_census.py](../computations/verify_live_three_zero_higher_split_q5_boundary_census.py)
reconstructs every formal selection, imports the exact frontier
classification, checks the invariant excess (4), reproduces both tables,
and proves the symbolic survivor descriptions.
