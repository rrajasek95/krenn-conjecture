# The eighth split at \(k=5\): current exact collision census

## 1. Frozen baseline

Put

\[
 h=8,\qquad p=13,\qquad k=5,\qquad M=p+h+2=23.       \tag{1}
\]

The frozen no-extra-singular \(H/S/C/L/Q/V\) classifier gives

\[
\begin{array}{c|rrrrrrrr}
 &H&S&C&L&Q&V&R&D\\ \hline
 (8,13)&637&501&30&23&19&0&44&1.
\end{array}                                             \tag{2}
\]

Thus the initial fifth-order residual slice has exactly 44 collision
profiles.  This ledger credits a profile only when a complete proof note
and an exact passing checker are present; exploratory routes receive no
credit.

## 2. Accepted closures

The first eighteen accepted closures, in chronological order, were:

\[
                              2^{11}1,
 \quad 2^{10}1^3,
 \quad 4^2 3^5,
 \quad 3^5 2^4,
 \quad 3^4 2^5 1,
 \quad 3^5 2^3 1^2,
 \quad 3^4 2^4 1^3,
 \quad 3^3 2^4 1^6,
 \quad 3^4 2 1^9,
 \quad 3^3 2^7,
 \quad 3^5 2^2 1^4,
 \quad 3^5 2 1^6,
 \quad 3^5 1^8,
 \quad 3^4 2^3 1^5,
 \quad 3^4 2^2 1^7,
 \quad 3^4 1^{11},
 \quad 3^3 2^6 1^2,
 \quad 3^3 2^3 1^8.                                   \tag{3}
\]

The first is proved in
[the eleven-double matching closure](live-three-zero-eighth-split-k5-eleven-double-one-singleton-matching-closure.md).
Five formal double layers give a cubic relation pencil; a fourth Boolean
difference gives \(e_2=0\) on near-perfect matchings of \(K_9\), and the
zero-increment and one-forbidden-edge lemmas finish the contradiction.

The second is proved in
[the ten-double projective matching closure](live-three-zero-eighth-split-k5-ten-double-three-singleton-projective-matching-closure.md).
Four formal double layers and two formal singleton layers again give a
cubic relation pencil.  The fourth row-minor difference yields a
nondegenerate projective quadratic pairing on perfect matchings of \(K_8\).
Its exact equality backtrack forces a monochromatic \(K_5\), contradicting
a quartic fibre bound.

Three further profiles are proved together in
[the fifth-order formal-five-layer increment](live-three-zero-eighth-split-k5-formal-five-layer-increment.md).
The all-order theorem gives complementary root signatures
\((c,s)=(7,5),(5,1),(5,1)\), respectively, and in each case
\(s>2c-10\).  Its exhaustive checker verifies every five-layer choice and
all ten pair-drop cores, including every possible singleton-zero placement,
and certifies that the theorem adds no fourth profile.

The sixth and seventh are proved in
[the five-triple saturated-cubic closure](live-three-zero-eighth-split-k5-five-triple-saturated-cubic-robin-rectangle-closure.md).
Selecting all three doubles and any two triples gives complementary
profile \(3^3 1^4\).  Its four simple roots saturate the Wronskian of the
cubic relation pencil.  The accessory residue sum and a choose-two Boolean
rectangle force every four of the five triple values to sum to zero.  For
\(3^4 2^4 1^3\), selecting all four doubles and one triple gives the same
complement.  The top three accessory moments put all four triple values on
one fixed nonzero quadratic.

Two mixed formal-role selections close the eighth and ninth profiles in
[the mixed linear-plane increment](live-three-zero-eighth-split-k5-mixed-linear-plane-increment.md).
Selecting two doubles and six singletons in (3^3 2^4 1^6), or one
double and eight singletons in (3^4 2 1^9), fills the entire linear
dual plane.  Exact complementary residues then give, respectively, a
quadratic-fibre contradiction and a nonzero-unit contradiction.

The tenth profile is closed in
[the seven-double formal linear-plane closure](live-three-zero-eighth-split-k5-seven-double-formal-linear-plane-closure.md).
Any five formal double layers again fill the linear dual plane.  Swapping
selected and complementary doubles would put six distinct values in one
fibre of a nonzero quadratic rational map.

