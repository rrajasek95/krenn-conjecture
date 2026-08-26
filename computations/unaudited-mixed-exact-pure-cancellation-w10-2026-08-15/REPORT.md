# W10 — mixed-exact pure cancellation — REPORT (UNAUDITED, 2026-08-15)

Pinned HEAD c4eb9eb (moved to 7adc0db mid-run; no dependency
touched). Exact arithmetic + Singular over Q for every verdict;
floats only in labelled searches. Agent's write was policy-blocked;
this transcribes its delivered report. 20 run scripts, 16 JSONs, 25
logs here.

## VERDICT: EXISTS (the fork's YES branch)
Mixed-exact sources on fully admissible (T4/T5/T6/S) templates with
every pure coefficient vanishing BY CANCELLATION exist at every
admissible support at N=6 (m=9..15) and N=8 (m=12..28), at the
MAXIMUM cell count Sigma = 9m. Mechanism: A_uv = t_uv * J (all-ones
blocks) => H_w = haf(t) for EVERY word; solve haf(t)=0 on any graph
with >= 2 perfect matchings. Symbolically certified over Q
(Singular: H_w - haf(t) = 0 identically, 729/729 words at N=6).
Free-block variant (rank-3 blocks) exits the constant-block gauge
orbit; tangent dim 62 at W-A.

## LEMMA W10-G (sharpened P2 fact 5; load-bearing for W15)
A mixed-exact source with ALL THREE pures nonzero is gauge-equivalent
— SAME TEMPLATE — to a fully exact source (g_{0,c} = 1/H_{c^N}).
Verified 20/20 + controls. Consequences: (a) COROLLARY W10-6: every
mixed-exact six-site source has a vanishing pure; (b) the survivor
value systems ("mixed = 0, pures != 0") carry NO SLACK relative to
exactness — they ARE the exactness problem up to gauge; (c)
mixed-exact + pures nonzero FORCES (SC) (via gauge-invariance of
(SC), verified); mixed-exactness alone does NOT (all 26 W10
witnesses fail (SC) at every slot — 18/18 and 24/24).

## LAYER SEPARATION (the consequence map)
- Layer 1 (W9's T4/T5/T6/S): DOOR A CLOSED UNCONDITIONALLY, strongest
  form — no ceiling below the trivial 9m is provable from the mixed
  equations plus any template condition implied by T4/T5/T6/S.
  (W9's closure 2 extends to the admissible stratum.)
- Layer 2 (+ (SC)): OPEN and untouched — (SC) is the ONLY template
  ingredient a ceiling proof may still use; W10's witnesses are
  ready-made falsifiers for any argument not consuming it
  essentially.
- CORRECTION IN H4'S FAVOUR: W6's and W9's Sigma_min certificates
  all violate (SC) (0/18), so recorded Sigma_min UNDER-estimates the
  honest (SC)-stratum price Sigma_min+. But counting stays closed:
  singleton-free ADM+(incl. SC) templates found at Sigma = 65/71/87
  (m = 21/24/27), below the best budget ceiling.

## W8/W12 SURVIVORS
All four audited survivors pass ALL FIVE filters (T4/T5/T6/S/(SC))
— no free kills remain on (R). Value-level probes INCONCLUSIVE
(four variants, each failed a control — documented, no conclusion
drawn). One control-calibrated observation: mixed-only optimisation
reaches ~1e-10 on the survivors while adding the three pure
equations stalls at 6.6e-4 — a six-order separation pointing at the
PURE equations as the obstruction, as the six-site analogue
(W10-6) predicts.

## Also established
Delta_{N,2} exists for every even N (exact cycle construction;
inadmissible template). N=6 taxonomy of nonzero pures: 3 impossible
(W10-G + six-site theorem); 2 exists exactly (inadmissible), open on
admissible; 1 float-found on admissible (NOT exactified — three
methods failed, positive-dimensional irrational stratum; template
audit exact, values float); 0 exact everywhere. Restriction lemma
proved (H(A|_S)_w = H(A)_w on S-words). Mixed-exact => (S); (T4) =>
(T6).

## Controls: all fire (both directions), including the decisive
haf != 0 positives, cell deletions, degree drops, single-matching
impossibility, (SC) checker passing on the cube, ideal-membership
controls in Singular. Soft spots: exact witnesses have H = 0 (not
near-counterexamples); the sharp 1-pure object is float-only; value
probes inconclusive; Sigma_min+ values are search bounds; W6/W9
numbers quoted not re-derived (except their (SC) audits, re-run).
