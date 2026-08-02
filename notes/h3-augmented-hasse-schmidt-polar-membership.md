# The five-polar membership criterion is not yet composed with the split cap

Research reduction and correction.  This note proves the general
Hasse--Schmidt membership criterion and reconstructs the five exact polar
symbols.  Separately, it audits the already known split-cap obstruction
\((\kappa Yw_v,0,0)\).  It does **not** construct the comparison which would
carry the polar class \((h_vY_0,0,0)\) into that split-cap module.  No new
full-source correction is constructed, so Krenn's conjecture remains open.

## 1. Outcome

The five identities from commit `7723671` are genuine Hessian symbols:

\[
 {\partial^2H_{c_v}\over
  \partial a_{xv}^{00}\partial a_{pq}^{00}}=h_v,
 \qquad v=1,\ldots,5.                                    \tag{1}
\]

They are not yet source cells.  If \(J\) is a specified literal source
Jacobian, \(H\) its mixed Hessian, and target and ordinary residue are
included as two additional constraint rows, a source-valid invisible mixed
second jet with already constructed first jets exists precisely when

\[
             -\widehat H(\xi,\eta)\in\operatorname{im}\widehat J,
 \qquad
 \widehat J=\begin{pmatrix}J\\J_{\rm tgt}\\J_{\rm ores}\end{pmatrix}.
                                                               \tag{2}
\]

This is an if-and-only-if, not a heuristic curvature condition.  It follows
by expanding a Hasse--Schmidt jet over
\(S[\epsilon,\delta]/(\epsilon^2,\delta^2)\).

For the five fixed polar symbols, the formal obstruction map is

\[
 S^5\longrightarrow\operatorname{coker}\widehat J,
 \qquad e_v\longmapsto[(h_vY_0,0,0)].                    \tag{3}
\]

once the first-jet representatives and the literal augmented Jacobian have
been supplied.  The symbol \(e_v\) is promoted exactly when its class in
(3) is zero.  Different choices have indeterminacy \(\ker\widehat J\), so
any later landing functional is single-valued exactly when it annihilates
that kernel.

There is a separate, already audited split-cap calculation.  In its selected
three-coordinate quotient, each formally labelled face has matrix

\[
 \widehat J_v=
 \begin{pmatrix}
    -Y&1\\
     1&0\\
     0&1
 \end{pmatrix},                                           \tag{4}
\]

whose rows are selected cap boundary, physical target, and ordinary
residue, and whose columns are the target coordinate \(T_v\) and response
coordinate \(\rho_v\).  The independently derived split-cap class is

\[
                         p_v=(\kappa Y,0,0)^{\mathsf T}.   \tag{5}
\]

Deleting the third row makes (5) a column combination; retaining it raises
the rank from two to three.  For five formal block-diagonal copies the rank
jump is

\[
                              10\longrightarrow15.         \tag{6}
\]

Equations (3) and (5) are not the same class.  The first contains the
universal nonunit quadratic \(h_v\); the second has coefficient \(\kappa Y\),
a unit on the stated active open.  The checker reconstructs (1) and audits
(4)--(6) independently, but it constructs no first jets and no source-valid
map

\[
 (h_vY_0,0,0)\longmapsto(\kappa Yw_v,0,0).              \tag{6a}
\]

Therefore the ranks (6) prove no failure or necessity statement for the
five polar classes.  They only restate the split-cap obstruction.  The
precise remaining theorem is to construct invisible tangent lifts
\(\xi_v,\eta_v\) and a source-provenant comparison morphism of augmented
complexes whose mixed Hessian is \(h_vY_0\), whose image in the cap quotient
is \(\kappa Yw_v\), and which intertwines target and ordinary-residue rows.

## 2. The augmented mixed-jet theorem

Let \(k\) have characteristic zero, let

\[
 R=k[x_1,\ldots,x_N],\qquad
 S_0=R/(F_1,\ldots,F_M),                                  \tag{7}
\]

