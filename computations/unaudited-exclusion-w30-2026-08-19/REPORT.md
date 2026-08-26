# W30 — the residual pairwise exclusion — FINAL (UNAUDITED, 2026-08-20)

PINNED_HEAD 021b1a3. Exact arithmetic; Q + F_13/F_31 (= 1 mod 3).
Transcribed by the manager from the lane's final message. 29
detached checkpointed jobs were still running at close; all
results harvestable from disk in this dir.

## BOTTOM LINE
**W26's named pair (L2,R5) is FALSE at m=28** (explicit points,
8-control verification incl. W26's own engine; 2,270 found / 17
fully re-verified over F_31, replicated F_13; also refuted:
(R5,R6), (R5,R7), (L0,L2)). **And the pairwise framing was the
wrong statement at 25/26/27**: one member of each pair NEVER
fails — Theorem W30-X gives the mechanism and predicts exactly
why m=28 differs.

## Key discovery about W26's evidence
W26 sampled 40-60 ambient words/point vs 243-823 admissible index
choices (~2% coverage), and DELIVERS is a disjunction over index
choices => undersampling systematically OVER-REPORTS failure.
W30's exhaustive engine: C1 agreement 39/39 on stored points; 2 of
W26's 11 off-stratum failure patterns were spurious. W26 failure
counts = upper bounds only.

## THEOREM W30-X [probe-proved; hypothesis (H) residual]
Slice matrix S(tau)[t][j] = A_{v,s_j} cell (letter t of v, letter
tau_j of s_j); trigger-free. (1) Reduction: one absent column +
u_q0 != 0 + sc != 0 => ROWS = psi(S), psi in GL_3, so v delivers
iff rank S = rank(S | clean rows). (2) Two distinct firing letters
realised at a common tau + all Gamma cells nonzero: non-delivery at
both => rank S(tau) = 3. (3) Cofactor identity (hafnian
multilinearity only): Phi(w|v=t) = <S(tau)_t, Q(w)>, Q_j =
haf_{Gamma-{v,s_j}}(w); three clean letters => S.Q = 0, so Q != 0
=> det S = 0 (rank <= 1 when |N(v)| = 2). (2)+(3) contradict => v
delivers. Protected vertices: m=25 R6 (|N|=2 — UNCONDITIONAL,
step (3) not needed), m=26 R5+R6, m=27 R5 (via det S = 0), m=28
NONE (every vertex has 4 Gamma-neighbours; S is 3x4; the mechanism
evaporates — exactly matching the observed refutation). Prediction
tested on 21,927 adversarially steered clean points: 0 violations;
dedicated falsification hunters scored 0.0000 on the protected
vertices. Step (3) is also a short independent proof of W26's
"det M = 0". Residual hypothesis (H): tuple/index-choice
realisation with hafL != 0 (and Q != 0 for |N|=3) — verified
pointwise (0 violations, typically 12/12 tuples), NOT eliminated.

## Route A status after W30
- m=26: unconditional (W26-1); W30 = second mechanism.
- m=25/27: joint theorem follows from W30-X modulo (H); m=25's
  protected vertex needs no det-S input at all. Natural closer:
  Singular elimination of the (H) escape (staged, NOT executed —
  no Singular ran in this lane).
- m=28: the pairwise-exclusion route AS POSED IS DEAD. Survivors
  (L1|L2, L1|R5, L1|R6, L2|R6) have no structural support. A NEW
  residual statement is needed. The DISJUNCTION itself survived
  everywhere: max 6-of-8 across 21,973 points incl. a lane
  explicitly maximising failures (best 7.119/8, never 8).

## 8x8 co-failure table (results_cotable.json)
m=25: 3,741 pts, max 4 simult., never-failed {R4,R6,L2}, 18/28
pairs never co-fail; m=26: 1,235 / max 3 / {R5,R6,L2} / 23/28;
m=27: 9,563 / max 6 / {R5} / 10/28; m=28: 7,434 / max 6 / none /
4/28.

