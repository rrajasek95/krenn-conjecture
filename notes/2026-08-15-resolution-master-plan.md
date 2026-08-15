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
