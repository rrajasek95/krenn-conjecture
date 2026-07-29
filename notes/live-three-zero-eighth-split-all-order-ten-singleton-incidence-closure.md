# The eighth split: all-order ten-singleton incidence closure

## 1. Uniform statement

Fix \(h=8\) and any common-pole order \(k\geq1\).  Suppose a
no-extra-singular collision profile contains ten distinct singleton value
classes.  Select those ten classes at formal role one.  Then the
isolated-star pivots cannot all vanish.

Equivalently, every \(d=0,s=10\) formal selection in the
[all-order mixed-role theorem](live-three-zero-eighth-split-all-order-mixed-role-pair-drop-duality.md)
is impossible.  The proof uses only the selected lift incidence inside
\(\mathbb C[z]_{\leq11}\); it is independent of the complementary profile
and of \(k\).

Let the selected singleton values be \(r_1,\ldots,r_{10}\), and put

\[
                      f_i(z)=(z-r_i)(z+r_i)^2.           \tag{1}
\]

The values are distinct and pairwise nonopposite, and at most one is zero.
Consequently the ten cubic polynomials \(f_i\) are pairwise coprime.

## 2. The four-space and its incidence subspaces

Assume all isolated-star pivots vanish.  Every pair-drop core is legal:
lowering two selected singleton layers leaves at least one nonzero
singleton guard.  The all-order theorem therefore gives

\[
 K=W\subseteq\mathbb C[z]_{\leq11},\qquad \dim K=4,      \tag{2}
\]

where \(W\) is spanned by nonzero pair lifts \(P_{ij}\) divisible by
\(f_if_j\).  Define

\[
                         U_i=K\cap f_i\mathbb C[z].      \tag{3}
\]

The standard neighbor-product argument gives \(\dim U_i\geq2\): if all
nine lifts through \(i\) lay on one line, their nine coprime neighbor
factors would divide a nonzero polynomial of degree at most eleven.

## 3. A pencil-incidence lemma

We use the following elementary lemma twice.

**Lemma 3.1.**  Let \(V\subseteq\mathbb C[z]_{\leq N}\) be a polynomial
pencil.  Suppose that for each of \(m\) distinct, pairwise nonopposite
nonzero values \(r\), the pencil contains a nonzero section divisible by
\((z-r)(z+r)^2\).  If the parity determinant of a basis has more forced
roots than its degree, then

\[
             m\leq g+2\left\lfloor{N-g\over2}\right\rfloor-2,         \tag{4}
\]

where \(g\) is the degree of the pencil gcd.

Indeed, for a basis \(p,q\), the parity determinant

\[
             \Delta(z)=p(z)q(-z)-p(-z)q(z)              \tag{5}
\]

is odd of degree at most \(2N-1\).  A section divisible by the cubic in
the lemma makes \(\Delta\) vanish at both \(r\) and \(-r\).  Once the
forced roots make \(\Delta=0\), divide the pencil gcd \(G\).  The primitive
ratio is even, so

\[
                         V=G(z){\cal E}(z^2),            \tag{6}
\]

with a primitive pencil \({\cal E}\) of degree at most
\(n=\lfloor(N-g)/2\rfloor\).  For each node, either \(G(-r)=0\), consuming
a distinct gcd root, or the corresponding member of \({\cal E}\) has a
double root at \(r^2\).  In the latter case \(r^2\) is a root of the
nonzero Wronskian of \({\cal E}\), whose degree is at most \(2n-2\).
This proves (4).  Pairwise nonoppositeness makes the squares distinct.

For \(N=8\), the right side of (4) is at most six.  For \(N=5\), it is at
most three.  A possible zero node is simply omitted from these counts.

## 4. No \(U_i\) is a plane

Suppose \(\dim U_i=2\).  Dividing by \(f_i\) gives a pencil

\[
                         U_i/f_i\subseteq\mathbb C[z]_{\leq8}.        \tag{7}
\]

For every \(j\ne i\), the nonzero lift \(P_{ij}/f_i\) is divisible by
\(f_j\).  Among these nine neighbor nodes at least eight are nonzero.  They
give sixteen distinct roots of the odd parity determinant, whose degree is
at most fifteen.  Lemma 3.1 then allows at most six such nonzero nodes, a
contradiction.  Hence

\[
                              \dim U_i\geq3              \tag{8}
\]

for every \(i\).

## 5. No selected factor is absorbed by all of \(K\)

Let \(A\) be the set of indices with \(U_i=K\), and write \(a=|A|\).
If \(a>0\), pairwise coprimeness lets us divide their product from all of
\(K\), leaving a four-space of degree at most \(11-3a\).  Every remaining
\(U_j\) has dimension exactly three.  At the double root \(-r_j\) of
\(f_j\), the reduced four-space has vanishing sequence at least

\[
                              (0,2,3,4),                  \tag{9}
\]

and hence Wronskian weight at least three.  A zero node has the stronger
sequence \((0,3,4,5)\).

For \(a=1,2\), the forced weight and polynomial Wronskian cap would require

\[
              3(10-a)\leq4\bigl((11-3a)-3\bigr),        \tag{10}
\]

which is false.  For \(a\geq3\), the reduced ambient polynomial space has
dimension at most three and cannot contain the four-space.  Thus \(a=0\),
and (8) gives

\[
                              \dim U_i=3                 \tag{11}
\]

for all ten indices.

## 6. The second pencil contradiction

The \(U_i\) are now ten hyperplanes in the four-space \(K\).  The
intersection of any four is zero: a member would be divisible by four
pairwise coprime cubics, whose product has degree twelve, greater than the
ambient degree eleven.  Therefore every four quotient covectors are
independent.  It follows that

\[
 \dim(U_i\cap U_j)=2,\qquad
 \dim(U_i\cap U_j\cap U_\ell)=1                         \tag{12}
\]

for distinct indices.

Fix \(i,j\).  Dividing the two-dimensional intersection by \(f_if_j\)
gives a pencil

\[
             (U_i\cap U_j)/(f_if_j)
                       \subseteq\mathbb C[z]_{\leq5}.    \tag{13}
\]

For each of the other eight indices \(\ell\), the nonzero triple
intersection in (12) supplies a member of this pencil divisible by
\(f_\ell\).  At least seven of those nodes are nonzero.  Their fourteen
opposite roots force the degree-at-most-nine parity determinant to vanish,
while Lemma 3.1 permits at most three nonzero nodes.  This final
contradiction proves the theorem.

## 7. Exact audit

[verify_live_three_zero_eighth_split_all_order_ten_singleton_incidence_closure.py](../computations/verify_live_three_zero_eighth_split_all_order_ten_singleton_incidence_closure.py)
checks both parity degrees and forced-root counts, every gcd/Riemann--Hurwitz
bound in Lemma 3.1, the absorbed-factor Wronskian inequalities, the
four-hyperplane dimension chain, and both quotient-pencil degree caps.

