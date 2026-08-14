# Claim index for PROOF-SKETCH.md

**What this note is.** A claim-by-claim map from every labelled statement in
[`PROOF-SKETCH.md`](../PROOF-SKETCH.md) to its best backing artifact — the
prose note or proof page that actually proves it, and the exact checker that
certifies it — together with an assessment of whether that backing page is
ready to be read by someone outside this repository.

This is a routing and editorial index. It makes no new mathematical claim,
and it does not re-audit anything: where it disagrees with a label in the
sketch, it says so and names the artifact the disagreement comes from.

Synchronized against `PROOF-SKETCH.md` as of **2026-08-13 19:48**. The
sketch was renumbered that afternoon (Theorem A/B became Theorems 3.1/3.2,
and the open statement became Conjecture 6.2); this index uses the new
numbering.

## How to read the readiness column

| verdict | meaning |
|---|---|
| **READY** | Self-contained statement, terms defined, LaTeX that renders on GitHub. A stranger can read it. |
| **NEEDS-POLISH** | Mathematically sound, but written agent-to-agent: telegraphic prose, undefined internal jargon, commit hashes used as citations, ASCII math in backticks, or `\[ … \]` / `\( … \)` delimiters that GitHub silently drops. |
| **MISSING** | No single authoritative page. The content exists but is scattered, or the page that states it is titled for something else. |

Two mechanical notes that drive many of the verdicts:

* **Delimiter split.** `proofs/*.md` and the two polished §6 notes use
  `$…$` / `$$…$$`, which GitHub renders. **1,822 of the 2,050 notes** use
  `\[ … \]` or `\( … \)`, which GitHub does **not** render — the math
  disappears into literal backslashes. Any page promoted out of `notes/`
  needs a delimiter pass.
* **Naming convention.** `notes/some-name.md` pairs with
  `computations/verify_some_name.py`. Checkers below are given in full
  where the convention is broken or where the checker lives elsewhere.

## 1. Introduction

| claim | label | best backing | checker | readiness |
|---|---|---|---|---|
| **Prop. 1.1** (colour reduction) — a solution for any `d ≥ 3` restricts to a ternary one | **[P]** | [`final-resolution-foundations-draft.md`](final-resolution-foundations-draft.md) §2.4, **Lemma 2.7** (coordinate projection is exact); also [`clean-pair-cap-exact-descent-target.md`](clean-pair-cap-exact-descent-target.md) §5 and [`proofs/six-site-arbitrary-complex-obstruction.md`](../proofs/six-site-arbitrary-complex-obstruction.md) §2 | `verify_colour_projection_monotonicity.py`; Lean: `restrictColors` / `eqSystemN_restrictColors` in [`formal/MonochromaticQuantumGraphKeyLemmas.lean`](../formal/MonochromaticQuantumGraphKeyLemmas.lean) (ledger id **A7**, status **F**) | **READY** |

This is the best-supported claim in the sketch — the only one that is both
machine-formalized and stated in publication register.
[`final-resolution-foundations-draft.md`](final-resolution-foundations-draft.md)
is a 1,227-line paper-style manuscript covering orders 2, 4 and 6, and is
the single best source anywhere in the repository for lifting material into
a preprint. Note the convention break: the checker
`verify_colour_projection_monotonicity.py` has no matching
`notes/colour-projection-monotonicity.md`.

## 2. Interference, gauge freedom, and sign obstructions

