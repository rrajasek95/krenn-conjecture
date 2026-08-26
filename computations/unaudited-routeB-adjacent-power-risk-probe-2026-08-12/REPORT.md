# UNAUDITED RISK PROBE — Route B adjacent-power cone (2026-08-12)

**Status: UNAUDITED external probe; not spine material. Pinned HEAD
`b63c76c8624996044423a0dde60a2b60c9e8fa3d` ("Record generic inactive upper
target construction"); all work ran against a git-archive snapshot. Exact
Fraction arithmetic. All seven relevant committed checkers re-run on the
snapshot and PASS (ledger df9cb21b… matches) — findings below concern the
gap between b63c76c's prose and what constructors establish, not any
broken checker.**

Scripts: `probe_a_jstar.py`, `probe_b_identity.py`,
`probe_cd_mv_and_collision.py`.

## Verdicts

**A. J_* identity REPRODUCED and generalized.** b63c76c is note-only (no
checker; zero hits for J_star constructors in computations/). Derived from
`verify_diagonal_rees_saturation_cap_jet_bockstein.py` conventions:
T(J_*) = −3αβΔ and hT(J_*) = −9αβΔ hold exactly over 73 generic + 3
collision instances, h=3. Unrecorded generalization: "T(c₁J₁+c₂J₂) ∝ Δ" is
the single equation c₁(α+β)+c₂((h−1)α−β)=0, solution line
(c₁,c₂) ∝ (β−(h−1)α, β+α), value −hαβ (verified h=3..8; uniqueness by
exhaustive search). Unrecorded readout: ⟨J_*, block⟩ = −3αβτ (nonzero
unless τ=0 — favourable for adjacent-power typing, but untracked).

**B. The upper-target claim is CONDITIONAL, and read literally FAILS.**
- Literal vector equality λ·hT(J_*) = −2(w−1)Δ in the 5-coordinate word
  module: NO λ works; best-case defect = 2wΔ = 2(111111+020020+202202),
  whose mixed part is provably outside the span of the entire committed
  diagonal + pure-row + global-transport family (rank 3 vs 4). Structural:
  every c₁J₁+c₂J₂ has zero mixed coordinates, all α,β,h,a.
- Intended Cartan reading is arithmetically exact: modulo im(d) and for
  ρ-even X, (1+ρ)H_w d(X) = 2(w−1)X, and (1/(9αβ))·hT(J_*) = −Δ gives
  −2(w−1)Δ coordinate-wise. BUT its load-bearing hypothesis is verbatim
  the datum `h3-signless-cartan-adjacent-power-shared-cell-gate.md`
  declares missing: a source-labelled Hasse/Rees-linear two-root
  comparison ι identifying hT(J) with 2(w−1)Δ as elements ("not a
  consequence of the committed inventories"; non-tautological by the same
  rank-3-vs-4 fact). Further silent assumptions: the Rees boundary must
  absorb im(d); N_lit has no span constructor (only the 3-basis
  counterguard); ρ-even is vacuous on monochromatic words (the factor 2 is
  entirely word-side); the 1/(9αβ) normalization is block-dependent
  (stratum-local, not a uniform source cell).
- The remaining LOWER face — (1+ρ)H_w d(P(J_*)) vs the adjacent response
  face mod N_lit — is NOT COMPUTABLE from committed constructors: H_w
  executable only on 2-variable de Rham forms; P(−) exists only as its
  scalar shadow; N_lit no constructor; "adjacent response face" is a
  ledger type string. Whether (H_0−u)e_Eq absorbs the 2wΔ defect is NOT
  WELL-POSED (different modules, no committed map). One favourable
  signal: the row-space invisibility no-go applies only to target-zero
  rows — a target-bearing adjacent-power cell escapes it.

**Suggested reading of b63c76c: "we now know which diagonal combination to
feed the missing comparison," not "the upper target is constructed."**

**C. β=0 trace collision: J_* supplies nothing** (J₂=(h−1)J₁, T(J_*)=0 —
localization at αβ excises exactly this stratum). GUARD WEAKNESS FOUND:
the committed unary-target guard is hardcoded (h,0,0) with only a
non-proportionality rank test — the colour-blind vector (0,1,0) also
passes; it does not certify "carries the selected colour." Good signal:
adaptive uncollision confines the β=0 obligation to the intrinsic
coordinate-unit block A = αE_aa (checker PASS), though the adaptive D is
not yet source-faithful through the two-chart overlap. On that block both
alternatives remain open (unary jet never constructed/never obstructed;
complementary-survival blocked by the executable h=4 counter-model).

**D. Rank-two vs target-zero VERIFIED** from real constructors
(rank(T(J₁),T(J₂)) = 2 iff β≠0, =1 at β=0; M_v corner targets all zero,
mutation-detected). Caveat: the comparison spans three mutually
unidentified modules — juxtaposition, not one-vector-space statement.

**E. Mutations:** all probe claims survive sign/coefficient mutations; the
one control failure is on the committed side (the β=0 colour-blind guard
above).

## Exact list of missing constructors

(1) (1+ρ)H_w on any module carrying P(J_*); (2) P(−) as a map; (3) N_lit
span; (4) coordinates for the "adjacent response face"; (5) the comparison
ι (provably non-tautological); (6) any map from e_Eq (8-site Eq module) to
mixed word coordinates; (7) an order-h unary target/anchor cell at β=0.
