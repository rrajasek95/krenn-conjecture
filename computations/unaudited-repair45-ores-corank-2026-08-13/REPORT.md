# UNAUDITED REPAIR PROBE — items 4 and 5

**Pinned HEAD `7d57c552a3ef57d3a95c3bc933af547ad55e087d` (branch `main`).**
All committed code was read from a `git archive HEAD` snapshot at
`/private/tmp/.../scratchpad/repair45/snap`, never from the dirty worktree.
Everything below is exact over **Q** (`fractions.Fraction`), with one
independent `sympy` cross-check of the central rank.

This directory is untracked and un-audited. Treat every claim here as a
probe result, not as a committed theorem.

| script | what it computes |
|---|---|
| `probe_a1_literal_readout_and_symmetry.py` | literal `(lower, ainc)` readout of all 288 canonical columns; site-permutation symmetries |
| `probe_a2_full_symmetry_group.py` | the order-1536 symmetry group, its pure-word stabiliser, the induced label group, the Cartan orbit |
| `probe_a3_pure_ores_membership.py` | membership + separator certificates across four inventories |
| `probe_a4_inventory_lattice.py` | rank/corank lattice over 14 inventories, mutation controls |
| `probe_a5_placement_sensitivity.py` | 900-pair sweep over (M_v placement, Cartan placement) |
| `probe_a6_decisive_criterion.py` | **decisive**: FACT 1, FACT 2, 30-placement classification, separator closed form, controls |
| `probe_b1_corank_and_literal_equivariance.py` | literal equivariance of audited rows; corank of every constructible candidate block; corank-1 sensitivity |

Outputs: `out_a1.json` … `out_a6.json`, `out_b1.json`.

---

## 0. Headline

The scope guard prints *"labelwise pure-ores section: NOT CONSTRUCTED —
Gate-I assembly now: NO"*. Its argument is that the ores block alone
(aggregate diagonal + one placed Cartan residue line) has rank 2 and
contains none of the four repair directions.

**That argument is a non sequitur.** Membership of `x_v = (lower=v, ainc=-1)`
in the 25-row cone does not require a column equal to `(ores=v)`; the ores
defect of `R_v - T_v - rho_v` can be routed through the lower/W/target
blocks. The correct criterion is a rank condition on the whole 25-row cone:

> **rank(physical cone) = 18 + rank( span{aggregate diagonal} + Cartan residue orbit )**
> Gate-I assembly needs rank 24, i.e. the aggregate diagonal together with the
> label-group orbit of the ONE placed endpoint-odd Cartan residue must span
> all six ores coordinates.

Of the 30 placements of a `+/-(-1,+1,+1,-1)`-type residue on four of six pure
multiplier labels, **14 give Gate-I YES and 16 give NO.** The repo pins two
mutually inconsistent placements and **both land in the NO half** — but
neither is derived from anything.

The answer to item 4 is not "the sections do not exist". It is: **the whole
question reduces to one undetermined datum — which four of the six labels the
physical Cartan residue sits on.**

---

## A. Pure-ores construction attempt

### A.1 What is literally there (probe_a1)

Canonical component `complete.CUBIC_PAIRS[1]`, faces (3,5): **288 literal
columns** over 32 words, each a boundary of exactly 90 matching monomials.
Reading every column on the rows that exist literally — the six selected
private matching features (-> `lower_B`) and the pure-aggregate marker
(-> `ainc`), with the bridge sign convention (`column[(3,mon)] = -1`,
`column[(4,"pure_aggregate")] = +1`):

| readout | count |
|---|---|
| `lower = e_j`, `ainc = -1` (exactly the `r0_j` column) | 6 |
| `lower = 0`, `ainc = 0` (invisible to every literal audited row) | **282** |

`nu = sum(lower) + ainc` is **0 on all 288 columns**, recomputed from raw
combinatorics — an independent re-derivation of the pinned covector fact.

So: the six pure-label columns *are* the six `r0_j` columns (they carry
`lower` and `ainc`, hence are not candidate sections), and 282 of 288 literal
columns are completely invisible to every literal audited row. Those 282 are
the only candidate residue carriers, and nothing committed says what their
residue is.