and allow localization or further quotient of \(S_0\).  In the application
this is the active full-nine source ring, localized at \(\kappa Y\).  Add whatever polynomial
target and ordinary-residue constraints the chosen literal complex is
required to preserve, and denote the complete constraint map by

\[
                    \widehat F=(F,F_{\rm tgt},F_{\rm ores}). \tag{8}
\]

The last two components may instead be module-valued linear readouts; the
same calculation applies, with zero Hessian in those linear components.
Fix an \(S_0\)-algebra \(S\) on which all components of (8) vanish.  Write
\(\widehat J\) for the Jacobian of (8), reduced to \(S\), and define

\[
 \widehat H(\xi,\eta)_\alpha
   =\sum_{i,j}{\partial^2\widehat F_\alpha
                    \over\partial x_i\partial x_j}\xi_i\eta_j. \tag{9}
\]

There is no factor of two in (9); it is the coefficient of the mixed
monomial \(\epsilon\delta\).

**Theorem (augmented Hasse--Schmidt criterion).**  Put

\[
 D=S[\epsilon,\delta]/(\epsilon^2,\delta^2).
\]

The coordinate assignment

\[
 x_i\longmapsto x_i+\epsilon\xi_i+\delta\eta_i
                         +\epsilon\delta\zeta_i           \tag{10}
\]

defines a mixed second jet through the augmented constraint locus if and
only if

\[
 \widehat J\xi=0,\qquad
 \widehat J\eta=0,\qquad
 \widehat J\zeta+\widehat H(\xi,\eta)=0.                 \tag{11}
\]

Consequently, for fixed invisible first jets \(\xi,\eta\), a mixed
correction \(\zeta\) exists if and only if (2) holds.

**Proof.**  Substitute (10) into each component of (8).  Modulo
\((\epsilon^2,\delta^2)\), its Taylor expansion is

\[
 \widehat F(x)+\epsilon\widehat J\xi
 +\delta\widehat J\eta
 +\epsilon\delta\bigl(\widehat J\zeta
                   +\widehat H(\xi,\eta)\bigr).           \tag{12}
\]

The constant term vanishes in \(S\).  The three remaining coefficients
vanish exactly under (11).  Since (10) is an algebra homomorphism on the
polynomial ring, vanishing on the chosen generators is sufficient for it to
factor through their quotient.  This proves both directions. \(\square\)

If only a specified literal correction module \(L\) is admitted, with
source-coordinate map \(a:L\to S^N\), replace \(\widehat J\) in (2) by
\(\widehat Ja\).  This is the source-provenance restriction: allowing all
formal vectors in \(S^N\) and allowing only connection/normal/curvature rows
are different membership problems.

There are two logically separate requirements here.  A principal-parts
symbol such as (1) first has to be represented by invisible tangent lifts
\(\xi,\eta\); then its augmented second fundamental form must vanish by
(2).  If the tangent lifts have already been supplied by a chart
comparison, (2) is the complete remaining condition.  The bare equality
(1) supplies neither tangent lifts nor the membership.

## 3. The formal five-symbol membership complex

The preceding nonlinear jet condition has a smallest linear complex once
the five symbols are fixed.  Let \(L\) be the chosen literal mixed-correction
module and let

\[
 E_{\rm aug}=E_{\rm bdry}\oplus E_{\rm tgt}\oplus E_{\rm ores}.
\]

Let \(\Sigma=S\langle s_1,\ldots,s_5\rangle\) record the five prescribed
principal symbols, and set

\[
 P(s_v)=(h_vY_0,0,0).                                    \tag{13}
\]

Define

\[
 \boxed{
 C^{1}_{\rm Rees}=L\oplus\Sigma
 \mathop{\longrightarrow}^{d_2}E_{\rm aug},\qquad
 d_2(\ell,s)=\widehat J a(\ell)+P(s).}                   \tag{14}
\]

