> **UNAUDITED — H1 blocker-4 portability scan.**

Static scan only. No script was executed; every verdict below comes from
reading source. Produced 2026-08-15 by an H1 sub-auditor.

**Path convention:** every path in the tables is **repo-root-relative**, with
repo root = `/Users/rishi/workplace/krenn-conjecture`. So
`computations/unaudited-thickfibre-w12-2026-08-15/w12_core.py` means
`/Users/rishi/workplace/krenn-conjecture/computations/unaudited-thickfibre-w12-2026-08-15/w12_core.py`.

**Scope:** the nine promotion drafts in
`computations/unaudited-promotion-drafts-2026-08-15/`. Every backticked path
and every "Certificates and checkers" table row was extracted; bare basenames
(e.g. `chk09_controls.py`) were resolved against the lane named in the same
table block — all of them resolved uniquely. **83 distinct cited `.py`/`.sing`
artifacts** were found; **all 83 exist on disk** (see §5 for the cited
non-script artifacts that do not).

## 0. Debt codes

| code | meaning |
|---|---|
| **D1** | hard-coded absolute path literal in the source (`/Users/rishi/...`) |
| **D2** | `sys.path` manipulation, cross-lane import, or self-directory hack |
| **D3** | cwd dependence: bare relative filename read/written, or import that only resolves when cwd is the script's own directory |
| **D4** | Singular guard status — (i) `zzg*` prefix / no-shadowing guard, (ii) stdout `?`-line parsing, (iii) `LIB "elim.lib";`, (iv) `list L = sat(I,J); ideal S = L[1];`, (v) explicit-point control |
| **D5** | bare `assert` count (vanishes under `python3 -O`) / third-party imports (blocks `python3 -I -S`) |
| **D6** | cited but absent from disk |

D2 sub-codes used in the tables:

* `ABS` — `sys.path.insert(0, "/Users/rishi/...")`, a hard-coded absolute lane path (also a D1);
* `SELF` — `sys.path.insert(0, __file__.rsplit("/",1)[0])` or `os.path.dirname(os.path.abspath(__file__))` (portable within the repo, but a self-directory hack);
* `CWD` — `sys.path.insert(0, '.')` (only works from the lane directory);
* `XLANE(...)` — reaches into a *different* `computations/unaudited-*` lane, named in parentheses;
* `none` — no `sys.path` code; sibling imports supplied by the caller (module) or by cwd (see D3).

`n/a` in D4 means the script neither spawns Singular nor writes/uses a `.sing` file.

## 1. Per-draft tables

### 1.1 `draft_Lh_law.md` (A5 audit + W13 lane)

| script | D1 abs-path | D2 cross-lane import | D3 cwd-dependent | D4 singular-guard | D5 assert / 3rd-party | D6 |
|---|---|---|---|---|---|---|
| `computations/unaudited-audit-a5-w13-2026-08-15/a5_core.py` | no | none | no | n/a | **8 asserts** / numpy | present |
| `computations/unaudited-audit-a5-w13-2026-08-15/a5_h4_indep.py` | **YES** | ABS (self lane) | **YES** — `open("results_h4_indep.json","w")` | n/a | 0 / — | present |
| `computations/unaudited-audit-a5-w13-2026-08-15/a5_t1_controls.py` | **YES** | ABS (self lane) | no | n/a | **1** / — | present |
| `computations/unaudited-audit-a5-w13-2026-08-15/a5_t1_expansion.py` | **YES ×3** (incl. the JSON write path) | ABS + **XLANE(unaudited-induction-w13-2026-08-15)** — imports `w13_core` | no | n/a | 0 / — | present |
| `computations/unaudited-audit-a5-w13-2026-08-15/a5_t2_law.py` | **YES** (`OUT = "/Users/rishi/..."`) | ABS (self lane) | no | n/a | 0 / — | present |
| `computations/unaudited-audit-a5-w13-2026-08-15/a5_t3_h4.py` | **YES** (`OUT`) | ABS (self lane) | no | n/a | **2** / numpy | present |
| `computations/unaudited-audit-a5-w13-2026-08-15/a5_t4_hunt.py` | **YES** (`OUT`) | ABS (self lane) | no | n/a | 0 / — | present |
| `computations/unaudited-audit-a5-w13-2026-08-15/a5_t4_refutation.py` | **YES** (`OUT`) | ABS (self lane) | no | n/a | **2** / — | present |
| `computations/unaudited-audit-a5-w13-2026-08-15/a5_t4_taxonomy.py` | **YES** (`OUT`) | ABS (self lane) | no | n/a | **2** / — | present |
| `computations/unaudited-audit-a5-w13-2026-08-15/a5_t57_apolarity.py` | **YES** (`OUT`) | ABS (self lane) | no | n/a | 0 / — | present |
| `computations/unaudited-audit-a5-w13-2026-08-15/a5_t5_apolarity_fixed.py` | **YES** (`OUT`) | ABS (self lane) | no | n/a | **1** / — | present |
| `computations/unaudited-audit-a5-w13-2026-08-15/a5_t8_transfer.py` | **YES** (`OUT`) | ABS (self lane) | no | n/a | **2** / numpy | present |
| `computations/unaudited-audit-a5-w13-2026-08-15/a5_final_checks.py` | **YES** (`OUT`) | ABS (self lane) | no | n/a | 0 / — | present |
| `computations/unaudited-induction-w13-2026-08-15/w13_core.py` | no | none (module) | no | n/a | 0, has raising `require()` | present |
| `computations/unaudited-induction-w13-2026-08-15/w13_task1_iff.py` | no | SELF (`__file__.rsplit`) | no | n/a | 0 / — | present |
| `computations/unaudited-induction-w13-2026-08-15/w13_task1_law.py` | no | SELF | no | n/a | 0 / numpy | present |
| `computations/unaudited-induction-w13-2026-08-15/w13_task1_h5.py` | no | SELF | no | n/a | 0 / — | present |
| `computations/unaudited-induction-w13-2026-08-15/w13_task1_taxonomy.py` | no | SELF | no | n/a | 0 / — | present |
| `computations/unaudited-induction-w13-2026-08-15/w13_task3_transfer.py` | no | **CWD** (`sys.path.insert(0,'.')`) | **YES ×2** — imports `w13_core` only via `'.'`, and `open('results_task3_transfer.json','w')` | n/a | 0 / — | present |

