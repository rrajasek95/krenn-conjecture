# Proof sketch: the Krenn–Gu conjecture by clean-pair descent

*A rough end-to-end sketch of the intended proof, with every step
labelled **proved** (checker + independent audit), **generation-side**
(checker-backed, awaiting independent re-audit), or **open**. This is a
companion to the [README](README.md); the authoritative technical
statements live in the linked notes. Last synchronized: 2026-08-13.*

---

## 0. Statement and reduction

For even `n` and dimension `d`, assign to each edge `uv` of `K_n` a
complex matrix `A_uv(i,j)` (general bicoloured model). The
perfect-matching tensor is

    H(A) = Σ_{M perfect matching} ⊗_{uv ∈ M} A_uv .

**Conjecture (Krenn–Gu, strong form).** For even `n ≥ 6` and `d ≥ 3`
there is no `A` with `H(A) = Δ_{n,d} = Σ_{c=1}^d e_c^{⊗n}`.

**Reduction to ternary (proved, elementary).** Projecting onto any three
colours sends `Δ_{n,d}` to `Δ_{n,3}`. So it suffices to prove: **no
ternary source exists for even `n ≥ 6`.** Together with the known `d = 2`
constructions and the `n = 4` exceptional analysis, this yields the full
`k_max(n)` formula.

## 1. The global induction

    ternary source at order n
            │  normalize: maximize protected mutual anchors,
            │             then minimize occupied scalar support
            ▼
    find an ACTIVE CLEAN PAIR
            │  exact cap/deletion descent          [proved]
            ▼
    ternary source at order n − 2
            │  iterate
            ▼
    six-site contradiction                          [proved]

- **Base case (proved + audited).** No exact ternary source on six
  sites, for arbitrary complex endpoint-ordered matrices:
  `proofs/six-site-arbitrary-complex-obstruction.md` (19-type census,
  exact certificates; independently audited; corroborated by a
  concurrent independent Lean 4 certificate of the normalized fiber).
- **Descent step (proved).** If an active clean pair exists, deleting
  its two sites reproduces the ternary GHZ system at order `n − 2`.
- Everything else in the proof exists to manufacture the active clean
  pair — or to derive a contradiction directly when it cannot be
  manufactured.

## 2. The local funnel at a minimal counterexample (proved /
generation-side)

At a normalized minimal counterexample, exact branch analysis funnels
all difficulty into one place:

1. the axis-pure complete-source branch is **empty** (proved; exhaustive
   cell censuses through three simultaneous cells, ~2.1M
   specializations, all source units);
2. off-axis support produces an **active private-site fan**
   (generation-side; the determinant-bright entry step is proved
   exhaustively over all 3^15 sign patterns);
3. a four-good fan already yields a clean cap (proved);
4. closed-shore recurrences terminate — the termination combinatorics
   (5,141 inputs, 446 saturated concepts, six types up to symmetry) is
   proved — into a single **trapped pure-colour-coloop branch**;
5. that last branch, together with the rootless/inactive comparison of
   the parallel lane, reduces to the single obstruction class of §4.

## 3. The machinery: source-constrained homological calculus
(generation-side, partially audited)

The engine is an equivariant Cartan–Spencer calculus over the
principal-parts resolution of the source equations, with a hard typing
discipline: **every map must be source-provenant** — a literal,
label-preserving consequence of the equations (word, fine degree,
repeated grade, provenance all retained). Exact negative results (the
*fencing theorems*) show this discipline is not pedantry but the entire
content: the fully saturated all-matching machinery — Koszul
resolutions, diagonal contractions, all flattening ranks at once, pure
normalizations, Reynolds averaging — provably cannot reach the
obstruction class below, and unconstrained homological algebra proves
nothing here.

Key verified components: the Ward covariance of the physical
presentation; the endpoint-odd Cartan prism and its `−δ` secondary
transfer (audited: the `−δ` pinning is forced and content-hashed); the
output cell `M_v = −O_α + K` on the normalized slice, whose terminal
(eta/sigma) law is now derived from the physical ridge rather than
stipulated; the anchor-fibre generator/separator dichotomy; and the
association-scheme spectral identities of §5.

