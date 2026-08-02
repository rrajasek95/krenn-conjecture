# The five polars reduce to an augmented Jacobian--Hessian membership

Research reduction only.  This note defines the smallest second-jet/Rees
complex which can promote the five exact polars.  Its criterion is necessary
and sufficient inside any specified source correction module, but the
criterion fails for the presently available connection/normal/curvature and
split-cap rows.  No new full-source correction is constructed, so Krenn's
conjecture remains open.

## 1. Outcome

The five identities from commit `7723671` are genuine Hessian symbols:

\[
 {\partial^2H_{c_v}\over
  \partial a_{xv}^{00}\partial a_{pq}^{00}}=h_v,
 \qquad v=1,\ldots,5.                                    \tag{1}
\]

They are not yet source cells.  The exact promotion question is an
augmented Jacobian membership problem.  If \(J\) is the literal source
Jacobian, \(H\) its mixed Hessian, and target and ordinary residue are
included as two additional constraint rows, a source-valid invisible mixed
second jet exists precisely when

\[
             -\widehat H(\xi,\eta)\in\operatorname{im}\widehat J,
 \qquad
 \widehat J=\begin{pmatrix}J\\J_{\rm tgt}\\J_{\rm ores}\end{pmatrix}.
                                                               \tag{2}
\]

This is an if-and-only-if, not a heuristic curvature condition.  It follows
by expanding a Hasse--Schmidt jet over
\(S[\epsilon,\delta]/(\epsilon^2,\delta^2)\).

For the five fixed polar symbols, (2) packages into one finite-free Rees
complex.  Its obstruction map is

\[
 S^5\longrightarrow\operatorname{coker}\widehat J,
 \qquad e_v\longmapsto[(h_vY_0,0,0)].                    \tag{3}
\]

The symbol \(e_v\) is promoted exactly when its class in (3) is zero.
Different choices have indeterminacy \(\ker\widehat J\), so any later
landing functional is single-valued exactly when it annihilates that
kernel.

The existing rows pass the boundary-only and target-augmented parts of this
test but fail after ordinary-residue invisibility is imposed.  In the exact
selected cap quotient, each face has augmented matrix

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
coordinate \(\rho_v\).  After the adjugate curvature contraction, the
required invisible column is

\[
                         p_v=(\kappa Y,0,0)^{\mathsf T}.   \tag{5}
\]

Deleting the third row makes (5) a column combination; retaining it raises
the rank from two to three.  For five independent faces the exact rank jump
is

\[
                              10\longrightarrow15.         \tag{6}
\]

Thus the Hasse--Schmidt formulation does not automatically solve the old
gap.  It proves that the old gap is exactly the missing augmented Hessian
membership: one new target- and ordinary-residue-invisible column \(n_v\)
per face, with boundary \(\kappa Yw_v\), is necessary and sufficient in
this smallest complex.

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

## 3. The smallest five-symbol Rees complex

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

This proves the necessary-and-sufficient module criterion (3).  It is also
minimal: adjoining a formal generator whose augmented boundary is
\(P(s_v)\) makes \((-n_v,s_v)\) a cycle, and any cycle with symbol \(s_v\)
supplies exactly such a correction.

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

Thus a filtered comparison can see (13): the same global row has its polar
in different chart sectors.  But the strict chart difference is still zero.
Complex (14) asks exactly whether that sector symbol has a source-valid
mixed correction; it does not declare the answer from the sector placement.

## 5. Existing rows fail exactly at ordinary-residue invisibility

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

which is (4).  The wanted invisible correction has (5).  If only the
boundary row is retained, or if boundary and target are retained, then

\[
                         p_v=\kappa Y\,\widehat J_v(\rho_v).
                                                               \tag{20}
\]

This is the tempting unaugmented Hessian lift.  It fails the ordinary
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
missing augmented membership, not merely a sufficient repair.

The five \(h_v\) have disjoint fine supports, so the five copies of (19)
form a block diagonal matrix of rank ten.  Adjoining the five columns (5)
raises its rank to fifteen, proving (6).  The smallest Rees extension needs
five independent columns; connection, normal, curvature, direct-double, and
the common anchor supply none of them.

This is the same mathematical gap previously described as an invisible
cross-word lift or a specialization-created Tor transgression.  The new
content here is the exact second-jet criterion: the polar construction can
succeed by this route if and only if the five classes (3) vanish in the
augmented Jacobian cokernel, followed by the independent zero-indeterminacy
condition (16).

## 6. Exact verification and scope

The dependency-free checker
[verify_h3_augmented_second_jet_polar_membership.py](../computations/verify_h3_augmented_second_jet_polar_membership.py)

- reconstructs all five eight-site mixed rows and their two-edge polars;
- checks that each polar lies wholly in the \(pq\)-direct and
  \(pr\)-two-star sectors;
- verifies the adjugate identities (18) on exact active rational packets,
  including the direct-free case \(B=0\);
- checks boundary-only, target-augmented, and fully augmented membership;
- obtains the one-face rank jump \(2\to3\) and five-face jump
  \(10\to15\); and
- verifies that a hypothetical invisible column gives exactly the cycle
  (23).

It passes normal, optimized, isolated, and no-site-library execution with
digest

    b9c1d442dac415ebde2fca5d97922fbda7060657c0bcd1d907c584a466fa136e

The finite rank test is a quotient of the full source problem.  It proves
that the named existing rows do not satisfy (2); it does not rule out a new
all-label cross-word chain, a non-flat specialization kernel, or a larger
source resolution whose new column realizes (22).  Finding precisely such
a column remains the positive construction.