### 1.2 `draft_cut_mechanism.md` (W12 lane + A4 audit)

| script | D1 abs-path | D2 cross-lane import | D3 cwd-dependent | D4 singular-guard | D5 assert / 3rd-party | D6 |
|---|---|---|---|---|---|---|
| `computations/unaudited-thickfibre-w12-2026-08-15/w12_core.py` | no | none (module) | no | **(i) ABSENT (ii) ABSENT (iii) ABSENT (iv) n/a — no `sat` (v) ABSENT** | 0, has raising `require()` | present |
| `computations/unaudited-thickfibre-w12-2026-08-15/w12_split.py` | no | none (module; caller supplies path) | no (module) | n/a | **1** / — | present |
| `computations/unaudited-thickfibre-w12-2026-08-15/w12_cut.py` | no | none (module) | no (module) | n/a | 0 / — | present |
| `computations/unaudited-thickfibre-w12-2026-08-15/w12_cutdecide.py` | no | none (module; imports `w12_reduce`, `w12_torus`) | no (module) | inherits `w12_core.run_singular` → **(i)–(v) all ABSENT except none** | 0 / — | present |
| `computations/unaudited-thickfibre-w12-2026-08-15/run_t2_split.py` | no | SELF | no | n/a | 0 / — | present |
| `computations/unaudited-thickfibre-w12-2026-08-15/run_t3_cut.py` | no | SELF | no | via `w12_core` — see above | 0 / — | present |
| `computations/unaudited-thickfibre-w12-2026-08-15/run_t7_filters.py` | no | SELF | no | n/a | 0 / — | present |
| `computations/unaudited-thickfibre-w12-2026-08-15/run_t9_propcheck.py` | no | SELF | no | n/a | 0 / — | present |
| `computations/unaudited-thickfibre-w12-2026-08-15/run_t4_controls.py` | no | SELF + **XLANE(w9 cell-ceiling, w6 bridge, p1 witness-splitting)**, paths derived from `__file__` | no | n/a | 0 / — | present (its **output JSON is not** — see §5) |
| `computations/unaudited-thickfibre-w12-2026-08-15/run_t8_soundness.py` | no | SELF + **XLANE(w9, w6, p1)**, `__file__`-derived | no | n/a | 0 / — | present (its **output JSON is not** — see §5) |
| `computations/unaudited-audit-a4-w12w10-2026-08-15/a4_cut.py` | no | none (module, imports `a4_engine`) | no (module) | (i) ABSENT (ii) **PRESENT** (substring `"?" in stdout`, not line-anchored) (iii) ABSENT (iv) n/a — no `sat` (v) ABSENT | **3** / — | present |
| `computations/unaudited-audit-a4-w12w10-2026-08-15/chk03_split_theorem.py` | no | SELF + reads W8 lane JSON (`__file__`-derived) | no | n/a | 0 / — | present |
| `computations/unaudited-audit-a4-w12w10-2026-08-15/chk04_cut_extraction.py` | no | SELF + reads W8 lane JSON | no | n/a | 0 / — | present |
| `computations/unaudited-audit-a4-w12w10-2026-08-15/chk05_gamma_boundary.py` | no | SELF + reads W8/W11/W12 lane JSON | no | n/a | **2** / — | present |
| `computations/unaudited-audit-a4-w12w10-2026-08-15/chk06_reduction_and_negative_control.py` | no | SELF + **XLANE imports `w12_cutdecide`, `w12_reduce`, `w12_torus` from unaudited-thickfibre-w12** + imports `verify_n8_d2_kill_and_monochrome_rigidity` from `computations/` | no | n/a (Singular reached indirectly through the imported W12 modules) | 0 / — | present |
| `computations/unaudited-audit-a4-w12w10-2026-08-15/chk09_controls.py` | no | SELF + **XLANE imports `w12_core`, `w12_cut`** + `computations/verify_n8_d2_...` | no | n/a (same indirect exposure) | **1** / — | present |

