# The Krenn–Gu conjecture: a descent program

This repository is an active research program on the **Krenn–Gu
conjecture** on monochromatic quantum graphs, in its strongest (general
bicoloured, complex-weighted) form. It contains proved theorems with
machine-checked certificates, a conditional global proof architecture, an
exhaustive registry of closed and refuted routes, and the current open
frontier — stated precisely.

**A rough end-to-end proof sketch, with every step labelled by its
verification status, is in [PROOF-SKETCH.md](PROOF-SKETCH.md).**

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

## The problem

For an even number of parties `n` and dimension `d`, a *quantum graph
experiment* assigns to each pair of parties `uv` a complex matrix
`A_uv(i,j)` (the general bicoloured model: entries may depend on both
endpoint colours, and multi-edges are absorbed into the entries). The
perfect-matching tensor is

    H(A) = sum over perfect matchings M of K_n
           of the tensor product of the A_uv along M.

The experiment is *monochromatic GHZ* when `H(A) = Delta_{n,d} :=
sum_c e_c^{⊗n}`. Krenn and Gu conjectured that for `n > 4` this is
impossible for `d >= 3` (while `d = 2` is achievable, and `n = 4, d = 3`
has the known exceptional witness). Projection onto any three colours
reduces the upper bound to the ternary case: **no ternary source for even
`n >= 6`** — the statement this program attacks. The smallest open case
anywhere, in this repository's formulation and in DeepMind's
`formal-conjectures` registry, is `n = 8, d = 3`
(`eqSystem8_no_solution_d3`, whose Lean statement is the general
bicoloured one — its edge type carries both endpoint colour indices). It
remains open. Its **block-diagonal** stratum — the classical
monochromatic-edge model — is closed here, with the edge-coloured
statement at `n = 8` as a corollary
(`proofs/eight-site-diagonal-obstruction.md`).

## Established core and verification status

- **Six-site obstruction.** No exact ternary source exists on six sites
  with arbitrary complex endpoint-ordered matrices — the `(6,3)` case of
  the general bicoloured model. Proof: a 19-type rank/defect census with
  exact certificates; independently audited (from-scratch re-encoding,
  byte-identical CNF digests, hand re-derivation of the census).
  `proofs/six-site-arbitrary-complex-obstruction.md`. (See *Related
  work* for the concurrent independent Lean certificate of the
  normalized fiber of this statement.)
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
- **Exact clean-pair descent [P].** Given an *active clean pair* at order
  `n`, deleting its two sites yields the same ternary GHZ system at
  order `n - 2`. Descent plus the six-site obstruction closes the
  induction. The proof, standalone symbolic checker, and independent audit
  are complete.
- **Branch funnel at `h = 3` [mixed P/G/O status].** The axis-pure
  complete-source branch is
  empty; off-axis support produces an active private-site fan; the
  four-good fan branch yields a clean cap; closed-shore recurrences
  terminate into a single trapped pure-colour-coloop branch. Verified by
  exact censuses (e.g. the complete 461,700-packet activity/orbit
  inventory; the determinant-bright entry step is proved exhaustively
  over all 3^15 sign patterns). The newest source-labelled comparison and
  arbitrary-packet routing steps remain conditional and are tracked in the
  proof sketch rather than silently included in this bullet.
- **Fencing theorems.** The fully saturated all-matching machinery
  (Koszul resolutions, diagonal contractions, flattening ranks, pure
  normalizations, Reynolds averaging) provably cannot reach the
  remaining obstruction class — it survives every such operation. These
  negative results are exact and checker-backed; they delimit where the
  remaining proof must live.

## The architecture (conditional, generation-side)

A minimal counterexample is normalized (maximum protected anchors, then
minimum support) and attacked through an exhaustive fork whose every
successful branch ends in one of four accepted terminal outputs
(source unit / anchor-safe deletion / four-good pair + descent /
relative generator or Fredholm separator). The machinery is an
equivariant Cartan–Spencer calculus over the principal-parts resolution
of the source equations, with all maps required to be *source-provenant*
(literal, label-preserving consequences of the equations) — ordinary
homological algebra is provably too permissive here, and the discipline
of physical typing is enforced by exact checkers throughout.

**The dominant local seed obstruction** is now explicit. In the
ordered chart basis `(A_[a|b], A_[b|a], B, C)` of a fixed four-site
residual window, the class

    z = (1, 1, -1, -1)

is simultaneously: the Gate-II direction charge, the unique missing
direction of the balanced recurrent K_{2,2} companion square, and the
chart-sign class of the all-order Bianchi comparison
(`notes/uniform-balanced-chart-square-master-obstruction.md`). After a
shore-sign gauge, `z` is the constant augmentation class. The local open
theorem is a win-win alternative:

> **Balanced chart-square saturation (open).** Construct a source-valid
> relative-C4 cell with boundary `z` (natural in restriction,
> reinsertion, and chart overlap) — or extend the normalized dual
> `psi_z` to the accepted physical terminal, which yields the required
> contradiction by the Fredholm branch.

