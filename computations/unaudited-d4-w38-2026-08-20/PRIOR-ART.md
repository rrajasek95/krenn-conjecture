# W38 — PRIOR ART for n = 8, d = 4 (and the d ≥ 4 regime) — UNAUDITED

**UNAUDITED. Design phase only.** Pinned HEAD
`4ee924e7aab113d121fac52b7987eb80185922b5`. Repo-internal sweep done by a
read-only fan-out lane over `notes/` (2 261 files), `proofs/`,
`computations/`, `references/`, `certification/`, `formal/`, `README.md`,
`PROOF-SKETCH.md`. External items are **as recorded in the repo**; this lane
did no web access.

Every `(8,4)`-shaped hit below is tagged with its sense: **[nd]** =
`(vertices, colours)`, **[Nk]** = `(sites, ladder level)` at `d = 3`.

---

## 1. Headline

**The repo is a `d = 3` programme.** There are exactly three places where
`d ≥ 4` is a real object of study, and none of them targets `n ≥ 6, d ≥ 4`
directly:

1. colour projection, which *inherits* `d ≥ 4` from `d = 3`;
2. `n = 4`, where `k_max(4) = 3` is proved in-repo;
3. `references/REFERENCES.md`, which records the external `d ≥ 4` literature.

**No repo proof, note, or computation attacks `d ≥ 4` at `n ≥ 6` as a target
in its own right.** No file is named for a four-colour case. There is no
`(10,4)` **[nd]** anywhere in the repo.

---

## 2. Repo-internal, `d ≥ 4`

### 2.1 The colour-projection monotonicity layer — the only artifact that *closes* `d ≥ 4` cases

| artifact | content |
|---|---|
| `formal/MonochromaticQuantumGraphKeyLemmas.lean:200-235` | Lean 4, ledger id **A7**, status **F**. `eqSystemN_restrictColors` (restriction along any injection `Fin D' → Fin D`), `exists_eqSystemN_of_le`, **`not_exists_eqSystemN_of_le`** ("non-existence at palette size `D'` propagates upwards"), `no_solution_ge3_of_no_solution_d3`. Ledger entry `formal/FORMALIZATION.md:67`. |
| `PROOF-SKETCH.md:102-108` | **Proposition 1.1 (colour reduction) [P]**, publication register. |
| `notes/proof-sketch-claim-index.md:41` | status **READY**; "the best-supported claim in the sketch — the only one that is both machine-formalized and stated in publication register". Flags the convention break: the checker has no matching `notes/colour-projection-monotonicity.md`. |
| `computations/verify_colour_projection_monotonicity.py` | P1 monotonicity; **P2** — "since `(6,3)` is closed […] **`(6,4)` and `(6,5)` are closed too**, though both are listed as open upstream. At every `n` the conjecture reduces to `d = 3`"; **P3** — one-wayness, "the settled large-`d` cases — `(4,4)`, `(6,6)`, `(8,10)`, `(10,10)` **[nd]** — imply nothing about `(8,3)`". Coefficient identity checked at `(n,d',d) = (4,4,3), (6,5,3), (6,4,2), (8,4,3)` — the `(8,4,3)` here **is [nd]**, one of the very few genuine `n=8, d=4` objects in the repo. Git: `c561d0b "Verify colour projection is monotone, closing (6,4) and (6,5)"`. |
| prose | `proofs/six-site-arbitrary-complex-obstruction.md` §2 (lines 63-79, "rules out every palette of size at least three"); `notes/final-resolution-foundations-draft.md` §2.4 **Lemma 2.7** ("coordinate projection is exact"); `notes/clean-pair-cap-exact-descent-target.md` §5; `notes/2026-08-14-proof-zoomout-and-parallel-attack-plan.md:22-23` (spine step 1, "Palette reduction [P]"); `README.md:48-51`. |
| audit trail | `notes/wip-attack-map-2026-08-03.md:2126-2129` ("REDUCTION VERIFIED"); a repaired defect — "silently assumed equal amplitudes" — at `certification/SUPERSESSIONS.md:307-310`. |
| recorded **limitation** | `notes/target-flattening-essential-star-pair-bound.md:186-190` + its independent audit: "When the original palette has more than three colours, it concerns one fixed ternary projection at a time. The good pair supplied for one chosen triple need not work for every other triple." **This is the sharpest caveat in the corpus and it bears directly on Route 3 of ATTACK-PLAN.** |

