# W17 — the scalar-slice / rank-one cap question — REPORT (UNAUDITED, 2026-08-15)

Pinned HEAD 9ceaf0a. All verdicts exact (int/Fraction; Singular +
Rabinowitsch; every certified verdict re-decided mod 32003 and
1000003). No floats. Family (R) untouched. Agent's write was
policy-blocked; this transcribes its report.

## HEADLINE
1. THE RANK-ONE RE-BASING IS LOSSY — refuted as an equivalence at
   h=2 AND h=3, at pair and source level, WORST NEAR EXACTNESS:
   P2 fleet: 17/1,144 witness pairs have no admissible rank-one
   witness; 5/288 SOURCES have witness pairs but no rank-one witness
   anywhere. Near-exact fleet (97.8-99.9% satisfied): 39.8% loss
   (66/166); one source with 9 witness pairs and 0 rank-one. h=3:
   7/7 constructed pairs with explicit rank-3 clean caps have no
   rank-one witness. W14's 29/29 reproduced exactly (120/120
   agreement) — its sample was seeds 1000-1008 only; every loss
   lies beyond it. Rank-one search = cheap SUFFICIENT test only.
2. h=2 COMPLETELY SOLVED (Theorem W17.1): E = 0 iff homogeneous
   elementary-symmetric conditions on the degenerate-site ratios;
   geometric reading: a witness needs three codim-2 degeneracy
   divisors at once (codim 6 in a 4-fold) — PROVES generic blocking
   (P2's 750/750 explained); |I|=1 branch complex-only (exact
   Q(omega) instance built).
3. h=3 EXACT CRITERION (Theorem W17.6 via the ⊥-contraction law):
   finite condition set (A)+(B)+(C). HARD COROLLARIES (W17.4): a
   clean rank-one cap with all sites nondegenerate forces EVERY
   internal block rank <= 2 (prescribed kernels); one degenerate
   site => rank <= 1; rank-0 site => vanish. RARITY (W17.9):
   admitting an admissible clean rank-one cap is codim >= 110 in
   the 135-dim internal-block space — no h=2 analogue (the h=2
   error ignores internal blocks entirely; the structural reason
   h=2 calibration cannot certify h>=3).
4. STAGE_A: rank-one witnesses at EXACTLY (0,2), (1,3), (2,3) —
   P1's two ground-truth pairs re-verified AND ITS UNDECIDED PAIR
   (2,3) NOW DECIDED (explicit tiny-integer caps). Lossless there
   (deep degenerate stratum — no full-rank block in the source).
5. DEFINITIONAL HAZARD RESOLVED (Lemma W17.10): W5's scalar slice
   error is ONE COMPONENT of the tensor cap error; equivalent at
   h=2 on the all-degenerate stratum; drastically weaker at h>=3
   (caps with scalar error 0 and 728/729 components nonzero). The
   v22-relayed witness-search predicate was WRONG at h=3 —
   corrected to the full tensor criterion (relayed to W16). W14's
   CODE used the right object; its prose misled.
6. GAP D DISSOLVES for the re-based route (colour diagonal graphs
   of an exact source have perfect matchings => >= N/2 live pairs;
   admissible rank-one caps Zariski-open at live pairs). The OLD
   Gap D (full-rank pair) FAILS on STAGE_A (no full-rank block).
7. AVERAGING ROUTE CLOSED: E is bihomogeneous (h,h), torus average
   identically 0 for every source at every order.

## Structure
Rank-one closed form (Lemma W17.0): E(u tensor v) = sum_k s^{h-k}
k! sum_{|S|=2k} e_{S,k}(alpha,beta) tensor Haf_{U\S}(A) — the
TENSOR analogue of W5's scalar form (3^{2h} components). h=2: E =
2 e_{U,2}(alpha,beta), independent of internal blocks and A_pq.
h=3: affine in internal blocks. Cost-of-cleanliness table (system
rank 120 at 0 degenerate sites -> 33 at six+rank-0).

## Controls (0 failures)
Three independent evaluators; rank-one = general-K at u tensor v;
vs P2's quadrics; vs P1's error tensor; W17.1 vs ideal decision
250/250; 19/19 x4 mutation controls; W5 shadow 60/60; inter-probe
120/120 with W14; all loss certifications across Q + branches + two
primes; |Z|>=3 vacuity 3,506/3,506; W17.10 452/452.

## Soft spots
Refutes the RE-BASING, not the descent (blocked => all rank-one
slices dirty still holds); P2/W1 sources not exact; h=3 losses are
constructed sources (mechanism generic, not realized-on-exact);
W17.4 closed-form ranks proved for two degeneracy patterns (rest
covered by decidable W17.6); STAGE_A witness/rank-2/diagonal
pattern [CONJECTURED]; near-exact fleet used a 2-round push.

## Recommendation (adopted)
Keep rank-one as a cheap sufficient search (it decided STAGE_A
(2,3)); the chain requirement stays with GENERAL caps; any (R)
search must use the full tensor predicate.
