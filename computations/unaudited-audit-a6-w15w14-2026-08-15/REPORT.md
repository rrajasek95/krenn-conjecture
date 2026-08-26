# AUDIT A6 — W15 (m=24 kill) + W14 (monochrome layers) — REPORT (UNAUDITED, 2026-08-15)

Pinned HEAD 9ceaf0a. Every engine from primary definitions; no probe
code imported; exact arithmetic (mod-p only as rigorous lower
bounds). Agent's write was policy-blocked; this transcribes its
report. 95 files here.

## W15 (m=24): PROMOTION-READY, WITH CORRECTIONS THAT STRENGTHEN IT
- Template/fibres/histogram/binomial shape: CONFIRMED (shape holds
  on all 2,952 effectively-clean words — more than the 2,152
  "syntactic clean" W15 counted; terminology conflation noted).
- 0^8 effectively clean: CONFIRMED (parity re-derivation + direct
  enumeration: 0 supported matchings through A04[0][0]).
- Ideal membership: CONFIRMED three independent ways.
- "Leave-one-out minimality 6/6": REFUTED — w4 = 12001200 is
  REDUNDANT. A6 supplies the stronger SIX-WORD certificate (five
  mixed + constant; multiplier A07[1][0]^2 A23[0][0]^2 A56[2][0]^2
  A14[0][1] A14[2][0]; 27 monomials, hand-checkable), with each of
  the five proved load-bearing TWICE (five exact rational witnesses
  + saturation). W15's control tested minimality of ITS multiplier,
  not of the word set. Multiplier also not minimal (K^2 A14[2][1]
  suffices for the six-word ideal, and is tight there).
- Non-vacuity: CONFIRMED by A6's own from-scratch solution of the
  clean stratum (108/108 cells nonzero, 0 violations, Phi = 0
  everywhere; the A23 degeneracy reproduced independently).
- Hypotheses: minimal as claimed, plus specifically H_{0^8} != 0.
- Scope note: the kill covers W8's immunity template at m=24; a
  support level is not a singleton (coverage consistent: W12 closes
  20-23, W15 closes this 24 instance, 25-28 open pending W16 incl.
  the (R) enumeration).

## W14: CORE CONFIRMED AND UPGRADED
- W14.1/W14.2: CONFIRMED with proofs supplied (456/456, 108/108;
  eq (4) evaluated literally = matching sum — factorials verified).
- W14.3 DIRECTNESS: CONFIRMED, and THE MISSING GENERAL-h PROOF IS
  NOW SUPPLIED by A6 (reduction to T((I_Segre)_h) = S^{h-1}, proved
  by base + step with every step machine-checked). Now a theorem at
  every h; write it up before anything quantifying over all N cites
  it. Dims 136/131/125, L_4 = 361, L_5 = 802 all direct, confirmed.
- W14.5: CONFIRMED (it is the evaluation homomorphism — degree-free,
  no rank hypothesis); the "iff" overstates (one direction only;
  witness: F1 instance with A_cc = 0 and s kappa_0^2 outside).
  Counterexample family confirmed 4/4 with matching span dims;
  regime non-vacuous at h=4 (closes W14's loose end); correct
  reading: "the transfer lemma is unprovable without exactness".
- Closed forms: h=2 det law confirmed (240/240 across three
  engines); h=3 phi_A confirmed on 92 matrices AND phi_A ⊥ J_4 now
  PROVED SYMBOLICALLY in Z[A] (1,224 pairings vanish identically) —
  upgrades W14's verified-not-proved. CORRECTION: the char-poly
  identity carries a factor det(A)^2 (e2(N)^2 - 4 e1(N) e3(N) =
  det(A)^2 phi_A).
- RANK-ONE LOSSLESSNESS: numerically confirmed 120/120 but FAR
  WEAKER THAN IT READS: 9 sources run (docstring said 70), all 29
  witness pairs from 3 sources, 11/29 vacuous (E = 0) — real
  evidence is 18 pairs / 3 sources / h=2 only. Narrative caution
  for the re-basing motivation; W17's T1 is the load-bearing check.

## Tooling
Independently re-hit the sat(J,f)[1] Singular trap (already in the
conventions ledger from A4) — two audits, same trap, both caught by
toy controls. 17-row + 19-row + 7-row mutation ledgers, all fire;
two self-defects caught and fixed (double-listed edges; the sat
trap).
