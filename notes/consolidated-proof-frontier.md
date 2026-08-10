# Consolidated proof frontier

Audit date: 2026-08-02.

This is the compact task-allocation map.  The conjecture is still open.
The longer [supersession audit](proof-route-supersession-audit.md) records
why older routes are closed, guarded, or demoted; it should not be read as a
list of independent remaining obligations.

Certification maintenance on 2026-08-01 leaves the mathematical frontier
unchanged.  The six-site terminal theorem `SP-K6` retains exactly its prior
statement, with its repaired proof and checker suite accepted at commit
`4a510193d97fd84cc819912231504711281dbbab` by
`SUPERSESSION-2026-08-01-03`.  The `LOCAL-INVERTIBLE` proof statement is also
unchanged; `SUPERSESSION-2026-08-01-04` records only an optimized-mode-live
checker hash at commit `6e622d9a9572524246d7714ef7ddcb6c4742d7bf`.  Those entries procedurally
replace the incomplete records `SUPERSESSION-2026-08-01-01` and
`SUPERSESSION-2026-08-01-02`, which lacked permanent audit reports, exact
scope coverage, and this required spine update.  Neither maintenance record
touches the dashed clean-point implication below.

Strategic allocation update on 2026-08-01: the sole primary target is now the
[unified tilted/one-sided full-nine two-chart overlap--jet saturation theorem](unified-full-nine-two-chart-overlap-jet-saturation-target.md).
Its four open components are tilted/direct-free source overlap,
complete-anchor incidence or maximal-shore conversion, source-provenant
residual Macaulay annihilation, and inactive-boundary/mixed-ledger
exactness.  The shore and level-two packets below remain local structure or
falsification tests for those components, not parallel top-level proof
programs.  At \(N=8\), the [eight-vertex calibration](clean-bridge-at-eight-is-the-open-case.md)
shows that **SP-CLEAN-BRIDGE** is equivalent to emptiness; the unified target
is therefore an organized statement of the full obstruction, not a weaker
shortcut.

## 1. One missing conjecture-level implication

After selecting three palette colours, write the endpoint-ordered aggregate
matching equation as

\[
                         H_B(A)=\Delta_{B,3}.
\tag{1}
\]

**Model.**  The blocks \(A_{uv}\) are endpoint-ordered with cells
\(A_{uv}(i,j)\), \(i\) read at \(u\) and \(j\) at \(v\), and cells with
\(i\ne j\) are **allowed**: (1) is the **GENERAL (bicoloured) model** over
\(\mathbb C\), which is the model of the open case \(N=8,d=3\) (DeepMind's
Lean `eqSystem8_no_solution_d3`, research open).  The
MONOCHROMATIC-EDGE restriction — \(A_{uv}\) diagonal — is a strict
special case in which \(N=8,d=3\) and \(N=10,d=3\) are already closed by
[`proofs/diagonal-hafnian-recurrence-obstruction.md`](../proofs/diagonal-hafnian-recurrence-obstruction.md);
diagonal results are consumed here only as necessary conditions on the
diagonal shadow.  See
[`references/REFERENCES.md`](../references/REFERENCES.md).

For every even \(|B|\geq8\), the proved spine is