## Soft spots (verbatim from the lane, abridged)
W30-X probe-proved not audited; (H) pointwise only; refutations
over F_31/F_13 not Q (Q hunter 1.174/3) — for the C-statement the
m=28 exclusion is not formally dead, but the characteristic-free
ideal route to it IS; the (H)-escape counting argument does NOT
close (H) (escape hunter reached 30/81 at m=25/F_13 without the
required cover pattern) — only the cover structure does, weakest
point; "never co-failed" cells are failed searches, not evidence
(ledger 18); w30_build/w30_rank1 produced zero clean points
(failed searches, establish nothing); w30_thm "0 good tuples" at
m=25 R6 is a checker artifact (requires |N|=3), not an escape;
adv2 builders attack survivor STARS (different object), not
duplicated. Certificates: results_verify_hunt.json,
results_cotable.json, results_struct.json, results_thm_*.json,
points_hunt.json (350 verified points), engines w30_*.py.

---

# W30 FOLLOW-ON ROUND (2026-08-20; 33 detached jobs still checkpointing)

## The staged (H)-elimination target is FALSE
Explicit escape object (results_escverify.json): m=27/F_13, hafL
vanishing on 36/81 L-words covering EVERY two-pair tuple at R5 —
yet clean (2 routes), off-stratum (1107 nonzero words), all 135
Gamma cells nonzero, AND ALL EIGHT VERTICES STILL DELIVER. So (H)
is sufficient-never-necessary; the containment statement staged
for elimination is refuted; do not attempt it.

## THEOREM W30-Y [probe-proved] — the Q-span law, uniform in m
rank S(tau) <= |N(v)| - dim span{Q(w) : w untriggered with tuple
tau} (from S.Q = 0 at untriggered words). If v has two distinct
firing letters, tau realises both clean pairs with a surviving
index choice (scale != 0), and dim span Q >= |N(v)| - 2, then both
clean pairs cannot collapse => v DELIVERS. 604 points, 0 law
violations, 0 kernel-bound violations (results_qspan_law.json,
running). Predicts the ENTIRE failure table: m=25 R6 (|N|=2,
threshold 0 — automatic given realisation), m=26 R5/R6, m=27 R5
(threshold 1, met at every point), m=27 R6/L1/L2 + m=28 R5/L2
fail exactly when the hypothesis fails, m=28 R6/L1 protected
(586/586, 585/586). The single apparent exception traced EXACTLY
to the scale side condition (hafR = 0 killed every index choice).
Explains: why m=25/R6 is near-unconditional, why m=28 has no
absolutely-protected vertex, why every maximal m=28 survivor set
contains L1.

## m=28 disjunction: reduced but the converse fails
Mechanism-targeted hunters drove the W30-Y hypothesis to 0 for
L1+L2 simultaneously (and for R5+R6) — neither vertex failed. So
the disjunction needs strictly more than the Q-span law.

## Singular/lattice
w30_sing.py harness built + self-tested 7/7 (guards, ?-parse,
sat form); m=25 elimination thrashes. Binomial lattice engine
(Farkas-type torus certificates): 0/64 branches certified —
FAILED SEARCH, incomplete kernel enumeration, not evidence
(ledger 18). Q-lift of the m=28 refutation: still open (targeted
Q hunters got L2 to qspan 0, R5 stayed 24).

Soft spots: W30-Y probe-proved not audited; scale side condition
is a genuine hypothesis; no Singular verdict on any real branch
yet; qspan tally partial (604/1300).

---

# W30 ROUND 3 (2026-08-20; 37 detached jobs; results_diag28_ep2.json, results_side.json)

## THEOREM W30-Z [probe-proved; supersedes W30-Y as governing law]
At a two-firing-letter vertex with a two-pair tuple whose both
clean pairs survive and S_{t1} not in ker phi: **rank S(tau) <= 2
=> the vertex DELIVERS; failure requires rank S(tau) = 3.** W30-Y
is the special case via the Q-span bound. Delivery-mechanism
classification at the adversarial endpoints is TOTAL (D1b rank<=2
beyond the cofactor bound: 1363; D2 ker-phi delivery at rank 3:
320; D1a = W30-Y: 32; other: 0; G2/G3 controls pass). Blind test
60 pts x 4 vertices: deliver at rank<=2 124/126, FAIL at rank 3
112/114, both exceptions = the known scale side condition + one
D2. W30-Y controls now 2,340 pts, 0 violations. At the endpoints
rank S is CONSTANT over all 81 tuples and equals the common
Gamma-block degeneracy.

## m=28 disjunction, sharpened
Now a determinantal statement (36 vars/vertex): AT LEAST ONE of
R5, R6, L1, L2 has slice rank <= 2. Rank hunters (F_31/F_13/Q):
best ever reached = 2 of 4 at rank 3 (pairs {L1,L2},{R5,L2}),
never 3 or 4. Proper Singular-sized target; not yet launched.

