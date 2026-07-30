# The universal cycle-span Hessian detector fails on a signed base

## 1. Outcome

Let \(F=\operatorname {Haf}_6\), let \(H_q=\operatorname {Hess}F(q)\),
fix \(e=01\), and let \(C_q\) be the span of the gradients at \(q\) of
all quadratic four-cycle binomials.  The proposed implication

\[
 \partial_{01}F(q)\ne0
 \quad\Longrightarrow\quad
 \exists\lambda\in C_q\cap\operatorname {im}H_q
                    \text{ with }\lambda_{01}\ne0                 \tag{1}
\]

is **false over \(\mathbb C\)**.  There is a small integral signed base
with \(\partial_{01}F(q)=-36\), together with an explicit rational
separator

\[
              w\in C_q^\perp,
 \qquad       w-\mathbf e_{01}\in\ker H_q.                       \tag{2}
\]

Consequently every element of
\(C_q\cap\operatorname {im}H_q\) has zero \(01\)-coordinate.  This
explains why exhaustive \(0/1\) tests can be positive without proving
(1): the obstruction occupies a genuinely signed family.

## 2. The separator criterion

Use the standard coordinate pairing on the fifteen edges.  Since \(H_q\)
is symmetric,

\[
 \bigl(C_q\cap\operatorname {im}H_q\bigr)^\perp
       =C_q^\perp+\ker H_q.                                  \tag{3}
\]

For a fixed \(q\) with \(\partial_{01}F(q)\ne0\), failure of the conclusion
in (1) is equivalent to the existence of \(w\) satisfying (2).  Indeed, if
\(\lambda\in C_q\cap\operatorname {im}H_q\), then

\[
 w\mathbin\cdot\lambda=0,
 \qquad
 (w-\mathbf e_{01})\mathbin\cdot\lambda=0,
\]

and subtraction gives \(\lambda_{01}=0\).

There is a useful local form of these equations.  For a matching
\(ab\mid cd\) in a four-set \(S\), put

\[
 D_{ab\mid cd}(q,w)=q_{ab}w_{cd}+q_{cd}w_{ab}.              \tag{4}
\]

The condition \(w\in C_q^\perp\) says precisely that the three values
(4) are equal on each four-set.  If their common value is \(t_S\), the
row of \(H_qw\) indexed by the complementary edge of \(S\) is \(3t_S\).
Therefore (2) is equivalent to

\[
 t_S=
 \begin{cases}
  q_{S\setminus\{0,1\}}/3,&\{0,1\}\subset S,\\
  0,&\{0,1\}\not\subset S.
 \end{cases}                                                \tag{5}
\]

This is also a direct, fifteen-small-equation way to audit the guard.

## 3. An integral counterexample

Set

\[
\begin{aligned}
 q_{02}=q_{03}=q_{04}=q_{05}
 &=q_{12}=q_{13}=q_{14}=q_{15}=1,\\
 q_{23}&=6,\qquad q_{45}=-6,                              \tag{6}
\end{aligned}
\]

and set the remaining five edges

\[
                   01,24,25,34,35                         \tag{7}
\]

to zero.  Its complementary hafnian is

\[
 \partial_{01}F(q)
   =q_{23}q_{45}+q_{24}q_{35}+q_{25}q_{34}=-36\ne0.        \tag{8}
\]

Define

\[
\begin{aligned}
 w_{01}&=\tfrac13,\\
 w_{02}=w_{03}=w_{12}=w_{13}&=1,\\
 w_{04}=w_{05}=w_{14}=w_{15}&=-1,\\
 w_{23}=w_{45}&=6,                                      \tag{9}
\end{aligned}
\]

with \(w_{24}=w_{25}=w_{34}=w_{35}=0\).  Equivalently,

\[
 3(w-\mathbf e_{01})
 =-2\mathbf e_{01}
  +3(\mathbf e_{02}+\mathbf e_{03}+\mathbf e_{12}+\mathbf e_{13})
  -3(\mathbf e_{04}+\mathbf e_{05}+\mathbf e_{14}+\mathbf e_{15})
  +18(\mathbf e_{23}+\mathbf e_{45})                     \tag{10}
\]

is an integral vector in \(\ker H_q\).

To verify \(w\in C_q^\perp\), partition the complementary sites as
\(A=\{2,3\}\), \(B=\{4,5\}\).  On \(01\cup A\), the three values in
(4) are all \(2=q_{23}/3\); on \(01\cup B\), they are all
\(-2=q_{45}/3\); and on \(01\cup\{a,b\}\) with
\(a\in A,b\in B\), they are all zero.  Every four-set not containing
both 0 and 1 also has all three values zero: a nonzero \(A\)-edge is
paired with the \(+1\) spokes, a nonzero \(B\)-edge with the \(-1\)
spokes, and every \(A\)-to-\(B\) internal edge vanishes.  Hence (5)
holds, proving both assertions in (2).

## 4. The counterexample is a family, not an isolated accident

The same construction works with a nonzero parameter \(r\).  Set
\(q_{01}=0\), kill the four \(A\)-to-\(B\) internal edges, and choose
nonzero spokes subject to

\[
\begin{aligned}
 q_{23}&=6r q_{02}q_{13}=6r q_{03}q_{12},\\
 q_{45}&=-6r q_{04}q_{15}=-6r q_{05}q_{14}.               \tag{11}
\end{aligned}
\]

Take \(w_{01}=1/3\), put \(w=rq\) on the four spokes to \(A\) and on
edge \(23\), put \(w=-rq\) on the four spokes to \(B\) and on edge
\(45\), and set \(w=0\) on the killed cross edges.  Equations (4)--(5)
hold verbatim.  Moreover,

\[
 \partial_{01}F(q)=q_{23}q_{45}
   =-36r^2q_{02}q_{13}q_{04}q_{15}\ne0,                 \tag{12}
\]

so every allowed packet is still a counterexample to (1).  The
specialization \(r=1\) with all spokes equal to one is (6)--(9).

So no case-free certificate of (1) can exist from the scalar hafnian and
the full quadratic cycle span alone.  Any positive proof must use extra
physical information that excludes this signed two-block pattern (for
example, complete decorated full-nine constraints or a genuine
grade-preserving overlap identity).

The exact hypothesis witnessed here is only the nonzero scalar cofactor

\[
                     \partial_{01}F(q)=-36.                \tag{13}
\]

The guard is not claimed to arise from a complete decorated ternary source,
nor to satisfy the physical full-nine equations in either chart.  It
therefore refutes the proposed scalar aggregate lemma, not the conjecture
and not any stronger lemma which uses those omitted tensor constraints.

Even on bases where aggregate detection does hold, this would settle only
the Hessian row-space problem.  The separate filtered source-provenance
condition is still required before the resulting cycle mixture can be
used in the proof of the conjecture.

The dependency-free
[checker](../computations/verify_universal_cycle_span_hessian_signed_counterfamily.py)
enumerates all fifteen four-sets, verifies (5), checks the Hessian kernel
certificate, and performs the exact separator test over the rationals.
