# BUILD-STATUS — what compiles, under which toolchain

> **UNAUDITED — lane L1, 2026-08-20.** Pinned krenn-conjecture HEAD
> `f9a3bd6b93417a43d86ad782d1f76b62f14bc50a`. Not spine. Nothing submitted.

## Toolchain

Everything below uses **the toolchain formal-conjectures itself pins**, taken
from its own `lean-toolchain`:

| | |
|---|---|
| Lean | `leanprover/lean4:v4.27.0` (`db93fe1608548721853390a10cd40580fe7d22ae`) |
| mathlib | `a3a10db0e9d66acbebf76c5e6a135066525ac900` (= `v4.27.0` tag) |
| formal-conjectures | shallow clone of `google-deepmind/formal-conjectures` default branch, 2026-08-20 |
| host | macOS 25.5.0, arm64 (Apple silicon), 18 cores |

algal's `krenn-gu-6x3-certificate` pins the identical Lean and mathlib
revisions, so the three code bases are toolchain-compatible with no work.

**Environment note that cost time and will cost it again.** The v4.27.0
toolchain ships an **x86_64** Mach-O binary, so on this arm64 host every
Lean/Lake invocation runs under Rosetta 2. The *first* run of a cold `lean`
binary stalls for minutes while Rosetta AOT-translates it, with no output. This
is not a hang and not a corrupt install — do not kill it. After the first run it
is fast. All timings below are post-warm-up.

---

## A. `statement.lean` — the proposed registry addition

**Status: COMPILES, clean, against the real upstream module.**

Method: the four hunks of `../statement.lean` were spliced into a shallow clone
of `google-deepmind/formal-conjectures` at their intended insertion points
(`work/splice.py`), then built exactly as the repository's own `AGENTS.md`
prescribes:

```
lake --wfail build FormalConjectures.Paper.MonochromaticQuantumGraph
```

| result | |
|---|---|
| exit code | **0** |
| jobs | 8057 |
| module build time | 52 s |
| warnings | none — and `--wfail` makes warnings fatal, as CI does |
| diff | **84 additions, 0 deletions**, one file (`../statement.diff`) |

Axiom audit of the declarations that carry real proofs:

```
MonochromaticQuantumGraph.eqSystemNZ_of_eqSystemN
  depends on axioms: [propext]
MonochromaticQuantumGraph.isDiagonal_witness4_d3
  depends on axioms: [propext, Classical.choice, Quot.sound]
MonochromaticQuantumGraph.eqSystem4_has_diagonal_solution_d3
  depends on axioms: [propext, Classical.choice, Quot.sound]
```

No `sorryAx`. The three `N = 8` theorems are deliberate `sorry` placeholders
carrying `formal_proof using lean4` links, which is the shape formal-conjectures
uses for results proved in an external repository (PR #4610).

The `N = 8` statements were also type-checked against their intended
propositions, and `eqSystem8_no_solution_d3_diagonal_domain` was checked to
specialise directly to `ℂ`, `ℝ` and `ℤ`, with the `{-1,0,1} ⊆ ℤ` reading
following from the `ℤ` one in three lines. All four elaborate. One theorem
therefore covers the diagonal reading of every open `n = 8, d = 3` registry
coefficient domain.

### What this establishes

* `IsDiagonal` elaborates with `[Zero α]` only, and unifies with `EqSystemN`'s
  `[Semiring α]` and with `[CommRing α] [IsDomain α]` without instance trouble.
* `EqSystemNZ` and the bridge `eqSystemNZ_of_eqSystemN` are correct as written —
  the amplitude-nonzero strengthening is a two-line consequence of `EqSystemN`
  over any nontrivial semiring.
* **The registry's own `Witness4_d3` is diagonal.** `isDiagonal_witness4_d3`
  proves it. So the `N = 4` sharpness control (§7.3 of the proof document) is
  already formalised, and the `N = 8` theorem cannot be an artefact of the
  diagonal restriction alone.
* The file's linters (`category`, `AMS`, docstring, LaTeX-docstring, namespace,
  stub, import) all pass on the addition.

---

## B. `lrat-probe/` — the UNSAT layer

**Status: COMPLETE. All 87 orbit refutations are kernel-checked Lean theorems.**

`Std.Tactic.BVDecide.Reflect` ships *inside* the v4.27.0 toolchain, so this
package has **no dependencies at all** — no mathlib, no formal-conjectures. It
builds from a bare `lean-toolchain` + `lakefile.toml` in seconds.

```
skeleton/lrat-probe/
  lean-toolchain                 leanprover/lean4:v4.27.0
  lakefile.toml                  no [[require]] at all
  LratProbe/CnfCheck.lean        DIMACS parser (77 lines, after algal's)
  LratProbe/Orbit0.lean          worked single-orbit example
  LratProbe/Kernel.lean          kernel-`decide` variant (FAILS — see below)
  LratProbe/Orbits/Orbit00..86   87 generated modules, 22 lines each
  LratProbe/AllOrbits.lean       import aggregator
  LeanCheck.lean                 axiom audit
  artifacts/                     87 .cnf + 87 .lrat (29 MiB)
```

Each generated module is:

```lean
def orbitNParsed : Option ParsedDimacs := parseDimacs (include_str "../../artifacts/n8k4_N.cnf")
def orbitNCNF : CNF Nat := orbitNParsed.map (·.cnf) |>.getD []
theorem orbitNParsed_ok : orbitNParsed.isSome = true := by native_decide
theorem orbitNUnsat : orbitNCNF.Unsat := by
  apply Reflect.verifyCert_correct orbitNCNF (include_str "../../artifacts/n8k4_N.lrat")
  native_decide
```

| measurement | value |
|---|---|
| `lake build LratProbe` | **rc 0, 19.22 s wall**, 93/93 jobs, 18 cores, 64 s CPU |
| per orbit | ~3.5 s |
| peak RSS, one orbit in isolation | 353 MB |
| `verifyCert` on all 87, interpreted (`#eval`) | 87/87 `true`, 59.8 s |
| axiom closure of `orbit0Unsat` etc. | `[propext, Classical.choice, Lean.ofReduceBool, Lean.trustCompiler, Quot.sound]` |
| `sorryAx` | absent |

That closure is character-for-character algal's, as reported in his
`VERIFICATION-RESULTS.md` and in PR #4610.

### Provenance of the embedded CNFs

All 87 `artifacts/n8k4_*.cnf` are **byte-identical (sha256, 87/87)** to
`computations/unaudited-promotion-diag-2026-08-20/certified_package/orbits/`.
Nothing was re-encoded. The LRAT files are new; see `../lrat/MANIFEST.md`.

### The kernel-`decide` variant does NOT compile — this is a result, not a gap

`LratProbe/Kernel.lean` is `Orbit0.lean` with `native_decide` replaced by
`decide` (plus `set_option maxRecDepth 100000`). Result:

```
Stack overflow detected. Aborting.
1.17 real   rc=134
```

So there is no kernel-only replay at this scale, and the "kernel LRAT replay
would be strictly stronger" option is not on the table. `native_decide` on a
kernel-proved checker is the only route, exactly as for `bv_decide` itself.
Any PR should state this rather than present it as a deferred improvement.

---

## C. `defs-layer/` — the certificate repository's definitional layer

**Status: COMPILES (checked inside the formal-conjectures clone, not as a
standalone package — see the caveat).**

`defs-layer/` is the proposed package shape for the future certificate
repository, in algal's arrangement: a `lean-toolchain` pinning
`leanprover/lean4:v4.27.0`, a `lakefile.toml` requiring `formal_conjectures`,
and `KrennGuDiagonal/Defs.lean` fixing the three target propositions in one
place so the goal cannot drift. It mirrors the job of algal's
`KrennGuCertificate/OfficialBridge.lean` — pin the pinned dependency's
conventions rather than restate them.

It contains three sorry-free bridge theorems, verified:

```
KrennGuDiagonal.targetDomain_of_targetNZ  [propext]
KrennGuDiagonal.targetC_of_targetDomain   [propext, Classical.choice, Quot.sound]
KrennGuDiagonal.target_trinary_int        [propext, Classical.choice, Quot.sound]
```

The first is the implication that makes `EqSystemNZ` the right thing to prove
(the unnormalised system is the weaker hypothesis, so its non-existence
statement is the stronger one). The other two show a single domain-level result
delivers the `ℂ` and `{-1,0,1} ⊆ ℤ` readings for free.

**Caveat, stated plainly.** A standalone `lake build` of this package was
**not** run. Even with a local `path =` require, Lake resolves
formal_conjectures' dependency graph from scratch and re-clones mathlib
(~5 GB); with 29 GiB free that is not worth spending for a weaker check. The
identical file was instead compiled inside the already-built clone via
`lake env lean`, exit 0, no errors and no linter warnings. So `defs-layer/`'s
**Lean content is verified** and its **packaging is proposed but unbuilt**.
Details in `../work/DEFS_BUILD.txt`.

---

## D. What is NOT built

Everything in `architecture.md` §3–§6, i.e. the entire mathematical bridge:

* `haf`, `haf_cons`, the fuel lemma (§3.1–3.3)
* `pmSumList_diagonal`, the product formula (§3.4) — **the highest-risk item**
* FREE / B1 / B2 (§4)
* `pullWeights` and `eqSystemNZ_pullWeights` (§5.3) — **second-highest risk**
* the semantic ledger and `replayExact` (§6.3)
* the nine `*_clause_true` lemmas (§6.2)
* the 4096 → 87 coverage table (§5.2)
* the final assembly (§8.1)

No `sorry`-free claim is made about any of them, and no skeleton file asserts
any of them.

---

## E. Reproducing

```bash
# A -- the statement
cd work/fc && lake exe cache get
python3 ../splice.py
lake --wfail build FormalConjectures.Paper.MonochromaticQuantumGraph

# B -- the UNSAT layer (no dependencies; needs only the toolchain)
cd skeleton/lrat-probe && lake build LratProbe
lake env lean LeanCheck.lean          # axiom audit

# regenerate the LRAT from the audited CNFs
bash work/make_lrat.sh                # 6.4 s for all 87

# the 4096-case cost measurement behind architecture.md sec. 5.1
python3 work/measure_4096.py          # 464 s, checkpointed to measure_4096.jsonl
```

`work/fc/FormalConjectures/Paper/MonochromaticQuantumGraph.lean.orig` is the
untouched upstream file; `splice.py` always re-splices from it, so the operation
is idempotent.
