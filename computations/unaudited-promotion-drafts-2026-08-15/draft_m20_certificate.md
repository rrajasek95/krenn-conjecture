> **UNAUDITED DRAFT — not spine.**  Drafted 2026-08-15 at pinned repository
> HEAD `e0c4d7c548dd1b252a87b3fc16e76182a3a0bbfb` (recorded in
> `PINNED_HEAD.txt` beside this file).  It becomes spine only when committed
> through the supersession discipline of `certification/SUPERSESSIONS.md`,
> with the pre-commit items of `draft_promotion_checklist.md` discharged.
> All paths are repository-root-relative.

# The eight-word certificate: the m = 20 survivor template at N = 8 carries no exact source

**Proposed status on promotion: `[P]` — proved by a hand-checkable
certificate, machine-confirmed by three independent routes, independently
re-audited (A4).**

## 0. Setting and notation

Eight sites `B = {0,...,7}`, three colours, one endpoint-ordered block
`A_uv` in `C^{3x3}` per pair `u < v` (rows = colour at `u`, columns = colour
at `v`).  For a word `w` in `{0,1,2}^8`,

```text
H_w(A) = sum over the 105 perfect matchings M of K_8 of
         prod_{uv in M} A_uv[w_u][w_v].
```

A source is **exact** when `H_w = 0` at all 6,558 mixed words and
`H_{c^8} != 0` for `c = 0,1,2` (the three constant values may be normalised
to 1 by the diagonal gauge of `draft_gauge_lemma.md` §1, so this is the
standard exactness system).  The **template** of a source is its support
pattern: `T[uv]` is the 9-bit mask whose bit `3i + j` records that the cell
`A_uv[i][j]` is nonzero.  In this notation:

> a source with template `T` is a choice of **nonzero** values on the
> occupied cells of `T` such that every mixed fibre sums to zero and the
> constant fibres do not
> (`computations/unaudited-thickfibre-w12-2026-08-15/w12_core.py`, module
> docstring).

Write `x_{uv,ij} := A_uv[i][j]` for the value at an occupied cell, and
`m = supp(T)` (number of nonzero blocks), `Sigma(T)` (number of occupied
cells), `beta` (number of single-cell blocks).

**Terminology guard** (`notes/2026-08-15-conventions-and-hazards.md`, items
1–2).  No sense of "clean" is used in this document.  The template below is a
*SAT template witness* in the sense of the W8/W11 support enumeration — not a
cap witness `(p,q,K)` and not the legacy `C_{u,r} = 0` site.

## 1. The template

`T20` is the survivor of W8's CEGAR search at support `m = 20`, with
`Sigma = 58` and `beta = 9`.  In the fixed edge order
`combinations(range(8), 2)` its 28 masks are

```text
[256, 0, 16, 0, 0, 0, 1, 1, 6, 2, 7, 7, 16, 292,
 146, 511, 511, 0, 129, 256, 448, 0, 56, 16, 256, 511, 0, 0]
```

which decodes to the twenty nonzero blocks

| pair | mask | occupied cells | class |
|---|---|---|---|
| 01 | 256 | (2,2) | single |
| 03 | 16 | (1,1) | single |
| 07 | 1 | (0,0) | single |
| 12 | 1 | (0,0) | single |
| 13 | 6 | (0,1), (0,2) | thin |
| 14 | 2 | (0,1) | single |
| 15 | 7 | (0,0), (0,1), (0,2) | thin |
| 16 | 7 | (0,0), (0,1), (0,2) | thin |
| 17 | 16 | (1,1) | single |
| 23 | 292 | (0,2), (1,2), (2,2) | thin |
| 24 | 146 | (0,1), (1,1), (2,1) | thin |
| **25** | **511** | all nine | full |
| **26** | **511** | all nine | full |
| 34 | 129 | (0,0), (2,1) | fat |
| 35 | 256 | (2,2) | single |
| 36 | 448 | (2,0), (2,1), (2,2) | thin |
| 45 | 56 | (1,0), (1,1), (1,2) | thin |
| 46 | 16 | (1,1) | single |
| 47 | 256 | (2,2) | single |
| **56** | **511** | all nine | full |

