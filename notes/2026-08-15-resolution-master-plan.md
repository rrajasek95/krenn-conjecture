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
