# One-bad-core repair and completion of the eighth split at $k=1$

## 1. Result

Let

\[
 h=t-r-1,\qquad p=h+k,qquad k\ge1,                       \tag{1}
\]

and suppose an exceptional multiplicity profile has exactly $h$
singleton value classes.  Their value set will be denoted by $S$, so
$|S|=h$.  Among one-label-per-class $h$-cores, the only core which can
fail the singleton-row hypothesis is $S$ itself.

This note proves a uniform repair.

**Theorem 1.1 (one-bad-core repair).**  Suppose every isolated-star pivot
vanishes.  For every $(h+1)$-set $T$ of value classes there is a
nonzero residual

\[
                         q_T\in\mathbb C[z]_{\le h-2}      \tag{2}
\]

satisfying the Robin equations on $T$, even when

\[
                              T=S\cup\{x\}                \tag{3}
\]

for a repeated class $x$.  Consequently the ordinary cubic-exchange
induction starts at size $h+1$ and propagates through every larger value
core.

The only new point is an eight-of-nine, or in general $h$-of-$(h+1)$,
lift lemma.  The $h$ available lifts span at least three dimensions even
though the deletion indexed by $x$ is missing.  A possible zero
singleton is retained: its gauge $g_0=z^3$ supplies a triple zero in the
parity determinant before evenness is known, and a ramification
contribution two after evenness.

Apply the theorem to the last profile at the first higher frontier,

\[
 (h,k;\lambda)=(8,1;(3,2^4,1^8)).                        \tag{4}
\]

It produces the full exchange space which this profile alone was missing.
Its collision excess is $e=6$, so the terminal antiderivative--Wronskian
theorem gives a contradiction.  Together with the constant-role and
ordinary collision-excess closures, this eliminates all 35 collision
profiles formerly labelled R at $(h,k)=(8,1)$.

## 2. The unique illegal $h$-core

An $h$-set of value classes selected once each leaves a singleton row
class exactly when it contains a double class or omits a singleton class.
An illegal core must therefore contain every singleton and contain no
double.  When there are exactly $h$ singleton classes, its size forces
it to be precisely $S$.  Thus every $h$-core other than $S$ has a
nonzero Hermite residual

\[
                  q_R\in\mathbb C[z]_{\le h-3}.           \tag{5}
\]

Fix a repeated class $x$ and put $T=S\cup\{x\}$.  For each $s\in S$,
the deletion $T\setminus\{s\}$ is legal: the omitted singleton $s$
is untouched in the complement.  Hence all $h$ residuals

\[
                         q_{T\setminus\{s\}},\qquad s\in S, \tag{6}
\]

exist, including when $x$ is a triple or a higher-multiplicity class.
The class $x$ is repeated and therefore structurally nonzero.  At most
one member of $S$ may be zero.

## 3. The partial-lift lemma

We isolate the exact polynomial statement used in the repair.

**Lemma 3.1 (\(h\)-of-\((h+1)\) lifts).**  Let

\[
                         T=S\mathbin{\dot\cup}\{x\},
             \qquad |S|=h,\qquad x\ne0,                  \tag{7}
\]

where all values are distinct and no two are opposite.  For every
\(s\in S\), suppose a nonzero polynomial \(q_s\) of degree at most
\(h-3\) satisfies the Robin equations on \(T\setminus\{s\}\).  Put

\[
                         g_s(z)=(z-s)(z+s)^2,qquad
                         P_s=g_sq_s.                       \tag{8}
\]

Then the \(P_s\) have degree at most \(h\), satisfy one common Robin
system at all \(h+1\) nodes in \(T\), and span at least three dimensions.

The common-system assertion follows from

