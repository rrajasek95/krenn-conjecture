# Audit record: SUPERSESSION-2026-08-01-03

Dependency: `SP-K6`.

Replacement commit: `4a510193d97fd84cc819912231504711281dbbab`.

Independent auditors:

* `/root/terminal_math_certification_audit` (import and certification audit);
* Claude session `3a596df9-733e-4f60-b63e-dd1c89fd67d9`, subagent
  `agent-aed5ba1e4665adb1d` (independent remediation audit).  The preserved
  source trace is
  `/Users/rishi/.claude/projects/-Users-rishi/3a596df9-733e-4f60-b63e-dd1c89fd67d9/subagents/agent-aed5ba1e4665adb1d.jsonl`.

Outcome: **PASS with certification-metadata corrections; no mathematical
correction and no weakening of Theorem 1.1.**

The audits independently checked the following load-bearing repairs.

1. The `C_3 \sqcup C_3` support formula now includes the zero-or-rank-at-least-two
   alternative directly.  All 134 orbit formulas are UNSAT under both shipped
   solvers, including the zero alternative.  The 56 empty clauses arise only
   when a constant colouring has no basis-compatible perfect matching; an
   independent solver also refuted all 134 formulas after those clauses were
   stripped.
2. The three-term step in the one-slice covering lemma is replaced by an
   evaluation proof.  It uses only that the three coordinate restrictions span
   a space of dimension at least two and that a vector space is not the union
   of two proper subspaces.  The activity conclusion is retained.  It is not
   needed inside `SP-K6`, but other consumers use it.
3. Projection from a palette of size at least three retains possibly unequal
   nonzero diagonal amplitudes.  The replacement includes the missing
   invertible diagonal normalization over `C`.
4. The four-edge minor argument no longer multiplies two zero equations.  It
   compares two equal nonzero products and cancels the already nonzero factor
   `K^2`.
5. The low-rank replay validates mixed-versus-constant fibre semantics and
   performs its checks under `python3 -O`; the translated-trinomial census is
   corrected to the three cases `P3+3P1`, `P2+4P1`, and `6P1`.
6. The saturated checker handles zero blocks explicitly, uses two solver
   backends, and keeps all checks live under optimization.
7. The optional DRUP regeneration command, display delimiters, checker scope,
   and consumer documentation are corrected.

The import auditor ran the slice-cover checker under `python3`, `python3 -O`,
and `python3 -I -S`; all modes passed.  The saturated graph checker passed in
normal and optimized modes, with all 134 two-triangle formulas UNSAT under
Glucose and CaDiCaL.  The import audit stopped a fresh `6P1` low-rank replay
after about sixty seconds and makes no new claim from that partial run.  The
earlier independent remediation audit completed the full replay, independently
checked the finite identities and SAT encodings, and reported no unsound repair.

`SUPERSESSION-2026-08-01-01` did not name the auditor or a permanent report,
used abbreviated commit identifiers, omitted several changed proof artifacts,
and was not linked to a consolidated-spine update.  This record is the
append-only procedural replacement for that incomplete entry.

SHA-256 at the replacement commit:

```text
df823fac7f34538e22a8a82eab590970c4531721bc006be465f26bdda881722f  computations/certify_low_rank_graph_laurent.py
d36291bfe8be3b33700dc2569df9a386bc153870b3cfb11b3d880ccca325a26b  computations/verify_saturated_rank_graph_obstruction.py
1bbfb9212cb66e55731d8a0a124a378ac614c11f08cfe606e4dd44e0014a8992  computations/verify_slice_cover_three_term_step.py
35c40e4d4dd2acda02114c695e7cac116fdbaecba35e2e1b61349eafe6f3848f  notes/final-resolution-foundations-draft.md
762338a618244dba346d87a49e502f5053a80f5be7aef2d787691d4d03c49465  notes/route-registry.md
dd4b99ca9c75c7081682e8de57c9915984395bf642ab4ababb4037711d6ed989  notes/slice-cover.md
e9dee45efb1508273decb21dd7435d153109be3092cbabd075487919806500b1  proofs/exceptional-triangle-obstruction.md
6982d5cb706ecc02c33f67ccba389e98f4a38111b177a7230540dea632c7235d  proofs/four-edge-rank-graph-obstruction.md
97f7f1003f0e5c3f2b68e91a8ad1f514390339c7fcf5327fbfab93ec116db841  proofs/saturated-rank-graph-obstruction.md
0004d49d6216c4d86636de15d59b81309c1a0080b8dc427298c2eba65f83f244  proofs/six-site-arbitrary-complex-obstruction.md
```
