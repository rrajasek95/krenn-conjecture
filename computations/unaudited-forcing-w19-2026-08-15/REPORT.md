# W19 — forcing theorem + (R) census — REPORT (UNAUDITED, 2026-08-15)

Pinned HEAD d377b71. All-exact; no floats in any verdict path;
no-shadowing guard active; modular ranks only as sound upper bounds.
Agent's write was policy-blocked; this transcribes its report.

## HEADLINE 1 — ESCALATION: the forcing theorem cannot close N=8
THEOREM W19-K [proved]: matchings inside Gamma are supported at
every word, so k(w) = fibre(w) - |F(Gamma)|; if |F(Gamma)| <= 2 the
effectively-clean layer is EMPTY (mixed words need fibre >= 3).
The stratum is NON-EMPTY: explicit re-audited (R) member with
Gamma = C_8 (Hamilton cycle 0-4-3-6-1-7-2-5-0), |F|=2, m=28,
Sigma=148, min mixed fibre 6, ZERO effectively-clean words (min k =
4). There, W16-B / k=1 / k=2 / W15-A all have EMPTY INPUT. New
residual case: (R) members with no effectively-clean word (214/794
census representatives; provably the whole |F| <= 2 stratum). Clean
layers are also fragile inside |F| >= 3 (2152 -> 120 -> 48 -> 24 ->
8 under single-cell downgrades).

## HEADLINE 2 — m=25 CLOSED [PROVED-HERE]
Fix 1: the EXACT effectively-clean set (2,624 words, a product box
S4 x S5 x S6 x S7 for every L-word) has 24 L-words with full S4 —
W16's word-clean X_free (x1=2 only) had F_a = 1 identically, making
the (E2) equations vacuous: the measured insufficiency now has a
cause. Fix 2: eliminating lambda_x gives (E1) G_i K_j = G_j K_i and
(E2) (F_a - F_a') K_i = 0; exhaustive three-case split on A14 rows
(gauge A14[i][0]=1): case 1 => site 4 factors (9/9 minors, 0.1 s);
cases 2,3 => site 6 factors (45/45; case 2 has a two-line hand
proof). All runs report clean_layer_unit_ideal = False (not a
hazard-13 artefact); explicit-point control C5 passes (an all-cells-
nonzero Branch-B point satisfies all 2,624 clean equations and all
"forced" verdicts hold at it). With W16-A's dichotomy: m=25 DEAD.

## HEADLINE 3 — local geometry of the clean layer [PROVED-HERE]
THEOREM W19-A (J-point tangent space, ANOVA proof): dim = 5|Gamma|
- 17; every first-order deformation keeps all blocks rank <= 1.
COR A2: first-order forcing at site t works IFF deg_Gamma(t) <= 2
(codim 2 deg - 4) — why m=25 (a degree-2 site) was easy and why NO
first-order proof exists at m=26/27/28 (min degree 3). Second order:
at m=28 the order-2 variety is 33-dim vs eight 32-dim aligned
subvarieties — directions escape every site, so NO order-<=2 proof
of forcing at m=28. Forcing at 26..28 needs order >= 3 or global
arguments.

## HEADLINE 4 — the rank-two (bracket/Plucker) stratum is EMPTY
For all 10 (R) Gammas tested: no bracket point of Phi = 0 (complete
sign search modulo gauge + Singular over the closure). POSITIVE
CONTROL: at N=4 the bracket family DOES give an explicit all-integer
point (all 54 cells nonzero, all blocks rank 2, no factoring site) —
the forcing analogue is FALSE at N=4, exactly matching the known K_4
exceptional GHZ witness (k_max(4) = 3). The machinery that finds it
finds nothing at N=8.

## THE CENSUS (sub-probe; headlines re-verified by W19 itself)
794 admissible Gamma iso-classes (18,763,675 labelled), EVERY one
supports an (R) member (explicit witnesses). |Gamma|=8 => C_8
exhaustively (all 2,520 spanning 2-connected 8-edge graphs are
2-regular). |Gamma|=16 completely classified (6 cubic classes;
exactly 6^8 placements per labelled graph; 136,094 iso-classes).
Total bracket 8.96e32 <= |(R)| <= 1.56e35 labelled; thin/fat members
dominate. TWO W16 CORRECTIONS (re-verified): its "seven skeletons"
= 4 of the exactly 6 cubic iso-classes (two missed); diagonal
placement/proper colouring NOT required. Kill status over 794
representatives: k=1 available 513; k=2-only 65; NO CLEAN LAYER —
every known mechanism vacuous: 214; clean-but-no-usable-pair 2.
SYMMETRY HAZARD: S_3^8 does NOT preserve (R) (per-site colour
permutations break (SC)/constants); the (R)-preserving group is
S_8 x S_3(global), order 241,920.

## Controls
C1 engine reproduces W16's per-site pair counts exactly (0
mismatches); C2 W16-1 at m=26 both sides; C3 dichotomy sharp on 36
instances; C4 J-point non-vacuity at 25..28; C5 explicit-point
control (ledger 13) with firing mutation; C6 gauge chain; C7
negative targets 10/12 correctly not-forced (2 forced ones are true
consequences with hand proof); 19,683 closed-form evaluations 0
mismatches; census external ground truths (A008406, 19,355, 2,520)
+ independent DP + 719/719 witness constructions.

## Status
m <= 25 CLOSED. m=26/27/28: downstream certified, forcing open
(provably not order-<=2 at a J-point). NEW RESIDUAL: the
empty-clean-layer stratum. Sharpest uniform statement proved:
first-order forcing iff deg_Gamma <= 2. No feasible point of any
exact-source system found anywhere.

## Soft spots
m=25 uses W16-A as stated (reproduced, not re-derived); lambda
relaxation infeasibility-only; order-2 positive containments
untested; 27/48 random-Gamma tangent sweeps skipped (degenerate
J-points); bracket exclusion covers matched-kernel rank-2 only;
census big counts not independently re-derived (headlines were);
phi-downgrade tables differ from sub-probe (different blocks
downgraded; conclusions unaffected).