| claim | label | best backing | checker | readiness |
|---|---|---|---|---|
| **Lemma 2.1** (forced interference) — Bogdanov forces nonvanishing mixed terms | **[P]** | [`triple-matching-rewrite.md`](triple-matching-rewrite.md) (decorated occurrences, cubic union, fourth-matching rewrite, Bogdanov attribution); sharpest form is [`finite-obstruction.md`](finite-obstruction.md) §7 **Cor. 7.2** | `verify_triple_matching_rewrite.py`, `verify_finite_obstruction.py` | **NEEDS-POLISH** |
| GHZ tensor `Δ` lies in the **closure** of matching tensors; approach needs amplitudes diverging in the inverse residual | **[P]** | [`tensor-route.md`](tensor-route.md) §6, the **Border theorem** — an explicit Laurent family with `H_n(A(t)) = Δ_{n,3} + Σ_{k≥1} t^k T_k` and a Zariski-closure corollary, for every even `n ≥ 6`; GIT complement in [`finite-obstruction.md`](finite-obstruction.md) | `verify_prism_border.py`; supporting `verify_cancellation_example.py`, `verify_finite_obstruction.py` | **NEEDS-POLISH** (mild) |
| Lattice `L_S` has rank **228** for the full ternary support at `n = 8` | **[P]** | [`2026-08-11-external-theory-reformulation-survey.md`](2026-08-11-external-theory-reformulation-survey.md) §2 item 2 (`228 = 252 − 24`); restated in [`2026-08-11-signed-matching-holonomy-programme.md`](2026-08-11-signed-matching-holonomy-programme.md) | **inline Python inside the survey note**, not a `computations/verify_*.py` | **NEEDS-POLISH** |
| **Lemma 2.2a** (soundness) — (O1), (O2) and a finite list of integral certificates account for every refuted support across the censuses (`11,578` supports) | **[P]** | [`2026-08-11-signed-matching-holonomy-programme.md`](2026-08-11-signed-matching-holonomy-programme.md) §2 (the (O1)/(O2)/(O3) trichotomy); census of record [`n8-sharp-exact10-augmented-group-block8.md`](n8-sharp-exact10-augmented-group-block8.md) (`11,578 = 8,523` sign units `+ 3,055` one-class units, zero third types) | `verify_n8_sharp_exact10_augmented_group_block01.py`, `..._block45.py`, `..._block6.py`, `..._block8.py`, `verify_n8_sharp_exact10_least_cell_cutoff.py` | **NEEDS-POLISH** — see label note **L1** |
| **Lemma 2.2b** (sharpness I) — two supports with *identical unsigned data* split by (O1) vs (O2) | **[P]** | [`n8-sharp-exact10-signature-counterguard.md`](n8-sharp-exact10-signature-counterguard.md) — the exact-ten repairs `A` and `B` | `verify_n8_sharp_exact10_signature_counterguard.py` | **NEEDS-POLISH** (closest to READY in §2) |
| **Lemma 2.2c** (sharpness II) — an explicit satisfiable 8-vertex configuration with an odd cycle of holonomy `−1` whose relation vectors are linearly independent | **[P]** | mechanism in [`n8-toric-binomial-lattice-audit.md`](n8-toric-binomial-lattice-audit.md) (consistency over the complex torus iff `(0,1) ∉ L`); the specific witness is **not located** — see **L2** | `search_n8_toric_binomial_lazy_cegar.py`, `reconstruct_n8_toric_witness.py`, `verify_n8_toric_constant_product.py` | **MISSING** |

## 3. Descent and the base case

| claim | label | best backing | checker | readiness |
|---|---|---|---|---|
| **Thm. 3.1** (six-site obstruction, "Theorem A") — 19 rank types, exact certificates | **[P]** | [`proofs/six-site-arbitrary-complex-obstruction.md`](../proofs/six-site-arbitrary-complex-obstruction.md) | `verify_f4_support_obstruction.py`, `search_f5_support_sat.py`, `certify_f5_c4_p2_transfers.py`, `verify_saturated_rank_graph_obstruction.py`, `certify_low_rank_graph_laurent.py`, `verify_color_sensitive_support_obstruction.py`, `certify_exceptional_triangle_obstruction.py` (+4 supplements) | **READY** |
| **Thm. 3.2** (clean-pair descent, "Theorem B") | **[P]** | [`clean-pair-cap-exact-descent-target.md`](clean-pair-cap-exact-descent-target.md) Theorem 1.1 — **no standalone page in `proofs/`** | `verify_clean_pair_cap_exact_descent_target.py` | **MISSING** as a proof page; **NEEDS-POLISH** as content — see **L3** |
| **Problem 3.3** (clean-pair existence) — normalization: maximum protected anchors, then minimum support | **[O]** | normalization: [`anchor-lexicographic-curvature-synchronization.md`](anchor-lexicographic-curvature-synchronization.md) Thm 1.1; open reduction: [`consolidated-proof-frontier.md`](consolidated-proof-frontier.md) §§1–2 | `verify_anchor_lexicographic_curvature_synchronization.py` | **NEEDS-POLISH** |
| **Lemma 3.4 case 1** — axis-pure/degenerate branches empty; `1,020` / `57,291` / `2,126,208`; multiaffinity | **[P]** | emptiness: [`h3-axis-pure-global-min-support-census.md`](h3-axis-pure-global-min-support-census.md); censuses: [`h3-c6-e14-pure11-unary-unit.md`](h3-c6-e14-pure11-unary-unit.md) (1,020), [`h3-c6-e14-two-cell-unit-frontier.md`](h3-c6-e14-two-cell-unit-frontier.md) (57,291), [`h3-c6-e14-three-cell-top-degree-boundary.md`](h3-c6-e14-three-cell-top-degree-boundary.md) (2,126,208) | matching `verify_*.py` for each | **MISSING** (two chains fused) — see **L4**, **L5** |
| **Lemma 3.4 case 2** — off-axis support forces an active fan; `3^15` sign patterns; fan gives the rank conditions | **[P]** | [`h3-active-fan-coloop-or-four-good.md`](h3-active-fan-coloop-or-four-good.md); balanced-cut half [`h3-balanced-only-determinant-debt.md`](h3-balanced-only-determinant-debt.md); rank step [`uniform-bidirectional-private-site-fan-rank-boundary.md`](uniform-bidirectional-private-site-fan-rank-boundary.md) | matching `verify_*.py`; **no checker for the `3^15` exhaustion** | **NEEDS-POLISH** — see **L6**, **L7** |
| **Lemma 3.4 case 3** — recurrent branches terminate; `5,141` → `446` → six types | **[P]** | [`h3-active-fan-coloop-saturation-boundary.md`](h3-active-fan-coloop-saturation-boundary.md) | `verify_h3_active_fan_coloop_saturation_boundary.py`; scope in `verify_h3_active_coloop_literal_packet_termination_scope.py` | **NEEDS-POLISH** — see **L8** |