\[
\begin{aligned}
(1)
&\Longrightarrow
 \text{a maximum-anchor, then minimum-support representative}\\
&\Longrightarrow
 \text{a nonzero physical minor and a generically active cap line}\\
&\dashrightarrow
 \text{an active zero of the clean error }{\cal E}_{p,q}\\
&\Longrightarrow
 H_{B\setminus\{p,q\}}(A')=\Delta_{B\setminus\{p,q\},3}\\
&\Longrightarrow
 \text{the proved six-site contradiction after repeated descent and re-minimization}.
\end{aligned}
\tag{2}
\]

The first two arrows are the
[unconditional curvature-line theorem](unconditional-curvature-line-selection.md)
with the independently audited
[anchor--curvature synchronization theorem](anchor-lexicographic-curvature-synchronization.md).
The fourth arrow is the
[exact clean-pair descent](clean-pair-cap-exact-descent-target.md), and the
last arrow uses the
[arbitrary-complex six-site obstruction](../proofs/six-site-arbitrary-complex-obstruction.md).
After each descent one makes the same lexicographic choice at the new order
before applying curvature selection again; equivalently, the conditional
resolution may be phrased as a minimal-order contradiction.
The dashed arrow is the only missing conjecture-level implication on this
spine.  The order-two and order-four cases and all displayed lower
constructions are already complete; order six is the terminal ternary
obstruction.

In particular, the following are not additional top-level obligations:
global flat-fan classification, E1/E2 selection, pairification of every
higher cumulant, or another six-site support census.  They are proved inputs,
superseded targets, or independent ways to attack the dashed arrow.

## 2. Exact split of the dashed arrow

On a selected physical line, failure to find an active clean point has two
exhaustive forms.

1. **Rootless:** the scalar coordinates of \({\cal E}\) have gcd one.  The
   residual Sylvester/Macaulay multiplication map is then surjective.  Its
   abstract rank--gcd algebra is complete; what is missing is a
   source-provenant annihilator built from the literal nine rows.
2. **Roots exist, but all are inactive:** the common divisor is supported on
   the activity divisor.  On an off-diagonal selected line, the independently
   audited
   [base-locus--ternary endpoint theorem](offdiagonal-base-locus-ternary-omega-residue.md)
   now makes coefficient routing exhaustive: at least one of the two
   inactive endpoints is clean, removing its factor leaves a degree-\(h-1\)
   residual with bounded certificate \((tu)^{h-1}\), and two clean endpoints
   sharpen both values to \(h-2\).  Every surviving colour has the universal
   normalized odd residue \(-\overline Y_c\).  The independently audited
   [minimum-order survival lemma](odd-residue-minimality-survival.md) forces
   at least one \(\overline Y_c\ne0\), and the off-diagonal endpoint detects
   every label.  The independently audited
   [same-power lock and adjacent-power ledger](offdiagonal-same-power-target-residue-lock.md)
   now show that no literal quadratic companion on the same complement can
   cancel the diagonal target while retaining this residue: target and
   ordinary odd residue are locked coefficientwise.  The literal
   connection, normal, curvature, and direct-double rows instead give one
   exact adjacent-power source syzygy.  Thus the remaining off-diagonal
   task is specifically to turn that syzygy and the scalar-zero cap
   extension into a well-defined secondary comparison (of Bockstein/Yoneda
   type) before passing to the odd quotient, and then use it to force a
   clean-point contradiction.  No such chain operation is currently
   constructed.  On a diagonal selected line, the independently audited
   [three-boundary routing theorem](diagonal-three-boundary-inactive-routing.md)
   gives the exact activity divisor, exhausts the scalar boundary factors,
   and provides both a symmetric bounded certificate and a sharper
   chartwise two-boundary certificate after third-factor coordinate-gcd
   saturation.  The independently audited
   [diagonal Rees and cap-jet theorem](diagonal-rees-saturation-cap-jet-bockstein.md)
   gives both normalized generic jets division-free literal cap
   representatives, so their source normalization and label transport are
   complete.  It also proves the exact lifting criterion: third-factor
   scalar division is source-valid if and only if every discarded
   transverse principal part lies in the literal boundary submodule, not
   merely in the evaluation kernel.  What remains is to prove these
   relative-saturation memberships and an adjacent-power target
   null-homotopy.  The independently audited
   [adaptive diagonal theorem](adaptive-diagonal-uncollision-cap-routing.md)
   now shows that the trace collision of the canonical \(I-E_{aa}\)
   direction is avoidable at the one-chart coefficient level whenever the
   full direct block is not \(\alpha E_{aa}\).  A literal adaptive direction
   has activity divisor \(tu^2(t+\gamma u)\), two division-free jets with
   determinant \(h\gamma\), and visibility of every label.  Ordinary matrix
   singularities add no activity boundary.  This does not transport an
   arbitrary adaptive direction through the source-faithful two-chart
   overlap.  For the intrinsic block \(A_{pq}=\alpha E_{aa}\), the ordinary
   boundary rows and same-power odd residue still miss the selected colour,
   whose target first appears at transverse order \(h\).  The independently
   audited [full normal-jet theorem](scalar-unit-full-normal-jet-unary-anchor-ledger.md)
   now retains all nine rows and identifies the information which survives
   before that collapse.  With
   \(G_a=\alpha q+R_{aa}\), unary error \(U_a\), and arbitrary normal response
   \(R_D\), it gives
   \[
     {\cal E}(xE_{aa}+D)
       =x^hU_a+x^{h-1}R_D\Theta_a
         +\sum_{m=2}^h x^{h-m}R_D^{[m]}G_a^{[h-m]}.
   \]
   At an intrinsic scalar-unit good pair of the synchronized representative,
   \((U_a,\Theta_a)\ne(0,0)\); hence a clean unary cap forces
   \(\Theta_a\ne0\).  Moreover
   \(\Theta_a=R_{aa}H_a\) and
   \(R_{ij}\Theta_a=R_{ia}R_{aj}H_a\), so the collision moves the first
   surviving comparison into literal two-step off-diagonal squares.  On the
   subbranch where an admissible source-provenant top selector detects that
   packet, the
   [selector localization theorem](scalar-unit-catalecticant-four-cut-localization.md)
   gives a nonzero literal oriented curvature against an adjacent
   \(q^{[h-2]}\)-cofactor.  The
   [physical target-jet theorem](scalar-unit-physical-target-jet-constraints.md)
   factors every jet through one common four-site \(H_a\)-carrier.  The
   latter carrier can nevertheless have rank two; an exact eight-of-nine-row
   guard fails only the complementary diagonal row.  With all nine rows, a
   leakage-free coordinate-monomial packet is excluded except on an exact
   target-cancellation boundary.  What remains is therefore to use that restored
   row together with the common carrier to exclude cancellation/leakage, or
   to construct a source-faithful
   adjacent-power/four-cut operation which transports the localized class
   from \(q^{[h-2]}\) to \(H_a\) with zero lift indeterminacy.  Root avoidance
   alone does not make a Taylor coefficient vanish.  On the target-plane
   unary/binary branch, the audited
   [zero-coordinate charge](scalar-unit-binary-residual-target-branch.md)
   forces missing-colour near-perfect matchings and the sharp bounds
   \(|\operatorname{supp}q|\ge3h-2\) or \(3h-1\).  In the binary equality
   branch, a uniform clean Hamilton switch shows that the latter bound is
   not a contradiction.  The exact replacement target for that
   top-preserving binary route is an anchor-preserving nine-row
   Hamiltonization, not minimization of the top fibre alone.  A top-changing
   replacement satisfying the general nine-row difference system remains a
   distinct possible descent mechanism.

These are different local ledgers.  A single two-chart theorem may close
both, but that unification remains to be proved.

The label split is also real.  A selected line has the form
\(K_z=E_{ab}+zI\), without a proof that \(a\ne b\).  Off-diagonal inactive
coefficient routing and nonzero-residue detection are now complete.  One-chart
diagonal coefficient routing and visibility are also complete
away from the intrinsic coordinate-unit block, rather than merely away
from the canonical trace-collision equation.  The off-diagonal
scalar-zero/rootless packet still requires \(a\ne b\).  A uniform clean-point
bridge must transport the intrinsic block's nonzero normal comparison,
carry an adaptive direction through the two-chart source filtration, or
prove a curvature-compatible relocation; in every case the coefficient
residue and any scalar-gcd saturation still have to be lifted through the
physical source filtration.

## 3. Rootless selector frontier

In the off-diagonal rootless packet, the two endpoint Rado matroids either
have disjoint bases or they do not.

The independently audited
[automatic two-chart extraction theorem](two-chart-joint-hypothesis-extraction.md)
proves that every rootless selected chart already has an ordinary three-site
selector at both endpoints, including when its selected cell is diagonal.
The split below concerns compatibility between those selectors, not their
individual existence.

* **Disjoint bases:** ordinary Hall data are insufficient.  The
  [weighted K6 provenance guard](k6-lefschetz-source-provenance-guard.md)
  proves that even separated selectors, a maximal-rank matching-Lefschetz
  map, and one complete diagonal row do not force an own-edge tangent.  The
  live candidate needs two differently labelled anchors and the crossed
  four-index row transported through a source-faithful overlap, or an
  equivalent direct construction of the residual Macaulay annihilator.
* **No disjoint bases:** the
  [uniform maximal-shore theorem](uniform-selector-union-maximal-defect-shore.md)
  gives the following exhaustive local boundary list on the complete
  residual ground set.

| Boundary | What is proved | Exact residue |
|---|---|---|
| [Common coloop](common-coloop-clean-cap-affine-fibre.md), \(b=1\) | The scalar-extended and cross-row reductions restore full row provenance and prove \(Q\ne0\Rightarrow a_{rt}a_{ts}=0\). The [extremal residue audit](common-coloop-extremal-coupled-residue-boundary.md) then uses maximum anchors/minimum support to exclude \(Q=0\) on the selected good chart. It also corrects the rank boundary: local-rank-one with both cross coefficients zero is a dark sub-stratum, while either one-sided branch has a surjective scalar map | Close three source-provenant families: dark nonzero top of any local rank with \(\alpha A=\beta A=0\), and the two one-sided branches \(\widetilde\alpha A=-Q\), \(\Lambda(\widetilde\alpha D)=\mu\). The four remaining literal rows determine the corrected curvature rectangle (18); the missing datum is its common factorization \(\Gamma_{ij}=\rho\bar p_i\bar s_jq_0^{[h-2]}\) coupled to the same arms' \(D_{\bar K}(z)\)-images |
| [Line plus plane](line-plus-plane-shore-clean-cap-pencil.md), \(b=2\) | A whole projective clean pencil; its generic member is active | A kernel line missing one fixed diagonal label, or a rank-one endpoint confined to one fixed row, together with the endpoint-transposed versions |
| [Rank \((1,1)\)](rank-one-rank-one-shore-clean-quotient-plane.md), maximal \(b=3\) endpoint-dark refinement | A four-dimensional clean double-annihilator plane; its generic member is active | A fixed coordinate row/column, or \(a=\lambda x^{\mathsf T}+y\mu^{\mathsf T}\); without a coordinate gate, the scalar gate is already impossible for \(b\leq2\), while overlaps of the gates remain unclassified |

The maximal scalar gate has since narrowed further.  Its source-provenance
quotient is dual to the one- or two-dimensional target-free cap space.  The
released-site equations force a literal local coordinate plane.  If the
diagonal map has rank three and that plane occurs on the three-site response
support, the
[fixed-plane provenance closure](n8-rank11-scalar-fixed-plane-provenance-closure.md)
proves \(\ker\delta\subseteq\ker\Phi\) in both diagonal ranks, so the
quotient itself vanishes.  The remaining rank-\((1,1)\) scalar case is the
fixed dark-shore plane; a complement-plane assignment-sum row is no longer
an open subcase.
| [Endpoint-dark shore](endpoint-dark-shore-consecutive-power-jet.md) | Every fully dark contraction factors the fixed target through one literal consecutive-power cofactor map | The fixed-plane [one-site guard](n8-rank11-scalar-fixed-dark-plane-one-site-guard.md) realizes the aligned alternative on two distinct complete one-site contractions and contains an exact projective three-space of canonically clean caps, every point inactive.  The [joint labelled carrier theorem](n8-rank11-scalar-fixed-dark-plane-joint-labelled-carrier.md) kills all three natural 24-cell completions by at most three rows; inclusion--exclusion compresses the unrestricted escape to one six-term residual-to-dark permanent plus 12 mixed carriers.  Routing this common ledger through entry minimality/the second chart must now force activity, leave the scalar plane, descend, or produce a source unit; clean existence alone is insufficient |

Additive N=8 scalar-shore update: the
[released-site splitting theorem](n8-rank11-scalar-released-site-three-target-closure.md)
shows that no site release can expose all three targets.  Since both
multiplier rows vanish at the released site, a three-colour diagonal
response would split into three individual pure targets, contradicting the
proved four-site bound.  The earlier claim that a singleton blocker for one
label makes all three released functionals nonzero was too strong.  The
exact residue is a two-site blocker-incidence packet (same-label multiple
or different-label singleton blockers) plus the already named
source-provenant dark-cut comparison.  On its two-live released boundary,
one physical complement site is forced onto the corresponding coordinate
plane.  If every release has at most one live label and no dark site is a
coordinate plane, the six possible blocker ledgers are rainbows; their
three releases put all three pure targets in one three-site multiplier and
are impossible.  Thus the scalar residue always reaches a literal local
coordinate plane.  Varying the full-support annihilator cap makes this
uniform: either one dark-site plane is fixed, or at one complement site and
one target coordinate the three endpoint cells are proportional to
\(\lambda\), and the opposite three to \(\mu\).  Turning that fixed-label
identity or the dark cut into the admitted two-chart comparison remains
open.  The complement-plane alternative has zero scalar provenance
quotient in both diagonal ranks.  On the fixed dark plane, however, a
rank-three rational guard retains a four-dimensional physical response
family, two distinct complete nine-row releases, one actual
consecutive-power quadratic, and a nonzero target-free response.  Thus even
two separate released-site comparisons are provably insufficient; the
missing input is their individually labelled joint five-site coefficient,
or the source-labelled overlap which supplies that comparison.  The joint
error in the guard is \(\lambda\mu^{\mathsf T}W\), so its cap-plane sum
vanishes identically; a further cap contraction cannot see the missing
class.  The individual labels do see it: all three natural exposed-site
fibres have ordinary units using at most three rows.  After all \(q\)-cells
are restored, every cut leaves twelve pure-zero matchings avoiding its
selected edge and a small mixed ledger.  Hence the live scalar
task is their source-minimal/two-chart routing, not another cap contraction
or separate release.

The three ledgers are not independent.  Their pure parts combine with the
top row to the six-term permanent of the \(3\times3\) residual-to-dark
pure-zero cross block.  The exact common identity is
\(2P_{B,A}+M_{45}+2M_{35}+2M_{34}=2\), with twelve displayed mixed
carriers.  This is the preferred interface to the overlapping chart: a
cross edge becomes an endpoint-star or direct coefficient after deletion.
On the rational guard, however, the full dark maps still satisfy
\(\operatorname {rank}E_A=\operatorname {rank}\beta_A=1\) and
\(\ker E_A=\ker\beta_A\).  The permanent identity is therefore explicit
parity-layer provenance, not the missing kernel/target separation.  The
overlap must use its curvature/clean-error data to break that equality.
More sharply, the direct functional vanishes on the four-dimensional cap
plane and all twenty polarized cubic products of its response basis vanish.
Thus the canonical clean error is identically zero on a projective
three-space, every point inactive.  A separate rank-two linear map is only
the contracted source-row residual and must not be identified with the
descent error.  This makes activity conversion, escape from the scalar
plane, or a source contradiction—not clean-cap construction—the exact
endpoint-dark obligation of the overlap theorem.

Thus the generic \(b=2\) and rank-\((1,1)\), \(b=3\) geometries are
finished.  The latest gate reductions identify the line--plus--plane
cofactor-kernel normal forms, the rank-\((1,1)\) coordinate
quadratic/cubic line and scalar adjacent-power comparison, and the
common-coloop curvature-factorization residue.  These are bounded tests of
Component II in the unified target.  They should not be developed as
independent branch enumerations, and the old unrestricted shore
classification should not be reopened.

## 4. The common mechanism exposed by the guards

The recent exact guards all fail at the same interface.

* A Hall permanent, separated selectors, six off-diagonal rows, or one
  diagonal anchor do not supply an own-edge lift.  This remains false even
  when the weighted K6 matching-Lefschetz map is invertible.  Its four-cycle
  obstruction transports to four complementary cuts and is the linearized
  curvature normal.  The audited
  [finite-polarization theorem](k6-finite-curvature-polarization-and-grade-transport.md)
  now proves that every nonzero finite \(AU-BF\) rectangle is the exact
  derivative of a rank-one correction, and that this determinant class is
  invariant under the reciprocal factor gauge.  The remaining obstruction
  is not finite-versus-linear algebra: a source-faithful overlap must produce
  that transverse correction while preserving the direct/star/internal
  grading.  Mapping \((AU-BF)z\) to the radial base direction is killed by
  the four-cycle functional.
* [Top apolar membership for the generic
  hafnian](shafiei-generic-hafnian-apolar-lift-obstruction.md) reduces to the
  original scalar tangent equation.  It loses the lower-degree lift and
  cross-word information.
* The independently audited
  [global Wick boundary](global-wick-top-invariant-counterguard.md) puts
  ternary GHZ in the ordinary and Zariski closure of the unrestricted top
  matching-tensor image at every even order at least six, even with
  nonsingular algebraic complex-symmetric global covariance.  Thus no
  output-only polynomial or target-regular rational identity, nor any fixed
  polynomial construction from flattenings, contractions, or matchgate
  data, can separate the target.  The independently audited
  [one-hot torus quotient counterguard](one-hot-torus-quotient-border-collapse.md)
  shows that retaining the sparse one-hot source but passing to the affine
  target-stabilizer quotient still loses the needed information.  For each
  fixed properly three-coloured support, its normalized chart is one orbit
  of the full port torus \(T_\Delta\); its all-unit source orbit is closed,
  while the finite non-GHZ output and GHZ have the same target-quotient
  point.  Hence an invariant pole order, source Hilbert--Mumford instability,
  or properness of this induced affine torus quotient alone cannot
  distinguish exact finite membership from the boundary.  A viable
  valuative argument must retain additional source-faithful data, for
  example a non-invariant normal weight or singular gauge/chart, or use a
  different group.  The independently audited
  [source cycle separator](one-hot-source-cycle-invariant-separator.md)
  shows that retaining the **full source quotient** does recover some of
  that lost information.  For every extra matching \(M\),

  \[
     I_M=H_{m(M)}\prod_{e\notin M}A_e^{c(e)c(e)}
  \]

  is a regular \(T_\Delta\)-invariant on the arbitrary endpoint-colour
  source, equal to one on the Laurent boundary orbit and zero on every exact
  GHZ source.  Thus the source quotient separates the known boundary, while
  Hilbert--Mumford polystability alone still does not: both the boundary
  source and any nonempty exact fibre admit closed orbits.  Since the
  separator vanishes on the exact fibre by its mixed-equation factor, it
  does not prove that fibre empty; it identifies the missing global input as
  a source-ideal relation, not another output invariant.
  The first exact full-source membership test for that relation is negative.
  On the eight-site expanded-prism boundary, the
  [balanced source-ideal calculation](n8-full-source-cycle-product-first-membership-obstruction.md)
  constructs a rational dual supported on 93 port matchings and proves

  \[
                   P_G\notin I_{\rm mix}
  \]

  in the full 252-variable arbitrary endpoint-colour ring.  The sparse dual
  is not a multiplicative edge/Pfaffian character, and its convolution
  square fails on an exponent-two mixed column.  Thus the cheapest
  exponent-one certificate and the automatic all-power extension are both
  closed; neither result decides (P_G^2), radical membership, or the full
  fibre.  On the 60-coordinate chart selected by that dual, the exact
  [localized sparsity calculation](n8-localized-dual-edge-sparse-no-go.md)
  goes further: after normalizing the twelve boundary variables, there is
  no mixed common zero using at most thirteen of the remaining 48
  coordinates in characteristic different from two.  Its four minimal
  twelve-coordinate supports and all 48 admissible one-coordinate
  extensions each contain a three-binomial \(1=-1\) certificate.  The
  continuation excludes every support through seventeen extras, but at
  eighteen it finds an exact
  [localized radical counterexample](n8-localized-radical-counterexample.md):
  a five-parameter Laurent torus on which all 6,558 mixed coefficients
  vanish and \(P_G=1\), with pure tuple \((0,0,1)\).  Hence
  \(P_G\notin\sqrt{I_{\rm mix}}\) even in the full 252-variable ring.  This
  kills the proposed boundary-product radical route without giving a GHZ
  source; the relevant strengthened question must use all three nonzero
  pure anchors.  On the entire normalized 60-edge chart, that strengthening
  now succeeds by an exact
  [pure-product certificate](n8-60-edge-pure-product-certificate.md): 73
  mixed rows with 282 integer multiplier terms satisfy

  \[
             \sum_i A_iH_{c_i}=2H_0H_1H_2.
  \]

  Hence the chart has no three-pure point at any sparsity.  At the Laurent
  torus, the mixed Jacobian has rank 196 and the pure map has tangent rank
  one; the two missing pure differentials already lie in the mixed
  conormal.  Exact conormal division explains their quadratic locks by
  sparse five- and nine-product identities, and the corrected colour-zero
  cubic is likewise a sum of 33 mixed conormals with quadratic multipliers.
  More importantly, the full second-order lift obstruction

  \[
    \operatorname {Sym}^2(T_p)\longrightarrow
    \operatorname {coker}J_{\rm mix}
  \]

  has rank 39, and the only surviving corrected colour-one cubic factors as
  a tangent coordinate times one of its quadratic obstruction components.
  Consequently both missing pure coefficients have at least quartic contact
  along every formal mixed-fibre arc through the torus.  The next
  colour-zero residual is nonzero on the unrestricted tangent space but
  restricts there to one four-factor rectangle.  Exact reduction against
  the rank-39 obstruction basis proves that rectangle is a single quadratic
  multiplier times one of the second-lift obstruction equations.  Hence
  \(H_0\) in fact has at least quintic contact on every genuine mixed-fibre
  arc.  The colour-one quartic obeys the corresponding source-relative
  identity: after retaining the free second-jet tangent part, its true
  36-term coefficient plus a tangent coordinate times one literal
  third-lift equation lies in the ideal of the 39 quadratic lift
  obstructions.  Thus \(H_1\) also has at least quintic contact on every
  genuine arc.  Full mixed-equation back-substitution strengthens both arc
  statements to literal local congruences

  \[
                  H_0,H_1\in I_{\rm mix}+\mathfrak m_p^5.
  \]

  A literal-provenance automatic local reducer then iterates the same two
  operations—division by the 196 conormals and reduction by the 39 lifted
  quadratic obstructions—and proves the stronger bounded congruences

  \[
        H_0\in I_{\rm mix}+\mathfrak m_p^7,
        \qquad H_1\in I_{\rm mix}+\mathfrak m_p^6.
  \]

  The largest completed ambient leading forms have 291,123 and 380,392
  terms, but their tangent normal forms have only 32 and 126 terms and
  reduce to zero exactly.  This is strong evidence for a compact
  tangent-quotient recursion; it is not yet an all-orders membership proof.

  The rank-39 quadratic obstruction ideal itself has a 48-element Gröbner
  basis.  Its radical is a 42-generator Ferrers edge ideal with exactly five
  linear minimal components of dimensions \(51,47,46,45,45\); only six
  radical generators require squaring modulo the obstruction ideal.  Thus
  the next fifth-order tests can be performed on five explicit linear
  branches, while retaining the nilpotent obstruction scheme for actual
  ideal membership.  The nine cubic generators in that Gröbner basis have
  compact two-term lifts to the literal mixed ideal.  An exact lifted
  Schreyer audit now covers every critical-pair class: all 201 nontrivial
  quadratic--quadratic overlaps, 107 quadratic--cubic overlaps, and 36
  cubic--cubic overlaps have zero first lifted remainder; the other 784
  pairs are covered by Buchberger's product criterion.  One genuinely
  coupled cubic pair also closes one order farther.  The remaining local
  gap is therefore a single all-orders issue: construct a maximal-ideal
  unit loop, or equivalently kill the positive-weight deformation class of
  the tangent standard basis.  First-tail closure alone does not prove that
  contraction.  In fact the cubic tail is a genuine embedded deformation:
  exact module reduction modulo coordinate and generator changes leaves the
  nonzero five-term class

  \[
    a\bigl(z_4(s-r)e_{16}+z_5(s-r)e_{22}-z_4t e_{19}\bigr).
  \]

  Thus formal rigidity of the whole nonreduced tangent scheme is false.
  Every coefficient of this class nevertheless lies in the Ferrers radical,
  and it restricts to zero on each of the five reduced linear branches.
  This makes branchwise radical analysis strictly more promising than full
  local ideal membership: the next local task is to lift those five smooth
  tangent branches and show that one of \(H_0,H_1\) vanishes on each.
  Exact rational Jacobian minors now give the expected generic ranks
  \(5,9,10,11,11\) on those five linear branches, so the scheme cut out by
  the 39 known tangent equations is generically smooth along every reduced
  component.  On the second branch the complete cubic deformation is a
  Jacobian coboundary, with a 369-column exact lift, and the same quadratic
  bend keeps \(H_1\) zero through degree four.  This supplies candidate
  Hensel pivots but deliberately does not claim that no higher
  strict-transform equation cuts a branch.

  There is also an exact 31-chart localization cover of the full ternary
  target.  At any three-pure point, one nonzero matching monomial can be
  selected in each pure coefficient.  Their product is a unit in one of
  exactly 31 \(S_8\times S_3\)-orbits, so chartwise saturated pure-product
  membership is sufficient.  Every chart has a mixed support one-factor;
  exactly two charts have the minimum of two.  The expanded-prism support
  used by the local and filtered calculations is one of these two hardest
  charts, rather than a generic easy case.  The other extremal chart has
  two \((4,4)\)-colour mixed factors with Hamilton-eight-cycle complements.
  On its natural 36-coordinate carrier, the pure product has the exact
  one-generator identity

  \[
    H_0H_1H_2=(1+x_3x_{12})(1+x_{16}x_{19})H_{11112222}.
  \]

  It rehomogenizes polynomially with four degree-eight multiplier monomials
  and no denominators.  Restoring all 252 coordinates creates no
  off-chart-degree-one tail; the first tail has 592 rows in degree two.  An
  exact 275-column rational correction, with denominator lcm four, removes
  the complete degree-two tail and proves

  \[
                 H_0H_1H_2\in I_{\rm mix}+K^3
  \]

  in the full 252-variable source.  A fixed degree-three continuation is
  inconsistent, but this is only an associated-graded obstruction.  Keeping
  the complete degree-two kernel gives a coupled 29,704-row solve.  Its
  1,430-dimensional Bockstein image kills the obstruction, and an exact
  1,634-orbit-column certificate (denominator lcm two), replayed on every
  labelled row, proves the stronger characteristic-zero statement

  \[
                 H_0H_1H_2\in I_{\rm mix}+K^4.
  \]

  A later attempted degree-four modular Schur transfer was withdrawn on
  2026-08-02: its quotient reduction stopped at the first free coordinate,
  leaving later `A4` pivots inside lower-kernel tails and inflating the
  reported transfer rank.  A corrected common echelon gives additional
  transfer rank 6006 modulo 1009, not 17224.  More importantly, the corrected
  calculation collapses to an exact characteristic-zero
  [four-row dual](n8-chart25-degree4-exact-four-row-dual.md), with integral
  values ((-2,-1,-1,+1)).  Only nine source-column orbits meet its support;
  exact replay gives pairing zero on all nine and hence on all 59488 older
  and 913608 degree-four columns, including every one of the 31584 lower
  kernel tails.  Splitting the functional as the exact lifted cochain
  \((-\mu,\lambda)\) gives the source-provenant Schur target pairing one.
  The older displayed value three paired the lower raw target with an already
  reduced degree-four coordinate and counted the certificate tail twice.
  Therefore

  \[
                 H_0H_1H_2\notin I_{\rm mix}+K^5.
  \]

  After a common eight-variable factor is removed from the four functional
  rows, three residual monomials are decorated alternating-(C_4) terms and
  the fourth is their parallel-pair degeneration.  This is the same local
  circuit geometry exposed by the chart-26 base-exchange cells.  The result
  remains an unsaturated finite-order obstruction: it does not rule out a
  support multiplier, a higher target power, or homogenized (t)-torsion.

  Thus chart 25 displays both sides of the source-relative phenomenon: the
  apparent degree-three failure disappears after earlier kernel tails are
  retained, whereas the degree-four circuit class survives the complete
  source-faithful transfer.

  The proposed reduction of the other 29 charts to these two is false at
  the first support-incidence layer.  The exact 31 by 31 incidence matrix
  has rank 24; a Hall deficiency-five witness forces at least five raw
  critical rows, and an acyclic lexicographic column contraction leaves
  precisely chart types 25--31.  Its transferred leading map on the seven
  critical source and target spaces is zero.  The actual next datum is the
  source-labelled 7 by 7 higher block \(\pi\delta_r\Sigma\); abstractly it
  can be arbitrary without changing the leading incidence, so the five
  extra types cannot be removed from chart counts alone.

  The full-ring lift of the 60-coordinate pure-product certificate is now
  exact through five off-support filtration layers.  At degree four, an
  exhaustive 24-port Macaulay calculation includes a disconnected 22-row
  target component.  At degree five, retaining all earlier kernel freedom
  gives a coupled \(72{,}985\)-row by \(224{,}153\)-column Schur system;
  a 7,861-column rational certificate with denominator lcm four proves

  \[
       H_0H_1H_2\in I_{\rm mix}+J^6.
  \]

  Exact replay covers all 818 target orbits through degree five.  This is
  truncated consistency, not full ideal membership; the next unsolved
  layer is degree six, and its coupled calculation must again retain the
  full kernel of every earlier layer.  The coupling now has an exact
  [Schur--Bockstein criterion](n8-filtered-macaulay-bockstein-schur-criterion.md):
  for a filtered block
  \(\left(\begin{smallmatrix}A&0\\T&B\end{smallmatrix}\right)\), a leading
  dual \(\lambda B=0\) survives precisely when
  \([\lambda T]=0\) modulo \(\operatorname {row}A\), after which its target
  value is the well-defined secondary pairing \(\lambda c-\mu b\).
  At degree five this connecting map kills 153 of 234 apparent leading
  duals; all 81 survivors annihilate the target.  This is a literal-source
  model for the secondary comparison sought in the uniform proof, although
  its uniform physical identification is still open.  At degree six, the
  fixed-tail leading closure has 590,739 row orbits, 1,425,600 column
  orbits, rank 579,546 over \(\mathbf F_{1009}\), and 11,193 apparent dual
  obstructions; the chosen residual is inconsistent in 6,254 coordinates.
  The first zero-frequency obstruction is killed by an exact integral
  two-column relation in the degree-at-most-five kernel.  Its degree-six
  tail has twelve row orbits and value one on the selected row.  After
  cumulative dual separation, however, a genuine half-integral class
  survives in the single balanced port multidegree: it has 80 lower and 20
  degree-six row orbits, annihilates all 706 incident actual columns over
  \(\mathbb Q\), and pairs to \(-1\) with the pure product.  Therefore

  \[
                         H_0H_1H_2\notin I_{\rm mix}
  \]

  at exponent one in the unsaturated polynomial ring.

  This is not a localized obstruction.  Normalizing the twelve support
  variables to one is exactly equivalent to localization at their product;
  it retains all 240 other coordinates and includes every Laurent support
  translation omitted by the balanced component.  The 100 dual rows descend
  to 100 distinct normalized monomials, but 903 of the 1,091 incident
  normalized columns violate the old dual.  Six half-integral column orbits
  already hit its projected target and leave a 564-orbit tail.  Thus the
  balanced critical class dies after the permitted localization.  A finite
  normalized certificate or a well-founded graded-Morse reduction remains
  open; because the normalized generators are inhomogeneous, a bounded
  degree rank calculation alone would not prove membership.  Homogenizing
  the normalized generators to degree four identifies the exact termination
  question with \(t\)-saturation.  The first residual-led closure has now
  been exhausted through homogeneous degree seven: an exact 49-row dual
  annihilates all 220 incident labelled columns and proves

  \[
                              t^7\notin I^h.
  \]

  This rules out a multiplier-degree-at-most-three unit repair only.  It is
  not the degree-twelve test for \(F^h\), and higher homogeneous S-pairs may
  still remove the class through \(t\)-torsion.  There is now a sharper
  finite route.  The 6,558 original homogenized generators have distinct
  squarefree degree-four leading monomials, so all non-product Buchberger
  pairs occur in degrees at most seven; a squarefree completion would make
  the normalized ideal radical and reduce the chart to one normal-form
  test.  The original generators fail this audit at the first degree-five
  pair: the Hamming-one words 1 and 2 leave an exact 180-term remainder,
  whose two nonzero stabilizer-orbit leading terms are nevertheless
  squarefree and \(t\)-free.  This cell is the universal Laplace
  star-minor transport

  \[
   B_uH_a-A_uH_b
       =\sum_{w\ne u,v}(B_uA_w-A_uB_w)
          H_{B\setminus\{v,w\}}.
  \]

  Its same-star critical pairs satisfy exact Pluecker and three-colour
  Koszul reductions.  Exhausting every original--original overlap completes
  degree five: 44,028 one-end transports and 39,977 direct-double
  transports give 84,005 mutually reduced 180-term cells with distinct
  squarefree leading monomials.  Cross-vertex compatibility breaks the
  squarefree degeneration at the next possible degree.  After the complete
  degree-five replay, the exact 546-term cell has the minimal leading
  monomial

  \[
       (02{:}00)(13{:}00)(46{:}00)^2(57{:}01)(57{:}12).
  \]

  None of its five squarefree degree-five divisors occurs in the completed
  leading set.  The opposite-order Bianchi square cancels as an identity
  but does not reduce either composition.  Hence this term order genuinely
  has a nonsquarefree initial ideal; this does not imply that the ideal is
  nonradical.  The repeated coordinate \(x=x_{46}^{00}\) instead selects
  the exact geometric vertex decomposition

  \[
       \sqrt I=\sqrt{I+(x)}\cap\sqrt{I:x^\infty}.
  \]

  For this first compatibility cell, both branches are now exact.  On
  \(x=0\), 258 terms disappear and the remaining 288-term polynomial is
  unreduced by the restricted degree-four/five basis, with squarefree lead
  `0951acd9e1f5`.  On \(x\ne0\), the Laurent multiple \(x^{-2}G\) has the
  squarefree pivot `0948ebef`; clearing denominators recovers \(G\).
  The Bianchi mate is the same source polynomial and supplies no ordinary
  polynomial factor of \(x\).  These statements resolve the multiplicity
  of the first cell only, not either branch's pure-target radical
  membership.  The split is also not forced by the ideal itself: an exact
  integral weight vector, supported on 103 normalized coordinates, preserves
  every certified degree-four and degree-five lead and gives the same
  546-term cell the unique squarefree lead `0951b4c7ebf5`, with weight
  margin one.  Thus the multiplicity is specific to the old lex refinement,
  not to the whole certified Groebner cone.  The
  [weighted degree-six census](n8-chart26-weighted-degree6-census.md) now
  counts the entire next frontier without expanding it: the degree4--4,
  degree4--5, and degree5--5 blocks contain respectively 967750, 792653,
  and 1165402 LCM-degree-six pairs, but only 7, 15, and 21 coarse
  source/overlap classes.  Exact reduction of one representative of each
  class gives 12 zero, 27 squarefree, and four nonsquarefree outcomes.  Two
  exceptional representatives contain hundreds of simple path-forest terms
  but none with either input's alternating base matching; they are genuine
  base-matching-exchange curvature.  The other two contain no simple path
  forest and suggested branch elimination before ordinary straightening.
  The latter two coarse signatures now have a complete
  [source-labelled refinement](n8-chart26-branch-class-uniformity.md), and
  they are not uniform normal-form classes.  The 8,412 mixed pairs split as
  2,986 squarefree and 5,426 collision cells; the 45,776 transport pairs split
  as 29,212 squarefree and 16,564 collision cells.  Every collision cell has
  one double coordinate, an exact lower contraction on its zero branch, and
  a squarefree `P3+P2+P2+P1` Laurent pivot on its open branch, with zero
  positive-power lower-normality failures.  This proves a uniform
  continuation/split routing rule for all 54,188 labelled pairs, although the
  32,198 squarefree outputs are themselves a new non-path frontier: 25,908
  have branched skeletons and 6,290 are decorated-squarefree with a physical
  parallel edge.  The other coarse classes remain representative data only.

  The underlying termination statistic is no longer conjectural at the
  combinatorial level.  The
  [path-forest skeleton](hafnian-path-forest-straightening.md) proves
  uniformly that every top term of a one-end or direct-double transport is
  a spanning forest $P_4+(h-2)P_2$.  Every even-component path forest has
  a unique alternating perfect matching $M$ and a partial join matching
  $J$; legal transports decrease the component count and terminate by
  degree $2h-1$ at an alternating Hamilton path.  Its two endpoints are
  the canonical candidate clean pair, while $J$ is a perfect matching on
  the remaining $2h-2$ vertices.  For fixed $M$, all higher source
  coherence already has an exact Koszul tower: the primitive star and
  direct-double cells are common-factor cancellations of
  
  \[
      \mu_M(d)H_c-\mu_M(c)H_d,
  \]

  whose triangle, tetrahedron, and higher simplex syzygies are formal.  The
  remaining new mathematics is to glue these fixed-base complexes through
  alternating matching flips and to control the primitive colon classes.
  The first gluing cell is now exact: for one alternating $C_4$ exchange, the
  [three-row determinantal audit](hafnian-path-forest-straightening.md#51-exact-alternating-c4-exchange-and-its-three-cell)
  verifies twelve endpoint identities, four 498-term base-exchange
  determinants, and two tetrahedral source syzygies.  The two input matching
  terms cancel separately in every determinant.  This supplies the local
  three-cell for the two path-bearing exceptional representatives.
  The subsequent
  [primitive colon audit](hafnian-path-forest-straightening.md#52-primitive-factorization-exposes-a-colon-obstruction)
  proves that this coherence does not reduce either remainder.  For the
  first class its primitive degree-six endpoint face is already lower-exact;
  for the second it only carries the remainder to degree-seven coordinate
  multiples.  Multiplication by every decorated $C_4$ coordinate remains
  irreducible against the complete degree-four/five basis, while the
  primitive three-state determinants first occur in degree eight.  The
  essential parallel-pair term in the chart-25 four-row dual is therefore
  the precise diagonal/colon correction absent from a genuine cycle minor.
  Equivalently, the polarized forest resolution must be
  transverse in the derived sense to all source-label identifications; local
  Bianchi squares alone do not imply this.  Collision cells in the two fully
  audited signatures now use the exact geometric vertex split uniformly as
  the fallback, while their squarefree strata enter a separate
  branched/parallel straightening problem without a split.  The
  next local theorem must incorporate the parallel-pair degeneration into the
  path-bearing base-exchange cells.  This replaces another
  blind homogeneous degree cap by a source-labelled forest/Koszul complex,
  but its base-exchange and terminal target readouts remain open.
  A sharper [curvature-Bockstein-or-Hamilton target](curvature-bockstein-or-hamilton-descent-target.md)
  reverses the role of the surviving colon class.  Global derived
  transversality may be unnecessary: a collision class which contracts can
  continue the forest, while a class which survives may itself be the
  source-relative obstruction, provided its connecting map has the exact
  curvature-weighted pure-target pairing and zero lift indeterminacy.  Chart
  25's four-row pairing three is the finite model for this second branch.
  The resulting target is a local obstruction/continuation/split dichotomy
  plus the terminal Hamilton-path clean-cap readout, rather than a complete
  Groebner basis or a global radicality theorem.  This is currently a
  proposed architecture, not a proved implication.  The
  [exact terminal audit](n8-chart26-terminal-hamilton-readout.md) now proves
  why its augmentation and zero-indeterminacy clauses are essential.  All
  $105^3$ normalized pure-target monomials retain unique matching-triple
  provenance; 5,596 degree-seven target rows are Hamilton paths and 5,388
  have a support-unit edge between their endpoints.  Nevertheless the 300
  path terms of the first mixed degree-six cell have 10,173 legal normalized
  terminal extensions with zero physical-target intersection.  On one
  uniquely sourced target Hamilton row an explicit active cap is clean on the
  coordinate face, but adding one invisible off-path spoke preserves its
  terminal coefficient and activity while changing the cap error from zero
  to four coefficients equal to two.  Hence a terminal forest coefficient is
  not yet the physical clean-cap readout; the transferred augmentation must
  reach the target and kill this source-lift ambiguity.  The abstract
  [augmented HPL lemma](augmented-hpl-terminal-bockstein-lemma.md) now proves
  the exact formula for such a readout:

  \[
       a_H=a(1+h\delta)^{-1}i,
       \qquad D_2=-p\delta h\delta i.
  \]

  It proves homology-class independence and explains why the naive terminal
  coefficient omits off-path corrections; the remaining content is the
  literal hafnian contraction and its physical augmentation.  On the first
  explicit spoke that content is now exact.  The
  [augmented terminal-chain audit](n8-chart26-augmented-terminal-chain.md)
  proves on the selected localized face that
  $H_{01000111}=x_{02}^{00}$ and that the four cap errors are the monomial
  multiples
  $(2x_{23}^{00}x_{57}^{00},2x_{23}^{00},2x_{57}^{00},2)H_{01000111}$.
  Thus one actual mixed source boundary supplies the complete first
  corrected-readout term.  Uniform terminal control has been reduced to a
  compatible triangular exposure order for all invisible coordinates; only
  the one-spoke instance is proved.

  The first proposed confluent $C_4$ transfer also has a sharp
  source-faithfulness correction.  The
  [literal chart-25 audit](n8-literal-hafnian-hpl-local-no-go.md) expands the
  quotient circuit to four $AB$ leaves and one $B^2$ centre.  All 56 incident
  actual columns obey $[D]=\sum_{j=1}^4[A_j]$.  Therefore a literal acyclic
  pair with first transfer $-A_1-A_2-A_3$ forces second transfer $-3D$, not
  the quotient toy value $+D$.  Their difference is the exact projected
  vector $4D$, which pairs nontrivially with the source dual and cannot come
  from any known raw mixed-hafnian column or zero-boundary syzygy.  The
  [exact relative-cell classification](n8-chart25-relative-4d-obstruction.md)
  also rules out the two obvious functorial repairs.  Ordinary
  label-diagonal Koszul tensoring specializes back to the same rank-four
  five-row source image, while Reynolds transfer carries $4D$ to the
  invariant $D$-orbit sum with pairing one.  The target mapping cylinder does
  contain $d(4sD)=4D-\tau$, with a source-labelled $d^2=0$ completion on all
  14 columns over the frozen centre, but this says only that the quotient
  packet is homologous to the target generator.  It is formal obstruction
  bookkeeping, not a correction.  Using the quotient obstruction therefore
  requires a new mixed source--diagonal transgression which derives the
  $-\tau$ component; merely adjoining the graph cell would be circular.
  Separately, the exact
  [cyclic eight-site calculation](cyclic-n8-diagonal-unit-ideal.md) excludes
  the twelve-parameter translation-invariant colour-diagonal chart by a
  rational unit ideal.  The unrestricted 33-parameter cyclic chart has full
  (834/834) linear output rank, so any obstruction there must be nonlinear.
* [Three-channel factorization, endpoint injectivity, response purity, and a
  common-power equation](curved-pure-binary-three-channel-response-guard.md)
  can hold simultaneously in an exact contracted guard.  The guard fails an
  uncontracted full row.
* The independently audited
  [pure-slice routing lemma](full-nine-pure-slice-channel-routing.md) uses
  that missing row to rule out a colour hidden in the same wrong singleton
  channel at both endpoints.  The audited
  [Hamming-one extension](full-nine-hamming-one-second-polar-routing.md)
  now replaces its vague surviving exits by an exact alternative: the direct
  block lies in the displayed channel cross, or every residual site is
  covered by a low-rank endpoint spoke or a fixed-label second-polar lift
  \(\Gamma_x(e)=\delta_{ed}M_d\).  Any off-diagonal direct entry also forces
  a singular spoke at both endpoints.  The audited
  [two-chart synchronization theorem](two-chart-hamming-one-gamma-synchronization.md)
  closes the generic simultaneous-lift branch at the two cross sites: if
  both lifts have the theorem's nonzero-compression provenance, both pure
  hafnian coefficients must vanish.  On that double-zero boundary all
  one-defect coefficients and cohafnian covectors vanish, while simultaneous
  bare identities at a common site reduce to the single cross-product
  residue \([\Theta z^{[h-2]}]=0\).  The independently audited
  [diagonal-anchor polar descent](double-zero-diagonal-anchor-polar-descent.md)
  now uses the completed full-nine system.  Uniform binary contraction
  factors a guaranteed \(t^2\), but does not produce a smaller hafnian
  source.  A diagonal-detecting compression instead exports a literal
  unary/binary source-provenant cap or a one-coordinate boundary.  The
  [common-label repair](double-zero-common-label-repair.md) closes every
  row hook, column hook, and crossed coordinate mismatch by a rank-one
  source-valid correction.  Its sole normalized-one-row survivor is the
  opposite-pure-diagonal, selected-entry-zero packet; the full second direct
  block is nonzero, so this is not the intrinsic direct-free boundary.
  When a common label is available, the two normal rows leave the exact
  noncancellable cubic with the required direct scalars retained.
* The independently audited
  [anchor--curvature selector](curvature-bearing-diagonal-anchor-selection.md)
  now puts a diagonal target and nonradial curvature into one literal cap.
  On the \(T=0\) branch its conditions are exactly
  \(K\notin\mathbb C C\) and
  \(\mathcal D\not\subseteq\mathbb C C\), and the selector can be rank one.
  On the \(T\ne0,\chi=0\) branch, the
  [full-square carrier theorem](full-missing-square-cap-carrier-resonance.md)
  reduces failure on one prescribed decorated edge to
  \(W=UC/h+H+G=0\).  The audited
  [relocation theorem](full-cap-carrier-resonance-relocation.md) proves that
  this is not a global carrier obstruction: all full-nine coefficient
  matrices span the diagonal target plane, so another literal edge exists.
  Off the radial line \(K\notin\mathbb C C\), one rank-one direct-zero cap can
  retain the curvature while relocating its edge.  The independently
  audited [radial relocation theorem](radial-common-line-curvature-relocation.md)
  closes the remaining singular common-line packet: every nonzero
  relocated cap coefficient is the negative sum of its two oriented
  physical transition-curvature evaluations, so at least one is nonzero
  and lies outside \(\mathbb C C\).  The original radial coefficient remains
  invisible, as it must; the proof discards it.  What is not supplied is a
  common relocated edge/probe choice across two charts.
* At the six-site boundary, the audited
  [physical dark-cut theorem](curvature-bearing-cap-to-k6-dark-cut.md)
  turns such a rank-one cap into a nonzero physical four-cycle differential
  whenever one active target colour is visible on all four sites
  complementary to a nonzero cap edge.  The
  [target-incidence audit](target-blocked-incidence-rank-drop-audit.md)
  rules out a generic-avoidance shortcut: both cap factors lie in the same
  missing-colour plane, so visibility requires a common zero of four
  bilinear wedge forms.  On a full invertible \(2\times2\) compression this
  leaves at most two candidates, and on a singular full square at most one
  per eligible ruling unless an exact alignment occurs.  The independently
  audited [blocked-site descent](target-blocked-site-polar-descent.md) then
  uses blocking positively: if an active target is blocked at at most two
  sites, a coordinate-endpoint cut and four quotient slots isolate a
  nonzero cap edge times a physical four-site hafnian, hence a dark
  matching for the same cap.  Thus total failure forces at least three
  blocked sites for every active target.  With two active missing labels,
  the residue is either a rank-two blocked site or a complementary
  \(3+3\) partition by the two coordinate lines.  The sharp guard already
  satisfies the selected diagonal and all six off-diagonal rows and fails
  exactly the other two diagonal anchors; those anchors or a second chart
  must now be used positively.  The independently audited
  [full-nine selector normal form](full-nine-isotropic-selector-blocking-normal-form.md)
  now uses all three labels rather than staying in the missing-colour
  plane.  For each target \(e\), define
  \[
       N_{x,e}=P_x^{\mathsf T}J_eS_x,
       \qquad T_e=\{x:N_{x,e}\in\mathbb C d\}.
  \]
  If \(\operatorname{rank}d\ge2\), total dark-cut failure forces
  \(|T_e|\ge3\) for every target; if \(d\) is invertible these are literal
  zeros \(N_{x,e}=0\).  Rank-one \(d\) has exact left/right ruling
  alignments, and \(d=0\) has the zero-matrix version.  The selector is
  target-specific, but its resulting edge automatically detects one of the
  two oriented physical transitions.  Thus the cap-dependent blocked-site
  split is superseded by source-level endpoint-wedge/direct-form
  alignments; comparing those alignments across the second chart is the
  remaining incidence task.
  The audited [two-chart alignment normal
  form](two-chart-alignment-curvature-normal-form.md) and
  [rank-two kernel-cap descent](rank-two-alignment-kernel-cap-descent.md)
  sharpen this rank by rank.  A same-target nonzero rank-two alignment
  synchronizes the two literal left-kernel lines.  Its full-nine kernel
  contraction either gives a physical dark cut, descends to zero endpoint
  wedges for both other labels, or reaches a common zero row/column or the
  target-centred support cross.  If both direct blocks have rank at most
  one, their left-kernel planes intersect automatically, so the same
  contraction exists without an alignment hypothesis.  On the invertible
  branch, the audited [zero-alignment incidence
  theorem](invertible-zero-alignment-two-chart-anchor-guard.md) gives the
  case-free bound \(2L+C\geq3\): either at least two repeated-alignment
  sites have endpoint-rank sum at most three, or at least three sites carry
  a common literal coordinate plane (with mixed alternatives measured by
  the same inequality).  The complete diagonal anchors additionally impose
  the pure-slice identity
  \(P_c^{\mathsf T}H_cS_c=E_{cc}-F_cd\).  A sharp two-chart seven-row
  guard misses exactly two diagonal anchors, so those pure slices, rather
  than invertibility or incidence alone, are the live input on this branch.
  The independently audited [complete-anchor one-hole
  descent](invertible-complete-anchor-one-hole-filtered-descent.md) now uses
  that input.  Since \(2L+C\geq3\) forces at least two doubly aligned sites,
  one lies on the five-site chart overlap.  Its two-target geometry is
  either a literal physical-channel hole or a total-wedge shore.  Taking
  the missing-colour coefficient of a diagonal anchor and an off-diagonal
  overlap row gives, on four sites,
  \[
       g_cA_{cc}+\lambda B_{ccc}=X_c,
       \qquad g_cA_{ij}+\lambda B_{ijc}=0\quad(i\ne j).
  \]
  Thus \(g_c\ne0\) gives an explicit lower-order divisibility
  representative, while \(g_c=0\) gives a named class in
  \(\operatorname {Ann}_3(\lambda)\); the total-wedge selector has the
  same alternative.  Coincident selected curvature forces the divisibility
  branch, but other positions and colours retain the colon residue.  This
  supersedes the former stopping point, not the incidence theorem or its
  guard, and is still not a complete invertible exclusion.
* On the singular target-centred cross, the complete 27-row overlap has a
  uniform odd-complement contraction.  The audited
  [shared-kernel rectangle](shared-kernel-odd-five-site-koszul-normal-form.md)
  gives
  \[
    L\left(y_jt_k+{T_{jk}\over h-1}z\right)z^{[h-2]}
       =\delta_{jk}\xi_jX_j,
  \]
  and the audited [right-kernel
  companion](target-centred-cross-odd-overlap-descent.md) supplies the
  complementary anchor packet.  Noncoordinate kernels therefore put all
  three literal target labels in one overlap.  The two crossed rows force
  exactly one selector-provenance class
  \(\omega_T\in\operatorname {Ann}_2(Lz^{[h-2]})\); they do not permit
  cancellation of the common factor.  The independently audited
  [complementary-kernel guard](complementary-kernel-colon-single-row-guard.md)
  realizes this sharply at \(h=3\): it has rank-two direct blocks,
  nonzero selected curvature, both kernel packets, and 26 of the 27 scalar
  overlap rows, while \(\omega_Tz\ne0\).  Its sole residual is the literal
  \((b,e,a)\) row, exactly the first row carrying
  \(x_b\omega_T\) with its direct--star companion.  This identifies the
  next source row but does not by itself construct the separate
  \(\operatorname {Sym}^{h-1}\) Macaulay prolongation.
* Once a physical differential exists, the audited
  [general \(K_6\) pullback theorem](general-k6-curvature-rowspace.md)
  identifies multiplication by the scalar base with the Hessian of the
  six-site hafnian.  The four-cycle covector pulls back exactly when it
  annihilates the Hessian kernel, equivalently when an explicit Schur
  compatibility holds.  Invertibility suffices, but the complementary
  four-site hafnian alone does not: a corank-one \(0/1\) guard violates the
  condition.  The independently audited
  [physical counterlift](physical-dark-cut-hessian-kernel-counterlift.md)
  shows that factor rank one, a literal unary cap equation, the pure
  two-site quotient, a dark matching, injective endpoint triples, and an
  invertible direct block still do not repair it.  That packet satisfies
  exactly seven full-nine rows and fails the same two unused diagonal
  anchors, so it does not test a complete full-nine or second-chart
  compatibility theorem.  Even a successful pullback is only aggregate; the
  direct/star/internal source grading still has to be transported through
  the literal overlap.  The independently audited
  [filtered provenance criterion](hessian-pullback-filtered-source-provenance.md)
  makes this second obstruction exact.  For a physical cap family
  \(C_{\rm cap}\), a selected pullback \(\mu\) comes from the top cap row
  exactly when
  \[
     \mu\in\operatorname{im}U_q^*+(L_qC_{\rm cap})^\perp
  \]
  (enlarged by any literally admitted graded-overlap rows).  An invertible
  uniform-\(K_6\), rank-one-pencil guard violates this condition.  The
  degree-five Macaulay cokernel functional is a further, separate output;
  prolonging the same filtered overlap is a natural sufficient route, not
  an automatic consequence of Hessian pullback.  On the literal full-nine
  selector family, the independently audited
  [small-matrix specialization](full-nine-selector-family-source-provenance.md)
  reduces source validity to
  \[
       F\in\Delta+\mathbb C d.
  \]
  For a completed \(2\times2\) square this is generically the single scalar
  \(\omega_d(F)=0\).  The cap edge uses the sum of the two oriented
  assignment tables, whereas the known Bianchi row controls their
  difference.  A two-anchor guard shows that even granting that difference
  as source-valid need not kill the scalar.  This is a fixed-selector-family
  criterion; it does not perform the separate physical-line Macaulay
  prolongation.
  Mixing several physical four-cycle covectors can repair an individual
  Schur-kernel failure, as the audited
  [cycle-mixing criterion](k6-cycle-span-hessian-mixing.md) shows, but this
  is not a universal escape: the audited
  [signed counterfamily](universal-cycle-span-hessian-signed-counterfamily.md)
  has nonzero curvature outside the pullback span of every cycle, and the
  [selector-sum lock](cycle-mixing-selector-sum-lock.md) shows that any
  same-orientation mixture still measures the same one-dimensional
  assignment-sum provenance class.  Cycle enumeration is therefore a
  diagnostic, not the missing source theorem.
* Fully dark shore contractions can attain equality.  In the sharp equality
  guard, the first row that detects the defect is the one-bright,
  uncontracted four-site jet.
* The independently audited
  [common-coloop counterguard](common-coloop-a-to-D-overlap-attack.md) proves
  that multiplication by the first common power \(A\) does not by itself
  control the second-polar part of multiplication by the polar difference
  \(D_{\bar K}(z)\).  Any successful transfer must use omitted full-nine
  rows or a nonflat second chart before multiplying by \(A\).  This is a
  negative guard, not a full-nine common-coloop theorem.

The shared lesson is not merely that “more equations are needed.”  Within
the focused anchored program, the surviving candidate mechanism is
consistently **source-relative full-nine overlap before contraction by the
common power**.  The current reductions do not prove that every possible
route to the dashed arrow must use this mechanism.

## 5. The sole primary target

The independently audited
[joint-extraction theorem](two-chart-joint-hypothesis-extraction.md) now
removes most of the proposed theorem's extraction ledger.  One selected
minor automatically supplies both physical-label full-nine systems, their
diagonal anchors, all four good endpoint maps, the all-label power-free
overlap and shared \((L,M)\) packet, first-chart activity, and ordinary
rootless selectors.  The audited
[tilted-chart theorem](tilted-second-chart-activity-and-zero-block-boundary.md)
removes scalar activity of the second chart as a separate extraction
obligation.  If \(A_{pr}\ne0\), either the canonical line is already active
or the theorem supplies an explicit active tilt through the same cap; in
either case the original curvature is retained as the \(u\)-coefficient.  If
\(A_{pr}=0\), activity on that pair is impossible, but the direct-free chart
remains a triangular, power-free auxiliary and a one-sided saturation
theorem does not need to localize it.

The genuine residuals are now:

1. a source-faithful overlap theorem for the tilted matrix direction, or its
   one-sided direct-free boundary; the canonical common-\((L,M)\) routing
   does not automatically survive the tilt;
2. on the anchored six-site interface, a positive use of the remaining
   complete-anchor rows which compares the at-least-three-site
   endpoint-wedge/direct-form alignments for the target-specific full-nine
   selectors: on the invertible branch the certified coupling of pure
   slices to \(2L+C\geq3\) now lands in a four-site
   divisibility-or-\(\operatorname {Ann}_3(\lambda)\) packet, which must be
   killed or converted into a dark cut; on the singular branch it must
   close the target-centred colon or its coordinate zero-row/column
   boundary;
3. on the resulting physical four-cycle differential, the Hessian-kernel
   compatibility on a singular scalar base and, on every base, a
   grade-preserving source overlap which kills the explicit filtered
   provenance class.  On the target-centred cross, the first unsuspended
   carrier is the weighted \((b,e,a)\) row, but a uniform chain map to one
   common \(\operatorname {Sym}^{h-1}\) Macaulay annihilator is still a
   separate requirement; and
4. branch-specific inactive routing for the tilted weighted target and the
   direct-free unary/complementary bridge.

At the first \(h=3\) boundary, these residuals have a particularly small
response-grade form.  For a selected off-diagonal row put

\[
 Q_j=R^{[j]}q^{[3-j]}\qquad(0\leq j\leq3).
\]

The admitted row is the first endpoint relation
\(\alpha Q_0+Q_1=0\), while the required pure-colour clean coefficient is
the reciprocal endpoint relation
\([c^6](\alpha Q_2+Q_3)=0\).  The
[conditional unipotent transgression](unipotent-response-transgression-clean-tail.md)
kills all four response grades if a response- and target-compatible lift
exists.  The independently audited
[Hamming-two boundary](h3-hamming-two-tangent-or-clean-boundary.md) proves
that the complete distance-two/full-nine truncation does not force a
global site derivation; its exact obstruction packet is nevertheless
already clean.  The independently audited
[complementary-diagonal guard](h3-diagonal-segre-second-transgression-seven-row-guard.md)
goes in the other direction: the selected all-word row, all six
off-diagonal rows, one diagonal target, good Segre stars, and one literal
adjacent decomposition can leave
\([2^6](\alpha Q_2+Q_3)=-2\).  Thus a positive local theorem must either

* construct a response-grade-aware, source-provenant second transgression
  from the simultaneous three-diagonal sector and the overlap; or
* prove a tangent-or-clean dichotomy in which failure of the compatible
  lift forces the reciprocal endpoint relation directly.

The second alternative cannot be proved after scalarizing the nine endpoint
rows.  The exact uniform
[scalar tangent--clean counterguard](uniform-full-nine-scalar-tangent-clean-counterguard.md)
has, for every (h\ge3), all nine scalar anchors, a rank-one Segre response,
three nonzero targets, and nonzero curvature, while both the shifted
comparison cokernel class and the reciprocal clean tail are nonzero.  A
physical tangent-or-clean theorem must therefore construct the annihilator
identity \(\tau_h o_h=0\) before discarding multisite grading or cross-chart
provenance.

The latest bounded audits make the first alternative substantially more
specific.  The
[selected-cap landing counterguard](h3-five-exposed-two-chart-selected-cap-landing-counterguard.md)
shows that the selected five-exposed coefficient packet alone does not force
the desired curvature landing; its direct-free and tilted specializations
fail the complete eight-site `pq` tensor EqSystem in exactly six and seven
coefficients, respectively.  The independently audited
[target-augmented filtered model](h3-target-augmented-filtered-d2-first-obstruction.md)
then shows that its raw curvature-weighted \(\beta_2\) representative is the
full target--residue cap graph and is killed by the common diagonal-anchor
mode.
Deleting the target coordinate would leave the desired odd residue, but the
result is not a cycle: its square defect is exactly \(-\kappa Y_c\,w\) and
requires a new adjacent-power/cross-quotient boundary.

Two natural repairs are now independently excluded at this same bounded-row
scope.  The
[selected adjugate contraction](selected-curvature-square-adjugate-tilted-overlap-contraction.md)
gives polynomial all-label identities for every \(I+E_{uv}\) tilt and remains
triangular on the whole-block direct-free boundary.  On the selected
nondegenerate two-channel summand it is a localized row-span contraction, not
a chain contraction of the full source complex; the accompanying absolute
rows retain the diagonal targets, while the relative rows cancel their common
mode.  The
[three-label target-Koszul audit](h3-multilabel-target-koszul-crossword-no-go.md)
shows that ordinary wedges, determinants, and the degree-two/three target
Koszul complexes cannot repair this.  After the exact missing rows are
included, the target-zero mixed rows have odd-tag spaces
\(\langle12112,12212\rangle\) in the direct-free packet and
\(\langle02012,22012\rangle\) in the tilted packet, whereas the required
pure tag is \(Y_0=00000\).  The odd-response image of the target kernel has
rank two, and adjoining that pure tag raises the rank to three.

The independently audited
[mixed-word reset calculation](h3-mixed-word-reset-cross-quotient-chain-lift-no-go.md)
now crosses the remaining word-space gap but not the source-chain gap.
Coefficient extraction at a mixed word followed by ordered reinsertion of
`00000` descends on the actual odd quotient for the direct-free tags `12112`
and `12212` and the tilted tag `02012`; the tilted tag `22012` fails descent
by exactly two displayed denominator terms.  On the rational guards, the
descended resets have the numerical output \(-\kappa[00000]\).  Their inputs,
however, are precisely the nonzero EqSystem defects and hence vanish on a
true source.  Moreover the two direct-free resets define distinct quotient
maps, so zero indeterminacy does not follow from their agreement on the
guard.

Consequently the smallest live \(h=3\) construction is a one-higher relative
source syzygy lifting one of these resets to the EqSystem/cap complex.  Its
filtration-lowering term must supply the lower boundary
\(d_0n_0=\kappa Y_0w\), canceling the already-audited square defect
\(-\kappa Y_0w\), retain \(-\kappa[00000]\) in the associated-grade odd
readout, and have zero readout on the difference of any two physical lifts.
Neither these strict word-space resets nor the audited undecorated
target-side higher operations supply those properties.  The chain lift and
zero-indeterminacy must be proved before the rootless Macaulay readout is
invoked.  This is the bounded-row formulation at the interface of Components
III--IV of the unified theorem, not a complete \((8,3)\) argument.

The first universal two-row source-resolution test is now independently
audited in the
[first-syzygy multidegree gate](h3-direct-free-first-syzygy-multidegree-gate.md).
For the global word \(m_8=01211222\), fine site--colour degree excludes a
comparison with the pure row below edge degree four.  On those two rows the
unique primitive first cell is the ordinary Koszul syzygy

\[
 K_{m_8}=H_{m_8}r_0-(H_0-u)r_{m_8}
     =u r_{m_8}+H_{m_8}r_0-H_0r_{m_8} .
\]

After dehomogenizing, its lowest symbol is \(+r_{m_8}\), and scaling by
\(1/4=-\kappa_{\rm df}\) gives the required formal normalization.  The
obstruction occurs one layer earlier: coefficient reset at `12112` fails on
the universal odd denominator presentation.  Writing
\(\bar m=12112\), the five independent columns are

\[
 d_{v,\bar m_v}\longmapsto h_vY_0,
 \qquad
 h_v=\operatorname {Haf}(q_{\bar m}|_{D\setminus\{v\}}),
 \quad v=1,\ldots,5.
\]

The independently audited
[universal reset no-go](h3-universal-denominator-reset-polynomial-no-go.md)
proves that every polynomial denominator annihilator has all word
coordinates in the \(q\)-augmentation ideal; in particular no normalized
polynomial correction exists.  At pure output the old five denominator
faces and these five mixed faces have combined rank ten in the associated
\(q\)-degree-two pure-output piece.  The minimal abstract presentation has
five independent labelled initial components, which can be displayed as
\(d\tau_v=h_vY_0\).  This neither supplies physical source data nor proves
that five separate physical cells are necessary: one equivariant/relative
cell or one full-source Tor construction could package the components.

Three plausible ways of manufacturing those components are now sharply
bounded.  First, the independently audited
[derived cap calculation](derived-base-change-relative-cap-obstruction.md)
shows that the split cap and formal occupancy blocks create no new required
target-zero class under ordinary derived base change.  Non-flat base change
of the **full** source complex may still create invisible chains through
\(\operatorname {Tor}_1(\operatorname {coker}b,S)\), but the independently
audited
[minimal denominator calculation](h3-denominator-tor-transgression-fitting-gate.md)
has transgression rank only four on the direct-free non-source rational
guard and three on the tilted non-source rational guard, despite nonzero
curvature and vanishing of all five scalar \(h_v\).  These ranks are
counterguards, not constraints on the full-nine quotient.  The exact
full-ring target is the module membership
\(b_{\rm sel}(S^5)\subseteq\operatorname {im}b_{\rm oth}\), with the local
augmented-minor test valid only on a constant-rank stratum.  Second, the
independently audited
[sitewise covariance calculation](h3-sitewise-gl3-covariance-face-tau-no-go.md)
gives, for every \(S\subseteq F_v\),

\[
 \left(\prod_{x\in S}L_x\right)
 \left(\prod_{x\in F_v\setminus S}D_x\right)\delta
     =h_vY_0.
\]

Thus all sixteen corners agree; the alternating connection cube is zero and
merely locks the desired output to an equal source-derivation companion.
Third, the
independently audited
[literal four-face search](h3-direct-free-literal-four-face-full-nine-no-go.md)
finds rank \(48/48\) in every first compatible fine-degree block.  Doubling
the `pq/pr` presentation adds only tautological chart comparisons, on which
every readout through the common global coefficient vanishes.

The complete all-face refinement
[checks the full strict first fine degree](h3-direct-free-complete-first-fine-degree-membership.md),
not only the 48 EqSystem columns.  For every deleted face, all fifteen raw
denominator columns have no term dividing the proposed squarefree EqSystem
degree; the doubled EqSystem block still has rank 48 and exactly the 48 chart
comparisons as kernel.  The reset output \(h_vY_0\) belongs to a different
shifted module degree: its displayed slot degree omits the three
\(x,p,q\) zero slots of the EqSystem degree.  Thus the census excludes an
overlooked **raw** strict denominator column, but an explicit module shift
is still part of any degree-lowering comparison.  A programmed
cap--target graph has rank \(48\to49\), but its \(U_0\mapsto Y_0\) landing
and sign are declared inputs, not a reconstructed physical augmented
differential; that rank cannot be used as source provenance.  In the fixed
direct-free chart the five labelled faces have the three symmetry orbits
\(\{1,4\},\{3\},\{2,5\}\); two templates occur only across a separately
compatible family of relabelled \(r\)-charts.

That last search also identifies the missing symbols exactly.  If \(c_v\)
is mixed on \(D\setminus\{v\}\) and zero on \(x,v,p,q\), then

\[
  \frac{\partial^2H_{c_v}}
      {\partial a_{xv}^{00}\,\partial a_{pq}^{00}}=h_v,
\]

with the three terms lying in the `pq`-direct sector and the same three in
the direct-free `pr`-two-star sector.  The
[shifted principal-parts comparison](h3-shifted-principal-parts-comparison-obstruction.md)
now constructs this strict source-relative object through that symbol.  For
\(K_v=r_{c_v}^{pq}-r_{c_v}^{pr}\), both first faces and the mixed global
boundary cancel, while the Rees filtration records precisely the transfer
of \(h_v\) from the `pq`-direct to the `pr`-two-star sector.  Fine grading
forces the unique shift

\[
                   \sigma=e_{x,0}+e_{p,0}+e_{q,0}.
\]

This removes the former ambiguity between ordinary differentiation and a
genuine relative comparison, but it also exposes the next obstruction.  The
reset commutator has five independent components modulo the old denominator
image, and the desired scalar cap coefficient obeys
\([\kappa Y]\ne0\) in \(R/(h_1,\ldots,h_5)\).  The diagonal GHZ stabilizer
independently assigns these five components five independent characters;
weight-space contraction would merely adjoin the missing physical
homotopies by hand.

Two additional internal derivatives nevertheless produce a canonical
[degree-zero four-cube symbol](h3-qzero-denominator-rees-four-cube.md): for
every perfect matching \(N\) of the complementary four-face,

\[
 \partial_N\partial_{u_v}\partial_tH_{c_v}=1,
 \qquad
 \partial_N(P_m\delta)(d_{s,a})=\delta_{(s,a),(v,m_v)}Y_0.
\]

There is no leakage into the other fourteen denominator columns, the cube
signs close, and Reynolds averaging gives the uniform selector
\(L_v(h_s)=\delta_{vs}\) for every odd face set.  The
[independent audit](h3-qzero-denominator-rees-four-cube-independent-audit.md)
shows exactly why this is not yet the cap landing: the polynomial jet has no
constructed comparison to the split-cap complex and no defined ordinary
residue.  The same evidenced boundary and target are compatible both with
the rank-raising column \((\kappa Y,0,0)\) and with the old graph column
\((\kappa Y,0,\kappa Y)=\kappa Y\rho\).  Thus the live object is no longer
an unspecified polar; it is an attaching map from this denominator-marked
four-cube whose ordinary residue must be proved zero, followed by the
curvature remainder needed for a genuine filtered cycle.

The exact
[bare-cap attaching obstruction](h3-reynolds-attach-coupled-obstruction.md)
shows that these tasks cannot be performed sequentially.  In the old cap
span \(\langle T,\rho\rangle\), an invisible chain with boundary
\(\gamma w\) exists if and only if \(\gamma=0\): target-zero forces the
unique lift \(\gamma\rho\), whose ordinary residue is \(\gamma\).  Thus the
higher Koszul and curvature sector must manufacture the missing chain at
the same time.

There is now a positive exact model for that coupling.  The
[higher-Koszul jet calculation](h3-koszul-reynolds-higher-commutator-obstruction.md)
applies the Reynolds selector and the minimal endpoint-\((22\to00)\)
operator to the physical cell
\(K_m=ur_m+H_mr_0-H_0r_m\), obtaining the closed pure-row symbol
\(s_v=r_0\).  In the selected principal-parts/cap cone,

\[
 n_v=s_v-T_v,qquad
 (d,\operatorname {tgt},\operatorname {ores})(n_v)
       =(Y_0w_v,0,0),
\]

and \(\kappa(s_v-T_v-Y_0\rho_v)\) is a target-zero cycle with ordinary
residue \(-\kappa Y_0\).  This derives rather than declares the missing cap
column in the formal jet cone.  Its remaining gap is functorial descent:
the selector has nonzero second-order Leibniz commutators, so one must
realize it as an \(R\)-linear map from a genuine principal-parts
totalization, glue its `pq/pr` faces, and prove that physical ordinary
residue remains zero.  The same-power lock does not apply before this
descent because \(s_v\) lies in the adjacent-power jet summand, not the old
cap graph line.

The complete
[fourth-Hasse cone audit](h3-full-hasse-cone-d4-descent-obstruction.md)
performs the first of those tasks and sharpens the last.  With squarefree
jet generators it constructs the honest prolonged Koszul chain

\[
 s_I=\sum_{S\subseteq I}(\partial_SH_m)r_0[I\setminus S]
       -(H_0-u)r_m[I],
 \qquad n_I=s_I-T,
\]

so \(dn_I=Yw\) with zero target and cap residue; all proper Hasse faces,
both strict chart sectors, and all fifteen denominator supports check.
But diagonal projection to the old physical cone has the exact commutator
\((H_0-u)e_0\), and the selected fourth operator sends the source equation
\(H_m\) to one.  Therefore neither projection nor post-specialization is a
physical chain map.  The missing object is now specifically a source-valid
fourth Spencer/Hasse lift which absorbs the proper faces without turning
the zero class of \(H_m\) into the unit.

The corrected
[augmented Hasse--Schmidt criterion](h3-augmented-hasse-schmidt-polar-membership.md)
makes the typing requirement exact: for already constructed invisible first
jets, a mixed correction exists if and only if its augmented Hessian class
lies in the image of the augmented source Jacobian, and a later landing is
well defined exactly when it kills the Jacobian kernel.  It does **not** yet
compose the formal polar class \(h_vY_0\) with the independently known split
cap class \(\kappa Yw_v\); source-valid first jets and a target/residue-
compatible comparison morphism remain missing.  The exact
[dual Schur audit](h3-literal-full-nine-schur-polar-no-go.md) now tests the
bare marked principal-parts comparison on its literal source columns.
The ten \(pq/pr\) columns have lower rank five and kernel generated by the
five pairwise chart differences.  Their marked polar tails give the exact
source-relative connecting matrix \(I_5\).  Hence none of the five leading
polar cochains admits \(\Lambda T'=MA'\), and the otherwise exact
target-side factorization \(1\cdot\kappa\cdot Y=\kappa Y\) is not yet a
well-defined Schur pairing.  The denominator-marked two-edge comparison
must contribute \(-I_5\) before the target is evaluated.
Full sitewise semisimplicity does not supply that morphism.  The
[\(\mathfrak{sl}_3\) Casimir counterguard](h3-full-sitewise-sl3-casimir-face-counterguard.md)
places the old face denominator in the trivial summand of
\(\operatorname{End}(\mathbb Q^3)^{\otimes4}\) and the polar in
\(\operatorname{ad}^{\boxtimes4}\); the total Casimir eigenvalues are zero
and 24.  It therefore splits the polar into the cokernel rather than giving
a source preimage.  Moreover the actual four-site GHZ stabilizer is only a
six-dimensional abelian diagonal algebra, so a Whitehead/Casimir contraction
is not an operation on the fixed-target augmented complex.  A Spencer use
would have to adjoin and type precisely the missing jet generator.

Ordinary first-derivation solvability and an unweighted sum of the selected
Hamming-two coefficients are both strictly stronger or simply false
targets.  This \(h=3\) formulation is a diagnostic for the uniform overlap
lemma below, not a new certified-spine dependency.

The strongest literature-derived aggregate object for item 3 is the audited
[explicit \(K_6\) matching-Lefschetz inverse](related-work-and-lean-artifacts.md#2-matching-algebra-lefschetz-inverse).
It inverts the edge-to-four-set incidence exactly.  The
[source-provenance guard](k6-lefschetz-source-provenance-guard.md) proves
that aggregate invertibility and one anchor are insufficient.  It also
reduces the candidate comparison to four weighted complementary cuts.  The
[finite-polarization theorem](k6-finite-curvature-polarization-and-grade-transport.md)
proves that every finite curvature rectangle has a case-free rank-one
polarization detected nontrivially by those cuts.  The new cap theorems now
construct a literal factorized candidate \(\beta\) carrying diagonal target
data and curvature, and the dark cut produces
\(d\kappa_q(\beta)\ne0\) when its target is locally visible.  For an
arbitrary physical scalar base, the exact aggregate pullback criterion is
\[
                 d\kappa_q(\ker\operatorname{Hess}
                    (\operatorname{Haf}_6)_q)=0.
\]
This cleanly separates two missing statements.  First, the remaining
two-chart overlap must make the full-star/direct-form alignment normal
forms incompatible with the selected nonzero curvature, and the two unused
diagonal anchors must control the singular Hessian kernel.  Second, even
when the aggregate pullback exists, the direct/star/internal overlap must
kill the fixed-chart scalar provenance class before the common power and
must also produce a nonzero degree-five Macaulay cokernel functional.  The
shared sign pattern, a nonzero complementary hafnian, a Bianchi difference
row, and a single-beta scalar match do not supply these family-level
statements by themselves.

The precise target, with its automatic hypotheses, literal modules, four
missing components, dependency table, implication proof, and explicit
nonclaims, is the
[unified full-nine two-chart overlap--jet saturation theorem](unified-full-nine-two-chart-overlap-jet-saturation-target.md).
It is the unconditional tilted/one-sided replacement for the earlier
conditional [diagonal-anchored overlap lemma](adjacent-literature-and-anchored-overlap-jet-lemma.md):

> An active \(pq\)-chart and the source-faithful \(pr\)-overlap auxiliary
> selected by one nonzero minor—using an active tilt when \(A_{pr}\ne0\)
> and the direct-free triangular packet when \(A_{pr}=0\)—cannot realize the
> rootless or all-inactive obstruction after the two labelled anchors,
> crossed four-index row, and weighted curvature-normal class are transported
> through the same overlap.

Its required conclusion is an active clean cap, on the first chart in the
one-sided boundary and on at least one chart when both are localized.  This
is a proposed lemma, not a proved consequence of a standard determinantal
complex.  The extraction problem is now precisely the four-item residual
above, rather than a demand to prove second canonical activity.  No
fixed-colour selector, diagonal unary--complementary routing, or cofactor
root is included as an assumption.

It has two concrete outputs rather than a new case census.

* In the rootless ledger, it forces a rank defect in the residual quotient
  after the known nonvanishing Macaulay block is removed—equivalently, it
  constructs the required physical annihilator.
* In the inactive-root ledger, its displayed \(\Omega\)-pair conclusion is
  the first boundary \(h=3\) normal form: it prevents both
  source-provenant charts from realizing the independent or
  exactly-one-zero alternatives.  A uniform theorem must replace this by
  the degree-\((h-2)\) boundary certificate.

The shore gates in Section 3 are local normal forms on which this theorem
must be proved or tested.  They are not four unrelated conjecture-level
lemmas.  Likewise, the \(h=3\) response-grade split is a bounded
falsification/structure gate: an inactive clean landing by itself does not
satisfy the active-clean conclusion.

## 6. Work that should not be reopened

Unless a new invariant connects it directly to the dashed arrow in (2), do
not allocate agents to:

* finding a curved pair or reclassifying the globally flat branch;
* forcing the stronger identity \(r^2=0\);
* another fixed six-site pure-lift or coordinate-plane profile;
* Hall-, selector-, one-anchor-, or top-apolar-only implications;
* another fully dark rank refinement without a one-bright row;
* another generic-avoidance argument confined to the missing-plane
  rank-one selector conic: the full three-label selector has already
  converted failure into universal endpoint-wedge/direct-form alignments;
* treating one equality \(W_{rs;c,d}=0\) as a global cap-carrier failure;
* inferring four-cycle row-space pullback from a nonzero complementary
  hafnian without checking the Hessian-kernel condition;
* treating a scalar top-row match on one selected cap as a source lift on
  the cap family or as a Macaulay cokernel functional;
* deriving \(A\)-to-\(D(z)\) transfer from \(A\)-annihilation alone; or
* another isolated collision cell with no all-order mechanism.

## 7. Secondary tests, not independent primary routes

The unified two-chart overlap theorem is the sole primary allocation.  The
following narrower packets remain useful only when they construct, test, or
falsify one of its four literal module maps:

1. on the exact double-hafnian-zero packet, use the second chart to
   contradict or descend from the at-least-three-site
   endpoint-wedge/direct-form alignments.  Common-label hook mismatches,
   the cap-dependent blocked-site split, and the one-chart radial carrier
   are already superseded or repaired; the
   opposite-pure-diagonal selected-entry-zero packet and possible
   two-chart coefficient synchronization remain.  Failure of a
   \(\Gamma\)-lift is already a sitewise low-rank-spoke alternative;
2. an E1/E2 physical overlap packet which directly yields a clean cap or a
   source contradiction, rather than merely selecting a line;
3. on the six-site scalarization, use the two missing diagonal anchors to
   kill the offending Schur-kernel class, then use a source-valid second
   crossed/overlap row to kill the scalar selector-family provenance class
   and prolong to one nonzero Macaulay cokernel functional; and
4. exact unrestricted counterexample search, accepted only with a finite
   decorated lift satisfying every colouring coefficient.

Any success here must be exported to the unified theorem or directly
produce one active clean point.  It then returns immediately to the proved
descent in (2); no further global structural classification is needed.
