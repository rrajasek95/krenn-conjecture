# Certified-spine supersession ledger

This ledger is append-only.  It is initially empty because
`certified-spine-2026-07-30` is the certification baseline.

A research result, computation, or author self-check does not modify the
certified spine.  A supersession is accepted only when all of the following
are recorded:

1. the stable dependency ID from [`BASELINE.md`](BASELINE.md), or from an
   earlier accepted supersession;
2. the exact old file and certified commit being replaced or narrowed;
3. the new theorem or guard, with its exact hypotheses and scope delta;
4. the new proof artifact and exact checker, when computation is used;
5. an independent audit performed by an agent other than the author;
6. the audit outcome and every correction it required; and
7. the commit that contains the audited replacement.

Use this record format:

```text
## SUPERSESSION-YYYY-MM-DD-NN

- Dependency ID:
- Replaces:
- Replacement:
- Scope delta:
- Proof artifact:
- Checker:
- Independent auditor:
- Audit outcome/corrections:
- Certified commit:
```

After appending an accepted record, update the current consolidated spine in
the same commit or in a directly linked follow-up commit.  Claims not covered
by the named scope delta retain their prior certified status.  Negative
guards may narrow a dependency or invalidate a proposed implication, but
must not be described as positive closure.

## SUPERSESSION-2026-07-30-01

- Dependency ID: `LOCAL-INVERTIBLE`
- Replaces: the stopping point after the `2L+C>=3` incidence and pure-slice
  identities in `notes/invertible-zero-alignment-two-chart-anchor-guard.md`
  at baseline commit `835ed0db2ba1111cffad2ce7b3a231ce081c3178`.
- Replacement: `notes/invertible-complete-anchor-one-hole-filtered-descent.md`
  at commit `b04cc6430d7b70ed4bbbba2f97243bbe6a88a2b4`.
- Scope delta: complete anchors now force a doubly aligned witness on the
  common five-site overlap and an exact four-site divisibility-or-colon
  packet.  This supersedes the old *stopping point*, but retains the old
  incidence theorem, pure-slice identity, and guard.  It does not prove a
  dark cut, a Macaulay functional, or complete invertible exclusion.
- Proof artifact: `notes/invertible-complete-anchor-one-hole-filtered-descent.md`.
- Checker: `computations/verify_invertible_complete_anchor_one_hole_filtered_descent.py`.
- Independent auditor: `/root/sol_ultra_audit_invertible_one_hole_descent`;
  permanent report in
  `certification/audits/SUPERSESSION-2026-07-30-01.md`.
- Audit outcome/corrections: PASS; no corrections required.
- Certified commit: `b04cc6430d7b70ed4bbbba2f97243bbe6a88a2b4`.

## SUPERSESSION-2026-07-30-02

- Dependency ID: `INACTIVE-BOUNDARY`
- Replaces: the off-diagonal part of the all-inactive stopping point in
  Section 2 of `notes/consolidated-proof-frontier.md` at baseline commit
  `835ed0db2ba1111cffad2ce7b3a231ce081c3178`, which required routing every
  inactive selected line into two diagonal unary--complementary subpackets.
- Replacement: `notes/offdiagonal-base-locus-ternary-omega-residue.md` at
  commit `e9ffdf3e78562bddb839a415d9b485f725f61e03`.
- Scope delta: on every all-inactive off-diagonal selected line, the
  nonconstant coordinate gcd forces at least one of the two inactive
  endpoints to be clean.  Removing that endpoint factor gives a degree
  `h-1` residual and the bounded certificate `(tu)^(h-1)`; if both endpoints
  are clean the degree and exponent sharpen to `h-2`.  Every surviving
  colour has normalized odd residue `-Ybar_c`, so off-diagonal coefficient
  routing no longer depends on a diagonal unary--complementary interface.
  This does not handle a diagonal selected line, prove that some `Ybar_c`
  survives, construct the source-filtered overlap correction, or produce an
  active clean point.  All other parts of `INACTIVE-BOUNDARY` retain their
  prior status.
- Proof artifact: `notes/offdiagonal-base-locus-ternary-omega-residue.md`.
- Checker:
  `computations/verify_offdiagonal_base_locus_ternary_omega_residue.py`.
- Independent auditor:
  `/root/sol_ultra_inactive_omega_two_chart_coboundary`; permanent report in
  `certification/audits/SUPERSESSION-2026-07-30-02.md`.
- Audit outcome/corrections: PASS after a fresh audit of the strengthened
  reverse-endpoint orientation and exhaustive gcd routing; no corrections
  required to the certified replacement.
- Certified commit: `e9ffdf3e78562bddb839a415d9b485f725f61e03`.

## SUPERSESSION-2026-07-30-03

- Dependency ID: `INACTIVE-BOUNDARY`
- Replaces: the surviving-class limitation retained by
  `SUPERSESSION-2026-07-30-02` and by Section 2 of
  `notes/consolidated-proof-frontier.md` at certification commit
  `0e7218402c5af79cef8f2b629f9164974e424d91`.
- Replacement: `notes/odd-residue-minimality-survival.md` at commit
  `779e5bfc7d21dfe40fa167b5ed120ded78ae4314`.
