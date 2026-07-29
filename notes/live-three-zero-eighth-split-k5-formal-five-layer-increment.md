# The eighth split at \(k=5\): the formal-five-layer increment

## 1. Result

Apply the
[all-order formal-five-layer duality theorem](live-three-zero-eighth-split-all-order-formal-five-layer-duality.md)
to the 42 profiles left after the first two fifth-order closures.  It closes
exactly

\[
                  4^2 3^5,\qquad 3^5 2^4,
                  \qquad 3^4 2^5 1.                    \tag{1}
\]

No other currently open \((h,k)=(8,5)\) profile satisfies this theorem.

Recall its criterion.  Choose five repeated value classes and use two
labels from each as formal double layers.  All ten cores obtained by
lowering two distinct layers must be legal.  After subtracting those ten
labels, let \(c\) be the number of complementary value classes and \(s\)
the number of simple complementary roots.  The profile is impossible if

\[
                         c<5\qquad\hbox{or}\qquad
                         s>2c-10.                        \tag{2}
\]

At fifth order the complementary polynomial always has degree
\(k+8=13\).

## 2. The three witnesses

For \(4^2 3^5\), select all five triple classes.  The complementary
profile and root signature are

\[
                         (4,4,1^5),\qquad(c,s)=(7,5).    \tag{3}
\]

Every pair drop lowers two triples to role one.  The other three selected
triples retain one unselected label apiece, so every one of the ten cores
has three nonzero singleton guards.  Equation (2) applies because
\(5>2\cdot7-10=4\).

For \(3^5 2^4\), select any one triple and all four doubles.  Then

\[
                           (3^4,1),\qquad(c,s)=(5,1).    \tag{4}
\]

There are six drops involving two doubles; the two lowered doubles and the
unlowered selected triple give three singleton guards.  There are four
drops involving the triple and one double; the lowered double itself gives
one singleton guard.  These guards lie at repeated input values and hence
are structurally nonzero.  Thus all ten cores are legal, and
\(1>2\cdot5-10=0\).  The five choices of selected triple are equivalent but
are all checked.

For \(3^4 2^5 1\), select all five doubles.  Its complement again has

\[
                           (3^4,1),\qquad(c,s)=(5,1).    \tag{5}
\]

Every pair drop leaves singleton mates at the two lowered double values.
Both are nonzero.  Consequently all ten cores remain legal even if the
original singleton in (5) is the exceptional zero value.  The same strict
inequality \(1>0\) proves the closure.

## 3. Exhaustiveness on the current ledger

The exact scan starts from all 44 frozen profiles, removes only the two
previously accepted profiles \(2^{11}1\) and \(2^{10}1^3\), and examines
every five-subset of repeated classes in each of the remaining 42 profiles.
For every choice it examines all ten pair drops.  Legality is required for
every possible placement of the exceptional zero among the original
singleton classes; a residual singleton inherited from a repeated input
class is always nonzero.

There are 1,365 five-layer choices and 44,850 pair-core/zero-placement
tests.  Exactly 1,104 choices have ten legal cores.  Among those, exactly
seven choices satisfy (2): the unique choices in the first and third
profiles of (1), and the five choices of triple in the middle profile.
Their image consists of exactly the three profiles (1).  Hence the theorem
closes no other member of the current open ledger.

## 4. Exact audit

[verify_live_three_zero_eighth_split_k5_formal_five_layer_increment.py](../computations/verify_live_three_zero_eighth_split_k5_formal_five_layer_increment.py)
recomputes the frozen slice, enumerates every five-layer choice and all ten
cores, audits every singleton-zero scenario, checks (3)--(5) and the strict
Wronskian inequalities, and verifies the exhaustive \(5\)-closed,
\(39\)-open ledger.