### A.2 The ores readout has no committed definition

- `verify_h3_direct_free_complete_first_fine_degree_membership.py` docstring:
  *"the checker does not reconstruct the physical cap differential or
  ordinary-residue formula."*
- `verify_h3_rootless_non_euler_90term_chart_h1_separator.py:94`:
  `def augmented_boundary(physical_row, target, ores)` — `ores` is a free
  **input dict**, not computed.
- `audit_h3_qzero_denominator_rees_four_cube_independent.py:379-385` requires
  `'"ordinary_residue": "not defined"' in source` **and**
  `"def ordinary_residue" not in source`.
- The only `def ordinary_residue(chain)` in the repo
  (`verify_h3_reynolds_attach_coupled_obstruction.py:216`) is `return chain[1]`
  — a projection of a formal two-component symbol.
- The physical Cartan packet's residue `[-1,1,1,-1]` is a **hardcoded literal
  in the ledger dict** of `verify_h3_physical_cartan_source_orbit_descent.py`.

**Therefore** "a source-provenant column with `ores_Bj = 1` and all other
audited rows zero" is **not decidable at HEAD** in its literal form. What is
decidable exactly is membership in the 25-row projected cone under each
candidate physical column inventory. That is what follows.

### A.3 The realised symmetry group (probe_a1, probe_a2)

Largest group of the committed literal presentation fixing the canonical fine
degree: pairs `(sigma, tau)`, `sigma` a site permutation preserving
`DIRECT_FREE_PAIR = {3,6}` setwise, `tau` a per-site colour relabelling, with
`td[3*sigma(s)+tau_s(c)] == td[3*s+c]`.

- group order **1536**
- `m -> sigma(m)` is a bijection of the 90 direct-free matchings for **all
  1536 elements** (0 failures)
- literal `full_row` equivariance verified on **all 3^8 = 6561 words** for 10
  sampled elements including generators: 65,610 word-checks, 0 failures
- pure-word stabiliser order **96**; none leaves the six-pure-label set
- **induced label group: order 6** — images
  `[0,1,2,3,4,5] [0,2,1,3,5,4] [4,2,3,1,5,0] [4,3,2,1,0,5] [5,1,3,2,4,0] [5,3,1,2,0,4]`
- the dichotomy's `TARGET_ACTION = (5,1,3,2,4,0)` **is** in this group

**Literal equivariance of the audited rows** (probe_b1): for all 96 stabiliser
elements and all six labels, the automorphism carries the private
matching-feature *set* of pure column `j` onto that of pure column
`sigma(j)` — **576 checks, 0 failures** — and permutes the 288-column set
preserving the pure-word predicate — **96 checks, 0 failures**. (An earlier
run reported 496 failures; artefact of `selected_private_features`
tie-breaking with `min()`. Both numbers are in `out_b1.json`.)

This licenses transporting the placed physical packet around its orbit for the
`lower`/`ainc` readouts. It does **not** license it for `ores`, which is
undefined — see section D.

### A.4 Two exact structural facts (probe_a6)

**FACT 1 — the M_v family is redundant.** For every zero-sum `alpha`:

    (lower = alpha) = sum_i alpha_i * (r0_i - T_i - rho_i) + (ores = alpha)

exact identity, verified at **all 30 placements**. The literal M_v alpha
column is already in the span of the core inventory plus the Cartan residue
column *at the same placement*; M_v contributes no rank of its own.

The same computation shows the dichotomy's **"clean collision difference"
grant is exactly as strong as granting the five zero-sum labelwise pure-ores
directions**:

    (lower = e_i - e_j) = (r0_i - r0_j) - (T_i - T_j) - (rho_i - rho_j) + (ores = e_i - e_j)

verified for all 15 pairs. Granting the collisions is 5/6 of the same
assumption, not a weaker one.

**FACT 2 — the rank formula.**

    rank(physical cone) = 18 + rank( span{diagonal} + Cartan residue orbit )   in R^6

verified at all 30 placements. `nu` kills the core and every Cartan placement
(control), so the cone always sits inside `ker nu`; it equals `ker nu` exactly
when the ores span is all of R^6.

### A.5 The inventory lattice (probe_a4)

