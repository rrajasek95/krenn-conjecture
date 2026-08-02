# Multi-label target Koszul operations do not cross the residual-word gap

Research obstruction only.  The unified overlap theorem,
`SP-CLEAN-BRIDGE`, and Krenn's conjecture remain open.

## 1. Outcome

The first obstruction in
[`h3-target-augmented-filtered-d2-first-obstruction.md`](h3-target-augmented-filtered-d2-first-obstruction.md)
cannot be repaired merely by retaining all three physical targets and taking
ordinary wedges, determinants, or the degree-two/three target Koszul complex.

Let

\[
 \mathcal T=\langle X_0,X_1,X_2\rangle,
 \qquad \phi(X_i)=Y_i,                                   \tag{1}
\]

where \(Y_i\) is the pure odd residue of the same-label cap.  The three
same-power cap graphs and diagonal anchors are

\[
                         g_i=(X_i,Y_i).                    \tag{2}
\]

The graph shear

\[
             S_\phi(T,R)=(T,R-\phi(T))                    \tag{3}
\]

sends every \(g_i\) to \((X_i,0)\).  Therefore target cancellation by any
number of same-power anchors cancels their residues at the same time.  For
every \(k=1,2,3\), target projection restricts to an isomorphism

\[
 \Lambda^k\operatorname {graph}(\phi)
                    \mathop{\longrightarrow}^{\sim}\Lambda^k\mathcal T.
                                                                    \tag{4}
\]

There is no target-zero exterior class hidden among the three cap graphs.

The exact full-word failure loci of the selected direct-free and tilted
packets make the remaining obstruction sharper.  Besides the three missing
pure anchors, every missing coefficient has distinguished \(x\)-label zero.
After exposing \(x\), their odd word tags are

\[
 \begin{array}{c|c|c}
 \text{packet}&\text{mixed odd tags}&\text{desired tag }Y_0\\ \hline
 \text{direct-free}&12112,\ 12212&00000\\
 \text{tilted}&02012,\ 22012&00000.
 \end{array}                                               \tag{5}
\]

Thus even adjoining every one of those exact missing rows supplies a
two-dimensional mixed-word boundary space which does not contain \(Y_0\).
The \(h=3\) adjacent-power target representatives add two defect classes
\(A_N,B_N\), but the retained selected rows impose no cross-word relation
placing \(Y_0\) in their span.  Assigning those two defects to the two exact
mixed directions gives a rational countermodel to every such selected-row
derivation.

In this model all two- and three-fold wedge contractions, after target
cancellation by (3), remain in the same mixed-word span.  The ordinary target
Koszul complexes are exact in positive exterior degree.  Hence neither the
two-anchor wedge nor the triple determinant/Massey-shaped Koszul cell produces
the requested class

\[
                         (0,-\kappa Y_0).                  \tag{6}
\]

This is a sharp selected-row no-go, not a no-go for a new decorated higher
operation.  The next genuinely missing datum is a source-level cross-word,
cross-quotient comparison which changes one of the mixed tags in (5) into the
pure tag `00000`, with target component zero and the prescribed curvature
coefficient.  Equivalently, one needs a typed generator \(n_0\) with

\[
                         d_0n_0=\kappa Y_0w,               \tag{7}
\]

whose associated-grade readout retains \(-\kappa Y_0\).  Target Koszul
bookkeeping alone cannot supply (7).

## 2. The exact missing cross-word rows

The independent audit of the
[five-exposed selected-cap packet](h3-five-exposed-two-chart-selected-cap-landing-counterguard.md)
enumerates all \(3^8=6561\) coefficients of its `pq` EqSystem.  The
direct-free packet fails exactly six coefficients:

\[
\begin{array}{c|c|c|c|c}
\text{residual word}&(i,j)&\text{value}&\text{target}&
  \text{odd tag after deleting }x\\ \hline
000000&(0,0)&0&1&00000\\
111111&(1,1)&0&1&11111\\
222222&(2,2)&0&1&22222\\
012112&(2,2)&1&0&12112\\
012212&(2,1)&1&0&12212\\
012212&(2,2)&1&0&12212.
\end{array}                                                \tag{8}
\]