The trapped pure-colour coloop that survives case 3 has **no note of its
own**. Its nearest home is
[`h3-active-fan-coloop-gate-ii-assembly-boundary.md`](h3-active-fan-coloop-gate-ii-assembly-boundary.md),
and its destination is the §6 master note.

## 4. Certificates as constrained homotopies

| claim | label | best backing | checker | readiness |
|---|---|---|---|---|
| **Prop. 4.1** — under `Φ_{c^n} = 1` the full matching complex is explicitly contractible | **[P]** | [`uniform-chart-odd-matching-exchange-operation-tag-tor-gate.md`](uniform-chart-odd-matching-exchange-operation-tag-tor-gate.md) eqs (7)–(9) | `verify_uniform_chart_odd_matching_exchange_operation_tag_tor_gate.py` | **NEEDS-POLISH** — the lemma is buried in a note titled for something else |
| **Thm. 4.2** (fencing) — the residual class is chart-antisymmetric; every matching-side operation is symmetric | **[P]** | no hub page. Koszul/determinant half: [`uniform-balanced-chart-square-master-obstruction.md`](uniform-balanced-chart-square-master-obstruction.md) §1; Reynolds: [`uniform-chart-complete-torus-reynolds-gate.md`](uniform-chart-complete-torus-reynolds-gate.md); flattenings: [`simultaneous-diagonal-flattening-palette-fusion-gate.md`](simultaneous-diagonal-flattening-palette-fusion-gate.md); pure-target: [`pure-target-one-site-polarization-and-odd-cofactor-gap.md`](pure-target-one-site-polarization-and-odd-cofactor-gap.md) | one per note; pure-target checker is `verify_pure_target_one_site_polarization_odd_cofactor.py` (**breaks the naming convention**) | **MISSING** — see **L9** |
| each unordered cut retains an independent `GL_3` gauge | **[P]** | [`simultaneous-diagonal-flattening-palette-fusion-gate.md`](simultaneous-diagonal-flattening-palette-fusion-gate.md) | `verify_simultaneous_diagonal_flattening_palette_fusion_gate.py` | **NEEDS-POLISH** — note says *unoriented* cut and general `GL_r`; sketch says *unordered* and `GL_3` |
| equivariant Cartan–Spencer calculus on the principal-parts resolution | **[G]** | scattered: [`h3-complete-hasse-cartan-naturality-square-gate.md`](h3-complete-hasse-cartan-naturality-square-gate.md), [`h3-universal-spencer-euler-contraction.md`](h3-universal-spencer-euler-contraction.md), [`h3-shifted-principal-parts-comparison-obstruction.md`](h3-shifted-principal-parts-comparison-obstruction.md); map note [`2026-08-12-interference-cartan-proof-map.md`](2026-08-12-interference-cartan-proof-map.md) | per-gate checkers | **MISSING** — no page defines the object |
| Ward identity `X_src Φ_c = Φ_{Xc}`, verified termwise | **[P]** | [`uniform-physical-cartan-source-prism.md`](uniform-physical-cartan-source-prism.md) eq (2) | `verify_uniform_physical_cartan_source_prism.py`, `verify_h3_physical_cartan_source_orbit_descent.py` | **NEEDS-POLISH** — see **L10**; the note has an **unclosed `\[`** at the Ward identity itself |
| Cartan homotopy `K = (1−s)H_w`, `dK + Kd = (1−s)(w−1)`, annihilating the endpoint-even summand | *(unlabelled)* | [`h3-endpoint-odd-cartan-prism-augmentation.md`](h3-endpoint-odd-cartan-prism-augmentation.md) eqs (1)–(5) | `verify_h3_endpoint_odd_cartan_prism_augmentation.py` | **NEEDS-POLISH** (mild — best-conditioned page in §4) |
| secondary transfer identifies `−δ = (−1,+1,+1,−1)`, forced and unique | **[P]** | [`h3-order6-endpoint-odd-hpl-secondary-transfer.md`](h3-order6-endpoint-odd-hpl-secondary-transfer.md); the value `−δ` is defined in [`h3-endpoint-odd-cartan-prism-augmentation.md`](h3-endpoint-odd-cartan-prism-augmentation.md) eq (4) | `verify_h3_order6_endpoint_odd_hpl_secondary_transfer.py` | **NEEDS-POLISH** — see **L11** |

