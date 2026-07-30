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
