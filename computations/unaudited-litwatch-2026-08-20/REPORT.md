# UNAUDITED — Lane LW (Literature Watch) sweep, 2026-08-20
(Transcribed by the manager; the lane's write was harness-blocked.)
Repo HEAD at sweep: c375a0a (v65). Window 2026-08-12 -> 08-20.
Web-only: gh CLI, arXiv API, StackExchange API, HTTP.

## URGENT U1 — formal-conjectures PR #4659 claims n=8 d=3 over Z
AND over {-1,0,1}, PLUS the full even-N>=6 D>=3 integer case.
KitaKen1; opened 07-29; community-verified 08-08 (williamjblair);
OPEN/unmerged (reviewer silent). Method: restrict to 3 colours;
push Z -> ZMod 2; a complete N -> N-2 contraction lemma
(eqSystem_contract_two_zmod2: multi-update-edge cross terms have
EVEN MULTIPLICITY and vanish in char 2); six-vertex char-2 base
via CNF/LRAT (Mathlib lrat_proof). Axioms clean (no native_decide,
no sorryAx). Flips 12 answer(sorry) entries incl.
eqSystem8_no_solution_d3_int and _trinary_int and the general
eqSystem_no_solution_ge6_ge3_int/_trinary_int. NO collision with
our headline (theirs: full generality, one characteristic; ours:
diagonal structure, all characteristics); the char-0 field cases
(C, R) remain open on main. FREE CONSISTENCY CHECK: over F_2
their theorem must imply our K_8 block-diagonal d=3 statement.

## URGENT U2 — a complete kernel-checked descent induction exists,
char-2 only. The contraction proof isolates exactly why char-0
descent is hard: the cross terms our machinery must control vanish
there by a characteristic-2 accident. READ BEFORE STAFFING the
induction — it supplies the induction's shape (carry cross terms
as explicit error) or documents that naive descent is char-2-only.

## Other findings
- formal-conjectures: NOTHING merged; all five KG PRs (4511, 4610,
  4659, 4661, 4664) open; mo271 has pinged MarioKrenn6240 five
  times, zero responses (Krenn's account otherwise active) => THE
  FC LEDGER IS A LAGGING INDICATOR — do not use answer(sorry) on
  main as the open/closed oracle. #4661 (D<=N-2, integral domains,
  solver-free) got the only human movement (08-18 ping).
- arXiv: the Krenn/Firsching/Tsoukalas/Gajjala/Gu/Chaudhuri
  tensor-algebraic no-go paper is STILL unposted ("in preparation"
  since May) — the largest unbounded external risk; weekly checks
  are the only mitigation.
- YesterdaysLemon/krenn-gu-research: ~60 commits in the window,
  frontier doc 838 -> 1542 lines; global status still UNRESOLVED;
  NO n=8 movement (S3C unchanged); the overlapping holonomy/
  rank-strata nodes (U1/U7B/U7C/U7D) all pre-existing and
  unmoved; new material = a cell-exclusion atlas + a response-
  atlas/deck-selector family (different objects; their "m" is not
  our m); one transfer-valuable NEGATIVE (BO1: bounded-window
  characterisations can be blind). Same combinatorial-explosion
  signature as our W-series; possibly decelerating.
- **Krenn is personally watching the competing repo** (issue #5,
  2026-08-01: "the most serious agentic approach i am aware of")
  and is unaware of ours: our repo has 0 stars/forks/issues/
  external citations after 3 public weeks; theirs got his
  attention within 5 days. Prize page unchanged (n=8 d=3 open,
  EUR 3,000, peer-reviewed publication required). MO 311325
  unchanged (0 answers).
- 21-item NO-CHANGE list verified (incl. AlphaProof nexus outputs
  frozen; benchmark repos scaffolding-only; no new entrant repos).

## Recommended follow-ups
1. Read eqSystem_contract_two_zmod2 before staffing descent.
2. Run the F_2 consistency check on our headline (assigned: L1).
3. Stop treating the FC ledger as the oracle.
4. Weekly arXiv check on the no-go paper.
5. USER DECISION: external visibility (prize needs peer-reviewed
   publication; the competing programme has the prize-giver's
   personal attention, ours has none).