## 5. Uniformity in the order

| claim | label | best backing | checker | readiness |
|---|---|---|---|---|
| **Prop. 5.1** — the eigenvalue of `A_h` on `[2h−2,2]` is `h² − 3h + 1`; five-sector spectrum of `B_h` | **[P]** | [`uniform-centered-occurrence-matching-eigenspace-correction.md`](uniform-centered-occurrence-matching-eigenspace-correction.md); [`uniform-centered-occurrence-endpoint-association-projector.md`](uniform-centered-occurrence-endpoint-association-projector.md) | `verify_uniform_centered_occurrence_matching_eigenspace_correction.py`, `..._endpoint_association_projector.py` (frozen ledgers) | **NEEDS-POLISH** |
| **Prop. 5.1** — composite transfer constant `56h³(2h−1)`, out of sample through `h = 12`; multiplicity-one residual shape; `π A_{h+1} ι = A_h` | **[P]** | **only** `computations/unaudited-stress-repstability-2026-08-13/REPORT.md` | none committed | **MISSING** — see **L12**, the sharpest label risk in the sketch |
| naturality along `ι` alone does not transport the `[2h−2,2]` statement | **[P]** | [`pointed-h3-spectator-uniformization-no-go.md`](pointed-h3-spectator-uniformization-no-go.md) | `verify_pointed_h3_spectator_uniformization_no_go.py` | **NEEDS-POLISH** — see **L13**, the committed no-go proves a neighbouring statement |
| **Prop. 5.2** (moment collapse) — carrier `Γ` with `dΓ = r − 2q`; Rodrigues-type moment identity | **[G]** | `dΓ = r − 2q`: [`h3-chart-odd-gate-ii-augmented-filler-terminal-fork.md`](h3-chart-odd-gate-ii-augmented-filler-terminal-fork.md) eq (33); moments: [`uniform-physical-horizontal-moment-saturation-bridge.md`](uniform-physical-horizontal-moment-saturation-bridge.md) | `verify_uniform_physical_horizontal_moment_saturation_bridge.py`, `verify_scalar_unit_carrier_moment_tower_hilbert_cauchy.py` | **NEEDS-POLISH** — see **L14** |

## 6. The remaining statement

This is the best-documented section in the repository: two of its notes are
the only pages written in a public register, and both link back to the
sketch.

| claim | label | best backing | checker | readiness |
|---|---|---|---|---|
| the four-site residual window `A = D q₀₁ H`, `B = p₀ s₁ H`, `C = p₁ s₀ H` | *(definition)* | [`h3-fixed-window-centered-k22-physical-routing-gate.md`](h3-fixed-window-centered-k22-physical-routing-gate.md) eq (1) | `verify_h3_fixed_window_centered_k22_physical_routing_gate.py` | **NEEDS-POLISH** — `\[ … \]` throughout; the window definition should move into the master note |
| **Thm. 6.1** — `z = (1,1,−1,−1)` is the unique annihilator of the mate rows; three obstructions coincide with it | **[P]** | [`uniform-balanced-chart-square-master-obstruction.md`](uniform-balanced-chart-square-master-obstruction.md) §§1–2 | `verify_uniform_balanced_chart_square_master_obstruction.py`, which pins [`h3-gate-ii-switch-weyl-product-rule-idempotent-gate.md`](h3-gate-ii-switch-weyl-product-rule-idempotent-gate.md), [`uniform-recurrent-core-complete-row-projection-boundary.md`](uniform-recurrent-core-complete-row-projection-boundary.md), [`uniform-chart-odd-matching-exchange-operation-tag-tor-gate.md`](uniform-chart-odd-matching-exchange-operation-tag-tor-gate.md), [`h3-chart-odd-gate-ii-augmented-filler-terminal-fork.md`](h3-chart-odd-gate-ii-augmented-filler-terminal-fork.md) | **READY** |
| **Conj. 6.2** (balanced chart-square saturation) | **[O]** | [`uniform-balanced-chart-square-master-obstruction.md`](uniform-balanced-chart-square-master-obstruction.md) §4 | same | **READY** |
| `ψ_z = ¼(1,1,−1,−1)` annihilates every presently constructed physical column | **[P]** | [`uniform-balanced-chart-square-master-obstruction.md`](uniform-balanced-chart-square-master-obstruction.md) eq (5); [`h3-balanced-square-pointed-full-q-cone-gate.md`](h3-balanced-square-pointed-full-q-cone-gate.md) §4 | `verify_h3_balanced_square_pointed_full_q_cone_gate.py` | **READY** |
| terminal `q = Σⱼ mⱼ − ainc` annihilates the complete `8,580`-column operator block and all `288` repeated columns | **[P]** | [`h3-first-flat-physical-anchor-six-term-separator.md`](h3-first-flat-physical-anchor-six-term-separator.md) eq (3) | `verify_h3_first_flat_physical_anchor_six_term_separator.py` | **NEEDS-POLISH** — `\[ … \]`, and a broken macro `-operatorname{ainc}` in the boxed equation (3) |
| counterguards — `du = 0`; the `171`-column `q`-Jacobian has no restriction face; internal `K₂,₂` can be perfectly centered | **[P]** | [`h3-balanced-square-pointed-full-q-cone-gate.md`](h3-balanced-square-pointed-full-q-cone-gate.md); centering counterpoint is eq (7) of the master note | `verify_h3_balanced_square_pointed_full_q_cone_gate.py` | **READY** |

