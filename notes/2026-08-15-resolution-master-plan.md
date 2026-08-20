# Resolution master plan: the lemma DAG and parallel assignments

Status: **attack plan** (targets, not claims). Successor to the
zoomout/parallel-attack notes and the witness-splitting plan v2.
Discipline: the decision rule of `2026-08-14-proof-zoomout` binds every
lane; probes are unaudited external input until re-derived.

## 0. The root

**Intrinsic trichotomy (committed, 2026-08-14-problem-first).** A
minimal normalized exact ternary source yields (i) a source-ideal
unit/accepted separator, (ii) a clean pair (then Theorem B descent to
the Theorem A base), or (iii) a normalization-reducing deformation.
Every lemma below forces one of (i)-(iii). Theorems A and B are [P]
with independent audits; nothing downstream of a closed trichotomy is
open.

## 1. The lemma DAG (targets)

**Route I — coordinate dichotomy (Problem 3.3 direct).**
- **J.1 (blocking rigidity) [open]:** an exact source with every live
  pair witness-blocked has its rank-one structure forced into the
  coordinate/monomial regime. Evidence: P2's exhaustive h=2 pattern
  laws (s-patterns force rank/support collapse; witness statistics
  split cleanly on coordinate-ness); P1 (running) is deriving the h=3
  analogues.
- **J.2 (coordinate death) [open; partially committed]:** exact
  sources in the coordinate/monomial regime die by singleton/O2 and
  census mechanisms. Needs: the precise regime definition that makes
  J.1's output equal J.2's input, and the map to committed kills.
- J.1 + J.2 close Problem 3.3: witness pair (descend) or refute.

