# W14 — monochrome transfer + certificate layers — REPORT (UNAUDITED, 2026-08-15)

Pinned HEAD c080b8a. All-exact (int/Fraction, Fraction RREF +
fraction-free elimination, Singular over Q); no floats anywhere.
Agent's write was policy-blocked; this transcribes its delivered
report. Scripts w14_*.py + logs + JSONs here.

## Verdicts
1. TRANSFER LEMMA AS STATED: FALSE. Exact counterexample at h=3:
   full-rank pair, no zero row/column, colour-c slice CLEAN, yet
   s*kappa_c^2 IS in the degree-3 error span (12/12 instances,
   certificate re-verified; regime: a >= 1 AND A_pq(c,c) = 0; the
   regime is forced, since A_cc != 0 makes those slices dirty).
   Non-vacuous at h=4 too (membership verdict there timed out —
   the one loose end).
2. REPAIRED LEMMA PROVED, DEGREE-FREE (Theorem W14.5, evaluation
   principle): colour-c slice clean <=> E_cc in V(I_pq); hence NO
   L-monomial m with m(E_cc) != 0 lies in the ideal AT ANY DEGREE:
   kappa_c^d excluded unconditionally (lifts P1's F1 to all
   degrees); s^a kappa_c^b and s^d excluded iff A_pq(c,c) != 0;
   monomials carrying another colour: NO information.
3. STRUCTURE: Lemma W14.1 (hafnian closed form), Theorem W14.2
   (level law: W13's graded data = internal-edge-weighted slice
   hafnians G_j; slice error = sum_j s_c^j G_j^{(c)}), Theorem
   W14.3 (DIRECTNESS of L_h(A) at full rank — proved via apolarity;
   fails at rank <= 2: dims 136/131/125), Corollary W14.4 (graded
   transfer projection; exact criterion G_a^{(c)} != 0).
   W13's 6/6 evidence explained: its clean-by-construction sources
   force ALL G_j = 0 (strictly stronger than cleanness).
4. GAP B ANSWERED IN CLOSED FORM: universal (A-only) exclusion
   exists ONLY at degrees h and h+1. Degree h+1 perp is
   1-dimensional at full rank: det K at h=2; phi_A = q_A^2 -
   4<K, cof A> det K at h=3 (= discriminant form of K adj(A);
   verified 15/15 vs Singular). Degree >= h+2: NO obstruction at
   full rank (hand proof at h=2). MEASURED (P2 fleet, 4,500 pairs,
   rebuilt exactly): 37,572 degree-3 certificates, 0 law
   violations; kappa_0 kappa_1 kappa_2 occurs 0 times (the unique
   predicted exclusion); OF 316 PAIRS WITH MINIMAL DEGREE h+1, 314
   HAVE MULTI-COLOUR MINIMAL CERTIFICATES — W13's T2 IS FALSE ONE
   DEGREE UP; minimal-degree distribution {2:5209, 3:1358, 4:234}
   (23% block only above degree h). RECORD CORRECTION: P2's
   "degrees 2..5" is NOT reproducible — every runner used
   max_degree=4; no degree-5 query was ever issued.
5. U(N)-W14 CHAIN with named gaps: B1 (certificates need not be
   monochrome from degree h+1 — typically are not), B2 (the
   A_cc = 0 boundary), A' (J.1b-SUPPORT observed not proved), D
   (existence of a full-rank nonzero-diagonal pair).
6. RECOMMENDED RE-BASING (the strategic result): rank-one caps are
   admissible, so BLOCKED => every scalar slice (u,v) with
   u_c v_c != 0 (all c) and u^T A_pq v != 0 is dirty — W5's scalar
   closed form, 4 projective parameters, NO ideal, NO taxonomy, NO
   degree bound. MEASURED LOSSLESS on P2's fleet: 29/29 witness
   pairs carry a rank-one witness, 0/91 blocked pairs do. The next
   question is W5-shaped: can the whole 4-parameter scalar-slice
   family be dirty at every pair of an exact source?

## Controls: 7/7 mutation controls fire + four-way expansion
agreement with W13 + graded-vs-direct identity + phi_A table +
37,572-certificate law check. Soft spots: counterexample uses a
random (non-exact) source; span = L_h generically is W13's input;
W14.6 containment proved, equality verified-exact only; phi_A
verified not proved; rank-one losslessness is a 120-pair h=2
sample; h=4 membership unfinished.
