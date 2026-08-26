# W21 — the two finishing moves — REPORT (UNAUDITED, 2026-08-15)

Pinned HEAD e0c4d7c. Exact-only (no floats anywhere); independent
engine (0 mismatches vs W20 across 300 supports / 375 Phi / 120
factoring / 5 templates). Agent's write was policy-blocked; this
transcribes its report. Sub-probe dirs tensor/, move2sing/,
move2geo/ inside.

## HEADLINE 1: THE MOVE-1 TARGET IS FALSE AT m=28 TOO [PROVED-HERE]
Exact rational points of the m=28 clean layer with ALL 144 Gamma
cells nonzero and NO factoring site (three witnesses; verified by
three engines on all 2,152 clean equations; reproduced from scratch
— 7 of 57 random-order descents land on zero factoring). Corroborates
A7's m=25 refutation: the phenomenon is real, not W19's sign
artefact. THEY ARE NOT COUNTEREXAMPLES: fixing Gamma and solving for
the 12 single cells, the residual system is LINEARLY INCONSISTENT —
no completion exists at all. At m=26/27 no zero-factoring point
found (96/79 descents; the sub-probe classification gives the
structural reason: m=26 forces >= 2 reduced factoring sites, m=27
>= 1, m=28 nothing).

## HEADLINE 2: THE REPLACEMENT — THE RESIDUAL LINEAR TEST
[CONJECTURED, 221/221 exact points, no survivor]
Fix the Gamma blocks at a clean point; the non-Gamma occupied cells
(12 scalars) are unknowns; keep only the degree-<=1 equations (the
k=1 family): an inhomogeneous LINEAR system. KILLED = inconsistent
OR some occupied cell identically zero on the affine solution set.
NO factoring hypothesis. Results: m=28 46/46 (incl. all 3
zero-factoring points), m=27 50/50, m=26 57/57, m=25 64/64
(incl. A7's ENTIRE 12-member refutation family — killed by outright
inconsistency), m=24 4/4. Ledger-18-compliant sampling (0..5
factoring sites, 100% kill in every bucket). WHY: the clean
equations force haf_Gamma(x,.) = 0 on all 81 R-words for the four
full-box L-words (W21-B2), generating ~1,900 pure monomial
equations c z_i = 0 plus nonzero-constant rows.
THE STATEMENT TO PROVE: for EVERY point of the clean variety with
nonzero Gamma cells, this linear system is inconsistent-or-forcing.

## Move-1 tools [PROVED-HERE unless noted]
- W21-Pf: Gamma Pfaffian at 25..28 + C_8 (explicit signing,
  symbolically complete); on the clean layer rank Q(w) <= 2 (exact
  at all 2,152 words of every point; mutation control pushes to 8);
  the eight sites' W20-L coefficient vectors at a word are rows of
  ONE rank-<=2 form. Not uniform over Gamma (fails |Gamma| >~ 18;
  K_{4,4}, K_8 not Pfaffian).
- W21-C chain identity + rank inequality (0/3,120); W21-D far-image
  tightness (empirical, corrected hypothesis after a caught gap);
  W21-F (all far sites factoring => site unconstrained).
- W21-B1/B2 BLOCK/SCHUR REDUCTION: at 26/27/28 Gamma = K_4(L) u
  G_R(R) + the 0-7/1-4/2-5/3-6 matching; clean <=> avoids 12
  forbidden (x_i,y_j) pairs (explains the identical 2,152 clean
  sets); Phi factors through a K_4 hafnian of a Schur-type matrix;
  EXACTLY FOUR full-box L-words => eight identically-vanishing K_4
  hafnian identities. Sub-probe classified the identically-vanishing
  K_4 hafnian completely (six strata; two empty by Singular with
  explicit-point controls; the all-rank-2 stratum is a single
  GL_3^4 orbit and is the m=28 hole). NEEDS AUDIT.
- Automorphism split settled: site-permutation symmetry trivial at
  26/27, exactly <u -> 7-u> at 28 — cannot carry a proof.

## Move 2: C_8 NOT KILLED — false kill caught by cross-lane
## contradiction
Sub-probe SING claimed a kill via "Theorem W21-M2" (per cannot
vanish on products of 2-dim non-coordinate subspaces); sub-probe GEO
built a Q(omega) counterexample; W21 adjudicated in exact
Q[omega]/(omega^2+omega+1): ALL 16 basis permanents vanish, subspaces
non-coordinate, mutation control (omega -> 1) fires. W21-M2 FALSE;
kill invalid. The L-free/R-free reduction itself re-verified
(0/14,580). SALVAGE: the DOUBLE-DEAD-COLUMN obstruction — x =
(1,0,0,2) is the unique 4-dirty L-free word with a double dead-cell
column (site 6), y = (0,2,0,1) its mirror; the omega-family fails
exactly that constraint; a corrected lemma using the double column
may recover the kill. GEO also corrected W20's box-cover convention
and proved the codimension budget + collinearity-only routes cannot
close C_8.

## NEW LEDGER HAZARDS (adopted as items 19-20)
19: single-small-field exhaustive sweeps are INSUFFICIENT for NEVER
claims over Q — a complete F_5 classification produced a false kill
(F_5 has no primitive cube root of unity) that passed mutation AND
positive controls in two independent pipelines; char 3 is degenerate
for 4x4 permanents (4! = 0). Cross-check a second prime with the
right residues, or eliminate over Q.
20: CROSS-LANE CONTRADICTION is the control that worked — for any
new NEVER lemma, require an independent lane that tries to BUILD the
forbidden object.

## Controls
Engine cross-checks; W20's nine clean points re-verified; 45/45
perturbations; mutation controls on every tool; explicit-point
controls both residual verdicts; one own-error caught and fixed
(forced-zero criterion valid only for unique solutions — corrected
to identically-zero-on-the-affine-set).

## Soft spots
Residual kill 221 points, not proved; dictionary + W21-D empirical;
the K_4 classification and Move-2 lemmas are sub-probe work needing
audit; Pfaffian frame not Gamma-uniform; zero-factoring existence at
26/27 unresolved (structural reason, not proof of absence).

## FINAL ADDENDUM (all background jobs complete)
Residual-linear-test tally rises to **274/274 exact kills, zero
survivors** (m=24: 57/57 NEW ROW; 25: 64/64 incl. A7's full family;
26: 57/57; 27: 50/50; 28: 46/46 incl. all zero-factoring points).
Provenance: 216 fresh descents + 38 stored W20/W21 points + 20
A7-family/descent points; ledger-18 spread intact (0..5 factoring
sites, 100% kill in every bucket). Status still [CONJECTURED,
274/274]. Everything else in the report unchanged. Index:
results_index.json.
