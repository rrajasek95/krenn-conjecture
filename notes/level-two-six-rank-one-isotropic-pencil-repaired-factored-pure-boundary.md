# A two-block repair reaches the rank-\(55\) factored boundary through \(6R\)

Research evidence only. Krenn's conjecture remains open,
**SP-CLEAN-BRIDGE** is untouched, and no certified dependency changes.

## Outcome

Modify the sharp residual packet \(M^\sharp\) only on the two blocks
\(04\) and \(15\), replacing each by \(E_{10}\).  Call the resulting packet
\(M^\dagger\).  It retains

\[
 \operatorname{rank}d\Psi_{M^\dagger}=55,\qquad
 \operatorname{rank}(d\Psi_{M^\dagger})_{\rm mixed}=53,       \tag{1}
\]

and the two separate literal endpoint-star assignments still realize

\[
                         (e_{0^6},0,0,0),\qquad
                         (0,0,0,e_{1^6}).                      \tag{2}
\]

Unlike the original packet, \(M^\dagger\) has two internal residual-R2
witnesses with nonzero cofactors at **all six** roots.  Therefore, for any
subset \(A\subseteq\{0,\ldots,5\}\), put

\[
 X_i=h_i e_0^{\mathsf T}\quad(i\in A),\qquad X_i=0\quad(i\notin A),
 \qquad \nu_i=0.                                               \tag{3}
\]

Every choice satisfies generic-kernel, selected, and residual-R2
conditions.  Consequently one exact common-isotropic-pencil family reaches
the rank-\(55/53\) separate-factored-pure boundary in every endpoint pattern

\[
                         kR+(6-k)Z,\qquad 0\le k\le6.          \tag{4}
\]

The two assignments in (2) are separate.  The old simultaneous unit-ideal
certificate does not apply verbatim to \(M^\dagger\), because one of its four
core blocks has changed.  A fresh computation in the
[repaired factor obstruction](level-two-six-rank-one-repaired-factor-obstruction.md)
shows that the modified four-edge ideal is nevertheless still the unit
ideal, so this repaired packet has no shared four-slice completion.

## Why the two-block repair preserves the pure faces

The pure-zero assignment has one tangent cell \(01(0,0)\); its derivative
uses only the complementary residual sites \(2,3,4,5\).  The pure-one
assignment has one tangent cell \(45(1,1)\); its derivative uses only sites
\(0,1,2,3\).  Neither complement contains the repaired edges \(04\) or
\(15\).  Hence both factored derivatives remain literally unchanged.

Exact rational and three-prime row reduction gives the five incidence
signatures

\[
 \operatorname{rank}D=\operatorname{rank}[D\mid e_{0^6}]
 =\operatorname{rank}[D\mid e_{1^6}]
 =\operatorname{rank}[D\mid e_{0^6}\mid e_{1^6}]=55,
 \qquad \operatorname{rank}D_{\rm mixed}=53.                  \tag{5}
\]

Thus the repair neither loses maximal residual rank nor merely makes the
pure targets incident: the original localized factorizations survive.

## Six-root R2 table

The physical internal witness edges are

\[
\begin{array}{c|cc}
\text{root}&\text{output }0&\text{output }1\\ \hline
0&03&02\\
1&12&13\\
2&23&20\\
3&32&31\\
4&45&40\\
5&54&51.
\end{array}                                                     \tag{6}
\]

The last two pure-one witnesses are exactly the transposes of the repaired
\(E_{10}\) blocks.  Every displayed edge has a nonzero complementary
four-site cofactor.  An active site in (3) therefore uses the
two-internal-witness alternative, while an inactive site preserves the
residual binary pair.

Because \(e_0^{\mathsf T}Je_0=0\), all pairwise selected numerators vanish.
The checker also evaluates the rare/rare endpoint slice literally for all
\(64\) active subsets and obtains zero every time.

The standard-library checker
[verify_level_two_six_rank_one_isotropic_pencil_repaired_factored_pure_boundary.py](../computations/verify_level_two_six_rank_one_isotropic_pencil_repaired_factored_pure_boundary.py)
exhausts the subset census \(1,6,15,20,15,6,1\), audits all selected and R2
conditions, directly sums the endpoint slices, and verifies (1) and (5)
over the rationals and three prime fields.  It passes normal, optimized,
and isolated Python.