25 rows: `lower_B0..B5 | ainc | W_B0..B5 | target_B0..B5 | ores_B0..B5`.

| inventory | cols | rank | corank | six sections | four `x_v` |
|---|---|---|---|---|---|
| REPO GRANTED (r0+T+rho+**pure_lab6**+coll15+mv15+cartan15) | 69 | 24 | 1 | 6/6 | 4/4 |
| core `r0+T+rho` | 18 | 18 | 7 | 0/6 | 0/4 |
| core + aggregate ores | 19 | 19 | 6 | 0/6 | 0/4 |
| core + agg + one placed Cartan | 20 | 20 | 5 | 0/6 | 0/4 |
| core + agg + Cartan **symmetry orbit** (scope-guard placement) | 25 | **21** | **4** | 0/6 | 0/4 |
| core + agg + all 15 Cartan placements | 34 | 24 | 1 | 6/6 | 4/4 |
| core + agg + all 15 M_v placements | 34 | 24 | 1 | 6/6 | 4/4 |
| core + agg + all 15 collisions | 34 | 24 | 1 | 6/6 | 4/4 |

`U_v = (lower=v)` stays outside every inventory (0/4 everywhere): the
dichotomy's actual no-go survives untouched at every placement.

### A.6 Per-label verdict

**At the scope guard's pinned placement** `cartan_line = (1,0,1,-1,0,-1)` =
`(+,+,-,-)@(0,2,3,5)` (`verify_h3_cut_swap_shared_repair_source_scope_guard.py:186`),
orbit size 6, ores span rank 3, cone rank 21, corank 4:

| target | verdict | separator value |
|---|---|---|
| B0 | **OBSTRUCTED** | 3 |
| B1 | **OBSTRUCTED** | -2 |
| B2 | **OBSTRUCTED** | -2 |
| B3 | **OBSTRUCTED** | 1 |
| B4 | **OBSTRUCTED** | 1 |
| B5 | **OBSTRUCTED** | 1 |
| `x_fixed_B1` | **OBSTRUCTED** | -2 |
| `x_fixed_B4` | **OBSTRUCTED** | 1 |
| `x_paired_B0_B5` | **OBSTRUCTED** | 3/2 |
| `x_paired_B2_B3` | **OBSTRUCTED** | -1/2 |

**Separator certificates, closed form** (verified at all 30 placements): the
left kernel of the physical cone is exactly

    < nu >  (+)  { phi_c : c _|_ diagonal, c _|_ every vector in the Cartan orbit }
    phi_c := sum_j c_j ( lower_Bj - W_Bj - target_Bj + ores_Bj )

`phi_c` is precisely the labelwise version of the repo's own committed private
separator `phi = private - W - target + R`
(`verify_h3_residual_q_literal_mapping_cone_private_boundary_gate.py`, in
`augmented_private_pivot_no_go`). At the scope-guard placement the left kernel
has dimension 4 = 1 + (6 - 3); `c = (3,-2,-2,1,0,0)` separates B0..B3 and
three of the four `x_v`; `c = (2,-1,-2,0,1,0)` separates B4 and `x_fixed_B4`.

**At the dichotomy's placement** `ALPHA = (-1,+1,+1,-1)` in increasing label
order on `(0,1,2,3)` (`..._anchor_fibre_dichotomy.py:190`): orbit size 3, ores
span rank 4, cone rank 22, corank 3 — **also all six OBSTRUCTED**. The two
files pin *incompatible* placements.

**At 14 of 30 placements: all six CONSTRUCTED, all four `x_v` CONSTRUCTED,
cone rank 24, corank 1.** Explicit certificate at `(+,+,-,-)@(0,1,2,3)`,
residue `(1,1,-1,-1,0,0)`, orbit of size 6:

    d_ores,B1  = (1/6)*aggregate - (1/3)*C0 - (1/6)*C2 + (1/6)*C3 - (1/6)*C4
    x_fixed_B1 = r0[1] - T[1] - rho[1] + d_ores,B1

— exactly the repo's intended formula `x_v = R_v - T_v - rho_v + d_ores,v`,
with `d_ores,v` built entirely from the aggregate scalar ores column and the
symmetry orbit of the one placed Cartan packet. No new source chain needed.

