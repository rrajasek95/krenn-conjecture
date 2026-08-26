> **UNAUDITED DRAFT — not spine.**  Drafted 2026-08-15 at pinned repository
> HEAD `e0c4d7c548dd1b252a87b3fc16e76182a3a0bbfb` (recorded in
> `PINNED_HEAD.txt` beside this file).  It becomes spine only when committed
> through the supersession discipline of `certification/SUPERSESSIONS.md`,
> with the pre-commit items of `draft_promotion_checklist.md` discharged.
> All paths are repository-root-relative.

# The six-word certificate: the m = 24 residual template at N = 8 carries no exact source

**Proposed status on promotion: `[P]` — proved by a hand-checkable
certificate, machine-confirmed by four independent routes, independently
re-audited (A6), whose audit replaced the source lane's certificate by a
strictly stronger one.**

## 0. Setting

Notation is that of `draft_cut_mechanism.md` §0: eight sites `B = {0,...,7}`,
three colours, endpoint-ordered blocks `A_uv` in `C^{3x3}`, word coefficients

```text
H_w(A) = sum_{M in PM(B)} prod_{uv in M} A_uv[w_u][w_v],
```

templates as 9-bit masks per pair, and "a source with template `T`" meaning
nonzero values on the occupied cells of `T`.  A block with all nine cells
occupied is **full**; `Gamma(T)` is the graph of the full blocks.

**Terminology guard** (`notes/2026-08-15-conventions-and-hazards.md` items
1–2, and the conflation audit A6 records).  Two distinct cleanness notions
appear here, and they are **not** the *slice-clean* or *cut-clean* senses:

* a word `w` is **word-clean** (W15's syntactic notion) when no single-cell
  block is active on it, i.e. no single-cell block `A_uv` with occupied cell
  `(i,j)` has `w_u = i` and `w_v = j`;
* a word `w` is **effectively clean** when its fibre is exactly the set
  `F(Gamma)` of perfect matchings all of whose blocks are full.

Word-clean implies effectively clean; the converse fails, and the gap is
load-bearing here — the constant word `0^8` is effectively clean but not
word-clean.  At this template there are **2,152** word-clean words (all
mixed) and **2,952** effectively clean words (2,951 mixed, plus the single
constant word `0^8`).

## 1. The template

`T24` is W8's immunity template at support `m = 24`.  In the fixed edge order
`combinations(range(8), 2)` its 28 masks are

```text
[511, 511, 511, 1, 2, 4, 511, 511, 511, 511, 8, 16, 4, 511,
 8, 0, 128, 32, 64, 128, 0, 256, 511, 0, 511, 511, 0, 511]
```

with `m = 24`, `Sigma = 120`.  Structurally:

* **twelve full blocks**, forming
  `Gamma = K_4 on {0,1,2,3}  u  C_4 on 4-5-6-7-4  u  {07, 14}`, i.e. the
  edge set `{01, 02, 03, 12, 13, 23} u {45, 56, 67, 47} u {07, 14}`.
  `Gamma` is spanning and 2-connected, so by Theorem W12-C
  (`draft_cut_mechanism.md` §4) **no cut is feasible** and the entire cut
  mechanism has empty input on this template;
* **twelve single-cell blocks**:
  `04:(0,0)`, `05:(0,1)`, `06:(0,2)`, `15:(1,0)`, `16:(1,1)`, `17:(0,2)`,
  `24:(1,0)`, `26:(2,1)`, `27:(1,2)`, `34:(2,0)`, `35:(2,1)`, `37:(2,2)`;
* **four empty blocks**: `25`, `36`, `46`, `57`.  The two empty `R`-side
  blocks `46` and `57` are the chords of the `C_4`, which is why the
  right-hand half-permanent below has two terms rather than three.

`F(Gamma)`, the set of perfect matchings all of whose blocks are full, has
seven elements:

```text
(01)(23)(45)(67)   (01)(23)(47)(56)   (02)(13)(45)(67)   (02)(13)(47)(56)
(03)(12)(45)(67)   (03)(12)(47)(56)   (07)(14)(23)(56)
```

Every one of them is supported on **every** word, so `F(Gamma)` is contained
in every fibre.  The minimum mixed fibre size is 7, and the three constant
fibres have sizes 7, 8, 8 for `0^8`, `1^8`, `2^8`.

## 2. The clean shape and the constant word

Write a word as `w = (x, y)` with `x = (w_0,w_1,w_2,w_3)` on the left sites
and `y = (w_4,w_5,w_6,w_7)` on the right.  Put

```text
P_L(x) = A01[x0][x1] A23[x2][x3] + A02[x0][x2] A13[x1][x3]
                                  + A03[x0][x3] A12[x1][x2],
P_R(y) = A45[y4][y5] A67[y6][y7] + A47[y4][y7] A56[y5][y6].
```

> **Lemma (clean shape).**  For every effectively clean word `w = (x,y)`,
>
> ```text
> H_w = P_L(x) P_R(y) + A07[x0][y7] A14[x1][y4] A23[x2][x3] A56[y5][y6].
> ```

This is just the enumeration of `F(Gamma)`: the six matchings of the first
two rows contribute `P_L P_R`, and `(07)(14)(23)(56)` contributes the second
term.  The shape was verified on all 2,952 effectively clean words (A6) and
on the 2,152 word-clean ones (W15), with a control confirming that it fails
off the clean stratum (0 of 201 non-clean words agree).

> **Lemma (the constant word `0^8` is effectively clean).**  The only
> single-cell block active on `0^8` is `A04[0][0]`, and no `T24`-supported
> perfect matching uses the edge `04`.  Hence the fibre of `0^8` is exactly
> `F(Gamma)` and `H_{0^8} = P_L(0000) P_R(0000) + A07[0][0] A14[0][0]
> A23[0][0] A56[0][0]`.

Both a crossing-parity derivation and a direct enumeration (0 supported
matchings through `A04[0][0]`) confirm it.  The other two constant words have
fibres of size 8 — they are *not* effectively clean — which is why the kill
targets `0^8` specifically.

## 3. Atoms

All quantities below are values of occupied cells, hence nonzero on any
source with template `T24`:

```text
U0 = A07[0][0]   U1 = A07[1][0]   C = A23[0][0]   S00 = A56[0][0]   S20 = A56[2][0]
V00 = A14[0][0]  V01 = A14[0][1]  V20 = A14[2][0] V21 = A14[2][1]

K  = U1 C S20     K' = U0 C S20     J  = U1 C S00     J' = U0 C S00
```

so that the *atom identity*

```text
J K' = U0 U1 C^2 S00 S20 = K J'                                      (A)
```

holds identically.  For the left and right half-permanents:

```text
L0 = P_L(0000),  L1 = P_L(1000),  L2 = P_L(1200),
R0 = P_R(0000),  Ra = P_R(0200),  Rb = P_R(1200).
```

## 4. Theorem

> **Theorem (m = 24 kill).**  There is no exact source with template `T24`.
>
> More precisely, there are no complex values on the occupied cells of `T24`
> for which the five mixed words
>
> ```text
> w1 = 10000200,  w2 = 10001200,  w3 = 12000200,
> w5 = 00001200,  w6 = 12000000
> ```
>
> have vanishing coefficients, the five cells
> `A07[1][0], A23[0][0], A56[2][0], A14[0][1], A14[2][0]` are nonzero, and
> `H_{0^8} != 0`.

The hypotheses consumed are exactly: **five named cells nonzero, five named
mixed coefficients zero, and the one constant coefficient `H_{0^8}` nonzero**.
No admissibility condition and no property of the remaining 100-odd cells is
used.  (By Lemma W10-G of `draft_gauge_lemma.md`, "mixed coefficients vanish
and the pure coefficients are nonzero" is equivalent to exactness up to
gauge, so the theorem is a statement about exactness at this template.)

## 5. Proof

By §2, the five mixed words and the constant word are all effectively clean,
and their coefficients take the normal forms

```text
E1 = H_{w1} = L1 Ra + K V00          (w1 = 10000200)
E2 = H_{w2} = L1 Rb + K V01          (w2 = 10001200)
E3 = H_{w3} = L2 Ra + K V20          (w3 = 12000200)
E5 = H_{w5} = L0 Rb + K' V01         (w5 = 00001200)
E6 = H_{w6} = L2 R0 + J V20          (w6 = 12000000)
G  = H_{0^8} = L0 R0 + J' V00        (the constant word)
```

— each read off the clean shape.  (For instance `w1 = 10000200` has
`x = (1,0,0,0)` and `y = (0,2,0,0)`, so `P_L(x) = L1`, `P_R(y) = Ra`, and the
seventh matching contributes `A07[1][0] A14[0][0] A23[0][0] A56[2][0] =
K V00`.)

**The certificate.**  In `Z[occupied cells]` the following identity holds:

```text
K^2 V01 V20 * G  =  J K' V01 V20 * E1
                  - L0 R0 L2 Ra   * E2
                  + K V01 L0 R0   * E3
                  + L1 Ra L2 R0   * E5
                  - K' V01 L1 Ra  * E6.                              (B)
```

*Proof of (B).*  Substitute the normal forms into the right-hand side and
expand:

```text
  J K' V01 V20 (L1 Ra + K V00)     =  J K' V01 V20 L1 Ra  +  J K' K V01 V20 V00
- L0 R0 L2 Ra  (L1 Rb + K V01)     = -L0 L1 L2 Ra Rb R0   -  K V01 L0 R0 L2 Ra
+ K V01 L0 R0  (L2 Ra + K V20)     = +K V01 L0 R0 L2 Ra   +  K^2 V01 V20 L0 R0
+ L1 Ra L2 R0  (L0 Rb + K' V01)    = +L0 L1 L2 Ra Rb R0   +  K' V01 L1 Ra L2 R0
- K' V01 L1 Ra (L2 R0 + J V20)     = -K' V01 L1 Ra L2 R0  -  J K' V01 V20 L1 Ra
```

Four pairs of terms cancel, each pair appearing once with each sign:
`L0 L1 L2 Ra Rb R0` (rows 2 and 4), `K V01 L0 R0 L2 Ra` (rows 2 and 3),
`K' V01 L1 Ra L2 R0` (rows 4 and 5), and `J K' V01 V20 L1 Ra` (rows 1 and 5).
What survives is

```text
J K' K V01 V20 V00 + K^2 V01 V20 L0 R0
  = K^2 V01 V20 ( J' V00 + L0 R0 )        [by the atom identity (A)]
  = K^2 V01 V20 * G,
```

which is the left-hand side. ∎

**Conclusion.**  Assume a source with template `T24` has `H_{w} = 0` at the
five mixed words `w1, w2, w3, w5, w6`.  Then every term on the right of (B)
vanishes, so `K^2 V01 V20 * H_{0^8} = 0`.  But `K = A07[1][0] A23[0][0]
A56[2][0]`, `V01 = A14[0][1]` and `V20 = A14[2][0]` are products of occupied
cells, hence nonzero.  Therefore `H_{0^8} = 0`, contradicting `H_{0^8} != 0`.
No exact source has template `T24`. ∎

**The mechanism.**  Every matching of full blocks is supported on every word,
so each coefficient is `Phi(x,y)` — the `Gamma`-matching sum — plus the
"extra" monomials contributed by matchings that use a single-cell block.  A
word whose fibre carries no extras is effectively clean, and there the mixed
equations are equations on `Phi` alone.  The kill is the case `k = 0`: a
*constant* word is effectively clean, so the clean mixed equations force
`Phi = 0` at a point where it must be nonzero.  This mechanism ignores the
2-connectivity of `Gamma` entirely, which is what lets it operate exactly
where the cut mechanism cannot.

## 6. Minimality, stated relative to its frame

Per `notes/2026-08-15-conventions-and-hazards.md` item 15, every minimality
claim below names its frame; the three recorded claims in the corpus are
consistent only when read that way.

* **Word-set minimality, at the multiplier `K^2 V01 V20`.**  No four of the
  five mixed words suffice.  Proved twice: (i) five **explicit exact rational
  witnesses** — for each dropped word, a point with all 108 full-block cells
  nonzero satisfying the four retained equations with `G != 0`, stored as
  `computations/unaudited-audit-a6-w15w14-2026-08-15/witness_drop_w{1,2,3,5,6}.json`
  (with `G = -3682/25, -3133/810, 1593/32, 1292/1125, 6076/75` respectively);
  (ii) Singular **saturation**: `G` is not in the saturation of any
  four-generator sub-ideal by the named cells (five `expect 0` probes, all
  0).
* **Multiplier minimality is a different frame.**  Within the family
  `K^a V21^b` and for the ideal generated by the **six** mixed words
  `w1,...,w6`, the multiplier `K^2 A14[2][1]` suffices and each of its three
  factors is necessary (the three one-factor weakenings all fail).  A
  separate exhaustive search over exponent vectors on the four base cells
  finds a strictly smaller degree-6 multiplier
  `A07[1][0]^2 A23[0][0] A56[2][0]^2 A14[2][1]` for that same six-word ideal
  (`computations/unaudited-residual2-w16-2026-08-15/w16_m24b.py`,
  `results_m24b.json`; that lane is unaudited, and the item is recorded here
  only to keep the frames straight).
* **The source lane's "leave-one-out 6/6" is refuted as a word-set claim.**
  W15's seven-word certificate (six mixed words `w1,...,w6` plus the constant,
  multiplier `A07[1][0]^4 A23[0][0]^3 A56[2][0]^3 A14[2][1]^2`) is correct as
  an identity, and its leave-one-out control is correct *for that
  multiplier*; but `w4 = 12001200` is redundant — the five-word certificate
  (B) omits it.  Singular reproduces both facts: W15's multiplier does not
  put `G` in the five-word ideal (which is why its control fired), while
  `K^2 V01 V20` does.