### 1.3 `draft_evaluation_principle.md` (A6 B-side + W14 lane)

| script | D1 abs-path | D2 cross-lane import | D3 cwd-dependent | D4 singular-guard | D5 assert / 3rd-party | D6 |
|---|---|---|---|---|---|---|
| `computations/unaudited-audit-a6-w15w14-2026-08-15/a6_bcore.py` | no | none (module) | not itself, but it is only importable via cwd — every `a6_B*` runner below reaches it that way | n/a | **2** / — | present |
| `computations/unaudited-audit-a6-w15w14-2026-08-15/a6_B6_directness.py` | no | **none** — bare `import a6_bcore` | **YES ×2** — import needs cwd = lane; `open("results_B6_directness.json","w")` | n/a | 0 / — | present |
| `computations/unaudited-audit-a6-w15w14-2026-08-15/a6_B6b_keylemma_h5.py` | no | none | **YES ×2** (`results_B6b_keylemma.json`) | n/a | 0 / **numpy** | present |
| `computations/unaudited-audit-a6-w15w14-2026-08-15/a6_B6c_proof.py` | no | none | **YES ×2** (`results_B6c_proof.json`) | n/a | 0 / — | present |
| `computations/unaudited-audit-a6-w15w14-2026-08-15/a6_B6d_apolarity.py` | no | none | **YES ×2** (`results_B6d_apolarity.json`) | n/a | 0 / — | present |
| `computations/unaudited-audit-a6-w15w14-2026-08-15/a6_B7_evaluation.py` | no | none | **YES ×2** (`results_B7_evaluation.json`) | n/a | 0 / — | present |
| `computations/unaudited-audit-a6-w15w14-2026-08-15/a6_B7b_h4regime.py` | no | none | **YES ×2** (`results_B7b_h4regime.json`) | n/a | 0 / — | present |
| `computations/unaudited-audit-a6-w15w14-2026-08-15/a6_B8_hafnian.py` | no | none | **YES ×2** (`results_B8_hafnian.json`) | n/a | 0 / — | present |
| `computations/unaudited-audit-a6-w15w14-2026-08-15/b9_core.py` | no | none (module) | no | **(i) ABSENT (ii) ABSENT — returncode-only (iii) ABSENT (iv) n/a (v) ABSENT** | **2** / **numpy** | present |
| `computations/unaudited-audit-a6-w15w14-2026-08-15/b9_c1_detlaw.py` | **YES ×2** (`HERE` + `sys.path`) | ABS (self lane) | no | inherits `b9_core` — (ii) ABSENT | 0 / — | present |
| `computations/unaudited-audit-a6-w15w14-2026-08-15/b9_c2_phi.py` | **YES ×2** | ABS (self lane) | no | inherits `b9_core` — (ii) ABSENT | 0 / — | present |
| `computations/unaudited-audit-a6-w15w14-2026-08-15/b9_c2_symbolic.py` | **YES ×2** | ABS (self lane) | no | n/a | 0 / — | present |
| `computations/unaudited-audit-a6-w15w14-2026-08-15/b10_summary.py` | **YES ×3** (`HERE`, `W14`, `P2` all `/Users/rishi/...`) | ABS reads of the W14 lane and `unaudited-witness-splitting-p2` | no | n/a | 0 / — | present |
| `computations/unaudited-monochrome-w14-2026-08-15/w14_core.py` | no | none (module) | no | n/a | 0, has raising `require()` | present |
| `computations/unaudited-monochrome-w14-2026-08-15/w14_task1_h4.py` | no | SELF | no | n/a | 0 / — | present |
| `computations/unaudited-monochrome-w14-2026-08-15/w14_task1_h4b.py` | no | SELF | no | n/a | 0 / — | present |
| `computations/unaudited-monochrome-w14-2026-08-15/w14_task1_transfer.py` | no | SELF | no | n/a | 0 / — | present |
| `computations/unaudited-monochrome-w14-2026-08-15/w14_task2_layers.py` | no | SELF | no | **(i) ABSENT (ii) ABSENT — returncode-only (iii) ABSENT (iv) n/a (v) ABSENT** | 0 / — | present |