## Side conditions per support
(a) two distinct firing letters: **PROVED per support by
exhaustive template enumeration** (R6@25 {1,2}; R5@26 {0,1};
R6@26 {1,2}; R5@27 {0,1}); negative control: "two firing letters
AND |N|<=3" selects EXACTLY the protected set, 0 mismatches.
(b) realisation half PROVED combinatorially (6/12/16/12 two-pair
tuples); scale half = the (H) escape, point-dependent, reachable
at m=27 (verified object), minimal escape sizes exact (>=12/81 at
m=25 and m=26/R6; >=24/81 at m=26/R5, m=27/R5); m=25 hunters at
33/81 without ever achieving a cover (failed search, not proof).
(c) REDUCED TO AN N=6 STATEMENT at m=27/R5: Gamma-{5,s} is a
6-vertex 4-matching model (K3+K3+PM); the escape = all three
N=6 sub-points on their vanishing strata (672 equations); the
(c) hunter cannot move qspan off 12/12 in either prime. Hand-off
to the campaign's N=6 machinery indicated.

## Standing
m=25 closest to unconditional (threshold 0; only the scale half
remains). Lattice engine: 0/64 branches certified (honest
negative, positive control confirms no over-fire). Q-lift open;
char-0 rank hunter hits the same 2-of-4 ceiling (mild evidence
against small-characteristic artifact; NOT a Q co-failure).
Soft spots: W30-Z side condition stated not eliminated (2/240
measurements live there); all ceilings are search results.

---

# W30 ROUND 4 (2026-08-20; 41 detached jobs, 4 Singular live)

## Own candidates refuted (controls working)
- W30-W ("R6 never at rank 3" — would have made the m=28
  disjunction unary): REFUTED over Q — verified clean off-stratum
  point, all 144 Gamma cells nonzero, R6 at rank 3 at ALL 81
  tuples yet delivering via D2 (1/205 index choices). Also shows
  W30-Z's CONVERSE is false (rank 3 does not imply failure).
  W30-Z itself untouched.
- Side condition (c) REFUTED as necessary: R5 Q-span driven to 0
  at m=27/F_13 (and m=26 both vertices) — still delivers, rank 1.
  Only W30-Z governs.

## m=28 target identified exactly (results_cover.json)
Rank-3 sets over 400 pts: max simultaneous = 2 of 4 (F_31, F_13,
AND Q). Reached pairs: {L1,L2}, {L2,R5}. Never reached: {R5,R6},
{R5,L1}, {R6,L1}, {R6,L2}. All-eight-fail needs all four at rank
3 => ANY ONE of those four 2-subset rank-3 exclusions gives the
disjunction. That is the elimination target.

## m=25 (the first committed support-band theorem candidate)
Escape-cover structure EXACT: 5 covers, exactly 2 inclusion-
minimal (sizes 12 and 30; C3/C4 minimality controls 0 violations).
Size-12 cover = {x : x0=0, x1!=1, x2!=2}. Elimination launched:
74 generators / 45 variables in char 0, 13, 31 — first feasible-
looking Singular target; no verdict yet. Fibre-counting alone does
NOT close it (1200/2187 y6-fibres provably contain a clean word;
not all).

## N=6 hand-off narrowed + the disjointness lemma
Closed forms verified exactly: Q2 IS the N=6 KG hafnian
(K3+K3+sigma-matching); Q4/Q6 are 4+2 splits, NOT N=6 models —
and the six-site theorem is about exactness, not vanishing, so no
direct bridge. LEMMA (algebraic, one line): on hafL = 0,
Q4 = d0.d3.l12 — a product of three Gamma cells, nonzero by
hypothesis => the (b) and (c) escapes are DISJOINT (confirmed on
the m=27 escape object 12/12; vacuous on stored points — reported,
not counted).

Soft spots: no Singular verdict on any real ideal yet; all
ceilings are failed searches (and the Q counterexample above is
the live warning of how ceilings break); Q-lift of an m=28
CO-FAILURE still unachieved (this round's Q object is a
delivering point).

---

# W30 ROUND 5 (2026-08-20; A10 corrections adopted)