## 7. Non-vacuity

A kill of this shape would be worthless if the clean subsystem were
infeasible.  It is not:

> There is an **exact rational point** with all 108 cells of the twelve full
> blocks nonzero which satisfies **every one of the 2,951 effectively clean
> mixed equations** (hence also all 2,152 word-clean ones), on which `Phi`
> vanishes identically at all 6,561 words, and which therefore has
> `H_{0^8} = 0`.

The point is constructed from scratch by the audit — the full blocks are
given rank-one shapes making `P_L P_R` cancel the seventh matching
identically — and is stored at
`computations/unaudited-audit-a6-w15w14-2026-08-15/a6_nonvacuity_point_seed11.json`
(three seeds run, identical outcome; the source lane's independently
parametrised construction agrees at five seeds).  Controls fire: a random
point violates all 2,951 clean equations, and perturbing a single cell breaks
between 217 and 293 clean equations — except for the nine cells of `A23`,
where it breaks none, the degeneracy predicted by the shape (`Phi` carries
`A23` as a scalar factor) and found independently by both engines.

So the clean stratum is a genuine variety, `Phi` vanishes on it, and the
theorem says the *constant* equation cannot be added.

## 8. Scope

* The theorem is about **W8's immunity template at `m = 24`** — one template.
  It is not a statement about the support level `m = 24`, and not a statement
  about the residual family of spanning-2-connected-`Gamma` templates at
  `m = 24`.  (Later, unaudited work found that family to be large; that makes
  the distinction load-bearing rather than pedantic.)
