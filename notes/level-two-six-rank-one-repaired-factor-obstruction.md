# The repaired \(6R\) boundary has no shared factored completion

Research evidence only. Krenn's conjecture remains open,
**SP-CLEAN-BRIDGE** is untouched, and no certified dependency changes.

## Outcome

The repaired common-isotropic-pencil packet \(M^\dagger\) reaches
differential rank \(55/53\), selected residual R2 at all six active
rank-one roots, and separate literal factorizations of both pure targets.
Nevertheless it has no one endpoint-star assignment realizing all four
binary \(L_0\) slices.

Thus the exact \(6R\) boundary remains a sharp separation:

\[
 \text{generic kernel + selected rows + R2 + each factored pure face}
 \quad\not\Longrightarrow\quad
 \text{shared four-slice compatibility}.                       \tag{1}
\]

The statement applies to the fixed repaired residual packet, not to the
full \(6R\) stratum.

## Exact weakened factor system

The repaired differential has rank \(55\), and its five universal vertex
gauges are independent.  Hence its kernel is exactly the gauge kernel.
Euler's identity absorbs the direct endpoint coefficient into those gauge
scalars, just as for the original sharp packet.

Retain vertices \(0,1,4,5\) and the four edges

\[
                              01,04,05,45.
\]

Their repaired blocks are

\[
\begin{aligned}
M_{01}&=\begin{pmatrix}2&3\\4&6\end{pmatrix},&
M_{04}&=\begin{pmatrix}0&0\\1&0\end{pmatrix},\\
M_{05}&=\begin{pmatrix}6&7\\13&9\end{pmatrix},&
M_{45}&=\begin{pmatrix}1&0\\0&0\end{pmatrix}.
\end{aligned}                                                   \tag{2}
\]

For the four endpoint-colour slices, weaken every vertex-sum gauge
coefficient to an independent scalar on each retained edge.  The resulting
system has 32 star coordinates, 16 edge scalars, and 64 quadratic
equations.  It contains every possible shared factored completion, but
exact degree-reverse-lexicographic elimination gives

\[
                         \operatorname{std}(I)=(1)              \tag{3}
\]

over both \(\mathbb Q\) and \(\mathbb F_{32003}\).  Therefore even the
weakened system is empty, proving the claimed obstruction.

This is a fresh computation: the original packet's certificate could not
simply be reused after changing \(M_{04}\).  The repaired four-edge ideal
nevertheless remains the unit ideal.

The checker
[verify_level_two_six_rank_one_repaired_factor_obstruction.py](../computations/verify_level_two_six_rank_one_repaired_factor_obstruction.py)
rechecks rank and the exact gauge kernel, pins the two localized pure
tangent columns, generates all equations in memory, and requires the unit
Gröbner basis in both characteristics.  Python dependencies are standard
library only; Singular is the sole external executable.  The conjecture
and the general rank-\(55\) incidence locus remain open.
