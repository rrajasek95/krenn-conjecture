# Higher collisions: the antiderivative--Wronskian closure

## 1. Result

Put

\[
 h=t-r-1,\qquad p=h+k,\qquad k\ge1,
 \qquad M=2h+k+2.                                         \tag{1}
\]

Let the exceptional multiplicity profile have \(c\) distinct value classes,

\[
 \lambda=(\lambda_v:v\in V),\qquad
 \sum_v\lambda_v=M,\qquad
 e=M-c=\sum_v(\lambda_v-1).                               \tag{2}
\]

The number \(e\) is the collision excess.  Assume that \(c\ge h+1\) and
that every one-label-per-class \(h\)-core leaves a singleton in its
complement.  Equivalently, if \(n_1,n_2\) count singleton and double
classes, assume

\[
                         n_1\ge h+1
                  \quad\hbox{or}\quad n_2\ge c-h+1.        \tag{3}
\]

This is the exact legality criterion proved in the companion value-core
exchange note.

**Theorem 1.1 (collision-excess closure).**  Under (1)--(3), a collision
profile with

\[
                              1\le e\le8                   \tag{4}
\]

is impossible on the no-extra-singular stratum.

The proof uses the full polynomial space produced by cubic exchange, but
replaces the value-node Wronskian count by its rational antiderivative.
The numerator degree of that antiderivative is at most \(e-1\), independent
of \(c,h,k\).  Repeated values force missing local jets whose total weight
is \(e(d-1)\); a gcd can only strengthen the inequality.  The resulting
deficit is at least \(d^2-e>0\).

## 2. The full exchange space

Assume for contradiction that all isolated-star pivots vanish.  By (3),
every \(h\)-value core has a nonzero Hermite residual of degree at most
\(h-3\).  Cubic exchange and top-coefficient cancellation propagate these
residuals through all proper value cores.  At the last step retain the lift
span.  It gives a space

\[
 K\subset\mathbb C[z]_{\le c-1},\qquad d:=\dim K\ge3.      \tag{5}
\]

Put

\[
 B(z)=\prod_{v\in V}(z-v)^{\lambda_v-1},\qquad
 P(z)=\prod_{v\in V}(z+v).                                \tag{6}
\]

For \(q\in K\), the multiplicity-correct full-core rational function is

\[
                    F_q(z)={B(z)q(z)\over
                    (z+\mu)^{k+1}P(z)^2}.                 \tag{7}
\]

Every pole \(-v\) has zero residue by the full-core Robin equations.
Moreover,

\[
 \deg B=e,qquad \deg q\le c-1,qquad
 F_q(z)=O\bigl(z^{-2(c-h)}\bigr)=O(z^{-2}).                \tag{8}
\]

There is no residue at infinity.  The residue theorem therefore also kills
the residue at the only remaining pole, \(-\mu\).  Thus **every** finite
residue of \(F_q\) vanishes.

## 3. The unique rational antiderivative

A rational function has a rational antiderivative precisely when all of
its finite residues vanish.  Choose the unique antiderivative of \(F_q\)
which vanishes at infinity.  The double poles at \(-v\) become simple and
the pole of order at most \(k+1\) at \(-\mu\) becomes order at most \(k\).
Consequently it has the form

\[
                 {R_q(z)\over D_0(z)},\qquad
                 D_0(z)=(z+\mu)^kP(z).                    \tag{9}
\]

The decay in (8) makes this representation sharply small.  Since
\(\deg D_0=k+c\),

\[
\begin{split}
 \deg R_q
 &\le k+c-\bigl(2(c-h)-1\bigr)\\
 &=2h+k+1-c=e-1.                                          \tag{10}
\end{split}
\]

Notice that

\[
 \deg D_0-(e-1)=2(c-h)-1\ge1.                             \tag{11}
\]

Thus a zero derivative cannot hide a nonzero constant multiple of
\(D_0\).  The assignment \(q\mapsto R_q\) is linear and injective.  Its
image

\[
                 J=\{R_q:q\in K\}\subset
                 \mathbb C[z]_{\le e-1}                   \tag{12}
\]

therefore also has dimension \(d\ge3\).

Differentiating (9) and comparing with (7) gives the exact polynomial
identity