- Scope delta: for a minimum-order exact ternary source in the forbidden
  range `|B|>=6`, at least one monochromatic class `Ybar_c` survives in
  every odd quotient arising after the selected two-site cap.  If all
  three vanished, their linear lifts would assemble, without division,
  into an exact ternary source on `|B|-2>=6` sites.  Since every diagonal
  coefficient of the off-diagonal scalar-zero endpoint is the same
  nonzero scalar `-alpha`, that endpoint detects whichever class survives.
  Thus nonzero-label survival is complete on the routed off-diagonal
  inactive branch.  This does not construct the source-filtered overlap
  correction, handle visibility at unequal or collided diagonal boundary
  coefficients, or produce an active clean point.
- Proof artifact: `notes/odd-residue-minimality-survival.md`.
- Checker: `computations/verify_odd_residue_minimality_survival.py`.
- Independent auditor: `/root/sol_ultra_two_site_collision`; permanent
  report in `certification/audits/SUPERSESSION-2026-07-30-03.md`.
- Audit outcome/corrections: PATCHED/PASS.  The auditor corrected the
  minimality quantifier to exclude the allowed order-four ternary source,
  repaired TeX corruption, and added exact aggregate-to-decorated-source
  and order-four exception checks.  No mathematical gap remains in the
  patched scope.
- Certified commit: `779e5bfc7d21dfe40fa167b5ed120ded78ae4314`.

## SUPERSESSION-2026-07-30-04

- Dependency ID: `INACTIVE-BOUNDARY`
- Replaces: the unresolved diagonal coefficient-routing part of Section 2
  of `notes/consolidated-proof-frontier.md` retained by
  `SUPERSESSION-2026-07-30-03` at certification commit
  `47440f90434c51533959b4232a283962e0761c5a`.
- Replacement: `notes/diagonal-three-boundary-inactive-routing.md` at
  commit `f57ee88f3dce38b3770bd2a08b2f005be782cb30`.
- Scope delta: a diagonal selected line has exact activity divisor
  `t u^2 (t+beta u)`.  For `beta!=0` its three distinct inactive boundary
  points admit exhaustive scalar coefficient routing, a symmetric bounded
  certificate, and a chartwise two-boundary certificate after removal of
  the full third-boundary coordinate-gcd multiplicity.  Its two normalized
  boundary jets have determinant `h beta`, and each generic jet detects
  every possible surviving colour.  For `beta=0`, the boundary collision
  is the binary unary--complementary packet and may be blind to the selected
  colour.  This supersedes the diagonal activity, factor, certificate, and
  generic coefficient-visibility gaps.  It does not prove that scalar-gcd
  saturation or jet transport lifts through the literal source filtration,
  resolve selected-colour blindness at collision, construct the middle
  correction, or produce an active clean point.
- Proof artifact: `notes/diagonal-three-boundary-inactive-routing.md`.
- Checker:
  `computations/verify_diagonal_three_boundary_inactive_routing.py`.
- Independent auditor:
  `/root/sol_ultra_audit_diagonal_three_boundary`; permanent report in
  `certification/audits/SUPERSESSION-2026-07-30-04.md`.
- Audit outcome/corrections: PASS; the auditor independently re-derived the
  activity geometry, collision, factor orientations, certificates, and
  normalized jets.  No corrections were required.
- Certified commit: `f57ee88f3dce38b3770bd2a08b2f005be782cb30`.

## SUPERSESSION-2026-07-30-05

- Dependency ID: `INACTIVE-BOUNDARY`
- Replaces: the unspecified same-complement source-correction route retained
  on the off-diagonal branch by `SUPERSESSION-2026-07-30-03` and Section 2
  of `notes/consolidated-proof-frontier.md` at certification commit
  `122fb66f0d8d499da32853d45e5807001468eda9`.
- Replacement: `notes/offdiagonal-same-power-target-residue-lock.md` at
  commit `bcb7ddf6bc17140fc37a8fc049b9cb9d2eba5fa0`.
- Scope delta: the scalar-zero cap calculation yields the legal
  response--target pair `(alpha^-1 R,-Delta)`, not a proved map from the
  radial generator to `alpha^-1 R`; the distinction includes exact
  `tau=0` and `tau!=0` normalization guards.  Every literal quadratic row
  on the same complement and against the same divided power has its
  diagonal target coefficient locked to its ordinary odd residue, so a
  same-power target companion necessarily erases the desired response.
  The literal connection, normal, curvature, and direct-double rows do
  provide the exact adjacent-power overlap syzygy (35), with all signs and
  factorials fixed.  They do not define a Bockstein, Yoneda product,
  cross-quotient comparison, or physical correction.  The remaining route
  must construct such a secondary chain operation before the two power
  layers are collapsed.
- Proof artifact: `notes/offdiagonal-same-power-target-residue-lock.md`.
- Checker:
  `computations/verify_offdiagonal_same_power_target_residue_lock.py`.
- Independent auditor: `/root/sol_ultra_audit_same_power_bockstein`;
  permanent report in
  `certification/audits/SUPERSESSION-2026-07-30-05.md`.
- Audit outcome/corrections: PATCHED/PASS.  The auditor corrected the
  lift-normalization and parameter-ring scope and replaced an overclaim
  that the adjacent-power identity already was a constructed Bockstein by
  the exact proved statement that it is a source syzygy of Bockstein shape.
- Certified commit: `bcb7ddf6bc17140fc37a8fc049b9cb9d2eba5fa0`.

