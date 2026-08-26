> **UNAUDITED DRAFT — not spine.**  Drafted 2026-08-15 at pinned repository
> HEAD `e0c4d7c548dd1b252a87b3fc16e76182a3a0bbfb` (recorded in
> `PINNED_HEAD.txt` beside this file).  It becomes spine only when committed
> through the supersession discipline of `certification/SUPERSESSIONS.md`,
> with the pre-commit items of `draft_promotion_checklist.md` discharged.
> All paths are repository-root-relative.

# The cut mechanism: splitting the site set kills thick fibres

**Theorems W12-A (split kill), W12-B (cut extraction) and W12-C (the exact
structural boundary).  Proposed status on promotion: `[P]` — proved, with
exact checkers and an independent re-audit (A4).**

## 0. Notation and terminology

Let `B` be a site set of even cardinality `N` and three colours `{0,1,2}`.
A source assigns to each pair `u < v` an endpoint-ordered block `A_uv` in
`C^{3x3}` (rows = colour at `u`, columns = colour at `v`); its **template**
`T` records which cells are nonzero, `T[uv]` being the set of occupied cells
`(i,j)`.  Write `m = supp(T)` for the number of nonzero blocks, `Sigma(T)`
for the number of occupied cells.  A block with all nine cells occupied is
**full**.  For a word `w` in `{0,1,2}^B`,

```text
H_w(A) = sum_{M in PM(B)} prod_{uv in M} A_uv[w_u][w_v].
```

A perfect matching `M` is **supported on `w`** when every `uv` in `M` has
`(w_u, w_v)` occupied; the **fibre** `F_w` of `w` is the set (equivalently,
the polynomial sum) of those matchings.  Following the corpus convention:

> a source **with template `T`** is a choice of nonzero values on the
> occupied cells of `T`; it is **exact** when every mixed fibre sums to zero
> and each of the three constant fibres sums to something nonzero
> (`computations/unaudited-thickfibre-w12-2026-08-15/w12_core.py`).

**Cuts.**  An **even cut** is an unordered bipartition `B = L u R` with `|L|`
and `|R|` both even and nonzero.  A **crossing edge** is a pair with one
endpoint in each part.  A crossing edge `pq` (`p in L`, `q in R`) is
**active on `w`** when the cell `(w_p, w_q)` is occupied.  For a sub-word `u`
on `L`, `F^L_u` denotes the sum over perfect matchings of `L` supported on
`u`; likewise `F^R`.

**Terminology guard** (`notes/2026-08-15-conventions-and-hazards.md` items
1–2).  "Clean" has three incompatible senses in the corpus; this document
uses only the **cut-clean** one, and distinguishes two versions of it:

* a word `w` is **cut-clean** for `(L,R)` — the *exact* criterion — when no
  `T`-supported perfect matching of `B` uses a crossing edge;
* `w` is **star-clean** for `(L,R)` — the *sufficient* criterion — when the
  active crossing edges on `w` are pairwise intersecting (no two of them are
  vertex-disjoint).

Star-clean implies cut-clean (Lemma 1.1); the converse fails, so the exact
criterion is the one to implement (§3.4).  This document never uses
*slice-clean* (the colour-`c` pair-slice sense of W5/P1/W13/W14) or
*word-clean* (the single-cell-inactive sense of W15).  Similarly, "witness"
here always means a *SAT template witness* of the W8/W11 support enumeration,
never a cap witness `(p,q,K)` and never the legacy `C_{u,r} = 0` site.

## 1. The parity lemma

> **Lemma 1.1 (crossing parity).**  Let `(L,R)` be an even cut and `w` a
> word.  (i) Every `T`-supported perfect matching of `B` uses an even number
> of crossing edges.  (ii) If `w` is star-clean then it is cut-clean, and
> then
>
> ```text
> F_w = F^L_{w|L} . F^R_{w|R},
> ```
>
> the product being a literal identity of polynomials: the supported
> matchings of `w` are exactly the unions `M_L u M_R` of a supported matching
> of `L` and one of `R`.

