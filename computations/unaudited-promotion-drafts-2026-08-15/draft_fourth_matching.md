> **UNAUDITED DRAFT — not spine.**  Drafted 2026-08-15 at pinned repository
> HEAD `e0c4d7c548dd1b252a87b3fc16e76182a3a0bbfb` (recorded in
> `PINNED_HEAD.txt` beside this file).  It becomes spine only when committed
> through the supersession discipline of `certification/SUPERSESSIONS.md`,
> with the pre-commit items of `draft_promotion_checklist.md` discharged.
> All paths are repository-root-relative.

# The fourth matching in a properly 3-edge-coloured cubic graph, and the support floor

**This theorem is not new.**  It is **Bogdanov's observation** — the standard
three-one-factors lemma — restricted to properly 3-edge-coloured cubic
graphs, and is strictly weaker than the published multigraph form.  Cite
`[Bogdanov2017]`, published as Theorem 1 of `[ChandranGajjala2026]`
(arXiv:2202.05562) and in multigraph form as Theorem 1.7 of
`[ChandranGajjalaIllickan2024]` (arXiv:2407.00303); see
`references/REFERENCES.md`.  **No priority is claimed here for any part of
it**, and none may be claimed later
(`notes/2026-08-15-conventions-and-hazards.md` item 10).  The proof below is
included only because the audit discipline of this repository requires every
consumed statement to be either cited to a checked source or proved inside
the artifact; the same proof is already committed in
`proofs/odd-near-perfect-gadget-obstruction.md` and in
`notes/finite-obstruction.md` §7.

**Proposed status on promotion: `[P]` for the theorem (external prior art
with a self-contained proof); `[P, conditional]` for the support-floor
corollary, which consumes an unaudited budget lemma; the two further
corollaries below are `[recorded, unproved]` and must not be promoted.**

## 1. The theorem

