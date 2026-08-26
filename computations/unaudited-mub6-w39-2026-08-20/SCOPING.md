# UNAUDITED — W39: is the campaign's finite-nonexistence engine applicable to MUB(6)?

**UNAUDITED.** Lane W39, ancillary-target scoping study, 2026-08-20.
Pinned HEAD `5f8ab49245bf6cde841bb4e92fbdb5781ac2f866` (`PINNED_HEAD.txt`).
Design phase only: reading, web research, exact statement-writing, and
seconds-scale exact computation. No writes outside this directory, no
commits, no heavy compute.

Companion documents: `FORMULATIONS.md` (the exact systems and every
measured size), `VERDICT.md` (one page).

Hazard ledger `notes/2026-08-15-conventions-and-hazards.md` binding.
Items that bite hardest here: **18** (numerical silence is not evidence —
almost the entire MUB(6) "state of knowledge" is numerical silence),
**19/24** (characteristic scoping — an `F_p` result decides nothing about
`C`, and here it does not even decide about `R`), **23** (three-way
outcomes: our `S_6` char-0 run is `unchecked`, not `infeasible`), **29**
(a builder needs a calibratable positive — MUB(6) *has* one, unlike the
Krenn campaign; see §2.5).

---

## 0. The repo's own prior flag on MUB-6

`notes/2026-08-11-signed-matching-holonomy-programme.md`, Problem 6
("export handles"), line 137:

> **Problem 6 (export handles).** For each same-shaped nonexistence
> target (MUB dimension 6; Butson/Hadamard families; SIC existence),
> identify the analogue of the matching lattice: the gauge group, the
> invariant lattice, and the combinatorial move playing the role of the
> alternating-cycle exchange. **Honest note: the (O1)/(O2) mechanisms
> feed on multilinear matching structure those problems lack; without a
> structural handle the export is methodology only (multigraded dual
> certificates, adversarial audit discipline).**

**This study confirms that caveat and sharpens it.** The (O1)/(O2)
holonomy mechanisms do not export — MUB(6) has no matching lattice and no
alternating-cycle exchange. What *does* export is narrower and different
from what Problem 6 anticipated: the **stratify-then-solve-exactly**
discipline (§2), not the holonomy machinery. And the gauge group Problem 6
asked for is identified in `FORMULATIONS.md` §0: `H_a ↦ D_L H_a D_{R,a}`
with a shared left factor, of continuous dimension `6 + 6k − 1`.

---

## 1. The polynomial-formulation landscape

### 1.1 The standard formulations

Sizes derived exactly in `FORMULATIONS.md` §1–2 and computed by
`run_01_systems.py`:

- **Gram/unitary form.** `|⟨e_i|f_j⟩|² = 1/6` across bases. As a raw
  system for a quadruple: **85 essential real unknowns, 198 real
  equations** after quotienting the 23-dimensional continuous gauge.
- **Hadamard form.** `{I, H_1/√6, H_2/√6, H_3/√6}` with all `H_a` and all
  `H_a^†H_b/√6` complex Hadamard. Same 85/198 count; this is the form
  every serious attack uses.