`b9_c2_phi.py`, `b9_c2_symbolic.py` and `b9_c1_detlaw.py` are the "Certificates
and checkers" entries for the C1/C2 replications; all three carry a hard-coded
`/Users/rishi` `HERE`.

### 1.4 `draft_fourth_matching.md` (A3 lane)

| script | D1 abs-path | D2 cross-lane import | D3 cwd-dependent | D4 singular-guard | D5 assert / 3rd-party | D6 |
|---|---|---|---|---|---|---|
| `computations/unaudited-uniform-n-a3-2026-08-15/a3_core.py` | no | none (module) | no | n/a | **1** / — | present |
| `computations/unaudited-uniform-n-a3-2026-08-15/a3_task2_floor.py` | no | SELF (`__file__.rsplit("/",1)[0]`, POSIX-only) | no | n/a | **1** / — | present |

Note (not a portability debt but an encoding hazard in the same file):
`a3_core.py:183-184` declares and tests an identifier `allе` whose third
character is **Cyrillic `е` (U+0435)**, not Latin `e`. The file parses, but the
name is untypeable and grep-invisible.

### 1.5 `draft_gauge_lemma.md` (W10 lane + A4 audit)

| script | D1 abs-path | D2 cross-lane import | D3 cwd-dependent | D4 singular-guard | D5 assert / 3rd-party | D6 |
|---|---|---|---|---|---|---|
| `computations/unaudited-mixed-exact-pure-cancellation-w10-2026-08-15/w10_core.py` | no | none (module) | no | n/a | 0, has raising `require()` | present |
| `computations/unaudited-mixed-exact-pure-cancellation-w10-2026-08-15/run_a_gauge_and_crosscheck.py` | no | SELF + **XLANE(unaudited-bridge-w6, unaudited-cell-ceiling-w9)** — imports `w6_core`, `w9_template`; paths `__file__`-derived | no | n/a | 0 / — | present |
| `computations/unaudited-mixed-exact-pure-cancellation-w10-2026-08-15/run_j_sc_gauge.py` | no | SELF + **XLANE(unaudited-template-kill-w8)** — imports `w8_core` | no | n/a | 0 / — | present |
| `computations/unaudited-audit-a4-w12w10-2026-08-15/chk07_w10G_gauge.py` | no | SELF | no | n/a | **15 asserts** (highest in the cited set) / — | present |
| `computations/unaudited-audit-a4-w12w10-2026-08-15/chk08_w10_corollaries.py` | no | SELF + reads W10 lane JSON and a `proofs/*.md` file (`__file__`-derived) | no | n/a | **3** / — | present |

### 1.6 `draft_m20_certificate.md` (W12 lane + A4 audit)

| script | D1 abs-path | D2 cross-lane import | D3 cwd-dependent | D4 singular-guard | D5 assert / 3rd-party | D6 |
|---|---|---|---|---|---|---|
| `computations/unaudited-thickfibre-w12-2026-08-15/w12_core.py` | no | none (module) | no | **(i) ABSENT (ii) ABSENT (iii) ABSENT (iv) n/a (v) ABSENT** | 0, `require()` | present |
| `computations/unaudited-thickfibre-w12-2026-08-15/run_t1a_survivor_analysis.py` | no | SELF | no | n/a | 0 / — | present |
| `computations/unaudited-thickfibre-w12-2026-08-15/run_t1c_survivor_groebner.py` | no | SELF | no | via `w12_core.run_singular` — **(ii) ABSENT**; writes `survivor_full.sing`, `survivor_mixed_only.sing` (HERE-joined) | 0 / — | present |
| `computations/unaudited-thickfibre-w12-2026-08-15/run_t1d_certificate.py` | no | SELF | no | via `w12_core.run_singular` — **(i) ABSENT (ii) ABSENT (iii) ABSENT (iv) n/a (v) ABSENT**; writes `survivor_certificate.sing` | **1** / — | present |
| `computations/unaudited-thickfibre-w12-2026-08-15/run_t3_cut.py` | no | SELF | no | via `w12_core` | 0 / — | present |
| `computations/unaudited-thickfibre-w12-2026-08-15/run_t4_calibration.py` | no | SELF + reads W8 lane JSON | no | n/a | 0 / — | present |
| `computations/unaudited-thickfibre-w12-2026-08-15/run_t8b_mutation.py` | no | SELF + **XLANE(w9, w6, p1)** | no | n/a | 0 / — | present |
| `computations/unaudited-audit-a4-w12w10-2026-08-15/chk01_engine_and_certificate.py` | no | SELF + reads W8 lane JSON | no | n/a | **10 asserts** / — | present |
| `computations/unaudited-audit-a4-w12w10-2026-08-15/chk02_certificate_singular_and_mutations.py` | no | SELF + reads W8 lane JSON | no | **(i) ABSENT (ii) PRESENT (iii) PRESENT `LIB "elim.lib";` (iv) PRESENT `list SL=sat(I,pr); ideal S=SL[1];` (v) ABSENT** — best of the cited Singular users | **2** / — | present |

