# Seventh split: repeated-double closure from full DR4

## 1. Result

Continue from the exact collision frontier and the full theorem
[dr4-full-endpoint-rigidity.md](dr4-full-endpoint-rigidity.md).
Let a seventh-split double/single profile have

\[
                         c=d+s
\]

distinct exceptional value classes and at least one double class.

**Theorem.**  If \(c\ge14\), the profile is closed.

The threshold fourteen is the strict threshold of this one-moving-variable
argument: the cleared determinant has degree at most eight and has
\(c-5\) moving roots.

## 2. A double background and four simple anchors

Fix a double value \(a\) and select both of its labels.  Choose four
distinct nonzero value classes

\[
                         C=\{b_0,b_1,b_2,b_3\}               \tag{1}
\]

different from \(a\), selecting one label from each.  For a moving value
\(x\notin\{a\}\cup C\), select one further label:

\[
                         R_x=\{a,a\}\cup C\cup\{x\}.          \tag{2}
\]

The seven labels in (2) represent six value classes.  Whenever the
complement \(N_x\) has a singleton class, the seventh-split Hermite
reduction gives

\[
                         Q_{R_x}(z)=P_{N_x}(z)q_x(z),
                         \qquad0\ne q_x,\quad\deg q_x\le3.    \tag{3}
\]

At a simple anchor \(b_i\), absorb the fixed double background and the
other three anchors into a translation \(U_i(C;a)\).  Selecting one label
from the moving class contributes

\[
 \psi(b_i,x)={1\over b_i+x}-{2\over x-b_i}
             =-{x+3b_i\over x^2-b_i^2}.                     \tag{4}
\]

In nodal coordinates \(t_i=-b_i\), the four cleared rows on the cubic
\(q_x\) are exactly

\[
 \mathcal R_i(x)q_x
 =(x^2-t_i^2)\bigl(q_x'(t_i)+U_i(C;a)q_x(t_i)\bigr)
 -(x-3t_i)q_x(t_i).                                        \tag{5}
\]

Thus their determinant is a polynomial of degree at most eight.

## 3. More roots than degree, then DR4

There are

\[
                         c-5\ge9                             \tag{6}
\]

distinct moving value classes outside the double background and the four
anchors.  None is a pole of (5): equality with an anchor is excluded by
the choice of classes, equality with its negative violates the structural
pair-sum condition, and a possible zero moving value is harmless because
the anchors are nonzero.

If all isolated-star pivots vanished, the determinant in (5) would vanish
at all \(c-5>8\) moving values.  Hence it would be identically zero.  Full
DR4 then gives

\[
                         U_i(C;a)=0\qquad(0\le i<4).          \tag{7}
\]

## 4. Varying one anchor

Fix a nonzero anchor \(b\), two nonzero companions \(u,v\), and the double
background \(a\).  Let \(y\) vary over the remaining nonzero value classes
and apply (7) to

\[
                         C_y=\{b,u,v,y\}.                    \tag{8}
\]

All terms of \(U_b(C_y;a)\) except the last anchor contribution are fixed,
so (7) says

\[
                         \psi(b,y)=\text{constant}.          \tag{9}
\]

Even if the unique possible zero class is discarded, there are at least

\[
                         c-4-1=c-5\ge9                       \tag{10}
\]

eligible values of \(y\).  But a fibre \(\psi(b,y)=\lambda\) is the
nonzero polynomial equation

\[
                         \lambda(y^2-b^2)+y+3b=0,            \tag{11}
\]

of degree at most two; its coefficient of \(y\) is one.  Equations
(9)--(11) are impossible.

## 5. Singleton and zero legality

The singleton-row hypothesis used in (3) can be made uniform in \(x\) and
in the varying core (8).

- If there is another double class besides the background \(a\), choose
  \(b\) from that class and select only one of its labels.  Its mate remains
  a singleton class in every complement.
- If \(a\) is the only double class, all other classes are singletons.
  At \(c\ge14\), the four anchors and one moving class consume only five of
  the \(c-1\) singleton classes, leaving at least eight untouched.

A repeated zero is structurally impossible, so both the double background
and the optional double guard anchor are nonzero.  Among all remaining
classes at most one singleton has value zero.  It can be left in the moving
pool or omitted when a nonzero fixed anchor is required; the counts (6) and
(10) already include the worst-case loss where appropriate.

This proves the theorem.

## 6. Exact effect on the residual census

For a double/single profile with total size \(p+9\),

\[
                         c=d+s=p+9-d.                        \tag{12}
\]

Combining \(c\ge14\) with the earlier constant/linear/quadratic moving
closures leaves exactly the following double counts, with
\(s=p+9-2d\):

\[
\begin{array}{c|l}
p&d\\ \hline
8&4,5,6,7,8\\
9&5,6,7,8,9\\
10&6,7,8,9\\
11&7,9,10\\
12&10.
\end{array}                                                   \tag{13}
\]

There is no double/single residual for \(p\ge13\).  The previously listed
triple-containing residuals are unaffected and remain open.

## 7. Exact audit

[verify_live_three_zero_seventh_split_repeated_double_dr4_closure.py](../computations/verify_live_three_zero_seventh_split_repeated_double_dr4_closure.py)
checks the Hermite residual degree, the degree-eight cleared determinant,
the strict \(c=14\) root count, both singleton mechanisms, the possible
zero class, the quadratic fibre, and the exact residual table (13).