Its full-block graph is the triangle `Gamma(T20) = {25, 26, 56}` — three
edges on three of the eight sites, hence not spanning, so the boundary
proposition W12-C (`draft_cut_mechanism.md` §4) predicts a feasible cut here,
and indeed all 63 even cuts are feasible.  The template is thick in the sense
that matters for W8's immunity screen: its mixed-fibre histogram is
`{2: 90, 3: 42, 8: 8, 10: 12, 12: 6, 15: 1}` over 159 live mixed words
(`computations/unaudited-thickfibre-w12-2026-08-15/results_t1a_survivor.json`),
matching W8's recorded histogram for this survivor exactly.

## 2. Theorem

> **Theorem (m = 20 kill).**  There is no exact source with template `T20`.
>
> More precisely, and this is what the proof uses: there are no complex
> values on the occupied cells of `T20`, all nonzero, such that the seven
> mixed words
>
> ```text
> w1 = 00011000,  w2 = 00011020,  w3 = 00111000,  w4 = 00111020,
> w5 = 00100000,  w6 = 00100020,  w7 = 00000020
> ```
>
> all have vanishing fibre sums and the constant word `c0 = 00000000` has a
> nonvanishing one.

The hypotheses actually consumed are therefore: *the eighteen named cells are
nonzero, seven named mixed coefficients vanish, and one named constant
coefficient does not*.  No admissibility condition — not (SC), not (SC+), not
the singleton screen, not the J.1d budget — enters the argument.  Only 8 of
the template's 162 live words are used.

## 3. Proof

Expanding the eight fibres over the 105 perfect matchings of `K_8` and using
only the occupied cells of `T20` gives, with the common nonzero factors
`x_{07,00} x_{13,01}` (for `w1,...,w4`) and `x_{07,00} x_{34,00}` (for
`w5, w6, w7, c0`) divided out:

```text
w1 = 00011000 :  x_{24,01} x_{56,00} + x_{26,00} x_{45,10}                     = 0
w2 = 00011020 :  x_{24,01} x_{56,02} + x_{26,02} x_{45,10}                     = 0
w3 = 00111000 :  x_{24,11} x_{56,00} + x_{26,10} x_{45,10}                     = 0
w4 = 00111020 :  x_{24,11} x_{56,02} + x_{26,12} x_{45,10}                     = 0
w5 = 00100000 :  x_{15,00} x_{26,10} + x_{16,00} x_{25,10}                     = 0
w6 = 00100020 :  x_{15,00} x_{26,12} + x_{16,02} x_{25,10}                     = 0
w7 = 00000020 :  x_{12,00} x_{56,02} + x_{15,00} x_{26,02} + x_{16,02} x_{25,00} = 0
c0 = 00000000 :  x_{12,00} x_{56,00} + x_{15,00} x_{26,00} + x_{16,00} x_{25,00} != 0
```

(The unreduced fibres, monomial by monomial, are recorded in
`computations/unaudited-thickfibre-w12-2026-08-15/results_t1d_certificate.json`,
key `fibres`; the eighteen variables occurring are listed there under
`variables_used`.)

**Step 1 — three fibre-proportionality pairs.**  All occupied cells are
nonzero, so we may divide.

* From `w1` and `w2`: `x_{24,01} x_{56,00} = -x_{26,00} x_{45,10}` and
  `x_{24,01} x_{56,02} = -x_{26,02} x_{45,10}`; dividing (legitimate, since
  `x_{24,01}, x_{45,10}, x_{56,02}, x_{26,02} != 0`) gives

  ```text
  x_{56,00} / x_{56,02} = x_{26,00} / x_{26,02}.
  ```

* From `w3` and `w4`, the same division with `x_{24,11}` in place of
  `x_{24,01}`:

  ```text
  x_{56,00} / x_{56,02} = x_{26,10} / x_{26,12}.
  ```

* From `w5` and `w6` (dividing by `x_{15,00}` and `x_{25,10}`):

  ```text
  x_{26,10} / x_{26,12} = x_{16,00} / x_{16,02}.
  ```

**Step 2 — one scalar.**  Put `lambda := x_{56,00} / x_{56,02}`, a nonzero
scalar.  Chaining the three identities,