Here \(\Sigma\) is a symbol ledger, not five declared physical cells.  A
cycle \((\ell,s_v)\) is precisely a physical promotion of the \(v\)-th
symbol.  Therefore

\[
 \boxed{
 s_v\text{ promotes in }L
 \iff P(s_v)\in\operatorname{im}(\widehat Ja).}           \tag{15}
\]

This proves the necessary-and-sufficient module criterion (3) **after**
\(L\), \(a\), the tangent lifts, and their common augmented target have
been specified.  It is formally minimal: adjoining a generator whose
augmented boundary is \(P(s_v)\) makes \((-n_v,s_v)\) a cycle, and any
cycle with symbol \(s_v\) supplies exactly such a correction.  The checker
below does not instantiate these data for the five polars.

Two lifts differ by \(\ker(\widehat Ja)\).  Hence, for any proposed
associated-grade landing \(q:L\to Q\), the promoted value is independent of
the lift if and only if

\[
                         q(\ker(\widehat Ja))=0.           \tag{16}
\]

Equations (15) and (16) cleanly separate existence from zero indeterminacy.

## 4. Substitution of the five exact polars

Use the direct-free eight-site notation

\[
 x=0,\quad D=(1,2,3,4,5),\quad p=6,\quad q=7,
 \quad A_{pr}=0,
\]

and the odd word \(12112\).  For \(v\in D\), let \(c_v\) be mixed on
\(D\setminus\{v\}\) and zero elsewhere.  A matching in \(H_{c_v}\)
contains both \(xv\) and \(pq\) exactly when its other two edges form a
perfect matching of \(D\setminus\{v\}\).  Removing the two marked edges
gives the three terms of \(h_v\), proving (1) term by term.

The chart placement is equally exact:

\[
\begin{array}{c|c|c|c}
v&c_v&D\setminus\{v\}\text{ word}&
       (pq\text{ sector},pr\text{ sector})\\ \hline
1&00211200&2112&(\mathrm{direct},\mathrm{two\!\!-star})\\
2&01011200&1112&(\mathrm{direct},\mathrm{two\!\!-star})\\
3&01201200&1212&(\mathrm{direct},\mathrm{two\!\!-star})\\
4&01210200&1212&(\mathrm{direct},\mathrm{two\!\!-star})\\
5&01211000&1211&(\mathrm{direct},\mathrm{two\!\!-star}).
\end{array}                                                \tag{17}
\]

Thus the sector placement suggests the input (13), but it does not provide
the invisible first jets or a map into \(E_{\rm aug}\).  The strict chart
difference is still zero.  Complex (14) asks whether a **specified**
source-valid comparison realizes that symbol; the displayed polar identity
does not construct the comparison.

## 5. Independent split-cap obstruction at ordinary-residue invisibility

After the selected connection/normal/curvature contraction, put

\[
 D=\begin{pmatrix}A&B\\F&U\end{pmatrix},\qquad
 \kappa=AU-BF,\qquad Y=\overline Y_c,
\]

and work where \(\kappa Y\) is a unit.  The adjugate identities

\[
 (-F,A)\binom AF=(U,-B)\binom BU=0,
 \qquad
 (-F,A)\binom BU=(U,-B)\binom AF=\kappa               \tag{18}
\]

show that the connection/normal middle terms close and leave the curvature
carrier.  Including the direct curvature correction produces the actual
cap-graph response already found by the filtered \(d_2\) calculation.

For one face, use the basis \((w_v,\operatorname{tgt},
\operatorname{ores})\).  The two existing split-cap columns are

\[
 \widehat J_v(T_v)=(-Y,1,0)^{\mathsf T},\qquad
 \widehat J_v(\rho_v)=(1,0,1)^{\mathsf T},               \tag{19}
\]

which is (4).  The split-cap invisible correction would have (5).  If only the
boundary row is retained, or if boundary and target are retained, then

