# W23 — the pure-equation witness core — REPORT (UNAUDITED, 2026-08-15)

Pinned HEAD 02336a6. All-exact (int/Fraction; Singular+Rabinowitsch;
headline verdicts re-decided mod 32003 and 1000003); no floats.
Agent's write was policy-blocked; this transcribes its report.

## HEADLINE: THE EQUATION LADDER, MEASURED EXACTLY (N=6)
X_0 (pures) ⊂ X_1 (+L1) ⊂ X_2 (+L2) ⊂ X_3 (+three-off) ⊂ X_4 =
exact (3/39/219/639/729 words). All-blocked points: X_0 YES; X_1
YES (L1 automatic on the diagonal stratum — proved); X_2 YES for
general sources (4/20 walked objects, full battery, two full-rank
blocks; pures (1,1,1), 14 live pairs all BLOCKED over Q + two
primes) but NO on the all-1 diagonal stratum (EXHAUSTIVE: 56
S_6 x S_3 classes / 136,800 ordered triples, min 9 witnesses each);
X_3: none found (40 walked objects — EVERY one has EXACTLY 9
witness pairs); X_4 empty (six-site re-derived on a stratum
strictly larger than W22's sweep). TWO RECORD CORRECTIONS:
(1) the pure equations ALONE do not force witnesses (all-blocked
X_1 points with pures exactly (1,1,1) — strictly stronger
falsifiers than W22-1's); (2) L2 is not the load-bearing rung for
general sources — the first rung that bites at N=6 is X_3.

## THE TENSOR L2 [PROVED-HERE every N; verified N=4,6,8,10]
[H_{w(d,e)}]_{d,e} = C^(c)_ab A_ab + Phi^(c)_ab, Phi = sum over
u != v of C^(c)_{a,b,u,v} sigma^(c)_au (x) sigma^(c)_bv. Exactness
form: C A_ab + Phi = e_c e_c^T. New content vs L1 = exactly the 2x2
off-colour corner (rows/cols of colour c ARE W22-S). Corollaries:
triple determination + 3 diagonal relations (vacuous on all current
objects — a theorem in the diagonal regime; content only on
non-diagonal exact sources); rank law W23-R (rank(C A - e e^T) <=
min star spans); N=4 closed form (invertible A_ab forces diag of
complementary block = diag of A_ab^{-1}; 18/18 on Delta_{4,3});
bridge W23-L2K to the descent cap identity (36/36). 613/613
algebraic checks; exact sources 0 violations; Delta_{N,2} padded
fails at exactly the (2,2) entry of colour 2 — precisely its failed
pure. The committed near-exact source satisfies ALL of L1+L2 (it is
an X_3 point, fully diagonal).

## Composition results
- W23-M matrix L1: sum_y A_py D_y = I_3 (W22-X1 one line).
- W23-F: W22-1's family has L1 residual exactly -e_c everywhere
  (dies at rung X_0; maximal failure).
- W23-S1: exhaustive m=5 L1-feasibility pattern characterisation
  (1,048,576 patterns; explicit rational realisation for every one
  of the 302,919 feasible).
- W23-N1 [negative, proved]: the ONE-VERTEX composition of L1 +
  W22-X2 (+L2) is CONSISTENT — explicit certificate; no
  contradiction extractable at a single vertex (9 equations vs 45
  parameters). Kills the one-vertex reduction route.
- Side-B exact detachment decision procedure (kernel not in a
  coordinate hyperplane); W22-X3 realised on the near-exact source.

## N-UNIFORM THEOREMS [PROVED-HERE]
- W23-U1: the disjoint-three-PM diagonal family Delta^(3)_N (unit
  matching products) lies in X_2 and is not exact, every even N —
  the natural generalisation of Delta_{4,3} (which IS exact).
- **W23-U2 (the first N-uniform witness-existence theorem): every
  live pair of Delta^(3)_N carries a witness, every even N >= 6 —
  with the EXPLICIT ANTISYMMETRIC CAP K = I + E_{c2c3} - E_{c3c2}**
  (the two surviving matching terms cancel by antisymmetry; rainbow
  triangles give E = 0 outright). Verified at every live pair,
  N = 6, 8, 10 (+ Singular cross-check); mutation controls fire.
- W23-DR: diagonal X_2 forces three pairwise-disjoint monochrome
  rank-one vertex covers (>= 3N/2 rank-one blocks) — re-derives
  W5's diagonal corollary from L2 alone. Verified through N=10 +
  all 56 classes + 60 N=8 points.
- Detachment fragment: >= N-3 detached sites => witness (every N).

## Detachment law: REFUTED in general (full (det_p,det_q) table
over 643 exactly-decided pairs; witnesses at (1,1) and (0,1) exist,
blocked at (0,1)/(1,0)); SURVIVES: max(det_p, det_q) >= 2 =>
WITNESS [exhaustive 516/516]. W22's object reproduced exactly.

## N=8: complete X_2 generator built (M_c + dead edges; ~10^9
points); 60 sampled, all re-verified, fully decided (0 undecided):
0 all-blocked, min 3 witnesses. Cheap-witness test: 0 unsound
claims / 6 misses on 643 ground-truth pairs.

## Tooling hazard (ledger 22): sympy default printing sends
rational coefficients (k^2/9) to Singular, whose parser rejects
with rc 0 — the '?' guard is the only protection. Fix: clear
denominators first; sound because every term of E has total degree
2h (rescaling scales E by lambda^{2h}; verified 6/6).

## Controls: full mutation battery (with two vacuous-mutation cases
diagnosed and labelled rather than counted); resolution-of-L1+L2
measurements (12/120 mutations of Delta_{6,2} invisible to L1+L2);
inter-probe agreements with W22/W17 (incl. the 9-witness count,
three deciders); explicit-point + ledger-12/17 discipline
throughout. Soft spots: exhaustive only on D6(1) (cancellation
stratum open — the |F(e)| characterisation is proved); X_3 walk
samples one component; W23-U2 needs no-dead-edges; W23-N1 is about
the abstraction; L2D vacuous on current objects.

## Named next objects: (1) decide "X_3 => witness" at N=6 exactly —
the N=6 form of the U(N) core, not refuted; (2) the N=8 general
ladder ((4,4,0)/(4,2,2) shapes); (3) the cancellation stratum;
(4) push W23-U2 past dead edges.
