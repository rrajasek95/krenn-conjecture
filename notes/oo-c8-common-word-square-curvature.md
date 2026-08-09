# Common-word square curvature on the active OO regressions

The one-leader quotient leaves 113 profiles whose two active cofactor
leaders have distinct words on the common five sites.  This note tests the
next proposal: place the words in a Hamming `2`-face and take the
alternating second difference of both cofactor functions.

## Geometry of the leader words

Their common-five Hamming distances are

\[
\begin{array}{c|rrrrrr}
\text{distance}&0&1&2&3&4&5\\ \hline
\text{profiles}&1&65&3&31&4&10.
\end{array}                                                \tag{1}


Two words lie in one Hamming `2`-face only when their distance is at most
two.  For distance one, use the leader edge and the first canonical
transverse colour change; for distance two, the leaders are opposite corners of the unique
coordinate face.  Thus a literal one-square construction is available in
68 profiles.  The 45 profiles at distances three through five cannot be
handled by one face: they require transport along several faces or a
higher discrete derivative.  The distance-zero profile is the separate
proportional-word branch.

## Exact Hessian atom on the 68 faces

For each pair chart, fix the exclusive-site colour supplied by its leader
and let `Q` be the resulting cofactor coefficient function on common-five
words.  On a face with corners `00,10,01,11`, form

\[
       \nabla_1\nabla_2 Q=Q_{00}-Q_{10}-Q_{01}+Q_{11}.    \tag{2}


Both cofactor Hessians are nonzero in all 68 profiles.  More strongly, the
chosen leader monomials survive with coefficient

\[
(+1,-1)\quad\text{in all 65 adjacent-word faces},\qquad
(+1,+1)\quad\text{in the three opposite-corner faces}.   \tag{3}


Their Laurent product is nonzero.  The normalized direct blocks satisfy

\[
[E_{10},E_{11}]=-E_{10}\ne0,                              \tag{4}


so the formal Hessian commutator is a nonzero Laurent multiple of the
curved rank-one direct-block atom, exactly as proposed.

For every adjacent pair the checker exhausts all eight choices of
transverse common site and alternate colour.  Forty-five profiles have all
eight choices clean, three have seven clean choices, and 17 have none.
Thus target-side cancellation is clean on 51 profiles: 48 adjacent and all
three opposite-corner profiles have only mixed residual words in both
charts.  The remaining 17 adjacent profiles unavoidably contain their pure
leader corner, so their alternating target tensor does not vanish and they
require subtraction of that diagonal anchor before using (4).

## Verdict

The discrete-Hessian mechanism is real but not yet uniform:

* 51 profiles have a clean mixed-target nonzero square-curvature atom;
* 17 have the same nonzero source Hessians with one diagonal target
  contamination;
* 45 have no common `2`-face containing both leaders; and
* one has proportional common words.

This checker does **not** assert that two arbitrary response Hessians must
commute.  That is the exact missing Bianchi/connection implication needed
to turn the nonzero atom (4) into a contradiction.  A valid next theorem
must prove this coupling on a clean face, then transport it along a
shortest path for distances three through five and subtract the diagonal
corner in the contaminated branch.

## Reproduction

```text
python computations/verify_oo_c8_common_word_square_curvature.py
python -O computations/verify_oo_c8_common_word_square_curvature.py
```

The checker reconstructs all 114 regressions, exact cofactor polynomials,
leader faces, alternating Hessians, Laurent products, target-word types,
and the direct-block commutator.
