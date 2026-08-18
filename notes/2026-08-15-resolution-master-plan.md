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
