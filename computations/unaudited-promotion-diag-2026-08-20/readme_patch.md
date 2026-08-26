# `README.md` — exact replacement text

> **STAGED — not applied.** Drafted 2026-08-20 by lane P2-diag at pinned
> repository HEAD `5377acdc43992e8eaaf4f17f4f1068b7242dfe73`. Three patches.
> Old text is quoted verbatim from `README.md` at that HEAD; apply only after
> the proof document is committed and `SUPERSESSION-2026-08-20-01` is
> appended.

---

## Patch 1 — the status paragraph (`README.md` lines 13–23)

### CURRENT TEXT

```markdown
**Status (2026-08-14): the conjecture is not yet proved here.** What
exists is a rigorous conditional proof spine and a sharply identified
local seed obstruction (the *balanced chart square*, below). Closing that
seed at `h = 3` is necessary but not by itself sufficient: the global proof
also needs its fully augmented physical comparison, a branch-complete
uniform prolongation `PAComp(h)`, and promotion of every non-lift to the
actual source terminal. The clean-pair descent now has both an exhaustive
symbolic checker and an independent from-scratch audit. Claims are labelled
**proved** (checker + audit), **P-prose** (complete mathematical proof with
verification debt), **generation-side** (checker, not yet independently
re-audited), or **open**.
```

### NEW TEXT

```markdown
**Status (2026-08-20): the conjecture is not yet proved here.** What
exists is a rigorous conditional proof spine, a sharply identified local
seed obstruction (the *balanced chart square*, below), and — new at this
revision — one closed stratum at the smallest open order: **the
block-diagonal (classical monochromatic-edge) case of `n = 8, d = 3` is
proved**, over any field, with machine-checked UNSAT certificates and two
independent audits. **The order itself stays open.** The general
bicoloured `n = 8, d = 3` case — which is what the `formal-conjectures`
registry item `eqSystem8_no_solution_d3` states, and what this program
targets — is not resolved by it; the pieces still missing there are the
non-diagonal transfer (the product factorisation that carries the
diagonal proof has no bicoloured analogue), the residual support family
(R) at `25 <= m <= 28`, and the global induction's own hypotheses. Closing the balanced-chart seed at `h = 3` is
necessary but not by itself sufficient: the global proof also needs its
fully augmented physical comparison, a branch-complete uniform
prolongation `PAComp(h)`, and promotion of every non-lift to the actual
source terminal. The clean-pair descent now has both an exhaustive
symbolic checker and an independent from-scratch audit. Claims are
labelled **proved** (checker + audit), **P-prose** (complete mathematical
proof with verification debt), **generation-side** (checker, not yet
independently re-audited), or **open**.
```

---

## Patch 2 — a new bullet in *Established core and verification status*

Insert **immediately after** the existing "Six-site obstruction" bullet
(`README.md` lines 47–54), which is unchanged:

### CURRENT TEXT (context, unchanged)

```markdown
- **Six-site obstruction.** No exact ternary source exists on six sites
  with arbitrary complex endpoint-ordered matrices — the `(6,3)` case of
  the general bicoloured model. Proof: a 19-type rank/defect census with
  exact certificates; independently audited (from-scratch re-encoding,
  byte-identical CNF digests, hand re-derivation of the census).
  `proofs/six-site-arbitrary-complex-obstruction.md`. (See *Related
  work* for the concurrent independent Lean certificate of the
  normalized fiber of this statement.)
```

### NEW TEXT (inserted after it)

```markdown
- **Eight-site block-diagonal obstruction.** No exact ternary source
  exists on eight sites when every pair matrix is diagonal,
  `A_uv = diag(t^0, t^1, t^2)` — three independent edge-weight
  functions. The statement holds over **any field, of any
  characteristic**, and in the strengthened *unnormalised* form: all
  three constant-word amplitudes nonzero and all mixed amplitudes zero
  is already impossible, so no algebraic closure or amplitude rescaling
  is used. The classical edge-coloured (single-cell) Krenn–Gu statement
  at `n = 8` is the corollary. Proof: a free-set-triple normal form
  reducing to a 4,096-case ledger (87 orbits), plus a vanishing-pattern
  Boolean abstraction whose nine clause families are each one-line-sound
  in every characteristic and which allows *all* cancellation — so UNSAT
  is nonexistence over any field. UNSAT on all 4,096 cases and all 87
  orbits, five solvers agreeing, every orbit proof verified by drat-trim
  (truncated, corrupted and cross-case proofs all rejected); `n = 6`
  closes the same way with independent Gröbner corroboration in five
  characteristics, and `n = 4` is correctly satisfiable — the
  exceptional source survives, as it must. Independently audited at the
  promotion gate (from-scratch re-derivation of every clause validity,
  inverted-polarity re-encoding, five-engine re-solve).
  `proofs/eight-site-diagonal-obstruction.md`. **Scope:** the general
  bicoloured `n = 8, d = 3` case — the `formal-conjectures` registry
  statement — is untouched and remains this program's target; and this
  machine does *not* extend past `n = 8` — at `n = 10` the exact level
  rises to `X_6` and the abstraction is satisfiable there, so `n >= 10`
  is open for it.
```

---

## Patch 3 — the "smallest open case" sentence (`README.md` lines 40–44)

### CURRENT TEXT

```markdown
`n >= 6`** — the statement this program attacks. The smallest open case
anywhere, in this repository's formulation and in DeepMind's
`formal-conjectures` registry, is `n = 8, d = 3`
(`eqSystem8_no_solution_d3`).
```

### NEW TEXT

```markdown
`n >= 6`** — the statement this program attacks. The smallest open case
anywhere, in this repository's formulation and in DeepMind's
`formal-conjectures` registry, is `n = 8, d = 3`
(`eqSystem8_no_solution_d3`, whose Lean statement is the general
bicoloured one — its edge type carries both endpoint colour indices). It
remains open. Its **block-diagonal** stratum — the classical
monochromatic-edge model — is closed here, with the edge-coloured
statement at `n = 8` as a corollary
(`proofs/eight-site-diagonal-obstruction.md`).
```

---

## Not patched, and why

* **The *Related and concurrent work* section is left exactly as it stands.**
  The proof document credits Bogdanov, Chandran–Gajjala(–Illickan), AlphaProof
  Nexus, algal's `(6,3)` Lean certificate (PR #4610) and the PR #4661 anchor
  lemma in the same terms this section already uses; nothing in the new theorem
  changes any attribution, and the concurrent-work claims are the ones most
  likely to drift if reworded. No novelty is claimed against any of them
  (`notes/2026-08-15-conventions-and-hazards.md`, item 10).
* **The *Verification discipline* paragraph is left as it stands** — its
  sentence "Directories named `computations/unaudited-*` contain external
  probes, audits, and repair candidates that have **not** passed the
  repository's audit gauntlet; they are inputs, not spine" stays literally true
  of the W29/A9/P2-diag lanes until the proof document is committed under
  `proofs/`.