### 1.7 `draft_m24_certificate.md` (A6 A-side + W15 + W16)

| script | D1 abs-path | D2 cross-lane import | D3 cwd-dependent | D4 singular-guard | D5 assert / 3rd-party | D6 |
|---|---|---|---|---|---|---|
| `computations/unaudited-audit-a6-w15w14-2026-08-15/a6_engine.py` | no | none (module) | not itself, but it is only importable via cwd — every `a6_A*` runner below reaches it that way | n/a | **2** / — | present |
| `computations/unaudited-audit-a6-w15w14-2026-08-15/a6_A1_fibres.py` | no | **none** — bare `import a6_engine` | **YES ×2** (`results_A1_fibres.json`) | n/a | 0 / — | present |
| `computations/unaudited-audit-a6-w15w14-2026-08-15/a6_A3_minimality.py` | no | none | **YES ×3** (`results_A3_minimality.json`, `witness_drop_w%d.json`) | n/a (Python-side); **does** build exact rational point witnesses (a (v)-style control, for the four-word relaxation) | 0 / — | present |
| `computations/unaudited-audit-a6-w15w14-2026-08-15/a6_A4_gen_singular.py` | no | none | **YES ×2** — `open("a6_A4_singular.sing","w")` bare | **(i) ABSENT (ii) ABSENT — never spawns Singular at all; the operator runs the emitted `.sing` by hand, so no `?` parsing exists anywhere in this route (iii) ABSENT — emits no `LIB "elim.lib";` yet emits `sat(...)` (iv) ABSENT — emits the `sat(I,J)[1]` TRAP (v) ABSENT** | 0 / — | present |
| `computations/unaudited-audit-a6-w15w14-2026-08-15/a6_A4_singular.sing` | n/a | n/a | n/a | **(i) ABSENT — ring vars `v1..v26`, generators `p1..p6`/`gz`/`kk`/`cells`, no `zzg*`, no guard (ii) ABSENT (iii) ABSENT — no `LIB "elim.lib";` but line 31 calls `sat` → `sat` is undefined on the W16-calibrated build (ledger 14) (iv) ABSENT — `ideal S6 = sat(J6, cells)[1];` is the ledger-11 `[1]` TRAP verbatim, three times (lines 31, 33, 36...) (v) ABSENT** | n/a | present |
| `computations/unaudited-audit-a6-w15w14-2026-08-15/a6_A4b_sat.sing` | n/a | n/a | n/a | **(i) ABSENT (ii) ABSENT (iii) PRESENT `LIB "elim.lib";` (iv) PARTIAL — `ideal S6 = sat(J6, cells);` avoids `[1]` but is not the `list L = sat(...); ideal S = L[1];` portable form (v) PARTIAL — carries a sat-*semantics* control (`ring rt = 0,(a,b,c)`, expect_1/expect_0), not an explicit rational point of a feasible relaxation**. Also re-declares `poly cells` and `ideal Jd1..Jd6` twice (lines 15/21 and 16–20/26–30); `--no-warn` suppresses the redefinition warnings | n/a | present |
| `computations/unaudited-audit-a6-w15w14-2026-08-15/a6_A5_nonvacuity.py` | no | none | **YES ×3** (`a6_nonvacuity_point_seed11.json`, `results_A5_nonvacuity.json`) | n/a; **this is the lane's explicit-point construction** | 0 / — | present |
| `computations/unaudited-residual-w15-2026-08-15/w15_core.py` | no | none (module) | no | n/a | 0, **no `require()`** | present |
| `computations/unaudited-residual-w15-2026-08-15/w15_forcing.py` | no | SELF | no | **(i) ABSENT (ii) ABSENT — `run_singular` returns `p.stdout + p.stderr` with NO check of any kind, not even the return code (iii) ABSENT (iv) n/a (v) ABSENT** | **3** / — | present |
| `computations/unaudited-residual-w15-2026-08-15/w15_task0_calibrate.py` | **YES** (`ROOT = "/Users/rishi/workplace/krenn-conjecture"`) | ABS-rooted read of the W8 lane | no | n/a | **3** / — | present |
| `computations/unaudited-residual-w15-2026-08-15/w15_task1_m24.py` | no | SELF | no | **(i) ABSENT — ring vars `z0..z25`, generators `q1..q6`/`gc`/`mm`, no `zzg*`, no guard (ii) ABSENT — emits `sing_m24_membership.sing` and never spawns Singular; the m=24 verdict rests on a hand-run whose stdout was never `?`-parsed (iii) ABSENT (iv) n/a — no `sat` (v) ABSENT in this file** | **11 asserts** (2nd highest) / — | present |
| `computations/unaudited-residual-w15-2026-08-15/w15_task4_controls.py` | no | SELF | no | n/a | **2** / — | present |
| `computations/unaudited-residual-w15-2026-08-15/sing_m24_membership.sing` | n/a | n/a | n/a | **(i) ABSENT (ii) ABSENT (iii) ABSENT — not needed, no `sat` (iv) n/a (v) ABSENT — carries leave-one-out `reduce` controls only** | n/a | present |
| `computations/unaudited-residual2-w16-2026-08-15/w16_m24b.py` | no | SELF | no | via `w16_sing` — **(i) partial: harness exposes `check_no_shadowing` but this script never calls it and uses no `zzg*` names (ii) PRESENT (iii) ABSENT (iv) n/a (v) ABSENT** | 0 / — | present |

