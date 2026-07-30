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