The tilted packet fails exactly seven:

\[
\begin{array}{c|c|c|c|c}
\text{residual word}&(i,j)&\text{value}&\text{target}&
  \text{odd tag after deleting }x\\ \hline
000000&(0,0)&0&1&00000\\
111111&(1,1)&0&1&11111\\
222222&(2,2)&0&1&22222\\
002012&(2,2)&1/2&0&02012\\
022012&(0,2)&-3/2&0&22012\\
022012&(2,0)&1/2&0&22012\\
022012&(2,2)&-1/4&0&22012.
\end{array}                                                \tag{9}
\]

The first three rows of either table are exactly the three pure target
anchors.  If they are adjoined as same-power cap rows, their low
target/residue images are the graph generators (2), and the shear (3) makes
them pure target.  The remaining rows are target-zero but carry mixed source
words.  Deleting the distinguished first residual letter gives precisely the
two tags in (5).  In particular, none is the pure odd word \(Y_0=00000\).

The existing crossed four-index selected row is stronger in a different
direction: its low target and ordinary-residue coordinates are both zero.  It
therefore contributes a source tag but no vector to the target/residue module.
It cannot identify either mixed word in (5) with \(Y_0\) without an additional
source differential.

## 3. Adjacent-power target representatives

On the rank-\((1,1)\) scalar gate, the proved adjacent-power normal form uses

\[
 \begin{aligned}
 A_N&=s^{h-1}\bigl(r_0y^{[h-1]}-T_0\bigr),\\
 B_N&=s^{h-1}\bigl(sy^{[h]}-T_N\bigr),
 \end{aligned}                                             \tag{10}
\]

with

\[
 T_0=\sum_i(K_0)_{ii}X_i,
 \qquad T_N=\sum_iN_{ii}X_i.                              \tag{11}
\]

At \(h=3\), write \(a,b\) for the low defects of these two source classes.
Their target-augmented selected-row representatives have the general form

\[
 u_0=\bigl(s^2T_0,s^2\phi(T_0)+a\bigr),
 \qquad
 u_N=\bigl(s^2T_N,s^2\phi(T_N)+b\bigr).                  \tag{12}
\]

Applying (3) gives

\[
                         S_\phi(u_0)=(s^2T_0,a),
 \qquad S_\phi(u_N)=(s^2T_N,b).                          \tag{13}
\]

Thus the adjacent-power formulas retain their physical target provenance but
do not themselves identify \(a\) or \(b\) with a pure odd residue.  In any
linear combination of (2) and (12), the target equations uniquely remove the
graph pieces.  The remaining response is a linear combination of \(a,b\):

\[
 \ker(\operatorname {tgt})\longrightarrow\mathcal R_{\rm odd},
 \qquad \operatorname {image}\subseteq\langle a,b\rangle. \tag{14}
\]

For both exact packets, take \(a,b\) to be the two independent mixed word
directions in (5).  This assignment satisfies every retained target equation,
uses the exact nonzero missing-row coefficients, and gives

\[
              Y_0\notin\langle a,b\rangle.                \tag{15}
\]

Consequently the selected rows and target representatives do not imply (7).
This is a module countermodel to derivability, not a physical exact ternary
source and not a claim that the actual \(A_N,B_N\) must have those values.

## 4. Exterior and Koszul audit

After the shear, every anchor lies in \(\mathcal T\), while every response part
of an adjacent or missing-row generator lies in the mixed module

\[
 \mathcal M_{\rm df}=\langle12112,12212\rangle,
 \qquad
 \mathcal M_{\rm tilt}=\langle02012,22012\rangle.           \tag{16}
\]

Contract a wedge of two generators by one target covector, or a wedge of
three generators by two target covectors.  Its target-cancelled response is a
linear combination of the response parts of its factors.  It therefore lies
in \(\mathcal M\).  The checker enumerates every such contraction and verifies