## SUPERSESSION-2026-07-30-06

- Dependency ID: `INACTIVE-BOUNDARY`
- Replaces: the generic diagonal source-normalization and third-factor
  source-lifting limitations retained by `SUPERSESSION-2026-07-30-04` and
  Section 2 of `notes/consolidated-proof-frontier.md` at certification
  commit `7f5b53eb93174549c79c2f2fb4faa9462fdbd43b`.
- Replacement: `notes/diagonal-rees-saturation-cap-jet-bockstein.md` at
  commit `8d7b561fffc4c9b2725a45996c84ff613460cb86`.
- Scope delta: both generic normalized diagonal boundary jets have explicit
  division-free literal cap representatives, so their source
  representatives, normalizations, and physical-label transport are
  complete.  Removing a scalar third-boundary gcd lifts through a specified
  literal source quotient exactly when all discarded transverse principal
  parts lie in its boundary submodule; coordinate divisibility proves only
  membership in the evaluation kernel.  Thus the formerly vague lifting
  gap is the explicit relative Rees-saturation class `ker(epsilon)/N`, not
  an automatic division.  At `beta=0` the two ordinary jet rows collapse
  and miss the selected colour, whose target first occurs in transverse
  order `h`; after palette projection, vanishing of the two complementary
  odd classes constructs an allowed binary source and gives no minimality
  contradiction.  This does not prove the required principal-part
  memberships, adjacent-power target null-homotopy, collision unary-anchor
  transport, or an active clean point.
- Proof artifact: `notes/diagonal-rees-saturation-cap-jet-bockstein.md`.
- Checker:
  `computations/verify_diagonal_rees_saturation_cap_jet_bockstein.py`.
- Independent auditor: `/root/sol_ultra_audit_diagonal_rees`; permanent
  report in `certification/audits/SUPERSESSION-2026-07-30-06.md`.
- Audit outcome/corrections: PATCHED/PASS.  The auditor corrected the
  complementary-colour palette argument by functorial projection, restored
  a missing factor `h` in the unnormalized companion residue, sharpened the
  `tau=0` and family-relative saturation scopes, and expanded adversarial
  checks.
- Certified commit: `8d7b561fffc4c9b2725a45996c84ff613460cb86`.

## SUPERSESSION-2026-07-30-07

- Dependency ID: `INACTIVE-BOUNDARY`
- Replaces: the canonical diagonal trace-collision scope retained by
  `SUPERSESSION-2026-07-30-04`, `SUPERSESSION-2026-07-30-06`, and Section 2
  of `notes/consolidated-proof-frontier.md` at certification commit
  `2212893fa92e603142ea6db999a4689437c4b9dc`.
- Replacement: `notes/adaptive-diagonal-uncollision-cap-routing.md` at
  commit `e23e5c413124f77fa4b9c51d9755c01c7a60920b`.
- Scope delta: for a selected diagonal entry `alpha=a_aa!=0`, a literal
  direction `D` with `D_aa=0`, both complementary diagonal entries
  nonzero, and `gamma=<D,A_pq>!=0` exists exactly when
  `A_pq!=alpha E_aa`.  Its one-chart pencil has activity divisor
  `t u^2 (t+gamma u)`, two division-free literal cap jets with coefficient
  determinant `h gamma`, exhaustive bounded coefficient certificates, and
  visibility of every physical label.  Zeros of the ordinary matrix
  determinant are not additional activity boundaries.  Thus the canonical
  equation `trace(A_pq)=alpha` is not the intrinsic collision locus; the
  intrinsic one-chart locus is the scalar coordinate-unit block.  This
  does not prove relative source saturation, a target-cancelled
  adjacent-power comparison, transport of an arbitrary adaptive direction
  through the two-chart `AU-BF` overlap, relocation to another good chart,
  or an active clean point.
- Proof artifact: `notes/adaptive-diagonal-uncollision-cap-routing.md`.
- Checker:
  `computations/verify_adaptive_diagonal_uncollision_cap_routing.py`.
- Independent auditor: `/root/sol_ultra_audit_adaptive_diagonal`; permanent
  report in `certification/audits/SUPERSESSION-2026-07-30-07.md`.
- Audit outcome/corrections: PATCHED/PASS.  The auditor narrowed two
  global-selection claims to sufficient fixed-rectangle cases, restricted
  the displayed unresolved ledger to the two distinguished good charts,
  and made explicit that one-chart source legality does not supply
  source-faithful adaptive-direction transport through `AU-BF`.
- Certified commit: `e23e5c413124f77fa4b9c51d9755c01c7a60920b`.

## SUPERSESSION-2026-07-30-08

- Dependency ID: `INACTIVE-BOUNDARY`
- Replaces: the intrinsic scalar-coordinate-unit stopping point retained by
  `SUPERSESSION-2026-07-30-06`, `SUPERSESSION-2026-07-30-07`, and Section 2
  of `notes/consolidated-proof-frontier.md` at certification commit
  `be84db68454bf5da90b0e91e65e4cf738a59a87c`.
- Replacement:
  `notes/scalar-unit-full-normal-jet-unary-anchor-ledger.md` at commit
  `7f0a212c8cb4e4ec8c2502052c0b93f537e39c0d`.