> **Theorem A3.4 (= Bogdanov's observation, cubic case).**  Let `U` be a
> simple cubic graph on `N >= 6` vertices carrying a proper 3-edge-colouring
> `U = M_0 u M_1 u M_2`.  Then `U` has a perfect matching `S` with
> `S not in {M_0, M_1, M_2}`.

`N` is even automatically (each `M_r` is a perfect matching).  Connectivity
and bridgelessness are **not** assumed.  The bound `N >= 6` is sharp: at
`N = 4` the one-factorisation of `K_4` has exactly three perfect matchings.

The published forms, quoted from `references/REFERENCES.md`:

> `[Bogdanov2017]`: *Three pairwise edge-disjoint perfect matchings on an
> even vertex set of size at least six have a fourth perfect matching in
> their union.*

> `[ChandranGajjala2026]` **Theorem 1.**  For a graph `G` which is
> non-isomorphic to `K_4`, `mu(G) <= 2` and `mu(K_4) = 3`.

> `[ChandranGajjalaIllickan2024]` **Theorem 1.7.**  In a coloured
> multi-graph `G_c` with `|V(G)| > 4`, if there exist three monochromatic
> perfect matchings of different colours, then there must be a
> non-monochromatic perfect matching.

Theorem A3.4 is the special case of the first in which the three matchings
are the colour classes of a proper 3-edge-colouring, so that their union is
all of `U`; the third statement covers multigraphs and therefore subsumes it.

## 2. Proof

Write `M_0, M_1, M_2` for the three colour classes; they are pairwise
edge-disjoint perfect matchings with union `U`.

**Step 1 — some pair union is disconnected.**  For `a != b`, `M_a u M_b` is a
disjoint union of alternating even cycles.  If it has at least two
components, let `C` be one of them and put

```text
S = { e in M_a : e subset C }  u  { e in M_b : e not subset C }.
```

`S` is a perfect matching, and it differs from `M_a` (it uses `M_b` outside
`C`) and from `M_b` (it uses `M_a` inside `C`); it differs from `M_c` because
`M_c` is edge-disjoint from `M_a u M_b`.  Done.

**Otherwise** every pair union is a single alternating Hamilton cycle.  Fix
the cycle formed by `M_0 u M_1` and number the vertices `v_1, ..., v_N` along
it, so that `M_0` and `M_1` alternate on its edges.  Then `M_2` is a perfect
matching of *chords* of this cycle.  Write `k = N/2` for the number of
chords; `N >= 6` means `k >= 3`.

**Step 3 — a chord joining opposite parities.**  If some chord `c` joins two
positions of different parity, the two arcs of the cycle complementary to `c`
have even length, so each carries an alternating perfect matching along cycle
edges.  Together with `c` they form a perfect matching `S`.  It uses a chord,
so `S != M_0, M_1`; it uses exactly one chord, a **proper** subset of `M_2`
because `k >= 3`, so `S != M_2`.  Done.

**Step 4 — an even chord crossing an odd chord.**  Otherwise `M_2` matches
even positions to even and odd to odd.  Suppose some even-position chord and
some odd-position chord *interlace* (their endpoints alternate around the
cycle).  The four complementary arcs then have even length, and the two
chords together with alternating matchings on those four arcs give a perfect
matching `S`.  Again `S != M_0, M_1`, and `S` uses exactly two chords, a
proper subset of `M_2` because `k >= 3`.  Done.

**Step 5 — the residual case is empty.**  It remains to rule out the
situation in which no even chord interlaces an odd chord.  If no two chords
interlaced, each chord would cut off a set of positions closed under the
matching of the opposite parity, so its two endpoint indices would be
congruent modulo two.  Restricting the argument to either parity class
repeats it and forces the endpoints to be congruent modulo every power of
two, which is impossible for two distinct indices in a finite matching. ∎

**Sharpness at `N = 4`.**  There `k = 2`, and the constructions of Steps 3
and 4 are no longer proper subsets of `M_2`: the crossing pair of Step 4 is
*all* of `M_2`, so the construction returns `M_2` itself.  Both
one-factorisations of `K_4` genuinely have only three perfect matchings.
`N >= 6` therefore enters the proof exactly through `k >= 3`, i.e. through
*properness of the chord subset*, not through the parity tests.

## 3. Verification

The constructive proof was executed on **every** properly 3-edge-coloured
cubic chart at `N = 4, 6, 8, 10` — a *chart* being an ordered triple
`(M_0, M_1, M_2)` of pairwise disjoint perfect matchings of `K_N` with `M_0`
pinned to the canonical matching by relabelling — and the matching it outputs
was checked to be a perfect matching of `M_0 u M_1 u M_2` outside
`{M_0, M_1, M_2}`:

| `N` | charts | branch census | max perfect matchings | theorem holds |
|---|---|---|---|---|
| 4 | 2 | step 4: 2 | 3 | **no** (sharpness) |
| 6 | 32 | step 3: 32 | 6 | yes |
| 8 | 1,884 | step 1: 924, step 3: 768, step 4: 192 | 9 | yes |
| 10 | 159,232 | step 1: 102,400, step 3: 56,832 | 18 | yes |

`32 + 1884 + 159232 = 161,148` charts at `N >= 6`, zero failures.  Two
provenance notes for the record:

* the `N = 4, 6, 8` counts (2 / 32 / 1,884) reproduce the committed
  exhaustive enumeration in `notes/termwise-rank3-cubic-uniqueness.md`; the
  new datum is `N = 10`;
* **Step 5 is exercised zero times** in that range, and the source lane's
  script labels it `step5-contradiction(unreachable)` without implementing
  it.  The verification therefore certifies Steps 1/3/4 on all enumerated
  charts; the general-`N` completeness of the proof rests on the Step 5
  argument above, which is committed hand mathematics
  (`proofs/odd-near-perfect-gadget-obstruction.md`,
  `notes/finite-obstruction.md` §7,
  `notes/termwise-rank3-cubic-uniqueness.md` §3.5), not on the enumeration.

A deliberately overlapping triple is rejected by the enumeration's
disjointness assertion (control).

## 4. Corollary: the support floor dies at every even `N >= 6`

**Definitions.**  A *monomial template* assigns to each unordered pair either
ABSENT or an ordered colour label `(a,b)`, meaning `A_uv = w_uv e_a^{(u)} (x)
e_b^{(v)}` with `w_uv != 0`; it is *diagonal* when every label has `a = b`.
For a diagonal template the *colour graphs* are `G_r = { uv : label(uv) =
(r,r) }`, and for a word `c` the fibre of `c` is the set of supported perfect
matchings, which factors as the disjoint union over `r` of the perfect
matchings of `G_r` restricted to `c^{-1}(r)`.  A *singleton mixed fibre* kills
the template: a non-constant word whose fibre is a single matching has
coefficient one nonzero monomial, which cannot vanish (mechanism O2).

> **Corollary A3.4-a.**  For every even `N >= 6`, no exact monomial source has
> support `m = 3N/2`.
>
> *Proof.*  At `m = 3N/2` the budget lemma J.1d forces the source into the
> single-cell diagonal regime with `G_0, G_1, G_2` perfect matchings on a
> properly 3-edge-coloured cubic support graph `U`.  By Theorem A3.4 there is
> a perfect matching `S` of `U` outside `{G_0, G_1, G_2}`.  Define a word by
> `c(v) = ` the colour of the `S`-edge at `v`; this is well defined and
> constant on each `S`-edge.  It is mixed: if `c` were the constant word `r`,
> then every edge of `S` would have colour `r`, so `S = G_r`.  Its fibre is
> exactly `{S}`: at a vertex `v` of colour `s` the graph `U` has exactly one
> incident edge of colour `s`, namely its `G_s`-edge, so any supported
> matching is forced edge by edge and equals `S`.  A mixed singleton fibre is
> impossible. ∎

**The verification** re-derives the singleton statement per chart with two
disjoint engines (the product formula over the colour graphs, and direct
enumeration of all `(N-1)!!` matchings), requiring both to return fibre size
1 *and* the word to be mixed: **0 failures on all 161,148 charts** at
`N = 6, 8, 10`, and exactly 2 failures at `N = 4` — both being the `K_4`
one-factorisations, where the constructed matching is `M_2` and the word is
constant.  Mixedness is precisely what fails at `N = 4`.

**Two scope statements that must travel with this corollary.**

1. **It is conditional.**  The chain consumes the J.1d budget lemma (the
   `m >= 3N/2` bound and the forcing into the single-cell diagonal regime at
   equality), which lives in an unaudited probe lane
   (`computations/unaudited-bridge-w6-2026-08-15/REPORT.md`).  Until that
   lemma is itself promoted, the corollary is conditional on it.  What is
   unconditional is the graph theory: a properly 3-edge-coloured cubic graph
   on `N >= 6` vertices has a mixed word with a singleton fibre.
2. **A stronger statement is already committed.**  Corollary 7.2 of
   `notes/finite-obstruction.md` states that for every even `n >= 6` no
   collection of aggregate matrices whose nonzero support graph is 3-regular
   can satisfy the exactness system — with **no** diagonal or monomial
   hypothesis.  Corollary A3.4-a is that statement restricted to diagonal
   monomial templates, reached through the budget lemma.  Its contribution is
   the uniform derivation of the `N = 8` cube-chart kill and the machine
   verification, not new mathematics.

## 5. Recorded, and deliberately not promoted

Two further corollaries appear in the source lane's report:

* `m = 3N/2 + 1` dies;
* every diagonal monomial source with even-cycle-free colour graphs dies.

**Neither has a proof or a checker anywhere in the corpus** — they are
report-level prose only.  (The plausible arguments are short — at `3N/2 + 1`
the budget leaves one edge above the cubic chart, and even-cycle-free colour
graphs force `pm(G_r[S]) <= 1` — but neither is written down, and neither
should be promoted on that basis.)  The source lane's "reach" data above the
floor is a *search*: rows reporting no singleton-free template found are
search failures, not emptiness claims, and at the floor itself the search did
not even find three live constant fibres.

Also not promoted: the source lane's `Sigma_min` numbers at `N = 10`, which
that lane withdrew itself.

## 6. Prior-art hygiene (mandatory at commit time)

* First line of the promoted document must state that the theorem is
  Bogdanov's observation restricted to properly 3-edge-coloured cubic graphs,
  with the three citations above and an explicit "no priority is claimed".
  This repository has a documented false-novelty incident on **exactly this
  statement** (a committed note once called it "new, standalone"); the
  correction is recorded in `notes/wip-attack-map-2026-08-03.md` and the
  attribution boilerplate now appears in roughly sixteen committed files.
* The method is also not new: §2 of arXiv:2202.05562 sets up the same
  apparatus on a Hamiltonian cycle — legal/illegal edges, **crossing pairs**,
  nice crossing pairs, **drums**.  Under that dictionary, "every chord joins
  equal parities" is their Observation 1, and "a mixed pair is admissible iff
  the two chords cross" is their nice-crossing-pair notion.  Say so.
* Do **not** describe the corollaries as new mechanisms without the
  cross-check `references/REFERENCES.md` flags as still open: Theorems 1.11
  and 1.12 of `[ChandranGajjalaIllickan2024]` concern cubic *input* graphs,
  whereas the corollary concerns a cubic support graph derived inside a
  realisation; neither is known here to subsume the other, and that check
  "should be [done] before any novelty claim about a cubic statement".
* The repository's own "crossing pairs" (sites straddling a live split of the
  site set — the sense used in `draft_cut_mechanism.md`) are **unrelated** to
  the cyclic-order crossing pairs of arXiv:2202.05562.  No overlap exists
  there and none may be disclosed.

