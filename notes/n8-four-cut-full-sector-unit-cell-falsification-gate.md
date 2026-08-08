# An anchored N=8 one-cell falsification gate for four five-cuts

## Outcome

There is now a smallest executable test of the still-viable multi-cut route.
It is deliberately a **falsification gate**, not a proof of a four-cut
theorem.

Start with the twelve-source integral family in
[`three-adjacent-five-cut-complete-quotient-countermodel.md`](three-adjacent-five-cut-complete-quotient-countermodel.md),
add its two-source repair

\[
              A_{23}\mathrel{+}=E_{21},\qquad
              A_{67}\mathrel{+}=-E_{12},
\]

and then add the two diagonal cells

\[
              A_{23}\mathrel{+}=E_{00},\qquad
              A_{67}\mathrel{+}=E_{00}.                    \tag{1}
\]

The resulting sixteen-source endpoint-decorated family has all three pure
coefficients equal to one.  Its full tensor has exactly eight nonzero mixed
coefficients, so it is not a Krenn counterexample.  On the adjacent five-cuts
labelled by \(z=2,3,4\), however, it satisfies the complete high-sector
quotient identity and has nonzero target defect.  The other three cuts
\(z=0,1,5\) fail the complete identity.

The checker changes each of the \(28\cdot9=252\) endpoint-colour aggregate
coordinates by \(+1\) and \(-1\), including already occupied coordinates.
For every one of these 504 exact integral mutations it reconstructs the full
matching tensor and every cut space over \(\mathbb Q\).  Of the mutations,

\[
 \begin{array}{c|r}
 \text{condition}&\text{count}\\ \hline
 \text{all three pure coefficients remain one}&478\\
 \text{also retain the active complete cuts }2,3,4&34\\
 \text{also acquire an active complete cut in }\{0,1,5\}&0.
 \end{array}                                                \tag{2}
\]

Thus no signed-unit one-cell repair of this anchored source turns the known
three-cut guard into a four-cut guard.

## Exact test and dependency graph

For \(z\in\{0,\ldots,5\}\), put

\[
 U_z=\{0,\ldots,5\}\setminus\{z\},\qquad C_z=\{z,6,7\}.
\]

The checker follows only literal source constructions:

\[
\begin{array}{c}
\text{endpoint-ordered aggregate cells}\\
\downarrow\ \text{all 105 perfect matchings}\\
H_B=T_{1,z}+T_{3,z}\\
\downarrow\ \text{four-site cofactors}\\
{\cal S}_{U_z}=\sum_{u\in U_z}V_u\otimes H_{U_z\setminus\{u\}}\\
\downarrow\ \text{exact sparse row reduction over }\mathbb Q\\
T_{1,z}\in V_{C_z}\otimes{\cal S}_{U_z},\qquad
T_{3,z}-\Delta_{8,3}\in V_{C_z}\otimes{\cal S}_{U_z}\\
\downarrow\\
\dim\bigl({\cal G}_{U_z}+{\cal S}_{U_z}\bigr)
       -\dim{\cal S}_{U_z}>0.
\end{array}                                                 \tag{3}
\]

An odd \(3\mid5\) cut has only the one- and three-crossing sectors, so (3)
checks its complete sector packet.  The first membership is the atomwise
one-crossing factorization.  The second is, by annihilator duality, the
complete high-sector quotient identity.  The final strict inequality says
that the quotient detects at least one constant target colour.  A **four-cut
falsifier** is an exact mutation for which all three tests hold on the fixed
cuts \(2,3,4\) and on at least one of \(0,1,5\), while all pure anchors remain
one.

This retains the lower source sectors and their common aggregate factors; it
does not factor through the top output tensor or its Zariski closure.  It is
therefore a legitimate finite-versus-border test despite the all-even border
theorem.

## Verdict and stopping rule

The test returns **no falsifier**.  This is modest positive evidence that a
fourth source-faithful cut adds real rigidity near the smallest known
three-cut guard.  It is much stronger than checking a formal tensor or an
output-only invariant, because every candidate is an actual finite decorated
source and both crossing sectors are rebuilt from it.

Its scope is intentionally narrow:

* coefficients outside the base family are tested only as one integral unit
  increment;
* two-cell, arbitrary-weight, and dense repairs are not excluded;
* the eight surviving mixed coefficients are not imposed to vanish; and
* no statement is made at orders above eight.

The next admissible computation is an arbitrary-weight one-cell elimination
or a symmetry-reduced two-cell search which retains all three pure anchors.
Stop this local repair lane if a four-cut source appears.  If increasingly
dense repairs remain empty but do not expose a bounded source identity, stop
enumerating: the uniform route needs a theorem coupling four cut cylinders,
not a larger finite census.

## Reproduction

```sh
python3 computations/verify_n8_four_cut_unit_cell_falsification_gate.py
python3 -O computations/verify_n8_four_cut_unit_cell_falsification_gate.py
python3 -I computations/verify_n8_four_cut_unit_cell_falsification_gate.py
python3 -S computations/verify_n8_four_cut_unit_cell_falsification_gate.py
```

The checker uses only the Python standard library and the literal source
utilities from the existing three-cut verifier.  It uses raising checks, so
optimized mode does not weaken the audit.
