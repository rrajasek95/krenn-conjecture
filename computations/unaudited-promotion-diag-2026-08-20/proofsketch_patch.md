# `PROOF-SKETCH.md` — exact replacement text

> **STAGED — not applied.** Drafted 2026-08-20 by lane P2-diag at pinned
> repository HEAD `5377acdc43992e8eaaf4f17f4f1068b7242dfe73`. Four patches.
> Old text is quoted verbatim from `PROOF-SKETCH.md` at that HEAD; apply only
> after the proof document is committed and `SUPERSESSION-2026-08-20-01` is
> appended.

---

## Patch 1 — the synchronisation stamp (`PROOF-SKETCH.md` lines 3–7)

### CURRENT TEXT

```markdown
*Proof-architecture companion to the [README](README.md). Statements
are labelled **[P]** proved (exact checker and independent audit),
**[G]** generation-side (checker-backed, awaiting independent
re-audit), or **[O]** open. Full statements and certificates are in the
linked repository notes. Last synchronized: 2026-08-14.*
```

### NEW TEXT

```markdown
*Proof-architecture companion to the [README](README.md). Statements
are labelled **[P]** proved (exact checker and independent audit),
**[G]** generation-side (checker-backed, awaiting independent
re-audit), or **[O]** open. Full statements and certificates are in the
linked repository notes. Last synchronized: 2026-08-20.*
```

---

## Patch 2 — the known-partial-results paragraph (`PROOF-SKETCH.md` lines 62–71)

### CURRENT TEXT

```markdown
already for complex weights and bicoloured multigraphs. In the
opposite regime of many colours, the automated formal-proof system of
[6] certified the diagonal cases $n = d \in \{4, 6, 10\}$ together
with an explicit certificate family for $d = n$ at every even $n$, and
further instances with $d > n$; a solver-free argument over arbitrary
integral domains [12] yields the general bound $k_{\max}(n) \le n-2$.
A tensor-algebraic no-go theorem by Krenn, Firsching, Tsoukalas,
Gajjala, Gu, and Chaudhuri is announced as in preparation in [6]. The
smallest case left open by all of the above — here and in the
`formal-conjectures` registry [7] — is $n = 8$, $d = 3$.
```

### NEW TEXT

```markdown
already for complex weights and bicoloured multigraphs. In the
opposite regime of many colours, the automated formal-proof system of
[6] certified the diagonal cases $n = d \in \{4, 6, 10\}$ together
with an explicit certificate family for $d = n$ at every even $n$, and
further instances with $d > n$; a solver-free argument over arbitrary
integral domains [12] yields the general bound $k_{\max}(n) \le n-2$.
A tensor-algebraic no-go theorem by Krenn, Firsching, Tsoukalas,
Gajjala, Gu, and Chaudhuri is announced as in preparation in [6]. The
smallest case left open by all of the above — here and in the
`formal-conjectures` registry [7] — is $n = 8$, $d = 3$.

That case remains open. One of its strata is now closed.
**Theorem 1.2 [P] (`proofs/eight-site-diagonal-obstruction.md`).** Over
any field, of any characteristic, no *block-diagonal* ternary weighting
of $K_8$ — one in which every pair matrix is
$A_{uv} = \operatorname{diag}(t^0_{uv}, t^1_{uv}, t^2_{uv})$, i.e. the
weights are supported on $i = j$, the classical monochromatic-edge model
of [1] — has all three constant-word amplitudes nonzero and all mixed
amplitudes zero. Equivalently, no unnormalised
$\sum_c \lambda_c e_c^{\otimes 8}$ with every $\lambda_c \neq 0$ is
reachable in that model; no algebraic closure or amplitude rescaling is
used. The classical *edge-coloured* Krenn–Gu statement at $n = 8$ is the
corollary. The proof is a free-set-triple normal form (three forced
distinct B2 witness sites, a 4,096-case ledger in 87 orbits) followed by
a vanishing-pattern Boolean abstraction that allows all cancellation, so
its UNSAT is nonexistence over every field at once; every orbit
certificate is verified by `drat-trim`, and the same machine closes
$n = 6$ (with Gröbner corroboration) and correctly *fails* at $n = 4$,
where the exceptional weighting exists.

Two boundaries matter. **The general bicoloured case at $n = 8$ is
untouched**: that is the statement of the registry item
`eqSystem8_no_solution_d3` of [7] — whose Lean edge type carries both
endpoint colour indices, so its weights depend on the colours at both
ends — and it remains the target of this document. (Its constant words
are normalised to $1$, which the amplitude-nonzero form above covers a
fortiori on the diagonal sub-case.) And the machine does not reach
$n \geq 10$: there the exact level rises from $X_4$ to $X_6$, and the
abstraction is satisfiable.
```

---

## Patch 3 — §7.1's `[U]` preamble and the diagonal statement (`PROOF-SKETCH.md` lines 700–706)

### CURRENT TEXT

```markdown
A parallel decomposition of Problem 3.3, developed on 2026-08-15 and
recorded with its evidence trail in
`notes/2026-08-15-resolution-master-plan.md`, attacks the same gap from
the support side. Its status labels are as in the rest of this
document, with one addition: **[U]** marks results established by
exhaustive exact computation in `computations/unaudited-*` directories
that have not yet passed this repository's independent audit gauntlet.
```