**Nothing anywhere claims a reduction in the other direction**;
`verify_colour_projection_monotonicity.py:36-41` explicitly refutes it with
the `(4,3)` source and a padded `(4,2)` packet.

### 2.2 `n = 4`, all `d ≥ 4` — proved in-repo

`notes/final-resolution-foundations-draft.md:678-698` — **Theorem 4.5:
`k_max(4) = 3`**, by partition rank ("the left side has partition rank `q` by
Lemma 4.2. Hence `q ≤ 3`"), for arbitrary complex matrices (general
bicoloured). Line 1173: "Theorems 4.5 and 5.1 rule out any monochromatic
graph with `q ≥ 4`, resp. `q ≥ 3`". Support: `notes/first-lemmas.md:22-36`,
`notes/tensor-route.md:59-108`. Corollary 5.2 (line 729): `k_max(6) = 2`.

### 2.3 `W32-2COL` — colour-*subset* restriction inside `d = 3`

`computations/unaudited-x4general-w32-2026-08-20/run_01_words.py:10-24`
states W32-2COL and W32-RES; `w32_core.py:321-329` (`restrict_pair`);
calibration `run_02_calib.py:7-15` ("W32-2COL CANNOT kill on its own").
**Sense: [Nk]** — `X_4` is level 4, at `d = 3` colours. Follow-on lane
**W33** studies "the exact `d=2` variety at `n=8`"
(`computations/unaudited-x4general-w33-2026-08-20/run_01_controls.py:2-4`).

### 2.4 The `(8,4)` **[Nk]** hits — all `d = 3`, none relevant to this target

* `notes/2026-08-15-resolution-master-plan.md:1878-1879` — the v43 W27 record
  the brief quoted. Sense **[Nk]**.
* `computations/unaudited-penult-w27-2026-08-18/REPORT.md:16-20`: "fires
  40/40 at `(6,3)` and 25/25 at `(8,3)` (known nonempty), silent at `(6,4)`
  (known empty) — and **`(8,4)` has the signature of `(6,4)`, not `(8,3)`**".
  Driver `run_t1f_calib.py:229-238` iterates `for n, k in ((6,3),(6,4),(8,3),
  (8,4))` and prints `"(N,k) = …"` — **definitive**.
* `computations/unaudited-x4empty-w28-2026-08-18/REPORT.md:68`;
  `computations/unaudited-audit-a8-2026-08-19/log_t8.txt:20-29` (prints
  `(N=6, k=4)` / `(N=8, k=4)` then abbreviates).
* `notes/2026-08-15-conventions-and-hazards.md:38-76` item 6 pins the `X_k`
  convention but **does not flag this pair collision** — hence the proposed
  ledger 30.

False positives to ignore: `kernel.shape == (6,4)` in two verify scripts,
`comb(6,4)` in audit scripts, `w15_task2_run.py:39`, SHA-256 substrings
containing `4664`, dihedral/cell `D4`, degree-4 and Hasse `D_1..D_4`.

---

## 3. External, as recorded in the repo

### 3.1 The 2021/2022 SAT result — the ONLY external `n = 8, d = 4` **[nd]** result

**A. Cervera-Lierta, M. Krenn, A. Aspuru-Guzik, "Design of quantum optical
experiments with logic artificial intelligence", *Quantum* **6**, 836 (2022);
arXiv:2109.13273.** `references/REFERENCES.md:195-226`, marked *[primary —
ar5iv text read]*. Verbatim:

> "We test this approach to check if there exists a graph with monochromatic
> edges that generate the GHZ state of `n > 4` parties and `d ≥ n/2` local
> dimensions. […] We obtained `K =` False for `n` up to `8` and `d = n/2`
> colors."

**Scope, per the repo's own reading (REFERENCES.md:212-226):**
(i) verified cases are exactly **`n = 6, d = 3` and `n = 8, d = 4`** — `d =
n/2` exactly; `d ≥ n/2` is their *conjecture*, not their result.
(ii) **monochromatic-edge model** only.
(iii) SAT variables are Boolean edge literals, "so the argument is about
supports […] it is not a weighted no-go".
Hence `N=8, d=3` and `N=10, d=3` in the monochromatic-edge model are **not**
covered.

There is a **citation erratum** in the corpus:
`notes/wip-attack-map-2026-08-03.md:1999-2001` originally recorded their
scope as "`N=8 d≥4`"; `:2045-2053` corrects it to exactly `(6,3)` and
`(8,4)`. **The brief's premise "the monochromatic versions of `(8, d≥4)`
were SAT-closed externally in 2021" is the pre-correction over-statement:
only `d = 4` was closed, not `d ≥ 4`** (though `d ≥ 4` at `n=8` follows from
`d=4` by Lemma P, which their paper does not invoke).

Cross-ref: `proofs/diagonal-hafnian-recurrence-obstruction.md:41-46`.

### 3.2 Chandran–Gajjala and successors

| paper | recorded scope | model |
|---|---|---|
| **arXiv:2202.05562**, Chandran–Gajjala, EJC 2026 (journal data marked *unverified*) | Theorem 1 (`REFERENCES.md:112-113`): "For a graph `G` non-isomorphic to `K_4`, `μ(G) ≤ 2` and `μ(K_4) = 3`" — Bogdanov's three-one-factors lemma. Own contribution: characterisation of `μ=1`, `μ=2`, and Krenn–Gu for a sub-class. Also credited with "`d > N-2` (EJC 2026)" at `notes/wip-attack-map-2026-08-03.md:2001-2003`. | §2 machinery (Hamiltonian cycle, legal/illegal edges, crossing pairs, drums) is `d = 2`-internal; the `μ(G) ≤ 2` theorem is `d`-free in form. |
| **arXiv:2407.00303**, Chandran–Gajjala–Illickan–Krenn, MFCS 2024 | Thm 1.7 (multigraph three-one-factors); **Thms 1.9–1.12 are `d`-free and constrain the open case directly** (`REFERENCES.md:155-158`): `κ(G) ≤ 2 ⇒ μ(G) ≤ 2`; vertex-count reduction across a 3-cut "valid for multigraphs with bichromatic edges and with no hypothesis on `d`"; max degree 3; min degree 3 ⇒ `μ ≤ 3`. Also records that the four-vertex bicoloured case was settled by Mantey via exact Gröbner (`README.md:201-203`). | **general bicoloured multigraph** |
| **arXiv:2304.06407**, *Quantum* **8**, 1396 | Thm 2.6 (`REFERENCES.md:227-253`): "It is not possible to generate an `n > 4` vertex experiment graph with dimension `d ≥ n/√2`." At `n = 8` this closes `d ≥ 6`. | general model, but **explicitly for simple graphs**, and "vacuous at `d = 3`" (at `n=8`, `μ=3` reads `k(v) ≥ -1`). |

None of these is an `n`-by-`d` case list; all are stated for general `n`.

### 3.3 AlphaProof / "DeepMind prover agent"

`README.md:191-193` and `proofs/eight-site-diagonal-obstruction.md:1032-1034`
record "**DeepMind's AlphaProof Nexus** (arXiv:2605.22763) resolved the
many-colour regime `n = d ∈ {4, 6, 10}`". `references/REFERENCES.md:265-277`
adds that this is the paper behind the `d = N` results, that "neither covers
`d = 3`", and corrects the record that **M. Krenn is not an author**.