## Cover-based m=25 elimination RETIRED
A10's Q point 925024 re-verified (clean, cells nonzero,
off-stratum, over Q): hafL zero on 54/81 L-words; **fully contains
the size-30 cover** => that target FALSE. Size-12 not contained
(jobs stay live but OFF the critical path). Deeper: R6 there has
559 zero-scale choices yet DELIVERS at 264/264 surviving ones —
satisfying a cover does not make the vertex fail; the covers were
necessary only for the two-pair rank-1 device, not for
FAIL_primary.

## D2 candidate closed form REFUTED — and D2 is NOT the escape
mechanism
(D2*) "D2 fires iff <kappa, Q(w)> = 0" refuted: agreement
500/3468; the pairing is evidently an identity (the master
relation itself) — caught by the lane's own outside-locus control.
Sharper: **D2 fires at NONE of the three escape objects tested**
(0 events at every vertex of A10's m=25/Q point and the m=27/F_13
cover object). At A10's point the deliveries are plain
non-collapse (rank phi(S') = rank S' throughout). The proposed
case split "W30-Y off the escape locus, D2 on it" DOES NOT EXIST.
What protects escape points remains unidentified — now with two
mechanisms eliminated.

## Statement hygiene adopted retroactively
W30-X retired; S' (augmented, sigma column = d) everywhere;
FAIL_primary named; |T_f| = 1 explicit; m=28 refutation = F_31
only (F_13 replicates (R5,R6)); count corrected 2,270 -> 1,657
distinct; char-0 statement open (ledger 24); A10-D5 accepted
(pure rows survive at every co-failure point).

## m=28 pairwise rank-3 exclusions: unchanged, still the target.

Soft spots: D2 refutation rests on own column ordering (one bug
fixed mid-run; third-party kappa re-derivation wanted);
"264/264" is one point not a pattern (no escape-locus delivery
statistics yet); still no Singular verdict in five rounds.

---

# W30 ROUND 6 (2026-08-20)

## Escape-locus mechanism SETTLED empirically: plain non-collapse
30-point sweep (22 genuine escapes), every |T_f|=1 index choice
classified: M_nocol 6,523; M_zero 5,081; M_fail 808 (ONLY on the
escape locus — escape makes collapse possible, never universal);
M_inside 0; M_D2 0. Delivery on the escape locus = absence of
letter collapse; the escape only deletes choices via sc = 0.

## FAIL_primary case tree (pruned by W30-Z + the sweep)
Failure at v = at every admissible |T_f|=1 choice: hafL(x) = 0 OR
collapse with firing row outside. BRANCH T (total degeneracy):
hafL == 0 on X_v, and **|X_v| = 42 of 81 uniformly** (every
protected vertex, every support 25-28). Necessary for ANY failure.
Never reached: A10's record point has 54/81 zeros but MISSES 12 of
the 42 (exactly why it keeps 264 surviving choices); hunters top
out at 45/81. Now a sharp 42-equation elimination target in the 54
L-block cells + cleanliness. BRANCH C: survivors all collapse —
the round-3 collapse machinery's branch; 89% of survivor choices
are M_nocol even on the escape locus.

## Standing pre-launch control adopted
No elimination launches until its target is evaluated at every
stored escape/refutation object (this is what stopped a cover-
style mis-formulation of Branch T this round).

Soft spots: the sweep sample is generator-correlated (30 pts, own
hunters); Branch-T-unreached is a failed search (~5 hunter-days;
the 54/81 record came from ANOTHER lane's generator); kappa
identity still observation-only; the size-12 cover job is off the
critical path.

---

# W30 ROUND 7 (2026-08-20; load 146 post-purge)

## THE m=25 STRUCTURAL RESULT (dissolves the intersection frame)
At m=25, N(R6) = {5,7} (sigma edge absent), so ROWS =
hafL.[c7 | 0 | c5] with a 3x2 slice matrix S'(y5,y7), and the
cofactor identity has TWO terms: Phi(w|y6=t) = A67[t][y7].B(w) +
A56[y5][t].C(w), Q = (B,C). At untriggered words S'.Q = 0, so
**Q != 0 forces rank S' <= 1 = rank S'|_P (rows nonzero by
all-cells-nonzero) => R6 DELIVERS at every admissible choice with
hafL != 0.** No collapse analysis, no covers, no escape geometry —
the intersection target CANNOT OCCUR at m=25. Verified: rank
S' = 1 at 90/90 (point,y5,y7) combos on all 10 off-stratum points
+ A10's 925024; Q = 0 never observed (120/120); A56, A67 rank one
at every point (why collapse was constant in (y5,y7) and why
survivors never collapsed).

RESIDUAL (conditional): (alpha) some admissible choice has
hafL != 0 (= NOT Branch T; empty in 801/801 stored failures);
(beta) Q != 0 at a matching untriggered word — Q = 0 needs
hafL.r45 = -l03.d1.d2 AND hafL.r47 = -l23.d0.d1 simultaneously
(RHS nonzero products of Gamma cells) — a two-equation pinning,
never observed.

## Hardness call
The 45-variable cover elimination: 3 jobs, ~10 CPU-min each at
load 146 with cores available, no output => **genuinely hard, not
starved** — and moot: formulated against the wrong mechanism.
Not reformulating.

## m=28 {R6,L1} deliberately NOT launched (judgement call)
The m=25 lesson: eliminate against the mechanism's frame, not a
symptom's. At |N| = 4 the analogous bound needs Q-span >= 2,
which the round-4 Q counterexample shows can fail at R6. The
|N|=4 mechanism must be re-derived before the determinantal ideal
is worth CPU. Deferral flagged for coordinator overrule.

## Soft spots
Corpus thin (10 points, one factory, + A10's point) — wants an
independent generator; (alpha)/(beta) unproved; the |N|=2
argument is m=25-SPECIFIC (m=26/27 have |N|=3, m=28 |N|=4 — this
is exactly why m=25 was always closest and the others resist);
seven rounds, zero Singular verdicts — every advance is structure
+ exact enumeration; ideals must get an order of magnitude
smaller to be worth launching.

---

# W30 ROUND 8 (2026-08-20)

## (beta) derived exactly; binomial route exhausted
B = hafL.r45 + l03.d1.d2, C = hafL.r47 + l23.d0.d1. Q = 0 pins
hafL twice; eliminating gives the pure binomial (CELL):
A03[x0][x3].A25[x2][y5].A47[y4][y7] =
A23[x2][x3].A07[x0][y7].A45[y4][y5]. 376 untriggered words in 9
(y5,y7) classes. Lattice engine: NO certificate in any class.
Pre-launch control (corrected mid-round): (CELL) ALONE holds on
whole classes at stored points (necessary != sufficient — e.g.
rank-one blocks satisfy it identically); the true target is
B = 0 AND C = 0, observed at 0/3,760 words. (beta) unproved.

## (alpha) Branch T at R6@25: no certificate
Correct X_{R6,25} (42 words). RED binomial system 296 gens / 53
vars: no certificate. Pre-launch control passes (closest object
12 short). (alpha) unproved. THEOREM W30-M25 NOT stated.

## Independent-generator control: mechanism survives, claim refined
A10-style builder (second family), F_13 + F_31: rank S' = 1 at
9/9 tuples on 6/6 points, R6 delivers 6/6. REFINEMENT: Q = 0 DOES
occur (6 words at one F_13 point) — but rank stays 1 and R6
delivers because Q != 0 at OTHER words in the class. Correct
statement: need Q != 0 at SOME untriggered word per relevant
class, which holds everywhere. (Third correction-by-independent-
construction of the lane; run the second family BEFORE stating
mechanisms.)

## Standing-rule refinement
Pre-launch controls must test the EXACT target, not a relaxation
(the (CELL)-only control produced a false alarm before
correction).

Soft spots: (alpha)/(beta) remain unproved with the binomial
engine exhausted; remaining formulations non-binomial; the lane's
Groebner record is 0-for-8 from 45 variables up; independent run
small (6 points).

---

# W30 ROUND 9 + CONSOLIDATED CLOSE-OUT (2026-08-20)

(Sections 1-3/5-8 of the lane's consolidated final report
restate rounds 1-8 above with A10's corrections adopted; new
content below.)

## Round 9 results
- (beta) linear route: words sharing an L-part differ only in y4;
  the double hafL pinning eliminates hafL leaving 36 binomials in
  24 variables — no lattice certificate, BUT the structure is
  decisive: y5, y7 range over all three letters, so **the
  (beta)-escape FORCES A45 and A47 to be rank one.**
- (alpha) evaluation matrix: 42 words x 126 monomials, exact rank
  42 (full ROW rank; column kernel dim 84) — the linear layer
  cannot force the contradiction (42 < 126). RED system: no
  certificate. (alpha) unproved.
- Measured block ranks at all 10 m=25 off-stratum points: A56
  rank 1 (10/10), A67 rank 1 (10/10), A14 rank 1 (9/10), **A45
  rank 2 (9/10) or 3 (1/10) — NEVER rank one.**

## THE HAND-OFF TARGET (smallest of the campaign)
> At a clean, off-stratum, all-Gamma-cells-nonzero m=25 point,
> **A45 is never rank one** — one 3x3 determinant condition
> (9 variables) against cleanliness.
If proved, (beta) closes; with (alpha) it gives THEOREM W30-M25.
Status: never-observed-in-10-points (ledger 18 — a target, not
evidence).

## Lane close-out
Firm results: the F_31 refutation (predicate-named, char-scoped);
the sampling correction; the cofactor/Q-span/W30-Y/W30-Z
machinery (promotion-ready per A10); the total mechanism
classification; the m=25 3x2 conditional theorem; the
withdrawn-claims table (7 entries, all caught by own controls or
A10). No unconditional protection statement; no Singular verdict
in nine rounds (the 45-var ideal formally called genuinely hard).
Still live: 2 escape hunters, Q co-failure hunter,
independent-family generators, 3 m=25 Singular jobs — all
checkpointed.

---

# W30 ROUND 10 — FINAL (2026-08-20; lane budget spent)

## The A45 reduction REFUTED by the lane's own build
Over F_31 the adversarial builder reached a clean, off-stratum,
all-cells-nonzero m=25 point with rank A45 = 1
(results_r10_beta_31.json) — the round-9 hand-off statement was a
10-point never-observed and fell in one round (ledger 27 again:
necessary-not-sufficient mistaken for the target). THE TRUE
(beta)-ESCAPE TARGET, settled analytically: **A45 AND A47 both
rank one WITH A COMMON COLUMN DIRECTION, shared with A14's row
x1** (the pinning pairs force every column of A45 parallel to one
vector as y5 ranges over all three letters; (P2) does the same
for A47 with the same direction). The pair-with-common-direction
has never been reached (rank A47 = 2 at the built point; R6
still delivers).

## The mechanism's exception, found by the independent family
One F_13 point (idx 5, of 33 independent points): rank S' = 2 at
ALL nine tuples, 54 untriggered words with Q = 0 — and R6 STILL
delivers (plain non-collapse). So "rank S' = 1" holds only where
(beta) holds — exactly as the conditional theorem states; no
counterexample to the CONCLUSION exists anywhere in the corpus
(43 points, two families, three fields). Corpus Q = 0 count: 123
words, ALL in the independent family — the lane's own generator
systematically missed that region.

## THEOREM W30-M25-CONDITIONAL [stated for promotion]
Hypotheses: (H1) clean, (H2) all Gamma cells nonzero, (H3)
off-stratum, (alpha) some admissible R6 index choice has
hafL != 0, (beta) at some such (y5,y7) an untriggered word has
Q = (B,C) != 0. Conclusion: R6 delivers => pure row => the m=25
joint-theorem mechanism fires. Proof chain: N(6) = {5,7} exactly
=> ROWS = hafL.[c7|0|c5], S' is 3x2; cofactor identity
Phi(w|y6=t) = <S'_t, Q(w)>; untriggered => S'.Q = 0; (beta) =>
rank S' <= 1; (H2) => rows nonzero => rank S'|_P = rank S' = 1
=> firing row inside; (alpha) => a surviving choice exists =>
delivery. QED. Verification: 90/90 (Q family) + 32/33
(independent family; the 1 exception fails (beta) and the
conclusion still holds). Hypotheses status: (alpha) unproved
(linear layer provably insufficient — eval matrix 42x126 rank 42,
kernel 84; lattice: no certificate); (beta) unproved (binomial
route exhausted; rank-one reduction necessary-not-sufficient).

## Lane close-out (10 rounds)
Firm: the F_31 refutation (scope-corrected), the sampling
correction, cofactor identity, Q-span bound, Lemma W30-Y
(S'-form), W30-Z, mechanism classification, Branch T/C split,
W30-M25-CONDITIONAL. Open: (alpha), (beta) (true target = the
common-direction pair), four m=28 rank-3 exclusions, Q
co-failure. Never achieved: any unconditional protection
statement; any Singular verdict (10 rounds). 13 processes remain
live + checkpointed (5 round-10 builds — the alpha-builds had NO
output at close, no conclusion either way — 2 escape hunters, Q
hunter, 2 generators, 3 Singular jobs); all harvestable from
disk.