- Scope delta: for the intrinsic block `A_pq=alpha E_aa`, the complete nine
  pair rows give the exact affine normal expansion
  `E(x E_aa+D)=x^h U_a+x^(h-1) R_D Theta_a+sum_(m>=2)
  x^(h-m) R_D^[m] G_a^[h-m]`.  Its first normal coefficient has the literal
  factorization `Theta_a=R_aa H_a` and
  `R_ij Theta_a=R_ia R_aj H_a`.  At a minimum-entry-support good pair,
  `(U_a,Theta_a)!=(0,0)`; in particular a clean unary cap forces
  `Theta_a!=0`.  Thus the intrinsic collision does not erase the first
  comparison datum: it moves it into adjacent-power two-step squares.
  This does not prove that a selected curvature rectangle detects that
  class, construct the required source-faithful four-cut/adjacent-power
  comparison, turn root avoidance into coefficient vanishing, give a clean
  point, or close the conjecture.
- Proof artifact:
  `notes/scalar-unit-full-normal-jet-unary-anchor-ledger.md`.
- Checker:
  `computations/verify_scalar_unit_full_normal_jet_unary_anchor_ledger.py`.
- Independent auditor: `/root/sol_ultra_audit_scalar_normal_jet`; permanent
  report in `certification/audits/SUPERSESSION-2026-07-30-08.md`.
- Audit outcome/corrections: PATCHED/PASS.  The auditor rederived every
  divided-power coefficient and Segre square, checked the minimum-support
  row deletion after arbitrary cancellation, restored stripped TeX
  delimiters, clarified the root-avoidance and source-level scope, and
  memoized the checker without weakening its tests.
- Certified commit: `7f0a212c8cb4e4ec8c2502052c0b93f537e39c0d`.

## SUPERSESSION-2026-08-01-01

- Dependency ID: `SP-K6`
- Replaces: `proofs/six-site-arbitrary-complex-obstruction.md` and the
  supporting `notes/slice-cover.md` at baseline commit
  `835ed0db2ba1111cffad2ce7b3a231ce081c3178`, specifically (i) the
  section 5.1 claim that the `C_3 \sqcup C_3` support relaxation is UNSAT,
  which left zero internal matrices to an off-file exclusion; (ii) the
  proof of the one-slice covering lemma's three-term step, which routed
  through a classification of decomposable dependences that the first
  audit judged insufficient; and (iii) the section 2 reduction of a
  palette-`q >= 3` monochromatic graph to `Delta_{6,3}`, which silently
  assumed equal amplitudes.
- Replacement: the same two files at commit
  `4a51019` (`Remediate the eight audit defects in SP-K6, and strengthen
  two steps`).
- Scope delta: **the statement of Theorem 1.1 is unchanged.**  This is a
  proof replacement and a strengthening, not a new positive result.  (i)
  the SAT encoding now refutes the *zero-or-rank-at-least-two* relaxation
  directly, so no separate zero-chord or torus-zero exclusion is needed;
  (ii) the three-term step is now proved by evaluation at explicitly
  constructed points, using only that the three coordinate restrictions at
  a mode span a space of dimension at least two, and that a vector space is
  never the union of *two* proper subspaces -- both field-independent, so
  the statement now holds over any field and the finite-field search is a
  genuine adversarial test rather than corroboration; the activity clause
  `C_pj != 0` is retained unchanged.  (iii) the amplitude reduction now
  carries an explicit invertible diagonal.  This supersession does **not**
  establish any new case of the conjecture, does not touch
  `SP-CLEAN-BRIDGE`, and does not alter any consumer of `SP-K6`.
  Newly recorded scope: the activity clause is *not* used inside `SP-K6`,
  whose section 3 needs only `d_R(v) >= 3`; it is retained because
  `proofs/prism-plus-one-edge-obstruction.md` consumes it.
- Proof artifact: `proofs/six-site-arbitrary-complex-obstruction.md`,
  `notes/slice-cover.md`.
- Checker: `computations/verify_slice_cover_three_term_step.py` (new),
  `computations/verify_saturated_rank_graph_obstruction.py`,
  `computations/certify_low_rank_graph_laurent.py`.
- Independent auditor: a fresh agent that read only the artifacts and
  attempted refutation; it rebuilt the `C_3 \sqcup C_3` orbit reduction
  from the definitions, confirmed the 56 empty clauses arise only from
  constant colourings with no basis-compatible perfect matching, and
  confirmed all 134 stripped formulas are UNSAT under a third independent
  solver *without* those clauses, so the refutation never rested on them.
- Audit outcome/corrections: **PASS on every defect; no unsound repair and
  no weakened statement found.**  Corrections required and applied: the
  proof said one case used translated trinomials where the shipped
  certificate has records in three (`P3+3P1`, `P2+4P1`, `6P1`, checked
  against the JSON); four unterminated display-math blocks; and the new
  checker tests the three-term *step*, not the covering lemma, finding no
  identities at all at `m = 2`, so only its second search exercises the
  sharp case.
- Certified commit: `4a51019`.

## SUPERSESSION-2026-08-01-02

- Dependency ID: `LOCAL-INVERTIBLE`
- Replaces: the recorded SHA-256
  `4be6c2add51e8da4c144f0332f6ad7b1cc2f3dadaf7b49629d08d56dd0227c8d`
  for `computations/verify_invertible_complete_anchor_one_hole_filtered_descent.py`
  in `certification/audits/SUPERSESSION-2026-07-30-01.md`.