\[
 \operatorname {rank}(\text{all exterior responses})=2,
 \qquad
 \operatorname {rank}(\text{responses},Y_0)=3             \tag{17}
\]

for both packets.  In particular,
\(S_\phi(g_0)\wedge S_\phi(g_1)\) has nonzero target wedge
\(X_0\wedge X_1\), and the three-anchor determinant has coefficient one on
\(X_0\wedge X_1\wedge X_2\).  Neither is target-zero.

The ordinary Koszul complex of the regular target sequence
\((X_0,X_1,X_2)\), in fixed total degree \(m\), is

\[
 K_p(m)=\Lambda^p\mathcal T\otimes\operatorname {Sym}^{m-p}\mathcal T,
 \quad
 \partial(e_{i_1}\wedge\cdots\wedge e_{i_p}\otimes f)
 =\sum_a(-1)^{a-1}e_{I\setminus i_a}\otimes X_{i_a}f.     \tag{18}
\]

The exact rational ranks are

\[
\begin{array}{c|c|c}
m&\dim(K_0,K_1,\ldots)&\operatorname {rank}(\partial_1,\partial_2,\ldots)\\
\hline
2&(6,9,3)&(6,3)\\
3&(10,18,9,1)&(10,8,1).
\end{array}                                                \tag{19}
\]

Hence all positive exterior homology vanishes in the two degrees relevant to
a wedge or triple determinant.  The ordinary target Koszul DGA has no
surviving positive class from which a nonzero triple Massey/Koszul value could
be read.  This statement does not exclude a decorated Massey operation in a
larger source complex; such a decoration would be exactly additional data
beyond (18).

## 5. The next missing cross-word datum

For the direct-free packet, a candidate source relation would have to produce
a typed comparison of the shape

\[
 \alpha[12112]+\beta[12212]
                 \longmapsto -\kappa[00000].              \tag{20}
\]

For the tilted packet the left side is instead a combination of
`02012` and `22012`.  No map in the selected target-Koszul complex
changes a residual-word tag, and the exact missing EqSystem rows merely say
that the mixed coefficients must vanish in a true source.  They do not provide
the map (20).

What is needed is a coefficient-exposure/reinsertion or cross-quotient chain
homotopy between different residual words (equivalently, between the relevant
odd quotients) whose target component is the identity or zero as appropriate,
but whose residue commutator is the right side of (20).  This is precisely the
new source datum required to realize (7).  After it is constructed, the
common-mode zero-indeterminacy and rootless Macaulay readout remain separate
problems.

The no-go therefore sits at the interface of Components III and IV of the
[unified full-nine target](unified-full-nine-two-chart-overlap-jet-saturation-target.md):
the target exterior algebra does not couple the rootless and inactive
readouts; a literal cross-word comparison must do so.

## 6. Exact scope

The proved statements are limited to the bounded target/word-tag module.

* All three target axes, cap graphs, and pure diagonal anchors are retained.
* The two-anchor wedge, triple determinant, complete degree-two/three target
  Koszul complexes, existing crossed target-zero row, adjacent target
  representatives, and every exact missing row in (8)--(9) are included.
* The direct-free and tilted curvature values are retained:
  \(\kappa=-1/4\) and \(\kappa=-5/2\), respectively.
* No full all-label source complex, cross-word differential, physical
  \(n_0\), or nonexistence theorem for arbitrary decorated higher operations
  is claimed.

The dependency-free checker
[`verify_h3_multilabel_target_koszul_crossword_no_go.py`](../computations/verify_h3_multilabel_target_koszul_crossword_no_go.py)
checks the exact six- and seven-row failure loci, their odd tags, graph shear,
target-kernel response ranks, every two-/three-fold exterior contraction, the
Koszul ranks and compositions, the two adjacent-power target representatives,
and the strict rank jump excluding \(-\kappa Y_0\).
