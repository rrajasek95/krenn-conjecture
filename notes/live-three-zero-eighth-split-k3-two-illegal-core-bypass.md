# The eighth split: bypassing the two illegal third-order cores

## 1. Result

At \(h=8,k=3\), consider the last no-extra-singular collision profile

\[
                         \lambda=3^2 2^4 1^7.             \tag{1}
\]

Write \(S\) for the seven singleton values, \(a,b\) for the two triple
values, and \(D\) for the four double values.  All six repeated values
are nonzero, while one member of \(S\) may be zero.

**Theorem 1.1.**  Profile (1) is impossible.

There are exactly two illegal one-value-per-class eight-cores,

\[
                         I_a=S\cup\{a\},\qquad
                         I_b=S\cup\{b\}.                 \tag{2}
\]

We do not construct residuals on either core.  Instead, a one-missing
lift constructs every nine-core except their union
\(T_0=S\cup\{a,b\}\).  A second one-missing lift constructs every
ten-core, including each \(T_0\cup\{d\}\), \(d\in D\), without ever
using a residual on \(T_0\).  Ordinary cubic exchange then resumes from
size ten and reaches the full thirteen-class core.  The resulting
three-dimensional full-core space contradicts the terminal
antiderivative--Wronskian inequality

\[
                              d^2-e\ge3^2-8=1>0.          \tag{3}
\]

## 2. A general one-missing lift

We use the following form of the partial-lift lemma.  It is important
that the anchors need not themselves be singleton classes.

**Lemma 2.1 (one missing deletion).**  Let

\[
                 T=R\mathbin{\dot\cup}\{x\},\qquad |R|=m,\qquad x\ne0,
                                                                    \tag{4}
\]

where the values are distinct and pairwise nonopposite.  For every
\(s\in R\), suppose that a nonzero residual

\[
                 q_s\in\mathbb C[z]_{\le m-3}             \tag{5}
\]

exists on \(T\setminus\{s\}\), with the usual compatible Robin rows.
Put

\[
                 g_s(z)=(z-s)(z+s)^2,qquad P_s=g_sq_s.   \tag{6}
\]

Then the \(P_s\) lie in one Robin kernel in
\(\mathbb C[z]_{\le m}\) and span at least three dimensions.  Hence a
nonzero linear combination has degree at most \(m-2\), the correct
bound \((m+1)-3\) for a residual on \(T\).

**Proof.**  The exchange identity

\[
 {B_{U\cup\{s\}}(z)g_s(z)q(z)\over
       \Delta_{U\cup\{s\}}(z)}
       ={B_U(z)q(z)\over\Delta_U(z)}                     \tag{7}
\]

shows that all \(P_s\) satisfy the same rows.  Equivalently, away from
the newly added node,