### NEW TEXT

```markdown
A parallel decomposition of Problem 3.3, developed on 2026-08-15 and
recorded with its evidence trail in
`notes/2026-08-15-resolution-master-plan.md`, attacks the same gap from
the support side. Its status labels are as in the rest of this
document, with one addition: **[U]** marks results established by
exhaustive exact computation in `computations/unaudited-*` directories
that have not yet passed this repository's independent audit gauntlet.

One branch of this decomposition has since left **[U]** status. The
*block-diagonal* stratum at $n = 8$ — every pair matrix diagonal, so
that a word's amplitude factorises as
$\Phi(w) = \prod_c \operatorname{haf}(t^c \mid w^{-1}(c))$ — is
**[P] empty**, over any field: `proofs/eight-site-diagonal-obstruction.md`.
Two consequences for the support programme below. First, the
single-cell diagonal regime that the budget forces at $m = 3n/2$ is
refuted at $n = 8$ by a second, independent route, one that does not go
through the properly 3-edge-coloured cubic classification. Second, and
limiting: the diagonal proof consumes the product factorisation, which
no bicoloured $A_{uv}$ provides, so it does **not** shorten the
residual family (R) at $25 \leq m \leq 28$, where the blocks are full.
The remaining $n = 8$ gap is exactly the non-diagonal part.
```

---

## Patch 4 — the open-item table (`PROOF-SKETCH.md` lines 679–688)

### CURRENT TEXT

```markdown
| open item | status |
|---|---|
| Conjecture 6.2 (balanced chart-square local seed) | **[O]** — both branches under active attack |
| physical response-KS to cap-`r0` comparison and augmented readouts | **[O]** — first missing source-labelled operation arrow |
| remaining window faces and placement maps | **[G/O]**; named finite pieces are checked, physical comparison is absent |
| uniform `PAComp(h)` prolongation and rootless/inactive/face-zero routing | **[O]**; coefficient half **[P]**, physical half open |
| terminal promotion / source-grade essential surjectivity | **[O]** — finite cokernel dual is not yet an accepted physical terminal |
| clean-pair descent verification | **[P]** — proof page, substantive checker, and independent audit complete |
| support-theoretic reduction of Problem 3.3 (Section 7.1) | **[O]** — reduced to a per-support SAT decision under (SC); three regimes proved empty; general decision running with independent implementations |
| independent re-audit of the newest layer | in progress (`computations/unaudited-*`) |
```

### NEW TEXT

```markdown
| open item | status |
|---|---|
| Conjecture 6.2 (balanced chart-square local seed) | **[O]** — both branches under active attack |
| physical response-KS to cap-`r0` comparison and augmented readouts | **[O]** — first missing source-labelled operation arrow |
| remaining window faces and placement maps | **[G/O]**; named finite pieces are checked, physical comparison is absent |
| uniform `PAComp(h)` prolongation and rootless/inactive/face-zero routing | **[O]**; coefficient half **[P]**, physical half open |
| terminal promotion / source-grade essential surjectivity | **[O]** — finite cokernel dual is not yet an accepted physical terminal |
| clean-pair descent verification | **[P]** — proof page, substantive checker, and independent audit complete |
| block-diagonal stratum at $n = 8$ | **[P]** — empty over any field; machine-checked UNSAT certificates, two independent audits; the classical edge-coloured $n = 8$ statement follows |
| general bicoloured $n = 8$, $d = 3$ | **[O]** — the `formal-conjectures` registry statement (`eqSystem8_no_solution_d3`; both endpoint colour indices) and this program's target. The diagonal proof does not transfer — it consumes the product factorisation — and the residual support family (R) at $25 \leq m \leq 28$ is untouched by it |
| the same machine at $n \geq 10$ | **[O]** — refuted as an extension: the exact level rises to $X_6$ at $n = 10$ and the abstraction is satisfiable there |
| support-theoretic reduction of Problem 3.3 (Section 7.1) | **[O]** — reduced to a per-support SAT decision under (SC); three regimes proved empty; general decision running with independent implementations |
| independent re-audit of the newest layer | in progress (`computations/unaudited-*`) |
```

---

## Not patched, and why

* **§7.1's item 5 (family (R) at $25 \le m \le 28$) is untouched.** The
  diagonal theorem does not bear on it: family (R) is defined by *full*
  blocks on the complement of `Gamma`, which is the opposite of diagonal, and
  the transfer would need the product factorisation that only diagonality
  supplies. Patch 3 says so explicitly rather than leaving the reader to infer
  a reach the theorem does not have.
* **§7.1's item 4 and the "single-cell diagonal regime" sentence of the
  *Budget* paragraph are untouched.** The existing text — "at $m = 3n/2$ the
  source is forced into the single-cell diagonal regime on a properly
  3-edge-coloured cubic graph, where it is refuted exhaustively" — remains
  correct as written; Patch 3 records that this regime now has a second,
  independent refutation at $n = 8$ rather than rewriting the first.
* **The *Acknowledgements of independent and concurrent work* section is left
  exactly as it stands**, for the same reason as in `readme_patch.md`: no
  attribution changes, and reworded credit is the likeliest place for drift.
