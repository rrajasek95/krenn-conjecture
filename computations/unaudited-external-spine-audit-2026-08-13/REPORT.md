# External adversarial audit of the 2026-08-12 layer — consolidated report

**Date 2026-08-13 (early). Four independent audit agents, each pinned to its
own git-archive snapshot (HEADs d81ec47 / e5eb1fe / e5eb1fe / current at
run time; every finding re-checked byte-identical or explicitly marked).
All committed checkers reran clean in plain/-O/-I -S with matching frozen
digests — no finding below is a broken checker. This report is itself
external and un-re-audited; treat per repo discipline. Audit scripts in the
session scratchpad (audit-foundations/, audit-mv/, audit-dichotomy/,
audit-combinatorial/ + indep/); this file is the distilled verdict.**

## One-paragraph summary

Everything enumerative or linear-algebraic that the auditors recomputed is
TRUE — several claims were upgraded to exhaustive proofs in the process.
But nearly every promotion from model to physical is currently stipulated,
not verified: checkers hash counts/strings/booleans, hardcoded constants
are consumed as proof steps across files, and the repo's own newest
commits already retracted the strongest closure (scope guard: "Gate-I
assembly now: NO"). No theorem was refuted anywhere. The gap is uniformly
missing-evidence + overclaiming prose, never wrong mathematics — with the
mathematics in several key cases verified true by the auditors directly.

## Verified TRUE by independent re-derivation (not by committed checkers)

- Lambda = Σm_j − ainc kills ALL 8,580 operator columns and ALL 288
  repeated columns (structural reason: 0 of 8,580 operator columns touch
  the six selected features). The committed checker hardcodes these as
  literals; the fact itself is now independently established.
- The 8,580-column operator has literal source output 0 and D1 output 0 —
  genuine cancellation (305 distinct source rows, 481 incidences), and
  8,580 is a real count of distinct columns.
- The O_alpha census: all 5 components × 15 corner choices, 288 columns,
  360-term supports, 75 content-bearing distinct digests — reproduced
  digest-for-digest from raw combinatorics.
- Secondary transfer −delta pinning: forced, unique, mutation-sensitive
  (the one claim whose ledger hashes real mathematical content).
- The sl2 prism toy: every identity reproduced from scratch, extended to
  degree 8, no failure.
- Anchor-fibre dichotomy internal linear algebra: rank exactly 24,
  cokernel nu, all four repair directions — rebuilt independently.
- Determinant-bright entry: proved EXHAUSTIVELY (all 3^15 patterns;
  2,669,328 bright rows; 0 lack a nonzero offdiagonal cell).
- Termination combinatorics 5,141 / 446 / six types: exact, plus
  446 = 448 total Galois-closed sets minus 2 degenerate.
- Shared-loop census: re-derived from the intertwining condition; the four
  equivariant collapses, paired orbits {0,5}/{2,3}, fixed targets 1/4 all
  confirmed.
- Coloop pivot identity: true on an honest complete-row model (200 exact
  trials) — but see FAIL list for what the committed checker verifies.
- Ward identity: TRUE — but structurally near-tautological (holds for any
  forbidden pair and any matching subset; 8,748 rows ≈ 1 statement up to
  manifest symmetry).

## CRITICAL defects (block spine status)

1. **K's physicality is open, and the repo says so elsewhere.** The
   descent checker never loads the 8,580-column operator; it hardcodes the
   three values the M_v composition compares; three files agree because
   the same literal was typed into each. The needed operator-to-physical
   chain map is printed OPEN by verify_h3_order6_endpoint_odd_hpl_
   secondary_transfer.py itself.
2. **D2 = −delta is attainability, not equality.** expected_second_shadow
   is built FROM (−1,+1,+1,−1); on ker(source, D1) the shadow has
   488-dimensional freedom (rank 840 vs 1328). "canonical_on_D1_homology"
   is a hardcoded boolean.
3. **The ridge/terminal (eta_z, sigma) is asserted, never derived.**
   Hardcoded strings compared to themselves; the one "derivation" solves
   backwards from eta/sigma as input; the terminal rows of the M_v
   identity are VACUOUS — an empty terminal packet passes all gates with
   unchanged digest. Hardcoded "…can_tensor_with_ridge_jet": True is
   consumed as a proof step by another file.
4. **x_v is not source-typed** (repo's own scope guard already retracted
   the Gate-I assembly): the six labelwise pure-ores columns are granted,
   not constructed; the generous cone is unsound in the construction
   direction (it must CONTAIN x_v — generosity only safe for excluding).
5. **The (2,3)→(3,3) rank claim's checker computes no rank** (two literals
   compared to themselves; negating the claim leaves a byte-identical
   digest); the 270-case interference identity verifies a partition that
   holds for any edge in any packet.