**Route II — band squeeze (unconditional).**
- **II.1 (floor):** supports 18..k dead (lanes' ratchet; monotone).
- **II.2 (ceiling):** supports 28..k+1 dead (permanent-triangle/C6
  machinery; executing).

**Route III — terminal (conditional; paused per midnight law).**
- **III.1 (source connection)** and **III.2 (enrichment census)**:
  owned by the lanes; not assigned here.

**Route A — GIT/moment stratification (new).**
- **A.1 (instability degeneration) [open]:** a gauge-unstable exact
  source degenerates along its destabilizing one-parameter subgroup to
  a solution of an initial-form system at strictly smaller support;
  the floor/census kills extend to these initial systems. Motivation:
  destabilizing weights = support filtrations, so the Kirwan
  stratification IS the support stratification; the observed
  eps^{-1/23} scaling is the destabilizing 1-PS signature.
  [CORRECTION, v5: that numeric had no repository backing — an
  unbacked import by this plan's author; struck. W3 shows the
  committed near-solution divergence is CLOSED-ORBIT gauge flow to
  the prism border point, not instability.]
- **A.2 (balanced normal form) [open]:** hence WLOG the counterexample
  is gauge-semistable, so it admits a moment-balanced representative
  (all vertex-colour loads equal); the ~24 balance equations join the
  system. Then: balanced + dense + sign-consistent is the target of a
  new overdetermination kill.
- A.1 + A.2 either empty the dense stratum or hand Route I/II a
  balanced normalization for free.

**Route T — tropical/initial-ideal dense emptiness (new; A.1's
polyhedral twin).**
- **T.1 [open]:** for every weight vector on the cells, some initial
  ideal of the Laurent-saturated GHZ ideal contains a monomial
  (per-cone singleton mixed initial forms — O2 tropicalized, over the
  matching polytope's face structure). T.1 alone empties the
  full-support stratum.

**Route F — 16-Pfaffian linearization (support to J.1).**
- **F.1 [open]:** express the pair data (s, kappa_c, E_pq) in the
  genus-2 Kasteleyn 16-Pfaffian coordinates; blocking conditions
  should become Plucker-rank degenerations, giving J.1's regime
  classification classical form.

**Cross-cutting:** uniformity is inherited by Route I (the error
polynomial is order-uniform); audit of any closing route; write-up.

## 2. Assignments (parallel, this session's agents)

| agent | target | first deliverable | falsifier |
|---|---|---|---|
| P1 (running) | J.1 at h=3 | blocking-forcing laws + equivariant home of the 729 components | a blocked pair with no structural collapse |
| W1 | J.1/J.2 bridge (P3') | exactness-push on the 36 all-blocked shadows: witness emergence vs coordinate collapse, with exact certificates | shadows reach exactness still blocked and non-coordinate |
| W2 | J.2 | regime definition + map to committed O2/census kills; the composable J.1->J.2 interface statement | a coordinate-regime exact source no committed mechanism kills |
| W3 | A.1 + A.2 | instability=>initial-degeneration lemma (formal), floor-on-initial-systems check, balanced equations tested on band strata | an unstable exact source whose initial system escapes the floor's methods |
| W4 | F.1 (+T.1 scouting) | pair data in Pfaffian coordinates; report whether blocking = Plucker degeneration; feasibility map for T.1's cone decomposition | Pfaffian form no simpler than cell form |

Difficult-vs-easy policy per the goal: W3 is the hard, deep attack
(classical GIT, high payoff, real risk); W1/W2 are the direct
composable pair; W4 is cheap support. Route II continues under the
lanes untouched.

---

## v2 addendum: P1 results land (2026-08-15, ~10:00)

The h=3 probe (`computations/unaudited-witness-splitting-p1-2026-08-15/`,
unaudited) delivered the blocking taxonomy:

- **FACT 1 (proved):** the 729 error components lie in the
  codimension-one equivariant subspace `ker det(d)`; the determinantal
  (`Lambda^3 x Lambda^3`) pairing is the *only* equivariant degree-3
  obstruction, and it yields the **uniform minor law**:
  `D(s^{3-j} k_{c_1}..k_{c_j}) = (3-j)! x` complementary minor of
  `A_pq`. All of P2's h=2 laws are the h=2 case of the same mechanism.
- Consequences: `k_0k_1k_2` never blocks; `s`-pattern blocking forces
  minor collapse of the pair block (`s^3 => det A_pq = 0`, observed
  iff); a **full-rank pair can only be degree-3 blocked through dirty
  monochrome slices** (`k_c^3`-blocking requires the colour-`c` slice
  error `E^(c) != 0` — F1, proved necessary).
- Calibration: the committed near-exact 8-site source carries **two
  explicit verified clean-cap witnesses**; exactness at pair (0,2)
  would contradict Theorem A via descent — near-exactness already
  manufactures witnesses, precisely as the route predicts.

**J.1 therefore splits into:**
- **J.1a (proved core + measured converse):** blocking at a pair
  forces minor-degeneracy or slice-dirtiness (the tables above).
- **J.1b (new target, well-posed, intrinsic):** an exact source cannot
  have all three monochrome slices dirty at every full-rank pair,
  given the pure normalizations and the forced interference structure.
  Owner: probe W5. Falsifier: an exact-satisfying template with all
  slices dirty everywhere — which would sharpen the counterexample
  portrait to "globally slice-dirty", itself a strong new constraint.

Updated route-I chain: J.1a [P-probe] + J.1b [open] + J.2 [W2, open]
=> Problem 3.3.

---

## v3 addendum: W2 lands — J.2 proved at N<=8 (R_cell); the bridge renamed (2026-08-15, ~11:30)

W2 (`computations/unaudited-witness-splitting-w2-2026-08-15/`,
unaudited) delivered:

- **J.2 at `N <= 8`, `R_cell`: proved by complete exhaustion** with a
  sharp mechanism split — mixed singletons carry every support
  `<= 27`; exactly 28 no-singleton templates exist, all at full
  support, all killed by odd holonomy. Six sites: all 2M templates
  singleton-killed at every support. Multi-cell (`R_mon`) upgrades
  probed (174k templates, all killed); annealed band hunts empty.
  The coordinate-regime counterexample hunt is an emptiness proof.
- **Regime fixed:** `R_mon` (monomial blocks / partial injections),
  gauge-stable, implied by the combined blocking chain.
- **Composition corrected:** the `kappa_c^h` blocking slot is
  structurally vacuous (fires iff span = W = generic), so J.1's
  original blocking hypothesis adds no information on the generic
  stratum — confirming the P1-era correction: the content is
  slice-dirtiness (J.1b) plus the NEW bridge:
- **J.1c (minor-to-support bridge) [open]:** at every blocked live
  pair of an exact source, at least two mixed `s*kappa` patterns
  fire (rank conclusions upgrade to support conclusions). Owner: W6.
- **J.1d (cells-vs-support counting) [open, flagged most promising]:**
  generalize the defect budget (`#coordinate R-edges >=
  N(7-N)/2 + |F|`; saturation iff `|F| >= N(N-4)/2` — attained at
  N=6, which is WHY the six-site proof worked; = 16 at N=8) into a
  counting lemma trading occupied cells against the support ceiling:
  noncoordinate rank-one blocks cost >= 2 cells. Owner: W6.
- **Portrait:** any counterexample is non-monomial on some edge.
- **J.2 residue:** uniform `N >= 10` statement (= the committed
  monomial-fiber note's section 3, confirmed as the target); full
  `R_mon` exhaustion at N=8; K3 in quotient-ring form.

Updated Route-I chain:
`J.1b [W5] + J.1c/J.1d [W6] => A in R_mon; J.2 [probe-proved N<=8,
uniform open] => contradiction; else witness => Theorem B descent.`

---

## v4 addendum: W4 lands — the Pfaffian frame proves the calibrations and supplies the bridge (2026-08-15, ~12:30)

W4 (`computations/unaudited-pfaffian-w4-2026-08-15/`, unaudited):

- **The dictionary:** R-blocks are Gram matrices of the hyperbolic
  form `B_K`; every error component is a `K_4` Pfaffian (Klein
  quadric); the error span is the image of `mu_pq` from four
  `<= 3`-planes; `kappa_c^2`-blocking is apolarity at a marked
  Segre-Veronese point. P2's FACTS 1-2 are now proofs. The witness
  condition classically: the 4x4 Kasteleyn matrix has rank `<= 2` for
  every parameter (a family of lines in `P^3`).
- **Criterion (C), the h=2 bridge (feeds J.1c, relayed to W6):** in
  `R_cell`, `kappa_c^2`-blocking is EQUIVALENT to an explicit 2+2
  colour-split support condition on the cell pattern. The rank->
  support bridge exists at h=2; J.1c's residue is the tied class,
  non-R_cell blocks, and the h=3 analogue.
- **Degree law (proved via Cauchy/Pieri):** pattern laws exist ONLY in
  degrees 2 and 3 (`I_3` misses `<det K>`; nothing in degree >= 4) —
  explaining the observed blocking-degree spectrum.
- **Arf verdict:** spin sectors = `H_1(T^2;F_2)` matching classes;
  every two-term O1 fibre equation IS a spin-sector
  Pfaffian-vanishing statement (classical home for the binomial
  layer), BUT `epsilon` does not factor through the spin grading (two
  committed certificates have `alpha = 0` fibres): O1's classical
  home is `H_1` of the CELL graph, not the surface. Both directions
  of the prediction resolved exactly.
- **T.1 failure locus mapped:** mod the 18-dim gauge lineality, the
  no-singleton weights are essentially the 6-dim edge-independent
  symmetric colour forms `f(i,j)` inside the `S_6`-invariant cone.
  **W7 launched** to close this residual cone, testing the reduction
  of its initial systems to the committed diagonal-pencil
  insolubility.

Fleet: W1 (exactness push), W3 (GIT), W5 (slice-dirtiness), W6
(bridge, now fed criterion (C)), W7 (tropical symmetric cone).


---

## v5 addendum: W3 lands — A.1/A.2 proved; the conjecture is phase-only after balancing (2026-08-15, ~13:30)

W3 (`computations/unaudited-git-moment-w3-2026-08-15/`, unaudited):

- **Theorem A.1 + Corollary A.2 proved, cleaner than planned:** no
  exact source is gauge-unstable (the pure rows force it); the true
  alternative is degenerate-to-a-SMALLER-SUPPORT-EXACT-SOURCE vs a
  balanced representative (loads = one constant per colour; 21 real
  conditions at n=8). Unconditionally: **WLOG a minimum-cell-support
  counterexample is balanced.** Crux lemma: gauge weights give every
  matching of a word the same weight, so gauge-initial systems are
  plain restrictions (Routes A and T are genuinely different).
- **The degeneration at n=8 equals the committed independent-four-set
  collapse** — now with a hypothesis-free, uniform-in-n proof and a
  MONOTONE POTENTIAL (cell count) the floor notes explicitly lacked.
  Offered to Route II.
- **The balanced-modulus kill is refuted by proof:** all-moduli-one
  satisfies every modulus-level condition; the modulus content of the
  balanced system is exactly {singleton, missing-pure}. **After
  balancing, the conjecture is a pure PHASE/HOLONOMY problem** — the
  strongest confirmation of certificate-centrality, and a major
  simplification for every deformation lane: searches may fix all
  moduli to 1 and work on the phase torus.
- **Author correction (decision-rule hygiene):** the plan's
  eps^{-1/23} numeric is struck (inline correction above).

Fleet after W3: W1 (exactness push — advised to work on the balanced
phase torus), W5 (slice-dirtiness), W6 (bridge, fed criterion (C)),
W7 (tropical symmetric cone).

---

## v6 addendum: W1 lands — J.1 re-axed from coordinates to singletons (2026-08-15, ~14:30)

W1 (`computations/unaudited-witness-splitting-w1-2026-08-15/`,
unaudited) pushed all 36 shadows toward exactness with exact
arithmetic (star linearisation; every verdict over Q):

- **Witnesses appeared 36/36** before any stall; 35/36 stalls have
  violated-set = singleton-set exactly; the all-blocked frontier caps
  at 98.6% of the mixed system.
- **J.1's coordinate phrasing is FALSE** (exact certificate: a fully
  live, all-blocked source with a non-coordinate rank-one block at
  97.4% mixed satisfaction). Blocking is indifferent to
  coordinate-ness (33% decoordination survival).
- **Proved exhaustively (2M configurations): monomial six-site
  death** — every monomial source with nonzero pures has a singleton
  mixed class (s >= 1; s >= 4 at full support; attained), so it
  satisfies at most 726 - s mixed equations.
- **Observed mechanism:** singleton-constrained imposition forces
  block death => error degeneration => witnesses.

**Route I, re-axed (the singleton law).** Replace the coordinate
regime by the fibre condition:

> **J.1-s (singleton law) [open; monomial case proved by W1, R_cell
> case by W2]:** an all-blocked source cannot satisfy the full mixed
> system — the all-blocked frontier is bounded away from exactness by
> a nonvanishing singleton obstruction (equivalently: exactness
> forces a witness pair somewhere).
> **J.2-s:** a singleton mixed fibre contradicts exactness directly
> (this IS O2 — already committed).

Open content: the non-monomial all-blocked frontier at N=8 (W1's two
certified near-exact all-blocked objects are the test data). W6's
J.1c/J.1d bridge re-aims accordingly: the counting lemma J.1d now
targets singleton forcing (cells-vs-support => some mixed class is a
singleton), not coordinate forcing. W5's slice-dirtiness remains part
of the blocking taxonomy (kappa^3 side) and continues.

### v6.1: W1 final report — the ceiling-saturation law (2026-08-15)

W1's consolidated final report adds three items to v6:

1. **Ceiling saturation.** Where a stall's violated set equals its
   singleton set (35/37 cases), the stall sits at the modulus-level
   ceiling `726 - s` of its support and is therefore optimal over
   **C** (by W3's phase-only reduction), not merely over Q. Three
   all-blocked frontiers saturate the ceiling *exactly* (hunt50010,
   hunt50020, hunt50024 — all 15 pairs live, coordinate supports):
   **on coordinate-rich supports, blocking costs nothing — the
   all-blocked locus reaches the support's exactness ceiling, and the
   only obstruction to exactness is the singleton count s.** This
   makes J.1-s quantitative: exactness demands s = 0 while staying
   all-blocked, and s is a support invariant that non-monomial
   spreading must drive to zero. W6's cost bound is now the single
   open inequality of Route I.
2. **Cross-validation.** W1's exhaustive monomial classification
   independently reproduces W2's B.3 (minimum 4 singleton fibres at
   support 15) — same 2M templates, disjoint code paths.
3. **Slice-exactness does not force witnesses** (hunt50010 is exact
   on a full colour slice and all-blocked) — closes a tempting
   shortcut lemma.

---

## v7 addendum: W5 lands — J.1b re-posed as a support condition (2026-08-15)

W5 (`computations/unaudited-slice-dirtiness-w5-2026-08-15/`,
unaudited) decided J.1b's structure:

- **The normalization half of J.1b is false, definitively.** Slice
  cleanliness is gauge-invariant under site scalings (pure equations
  are vacuous for it), and the 28 slice errors are algebraically
  independent — no cofactor-weighted sum rule exists (differential
  rank 28/28; one relation on {haf=1}, involving all 28, forcing
  nothing). Exact all-dirty witnesses with haf=1 at N=6 and N=8.
  Level separation explains it: pure/mixed equations live at k<=1 of
  the pair expansion, the slice error is the k>=2 remainder.
- **The true mechanism is support collapse.** On the whole all-blocked
  fleet 0/93 full-rank pairs are all-three-dirty, and a
  support-matched control reproduces this exactly: the zero pattern
  alone is responsible. For nonnegative weightings cleanliness is
  *equivalent* to support poverty (positivity of E).
- **Re-posed lemma (adopted): J.1b-support** — in an exact source,
  at every full-rank pair some colour fails the attachment condition
  (three disjoint attachment pairs, or two plus an internal edge).
  Combinatorial in the three diagonal-support graphs; the natural
  J.2 interface. Residual risk: the nonempty codimension-one
  cancellation-clean stratum.
- **New exactness laws** L1/L2 (Laplace/Wick at levels 1–2), with the
  **diagonal-regime corollary**: an exact diagonal source has all
  three slice cofactors vanishing at every full-rank pair, >= 12
  colour-exclusive edges, and <= 16 full-rank pairs — direct budget
  input for W6's counting.
- **Ternary J.1b is vacuous at six sites** (no exact source exists);
  N=8 is its smallest honest test. Numeric N=8 pushes show the
  tension concretely: keeping a full-rank all-three-dirty pair always
  costs a pure normalization.

**Convergent theme across W1/W3/W5:** blocking, cleanliness, and the
exactness frontier are all *support/phase* phenomena — moduli and
coordinate values are gauge. Route I's open content is combinatorics
of the three colour-support graphs at N=8: the singleton count s
(W1/W6) and the attachment condition (W5) are the two support
invariants the counterexample must simultaneously defeat.

---

## v8 addendum: W6 lands — Route I compresses to one number (2026-08-15)

W6 (`computations/unaudited-bridge-w6-2026-08-15/`, unaudited):

- **J.1c struck** (no co-occurrence law; the census is decisive). In
  its place, two exact tools: the **(STAR) pinning identity**
  (exactness determines a pair's whole block from its complement
  whenever some non-constant word has a nonzero complementary
  cofactor — on the committed near-exact source the mixed system is
  fully exact, (STAR) has zero residual on all 28 pairs, and the
  unpinned pairs are exactly where P1's witnesses live) and the
  **R_cell h=3 permanent dictionary**.
- **J.1d proved in exact form** (budget beta >= 3N - m + |H| with a
  Hall refinement) with unconditional corollaries: every exact
  source has m >= 3N/2; at m = 3N/2 the source is forced into
  R_cell with single diagonal cells on a properly 3-edge-coloured
  3-regular graph (at N=8: the committed support-12 cube chart is
  *derived*, not assumed); exact N=8 support <= 23 forces a
  single-cell block.
- **Two W2 record corrections** (adopted): the "Sigma cells <= 27"
  ceiling does not exist (27 counts live edges; the only committed
  cell ceiling is 189 in the structural 0/2 model), and "12 constant
  cells on >= 12 distinct edges" is false (correct: t1+2t2+3t3=3N/2
  with beta <= m - t2 - t3).
- **The band is not closed by counting alone**: zero-singleton
  templates exist at every support m >= 15 (certificates saved), and
  the measured cell price of singleton-freeness is Sigma_min(m) ~
  3.2m (61 at m=19 up to 98 at m=27). Hence any closing lemma must
  supply a **cell ceiling C(m) < Sigma_min(m)** — this hypothesis
  (H4) is the entire residual of Route I, and W6's certificates
  prove it necessary, not just convenient.
- **Composed conditional theorem** recorded (H1 committed + H2 band
  + H3 = O2 + H4 open => N=8 closes through the witness branch).
- **Convergence with the lanes**: W6's diagonal-regime kill (no
  singleton-free diagonal template at any support 12..27, any beta)
  independently reproduces and extends the lanes' fresh
  n8_diagonal_support12_27 DRUP certificates.

**Successor probes launched:** W8 (hybrid template-kill: singleton-
free templates at m >= 15 must die at the value level — O1 odd
holonomy / rank / SAT, in the lanes' certificate style; any survivor
is a concrete counterexample candidate and escalates immediately) and
W9 (the cell ceiling H4 itself: balance + local irredundancy +
(STAR)-pinning sparsity; calibrate against the committed near-exact
source first). Between them: W8 closes the band if value-level kills
are uniform; W9 closes it if exactness forces cell sparsity; if BOTH
fail on the same support, that support hosts the counterexample
search target.

---

## v9 addendum: W7 lands — Route T retired; salvage recorded (2026-08-15)

W7 (`computations/unaudited-tropical-w7-2026-08-15/`, unaudited)
closed 19,907 of 21,465 cells of the residual colour-form fan at N=8
(795 g-faces enumerated exactly) — and then proved the route cannot
finish: at N=6, where committed Theorem A makes T.1 true at every
weight, four residual cones carry genuine torus solutions of the
generator-level initial system (60-digit verification). The GHZ
generators are NOT a tropical basis, so cone-by-cone certificates are
structurally incapable of closing T.1. **Route T is retired.**

Corrections adopted: (1) my brief mis-cited the committed diagonal
result — the PENCIL equation is soluble for every k (committed
guard note); the insoluble system is the TERMWISE one, and W7's
chamber reduction corroborates exactly that theorem. (2) T.1's true
payoff is RIGIDITY, not emptiness: full success would show the
dense-cell stratum is empty or a finite union of gauge orbits
(Bieri–Groves) — worth having (it collides with any
positive-dimensional deformation family, trichotomy branch (iii)),
but "T.1 empties the stratum" is struck. (3) The singleton mechanism
is provably worthless on the dense family at N=8 (0/795 faces; no
content of multiplicity one) — the sharp reason six sites was easy.

Salvage kept: the exact fan; **Lemma H4** (symmetric zero-diagonal W,
N>=6, all off-diagonal entries nonzero, char != 2,3 => some 4-subset
hafnian is nonzero — self-contained, Groebner-verified at N=6, kills
the monochrome-favouring chamber at every order); the edge-vs-cell
reconciliation (the ceiling front's densest tested object has 51 of
252 cells; the dense-cell interior and edge-supports 19..27 are the
honest open gap — consistent with v8's band statement).

**Route ledger after nine probes:** I = the H4-ceiling/W8-kill pincer
(active, the critical path); II = lanes' certificate grind (active);
III paused; A delivered (balance + phase reduction); F delivered
(dictionary); T retired (salvage above). Fleet: W8, W9.

---

## v10 addendum: W9 lands — Door A (cell ceiling) retired; Route I goes hybrid (2026-08-15)

W9 (`computations/unaudited-cell-ceiling-w9-2026-08-15/`, unaudited,
REPORT.md in place) closed the ceiling question negatively, three ways:

1. **Counting route closed at 9/9 band supports.** The only proved
   cell bound (W6's budget, C(m) = 9m − 8·max(0,24−m)) is TIGHT —
   admissible band certificates attain it — and even the best
   conceivable slice-cover strengthening (|H| <= m−12) stays above
   the singleton-free price everywhere.
2. **Every mixed-equation route closed where tested.** Mixed-exact
   sources with cell count at or above the singleton-free price exist
   at 4/4 supports tested (Sigma_mix = 60/73/77/81 at m = 20/22/23/24)
   — so no ceiling provable from (STAR)/L1/L2/attachment/permanents
   can undercut it. The pure equations add exactly 0 constraints at
   value level on all six band templates (measured, control fires).
3. **(STAR) pinning points the wrong way**: it yields a conditional
   cell FLOOR (Sigma >= 72, Corollary W9-2), and W7's Lemma H4 closes
   its dense branch (M(v) is the 4-subset-hafnian matrix; complete
   W(v) forces M(v) != 0).

**Two corrections to W6's record (adopted):** (a) W6's Sigma_min
pinned beta at the budget floor, which is not forced — with beta free
the singleton-free price drops to 51..73 across the band (all 13 W6
certificates themselves re-audit correctly); (b) six of nine W6
certificates are W3-case-(D) degenerate, hence inadmissible as
minimal-counterexample templates; the honest case-(P) price is
51, 56, 63, 56, —, 63, 60, 74, 73 (m = 19..27).

**Calibration:** near-exact objects sit at 28–32% cell density
(Sigma/m ~ 3.0–3.4); STAGE_A's sparsity is a support degeneration
(empty pure fibres, 16/24 slots), not a sparsity law.

**New tools kept:** Lemma W9-1 (row death; proved, 682/702 fires with
0 violations); the **overdetermination slack** Sigma − r(T) + 3 −
J(T), resting on the rigorous gauge fact that a nonempty exact locus
carries a component of dim >= r − 3: it is +19 on the object that
exists and **−11..−14 on every band template** — every singleton-free
band template is value-level overdetermined.

**Route I is now hybrid with W8 the critical path**: the singleton-free
templates must die at value level, and the negative slack on all of
them is the quantitative reason to expect they do. Named follow-up
(W9's soft spot): exhibit a mixed-exact source with all three pure
fibres nonempty and a pure hafnian vanishing by cancellation, or prove
none exists — the clean finish for the C3/T4/T6 closure.

---

## v11 addendum: audit A2 lands — the (SC) admissibility correction (2026-08-15)

Adversarial audit A2 (`computations/unaudited-audit-a2-w6w2-2026-08-15/`,
unaudited, fully independent code — subset-DP fibre counter, HNF-based
O1, fresh SAT encodings) re-verified the W6/W2 layer and the W9 layer.

**Survives intact:** the budget + Hall arithmetic (confirmed, controls
fire, no hidden hypotheses — distinctness of the three slice-cover
neighbours is provable, not assumed); the m = 3N/2 forced-cube chain;
(EXP)/(STAR) — now verified over ALL 726 words on all 28 pairs with a
strengthening correction: **26/28 blocks recovered and the unpinned
pairs are EXACTLY P1's two witness pairs**; W2's entire exhaustion
layer (13 orbits, 28 full-support templates, all O1-dead — re-proved
by lattice membership; R_mon 174,048; B.3 third code path); m = 12
now killed directly (197,820 forced configurations, all with 2-6
singletons), independent of W2.

**The load-bearing discrepancy (D1): every zero-singleton certificate
in the campaign is inadmissible.** The committed slice-cover theorem
forces, at template level, condition **(SC)**: for every (vertex p,
colour r) some incident edge has all its cells carrying colour r at
the far endpoint. W6 imposed only the counting consequence
d_R(v) >= 3 and searched a class violating the original: its 13
Sigma_min certificates fail (SC) with 10-16 unservable slots — and
also violate W6's OWN budget (anti-diagonal 2-cell blocks are rank 2
by the rectangle criterion, forcing beta above what the certificates
carry). W9's beta-free and case-(P) sets pass the budget but fail
(SC) (3-10 unservable slots; case-(P) m=21 also fails Hall). W2's 28
templates pass (SC) — the test is not vacuous.

**Consequences adopted:**
1. Both Sigma_min rows (v8 and v10) are struck as prices of
   singleton-freeness for exact sources; they price an excluded
   class. v10's "counting route closed 9/9", "mixed-only closed
   4/4", and the −11..−14 slack table are all measured on that class
   and are **suspended pending (SC)-remeasurement**. Door A's status
   reverts from "closed" to "unresolved — possibly moot" (see 3).
2. W6 Result 1 struck (certificates exist at m = 14 — A2 saved a
   witness — and m=15's was never saved; none anywhere are
   (SC)-admissible). W6 Result 3's literal "any beta" form struck
   (SAT witnesses at m = 20..27); its admissible form is now PROVED
   exactly: **no (SC)-admissible zero-singleton diagonal template
   exists at any support <= 27** (cadical UNSAT, 51k clauses).
3. **The strongest position of the campaign:** under (SC), no
   zero-singleton template is known at ANY band support, three
   regimes are proved empty (diagonal <= 27 by UNSAT; R_cell <= 27;
   general m = 12 by exhaustion), and A2's best admissible search
   result is one singleton short at m = 27. If the general
   (SC)-admissible decision comes back UNSAT at m = 13..27, **Route
   I closes by singleton + (SC) alone — no cell ceiling, no
   value-level kills below 28** (m = 28's admissible zero-singleton
   templates are W2's, all O1-dead; the non-R_cell m=28 question
   remains to decide). W8 is re-aimed at exactly this per-support
   SAT decision. Honesty note: A2's admissible annealer failed its
   positive control, so its empty-handed searches carry no weight —
   the SAT decisions are the evidence that counts.
4. Provenance flag on R_mon's "implied by the blocking chain"
   (downstream of the abandoned pre-v6 hypothesis; the regime
   results stand on their own exhaustions).

Fleet: W8 re-aimed (per-support (SC)-admissible SAT decision, then
kills on real survivors only), W10 updated (grade conclusions by
(SC)), A1 (W3 audit) and A3 (uniformity) unchanged.

---

## v12 addendum: audit A1 lands — W3's GIT half confirmed, modulus half struck (2026-08-15)

A1 (`computations/unaudited-audit-a1-w3-2026-08-15/`, independent
exact re-derivation, 16/16 mutation controls killed):

**Confirmed and now double-derived:** crux lemma L1; Theorem A.1
(both branches, exclusivity, the 21 balance conditions); Corollary
A.2 (WLOG balanced — measure is CELLS); the independent-four-set
identification with a 537,355-graph exhaustion re-proved by an
independent fpm-polytope route; the eps striking and the closed-orbit
prism collapse. W9's case-(D)/case-(P) admissibility filter is sound.

**Struck:**
1. **The phase-only reduction (v5) is refuted.** W3's certifying
   script was a tautology (D1), and A1 built an exact 13-cell n=8
   witness with NO singleton mixed fibre whose coupled fibres force
   the modulus condition |a1 a4| = 2|a0 a6| — solvable over Q with
   general moduli, impossible with all moduli 1 on the entire gauge
   orbit. The licence "searches may fix all moduli to 1" is
   WITHDRAWN: the all-ones point is an equilateral ansatz of
   codimension |S| - 3n, not a normalization. (W1's v6.1 over-C
   ceiling stands via the elementary singleton bound; citation
   corrected.)
2. **Route II warning (D3):** W3's potential descends in cells, not
   blocks; its "19->16 block reductions" were colour-class
   reductions at fixed aggregate support 28. The cell potential is
   not a block-support ratchet.

**Critical-path impact: none.** The (SC)-admissible singleton
decision (v11) is support-level; O2 is elementary over C; balance
(A.2) — the only W3 input the current chain uses — is the part that
survived with an independent second derivation.

---

## v13 addendum: A3 lands — uniformity restructured; N=8 path unchanged (2026-08-15)

A3 (`computations/unaudited-uniform-n-a3-2026-08-15/`, unaudited)
delivered the node-4 groundwork. Four headline items:

1. **The uniform singleton statement is dead, twice over.** (i) An
   explicit family F_n of monomial templates (one for every
   N = 0 mod 4; F_4 IS the committed K_8 counterexample) has three
   nonzero pures and no singleton mixed fibre — proved uniformly
   (Theorem A3.1). (ii) The v11-shape statement "(SC)-admissible +
   below full support => singleton" is REFUTED at N=10: six
   certified (SC)-admissible diagonal singleton-free templates at
   supports 31..43 (of max 45), verified by three disjoint engines
   including W2's, all dying by O1 odd holonomy. "Singleton-free
   only at full support" is an N=8 artefact. **The N=8 decision is
   unaffected** — A3's calibration control reproduces the committed
   N=8 emptiness at 12..27 — but the per-support SAT route has no
   uniform analogue (R5: the singleton-free region reaches >= 14
   supports below the top already at N=10).
2. **The uniform mechanism is identified and partly proved: the
   Perm-K_{2,3} odd circuit** (char != 2: a 2x3 all-nonzero matrix
   cannot have all three 2x2 permanents zero — the canonical form
   of the committed note's §3 obstruction). Theorem A3.3 kills F_n
   for every n with no enumeration; Theorem A3.3' states the
   general circuit (its complement-splitting hypothesis (c) is
   where the remaining difficulty lives). Corrected uniform shape:
   **singleton below a threshold m*(N), odd circuit above** (R1a +
   R1b), with every known singleton-free object O1-dead.
3. **Two uniform theorems proved and exhaustively verified**
   (161,148 charts at N = 6,8,10, every proof branch exercised,
   sharp at N=4): the FOURTH-MATCHING THEOREM for properly
   3-edge-coloured cubic graphs, killing the support floor m = 3N/2
   for EVERY even N (the committed cube-chart kill is now derived
   uniformly), plus m = 3N/2 + 1 and the even-cycle-free class.
   Also: (SC) re-derives W6's budget (2*beta + #constant-sided
   multi-cell edges >= 3N) — the budget's conceptual home.
4. **Interface verdicts:** Theorem B (descent) is genuinely
   N-uniform (proof body clean of N=8 facts). P1's minor law is
   N-uniform. But **the blocking taxonomy is intrinsically h = 3**
   (cap errors are degree-h forms; Lambda^4 of a 3-space vanishes,
   so no determinantal obstruction exists at N >= 10) — residual
   **R4 (taxonomy repair)** is the hard open core of witness theory
   at higher order.

**Recommended U(N) (adopted):** witness existence at MINIMUM even
order — the committed descent target with the free minimality
hypothesis added — assuming balance (audit-survived), m >= 3N/2 + 2
(now proved), and the all-blocked reduction. The full-conjecture
architecture is therefore: **N=8 by the (SC) singleton decision
(W8/W11, running) + descent (N-uniform, audited) + U(N) for N >= 10
(open; mechanism = R1a/R1b ladder in the monomial stratum, R4 for
the witness theory beyond it)**. R2 (parity dichotomy) is recorded
as refuted so nobody re-derives it; A3 withdrew its own non-(SC)
Sigma_min numbers (same class error as W6 — the discipline holds).

---

## v14 addendum: W8 lands — band closed through 17; the thick-fibre regime is the final open (2026-08-15)

W8 (`computations/unaudited-template-kill-w8-2026-08-15/`, unaudited;
DRUP proofs + independently verified kill certificates) ran the
(SC)-admissible sweep. Verdict, per support at N=8:

- **m <= 15: closed by singleton + (SC) alone** (31/31 orbit UNSAT,
  DRUP; the admissible zero-singleton threshold is **16**, correcting
  v11's "none known at any band support").
- **m = 16: closed** — exactly 12 admissible zero-singleton
  templates (2 classes up to S8 x S3, complete enumeration), both
  classes killed by O1.
- **m = 17: closed** — 31/31 orbits UNSAT after 9,900+ verified
  value-level kills; independent enumeration cross-check (564
  templates, 77 classes, all killed).
- **m = 18, 19: zero survivors seen, not exhausted** (finishing job;
  W9-1 row-death preprocessing is the named accelerator).
- **m = 20..28: certified survivors exist, and their immunity is a
  THEOREM**: any template with nonempty constant fibres whose mixed
  fibres all have size >= 3 defeats the entire lattice machinery
  (O2/O1/one-live-class/K3) — no binomial relations can ever be
  generated. The construction (12 single cells + nine-cell blocks
  carrying two disjoint 4-cycles) exists at every support 20..28 and
  the bound m >= 20 is sharp. These are **certificate gaps, not
  counterexample candidates**: all 34 measured admissible
  zero-singleton templates, survivors included, have negative
  overdetermination slack (-7..-14).

**The N=8 endgame is therefore three concentric jobs:** (i) finish
18/19 (computational); (ii) kill the thick-fibre regime 20..28 with
NON-lattice methods — the value systems there are honest polynomial
systems (every mixed fibre a sum of >= 3 monomials), so the tools are
(STAR) pinning (audited), W9-1 row death, W5's L1/L2, witness
existence via the P1/P2 decide_pair machinery (a witness on a
survivor descends it to N=6, dead), and Groebner escalation; (iii)
audit-promote the certified layers. Convergence note: the thick-fibre
value systems are exactly W10's object (mixed-exact + nonzero pures),
so W10's N=6 verdict will calibrate (ii) directly. **W12 launched**
on (ii) with the support-20 survivor (Sigma 58) as first target.

W8/W11 comparison pending — W11 remains firewalled and its
independent per-support verdicts will cross-validate the SAT layer.

---

## v15 addendum: W11 lands — the SAT layer is double-derived; proof-file hazard found (2026-08-15)

W11 (`computations/unaudited-sat-pair-w11-2026-08-15/`, firewalled:
encoding derived from the committed definitions only, W8's directory
opened only after all verdicts were fixed) reports:

1. **Exact agreement with W8 on everything**: threshold 16; m <= 15
   empty (independent DRUP, all RUP-verified); at m = 16 the
   identical complete census — 12 templates, 2 orbits, Sigma 34/40,
   same block shapes — from a completely different decomposition
   (12,346 support-graph iso classes vs W8's 31 constant-witness
   orbits); SAT at every 17..28; diagonal <= 27 empty across all
   2,589 classes; m = 28 non-single-cell SAT. The certified rungs of
   the N=8 ladder (v14) are now independently double-derived, which
   is the audit-grade standard for this layer.
2. **(SC+)**: the support shadow of the committed activity clause
   (complement of a serving edge must carry a perfect matching) is a
   legitimate free strengthening — it flips individual classes but
   not the threshold, and the m=16 pair survives it.
3. **Cross-lane tooling hazard (own note:
   `notes/2026-08-15-pysat-cadical-proof-truncation-hazard.md`)**:
   pysat's cadical get_proof() truncates proofs; 7 of W8's stored
   DRUP files fail replay. W8's verdicts re-solve UNSAT under three
   solvers and verified replacement proofs are stored in W11's
   w8_reproofs/. Every certificate-emitting lane must re-check
   proof-file integrity.
4. Soft spots to carry: the J.1d budget is not in either encoding
   (worth one pass over the 44 witnesses); the faithful activity
   clause is value-level and belongs to the kill layer, not the
   template decision.

Status unchanged from v14 otherwise: 12-17 closed (templates by
decision, values by W8's exhaustive kills), 18/19 finishing, 20..28
thick-fibre (W12 running, now with W11's 44 verified witnesses as an
enriched target list — W12 should also apply (SC+) as a free filter).

---

## v16 addendum: A3 closes its soft spots — F'_n and m*(10) = 31 (2026-08-15)

A3's addendum upgrades v13 in two places: (1) an explicit
construction F'_n (a one-vertex parity-defect variant of F_n) gives
(SC)-admissible singleton-free monomial templates at every
N = 2 mod 4, verified at N = 10 (reproducing the search certificate
exactly) and N = 14 — so combined with F_n, **explicit singleton-free
templates exist at every even N >= 8**, by construction; the
parity-dichotomy conjecture is definitively retired. (2) The N = 10
threshold bracket is closed: **m*(10) = 31** (nothing at 24..30, hit
at 31), so the gap C(N,2) − m*(N) goes 0 → >= 14 from N = 8 to 10.
Both firm up the v13 architecture: the induction must run through
the odd-circuit mechanism (R1b, now with F'_n added to the family
the proof must cover — W13 informed) and the witness statement U(N).

### v16.1: W11 final update (2026-08-15)

(SC+) complete: threshold 16 under both admissibility readings; no
support in the band empties. W11's m=28 single-cell census control is
a lower bound (15, budget-cut), not a discrepancy. W8 proof-file
audit still counting (7 failures so far; mathematics re-confirmed).
One live caveat adopted as a W12 task: run the J.1d budget
(beta >= 24 - m + |H|, rectangle-forced |H|) over the 49 witnesses —
a budget violation is a free template kill.

---

## v17 addendum: W13 lands — R4 answered, the L_h law, and the uniform circuit (2026-08-15)

W13 (`computations/unaudited-induction-w13-2026-08-15/`, unaudited;
9/9 mutation controls) delivered the induction's mathematical core:

1. **R4 is answered positively.** The determinantal obstruction was
   only the equivariant shadow of the true law: **E_w always lies in
   L_h(A_pq) = Sigma_h + s Sigma_{h-1} + ... + s^{h-2} Sigma_2**
   (Cauchy permanental components) — at every order, with growing
   codimension (9, 29, 134, 485 at h = 2..5). It explains P1's
   unexplained "generic span 136" exactly, subsumes P2/W4's h=2 laws
   and FACT 1, and has a clean geometric form (apolarity: order-(h-1)
   vanishing along A_pq on the Segre). Consequence: **the blocking
   taxonomy survives to every N and blocking gets relatively harder**
   — only the 3(h-1) monochrome monomials can block at full-rank
   pairs (two kappa-colours NEVER block; s^h iff det A_pq = 0, now
   exact — also sharpening N=8, where kappa_c^2 kappa_c' is newly
   excluded). Caveat: single-cell pairs (R_cell) degenerate the
   taxonomy — apply pair by pair there.
2. **R1b is proved for both explicit families at every even N >= 8**
   (Theorem W13.6; the K_{2,3} circuit survives F'_n's defect;
   machine-checked to N = 50). Every explicitly known singleton-free
   object at every even order is now O1-dead by a uniform theorem.
   Exact reformulation: R1b = "R_cell forbids W8's immunity shape";
   no counterexample in 8,701 matching-rich splittings; the
   singleton-free stratum at N=10 is isolated (local search
   structurally cannot reach it).
3. **U(N)-W13 + the single next lemma.** Provable now: at every
   full-rank pair of a minimal blocked source the degree-h
   certificate is monochrome. The one missing step to make W5's
   slice work transfer uniformly is the **monochrome-transfer lemma**
   (s^a kappa_c^{h-a} in the error span => colour-c slice dirty;
   evidence 3/3 at h=3). Gap B remains: higher certificate layers
   (blocking degrees 2..5) need a saturation argument.

**W14 launched** on the monochrome-transfer lemma + Gap B. The
induction now has: descent (audited, N-uniform) + floor kills
(proved all N) + the L_h taxonomy (all N) + the uniform circuit for
the known singleton-free landscape + two named residuals
(monochrome transfer; general R1b).

### v17.1: W11 closing — certificate audit conclusive; one debt item (2026-08-15)

W11's audit of W8's stored proofs is final for the checkable
families: 7 of 62 fail replay, all by the (silent) pysat truncation,
all 7 re-solved UNSAT by three solvers with verified replacements
stored. Sharpened hazard: passing files do not vindicate the
extraction method — replay is mandatory. New debt item for the
audit-promotion queue: the m=17 closure proofs (~66.5M lines) are
unaudited at scale — verify with drat-trim or regenerate with
solver-native proof writing before promotion. Headline unchanged:
threshold 16 under both readings; m=16 census identical across both
lanes; the J.1d budget check over the 49 witnesses remains assigned
to W12.

---

## v18 addendum: W12 lands — the thick-fibre regime falls to the cut; one residual family left (2026-08-15)

W12 (`computations/unaudited-thickfibre-w12-2026-08-15/`, unaudited)
broke the immunity: **cutting the site set in half turns thick fibres
into binomial half-fibres** — thickness is a property of whole-B
fibres and is not preserved by cutting, which is exactly the blind
spot of W8's immunity proposition. Results:

- **Everything known at N=8 is killed — 130/130**: the m=20 CEGAR
  survivor (three independent routes, including an eight-word
  hand-checkable certificate via a new mechanism — two fibre
  polynomials proportional modulo the binomial relations, one mixed
  and one constant); W8's immune construction at m = 20, 21 (a
  three-line crossing-parity factorisation kill), 22, 23 (cut
  extraction); all 47 W11 witnesses (< 1 s each); all 77 W8 m=17
  classes as an independent positive control. No target anywhere was
  found feasible.
- **Uniform tools, general N** (audit-promotion candidates): Theorem
  W12-A (split kill), Theorem W12-B (cut extraction — pinned left
  sub-words force right half-fibre equations, which are binomial at
  |R| = 4), Proposition W12-C (a feasible cut exists iff the graph
  Gamma of full nine-cell blocks is NOT spanning 2-connected — the
  predicate matches the outcome on all 135 targets), Corollary W12-D
  (the residual costs m >= 20, Sigma >= 84 — the cell-expensive
  corner far above the singleton-free prices).
- **The last open object at N=8 is now exactly one family, (R)**:
  thick templates whose full-block graph is spanning 2-connected —
  known instances: W8's construction at m = 24..28 only. Partial
  structure already forced (half-permanent binomials; two blocks
  rank-one); the residual identity has honest all-nonzero solutions,
  so (R) needs the witness instrument: every (R) pair is multi-cell
  full-rank, which is precisely W13's taxonomy hypothesis.
- **New exact structural fact** (recorded; apparently absent from the
  notes): an exact d=3 source restricts to an exact d=2 source on
  the same sites for every colour pair. Float evidence says d=2
  sources exist at N=8 (consistent with the known k=2
  achievability), so the lever does not close N=8 by itself.
- Free filters over all targets: (SC+) fails on 21; the J.1d budget
  fails on 0 (W11's term-rank guess confirmed).

**W15 launched on residual (R).** N=8 status after W12: m <= 17
certified closed; 18/19 zero survivors seen (finishing); 20..23
closed by W12; **24..28 = family (R), the single remaining question
of the open case.**

---

## v19 addendum: W10 lands — the fork resolves EXISTS; no-slack lemma for (R) (2026-08-15)

W10 (`computations/unaudited-mixed-exact-pure-cancellation-w10-2026-08-15/`,
unaudited) decided the mixed-exact pure-cancellation question:

1. **EXISTS, everywhere, maximally**: mixed-exact sources on fully
   admissible (T4/T5/T6/S) templates with all pures vanishing by
   cancellation exist at every support (N=6: 9..15; N=8: 12..28) at
   the maximum cell count Sigma = 9m — via A_uv = t_uv J and
   haf(t) = 0, certified symbolically over Q. Hence **Door A is
   closed unconditionally on the (T4/T5/T6/S) layer** in the
   strongest form (no nontrivial ceiling is provable there), and
   **(SC) is the only template ingredient any ceiling argument may
   still use**.
2. **Lemma W10-G (adopted; sharpens P2 fact 5)**: mixed-exact with
   all three pures nonzero = fully exact up to gauge WITH THE SAME
   TEMPLATE. Consequences: every mixed-exact six-site source loses a
   pure (W10-6); mixed-exactness alone does not force (SC) but
   mixed-exact + pures-nonzero does; and **the (R) survivor systems
   carry no slack — "mixed = 0, pures != 0" IS the exactness
   question**; a feasible point there is a counterexample outright.
3. **Correction in H4's favour, without reopening it**: all W6/W9
   Sigma_min certificates violate (SC), so the recorded prices
   under-estimate the honest (SC)-stratum price Sigma_min+; but
   singleton-free ADM+(incl. (SC)) templates exist at Sigma =
   65/71/87 (m = 21/24/27), still below the best budget — counting
   stays closed.
4. **The (R) survivors pass all five filters including (SC)** — no
   free kills remain; and W10's control-calibrated numerics show a
   six-order separation between the mixed system (solvable to 1e-10)
   and mixed + pures (stalls at 6.6e-4): **the pure equations are
   the obstruction**, exactly as W10-6 predicts at six sites. W10's
   own value probes were honestly inconclusive (four variants, four
   documented control failures).
5. Also recorded: Delta_{N,2} for every even N (exact cycle
   construction); the N=6 taxonomy of nonzero-pure counts; the
   restriction lemma.

Fleet: W14 (monochrome transfer), W15 ((R) kill — briefed with
W10-G's no-slack equivalence and the pure-equation target).

---

## v20 addendum: prior-art sweep S1 — verdicts on the three (R) ideas (2026-08-15)

A read-only sweep (55 term passes over the 2,259-file notes corpus +
the route registry + all probe reports) graded the three candidate
ideas for family (R):

1. **Witness-forcing via taxonomy: TRIED-AND-LIVE — it is the
   current critical path, and its strongest form has never been
   assembled.** New composition now available: W14 (running) has
   proved the transfer lemma's positive half (evaluation principle —
   a clean colour-c slice forces f(E_cc) = 0 for the whole degree
   layer of the ideal) and found an exact counterexample to the
   unrestricted form (residual case a >= 1 with A_pq(c,c) = 0,
   striking W13's "removes EVERY" phrasing — corrected hypothesis:
   s_c != 0). **On (R) pairs the counterexample regime cannot occur**
   (full nine-cell blocks => all diagonal cells nonzero), so: at an
   (R) pair with a clean colour-c slice, no {s, kappa_c}-monomial of
   ANY degree lies in the radical of the error ideal; all three
   slices clean => every surviving certificate needs >= 2 distinct
   kappa colours, excluded at degree h by W13-T2 — the operative
   residual is mixed-kappa certificates ABOVE degree h (Gap B). S1
   measured four all-three-clean Gamma-pairs on the m=24 instance
   (support-forced). Also fixed a terminology hazard: three distinct
   meanings of "clean" (slice-/word-/cut-) and two of "witness" now
   in circulation — future notes must qualify.
2. **Multi-cut/pinning consistency: effectively closed.** Registry
   route OC1 negatively closed bare <= 3-cut consistency with
   coexistence countermodels ("a continuation must use at least four
   overlapping cuts... or another global invariant"); the
   chart-square overlap architecture failed by exact rank deficiency
   (consistent, not overdetermined); A2's calibration shows (STAR)
   pinning is perfectly consistent on the near-exact source; W7's
   Lemma H4 immunises dense supports against (STAR) block-killing.
   Only the cross-pair fixed-point closure is genuinely untried —
   lowest expected value; do not budget it.
3. **Ear/brick-brace/tight-cut on Gamma: PARTIALLY ADJACENT with a
   genuinely new opening.** The U7H import (2026-08-13) brought the
   matching-covered/tight-cut/brick-brace theory but aimed it at
   Problem 2's lattice, never at templates or Gamma; three recorded
   counterguards warn against graph-structure-only arguments, and
   the 3-connectivity filter measured 0% pruning at m >= 24 — but
   that measurement concerns the SUPPORT graph, and Gamma is sparse.
   NEW: Gamma at m=24 is matching-covered, non-bipartite, NOT a
   brick, with EIGHT odd-shore tight cuts — and W12's even_cuts()
   structurally cannot test odd shores. Family (R) is defined by the
   absence of feasible EVEN cuts; odd tight-cut CONTRACTION (every
   perfect matching crosses exactly once => H decomposes as a sum
   over the crossing edge of two contractions) is the untested
   complement. Fed to W15 as the fallback mechanism.
4. **"Pure-from-mixed forcing": already the working kill mechanism**
   (W12's m=20 certificate; an older committed instance in the
   orbit8 boundary-repair note; and — observed in W15's live logs,
   formal report pending — a completed Singular-verified kill of the
   (R) instance at m=24 by exactly this route). Rank counterweight
   recorded: the pure differentials lie in the mixed span
   generically, so these kills are exact ideal-membership
   statements, never rank arguments.

Cross-feeds sent: the sharpened composition + odd-tight-cut opening
+ OC1 warning to W15; the corrected-hypothesis audit note to A5. S2
(induction-side prior art) still running.

---

## v21 addendum: prior-art sweep S2 — the induction-side verdicts (2026-08-15)

S2 (read-only sweep, coverage stated in its report) on the three
induction lemma targets:

1. **Degree bounds (Gap B): ANSWERED TODAY IN FLIGHT, and the answer
   redirects the lemma.** Castelnuovo-Mumford regularity was never
   invoked in the repo by name — but W14's Task 2 computed the
   operative fact: universal (A_pq-only) certificate exclusion
   exists ONLY at degrees h and h+1 (codim 29 -> 1 -> 0 at h=3;
   verified against P2's fleet, 37,572 degree-3 certificates, 0 law
   violations; the degree-(h+1) obstruction has the closed form
   phi_A = q_A^2 - 4<K, cof A> det K). From degree h+2 every
   L-monomial is in the universal layer, so **no layer-level degree
   bound can exclude high-degree blocking — any Gap B lemma must be
   source-dependent.** This makes S1's evaluation-principle
   composition (kills {s,kappa_c}-monomials at EVERY degree in the
   radical, on clean-slice full-block pairs) the only available
   above-(h+1) exclusion — reinforcing its critical-path status.
   Effective-Nullstellensatz routes were tried three times,
   bounded-only, and sit on the do-not-reopen list. RECORD FLAG: the
   "blocking degrees 2..5" claim needs reconciliation — P2's stored
   histograms cap at max_degree=4 (with a None bucket) while P1's
   saturation_verdicts.json contains degree-5 monomials; re-derive
   before sizing anything against "degree 5".
2. **General R1b: TRIED-AND-BOUNDED, and the boundary is razor-thin.**
   Four artifacts pin it: the binomial-incidence countermodel (the
   +/-1-signing form is FALSE without nonzero constant FIBRE SUMS —
   and its closing sentence warns the strengthened form "is
   essentially the remaining binomial-support case of the Krenn
   problem rather than a support-only incidence lemma"); the U7D
   witness (odd CYCLE with holonomy -1 is not enough — the relations
   must reach an odd HANDCUFF in Zaslavsky's frame lattice; the
   trivial-dependency clause of O1 cannot be weakened); W8's
   immunity theorem (unrestricted R1b is FALSE — the R_cell
   hypothesis is essential, as W13 scoped); and the signature
   counterguard (unsigned support data cannot decide O1 vs O2). The
   holonomy programme already frames the true statement: Bogdanov is
   the pi_0 level and R1b-general is the H^1 level of one theory
   (Problem 2's conjecture). Calibration: R1b-general should be
   treated as HARD (adjacent to the problem itself), and the
   families + R_cell-threshold version (proved/in hand) as the
   realistic induction input.
3. **The Bogdanov strengthening IS A3.3'(c), already named.** The
   closest prior attempt (termwise-rank3 profile classification)
   proves the k=3 case closes over any field and shows k >= 4 is "a
   genuinely order-specific accident" — the forcing must bite at
   size-4 profile parts, exactly where measured cancellation lives;
   the note states the missing piece verbatim: "a quantitative
   version of that tension — enough non-anchor edges to cancel
   with, few enough to keep all the co-supports empty." Uniform
   counterguards close graph-only routes (girth-10 Heawood voltage
   cover; the literal K_{2,3} support core with an explicit all-unit
   escape). CITATION HYGIENE: A3.4 is mathematically Bogdanov
   restricted to simple cubic graphs (the repo has a documented
   false-novelty incident on exactly this shape); CG's "crossing
   pairs"/"drums" vocabulary already covers the K_{2,2}
   configuration — commit A3.4's artifact WITH those citations, no
   novelty claims.
4. Bonus recorded: the uniform-statement fate table (14 entries);
   the N=8->N=10 cylinder-contraction frontier ("cross-edges
   incident to the two new vertices remain the precise obstruction";
   the five-cross census closed <= 3 cross coordinates, frontier at
   4); and a convention trap — the old spine uses N = 2h while the
   witness campaign uses h = N/2 - 1 (the two h's differ by one;
   qualify in every new note).

---

## v22 addendum: W14 lands — repaired transfer proved degree-free; Gap B closed-form; the rank-one re-basing (2026-08-15)

W14 (`computations/unaudited-monochrome-w14-2026-08-15/`, unaudited,
all-exact) delivered:

1. **The transfer lemma as conjectured is FALSE; the repaired form is
   PROVED at every degree.** Evaluation principle (W14.5): a clean
   colour-c slice puts E_cc on the error variety, so no L-monomial
   surviving at E_cc lies in the ideal at ANY degree — kappa_c^d
   unconditionally; s^a kappa_c^b and s^d iff A_pq(c,c) != 0. The
   counterexample regime (a >= 1, A_cc = 0) is exact and forced.
   W13's 6/6 evidence explained (its sources satisfied a strictly
   stronger hypothesis). Directness of the graded decomposition
   proved at full rank (fails below).
2. **Gap B answered:** universal exclusion lives only at degrees h
   and h+1 (closed forms: det at h=2, the discriminant form phi_A
   at h=3); nothing above. **T2 is false one degree up in measured
   data** (314/316 minimal degree-(h+1) certificates are
   multi-colour) — so GAP B1 (certificates need not be monochrome)
   is a REAL hole in any taxonomy-based witness-forcing chain,
   including the (R) composition of v20: on (R) pairs, clean slices
   kill all monochrome certificates at all degrees, but
   multi-colour certificates from degree h+1 remain possible.
   RECORD CORRECTION adopted: P2's "blocking degrees 2..5" is not
   reproducible (max_degree=4 throughout); the D(3)=5 folklore is
   withdrawn pending a real degree-5 certificate.
3. **The strategic re-basing (adopted as the primary witness
   instrument):** rank-one caps are admissible, so blocking forces
   EVERY admissible scalar slice (4 projective parameters, W5's
   closed form) to be dirty — no ideal, no taxonomy, no degree
   bound, and measured LOSSLESS on P2's fleet (29/29 witness pairs
   have rank-one witnesses; 0/91 blocked pairs do). The chain's
   remaining question becomes purely W5-shaped: **can the whole
   scalar-slice family be dirty at every pair of an exact source?**
   For family (R): a witness at an (R) pair can be sought DIRECTLY
   as (u,v) with u_c v_c != 0, u^T A_pq v != 0, and W5's scalar
   slice error zero — relayed to W15.

U(N) chain state: steps 1, 2, 4 proved; B1 (open, now known
typical), B2 (boundary), A' (J.1b-SUPPORT), D (pair existence) are
the named gaps — with the re-basing collapsing B1/B2 out of the
chain entirely if the scalar-slice question resolves.

---

## v23 addendum: W15 lands — m=24 of family (R) is dead; the ladder narrows to 25..28 (2026-08-15)

W15 (`computations/unaudited-residual-w15-2026-08-15/`, unaudited,
float-free) formally killed the m=24 instance — W12's "honest
blocker" — by the Phi-forcing mechanism W15-A (effectively-clean
words; the constant word 0^8 is effectively clean at m=24, its clean
binomial shape collapses under six mixed equations, and a seven-word
hand certificate with occupied-cell multiplier proves H_{0^8} = 0 —
exactly W10's the-pures-are-the-obstruction prediction, and the
first mechanism that ignores Gamma's 2-connectivity). Doubly
verified with leave-one-out minimality and the decisive non-vacuity
control (the clean subsystem is exactly feasible; Phi vanishes
identically on it). W12's residual identity is BYPASSED, not solved.

**N=8 ladder now: m <= 23 closed, m = 24 closed, m = 25..28 open.**
W15's sharp blocker map for the rest: k=0 (constant-word route) is
closed at 25+ (added cross blocks complete the extras); k=1 (mixed
word with one extra) is the designated route at 25..27 (1406/1438/
719 target words; the clean layer currently yields a rank dichotomy,
not a collapse); k=2 (binomial re-entry) is designated at m=28
(extras always even). Odd tight cuts exist only at m <= 25. The
rank-one scalar witness search must use W5's slice_core predicate
(W15's support proxy is NOT that invariant — definitional handoff
recorded). Largest open item: (R) IS NOT ENUMERATED — whether W8's
family is all of (R) remains to be decided (SAT + the |Gamma|=8 =>
C_8 case). W16 launched on all of this. Singular tooling hazard
recorded (reserved identifiers e1/mult/I; leading unary +).

---

## v24 addendum: audit A4 lands — the cut layer is promotion-ready (2026-08-15)

A4 (fully independent engine, exact incl. Q(i)) audited W12 and
W10-G: **every mathematical claim CONFIRMED, zero refutations** — the
first audit of the campaign with no mathematical discrepancy. W12-C
upgraded from 4,000-graph sampling to an exhaustive extremal PROOF
(N = 4..10; the old evidence never touched dense graphs). The m=20
survivor certificate re-verified three independent ways with
leave-one-out strengthened to explicit witnesses. W10-G shown easier
than billed (any gauge preserves mixed-exactness; the three
normalisations decouple exactly). Reduction soundness scoped
precisely (valid over C; the untested elementary-divisor branch
behaviourally verified to return undecided, never killed).

Six discrepancies, all evidence-side: the 48th W11 witness had no
recorded verdict anywhere (A4 killed it independently — 130/130
stands, now fully evidenced); two of W12's control files were never
written (C1/C2 round-trips unevidenced — re-run on promotion); the
negative control's non-vanishing half is vacuous as phrased; the
star cleanness test is conservative (exact criterion yields strictly
more equations — 156 vs 152 — swap recommended, RELAYED TO W16 for
the m=25..27 k=1 route); W12-C's old evidence gap; two new Singular
traps added to the conventions ledger.

**Promotion queue updated:** W12-A/B/C (with the extremal-proof
replacement and exact-cleanness swap), the m=20 certificate, and
W10-G/W10-6 are audit-cleared. Remaining under audit: A5 (W13), A6
(W15's m=24 + W14).

---

## v25 addendum: audit A5 lands — the L_h core is proved; T2 refuted as stated, repaired (2026-08-15)

A5 (independent code from the descent note alone; exact throughout)
audited W13:

**Confirmed as the solid core:** the configuration expansion (run
for the first time from eq. (4) exactly as written), the L_h law
with exhaustive exact membership through h=4, tightness, the
apolarity picture (det unique at h=3, nothing A-independent at h=4),
the K_{2,3} circuit theorem (reproduced with honest difference
vectors and the parity logic verified invariant under orientation
flips), the slice bridge W13.7, and T1/T3.

**Refuted: T2 as stated.** An explicit full-rank, no-zero-line
witness (a permutation matrix) admits the two-colour degree-3
certificate kappa_0 kappa_1^2 — hand-checkable, reaching the real
error span of actual sources (a genuine two-colour degree-h blocking
certificate). 17% of the no-zero-line 0/1 stratum violates. A5
derived the EXACT corrected law (three forced zeros) and the
repaired hypothesis: **A_pq with no zero entry** (0 violations on
220 matrices + a weight-space mechanism argument). Consequences:
U(N)-W13 and the "N=8 sharpening" inherit the repaired hypothesis
(P1 is vindicated — its inability to exclude kappa_c^2 kappa_c' was
correct); **family (R) is exactly safe** (full nine-cell pair blocks
have no zero entry) — relayed to W16 with the warning never to apply
T2 at sparse pairs. The transfer-protocol corrections reproduce
W14's independently. Method lesson adopted into the conventions
ledger: "NEVER" claims need exhaustive small-stratum sweeps, not
random batteries. Open: whether an EXACT source can carry a
T2-violating sparse pair block (the refutation stands against the
theorem as stated).

Audit column status: A4 clean-confirmed (v24); A5 = core proved +
one taxonomy claim repaired; A6 (W15 m=24 + W14) still running.

---

## v26 addendum: audit A6 lands — the audit column completes (2026-08-15)

A6 (fully independent, exact) audited W15's m=24 kill and W14's
theorems:

1. **The m=24 kill is promotion-ready and STRONGER than advertised.**
   All load-bearing content confirmed (template, fibres, the
   binomial shape — on all 2,952 effectively-clean words, more than
   W15 counted — the parity argument for 0^8, membership by three
   routes, non-vacuity by an independent from-scratch solution).
   One headline sub-claim refuted: w4 is redundant — **the canonical
   certificate is now SIX words** (five mixed + constant, 27
   monomials, smaller multiplier, each word proved load-bearing
   twice). W15's "6/6" control tested its multiplier, not the word
   set. Promotion should ship A6's six-word form.
2. **W14 upgraded twice**: the directness theorem W14.3 now has its
   general-h PROOF (A6 closed the gap: T((I_Segre)_h) = S^{h-1},
   machine-checked) — the graded projection is a theorem at every
   order; and phi_A ⊥ J_4 is now proved symbolically in Z[A]
   (correction: the char-poly identity carries det(A)^2). W14.5
   confirmed as the degree-free evaluation homomorphism (soften its
   "iff"; correct reading of the refuted transfer lemma:
   "unprovable without exactness").
3. **One motivation cut to size**: the rank-one losslessness behind
   the re-basing is real but thin — 18 informative pairs from 3
   sources at h=2 (11 of 29 vacuous; 9 sources run, not 70). W17's
   T1 (prove losslessness at h=2, or find the gap) is therefore the
   load-bearing check, and W17 has been re-briefed.

**Audit column complete: A4 (clean), A5 (core proved + T2 repaired),
A6 (promotion-ready + two upgrades).** Every structural theorem
audited today survived; every refuted item was a headline
overstatement with an exact repair. Promotion queue now: W12-A/B/C +
m=20 certificate + W10-G/W10-6 (A4), the L_h law + circuit theorem
(A5, with T2's no-zero-entry repair), the m=24 six-word certificate
+ W14.3 + W14.5 (A6). Attack fleet: W16 ((R) 25..28 + enumeration),
W17 (scalar-slice), W18 (18/19).

---

## v27 addendum: W17 lands — the re-basing is lossy; h=2 solved; h=3 criterion; predicate corrected (2026-08-15)

W17 (`computations/unaudited-scalar-slice-w17-2026-08-15/`,
unaudited, float-free) settled the scalar-slice question with a
refutation and two theories:

1. **The rank-one re-basing (v22) is REFUTED as an equivalence** —
   lossy at h=2 (17/1,144 pairs; 5/288 whole sources), at h=3 (7/7
   constructed pairs), and worst near exactness (39.8% of witness
   pairs; one 99.59%-satisfied source with 9 witness pairs and 0
   rank-one). W14's losslessness sample is reproduced exactly and
   was simply too narrow (as A6 warned hours earlier). **Downgraded
   to a cheap sufficient search**; the chain requirement returns to
   GENERAL caps (P2's decide_pair as the two-sided instrument).
2. **h=2 is completely solved** (Theorem W17.1) with the geometric
   reading that witnesses need a codimension-6 coincidence —
   *proving* generic blocking. **h=3 has an exact finite criterion**
   (W17.6) with hard structure (W17.4: a clean rank-one cap with
   nondegenerate sites forces every internal block to rank <= 2 —
   whence rarity, codim >= 110, and the explanation of the h=3
   losses AND of why near-exact objects, which are deeply
   degenerate, are exactly where rank-one works).
3. **Predicate correction (urgent, relayed to W16):** W5's scalar
   slice error is one component of the tensor cap error (W17.10) —
   equivalent at h=2, drastically weaker at h>=3; the v22-phrased
   witness search would report false witnesses. The correct
   rank-one predicate is the full tensor criterion; and on (R)
   pairs whose complements contain rank-3 full blocks, W17.4 makes
   rank-one witnesses likely impossible — the (R) witness route
   must use general caps.
4. **Bonuses:** STAGE_A's undecided pair (2,3) is DECIDED (explicit
   integer witness cap — with (0,2),(1,3) re-verified); Gap D
   dissolves for live-pair purposes (exact sources have >= N/2 live
   pairs; admissible caps Zariski-open there) while the OLD Gap D
   fails on STAGE_A (no full-rank block at all); the averaging
   route is closed (bidegree (h,h) => torus average identically 0).

**U(N) chain after W17:** witness existence with GENERAL caps at a
live pair of a minimal exact source; instruments = the evaluation
principle (audited), the W17.6 rank-one criterion as the cheap
first pass, decide_pair as the decision layer; structure theory =
W17.1/W17.4/W17.6. The induction's open core is unchanged in name
(witness existence) but now has a complete h=2 theory, an exact
h=3 criterion, and honest calibration of every shortcut.

---

## v28 addendum: W16 lands — (R) is a large family; the forcing statement is the last N=8 question (2026-08-15)

W16 (`computations/unaudited-residual2-w16-2026-08-15/`, unaudited,
float-free) restructured the endgame:

1. **ESCALATION: family (R) is large.** |F(Gamma)| >= 3 alone
   implies the (R) fibre conditions, and the constructive recipe
   (12 diagonal single cells on any properly 3-edge-coloured cubic
   graph + full blocks on the complement) yields at least SEVEN
   distinct skeletons at m=28 — W8's construction is one of them.
   Killing five templates was never going to close N=8; the closure
   must be uniform over (R). The v18 framing is corrected.
2. **The uniform instrument exists: vertex factorisation (W16-B,
   proved)** — a factoring site transports clean words across it: a
   one-extra neighbour kills outright; a two-extra neighbour yields
   a binomial. Downstream halves are DONE: m=28's binomial route is
   fully certified at all eight sites (9-term odd-relation
   certificates); m=27 from any site; m=26 kills from any site via
   k=1 (no odd relations exist there); m=25 has a PROVED dichotomy
   (factoring site 6 kills; Branch B explicitly characterised).
   Odd tight cuts are closed (their identities coincide with the
   cross-matching factorisation W16-1). **The single remaining N=8
   statement: "the effectively-clean layer forces some site to
   factor"** — template-combinatorial, with the m=25 Branch-B
   infeasibility as its sharpest instance and a measured map of why
   the easy word-set (X_free) falls short at m >= 26.
3. **Budget lemma W16-C** (2 beta + h >= 24; 8 <= |Gamma| <= 16;
   |Gamma| = 8 forces C_8 where the thickness shortcut fails) — the
   skeleton for the (R) census, which remains a lower bound and
   needs W11-style canonicalisation.
4. **SEVERE HAZARD found and contained**: Singular identifier
   shadowing manufactured a false kill, invisible to the stdout
   guard, caught only by W16's explicit-point control. Ledger items
   13-15 added (no-shadowing guard + explicit-point control now
   required practice; certificate minimality must be stated
   frame-relative — reconciling W15's 6/6, A6's five-word form, and
   W16's degree-6 multiplier).

**W19 launched** on the two remaining N=8 items: the forcing theorem
("clean layer => some factoring site", uniformly over (R)) and the
proper (R) census. No feasible point has been found anywhere in the
campaign.

---

## v29 addendum: W19 lands — m=25 closed; the forcing route cannot finish; the endgame is two named residuals (2026-08-15)

W19 (`computations/unaudited-forcing-w19-2026-08-15/`, unaudited,
float-free, explicit-point controls throughout):

1. **m=25 of family (R) is CLOSED.** W19 found the exact cause of
   W16's stall (the word-clean X_free set makes the site-4
   equations vacuous; the exact effectively-clean set — 2,624 words,
   a product box per L-word — supplies them) and killed Branch B by
   an exhaustive three-case split, each case forcing a site to
   factor in seconds, with the mandatory explicit-point control
   passing. With W16-A's dichotomy: **N=8 is now closed through
   m = 25.**
2. **The forcing theorem cannot close N=8 (Theorem W19-K).**
   |F(Gamma)| <= 2 empties the effectively-clean layer, and that
   stratum is non-empty (explicit C_8-Gamma member, min mixed fibre
   6, zero clean words). Every mechanism in the arsenal has empty
   input there. **New residual case named: the empty-clean-layer
   stratum** (214 of 794 census classes).
3. **The local geometry now explains what arguments can work**
   (Theorem W19-A + corollaries): first-order forcing at a site
   works iff its Gamma-degree is <= 2 (exactly why m=25 was the easy
   one), and at m=28 no order-<=2 argument can prove forcing
   (order-2-surviving directions aligned at no site). Forcing at
   26/27/28 needs order >= 3 or a global argument.
4. **The rank-two bracket stratum is empty at N=8** for all Gammas
   tested — with the delightful positive control that at N=4 the
   bracket construction produces exactly the known exceptional K_4
   GHZ witness (the forcing analogue is FALSE at N=4, as it must
   be). The campaign's machinery is calibrated against the one true
   exception in the conjecture's landscape.
5. **The census is real now**: 794 admissible Gamma classes, all
   inhabited; |Gamma|=8 forced to C_8 exhaustively; |Gamma|=16
   completely classified; total bracketed at 10^32..10^35 labelled
   members; W16's skeleton count corrected (4 of exactly 6 cubic
   classes; diagonality not required); the (R)-preserving symmetry
   is S_8 x S_3(global) ONLY (S_3^8 breaks (SC) — a census-soundness
   hazard caught).

**N=8 endgame, restated exactly:** (i) forcing at m = 26, 27, 28
for clean-layer-nonempty members — needs an order->=3 or global
argument (downstream halves already certified at every site); (ii)
the empty-clean-layer stratum — needs a genuinely new mechanism
(candidates: almost-clean multi-word certificates a la W15's m=24
with k >= 1 extras; the general-cap witness route via decide_pair,
which W17's warning does NOT forbid — only rank-one caps are
excluded on (R)). **W20 launched on both.** No feasible point has
been found anywhere in the campaign.

---

## v30 addendum: W18 lands — 18/19 mechanism closed, exhaustion 84% and running (2026-08-15)

W18 (`computations/unaudited-finisher-w18-2026-08-15/`, unaudited)
delivered the finisher's substance: **Lemma W18-A** (the cut
contradiction with machine-checked reason sets — a 1 ms purely
combinatorial kill) plus **W18-D** (cut-local ratios) kill every
admissible zero-singleton template the campaign has ever surfaced —
48/48 W11 witnesses, 31/31 W8 orbit witnesses, ~1,700 sweep
templates, **zero survivors anywhere**. Exhaustion at hand-off:
m=18 416/437 classes, m=19 211/310 (84% total); the sweep workers
are alive and the agent has been revived to shepherd them to
completion. W8's stall is quantified (complete censuses: 12
templates at m=16 — matching both prior lanes — and 29,190 at m=17;
one m=18 class alone carries hundreds of thousands): reason-set
nogoods are mandatory. **Lemma W18-E** gives a third independent
derivation of "family (R) starts at m >= 20" from (SC) alone. Its
control suite is the campaign's fullest yet (explicit-point
controls: 121 feasible systems, zero false kills; shadowing guard
enforced; no verdict rests on Singular). One open item: ONE proof
of 626 fails replay (likely DRAT-vs-RUP checker mismatch — new
ledger item 16); that class is unverified until re-proved, and its
resolution is in the revived agent's mandate along with the 120
remaining classes.

---

## v31 addendum: W20 lands — both residuals transformed; two finishing moves named (2026-08-15)

W20 (`computations/unaudited-lasttwo-w20-2026-08-15/`, unaudited):

1. **New general tools**: Theorem W20-L (site linearity — the clean
   layer is three homogeneous linear systems per site; 1-dim common
   kernel PROVES factoring; constructs exact on-variety points) and
   Theorem W20-R (the pattern-rank criterion: connected covering
   regular patterns force factoring).
2. **Residual 1 (m=26/27/28)**: forcing is now boxed in from every
   side — explicit exact clean points kill any FIXED-SITE argument
   (at m=28 for the proved reason that the template has a real
   involution exchanging the two sides), W19 killed order-<=2 local
   arguments, the per-point criterion is proved and fires at the
   factoring sites of every constructed point, and hard exact
   search never reaches zero factoring sites (min 1 at m=28, with
   ~97% of factoring sites provably unbreakable where visited).
   Status: [CONJECTURED, strongest evidence]; the remaining
   obligation is one finite statement — at every all-nonzero clean
   point some site carries a connected covering regular family —
   an elimination in the Pfaffian frame (Gamma is Pfaffian at
   25..28, noted and unexploited).
3. **Residual 2 (the C_8 / empty-clean stratum)**: the stratum has
   its mechanism — the L-free/R-free reduction makes 3,960 of the
   6,558 mixed equations pure 4x4 permanent conditions on the cross
   blocks alone, and the new Lemma W20-P (permanents on products of
   hyperplanes vanish only on a common coordinate hyperplane —
   proved, with a 640,000-configuration exhaustive control) yields
   necessary rank conditions and a 9+9 box-cover arithmetic. A
   single L-free word is provably insufficient; the kill must
   combine the full permanent conditions of at least two. Probe
   signature indistinguishable from proved-dead templates.
   Status: [CONJECTURED dead, obstruction ladder explicit].
4. **Ledger item 17** added (vacuous-by-specialisation tests — a
   third false-kill mechanism found and fenced this cycle).

**W21 launched on the two finishing moves**: (i) the m=26/27/28
"some site factors" statement via the Pfaffian-frame elimination +
the W20-R criterion; (ii) the C_8 kill via multi-word permanent
conditions (and decide_pair as the fallback), then generalisation
over the 214-class stratum. W18-revived continues the 18/19
closure. No feasible point found anywhere, at any time, by any lane.

---

## v32 addendum: promotion drafts complete; the gating list is now the to-do (2026-08-15)

P1-doc delivered nine spine-document drafts
(`computations/unaudited-promotion-drafts-2026-08-15/`, untracked
pending review + gauntlet): the cut mechanism (with a NEW
draft-supplied general-N proof of both W12-C containments, flagged
audit-required — N=8 does not depend on it), both kill certificates
(m=20; m=24 in A6's five-mixed-word form with a bookkeeping
correction — the "27 monomials" figure belonged to A6's other
identity), the gauge lemma (existence half separated so W10-6 is
robust), the L_h law (tags split [P]/[V]; A5's corrected T2 law with
explicit stratum; the "three weight spaces" gloss marked unproved
prose), the evaluation principle (+ A6's directness proof written
out; characteristic-0 use localised to one step), the
fourth-matching theorem (attribution first line; two corollaries
EXCLUDED for lacking any checker in the corpus — "m = 3N/2 + 1
dies" and "even-cycle-free dies" have prose proofs in A3's report
only; the floor corollary marked conditional on the unaudited J.1d
budget and subordinate to the committed finite-obstruction Cor 7.2),
a supersessions entry proposing six new dependency IDs (needs
coordinator ratification), and an 81-item gating checklist.

**Hard blockers adopted as the promotion worklist:** (1)
UNIFORM-FLOOR has no independent audit at all; (2) W12's C1/C2
controls were never written to disk (A4-D2); (3) the m=17 closure
DRUPs were never replayed; (4) all pre-ledger Singular artifacts
need the shadowing guard + explicit-point re-runs; (5) cited
scripts live untracked, some with absolute paths. Hygiene agent H1
launched on (1)-(3) + a path scan; (4) folds into each document's
commit-time re-run per the checklist.

---

## v33 addendum: W22 lands — U(N) is a pure-equation statement; the induction program re-aimed (2026-08-15)

W22 (`computations/unaudited-induction2-w22-2026-08-15/`, unaudited,
float-free) restarted the induction layer and settled its direction:

1. **Retire every plan that would prove U(N) from the mixed
   equations** (Theorem W22-1): all-blocked mixed-exact sources
   exist at every even N — on W10's constant-block family the
   general-cap error collapses to sigma(K)^h times W5's scalar
   error, so every pair is simultaneously live and blocked; the
   pure equations are load-bearing for witness existence, exactly
   as they were for the (R) kills (W10's prediction, W15/W19's
   certificates). J.1b-support is likewise correctly localised as a
   pure-equation statement (its falsifier shape EXISTS on
   mixed-exact sources; W5's 0/93 was fleet-specific).
2. **New uniform tools**: the general-cap closed form W22-M with
   the attachment corollary W22-M1 (W5's condition at every h and
   every cap — the one N-uniform witness instrument); Theorem W22-T
   (h=2 witnesses are four-fold transfer coincidences or
   three-fold with cube-root-of-unity ratios — the precise machine
   form of complex-only, built exactly over Z[omega]); Theorem
   W22-X (exactness alone gives star injectivity; all-blocked
   forces >= 3 attached star directions per admissible cap vector);
   Lemma W22-S (the tensor L1 — the first pure-equation consequence
   touching the witness-relevant star data); and the exact
   block-wise linear walk on the mixed-exact variety.
3. **The counting attack's direction is settled**: overdetermination
   grows without bound, blocking gets MORE generic with N; the
   witness side pays the coincidence cost and only the pure
   equations can force it. The named next object: the TENSOR L2
   (two-off-colour analogue of W22-S) — the smallest identity
   seeing A_pq and the internal blocks at once.
4. **The N=10 tool-transfer table is drawn**: cut contradiction,
   site linearity, the permanent lemma family, and the L-free
   reduction all transfer with proofs; the cut-local ratios
   degrade; the blocking taxonomy is dead above h=3 (only W22-M1
   survives). The first genuinely N=10 gaps are OBJECT shortages
   (no (R)-census, the wide singleton-free band), not mechanism
   shortages — build them only after the N=8 (R) story closes so
   its final shape informs the census.

**W23 launched** on the pure-equation witness core: derive the
tensor L2, compose it with W22-X/W22-M1 toward "exact + all-blocked
is contradictory at some pair", and test the detachment-law
conjecture beyond its single object.

---

## v34 addendum: audit A7 — the m=25 kill is RETRACTED; the forcing route is dead as a clean-layer theorem (2026-08-15)

A7 (independent engines, exhaustive sweeps per ledger 12) audited
the m=25 chain, W19 and W20. The headline is a refutation the
campaign must absorb:

1. **RETRACTION: "N=8 closed through 25" reverts to "closed through
   24."** W19's case-3 kill rested on sign-flipped generators
   (w19_branchB.py:243: mu k_x + A03 g instead of − ; the flipped
   form forces g = 0 spuriously). A7 built an explicit 12-member
   family of exact witnesses — all cells nonzero, every
   effectively-clean equation satisfied, Branch B, rank M6 = 2, NO
   site factoring. **"The clean layer forces some site to factor"
   is FALSE at m=25** — refuted, not unproved — so it cannot be the
   uniform theorem at 26/27/28 either. The kills at 25..28 must
   consume equations beyond the clean layer (the k=1/k=2 words and
   the pure equations — exactly W22-1's lesson that the pures are
   load-bearing). The witness is NOT a Krenn–Gu counterexample (it
   violates 3,820 non-clean equations); it is the calibration
   negative every future composed system must kill. W21 re-aimed
   accordingly.
2. **Two methodology rules adopted (ledger 18)**: forcing-verdict
   explicit-point controls must be constructed OUTSIDE the asserted
   locus (W19's C5 point had all eight sites factoring — vacuous as
   a control); and search minima ("never reaches zero factoring
   sites") carry no evidential weight — A7 demonstrated the same
   search misses a provably existing zero-factoring point.
3. **What survives, mostly strengthened**: W16-A (with the honest
   two-case split — case 2 is vacuous under the exact clean set);
   the downstream factoring=>kill at every site of 24..28 (tables
   reproduced); W19-K + the C_8 member; the census (all 794 classes
   now certified by explicit witnesses; the S_3^8 prose corrected —
   576 per-site survivors, not a subgroup, operational conclusion
   intact); W20-L; W20-R (+ deg >= 2 hypothesis); the L-free
   reduction (now an exact polynomial identity); the m=28
   automorphism; Lemma W20-P (statement true; written proof step
   (B) replaced by A7's induction; char != 2 and through-the-origin
   added; NEW fully exhaustive n=5 verification over 2.3e8
   multisets); P4c proved.
4. **Scoreboard after A7**: m <= 24 closed; m = 25, 26, 27, 28 open
   with the route constraint now known (clean layer provably
   insufficient at 25; downstream halves remain certified
   everywhere); the C_8/empty-clean stratum open (W21 Move 2);
   18/19 finishing (W18). The audit column has now caught: five
   probe-headline errors, three false-kill tooling mechanisms, and
   one invalid closure — none of which reached the spine.

---

## v35 addendum: H1 discharges the promotion blockers — and finds a spine defect (2026-08-15)

H1 (`computations/unaudited-hygiene-h1-2026-08-15/`, unaudited):

1. **A defect in committed spine, found and disposed of**: the
   Step-5 paragraph of `proofs/odd-near-perfect-gadget-obstruction.md`
   is a non-sequitur (explicit counterexamples to its parity-class
   descent at N = 8, 16, 24). The THEOREM is true — two other
   committed proofs are sound (both re-verified), H1 added a
   one-line third, and the residual case is re-verified exhaustively
   to N = 20. Disposed via **SUPERSESSION-2026-08-15-01** (canonical
   file byte-frozen; correction note
   `notes/2026-08-15-step5-defect-and-repair.md`; permanent audit
   record under certification/audits/). First spine-level defect of
   the campaign; zero downstream impact.
2. **The m <= 17 closure is now fully proof-verified**: drat-trim
   built; 31 stored proofs replayed — 3 FAILED (two missing lemmas,
   one never closes) and were re-solved cadical-native with fresh
   VERIFIED proofs; the 7 earlier replacements verified by the
   second checker. 31/31 stand. Zero RAT lemmas anywhere (ledger 16
   unchanged: the RUP-only acceptances were luck).
3. **Fourth-matching layer audited** (UNIFORM-FLOOR unblocked):
   A3.4 confirmed with independent engines; A3.5's forcing step
   genuinely forced (unique budget solution). The two excluded
   corollaries: combinatorics PROVED and exhaustively verified (to
   14.3M templates at N=10) but "m = 3N/2 + 1" LACKS THE FORCING
   STEP (13 budget solutions — do not promote) and "even-cycle-free"
   needs N >= 6 (the K_4 one-factorisations are counterexamples at
   N = 4 — the exceptional witness's third cameo).
4. **W12's C1/C2 controls evidenced** (with a stronger exact
   exponent-identity form and the V-nonuniqueness caveat); C3
   deferred (B1 partial).
5. **Portability + hazard calibration**: no live shadowing
   collisions anywhere (ledger 13 is procedural debt); ledger 6
   corrected (build-specific reserved names — only `mult` on this
   build); A6's Singular artifact for the m=24 membership is
   DEFECTIVE (sat()[1] + missing elim.lib — fails silently) and
   must be re-run under guard at promotion — the certificate itself
   stands on the hand-expansion and two independent lanes; two
   load-bearing bare asserts in the A3 lane vanish under -O (fix at
   promotion).

Promotion gate after H1: I1/I2 discharged; UNIFORM-FLOOR audited
(with the two corollary exclusions confirmed as correct calls); B1
partial; A3 (cert-commit re-execution) and the guard re-runs remain
the commit-time items.

---

## v36 addendum: W21 lands — the target falls at m=28 too; the residual linear test replaces it (2026-08-15)

W21 (`computations/unaudited-finishing-w21-2026-08-15/`, unaudited,
float-free):

1. **The clean-layer forcing statement is FALSE at m=28 as well** —
   exact zero-factoring clean points with all 144 Gamma cells
   nonzero (three witnesses, three engines, reproduced from
   scratch), independently corroborating A7's m=25 refutation. The
   witnesses are NOT counterexamples: their residual single-cell
   systems are linearly inconsistent — no completion exists.
2. **The replacement mechanism: the RESIDUAL LINEAR TEST** — fix
   the Gamma blocks at a clean point and take only the degree-<=1
   equations in the twelve non-Gamma cells (the k=1 family); kill =
   inconsistent or an occupied cell forced identically zero.
   **221/221 exact points killed across m=24..28, including A7's
   entire refutation family and every zero-factoring point**, with
   ledger-18-compliant sampling across 0..5 factoring sites. The
   open statement of the m=25..28 endgame is now: *for every point
   of the clean variety with nonzero Gamma cells, the residual
   linear system kills.* W24 launched on proving it (the W21-B2
   block/Schur reduction — clean = avoiding 12 forbidden pairs;
   eight identically-vanishing K_4 hafnian identities — and the
   Pfaffian rank-<=2 frame are the structure to use).
3. **Move 2: C_8 is NOT killed, and a false kill was caught** by
   the strongest control yet: two independent sub-probes reached
   contradictory verdicts and W21 adjudicated in exact Q(omega) —
   the claimed impossibility lemma has an omega-family
   counterexample that passed a complete F_5 classification (no
   cube roots of unity there). Ledger items 19-20 adopted
   (characteristic caveats; the adversarial-builder control).
   Salvage: the double-dead-column obstruction at the unique word
   x = (1,0,0,2) — the omega-family fails exactly that constraint —
   may recover the kill with a corrected lemma.
4. Tools proved: the Pfaffian frame (rank Q <= 2 on the clean
   layer), the chain identity, the block/Schur reduction (which
   explains the identical clean sets at 26/27/28), the settled
   automorphism split; the sub-probe's complete classification of
   the identically-vanishing K_4 hafnian (needs audit; its
   consequence: m=26 forces >= 2 reduced factoring sites, m=27
   >= 1, m=28 nothing — exactly where the witnesses live).

Scoreboard unchanged (m <= 24 closed); the open surface is now ONE
candidate-uniform statement (the residual linear kill at 25..28) +
the C_8/empty-clean stratum (double-column route) + W18's sweep.

### v36.1: W21 final tally (2026-08-15)
The residual linear test now stands at **274/274 exact kills, zero
survivors, m = 24..28** (new complete m=24 row; ledger-18 spread
intact). Status unchanged: [CONJECTURED] pending W24's proof over
the whole clean variety.

---

## v37 addendum: W18 second report — 661/747 closed, zero survivors ever, the sector escalation resolved (2026-08-15)

W18 (revival phase; sweep self-continuing with supervisor + disk
monitor): m=18 at 428/437, m=19 at 233/310 — every remaining class
attempted (wall-clock budget under load ~50), zero survivors and
zero certificate failures in the entire lane's history. The first
templates ever to survive all four cheap engines (a site-7
sector-splitting structure where only 3-5 cuts carry content) are
KILLED with machine-verified certificates. Two engine advances with
their own control suites: 6-site cut sides and a GAUGE-FIXING
licence for half-system decisions (divisibility argument; GC1-GC3
controls; hardest template 5400 s -> 17 s). The 7847550 replay
failure is resolved and a strict sweep of all ~660 stored proofs
found two more defective ones (~0.45% pysat get_proof defect rate —
both re-solving; the lane has been pointed at H1's cadical +
drat-trim binaries to re-emit solver-native at completion). Ledger
item 21 added (controls must fail loudly if skipped — W18 found its
own EPC2b had silently never run). Remaining: 86 classes on budget
+ two repairs; nothing blocks them but wall-clock.

---

## v38 addendum: W23 lands — the tensor L2, the equation ladder, and the first N-uniform witness theorem (2026-08-15)

W23 (`computations/unaudited-pure-core-w23-2026-08-15/`, unaudited,
float-free):

1. **The tensor L2 is proved at every N** (the two-off-colour
   identity: C^(c)_ab A_ab + Phi^(c)_ab, with exactness pinning it
   to e_c e_c^T), with the rank law, the N=4 closed form (an
   invertible block forces the complementary block's diagonal to be
   its inverse's diagonal — verified on the exceptional K_4
   witness), and the bridge identifying L2 as the one-slot form of
   the descent cap identity.
2. **The equation ladder is measured, and it corrects the framing
   twice**: all-blocked points exist at rung X_1 with pures exactly
   (1,1,1) — so the pure equations ALONE do not force witnesses
   (stronger falsifiers than W22-1's); and while L2 closes the
   all-1 diagonal stratum EXHAUSTIVELY at N=6 (56 classes, min 9
   witnesses), general-source all-blocked X_2 points exist — **the
   first rung that bites for general sources is X_3 (the three-off
   words)**. X_3 shows no all-blocked point in 40 walked objects,
   every one carrying exactly 9 witnesses; X_4 is empty (six-site
   re-derived on a larger stratum). The N=6 form of the U(N) core
   is now the named statement "X_3 => witness" — not refuted, and
   the last nonempty rung.
3. **The first N-uniform witness-existence theorem (W23-U2)**:
   every live pair of the disjoint-three-matching diagonal family
   carries a witness at every even N >= 6, via an explicit
   antisymmetric cap whose two surviving matching terms cancel by
   antisymmetry. With W23-U1 (the family lies in X_2, never exact)
   and W23-DR (diagonal X_2 forces three disjoint monochrome
   rank-one vertex covers — re-deriving W5's corollary from L2
   alone), the diagonal wing of the induction now has proofs, not
   measurements. The detachment law is refuted in general but
   survives one-directionally (max detachment >= 2 => witness,
   exhaustive), with a proved fragment at every N.
4. **A route closed cleanly**: the one-vertex composition cannot
   yield the contradiction (W23-N1's explicit consistency
   certificate) — U(N) needs at least two-vertex/global structure.
   Ledger 22 added (rational-coefficient emission hazard, with the
   homogeneity-licensed fix).

**W25 launched** on W23's named next objects: decide "X_3 =>
witness" at N=6 exactly (adversarial-builder discipline per ledger
20); push W23-U2 past dead edges (W23-DR pins the live structure);
and the N=8 general ladder. No feasible point of any exact system,
anywhere, ever.

---

## v39 addendum: W24 lands — the residual kill is a theorem on the vanishing stratum; the gap is three tiny statements (2026-08-16)

W24 (`computations/unaudited-residualkill-w24-2026-08-15/`,
unaudited, exact-only):

1. **Theorem W24-A [proved]**: at every clean point with all Gamma
   cells nonzero where haf_Gamma vanishes identically, the residual
   degree-<=1 system kills — all four supports, every
   characteristic != 2 (the char-2 exclusion is genuine and fires).
   The proof runs through the new **Lemma W24-C**, an unconditional
   pointwise identity (the three coefficients at an L-vertex have
   det M = 2 X_1 X_2 X_3), plus virtual-word solo certificates.
   This stratum contains roughly three quarters of every clean
   point ever constructed.
2. **The finite reduction**: survival is equivalent to the absence
   of a PURE ROW, and the system splits into row-isolating
   sub-systems in 1-3 unknowns with size-1/2 minimal certificates.
   **The whole m=25..28 endgame is now three explicit statements**:
   rule out Case 2b at m=25 (a nine-fold parallelism configuration
   never observed — rank 1 at 9/9 everywhere); the one-unknown
   (2,6) sub-system at m=26/27 (whose coefficient is a MONOMIAL,
   nonzero at every word); the three-unknown vertex-0 sub-system at
   m=28.
3. **Correction adopted**: the regime dichotomy (vanishing <=> 
   consistent) is FALSE (explicit m=27 point) — struck before
   anything was built on it.
4. Adversarial builder: no survivor over Q, Q(omega), Q(i) (124
   fresh + 39 stored points), and it re-derived the core identity
   independently. Tally across lanes now 95/95 + 274/274 with the
   proved stratum absorbing most of it.

**W26 launched** on the three blocker statements (with the Case-2b
forcing chain to finish, the monomial-ratio statement at 26/27, and
the m=28 vertex system — full ledger discipline including the
adversarial builder).

---

## v40 addendum: the sleep-cycle harvest — the rung shifts to X_4; the sub-statements fall; the full kill survives everything (2026-08-17/18)

The agent loops died in machine-sleep cycles on 08-16, but their
orphaned compute continued through every wake window. Harvest from
disk (all checkpointed with control manifests per ledger 21):

1. **W25's N=8 all-blocked X_3 object is VERIFIED to the full
   standard** (25 hours of exact compute): all 21 live pairs BLOCKED
   by a THIRD independent decision route (saturation), 0
   disagreements with the two Rabinowitsch deciders; a 1,244-cap
   explicit witness search finds 0 (with the same search FIRING on
   a diagonal positive control — 11 witnesses); mutation controls
   pass. **The N=6 biting rung (X_3) does not bite at N=8**, and
   the reason is measured: the X_3 site-system kernels are
   dramatically larger at N=8 (rigidity collapse). X_4 screening
   from 6 seeds reached nothing — **the N=8 U-core candidate moves
   to the X_4 rung**, with the ladder now known to be
   order-dependent.
2. **W26's adversarial builder constructed ALL the forbidden
   configurations** (ledger-20 discipline): an explicit Case-2b
   point at m=25 (all cells nonzero, clean, ninefold parallelism,
   OFF the vanishing stratum, verified over Q and Q(i)) — **S1's
   shape is FALSE**; explicit (2,6)-solo-survivor points at m=26
   AND m=27 with constant nonzero ratio (= 2 over Q; 20*omega and
   20*i in the extension families) — **S2's per-sub-system shape is
   FALSE** (the (2,6) and (1,6) sub-systems are individually
   consistent there).
3. **AND THE FULL RESIDUAL KILL SURVIVED EVERY ONE OF THEM**: the
   Case-2b point — full system inconsistent (rank 11 in 10
   unknowns, 2,743 rows), killed; both solo-survivor points — full
   system inconsistent (rank 13 in 12 unknowns), killed. W26's scan
   additionally re-killed every W20/W21 stored point including the
   zero-factoring ones and the off-stratum m=27 points (KKKKKK
   throughout). **The conjectured theorem — the full degree-<=1
   residual system kills at every clean point — has now survived
   targeted adversarial construction against each of its parts.**
   Consequence for the proof: the W24-style reduction must treat
   the six sub-systems JOINTLY (single sub-systems provably do not
   suffice); the per-support statements S1/S2/S3 are retired as
   individually-sufficient shapes.
4. W18's sweep continued through the wake windows: certificates on
   disk now 436 (m=18) + 249 (m=19) = 685/747; the fourth defective
   proof's native re-emission is in drat-trim now; zero survivors
   ever, zero certificate failures.

Agents revived to write final reports and re-aim the proof at the
joint system.

---

## v41 addendum: W25's final report — the ladder theory matures (2026-08-17/18)

Beyond the v40 harvest, W25 delivered: the **L3 identity** (three-off
tensor form, every N; new content = the 2x2x2 all-off corner — the
L1/L2 pattern continues); **W25-D1** (odd rungs are automatic on the
diagonal stratum — diagonal X_2 = X_3 at every even N; Delta^3_N
lies in X_3 with first failures exactly the bicoloured 4-cycles, so
"X_3 => witness" is TRUE on that whole family); **the cancellation
stratum is EMPTY at N=6** (exhaustive over all 1,646,850 skeleton
triples — W23's flagged gap closed; 24 diagonal classes fully
classified with nonempty weight varieties); **the all-blocked X_2
locus in closed form** (one skeleton class; X_2 = a 12-dimensional
affine family, generically all-blocked; X_3 collapses it to the
single diagonal point with 9 witnesses — the added equations
annihilate exactly the dangerous deformation); **Theorem W25-U3**
(both-endpoints-clean => witness at every even N, no X_2 needed —
the correct extension of W23-U2, whose naive form is refuted; one
clean endpoint suffices at N=6 only); **no diagonal X_2 source at
N=6 is all-blocked** [proved, incl. the (5,5,5) class by an explicit
single-component cap]; and the **record correction** that W23's
detachment law does not extend to N=8 (F8 violates it at 20/21
pairs). The U-core candidate is now the PENULTIMATE RUNG (X_3 at 6,
X_4 at 8, X_5 at 10) — with the honest caveat that no X_4 point at
N=8 has been constructed at all yet.

**W27 launched** on W25's named next objects: build X_4 at N=8 and
decide it (the real N=8 U-core); decompose X_3 at N=6 (turn the 857-
object verdict into a theorem); the skeleton-level witness
criterion (constant across weights in all 24 classes — an
unidentified combinatorial law); the cancellation stratum and
diagonal classification at N=8.

### v42: W18 milestone — support 18 fully closed (2026-08-18)

m = 18 is CLOSED: 437/437 support-graph classes, 0 survivors,
437/437 proofs replaying to the empty clause, 111,176 verified kill
certificates (O2 does the overwhelming bulk; the cheap combinatorial
lemmas the rest; the Groebner layer never fired). Scope honestly
stated: the value-level exhaustion W8 left open, with 432 proofs
pysat-emitted-but-replay-clean pending the native backfill. m19 at
254/310. The N=8 open surface shrinks to: 56 m19 classes, the joint
residual theorem at 25..28, and the C_8/empty-clean stratum.

---

## v43 addendum: W27 lands — a second route to N=8 opens; the diagonal case nearly closes; the N=6 witness law found (2026-08-18)

W27 (`computations/unaudited-penult-w27-2026-08-18/`, unaudited,
checkpointed):

1. **The ladder route to N=8 is real and calibrated.** X_5 = EXACT
   at N=8 (profile theorem), so **X_4 empty would prove the open
   case**; on the diagonal X_4 = EXACT already, so the diagonal
   cannot calibrate — and W27's probe, which fires on every known
   nonempty rung and is silent on the known-empty one, finds (8,4)
   wearing the empty signature. ~4,300 backgrounds, no X_4 point.
   [CONJECTURED: X_4 = ∅ at N=8.] The site reduction (W27-R1) +
   the colour-symmetric slice (W27-R2, ~7 orbit parameters) turn
   the symmetric case into a FEASIBLE SYMBOLIC ELIMINATION — the
   named attack.
2. **The diagonal case of N=8 is nearly closed by combinatorics
   alone (W27-D3)**: over all 32,970 disjoint-PM triples of K_8,
   the (4,4,0) conditions hold iff all three pairwise unions are
   Hamiltonian (16,800 triples) and the (4,2,2) conditions hold on
   8,610 — and the intersection is EMPTY. No diagonal exact source
   at N=8 exists outside the cancellation stratum. The cancellation
   stratum is the one remaining diagonal gap.
3. **The N=6 skeleton witness law is found and exact (W27-S1)**:
   witness iff an endpoint is c1-simple or both are almost-clean —
   all 279 pairs, no exception, strictly sharper than W25-U3. It is
   N=6-only, but the phenomenon survives at N=8 (witness sets
   constant across weights — a non-local invariant exists), with a
   new proved blocked-condition (npm = 0 => blocked at N=8, false
   at N=6). The X_3 decomposition adds 120 points (977 total, zero
   all-blocked) and a striking regularity: the rigid stratum
   carries EXACTLY 9 witnesses at all 51 points.

**W28 launched** on the two decisive attacks: the symmetric-slice
elimination for X_4 emptiness + the diagonal cancellation stratum
(completing the diagonal theorem), with the skeleton-invariant hunt
as the third task.

### v43.1: W28 interim — the sigma slice is informative and X_4-empty (2026-08-19)

W28's detached overnight run (27,345 s, checkpointed) delivered the
informativeness verdict for the symmetric-slice attack: the
sigma-diagonal family at N=8 is exhaustively swept (16,384
backgrounds) with rung profiles {[0,0,0,0]: 6,607, [3,0,0,0]:
7,653, **[3,3,3,0]: 2,124**} — i.e. 2,124 backgrounds reach X_3
with all three colour systems feasible (the slice genuinely
contains the penultimate rung, unlike the uninformative F21 slice,
which W28 correctly flagged and set aside), and **none reaches
X_4**. The char-0 symbolic elimination on this slice — which would
upgrade the sweep to the proved theorem "X_4 ∩ {sigma-symmetric} =
∅ over all complex weights" — is the running next step, alongside
the T2 diagonal-cancellation enumeration. The machine's sleep
cycles keep killing agent loops but not detached compute; the lane
now runs fully detached with the loop reduced to polling.

---

## v44 addendum: W28 lands — the symmetric-case theorem; the diagonal case is one computation from closed (2026-08-19)

W28 (`computations/unaudited-x4empty-w28-2026-08-18/`, unaudited,
33 checkpoints):

1. **THEOREM W28-T1 [proved, char 0]: the symmetric case of
   X_4-emptiness** — no sigma-symmetric diagonal background admits
   a feasible X_4 site system at N=8, over ALL complex weights (127
   free-set ideals, all unit; pipeline calibrated at k=3; slice
   proven informative — 2,124 of 16,384 patterns reach X_3, none
   X_4). Enabled by three new lemmas (averaging; diagonal parity
   decoupling 21 -> 7 unknowns; the free-site split) and one
   soundness catch (orbit reduction would have been unsound — the
   colour action moves the systems).
2. **Route hygiene**: the maximal-symmetry F_21 slice is proved
   infeasible from X_2 up and RETIRED as information-free — the
   ledger-18 lesson operating at the scale of a whole attack.
3. **The diagonal case of N=8 is now one computation from being a
   theorem.** W28-DEL closes W27-D3's gap (the no-cancellation
   reduction is complete); the cancellation stratum is exhausted
   over ~745 million skeleton triples (0 survivors) plus 75,000
   calibrated builder starts and a 330,000-background census (0
   three-colour X_4 anywhere, ever); the honest boundary is
   explicit (the single-colour statement is false off the slice);
   and the remaining object is T1h — the three-colour free-site
   ideal (96 generators, 66 variables, timed out once). **If T1h
   terminates unit, "no diagonal exact source at N=8" is a theorem
   including cancellation — the classical edge-coloured Krenn–Gu
   statement at the open order.** W29 launched on it with the named
   tactics.
4. Also: W28-LAM (the diagonal problem as a Waring-type hafnian
   identity), W28-GOOD (three disjoint spanning good classes
   forced), and the N=8 skeleton invariant measured 95.8% local
   with a new best rule (npm_drop).

X_4 = empty at N=8 overall: still [CONJECTURED] — now with a proved
symmetric case, a complete no-cancellation reduction, and
three-quarters of a billion exhausted configurations behind it.

---

## v45 addendum: W26 interim — the joint theorem's true shape; S3 falls; two items remain (2026-08-19)

W26's three-day interim (checkpoints in
`computations/unaudited-blockers-w26-2026-08-16/`):

1. **The "+1 inconsistency row" lead (mine, v40) is corrected**: off
   the vanishing stratum there are TWO kill modes — INCONSISTENCY
   (rank = unknowns + 1, now with tiny exact FARKAS CERTIFICATES: 3
   rows at m=25, 4 at m=26/27 — the promotable artifact shape) and
   FORCING (rank = unknowns, consistent, 9-10 of 12 cells forced to
   zero — the m=28 mode). The joint theorem must read "inconsistent
   OR forcing"; a proof hunting only the extra row would miss half
   the cases.
2. **S3 is refuted too**: the builder constructed m=28 clean points
   (all 144 Gamma cells nonzero, off-stratum) with the whole
   vertex-0 solo triple simultaneously surviving — all three
   per-sub-system statements are now dead by explicit construction,
   AND the full system killed every one of them. Running total:
   139/139 points killed (39 stored + 100 fresh, 37 off-stratum),
   KKKKKK throughout. The builder NEVER exceeded 3 simultaneously
   nonzero singles of 12 — the sharpest empirical face of the joint
   theorem.
3. **New proved identities**: Theorem W26-M (h Psi[D_p] = sum_q D_q
   l_ij Psi_q — every vertex reduces to a three-vector slice
   equation at every support incl. m=28) and its dual W26-M*; the
   R-VERTEX grouping beats W24's L-vertex decomposition (the j=6
   system alone kills 39/39 stored points); the det-M-transfer
   mechanism (det M depends only on untriggered variables, so its
   vanishing transfers to triggered words and yields pure rows) —
   det M nonzero has occurred ZERO times anywhere.
4. **Remaining, named**: (i) the m=27 side-condition of W26-K (fires
   at exactly one known point — a real case, ~day-scale); (ii)
   m=28 "some vertex always delivers a pure row" (the real item —
   no missing R-edge there, so no Psi_q is forced nonzero; wide
   points exist where vertices 4 and 7 deliver nothing and 5/6 do);
   (iii) restate the theorem as inconsistent-or-forcing
   (bookkeeping). HONEST CONTROL FLAGS per ledger 21: the
   multi-characteristic sweep was VACUOUS (mod-p site solves found
   zero clean points — seeding failure), so ledger 19 is UNSATISFIED
   for the det-M claim pending the rank-one seeding fix; the early
   fresh-point tallies were empty by design quirk and carry no
   evidence; no Singular ran in the lane.

### v45.1: W26 partial — ledger 19 satisfied and it caught an overstatement; the disjunction is the last statement (2026-08-19)

The fixed rank-one mod-p seeding produced 216 clean F_p points over
six primes (five = 1 mod 3), satisfying ledger 19 for the det-M
lemma — and F_7 immediately caught an overstatement Q-sampling had
missed: the vertex-4 route at m=25 needs a hafL != 0 hypothesis
(the symbolic table said so; 22/324 failures at p=7, all localised
there; vertex 7 is clean in all 5,832 tests across every prime).
Exactly the ledger-19 rationale working as designed. The m=27
side-condition is closed by VERTEX-SHIFT (three vertices fail at
the firing point, five deliver — the point dies); refinement
recorded: letter collapse does not imply failure (needs collapse +
the firing row outside the line). THE DISJUNCTION ("no clean point
has all eight vertices failing") now holds 116/116 with per-vertex
failure counts showing every vertex fails somewhere — so the
disjunction, not any single vertex, is the theorem; the forbidding
relation is the one remaining statement of the template route.

---

## v46 addendum: audit A8 — the ladder chain confirms; the census exhaustion becomes a hand theorem (2026-08-19)

A8 (fully independent engines) audited the ladder route:

1. **The diagonal chain FULLY CONFIRMS** — the profile theorem, the
   parity lemma, diagonal X_4 = EXACT, and the D3 census verified
   by THREE independent routes (including a pure
   inclusion-exclusion identity). The "(C) <=> pairwise-Hamiltonian"
   step is derived, not assumed. **And the audit contributed a
   short structural PROOF of the incompatibility** ((C) => not-(D)
   via distance-3 chords or the parity-shift survivors — verified
   on all 16,800 cases): the 32,970-case exhaustion is now a
   theorem with a hand argument.
2. **W28-T1 CONFIRMS as computation and argument** (45/45 re-encoded
   ideals unit in three characteristics, full independent 127-sweep
   relaunched and clean so far; calibration exact; the
   orbit-unsoundness catch witnessed; the ledger-18 outside-locus
   control SUPPLIED by the audit itself).
3. **Seven repairs, none theorem-breaking** (adopted): W28-DEL's
   printed justification refuted as unqualified (cancelling-weight
   witness; W28's own deletion control was vacuous — positive
   weights only) with the cleaner npm-monotonicity repair; W28-LAM
   downgraded to a one-way implication (explicit X_3-not-X_4 point
   satisfying the Waring identity); SYM's missing invertibility
   hypothesis + T1 re-attributed to DEC+FREE; the disjointness
   docstring fixed (only GOOD classes are disjoint — the sweep's
   disjoint-support restriction is real); the sweep's true scope is
   8 of 10 profiles / 1.54 BILLION triples with (5,6,6) and (6,6,6)
   never run (assigned to W29 as a detached side task); the
   special-order criterion is N = 2 mod 6; two rung implementations,
   not three.
4. **The gate for the committable theorem is now exact**: T1h's
   reduction is independently confirmed sound, its calibration
   correct — and A8's load-bearing note for W29 is relayed: a mod-p
   unit verdict does NOT prove the char-0 kill; char 0 is the run
   that counts.

---

## v47 addendum: W29 lands — THE DIAGONAL THEOREM (2026-08-19/20)

W29 (`computations/unaudited-diagclose-w29-2026-08-19/`, unaudited):

1. **THEOREM W29-T1 [probe-proved, proof-checked three ways]: no
   diagonal exact source exists on K_8 over any field** — the
   classical edge-coloured Krenn–Gu statement at the open order.
   The machine: the free-set-triple normal form (three forced
   distinct witness sites; an 87-orbit case ledger) + a
   vanishing-pattern Boolean abstraction whose eight clause
   families are each one-line-sound in every characteristic and
   which ALLOWS ALL CANCELLATION — so UNSAT is nonexistence over
   any field. UNSAT at N=8 across all 4,096 cases and all 87
   orbits, with the k=3 calibration SAT everywhere and real X_3
   sources passing the encoder end-to-end (1,200 checks); the N=4
   exceptional source is correctly SAT with zero violations; N=6
   closes the same way with independent Groebner confirmation.
   Five solvers + an own RUP checker + drat-trim verify every
   orbit's proof. **Uniform in even N**: N=10 in flight (calibration
   passed), N=12 queued — the diagonal statement is closing beyond
   the open order, not just at it.
2. **The assigned computation was a dead end, found honestly**
   (W29-A1): T1h is NOT unit — an explicit 21-parameter family sits
   in its variety; the timeout was a formulation artifact (it kept
   only the singleton rows). Retired. This also SUBSUMES A8's
   missing-profile repair item — the abstraction covers the
   cancellation stratum entirely.
3. Scope stated honestly: diagonal only (the product structure is
   what diagonality buys); general X_4-emptiness at N=8 remains
   conjectured; the minimal UNSAT core (361 constraints) is the
   hand-proof target.

**A9 launched: the promotion-gate audit of W29-T1** — the campaign's
headline theorem so far rides on eight one-line clause validities,
one normal-form derivation, and one encoder; every piece gets the
full adversarial treatment before anything is committed.

---

## v48 addendum: W26 final — Route A proved at 26; one pairwise exclusion left at 25/27/28 (2026-08-20)

W26's final report: the joint residual theorem is **PROVED at
m=26** (Lemma W26-1's unconditional monomial forcing), **PROVED at
m=25/27 modulo one statement**, and **reduced to the same statement
at m=28**: a single 2-of-8 pairwise exclusion (L2 and R5 — or L2
and R6 — never both fail). Machinery proved: the master relations
W26-M/M* (every vertex at every support reduces to a three-vector
slice equation), Theorem W26-K (trigger-free slice matrices =>
det-M transfer => pure rows — the forcing branch that kills every
constructed counter-object), and the two-branch statement with
explicit Farkas certificates. The lane's controls caught and
withdrew TWO of its own claims (the vertex-4 lemma at m=25 via an
F_7 escape; the triangle exclusion via a p=7 co-failure) plus a
census keying bug — and its report honestly deflates its own
headline evidence (zero co-failures of (L2,R5) in 318 points is
weak support given base rates ~9/318 each; the DISJUNCTION at
318/318 with max 6-of-8 failures is the well-supported part).
**W30 launched on the exclusion** — with the explicit instruction
that the proof target is "some provable pairwise exclusion covering
all failure patterns", not necessarily (L2,R5).

---

## v49 addendum: A8 sweep complete — W28-T1 confirmed at full scale (2026-08-19)

A8's finishing computation landed: the full 127-case free-set
ideal sweep, on an implementation independent of W28's, returned
**381/381 unit verdicts** (127 cases x {char 0, char 1000003,
char 32003}, both primes = 1 mod 3 per ledger 19), 0 timeouts,
with the k=3 calibration correctly NOT-unit and an exact rational
point as the ledger-18 control. **W28-T1 (the symmetric case of
X_4-emptiness) is now confirmed at full scale, not sampled scale.**
Its stopped T1h run carries no information; A8's remark that T1h
would commit the diagonal chain is superseded by W29's normal-form
route (v47) — the diagonal theorem's gate is audit A9, in flight.
Lane record: computations/unaudited-audit-a8-2026-08-19/REPORT-FINAL.md.

---

## v50 addendum: A9 CONFIRMS W29-T1 at the promotion gate — commit as spine (2026-08-20)

A9's final verdict: **CONFIRMED, committable as spine, slightly
stronger than stated** — independently re-derived (every clause
family by hand from field facts alone), re-encoded with inverted
polarity, re-solved by five engines, drat-trim-verified (87/87 +
64/64), with the A2 row set re-derived from the raw 6561-word
enumeration (k=4 drops nothing at N=8: EXACT = X_4) and the XF
biconditional's licence traced to the true point. Strengthening
adopted: the machine only uses nonvanishing of the constant-word
amplitudes, so the theorem covers unnormalised GHZ over any field,
no algebraic closure. Scope: block-diagonal (classical edge-coloured
KG at N=8 is a corollary). TWO corrections around the theorem:
the **uniform-in-N claim is REFUTED** (N=10's exact level is X_6;
k=4 there is a strict relaxation and mostly SAT; even k=6 is SAT on
sampled orbits — honest scope: N=6 and N=8 closed, N>=10 open for
this machine; the in-flight N=10 k=4 run was STOPPED on this
verdict), and W29's 1,200-check control was single-case (repaired:
320 checks / 37 cases / 0 violations). Full record:
computations/unaudited-audit-a9-2026-08-20/REPORT.md. **Promotion
round launched (P2-diag)**: proof document + certified computation
dir + SUPERSESSIONS entry + README/PROOF-SKETCH updates, staged for
manager review, incorporating A9's three write-up repairs. The
now-moot diagonal adversarial builder was also stopped; the N=8
Groebner case-ideal corroboration keeps running.

---

## v51 addendum: W30 — (L2,R5) REFUTED at m=28; Theorem W30-X reframes 25-27; m=28 needs a new statement (2026-08-20)

W30's landing restructures Route A's endgame. (1) **W26's named
residual pair (L2,R5) is FALSE at m=28**: explicit co-failure
points over F_31 (2,270 found, 17 re-verified through 8 controls
including W26's own engine; replicated at F_13; (R5,R6)/(R5,R7)/
(L0,L2) also refuted). Root cause of the bad evidence: W26's ~2%
index-choice sampling over-reports failure (DELIVERS is a
disjunction over index choices); W30's exhaustive engine corrected
2 of 11 stored off-stratum patterns. Ledger lesson: evidence
tables built by SAMPLING a disjunctive predicate are upper-bound
evidence only — new hazards-ledger item candidate. (2) **The right
statement at 25/26/27 is unary, not pairwise — THEOREM W30-X
[probe-proved]**: via the trigger-free slice matrix + a cofactor
identity (a short independent proof of W26's det-M law), one
vertex per support NEVER fails: R6 at m=25 (|N|=2, unconditional
mechanism), R5+R6 at m=26, R5 at m=27 — verified sharp on 21,927
adversarial points, dedicated falsifiers scoring exactly 0. Gap:
hypothesis (H) (realisation with hafL != 0), verified pointwise,
not eliminated — the staged Singular elimination is the closer for
m=25/27. (3) **m=28 is structurally different** (every vertex has
4 Gamma-neighbours; the protection mechanism provably evaporates)
and the pairwise route there is dead as a characteristic-free
statement; the DISJUNCTION itself survived everywhere (max 6-of-8
over 21,973 points incl. a failure-maximising lane) and is now the
proof target at m=28. FOLLOW-ONS: A10 launched (audit of the
refutation + W30-X); W30 resumed to execute the (H) elimination
and design the m=28 disjunction attack; adv2's star builders
stopped (different object, not on the critical path). Lane record:
computations/unaudited-exclusion-w30-2026-08-19/REPORT.md.

---

## v52 addendum: registry scope verified from Lean source; Lean lane L1 launched (2026-08-20)

Verified directly against google-deepmind/formal-conjectures
(FormalConjectures/Paper/MonochromaticQuantumGraph.lean):
**eqSystem8_no_solution_d3 is the GENERAL BICOLOURED statement** —
`EdgeN` carries both endpoint indices and the matching sum uses
`W (mkEdge v u (iota v) (iota u))`; normalisation pmSum = 1 on
constant words. Consequences: (1) W29-T1 does NOT close the
registry case; it is the registry statement's DIAGONAL sub-case
(classical monochromatic-edge model) — P2-diag instructed to purge
any over-claim from the staged spine documents; (2) the registry
file carries FOUR open n=8 d=3 variants (C, R, Z, trinary-Z) —
closing our general bicoloured target closes all four at once
(any-field => any integral domain; the amplitude-nonzero
strengthening covers their =1 normalisation a fortiori).
**L1 launched** (Lean formalization lane): stage a
formal-conjectures-style variant statement
eqSystem8_no_solution_d3_diagonal + full formalization
architecture per algal's PR #4610 template, convert the 87 DRAT
proofs to LRAT, build the definitional skeleton on their pinned
toolchain, and measure kernel-replay feasibility. PR submission
itself is gated on the user.

---

## v53 addendum: W30 round 2 — the Q-span law (Theorem W30-Y); (H)-elimination target refuted (2026-08-20)

The staged (H)-containment was FALSE (explicit m=27/F_13 escape
with full controls — all vertices deliver there anyway), so (H)
was sufficient-never-necessary and the elimination is off. In its
place, **THEOREM W30-Y [probe-proved]: the Q-span law** — rank
S(tau) <= |N(v)| - dim span Q(tau); with two firing letters +
realised clean pairs (scale != 0) + span >= |N(v)|-2, the vertex
DELIVERS. Uniform in m; predicts the entire observed failure
table (604 pts, 0 violations), reduces m=25/R6 to realisation
side conditions alone (threshold 0), and explains m=28's survivor
structure (L1 in every maximal survivor set). REMAINING at
25/27: prove the realisation side conditions from template
combinatorics. At m=28: the law is sufficient-not-necessary
(hunters zeroed the hypothesis on vertex pairs without producing
failures) — the disjunction needs one more idea. Q-lift of the
m=28 refutation still open. A10's scope extended to W30-Y; W30
resumed on the side-condition theorem + the m=28 gap.

---

## v54 addendum: THE DIAGONAL THEOREM IS COMMITTED SPINE (2026-08-20)

SUPERSESSION-2026-08-20-01 accepted; certified commit 5c43902
(follow-up 248fb7e records it). Now on the public spine:
`proofs/eight-site-diagonal-obstruction.md` (dependency ID
N8-DIAGONAL) — no block-diagonal ternary weighting of K_8, over any
field of any characteristic, has all three constant-word amplitudes
nonzero and all mixed amplitudes zero; the classical edge-coloured
Krenn-Gu statement at n=8 is a corollary. Shipped with it:
`computations/verify_eight_site_diagonal_obstruction.py` (house
checker, SHA-256 frozen in the doc; passes python3/-O/-I -S; found
drat-trim and verified 87/87 proofs at the certifying commit),
`computations/certificates/n8_diagonal/` (193 hashed artifacts:
87 CNF+DRAT pairs, three UNSAT cores, orbit ledger with two
counting routes, replay driver, audit encoder + inspection-only
originals), `certification/audits/SUPERSESSION-2026-08-20-01.md`
(A9's audit of record + P2-diag's reproduction, kept separate),
and the README / PROOF-SKETCH / conventions-ledger patches (the
new bullet, Theorem 1.2 [P], the open-item table rows, hazard
items 5-6 of the terminology section: the fourth "witness" sense
and the X_k notation collision + per-N exactness-level table).
One promotion-mechanics defect caught and fixed mid-apply: the
mechanical patch application replaced the six-site README bullet
instead of inserting after it (restored immediately; both bullets
present). Honest boundary, stated in every touched document: the
general bicoloured n=8 (eqSystem8_no_solution_d3) REMAINS OPEN and
is this program's target; the diagonal proof consumes the product
factorisation and does not transfer to family (R) at 25<=m<=28.

---

## v55 addendum: W30 round 3 — Theorem W30-Z (failure requires slice rank 3); m=28 reduced to a determinantal disjunction; side conditions proved per support (2026-08-20)

The delivery-mechanism classification at W30's adversarial
endpoints is TOTAL, and it yields **THEOREM W30-Z [probe-proved]:
failure at a protected-class vertex requires slice rank 3**
(rank <= 2 => deliver, under the stated side conditions); W30-Y is
its special case. Blind-tested 240 measurements, 2 traced
exceptions. Consequences: (1) **m=28's disjunction is now the
determinantal statement "one of R5/R6/L1/L2 has slice rank <= 2"**
(36 vars/vertex; hunters in three fields never exceed 2-of-4 at
rank 3; Singular-sized, launch next); (2) the two-firing-letters
condition is **PROVED per support by exhaustive template
enumeration** with an exact negative control (the criterion
selects precisely the protected set); (3) the realisation half of
the tuple condition is PROVED combinatorially; the scale half is
the known point-dependent escape with exact minimal sizes
(>=12/81 at m=25 — hunters reach 33/81 but never a cover);
(4) the Q-span escape at m=27/R5 is **reduced to an N=6
statement** — the three 6-vertex sub-models (4 matchings each)
all on their vanishing strata — a hand-off to the campaign's
proved N=6 machinery. m=25 is one scale-escape statement from
unconditional. Round 4 tasked: the 36-variable Singular
elimination at m=28; the N=6 hand-off at m=27; the m=25 cover
characterisation.

---

## v56 addendum: W30 round 4 — unary shortcut refuted over Q; m=28 = one of four pairwise rank-3 exclusions; m=25 down to two minimal covers, 45-var elimination in flight (2026-08-20)

W30's own falsification hunters killed its two newest candidates
before use: the unary "R6 never at rank 3" shortcut (Q
counterexample — also proving W30-Z's converse false) and side
condition (c) as a necessity (Q-span 0 with delivery at rank 1).
W30-Z survives untouched and governs. The m=28 disjunction target
is now exact: max simultaneous rank-3 is 2-of-4 in three fields
(only {L1,L2}, {L2,R5} ever reached), so ANY ONE of the four
never-reached 2-subset exclusions ({R5,R6}, {R5,L1}, {R6,L1},
{R6,L2}) closes m=28. m=25's scale escape has EXACTLY two
inclusion-minimal covers (12, 30; minimality machine-checked);
the size-12 elimination (74 gens / 45 vars) is running in three
characteristics — the first tractable-looking Singular job of the
lane. Bonus lemma: the (b) and (c) escapes are disjoint (on
hafL = 0, Q4 degenerates to a product of three Gamma cells). The
N=6 hand-off narrowed: only Q2 is a true N=6 model, and the
six-site theorem addresses exactness not vanishing — no direct
bridge; noted for the induction lanes. Round 5: harvest the m=25
verdicts, eliminate the size-30 cover too, launch one m=28
pairwise exclusion, keep the Q co-failure hunt alive.

---

## v57 addendum: A10 confirms W30's core with corrections — the pure rows survive at every co-failure point; the (H) gate is retired (2026-08-20)

A10 (from-scratch engine, zero code reuse) CONFIRMS: the m=28
refutation (17/17, mutation controls 8/8) under the OPERATIVE
predicate FAIL_primary (both lanes' code compute the same
predicate — the hazard was W26's prose (*), a consequence valid
only where a coefficient is forced, and none is forced at m=28);
Theorem W30-Y (strictly cleaner than W30-X, which A10 retires:
its step (1) is false as written — the correct object is the
augmented slice matrix S', which the CODE already used — and
unnecessary); the escape object; the m=28/L2 exception; the
protected table (recounted exactly); and the sampling artifact
(WORSE: effective coverage ~9-21 choices per vertex; a third
spurious stored verdict found). CORRECTIONS TO v51: the
refutation is over F_31 (F_13 replicates (R5,R6), not the named
pair); the C-statement is untouched (ledger 24 added); and —
decisive for Route A — **every one of the 17 co-failure points
still carries 410-1,694 genuine pure rows: the residual system
still kills them all. What died is the proof device, not the
kill.** Ledger 25 added (sampled disjunctive predicates are
one-sided). THE (H)-ELIMINATION GATE IS RETIRED: three
independent escape objects exist (incl. one over Q at m=25 and
one co-occurring with a real failure); (H) is not implied by
cleanness; at every escape point the vertices still deliver for
an unexplained reason — identifying THAT mechanism (or a case
split over the escape locus) is the real remaining problem at
m=25-27. Promotion-ready per A10: the W26-M/M* identities, the
cofactor identity, the Q-span bound, conditional Lemma W30-Y
(S'-form), and the record corrections. W30 redirected: test
A10's Q escape point against the m=25 cover ideals BEFORE
trusting the in-flight eliminations; the m=28 pairwise rank-3
exclusion targets are unaffected and continue.

---

## v58 addendum: m19 verdict-complete (310/310, 0 survivors); W30 round 5 — cover route retired, D2 eliminated as the escape mechanism (2026-08-20)

**m19 MILESTONE: all 310/310 classes now carry verdicts, 0
survivors** — Route A's support ladder is verdict-complete through
m=19. Residue per ledger 23: ten classes sit in the unchecked
proof-verification queue (drat-trim timeouts / RUP-on-DRAT
mismatches) with the full-DRAT re-checks running; the ladder claim
stays "verdict-complete, proof-verification queue draining".
W30 round 5: the m=25 cover-based elimination is RETIRED (A10's Q
point contains the size-30 cover outright and its R6 delivers at
264/264 surviving choices — covers were the old device's
necessity, not FAIL_primary's); the D2 closed-form candidate was
refuted by the lane's own control (the pairing is an identity);
and **D2 fires at none of the escape objects** — so the
escape-point protection is neither Q-span nor D2, and my proposed
case split is dead. Two mechanisms eliminated; the open problem at
m=25-27 is now sharply "what forces delivery on the escape
locus?" (at A10's point: plain non-collapse). Round 6 tasked:
sweep the escape locus for delivery-mode statistics FIRST, then
formulate FAIL_primary at the protected vertex as a finite case
tree pruned by W30-Z (the all-degenerate branches look like
total-degeneracy exclusions — e.g. all index choices zero-scale
forces hafL-type vanishing everywhere, to be contradicted from
cleanliness + cells-nonzero + off-stratum via the master
relation). m=28 pairwise eliminations continue unchanged.

---

## v59 addendum: W30 round 6 — escape mechanism = plain non-collapse; Branch T (|X_v| = 42, uniform) is the new sharp target; fleet triage at load 248 (2026-08-20)

The escape-locus sweep settles the mechanism question empirically:
deliveries there are plain non-collapse (M_D2 = 0, M_inside = 0
across 22 escape points / 6,523 index choices); the escape
geometry deletes choices (sc = 0) and uniquely enables — but never
universalises — collapse. FAIL_primary now splits as a case tree:
**Branch T** (hafL vanishing on X_v — with the clean uniform
invariant |X_v| = 42/81 at every protected vertex and every
support 25-28) is NECESSARY for any failure, has never been
reached (A10's 54/81 record point misses 12 of the 42), and is a
sharp 42-equation elimination target; **Branch C** (all survivors
collapse) is where the round-3 collapse machinery lives. The
pre-launch control (test every elimination target against stored
escape/refutation objects) is standing practice. OPS: machine at
load 248/18 cores — Singular starvation is the likely cause of six
rounds without a verdict; W30 told to triage its ~40-process fleet
to <= 8 (Branch-T hunters, Q co-failure, Singular jobs get the
cores); W18 told to drop to 2 workers (m19 is verdict-complete;
only the 10-proof recheck queue remains); A10's finished builder
stopped. LAUNCHED LIGHT: P3 (promotion staging of A10's green-lit
pieces + the m<=19 ladder closure document) and W31 in DESIGN MODE
(the C_8/empty-clean stratum: statement + attack plan + pre-launch
controls; compute phase gated on the fleet draining).

---

## v60 addendum: L1 — the Lean UNSAT layer is DONE; feasibility confirmed with four plan changes (2026-08-20)

L1's deliverables landed (computations/unaudited-lean-l1-2026-08-20/):
**all 87 orbit refutations are already Lean theorems** (kernel-
checked via Std.Tactic.BVDecide verifyCert_correct; lake build
19.2s; axiom closure clean, no sorryAx; payload 29 MiB), and the
proposed registry statement ELABORATES against formal-conjectures'
pinned toolchain (lake --wfail rc 0; 84 additions, 0 deletions;
the registry's own Witness4_d3 proved diagonal, sorry-free — the
N=4 sharpness control is formalised). Plan changes: (1) drat-trim
-L LRAT is REJECTED by Lean's checker (CaDiCaL native --lrat
accepted on all 87); drat-trim -f forward-mode LRAT emission is
rejected even by its own checker — note for the certified
package's docs (verification chain unaffected; emission only);
(2) algal's PR is kernel-proved via verifyCert_correct (not raw
native_decide) — our trust story can equal, not beat, it; plain
`decide` stack-overflows; (3) 87 orbits beat 4096 decisively
(29 MiB vs 1.3 GiB; the coverage table is ~300 lines since the
normal form already forces the symmetry machinery); side benefit:
a fresh 4096/4096 full-ledger reconfirmation of the theorem;
(4) STATE OVER CommRing + IsDomain — covers the diagonal reading
of ALL FOUR open n=8 d=3 registry variants (C, R, Z, trinary) in
one theorem; verified to elaborate. Remaining: the mathematical
bridge, 13-19 agent-sessions (product formula highest risk; an
a9_enc variable-numbering fix is mandatory BEFORE bridge code).
Recommended order adopted: canonical re-emission -> **N=6
rehearsal (13 orbits, full bridge in miniature)** -> N=8 bridge ->
pinned certificate repo -> PR (timing gated on the user and on
PR #4610's precedent). Drive-by for the user: the upstream module
miscredits Chandran2022/2024 (should be L. Sunil Chandran,
Rishikesh Gajjala) — an upstream issue is the user's call.

---

## v61 addendum: TWO CORRECTIONS — m19 is 267/310 (v58's headline was the manager's miscount); Branch T is empty, not necessary (2026-08-20)

(1) **v58's "m19 verdict-complete (310/310)" is WITHDRAWN.** W18's
reconciliation of closing rows against CNF certificates (two
views, exact agreement) shows **m19 = 267/310 with 43 classes
bearing no verdict at all**, and the recheck queue is 1 (the
15711611 drat18 run), not 10 — both wrong figures were the
manager's own naive record count over worker jsonl streams.
Ledger item 26 added. W18 restarted 2 nice-12 workers on the 43
open classes and will post the final tally only when the numbers
are real. (2) **W30's round-6 claim "Branch T is necessary for
any failure" is WITHDRAWN** (its own round-6b classification:
FAIL = T OR C, and all 801 stored vertex failures across every
support are Branch C; Branch T has never occurred — eliminating
it would close nothing; the pre-launch control surfaced this
before the elimination launched, its second save). Also corrected:
|X_v| = 42 is not uniform (six sampled R-vertex cases
over-generalised; per-(m,vertex) table now stored). THE SHARP
RESIDUAL at protected vertices is now the INTERSECTION statement:
FAIL_primary <=> (the (b)-escape: no slice tuple has both clean
pairs surviving) AND (every surviving index choice collapses with
the firing row outside) — each conjunct separately witnessed
(A10's Q point; the 6,523 non-collapse deliveries), the
conjunction never observed, and known-hard (the round-3 lattice
run returned 0/64 certificates on its m=25 form). W30's fleet is
purged to 6 jobs; the load (217-245) is now mostly other lanes;
the 45-variable m=25 elimination has had cores and still returns
nothing — to be called genuinely hard if silent after an hour at
the reduced fleet. m=28 unchanged (four pairwise rank-3
exclusions; Branch T contributes nothing there — the co-failures
are all Branch C).

---

## v62 addendum: W30 round 7 — the m=25 mechanism found (3x2 slice matrix); theorem conditional on two small algebra statements (2026-08-20)

The structure-first directive paid off: at m=25 the whole
escape/collapse frame dissolves — N(R6) = {5,7} makes S' a 3x2
matrix, the cofactor identity two-term, and **Q != 0 forces
rank S' <= 1 with nonzero rows, i.e. delivery at every hafL != 0
choice**. The intersection target cannot occur at m=25. What
remains for THEOREM W30-M25 ("R6 delivers at every clean
off-stratum all-cells-nonzero m=25 point") is exactly two small
statements: **(alpha)** not every admissible choice has hafL = 0
(Branch T at R6@25 — never observed anywhere, now a SMALL hafnian
system to eliminate), and **(beta)** some matching untriggered
word has Q != 0 — where Q = 0 forces TWO required values of the
SAME hafL, i.e. a Gamma-cell identity (l03.d1.d2.r47 =
l23.d0.d1.r45 after eliminating hafL) — candidate for a few-
variable elimination or a direct cleanliness contradiction. Both
are order-of-magnitude smaller than anything launched before —
matching the lane's own diagnosis that its ideals were too big.
The 45-variable cover elimination is called GENUINELY HARD and
moot. The m=28 {R6,L1} launch was deferred on mechanism grounds
(the |N|=4 analogue needs Q-span >= 2, refutable per the round-4
Q counterexample) — deferral endorsed; the |N|=4 mechanism
re-derivation is round 8's second task. Corpus-thinness flagged:
the m=25 result rests on 10 one-factory points + A10's; an
independent generator is round 8's control task.

---

## v63 addendum: W30 round 8 — (alpha)/(beta) survive the binomial engine; mechanism cross-validated in a second family; ledger 27 (2026-08-20)

Both m=25 residuals came back certificate-free from the lattice
engine (honest negatives; the binomial route is exhausted against
them — their remaining content is non-binomial: the hafL pinning
for (beta), the 42-trinomial system for (alpha)). The 3x2
mechanism itself REPRODUCED in an independent construction family
over F_13 and F_31 (rank S' = 1 at 9/9 tuples, delivery 6/6) —
with a refinement the second family caught: Q = 0 can occur at
individual words (6 at one F_13 point); the operative and
observed statement is "Q != 0 at some untriggered word per
class". Ledger 27 added (pre-launch controls must test the exact
target). ROUND 9 redirects both residuals to their LINEAR
structure, below the Groebner threshold: for (beta), the escape
needs Q = 0 at EVERY word of EVERY class — words sharing an
L-part force EQUAL pinned hafL values, i.e. pure cell identities
across word pairs (enumerable, hand-checkable); for (alpha),
hafL is one multilinear form and Branch T = 42 evaluations
vanishing — compute the exact rank of the evaluation map on the
monomial support: full column rank would force all cell-product
coefficients to vanish against cells-nonzero. Both are exact
linear algebra, the lane's proven strength.

---

## v64 addendum: W30 consolidated close-out — (beta) reduces to "A45 never rank one" (one 3x3 determinant); (alpha)'s linear layer cannot close (2026-08-20)

W30 round 9 + consolidated final report: neither residual proved,
but (beta) is now REDUCED — the escape forces A45 and A47 rank
one (the y5/y7 letters range over all three values, so the
eliminated-hafL binomial system factors through rank-one-ness),
while the measured corpus has A45 at rank >= 2 at 10/10 points.
**The hand-off target: "at a clean off-stratum all-cells-nonzero
m=25 point, A45 is never rank one" — one 3x3 determinant in 9
variables against cleanliness — the smallest open statement the
campaign has produced.** (alpha)'s linear layer is provably
insufficient (evaluation matrix 42x126 has full row rank, kernel
dim 84), so Branch T emptiness is genuinely nonlinear; the
adversarial route (build a Branch T point via the kernel
parametrisation, constrained by realizability of hafL
coefficients as cell products) is the honest next test — if a
Branch T point is buildable, (alpha) is FALSE and the m=25
theorem needs different scaffolding. Round 10 tasked on exactly
these two. The lane's nine-round record: 7 own claims withdrawn
under controls, 0 Singular verdicts, every advance from structure
+ exact enumeration; consolidated report persisted in the lane
REPORT.md; promotion-ready list matches A10's (P3 has it staged;
the W30-Y bundle stays gated on round 10's outcome).

---

## v65 addendum: W30 lane closed (10 rounds) — THEOREM W30-M25-CONDITIONAL stated; the A45 reduction refuted by its own build; the true (beta) target is the common-direction pair (2026-08-20)

W30's final round: (1) its own adversarial build REFUTED the
round-9 A45 hand-off (a clean rank-one-A45 point exists over
F_31 — a 10-point never-observed fell in one round; ledger 27's
lesson enforced by the lane on itself); the analytically-settled
true (beta)-escape target is **A45 and A47 both rank one with a
common column direction shared with A14's row** — never reached.
(2) The independent family found the mechanism's boundary: one
F_13 point with rank S' = 2 everywhere and 54 Q=0 words — where
(beta) fails and R6 STILL delivers — so the corpus contains no
counterexample to the CONCLUSION anywhere (43 points, two
families, three fields). (3) **THEOREM W30-M25-CONDITIONAL is
stated in full** (proof chain + verification record + hypothesis
status) and goes to the promotion pipeline alongside the
A10-confirmed machinery; hypotheses (alpha)/(beta) remain the
m=25 residue, with the honest possibility that the alpha-builds
still running on disk settle (alpha) either way. Lane record:
7 own claims withdrawn under own controls across 10 rounds, 0
Singular verdicts, every advance structural. NEXT: P3 finishes
the checker + audit record -> commit bundle 1 (identities +
record corrections, A10-covered); A11 will audit the
post-A10 additions (W30-Z, M25-conditional) before bundle 2;
the successor probe (W33: (alpha)/(beta)/common-direction pair +
the |N|>=3 mechanism at m=26-28) launches after W31/W32 report
and W30's detached builds are harvested.

---

## v66 addendum: attack-surface review — five named gaps (2026-08-20)

What the campaign is NOT attacking, ranked: (1) **the dormant
Cartan–Spencer architecture** — by its own 2026-08-13 accounting
Gate I stood at two relative C4 cells + one filler datum, with
the psi_z dual analysis showing one column datum (Eq = -u,
ainc = +1) closes both the balanced square and the shared-loop
frontier; untouched since; the only route stated at all h; QUEUED
as W34 (revival scoping) when a lane frees. (2) **archimedean
methods** — no lane has ever attacked the C-statement with
positivity (SOS/Positivstellensatz on the real-imaginary split);
a different engine that handles overdetermination well; QUEUED as
W35 (feasibility probe: can an SDP-guided exact rational SOS
certificate refute a small subsystem where Groebner failed —
calibrate on the proved m=26 case first). (3) **the n=4-echo
structure theory** — "every resisting stratum embeds 4-site
exceptional geometry" is an observed pattern (C_8 stratum,
4+2-split sub-hafnians, T1h family, the (4,4,2) profile at N=10)
worth a classification lane: how does the n=4 source embed in
K_8 and what does each embedding force; would unify the two
hardest leftovers. (4) **the full-block parity decomposition**
(the conjectured product-formula replacement) — only obliquely
covered by W32 line 3. (5) **external monitoring dark since
08-12/13** — LW launched now (web-only): formal-conjectures PR
status, the in-prep tensor-algebraic paper, the competitor repo,
and anything citing our published diagonal theorem. Also noted:
the general-bicoloured (6,3) + descent Lean formalization is a
deliberate non-goal for now; the m=20-24 promotion debt rides
with P3/P1-doc drafts.

---

## v67 addendum: promotion bundle 1 committed as spine; W31's design lands the frame-disjointness lemma; ff5/ff7 flagged hollow (2026-08-20)

**Committed spine (SUPERSESSION-2026-08-20-02/-03, certified
commit 32bb834)**: proofs/slice-master-relations.md — the master
relations, the cofactor identity on the augmented slice matrix,
and the Q-span bound (all A10-re-derived), with the house checker
(mandatory core at random non-clean blocks + mutation controls;
corpus steps optional-but-loud) and the record-corrections ledger
entry (three spurious verdicts retired; the m=28 refutation
scoped to F_31/FAIL_primary; pure-row survival recorded). §5
(conditional Lemma W30-Y) is GATED for -04. P3's checker caught
its own authoring error on first run (guessed m=27 PM count 13,
true 12) — the pattern holding.
**W31 design phase**: the stratum = W19-K's Gamma-forced
empty-clean layer, EXACTLY 75 of 794 admissible Gamma classes,
|F| in {0,2} (|F|=1 impossible: 2-connected => no bridge).
**LEMMA W31-1 [probe-proved]: every slack-0 (R) template has
>= 824 effectively clean mixed words** => the stratum requires
slack >= 1 => Route A's joint-theorem frame and the stratum are
DISJOINT BY A THEOREM (not by a failing hypothesis) — every
object of the joint theorem (hafL, hafR, S, Q, the 8 vertices) is
undefined there. Census done (75-class table; per-support
inhabitation NEVER decided — all stored (R) witnesses are m=28;
bounds |Gamma|+13 <= m <= 28; ~600-instance SAT sweep specified
with slack-0-must-UNSAT and m=28-must-SAT calibrations). Ranked
attack: R1 coverage/slack budget; R3 permanental Q-span (the
cofactor identity survives; L-free words replace clean words;
Gamma-degree 2 everywhere => MONOMIAL cofactors => Q != 0 is
FREE); R2 two-word permanent kill (gated on a zero-compute
extension test of the stored Q(omega) family); R4 the
never-yet-run adversarial stratum builder. Record corrections
from W31: the W19 retraction was NARROWER than assumed (A7
re-certified W19-K + the census; independently re-derived, 0
mismatches); "214 vs 75" disambiguated (stored representatives
vs Gamma-forced classes); **ff5/ff7 sweeps have full_checks: 0 —
the "complete F_5 classification" cited in this plan establishes
NOTHING as stored** and must be traced to m2ff5.py's code path
before anything leans on it. **W31 COMPUTE PHASE AUTHORIZED**:
R1 + R4 concurrently (single-threaded cadical, checkpointed,
nice), R3 immediately (seconds of exact linear algebra), R2 only
after its pre-launch extension test. W18 status: m18 done, m19
267/310 on 2 nice workers, backfill 352/~650, the one unchecked
proof under drat18 (its cheaper re-solve fallback approved).

---

## v68 addendum: W32 final — the 2-colour reduction (W32-2COL); the abstraction route closed by theorem (W32-ABS); first non-diagonal emptiness theorems (2026-08-20)

W32's landing gives Route B its sharpest-ever structure.
**W32-2COL [proved]**: an X_4 point's three 2-colour restrictions
are each exact d=2 sources on K_8 (the only off-count-5 profile at
N=8 is (3,3,2) and it is trichromatic — so bichromatic words are
all imposed). **W32-RES**: X_4 <=> three exact d=2 restrictions +
4116 trichromatic imposed words vanishing — i.e. the diagonal
census's "(C) and (D)" with the pair restrictions now ranging over
the FULL d=2 solution variety (nonempty: 21,760 exact d=2 sources
found, 2,208 genuinely non-diagonal — 2COL cannot kill alone).
**W32-ABS [proved]**: H_w = 0 implies a cell-vanishing disjunction
IFF exactly one matching is alive — and on full support the
hafnian is IRREDUCIBLE (Singular factorize, three sizes) => the
vanishing-pattern Boolean route is PERMANENTLY CLOSED for general
blocks ("the obstruction is irreducibility, not ingenuity" — do
not fund another abstraction attempt). **W32-M1 [proved, any
field]**: no X_4 point with disjoint-PM pure supports and <= 1
nonzero cross cell (156 orbit reps deciding 33,233,760
configurations, unit over ZZ); its m=0 case is an independent
full-Groebner proof of W29-T1 on PM supports (which the SAT route
had only sampled at N=4/6); m=2 in flight (6,808 orbit cases all
unit, 4/8 orbits). Lemma survival: W27-R1/R2 SURVIVE off-diagonal
(calibrated); W28-SYM only with trivial colour action (the
rotation version reproduced W28's own soundness catch); W28-DEC
and W28-FREE do NOT transfer (parity needs diagonality; the free-
site split needs SPARSITY). X_4 is a non-convex invariant cone —
averaging arguments cannot transfer, closing that route too.
Builder: calibrated at k=3 (1,215 fires incl. cross-cell
directions), silent at k=4 across ~2,000 backgrounds — searches,
not evidence. **The next-lane structure is named**: the
third-colour star kernel Ker_j (dim-6 on diagonal-like pairs, dim
0 at some site for genuinely non-diagonal d=2 sources — the
squeeze: diagonal restrictions land in W29-T1's territory,
non-diagonal ones collapse kernels; W32-KER: all 24 kernels zero
=> block-diagonal => W29-T1 kills); the d=2 solution variety at
n=8 is now a REQUIRED input; m=3 is feasible after run_22's
linear pruning (140/168 placements die linearly). W32's own
method-negatives recorded honestly (run_07 condemned by its own
control; run_10 repaired per ledger 27). **W33 LAUNCHED**: the
d=2 variety + kernel squeeze + m=3.

---

## v69 addendum: LW external sweep — n=8 d=3 over Z claimed externally (char-2 contraction); a complete char-2 descent exists; visibility gap (2026-08-20)

LW's sweep (full report:
computations/unaudited-litwatch-2026-08-20/REPORT.md). TWO urgent
items. (U1) formal-conjectures **PR #4659 claims n=8 d=3 over Z
and over {-1,0,1} — and the FULL even-N>=6 D>=3 integer case** —
community-verified, axiom-clean, unmerged only because the
reviewer has been silent for a month. Method: char-2 push + a
complete N->N-2 contraction + a six-vertex char-2 base.
Consequence for our registry story (amends v52): of the four open
n=8 d=3 variants, the Z and trinary ones are externally
claimed-closed; the genuinely open field cases are C and R — our
general-bicoloured target. No collision with our diagonal theorem
(complementary scopes); the free F_2 consistency check is
assigned to L1. (U2) **their contraction lemma is a complete
kernel-checked descent induction in char 2**, and its proof
isolates the char-0 obstruction exactly: the multi-update-edge
cross terms vanish by even multiplicity — a characteristic-2
accident. In char 0 those cross terms are precisely the residual
our descent must control. The unstaffed induction now has a
mandatory first reading and a candidate shape (carry the cross
terms as an explicit error term). Also: the FC ledger is a
LAGGING indicator (five verified-unmerged PRs; do not use
answer(sorry) as the oracle); the tensor-algebraic no-go paper
remains unposted (largest external risk; weekly checks); the
competitor repo made no n=8 progress and its overlapping nodes
did not move; **Krenn is personally watching the competitor and
unaware of us** (0 external signal on our repo in 3 public
weeks) — the visibility question is surfaced to the user.

---

## v70 addendum: W32 delta — THEOREM W32-M2 (m=2 of the cross-cell filtration, char 0, exhaustive) (2026-08-20)

run_17 completed: **11,920/11,920 placement-pair orbit
representatives unit in char 0, 0 survivors** — deciding
2,775,018,960 configurations (197,820 disjoint-PM triples x
14,028 cross-cell pairs) by orbit reduction. The cross-cell
filtration now reads: m=0 unit over ZZ (10 characteristics);
m=1 unit over ZZ (156/156, twice-derived); m=2 unit char 0 with
the ZZ upgrade in flight (run_23, ~650/11,920 at last checkpoint,
timeouts recorded as unchecked per ledger 23; results_t23.json).
The ledger-20 hunt stands at 1,707 backgrounds / 0 hits at k=4
vs 1,215 firing hits at k=3. W33 (already launched on the d=2
variety + kernel squeeze + m=3) pointed at the checkpoints.

---

## v71 addendum: user decision — the diagonal theorem ships as a formal-conjectures PR with full Lean formalization (2026-08-20)

The user chose the PR-with-Lean channel over an immediate arXiv
note. L1's bridge is now the campaign's primary external
deliverable: finish the remaining components (WLOG symmetrize,
FREE/B1, ledger + nine clause families, 4096->87 coverage table,
assembly; revised estimate 6-10 sessions), package per the
#4610/#4659 precedent (standalone certificate+Lean proof repo
staged for the user's account + a slim FC PR branch adding the
diagonal variant statements — over C, plus the CommRing+IsDomain
strengthening covering the diagonal reading of all four registry
variants), and stage the PR description with the two-audit
provenance and the #4610/#4659 relations. Everything staged
locally; the user pushes and submits under his identity; no
upstream contact by any lane. The arXiv note remains available as
a fallback if external priority risk materialises (the unposted
tensor-algebraic paper); the trust bar is the no-native_decide
standard, which the kernel-checked verifyCert_correct route
already meets.

## v71.1: packaging correction — the existing public repo IS the proof repo (2026-08-20)

Per the user: no separate standalone proof repo. L1's Lean project
+ canonical LRAT artifacts get committed INTO this repo (proposed
formal/n8-diagonal/, matching the existing formal/ conventions),
and the FC PR's formal_proof reference points here — one
provenance chain: proofs/eight-site-diagonal-obstruction.md +
computations/certificates/n8_diagonal/ + the Lean subtree, all
under rrajasek95/krenn-conjecture.

---

## v72 addendum: W31 compute phase — R2 gate refuted; ff5/ff7 unsound (ledger 28 + a ledger-19 correction); Lemma W31-1 independently reconfirmed; THE C_8 MEMBER IS A DOUBLED N=4 GHZ SOURCE (2026-08-20)

W31's opening results. (1) **R2's target is refuted at the
zero-compute gate**: an explicit exact witness (148 nonzero
occupied cells, all 162 permanent equations satisfied, full
controls) realises TWO L-free words simultaneously — including
the maximally coupled pair — so W20's two-word kill is
necessary-not-sufficient; a revived R2 needs >= 3 words or the
L/R mirror; no Singular was wasted. One ledger-17-style vacuous
control was self-caught and repaired mid-phase. (2) **The
ff5/ff7 trace: the sweeps were UNSOUND, not just unrun** — an
over-strong pre-filter (colspace vs restriction-to-V_1) rejected
every candidate including a stored INTEGER counterexample whose
permanent vanishes in every tested characteristic; ledger 28
added, and ledger 19's diagnosis of the W21 incident is corrected
(the practice stands, the cube-root explanation was wrong).
(3) R3's permanental Q-span law verified exact and TIGHT
(equality at the witness; generic points would force rank <= 0 —
the law is exactly the solution-locus constraint); sharpened
target dim P_j >= 3 => collapse; round 2 must be exhaustive over
the 30 L-free words (ledger 25). (4) R1's inhabitation sweep is
running with both calibrations green — including an independent
machine-checked reconfirmation of Lemma W31-1 (m=20 slack-0
UNSAT, drat-trim verified, via a different encoding); m=21..27 in
flight. (5) **THE STRUCTURAL HEADLINE: the C_8 stratum member is
two disjoint copies of the N=4 exceptional GHZ source** (its
twelve single cells realise the GHZ_4^3 template [1,16,256,256,
16,1] once per K_4 side) **joined by a cross Hamilton cycle of
full blocks + 8 fat cross blocks** — the n=4-echo pattern (v66
item 3) made concrete: the conjecture's one true positive
generates its hardest residue. It explains W20's L-free reduction
structurally (L-free words = the L-copy's GHZ inactive) and gives
R4 its correct ansatz (deform the doubled source over the 144
cross cells only). W31 directed to extend: check whether the
other 74 stratum classes also embed GHZ_4 copies — the n=4-echo
classification for the entire stratum.

---

## v73 addendum: W32-M2 upgraded to ANY FIELD; W37 launched on witness existence (2026-08-20)

The ZZ recomputation completed: **11,920/11,920 unit over the
integers** — a strong Groebner basis over ZZ containing 1 gives
1 = sum f_i g_i with INTEGER coefficients, valid in every
commutative ring. The cross-cell filtration (m = 0, 1, 2; 2.8B
configurations total) is now uniformly any-field, matching
W29-T1's strength. The decisive non-vacuity control: the same ZZ
pipeline is correctly NOT-unit at rungs k=2/k=3 and unit at k=4 —
the integer criterion genuinely separates the ladder. W32's lane
is fully closed (one detached hunt keeps checkpointing: 2,936
backgrounds, 0 hits at X_4 vs 1,215 firing at X_3).
**W37 LAUNCHED on T7@8 — witness existence at N=8** (the
campaign's highest-leverage missing theorem: with the committed
descent + six-site base it closes n=8 alone, and its all-n version
closes the conjecture): dissect the W25-F8 all-blocked X_3
falsifier against the X_4/X_5 equations (which violated equations
sit exactly at the blockage), formulate the SC-condition gap as a
local statement and test on the full stored corpora two-family
style, prove the N=6 rigid-stratum witness law (why exactly 9),
and run the X_4 all-blocked adversarial builder (its systematic
failure points ARE the witness-restoration mechanism). The
missing-theorem hierarchy (T1-T8) recorded in this addendum's
companion discussion: T7 (witness existence) > T1 (general X_4)
= T5 (full-block cancellation) > T2/T3/T4 (Route A set) > T6
(n=4-echo master) > T8 (char-0 descent with error term).

---

## v74 addendum: L1 session — trust-bar correction; DECISION: bespoke kernel RUP checker; the #4659 error term extracted (2026-08-20)

L1 corrected the manager's earlier claim: our stock LRAT replay
(verifyCert_correct) does NOT meet #4659's no-native_decide bar —
it matches #4610's native_decide precedent only, and the gap is
structural (Lean's LRAT parser is partial-def; even pre-parsed
check_sound kernel-sticks on a 1-variable instance).
**COORDINATOR DECISION: option (b) — write the bespoke
kernel-reducible RUP checker with its soundness proof**
(~1.5-2.5 sessions; our cores are RUP-only which bounds the work;
gen_lean_core.py already emits the input format; our own
formal/FORMALIZATION.md advertises the clean axiom set; the
axiom question is visibly what has stalled #4610 for a month).
Fallback: if the checker exceeds 3 sessions, revert to
native_decide with the axiom audit stated plainly. Burndown:
components 1-5 + 11 DONE sorry-free (incl. the staged
formal/n8-diagonal/ subtree building clean on their toolchain
with 87 core CNF/LRAT pairs at 4.1 MiB); remaining = FREE/B1,
the WLOG symmetrize, ledger + nine clause families, the coverage
table, and the checker. #4659 ANALYSIS (RELATED-4659.md): their
contraction does NOT preserve block-diagonality (200/200 leave
the stratum; genuinely different mechanisms, neither a corollary
of the other); **the char-2 contraction's rankTwo lemma is
exactly a factor-of-2 statement — the explicit error term
2.sum P_S.Q_{S^c} is now extracted symbolically**, the concrete
starting point for T8 (char-0 descent with error term), plus two
further char-2 leaves with their error terms and one pivot step
with NO char-0 analogue. F_2 direct consistency: N=4 SAT
(rediscovering the registry's own Witness4_d3 — their base is at
six for exactly this reason, and it is), N=6 UNSAT — mutual
corroboration with our machine. PR framing note adopted: if
#4659 lands, the Z slice is theirs; our claim is CommRing +
IsDomain with C/R ours alone.

---

## v75 addendum: LEMMA W31-2 — the GHZ_4 embedding classifies the stratum into three tiers; C_8 is the UNIQUE doubled class (2026-08-20)

W31's extension answered with the negative branch: the embedding
is NOT universal. **LEMMA W31-2 [probe-proved]**: a doubled-GHZ
placement needs every Gamma edge crossing a 4|4 split, i.e.
Gamma inside K_{4,4}; and since |F| IS the permanent of the 4x4
biadjacency matrix (strictly monotone on 2-connected graphs),
balanced-bipartite + spanning 2-connected + |F| <= 2 forces
Gamma = C_8. **Exactly ONE of the 75 stratum classes (C_8)
admits a doubled-GHZ template** (unique split, template verified
in (R)); 65 classes admit >= one GHZ_4 copy (including all six
|F|=0 classes); **10 classes admit NO copy at all** — the new
kill-priority list (masks recorded), since they lack the
structural protection. Structural punchline: "every Gamma edge
crosses the split" is EXACTLY the condition making hafL/hafR
vanish identically — the structure that makes the C_8 member
interesting is the same structure that makes it invisible to
Route A's slice machinery. Discipline notes: the census-rep-vs-
class confusion recurred (W19 reps have a different cell profile
— thin blocks serving (SC) in place of singles — so embeddings
CANNOT be read off representatives; caught by control E1, kept
as regression F2); R4's hill-climb objective is wrong for
exact-zero varieties (round 2 = structured ansatz + exact solve
on the doubled-GHZ deformation). R1 inhabitation sweep m=21..27
still in flight, calibrations green. Next: R3 round 2 (exhaustive
30-word span), the 10 no-copy classes under the R3 law first.

---

## v76 addendum: LEMMA W31-3 — the one-sided permanental reduction covers 65 of 75 classes; the tier structure is the reduction's DOMAIN; the calibration-gap finding (2026-08-20)

W31 checked the law's domain before running it, and the priority
inverted. **LEMMA W31-3 [probe-proved]: the L-free permanental
reduction exists iff Gamma has an independent 4-set, and ONE side
suffices** — a genuine generalisation of W20's identity (stated
for one member, used both sides) to 65 of the 75 stratum classes;
888 exact identity tests, 0 mismatches; negative control breaks
it at 160/162 words. The tiers are therefore the reduction's
domain, not protection levels: tier C = C_8 (two-sided), tier B =
64 classes (one-sided; the permanental Q-span law applies —
mechanised bulk), **tier A = the 10 classes with NO independent
4-set — no reduction, no input, the true hard core**, failing R3
exactly as the stratum fails Route A: empty input one level down.
The mechanism-less residue shrinks 75 -> 10. A row-constant
shortcut was checked and closed (8/16 cross blocks have a dead
cell with occupied column-mates). R4 RETIRED on a campaign-level
finding, now ledger 29: there is NO calibratable nontrivial
positive anywhere (GHZ_4^3 has all mixed fibres empty), so
build-an-exact-source searches cannot be validated in principle;
the working builder role is targeted refutation against named
lemmas. R1 grinding m=21 (the hardest instance, adjacent to the
slack-0 boundary), calibrations green. NEXT: run the one-sided
law across tier B; characterise the 10 tier-A graphs (8-vertex,
2-connected, |F|=2, no independent 4-set — high local density
means their bipartitions are nondegenerate, so a fat-block
generalisation of the W26 master relation may see exactly the
classes the permanent reduction cannot).

---

## v77 addendum: tier A gets its first mechanism candidate — the k=1 affine correction to the committed slice machinery (2026-08-20)

W31's tier-A analysis, with two self-caught premise corrections
(the manager's "internal edges => hafL nonzero" criterion replaced
— a hafnian needs a PERFECT MATCHING in the half, not an edge:
6/35 nondegenerate splits per class, uniformly; and an endpoint
bug in the Lemma-1.1 test fixed by its positive control). The
committed document proofs/slice-master-relations.md SPLITS
cleanly on tier A: **the cofactor identity (Thm 4.1) and Q-span
bound (Thm 4.3) transfer VERBATIM** (600 random-block tests, 0
mismatches, mutation fires — on a genuine tier-A (R) template
built by the R1 SAT engine and independently checked); the
sigma-count decomposition and master relations do NOT (they need
a perfect-matching cross split: 0/35 across all ten classes). So
the stratum's empty-input failure moved exactly one theorem
downstream, to Corollary 4.2 (untriggered words come from clean
words; tier A has none, min k = 1). **THE OPENING: at a k=1 word,
Phi_w = minus a single known monomial, so 4.2 relaxes to a
RANK-ONE AFFINE correction and 4.3 becomes an affine rank bound**
— a well-posed mechanism using only committed results + the k=1
census inventory, the first tier A has ever had (distinct from
W16-B's k=1 route, which needs a (clean,k=1) pair and is
genuinely vacuous here). All ten tier-A classes are uniform
(independence number 3, max degree <= 4, |F| = 2, exactly 6
nondegenerate splits). Tier B: per-class execution settled
(template-on-demand via the R1 engine + independent checker);
the 64-class one-sided Q-span sweep is the next compute item.
R1 still on m=21 (the boundary-adjacent hardest instance),
calibrations green.

---

## v78 addendum: W36 — THEOREM W36-M25 (the shared-letter argument eliminates (beta)); M2627 conditional on (Q3) alone; the m=28 joint-star object; the escape is self-defeating (2026-08-20)

W36's landing, the sharpest Route-A round yet. **THEOREM W36-M25
[probe-proved, replaces W30-M25-CONDITIONAL]**: hypotheses (H1)
clean + (H2) cells nonzero + (R25) some tuple carries two
surviving |T_f|=1 choices with DIFFERENT firing letters =>
R6 delivers. Proof is a pigeonhole: R6's firing letters {1,2}
give clean pairs {0,2} and {0,1} SHARING letter 0; if both
choices failed, both pairs would be rank 1, forcing all three
rows parallel (rank S' = 1) — but then every pair has rank 1 =
rank S' and delivers. Contradiction. **(beta) is ELIMINATED as a
hypothesis** — fitting, because W36 also FOUND the (beta)-escape
realised in W30's own corpus (a stored F_13 hunt point with
Q == 0 on entire families, rank S' = 2, R6 still delivering
695/743; W30's "never observed" was an artifact of not scanning
its own hunt output — ledger-25-adjacent). 42/42 stored points
verified; the load-bearing ROWS/S' reduction checked 0/10,472.
(R25)'s failure = exactly the size-12 hafL cover (independently
re-derived and EXPLAINED: it is the firing-letter-2 choice set),
and at all three stored cover-satisfying objects **rank S' = 1
everywhere — the escape forces the very parallelism that
delivers**. The remaining m=25 gap is therefore ONE implication:
cover-vanishing => rank S' = 1 (the measured cross-block
parallelism mechanism: all hafL zeros must agree on a ratio
independent of x, collapsing A07/A25/A03-vs-A23 ranks — measured
live at nZ = 30, not yet proved). **THEOREM W36-M2627-CONDITIONAL**:
the same shared-letter argument at |N| = 3 — Q != 0 buys
rank <= 2, the second firing letter buys the contradiction;
residual = (Q3) ONLY. Verified 100/100; the NEGATIVE control is
the lane's strongest evidence: the six one-firing-letter vertices
provably cannot use the mechanism and DO fail (77/226), while
the four protected vertices never fail anywhere — the protected
set {|N| <= 3} + {two firing letters} falls out exactly. **m=28
made concrete**: with H_e = haf(Gamma - e), rank-3 at v <=> v's
cofactor star is rank one; the four two-letter vertices form the
path 1-2-5-6 in Gamma; ALL FOUR at rank 3 forces 13 of the 16
cofactor hafnians jointly rank one — the pairwise exclusion is
now a rank condition on a 7-COLUMN matrix (the first genuinely
Singular-sized target in eleven rounds), with 6(n-1) equations
per n-word class. Structural surprise: pair (2,5) shares NO
untriggered words — the joint object is silent about exactly the
(L2,R5) pair W26 named, retroactively explaining why that target
was wrong. Ceiling reproduced under the sharper definition (max
2 of 4 at rank 3, 307 points). W36 continues: prove the
cover=>rank-1 implication (closes m=25 UNCONDITIONALLY as a
disjunction theorem), then the 7-column m=28 elimination. A11
notified that W36-M25 supersedes its target statement.

---

## v79 addendum: L1 — the bespoke kernel RUP checker is built and SOUND at the clean axiom bar (2026-08-20)

Component 9 landed: a 208-line, zero-import RUP checker with
`check_sound` proved — axiom closure exactly [propext,
Classical.choice, Quot.sound], the #4659 bar and what
formal/FORMALIZATION.md advertises. Design wins: RUP-only (the
emitter rejects RAT loudly) and deletions-ignored (dropping a
deletion only enlarges the store; every store clause stays
entailed — all removal bookkeeping vanishes). End-to-end
kernel-checked on the smallest orbit (5.1 s); the larger orbits
need the specified logarithmic store (kernel Array indexing is
O(h) — a binary-trie store + two soundness lemmas, 0.5-1
session; total checker cost stays inside the 3-session fallback).
The stock-machinery question is settled definitively: Lean's
LRAT.check is IRREDUCIBLE (stuck at maxRecDepth on a 1-variable,
2-clause instance) — building our own was the right call, and
the checker is a standalone contribution to Lean's verified-SAT
stack. Staged tree builds clean (8063 jobs), every declaration
at the clean closure. Remaining bulk: components 6-8 (ledger,
nine clause families, coverage table), FREE/B1, the WLOG
symmetrize, assembly.

---

## v80 addendum: LEMMA W31-4 (the affine cofactor law); every stratum class now has a mechanism; tier-B sweep running; ledger 30 (2026-08-20)

W31's execution round. **LEMMA W31-4 [probe-proved]**: the
decomposition H(w|v=t) = <S'(tau)_t, Q(w)> + E_t(w) (from the
committed Thm 4.1 + H = Phi + E; one matrix and one cofactor
vector serve all three letters; 480 tests, 0 mismatches; positive
control: on clean-word templates "mu = 0" and "untriggered"
coincide 400/400 — it genuinely generalises Corollary 4.2). The
k<=1 special form is VACUOUS on tier A (0 qualifying words —
min-max k is 2-4 across the ten classes), but what survives is
stronger: **the UNCONDITIONAL affine law S'(tau).Q(w) = -E(w) at
EVERY word of an exact source** — full 6,558-equation input with
no hypothesis — plus the Rouche-Capelli criterion (B2): a rank
failure of [Q | -E] at any (v,tau,t) means no exact source on the
template — the affine analogue of W26's Farkas branch, now with a
2-4-monomial RHS. **Coverage: all 75 stratum classes now carry a
defined mechanism** (tier C: two-sided permanental law — known to
RESIST, needs the threshold; tier B: one-sided law, sweep running
6/64 all THRESHOLD so far; tier A: the affine law, kill criterion
stated not executed). Honestly: nothing is claimed killed yet.
The tier-B calibration caught a third template-vs-class incident
(arbitrary template gave C_8 the wrong verdict) — codified as
LEDGER 30 (verdicts attach to templates; per-class claims need a
canonical construction or a transport lemma). R1 still on m=21.

---

## v81 addendum: A11 verdicts — M25 chain CONFIRMED with corrections; the supersession claim was WRONG (the theorems are incomparable); the (beta) target is a reduced scalar system; ledger 31 (2026-08-20)

A11's from-scratch audit (2,592-test engine controls, 31/31
stored-verdict reproduction): **W30-M25-CONDITIONAL CONFIRMED**
(with four statement corrections — notably (H1)/(H3) are inert
and |T_f|=1 unnecessary at m=25); **W30-Z CORRECTED** (missing
all-cells-nonzero hypothesis — A10's fix not inherited; one
redundant hypothesis; its round-3 blind-test record is not on
disk and must not be cited; A11's replacement blind test:
115/115); **the W36 pigeonhole CONFIRMED exhaustively**
(2,985,984 matrices, 0 both-fail; the n=3 analogue fails
183k/200k — why m=26/27 keep (Q3)); and **the manager's
supersession framing REFUTED: W36-M25 and W30-M25-CONDITIONAL
are incomparable** ((R25) fails at 4/32 corpus points, (beta) at
0/32) — the promotion object for record -04 is the DISJUNCTION
"(R25) or ((alpha) and (beta))", 32/32. Round 10's
"common-direction never reached" was STALE (reached in all three
fields incl. Q — and it buys nothing); A11 reduced the escape at
common-direction points to a SCALAR SYSTEM whose measured
obstructions are A07's rank (2, not 1) and the scalar Q==0
system (7.4% best completion) — **that reduced system is the
(beta) successor target**, replacing the round-10 formulation
(which also needed an unstated coverage condition). Defects:
W30's r10 hit test omitted its own target's condition; five r10
files carry ok=True with `_controls_run: []` (LEDGER 31 added);
`[::7]` stride samples labelled as censuses in two engines; the
independent-family points were never stored. P3 re-tasked to
restage the -04 bundle per A11's exact recommendation; W36
handed the corrections + the scalar-system target.
