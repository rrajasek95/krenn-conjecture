# Higher splits: the final five-triple even-span closure at \(p=19\)

## 1. Result

Continue from the moving-triple common-lift theorem at \(p=19\).  The
two one-quartic profiles with five exact triple classes are impossible:

\[
 \boxed{
   4\,3^5 1^{h+2},\qquad 4\,3^5 2\,1^h.}                    \tag{1}
\]

Equivalently, these are the parameter families

\[
             (e;a,b,u)=(1;5,0,2),\qquad(1;5,1,0).            \tag{2}
\]

The proof needs no comparison of the unknown local units.  Pairwise
quartic transports already fill the entire possible common kernel, and
one exact third-order row then gives a contradiction.

## 2. The common degree-eight kernel

Let \({\mathscr X}=\{x_1,\ldots,x_5\}\) be the five exact-triple
values.  Fix two ordinary singleton values to remain complementary in
every moving choice.  For the first profile, select one role-two layer at
the moving triple and all other required singleton layers.  For the second
profile, also select its exact double in role two.  In both cases the
formal complement is

\[
                         4\,3^4 1^3.                           \tag{3}
\]

Thus the exact relation space for the choice \(x\in{\mathscr X}\) is

\[
       {\cal S}_x\subseteq\mathbb C[z]_{\leq4},
       \qquad \dim {\cal S}_x=3.                              \tag{4}
\]

As in the moving-triple theorem, put

\[
                         B_x(z)=(z-x)^2(z+x)^2.                \tag{5}
\]

The exact transport replaces the residual simple row at \(x\) by the
baseline triple row and gives

\[
       {\cal T}_x:=B_x{\cal S}_x\subseteq{\cal K}
          \subseteq\mathbb C[z]_{\leq8},
       \qquad \dim{\cal T}_x=3,qquad\dim{\cal K}\leq5.       \tag{6}
\]

The common kernel is independent of the moving triple \(x\).  The
dimension bound is the already-audited six-space Wronskian obstruction:
the baseline has one quartic row, five triple rows, and two singleton
rows, whose forced six-space weight is

\[
             (6-4)+5(6-3)+2(6-1)=27>18
                =6(8+1-6).                                   \tag{7}
\]

Distinct triple classes are neither equal nor opposite, so the quartics
\(B_x\) are pairwise coprime.  For distinct \(x,y\),

\[
 B_x\mathbb C[z]_{\leq4}\cap B_y\mathbb C[z]_{\leq4}
                       =\mathbb C B_xB_y.                     \tag{8}
\]

Two three-spaces in the at-most-five-space (6) meet nontrivially.
Consequently

\[
                         B_xB_y\in{\cal K}
                  \qquad(x\ne y\in{\mathscr X}).             \tag{9}
\]

## 3. Four conic points span the even quartics

Set \(t=z^2\) and \(a_i=x_i^2\).  Structural nonopposition makes the
five numbers \(a_i\) pairwise distinct.  Equation (9) says that
\({\cal K}\) contains all ten polynomials

\[
                    (t-a_i)^2(t-a_j)^2,\qquad i<j.           \tag{10}
\]

We use the following elementary lemma.

**Lemma 3.1.**  If \(a_1,a_2,a_3,a_4\) are distinct, then the six
off-diagonal products

\[
                     (t-a_i)^2(t-a_j)^2,\qquad 1\leq i<j\leq4,
                                                                    \tag{11}
\]
span \(\mathbb C[t]_{\leq4}\).

**Proof.**  Let \(L\in\mathbb C[t]_{\leq4}^*\) annihilate (11), and
define a symmetric bilinear form on \(\mathbb C[t]_{\leq2}\) by

\[
                             \beta(f,g)=L(fg).                 \tag{12}
\]

Write \(b_i=(t-a_i)^2\).  Any three distinct \(b_i\)'s form a basis:
in the coefficient basis \((1,t,t^2)\), their determinant is a nonzero
constant times
\(\prod_{i<j}(a_i-a_j)\).  In the basis \(b_1,b_2,b_3\), the Gram
matrix of \(\beta\) is diagonal because
\(\beta(b_i,b_j)=0\) for \(i\ne j\).  Every coordinate of \(b_4\) in
this basis is nonzero; otherwise three distinct points
\(b_i\) on the Veronese conic would be linearly dependent.  The three
equalities \(\beta(b_4,b_i)=0\), \(i=1,2,3\), therefore kill all three
diagonal entries.  Hence \(\beta=0\).

Products of two quadratics span \(\mathbb C[t]_{\leq4}\), so
\(L=0\).  The annihilator of the span in (11) is zero, proving the
lemma. \(\square\)

Apply the lemma to any four of the five triple values.  Equations
(9)--(11) give

\[
                    \mathbb C[z^2]_{\leq4}\subseteq{\cal K}. \tag{13}
\]

The left side has dimension five, while (6) gives
\(\dim{\cal K}\leq5\).  Therefore

\[
                         \boxed{{\cal K}=\mathbb C[z^2]_{\leq4}.}
                                                                    \tag{14}
\]

## 4. One exact triple row is impossible

At most one of the five distinct triple values can be zero.  Choose a
nonzero \(v\in{\mathscr X}\).  The common baseline kernel has at \(v\)
the exact third-order row

\[
                         J_v(T)=(U_vT)'''(v)=0,
                         \qquad U_v(v)\ne0,                    \tag{15}
\]

for every \(T\in{\cal K}\).  No formula for the unit \(U_v\) is
needed.

By (14), the polynomial

\[
                            T_v(z)=(z^2-v^2)^3                 \tag{16}
\]

belongs to \({\cal K}\).  It has a zero of exact order three at \(v\),
and

\[
       T_v(v)=T_v'(v)=T_v''(v)=0,\qquad T_v'''(v)=48v^3\ne0. \tag{17}
\]

The product rule in (15) now gives

\[
                         (U_vT_v)'''(v)
                              =48U_v(v)v^3\ne0,                \tag{18}
\]

contradicting the exact row.  This closes both profiles in (1), including
the possible placement of a zero at one of the other triple values.

## 5. Exact audit

[verify_live_three_zero_higher_split_p19_five_triple_even_span_closure.py](../computations/verify_live_three_zero_higher_split_p19_five_triple_even_span_closure.py)
checks the two formal complements for every admissible \(h\), the common
six-space Wronskian gap, the quartic transport and coprime product line,
the Veronese-conic spanning lemma, the five-dimensional even kernel, and
the nonzero exact third jet in (17).
