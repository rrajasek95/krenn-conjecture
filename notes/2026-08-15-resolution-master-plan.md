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
