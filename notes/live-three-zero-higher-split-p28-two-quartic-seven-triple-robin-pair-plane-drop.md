# Higher splits: the \(p=28\) \(4^2 3^7 1\) Robin pair-plane drop

## 1. Result and scope

Continue from the
[first selected six-kernel boundary](live-three-zero-higher-split-p28-six-kernel-boundary.md).
At \(p=h+k=28\), consider the moving-triple family whose restored common
baseline is

\[
                              4^2 3^7 1_s.                    \tag{1}
\]

For a triple value \(i\), selecting that class in role two leaves relation
complement

\[
                         4^2 3^6 1_i1_s.                     \tag{2}
\]

This is the natural baseline for the two residual tuples

\[
                         (e,a,b,u)=(2,7,0,1),(2,7,1,-1).     \tag{3}
\]

In the second tuple, the unique double is held fixed in role two for all
seven moving-triple selections.

**Theorem 1.1 (two-quartic Robin pair-plane bound).**  At most three of
the seven moving-triple selections over (1) can have six-dimensional
selected row kernel.  Consequently at least four have selected kernel
dimension at most five.

This is a dimension-drop theorem only.  It does not close either collision
profile and does not assert that every selected kernel of dimension at most
five is contradictory.

The structural conventions are retained throughout: the seven repeated
triple values are nonzero, all exceptional values are distinct and
nonopposite, and the fixed singleton \(s\) is allowed to be zero.  In
particular, \(s\ne\pm i\) for every moving triple value \(i\).

## 2. The common saturated six-kernel

Suppose for contradiction that four moving selections have selected
kernel dimension six.  For each of their moving values \(i\), the relation-space
theorem applied to (2) supplies

\[
              {\cal S}_i\subseteq\mathbb C[z]_{\le6},
              \qquad \dim {\cal S}_i=4.                     \tag{4}
\]

Put

\[
                  B_i=(z-i)^2(z+i)^2=(z^2-i^2)^2.           \tag{5}
\]

The exact moving-triple transport gives

\[
       {\cal T}_i:=B_i{\cal S}_i\subseteq {\cal K}
                         \subseteq\mathbb C[z]_{\le10},
       \qquad \dim{\cal T}_i=4,                             \tag{6}
\]

where \({\cal K}\) is the common kernel of the exact rows belonging to
the restored baseline (1).

A seven-space in \(\mathbb C[z]_{\le10}\) would have forced finite
Wronskian weight

\[
             2(7-4)+7(7-3)+(7-1)=40,                        \tag{7}
\]

against cap

\[
                            7(11-7)=28.                       \tag{8}
\]

The exact-row gcd correction is nonnegative, so

\[
                              \dim{\cal K}\le6.              \tag{9}
\]

At the fixed singleton, normalize its exact first-order row by its regular
nonzero unit.  It has the common form

\[
                    L_s(P)=P'(s)+\beta P(s),                 \tag{10}
\]

for one scalar \(\beta\) independent of the moving value.

## 3. Every pair intersection is its full Robin plane

Write \(t=z^2\) and \(a_i=i^2\).  Structural nonopposition makes the
seven \(a_i\) distinct.  For distinct \(i,j\), the quartics \(B_i,B_j\)
are coprime, and hence

\[
 B_i\mathbb C[z]_{\le6}\cap B_j\mathbb C[z]_{\le6}
                    =B_iB_j\mathbb C[z]_{\le2}.             \tag{11}
\]

