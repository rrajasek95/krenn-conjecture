# W6 — bridge lemmas J.1c/J.1d — REPORT (UNAUDITED, 2026-08-15)

Pinned HEAD 31cefe2 (HEAD moved to 306133e mid-run; all used deps
byte-identical). Exact arithmetic; numpy only for integer fibre
counting (0/18 mismatches vs W2's cell_fibres). Agent's write was
policy-blocked; this transcribes its delivered report. 13 scripts +
12 JSON here.

## Headline
J.1c dead as stated; J.1d real, rigorous, and provably TOO WEAK to
close the band alone. Any cells-vs-support closing lemma needs a cell
ceiling C(m) < Sigma_min(m) ~ 3.2m; only committed ceiling is 189
(structural 0/2 model) — vacuous. Diagonal regime dies by O2 at every
support 12..27 (measured; independently reproduces the lanes'
n8_diagonal_support12_27 DRUP certificates and extends over beta).

## Task 1 — J.1c
- Co-occurrence law does not exist (pattern census over shadows,
  generic, census strata, anchored, near-exact: >=2 mixed patterns
  fire at only 0-38 of 1000s of blocked pairs; dominant blocked set
  is the vacuous {k0^2,k1^2,k2^2}). STRIKE J.1c.
- (EXP)/(STAR) PINNING (new, exact, general N): H_B(A)_(i,j,v) =
  A_pq[i][j] C(v) + (P(v)M(v)Q(v)^T)[i][j]; exactness => C(v) A_pq =
  -P M Q^T for every non-constant v. A pair with one C(v)!=0 has its
  whole 3x3 block determined cell-by-cell by its complement; rank
  A_pq <= rank M(v); support criterion A_pq[i][j]=0 iff p_i^T M q_j
  = 0. On the committed near-exact 8-site source the ENTIRE mixed
  system is exact (defects are the pure words 0^8,1^8 only); (STAR)
  holds with 0 residual on all 28 pairs; blocks recovered at 25/28;
  the unpinned pairs include BOTH of P1's witness pairs — being
  invisible to the mixed system is what lets a witness exist.
- Deformation forcing inside the pinned family: det=0 comes with a
  vanishing diagonal cofactor 92.7% / entry 78.3% (N=6, 5,200
  blocks) — support degeneration rides on singularity, but triggered
  by exactness, not blocking.
- h=3 R_cell PERMANENT DICTIONARY (10,206 word-components, 0
  mismatches): [r^3]_w = sum over 3+3 splits X of per_3(...); C3
  single-monomial criterion sufficient, measurably not necessary.

## Task 2 — J.1d (re-derived, corrected, re-targeted)
- Budget (general even N, from slice-cover forced incidences,
  d_R(v)>=3): beta >= 3N - m + |H|; at most min(m, 2m-3N) blocks not
  a single cell; Hall sharpening (non-basis R-edges inside S <=
  sum_S (d_R(v)-3)). 0 violations in simulation; tight at N=8 m=14;
  = W2's N(7-N)/2+|F| with saturation iff |F|=N(N-4)/2.
- W2 CORRECTIONS: (1) "Sigma cells <= 27" does not exist — 27 counts
  EDGES (occurrence-CNF semantics audit); only committed cell ceiling
  is O+D <= 189 (structural 0/2 model), so the cell trade is vacuous
  at N=8. (2) "12 cells on >=12 distinct edges" is FALSE (exhaustive:
  4..12 distinct edges); correct form: t1+2t2+3t3 = 3N/2, beta <=
  m - t2 - t3, t2+t3 <= 2m-3N-|H|.
- UNCONDITIONAL: m >= 3N/2; at m=12 (N=8) forced R_cell, all blocks
  single DIAGONAL cells on a properly 3-edge-coloured 3-regular
  graph = the committed support-12 cube chart; exact support <= 23
  => beta >= 1, <= 19 => beta >= 5.
- Result 1: zero-singleton templates EXIST at every N=8 support
  m >= 15 at floor beta (saved); none at m = 12..14 (m=12 proved via
  W2 exhaustion). The band is NOT closed by the floor.
- Result 2: measured cell price of singleton-freeness Sigma_min(m):
  52@16, 55@17, 58@18, 61@19, 64@20, 68@21, 70@22, 77@23, 82@24,
  85@25, 99@26, 98@27, 102@28 (~3.2 cells/block). These are
  certificates = upper bounds, so they CAP any counting lemma:
  C(m) < Sigma_min(m) is NECESSARY. beta=0 prices higher, beta=12
  lower — the "Sigma <= 3m diagonal" shortcut is invalid.
- Result 3: DIAGONAL templates have no singleton-free instance at any
  m = 12..27, any beta (m=28 recovers W2's 28 O1-killed templates).

## Task 3 — composed conditional
Exact N=8 source, support m, cells Sigma. H1 (committed slice-cover
+ support rules) + H2 (band 19<=m<=27; floor 18 ancestry-framed,
ceiling 28 restricted) + H3 (O2) + H4 (OPEN: cell ceiling C(m) <
Sigma_min(m), i.e. C(19)<61 ... C(27)<98) => no such source; with
H2, N=8 closes via the witness branch. H4 is the single residual;
the certificates prove it NECESSARY.

## Strike / reuse
STRIKE: J.1c; W2's Sigma<=27; W2's >=12-distinct-edges; hope that
counting alone closes the band. REUSE: (EXP)/(STAR) + pinning
(w6_core.py); budget + Hall; m=3N/2 forced-cube corollary; R_cell
permanent dictionary; fast exact fibre counter
(w6_task2_collision8.py, ~0.2 ms/template at N=8).

NEXT NUMBER TO CHASE: a committed cell ceiling for exact band
sources below 3.2m (starting points: W3 balance, slice-cover §4
local irredundancy, (STAR) pinning).
