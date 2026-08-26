# W12 — thick-fibre regime — REPORT (UNAUDITED, 2026-08-15)

Pinned HEAD 0fedca2. Exact arithmetic (int/Fraction, Singular over Q)
for every verdict; one labelled float search carries no verdict.
Agent's write was policy-blocked; this transcribes its delivered
report. 16 modules, 14 JSONs, 4 Singular scripts here.

## HEADLINE: THE THICK-FIBRE REGIME IS NOT IMMUNE.
The mechanism the lattice engine cannot see: CUTTING the site set in
half turns thick fibres into binomial half-fibres. Thickness is not
preserved by cutting — W8's immunity proposition governs fibres of
the whole B; the cut produces 4-site sub-problems that are binomial
regardless.

## Kills (130/130 of everything known at N=8; no escalation anywhere)
- m=20 CEGAR survivor (Sigma=58): KILLED, 3 independent routes,
  incl. an EIGHT-WORD HAND CERTIFICATE (three fibre-proportionality
  pairs force lambda; F(0^8) = lambda F(00000020) = 0 contradicts
  the constant word; Singular confirms; each of the 7 mixed words
  load-bearing). Mechanism named: two fibre polynomials proportional
  modulo the binomial relations, one mixed + one constant — W8's
  engine compares monomials inside one fibre, never across two.
- Immune construction m=20,21: THREE-LINE KILL (crossing-parity =>
  fibres factor as F^L * F^R on clean words; constants give both
  halves nonzero; mixed word 0^4 1^4 gives their product = 0).
  m=22,23: killed by cut extraction. m=24..28: UNDECIDED (see
  residual).
- All 47 W11 witnesses (m=16..28): killed < 1 s each.
- All 77 W8 m=17 classes: killed independently (positive control).

## Uniform theorems (general even N; candidates for audit promotion)
- W12-A (split kill): if for colours c != c' the words c^B, c'^B,
  c^L c'^R each have pairwise-intersecting active crossing edges,
  no exact source exists (crossing-parity factorisation).
- W12-B (cut extraction, MAIN TOOL): pinned left sub-words (unique
  supported matching, or clean constant) force F^R_y = 0 for every
  clean mixed completion — a value system on |R|=4 sites whose
  fibres have <= 3 terms (binomial regardless of B-thickness).
- W12-C (exact structural boundary): a feasible cut exists iff
  Gamma(T) — the graph of FULL nine-cell blocks — is NOT a spanning
  2-connected subgraph. Verified on 4,000 random graphs, 0
  violations; over 135 targets the predicate coincides with the
  outcome exactly (130 killed; 5 failures = immunity m>=24).
- W12-D (residual price): the residual has m >= |Gamma| + 12 >= 20
  and Sigma >= 9|Gamma| + 12 >= 84; if |Gamma| = 8 then Gamma = C_8
  (2 PMs) and the lattice engine re-enters.

## MINIMISED RESIDUAL (R) — the last open object at N=8
(SC)-admissible zero-singleton template, all mixed fibres >= 3,
Gamma(T) spanning 2-connected. Then m >= 20, Sigma >= 84, no
binomial relations at any cut. W8's immune family at m = 24..28 is
the ONLY known instance. Partial structure derived (single-cells-
inactive words give binomials in half-permanents: forces P_L, P_R
nonzero, rank A07 = rank A14 = 1, P_L = -kappa G H A23); the
residual identity has explicit all-nonzero solutions — honest
blocker, not a near-miss. W13's taxonomy is the natural instrument
(all residual pairs are multi-cell full-rank — its hypothesis
verbatim).

## Controls
Fibre engine matches W8 exactly (survivor histogram + 9/9 immunity
templates); mutation controls 58/58 + 168/168; reduction round-trips
0 mismatches; DECISIVE NEGATIVE CONTROL: the committed near-exact
source's template is itself thick and mixed-exact — the cut engine
extracts 12 equations + 229 non-vanishings and the source violates
NONE (and its own point solves the reduced system, so no false
"unit ideal" is possible there); discriminating-checker control (one
of 58 single-cell deletions yields no-kill). Free filters over 135
targets: (SC+) fails on 21; J.1d budget 0 failures (W11's guess
confirmed).

## Side observation (exact statement + float evidence, no verdict)
TWO-COLOUR RESTRICTION (exact, apparently unrecorded): an exact d=3
source restricts, for any colour pair, to an exact d=2 source on the
SAME sites. So "no d=2 at N" would imply "no d=3 at N" — but
validated float searches find d=2 sources at N=4,6,8 (residuals
~1e-15; harness control fails on a provably impossible instance), so
the lever does not close N=8; it explains why d >= 3 is essential.

## Soft spots
m=24..28 genuinely undecided (structural, not budget); W12-B kill
step only as strong as the half-system decision (3 of 4 verdicts
combinatorial; Singular timeout => undecided, never killed);
reduction soundness rests on divisibility of C* (stated for
auditors); elementary-divisor > 1 branch untested (never occurred);
(SC)/(SC+)/constant-witness inputs inherited (the §2/§3.1 kills use
NONE of them — only cells nonzero + mixed vanish + constants not);
the 130/130 is about KNOWN templates + the Gamma predicate, not an
exhaustive sweep of the thick regime.

## Recommendations
(1) Cut extraction into the standard screen FIRST (sub-second,
beat 900 s Groebner timeouts). (2) Attack (R) via W13 taxonomy /
half-permanent system. (3) Decide d=2 at N=8 exactly (low priority).
(4) Promote W12-A/B/C to the audited layer.