\[
 {g_s'(-a)\over g_s(-a)}=-\left({1\over a+s}-{2\over s-a}\right)
 \quad(a\ne s),qquad g_s(-s)=g_s'(-s)=0.                 \tag{9}
\]

Equivalently, the multiplicity-correct rational function is unchanged
when the missing class \(s\) is added.  This also covers \(s=0\), for
which \(g_0=z^3\).

### 3.1 Excluding a line

The cubics \(g_s\) are pairwise coprime.  If all \(P_s\) spanned a line,
its generator would be divisible by

\[
                              \prod_{s\in S}g_s,
\]

of degree \(3h\), although every \(P_s\) has degree at most \(h\).  Thus
the span is not one-dimensional.

### 3.2 A hypothetical pencil and its parity determinant

Suppose the span is a pencil.  Remove its gcd \(H\), write a basis as
\(Hp,Hq\) with \(\gcd(p,q)=1\), and let

\[
                           \phi=[p:q]:\mathbb P^1\to\mathbb P^1
\]

have degree \(\delta\ge1\).  Let \(\epsilon=1\) when \(0\in S\), and
put \(n=h-\epsilon\), the number of nonzero singleton anchors.  Among those
anchors let

\[
 \rho=|\{s:H(s)=0\}|,qquad
 \sigma=|\{s:H(-s)=0\}|.                                  \tag{10}
\]

Let \(e_0=\operatorname {ord}_0H\), with \(e_0=0\) when zero is not a
common root, and let \(\tau=\operatorname {ord}_{-x}H\).  A common root
at a Robin node is at least double, so every positive value of \(e_0\)
or \(\tau\) is at least two.  All roots counted below are distinct, and

\[
 \deg H\ge\rho+2\sigma+e_0+\tau,\qquad
 \delta\le h-\rho-2\sigma-e_0-\tau.                       \tag{11}
\]

For every nonzero \(s\) not absorbed at either \(s\) or \(-s\), the
member \(P_s/H\) vanishes at \(s\) and has a double zero at \(-s\).
Thus \(\phi(s)=\phi(-s)\).  At least

\[
                              u=n-\rho-\sigma              \tag{12}
\]

anchors survive this test.  The odd polynomial

\[
                    C(z)=p(z)q(-z)-p(-z)q(z)               \tag{13}
\]

has degree at most \(2\delta-1\) and has the \(2u\) roots \(\pm s\).
From (11),

\[
                           u-\delta\ge
                      -\epsilon+\sigma+e_0+\tau.          \tag{14}
\]

If the right side is nonnegative, (13) is identically zero.  The only
uncovered edge has

\[
                 \epsilon=1,\qquad\sigma=e_0=\tau=0,
                 \qquad u\ge\delta-1.                    \tag{15}
\]

Here \(H(0)\ne0\), and \(P_0/H\) has a zero of order at least three at
zero.  Use it as one basis member and choose the other member nonzero at
zero.  Then (13) has a zero of order at least three at zero.  Together
with the \(2u\ge2\delta-2\) nonzero roots, this exceeds its degree.  Thus
\(C\equiv0\) also in (15), and in every case

\[
                              \phi(z)=\phi(-z).             \tag{16}
\]

This is the point at which replacing \(g_0=z^3\) by a merely double-zero
gauge would lose the sharp edge.

### 3.3 The extra Robin node and ramification

For each nonzero \(s\in S\) with \(H(-s)\ne0\), the double zero of
\(P_s/H\) makes \(-s\) a ramification point.  Evenness supplies the
matching point \(s\).  These contribute at least \(2(n-\sigma)\) to the
ramification divisor.

If \(\tau=0\), the reduced pencil still satisfies the common Robin
equation at the ninth, or generally \((h+1)\)-st, node \(-x\).  Its
Wronskian vanishes there, so \(-x\) is ramified; evenness supplies \(x\).
This adds two more.  If \(\tau>0\), its multiplicity at least two has
already lowered the degree in (11).

Finally, if \(\epsilon=1\) and \(e_0=0\), the member \(P_0/H\) has a zero
of order at least three, contributing at least two at the ramification
point zero.  Define

\[
 I_x=\mathbf1_{\tau=0},\qquad
 I_0=\mathbf1_{\epsilon=1, e_0=0}.                        \tag{17}
\]

Half the forced ramification minus \(\delta-1\) is bounded below by

\[
 \begin{split}
 &n-\sigma+I_x+I_0-(\delta-1)\\
 &\qquad\ge
 1-\epsilon+\rho+\sigma+e_0+\tau+I_x+I_0>0.              \tag{18}
 \end{split}
\]

Thus the forced ramification is strictly greater than \(2\delta-2\), in
contradiction with Riemann--Hurwitz.  The hypothetical pencil cannot
exist, proving Lemma 3.1.

## 4. Repairing every \((h+1)\)-core and propagating upward

Apply Lemma 3.1 to \(T=S\cup\{x\}\).  Its at-least-three-dimensional
lift space lies in \(\mathbb C[z]_{\le h}\).  Cancel the coefficients of
\(z^h\) and \(z^{h-1}\); a nonzero member remains, of degree at most

\[
                             h-2=(h+1)-3.                  \tag{19}
\]

This proves (2) on every special set (3).

Every other \((h+1)\)-set has all of its \(h\)-deletions different from
\(S\).  All deletions are therefore legal, so the ordinary three-lift
lemma proves (2) there.  We have established property
\({\cal P}_{h+1}\) on every \((h+1)\)-set.  From this point onward every deletion required by
the ordinary cubic-exchange induction exists.  Top-two-coefficient
cancellation propagates \({\cal P}_m\) through every \(m\ge h+1\), and the
last lift step may be retained as a space of dimension at least three.

## 5. The profile \((3,2^4,1^8)\)

For (4), there are

\[
 c=13,\qquad M=19,\qquad e=M-c=6.                         \tag{20}
\]

Section 4 supplies a full exchange space

\[
                         K\subset\mathbb C[z]_{\le12},
                         \qquad\dim K\ge3.                \tag{21}
\]

The terminal half of the
[antiderivative--Wronskian theorem](live-three-zero-higher-split-antiderivative-wronskian.md)
requires only such a full space; its initial all-core legality hypothesis
was used solely to construct that space.  For each \(q\in K\), all finite
residues of

\[
 {B(z)q(z)\over(z+\mu)^2P(z)^2},
 \qquad \deg B=e=6,
\]

vanish.  The unique rational antiderivative has an injective numerator
space \(J\subset\mathbb C[z]_{\le e-1}=\mathbb C[z]_{\le5}\), still of
dimension \(d\ge3\).  At a repeated value \(v\), with
\(m_v=\lambda_v-1\), its covariant derivative vanishes to order \(m_v\).
Every nonbase node therefore has Wronskian weight \(m_v(d-1)\), while a
gcd root costs degree at least \(m_v+1\).  The global necessary deficit is
at least

\[
                              d^2-e\ge9-6=3>0.             \tag{22}
\]

This is impossible.  Hence (4) is closed.

## 6. Audit

[verify_live_three_zero_eighth_split_one_bad_core_repair.py](../computations/verify_live_three_zero_eighth_split_one_bad_core_repair.py)
checks the unique illegal core and every repaired deletion, the cubic lift
including zero, all pencil gcd inequalities, the triple-zero parity edge,
the extra-node and zero-node ramification counts, top-coefficient
cancellation and upward propagation, and the exact \(e=6\)
antiderivative--Wronskian deficit for multiplicities \((2,1,1,1,1)\).