*Proof.*  (i) A matching using `k` crossing edges leaves `|L| - k` sites of
`L` to be matched inside `L`, so `|L| - k` is even; `|L|` is even, hence `k`
is even.  (ii) If two of the crossing edges used by a supported matching were
present, they would be vertex-disjoint and both active on `w`, contradicting
star-cleanness; so `k <= 1`, and `k` is even by (i), so `k = 0`.  Every
supported matching therefore splits, and conversely every such union is
supported; expanding the product gives the displayed identity. ∎

Evenness of both parts is load-bearing and not a convenience: with an odd
part every supported matching uses an *odd* number of crossing edges, and a
single active crossing edge no longer yields a factorisation.  Measured on
W8's immune template at `m = 20` over all 6,561 words: for `L = {0,1,2}` the
realised crossing-edge counts are `{1,3}` and **all** 2,634 star words fail
to factor; for `L = {0}` the counts are `{1}` and all 6,561 star words fail;
for the even cut `L = {0,1,2,3}` the counts are `{0,2,4}` and **no** star
word fails (`computations/unaudited-audit-a4-w12w10-2026-08-15/chk09_controls.py`
§(a), `results_chk09.json` key `a_parity`).

## 2. Theorem W12-A (split kill)

> **Theorem W12-A.**  Let `T` be a template on `B` (`|B| = N` even) and let
> `(L,R)` be an even cut.  Suppose there are colours `c != c'` such that each
> of the three words `c^B`, `c'^B` and `w = c^L c'^R` is cut-clean for
> `(L,R)`.  Then no exact source has template `T`.

*Proof.*  If the fibre of `c^B` is empty then already no source with template
`T` has `H_{c^B} != 0`, and the template is dead outright.  So assume both
constant fibres are nonempty.  By Lemma 1.1 the three coefficients factor:

```text
H_{c^B}  = F^L_c  . F^R_c   != 0,        so  F^L_c  != 0;
H_{c'^B} = F^L_{c'} . F^R_{c'} != 0,     so  F^R_{c'} != 0;
H_w      = F^L_c  . F^R_{c'}.
```

But `w = c^L c'^R` is mixed (as `c != c'` and both parts are nonempty), so
exactness forces `H_w = 0`, while the two displayed non-vanishings make
`F^L_c . F^R_{c'} != 0`.  Contradiction. ∎

**Strengthening (audit A4).**  The first line of the proof is a theorem in
its own right and is stronger than the statement as originally implemented:
*if some constant word has an empty fibre, the template is dead with no cut,
no second colour and no mixed word at all* — the pipeline's `support-dead`
verdict.  The promoted statement should therefore be read as a case split
(empty constant fibre ⇒ dead; otherwise the factorisation argument), not as
a theorem carrying a hidden nonemptiness hypothesis.

**Character of the certificate.**  It reads only the occupied-cell pattern:
it is exact, purely combinatorial, and it is *not* a lattice or binomial
mechanism — it is the statement that a fibre polynomial factors and that both
factors are pinned nonzero by constant words.  That is why it is invisible to
the immunity proposition of the W8 layer, which governs fibres of the whole
of `B`.

**Instances.**  W8's immune construction at `m = 20` (`Sigma = 84`) and at
`m = 21` (`Sigma = 93`), with `L = {0,1,2,3}`, `R = {4,5,6,7}`, `c = 0`,
`c' = 1`, mixed word `00001111`; the three fibres have sizes 4, 4, 4 and both
half-fibres have size 2 (`computations/unaudited-audit-a4-w12w10-2026-08-15/results_chk03.json`).
A4 re-derived the star hypothesis, the crossing-freeness and the
factorisation *monomial by monomial* for all three words in each case.

## 3. Theorem W12-B (cut extraction)

### 3.1 Pinning