Placement classification (all 30):

| orbit size | ores span rank (with diagonal) | cone rank | corank | Gate-I | count |
|---|---|---|---|---|---|
| 6 | 6 | 24 | 1 | **YES** | **14** |
| 6 | 5 | 23 | 2 | NO | 6 |
| 3 | 4 | 22 | 3 | NO | 7 |
| 6 | 3 | 21 | 4 | NO | 3 |

Sweeping (M_v placement, Cartan placement) independently — 900 pairs, ignoring
the FACT-1 tie — gives rank 24 in 784/900 = 87%. That is the optimistic bound;
FACT 1 ties them, so 14/30 is the honest number.

### A.7 Weaker sections do not help

At the obstructed (scope-guard) placement, with the section allowed extra
output:

| relaxation | delivers `x_v`? |
|---|---|
| exact section `ores = v`, everything else zero | yes (trivially) |
| `ores = v` + zero-augmentation `lower` defect | **no** |
| `ores = v` + `W` defect | **no** |
| `ores = v` + `target` defect | **no** |
| `ores = v` + bare `ainc` (violates `nu`) | **no** |
| no section at all | **no** |

For all four `v`. Structural reason: every cone column satisfies `nu = 0`, so
`ainc` is forced to `-(augmentation of lower)`, and the same separator
`phi_c` that kills the exact defect kills every relaxed one.
**The "weaker section, then correct" route is closed.**

---

## B. Corank computation

### B.1 The block the bordered theorem is actually applied to

`verify_h3_anchor_dark_bordered_cartan_alternative.py` contains **no `load()`,
no `importlib`, no data of any kind**. Its input is a hardcoded 3x3 rational
array written twice verbatim (lines 105-109 and 181-185):

    A_D = ((4,-2,-1), (3,-2,0), (0,0,0))      k = (2,3,2)

