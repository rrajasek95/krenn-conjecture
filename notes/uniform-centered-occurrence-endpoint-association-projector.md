# The ordered-endpoint scheme has an exact cubic projector

## Outcome

After the matching filter, the remaining pointed occurrence row has a
five-dimensional ordered-endpoint cyclic module. Two natural coefficient
operators commute:

* \(S\), which reverses the ordered endpoints;
* \(B_h\), which moves exactly one endpoint through one residual matching
  edge.

Their joint spectrum on the pointed row is

\[
\begin{array}{c|ccccc}
             &(0)&(s)&(p)&(a)&(w)\\ \hline
B_h          &4h&2h-2&-2&2h&-2\\
S            &+1&+1&+1&-1&-1.
\end{array}                                                   \tag{1}
\]

The sectors are respectively the constant, symmetric standard,
symmetric-pair, alternating standard, and alternating-wedge pieces. Since
\(B_h\) alone separates the constant eigenvalue from all nonconstant
eigenvalues, the cubic

\[
 P_h(B_h)=(B_h+2I)(B_h-(2h-2)I)(B_h-2hI)                     \tag{2}
\]

kills every endpoint debt and acts on constants by

\[
                         P_h(4h)=8h(h+1)(2h+1).                \tag{3}
\]

Thus a rational endpoint projector exists uniformly in \(h\), and its
integral numerator is (2). Composing it with the matching projector from
the preceding theorem completes the centered occurrence projector at
coefficient level while keeping the marked delta outside the averaging
operators.

The remaining obstruction is entirely physical: lift the commuting
matching and endpoint coefficient operators to an augmented
Cartan/Hasse bicomplex and fill their product-rule faces.

Checker:
[verify_uniform_centered_occurrence_endpoint_association_projector.py](../computations/verify_uniform_centered_occurrence_endpoint_association_projector.py).

## 1. The endpoint-change graph

Write an occurrence as \((p,s,R)\), where \(R\) is a perfect matching on
the residual \(2h\) sites. For \(t\) residual with mate \(u=R(t)\), define
two neighbors

\[
\begin{aligned}
 b^p_t(p,s,R)&=(t,s,R-\{tu\}+\{pu\}),\\
 b^s_t(p,s,R)&=(p,t,R-\{tu\}+\{su\}).
\end{aligned}                                                \tag{4}
\]

Then

\[
                   B_h=\sum_{t\in R}(b^p_t+b^s_t)              \tag{5}
\]

has degree \(4h\). The swap

\[
                       S(p,s,R)=(s,p,R)                        \tag{6}
\]

commutes with \(B_h\). It also commutes with the residual two-switch
adjacency \(A_h\): changing an endpoint and switching two untouched
matching edges gives the same occurrence multiset in either order. The
checker verifies both graph commutations exactly.

After the matching projector, the pointed Gram row depends only on the
ordered endpoints relative to the marked endpoints and marked residual
pairs. Its cyclic span under \(B_h,S\) has dimension five for every tested
order. The following elementary endpoint-module decomposition proves the
five sectors uniformly.

Let \(W\) be the permutation module on sites and decompose
\(W=1\oplus V\), with \(V=[n-1,1]\), \(n=2h+2\). Ordered distinct endpoint
pairs form the off-diagonal part of \(W\otimes W\). The swap splits it into
symmetric and alternating parts:

\[
\begin{aligned}
\operatorname{Sym}:&\quad
 1\oplus V_s\oplus V_{\rm pair},\\
\operatorname{Alt}:&\quad
 V_a\oplus\Lambda^2V.                                   \tag{7}
\end{aligned}
\]

There is no higher component: these five modules exhaust the ordered-pair
permutation module. Their dimensions are

\[
 1,\quad n-1,\quad {n(n-3)\over2},\quad n-1,\quad
 {(n-1)(n-2)\over2},
\]

whose sum is \(n(n-1)\). The matching-flat pointed row has nonzero
projection to all five: its endpoint value is a linear combination of
equality with the two marked ordered endpoints, membership in the marked
residual-pair partition, and a constant. Hence its cyclic module is
precisely the five displayed pieces.

Direct neighbor counting in (4) gives the eigenvalues in (1). Equivalently,
one may check the symmetric and alternating minimal polynomials:

\[
\begin{aligned}
 (B_h+2)(B_h-(2h-2))(B_h-4h)\,v^+&=0,\\
 (B_h+2)(B_h-2h)\,v^-&=0,                            \tag{8}
\end{aligned}
\]