> **Definition.**  A sub-word `u` on `L` is **pinned** when `F^L_u` is forced
> nonzero for every source with template `T`.  Two rules suffice:
>
> * **(P1)** `L` has exactly one supported perfect matching at `u`.  Then
>   `F^L_u` is a single product of occupied cells, hence nonzero.
> * **(P2)** `u = c^L` and the constant word `c^B` is cut-clean.  Then
>   `F^L_c . F^R_c = H_{c^B} != 0`, so `F^L_c != 0`.

### 3.2 The theorem

> **Theorem W12-B (cut extraction).**  Let `(L,R)` be an even cut for a
> template `T`.  For every pinned sub-word `u` on `L` and every sub-word `y`
> on `R` such that the spliced word `(u,y)` is **mixed** and **cut-clean**,
> every exact source with template `T` satisfies
>
> ```text
> F^R_y = 0.
> ```
>
> These equations, together with the non-vanishings `F^R_y != 0` for pinned
> `y` on `R` and the requirement that all `R`-cells be nonzero, form a value
> system in the cells of `R` alone.  If that system is infeasible, no exact
> source has template `T`.

*Proof.*  By Lemma 1.1, `H_{(u,y)} = F^L_u . F^R_y`; the left side is zero
because `(u,y)` is mixed and the source is exact, and `F^L_u != 0` because
`u` is pinned. ∎

### 3.3 Why the extracted system is easier

The fibres of the extracted system are perfect matchings of `R` only.  At
`|R| = 4` there are exactly three of them, so every extracted equation has at
most **three** monomials, each of degree 2 — and very often two, which is a
binomial relation.  This is the entire point of the mechanism: *thickness of
the fibres of `B` says nothing about the fibres of `R`*.  The immunity
proposition of the W8 layer is a statement about whole-`B` fibres, and
thickness is not preserved by cutting; a cut of a thick template produces
four-site sub-problems that are binomial regardless.

### 3.4 The cleanness criterion to implement (audit A4, D4)

Theorem W12-B is stated above with the **exact** criterion.  The star
criterion is only sufficient, so an implementation using it extracts a
*subset* of the valid equations: on W8's immune template at `m = 20` the
exact criterion yields **156** zero-equations against the star criterion's
**152**, with identical non-vanishing sets (4,681 in both), while on the
`m = 20` survivor (373 vs 373) and on the immune template at `m = 24`
(0 vs 0) the two agree
(`computations/unaudited-audit-a4-w12w10-2026-08-15/results_chk09.json`, key
`c_cross_implementation`).  The swap costs nothing in soundness — every use
of the factorisation is verified monomially at the point of use — and gains
reach.

### 3.5 One-sidedness of the decision back-ends

The extraction produces a value system; deciding it is a separate step, and
every back-end used is **one-sided: it can miss a kill, never manufacture
one**.  Three checkpoints carry that claim.

1. **Monomial-value transport.**  The binomial rows are transported into a
   partial character `phi` on a sublattice of `Z^d`, stored in Hermite normal
   form with attached exact values; `learn` reports a contradiction only on a
   zero value or an exact value clash.  No approximation enters.
2. **Elementary-divisor guard.**  If the binomial lattice has a nontrivial
   elementary divisor the decision returns `undecided` and never `killed`.
   The branch had never fired in the probe's runs; A4 tested it
   behaviourally on synthetic systems, including one that is *feasible* over
   `C` with divisor 2 (`x_0^2 + x_1^2 = 0`, `x_0 + x_1 != 0`, solutions
   `t = +-i`), which returns `undecided` — a `killed` there would have been
   unsound (`results_chk06.json`, key `7b_synthetic`; `7b_no_wrong_kill =
   true`).
3. **Unit-ideal stability.**  The Groebner back-ends test membership of `1`
   in a saturated/Rabinowitsch ideal.  Unit-ideal tests are stable under
   `Q -> C`, so a `killed` verdict transfers to `C`; a `feasible` verdict
   would not, and is never used as one.  Solver failures and timeouts are
   downgraded to `undecided`, never upgraded.