## 7. Assembly

**Theorem 7.1** is a derivation from the statements above and needs no
separate backing artifact. Its dependency chain is exactly Prop. 1.1 →
Problem 3.3 (normalization) → Lemma 3.4 → Conj. 6.2 → Prop. 5.2 →
Thm. 3.2 → Thm. 3.1.

## Label notes

These are places where the sketch's label or wording is wider than the
artifact it rests on. Several come from
`computations/unaudited-external-spine-audit-2026-08-13/REPORT.md` and its
repair pass `computations/unaudited-repair678-checkers-2026-08-13/WORDING-FIXES.md`.
Per repository discipline those directories are **inputs, not spine**, and
none of their findings has itself been re-audited — but each of the six
wording items below was checked against the committed notes while building
this index, and the committed notes do read as the audit describes.

* **L1.** Lemma 2.2's soundness half is *census* content, and the census is
  a **prefix**. The programme note calls it "the empirical content of two
  years of CEGAR" and lists the uniform version as **Problem 1, the repo's
  oracle conjecture** — i.e. open. The census notes are explicit that the
  `11,578` figure covers chart-26 blocks 0–8 only: "Forty-four possible
  blocks remain. This is a certified prefix, not yet the complete exact-ten
  stratum", and "This remains bounded chart-26 progress, not a complete
  chart-26 or `N = 8` proof". The sketch's sentence is defensible read
  narrowly — every support that *was* refuted was refuted by these
  mechanisms — but under a **[P]** heading a reader will take it for the
  uniform statement. Add the "in the censuses carried out so far" scope.
* **L2.** I could not locate the explicit satisfiable 8-vertex
  configuration of Lemma 2.2c. See the search record at the end of this
  note.
* **L3.** The sketch states Theorem 3.2 with the hypothesis "**both caps
  have rank 3**". No artifact states it that way — `grep "both caps"`
  returns only `PROOF-SKETCH.md`. The proved hypothesis is
  `s·κ₀κ₁κ₂ ≠ 0` together with the vanishing of the higher-cumulant error
  `𝓔_{p,q}(K) = 0`, and the backing note warns explicitly that the
  nonvanishing conditions **alone are not sufficient**. Either restate
  Theorem 3.2 in the proved form, or supply a bridging lemma
  "rank-3 caps ⟹ `s·κ₀κ₁κ₂ ≠ 0` and `𝓔 = 0`" — which has no backing note
  anywhere in the repository. Note also that the repo's "four-good"
  predicate is about *four deleted-star ranks three*, not about cap rank,
  so it is not the missing bridge.
* **L4.** Case 1 fuses two independent chains. The axis-pure emptiness is
  proved by a **SAT/UNSAT census** (69 variables, 21,345 clauses, Glucose4
  + CaDiCaL), not by the `1,020` / `57,291` / `2,126,208` specialization
  censuses, which are the `E14`/`C6` chart chain. Presenting the second as
  the proof of the first is a category error. Two notes also claim the
  axis-pure theorem independently
  ([`h3-axis-pure-global-min-support-census.md`](h3-axis-pure-global-min-support-census.md)
  and [`h3-axis-pure-closure-active-crossword-frontier.md`](h3-axis-pure-closure-active-crossword-frontier.md));
  one should be designated authoritative.
