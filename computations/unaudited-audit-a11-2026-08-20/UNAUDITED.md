# UNAUDITED — audit lane A11 (2026-08-20)

**Nothing in this directory is a proved claim of the repository.** It is the
working record of an independent adversarial audit of lane W30's post-A10
additions (THEOREM W30-M25-CONDITIONAL, THEOREM W30-Z, the round-9/10
reductions, and the live round-10 builder data).

* Pinned repository HEAD: see `PINNED_HEAD.txt`
  (`14f53e79f56596d4403b9f19310158c44e6f5140`).
* Lane W30 pinned HEAD: `021b1a307e8edb10b964fadefd4b823bdb589035`
  (`computations/unaudited-exclusion-w30-2026-08-19/`).
* Audit A10 pinned HEAD: `f9a3bd6b93417a43d86ad782d1f76b62f14bc50a`.
* Committed spine consumed: `proofs/slice-master-relations.md`
  (dependency `SLICE-MASTER`, `SUPERSESSION-2026-08-20-02`); §5 is GATED and
  its promotion is what this audit reports on.

## Engine independence

`a11_lib.py` is written from scratch, standard library only, and imports
**nothing** from `w26_*`, `w30_*` or `a10_*`. It re-derives every structural
fact from the nine 28-entry template masks (combinatorial data, embedded and
re-checked against the recorded census), computes `Phi` by RAW enumeration of
the 105 perfect matchings of `K_8`, and builds the master relation, the
augmented slice matrix `S'`, the cofactor vector `Q` and the `FAIL_primary`
delivery predicate from the committed spine's statements only. Stored point
corpora are read as JSON DATA, never as code.

Exact arithmetic only: `Fraction` over `Q`, and `F_13` / `F_31` (both
`= 1 mod 3`, ledger 19).

## Files

| file | what it does | output |
|---|---|---|
| `a11_lib.py` | the engine | — |
| `a11_m25.py` | m=25/R6 machinery, closed forms, my own clean-variety walk | — |
| `a11_t0.py` | engine self-test: census, `Phi` two routes, (M), (C), MUT-A/B, wrong-slice negative control | `results_t0.json` |
| `a11_t1.py` | TARGET 1 proof chain (a)-(d) + hidden-hypothesis audit | `results_t1.json` |
| `a11_t2.py` | TARGET 1 verification record recomputed (Q family + A11 walk family) | `results_t2.json` |
| `a11_t3.py` | TARGET 2: W30-Z, side conditions, own blind test | `results_t3.json` |
| `a11_t4.py` | TARGETS 3/4: round-9/10 reductions, live r10 points | `results_t4.json` |
| `a11_t5.py` | engine cross-check vs stored verdicts, point-level escape, residual gap | `results_t5.json` |
| `a11_t6.py` | pure-row step, converse traces, escape fractions | `results_t6.json` |
| `a11_t7.py` | hypothesis-necessity ((H1)/(H3) inert), realisation census | `results_t7.json` |
| `a11_t8.py` | ledger-20 adversarial builder against the theorem | `results_t8_p*.json` |
| `a11_t9.py` | the (beta) escape reduced to seven requirements, measured at the live round-10 points | `results_t9.json` |
| `a11_t10.py` | addendum: W36-M25's shared-letter pigeonhole; the (beta) escape object in W30's own hunt output; the supersession question | `results_t10.json` |

Every result file carries a declared control manifest that is asserted before
the file is written (`a11_lib.Manifest`, ledger 21).

## Discipline

Hazards ledger items 1-27 binding; in particular 13/18/19/21/24/25/27.
No writes outside this directory; no commits.