**Scope of the torus reduction.**  The reduction `z = (x^{lambda_1}, ...,
x^{lambda_d})` used by the lattice back-end is surjective onto `(C^*)^d`
because `C^*` is divisible, hence injective as a `Z`-module; over `Q` the
same reduction is **unsound** (already `x |-> x^2` on `Q^*` is not onto).
The pipeline's verdicts are unit-ideal tests, so kills transfer `Q -> C`
(`computations/unaudited-audit-a4-w12w10-2026-08-15/chk06_reduction_and_negative_control.py`).

**Instances.**  The `m = 20` survivor is killed at `L = {0,1,3,7}`, side `R`,
by a pinned sub-word forced to vanish (`1111`, pinned by (P2), forced by the
(P1) sub-word `0010`), 0.91 s; W8's immune templates at `m = 20, 21` at
`L = {0,1,2,3}`, side `R` (`0000` pinned by (P2), forced by `2222`); at
`m = 22, 23` the half-system is decided infeasible by direct Groebner on 35
variables with 70 equations and 2 non-vanishings, in 43 s and 46 s
(`results_chk04.json`).  A4 obtained all of these with an independently
written extractor and a decision route sharing no code with the probe.

**Pinning is load-bearing.**  A mutation control replacing the pinning rules
by "everything is pinned" extracts 1,256 equations of which the genuine
near-exact source violates 1,222, and produces 126 spurious half-system kills
(`results_chk09.json`, key `d_bogus_pinning`).

## 4. Theorem W12-C (the exact structural boundary)

Let `Gamma(T)` be the graph on `B` whose edges are exactly the **full**
(nine-cell) blocks of `T`.  Call an even cut `(L,R)` **feasible** for a graph
`Gamma` when the `Gamma`-crossing edges are pairwise intersecting.  (This is
precisely the condition under which the mechanisms of §2–§3 can fire: a full
block is active on every word, so a `Gamma`-crossing edge is active on every
word, and cut-cleanness of any word requires the `Gamma`-crossing edges to
contain no two vertex-disjoint edges.)

> **Theorem W12-C.**  For every even `N` and every graph `Gamma` on `N`
> vertices:
>
> ```text
> a feasible even cut for Gamma exists   <=>   Gamma is NOT a spanning
>                                              2-connected subgraph of K_N.
> ```
>
> Here *spanning* means that `Gamma` touches all `N` vertices, and
> *2-connected* means that `Gamma` is connected and remains connected after
> the deletion of any single vertex.

### 4.1 Proof

Write `D = { Gamma : a feasible even cut exists }` and
`U = { Gamma : Gamma is spanning 2-connected }`, both regarded as families of
edge sets on the fixed vertex set `[N]`.  The claim is `D = U^c`.

**(0) Monotonicity.**  `D` is a **down-set**: deleting an edge from `Gamma`
only shrinks each crossing set, and a subfamily of a pairwise-intersecting
family is pairwise intersecting.  `U` is an **up-set**: adding edges
preserves spanning, connectivity, and 2-connectivity.  Consequently it
suffices to prove (a) no member of `D` is spanning 2-connected, and (b) every
member of `U^c` lies in `D`; and for (b) it suffices to exhibit, for each
member of a family covering `U^c` upward, a feasible cut.

**(a) `D n U = 0`.**  Let `(L,R)` be a feasible even cut for `Gamma`, and let
`X` be the set of `Gamma`-crossing edges.  If `X` is empty, `Gamma` has no
edge between the two nonempty parts `L` and `R`, so `Gamma` is disconnected
and not spanning 2-connected.  Otherwise `X` is a pairwise-intersecting
family of edges, all of which join `L` to `R`.  A pairwise-intersecting
family of edges is either a star or a triangle, and a triangle would need two
adjacent vertices on the same side of the cut, which no crossing edge
provides; hence `X` is a star, say with centre `x`, and we may assume
`x in L`.  Deleting `x` from `Gamma` removes every crossing edge, so in
`Gamma - x` no vertex of `L - {x}` is joined to any vertex of `R`.  Both
`L - {x}` and `R` are nonempty (`|L| >= 2`, `|R| >= 2`), so `Gamma - x` is
disconnected and `Gamma` is not 2-connected.