\[
 Bq=(z+\mu)P R_q'
       -\bigl(kP+(z+\mu)P'\bigr)R_q.                       \tag{13}
\]

Equivalently, with \(D=d/dz\),

\[
 {Bq\over(z+\mu)P}
       =\left(D-{D_0'\over D_0}\right)R_q.                \tag{14}
\]

## 4. Missing jets at the unreflected collision values

Fix a repeated value \(v\), and put

\[
                              m_v=\lambda_v-1\ge1.         \tag{15}
\]

The point here is \(z=+v\), not the Robin pole \(-v\).  Structural
admissibility makes \((z+\mu)P(z)\) a local unit at \(v\): repeated values
are nonzero, no two value classes are opposite, and \(v+\mu\ne0\).
Because \((z-v)^{m_v}\mid Bq\), equation (14) says

\[
 \left(D-{D_0'\over D_0}\right)R=O((z-v)^{m_v})
                         \qquad(R\in J).                  \tag{16}
\]

Locally divide by the unit \(D_0\).  Equation (16) becomes

\[
                         (R/D_0)'=O((z-v)^{m_v}).          \tag{17}
\]

Suppose first that \(J\) has no basepoint at \(v\).  One locally gauged
section has nonzero constant term.  Subtract its multiples from the other
\(d-1\) sections.  Equation (17) says that those sections have no terms of
orders \(1,\ldots,m_v\), so their vanishing orders are at least

\[
                       m_v+1,m_v+2,\ldots,m_v+d-1.         \tag{18}
\]

The vanishing sequence is therefore at least

\[
                       0,m_v+1,m_v+2,\ldots,m_v+d-1,       \tag{19}
\]

and the Wronskian weight at \(v\) is at least

\[
                              m_v(d-1).                    \tag{20}
\]

Now suppose the gcd of \(J\) vanishes to order \(t\ge1\) at \(v\).  After
the same unit gauge, a reduced section nonzero at \(v\) has leading term
\((z-v)^t\).  Its derivative has exact order \(t-1\), in characteristic
zero.  Equation (17) forces

\[
                              t\ge m_v+1.                  \tag{21}
\]

Thus absorbing a collision node into the gcd costs one degree more than
its multiplicity in \(B\).

A possible zero exceptional class causes no edge case.  It is necessarily
a singleton, hence has \(m_v=0\) and is not a root of \(B\).  Every point
used in (15)--(21) is a repeated, structurally nonzero value.

## 5. The gcd-corrected Wronskian contradiction

Let \(H=\gcd J\), write \(g=\deg H\), and divide it out.  Let \(S\) be the
set of collision nodes absorbed by \(H\), and put

\[
                         a=\sum_{v\in S}m_v.               \tag{22}
\]

Equation (21) gives the stronger estimate

\[
                         g\ge\sum_{v\in S}(m_v+1)\ge a.   \tag{23}
\]

At the nonbase collision nodes, (20) forces total Wronskian weight at least

\[
                             (e-a)(d-1).                   \tag{24}
\]

The reduced polynomial space has dimension \(d\) and degree at most
\(e-1-g\).  Its nonzero Wronskian has degree at most

\[
                         d(e-g-d).                         \tag{25}
\]

For (24) to fit inside (25), one would need

\[
                         (e-a)(d-1)\le d(e-g-d).           \tag{26}
\]

But the left side minus the right side is

\[
             d^2-e+d(g-a)+a\ge d^2-e.                     \tag{27}
\]

When \(d\ge3\) and \(e\le8\), (27) is at least one.  This contradicts
(26) and proves Theorem 1.1.

## 6. The first higher frontier

At \((h,k)=(8,1)\), the earlier H/S/C/L/Q/V census had 35 profiles in R.
The two constant-core role theorems close 17 of them.  The present theorem
closes 19; their union contains exactly 34 profiles.  The sole profile not
covered by either theorem is

\[
                         (3,2,2,2,2,1^8).                  \tag{28}
\]

It has \(c=13\) and \(e=6\), but fails (3), so the full value-core exchange
cannot be started.  This is now the smallest residual target.

In particular, the eight double/single old-R profiles

\[
                         (2^d,1^{19-2d}),\qquad1\le d\le8, \tag{29}
\]

all satisfy (3), and their collision excess is \(e=d\le8\).  They are
closed by Theorem 1.1.  The ninth double/single profile \((2^9,1)\) was
already closed by the direct value-core residue--Wronskian theorem.
Therefore no double/single profile remains at \((h,k)=(8,1)\).

## 7. Exact audit

[verify_live_three_zero_higher_split_antiderivative_wronskian.py](../computations/verify_live_three_zero_higher_split_antiderivative_wronskian.py)
checks the primitive and degree formulas, differentiates (9) to reconstruct
(13) for every small \(k\), audits injectivity using (11), verifies the
local unit gauge and sharp Wronskian weight, exhausts every gcd correction
for \(e\le8\), treats the zero singleton, and independently reconstructs
the 34/35 union census and all eight profiles in (29).
