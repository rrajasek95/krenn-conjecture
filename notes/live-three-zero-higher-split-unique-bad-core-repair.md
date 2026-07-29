# Unique-illegal-core repair for higher collision profiles

## 1. Result

Put

\[
 h=t-r-1,\qquad p=h+k,\qquad M=2h+k+2,
\]

and let an exceptional multiplicity profile have \(c\) value classes.
Write \(n_1,n_2,n_{\ge3}\) for the numbers of singleton, double, and
multiplicity-at-least-three classes.  An \(h\)-value core is *legal* when
selecting one label in each of its classes leaves a singleton class in the
complement.

**Theorem 1.1 (unique-bad-core repair).**  Suppose that exactly one
\(h\)-value core is illegal.  If all isolated-star pivots vanish, cubic
exchange nevertheless produces a full-core space

\[
 K\subset\mathbb C[z]_{\le c-1},\qquad \dim K\ge3.       \tag{1}
\]

Consequently every such profile with collision excess

\[
 e=M-c\le8                                                \tag{2}
\]

is impossible by the antiderivative--Wronskian theorem.

The numerical hypothesis has the exact closed form

\[
 \binom{n_{\ge3}}{h-n_1}=1,
 \quad 0\le h-n_1\le n_{\ge3},                           \tag{3}
\]

or equivalently

\[
             n_1=h\quad\hbox{or}\quad n_1+n_{\ge3}=h.
                                                                    \tag{4}
\]

The first alternative is the all-singleton bad core treated in the
one-bad-core note.  The second alternative is new: the unique bad core
contains every singleton and every class of multiplicity at least three.

## 2. Counting illegal cores

A one-label-per-class core fails to leave a singleton precisely when it
contains every singleton class and contains no double class.  Therefore an
illegal core consists of all \(n_1\) singleton classes and
\(h-n_1\) of the \(n_{\ge3}\) higher classes.  This proves (3).  When an
illegal core exists, its number is one precisely at the two endpoints of
the binomial row, proving (4).

Denote the unique illegal core by \(S\), so \(|S|=h\).  Every value class
\(x\notin S\) is repeated, hence structurally nonzero.  For the special
\((h+1)\)-core

\[
                         T=S\mathbin{\dot\cup}\{x\},      \tag{5}
\]

the deletion \(T\setminus\{x\}=S\) is unavailable, but every deletion
\(T\setminus\{s\}\), \(s\in S\), is legal because it is a different
\(h\)-core.  Thus the singleton-row Hermite reduction supplies

\[
 0\ne q_s\in\mathbb C[z]_{\le h-3}
 \quad\text{for every }s\in S.                           \tag{6}
\]

## 3. The partial lift applies without a singleton assumption

Set

\[
                  g_s(z)=(z-s)(z+s)^2,\qquad P_s=g_sq_s. \tag{7}
\]

Lemma 3.1 of
[the one-bad-core repair](live-three-zero-eighth-split-one-bad-core-repair.md)
is stated for a set \(S\) of distinct, pairwise nonopposite values and a
nonzero value \(x\notin S\).  Its proof uses only those properties and the
existence of the \(h\) residuals (6); it never uses that the members of
\(S\) have multiplicity one.  It therefore applies verbatim here.

The polynomials \(P_s\) lie in one common Robin kernel on \(T\), have
degree at most \(h\), and span at least three dimensions.  The gcd-corrected
parity determinant handles the possible zero member of \(S\) through
\(g_0=z^3\); the extra node \(-x\) then makes a hypothetical pencil exceed
the Riemann--Hurwitz ramification bound.  Cancelling the top two
coefficients in this at-least-three-dimensional span leaves a nonzero

\[
                         q_T\in\mathbb C[z]_{\le h-2}.    \tag{8}
\]

For every other \((h+1)\)-core, all \(h\)-deletions are legal, because no
deletion equals \(S\).  The ordinary three-lift lemma gives (8) there as
well.  Hence exchange is repaired on every core of size \(h+1\), after
which the usual top-two cancellation propagates to every larger core and
gives (1) at the terminal step.

## 4. Terminal contradiction and the eighth-split additions

The initial all-core-legality assumption in the antiderivative--Wronskian
proof is used only to construct (1).  Once (1) is available, its rational
antiderivative has an injective numerator space of the same dimension
\(d\ge3\) in degree at most \(e-1\).  Collision jets force a Wronskian
deficit at least

\[
                              d^2-e.                      \tag{9}
\]

Thus (2) makes (9) positive and proves Theorem 1.1.

At \((h,k,M)=(8,2,20)\), the new endpoint in (4) closes the two frozen
residual profiles

\[
             3^2 2^4 1^6\quad(e=8),\qquad
             3\,2^5 1^7\quad(e=7).                       \tag{10}
\]

Their unique illegal cores are respectively the six singleton values plus
both triple values, and the seven singleton values plus the sole triple
value.

## 5. Audit

[verify_live_three_zero_higher_split_unique_bad_core_repair.py](../computations/verify_live_three_zero_higher_split_unique_bad_core_repair.py)
checks the binomial characterization against literal core enumeration,
checks every special deletion and the nonzero outside class, imports the
partial-lift inequalities and terminal deficit audit, and identifies the
two exact additions (10) in the frozen \(h=8,k=2\) residual table.
