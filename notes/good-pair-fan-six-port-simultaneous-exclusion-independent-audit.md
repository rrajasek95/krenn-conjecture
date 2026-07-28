# Independent audit: the six-port simultaneous exclusion

## 1. Verdict

**Confirmed.**  Theorem A (both deleted star triples of a regular
nonbipartite pair chart are linearly dependent), Proposition C (each
27-row table is equivalent to the shared 81-row four-slot system, hence
the three tables are pairwise equivalent), and Corollaries B, D, E, F of
[the audited note](good-pair-fan-six-port-simultaneous-exclusion.md)
were reconstructed and re-verified in a clean room.  No discrepancy was
found in any statement, ledger, or guard claim.  One sharpening remark
was discovered (Section 6): the graph step of Lemma 4.1 also closes on
some *disconnected* graphs, so the connectivity hypothesis is
sufficient rather than sharp — this does not affect soundness.

Checker: [audit_fan_six_port_simultaneous_exclusion_independent.py](../computations/audit_fan_six_port_simultaneous_exclusion_independent.py)
(run from the repository root with
`uv run python computations/audit_fan_six_port_simultaneous_exclusion_independent.py`;
exits nonzero on any failure).  The full run reports
`checks run: 92` and `ALL CHECKS PASS` (about seven minutes; the
Singular saturations execute on 27 + 9 + 3 charts).

## 2. Clean-room protocol

The original artifacts
`computations/fan_six_port_simultaneous_exclusion_check.py` and
`computations/fan_six_port_simultaneous_singular_certificates.json`
were **not** read or imported.  Everything was rebuilt from the note's
prose plus the cited earlier theorem notes (source-Hessian dichotomy,
fan six-port reduction, target-flattening star bound, bridge frontier,
induced-zero four-cut, common-origin countermodel, all-pair missing-row
countermodel).  Deliberately different choices throughout:

* my own square-zero site algebra (monomials as base-4 integers, two
  bits per site), with divided powers computed by direct k-matching
  enumeration and cross-checked against repeated dict multiplication
  (`h^m = m! h^[m]` at N=6, 8);
* scattered vertex labels instead of natural ones: deleted pairs
  (2,5) and (0,7) at N=8 and (1,4) at N=6 for the pair identity; named
  fan vertices r=6, u=1, v=4, w=3 (Y = {0,2,5,7}) at N=8 and r=10,
  u=3, v=7, w=0 at N=12 — both storage orientations of every named
  block are exercised;
* my own prime 999983 (not 1000003) for the rank lower bounds, my own
  seed, my own random integer families;
* Proposition C verified at N=8 (full) and N=12 (the note reports
  N=10 as its own second order);
* Lemma 4.3 formulated my way, as an independent-transversal problem
  for the subspaces K_d = Ann(p_c) intersected over c != d, decided by
  Rado's criterion with exact rational linear algebra;
* Singular certificates rewritten from scratch: annihilator variables
  *before* p-variables in the ring order, charts enumerated in reversed
  lexicographic order, sequential saturation z-then-y-then-x, plus one
  certificate beyond the three the note describes (J4): the symbolic
  identity `det(p x s' + s x p') = 0`;
* complex values exercised through an exact Gaussian-rational class
  Q(i) (Fraction real/imaginary parts), including a gauge-rigid chart
  with complex entries.

## 3. What was reconstructed and measured

### 3.1 The pair contraction identity (imported input 1)

Rederived: for any full quadratic source h and deleted pair {y,z}, the
(c,d) two-slot coefficient of `h^[m]` equals
`a_cd q^[t] + p_c s_d q^[t-1]` (t = m-1), as a block identity prior to
any target equation.  Verified termwise against fully expanded
`h^[3]` (15 matchings, N=6) and `h^[4]` (105 matchings, N=8) for
random integer sources at three differently placed pairs; all 9 cells
nonvacuously nonzero in each test.  Additionally verified for a source
whose every block is an explicit parallel-decorated aggregate: a sum
of rank-one outer products including an exactly cancelling pair — the
identity retains aggregation and cancellation literally.

### 3.2 The annihilator trichotomy (Lemma 4.2)

Ann dimension 3/1/0 for support 1/2/>=3, with the stated generators
(V_x; the antipodal line (p_x, -p_y)):

* exact rationals on 4 and 5 sites, all support sizes, including
  sparse local vectors and negative entries;
* Q(i) on 4 sites;
* full census over F_3 on 3 sites: 19,682 nonzero forms = 78 one-site
  (dim 3) + 2,028 two-site (dim 1) + 17,576 support>=3 (dim 0) —
  matching the note's ledger exactly;
* my additional exhaustive census over F_5 on 2 sites (248 one-site
  dim 3, 15,376 two-site dim 1);