\[
                         p_v=\kappa Y\,\widehat J_v(\rho_v).
                                                               \tag{20}
\]

This is the tempting unaugmented split-cap lift.  It fails the ordinary
residue row because \(\rho_v\) has residue one.  Indeed, if

\[
 a\widehat J_v(T_v)+b\widehat J_v(\rho_v)=p_v,
\]

target invisibility forces \(a=0\), ordinary-residue invisibility forces
\(b=0\), and then the boundary coordinate cannot be \(\kappa Y\).  This is
the rank jump \(2\to3\).

The actual overlap mode is the cap graph

\[
                         g_v=T_v+Y\rho_v,
 \qquad \widehat J_v(g_v)=(0,1,Y).                        \tag{21}
\]

The connection/normal/curvature packet gives \(-\kappa g_v\), and the
common diagonal anchor gives \(+\kappa g_v\).  They cancel both target and
residue and add no new column to (19).  Keeping only the target-zero response
\(-\kappa Y\rho_v\) gives the desired response but has boundary
\(-\kappa Yw_v\), so it is not a cycle.

Adjoining one new chain \(n_v\) with

\[
 d n_v=\kappa Yw_v,\qquad
 \operatorname{tgt}(n_v)=\operatorname{ores}(n_v)=0       \tag{22}
\]

makes

\[
                         n_v-\kappa Y\rho_v               \tag{23}
\]

a target-zero cycle with response \(-\kappa Y\).  Conversely, any such
cycle yields (22) after adding \(\kappa Y\rho_v\).  Thus (22) is exactly the
missing nullhomotopy in this split-cap quotient.  It has not been derived
from a polar \(h_vY_0\).

Five formally labelled copies of (19) form a block diagonal matrix of rank
ten.  Adjoining five copies of the split-cap column (5) raises its rank to
fifteen, proving (6).  This says only that the block-diagonal split-cap
module has five independent missing directions.  It does not identify those
directions with the five disjoint fine supports of \(h_v\), and it proves no
lower bound for a full source module which may couple the faces.

The valid conclusion is a pair of uncomposed tests.  The polar construction
can succeed by the Hasse--Schmidt route if and only if the five classes (3)
vanish in the **actual** augmented Jacobian cokernel, followed by (16).
Independently, the selected split-cap quotient lacks (5).  To connect them
one must prove the comparison theorem stated after (6a); neither the
adjugate scalar identities nor the rank jump supplies it.

## 6. Exact verification and scope

The dependency-free checker
[verify_h3_augmented_second_jet_polar_membership.py](../computations/verify_h3_augmented_second_jet_polar_membership.py)

- reconstructs all five eight-site mixed rows and their two-edge polars;
- checks that each polar lies wholly in the \(pq\)-direct and
  \(pr\)-two-star sectors;
- verifies the adjugate identities (18) on exact active rational packets,
  including the direct-free case \(B=0\);
- checks boundary-only, target-augmented, and fully augmented membership
  for the **separate split-cap class** \((\kappa Yw_v,0,0)\);
- obtains the split-cap one-block rank jump \(2\to3\) and formal
  five-block jump \(10\to15\);
- verifies that a hypothetical split-cap invisible column gives (23); and
- records explicitly that no first jets or comparison map from
  \(h_vY_0\) to \(\kappa Yw_v\) have been constructed.

It passes normal, optimized, isolated, and no-site-library execution with
digest

    3defe8bcced1f144e0a7cbe247961ee2497b13dc2a270d2868b979765472be36

The finite rank test is only the selected split-cap quotient.  It does not
evaluate (2) on the polar class, prove that named full-source rows fail the
polar membership, or show that five new physical generators are necessary.
The remaining positive construction is stronger than merely finding (22):
it must supply the tangent lifts and the chain-level comparison (6a), prove
that the augmented Jacobian square commutes, and then establish the
zero-indeterminacy condition (16).
