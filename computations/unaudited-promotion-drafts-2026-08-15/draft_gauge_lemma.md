> **UNAUDITED DRAFT — not spine.**  Drafted 2026-08-15 at pinned repository
> HEAD `e0c4d7c548dd1b252a87b3fc16e76182a3a0bbfb` (recorded in
> `PINNED_HEAD.txt` beside this file).  It becomes spine only when committed
> through the supersession discipline of `certification/SUPERSESSIONS.md`,
> with the pre-commit items of `draft_promotion_checklist.md` discharged.
> All paths are repository-root-relative.

# Mixed-exact sources with three nonzero pure coefficients are exact up to gauge

**Lemma W10-G and Corollary W10-6.  Proposed status on promotion: `[P]` —
proved, with exact checkers and an independent re-audit (A4).**

## 0. Notation

Let `B` be a site set of even cardinality `N`, colours `{0,1,2}`.  An
*aggregate source* `A` assigns to every unordered pair `uv` of sites an
endpoint-ordered matrix `A_uv` in `C^{3x3}` (possibly zero); `A_uv[i][j]` is
the *cell* at colour `i` on the `u`-endpoint and colour `j` on the
`v`-endpoint.  For a *word* `w` in `{0,1,2}^B`,

```text
H_w(A) = sum_{M in PM(B)} prod_{uv in M} A_uv[w_u][w_v],
```

the sum running over the perfect matchings of the complete graph on `B`.  A
word is *constant* (written `c^B`) or *mixed* (non-constant).  Then:

* `A` is **exact** if `H_w(A) = 0` at every mixed word and `H_{c^B}(A) = 1`
  for `c = 0,1,2` — that is, `H(A) = Delta_{N,3}`, the system of
  `proofs/six-site-arbitrary-complex-obstruction.md` §1 at `N` sites;
* `A` is **mixed-exact** if `H_w(A) = 0` at every mixed word, with the three
  *pure coefficients* `H_{c^B}(A)` unconstrained;
* the **template** of `A` is its support pattern
  `T(A)_uv = { (i,j) : A_uv[i][j] != 0 }`, one subset of `{0,1,2}^2` per pair
  (`template_of` in
  `computations/unaudited-mixed-exact-pure-cancellation-w10-2026-08-15/w10_core.py`).

**Gauge.**  A *gauge* is a family `g = (g_u)_{u in B}` with `g_u` in
`(C^*)^3`, acting by

```text
(g . A)_uv[i][j] = g_u[i] * g_v[j] * A_uv[i][j]
```

(`apply_gauge`, same module).  The gauge group is `(C^*)^{3N}`: one nonzero
scalar per (site, colour) slot.  Gauge does not permute cells and does not
move support between pairs.

**Terminology guard** (`notes/2026-08-15-conventions-and-hazards.md`, items
1–2).  This document uses neither sense of "clean"; the mixed-exact sources
constructed by the W10 lane are *not* "witnesses" in either glossary sense
(they are neither active clean caps `(p,q,K)` nor sites with `C_{u,r} = 0`),
and are called *mixed-exact sources* throughout.

## 1. Lemma W10-G

> **Lemma W10-G.**  Let `A` be a mixed-exact aggregate source on an even site
> set `B`, and suppose all three pure coefficients are nonzero:
> `H_{c^B}(A) != 0` for `c = 0,1,2`.  Then `A` is gauge-equivalent to an
> **exact** source with the **same template**.  Explicitly, fix any one site
> `0` in `B` and take
>
> ```text
> g_0[c] = 1 / H_{c^B}(A)   (c = 0,1,2),      g_u = (1,1,1)  for u != 0;
> ```
>
> then `g . A` is exact and `T(g . A) = T(A)`.

### Proof

**(i) Every gauge rescales every word coefficient by one nonzero scalar.**
Fix a gauge `g` and a word `w`.  For a perfect matching `M` of `B`,

```text
prod_{uv in M} g_u[w_u] g_v[w_v] = prod_{u in B} g_u[w_u],
```

because `M` uses each site exactly once; the product is the same for every
`M`.  Hence, factoring it out of the matching sum,

```text
H_w(g . A) = ( prod_{u in B} g_u[w_u] ) * H_w(A).          (1)
```