### 1.8 `draft_promotion_checklist.md`

Cites, in addition to scripts already tabulated above
(`chk05_gamma_boundary.py`, `run_t4_controls.py`, `run_t8_soundness.py`,
`w12_cut.py`, `w12_split.py`, `a5_t5_apolarity_fixed.py`,
`a6_A4_singular.sing`, `a6_A4b_sat.sing`, `sing_m24_membership.sing`):

| script | D1 | D2 | D3 | D4 singular-guard | D5 | D6 |
|---|---|---|---|---|---|---|
| `computations/unaudited-residual2-w16-2026-08-15/w16_sing.py` | no | none (module) | no | **(i) PARTIAL — defines `check_no_shadowing()` but emits `z%d` ring vars and `q%d` generators, NOT the reserved `zzg*` prefix; the guard is never invoked by any cited script (ii) PRESENT — line-anchored `?` + "error occurred" (iii) ABSENT (iv) DOCSTRING ONLY — the file's docstring promises `list LL = sat(I,J); ideal S = LL[1];` but the module contains no `sat` call at all (v) ABSENT** | **1 bare assert** (line 64, `Fraction(c).denominator == 1` — the integrality check that keeps malformed polys out of Singular; silently disabled by `python3 -O`) / — | present |

Glob/template citations in this draft that are not real files:
`computations/verify_*.py`, `a6_A*.py`, `../computations/name.py`,
`certification/audits/SUPERSESSION-<id>.md`, `<lane>/REPORT.md`. These are
naming conventions, not missing artifacts.

### 1.9 `draft_supersessions_entry.md`

This draft cites the union of the scripts above (A3, A4, A5, A6, W10, W12,
W13, W14, W15 lanes) plus two not tabulated elsewhere:

| script | D1 | D2 | D3 | D4 | D5 | D6 |
|---|---|---|---|---|---|---|
| `computations/unaudited-audit-a6-w15w14-2026-08-15/a6_A2_certificate.py` | no | **none** — bare `import a6_engine` | **YES ×3** (`results_A2_certificate.json`, `results_A2b_reduced.json`) | n/a | 0 / — | present |
| `computations/unaudited-monochrome-w14-2026-08-15/w14_task2_layers.py` | no | SELF | no | **(i) ABSENT (ii) ABSENT — returncode-only (iii) ABSENT (iv) n/a (v) ABSENT** | 0 / — | present |

All other scripts it names are covered by §1.1–§1.7. Its `proofs/*.md` and
`certification/audits/SUPERSESSION-2026-08-15-0N.md` citations are promotion
*targets*, listed in §5.

## 2. Summary counts

83 distinct cited `.py`/`.sing` artifacts, all present on disk.