- Replacement: the same checker at commit `6e622d9`, SHA-256
  `6089e2b9a3105ebf1df499641727690ceba7ac02f1d476188b59bba53d1219c7`.
- Scope delta: **no mathematical claim changes.**  The checker's 21 bare
  `assert` statements became a `require()` that raises, and its
  `if not __debug__: raise` guard was removed.  The recorded audit's phrase
  "failed closed under `python3 -O`" described that guard and was accurate;
  the checker now *runs* under `-O` and performs every check there, which
  is strictly stronger.  Mutation-tested: six injected failures, all caught
  under both `python3` and `python3 -O`.  15 of the 16 SHA-256 values
  recorded in `certification/` still match; this is the only one that does
  not.
- Proof artifact: unchanged --
  `notes/invertible-complete-anchor-one-hole-filtered-descent.md`.
- Checker: `computations/verify_invertible_complete_anchor_one_hole_filtered_descent.py`.
- Independent auditor: a fresh agent auditing the corpus-wide
  `assert` -> `require()` conversion; it found this hash break, verified the
  other fifteen still match, and confirmed no `certification/`-cited
  checker was ever `-O`-unsafe.
- Audit outcome/corrections: PASS; the auditor's stated reason for
  withholding a commit recommendation on the unsplit tree was precisely
  that this hash change had no ledger entry.  This record is that entry.
- Certified commit: `6e622d9`.

## SUPERSESSION-2026-08-01-03

- Dependency ID: `SP-K6`
- Replaces: the `SP-K6` proof artifacts at baseline commit
  `835ed0db2ba1111cffad2ce7b3a231ce081c3178`, and procedurally supersedes
  the incomplete record `SUPERSESSION-2026-08-01-01` without deleting it from
  this append-only ledger.
- Replacement: the repaired proof and checker suite at exact commit
  `4a510193d97fd84cc819912231504711281dbbab`.
- Scope delta: **Theorem 1.1 is unchanged.**  The replacement (i) includes
  zero blocks in the `C_3 \sqcup C_3` zero-or-rank-at-least-two relaxation;
  (ii) replaces the slice-cover three-term argument with a field-independent
  evaluation proof while retaining its activity clause; (iii) inserts the
  missing invertible diagonal normalization for unequal nonzero amplitudes;
  (iv) repairs the four-edge minor proof by comparing nonzero products before
  cancelling `K^2`; (v) makes the low-rank semantic replay and saturated
  checks live under `python3 -O`; and (vi) corrects the certificate census,
  optional DRUP reproduction, display delimiters, checker scope, and consumer
  documentation.  It proves no new case beyond the already certified six-site
  obstruction and does not touch `SP-CLEAN-BRIDGE`.
- Proof artifact: `proofs/six-site-arbitrary-complex-obstruction.md`,
  `proofs/saturated-rank-graph-obstruction.md`,
  `proofs/four-edge-rank-graph-obstruction.md`,
  `proofs/exceptional-triangle-obstruction.md`, and `notes/slice-cover.md`,
  with consumer/reproducibility updates in
  `notes/final-resolution-foundations-draft.md` and `notes/route-registry.md`.
- Checker: `computations/certify_low_rank_graph_laurent.py`,
  `computations/verify_saturated_rank_graph_obstruction.py`, and
  `computations/verify_slice_cover_three_term_step.py` at the exact hashes in
  `certification/audits/SUPERSESSION-2026-08-01-03.md`.
- Independent auditor: `/root/terminal_math_certification_audit`, corroborated
  by Claude subagent `agent-aed5ba1e4665adb1d`; permanent report in
  `certification/audits/SUPERSESSION-2026-08-01-03.md`.
- Audit outcome/corrections: **PASS with procedural corrections; no
  mathematical correction or weakened statement.**  The prior entry omitted
  the permanent auditor identity/report, exact commit identifier, several
  load-bearing artifacts and scope changes, and the required consolidated
  spine update.  This entry and its linked report supply them.
- Certified commit: `4a510193d97fd84cc819912231504711281dbbab`.

## SUPERSESSION-2026-08-01-04

- Dependency ID: `LOCAL-INVERTIBLE`
- Replaces: the checker hash recorded in
  `certification/audits/SUPERSESSION-2026-07-30-01.md`, and procedurally
  supersedes incomplete record `SUPERSESSION-2026-08-01-02` without deleting
  it from this append-only ledger.
- Replacement: the same checker at exact commit
  `6e622d9a9572524246d7714ef7ddcb6c4742d7bf`, SHA-256
  `6089e2b9a3105ebf1df499641727690ceba7ac02f1d476188b59bba53d1219c7`.
- Scope delta: **no mathematical claim changes.**  Twenty-one bare assertions
  become raising checks and the optimized-mode guard is removed, so every
  verification step now executes under `python3 -O`.
- Proof artifact: unchanged --
  `notes/invertible-complete-anchor-one-hole-filtered-descent.md`.
- Checker:
  `computations/verify_invertible_complete_anchor_one_hole_filtered_descent.py`.
- Independent auditor: `/root/terminal_math_certification_audit`, corroborated
  by Claude subagent `agent-affa1534932acdab4`; permanent report in
  `certification/audits/SUPERSESSION-2026-08-01-04.md`.
