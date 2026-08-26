# Wording and scope fixes for the notes maintainers

**UNAUDITED. Pinned HEAD `7d57c552a3ef57d3a95c3bc933af547ad55e087d`.**
Source: the wording/scope section of
`computations/unaudited-external-spine-audit-2026-08-13/REPORT.md`.

Six items. Each gives the sentence as committed, the exact file and line
where it lives at the pinned HEAD, the correction, and how the correction is
substantiated. **None of these is a mathematical error** — every underlying
computation the auditors recomputed came out true. They are overstatements,
dropped qualifiers, and one impossible group-theoretic assertion.

---

## 1. The 270 are **two** orbits, not one

**As committed**

- `notes/2026-08-11-proof-first-primary-theorems.md:374` —
  "The final `270` form one double-coloop orbit"
- `notes/2026-08-11-proof-remainder-difficulty-map.md:198` —
  "The final `270` are exactly one double-coloop orbit"

**Correction.** The 270 residual ordered packets are **two** orbits of the
internal relabelling group `S6`: one of size **90** (the diagonal packets,
`matching1 = matching2`, identical two-edge tails) and one of size **180**
(tails one `C4` apart).

**Substantiation.** A single orbit of size 270 is impossible before any
computation: orbit sizes divide `|S6| = 720`, and `720 / 270` is not an
integer. `verify_double_coloop_interference_coefficients.py` in this
directory computes the orbit decomposition by union-find over the generators
`(0 1)` and `(0 1 2 3 4 5)`, gets exactly two orbits of sizes 90 and 180,
and verifies that the tail shape is constant on each. The committed checkers
already record the 90/180 split as `residual_shapes` — the prose simply did
not follow them.

**Suggested replacement text.** "The final `270` form two double-coloop
orbits, of sizes 90 and 180; the common-`S` hybrid row forces …"

---

## 2. `2,126,208` counts (chart, triple) **pairs**

**As committed**

- `notes/h3-c6-e14-three-cell-top-degree-boundary.md:6` —
  "All **2,126,208** unordered triples have a literal ordinary two-row
  source unit"
- `notes/2026-08-11-proof-remainder-difficulty-map.md:72`,
  `notes/2026-08-11-proof-first-primary-theorems.md:96`,
  `notes/2026-08-11-careful-global-proof-sketch.md:215`,
  `notes/consolidated-proof-frontier.md:58` — all restate the figure with
  the "on any of the nine charts" qualifier dropped.

**Correction.** `2,126,208` is the number of **(chart, triple) pairs** over
the nine canonical minimal `E14` charts, not the number of triples. The
audit reports **260,118** distinct triples. Every restatement must carry the
"across the nine canonical minimal `E14` charts" qualifier, because without
it the sentence reads as a statement about a single chart.

**Substantiation.** The audit computed both figures; this repair pass did
**not** recompute them (it would require the full `E14` chart machinery).
Re-derive `260,118` before writing it into a note; the qualifier itself is
independent of that number and should go in either way. Note also that
`2,126,208 / 9` is not an integer, so the figure cannot be a per-chart
count.

**Suggested replacement text.** "Across the nine canonical minimal `E14`
charts, all **2,126,208** (chart, triple) pairs — **260,118** distinct
triples — have a literal ordinary two-row source unit."

---

## 3. Three-cell emptiness is not "the last local monomial degree"

**As committed**

- `notes/2026-08-11-proof-remainder-difficulty-map.md:72` —
  "The last local monomial degree is empty: all `2,126,208` three-cell
  specializations are ordinary source units."
- `notes/2026-08-11-careful-global-proof-sketch.md:215` —
  "The three-cell top degree is now empty too."

**Correction.** The **three-cell** layer is empty. The four-cell layer is
not: the audit reports **264 four-cell survivors on chart `(1,3)`**. Calling
three cells "the last local monomial degree" invites the reading that the
local search is finished, which it is not.

**Substantiation.** The audit's figure; again **not** recomputed in this
repair pass, and the maintainer should re-derive the 264 before quoting it.
The wording fix does not depend on the exact number — it depends only on the
existence of four-cell survivors, which the audit asserts and which the
committed notes nowhere deny.

**Suggested replacement text.** "The three-cell layer is empty: all
`2,126,208` (chart, triple) pairs are ordinary source units. This exhausts
the local monomial *types* used by the complete response and unary
coefficients; it is not an emptiness statement at four cells, where chart
`(1,3)` still carries survivors."

---

## 4. "There is no unclosed linear branch" — scope to the 25-row model

**As committed**

- `notes/h3-cut-swap-shared-repair-anchor-fibre-dichotomy.md:37` —
  "With the already physical Cartan column adjoined, the anchor-dark
  bordered theorem refines this second outcome to a target-dark separator,
  an external-cokernel separator, or a unit-Cartan kernel. **There is no
  unclosed linear branch.**"

