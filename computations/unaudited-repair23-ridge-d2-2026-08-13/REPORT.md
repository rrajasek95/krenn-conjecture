# UNAUDITED REPAIR PROBE — repair items 2 & 3: ridge derivation + D2 canonicity (2026-08-13)

**Pinned HEAD `7d57c552a3ef57d3a95c3bc933af547ad55e087d`; re-verified at
de74a1a. Exact Laurent-ring / rational arithmetic; big ranks at two primes
(2^61−1, 2^31−1) agreeing. Scripts, four ledgers, PROVENANCE.json in this
directory. UNAUDITED external probe.**

## Verdicts

- **A. Ridge terminal (eta_z, sigma): DERIVED.** All three physical
  definitions already exist in the repo and were never composed:
  Omega_v from endpoint_ridge_paths() (rootless five-ridge Bianchi
  cokernel), eta_z = X_mu/t with mu = {(p,0):+1,(z,0):−1} (clean-C5
  separator endpoint kernel boundary), sigma = X_lambda with
  lambda = {(p,2):+1,(x,2):−1} (formal-F full-Jacobian boundary, GHZ
  stabilizer). Forward computation over the exact Laurent ring with
  −Omega_v = −a+t+b−u yields eta_z(−Omega_v) = 1 + delta_(vz)·u_z/t and
  sigma(−Omega_v) = −q_pq^22 — matching every stipulated constant for all
  25 (v,z) pairs and all 5 faces, reproducing the 7-row TERMINAL_ROWS
  packet entrywise. Readout proved exhaustive; 6/6 mutation controls
  detected. (ledger f8b2d3e2…)
- **B. Non-vacuous terminal gate: PASSES.** Vacuity of the committed gate
  reproduced (same literal spliced into K and desired; empty packet,
  flipped sigma, dropped eta1_U1, doubled etas ALL pass it). The repaired
  gate (repaired_mv_terminal_gate.py) adds: R1 −O_alpha carries no
  terminal row (PROVED for the r0 half via the word-invariant formula
  eta_z = [w6=0]−[wz=0], sigma = [w6=2]−[w0=2], verified on all 590,490
  monomials × 6561 words; only 294/6561 words are killed by all six
  fields — a real condition); R2 each terminal row equals the
  independently computed physical demand (minus separator/Jacobian
  defects); R3 non-empty. Under it, M_v = −O_alpha + K STILL PASSES with
  terminals compared, and every bad packet fails.
- **C. D2 = −delta: CANONICAL UP TO SCALE** (ledger f17c223a…). The
  audit's 488-dim shadow freedom is real, BUT it meets the 4-dim corner
  space in exactly the line through −delta: corner blocks independent mod
  image = 3 (projection rank), dim(F ∩ W) = 1, attainable corner
  directions = span(−delta) only. STRONGER than claimed: deleting the D1
  rows entirely leaves both numbers unchanged — the corner class is
  pinned by the source rows alone. Honest replacement for the hardcoded
  boolean: "the whole shadow is undetermined (488 dims); the corner class
  is canonical; only its scale is a convention (fixed by augmented-HPL
  second_transfer = {D:1})."

## Still not reconstructible (exact)

1. The two normalizations are inconsistent and undocumented (eta has 1/t,
   sigma does not; only this pairing yields the committed strings).
2. Why the terminal packet is the v=1 face (eta1_U1 and no other U) —
   unmotivated in every file.
3. T (target cap) and rho (residue cap) have NO literal cell inventory
   anywhere — hand-typed row vectors only; their zero terminal rows
   remain assumed (= audit HIGH defect 8; smallest missing definition
   for completing R1).
4. The SCALE of the D2 class (hardcoded dict in the augmented-HPL
   Bockstein lemma).
5. The D1+D2faces variant did not finish (machine load); it can only
   shrink F, so it cannot overturn dim(F ∩ W) = 1.

## Net effect

Audit CRITICALs 2 and 3 are substantially repaired (pending repo
re-audit): the ridge is a forward derivation, the terminal gate is
non-vacuous and M_v still passes it, and D2's corner class is canonical.
Repair item 1 (K's operator-to-physical chain map) and the labelled
shifted first-jet lift of −dOmega_v remain OPEN, as the repo itself
records. Both relevant committed checkers pass live at HEAD with pinned
digests — these findings concern active checkers.