**(b) `U^c` is contained in `D`.**  First, every `Gamma` that is not spanning
2-connected is a subgraph of a **two-clique graph**

```text
K(A u {x}) u K(B u {x}),     A, B a partition of [N] - {x} into two
                             nonempty parts,
```

for some vertex `x`.  Indeed, if `Gamma` is disconnected (this includes the
non-spanning case, an untouched vertex being an isolated component), pick any
`x` in one component `C`, put `A = C - {x}` and `B = [N] - C`; every edge of
`Gamma` lies inside `C` or inside another component, hence inside
`A u {x}` or inside `B u {x}`.  If `Gamma` is connected with a cut vertex
`x`, group the components of `Gamma - x` into two nonempty parts `A` and `B`;
every edge of `Gamma` lies inside `A u {x}` or inside `B u {x}`.

Second, every two-clique graph lies in `D`.  Put `a = |A|`, `b = |B|`, so
`a + b = N - 1` is odd and exactly one of `a, b` is even.

* If `b` is even, take `L = A u {x}` and `R = B`.  Then `|L| = a + 1` is even
  and `|R| = b` is even, and both are at least 2.  The crossing edges of the
  two-clique graph are exactly the edges from `x` to `B` — there are no
  `A`–`B` edges — so they form a star at `x` and the cut is feasible.
* If `b` is odd then `a` is even; take `L = B u {x}`, `R = A`, and argue
  symmetrically.

By monotonicity of `D` (step 0), every subgraph of a two-clique graph is in
`D`, so `U^c` is contained in `D`. ∎

**Provenance of the two halves.**  Steps (0), (a) and (b) are audit A4's
argument.  A4 verified the two containments by exhaustive enumeration of the
*maximal* elements of each family at `N = 4, 6, 8, 10`: for (a) the maximal
members of `D`, namely `E(L) u E(R) u {crossing edges at x}` for each even
cut and each vertex `x` — 12, 90, 504 and 2,550 graphs, none of them spanning
2-connected; for (b) the two-clique graphs — the same counts, all with a
feasible cut (`results_chk05.json`; `equivalence_proved = true` at all four
orders).  The general-`N` closure of those two finite checks written out
above (the star/triangle dichotomy in (a); the parity choice of cut in (b))
is **supplied by this draft** and must be re-audited before commit; nothing
downstream at `N = 8` depends on it, since the `N = 8` case is one of A4's
verified orders.

### 4.2 Verification record

* Exhaustive over **all `2^15` graphs on 6 vertices**: 32,768 graphs, 0
  violations; and all `2^6` graphs at `N = 4`.
* Stratified random sample at `N = 8`: 29 edge-counts × 1,200 = **34,800**
  graphs, 0 violations, with spanning 2-connected graphs appearing from 8
  edges upward (2 at 8 edges, 442 at 12, 1,200 at 22+).  This is what closes
  the evidence gap A4 recorded as D5: the probe's own 4,000-graph sample drew
  edge counts uniformly from `0..19` and so **never sampled the dense
  regime** where the interesting direction lives.
* Checker mutation control: replacing "2-connected" by "connected and
  spanning" produces 49 violations in 400 graphs, so the predicate is
  discriminating.
* Predicate versus outcome on the campaign's 135 `N = 8` targets, rebuilt
  from the original template sources: the joint distribution is exactly
  `{(2-connected, no feasible cut): 5, (not 2-connected, feasible cut): 130}`,
  and the five are `immunity_m24, ..., immunity_m28`; 57 recorded cut
  verdicts compared, zero mismatches (`results_chk05.json`).

## 5. What the mechanism decides at `N = 8`