* Sub-templates of `T24` are different templates and are not covered.
* The certificate is insensitive to admissibility conventions, since it uses
  none.

## 9. Deliberately not promoted here

* **"The clean system forces rank `A45 = A56 = A67 = A07 = A14 = 1`"** and
  **"`P_L`, `P_R` are nowhere zero"**.  These appear in the source lane's
  report as structure derived en route, but the forcing direction is verified
  by no script in either the source or the audit directory (the script the
  report cites for it does not exist), and the audit does not check them.
  What *is* verified is that the constructed non-vacuity points happen to
  have those five blocks of rank one — a property of the construction, not a
  consequence of the clean system.  The kill does not use any of this.
* **Any statement about `m = 25..28`.**  At `m >= 25` the added cross blocks
  give `0^8` a supported completion, so no constant word is effectively clean
  and this mechanism's `k = 0` route is closed; what replaces it is outside
  the audited layer.

## 10. Certificates and checkers

| item | artifact |
|---|---|
| template (verbatim from W8's stored immunity family), fibres, cleanness predicates | `computations/unaudited-residual-w15-2026-08-15/w15_core.py`, `w15_task0_calibrate.py`, `results_task0_calibrate.json` |
| `Phi`-forcing definitions (effectively clean, extras, the `k = 0,1,2` routes) | `computations/unaudited-residual-w15-2026-08-15/w15_forcing.py` |
| normal forms, the seven-word identity chain, W15's multiplier | `computations/unaudited-residual-w15-2026-08-15/w15_task1_m24.py`, `results_task1_m24.json`, `log_task1_m24.txt` |
| W15's Singular membership + its multiplier-relative leave-one-out control | `computations/unaudited-residual-w15-2026-08-15/sing_m24_membership.sing`, `log_sing_m24.txt` |
| independent template/fibre audit; the 2,152 vs 2,952 counts; `0^8` effectively clean | `computations/unaudited-audit-a6-w15w14-2026-08-15/a6_engine.py`, `a6_A1_fibres.py`, `results_A1_fibres.json` |
| **the promoted five-word certificate (B), closed form and expansion over Z** | `computations/unaudited-audit-a6-w15w14-2026-08-15/a6_A3_minimality.py`, `results_A3_minimality.json` |
| Singular membership and saturation for the five-word ideal; multiplier tightness probes | `computations/unaudited-audit-a6-w15w14-2026-08-15/a6_A4_gen_singular.py`, `a6_A4_singular.sing`, `a6_A4b_sat.sing`, `log_A4_singular.txt`, `log_A4b_sat.txt` |
| per-dropped-word exact witnesses | `computations/unaudited-audit-a6-w15w14-2026-08-15/witness_drop_w1.json` … `witness_drop_w6.json` |
| non-vacuity point and controls | `computations/unaudited-audit-a6-w15w14-2026-08-15/a6_A5_nonvacuity.py`, `results_A5_nonvacuity.json`, `a6_nonvacuity_point_seed11.json`; source-lane version `computations/unaudited-residual-w15-2026-08-15/w15_task4_controls.py`, `results_task4_controls.json` |

Four independent confirmations of the membership underlying (B): exact
expansion over `Z`; Singular Groebner reduction over `Q`; Singular saturation
by the named cells (the geometrically correct form, since it shows `H_{0^8}`
vanishes on every component of the clean variety not swallowed by a vanishing
named cell); and 293 random exact rational points of the five-equation system,
all with `G = 0`.

## 11. Audit record

* **Source lane:** `computations/unaudited-residual-w15-2026-08-15/REPORT.md`
  (W15, unaudited; all verdicts exact — `Fraction`, exact sparse polynomials,
  Singular over `Q`; no floats in that directory).
* **Independent audit:** `computations/unaudited-audit-a6-w15w14-2026-08-15/REPORT.md`
  (A6; every engine rebuilt from primary definitions, no probe code imported;
  exact arithmetic, with mod-`p` used only as a rigorous lower bound).
* **Verdict:** PROMOTION-READY, WITH CORRECTIONS THAT STRENGTHEN IT —
  "**Template/fibres/histogram/binomial shape: CONFIRMED (shape holds on all
  2,952 effectively-clean words — more than the 2,152 'syntactic clean' W15
  counted; terminology conflation noted).  0^8 effectively clean: CONFIRMED.
  Ideal membership: CONFIRMED three independent ways.  'Leave-one-out
  minimality 6/6': REFUTED — w4 = 12001200 is REDUNDANT.  A6 supplies the
  stronger SIX-WORD certificate (five mixed + constant) ... with each of the
  five proved load-bearing TWICE.  Non-vacuity: CONFIRMED by A6's own
  from-scratch solution of the clean stratum.  Hypotheses: minimal as
  claimed, plus specifically H_{0^8} != 0.**"
* **Corrections adopted in this draft:** the promoted certificate is A6's
  five-mixed-word one, not the source lane's six-mixed-word one; minimality
  is stated frame-relative in three frames; the effectively-clean count 2,952
  replaces the word-clean count 2,152 as the scope of the shape lemma;
  `H_{0^8} != 0` is named explicitly in the hypotheses; the unverified
  rank-one/`P_L`,`P_R` structure claims are excluded.
* **One bookkeeping correction to the audit's own prose.**  A6's report
  describes the promoted certificate as having "27 monomials".  The
  machine-recorded cofactor sizes are: 1, 36, 6, 36, 6 (total 85 monomials)
  for the five-mixed-word identity (B) promoted here, and 1, 1, 6, 12, 6, 1
  (total 27) for A6's *other*, six-mixed-word identity at multiplier
  `K^2 A14[2][1]`.  In the atom variables of §3 the five-word identity has
  five cofactors of at most four atoms each, which is the sense in which it
  is hand-checkable; the proof in §5 is written in those atoms and expands to
  nine terms, four cancelling pairs and one atom identity.
* **Pre-commit obligations:** the items of §D and §A of
  `draft_promotion_checklist.md`.