**(ii) Mixed-exactness and the template are gauge-invariant.**  The scalar in
`(1)` is a product of units, hence nonzero, so `H_w(g . A) = 0` if and only
if `H_w(A) = 0`; applying this at every mixed word, `g . A` is mixed-exact
whenever `A` is.  Likewise each cell is multiplied by the unit
`g_u[i] g_v[j]`, so `T(g . A) = T(A)` — the support pattern is literally
unchanged.  (This is audit A4's simplification: no hypothesis on `A` beyond
mixed-exactness is needed for either statement, and no computation is
involved.)

**(iii) The three constant normalisations decouple.**  Take `g` supported at
the single site `0`, i.e. `g_u = (1,1,1)` for `u != 0`.  At the constant word
`c^B`, `(1)` reads

```text
H_{c^B}(g . A) = g_0[c] * H_{c^B}(A),
```

so the three constant coefficients are rescaled by three *independent* free
scalars `g_0[0], g_0[1], g_0[2]`, and no other coefficient constrains them.
Since each `H_{c^B}(A) != 0`, the choice `g_0[c] = 1 / H_{c^B}(A)` is legal
(a unit) and gives `H_{c^B}(g . A) = 1` for all three colours simultaneously.
By (ii) the mixed coefficients of `g . A` are still zero and the template is
unchanged.  Hence `g . A` is exact with template `T(A)`.  ∎

**Scope.**  The lemma is an identity over any field (over `C` in the use
made of it); it asserts nothing about the existence of a mixed-exact source,
and nothing about sources with a vanishing pure coefficient.  Only the
*existence* of the three inverses is used, so "the pure coefficients are
nonzero" is exactly the hypothesis consumed — not "they are equal", and not
"they equal 1".

## 2. Corollary W10-6

> **Corollary W10-6.**  Every mixed-exact aggregate source on **six** sites
> has a vanishing pure coefficient.

### Proof

Suppose a mixed-exact source `A` on `|B| = 6` had `H_{c^B}(A) != 0` for all
three colours.  By Lemma W10-G there is an exact source `g . A` on six sites,
contradicting Theorem 1.1 of
`proofs/six-site-arbitrary-complex-obstruction.md` (dependency `SP-K6`: no
collection of complex `3x3` matrices on `K_6` has `H_6(A) = Delta_{6,3}`). ∎

Only the *existence* half of Lemma W10-G is consumed here: the contradiction
needs an exact six-site source, not the preservation of the template.  The
template-preservation half is what the residual-family applications use
(§3(a)).

## 3. Consequences, with their exact scope

**(a) The "mixed = 0, pures nonzero" systems carry no slack.**  Let `T` be a
template and consider the value system "`H_w = 0` at every mixed word, and
`H_{0^B}, H_{1^B}, H_{2^B}` all nonzero" on sources with template contained
in `T`.  By Lemma W10-G, a solution of that system *is* an exact source at
the same template after one gauge.  Hence a feasible point of such a system
at any even `N >= 6` is a counterexample to the conjecture at `N`, and
conversely infeasibility of the system is exactly infeasibility of exactness
on that template.  This is the equivalence the residual-family kill documents
(`draft_m20_certificate.md`, `draft_m24_certificate.md`) consume when they
work only with mixed equations and one nonvanishing constant coefficient.

**(b) Mixed-exactness alone does not force (SC); mixed-exactness with three
nonzero pures does.**  Recall (SC), the slice-cover / forced-incident-edge
condition of `notes/slice-cover.md` §2: for every site `p` and every colour
`r` there is a neighbour `j` with `A_pj = a (x) e_r^{(j)}` and `C_pj != 0`;
its template shadow is "all cells of `A_pj` lie in column `r` at `j`".  (SC)
is a template-level, gauge-invariant condition (verified in
`computations/unaudited-mixed-exact-pure-cancellation-w10-2026-08-15/run_j_sc_gauge.py`,
task J1; A4 reconfirmed the gauge-invariance).  Since exact sources satisfy
(SC) by the committed forced-incident-edge theorem, Lemma W10-G plus
gauge-invariance gives: *mixed-exact with all three pures nonzero implies
(SC)*.  The converse implication from mixed-exactness alone is false — the
mixed-exact sources exhibited by the W10 lane fail (SC) at **every**
(site, colour) slot (18/18 at `N = 6`, 24/24 at `N = 8`; same script, task
J2).  Note the reading of the slice-cover derivation this pins down: it
contracts the star expansion into an identity whose left side is
`sum_r lambda(e_r) H_{r^B} e_r^{(x)(B - p)}`, which has rank 3 exactly when
all three pure coefficients are nonzero.

