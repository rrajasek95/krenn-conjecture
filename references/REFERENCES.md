# References

The literature this program touches, with the exact statements we cite and
the exact status of each claim.  Entries are cited from the notes and
proofs by their **key** (e.g. `[Bogdanov2017]`).

Every entry is marked with how it was checked:

* **[primary]** — the arXiv/journal text or the source file itself was
  read, and the quoted statement is verbatim from it;
* **[secondary]** — taken from another paper's report of it, not yet read
  in the original;
* **[unverified]** — bibliographic detail we could not confirm; do not
  put it in a write-up without checking.

Two conventions of this repository, used below:

* **GENERAL / BICOLOURED model** — every unordered site pair `uv` carries
  an endpoint-ordered block `A_uv` with cells `A_uv(i,j)`, `i` read at `u`
  and `j` at `v`; cells with `i != j` are allowed.  This is the model of
  the Krenn–Gu conjecture and of the open cases.
* **MONOCHROMATIC-EDGE model** — `A_uv(i,j) = 0` for `i != j`, i.e. every
  source carries one colour at both ends.  Equivalent to the diagonal
  system in `W_c(u,v) = A_uv(c,c)` (see
  `notes/exact-source-live-split-forcing.md`).  This is a strict
  restriction of the general model, and results in it do **not** settle
  the corresponding general case.

---

## The conjecture and its origin

**[KrennGuZeilinger2017]** M. Krenn, X. Gu, A. Zeilinger, *Quantum
experiments and graphs: multiparty states as coherent superpositions of
perfect matchings*, Phys. Rev. Lett. **119**(24), 240403 (2017);
arXiv:1705.06646.  **[primary — bibliographic data]**
The graph/experiment correspondence: perfect matchings of an
edge-coloured weighted graph ↔ terms of the produced state.

**[GuErhardZeilingerKrenn2019]** X. Gu, M. Erhard, A. Zeilinger,
M. Krenn, *Quantum experiments and graphs II: quantum interference,
computation, and state generation*, PNAS **116**(10), 4147–4155 (2019);
arXiv:1803.10736.  **[primary — bibliographic data]**
Complex weights, hence destructive interference; the state amplitudes
become hafnian-type sums — the form our `H_B(A)` takes.

**[GuChenZeilingerKrenn2019]** X. Gu, L. Chen, A. Zeilinger, M. Krenn,
*Quantum experiments and graphs III: high-dimensional and multiparticle
entanglement*, Phys. Rev. A **99**, 032338 (2019).
**[secondary — cited as ref. [9] of [ChandranGajjalaIllickan2024]]**

**[KrennGuSoltesz2019]** M. Krenn, X. Gu, D. Soltész, *Questions on the
structure of perfect matchings inspired by quantum physics*, Proc. 2nd
Croatian Combinatorial Days, 57–70 (2019); arXiv:1902.06023.
**[primary — bibliographic data]**
The purely graph-theoretic formulation ("inherited vertex colouring").
This is the standard citation for the conjecture *as a graph problem*;
the conjecture itself is attributed to Krenn and Gu.

**Conjecture (Krenn–Gu).**  Verbatim as Conjecture 1.6 of
[ChandranGajjalaIllickan2024]:

> If `|V(G)| > 4`, then `mu(G) <= 2`.

Here `mu(G)`, the **matching index**, is the largest `k` for which `G`
admits a *PMValid `k`-edge-colouring*: an edge-colouring with `k` colours
in which every perfect matching is monochromatic and every colour class
contains at least one perfect matching.  A prize (EUR 3,000) is attached;
see [KrennPage].

**[KrennPage]** M. Krenn, *Inherited vertex coloring of graphs*,
https://mariokrenn.wordpress.com/graph-theory-question/ — the problem
page with the prize announcement and the record of which cases are
settled.  **[secondary]**

**[MO311325]** MathOverflow question 311325, *Vertex coloring inherited
from perfect matchings (motivated by quantum physics)*,
https://mathoverflow.net/questions/311325 .  **[secondary — listed as a
reference of [LeanMQG]]**

---

## Bogdanov's observation — the "three-one-factors lemma"

