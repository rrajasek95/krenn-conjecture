# Higher collisions: the double-guard shadow bypass

## 1. Result

Put

\[
 h=t-r-1,\qquad p=h+k,\qquad k\ge1,
 \qquad M=2h+k+2.                                      \tag{1}
\]

Let an exceptional multiplicity profile have \(c\) distinct value
classes, and write

\[
 S=\{v:\lambda_v=1\},\qquad
 D=\{v:\lambda_v=2\},\qquad
 H=\{v:\lambda_v\ge3\}.                               \tag{2}
\]

Thus \(V=S\mathbin{\dot\cup}D\mathbin{\dot\cup}H\).  Repeated values
are structurally nonzero, distinct value classes are pairwise
nonopposite, and at most one singleton value is zero.

**Theorem 1.1 (double-guard full exchange).**  Suppose

\[
                         c\ge h+1,qquad |D|\ge1.         \tag{3}
\]

If every isolated-star pivot vanishes, then cubic exchange produces a
full-core space

\[
 K\subset\mathbb C[z]_{\le c-1},\qquad \dim K\ge3.       \tag{4}
\]

No hypothesis that every initial \(h\)-value core is legal is needed.

Consequently, by the antiderivative--Wronskian theorem, every profile
satisfying (3) and

\[
                         1\le e=M-c\le8                  \tag{5}
\]

is impossible on the no-extra-singular stratum.

The mechanism is a simplicial shadow calculation.  All illegal
\(h\)-cores consist of every singleton class, no double class, and a
fixed-size subset of \(H\).  One-missing-deletion lifts carry this entire
family upward through the Boolean lattice.  At the top of the
non-double classes only one missing core remains, and adjoining any
double supplies the nonzero guard needed to bypass it.

## 2. The one-missing-deletion lemma

We recall the multiplicity-free form of the partial-lift argument.

**Lemma 2.1.**  Let

\[
                         T=R\mathbin{\dot\cup}\{x\},
             \qquad |R|=m,\qquad x\ne0.                 \tag{6}
\]

Suppose that for every \(s\in R\), the deletion \(T\setminus\{s\}\)
has a nonzero residual \(q_s\) of degree at most \(m-3\).  Then the
lifts

\[
                 (z-s)(z+s)^2q_s(z),\qquad s\in R,       \tag{7}
\]

belong to one Robin kernel in \(\mathbb C[z]_{\le m}\) and span at
least three dimensions.  In particular, cancellation of their top two
coefficients produces a residual of degree at most
\(m-2=(m+1)-3\) on \(T\).

The proof is the \(m\)-of-\((m+1)\) parity--ramification argument.  It
uses only the exact gauge identity