- Audit outcome/corrections: **PASS; no mathematical correction.**  Normal,
  optimized, and isolated standard-library modes agree, and a substantive
  mutation fails in normal and optimized modes.  The prior entry omitted the
  permanent auditor identity/report, exact commit identifier, and the required
  consolidated-spine update; this entry supplies them.
- Certified commit: `6e622d9a9572524246d7714ef7ddcb6c4742d7bf`.

## SUPERSESSION-2026-08-15-01

- Superseded: the Step-5 paragraph (lines 56-58) of
  `proofs/odd-near-perfect-gadget-obstruction.md` as a proof step.
  The file itself remains byte-frozen (pin-target discipline); this
  entry redirects the step.
- Replacement: Step 5 is carried by `notes/finite-obstruction.md` §7
  (adjacent-residue-class descent) or equivalently
  `notes/termwise-rank3-cubic-uniqueness.md` §3.5 (B3)
  (minimal-arc argument, no descent). Correction note:
  `notes/2026-08-15-step5-defect-and-repair.md`.
- Scope delta: **no mathematical claim changes** — the theorem and
  all downstream uses stand on the replacement proofs; only the one
  paragraph's argument is withdrawn.
- Independent auditor: hygiene agent H1 (Claude subagent, session
  f8396279); permanent report in
  `certification/audits/SUPERSESSION-2026-08-15-01.md`.
- Audit outcome/corrections: theorem PASS (two sound committed
  proofs re-verified; residual case re-verified exhaustively to
  N = 20); paragraph FAIL with explicit counterexamples to its
  descent step.

---

# Record — the eight-site block-diagonal obstruction (SUPERSESSION-2026-08-20-01)

## What kind of record this is

**This is an ADDITION of new spine, not a correction of certified material.**
Nothing in the certified spine is being replaced or narrowed. The ledger's
preamble admits records that "add to the spine", and the drafting convention
established by
`computations/unaudited-promotion-drafts-2026-08-15/draft_supersessions_entry.md`
is followed: since no *certified* statement is superseded, the **Replaces**
line names the unaudited probe-lane phrasing that this record corrects — which
is the honest content, because in two places the promoted statement is a
correction of the probe's.

The ledger's standing rule is preserved and restated inside the record: this is
**not a positive closure of any part of the Krenn–Gu conjecture**. It removes
the block-diagonal stratum at the smallest open order and leaves the general
bicoloured case `n = 8, d = 3` open.

## Coordinator decisions — all three settled (2026-08-20)

1. **Dependency ID: `N8-DIAGONAL`, RATIFIED.** The coordinator ratified a new
   ID rather than attaching this to `SP-K6`, on the grounds that `SP-K6` names
   the six-site *general bicoloured* theorem whereas this is the eight-site
   *block-diagonal* one — clean layering. `N8-DIAGONAL` is introduced by this
   record and is the only ID ratified in this round; the six IDs proposed in
   `draft_supersessions_entry.md` remain unratified.
2. **Target path: `proofs/eight-site-diagonal-obstruction.md`.** Settled as
   staged. A later rename would need its own supersession (§H0b), so if the
   coordinator wants a different name, it must change *before* this record is
   appended.
3. **Permanent audit report: drafted.** Staged at
   `computations/unaudited-promotion-diag-2026-08-20/audit_SUPERSESSION-2026-08-20-01.md`,
   to be moved to `certification/audits/SUPERSESSION-2026-08-20-01.md` at
   commit time. It preserves A9's verdict and trace; the underlying material is
   the manager transcription at
   `computations/unaudited-audit-a9-2026-08-20/REPORT.md` (whose own header
   says "Transcribed by the manager from A9's final message (agent writes
   outside this dir are blocked)") plus the lane's 12 result checkpoints, and
   this lane's independent replay and checker runs.

---

## SUPERSESSION-2026-08-20-01

- Dependency ID: `N8-DIAGONAL` (new; introduced by this record and **ratified
  by the coordinator on 2026-08-20**, `certification/BASELINE.md` covering no
  part of the `N = 8` diagonal layer).
- Replaces: **nothing in the certified spine.** This record *adds* spine. It
  supersedes the following unaudited probe-lane phrasings:
  1. the standing status of the diagonal case as recorded in
     `notes/2026-08-15-resolution-master-plan.md` v44 addendum item 3 — "**The
     diagonal case of N=8 is now one computation from being a theorem.** ...
     the remaining object is T1h — the three-colour free-site ideal (96
     generators, 66 variables, timed out once). **If T1h terminates unit, "no
     diagonal exact source at N=8" is a theorem including cancellation**" —
     which is superseded twice over: T1h's ideal is **not** unit (W29-A1,
     explicit 21-parameter rational family, `results_a9_08_t1h_gb.json`:
     `points 40`, `nonzero_generators 0`, `n_generators 96`), and the theorem
     was obtained by a different route;
  2. audit A8's framing, quoted and already superseded by the manager in
     `computations/unaudited-audit-a8-2026-08-19/REPORT-FINAL.md`: "A8's
     framing 'T1h in char 0 is the one computation that would commit the
     diagonal chain' is superseded";
  3. **[correction]** the theorem lane's own uniformity claim in
     `computations/unaudited-diagclose-w29-2026-08-19/REPORT.md` headline item
     3 — "**Uniform in even N**; N=10 k=4 in flight (k=3 calibration 386/386
     SAT), N=12 queued" — repeated in
     `notes/2026-08-15-resolution-master-plan.md` v47 item 1 as "**Uniform in
     even N**: N=10 in flight (calibration passed), N=12 queued — the diagonal
     statement is closing beyond the open order, not just at it." **This claim
     is REFUTED and is withdrawn by this record**; see the scope delta;
  4. **[correction]** the control phrasing in the same report — "1,200 site
     checks on 150 real X_3 sources + the canonical one, 0 violations" — which
     is true but is a *single-case* control: all 1,200 checks land in the one
     orbit `R = (Q,Q,Q)`
     (`computations/unaudited-diagclose-w29-2026-08-19/results_g2_x3mass.json`,
     `cases_seen`). Superseded by the 37-case replacement below.