- **MU-vector / Brierley–Weigert form.** Fix `H_1`; then every column of
  `H_2, H_3` lies in the fibre `V(H_1)` of vectors MU to `{I,H_1}`. The
  fibre system is **5 unimodular unknowns and 5 independent modulus
  equations** — square, hence 0-dimensional — realised as **10 variables,
  11 bilinear equations** after the substitution `y_j = conj(z_j)`,
  `z_j y_j = 1`. Brierley–Weigert state the same count as
  "`2(d−1) = 10` real variables constrained by `2(d−1)` simultaneous
  coupled quadratic equations"
  (https://arxiv.org/abs/0901.4051).
- **Noncommutative / C\*-algebra form.** Gribling–Polak reformulate
  existence as noncommutative polynomial optimisation with an SDP
  hierarchy, exploiting the `S_d ≀ S_k` symmetry
  (https://arxiv.org/abs/2111.05698, Quantum 8, 1318 (2024),
  https://quantum-journal.org/papers/q-2024-04-30-1318/).
- The 2026 review enumerates **fourteen** mathematically equivalent
  formulations of the existence problem (McNulty–Weigert, Quantum 10,
  2051 (2026), https://quantum-journal.org/papers/q-2026-04-01-2051/,
  arXiv https://arxiv.org/abs/2410.23997, §5).

### 1.2 What is known computationally

- **Brierley–Weigert** are the reference computation. They compute
  Gröbner bases of the MU-vector system with Buchberger's algorithm and
  then extract roots **numerically to 20 significant digits**
  (https://arxiv.org/abs/0901.4051). Headline data: **48 vectors MU to
  `{I, F_6}`**, arrangeable in **16** ways into a second Hadamard matrix,
  and **no two of those 16 are MU to each other** — so at most 3 MUBs
  contain `F_6`. They also report **90 vectors MU to `{I, S_6}`** with no
  third basis constructible from them, making Tao's spectral matrix the
  only known order-6 CHM not in any MUB triple. They tested "nearly 6000
  Hadamard matrices" and never found more than two mutually unbiased.
- **MU constellations.** Brierley–Weigert
  (https://arxiv.org/abs/0808.1614): four MUBs in `d=6` would give rise
  to 35 MU constellations; numerical minimisation located only 18. The
  17 missing constellations are the strongest numerical evidence against
  seven MUBs.
- **Butterley–Hall** (https://arxiv.org/abs/quant-ph/0701122): numerical
  evidence for the maximum number of MUBs in `d=6`.
- **Raynal–Lü–Englert**, "the four most distant bases"
  (https://arxiv.org/abs/1103.1025): numerical optimisation over
  quadruples; no four MUBs found. *(Our fetch of this PDF failed to
  render; the citation is from the search index and the review's
  bibliography, not from reading the paper — treat as unverified detail.)*
- **Maxwell–Brierley** (https://arxiv.org/abs/1402.4070) ran Matolcsi-style
  linear programs on the 3-parameter Karlsson family and report
  explicitly that they **could not** conclude a complete set is
  impossible from Karlsson Hadamards alone.
- **Cifuentes, Ciancaglini, Bellomo, Figueira, Bendersky**
  (https://arxiv.org/abs/2309.12399) give three first-order-logic
  algorithms that decide the maximal MUB number without numerical
  approximation, and state the required time is **impractical**. The 2026
  review's phrasing: the resources "are formidable, even for `d = 6`".
- **SoS/SDP degree barriers — the sharpest negative results, and they
  are recent.** Gribling–Polak's numerics indicate that a sum-of-squares
  refutation of more than 3 MUBs in `d = 6` requires **total degree
  ≥ 12**. Sarkar (June 2026, https://arxiv.org/abs/2606.13903) proves a
  degree-four SoS lower bound: for every `d` and every `m`, an explicit
  degree-four pseudoexpectation satisfies the vector-coordinate
  orthonormality and cross-unbiasedness constraints, so **degree-four
  vector-coordinate SoS cannot prove that seven MUBs fail to exist in
  `C^6`** — while a *projector-coordinate* Gram formulation already
  recovers `m ≤ d+1` at degree four. Formulation choice is decisive.

### 1.3 Exact (non-numerical) nonexistence results, and where exact methods died

**Proved, and they are few:**

| result | scope | proof character | citation |
|---|---|---|---|
| No MUB quadruple contains `{I, F(a,b)}`, for **any** `(a,b)` in the Fourier family | 2-parameter family | stated as the paper's "main result"; method is the generalized Pauli problem. *We did not obtain the proof's text; whether it is computer-assisted is unverified here.* | Jaming, Matolcsi, Móra, Szöllősi, Weiner, J. Phys. A 42, 245305 (2009), https://arxiv.org/abs/0902.0882 |
| (derived, mine) hence also no MUB quadruple contains `{I, F^T(a,b)}` | transposed Fourier family | derived remark W39-R1, `FORMULATIONS.md` §0 | this document |
| No triple of MU **product** bases can be extended by even a single MU vector; the 16 states from removing two orthogonal states from an MU product triple cannot appear in a complete set | product bases | **analytic**, explicitly "without recourse to computer algebra" | McNulty–Weigert, IJQI (2012), https://www.worldscientific.com/doi/abs/10.1142/S0219749912500566 |
| Complete classification of all MU product bases in `d=6`; no quadruple among them | product bases | exhaustive analytic classification | https://arxiv.org/abs/1111.3632, https://arxiv.org/abs/1111.3849 |
| No pair of Heisenberg–Weyl-type MU bases extends beyond three in `d=6` | monomial/"nice" MUBs | computer-algebraic (Grassl 2005) | via review §6, https://arxiv.org/abs/2410.23997 |
| A normalized order-6 CHM with three distinct columns each containing a `−1` belongs to the transposed Fourier family or the 2-circulant family | CHM structure, not MUB nonexistence | **exact Gröbner** | https://arxiv.org/abs/2405.09991 |

**Where exact methods died — with numbers.** The Gröbner precedent in
https://arxiv.org/abs/2405.09991 is the most useful calibration in the
literature: **9 variables, 61 polynomial equations, over `Q` with `i²+1`
or `1+w+w²` adjoined, degrevlex, Mathematica, 9.5 hours wall and 2.6 GB
peak** for a single lemma (a second case took ~3 minutes). Modulus
conditions are handled by `conj(h) = 1/h` plus a Rabinowitsch auxiliary
variable — **not** by a real–imaginary split. So the live exact regime in
this literature is *single-digit variable counts with hours of compute*.
Anything at 25 variables (a single dephased CHM) is already out; 85 (a
quadruple) is not discussed by anyone as a direct target.

### 1.4 2025–2026 movement — and a retraction that reopens strata

This is the most consequential finding of the sweep.

- **April 2025 — a foundational lemma is broken.** McNulty & Weigert,
  *Comment on 'Product states and Schmidt rank of mutually unbiased bases
  in dimension six'*, J. Phys. A 58, 168001 (2025),
  https://arxiv.org/abs/2504.13067. Abstract, verbatim: *"A lemma by Chen
  et al. [J. Phys. A: Math. Theor. 50, 475304 (2017)] provides a
  necessary condition on the structure of any complex Hadamard matrix in
  a set of four mutually unbiased bases in `C^6`. The proof of the lemma
  is shown to contain a mistake, ultimately invalidating three theorems
  derived in later publications."* The lemma in question (Chen–Yu Lemma
  11(v) Part 6) is: **"If a set of four MU bases in dimension six exists,
  none of the Hadamard matrices from the set contains a real 3×2
  submatrix."**
- **The Reply concedes.** Chen et al., https://arxiv.org/abs/2504.15576:
  *"The proof of this lemma has some mistakes. It is difficult to fix
  them relying solely on the existing techniques"*, and *"we are not able
  to save Theorem 2 and Lemma 1 at present."* They claim to repair
  Theorem 1 (the ≤ 22-real-entries bound) with a new proof. The three
  affected papers are Liang et al. (2019) ×2 —
  https://arxiv.org/abs/1904.10181 among them — and Chen et al. (2021),
  https://arxiv.org/abs/2110.13646.
- **What that retraction reopens.** The 2021 paper is the one whose
  headline is that a `H_2`-reducible matrix in a 4-MUB set has exactly
  nine `2×2` Hadamard submatrices, *"and this result can be applied to
  exclude from the four MUBs some known complex Hadamard matrices, such
  as symmetric `H_2`-reducible matrix, the Hermitian matrix, Diţă family,
  Björck's circulant matrix, and Szöllősi family"*
  (https://arxiv.org/abs/2110.13646). Since that paper is among the three
  invalidated and its authors decline to repair the chain, **the
  exclusion of the Diţă family, Björck's circulant matrix, the Szöllősi
  family, Hermitian CHM(6), and symmetric `H_2`-reducible CHM(6) from a
  four-MUB set is, as of 2025, not established.** These are named,
  low-parameter strata that were believed settled and are open again.
- **March/April 2026 — the authoritative survey.** McNulty & Weigert,
  Quantum 10, 2051 (2026),
  https://quantum-journal.org/papers/q-2026-04-01-2051/. Abstract,
  verbatim: *"To date, it remains unknown if complete sets of mutually
  unbiased bases exist in Hilbert spaces of dimensions different from a
  prime power… Fourteen mathematically equivalent formulations of the
  existence problem are presented."*
- **June 2026 — the degree-four SoS barrier** (Sarkar, §1.2 above),
  https://arxiv.org/abs/2606.13903.
- **August 2026 — a claimed complete classification of CHM(6).**
  Cárdenes Wuttig & Tindall, https://arxiv.org/abs/2608.18053 (submitted
  2026-08-18, i.e. two days before this study), claim a complete exact
  finite-incidence classification of order-six CHMs, **proving Szöllősi's
  conjecture** that `G_6^{(4)} ∪ K_6^{(3)} ∪ {S_6}` is exhaustive
  (Szöllősi's four-parameter family: https://arxiv.org/abs/1008.0632).
  **HAZARD.** This is a two-day-old preprint claiming a decades-open
  classification. Given that this very sub-literature just had a 2017
  lemma break in 2025 and take three theorems with it, the campaign's
  own discipline says: **treat 2608.18053 as unverified.** Any target
  whose *statement* depends on the catalogue being complete must be
  labelled conditional on it; a target that only *uses* named families as
  strata does not depend on it at all. Design targets of the second kind.

**Summary of §1.** MUB(6) is exactly the situation hazard 18 was written
for: a vast body of numerical silence (thousands of Hadamards sampled,
17 of 35 constellations never found, 20-digit root extractions), one
genuine exact family theorem (Fourier), one genuine analytic family
theorem (product bases), a broken lemma that just reopened five named
strata, and hard degree lower bounds saying the obvious convex relaxation
cannot work.

---

## 2. The honest toolkit match

### 2.1 Where the engine does NOT bite

**(a) The full quadruple system is out of reach and symmetry does not
save it.** 85 essential real unknowns (`FORMULATIONS.md` §1) against a
documented campaign ceiling of ~24 variables and a documented failure at
45. Crucially, **orbit reduction does not apply**: the W32 wins
(11,920 orbit representatives deciding 2,775,018,960 configurations,
`computations/unaudited-x4general-w32-2026-08-20/`) reduce the *number of
runs* over a **discrete** configuration space. MUB(6)'s solution space at
this layer is continuous and has no discrete configuration parameter. The
symmetry group is real (`S_6 ≀ S_k` plus phases) and Gribling–Polak
already exploit it for SDP block-diagonalisation — but symmetry reduces
*run count*, and here the binding constraint is *per-run size*.

**(b) The Boolean / vanishing-pattern abstraction has no analogue, for a
different reason than W32-ABS.** W32-ABS closed that route for the Krenn
campaign because the hafnian is irreducible on full support, so
`H_w = 0` does not decompose into a cell-vanishing disjunction. For
MUB(6) the route fails one step earlier and more completely: **the MUB
constraints are `|·|² = 1/6`, i.e. equalities to a NONZERO constant.**
There is no zero/nonzero dichotomy in the amplitudes to abstract — every
amplitude is forced nonzero. A vanishing-pattern Boolean abstraction is
not merely blocked, it is **type-incorrect**. So the W32-ABS no-go
applies *a fortiori*, and for a cleaner reason: no abstraction attempt
should be funded on the general system.

  *Partial exception, worth recording.* On the **Butson strata** (all
  entries roots of unity of bounded order) the orthogonality conditions
  become vanishing sums of roots of unity, and the Conway–Jones /
  Lam–Leung theory of vanishing sums *is* a sound finite combinatorial
  abstraction. That is a genuine SAT/CP-shaped route, but only on a
  measure-zero stratum. `S_6` lives there (it is `BH(6,3)`); the generic
  CHM does not.

**(c) The engine's signature verdict — "unit ideal over `ZZ`, hence
infeasible over any field" — is unavailable at the fibre layer, and this
is measured, not argued.** We computed the MU-vector ideal: `dim = 0`,
`vdim = 156` for `F_6` and `vdim = 162` for `S_6`, `isunit = 0` in every
run (`FORMULATIONS.md` §3). The variety is *necessarily* nonempty,
because MU vectors exist. Nonexistence at this layer is a statement about
**real points**, not about the ideal.

**(d) Moduli: the real cost, stated exactly.** Two models were built and
measured. The `conj(z) = 1/z` substitution keeps everything polynomial
with **no variable blow-up** (10 variables, all equations bilinear) — so
the naive worry "moduli force a real–imaginary split that doubles
variables" is *false* as stated. But the real–imaginary split
(`z = a+ib`, `a²+b² = 1`, 10 real variables) produces **exactly the same
`vdim`** (156 / 162, over `F_11` and `F_13`) — because over an
algebraically closed field the split is a linear coordinate change. The
correct statement is therefore:

> **Moduli cost nothing in variables and everything in semantics.** The
> torus condition `|z|=1` is not an algebraic condition over `C`; it
> selects the **real points** of a scheme the ideal already describes.
> Any nonexistence proof at the fibre layer needs real-root counting
> (Hermite quadratic form signature, Sturm–Habicht, or a rational
> univariate representation with certified real-root isolation) on a
> 0-dimensional ideal of degree ~160. **The campaign has built no such
> module.** Its `F_p`/`ZZ` any-field verdicts are the wrong instrument
> here (ledgers 19/24: an `F_p` verdict is about `F_p`-rational points).

### 2.2 Where the engine DOES bite

**The stratification is real, and it makes the problem finite.** For a
**fixed** `H_1`, the reduction in `FORMULATIONS.md` §2 is exact:
every column of `H_2` and `H_3` in a quadruple lies in the finite fibre
`V(H_1)`. So for fixed `H_1` the entire triple/quadruple question is:

1. solve a **0-dimensional ideal of degree ≤ ~162** exactly (10 variables,
   11 bilinear equations, seconds over `F_p`, minutes expected over the
   cyclotomic field);
2. select its real points;
3. test orthogonality and unbiasedness **exactly** among ≤ ~90 points
   (≤ 4005 pairwise tests);
4. search for 6-cliques and for two mutually-unbiased 6-cliques — trivial
   finite combinatorics.

Steps 1, 3, 4 are squarely the campaign's per-orbit exact pattern. Step 2
is the missing module. **This is the whole "does the engine bite" answer:
it bites at the fibre layer, per stratum, and it needs one new capability.**

### 2.3 Variable counts per stratum

| stratum | free params `k` | fibre system size (bilinear model) | assessment |
|---|---|---|---|
| `S_6` (Tao / spectral, isolated) | 0 | 10 vars, 11 eqs, `vdim` 162 | **in range**, measured |
| `F_6` (Fourier, single point) | 0 | 10 vars, 11 eqs, `vdim` 156 | **in range**, measured, char 0 done |
| `D_6^{(1)}`, `B_6^{(1)}`, `M_6^{(1)}` (1-parameter families) | 1 | 12 vars (+1 param, +1 conj-param) | plausible; unmeasured |
| `F(a,b)` / `F^T(a,b)` (Fourier family) | 2 | 14 vars | plausible; **already settled**, so this is a calibration, not a target |
| `K_6^{(3)}` (Karlsson) | 3 | 16 vars | at the edge; compare the 9-variable / 9.5-hour literature precedent |
| `G_6^{(4)}` (Szöllősi generic) | 4 | 18 vars | beyond confident estimation |
| full quadruple, unstratified | — | 85 real unknowns | **out of reach** |

### 2.4 Symmetry available for orbit reduction

Continuous: the `(6 + 6k − 1)`-dimensional gauge of `FORMULATIONS.md` §0,
already used to reach the counts above. Discrete: shared row permutation
(`S_6`), per-matrix column permutation (`S_6` each), basis permutation,
global complex conjugation, and transposition of the pair (derived remark
W39-R1). On the `S_6` target specifically, the stabiliser of Tao's matrix
in the monomial equivalence group is large and should be used to orbit-
reduce the 6-clique search of step 4 — this is the one place the W32
orbit machinery transfers verbatim, because step 4 *is* a discrete
configuration space.

The one genuinely **discrete** invariant stratifying CHM(6) is the
**real-entry pattern** (which of the 36 positions hold `±1`), modulo
`S_6 × S_6` — this is the invariant the whole Chen et al. line exploits
(possible real-entry counts `0–22, 24, 25, 26, 30`,
https://arxiv.org/abs/1904.10181) and it is the only visible route to a
W32-style orbit-reduced sweep. Forcing many real entries also collapses
continuous unknowns (each real entry is a `±1` choice, not an angle), so
the high-real-entry strata are small. This is worth a follow-up lane.

### 2.5 The methodological prize the campaign should notice

Hazard ledger item **29** records that the Krenn campaign has **no
calibratable positive** — its sole true positive `GHZ_4^3` gives a search
no gradient, and three builders failed calibration for that reason.
**MUB(6) has calibratable positives and negatives, both published and
both exact-checkable:**

- **must-SAT (positive):** `{I, F_6}`. Any correct pipeline must produce
  exactly **48** real fibre points and exactly **16** orthonormal
  6-subsets among them (Brierley–Weigert, https://arxiv.org/abs/0901.4051).
  We already reproduce the ambient complex scheme (`vdim = 156` over
  `Q(ζ_6)`, char-0, verified).
- **must-UNSAT (negative), family level:** no MUB quadruple contains
  `{I, F(a,b)}` — an exact published theorem
  (https://arxiv.org/abs/0902.0882). A pipeline that "finds" one is
  broken.
- **must-UNSAT (negative), point level:** the 16 second-bases of `F_6`
  must be pairwise **not** MU (Brierley–Weigert), and `{I, S_6}` must
  admit **no** third basis at all.

This alone is an argument for running the lane: it gives the campaign's
exact-nonexistence tooling a benchmark with ground truth in both
directions, which the Krenn target cannot supply.

---

## 3. The first target, precisely

### Settled vs open, per stratum (the map that picks the target)

| stratum | quadruple question | status | evidence quality |
|---|---|---|---|
| MU **product** bases | cannot extend a triple by even one vector | **SETTLED** | analytic proof, https://www.worldscientific.com/doi/abs/10.1142/S0219749912500566 |
| Fourier family `F(a,b)` | no quadruple contains `{I,F(a,b)}` | **SETTLED** | https://arxiv.org/abs/0902.0882 |
| Transposed Fourier `F^T(a,b)` | same | **SETTLED** (derived, W39-R1) | my derivation; cheap to re-check |
| Heisenberg–Weyl / "nice" / monomial | no more than three | **SETTLED** | Grassl 2005, via review |
| `S_6` (Tao) — **triple** level | `{I,S_6}` is in no MUB triple | **numerical only** | 90 fibre vectors, 20-digit roots, https://arxiv.org/abs/0901.4051 |
| Diţă `D_6^{(1)}`, Björck circulant, Szöllősi family, Hermitian, symmetric `H_2`-reducible | excluded from four MUBs | **REOPENED 2025** | proof chain broken, https://arxiv.org/abs/2504.13067; authors decline repair, https://arxiv.org/abs/2504.15576 |
| Karlsson `K_6^{(3)}` | open | **OPEN** | LP attempt explicitly inconclusive, https://arxiv.org/abs/1402.4070 |
| Szöllősi `G_6^{(4)}` generic | open | **OPEN** | sampling only |
| "no CHM in a 4-MUB set has a real `3×2` submatrix" | — | **OPEN, proof retracted** | https://arxiv.org/abs/2504.13067 |

### W39-T1 — the first target (smallest, calibrated, exactly open)

> **Statement.** Let `ω` be a primitive cube root of unity and let `S_6`
> be Tao's spectral matrix, the `BH(6,3)` Butson complex Hadamard matrix
> verified exactly in `run_01_systems.py`. Prove, over `Q(ω)` with an
> exact certificate and no floating-point step, that
> **`{I, S_6/√6}` extends to no mutually unbiased triple in `C^6`** —
> equivalently, that the 0-dimensional fibre `V(S_6)` (`vdim = 162` over
> `F_7`, `F_11`, `F_13`; char 0 `unchecked`) contains no six pairwise
> orthogonal unimodular-normalised vectors.

**Why this one.** It is the *only* isolated (0-parameter) stratum, so it
is the smallest possible instance. Its answer is known numerically
(Brierley–Weigert: 90 MU vectors, no third basis) so the target is
calibrated in advance, and the claim currently rests on 20-digit root
extraction — exactly the state hazard 18 forbids treating as evidence.
Converting it to an exact certificate is a self-contained, citable
result: *"the spectral matrix is provably in no MUB triple."* The field
is cyclotomic (`Z[ω]`), which is the campaign's native any-ring setting,
and the Butson structure additionally admits the Conway–Jones vanishing-
sums abstraction as an independent cross-check.

**Compute shape.**

| stage | size | estimate |
|---|---|---|
| 1. `std` of `I(S_6)`, 10 vars / 11 bilinear eqs, over `Q(ω)` | `vdim` 162 | seconds over `F_p` (measured); **minutes to low hours** over `Q(ω)` — our 50 s probe timed out, so this is `unchecked`, not slow |
| 2. RUR / triangular decomposition | degree 162 | minutes |
| 3. real-point isolation (expect 90) | degree 162 | **new module** |
| 4. exact pairwise orthogonality | ≤ 4005 tests | seconds |
| 5. 6-clique search, orbit-reduced by `Stab(S_6)` | ≤ 90 vertices | seconds |

Total: a single-day lane, not a fleet — *provided* stage 3 exists.

**Calibrations, named.** must-SAT: `{I, F_6}` → exactly 48 real points and
exactly 16 orthonormal 6-subsets. must-UNSAT: the 16 second-bases of
`F_6` are pairwise not MU; and the family-level `F(a,b)` theorem must not
be contradicted. Positive control lives *outside* the asserted locus
(ledger 18): `F_6` has a triple, `S_6` is claimed not to — the control
point is exactly where the target conclusion fails.

**Pre-launch check required (ledger 27: control the exact target).**
Confirm by direct reading — not by search summary — that no exact proof of
W39-T1 already exists. Our sweep found none, but our fetch of
Brierley–Weigert used a summariser, and Bengtsson et al. (2007) was not
read directly. If W39-T1 turns out to be already exact, fall through to
W39-T2.

### W39-T2 — the first genuinely-new target (the one worth the lane)

> **Statement.** For the one-parameter families reopened by the 2025
> retraction — Diţă `D_6^{(1)}(c)`, Björck's circulant `B_6^{(1)}`, and
> the symmetric / `H_2`-reducible one-parameter strata — prove exactly and
> **uniformly in the parameter** that `{I, H(c)}` extends to no MUB
> quadruple, by showing the parametric fibre `V(H(c))` contains no two
> disjoint mutually-unbiased orthonormal 6-subsets.

**Why this one.** These strata were believed excluded; the exclusion's
proof chain is broken and its authors have publicly declined to repair it
(https://arxiv.org/abs/2504.15576). A correct exact proof for even one of
them is a publishable repair of a hole in the literature, and it is the
campaign's exact pattern applied to a named stratum. Size: `10 + 2` fibre
variables plus a parametric elimination — comparable to the 9-variable /
9.5-hour precedent of https://arxiv.org/abs/2405.09991.

**Prerequisite:** W39-T1 must land first, because T2 needs the same
stage-3 module plus a parametric version of stages 4–6, and because T1 is
the only way to calibrate the pipeline against ground truth.

**Explicit non-target:** *"no CHM in a four-MUB set contains a real `3×2`
submatrix"* (the retracted Chen–Yu lemma). It is the most attractive
statement in the field right now and it is **not** our shape: its
conclusion quantifies over the whole quadruple, i.e. the 85-variable
system, with only 6 entries pinned to `±1`. Do not fund it.

---

## 4. Answers in one line each

1. **Landscape:** three formulations matter — raw quadruple (85 real
   unknowns, hopeless), MU-vector fibre (10 variables, 0-dimensional,
   measured), and noncommutative SDP (degree ≥ 12 needed; degree-4
   provably insufficient). Exact methods in this literature live at
   9 variables and 9.5 hours.
2. **Toolkit match:** the engine bites at the **fibre layer, per
   stratum**; it does not bite on the unstratified quadruple; the Boolean
   abstraction route is type-incorrect (moduli, not vanishing); and the
   any-field/unit-ideal verdict is the wrong instrument because the
   objects are **real points of a nonempty 0-dimensional scheme**.
3. **First target:** W39-T1 (`S_6` is in no MUB triple, exactly over
   `Z[ω]`), then W39-T2 (the 1-parameter strata reopened in 2025).
4. **Verdict:** see `VERDICT.md`.
