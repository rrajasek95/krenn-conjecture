# UNAUDITED — audit lane A10 (2026-08-20)

**NOTHING IN THIS DIRECTORY IS A PROVED CLAIM OF THE REPOSITORY.**
This is an independent adversarial audit of probe lane W30 (and, where
W30 depends on it, of W26's failure predicate). It is itself unaudited.

- Pinned HEAD of this lane: `f9a3bd6b93417a43d86ad782d1f76b62f14bc50a`
  (see `PINNED_HEAD.txt`).
- W30's pinned HEAD: `021b1a3`.  W26's pinned HEAD: `dee2ca3`.
- Exact arithmetic only (`int` mod p / `fractions.Fraction`). No floats.
- `a10_lib.py` imports NOTHING from `w26_*` or `w30_*`.  The engine, the
  105-matching enumeration, the template combinatorics, the clean-word
  set, the slice rows, the admissible-index enumeration and the rank
  routines are written from scratch from the model definition and from
  A10's own hand re-derivation of the master relation.
- The only things taken from W30/W26 are **data**: stored block matrices
  (`results_verify_hunt.json`, `points_*.json`, `results_escverify.json`,
  `results_qspan_*.json`) and the nine template masks, the latter
  independently corroborated against eight other lanes.
- No file outside this directory was written. No commits were made.

## Files
| file | what |
|---|---|
| `a10_lib.py` | the independent engine (+ the hand derivation, in the docstring) |
| `a10_smoke.py` / `results_smoke.json` | engine self-test + structure recount |
| `a10_t1.py` / `results_t1.json` | TARGET 1 — the m=28 refutation |
| `a10_t2.py` / `results_t2.json` | TARGET 2 — Theorem W30-X, steps (1)(2)(3) |
| `a10_t3.py` / `results_t3.json` | TARGET 3 — the sampling artifact |
| `a10_t4.py` / `results_t4.json` | TARGET 2-EXT — Theorem W30-Y + the escape object |
| `a10_t5.py` / `results_t5.json` | the m=28/L2 Q-span-law exception |
| `a10_mut.py` / `results_mut.json` | targeted mutation control on the co-failure verdict |
| `a10_build.py` / `results_build.json` | independent clean-point builder (ledger-20 adversarial control) |

The verdict itself was returned to the manager as A10's final message
(this lane writes no report file); the JSONs and `log_*.txt` here are its
evidence.

Every control script ends by asserting its executed-controls manifest
against its declared list (ledger 21).