- Replacement: `proofs/eight-site-diagonal-obstruction.md` (drafted as
  `computations/unaudited-promotion-diag-2026-08-20/proof_eight-site-diagonal-obstruction.md`)
  at commit *TBD*.
- Scope delta: **adds one theorem with one corollary, and withdraws one
  uniformity claim.**

  **Theorem (eight-site block-diagonal obstruction).** Over **any field, of any
  characteristic**, there is no block-diagonal ternary weighting
  `A_uv = diag(t^0_uv, t^1_uv, t^2_uv)` of `K_8` whose perfect-matching
  amplitudes satisfy: all three constant-word amplitudes nonzero, and every
  mixed-word amplitude zero. In particular no *unnormalised* GHZ tensor
  `sum_c lambda_c e_c^{⊗8}` with all `lambda_c != 0` is reachable in the
  block-diagonal model. Hypotheses used: only that the coefficient ring has no
  zero divisors and `1 != 0` — so the statement holds verbatim over any
  integral domain. **No algebraic closure, no root extraction, and no
  normalisation of the amplitudes are used.**

  **Corollary.** The classical *edge-coloured* (single-cell) Krenn–Gu statement
  at `N = 8` follows, as the specialisation in which at most one of
  `t^0_uv, t^1_uv, t^2_uv` is nonzero per pair.

  **Scope limits recorded in the document, and load-bearing:**
  * *Block-diagonal only; the registry item is NOT resolved.* The general
    bicoloured case `n = 8, d = 3` — arbitrary `3 x 3` matrices `A_uv` — is
    **untouched and remains open**, and it is what the `formal-conjectures`
    registry item `eqSystem8_no_solution_d3` states: verified against the Lean
    source (`google-deepmind/formal-conjectures`,
    `FormalConjectures/Paper/MonochromaticQuantumGraph.lean`), its edge type
    `EdgeN` carries *both* endpoint colour indices `i j : Fin D` and the
    matching sum evaluates `W (mkEdge v u (ι v) (ι u))`, with constant words
    normalised by `pmSum = 1`. This theorem is that item's **diagonal
    sub-case** (weights supported on `i = j`, the classical monochromatic-edge
    model of Krenn 2017), at the same smallest open order. The product
    factorisation `Phi(w) = prod_c haf(t^c | w^{-1}(c))` is exactly what
    diagonality buys and exactly what a general `A_uv` destroys, so the proof
    does not transfer. One direction of the comparison is favourable: the
    registry normalises constant amplitudes to `1` while this record assumes
    only that they are nonzero, so on the diagonal sub-case this covers the
    registry's normalisation *a fortiori*.
  * *Formalisation, recorded as future work and not as a claim.* The shipped
    certificates would support a Lean pull request adding a **proved diagonal
    variant** statement to that registry file, in its own idiom — the file
    already carries variant statements beside the headline one (for example
    `eqSystem8_no_solution_d3_trinary_int`), so a diagonal variant would be an
    addition in the established style and not a change to the open problem. No
    Lean development exists in this repository.
  * *Orders.* `N = 6` closes by the same machine (with independent Gröbner
    corroboration) and `N = 4` correctly does **not** close (the exceptional
    source is satisfiable, and its case ideal has `dim 3`). **`N >= 10` is
    open for this machine, and the earlier "uniform in even N" claim is
    refuted**: at `N = 10` the exact level is `X_6`, not `X_4` (the even
    profile `(4,4,2)` has off-count 6), so an `N = 10` run at `k = 4` decides a
    strict relaxation and is mostly satisfiable (`35` of `42` sampled orbits
    SAT); and at the true level `k = 6` the abstraction is **still** satisfiable
    on sampled orbits (`2` of `7`). `N = 12` was never run.
  * *Method.* The `N = 8` verdict is SAT-based, with machine-checked UNSAT
    certificates; its algebraic (Gröbner) corroboration exists at `N = 4` and
    `N = 6` only — the single `N = 8` case ideal attempted timed out at 3000 s
    and carries no information. The minimal unsatisfiable cores (361 constraint
    groups / 1,226 clauses in the singleton case; 857 clauses in the maximal
    case) are the target for a hand proof; **no hand proof exists**.
  * *Not a closure.* Per the ledger's standing rule, this record is **not a
    positive closure of any part of the Krenn–Gu conjecture**; it is a negative
    guard removing one stratum at the smallest open order.
