# W25 — the X_3 core — REPORT (UNAUDITED, 2026-08-15/17)

Pinned HEAD 3f91310. All-exact (int/Fraction/Z[omega]; Singular +
Rabinowitsch; headline verdicts re-decided mod 32003, 1000003,
1000033 — two = 1 mod 3 per ledger 19). Agent's write was
policy-blocked; this transcribes its report. Named object:
OBJECT_W25-F8_n8_allblocked_X3.json (+ README).

## HEADLINE
"X_3 => witness" SURVIVES at N=6 (857 exactly-decided objects from
four seed families, 0 all-blocked; PROVED on two large strata) and
DIES at N=8 (the explicit falsifier W25-F8: in X_3 against the raw
1,731-word definition, NOT in X_4 — first failure a (4,4) word;
pures (1,1,1); 21 live pairs ALL BLOCKED by three independent
deciders incl. a saturation route; 1,244-cap search 0 with the
positive control firing; full mutation battery). **The N-uniform
U-core candidate is the PENULTIMATE rung** — X_3 at N=6, X_4 at
N=8, X_5 at N=10 (rung N - ceil(N/3) - 1). Rigidity measured: X_3
freezes half the sites at N=6 ([0,0,0] kernels) and none at N=8.

## Proved structure
- L3 (the three-off tensor identity) at every N; degeneration to L2
  exact (648/648); new content = the 2x2x2 all-off corner.
- W25-D1 (diagonal parity, every even N): odd colour-class => H_w =
  0 on diagonal sources, so ODD RUNGS ARE AUTOMATIC there (diagonal
  X_2 = X_3; X_4 = X_5); Delta^3_N lies in X_3 with first failures
  exactly the bicoloured 4-cycles (W25-U1+). With W23-U2:
  "X_3 => witness" is TRUE on the whole family Delta^3_N, every
  even N.
- THE CANCELLATION STRATUM IS EMPTY AT N=6 [proved exhaustively]:
  all 1,646,850 ordered diagonal skeleton triples enumerated;
  40,710 pass the filter, forming 24 classes under S_6 x S_3; 0
  survivors with a genuine cancellation condition. W23's flagged
  gap closed. Weight varieties nonempty over Q AND Q(omega), dim
  exactly |L| - 3 in every class.
- THE ALL-BLOCKED X_2 LOCUS IN CLOSED FORM: W23's four objects =
  one skeleton class ((4,4,4) Latin colouring + rainbow triangle +
  three free triangle blocks); membership is a LINEAR system (X_2:
  affine dim 12, generically all-blocked; X_3: dim 0 — the unique
  point is the diagonal source with 9 witnesses). **X_3's added
  equations annihilate exactly the deformation that made X_2
  all-blocked.**
- W25-U3 [proved, every even N]: BOTH ENDPOINTS CLEAN (exactly
  three live blocks, one per colour) => the antisymmetric cap gives
  E = 0 => witness — no X_2 equation needed; with the sharp
  predictor (270/270). At N=6 ONE clean endpoint suffices (138/138
  identically, via an X_2-forcing argument); fails at N >= 8
  (28/213 — the exact obstruction family). NO DIAGONAL X_2 = X_3
  SOURCE AT N=6 IS ALL-BLOCKED [proved: uniform caps on 23/24
  classes + the explicit single-component cap argument for the
  (5,5,5) class].
- RECORD CORRECTION: W23's detachment law (max det >= 2 => witness)
  does NOT extend to N=8 (20 of F8's 21 blocked pairs violate it);
  the proved >= N-3 fragment untouched.

## Controls
Full ledger battery (manifests 9/9 runners, 0 missing): H
cross-checks 8,820/8,820; cap-error cross-check W22-M-form vs
subset-J 252/252 (independently re-verifying Lemma W22-M); decider
agreements incl. the 9-witness reproduction; ledger 18
outside-locus points; 12+19 exhaustive strata over Q and Q(omega);
13/17/21/22 enforced.

## Soft spots
T1's N=6 general verdict rests on 857 objects (search is not
evidence of absence — the N=8 refutation sharpens the caveat); X_4
at N=8: NO point constructed at all yet ("no all-blocked X_4"
currently means "no X_4"); the cancellation-stratum emptiness is an
N=6 exhaustion; W25-U3's one-clean upgrade is N=6-only; F8 is one
object (component/dimension unmeasured).

## Named next objects
(1) BUILD X_4 points at N=8 and decide all-blocked there — the real
N=8 U-core question; (2) decompose the X_3 variety at N=6 (the
frozen-site rigidity says it is small — would turn T1 into a
theorem); (3) the cancellation stratum at N >= 8 + the N=8 diagonal
classification (the technique transfers); (4) the N-uniform
penultimate-rung statement + what replaces the antisymmetric cap
with no clean vertex (the (5,5,5) mechanism is the only example);
(5) THE SKELETON-LEVEL WITNESS CRITERION: witness/blocked was
constant across all weight points in every one of the 24 classes —
a combinatorial rule of the skeleton, not yet identified.
