# P1/P1' witness-splitting at h=3 — REPORT (UNAUDITED PROBE, 2026-08-15)

Pinned HEAD 86a9479 (deps re-verified byte-identical at 26ba69f).
Exact arithmetic; 14 scripts + 9 JSON in this directory. Headlines:

1. FACT 1 AT h=3 (PROVED): all 729 cubic components of E_pq lie in
   ker(det(d)) = S_3xS_3 (+) S_21xS_21 — codimension ONE (164/165).
   Proof: orientation-grouping of the 120 r^3 configurations by p-site
   set (six bijections cancel by sgn), antisymmetry for 3sr^2x.
   Generic span 136; the determinantal obstruction is degree-3 ONLY
   (I_4 has rank 494/495).
2. UNIFORM MINOR LAW F2 (PROVED, exact constants):
   D(s^{3-j} k_{c1}...k_{cj}) = (3-j)! x (complementary minor of
   A_pq); D = 0 on repeated colours. Consequences: k_0k_1k_2 NEVER
   blocks at degree 3 (D=1); s^3-blocking => det A_pq = 0 (empirical
   iff, 30/30); s^2 k_c => cof_cc = 0; s k_c k_c' => diagonal entry
   0; k_c^3, k_c^2 k_c', s k_c^2 carry no determinantal obstruction.
   The SAME mechanism (Lambda^h x Lambda^h component) reproduces all
   four of P2's h=2 laws.
3. F1 (k_c^3 FORCING, proved necessary): coeff of K_cc^3 in E_w IS
   the monochrome-c slice error E^(c) (the h=3 cap error of the
   colour-c row data). k_c^3-blocking => the colour-c slice is
   NON-CLEAN at that pair. J.1 handle: k^3-blocked everywhere =>
   all 3x28 monochrome slices dirty — an intrinsic finite system.
   COROLLARY SHAPE: a FULL-RANK pair (det A_pq != 0) can only be
   degree-3 blocked through dirty slices.
4. CALIBRATION ON THE COMMITTED NEAR-EXACT 8-SITE SOURCE (STAGE_A,
   6559/6561 rows): 23 pairs blocked deg 3, 2 at deg 5, 3 unblocked —
   TWO EXPLICIT VERIFIED CLEAN-CAP WITNESSES (exact rational K at
   pairs (0,2) and (1,3); all 729 components zero, four scalars
   nonzero). Had STAGE_A been exact, descent at (0,2) would
   contradict Theorem A — the 2-word defect is load-bearing exactly
   where the attack predicts. Pair (2,3) undecided.
5. PATTERNS REFRAMED: E = c*l1l2l3 means rank C = 1 — sound,
   strictly stronger than membership; kept as the low-degree
   certificate layer (systems in splitting_systems.json). All 10
   colour-diagonal patterns realized; 0/10 mixed-colour ever
   (explained by F2 + a permanental factorization argument).
   T2: l^N in I => V(I) in V(l) explains 25/25 non-witness pairs.
6. CONTROLS: identity suite I1-I6 PASS (incl. cap identity vs
   brute-force 105-matching contraction); 17/17 + 7 h=3-specific
   mutations behave. Limitations honestly stated (STAGE_A not exact;
   s^3 iff measured not proved; (2,3) undecided; Singular-only
   negatives flagged).

CONSEQUENCE: the blocking taxonomy at h=2 and h=3 is now essentially
complete and J.1 sharpens to: all-blocked exact => at every pair,
minor-degeneracy (s-patterns) or all-slices-dirty (kappa-patterns) or
deep higher-degree degeneration. The next lemma (J.1b): an exact
source cannot have all three monochrome slices dirty at every
full-rank pair — now a well-posed intrinsic question about hafnian
slice errors, assigned to probe W5.