| debt class | count | share |
|---|---|---|
| **D1** hard-coded `/Users/rishi` absolute path | **17 scripts** | 20% |
| **D2** any `sys.path` hack or cross-lane import | **52 scripts** | 63% |
| — of which ABS (hard-coded lane path on `sys.path`) | 15 | |
| — of which SELF (`__file__`-derived self-dir insert) | 36 | |
| — of which CWD (`sys.path.insert(0,'.')`) | 1 | |
| — of which genuine **cross-lane imports** | **6** (`chk06_...py`, `chk09_controls.py`, `a5_t1_expansion.py`, `run_a_gauge_and_crosscheck.py`, `run_j_sc_gauge.py`, `run_t4_controls.py`) | |
| **D3** cwd-dependent | **18 mechanical / 14 operative** — 4 of the 18 (`a4_cut.py`, `w12_cut.py`, `w12_split.py`, `w12_cutdecide.py`) are library modules whose import path is supplied by their runners | 17% operative |
| **D4** scripts on a Singular route | **13** | |
| — (i) `zzg*` prefix / no-shadowing guard PRESENT | **0** | |
| — (ii) stdout `?`-line parsing PRESENT | **4** (`a4_cut.py`, `chk02_...py`, `w16_sing.py`, `w16_m24b.py` via `w16_sing`) | |
| — (iii) `LIB "elim.lib";` PRESENT | **2** (`chk02_...py`, `a6_A4b_sat.sing`) | |
| — (iv) `list L = sat(I,J); ideal S = L[1];` PRESENT | **1** (`chk02_...py`) | |
| — (iv) the `sat(I,J)[1]` TRAP actually emitted | **2** (`a6_A4_gen_singular.py`, `a6_A4_singular.sing`) | |
| — (v) explicit-point control PRESENT | **2** partial (`a6_A5_nonvacuity.py`, `a6_A3_minimality.py`); `a6_A4b_sat.sing` has a sat-semantics control only | |
| **D5** at least one bare `assert` | **26 scripts, 84 asserts total** | 31% |
| — worst: `chk07_w10G_gauge.py` 15, `w15_task1_m24.py` 11, `chk01_engine_and_certificate.py` 10, `a5_core.py` 8 | | |
| — scripts with a raising `require()` instead | 4 (`w12_core`, `w13_core`, `w14_core`, `w10_core`) | |
| **D5** third-party import (blocks `python3 -I -S`) | **6 scripts, numpy only** — `a5_core.py`, `a5_t3_h4.py`, `a5_t8_transfer.py`, `w13_task1_law.py`, `a6_B6b_keylemma_h5.py`, `b9_core.py` | 7% |
| **D6** cited script missing from disk | **0** | |

No cited script imports `sympy`, `pysat`, `scipy` or `networkx`. Every cited
script is stdlib-only except the six numpy users, so `python3 -I -S` is
achievable for 77 of 83 with no code change at all — the numpy uses should be
checked for whether they are load-bearing (e.g. `rank_mod_p_np`) or merely
convenience.

## 3. Worst offenders (most work to promote)

1. **`computations/unaudited-residual-w15-2026-08-15/w15_forcing.py`** — its
   `run_singular` performs **no error check whatsoever**: it returns
   `p.stdout + p.stderr` and discards the return code. Every ledger-11 and
   ledger-13 failure mode (errors on stdout with rc 0; silent identifier
   rebinding) passes straight through into a W15 verdict. Plus 3 bare
   `assert`s doing the clean-word/constant-word preconditions. Needs the full
   `w16_sing`-style harness before anything downstream of it is promotable.

2. **`computations/unaudited-audit-a6-w15w14-2026-08-15/a6_A4_gen_singular.py`
   + `a6_A4_singular.sing`** — the emitted script contains the ledger-11
   `sat(I,J)[1]` trap **and** omits `LIB "elim.lib";`, so on the W16-calibrated
   build `sat` is undefined; nothing in the pipeline parses stdout for `?`,
   because the generator never spawns Singular — a human ran it. Bare-filename
   write on top. This is the A6 independent confirmation of the m=24
   certificate, i.e. exactly the artifact whose independence is being claimed.

3. **`computations/unaudited-thickfibre-w12-2026-08-15/w12_core.py`** (and
   therefore `run_t1c_survivor_groebner.py`, `run_t1d_certificate.py`,
   `run_t3_cut.py`, `w12_cutdecide.py`) — `run_singular` raises only on
   non-zero return code, the precise case ledger item 11 says does not fire.
   This is the back-end for **both** the m=20 eight-word certificate and the
   cut kill. One file to fix, four cited checkers repaired.

4. **`computations/unaudited-residual-w15-2026-08-15/w15_task1_m24.py`** —
   emits `sing_m24_membership.sing` and never runs it: the m=24 membership
   verdict has no machine-checked error path at all. 11 bare `assert`s, the
   most of any cited runner, several of them carrying real preconditions.

5. **The whole `a6_A*`/`a6_B*` family (13 scripts)** in
   `computations/unaudited-audit-a6-w15w14-2026-08-15/` — no `sys.path`
   handling and bare `import a6_engine` / `import a6_bcore`, plus bare
   `open("results_*.json","w")`. They run *only* from inside their own lane
   directory and silently write their certificates into whatever cwd the
   operator happened to be in. Mechanical but 13-fold.

