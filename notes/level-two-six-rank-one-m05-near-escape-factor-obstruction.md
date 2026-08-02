# The first repaired \(6R\) factor escape dies on edge \(14\)

Research evidence only. Krenn's conjecture remains open,
**SP-CLEAN-BRIDGE** is untouched, and no certified dependency changes.

## Outcome

Start from the repaired common-isotropic packet \(M^\dagger\) and make one
further cross-block change,

\[
                              M_{05}=E_{01}.                    \tag{1}
\]

This new packet retains differential rank \(55/53\), the two separate
literal factorizations of the pure targets, and two internal residual-R2
witnesses with nonzero cofactors at every root.  Unlike \(M^\dagger\), its
original four-edge weakened factor ideal on

\[
                              01,04,05,45                       \tag{2}
\]

is not the unit ideal: its reduced Gröbner basis has \(394\) elements over
both \(\mathbb Q\) and \(\mathbb F_{32003}\).

This is the first local escape from the four-edge obstruction.  It does not
extend to a shared factored completion.  Adding the single unchanged edge
\(14\) gives a five-edge weakened system whose Gröbner basis is exactly
\((1)\) over both fields.  Thus edge \(14\) restores the contradiction.

## Why this is a sharp near escape

The changes \(04,05,15\) lie outside both four-site complements used by the
localized pure tangent cells \(01(0,0)\) and \(45(1,1)\).  The two factored
pure faces therefore remain exact.  Rational and three-prime row reduction
gives ranks \(55/53\), so the failure is not a differential-rank drop.

All six witness pairs remain:

\[
\begin{array}{c|cc}
\text{root}&\text{output }0&\text{output }1\\ \hline
0&03&02\\
1&12&13\\
2&23&20\\
3&32&31\\
4&45&40\\
5&54&51.
\end{array}                                                     \tag{3}
\]

The four retained vertices already form a connected nonbipartite graph, so
their four independent weakened edge scalars are equivalent to four
vertex-sum gauge scalars in characteristic zero.  The non-unit four-edge
ideal is therefore a genuine local compatibility locus, not merely an
artifact of weakening.  The fifth edge proves that this local solution
cannot satisfy the residual packet globally.

The checker
[verify_level_two_six_rank_one_m05_near_escape_factor_obstruction.py](../computations/verify_level_two_six_rank_one_m05_near_escape_factor_obstruction.py)
rechecks the exact gauge kernel, ranks, literal factored faces, and all R2
cofactors, then requires the four-edge payload \(394\) and the five-edge
unit payload over both fields.  Python dependencies are standard library
only; Singular is the sole external executable.  More general coupled
changes of \(M_{05}\), \(M_{14}\), or the surrounding core remain open.