\[
 g_s=(z-s)(z+s)^2,qquad
 {g_s'(-a)\over g_s(-a)}
   =-\left({1\over a+s}-{2\over s-a}\right),             \tag{8}
\]

pairwise coprimality of the \(g_s\), and the fact that \(x\ne0\).  If
the lift span were a pencil, remove its gcd and call the resulting map
\(\phi\).  The special members give \(\phi(s)=\phi(-s)\); the odd parity
determinant, with the triple-zero factor \(g_0=z^3\) in the only zero
edge case, makes \(\phi\) even.  The double zeros at \(-s\), together
with the extra Robin node \(-x\), then exceed the
Riemann--Hurwitz ramification degree.  This proof neither assumes that
the anchors in \(R\) are singleton classes nor uses their
multiplicities.  A complete gcd-order calculation is given in
[the two-illegal-core bypass](live-three-zero-eighth-split-k3-two-illegal-core-bypass.md#2-a-general-one-missing-lift).

## 3. The initial bad family

For an \(h\)-set \(T\subset V\), selecting one label from every class,
the complement has a singleton row class exactly when

* \(T\) contains a double class, whose unselected mate remains; or
* \(T\) omits a singleton class.

Therefore the illegal family is exactly

\[
 {\cal B}_h=
 \left\{S\cup U:U\in\binom{H}{h-|S|}\right\},           \tag{9}
\]

with the convention that it is empty unless
\(0\le h-|S|\le|H|\).  Every \(h\)-set outside (9) has the usual
simultaneous-Hermite residual

\[
                         0\ne q_T\in\mathbb C[z]_{\le h-3}. \tag{10}
\]

## 4. Propagating the bad shadow

For \(m\ge h\), let \({\cal P}_m(T)\) mean that the \(m\)-set \(T\)
has a nonzero residual of degree at most \(m-3\).  Put

\[
 {\cal B}_m=
 \left\{S\cup U:U\in\binom{H}{m-|S|}\right\}.           \tag{11}
\]

We prove inductively, for

\[
                         h\le m\le |S|+|H|,              \tag{12}
\]

that \({\cal P}_m(T)\) holds for every \(m\)-set outside
\({\cal B}_m\).  The case \(m=h\) is Section 3.

There is one immediate endpoint.  If \(|S|=h\), then
\({\cal B}_h=\{S\}\).  Every \((h+1)\)-set containing it has just one
missing deletion, indexed by an added repeated class and hence by a
nonzero value.  Lemma 2.1 constructs all \((h+1)\)-sets, after which
ordinary exchange applies.  If \(c=h+1\), retain the Lemma 2.1 lift span
on this already-final step; if \(c>h+1\), retain the ordinary lift span
when the later final step is reached.  Either way (4) follows at this
endpoint.  We may therefore assume below that

\[
                              h-|S|\ge1.                 \tag{12a}
\]

Fix an \((m+1)\)-set \(T\).  If two distinct deletions
\(T\setminus\{x\}\) and \(T\setminus\{y\}\) lie in
\({\cal B}_m\), then both contain every singleton and no double.  It
follows that \(T\) itself contains every singleton, contains no double,
and all its other members lie in \(H\).  Thus

\[
 \#\{x\in T:T\setminus\{x\}\in{\cal B}_m\}\ge2
       \quad\Longrightarrow\quad T\in{\cal B}_{m+1}.    \tag{13}
\]

Conversely, by (12a), a member of \({\cal B}_{m+1}\) has at least two
such deletions throughout the range in (12).  We simply continue to
leave those sets unconstructed.

If \(T\notin{\cal B}_{m+1}\), it therefore has either zero or one
unconstructed deletion.  With zero, the ordinary three-lift lemma gives
\({\cal P}_{m+1}(T)\).  With one, write the missing deletion as
\(T\setminus\{x\}\).  Because that deletion contains every singleton,
\(x\notin S\); because \(T\notin{\cal B}_{m+1}\) and (12a) holds, the
added class cannot belong to \(H\).  Hence

\[
                              x\in D.                    \tag{14}
\]

In particular \(x\ne0\).  The other \(m\) deletions are constructed,
so Lemma 2.1 gives \({\cal P}_{m+1}(T)\).  This proves the induction.

At

\[
                              m_0=|S|+|H|=c-|D|,          \tag{15}
\]

the bad family consists of the single set \(S\cup H\).  At size
\(m_0+1\), no family (11) remains: every such extension which contains
that last bad set adjoins a double, and Lemma 2.1 bypasses its sole
missing deletion.  Thus every \((m_0+1)\)-set is constructed.  Ordinary
cubic exchange propagates from there through every larger set size.

If \(|D|=1\), the step \(m_0+1=c\) is already the final one; retain the
at-least-three-dimensional lift span supplied by Lemma 2.1.  If
\(|D|>1\), retain the ordinary three-lift span on the final step.  In
both cases this gives (4), proving Theorem 1.1.

## 5. The collision-excess corollary

The terminal antiderivative construction depends only on the existence
of (4), not on how it was built.  It maps \(K\) injectively to a
same-dimensional numerator space

\[
                         J\subset\mathbb C[z]_{\le e-1}. \tag{16}
\]

At every repeated value \(v\), with \(m_v=\lambda_v-1\), its covariant
derivative misses \(m_v\) consecutive jets.  After every possible gcd
correction, a \(d\)-dimensional space would require

\[
                         0\ge d^2-e.                     \tag{17}
\]

But \(d=\dim J=\dim K\ge3\), so (5) makes the right side at least one.
This proves the corollary.

The profile \(3^2 2^4 1^7\) at \((h,k)=(8,3)\) is the first sharp
two-hole example: (11) has two members at size eight, their union is the
only bad nine-set, and a double guard removes it at size ten.  The
standalone proof records that instance in full detail.

## 6. Exact audit

[verify_live_three_zero_higher_split_double_guard_shadow_bypass.py](../computations/verify_live_three_zero_higher_split_double_guard_shadow_bypass.py)
exhausts the Boolean-shadow recurrence against literal deletion counts,
checks that every unique missing deletion is indexed by a nonzero
repeated class at the \(|S|=h\) endpoint and by a nonzero double in the
genuine shadow recurrence, explicitly audits the \(|D|=1\) retained
final span,
audits the one-missing parity and ramification inequalities including a
zero singleton, and verifies the terminal \(d^2-e\) bound.
