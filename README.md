# The Krenn–Gu conjecture: a descent program

This repository is an active research program on the **Krenn–Gu
conjecture** on monochromatic quantum graphs, in its strongest (general
bicoloured, complex-weighted) form. It contains proved theorems with
machine-checked certificates, a conditional global proof architecture, an
exhaustive registry of closed and refuted routes, and the current open
frontier — stated precisely.

**A rough end-to-end proof sketch, with every step labelled by its
verification status, is in [PROOF-SKETCH.md](PROOF-SKETCH.md).**

**Status (2026-08-13): the conjecture is not yet proved here.** What
exists is a rigorous conditional proof spine whose remaining obstruction
has been compressed to one sharply defined local comparison theorem (the
*balanced chart-square saturation theorem*, below), together with a
proved descent mechanism and a proved terminal contradiction. Nothing in
this README claims more than the cited artifacts establish; claims are
labelled **proved** (checker + audit), **generation-side** (checker, not
yet independently re-audited), or **open**.

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
(`eqSystem8_no_solution_d3`).

## Proved results (checker + independent audit)

- **Six-site obstruction.** No exact ternary source exists on six sites
  with arbitrary complex endpoint-ordered matrices — the `(6,3)` case of
  the general bicoloured model. Proof: a 19-type rank/defect census with
  exact certificates; independently audited (from-scratch re-encoding,
  byte-identical CNF digests, hand re-derivation of the census).
  `proofs/six-site-arbitrary-complex-obstruction.md`. (See *Related
  work* for the concurrent independent Lean certificate of the
  normalized fiber of this statement.)
- **Exact clean-pair descent.** Given an *active clean pair* at order
  `n`, deleting its two sites yields the same ternary GHZ system at
  order `n - 2`. Descent plus the six-site obstruction closes the
  induction; every remaining difficulty is the existence of the active
  clean pair.
- **Branch funnel at `h = 3`.** The axis-pure complete-source branch is
  empty; off-axis support produces an active private-site fan; the
  four-good fan branch yields a clean cap; closed-shore recurrences
  terminate into a single trapped pure-colour-coloop branch. Verified by
  exact censuses (e.g. the complete 461,700-packet activity/orbit
  inventory; the determinant-bright entry step is proved exhaustively
  over all 3^15 sign patterns).
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

**The single remaining local obstruction** is now explicit. In the
ordered chart basis `(A_[a|b], A_[b|a], B, C)` of a fixed four-site
residual window, the class

    z = (1, 1, -1, -1)

is simultaneously: the Gate-II direction charge, the unique missing
direction of the balanced recurrent K_{2,2} companion square, and the
chart-sign class of the all-order Bianchi comparison
(`notes/uniform-balanced-chart-square-master-obstruction.md`). After a
shore-sign gauge, `z` is the constant augmentation class. The open
theorem is a win-win alternative:

> **Balanced chart-square saturation (open).** Construct a source-valid
> relative-C4 cell with boundary `z` (natural in restriction,
> reinsertion, and chart overlap) — or extend the normalized dual
> `psi_z` to the accepted physical terminal, which yields the required
> contradiction by the Fredholm branch.

Downstream of this single family, the already-built ladder (occurrence,
residue, `W`, ridge, moment tower via a proved Rodrigues-type
calculation) supplies the clean cap, and descent finishes the ternary
upper bound. A separate uniformity-in-`h` layer (association-scheme
spectral identities, exact and polynomial in `h`) promotes the local
construction to all orders; its coefficient half is verified, its
physical half is the same open construction.

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
- **Independent Lean certificate for (6,3).** A complete Lean 4 proof of
  the normalized `(6,3)` fiber (`eqSystem6_no_solution_d3` over C) was
  developed concurrently and independently (formal-conjectures PR #4610);
  our six-site theorem keeps the palette-uniform general statement, and
  the two censuses are genuinely different decompositions —
  corroboration, not duplication. The solver-free `D <= N-2`
  anchor lemma of PR #4661 subsumes both projects' forced-column lemmas
  and is the right citation for that step.
- **YesterdaysLemon/krenn-gu-research** is an independent program with a
  complementary claim ledger (rank-stratum exclusions, matrix-unit
  holonomy); its eight-vertex phase-normal-form witness and its
  minimal-cofactor matching-covered theorem have been cross-validated
  against this repository's obstruction machinery (see
  `computations/unaudited-external-u7d-stress-test-2026-08-13/` and
  `unaudited-external-u7h-import-audit-2026-08-13/`), with full
  agreement where the formalisms overlap.

## Layout

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