**The README understates the scope.** Reading the registry directly, the
statements attributed to the DeepMind prover are:
`eqSystem_no_solution_even_ge4_d_eq_n_explicit` (all even `N ≥ 4`, `D = N`,
ℂ); `eqSystem4_no_solution_d4`; `eqSystem4_no_solution_ge4` (`n=4`, all
`D ≥ 4`); `eqSystem6_no_solution_d6`; **`eqSystem8_no_solution_d10`** (`n=8`,
`d=10` — `d ≠ n`); `eqSystem10_no_solution_d10`; plus the `_real`, `_int`,
`_trinary_int` variants at `n = 4`. **All are `d ≥ 4` [nd], all general
bicoloured.**

**So: the `d ≥ n` regime at `n = 8` is covered only at `d = 8` (`D = N`) and
`d = 10`. `d = 9` has no entry. `d = 4..7` have no entry.** The brief's
question "AlphaProof's `d ≥ n` regime at `n=8` covers `d ≥ 8` only?" —
answer: it covers `d = 8` and `d = 10` explicitly, and everything `d ≥ 8`
follows from `d = 8` by Lemma P (which the registry does not invoke, which is
why `d = 9` sits unstated).

### 3.4 formal-conjectures PRs — **all five open, nothing merged** (litwatch, window 2026-08-12→08-20)

| PR | claim | `d ≥ 4` relevance | status |
|---|---|---|---|
| **#4610** (algal) | Complete Lean 4 proof of the normalized `(6,3)` fibre over ℂ; general/bicoloured `EdgeN`. Axioms include `Lean.ofReduceBool`, `Lean.trustCompiler` (5 945 `native_decide` uses). `notes/external-six-site-lean-certificate.md`; reproduced by execution here. | via Lemma P would give `(6,d)` for all `d ≥ 3` — **unclaimed by them and by us** | open, "on the accepted track, not merged"; stalled ~1 month; **not audited here** |
| **#4659** (KitaKen1) | `∀ N D, N ≥ 6 → Even N → D ≥ 3 → ¬∃ W : WeightsN N D ℤ, EqSystemN N D W`. Method: `restrictToThreeColors` → mod 2 → `N→N-2` contraction → six-vertex char-2 base. Axioms clean `[propext, Classical.choice, Quot.sound]`, **no `native_decide`**. `computations/unaudited-lean-l1-2026-08-20/RELATED-4659.md` (280 lines). | **DIRECTLY covers `(8,4)` over ℤ and `{-1,0,1}`** — the full even-`N≥6`, `D≥3` integer case | open, community-verified 08-08 by williamjblair, reviewer silent. Does **not** touch ℂ or ℝ. |
| **#4661** | Solver-free `D ≤ N-2` / `k_max(n) ≤ n-2` anchor lemma `exists_fullColumnAt_domain`, arbitrary integral domains, all `N`, all `D ≥ 3`. Best repo statement: `notes/2026-08-11-external-theory-reformulation-survey.md:296-303` — "a hard wall at `D = N-2` with no purchase at `d = 3`; the lemma, not the count, is the asset". | closes `d = 7` at `n = 8` | open; **the only KG PR with human movement** (08-18 ping) |
| **#4664** | "a claimed `(6,4)` resolution over the complex numbers" (`README.md:199-200`; `PROOF-SKETCH.md:869`) = `eqSystem6_no_solution_d4`. **[nd]** | the closest external work to a `d=4` target at `n ≥ 6` | open, unmerged |
| #4511 | named only in the litwatch open-PR list; no content recorded | — | open |

**"Axis-Servant Lemma" / djh58.** `README.md:196-199` and
`PROOF-SKETCH.md:864-867` record only that "the same bound was derived
independently and concurrently by djh58 (the *Axis-Servant Lemma*)". **No
file in the repo states what the lemma says, who reviewed it, or where it
lives.** Cited as reference [12] at `PROOF-SKETCH.md:933-935`; used at
`proofs/six-site-obstruction-exposition.md:59-62` and
`proofs/eight-site-diagonal-obstruction.md:1070-1073`.