6. **The `a5_*` family (12 of 13 scripts)** in
   `computations/unaudited-audit-a5-w13-2026-08-15/` — every runner hard-codes
   `/Users/rishi/workplace/krenn-conjecture/...` twice (a `sys.path.insert`
   and an `OUT` prefix); `a5_t1_expansion.py` hard-codes a **third** path,
   into a different lane (`unaudited-induction-w13`), and hard-codes its JSON
   write path as a literal. Mechanical, but it is 12 files and the lane is
   uniquely un-relocatable as written.

7. **`computations/unaudited-audit-a6-w15w14-2026-08-15/b9_c1_detlaw.py`,
   `b9_c2_phi.py`, `b9_c2_symbolic.py`, `b10_summary.py`** — same hard-coded
   `HERE`/`W14`/`P2` absolute paths, and `b9_core.py`'s Singular runner is
   returncode-only.

8. **`computations/unaudited-induction-w13-2026-08-15/w13_task3_transfer.py`**
   — `sys.path.insert(0, '.')` plus a bare JSON write: the only cited script
   that fails to even *import* unless cwd is its lane.

9. **`computations/unaudited-audit-a4-w12w10-2026-08-15/chk06_...py` and
   `chk09_controls.py`** — the two audit checkers that import *live modules
   out of the lane they are auditing* (`w12_core`, `w12_cut`, `w12_cutdecide`,
   `w12_reduce`, `w12_torus`) plus
   `computations/verify_n8_d2_kill_and_monochrome_rigidity.py` at repo root.
   Portable (paths are `__file__`-derived) but it means A4's "independent"
   controls execute W12 code; worth stating explicitly in the promotion note.
   The other four cross-lane importers are benign by comparison:
   `a5_t1_expansion.py` → `w13_core` (deliberate, it is the cross-check, but
   via a hard-coded absolute path), `run_a_gauge_and_crosscheck.py` → `w6_core`
   + `w9_template`, `run_j_sc_gauge.py` → `w8_core`, `run_t4_controls.py` →
   `w9_core`, all `__file__`-derived. `run_t8_soundness.py` and
   `run_t8b_mutation.py` push the w9/w6/p1 lane paths onto `sys.path` without
   importing anything from them.

10. **`computations/unaudited-audit-a4-w12w10-2026-08-15/chk07_w10G_gauge.py`
    (15 asserts) and `chk01_engine_and_certificate.py` (10 asserts)** — no path
    debts, but the largest concentrations of `-O`-erasable checks in the cited
    set.

**Cross-cutting:** not one cited Singular script uses the reserved `zzg*`
generator prefix, and not one calls a no-shadowing guard. The guard exists in
`computations/unaudited-residual2-w16-2026-08-15/w16_sing.py` and is used by
later lanes (W18, W19, W20, W21, A7), but every cited script predates that
practice — consistent with the drafts' own "pre-commit obligations" wording.

## 4. Cited artifacts that DO NOT exist on disk

**Missing evidence (real gap):**

* `computations/unaudited-thickfibre-w12-2026-08-15/results_t4_controls.json`
  — cited by `draft_cut_mechanism.md` §7/§8 and `draft_promotion_checklist.md`.
  The runner `run_t4_controls.py` exists; the JSON was never written. This is
  A4's discrepancy D2 (the C1 torus round-trip control).
* `computations/unaudited-thickfibre-w12-2026-08-15/results_t8_soundness.json`
  — same two drafts, same status (C2 Smith substitution round-trip).
  `run_t8_soundness.py` and `log_t8_soundness.txt` exist, the JSON does not.

**Promotion targets, expected to be absent until the commit:**

* `proofs/cap-error-lh-law-and-blocking-taxonomy.md`
* `proofs/evaluation-principle-and-lh-directness.md`
* `proofs/even-cut-mechanism-and-gamma-boundary.md`
* `proofs/fourth-matching-cubic-support-floor.md`
* `proofs/mixed-exact-gauge-normalisation.md`
* `proofs/n8-m20-survivor-word-certificate.md`
* `proofs/n8-m24-residual-word-certificate.md`
* `certification/audits/SUPERSESSION-2026-08-15-01.md` … `-06.md`
  (and the placeholders `-NN.md`, `SUPERSESSION-<id>.md`)

**Glob/template citations, not files:** `computations/verify_*.py`,
`a6_A*.py`, `../computations/name.py`, `computations/unaudited-audit-*/REPORT.md`,
`<lane>/REPORT.md`, `BASELINE.md` (the real file is `certification/BASELINE.md`,
which exists and is also cited correctly).

Everything else cited by the nine drafts — all 83 scripts, and every
`results_*.json` / `log_*.txt` / `notes/*.md` / `proofs/*.md` reference not
listed above, including `log_A4_singular.txt`, `log_A4b_sat.txt`,
`log_sing_m24.txt`, `witness_drop_w1.json`, `witness_drop_w6.json`,
`b10_summary.json` and `PINNED_HEAD.txt` — is present on disk.
