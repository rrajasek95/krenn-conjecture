# Independent audit of the selected adjugate and multi-label Koszul no-go

This audit independently reconstructs the exact claims in commits `e5fecea`
and `1aca3f5`.  It does not import either primary checker.  The conclusion is
that both reductions are correct at their stated bounded-row scope, with one
terminological caution: the proved positive statement is a localized
**row-span contraction** of the selected two-channel star summand, not a chain
contraction of the full tilted source complex.

## 1. Adjugate contraction

Starting from the definitions of (f_i,g_{ik},\phi,\psi_k,H_i,N_{ik}), direct
sparse-polynomial expansion reproduces all four identities

\[
 f_it_k-g_{ik}y=D_{ik}z,
 \quad \psi_ky-\phi t_k=E_{ik}z,
\]

\[
 S_kf_i-Qg_{ik}=\Gamma_{ik}z+C_{ik},
 \quad t_kH_i-yN_{ik}=D_{ik}v-C_{ik}.
\]

It also reconstructs both normal differences as
(-(h-1)D_{ik}) and (+(h-1)E_{ik}).  Summing with the literal coefficients
of every (J=I+E_{uv}), including the three doubled-diagonal cases, gives the
claimed (D(J),E(J),\Gamma(J),C(J)).  Independently, the diagonal target
vector is ((1,1,1)) off diagonal and has a single (2) in position (u=v),
which is exactly (\Delta+\mathbf1_{u=v}X_u).

For the selected square, exact multiplication gives

\[
 \begin{pmatrix}U&-F\\-B&A\end{pmatrix}\binom y t=\binom E D,
 \qquad
 \begin{pmatrix}A&F\\B&U\end{pmatrix}\binom E D
     =(AU-BF)\binom y t.
\]

Setting the entire (R=A_{pr}) block to zero gives (D=At),
(E=Uy-Ft), and (\kappa=AU), so both recovery formulas remain polynomial
and do not divide by the vanished entry.  This verifies the asserted
power-free selected contraction.  It does not add the missing comparison
between the absolute diagonal target row and the target-zero normal carrier.

## 2. Exact gap tags and graph shear

The six/seven-row failure ledgers were already independently enumerated in
the selected-cap audit.  Taking that exact ledger as input, this checker
independently audits its new interpretation.  The distinguished residual site
is physical site zero, so deleting its first letter gives

\[
 \{12112,12212\}\quad\text{and}\quad\{02012,22012\}.
\]

None is (Y_0=00000).  Relative to the common selected word `012012`, the
direct-free changes occur only at (r=3), and the tilted changes only at
(r=1), confirming the claimed mixed (r)-word classification.  The three
remaining gaps are the pure target-bearing rows.

For (g_i=(X_i,Y_i)), the shear ((T,R)\mapsto(T,R-\phi(T))) sends all three
graphs to ((X_i,0)).  The compound target-projection matrices in exterior
degrees (1,2,3) consequently have ranks (3,3,1).  Thus no target-zero
class occurs in an exterior power of the graph itself.

## 3. Exterior and Koszul no-go

The audit builds a quotient countermodel containing all three sheared graph
anchors, two adjacent-power representatives with arbitrary target vectors and
independent mixed responses, every exact mixed gap row with its rational
coefficient, and the crossed zero-response row.  The anchors span the whole
target space.  Exact nullspace elimination gives response rank (2) on the
target kernel, while adjoining (Y_0) raises the rank to (3), for both the
direct-free and tilted ledgers.

Enumerating every contraction of a two-fold wedge by a coordinate target
covector and every contraction of a three-fold wedge by two coordinate target
covectors again gives response rank (2); adjoining (Y_0) again gives rank
(3).  This is not merely a sampled conclusion: every such response is a
linear combination of the response parts of its factors, hence remains in
the same two-dimensional mixed-word module.

Finally, independently generated fixed-total-degree Koszul matrices have

\[
\begin{array}{c|c|c}
m&\dim(K_0,K_1,\ldots)&\operatorname{rank}(\partial_1,\partial_2,\ldots)\\
\hline
2&(6,9,3)&(6,3)\\
3&(10,18,9,1)&(10,8,1).
\end{array}
\]

Every consecutive composite is zero and the adjacent ranks sum to the middle
dimension, so positive exterior homology vanishes in both degrees.

Therefore the asserted no-go follows from the modeled rows: ordinary target
linear combinations, wedges, determinants, and the undecorated degree-two or
degree-three target Koszul complex cannot produce
((0,-\kappa Y_0)).  The countermodel does **not** rule out a physical
cross-word differential, a decorated Massey operation, a larger relative
Rees complex, or the sought generator (n_0); both primary notes state these
nonclaims correctly.

The dependency-free checker is
[`audit_selected_adjugate_multilabel_koszul_no_go_independent.py`](../computations/audit_selected_adjugate_multilabel_koszul_no_go_independent.py).
