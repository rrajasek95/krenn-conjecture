# W33 — d=2 variety + kernel squeeze + m=3 — FINAL (UNAUDITED, 2026-08-20)

PINNED_HEAD 14f53e79. Independent engine (bitmask subset DP,
cross-checked 370/370). Transcribed by the manager from the
lane's final message; full detail in results_SUMMARY.json +
results_t{1..12}.json.

## 1. The d=2 variety at n=8: WILD, exactly stratified
- W33-D1 (parity lemma): every PM uses equally many P- and
  Q-internal edges of a Hamiltonian bipartition — explains every
  measured kernel number.
- W33-D2 [Groebner certificate]: Delta^2 + ARBITRARY 2x2 blocks
  on all six one-class chords is exact; stratum dim 30,
  irreducible, rational; only 2 of 256 word equations nontrivial.
- W33-D3 (wildness): gauge group dim 14; the chord stratum has a
  **16-dimensional moduli of gauge-inequivalent exact d=2
  sources** (Delta^2 alone is one rigid orbit, dim 6 = 6).
- W33-D4: 30,674 exact d=2 sources found over Q (two seeds);
  1,637/1,613 admit NO Hamiltonian-cycle witness; a rigid
  13-cell sporadic orbit carries a CROSSING-chord cell.
- W33-D5 (NEW, the dangerous family): **twisted 4+4** — two
  disjoint 4-cycles + exactly 4 crossing cross cells is exact
  over Q (explicit signs); 4 cells necessary (550/550 unit at
  <=3) and sufficient (1 of 6,123 orbit classes realisable);
  rigid (dim 8 = 8).
- W33-P (any field): with PM-pair diagonals and <=3 cross cells,
  a 4+4 pair is IMPOSSIBLE (union must be Hamiltonian); 85
  realisable orbit classes at the 8-cycle; all cross cells on
  same-parity chords except exactly 2 classes.

## 2. The kernel squeeze: both jaws have play; the instrument is
W33-K1
- W32-KER's hypothesis is NEVER satisfiable: min over 19,528
  exact sources of max_j dim Ker_j = 2 (all-kernels-zero occurs
  nowhere). Collapse is exactly HALF (one bipartition class).
- W33-K1: dim Ker_j = 2 deg_Z(j) + s_j (null pairs + syzygies);
  a nontrivial 2-term syzygy forces a common-cofactor
  factorisation of partial hafnians — the W32-ABS irreducibility
  obstruction again. Measured dim-6 kernels DERIVED.
- The support jaw closes: kernel conditions confine cross cells
  to triple-internal / level-2 supports, and **the whole cross
  freedom there is UNIT over ZZ (T7: 24/36 vars; T8: 56/60 vars)
  — all m at once**, with k=3 point + not-unit controls. The
  formula reproduces W32 run_22's 28/36 exactly (two-view).
  Level-3 (T9, 84 vars) running.

## 3. THEOREM W33-M3 [any field]: no X_4 point with disjoint-PM
diagonals and <= 3 cross cells. Phase A: 6/8 triple orbits die by
W32-2COL + W33-P (4+4 pairs need >= 4 own-type cells); Phase B:
18,676/18,676 survivor orbit cases unit over ZZ; controls incl.
prune-soundness resampling (11/11) and two-view tally.

## 4. Builder: two-sided calibration (accepts the PM-triple at
k=3 with 0 violations; rejects it at k=4 with 2); 31,960
candidates from 3,186 non-diagonal seeds over 4 primes; best 1
violation of 2,369; 0 hits; running.

## THE CASE TREE for general X_4-emptiness at N=8
(A) all pair restrictions diagonal: DEAD [W29-T1].
(B1) some pair union non-Hamiltonian: dead m<=3 [W33-M3]; **OPEN
m>=4 — live territory: the twisted 4+4 (W33-D5) is the concrete
dangerous seed.**
(B2a) Hamiltonian unions, cross cells in triple-internal/level-2
supports: DEAD over any field, all m [T7/T8].
(B2b) outside those supports: open; needs >=4 same-pair cells
with a non-chord cell, or the 2 exceptional classes, or a
nontrivial star syzygy (= common-cofactor factorisation, where
irreducibility bites). Level-3 rung running.
(C) diagonal support NOT a PM triple: wide open and POPULATED
(the chord family + sporadics). The named instrument: the
null-graph incompatibility question — can three exact d=2
restrictions have simultaneously large null graphs while sharing
diagonals pairwise?

## Corrections to the inherited picture (load-bearing)
(i) "non-diagonal forces kernel collapse" is FALSE globally —
collapse is exactly half; the true statement is W33-K1.
(ii) "every exact d=2 source is Hamiltonian-cycle/PM-pair up to
gauge" is FALSE by a 16-dim moduli; pair-Hamiltonicity is a
CONSEQUENCE of <=3 cross cells (W33-D5), not a general fact.