## HIGH defects

6. nu = −Lambda (lower_B ↔ six private matching rows) is prose resting on
   6 = 6; no computation links the 25-row model to the 8,868-column
   physical matrix (the fact is true — see verified list — but unproved
   in the chain).
7. The prism identity dK+Kd=(1−s)(w−1) is verified on no physical module;
   its content ("H_w exists physically and s is a chain map there") is
   checked nowhere. The endpoint involution check passes for 16 of 28
   transpositions (invariance group S6×S2); the ledger misreports "0<->1"
   after mutation.
8. T and rho exist only as hand-typed 2-row vectors duplicated across two
   files; no literal boundary anywhere; the census half and the sign half
   of the O_alpha claim are never connected.
9. The bordered trichotomy is exhaustive only on one stipulated 3×3;
   corank 1 is essential (factorization fails ~97% of corank-≥2 trials)
   and never established for the physical block. The Schur determinant is
   unimplemented and collapses at corank ≥ 2.
10. "The same pivot works for all six saturated concepts": the checker
    verifies zero of six (string + integer literal; the two audit
    functions never touch each other's data).
11. The 150,930 landing assumes an equivariance the computation refutes
    (three distinct values on one transitive S6 orbit; unstated
    renormalization).

## Wording/scope errors (fix in notes)

- "The 270 form one double-coloop orbit" is impossible (Lagrange); it is
  two orbits 90+180 — the checkers themselves record this.
- 2,126,208 counts (chart, triple) PAIRS; distinct triples = 260,118.
  All restatements dropped the "on any of the nine charts" qualifier.
- 264 four-cell survivors exist on chart (1,3); "the last local monomial
  degree is empty" invites the wrong reading.
- "There is no unclosed linear branch" is true only of the 25-row model.
- "Land ALL determinant-bright mixed rows" is accurate for entry,
  overstated for landing (fan + four-good links unverified; one pinned
  module never loaded).
- "Every new typed hole strictly enlarges the closure" is inflationarity
  (trivially true), not a termination result.

## Systematic issues

- Content-free frozen ledgers throughout the foundations layer (digests
  of counts/strings/booleans; removing every mathematical require from
  the sl2 prism checker leaves its digest unchanged). Exception: the
  −delta chain, which hashes actual content.
- Zero positive/negative controls in any audited checker.
- Self-pinned digests (EXPECTED_LEDGER_SHA256 in the same file as the
  ledger) cannot catch intentional restatement; the pin graph is cyclic.
- Hardcoded booleans consumed cross-file as proof steps (at least three
  instances found).

## Repair list (ordered)

1. Construct the operator-to-physical chain map for K (or demote M_v's
   K-half to conjecture) — this is the repo's own OPEN item and blocks
   everything downstream of M_v.
2. Derive eta/sigma from physical definitions; make the terminal rows of
   the M_v identity non-vacuous (include them in the compared signature).
3. Replace "D2 = −delta" with a canonicity argument on D1-homology or
   state attainability honestly.
4. Construct the six labelwise pure-ores sections (source-type x_v) —
   already tracked by the repo's scope guard.
5. Establish corank 1 for the physical bordered block or generalize the
   bordered theorem.
6. Rebuild the foundations ledgers to hash mathematical content; add
   positive controls; fix the involution check to pin the claimed
   transposition.
7. Repair the orbit-lifting checkers (compute the ranks; verify the
   interference identity's actual coefficients; state the two-orbit
   structure correctly).
8. Verify the six-concept pivot applicability (the mathematics appears
   true — one honest model confirms the identity — so this is checker
   work, not theorem risk).