* **L5.** Two counting corrections inside case 1. `2,126,208` counts
  **(chart, triple) pairs** across the nine canonical minimal `E14` charts
  — `260,118` distinct triples — and every downstream restatement, the
  sketch included, drops the "across the nine charts" qualifier. And
  "multiaffinity … shows no deeper stratum exists" overstates: the
  three-cell layer is empty, but the external audit reports **264
  four-cell survivors on chart (1,3)**, and the backing note itself says
  "It does not yet prove emptiness after allowing every internal cell
  simultaneously." **No authoritative multiaffinity page exists** — the
  claim survives only as one-sentence remarks in three frontier logs. The
  honest form is "this exhausts the local monomial *types*", not
  "no deeper stratum exists".
* **L6.** The `3^15` figure has **no committed checker and no note**. The
  string `3^15` appears in the repository only in `PROOF-SKETCH.md`,
  `README.md`, and the two unaudited external-audit files, where the
  exhaustion (`2,669,328` determinant-bright rows, none lacking a nonzero
  off-diagonal cell) is listed under "Verified TRUE by independent
  re-derivation (**not** by committed checkers)". The notes attribute it
  to commit `1ec750e` without stating the count. Either commit a checker
  or re-attribute the number.
* **L7.** In case 2, *entry* is exhaustive but *landing* is not. The
  sketch's "and expanding along that cell produces the rank conditions of
  Theorem 3.2, hence a clean pair" is stronger than the backing: the fan
  construction and the four-good links are unverified, and the backing
  note's own §4 boxes an unproved "Active-fan coloop normalization and
  landing". The **[P]** is correctly placed on the sign-pattern clause
  only, but the sentence invites the wider reading.
* **L8.** In case 3, "each type is routed either back to case 2 or to the
  refutation mechanisms" is **conditional**: the routing table applies only
  after the boxed, open "Active-fan coloop tight-set lift", and the note
  says it "does not close global entry". Also worth adopting from the
  audit: `446 = 448 − 2` (drop the empty family and the complete graph),
  and the 446 fall into **nine** `S₆`-orbits which blocker duality
  `F ↔ T(F)` pairs into the six types — three self-dual, three dual pairs.
  "Six types up to symmetry" skips the duality step.
* **L9.** The word "fencing" appears nowhere in `notes/`, `proofs/`, or
  `computations/`. It is `PROOF-SKETCH`/`README` vocabulary for five
  results proved in five unrelated notes, only one of which uses the chart
  involution framing that the sketch says is the uniform mechanism.
* **L10.** The Ward identity is verified, but the external audit records it
  as "structurally near-tautological (holds for any forbidden pair and any
  matching subset; 8,748 rows ≈ 1 statement up to manifest symmetry)". The
  notes also write it as `X_src H_z = H_{X_out z}`; the `H ↔ Φ` renaming
  and the suppression of `X_out` are undocumented.
* **L11.** "Forced and **unique**" is not asserted in those terms by any
  note. What is proved is well-definedness on `D1` homology — changing a
  first-page representative changes `D2` only by a `D1` boundary. Prefer
  "canonical" or "independent of the representative", or add the
  uniqueness argument.
* **L12.** `56h³(2h−1)` and the out-of-sample verification through `h = 12`
  exist **only** in a directory whose own header reads "UNAUDITED STRESS
  TEST". Under the sketch's own definition — **[P]** means exact checker
  *and* independent audit — this clause cannot carry **[P]**. The same
  source flags two caveats the sketch drops: `A_h` alone stops separating
  eigenspaces at `h = 6`, and the intertwining test is generic (it passes
  for a deliberately broken operator).
* **L13.** The committed spectator no-go is about `h = 3` → all-order
  functorial constructions. It never mentions `ι`, `π A_{h+1} ι = A_h`, or
  isotypic level; the `ι`-specific statement lives only in the same
  unaudited directory.
* **L14.** Prop. 5.2's **[G]** looks strong. The moment-bridge note states
  the identity as a *sufficient hypothesis* — "The currently proved
  overlapping-pair and four-cut identities do not imply (2)" — and the
  carrier descent is gated on an explicitly **open** chart-odd augmented
  saturation theorem. The existing "Granted the family of Conjecture 6.2"
  qualifier does not cover this second dependency.

## Polish worklist

Ordered by how much a public reader's trust depends on it. Items 1–3 are
about statements that are *labelled proved and are load-bearing*; items 4–7
are about presentation.

### 1. Assemble `proofs/clean-pair-descent.md` (Theorem 3.2) — **highest priority**

Theorem 3.2 is half of the sketch's spine and is the only pillar with no
proof page, no independent audit, and a printed hypothesis that does not
match the proved one (**L3**). Assemble from
[`clean-pair-cap-exact-descent-target.md`](clean-pair-cap-exact-descent-target.md),
in this order:

1. **Statement.** Resolve **L3** first — restate in the `(s, κ, 𝓔)` form,
   or prove the rank-3 bridging lemma. This is the one genuinely new
   mathematical task on the list.