## 4. The single remaining obstruction: the balanced chart square
(open)

All surviving difficulty is one four-coordinate representation class.
On a fixed four-site residual window with chart columns
`(A_[a|b], A_[b|a], B, C)`:

    z = (1, 1, −1, −1)

is simultaneously (exact checker,
`notes/uniform-balanced-chart-square-master-obstruction.md`):

- the Gate-II direction charge `(2, −1, −1)` after chart identification;
- the unique missing direction of the balanced recurrent `K_{2,2}`
  companion square;
- the chart-sign class `(1,−1)_chart ⊗ (1,1)_matching` of the all-order
  Bianchi comparison — exactly the class that survives every
  matching-side contraction (the fencing theorems).

After a shore-sign gauge, `z` becomes the constant augmentation class:
the entire local problem is to **produce one source-valid square-output
cell with nonzero augmentation**.

> **Balanced chart-square saturation theorem (open).** In every physical
> fixed-tail occurrence, construct a source-valid relative-C4 cell with
> boundary `z ⊗ (local C4 tail)`, natural under restriction,
> reinsertion, chart overlap, target, `q`, anchor, `W`, residue, and
> ridge — **or** extend the normalized dual `ψ_z = ¼(1,1,−1,−1)` to the
> accepted physical terminal.

Both branches finish the proof: a filler closes Gate II, the recurrent
`K_{2,2}` obstruction, and the chart-odd Bianchi class at every order;
a terminal extension of `ψ_z` is a Fredholm separator killing the
hypothetical counterexample's support directly. Exact counterguards
(checker-backed) already rule out every known shortcut: pure target
normalization, scalar localization of single C4 factors, all-matching
Koszul complexes, the existing response/Cartan/q-Jacobian rows, and
discarding the signed-Weyl Leibniz boundary.

## 5. Uniformity in `h` and the moment tower (coefficient half
verified; physical half = §4)

The construction must be natural in the order `h`. The coefficient
layer is representation-stable in a strong verified sense: transfer
residuals land in fixed padded partition shapes (multiplicity one), and
every structural constant is an exact polynomial in `h` (e.g. the
two-switch eigenvalue `h² − 3h + 1` on `[2h−2, 2]`; composite constants
verified out of sample through `h = 12`). Two verified caveats shape the
argument: stability is per composed transfer step, and the spectator
suspension raises the residual level by one — so promotion to all
orders is argued stepwise, not induced along suspension. Given the §4
family, the two oriented four-cut primitives descend to one carrier
with `dΓ = r − 2q`, and a proved Rodrigues-type moment calculation
kills the entire higher-moment tower, supplying the active clean cap.

## 6. Assembly

1. Minimal counterexample → normalized representative (§1).
2. Local funnel (§2) → either a terminal output directly, or the
   balanced square (§4).
3. §4, either branch → clean cap (via §5) or Fredholm contradiction.
4. Clean-pair descent (§1) lowers `n` by 2; iterate to the six-site
   contradiction.
5. The ternary upper bound plus the known lower bounds and the `n = 4`
   analysis give the full conjecture and the `k_max(n)` formula.

## 7. What remains, exactly

| item | status |
|---|---|
| balanced chart-square theorem (§4) | **open** — under active attack from both branches |
| odd-side faces (pointed conormal, primitive cap, ridge placement) and two E14 placement maps | generation-side reductions done; constructions mechanical, in progress |
| per-step uniformity argument (§5) | coefficient half verified; physical half rides on §4 |
| independent re-audit of the 2026-08-12/13 layer | in progress (see `computations/unaudited-external-spine-audit-2026-08-13/` and repair directories) |

The honest summary: **one open construction with a two-branch win-win,
mechanical residue, and an audit backlog.** Every other route is either
proved, fenced off by an exact negative result, or recorded as
superseded in `notes/proof-route-supersession-audit.md`.