```text
x_{56,00} = lambda x_{56,02},   x_{26,00} = lambda x_{26,02},
x_{16,00} = lambda x_{16,02}.
```

**Step 3 — the constant fibre is proportional to a mixed fibre.**
Substituting into `c0`:

```text
x_{12,00} x_{56,00} + x_{15,00} x_{26,00} + x_{16,00} x_{25,00}
  = lambda ( x_{12,00} x_{56,02} + x_{15,00} x_{26,02} + x_{16,02} x_{25,00} )
  = lambda * (fibre of w7)
  = 0,
```

contradicting `H_{0^8} != 0`.  ∎

**The mechanism.**  Two fibre polynomials — one mixed (`w7`), one constant
(`c0`) — become proportional modulo the relations extracted from the other
six words.  This is invisible to a monomial-comparison engine that works
inside a single fibre: the binomial/lattice screens of the W8 layer compare
monomials *within* one fibre and never across two, which is exactly why this
template survived them.

## 4. Independent machine confirmations

1. **Rabinowitsch certificate over `Q`** (the certificate above, verified
   symbolically).  The script writes and runs a Singular query in the
   polynomial ring on the eighteen used variables plus one Rabinowitsch
   variable `t`, forming `J = I + <t * (prod of the variables) * (c0 fibre) -
   1>` and reducing `1` modulo `std(J)`; the recorded output is `CERT 1`,
   i.e. the ideal is the unit ideal, so no point with all cells nonzero
   satisfies the seven mixed equations and keeps `c0` nonzero.
   Artifact: `computations/unaudited-thickfibre-w12-2026-08-15/run_t1d_certificate.py`,
   `results_t1d_certificate.json` (`singular_output = "CERT 1"`,
   `certificate_verified = true`).
2. **Cut extraction** (`draft_cut_mechanism.md` §3, Theorem W12-B): at the
   even cut `L = {0,1,3,7}`, `R = {2,4,5,6}` the extraction produces a
   half-system on the `R`-cells in which a pinned sub-word is forced to
   vanish — `immediate_contradiction = [[1,1,1,1]]`, from 3 pinned `L`
   sub-words, 81 forced-zero words and 27 live zero-equations on 34
   variables.  Time 0.6 s.  Artifact:
   `computations/unaudited-thickfibre-w12-2026-08-15/run_t3_cut.py`,
   `results_t3_cut_core.json` (record 0).
3. **Full Groebner / torus route**: the mixed-only system and the full system
   both reduce to the unit ideal (`ONEM 1`, `ONEJ 1`) after the reduction
   step; the reduced torus data is `d = 39`, binomial rank 27, free dimension
   12, elementary divisors `[1]`.  Artifact:
   `computations/unaudited-thickfibre-w12-2026-08-15/run_t1c_survivor_groebner.py`,
   `results_t1c.json`.

## 5. Minimality — stated relative to its frame

Per `notes/2026-08-15-conventions-and-hazards.md` item 15, minimality is
asserted **relative to the frame**: here the frame is *this word set together
with the divided-out multiplier* `x_{07,00} x_{13,01}` / `x_{07,00}
x_{34,00}` and the eighteen-variable ring above.

