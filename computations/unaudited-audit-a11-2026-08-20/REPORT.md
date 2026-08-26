# A11 — audit of W30's post-A10 additions + W36 checks — FINAL (UNAUDITED lane record, 2026-08-20)

PINNED_HEAD 14f53e7. From-scratch engine (a11_lib.py, stdlib, raw
105-matching Phi, own S'/Q/ROWS from the committed spine; zero
w26/w30/a10/w36 imports). Transcribed by the manager.

## VERDICTS
- W30-M25-CONDITIONAL: **CONFIRMED** (90/90 reproduced + 16 new
  points) with FOUR statement corrections: (i) T_c nonempty is a
  needed template fact (letter 0 is no live single's target —
  verified at all 823 choices); (ii) |T_f| = 1 is NOT needed at
  m=25 (152/823 choices have |T_f| = 2 and the rank-1 argument
  covers them); (iii) the zero-scale convention is load-bearing —
  (alpha) is needed twice (P injective AND live choices
  nonempty); (iv) (H1) clean and (H3) off-stratum are NEVER USED
  (implication holds at random non-clean and vanishing-stratum
  points); "=> pure row" is a control, not a step. Template-vs-
  point untriggered sets distinguished (376 vs 1,782 — sound
  sub-system; escape sizes measure the sub-system).
- W30-Z: **CORRECTED** — true, but restate: all-cells-nonzero
  (S'_{t3} != 0) is MISSING (A10's second W30-X fix, not
  inherited; explicit counterexamples otherwise); "S_{t1} not in
  ker phi" is REDUNDANT (implied by non-delivery); the round-3
  blind-test record (124/126, 112/114) is NOT ON DISK and cannot
  be re-traced — do not carry it as evidence (A11's own blind
  test: 115/115 deliver at rank <= 2; the 51/68 line is the
  refuted converse, all 17 exceptions = D2). W30-Z should GOVERN
  with W30-Y as corollary.
- Round-9/10 reductions: common-direction forcing needs an
  unstated COVERAGE condition (with the six-tuple live sets that
  actually occur, A45 is NOT forced rank one — an elimination
  against the round-10 "true target" would not close (beta));
  the 42x126 rank-42 fact is TRIVIAL (pairwise-disjoint row
  supports); the A45-only refutation confirmed. NEW: (A56,A67)
  and (A45,A47) common-line phenomena are the same fact.
- Round-10 "never reached" is STALE: the common-direction pair is
  reached in ALL THREE FIELDS incl. Q — and buys nothing. The
  escape at a common-direction point REDUCES TO A SCALAR SYSTEM:
  A25 rank one (holds), **A07 rank one (FAILS — rank 2 at all
  three points)**, hafL free of x1 (mixed), the scalar Q == 0
  system (fails everywhere; best class completion 7.4%). **The
  reduced scalar system is the successor target for (beta).**
- W36 checks: the shared-letter pigeonhole **CORRECT** (exhaustive
  2,985,984 all-nonzero 3x2 F_13 matrices: 0 both-fail;
  456,192 single-fail so non-vacuous; at n=3 the analogue FAILS
  at 183,176/200,000 — exactly why m=26/27 keep (Q3)). The
  escape object s1073 REAL and re-verified — but it refutes the
  STRONG reading only, NOT hypothesis (beta) (which holds there
  via the y7 != 2 tuples). **THE SUPERSESSION CLAIM IS WRONG:
  W36-M25 and W30-M25-CONDITIONAL are INCOMPARABLE** — (R25)
  fails at 4 of 32 corpus points (incl. 925024 and r10 alpha_13)
  while (beta) fails at 0/32. The right promotion object is the
  DISJUNCTION "(R25) OR ((alpha) and (beta))" — 32/32 coverage.

## Defects found
- W30 r10 builders: the hit test OMITTED the common-direction
  condition (ledger 27 in the success criterion); all five r10
  result files have `_controls_run: []` with ok=True BY FIAT —
  declared controls never executed (ledger-21 violation; see new
  ledger 31).
- `w30_indep.py` and `w36_escobj.py` sample with `[::7]` strides
  while docstrings/labels claim censuses; round 10's "123 Q=0
  words" and W36's word counts are 1-in-7 samples.
- The independent-family points were never stored ("32/33" not
  re-derivable; round 10's most informative exception object is
  LOST); round 7 double-counted 925024.
- A11's own ledger-20 build: 177 new clean points, 0 failures,
  0 escapes — failed search, stated as such.

## Recommendation
PROMOTE the gated §5 with edits: W30-Z restated (all-cells-
nonzero added, redundant hypothesis dropped, converse status
stated) as the GOVERNING lemma, W30-Y as corollary; ONE
disjunctive m=25 lemma "(R25) or ((alpha) and (beta))" with the
four statement corrections; the n=2-vs-n=3 structural note; fix
the strides and store the exception point before quoting counts.
Nothing unconditional is supported; nothing narrows a certified
dependency.
