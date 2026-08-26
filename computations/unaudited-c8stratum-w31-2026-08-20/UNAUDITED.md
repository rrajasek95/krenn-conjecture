# UNAUDITED — W31, the C_8 / empty-clean stratum (DESIGN PHASE)

**Nothing in this directory is a proved claim of the repository.** Everything
here is unaudited probe output plus design documents. No file outside this
directory was written; nothing was committed.

- Pinned HEAD: see `PINNED_HEAD.txt` (`fc988c6a1d565d84ed2bb0f1688d1de03cfed1c4`).
  NOTE: HEAD moved during this lane's read phase (it was
  `561217e85b62be8930066d55d081c3faf316d9a8` at the first read; another lane
  committed mid-session). Every number below was recomputed against the
  pinned HEAD's stored artifacts, which are untracked probe outputs and were
  not affected by the commit.
- Phase: **DESIGN ONLY**. Single process, exact integer arithmetic, no
  floats, no Singular, no finite fields, no detached jobs. Total compute in
  this directory is under six minutes of one core.
- Ledger discipline applied: control manifests asserted at the end of every
  script (item 21); every "cannot" statement is labelled as a search or a
  proof (item 18); no verdict rests on a single characteristic (item 19 — no
  field arithmetic was used at all here).

## Contents

| file | what it is |
| --- | --- |
| `STATEMENT.md` | the exact open statement: what the stratum is, why it escapes the joint residual theorem, what closing it buys |
| `PRIOR-ART.md` | everything already tried on this stratum, and exactly how each attempt ended |
| `ATTACK-PLAN.md` | four routes with targets, pre-launch controls, hazard exposure, compute shape |
| `CENSUS.md` | the exact census that is cheap, and the precise spec for the part that is not |
| `w31_census.py` → `results_census.json` | stratum census + frame-degeneracy, controls C1–C5 |
| `w31_slack.py` → `results_slack.json` | the slack-0 coverage lemma, controls D1–D3 + exact branch and bound |
| `w31_d4.py` → `results_d4.json` | controls D4 (positive) and D5 (scope) for the slack lemma |

## Result produced in this phase

**Lemma W31-1 [probe-proved, exact, unaudited]** — see `STATEMENT.md` §4 and
`results_slack.json`. It is the first structural separation between the
stratum and the family Route A is actually working on, and it is proved by
exhaustive exact computation over a finite space, not by search.