Over the campaign's 135 `N = 8` targets — the `m = 20` CEGAR survivor, W8's
nine immune templates at `m = 20..28`, the 48 SAT template witnesses of the
W11 enumeration, and W8's 77 support classes at `m = 17` — the cut mechanism
kills **130**, and the five it does not kill are exactly the five whose
`Gamma` is spanning 2-connected.  Two scope statements must travel with that
number:

* it is a statement about *known* templates plus the `Gamma` predicate, **not
  an exhaustive sweep** of the thick-fibre regime;
* the count is 130 of 135 only after audit A4's correction D1: the template
  `scplus_m19_5242749_0` — the 48th W11 SAT template witness — had no
  recorded verdict anywhere in the probe's outputs, because the probe's
  file glob ran a few minutes before that witness file was written.  A4
  killed it independently (`L = {0,7}`, side `R`, (P2) sub-word `222222`
  forced by the (P1) sub-word `21`, 1.4 s).  The kills actually recorded by
  the probe number 129.

The residual object at `N = 8` after the cut mechanism is therefore the
family of templates whose `Gamma` is spanning 2-connected — for which
Theorem W12-C says *no* cut is feasible, so this mechanism has provably
nothing to say there.  That family, and its `m = 24` member, are the subject
of `draft_m24_certificate.md`.

**Hypotheses actually used.**  Theorems W12-A and W12-B consume only: the
occupied cells are nonzero, mixed coefficients vanish, and constant
coefficients do not.  No admissibility condition — (SC), (SC+), the
zero-singleton screen, the J.1d budget — enters either statement or either
proof.

## 6. Deliberately not promoted here