2. **Setup.** §2 eqs (8)–(11): the site-square-zero algebra `𝒮_U`, `x`,
   `s = ⟨K, A_pq⟩`, `R_ab`, `r`.
3. **Cap expansion.** §2 eqs (12)–(13) — matchings split by whether they
   use `pq`. Ledger id **C2a**.
4. **Canonical error identity.** §3 eqs (14)–(17), with the `N = 8`,
   `h = 3` specialization `6𝓔 = 3sr²x + r³`. Ledger id **C2b**. Cite
   [`line-plus-plane-shore-clean-cap-pencil-independent-audit.md`](line-plus-plane-shore-clean-cap-pencil-independent-audit.md)
   as the independent re-derivation of these coefficients.
5. **The contraction.** §4 eqs (18)–(22) — complete as written; lift
   near-verbatim, converting `\( … \)` → `$…$`. Ledger id **C2c**.
6. **Corollary.** §5 Corollary 5.1 plus the palette-projection paragraph;
   cross-reference Theorem 3.1.
7. **Worked instances.**
   [`adjacent-cubic-pair-exact-descent.md`](adjacent-cubic-pair-exact-descent.md)
   (explicit, hypothesis-free `N → N−2` descent) and
   [`line-plus-plane-shore-clean-cap-pencil.md`](line-plus-plane-shore-clean-cap-pencil.md)
   (a whole clean pencil).
8. **Scope.** §6 items 1–6, rewritten declaratively. Keep item 6 — the
   prism root covers are a limitation a referee will ask about.

[`formal/FORMALIZATION.md`](../formal/FORMALIZATION.md) §4.2 already gives
this as a dependency-ordered table (C2a/C2b/C2c/C3/C4/C5/C6a/C6b); use it as
the section outline. Then commission the independent audit that Theorem 3.1
has and this does not.

### 2. Correct the four label-risk clauses in `PROOF-SKETCH.md`

No new mathematics; each is a wording fix backed by an artifact already in
the repository. In descending severity: **L12** (`56h³(2h−1)` / `h = 12`
rest on an unaudited directory — demote to **[G]** or commit the checker),
**L5** (`2,126,208` qualifier, and "no deeper stratum exists" versus 264
four-cell survivors), **L6** (`3^15` has no committed checker), **L1**
(soundness is census content, not the oracle conjecture). Then **L7**,
**L8**, **L11**, **L14** as a second pass.

### 3. Assemble a funnel page for Lemma 3.4

Case 1 is currently **MISSING** and cases 2–3 have no shared home. One page,
`proofs/local-funnel.md` or `notes/h3-local-funnel.md`, built from:
case 1(a) axis-pure emptiness from
[`h3-axis-pure-global-min-support-census.md`](h3-axis-pure-global-min-support-census.md)
(and retire or subordinate the duplicate); case 1(b) the three censuses,
presented as *local monomial type exhaustion* rather than emptiness (**L5**);
case 2 from
[`h3-active-fan-coloop-or-four-good.md`](h3-active-fan-coloop-or-four-good.md)
plus [`h3-balanced-only-determinant-debt.md`](h3-balanced-only-determinant-debt.md),
with the `3^15` claim re-attributed (**L6**); case 3 from
[`h3-active-fan-coloop-saturation-boundary.md`](h3-active-fan-coloop-saturation-boundary.md)
with the `448 − 2` and nine-orbits/blocker-duality refinement. Mark **[O]**
honestly on the multiaffinity gluing lemma, the fan landing, and the
tight-set lift.

### 4. Write the fencing hub note (**L9**)

One page stating the uniform mechanism once — residual class antisymmetric
under the chart involution, every matching-side operation symmetric — and
then citing the five per-operation results as instances. Four of the five
notes do not currently mention the involution at all, so this is genuine
consolidation, not a rename. Take the register from
[`uniform-balanced-chart-square-master-obstruction.md`](uniform-balanced-chart-square-master-obstruction.md).

### 5. Delimiter and rendering pass on the pages the sketch depends on

Not all 1,822 notes — only the ~25 backing pages named in the tables above.
Convert `\[ … \]` → `$$…$$` and `\( … \)` → `$…$`. Three concrete bugs to
fix while there:

* [`uniform-physical-cartan-source-prism.md`](uniform-physical-cartan-source-prism.md)
  — four `\[` opens, one `\]` close; the Ward identity display (eq 2) is
  never closed.
* [`h3-first-flat-physical-anchor-six-term-separator.md`](h3-first-flat-physical-anchor-six-term-separator.md)
  — `-operatorname{ainc}` (missing backslash) inside the boxed eq (3).
* [`h3-cut-swap-shared-repair-anchor-fibre-dichotomy.md`](h3-cut-swap-shared-repair-anchor-fibre-dichotomy.md)
  — `qquad` (missing backslash) at eq (6).