### 3.5 Litwatch, window 2026-08-12 → 08-20

`computations/unaudited-litwatch-2026-08-20/REPORT.md` (67 lines; the lane's
write was harness-blocked and the manager transcribed it; web-only). `d ≥ 4`
content: **PR #4659's `D ≥ 3` integer claim is the only `d ≥ 4` mathematical
movement in the window, and it is integers-only.** All five KG PRs open. The
Krenn/Firsching/Tsoukalas/Gajjala/Gu/Chaudhuri tensor-algebraic no-go paper
is "STILL unposted ('in preparation' since May) — the largest unbounded
external risk"; per `REFERENCES.md:271-277` that line is titled for `d = N`.
Prize page unchanged: `n=8 d=3` open, EUR 3 000, peer-reviewed publication
required. 21-item NO-CHANGE list verified, including "AlphaProof nexus
outputs frozen" — **no movement on any AlphaProof `d ≥ 4` result**.
Competitor repo `YesterdaysLemon/krenn-gu-research`: "NO `n=8` movement", all
`d = 3`. **The report contains nothing about `(6,4)`/`(6,5)`/`(8,4)` beyond
the bare "#4664 open" line, and no re-check of the 2021 SAT result.**

---

## 4. Explicit negatives (these matter)

1. **No repo proof or computation targets `d ≥ 4` at `n ≥ 6` directly.** The
   only in-repo `d ≥ 4` closures are `n = 4` (partition rank) and
   `n = 6, d = 4/5` *inherited* by monotonicity.
2. **No content on the Axis-Servant Lemma** beyond the name (2 real
   occurrences).
3. **No content on PR #4664** beyond "claimed `(6,4)` resolution over ℂ,
   open" (3 one-line mentions). No `RELATED-4664.md`, no author, no method,
   no verification — contrast the 280-line `RELATED-4659.md`.
4. **No content on PR #4511** beyond its number.
5. **No `(10,4)` [nd] anywhere.**
6. **No file named `prior-art*`, `competitor*`, or `lit-watch*`.**
   `notes/route-registry.md` (33.6 KB) has **zero** prior-art or `d ≥ 4`
   content.
7. **The repo never notices that its own `(6,3)` theorem + Prop 1.1 subsumes
   PR #4664's `(6,4)` claim** — despite
   `verify_colour_projection_monotonicity.py:32-33` stating the implication.
   `references/REFERENCES.md:322` still records
   `eqSystem6_no_solution_d4/d5` as OPEN. See STATEMENT §6.
8. **Local-modification caveat.** The `eqSystem8_no_solution_d3_diagonal*`
   entries marked `research solved` in
   `computations/unaudited-lean-l1-2026-08-20/work/fc/.../MonochromaticQuantumGraph.lean:517-554`
   are **this repo's own uncommitted staging** (`git diff` shows +99 lines on
   top of upstream `9f5ee77`), not upstream status. Do not cite them as
   registry facts.

---

## 5. Bottom line for `n = 8, d = 4`

| model | status |
|---|---|
| edge-coloured (support), ℂ | **closed externally 2021/2022** (Cervera-Lierta et al., SAT, `d = n/2`) |
| edge-coloured (weighted), any integral domain | **closed in-repo**, free: Corollary 1.3 + Lemma P (Corollary W38-2) — a strengthening of the above |
| block-diagonal, any integral domain | **closed in-repo**, free: Theorem 1.2 + Lemma P (Corollary W38-1) |
| general bicoloured, ℤ and `{-1,0,1}` | **claimed closed externally** by PR #4659 (unmerged, community-verified) |
| **general bicoloured, ℂ and ℝ** | **OPEN — and implied by `(8,3)`, which is the campaign's main target** |