**[Bogdanov2017]** I. Bogdanov, answer 267013 to MathOverflow question
267002, *Graphs with only disjoint perfect matchings* (2017),
https://mathoverflow.net/a/267013 .  **[secondary — cited and quoted by
[ChandranGajjala2026] and [ChandranGajjalaIllickan2024], which are
primary here; the MO page itself has not been re-read for this file]**

**This is the source of the statement this repository calls "the standard
three-one-factors lemma":**

> Three pairwise edge-disjoint perfect matchings on an even vertex set of
> size at least six have a fourth perfect matching in their union.

It is Bogdanov's observation in the form we use it.  Equivalently: the
Krenn–Gu conjecture holds when there is no destructive interference (all
weights real positive), because then no cancellation can kill the fourth
matching.  Its published forms are the next two entries.

**[ChandranGajjala2026]** L. S. Chandran, R. Gajjala, *Edge-coloured
graphs with only monochromatic perfect matchings and their connection to
quantum physics*, arXiv:2202.05562 (v1 Feb 2022, v2 Nov 2023); Electron.
J. Combin. (2026) **[the journal volume/page/year is
[unverified] — arXiv v2 carries no journal-ref; earlier the paper
circulated as "Perfect matchings and quantum physics: progress on
Krenn's conjecture"]**.  Statement quoted **[primary]** from the arXiv
text:

> **Theorem 1.**  For a graph `G` which is non-isomorphic to `K_4`,
> `mu(G) <= 2` and `mu(K_4) = 3`.

introduced there with "Bogdanov observed the following".  The paper's
own contribution is the characterisation of `mu(G) = 1` and `mu(G) = 2`
(hence a fast algorithm for `mu`), and the resolution of Krenn–Gu for a
sub-class of graphs.

**Scope of the overlap — read this before disclosing one.**  Section 2 of
arXiv:2202.05562 works on a Hamiltonian cycle with even/odd vertices,
`C`-edges, **legal** edges (endpoints of equal parity), **illegal**
edges, **crossing pairs**, "nice crossing pairs" and **drums**.  A
*crossing pair* there means two edges that cross **with respect to the
cyclic vertex order of a Hamiltonian cycle**, and a *drum* is a 4-cycle
built from a nice crossing pair plus two cycle edges: cyclic-order
notions internal to their `d = 2` Type-2 classification.

* The one place this genuinely touches us is the Hamiltonian-cycle
  parity argument used to prove the three-one-factors lemma; see
  `notes/termwise-rank3-cubic-uniqueness.md` §3.0, which records that
  correspondence exactly.
* It does **not** touch our *crossing pairs*, which are pairs of sites
  straddling a **live split** of the site set — formally unrelated to a
  cyclic-order crossing.  Do not disclose an overlap there: none exists.
  The vocabulary "crossing pairs", "drums" and "legal/illegal edges"
  occurs in neither arXiv:2304.06407 nor arXiv:2407.00303.
  **[primary — checked against the paper sources]**

**[ChandranGajjalaIllickan2024]** L. S. Chandran, R. Gajjala,
A. M. Illickan, *Krenn–Gu conjecture for sparse graphs*, MFCS 2024,
LIPIcs **306**:41; arXiv:2407.00303.  Statement quoted **[primary]**:

> **Theorem 1.7.**  In a coloured multi-graph `G_c` with `|V(G)| > 4`, if
> there exist three monochromatic perfect matchings of different colours,
> then there must be a non-monochromatic perfect matching.

This is the **multigraph** form of Bogdanov's observation and is the
strongest form of the three-one-factors lemma we know; anything we prove
about simple graphs is weaker than it.

The rest of that paper is in the **general (bicoloured, multi-edge)
model**, and two of its results are load-bearing for us because they are
`d`-free — they constrain the open case directly:

> **Theorem 1.9.**  For a graph `G`, if `kappa(G) <= 2`, then
> `mu(G) <= 2`.

> **Theorem 1.10.**  Given a graph `G` with `kappa(G) <= 3` and
> `V(G) > 4`, there [is a graph `G'`] with `|V(G')| <= |V(G)| - 2` and
> `mu(G') >= mu(G)`.

Thm 1.10 is a **vertex-count reduction across a 3-cut**, valid for
multigraphs with bichromatic edges and with no hypothesis on `d`; it is
what makes a minimal counterexample 4-connected, and it is the
literature's working descent — note that it *deletes* vertices, the
opposite direction to our (empty) descent-from-`N = 10`.  Also there:
Krenn–Gu for maximum degree 3 (Thm 1.11), and `mu(G) <= 3` when the
minimum degree is 3 (Thm 1.12).

**Cross-check still open.**  Several of our artifacts are about *cubic*
objects — `notes/finite-obstruction.md` Cor. 7.2 (3-regular supports are
impossible), `notes/flat-cubic-boundary-core-order-eight-reduction.md`,
`notes/first-slice-cubic-three-factor-obstruction.md`.  These concern a
cubic **occurrence union derived inside a realization**, whereas Thm 1.11
hypothesises a cubic **input graph** (in our terms: every site meets
three pairs *and* each pair carries a single coloured cell).  Neither is
known here to subsume the other; this has not been checked, and should be
before any novelty claim about a cubic statement.

**[Lovasz1983]** L. Lovász, *Ear-decompositions of matching-covered
graphs*, Combinatorica **3** (1983) 105–117.  **[secondary —
bibliographic data not re-verified]**
The classical cousin, under a different hypothesis: a matching-covered
graph has exactly three perfect matchings iff it is a bi-subdivision of
`Theta` or of `K_4`.  Neither implies nor is implied by the
three-one-factors lemma (it assumes matching-coveredness and no
colouring, and its conclusion admits the non-cubic
`Theta`-bi-subdivisions).  Relevant to
`notes/three-cut-cp-uniqueness-tight-boundary.md` §4.

---

## Coverage of the conjecture, by model

**[CerveraLiertaKrennAspuruGuzik2022]** A. Cervera-Lierta, M. Krenn,
A. Aspuru-Guzik, *Design of quantum optical experiments with logic
artificial intelligence*, Quantum **6**, 836 (2022); arXiv:2109.13273.
**[primary — the ar5iv text was read]**  Verbatim:

> We test this approach to check if there exists a graph with
> monochromatic edges that generate the GHZ state of `n > 4` parties and
> `d >= n/2` local dimensions. […] We obtained `K =` False for `n` up to
> `8` and `d = n/2` colors.

and their Conjecture:

> It is not possible to generate a graph `G` with `n > 4` vertices and
> monochromatic edges each with one of `d >= n/2` possible colors, such
> that it contains single-colored PMs for each of these `d` colors while
> no PMs with other vertex colorings are generated (or the amount of
> these PMs does not allow cancellations).

**Read the scope exactly.**  (i) The verified cases are `n = 6, d = 3`
and `n = 8, d = 4` — `d = n/2` exactly; `d >= n/2` is their *conjecture*,
not their result.  (ii) It is the **MONOCHROMATIC-EDGE model**: the paper
states that with bicoloured edges "there could be more tri-colored PM,
allowing cancellations", which is what makes the general case hard.
(iii) The SAT variables are Boolean edge literals (present/absent), so
the argument is about supports, with cancellation handled only through
the escape clause "or the amount of these PMs does not allow
cancellations" — it is not a weighted no-go.
Consequently `N = 8, d = 3` and `N = 10, d = 3` in the
monochromatic-edge model are **not** covered by this paper, which is why
`proofs/diagonal-hafnian-recurrence-obstruction.md` is not subsumed by
it.

**[ChandranGajjala2024]** L. S. Chandran, R. Gajjala, *Graph-theoretic
insights on the constructability of complex entangled states*, Quantum
**8**, 1396 (2024); arXiv:2304.06407; DOI 10.22331/q-2024-07-03-1396.
**[primary — ar5iv text read]**  Introduces **local sparsification**
(edge pruning to a representative sparse graph) and proves, in the
general model:

> **Theorem 2.6.**  It is not possible to generate an `n > 4` vertex
> experiment graph with dimension `d >= n/sqrt(2)`.

improving on the earlier target

> **Conjecture 2.5.**  It is not possible to generate an `n > 4` vertex
> experiment graph with dimension `d >= n/2`.

Technique to adopt: the reduction goes by *deleting* vertices, not
extending them — the opposite direction to our (empty) descent-from-`N=10`.

**Two limits that matter for us** **[primary — checked against the paper
source]**: (i) the local-sparsification machinery is stated for **simple**
graphs, so it does not apply as-is to our aggregate multigraph objects;
(ii) it is **vacuous at `d = 3`** — its Observation 3.1 gives
`k(v) >= 2mu - n + 1`, which at `n = 8`, `mu = 3` reads `k(v) >= -1`.
This is the concrete reason the published `d > n/sqrt(2)` line does not
reach our target and why `d = 3` is not attackable by importing it
unchanged.

Adjacent notion worth acknowledging where our E1 / pendant facts are
stated: their **colour-isolated edge** (Lemma 2.4 of the Quantum paper) —
a monochromatic edge with colour-degree 1 at both endpoints.  The
statements differ (theirs is an edge-minimality argument, ours a
vanishing-row condition), so this is adjacency, not overlap.

**[Tsoukalas2026]** G. Tsoukalas, A. Kovsharov, S. Shirobokov, A. Surina,
M. Firsching, G. Bérczi, F. J. R. Ruiz, A. Suggala, A. Z. Wagner,
E. Wieser, L. Yu, A. Huang, M. Z. Horváth, A. Ferraiuolo, H. Michalewski,
E. Lockhart, C. Grosu, T. Hubert, M. Balog, P. Kohli, S. Chaudhuri,
*Advancing Mathematics Research with AI-Driven Formal Proof Search*,
arXiv:2605.22763 (May 2026).  **[primary — title/authors/date; the
in-paper treatment of this problem was not read]**
This is the DeepMind formal-proof-search paper behind the `d = N` results
now marked *solved* in [LeanMQG]
(`eqSystem_no_solution_even_ge4_d_eq_n_explicit` and its corollaries).
**Correction to earlier internal notes:** M. Krenn is *not* an author of
arXiv:2605.22763; the Krenn/Firsching/Tsoukalas/Gajjala/Gu/Chaudhuri
tensor-algebraic no-go is a separate work *in preparation*, cited there.
Neither covers `d = 3`.

**[VardiZhang2022]** M. Y. Vardi, Z. Zhang, *Quantum-Inspired Perfect
Matching under Vertex-Color Constraints*, arXiv:2209.13063.
**[primary — title/authors/abstract]**
Complexity of EXISTS-PMVC (perfect matching under vertex-colour
constraints on bicoloured-edge graphs): NP-hardness for the
decision-diagram variant, polynomial equivalence with Exact Perfect
Matching for symmetric constrained versions on bounded colours.
**Caution:** an earlier internal note described this reference as a
Tutte-theorem-based Boolean encoding verifying Dicke states to `n = 40`;
that description is **not** supported by this paper's abstract and may
belong to a different Vardi–Zhang paper.  Verify before relying on it.

---

## Formalization

**[LeanMQG]** DeepMind *formal-conjectures*,
`FormalConjectures/Paper/MonochromaticQuantumGraph.lean`,
https://github.com/google-deepmind/formal-conjectures .
**[primary — the file was read on 2026-08-04]**

The model is **GENERAL / BICOLOURED**, verbatim:

```lean
structure EdgeN (N D : Nat) where
  u : V N
  v : V N
  i : Fin D
  j : Fin D

abbrev WeightsN (N D : Nat) (α : Type) := EdgeN N D → α
```

i.e. one weight per (edge, colour at `u`, colour at `v`) — exactly our
`A_uv(i,j)` with `i != j` allowed.  `EqSystemN N D W` quantifies over
every `ι : V N → Fin D` and requires `pmSumN N D W ι = 1` if `ι` is
constant and `= 0` otherwise — exactly our exactness condition
`H_B(A) = Delta_{B,d}`.

Status of the statements, as of 2026-08-04 (`@[category …]`
annotations):

| statement | status |
|---|---|
| `eqSystem4_has_solution_d2`, `eqSystem4_has_solution_d3`, `eqSystem6_has_solution_d2` | test (witnesses) |
| `eqSystem4_no_solution_nnreal_ge4`, `eqSystem_no_solution_nnreal_even_ge6_ge3` | research **solved** (the non-negative-real case = Bogdanov) |
| `eqSystem_no_solution_even_ge4_d_eq_n_explicit`, `eqSystem4_no_solution_d4`, `eqSystem4_no_solution_ge4`, `eqSystem6_no_solution_d6`, `eqSystem8_no_solution_d10` | research **solved**, with formal proofs linked |
| **`eqSystem6_no_solution_d3`**, `eqSystem6_no_solution_d4`, `eqSystem6_no_solution_d5`, `eqSystem6_no_solution_ge3` | research **OPEN** |
| **`eqSystem8_no_solution_d3`** | research **OPEN** |
| `eqSystem10_no_solution_d3` … `d9`, `eqSystem12/14/16_no_solution_d3`, `eqSystem_no_solution_ge6_ge3` | research **OPEN** |
| the `_real`, `_int` and `_trinary_int` analogues at `N = 6, 8, 10` | research **OPEN** |

All `research` statements carry `sorry`; "solved" means solved
mathematically (with a formal proof linked where one exists), "open"
means research open.

**Consequences for this repository.**

* `N = 8, d = 3` over `C` in the general model — our top-level target —
  is `eqSystem8_no_solution_d3`, marked **research open**.  It is the
  field's named next case.
* `N = 6, d = 3` over `C` in the general model is `eqSystem6_no_solution_d3`,
  also **research open**.  Our
  `proofs/six-site-arbitrary-complex-obstruction.md` Theorem 1.1 is
  stated in the general model, so if it holds it settles that case; it is
  under independent verification and is a **claim under review**, not a
  result.
* In the **monochromatic-edge** model, `N = 8, d = 3` and `N = 10, d = 3`
  are settled by our own
  `proofs/diagonal-hafnian-recurrence-obstruction.md`, which is why every
  diagonal-family artifact must carry its model qualifier: without it, a
  reader takes it for an attack on a case we have already closed.

**Bibliographic errata in the Lean file's own reference list** (do not
copy them): the authors of arXiv:2202.05562 are listed as
"N. Chandran, S. Gajjala" (correct: L. Sunil Chandran, Rishikesh
Gajjala); those of arXiv:2407.00303 as "N. Chandran, S. Gajjala,
S. Illickan, M. Krenn" (correct: L. Sunil Chandran, Rishikesh Gajjala,
Abraham M. Illickan — M. Krenn is not an author); and Soltész's initial
is given as "U." (correct: D., Daniel).

