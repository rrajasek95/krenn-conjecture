# The eighth split at \(k=3\): ten doubles and one singleton

## 1. Result

Consider

\[
                         (h,k;\lambda)=(8,3;2^{10}1).    \tag{1}
\]

Write \(V\) for the ten double values and \(r\) for the singleton value.

**Theorem 1.1.**  Profile (1) is impossible on the no-extra-singular
stratum.

Fix five doubles, select two partially and three fully, and lift the two
missing mates.  The ten resulting sextics fill a four-dimensional common
kernel of five exact second-order value rows.  Its two row relations map
injectively to a plane of quadratic multipliers.

The singleton pole forces \((z-r)^2\) into that plane.  For this
multiplier the singleton denominator cancels completely, leaving

\[
                         { (z+\mu)^3Q_T(z)^2\over C_O(z)^3} \tag{2}
\]

as the derivative of a rational function for every \(5/5\) partition of
the double values.  At an outside double, the zero-residue condition is a
quadratic equation in an affine subset sum.  Its mixed finite difference
under two disjoint swaps forces at least eight double values into one
fibre of a degree-two rational function.

## 2. Formal five-double lifts

Fix a five-set \(T\subset V\), put \(O=V\setminus T\), and define

\[
 Q_T(z)=\prod_{t\in T}(z+t),\qquad
 C_O(z)=\prod_{u\in O}(z-u),\qquad L(z)=z-r.             \tag{3}
\]

For each pair \(\{x,y\}\subset T\), select one label at \(x,y\) and both
labels at the other three members of \(T\).  This is an eight-label core
in five classes.  Its complement contains the two unselected mates at
\(x,y\), the five untouched doubles in \(O\), and the singleton at \(r\).
The missing mates are nonzero singleton guards, so the core is legal even
if \(r=0\).  The simultaneous-Hermite reduction gives

\[
                         0\ne q_{x,y}\in\mathbb C[z]_{\le2}. \tag{4}
\]

The rational dependence is

\[
 {q_{x,y}(z)(z-x)(z-y)C_O(z)^2L(z)\over
  (z+\mu)^4(z+x)^2(z+y)^2
  \prod_{t\in T\setminus\{x,y\}}(z+t)^3}.               \tag{5}
\]

Put

\[
 h_x(z)=z^2-x^2,\qquad
 P_{x,y}=h_xh_yq_{x,y}\in\mathbb C[z]_{\le6}.            \tag{6}
\]

Using

\[
                         {z-x\over(z+x)^2}
                         ={h_x(z)\over(z+x)^3},          \tag{7}
\]

equation (5) becomes the identical rational function

\[
 F_P(z)={C_O(z)^2L(z)P(z)\over
              (z+\mu)^4Q_T(z)^3},\qquad P=P_{x,y}.      \tag{8}
\]

The numerator and denominator degrees are at most \(17\) and \(19\), so
\(F_P=O(z^{-2})\).  Define

\[
 K_T=\left\{P\in\mathbb C[z]_{\le6}:
       \operatorname {res}_{z=-t}F_P=0\quad(t\in T)\right\},\qquad
 W_T=\operatorname {span}\{P_{x,y}:\{x,y\}\subset T\}.  \tag{9}
\]

At each of the five value poles, the complementary factor \(C_O^2L\) is
a unit.  Thus the rows defining \(K_T\) are exact second-order
functionals.  The residue theorem also kills the residue at the common
pole \(-\mu\), but the five value rows already give the sharp dimension
bound needed below.

## 3. The common kernel has dimension four

Let \(d=\dim K_T\), remove its polynomial gcd, and let \(n_1,n_3\) count
value nodes where that gcd has order one or at least three.  Gcd order two
is incompatible with removal of the gcd after imposing an exact
second-order row.  The forced Wronskian weight minus its degree bound is
at least

\[
 d^2-2d-10+(d+1)n_1+2(d+1)n_3.                          \tag{10}
\]

For \(d\ge5\), this is positive.  Hence

\[
                              \dim K_T\le4.               \tag{11}
\]

The ten nonzero lifts in (6) satisfy

\[
                    P_{x,y}\in h_xh_y\mathbb C[z]_{\le2}. \tag{12}
\]

Because the five \(h_t\) are pairwise coprime, their pairwise
divisibilities force \(\dim W_T\ge3\).  The equality case has the same
purely algebraic intersection classification as in the \(k=2\)
all-double argument:

