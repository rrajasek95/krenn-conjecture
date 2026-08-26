# UNAUDITED — audit lane A12 (independent audit of lane W36 round 2)

Nothing in this directory is a proved claim of the repository.

PINNED_HEAD: see `PINNED_HEAD.txt`. A12 was launched against
`1d034de542a62cbaf4fafc2928c9948ab1d650d2` (the v85 commit); the repository
HEAD moved to `fa4124abdc1f9e3d9ada4f5ba08ed032db8499a0`
(`SUPERSESSION-2026-08-20-04` certified) while A12 was running. Both are
recorded; every claim below was checked against the files as they stand at
the later HEAD.

**From-scratch engine.** `a12_lib.py` is standard library only and imports
**nothing** from `w26_core`, `w30_lib`, any `w36_*` module, or any `a11_*`
module. The only input taken from the repository is the 28-entry template
mask table, which is *committed*
(`computations/verify_slice_master_relations.py`, frozen SHA-256
`8b8385c1db6f5f1351558c7432be785b384677e9fdbb58052db44dea41681ab5`) and is
re-typed here and cross-checked against the committed structural census
(Remark 3.2 degrees; the `m = 27` Gamma perfect-matching count `12`).
Everything else — `Phi` by raw 105-matching enumeration, the decomposition
(1), the cofactor hafnians, live singles, clean words, admissible index
choices, the `ROWS` matrix of (M)/(M*), the augmented slice `S'`, the
`DELIVERS` predicate, the point builder — is re-derived here.

W36's, W30's and A11's directories are read **as data only** (stored points
and stored result records). Nothing was written outside this directory and
nothing was committed.

**Arithmetic.** Exact only: `Fraction` over `Q`, `int` mod `p` over `F_p`.
Fields used: `Q`, `F_13`, `F_31` (both primes `= 1 mod 3`).

**Discipline.** Every `results_t*.json` carries `_controls_declared`,
`_controls_run` and a computed `_manifest_ok`; the manifest helper refuses to
emit an `ok` on a block that carries no `executed` marker and raises if a
declared control did not run (ledger 21/31). Every verifier carries a
mutation control that is *shown to fire*. Long runs were detached and
checkpointed (`*.json.part`).

| file | contents |
|---|---|
| `a12_lib.py` | the engine |
| `a12_t0.py` / `results_t0.json` | engine calibration against the committed spine + mutation controls |
| `a12_t1.py` / `results_t1.json` | TARGET 1 (b)(c)(d): template facts, the 3x2 geometry with an exact polynomial certificate, the exhaustive model check of the assembly, load-bearing deletions |
| `a12_t2.py` / `results_t2.json` | TARGET 1 (a)(e)(f): the zero-witness census (no stride), the 42 stored objects, (R25) three ways |
| `a12_t3.py` / `results_t3.json` | TARGET 1 (e): 89 fresh points over `Q`/`F_13`/`F_31` from A12's own generator + adversarial search |
| `a12_t4.py` / `results_t4.json` | TARGET 2 (a)(b)(c): absent columns, full-census ROWS-vs-S' ranks, the transfer matrix `P`, the stored both-rank-3 objects |
| `a12_t5.py` / `results_t5.json` | TARGET 3: manifests, strides, the corrected census, the escape object, the stored exception points |
| `a12_t6.py` / `results_t6.json` | TARGET 2 (d): ROWS-verdict vs S'-verdict, the Gamma path and the `(2,5)` common class |
| `a12_t7.py` / `results_t7.json` | the (R25) count reconciliation, pinned to code |
| `REPORT.md` | verdicts |
