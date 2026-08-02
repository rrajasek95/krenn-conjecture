# Consolidated proof frontier

Audit date: 2026-07-31.

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

## 1. One missing conjecture-level implication

After selecting three palette colours, write the endpoint-ordered aggregate
matching equation as

\[
                         H_B(A)=\Delta_{B,3}.
\tag{1}
\]

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
| [Common coloop](common-coloop-clean-cap-affine-fibre.md), \(b=1\) | The [anchor--polar response quotient](common-coloop-anchor-polar-response-quotient.md) makes the comparison source-faithful. Its [polar-dual refinement](common-coloop-polar-dual-forced-diagonal-boundary.md) closes the fixed nonzero missing diagonal and classifies the other failures. The [literal two-arm kernel criterion](common-coloop-two-arm-polar-kernel-boundary.md) closes both nonmissing interpolation strata whenever two fixed-scalar polar-kernel arms have independent \(A\)-coordinates; an actual consecutive-power one-corner packet realizes the pre-scalar \(A/D\) tensor condition | In the two-arm-kernel subcase, force the source-determined residual into the polar image at some attainable \(z\ne0\). In general, avoid the original three dual strata: one polar-cokernel annihilator and the two labelled \(A\)-through-\(D_{\bar K}(z)\) interpolation covectors |
| [Line plus plane](line-plus-plane-shore-clean-cap-pencil.md), \(b=2\) | A whole projective clean pencil; its generic member is active | A kernel line missing one fixed diagonal label, or a rank-one endpoint confined to one fixed row, together with the endpoint-transposed versions |
| [Rank \((1,1)\)](rank-one-rank-one-shore-clean-quotient-plane.md), maximal \(b=3\) endpoint-dark refinement | A four-dimensional clean double-annihilator plane; its generic member is active | A fixed coordinate row/column, or \(a=\lambda x^{\mathsf T}+y\mu^{\mathsf T}\); without a coordinate gate, the scalar gate is already impossible for \(b\leq2\), while overlaps of the gates remain unclassified |
| [Endpoint-dark shore](endpoint-dark-shore-consecutive-power-jet.md) | Every fully dark contraction factors the fixed target through one literal consecutive-power cofactor map | A kernel/target separation in the one-bright four-site jet; two-site compatibility is needed only if every one-bright jet stays aligned |

Thus the generic \(b=2\) and rank-\((1,1)\), \(b=3\) geometries are
finished.  Agents should work only on the displayed fixed-coordinate,
scalar, cofactor, and affine-fibre gates—not on the old unrestricted shore
classification.

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

## 5. The natural breakthrough theorem

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

The most coherent main target is a tilted/one-sided generalization of the
proposed [diagonal-anchored two-chart overlap--jet saturation
lemma](adjacent-literature-and-anchored-overlap-jet-lemma.md):

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
above, rather than a demand to prove second canonical activity.

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
lemmas.

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

## 7. Parallel attacks that remain genuinely independent

The main two-chart overlap theorem should receive most effort.  The useful
independent backstops are narrower:

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

Any success in the main theorem or a backstop that produces one active
clean point immediately returns to the proved descent in (2); no further
global structural classification is then needed.