- Proof artifact: `proofs/eight-site-diagonal-obstruction.md`.
- Checker: `computations/verify_eight_site_diagonal_obstruction.py` (staged at
  `computations/unaudited-promotion-diag-2026-08-20/verify_eight_site_diagonal_obstruction.py`;
  SHA-256 to be frozen into the proof document at the certifying commit).
  Standard library only, no import from any `computations/unaudited-*`
  directory, house-style raising `require()` and no bare `assert`. It
  re-derives the case ledger by two independent routes, re-derives
  `EXACT = X_4` from the raw `3^8` word enumeration, **rebuilds all 87 orbit
  CNFs and requires every SHA-256 to match the shipped digest**, audits each
  formula structurally, and checks the shipped proofs are present with matching
  digests — all mandatory. Third-party proof replay through `drat-trim` is
  optional-but-loud: it runs when the binary is found (`DRAT_TRIM` environment
  variable) and prints a labelled SKIPPED line otherwise, because `drat-trim`
  is third-party and is not vendored here; `--proofs` makes it mandatory. Run
  record at the certifying HEAD:
  `computations/unaudited-promotion-diag-2026-08-20/checker_run_log.txt`
  (passes under `python3`, `python3 -O` and `python3 -I -S`; `87/87` proofs
  `s VERIFIED` when drat-trim is supplied; and a negative control in which
  `--proofs` with an unusable binary correctly FAILS). The replay material —
  an independent encoder, the case ledger with two orbit-count routes, a
  single-entry `replay.sh`, the 87 CNF/DRAT pairs and a `SHA256SUMS.txt` over
  every shipped artifact — is
  `computations/unaudited-promotion-diag-2026-08-20/certified_package/`.
  External tools, exact builds: CaDiCaL
  `computations/unaudited-hygiene-h1-2026-08-15/tools/cadical/build/cadical`
  (`--version` -> `3.0.1`) and drat-trim
  `computations/unaudited-hygiene-h1-2026-08-15/tools/drat-trim/drat-trim`
  (invoked `drat-trim CNF DRAT -f`, required to print `s VERIFIED`).
- Independent auditor: **A9** (Claude subagent, lane
  `computations/unaudited-audit-a9-2026-08-20/`, pinned HEAD `10eeae2`,
  auditing the theorem lane W29 at pinned HEAD `0016ec5`) — an agent other than
  the author of the result. Corroborated upstream on the shared chain by **A8**
  (`computations/unaudited-audit-a8-2026-08-19/`, pinned HEAD `0016ec56`).
  Permanent report **drafted** at
  `computations/unaudited-promotion-diag-2026-08-20/audit_SUPERSESSION-2026-08-20-01.md`,
  for `certification/audits/SUPERSESSION-2026-08-20-01.md`; its source material
  is the manager transcription at
  `computations/unaudited-audit-a9-2026-08-20/REPORT.md`, the lane's 12 result
  checkpoints and 12 run scripts, and this lane's independent replay and
  checker runs.
- Audit outcome/corrections: **CONFIRMED — and slightly stronger than stated;
  committable as spine.** A9 re-derived every clause validity by hand from
  field facts alone, re-encoded the system with an inverted polarity and its own
  variable layout (clause-set identical to the theorem lane's on four spanning
  cases, `0` clauses on either side alone; verdicts agree on all 87 orbits),
  re-solved with five engines (all `0/87` SAT), and drat-trim-verified `87/87`
  at `N = 8` plus `64/64` at `N = 6`, with truncated, corrupted and cross-case
  proofs all **rejected**. **Nothing in the proof chain required repair.**
  Three write-up corrections were required and are incorporated in the promoted
  document:
  1. the uniform-in-`N` / `N = 10` / `N = 12` claims are struck (see the scope
     delta);
  2. the "1,200 site checks on 150 real X_3 sources" control is qualified as
     single-case, and the replacement is cited — `40` objects, `320` site
     checks across **37 distinct cases**, `0` violations
     (`computations/unaudited-audit-a9-2026-08-20/results_a9_04_controls.json`,
     key `p3`);
  3. the scope is stated as **block-diagonal** (with the classical
     edge-coloured statement as a corollary), and the **amplitude-nonzero
     strengthening** is stated as the theorem, since the machine never uses
     `haf(t^c|V) = 1`, only `!= 0`.

  One further correction is recorded inside the audit lane and carried into the
  document rather than hidden: A9's first mutation battery
  (`results_a9_04_controls.json`, key `p5`) reported `PASS: false` — two of its
  five mutants were silent, because the detector was mispaired with the
  mutation and the probe objects all lay in one case. A9 rebuilt the battery
  (`results_a9_05_mut.json`, `MU0`–`MU7`, all firing, `PASS: true`) rather than
  reporting the original as a pass.
- Certified commit: *TBD*.

---

## Consolidated-spine follow-up required by the ledger preamble

"After appending an accepted record, update the current consolidated spine in
the same commit or in a directly linked follow-up commit." The staged patches
for that update are:

* `computations/unaudited-promotion-diag-2026-08-20/readme_patch.md` — the
  `README.md` status line and the *Established core* bullet list;
* `computations/unaudited-promotion-diag-2026-08-20/proofsketch_patch.md` —
  `PROOF-SKETCH.md` §1 (the known-partial-results paragraph), §7.1 (the
  support-theoretic reduction), and the open-item table.
