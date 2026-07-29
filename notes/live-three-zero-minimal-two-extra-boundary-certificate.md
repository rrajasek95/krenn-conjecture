# All eight two-extra boundary cells are uniformly injective

## 1. Outcome

For the first two-extra rescue configuration

\[
 (M_{e_2},M_{e_0})=(\{2\},\{0\}),\qquad (r,t)=(2,0),
\]

the complete response has rank \(20\) everywhere on each ordered
noncentral cell

\[
                   CB,\ BC,\ CE,\ EC,\ BB,\ BE,\ EB,\ EE.
\]

The factors are ordered: the first row plane belongs to \(e_2\), with
three retained star rows, and the second belongs to \(e_0\), with two.
Every selected maximal minor avoids source pair \(01\), so the result
allows an arbitrary direct \(B_{01}\) scale.

## 2. Exact certificates

The deterministic exact-support counts are

\[
\begin{array}{c|rrrrrrrr}
\text{cell}&CB&BC&CE&EC&BB&BE&EB&EE\\ \hline
\text{rational base supports}&23&19&7&7&10&3&3&1\\
\text{additional modular selectors}&0&4&1&1&2&0&0&0.
\end{array}                                                     \tag{1}
\]

The additional selectors all lie over \(\mathbf F_{17}\).  Their
finite-field coordinates choose response-row labels only.  Every
corresponding determinant is reconstructed over \(\mathbb Q\), specialized
to the exact Plücker cell, and replaced by its squarefree support.  For
each positive-dimensional cell, the resulting rational support ideal is
\((1)\); on \(EE\), the selected determinant is a nonzero constant.

The \(B\)-chart has \(p_{12}=1\) by construction, and \(E\) is its unique
projective endpoint.  Thus these are exact affine-cell computations and
need no omitted boundary localization.

## 3. Exact audit

[verify_live_three_zero_minimal_two_extra_boundary_cells.py](../computations/verify_live_three_zero_minimal_two_extra_boundary_cells.py)
reconstructs and verifies the eight ordered unit-minor certificates in one
clean default replay.  Discovery data and the disjoint \(C/B/E\)
specializations are in
[explore_live_three_zero_minimal_two_extra_boundary.py](../computations/explore_live_three_zero_minimal_two_extra_boundary.py).

Together with the uniform central certificate in
[live-three-zero-minimal-two-extra-response-frontier.md](live-three-zero-minimal-two-extra-response-frontier.md),
this closes all nine row-plane cells for the minimal two-extra response.