---

## Where these are used in this repository

* The **three-one-factors lemma** ([Bogdanov2017], published as
  [ChandranGajjala2026] Thm 1 and [ChandranGajjalaIllickan2024] Thm 1.7)
  is invoked in `proofs/odd-near-perfect-gadget-obstruction.md`,
  `proofs/selected-one-factor-cancellation-cycle.md`,
  `notes/finite-obstruction.md`, `notes/binary-entry-minimal-normal-form.md`,
  `notes/dual-rail-padding-obstruction.md`,
  `notes/first-slice-cubic-three-factor-obstruction.md`,
  `notes/fixed-star-common-cofactor-rigidity.md`,
  `notes/fixed-star-three-hole-gauge-dichotomy.md`,
  `notes/flat-cubic-boundary-core-order-eight-reduction.md` (and its
  independent audit), `notes/kruskal-visible-wick-rank-gap.md`,
  `notes/scalar-unit-pivot-global-potential-anchor-matching.md`,
  `notes/three-cut-cp-uniqueness-tight-boundary.md`,
  `notes/torus-osculation-bottom-top-collision.md`,
  `notes/triple-matching-rewrite.md`,
  `notes/termwise-rank3-cubic-uniqueness.md` (Theorem B), and
  `computations/verify_three_cut_cp_uniqueness_tight_boundary.py`.
  Self-contained proofs of it are given in
  `proofs/odd-near-perfect-gadget-obstruction.md` and
  `notes/finite-obstruction.md` §7 (kept because the audit discipline
  requires every consumed statement to be proved or cited to a checked
  source — no priority is claimed for any of them).
* `notes/termwise-rank3-cubic-uniqueness.md` §3.0 works out the exact
  relation between its Theorem B and the published forms.
