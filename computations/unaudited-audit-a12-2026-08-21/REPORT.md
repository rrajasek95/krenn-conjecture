# A12 — audit of W36 round 2 (W36-M25-FULL + the m=28 retraction) — FINAL
(UNAUDITED lane record; transcribed by the outgoing manager at
handoff. Full detail in results_t0..t7.json. Engine from scratch,
zero lane imports; fields Q/F_13/F_31.)

## VERDICTS
1. **THEOREM W36-M25-FULL: CONFIRMED — and PROVED, not merely
   evidenced**: (a) zero-witness lemma re-derived + stride-free
   census (6,912 dead choices / 12,216 clean-letter relations /
   5,304 minor checks — 0 bad anywhere); (b) closure lemma
   confirmed with its load-bearing negative direction; (c) the
   case analysis verified by EXHAUSTIVE MODEL CHECK — all 5^9
   per-tuple slice states x all liveness assignments on the 57
   relevant L-parts, seeking "fails yet a choice survives":
   UNSAT (an over-approximation of the real point set, so UNSAT
   proves the assembly); all four template facts load-bearing
   (each deletion makes it SAT); a SHORTER proof extracted;
   (d) the matrix steps reproduced third-engine, and the
   field-independence justification CORRECTED — the honest
   certificate is a polynomial identity over Z (two vanishing
   minors sharing a nonzero row force the third over any integral
   domain); (e) 42/42 stored + 89/89 fresh independent points, 0
   violations. Refinements: (H1) needed only at the T_c-completion
   words; (H2) at only 7 of 13 blocks. RESIDUAL stands: n_idx = 0
   unexcluded (needs hafL = 0 on all 57 L-parts; extreme observed
   36/57).
2. **(R25) DISCREPANCY ADJUDICATED: W36 right, A11 wrong** — the
   two definitions are THE SAME PREDICATE (0 disagreements);
   counts differ only by corpus (1/11 on A11's, 2/42 on W36's);
   **A11's "4/32" is supported by NO artifact** and has propagated
   into master-plan v81 AND the committed
   proofs/slice-master-relations.md §5.2 Remark 5.8 ("4/32",
   "28/32"), where it contradicts that document's own step-7
   checker record ("(R25) failures 1"). CORRECTION REQUIRED to
   committed spine (via the supersession discipline).
3. **The m=28 retraction: CONFIRMED and sharpened** — the slice
   criterion returns the OPPOSITE verdict on exactly the targeted
   objects (3,132 verdict disagreements at 4 objects; 0/13,539 at
   m=25-27). Root cause CORRECTED to ONE-WAY: transfer valid iff
   P injective (measured 100% at 25-27, 0% at 28); the absent
   column removes the GUARANTEE (ranks still agree 82-94% at
   m=28) — the v85 biconditional phrasing is wrong. "Eleven
   objects" was an unfinished-sweep snapshot: the completed
   prelaunch records **816**. W36's quoted mismatch numbers were
   1-in-17 stride samples; true full-census figures:
   652/54,348 (R5), 1,437/63,483 (R6), 502/63,399 (L1),
   1,416/54,208 (L2). Protected set = {two firing letters} AND
   {>= 1 absent column} (W36's table omitted m27/R6 and m25/L2
   as two-firing zero-absent). The (2,5) silence confirmed.
4. **A11-corrections implementation: PARTIAL** — the exact
   ledger-31 pattern is gone, BUT `_manifest_ok = True` is
   written as a LITERAL at w36_elim.py:312/:400 and
   w36_escobj.py:191 (in results_elim_prelaunch.json it is FALSE
   — 3 of 6 declared controls never ran, and that is the file
   the retraction cites); w36_m28fix.py still strides
   [::17]/[::11] (the v85-quoted numbers); six abandoned result
   files carry declared-never-run controls (not citable). One
   W36 control defect found: F5_negctl's mutation never fired
   yet reported ok (predicate mismatch) — replaced by A12 with
   must-fire mutations (12/12).

## RECOMMENDATION (for the successor/Codex)
Promote **W36-M25-FULL as the -05 m=25 object, superseding the
disjunctive Lemma 5.6**, with seven required edits: keep the
n_idx=0 residual in the statement; replace the (p-1)^3 field
argument with the integral-domain polynomial certificate;
CORRECT the committed Remark 5.8 (1/11 and 2/42, not 4/32);
any retained (R25) must say "two surviving |T_f| = 1" (a
counterexample to the loose reading exists); m=26/27 untouched;
never quote the strided m=28 numbers or "eleven objects" (use
the full-census figures and 816); re-run w36_m28fix.py
stride-free and fix the three by-fiat _manifest_ok sites before
citing m=28 again. Nothing here narrows a certified dependency;
the promotable object is one delivery lemma at one vertex of one
support.