Independently recomputed: rank 2, **corank 1**, `A_D*k = 0` OK, third row all
zeros ("*the zero output row lets the placed Cartan be either internal or
external*" — padding, admitted in the file's own comment).

Provenance: `(4,-2,-1)` comes from
`verify_h3_fan_coloop_cartan_circuit_comparison_gate.py:224-233` at a
**stipulated numerical point** `alpha=2, d=3, V=2 => U=4`
(`notes/h3-fan-coloop-cartan-circuit-comparison-gate.md:52-64`: *"At one exact
numerical point take alpha=2, d_i=3, V_i=2, U_i=4"*). The row `(3,-2,0)` has
no provenance — it is a row *chosen to complete* the first into a corank-one
block with the desired kernel
(`verify_h3_shared_odd_comparison_anchor_visibility_gate.py:136-137`:
*"the actual first-row scalar pivot from e6b390a **completed to** its
corank-one target-circuit block"*).

`lambda = (1,0,0)`, `sigma = (-1,0,0,1)`, external separator `(0,0,1,0)` and
the internal preimage `y1 = g1-g2, y2 = (3g1-4g2)/2` are all hardcoded and
verified, never solved. **"Schur" appears 0 times in the file**; the Schur
determinant is implemented only in
`verify_oo_zero_holonomy_schur_interference_reduction.py` on abstract weighted
cycles C4/C6/C8, and the rectangular alternative only in
`verify_rectangular_interference_anchor_cartan_alternative.py`, exhaustive over
**2x2 matrices only**, whose own scope line reads *"it does not identify the
physical source incidence map M."*

**Corank 1 is stipulated, not established** — asserted in the docstring
hypothesis, enforced by construction, re-checked on the literal array.

### B.2 Anchor-critical blocks and the protected incidence map are not constructed

Every occurrence of "anchor-critical" (5 files) and "complete protected
incidence map" / `J_col` (4 notes) is a name, never a construction:

- `verify_h3_cut_swap_odd_prism_kdu_typing_gate.py:290-292`: *"only the
  15-coordinate occurrence-forgetful shadow; **the complete protected J_col
  columns are not constructed**"*
- `verify_h3_complete_tangent_lower_protected_phi_reduction.py:345`: *"It does
  not construct the physical 15-label Phi."*
- `verify_global_dark_cartan_component_absorption.py:136-138` **enforces**
  corank one as a precondition on hardcoded 2x2 blocks, and concedes at line
  306: *"The theorem does not prove that arbitrary source components admit
  such an anchor-critical corank-one cover."*

There is no block decomposition to compute a corank of. Per the task
instruction I therefore computed the corank of the full protected incidence
map on the canonical packet.

### B.3 Corank of the full literal protected incidence map on the canonical packet

`complete.component(base, target_degree)` at faces (3,5), each column a
90-monomial literal boundary. Exact rank over **Q** by sparse elimination:

| quantity | value |
|---|---|
| rows (distinct literal matching features) | **19,116** |
| columns | **288** |
| exact rank over Q | **288** |
| **kernel dimension (corank, source side)** | **0** |
| row cokernel dimension | **18,828** |
| two-chart columns / rank / kernel | 576 / 288 / **288** |
| **corank exactly 1?** | **NO** |

The literal map is **injective**. Corank 1 fails in both directions by a wide
margin. Nothing in the repo restricts it to a corank-one block.

### B.4 Corank of the 25-row projected cone — the only corank-1 object in the grade

| inventory | rank | **corank** |
|---|---|---|
| repo's granted cone (six labelwise sections **granted**) | 24 | **1** OK |
| physical, core + aggregate ores only | 19 | 6 |
| physical, + one placed Cartan | 20 | 5 |
| physical, + Cartan symmetry orbit, **scope-guard placement** | 21 | **4** |
| physical, + Cartan symmetry orbit, **dichotomy placement** | 22 | **3** |
| physical, + Cartan symmetry orbit, best 14/30 placements | 24 | **1** |

**Corank 1 is not established physically.** It holds under the generous grant,
and under the physical inventory only for 14 of 30 placements; at both
placements the repo actually pins, the corank is 4 and 3.

(The bordered theorem is never applied to this matrix anyway. The link is an
`EXPECTED_LEDGER_SHA256` string comparison at
`verify_h3_cut_swap_shared_repair_anchor_fibre_dichotomy.py:268-270` plus
ledger prose. The 3x3 array never meets the 25x69 matrix.)

### B.5 Why corank exactly 1 is essential — quantified

The bordered hypothesis is `h(k) = 0` for the **one distinguished circuit**
`k`, not `h|ker(A) = 0`. That distinction is the whole theorem:

- `h|ker(A) = 0  =>  h = lambda*A` is **trivially true at every corank** (it is
  just `ker A subset ker h <=> h in rowspace A`). A first pass of this probe
  tested that and got 0 failures at coranks 1, 2, 3 — a null result, recorded
  so nobody repeats it.
- `h(k) = 0` for a single kernel vector `k` implies `h in rowspace(A)` **iff
  `ker A = <k>`, i.e. iff corank is exactly 1.**

Random exact trials, n=4 blocks over Q, seed 20260813:

| corank | trials | factored `h = lambda*A` | **failure rate** |
|---|---|---|---|
| **1** | 2458 | 2458 | **0 / 2458 (0%)** |
| 2 | 2963 | 247 | **2716 / 2963 (91.7%)** |
| 3 | 3000 | 43 | **2957 / 3000 (98.6%)** |

This confirms the dichotomy audit's ~97% figure and pins its cause. Since the
physical corank is 4 or 3 at the repo's own placements, the bordered
alternative's hypothesis fails there — with no fallback: the Schur determinant
is unimplemented for that file and collapses at corank >= 2.

---

## C. Mutation controls

All passing (`out_a4.json`, `out_a6.json`):

- `nu` kills every column of the core and of every one of the 30 Cartan
  placements — the covector is not accidentally satisfied.
- `nu` is the **unique** left-kernel vector of every rank-24 inventory
  (dimension exactly 1, vector `(1,1,1,1,1,1,1,0,...,0)`).
- `U_v = (lower=v)` is **rejected** for all four `v` at every placement tested
  — the dichotomy's no-go is not weakened by anything here.
- `(lower=v, ainc=-2)` (perturbed near-hit) is **rejected** — the `ainc=-1`
  normalisation is load-bearing.
- A random `nu`-zero vector with entries in all five row blocks **is** accepted
  by a rank-24 inventory — positive control against a solver that always says
  "no".
- Dropping the aggregate ores column from a rank-24 inventory drops rank
  24 -> 23 — that column is load-bearing.
- Core alone: rank 19 with aggregate, 18 without.
- The order-6 label group is verified **closed under composition**; its
  elements are verified to be genuine permutations.
- FACT 1 and FACT 2 verified at **all 30 placements**, not at one.
- The central rank (`PHYS1`, `PHYS15`, `GRANTED` = 24) cross-checked with
  `sympy.Matrix.rank()` against the hand-rolled exact eliminator; they agree.
- Literal `full_row` equivariance census (65,610 word-checks) and the
  matching-bijection census (1536 elements) are positive controls on the
  symmetry claim.

---

## D. Exact statements of what could NOT be reconstructed

1. **The ordinary-residue readout of a source chain.** No committed artifact
   defines a map from literal source columns to the six `ores_Bj` coordinates,
   and the repo asserts this deliberately
   (`audit_h3_qzero_denominator_rees_four_cube_independent.py:379-385`).
   Consequently the literal form of the construction problem is **not
   decidable at HEAD**, and every result in section A is a statement about the
   25-row projected model, not about literal source chains.

2. **Which four labels the physical Cartan residue sits on.** The single datum
   that decides item 4, nowhere derived. Two committed files pin
   *incompatible* conventions: the scope guard (line 186) uses
   `(1,0,1,-1,0,-1)`; the dichotomy (line 190) uses `ALPHA = (-1,+1,+1,-1)`
   in increasing label order. `verify_h3_physical_cartan_source_orbit_descent.py`
   gives the residue as the bare 4-tuple `[-1,1,1,-1]` in a hardcoded ledger
   dict with no label assignment at all.

3. **Whether the ores readout is equivariant for the realised order-6 label
   group.** The `lower` and `ainc` readouts provably are (576 + 96 literal
   checks, 0 failures). Transporting the placed Cartan packet around its orbit
   — which is what turns rank 2 into rank 3, and what makes 14/30 placements
   work — requires the same for `ores`. Since `ores` is undefined this is an
   assumption. It is **much weaker** than "construct two new rho-equivariant
   source chains", but it is not nothing.

4. **The W and target rows.** Neither has any literal counterpart in the
   288-column component. `T_i = (W=-e_i, target=e_i)` and
   `rho_i = (W=e_i, ores=e_i)` are hand-typed model columns.

5. **Any anchor-critical block decomposition.** Not constructed anywhere; the
   repo states this in three separate checkers. There is therefore no physical
   block whose corank could be the bordered theorem's hypothesis.

6. **The link between the 3x3 bordered block and the canonical packet.** A
   ledger-hash comparison plus prose. The two objects never meet in executable
   code.

---

## E. Suggested restatement of repair items 4 and 5

Item 4 as written ("construct the six labelwise pure-ordinary-residue
sections") is **the wrong target** — those sections are derived, not
primitive, and the M_v and collision grants are equivalent to them. Sharp
replacement:

> **Determine the label placement of the physically constructed endpoint-odd
> Cartan residue `(-1,+1,+1,-1)` among the six pure multiplier labels of the
> canonical faces-(3,5) component, and establish that the ordinary-residue
> readout is equivariant for the order-6 label group realised by the literal
> source automorphisms of that grade.**
>
> If the placement lands in the 14/30 good class, `x_v = R_v - T_v - rho_v +
> d_ores,v` is source-typed with `d_ores,v` an explicit rational combination of
> the aggregate scalar ores column and the Cartan orbit, and "Gate-I assembly
> now: NO" flips to YES with no new source chain constructed. If it lands in
> the other 16, the obstruction is certified by an explicit separator
> `phi_c = sum_j c_j(lower_Bj - W_Bj - target_Bj + ores_Bj)` and no weaker
> section repairs it.

Item 5 stands, and is worse than stated: corank 1 is not merely unestablished
for the physical block — there **is** no physical block; the one literal
candidate is injective (corank 0 out of 288 columns); and the 25-row cone has
physical corank 4 or 3 at the two placements the repo pins.
