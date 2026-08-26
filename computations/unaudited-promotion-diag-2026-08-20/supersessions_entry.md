# Proposed `certification/SUPERSESSIONS.md` record — the eight-site block-diagonal obstruction

> **STAGED — not appended.** Drafted 2026-08-20 by lane P2-diag at pinned
> repository HEAD `5377acdc43992e8eaaf4f17f4f1068b7242dfe73`. This block is in
> the record format of `certification/SUPERSESSIONS.md` and is to be appended
> **only** once the proof document is committed under `proofs/`, the checker
> obligations of `checklist_run.md` are discharged, and the permanent audit
> report is written.

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