* **Word-set minimality.**  Dropping any one of the seven mixed words
  destroys the certificate: all seven entries of `mutation_drop_one_equation`
  are `false` (`false` = "the reduced set no longer forces the
  contradiction", i.e. the word is load-bearing).  Artifact:
  `results_t1d_certificate.json`, key `mutation_drop_one_equation`.
* **Audit strengthening (A4).**  A4 replaced this leave-one-out test by
  *explicit exact witnesses*: for each dropped word it exhibits a rational
  point satisfying the remaining six mixed equations with all cells nonzero
  and `c0 != 0`.  This is strictly stronger than a failed ideal-membership
  query, since it rules out the possibility that the drop merely exceeded a
  solver budget.  Artifacts:
  `computations/unaudited-audit-a4-w12w10-2026-08-15/chk01_engine_and_certificate.py`,
  `chk02_certificate_singular_and_mutations.py`, `results_chk01.json`,
  `results_chk02.json`.
* **Specificity.**  The same seven equations do **not** force the other two
  constant coefficients to vanish: the control returns `false` for `1^8` and
  `2^8` (`results_t1d_certificate.json`, key `control_other_constants`).  The
  certificate is a statement about the colour-0 constant fibre of this
  template, not a generic degeneration.
* **Discriminating checker control.**  Of the 58 single-cell deletions from
  `T20`, exactly one yields a template the engine does *not* kill, so the
  checker is not a trivially-always-kill procedure
  (`results_t8b_mutation.json`, key `S4`).

## 6. Scope

* The theorem is about the template `T20` — sources whose support is exactly
  `T20`.  Sources with strictly smaller support are different templates and
  are covered (at this support level) by the separate W8/W11 support
  enumeration, not by this certificate.
* Nothing here is a statement about the support **level** `m = 20`: it is one
  template.  The level-wide statement at `m = 20..23` is the cut mechanism of
  `draft_cut_mechanism.md` applied to the enumerated templates, and it is a
  statement about *known* templates plus the `Gamma` predicate, not an
  exhaustive sweep.
* The certificate consumes no admissibility hypothesis, so it survives any
  later revision of the admissibility conventions ((SC), (SC+), the J.1d
  budget).

## 7. Certificates and checkers

| item | artifact |
|---|---|
| model, template masks, fibres, value system | `computations/unaudited-thickfibre-w12-2026-08-15/w12_core.py` |
| template provenance (W8 survivor at `m = 20`, `Sigma = 58`) and calibration against W8's histogram | `computations/unaudited-thickfibre-w12-2026-08-15/run_t4_calibration.py`, `results_t4_calibration.json` (`expected_m_sigma_beta = [20, 58, 9]`, `ms_match = true`) |
| survivor anatomy (159 live mixed words, fibre histogram, lattice ranks) | `run_t1a_survivor_analysis.py`, `results_t1a_survivor.json` |
| the eight-word certificate, its Singular confirmation, leave-one-out and specificity controls | `run_t1d_certificate.py`, `results_t1d_certificate.json` |
| independent cut kill | `run_t3_cut.py`, `results_t3_cut_core.json` (record 0) |
| independent Groebner/torus kill | `run_t1c_survivor_groebner.py`, `results_t1c.json` |
| single-cell deletion discrimination control | `run_t8b_mutation.py`, `results_t8b_mutation.json` |
| independent re-verification (200 generic rational points; independent saturation; own Rabinowitsch; per-word exact witnesses) | `computations/unaudited-audit-a4-w12w10-2026-08-15/chk01_engine_and_certificate.py`, `chk02_certificate_singular_and_mutations.py`, `results_chk01.json`, `results_chk02.json` |

## 8. Audit record

* **Source lane:** `computations/unaudited-thickfibre-w12-2026-08-15/REPORT.md`
  (W12, unaudited; exact arithmetic — `int`/`Fraction`, Singular over `Q` —
  for every verdict; the one float search in that lane carries no verdict and
  is not used here).
* **Independent audit:** `computations/unaudited-audit-a4-w12w10-2026-08-15/REPORT.md`
  (A4; from-scratch engine on deliberately different routes — bitmask
  matchings, active-subgraph fibres, canonical polynomial dictionaries,
  direct Groebner on half variables, no lattice/Smith/torus code; exact
  arithmetic including `Q(i)`).
* **Verdict:** CONFIRMED — "**m=20 survivor kill + eight-word certificate:
  CONFIRMED three ways (200 generic rational points; independent saturation;
  own Rabinowitsch); leave-one-out STRENGTHENED to explicit exact witnesses
  for each dropped word; specificity confirmed (does not force F(1^8),
  F(2^8)).**"  A4 records no mathematical discrepancy against this
  certificate.
* **Corrections adopted in this draft:** minimality is stated frame-relative
  (ledger item 15) and in A4's strengthened witness form; the multiplier that
  was divided out is named explicitly rather than left implicit.
* **Pre-commit obligations:** the items of §C and §A of
  `draft_promotion_checklist.md` — in particular the Singular artifacts must
  be re-run under the current hygiene rules (stdout `?`-parsing, the
  no-shadowing guard, and the explicit-point control), all of which postdate
  this certificate.