### 6. Give §2 a single signed-obstruction page

[`2026-08-11-signed-matching-holonomy-programme.md`](2026-08-11-signed-matching-holonomy-programme.md)
already has the right content — gauge descent, the Zaslavsky lattice, rank
228, (O1)/(O2)/(O3), and the sharpness pointers — but it is written as a
programme with open problems interleaved. Split it: a statement page for
Lemma 2.1/2.2 and the lattice, and a separate open-problems page. While
there, promote the rank-228 computation out of the survey note's inline
Python into a `computations/verify_*.py`, and resolve **L2**.

### 7. Convention repairs

Rename `computations/verify_pure_target_one_site_polarization_odd_cofactor.py`
to match its note. Replace commit-hash citations with note links in
[`2026-08-12-interference-cartan-proof-map.md`](2026-08-12-interference-cartan-proof-map.md)
(`abe582b`, `a4e15ab`),
[`h3-reynolds-attach-coupled-obstruction.md`](h3-reynolds-attach-coupled-obstruction.md)
(`ed60e2c`), and
[`h3-balanced-square-pointed-full-q-cone-gate.md`](h3-balanced-square-pointed-full-q-cone-gate.md)
(`0ffc23a`, currently the only definition of `z` in that note).

## Search record for the one unlocated claim

**Lemma 2.2c** — "an explicit satisfiable 8-vertex configuration carrying an
odd cycle of holonomy `−1` whose relation vectors are linearly independent".
This was searched independently twice, across `notes/`, `proofs/` and
`computations/`, with no backing page or checker found.

Terms searched: `sharpness`, `sign enrichment`, `unsigned data`, `identical
unsigned`, `linearly independent` (intersected with `holonomy` / `relation` /
`odd` / `circuit`), `satisfiable` (intersected with `odd` / `holonomy`),
`odd cycle` (intersected with `independent` / `satisfiable` / `eight`),
`odd cycle.*holonomy`, `holonomy -1`, `` holonomy `-1` ``, `odd triangle`,
`odd dependence`, `odd dependency`, `odd integer dependency`, `odd
coefficient sum`, `coefficient sum.*odd`, `lattice dependency`, `no lattice
dependenc`, `without a dependency`, `handcuff`, `character-consistent`,
`is a value`, `is a value, not`, `value, not a contradiction`, `not a
contradiction`, `does not refute` ∩ `odd`, `full rank` ∩ `holonomy`; plus
filename scans `ls notes/ | grep -iE "sharp|holonomy|countermodel|counterguard|odd-circuit|lattice"`
and `ls computations/ | grep -iE "sharp|sign|holonomy|unsigned"`.

The sentence "without a lattice dependency, odd holonomy is a value, not a
contradiction" occurs **only** in `PROOF-SKETCH.md` and nowhere else in the
repository.

What exists is the *mechanism* rather than the witness.
[`n8-toric-binomial-lattice-audit.md`](n8-toric-binomial-lattice-audit.md)
proves the exact criterion — the mixed equations `x^{d_i} = −1` are
consistent over the complex torus **iff** `(0,1)` is not in the lattice
generated by `(d_i, 1)` and `(0,2)`, i.e. iff there is no integer dependency
among the `d_i` with odd coefficient sum — which is exactly the content the
sketch is reaching for; the same criterion appears in
[`binomial-nonzero-constant-toric-boundary.md`](binomial-nonzero-constant-toric-boundary.md) §1
(consistency iff `d_f ↦ −1` extends to a character of `L`), with checkers
`verify_parallel_binomial_constant_toric_boundary.py` and
`search_parallel_binomial_nonzero_constants_cegar.py`.

The nearest explicit witnesses are all six-vertex or wrong-shaped:
[`binomial-incidence-odd-dependence-countermodel.md`](binomial-incidence-odd-dependence-countermodel.md)
(48-cell six-vertex support, consistent signs, no odd dependence — but all
three constants vanish),
[`uniform-cycle-switch-localization-countermodel.md`](uniform-cycle-switch-localization-countermodel.md)
("no odd Laurent dependency at all"),
[`uniform-signed-matching-holonomy-boundary-counterguard.md`](uniform-signed-matching-holonomy-boundary-counterguard.md)
("the top binomial alone has no holonomy circuit", six sites), and
`n8-one-bad-source-labelled-exchange-cycle-gate.md` ("holonomy is
`(-1)^4 = 1` … a valid local diamond, not a contradiction" — even holonomy).

Two possible resolutions: the witness is recorded only inside the CEGAR
artifacts under `computations/` with no prose page, in which case it needs
one; or the sketch's sentence should be rewritten to assert the lattice
criterion above — which *is* proved and checker-backed — rather than an
explicit 8-vertex configuration.