where \(v^\pm=(1\pm S)v\). The checker verifies (8) exactly at
\(h=2,3,4\), including the five-dimensional cyclic rank. The neighbor
count in (4) proves the formulas for all \(h\).

## 2. The uniform rational and integral projector

The nonconstant eigenvalues of \(B_h\) on the pointed module are

\[
                         -2,\quad2h-2,\quad2h.                  \tag{9}
\]

They are distinct from the constant eigenvalue \(4h\) for every
\(h\ge2\). Hence

\[
 \Pi_h^{\rm end}
 ={(B_h+2I)(B_h-(2h-2)I)(B_h-2hI)\over
   8h(h+1)(2h+1)}                                           \tag{10}
\]

projects the pointed module onto its constant line. No root or
order-dependent exceptional case occurs. Formula (2) is integral, while
the denominator in (10) is invertible in characteristic zero.

Let \(k_f\) be the negative Gram row from full endpoint induction. The
preceding matching projector is

\[
                 \Pi_h^{\rm match}
                 ={A_h-(h^2-3h+1)I\over2h-1}.                  \tag{11}
\]

Since \(A_h\) and \(B_h\) commute coefficientwise,

\[
       \Pi_h^{\rm end}\Pi_h^{\rm match}k_f=c_h\,1              \tag{12}
\]

for one rational scalar \(c_h\). Retain the marked delta outside both
operators and normalize its mass against (12):

\[
                 e_f-{1\over|\Omega_{h+1}|}1.                  \tag{13}
\]

Multiplying (13) by \(N_{h+1}\) gives exactly

\[
                     c_{f,h+1}=N_{h+1}e_f-1.                  \tag{14}
\]

Thus the coefficient problem is complete. The combined projector
denominator before the final harmless occurrence normalization is

\[
       (2h-1)\,8h(h+1)(2h+1),                                 \tag{15}
\]

and clearing it gives an integral coefficient identity. The marked
coefficient remains nonzero because neither adjacency is applied to the
delta term.

## 3. What physical lift (2) requires

The top coefficient operation \(B_h\) is a one-endpoint
Cartan/matching prism: replace \(p\) by \(t\) and pair the old endpoint
with the mate of \(t\), or do the analogous operation at \(s\). This is
the correct root/Cartan geometry for endpoint motion, but the coefficient
sum (5) is not by itself a source row.

The cubic (2) requires a coherent three-stage Hasse totalization:

1. every \(B_h\) factor has a one-endpoint Cartan product-rule face;
2. every pair of factors has a second Hasse face;
3. the cubic has a third totalization face.

Composing with (11) adds a mixed obligation between the endpoint prism and
the two-edge matching switch. Coefficientwise,

\[
                  [A_h,B_h]=0,\qquad[A_h,S]=[B_h,S]=0.         \tag{16}
\]

Physically, (16) must be upgraded to a filled commutator square retaining
literal word/fine/repeated grade, target, labelled residue, physical
\(q\), anchor, \(W\), eta/sigma, and the source-provenant terminal/Macaulay
quotient. The existing
matching/Bianchi differences do not provide this: they are differences of
already coupled ridge/response columns. The pinned Reynolds/endpoint audit
also exhibits nonzero Leibniz cross terms, so formal graph commutation
cannot be called a chain commutation.

The exact remaining theorem is:

> Lift the commuting coefficient pair \((A_h,B_h)\) to an augmented
> source-valid Cartan/Hasse bicomplex. Fill the two-switch, endpoint,
> mixed, quadratic, and cubic product-rule faces, or send their first
> nonfill to an accepted physical terminal. Then (10)--(14) construct the
> uniform centered occurrence cell and the scaled anchor bridge.

## Scope

This closes the entire occurrence association algebra over characteristic
zero. It does not prove that the coefficient projectors preserve the
physical source ideal or terminal readouts; that is now the single
load-bearing lift.

Run:

~~~text
python3 computations/verify_uniform_centered_occurrence_endpoint_association_projector.py
python3 -O computations/verify_uniform_centered_occurrence_endpoint_association_projector.py
python3 -I -S computations/verify_uniform_centered_occurrence_endpoint_association_projector.py
~~~

Frozen ledger SHA-256:

~~~text
f400b3a17f3630e9777fe237bc3eee7cbe09e075338d961550648d3544cf0a48
~~~