This alternative is the local seed, not the full globally sufficient
statement. The actual target is the source-labelled, anchor-faithful,
`k[beta]`-linear and `rho`-equivariant comparison-or-terminal package
`PAComp(h)`: it must carry occurrence, `q`, residue, `W`, ridge and
Bockstein data; cover rootless, inactive and simultaneous face-zero
strata; be natural at every `h`; and identify a finite separator with the
actual source Macaulay terminal. The coefficient and Rodrigues/moment
parts are largely proved. The abstract all-order Johnson/Hasse coherence and
normalized full-tail coverage are now also proved conditional on one
genuinely natural local comparison; they do not manufacture it. The open
load-bearing pieces are the physical mixed-jet-to-`AugP2` augmentation,
rootless/inactive/face-zero routing, and terminal promotion. See
`notes/2026-08-14-proof-zoomout-and-parallel-attack-plan.md`.

## Verification discipline

Every mathematical claim is backed by an exact-arithmetic checker
(stdlib Python, `Fraction`/integer arithmetic, run under `python3`,
`-O`, and `-I -S`) with a frozen content ledger. Spine changes require
independent re-audit by a fresh agent and are recorded through
`certification/SUPERSESSIONS.md`. The route registry
(`notes/proof-route-supersession-audit.md`) records why every historical
route is closed, guarded, demoted, or live. Directories named
`computations/unaudited-*` contain external probes, audits, and repair
candidates that have **not** passed the repository's audit gauntlet;
they are inputs, not spine.

An adversarial audit culture is load-bearing here: a majority of first
drafts historically failed audit, and the repository's recent history
includes a full external adversarial audit of the proof spine with a
consolidated defect list and subsequent repairs (`computations/
unaudited-external-spine-audit-2026-08-13/` and the
`unaudited-repair*-2026-08-13/` directories).

## Related and concurrent work

- **M. Krenn's problem page** poses the conjecture and prize; L. S.
  Chandran and R. Gajjala with co-authors proved the sparse and
  bounded-degree cases (arXiv:2202.05562, arXiv:2407.00303), and
  I. Bogdanov's matching-index theorem underlies the unweighted case.
- **DeepMind's AlphaProof Nexus** (arXiv:2605.22763) resolved the
  many-colour regime `n = d ∈ {4, 6, 10}`; `eqSystem8_no_solution_d3`
  remains listed open in `formal-conjectures`. A tensor-algebraic no-go
  theorem by Krenn, Firsching, Tsoukalas, Gajjala, Gu, and Chaudhuri is
  in preparation.
- **Further concurrent formal-conjectures work**: an independent
  derivation of the $k_{\max}(n) \le n-2$ bound by djh58 (the
  "Axis-Servant Lemma"), a characteristic-two Pfaffian route
  (PR #4659), and a claimed $(6,4)$ resolution over the complex
  numbers (PR #4664). The four-vertex bicoloured case was settled
  earlier by Mantey via exact Gröbner-basis computation, as recorded
  in arXiv:2407.00303.
- **Independent Lean certificate for (6,3).** A complete Lean 4 proof of
  the normalized `(6,3)` fiber (`eqSystem6_no_solution_d3` over C) was
  developed concurrently and independently (formal-conjectures PR #4610);
  our six-site theorem keeps the palette-uniform general statement, and
  the two censuses are genuinely different decompositions —
  corroboration, not duplication. The solver-free `D <= N-2`
  anchor lemma of PR #4661 subsumes both projects' forced-column lemmas
  and is the right citation for that step.
- **YesterdaysLemon/krenn-gu-research** is an independent, concurrent
  program on the conjecture with a complementary claim ledger
  (systematic rank-stratum exclusions, matrix-unit holonomy). Two of
  its results have been directly valuable here and are gratefully
  acknowledged: its eight-vertex phase-normal-form witness (which
  sharpens the odd-holonomy mechanism's boundary; verified on every
  claimed property in
  `computations/unaudited-external-u7d-stress-test-2026-08-13/`) and
  its minimal-cofactor matching-covered core theorem (audited sound
  and imported in corrected per-fibre form in
  `computations/unaudited-external-u7h-import-audit-2026-08-13/`),
  with full agreement wherever the two formalisms overlap.
- `notes/` — the proof frontier, theorem notes, route registry, and
  adversarial findings (~2,000 documents; the entry points are
  `notes/2026-08-13-three-interface-proof-frontier.md` and
  `notes/uniform-balanced-chart-square-master-obstruction.md`)
- `proofs/` — completed proof documents and their audits
- `computations/` — exact checkers, certificates, and censuses
  (~2,300 artifacts; `unaudited-*` directories are external inputs)
- `certification/` — supersession records for spine changes
- `formal/` — Lean formalization ledger (phase one)
- `references/` — background material

## Citation

A preprint of the six-site theorem and the descent architecture is in
preparation. Until it appears, please cite this repository directly and
note the status labels above; the balanced chart-square theorem is open,
and any use of generation-side material should preserve its label.