\[
 {g_s'(-t)\over g_s(-t)}
       =-\left({1\over t+s}-{2\over s-t}\right),
 \qquad g_s(-s)=g_s'(-s)=0.                              \tag{8}
\]

The polynomials \(g_s\) are pairwise coprime.  Thus the \(P_s\) cannot
span a line: a generator would be divisible by their degree-\(3m\)
product while having degree at most \(m\).

Suppose they span a pencil.  Remove its gcd \(H\), let
\(\phi=[p:q]\) be the resulting map of degree \(\delta\), and put
\(\epsilon=1\) if \(0\in R\), otherwise \(\epsilon=0\).  Among the
\(m-\epsilon\) nonzero anchors, let

\[
 \rho=\#\{s:H(s)=0\},\qquad
 \sigma=\#\{s:H(-s)=0\},                                \tag{9}
\]

and write \(e_0=\operatorname{ord}_0H\) and
\(\tau=\operatorname{ord}_{-x}H\).  A positive gcd order at a Robin
node cannot be one, so the degree bound gives

\[
 \deg H\ge \rho+2\sigma+e_0+\tau,qquad
 \delta\le m-\rho-2\sigma-e_0-\tau.                     \tag{10}
\]

For each nonabsorbed nonzero anchor, \(P_s/H\) vanishes at \(s\) and
twice at \(-s\).  Hence \(\phi(s)=\phi(-s)\).  If
\(u=m-\epsilon-\rho-\sigma\), the odd parity determinant

\[
                         C(z)=p(z)q(-z)-p(-z)q(z)         \tag{11}
\]

has the \(2u\) roots \(\pm s\), while

\[
                         u-\delta\ge
                    -\epsilon+\sigma+e_0+\tau.           \tag{12}
\]

Thus \(C=0\), except possibly when \(\epsilon=1\) and
\(\sigma=e_0=\tau=0\).  In that edge case \(u\ge\delta-1\), and the
factor \(g_0=z^3\) gives a zero of order at least three at the origin;
again the forced zero divisor exceeds \(\deg C\le2\delta-1\).  Therefore
\(\phi\) is even in every case.

For every nonzero \(s\) not absorbed at \(-s\), the double zero of
\(P_s/H\) ramifies \(\phi\) at \(-s\), and evenness supplies the paired
ramification at \(s\).  If \(\tau=0\), the unabsorbed Robin row at
\(-x\) ramifies \(\phi\) there and evenness supplies \(x\).  If
\(\epsilon=1,e_0=0\), the triple zero at the origin contributes two to
the ramification divisor.  With

\[
 I_x={\bf1}_{\tau=0},\qquad
 I_0={\bf1}_{\epsilon=1,e_0=0},                          \tag{13}
\]

half the forced ramification minus \(\delta-1\) is at least

\[
 \begin{aligned}
 m-\epsilon-\sigma+I_x+I_0-(\delta-1)
 &\ge1-\epsilon+\rho+\sigma+e_0+\tau+I_x+I_0\\
 &>0.                                                     \tag{14}
 \end{aligned}
\]

This contradicts Riemann--Hurwitz.  The pencil is impossible, proving
the lemma. \(\square\)

The proof used only the exchange identity, degree bounds, distinctness,
and nonoppositeness.  In particular, it did not use multiplicity one at
the anchors in \(R\).

## 3. The exact illegal-core census

A one-value-per-class eight-core is illegal precisely when it contains
every singleton class and no double class.  Since \(|S|=7\), it must
contain exactly one class of multiplicity at least three.  There are
exactly two such classes.  This proves (2), and there are no other
illegal eight-cores.

Let \({\cal P}_m(T)\) mean that the \(m\)-set \(T\) has a nonzero
residual of degree at most \(m-3\) satisfying its compatible Robin
system.  The simultaneous-Hermite lemma gives \({\cal P}_8(T)\) for
every eight-set other than \(I_a,I_b\).

## 4. Every nine-core except one

Let \(|T|=9\).  If none of its eight-deletions is (2), all nine
deletions satisfy \({\cal P}_8\), and the ordinary three-lift lemma gives
\({\cal P}_9(T)\).

If exactly one deletion is illegal, write

\[
                         T=I_a\cup\{d\}
             \quad\hbox{or}\quad T=I_b\cup\{d\},       \tag{15}
\]

where \(d\in D\).  The eight deletions indexed by the members of the
illegal core are legal; only deletion of \(d\) is missing.  Since a
double value is nonzero, Lemma 2.1 with \(m=8,x=d\) gives
\({\cal P}_9(T)\).

The only nine-set with two illegal deletions is

\[
                              T_0=S\cup\{a,b\}.           \tag{16}
\]

We leave \({\cal P}_9(T_0)\) completely unproved and unused.

## 5. Bypassing the missing nine-core at size ten

Let \(|U|=10\).  If \(T_0\not\subset U\), every nine-deletion of \(U\)
was constructed in Section 4, so ordinary cubic exchange gives
\({\cal P}_{10}(U)\).

If \(T_0\subset U\), then necessarily

\[
                              U=T_0\cup\{d\},\qquad d\in D. \tag{17}
\]

The nine deletions indexed by members of \(T_0\) are all known
nine-cores; only deletion of the nonzero double value \(d\) would require
the missing core \(T_0\).  Lemma 2.1 now applies with
\(m=9,R=T_0,x=d\), and gives \({\cal P}_{10}(U)\).

Thus every ten-set has the required residual.  From this point onward,
all deletions needed by ordinary cubic exchange exist.  It propagates
\({\cal P}_m\) for \(m=11,12,13\).  At the final lift step retain the
space rather than canceling its top two coefficients.  This gives

\[
 K\subset\mathbb C[z]_{\le12},\qquad \dim K\ge3,         \tag{18}
\]

in the full thirteen-class Robin kernel.

## 6. The terminal contradiction

For (1), the number of value classes and the collision excess are

\[
                 c=13,qquad e=21-13=8.                 \tag{19}
\]

The terminal half of the antiderivative--Wronskian theorem requires only
the full-core space (18).  For every \(q\in K\), all finite residues of

\[
 {B(z)q(z)\over(z+\mu)^4P(z)^2},qquad
 \deg B=e=8,                                             \tag{20}
\]

vanish.  Its unique rational antiderivative has an injective numerator
space \(J\subset\mathbb C[z]_{\le e-1}=\mathbb C[z]_{\le7}\), with
\(d=\dim J=\dim K\ge3\).  The repeated-value covariant jets force the
Wronskian deficit

\[
                              d^2-e>0.                   \tag{21}
\]

Indeed its least possible value is (3).  This is impossible, so profile
(1) cannot occur.  Together with the other third-order routes, this
empties the complete no-extra-singular \(h=8,k=3\) census.

## 7. Exact audit

[verify_live_three_zero_eighth_split_k3_two_illegal_core_bypass.py](../computations/verify_live_three_zero_eighth_split_k3_two_illegal_core_bypass.py)
checks the exact illegal-core census, every nine- and ten-set bypass
case, the generalized one-missing-lift inequalities including a zero
anchor, top-two-coefficient propagation, and the strict terminal deficit.