## 7. Certificates and checkers

| item | artifact |
|---|---|
| enumeration of charts, the constructive proof (steps 1/3/4), the branch census, the singleton corollary per chart | `computations/unaudited-uniform-n-a3-2026-08-15/a3_task2_floor.py`, `results_task2_floor.json`, `log_task2_floor.txt` |
| diagonal-template machinery (colour graphs, product formula, fibres) | `computations/unaudited-uniform-n-a3-2026-08-15/a3_core.py` |
| committed self-contained proofs of the same lemma | `proofs/odd-near-perfect-gadget-obstruction.md`, `notes/finite-obstruction.md` §7, `notes/termwise-rank3-cubic-uniqueness.md` §3 (with its §3.0 comparison to the published statements) |
| committed stronger corollary on 3-regular supports | `notes/finite-obstruction.md` Corollary 7.2 |
| the citations | `references/REFERENCES.md` (`[Bogdanov2017]`, `[ChandranGajjala2026]`, `[ChandranGajjalaIllickan2024]`) |
| the budget lemma consumed by §4 (unaudited) | `computations/unaudited-bridge-w6-2026-08-15/REPORT.md` |

Run (from the source lane's directory, which is where its outputs are
written):

```text
python3 a3_task2_floor.py        # -> log_task2_floor.txt, results_task2_floor.json
```

## 8. Audit record

* **Source lane:** `computations/unaudited-uniform-n-a3-2026-08-15/REPORT.md`
  (A3, unaudited; exact arithmetic for all verdicts).
* **Independent audit: NONE.**  No agent has audited this lane.  Under
  `certification/SUPERSESSIONS.md` rule 5 an independent audit is required
  before any of this may be committed as spine.  What partially substitutes,
  and must be recorded rather than glossed:
  * the theorem is **external prior art** with published proofs, and the
    repository already carries two independent committed proofs of it;
  * the chart enumeration at `N = 4, 6, 8` reproduces the committed
    exhaustive counts (2 / 32 / 1,884) from a different engine.
  Neither substitutes for an audit of the `N = 10` enumeration, of the
  corollary's per-chart singleton check, or of the J.1d chain.
* **Corrections adopted in this draft:** the attribution is the first line,
  not a footnote; the Step 5 gap between the coded branches and the general-`N`
  proof is stated explicitly; the corollary is marked conditional on the
  unaudited budget lemma and subordinate to the committed Corollary 7.2; the
  two unbacked corollaries are excluded.
* **Pre-commit obligations:** the items of §G and §A of
  `draft_promotion_checklist.md`, plus the audit required by rule 5.