**Correction.** The statement is true **of the 25-row generous cone that the
checker builds**, and only of it. Nothing in that file connects the 25-row
model to the physical 8,868-column matrix, and the generous cone is sound
only in the *excluding* direction (it must contain `x_v`; generosity cannot
be used to construct anything).

**Substantiation.** The auditors rebuilt the 25-row linear algebra
independently (rank exactly 24, one-dimensional cokernel `nu`, all four
repair directions) and confirmed it — and confirmed that no computation
anywhere links it to the physical matrix.

**Suggested replacement text.** "…or a unit-Cartan kernel. On the 25-row
generous cone there is no unclosed linear branch; whether the physical
8,868-column matrix inherits this is not established here."

---

## 5. Determinant-bright: **entry** is exhaustive, **landing** is not

**As committed**

- `notes/2026-08-12-two-gate-resolution-sketch.md:41` —
  "A determinant-bright zero mixed row has a nonzero offdiagonal cell, hence
  a source-provenant private-site fan."  (Accurate — this is entry.)
- `notes/2026-08-12-interference-cartan-proof-map.md:432` —
  "**In parallel, normalize and land the active-fan coloop.** Every
  determinant-bright zero mixed row now yields an active fan…"
- `notes/2026-08-12-interference-cartan-proof-map.md:516` — lists "physical
  landing of every determinant-bright zero mixed row on an offdiagonal
  private-site fan" among the achieved items.

**Correction.** *Entry* is proved exhaustively: all `3^15` patterns,
`2,669,328` determinant-bright rows, **zero** of them lacking a nonzero
off-diagonal cell — the auditors reproduced this. *Landing* is not: the fan
construction and the four-good links are unverified, and one pinned module
in that chain is never loaded. The two must not share a sentence.

**Substantiation.** Audit "verified TRUE by independent re-derivation"
(entry) versus audit wording/scope list (landing).

**Suggested replacement text.** "Determinant-bright **entry** is exhaustive
(`1ec750e`): across all `3^15` patterns, every one of the `2,669,328`
determinant-bright zero mixed rows has a nonzero off-diagonal cell. Physical
**landing** of those rows on an off-diagonal private-site fan remains open:
the fan and four-good links are not yet verified."

---

## 6. "Every new typed hole strictly enlarges the closure" is inflationarity

**As committed**

- `computations/verify_h3_active_fan_coloop_complete_row_pivot.py`,
  `audit_six_closed_concepts` — the check
  `require(len(closure(side | {hole})) > len(side), "a new typed hole failed
  to enlarge a closed shore")`, echoed in the surrounding prose as a
  termination-flavoured statement.

**Correction.** For a Galois closure operator, `X ⊆ cl(X)` and `X` closed
give `cl(X ∪ {h}) ⊇ X ∪ {h} ⊋ X` whenever `h ∉ X`. Strict growth is
therefore automatic — it is inflationarity, not a termination result.
Termination follows separately from `|E(K6)| = 15` being finite.

**Substantiation.** `verify_six_concept_pivot_applicability.py` in this
directory keeps the growth check (it is cheap and true) but no longer
presents it as content; the substantive per-concept statement it verifies is
that the *same* pivot identity `alpha U_i - d_i V_i = alpha` applies at
every one of the 30 oriented holes, in both target channels, on an honest
complete-row model.

**Suggested replacement text.** "A hole outside the shore enlarges the
Galois closure — automatically, since the closure is inflationary and the
shore is closed — so the process terminates after at most 15 steps. The
content is not the growth but that one source identity serves every concept."

---

## Two related corrections the audit made in passing

These are already correct in the checkers and only need the notes to catch
up.

- The **446** non-degenerate Galois-closed concepts on `K6` are `448 − 2`
  (drop the empty family and the complete graph). They fall into **9**
  `S6`-orbits, which the blocker duality `F ↔ T(F)` pairs into the **six**
  concept types the notes call "the six closed symmetry types": three
  self-dual orbits (triangle 3|3, path 3|3, star 5|5) and three dual pairs
  (1|9, 2|4, 2|6). Verified in
  `verify_six_concept_pivot_applicability.py`.
- The endpoint involution is pinned only **up to the invariance group**.
  `Aut` of the direct-free presentation is `Stab_{S8}({3,6}) ≅ S6 × S2`
  (order 1440); intersecting with the tail-pair condition leaves **eight**
  admissible transpositions, `0↔1`, `0↔4`, `0↔7`, `1↔4`, `1↔7`, `2↔5`,
  `3↔6`, `4↔7`. Prose that says "s **is** the residual-site transposition
  `0 ↔ 1`" should say "take `s` to be", since nothing in the chain forces
  that choice. Verified in `verify_involution_pinned.py`.