Seven further profiles are closed in
[the unified pair-drop linear-plane theorem](live-three-zero-eighth-split-k5-unified-pair-drop-linear-plane-closure.md).
The theorem permits any mix of \(d\) formal double roles and \(10-2d\)
formal singleton roles, as well as the sole triple--zero illegal core.
For six profiles, the complementary signature \(3^4 1\) makes the two
relations fill the linear space and the simple complementary residue is
impossible.  For \(3^3 2^6 1^2\), complementary-double swaps put five
distinct values in one quadratic fibre.  An independent adversarial audit
checked the missing-edge span, dual degree, all complement signatures, and
the exact profile enumeration.

The eighteenth profile is closed in
[the three-double second-jet theorem](live-three-zero-eighth-split-k5-three-double-second-jet-closure.md).
For \(3^3 2^3 1^8\), the same full linear relation space kills both
the first and second logarithmic jets at each complementary double.
Selected/outside swaps make all three double values pairwise isotropic for
\(5a^2+2ab+5b^2\); subtracting the three pair equations contradicts their
distinctness.  The signs and elimination were independently checked.

The
[all-order selected-lift incidence census](live-three-zero-eighth-split-all-order-mixed-role-census.md)
then closes exactly 25 of the remaining profiles:

\[
\begin{gathered}
3^3 2^2 1^{10},\quad3^3 2 1^{12},\quad3^3 1^{14};\\
3^2 2^5 1^7,\quad3^2 2^4 1^9,\quad3^2 2^3 1^{11},
 \quad3^2 2^2 1^{13},\quad3^2 2 1^{15},\quad3^2 1^{17};\\
3 2^6 1^8,\quad3 2^5 1^{10},\quad3 2^4 1^{12},
 \quad3 2^3 1^{14},\quad3 2^2 1^{16},
 \quad3 2 1^{18},\quad3 1^{20};\\
2^d1^{23-2d}\qquad(1\leq d\leq9).
\end{gathered}                                           \tag{4}
\]

These are uniform selected-kernel closures, not 25 unrelated profile
calculations.  The
[ten-singleton incidence theorem](live-three-zero-eighth-split-all-order-ten-singleton-incidence-closure.md)
handles \(d=0\) formal selections.  The
[low mixed-role incidence theorem](live-three-zero-eighth-split-all-order-low-mixed-role-incidence-closure.md)
uses parity-saturated quotient pencils, exact-row gcd costs, and
hyperplane intersections to eliminate every formal selection with
\(d=1,2,3\).  Its proof includes a possible zero singleton and the unique
triple--zero missing edge.  In particular, it closes the formerly isolated
pure profile \(2^9 1^5\).  The exact all-order census verifies that the 25
profiles in (4) are precisely the new fifth-order increment after the first
eighteen attributions.

The sole remaining profile \(3^2 2^8 1\) is closed by the
[five-double six-class residue theorem](live-three-zero-eighth-split-all-order-five-double-six-class-residue-closure.md).
Five selected exact-double layers give an exact four-dimensional kernel and
a two-dimensional dual plane in the six-class complement.  Its simple root
puts \((z-r)^2\) in that plane; varying the three complementary doubles then
forces five, or all seven, double values into one fibre of a quadratic
rational map.

Thus the accepted attribution is

\[
                              44=18+25+1.                \tag{5}
\]

## 3. Empty open ledger

Every one of the 44 frozen fifth-order residual profiles now has a complete
proof note and an exact passing checker.  The exact open ledger is empty.
This is a complete result for the frozen no-extra-singular \(h=8,k=5\)
collision slice; it is not by itself an all-\(k\), all-\(h\), or global
proof of the conjecture.

## 4. Exact audit

[verify_live_three_zero_eighth_split_k5_updated_census.py](../computations/verify_live_three_zero_eighth_split_k5_updated_census.py)
recomputes the frozen classifier counts, independently specifies all 44
residual profiles, preserves the disjoint historical attribution
\(18+25+1\), checks every accepted proof artifact, and verifies that the
open ledger is empty.