* 4-site F_3 census: all 104 + 4,056 low-support forms exact, 2,000
  random support>=3 forms trivial;
* 40 exact rational nullspace samples on 5 sites.

The characteristic-zero closure is carried by the three Singular
certificates (Section 3.7), not by the finite sweeps.

### 3.3 The collapse lemma (Lemma 4.3)

Formulated as an independent-transversal problem and decided by Rado's
criterion (exact rational): over 200 trials on 4 sites spanning
deliberate support patterns and random ones, an independent s-triple
exists **iff** all three p_c are one-site with a single common support
site (21 admitting / 179 blocked in the final run — the 20 planted
one-common-site patterns plus one random pattern that landed on the
admitting type, correctly detected).  In every admitting case the
constructed transversal was verified to lie in the common V_{x*} with
all diagonal products zero.  Same criterion verified over Q(i).

Class census over F_3 (3 sites): 1,017 nonzero annihilator classes =
1,014 antipodal lines + 3 coordinate factors V_x; distinct classes
intersect only in 0 (structural check on all classes, rank check on
4,000 sampled pairs); consequently exactly 3 ordered class triples
admit an independent transversal — the three all-V_x triples — and
all-equal line triples are blocked.  This reproduces the note's
1,017/1,014/3 ledger by a different route.

### 3.4 Gauge kernel and regular charts (imported input 2, nonvacuity)