* **The residual price inequalities** ("`m >= |Gamma| + 3N/2` and
  `Sigma >= 9|Gamma| + 3N/2` for an (SC)-admissible template; at `N = 8`,
  `m >= 20`, `Sigma >= 84`; `|Gamma| = 8` forces `Gamma = C_8`") are recorded
  in the source lane's report but implemented nowhere and not covered by the
  A4 audit.  They are omitted from this document.  (Their derivation is
  short — a full block serves none of the `3N` forced-incidence demands and
  every other block serves at most two, one per endpoint — but it consumes
  (SC), unlike everything above, and it needs its own checker.)
* **The two-colour restriction observation** (an exact `d = 3` source
  restricts to an exact `d = 2` source on the same sites, for every colour
  pair) is exact and cheap, but the half that would make it a lever — that
  `d = 2` sources exist at `N = 4, 6, 8` — is float-search evidence carrying
  no verdict.  It belongs in a note, not in this document.
* **The negative control's non-vanishing half.**  The committed near-exact
  source's template yields 12 extracted zero-equations (0 violated) and 229
  non-vanishings (0 violated), but audit A4's correction D3 applies: all 229
  are (P1) pins and single monomials, hence automatically nonzero at any
  all-cells-nonzero point, so that half of the control is vacuous; (P2) — the
  rule that carries the risk — is untested by it; and the template is
  support-dead (two of its three constant fibres are empty), so only the
  mixed-only mode has content.  The load-bearing part of the control is the
  12 zero-equations, plus A4's behavioural check that its own independent
  extractor returns `no-kill` on that genuinely mixed-exact source over 90
  half-systems.

## 7. Certificates and checkers

| item | artifact |
|---|---|
| model, templates, fibres, value systems | `computations/unaudited-thickfibre-w12-2026-08-15/w12_core.py` |
| W12-A as implemented and its instances | `computations/unaudited-thickfibre-w12-2026-08-15/w12_split.py`, `run_t2_split.py`, `results_t2_split.json` |
| W12-B as implemented, both pinning rules, the decision ladder | `computations/unaudited-thickfibre-w12-2026-08-15/w12_cut.py`, `w12_cutdecide.py`, `run_t3_cut.py`, `results_t3_cut_core.json`, `results_t3_cut_w11.json`, `results_t5_batch_m17.json` |
| `Gamma` predicate and the boundary on real targets | `computations/unaudited-thickfibre-w12-2026-08-15/run_t7_filters.py`, `results_t7_filters.json`, `run_t9_propcheck.py`, `results_t9_propcheck.json` (superseded as evidence by chk05, below) |
| **W12-C extremal proof** and the exhaustive/stratified verification | `computations/unaudited-audit-a4-w12w10-2026-08-15/chk05_gamma_boundary.py`, `results_chk05.json` |
| independent split-theorem check, monomial-exact factorisation, parity controls | `computations/unaudited-audit-a4-w12w10-2026-08-15/chk03_split_theorem.py`, `results_chk03.json`, `chk09_controls.py` §(a), `results_chk09.json` |
| independent extractor (exact cleanness criterion, direct Groebner back-end) | `computations/unaudited-audit-a4-w12w10-2026-08-15/a4_cut.py`, `chk04_cut_extraction.py`, `results_chk04.json` |
| exact-vs-star cleanness comparison (156 vs 152) and the bogus-pinning control | `computations/unaudited-audit-a4-w12w10-2026-08-15/chk09_controls.py` §(c), §(d), `results_chk09.json` |
| reduction soundness scope, elementary-divisor behaviour, negative control | `computations/unaudited-audit-a4-w12w10-2026-08-15/chk06_reduction_and_negative_control.py`, `results_chk06.json`, `results_chk06b_negcontrol.json` |

## 8. Audit record

* **Source lane:** `computations/unaudited-thickfibre-w12-2026-08-15/REPORT.md`
  (W12, unaudited; exact arithmetic for every verdict; one labelled float
  search, not used here).  The lane's own labels are `W12-1` (split kill) in
  `w12_split.py` and `W12-3` (cut extraction) in `w12_cut.py`; the report's
  `W12-A`/`W12-B` are the same statements, and this document uses the
  report's letters.
* **Independent audit:** `computations/unaudited-audit-a4-w12w10-2026-08-15/REPORT.md`
  (A4; from-scratch engine on deliberately different routes — bitmask
  matchings, active-subgraph fibres, canonical polynomial dictionaries, exact
  cleanness criterion, direct Groebner on half variables, no lattice/Smith/
  torus; exact arithmetic including `Q(i)`).
* **Verdict:** all mathematics CONFIRMED, with amendments that strengthen the
  statements — "**W12-A: CONFIRMED; actually slightly stronger than
  implemented (empty constant fibre already kills).  Evenness load-bearing.
  W12-B: CONFIRMED sound, both pinning rules valid; the back-ends can only
  MISS kills, never manufacture one.  CONSERVATIVE (D4): the star cleanness
  test is strictly weaker than the exact criterion — 156 vs 152 equations on
  immunity m=20; swap recommended.  W12-C: CONFIRMED and UPGRADED from
  sampling to an exhaustive extremal PROOF.**"  A4 is recorded as the first
  audit of the campaign with no mathematical discrepancy; its six
  discrepancies D1–D6 are evidence-side or tooling items.
* **Corrections adopted in this draft:** W12-C's proof replaces the sampling
  (D5); the exact cleanness criterion replaces the star test in the statement
  of W12-B (D4); the sweep is 130 of 135 over 48 W11 templates (D1); the
  negative control is phrased with its vacuity noted (D3); the reduction is
  scoped to `C` explicitly; the empty-constant-fibre case is separated out of
  W12-A.
* **Outstanding before commit:** A4's discrepancy D2 — W12's
  `results_t4_controls.json` and `results_t8_soundness.json` were never
  written, so the C1 (torus round-trip: `F_w(x) = x^{a_1}(1 + sum_k z^{c_k})`
  for every live word) and C2 (Smith substitution round-trip) controls are
  unevidenced.  A4 could not supply them, since it implements no lattice,
  Smith form or torus reduction by design.  Re-run
  `computations/unaudited-thickfibre-w12-2026-08-15/run_t4_controls.py` and
  `run_t8_soundness.py` and store their JSONs, or drop the corresponding
  claims.  See `draft_promotion_checklist.md` §B.