**(c) At six sites the hypothesis of (b) is empty**, by Corollary W10-6: for
mixed-exact six-site sources, (SC) is not available at all, so
"mixed-exact + (SC)" at `N = 6` is a separate object rather than a subclass.

## 4. Certificates and checkers

| item | artifact |
|---|---|
| definitions, `apply_gauge`, `gauge_to_exact`, `template_of` | `computations/unaudited-mixed-exact-pure-cancellation-w10-2026-08-15/w10_core.py` |
| gauge identity `(1)`, 4,145 checks / 0 violations; non-gauge control M1 (436/4,374 violations); zero-gauge control M2 | `computations/unaudited-mixed-exact-pure-cancellation-w10-2026-08-15/run_a_gauge_and_crosscheck.py`, `results_a_gauge_and_crosscheck.json` (keys `A2_gauge_identity`, `A2_control_M1_nongauge`, `A2_control_M2_zero_gauge_changes_template`) |
| Lemma W10-G end-to-end, 20/20 with controls | same JSON, key `A3_lemmaG`; control `A3_control_M3` |
| (SC) gauge-invariance (J1), failure of (SC) for mixed-exact sources (J2), the implication (J3), the `N = 6` vacuity (J4) | `computations/unaudited-mixed-exact-pure-cancellation-w10-2026-08-15/run_j_sc_gauge.py`, `results_j_sc_gauge.json` |
| independent re-derivation over `Q` and `Q(i)`, 45/45 end-to-end round trips at `N = 4`, decoupling of the three normalisations | `computations/unaudited-audit-a4-w12w10-2026-08-15/chk07_w10G_gauge.py`, `results_chk07.json` |
| Corollary W10-6 (existence half only) | `computations/unaudited-audit-a4-w12w10-2026-08-15/chk08_w10_corollaries.py`, `results_chk08.json` |
| consumed committed theorem | `proofs/six-site-arbitrary-complex-obstruction.md` (Theorem 1.1), `notes/slice-cover.md` §2 |

## 5. Audit record

* **Source lane:** `computations/unaudited-mixed-exact-pure-cancellation-w10-2026-08-15/REPORT.md`
  (W10, unaudited; exact arithmetic, Singular over `Q`; floats only in
  labelled searches).
* **Independent audit:** `computations/unaudited-audit-a4-w12w10-2026-08-15/REPORT.md`
  (A4; from-scratch engine, no probe code imported, exact arithmetic
  including `Q(i)`).
* **Verdict:** CONFIRMED, and simplified — "**W10-G: CONFIRMED and easier
  than billed — ANY gauge preserves mixed-exactness (support pattern
  literally unchanged); the three constant normalisations are exactly
  decoupled (three free scalars at one site); verified over Q and Q(i) incl.
  extreme moduli; 45/45 end-to-end round trips at N=4.  W10-6 CONFIRMED
  (needs only the existence half).  (SC) gauge-invariance trivial,
  confirmed.**"  A4 records no mathematical discrepancy against W10-G or
  W10-6; its six discrepancies (D1–D6) are all on the W12 side or are
  tooling notes.
* **Corrections adopted in this draft:** the proof of §1 is A4's (a
  one-line orbit computation, no case analysis); §2 states explicitly that
  only the existence half is consumed; §3(b) records the exact hypothesis
  the slice-cover derivation consumes.
* **Pre-commit obligations:** the items of §J and §A of
  `draft_promotion_checklist.md`.
* **Not claimed here:** that mixed-exact sources with three nonzero pures
  exist at any `N` (at `N = 6` they do not, by §2); any statement about
  sources with a vanishing pure coefficient; any ceiling or counting
  statement (W10's `Sigma_min+` numbers are search bounds and are **not**
  part of this document).