* `Z^alpha q^[t-1] = 0` verified exactly for random alpha and q.
* Gauge-rigid integer families constructed independently with every
  block of nonzero determinant:
  - |W|=4: exact rational rank **51/54**, kernel exactly 3;
  - |W|=6: rank **130/135** mod 999983 (exact lower bound) plus exact
    integer gauge annihilation and exact gauge independence, kernel
    exactly 5;
  - |W|=8 (the N=10 chart size, beyond the note's own sweep): rank
    **245/252**, kernel exactly 7.
  The 51/54 and 130/135 figures agree with the note's reported ranks.
* Edge cases inside the hypotheses: a zero-weight chart (block {1,4}
  deleted; G_3 = K_6 minus an edge, still connected spanning
  nonbipartite) is gauge-rigid with the same 130/135 certificate; a
  colour-diagonal chart at |W|=4 (all blocks invertible diagonal) is
  gauge-rigid (kernel 3) — a structured regular chart on which the
  exclusion applies; a Q(i) chart at |W|=4 has kernel exactly 3 over
  Q(i).

### 3.5 The degree-two vanishing mechanism (Lemma 4.1)

Split into independently checked steps, in my own order:

* E1: `q q^[t-1] = t q^[t]` (exact, |W|=4,6);
* E2/J4: product blocks `(P S)_{ij} = P_i x S_j + S_i x P_j` have rank
  <= 2 — random exact check plus the symbolic zero-determinant
  certificate;
* E3 (graph step): the affine system {alpha_i + alpha_j = gamma on
  edges, sum alpha = 0} has only the zero solution on 17 connected
  spanning nonbipartite graphs (K_4, K_6, C_5, C_7 + chord, K_6 minus
  an edge, 12 random); bipartite spanning (C_6, K_{3,3}, K_{2,4},
  star), nonspanning (triangle + isolated vertex), and disconnected
  (triangle + edge) graphs all admit nonzero solutions;
* E4 (operational collapse): on every certified regular chart
  (generic |W|=4 and 6, zero-block |W|=6, colour-diagonal |W|=4, and
  |W|=8 in Section H), the exact kernel of
  `(gamma, S) -> gamma q^[t] + P S q^[t-1]` equals `0 + Ann(P)` with
  dims 3/1/0 by the support of P.  This is precisely the note's claim
  that top-degree orthogonality plus gauge rigidity forces the literal
  degree-two identities a_cd = 0 and p_c s_d = 0.  At |W|=4,6 the
  kernel is computed exactly over Q; at |W|=8 by the two-sided
  certificate (exact annihilation of the embedded Ann(P) plus mod-p
  rank).

### 3.6 Theorem A endgame

* X_0, X_1, X_2 are distinct basis monomials (nonzero, pairwise
  independent) — so `a q^[t] = X_c` for two distinct colours is
  unsolvable for any q^[t] (including q^[t] = 0), verified on the
  rigid charts, where q^[t] has 78 (|W|=4) resp. 724 (|W|=6) impure
  monomials in the final run;
* products of two one-site forms vanish;
* endpoint exchange transposes a, swaps the two row families, and slot
  extraction commutes — verified concretely, so the mirrored case
  analysis (independent p-triple) is licensed and both triples are
  forced dependent;
* the three case branches (two p_c zero / all nonzero / exactly one
  zero) each terminate in one of the verified impossibilities; the
  assembly is recorded in the checker with its dependency list
  (E3/E4/C/F).

### 3.7 Singular certificates (parameter-uniform closure)

All over Q with fully symbolic entries, no anchor or value fixed, my
own orders:

* J1 (three-site kill): 27 charts, sequential saturation by z_k, y_j,
  x_i in reversed chart order; all nine annihilator variables in every
  saturated ideal;
* J2 (two-site branch): 9 charts; all six 2x2 alignment minors in the
  saturation;
* J3 (separation): 3 charts; all three s-variables in the saturation;
* J4 (extra): the generic product block determinant is the zero
  polynomial.

These correspond to the note's C3/C2/C1 (in my order J1/J2/J3) and
close Lemma 4.2 uniformly in characteristic zero.

### 3.8 Proposition C and the 81-row system

At N=8 (full, my labels r=6, u=1, v=4, w=3):

* `h^4 = 24 h^[4]` (105 matchings vs repeated products);
* matching classes of one table: **15 direct + 60 three-star + 30 dead
  on the zero blocks** (15+60 as claimed);
* all 27 triple contractions of `h^[4]` equal each of the three tables
  `p_c(b_de q_pair^[2] + s_d t_e q_pair^[1])`, for all three pairs;
* the spectator-free part of every R_de equals the Y-formula
  `b_de q_Y^[2] + s_d t_e q_Y^[1]` and is annihilated by every p_c
  (degree |Y| saturation);
* the spectator sectors of all three tables coincide with one shared
  T_def list, equal to
  `(b^uv_de g_f + b^uw_df t_e + b^vw_ef s_d) q_Y^[m-3]
   + s_d t_e g_f q_Y^[m-4]`; resummation is exact;
* all **81** four-slot contractions of `h^[4]` equal `p_c T_def`,
  nonvacuously (81/81 nonzero rows);
* the w-sector of the target `X_c^{W_uv}` is `delta_{fc} X_c^Y`,
  giving the table <=> 81-row equivalence on the right side.

At N=12 (sector identities, my labels r=10, u=3, v=7, w=0): for each
of the three tables, the 27 spectator-free Y-formulas, the 27 p_c
annihilations, and the 81 sector identities against the shared T list
all hold exactly (9-site matching enumeration on the pair chart versus
8-site Y-power assembly).  This is a larger second order than the
note's N=10.

### 3.9 Corollary ledgers

* Essential-subspace lemma (<= 3 deletion-essential subspaces of a
  spanning family in dimension 3): 60 random exact rational families
  plus an exhaustive F_2^3 census over all 18,831 spanning multisets
  of at most five subspaces.
* Star injectivity <=> independence of the row triple (exact, with
  planted dependent cases).
* Threshold-free arithmetic for every even N = 8..40: good pairs
  >= N(N-7)/2 (4 at N=8), fan degree >= N-7 >= 1; F = empty implies
  all fan pairs escape (strictly stronger than the old N-15 at
  N >= 16); the item-2 and hereditary triggers |F| >= 9, 17 are
  unreachable; Corollary D's alternative 1 holds for every k with
  N >= 7k+7; Corollary F's cap floor(3N/2) (12 at N=8, 60 at N=40)
  follows from <= 3 deficient partners per vertex and both
  orientations of a regular pair being deficient.
* Corollary E (bridge stratum 4 empty): the stratum is exactly
  Theorem A's hypothesis set plus both-injectivity; the mechanism was
  closed at chart sizes |W| = 4, 6 (N=8) and 8 (N=10), the last by a
  fresh two-sided kernel certificate.

### 3.10 Guard countermodels (all outside the hypotheses, as claimed)

1. The fan note's abstract three-port model (24): all 27 capped
   equations hold with one-site p_c at three **distinct** sites — so
   the capped table alone cannot force the one-site collapse; the
   exclusion must (and does) operate upstream of the cap.
2. The common-origin six-cycle countermodel: rebuilt from its note;
   `q^[3] = 0`, cofactor matrix equal to its (12), det C = **-256**,
   C^{-1} rows reproduce its explicit s_j, all nine
   `p_i s_j q^[2] = delta_ij` cells and `A_i B_j = 2 delta_ij` cells
   verified.  Outside the hypotheses on every count: q itself is an
   extra kernel vector, q is not a gauge vector (alpha_i + alpha_j = 1
   on an even cycle is incompatible with the zero sum), and all blocks
   have rank <= 1, so the ternary rank-3 graph is empty.
3. The complementary-support family: `A_i B_j = 2 delta_ij X_i` with
   genuine colour axes and no common q.
4. The fourteen-site bridge family: all 91 pairs both-aggregate-
   injective; the internal rank-3 graph fails connected-spanning for
   all 91 pairs; constant coefficients 29 / 701 / 3,812,509 at
   d = 1, 2, 9 (my own cross-subset enumeration, matching
   P(d) = 1 + 7d^2 + 14d^4 + 7d^6); an exhibited mixed coefficient is
   strictly positive (value 19 for my chosen mixed monomial), so the
   family is not an exact source.  It confirms the escape strata of
   Corollary E are coherently occupiable.
5. The all-pair-missing-row model: constant coefficients (49, 53, 41)
   before normalization reproduced by direct 105-matching expansion;
   6,558 mixed monomials, all positive (not an exact source); for all
   28 pairs the internal rank-3 graph is bipartite or fails
   connected-spanning — the model stays on the escape branch and is
   untouched by Theorem A.

## 4. Adversarial attempts

Attempts to break Theorem A within its stated hypotheses, all
unsuccessful (consistent with the theorem):

* **Colour-diagonal chart.**  All blocks invertible diagonal gives a
  regular chart (gauge-rigid, G_3 = K_4).  Colour-aligned rows
  p_c, s_d then make every mixed product visibly nonzero unless a row
  dies, and the E4 collapse applies verbatim: no independent triple
  survives.  The structured chart does not open a gap.
* **Zero-weight chart.**  Deleting one block (K_6 minus an edge)
  keeps the chart regular; the mechanism closes identically.
* **Complex entries.**  A Q(i) chart at |W|=4 is gauge-rigid over
  Q(i); the trichotomy and collapse criteria hold over Q(i).  Complex
  cancellation does not reopen the annihilator dimensions.
* **Parallel/decorated aggregates, asymmetric blocks, sparse local
  vectors.**  All families use fully asymmetric random blocks; one
  pair-identity test builds every block as an explicit sum of rank-one
  decorated sources with an exactly cancelling pair; aggregate rows
  with zero individual coordinates were planted in the trichotomy
  tests.  No change.
* **Escape-side sanity.**  On bipartite spanning graphs the affine
  gauge system has nonzero solutions (dim 1 in all four bipartite
  cases tested), matching the known bipartite antipodal escape — the
  mechanism genuinely needs the odd cycle, and the countermodels of
  Section 3.10 live exactly there.

## 5. Key numbers

| quantity | value |
|---|---|
| Hessian ranks (|W|=4 / 6 / 8) | 51/54, 130/135, 245/252; kernels 3, 5, 7 |
| F_3 annihilator census (3 sites) | 78 / 2,028 / 17,576 with dims 3 / 1 / 0 |
| F_5 census (2 sites) | 248 dim 3, 15,376 dim 1 |
| annihilator classes | 1,017 = 1,014 lines + 3 V_x; admitting ordered triples: 3 |
| Rado trials (4 sites, Q) | 200 trials: 21 admitting / 179 blocked, criterion exact |
| N=8 matchings / classes | 105; one table = 15 + 60, 30 dead |
| 81-row system at N=8 | 81/81 rows equal p_c T_def, nonvacuously |
| N=12 sector identities | 3 tables x (27 + 27 + 81) cells exact |
| guard reproductions | det C = -256; P(d) = 29, 701, 3,812,509; constants (49, 53, 41) |
| Singular | J1: 27 charts, J2: 9 charts (6 minors), J3: 3 charts, J4: det = 0; all PASS |
| F_2^3 essential census | 18,831 spanning multisets, essential count <= 3 |

## 6. Findings and remarks (non-blocking)

1. **Connectivity is sufficient, not sharp, in the graph step.**  Two
   disjoint triangles — a disconnected spanning union of nonbipartite
   components — also force (alpha, gamma) = 0 in Lemma 4.1's affine
   system, because each nonbipartite component pins alpha = gamma/2
   and the global zero-sum then kills gamma (characteristic zero).
   Theorem A is stated for connected spanning nonbipartite G_3 and is
   correct there; the strictly larger chart class "spanning with every
   component nonbipartite" satisfies the same degree-two collapse.
   This could slightly enlarge the emptied stratum in a future
   sharpening; it does not affect any claim audited here.
2. The note's phrase "connected as a graph on all of W" was read as
   connected + spanning; the checker treats isolated vertices as
   disconnecting, consistently with the cited dichotomy note's
   "connected, spanning".
3. All statements of the note that were checked are conditional
   identities or unconditional finite computations; no check required
   assuming an exact source exists.  The endgame contradiction
   `a q^[t] = X_c for two colours` is refuted for *arbitrary* q^[t]
   (zero or not), so the case analysis has no gap at degenerate
   charts.  (Consistently, on a regular chart q^[t] = 0 cannot occur
   at all, since q would then be a non-gauge kernel vector.)

## 7. Scope

This audit certifies Theorem A's proof chain, Proposition C's
equivalence, the corollary ledgers, and the guard discipline.  It does
not (and the note does not claim to) close Krenn's conjecture: the
good pairs are pushed into the extra-kernel / disconnected-or-
nonspanning / connected-bipartite strata, and the uniform descent must
now come from those charts.
