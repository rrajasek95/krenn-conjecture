# `formal/n8-diagonal` — the Lean side of the eight-site block-diagonal obstruction

> **STAGED, INCOMPLETE — lane L1, 2026-08-20.** Laid out as it should land in
> `rrajasek95/krenn-conjecture`. Not committed; not submitted anywhere. The
> theorem this subtree is being built toward is **not yet proved in Lean**; see
> `BUILD-STATUS.md` for exactly what compiles today.

The mathematical statement, its two audits, and its certificates already live
in this repository:

| what | where |
|---|---|
| the proof of record | `proofs/eight-site-diagonal-obstruction.md` (Theorem 1.2) |
| the certificates | `computations/certificates/n8_diagonal/` (87 orbit CNF/DRAT pairs, ledger, replay) |
| phase-one Lean ledger | `formal/FORMALIZATION.md`, `formal/MonochromaticQuantumGraphKeyLemmas.lean` |

This directory adds the machine-checked Lean proof of the same statement,
against the *upstream* `formal-conjectures` definitions of `WeightsN`,
`EqSystemN` and `pmSumN`, so that the theorem proved here is literally the
proposition a `formal-conjectures` entry would carry.

## Layout

```
formal/n8-diagonal/
  lean-toolchain          leanprover/lean4:v4.27.0   (what formal-conjectures pins)
  lakefile.toml           requires google-deepmind/formal-conjectures at a pinned rev
  N8Diagonal.lean         root
  N8Diagonal/
    Haf.lean              hafnians: no new recursion, they are pmSumList at a constant word
    Product.lean          the product formula (equation (2) of the proof document)
    Normal.lean           H1 / H2 / the B2 witness (Lemma 3.4)
    Symm.lean             hafnians are symmetric functions; Laplace at an arbitrary site
  encoder/
    l1_enc.py             canonical-numbering CNF emitter (base variables first)
    emit_canonical.py     emits the 87 orbit CNFs + native-LRAT certificates
    emit_cores.py         extracts UNSAT cores and re-certifies them
    gen_lean_core.py      renders a core refutation as Lean literals
  artifacts/cores/        87 core CNF + LRAT pairs, index.json, SHA256SUMS.txt
```

## Toolchain

Everything is pinned to what `formal-conjectures` pins for itself:

* Lean `leanprover/lean4:v4.27.0`
* Mathlib `a3a10db0e9d66acbebf76c5e6a135066525ac900`
* `formal_conjectures` at the revision in `lakefile.toml`

The same revisions are used by `algal/krenn-gu-6x3-certificate` (PR #4610) and
by `KitaKen1/monochromatic-quantum-graphs-lean` (PR #4659), so all three are
toolchain-compatible.

## Build

From a fresh clone of the repository:

```bash
cd formal/n8-diagonal
lake exe cache get          # Mathlib oleans; ~20 min cold, changes build time only
lake build N8Diagonal
```

`lake exe cache get` is strongly advised: without it Lake builds Mathlib from
source. This subtree is otherwise self-contained — it needs no other directory
of this repository to compile.

**Note on the host.** The v4.27.0 toolchain ships an x86_64 binary. On Apple
silicon every Lean/Lake invocation runs under Rosetta 2, and the *first* run of
a cold `lean` binary stalls for minutes with no output while Rosetta
AOT-translates it. That is not a hang; do not kill it.

## Replay of the certificates

The Lean proof consumes UNSAT cores, not the full orbit formulas. The cores are
subsets of the formulas the audited certificates refute, and a subset of an
unsatisfiable set is unsatisfiable, so this never strengthens the claim. To
regenerate and re-verify the whole chain:

```bash
python3 encoder/emit_canonical.py 8 z0   # 87 canonical CNFs + native LRAT   (~17 s)
python3 encoder/emit_cores.py            # extract cores, re-certify, check subsets
shasum -a 256 --check artifacts/cores/SHA256SUMS.txt
```

`emit_canonical.py` refuses to write unless every emitted formula has the same
clause **set** as the audit encoder's (`computations/certificates/n8_diagonal/encoders/`)
under the variable bijection — the canonical numbering is a renaming, not a
re-encoding. `emit_cores.py` refuses to write unless every core clause occurs
verbatim in the corresponding full formula.

Tools used: CaDiCaL 3.0.1 and Marijn Heule's `drat-trim` / `lrat-check`, both
from `computations/unaudited-hygiene-h1-2026-08-15/tools/`.

**LRAT dialect.** The certificates are produced by
`cadical <cnf> <lrat> --lrat=true --no-binary --checkproof=2`, not by
`drat-trim -L`. Lean's LRAT checker rejects `drat-trim -L` output at this scale
even though drat-trim and its own `lrat-check` both verify it; and `drat-trim -f`
emits LRAT that `lrat-check` itself rejects. Use the CaDiCaL route.

## Status

See `BUILD-STATUS.md`. In one line: the algebraic bridge through the product
formula, the normal-form facts and general-position Laplace is built and
`sorry`-free; the clause-family ledger, the case-coverage transport and the
final assembly are not.
