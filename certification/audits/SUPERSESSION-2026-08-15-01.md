# Audit record — SUPERSESSION-2026-08-15-01

Auditor: hygiene agent H1 (Claude subagent, session
f8396279-dd28-41de-876d-5c03a4d8d65a, 2026-08-15), working directory
`computations/unaudited-hygiene-h1-2026-08-15/` (untracked probe
output; key artifacts: h1_b1_fourth_matching.py,
h1_b1_step5_stepcheck.py, results JSONs).

Finding: the Step-5 paragraph of
`proofs/odd-near-perfect-gadget-obstruction.md` (lines 56-58) is not
a valid proof step; explicit counterexamples to the claimed
parity-class descent exist at N = 8, 16, 24. The THEOREM is
unaffected: two independent committed proofs
(`notes/finite-obstruction.md` §7; `notes/termwise-rank3-cubic-
uniqueness.md` §3.5 B3) are sound (both re-verified by H1), a third
one-line proof is supplied, and the residual-case emptiness is
re-verified exhaustively to N = 20 (893,025 configurations, zero
survivors, matching the committed §3.6 census).

Outcome: PASS for the theorem; FAIL for the paragraph; canonical
file left byte-frozen per pin discipline; correction note at
`notes/2026-08-15-step5-defect-and-repair.md` is the citable repair.
