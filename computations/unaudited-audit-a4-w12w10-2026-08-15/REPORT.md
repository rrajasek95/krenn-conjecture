# AUDIT A4 — W12 (cut mechanism) + W10 (Lemma W10-G) — REPORT (UNAUDITED, 2026-08-15)

Pinned HEAD a1a7748. From-scratch engine, deliberately different
routes (bitmask matchings; active-subgraph fibres; canonical
polynomial dicts; EXACT cleanness criterion; direct Groebner on half
variables — no lattice/Smith/torus). Exact arithmetic incl. Q(i).
Agent's write was policy-blocked; this transcribes its report.

## Verdicts — all mathematics CONFIRMED
- W12-A (split kill): CONFIRMED; actually slightly stronger than
  implemented (empty constant fibre already kills). Evenness
  load-bearing (odd-part controls fail as required).
- W12-B (cut extraction): CONFIRMED sound, both pinning rules valid;
  the back-ends can only MISS kills, never manufacture one (checked
  at three points: MonomialValues transport, elementary-divisor
  guard, unit-ideal Q->C stability). CONSERVATIVE (D4): the star
  cleanness test is strictly weaker than the exact criterion — 156
  vs 152 equations on immunity m=20; swap recommended (more reach,
  no soundness cost).
- W12-C (boundary): CONFIRMED and UPGRADED from sampling to an
  exhaustive extremal PROOF (hand proof both directions + down-set/
  up-set reduction verified at N=4,6,8,10; all 2^15 graphs at N=6;
  the probe's own random evidence never touched 20..28-edge graphs
  (D5) — replace it with the extremal check on promotion).
- m=20 survivor kill + eight-word certificate: CONFIRMED three ways
  (200 generic rational points; independent saturation; own
  Rabinowitsch); leave-one-out STRENGTHENED to explicit exact
  witnesses for each dropped word; specificity confirmed (does not
  force F(1^8), F(2^8)).
- Three-line immune kill m=20/21: CONFIRMED monomial-exactly.
- Sweep: CONFIRMED-WITH-CORRECTION (D1): there are 48 W11 witnesses,
  not 47 — scplus_m19_5242749_0 had NO recorded verdict anywhere;
  A4 killed it independently (L=[0,7], 1.4 s). 130/130 true, one
  entry unevidenced until now. m=22/23 kills reproduced by a
  DIFFERENT decision procedure (genuine verdict cross-validation).
- Reduction soundness: CONFIRMED, scope precise — valid over C
  (divisibility of C*; x^2 example shows Q fails); killed transfers
  Q->C; elementary-divisor>1 branch tested behaviourally on a
  synthetic feasible instance: returns undecided, never kills.
- Negative control: numbers reproduced to the unit (12 equations +
  229 non-vanishings, 0 violated) with correction D3: the 229 are
  (P1)-vacuous, (P2) untested by it, and the template is
  support-dead (mixed-only mode is the real content).
- W10-G: CONFIRMED and easier than billed — ANY gauge preserves
  mixed-exactness (support pattern literally unchanged); the three
  constant normalisations are exactly decoupled (three free scalars
  at one site). Verified over Q and Q(i) incl. extreme moduli;
  45/45 end-to-end round trips at N=4. W10-6 CONFIRMED (needs only
  the existence half). (SC) gauge-invariance trivial, confirmed.

## Discrepancies (evidence/bookkeeping, not mathematics)
D1 48th witness unrecorded (fixed here); D2 results_t4_controls /
t8_soundness never written — C1/C2 round-trip controls UNEVIDENCED
(re-run or drop); D3 negative-control phrasing; D4 star-vs-exact
cleanness; D5 W12-C evidence gap (now replaced by proof); D6 NEW
SINGULAR TRAPS: errors on stdout with return code 0 (must parse for
'?'); `ideal S = sat(I,J)[1]` silently takes the first GENERATOR —
use `list L = sat(I,J); ideal S = L[1];`.

## Bottom line
W12-A/B/C, the m=20 kill, W10-G/W10-6: SAFE TO PROMOTE with the
noted amendments. The (R) residual m=24..28 is correctly defined
(zero extractable equations at any even cut — matches the Gamma
predicate exactly). 20-row mutation-control ledger, all behave.
