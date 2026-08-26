# UNAUDITED STRESS TEST — "fusion square = Kruskal with provenance" (2026-08-13)

Pins: HEAD 6426204 at start (moved to 09eed6a mid-run; nothing depends on
it). Note under test: simultaneous-diagonal-flattening-palette-fusion-gate
(1883d99, sha 473cabec...). Exact arithmetic; suite ledger c1c1e7c6...;
passes plain/-O/-I -S. Full details in agent transcript; scripts in this
directory (t1..t4, run_all, RUNLOG).

## Verdict: half-right in form, wrong in force — does NOT advance the program

T1 CONFIRMED, no counterexample exists: 200/200 exact random instances
aligned; exact elimination over Q (516 non-monomial directions, nullspace
{0} every time); COMPLETE exhaustive search over F2/F3/F5 (549,536 pairs,
11 cases) — only palette columns survive. One-line proof found, stronger
than the note: a b^T = U diag(lambda) V^T forces |supp lambda| = 1 with NO
rank hypothesis; C in GL_r upgrades to a permutation. The note's full-rank
hypothesis is REDUNDANT (sound, not sharp) — strengthening opportunity.

T2: the fusion square IS a CP-uniqueness instance and Kruskal's 2r+2 bound
is EXACTLY sharp on it (every non-monomial square sits at budget 7; sharp
criterion k_U+k_V >= 5). Full column rank <=> k-rank = r always (m x r).
Explicit exact (2,2) counterexample constructed at budget 7. No gap in the
note: degenerate palettes are structurally unreachable (T2.7).

T3: the program's hypotheses are FAR PAST the boundary — and it buys
nothing. Decisive control: on the committed counterguard, k-ranks hold
with slack (9 >= 8) and the conclusion is false, because Kruskal's
hypothesis ("two CP decompositions of the same tensor") IS the fusion
square. Any Kruskal route is CIRCULAR: it consumes the square, it cannot
supply it. The missing datum is PROVENANCE (lifting a Schmidt column to an
occurrence/cap channel) — not an identifiability question.

T4: 9 mutation controls, 0 survivors (incl. one that refuted the agent's
own intermediate derivation — corrected to a stronger statement: every
rank-2/rank-2 palette pair admits a full-support rank-one element, 36/36).

## Consequence for the strategy map

The assembly hinge's mathematics is ELEMENTARY and DONE (the note's lemma,
now with a stronger form). The open item there is the provenance lift —
i.e., the same source-typing kernel as everything else. Tensor
identifiability should be dropped from the "needed mathematics" list.