\[
              \dim W_T=3\quad\Longrightarrow\quad
              W_T=G(z){\cal E}(z^2),\qquad
              \dim{\cal E}=3,\quad\deg G\le2.            \tag{13}
\]

If \(\deg G=1\) or \(2\), restricting any exact value row to
\(G(z)R(z^2)\) leaves a nonzero coefficient of \(R''\), \(R'\), or \(R\).
If \(G\) is constant, \({\cal E}\) is a hyperplane in the cubics in
\(z^2\).  The five value rows would be proportional to one annihilator,
whose dual cubic would have the five distinct roots \(t^2\), \(t\in T\).
Both alternatives are impossible.  Therefore

\[
                         W_T=K_T,\qquad\dim K_T=4.        \tag{14}
\]

Notice that this proof uses only the five exact value rows; the common
pole having order four rather than three causes no loss.

## 4. The quadratic relation plane

Put

\[
 \Omega_T(z)={C_O(z)^2L(z)\over(z+\mu)^4Q_T(z)^3}.       \tag{15}
\]

The five value rows on the seven-dimensional space
\(\mathbb C[z]_{\le6}\) have rank three by (14), so their relation space
has dimension two.  For a relation \(c=(c_t:t\in T)\), form

\[
 H_c(z)=\sum_{t\in T}c_t\,
                 \operatorname {pp}_{z=-t}\Omega_T(z).  \tag{16}
\]

The relation annihilates \(1,z,\ldots,z^6\).  Hence

\[
                 H_c(z)={N_c(z)\over Q_T(z)^3},
                 \qquad\deg N_c\le7.                    \tag{17}
\]

Distinct principal-part supports make \(c\mapsto N_c\) injective.  Divide
(16) by (15):

\[
                  G_N(z)={(z+\mu)^4N(z)\over C_O(z)^2L(z)}. \tag{18}
\]

At every root \(-t\) of \(Q_T\),
\(G_N-c_t=O((z+t)^3)\), so \(G_N'\) has a double zero.  Direct
differentiation gives

\[
 G_N'(z)={(z+\mu)^3\over C_O(z)^3L(z)^2}\,{\cal E}_O(N)(z), \tag{19}
\]

where

\[
 {\cal E}_O(N)=
 C_OL\bigl((z+\mu)N'+4N\bigr)
 -(z+\mu)\bigl(2C_O'L+C_OL'\bigr)N.                    \tag{20}
\]

Thus

\[
                         {\cal E}_O(N)=Q_T^2S_N.         \tag{21}
\]

Here \(\deg C_O=5,\ \deg L=1\).  If \(n=\deg N\le7\), the
nominal leading coefficient of degree \(n+6\) in (20) is

\[
                         n+4-(2\cdot5+1)=n-7.            \tag{22}
\]

It cancels at \(n=7\); otherwise the degree is already at most twelve.
Consequently

\[
                         S_N\in\mathbb C[z]_{\le2}.      \tag{23}
\]

The map \(N\mapsto S_N\) is injective.  Its kernel would make \(G_N\)
constant, but a nonzero identity

\[
                    (z+\mu)^4N=\gamma C_O^2L            \tag{24}
\]

fails at \(z=-\mu\), where the right side is a unit times \(\gamma\).
The relation image

\[
                  {\cal S}_T=\{S_N\}\subset\mathbb C[z]_{\le2} \tag{25}
\]

is therefore exactly two-dimensional, and every \(S\in{\cal S}_T\)
occurs in

\[
                       G_S'(z)=
 { (z+\mu)^3Q_T(z)^2S(z)\over C_O(z)^3(z-r)^2}.          \tag{26}
\]

## 5. Canceling the singleton

At \(z=r\), the residue of (26) is

\[
                         (B_rS)'(r),\qquad
 B_r(z)={(z+\mu)^3Q_T(z)^2\over C_O(z)^3}.              \tag{27}
\]

Since \(B_r(r)\ne0\), this is a nonzero first-order row on the
three-dimensional quadratic space.  Its two-dimensional kernel contains
\({\cal S}_T\), so it equals \({\cal S}_T\).  In particular,

\[
                              (z-r)^2\in{\cal S}_T.       \tag{28}
\]

Use this multiplier in (26).  The singleton factor cancels, and (2) is
the derivative of a rational function:

\[
                         G'(z)={ (z+\mu)^3Q_T(z)^2\over C_O(z)^3}. \tag{29}
\]

This step remains valid at \(r=0\); it never divides by the singleton
value.

## 6. The outside-double equation

Fix \(u\in O\), write \(C_u=C_O/(z-u)\), and put

\[
                         A_{T,u}(z)=
 { (z+\mu)^3Q_T(z)^2\over C_u(z)^3}.                    \tag{30}
\]

At \(u\), equation (29) is \(A_{T,u}(z)/(z-u)^3\).
Its residue is \(A_{T,u}''(u)/2\), so

\[
                         A_{T,u}''(u)=0.                 \tag{31}
\]

Define the first two logarithmic jets

\[
\begin{split}
\Xi_T(u)&={3\over u+\mu}
 +2\sum_{t\in T}{1\over u+t}
 -3\sum_{\substack{v\in O\\v\ne u}}{1\over u-v},\\
\Zeta_T(u)&=-{3\over(u+\mu)^2}
 -2\sum_{t\in T}{1\over(u+t)^2}
 +3\sum_{\substack{v\in O\\v\ne u}}{1\over(u-v)^2}.
\end{split}                                             \tag{32}
\]

Since \(A''/A=(\log A)'^2+(\log A)''\), equation (31) is

\[
                          \Xi_T(u)^2+\Zeta_T(u)=0.        \tag{33}
\]

Fix \(u\) and let \(W=V\setminus\{u\}\), so \(|W|=9\).  As \(T\) ranges
over the five-subsets of \(W\), write

\[
\begin{split}
\Xi_T(u)&=\kappa_u+\sum_{x\in T}\Phi_u(x),\\
\Zeta_T(u)&=\eta_u+\sum_{x\in T}\Psi_u(x),               \tag{34}
\end{split}
\]

where the constants \(\kappa_u,\eta_u\) are independent of \(T\), and

\[
\begin{split}
\Phi_u(x)&={2\over u+x}+{3\over u-x}
          ={5u+x\over u^2-x^2},\\
\Psi_u(x)&=-{2\over(u+x)^2}-{3\over(u-x)^2}.
\end{split}                                             \tag{35}
\]

## 7. Two disjoint swaps

Choose four distinct members \(a,b,c,d\in W\).  There is a five-subset
\(T\) containing \(a,c\) and excluding \(b,d\).  Apply (33) to \(T\), to
the two single swaps

\[
                T-a+b,\qquad T-c+d,
\]

and to the double swap

\[
                T-\{a,c\}+\{b,d\}.
\]

Take the alternating sum of these four equations.  The affine
\(\Zeta\)-terms cancel.  If

\[
 \delta_1=\Phi_u(b)-\Phi_u(a),\qquad
 \delta_2=\Phi_u(d)-\Phi_u(c),
\]

the square terms leave exactly \(2\delta_1\delta_2\).  Hence

\[
       \bigl(\Phi_u(b)-\Phi_u(a)\bigr)
       \bigl(\Phi_u(d)-\Phi_u(c)\bigr)=0                 \tag{36}
\]

for every four distinct \(a,b,c,d\in W\).

If all nine \(\Phi_u\)-values are equal, continue below.  Otherwise choose
\(a,b\) with different images.  Equation (36) says that the other seven
members of \(W\) have one common image, say \(\lambda\).  Applying (36)
to the disjoint pairs \((a,c)\) and \((b,d)\), with \(c,d\) among those
seven, shows that at least one of \(a,b\) also has image \(\lambda\).
Thus in every case at least eight distinct double values lie in one fibre
of \(\Phi_u\).

That fibre is cut out by

\[
                         \lambda(u^2-x^2)-5u-x=0.        \tag{37}
\]

It is a nonzero polynomial of degree at most two, because its coefficient
of \(x\) is \(-1\).  The denominators in (35) are nonzero: distinct double
values are neither equal nor opposite.  Eight distinct roots are
impossible.  This contradiction proves Theorem 1.1.

## 8. Exact audit

[verify_live_three_zero_eighth_split_k3_ten_double_one_singleton_closure.py](../computations/verify_live_three_zero_eighth_split_k3_ten_double_one_singleton_closure.py)
checks all \(2520\) legal partial-pair cores, the lift and degree counts,
the five-row gcd-corrected Wronskian bound, the three-dimensional
intersection obstruction, the relation-pencil dimension and sharp degree
drop, singleton cancellation including \(r=0\), the outside-double
residue equation, every double-swap configuration, the equality-pattern
consequence of (36), and the final quadratic fibre contradiction.