The restriction of \(L_s\) to the three-space on the right is nonzero:
\(B_i(s)B_j(s)\ne0\), so the coefficient of \(q'(s)\) in
\(L_s(B_iB_jq)\) is nonzero.  Therefore

\[
 {\cal A}_{ij}:=\ker\!\left(L_s\bigm|
                 B_iB_j\mathbb C[z]_{\le2}\right)
                 \quad\hbox{has dimension two}.             \tag{12}
\]

On the other hand, (6)--(9) give

\[
               \dim({\cal T}_i\cap{\cal T}_j)
                         \ge4+4-6=2.                         \tag{13}
\]

The intersection in (13) is contained in (12), so equality is forced:

\[
                 \boxed{{\cal T}_i\cap{\cal T}_j
                                      ={\cal A}_{ij}}.       \tag{14}
\]

In particular every Robin pair-plane \({\cal A}_{ij}\) lies in
\({\cal K}\).  Notice that (12)--(14) also exclude
\(\dim{\cal K}<6\); thus no equality case has been silently lost.

Put \(x=z-s\), \(P_{ij}=B_iB_j\), and

\[
 \gamma_{ij}=\beta+{P_{ij}'(s)\over P_{ij}(s)}
     =\beta+{4s\over s^2-a_i}+{4s\over s^2-a_j}.            \tag{15}
\]

All denominators in (15) are nonzero.  Two convenient members of
\({\cal A}_{ij}\) are

\[
 \begin{aligned}
       X_{ij}&=x^2P_{ij},\\
       Y_{ij}&=P_{ij}\bigl(1-\gamma_{ij}x\bigr).
 \end{aligned}                                              \tag{16}
\]

The second formula keeps the full nonlinear dependence of the Robin slope
on \(P_{ij}\); no fictitious linear operator on the product span is used.

## 4. Five square-products give a fixed five-space

For four distinct squares \(a_0,a_1,a_2,a_3\), take the five pairs

\[
                         01,02,03,12,13.                     \tag{17}
\]

In the coefficient basis \(1,t,\ldots,t^4\), the determinant of their
five products

\[
                         (t-a_i)^2(t-a_j)^2                  \tag{18}
\]

is

\[
\begin{aligned}
 4&(a_0-a_1)^4(a_0-a_2)(a_0-a_3)\\
  &\qquad\cdot(a_1-a_2)(a_1-a_3)(a_2-a_3)^2,                \tag{19}
\end{aligned}
\]

which is nonzero.  It follows from the first line of (16) that the span of
all pair-planes contains the five-space

\[
                   {\cal V}:=(z-s)^2\mathbb C[z^2]_{\le4}.  \tag{20}
\]

We now show that two further independent quotient directions are forced,
apart from one explicitly treated parity boundary.

## 5. A quotient invariant when \(s\ne0\)

Every \(R\in\mathbb C[z]_{\le10}\) has a unique parity decomposition

\[
                         R=E(t)+zO(t),
 \qquad \deg E\le5,\quad\deg O\le4.                         \tag{21}
\]

For \(s\ne0\), define

\[
        \Psi_s(R)=2sE(t)+(t+s^2)O(t)\in\mathbb C[t]_{\le5}. \tag{22}
\]

The kernel is exactly \({\cal V}\).  Indeed, \(\Psi_s(R)=0\) gives

\[
             R=(t+s^2-2sz)q(t)=(z-s)^2q(t),
             \qquad q=-{O\over2s}\in\mathbb C[t]_{\le4}.   \tag{23}
\]

For the second member of (16), direct substitution gives the exact
quotient image

\[
 \Psi_s(Y_{ij})=
   \bigl[2s+\gamma_{ij}(s^2-t)\bigr]
                  (t-a_i)^2(t-a_j)^2.                       \tag{24}
\]

The affine factor in brackets is not the zero polynomial when \(s\ne0\).
Choose three distinct moving squares \(a_1,a_2,a_3\).  If the two
nonzero degree-at-most-five polynomials
\(\Psi_s(Y_{12})\) and \(\Psi_s(Y_{13})\) were proportional, their
common value would be divisible by

\[
                   (t-a_1)^2(t-a_2)^2(t-a_3)^2,             \tag{25}
\]

which has degree six.  This is impossible.  Thus their two quotient
classes are independent modulo \({\cal V}\), and (14) forces

\[
                             \dim{\cal K}\ge5+2=7,          \tag{26}
\]

contrary to (9).

## 6. The complete \(s=0\) case split

Suppose now \(s=0\).  Every \(P_{ij}\) is even and
\(P_{ij}'(0)=0\), so (15)--(16) reduce to

\[
             X_{ij}=t(t-a_i)^2(t-a_j)^2,
 \qquad
             Y_{ij}=(1-\beta z)(t-a_i)^2(t-a_j)^2.          \tag{27}
\]

By (19), the \(X_{ij}\) span \(t\mathbb C[t]_{\le4}\), while the
\(Y_{ij}\) span \((1-\beta z)\mathbb C[t]_{\le4}\).

If \(\beta\ne0\), those two five-spaces meet only in zero: comparison of
odd parts in

\[
                 tq(t)=(1-\beta z)r(t)                      \tag{28}
\]

first gives \(r=0\), and then \(q=0\).  Hence their direct sum has
dimension ten, again contradicting (9).

It remains only \(s=\beta=0\).  Equations (27) and (19) then show that
the pair-planes span exactly

\[
       \mathbb C[t]_{\le4}+t\mathbb C[t]_{\le4}
                =\mathbb C[z^2]_{\le5},                    \tag{29}
\]

a six-space.  Thus (9), (14), and (29), using only the four chosen maximal
selections, would force

\[
                        {\cal K}=\mathbb C[z^2]_{\le5}.      \tag{30}
\]

But the Wronskian of the basis
\(1,z^2,z^4,z^6,z^8,z^{10}\) is a nonzero constant times \(z^{15}\).
It has no zero at any of the nine nonzero repeated nodes.  The two exact
order-four rows and seven exact order-three rows of (1), however, force
Wronskian weight at least

\[
                          2(6-4)+7(6-3)=25                  \tag{31}
\]

at those distinct nonzero nodes.  This contradiction excludes the final
parity boundary.  Since the four chosen maximal selections were arbitrary,
no four of the seven selections can be maximal, proving Theorem 1.1.

## 7. Exact audit

[verify_live_three_zero_higher_split_p28_two_quartic_seven_triple_robin_pair_plane_drop.py](../computations/verify_live_three_zero_higher_split_p28_two_quartic_seven_triple_robin_pair_plane_drop.py)
checks both residual selections at all six \(p=28\) splits, the selected
and common-kernel Wronskian gaps, coprime pair intersections and the
nonzero singleton-row restriction, the determinant (19), the exact Robin
slope and quotient identity (24), every \(s=0\) branch, and the exceptional
even-space Wronskian.

The
[independent audit](live-three-zero-higher-split-p28-two-quartic-seven-triple-robin-pair-plane-drop-independent-audit.md)
reconstructs the common transport and Robin row, all gcd corrections,
the quotient calculation, and both parity branches.  It verifies that
exactly four maximal values suffice, so the conclusion is the stated
at-most-three cap rather than merely an existence-of-one-drop statement.
