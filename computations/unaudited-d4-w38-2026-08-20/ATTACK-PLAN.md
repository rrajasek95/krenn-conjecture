# W38 — ATTACK PLAN for n = 8, d = 4 — UNAUDITED

**UNAUDITED. Design phase only; no compute lane was launched.** Pinned HEAD
`4ee924e7aab113d121fac52b7987eb80185922b5`.

Read STATEMENT.md §0 first: the campaign's "(8,4)" record from W27 is
`(N = 8, level k = 4)` at `d = 3` colours and has **nothing to do with this
target**.

---

## 0. The finding that reorders every route

`n = 8, d = 4` is **not an independent open problem**. Colour projection
(Lemma P — the campaign's own Proposition 1.1 [P], Lean-formalized at
`formal/MonochromaticQuantumGraphKeyLemmas.lean:200-235`, ledger A7, status
**F**) gives, at fixed `n`, over any semiring:

```
        no (8,3) source   ⟹   no (8,4) source   ⟹   no (8,5) source   ⟹  …
```

Consequences that govern the ranking below:

* **R0.** `(8,4)` is *strictly weaker* than the campaign's main target
  `(8,3)`. Every hour spent on `(8,4)` that also proves `(8,3)` was spent on
  `(8,3)`.
* **R1.** The campaign's stated lever for `(8,3)-C` — `X_4 = ∅ at N=8`
  (conjectured, master-plan v43) — **implies `(8,4)` as a corollary**
  (TRANSFER-AUDIT §2.3). `(8,4)` is downstream of the main lever.
* **R2.** `(8,4)-diag` and `(8,4)-ec` are **already theorems today**, free
  from committed results (STATEMENT §4). There is no first theorem to win
  there; there is a *claim* to write down.
* **R3.** The only mathematics at `d=4` that does not factor through
  `(8,3)` is the **six-pair-restriction layer** — six exact `d=2` sources on
  `K_8` sharing four pure matrices, each shared three ways.
* **R4.** If the goal is a cheap *new registry scalp* at `n = 8`, `d = 4` is
  the wrong `d`. The chain runs `(8,3) ⟹ (8,4) ⟹ (8,5)`, and with the
  external bounds (STATEMENT §3.2) the open ℂ-surface is `d ∈ {3,4,5}`.
  **`(8,5)` is the weakest open statement at `n = 8`** and is implied by
  everything `(8,4)` would prove.

---

## 1. RANKED ROUTES

### Route 1 — HARVEST (cost: one session, zero compute) — **DO THIS**

Write down, with proofs, the three corollaries that already exist:

| claim | from | compute |
|---|---|---|
| **W38-1** no block-diagonal `(8,d)` source, any `d ≥ 3`, any integral domain | Theorem 1.2 of `proofs/eight-site-diagonal-obstruction.md` + Lemma P | none |
| **W38-2** no weighted edge-coloured `(8,d)` source, any `d ≥ 3` | Corollary 1.3 + Lemma P | none |
| **W38-3** block-diagonal `(N,d)` source ⟹ `d ≤ N-1`; hence `(4,4)-diag` closes with zero cases | W29-B2 pigeonhole (TRANSFER-AUDIT §3.1) | none |

Each is one paragraph. **W38-2 is a strengthening of published work**: the
only external `n=8, d=4` result is Cervera-Lierta–Krenn–Aspuru-Guzik
(*Quantum* **6**, 836; arXiv:2109.13273), whose SAT variables are Boolean
edge literals — "it is not a weighted no-go"
(`references/REFERENCES.md:212-226`). W38-2 allows arbitrary weights and full
cancellation.

**Pre-launch controls (ledger 27 — test the target verbatim, not a
relaxation):** the target is *"`EqSystemN 8 4 W` for block-diagonal `W` is
unsatisfiable"*, so the control must be a `d=4` object. Two, both cheap:
(i) push the `(4,3)` exceptional source through the `d=4` reader as a padded
weighting and confirm it is **not** read as a `(4,4)` source (done: C3);
(ii) confirm the `d=4 → d=3` restriction map lands block-diagonal weightings
in block-diagonal weightings and preserves every amplitude (done: C1, 21 672
checks, 0 violations, at random weights per ledger 17).

**Calibration (ledger 29 — a calibratable positive is required):** the
campaign has genuine positives here, unlike the search-builder situation of
ledger 29. Any `(8,4)` machine must return
**SAT/nonempty at `(4,2)`, `(4,3)`, `(6,2)`** and **UNSAT at `(4,4)`**. The
`(4,4)` verdict is not a guess — `eqSystem4_no_solution_d4` is
`answer(True)`, `research solved`, with a DeepMind prover proof link. So:

> **The exceptional-structure landscape at `d = 4` is EMPTY. There is no
> known `(N, 4)` source for any `N`, and `(4,4)` is proved impossible.** The
> three known sources in existence are `(4,2)`, `(4,3)`, `(6,2)` — all
> `d ≤ 3`. A `d=4` machine therefore has **no positive to calibrate against
> at `d = 4`**; it must be calibrated at `d ≤ 3` and the transfer argued.
> This is a real instance of ledger 29 and it must be stated in any `d=4`
> lane's report.

**Risk.** W38-1/W38-2 are only as strong as Theorem 1.2 (A9-confirmed at the
promotion gate, master-plan v50, committed as spine) and Lemma P (status
**F**). Both are the campaign's best-supported objects. Low.

---

### Route 2 — RECONCILE THE `n = 6` LEDGER (cost: one session) — **DO THIS SECOND**

Lemma P + the committed six-site theorem gives **no `(6,d)` source over ℂ
for every `d ≥ 3`**, closing three registry entries currently marked
`research open` (`eqSystem6_no_solution_d4`, `_d5`, `_ge3`) and subsuming the
externally claimed PR #4664 `(6,4)` resolution. The repo *already knows this*
in one checker docstring
(`computations/verify_colour_projection_monotonicity.py:27-34`, git
`c561d0b`) but has never propagated it: `references/REFERENCES.md:318-326`
still says OPEN, `README.md` claims `d = 3` only, and no file connects it to
#4664.

**Deliverable:** one reconciliation pass over the open/closed ledger, plus a
decision on whether to claim `(6,4)`/`(6,5)` externally.
**Pre-launch control:** per ledger 27, gate on `(6,4)` itself — not on
`(6,3)` plus an argument. **Risk:** this lane did not audit the six-site
theorem; the claim inherits its status entirely. Send it through the
promotion gate before any external claim.

---

### Route 3 — THE SIX-PAIR-RESTRICTION SQUEEZE (cost: 1 lane-week + W33 input) — the only new mathematics

**The statement to attack, verbatim:**

> There is no assignment of four symmetric "pure" weightings `P^0,…,P^3` and
> twelve "cross" weightings `M^{cd}` (`c ≠ d`) to the 28 pairs of `K_8` such
> that, for each of the six colour pairs `{c,d}`, the `2×2`-block weighting
> built from `(P^c, P^d, M^{cd}, M^{dc})` is an **exact `d = 2` source on
> `K_8`**.

This is a necessary condition for an `(8,4)` source (TRANSFER-AUDIT §4:
every word on ≤ 2 colours has `off ≤ 4`, so `X_4` already forces it), and it
**mentions no 3-colour subsystem** — so it is the one route whose success
would not have proved `(8,3)`.

Why it might bind at `d=4` when it does not at `d=3`: each pure `P^c` is
shared by **3** of the 6 systems, against **2** of 3 at `d=3`. The coupling
graph is `K_4` (pures at vertices, systems at edges) rather than `K_3`.

**Required input:** the classification of the exact `d = 2` variety at
`n = 8` — which lane **W33** is already computing (launched v68, "the `d=2`
solution variety at `n=8` is now a REQUIRED input"). W32 found
`21 760` exact `d=2` sources with `2 208` genuinely non-diagonal, and
recorded that **2COL cannot kill alone** at `d=3`. Expect the same at `d=4`
*unless* the sharing structure bites. **Do not launch before W33 reports.**

**Compute estimate.** If W33 delivers a finite classification into `k`
families, the squeeze is a compatibility search over
`k` choices per pair with shared pures: a constraint problem of size
`≈ k^6` with 4 shared unknowns — feasible symbolically if `k` is small
(tens), infeasible if the variety has positive-dimensional components with
free pures. **The honest estimate is: unknown until W33 reports, and the
prior from the `d=3` analogue is negative.**

**Pre-launch controls (ledger 27/28/29).**
1. *Target verbatim*: the boxed statement, not "the pair restrictions are
   nonempty" (a relaxation W32 already knows is satisfied).
2. *Ledger 28 — every pre-filter ships with a witness that passes it*: any
   filter on `d=2` families must be exhibited passing on a stored genuinely
   non-diagonal `d=2` source from W32's 2 208.
3. *Ledger 29 — calibratable positive*: **there is none at `d=4`**. The
   available calibration is `d=3`: run the identical squeeze machinery on
   the three-pair `d=3` version and confirm it does **not** kill (W32 proved
   2COL cannot kill alone). A `d=4` squeeze that reports a kill while the
   `d=3` control also reports a kill is refuted by W32 and must be discarded.
4. *Ledger 20 (adversarial builder)*: spawn a lane whose sole job is to build
   six mutually compatible `d=2` sources with shared pures over an extension
   of ℚ.
5. *Ledger 19/24*: over ℚ/ℂ, use ≥ 2 primes with `p ≡ 1 mod 3` and
   `p ≡ 1 mod 4`; an `F_p` escape refutes an ideal-theoretic route, not the
   ℂ statement.

**Risk: HIGH.** W32's own verdict is that the pair layer cannot kill alone.
The `d=4` version is tighter but not obviously tight enough, and success
still yields only a statement implied by `(8,3)`.

---

### Route 4 — DIRECT `d = 4` RERUN OF THE W29 PIPELINE — **DO NOT FUND**

Costed for completeness, because the brief asked for the ledger size.

* Case ledger: `|Q| = n-1-d = 3`, **4 096 cases in 87 orbits** — identical to
  the committed `d=3` numbers, and identical *as a set*, being the transposed
  `0/1` matrices (TRANSFER-AUDIT §3.2).
* Instance sizes (control C7): `512` Booleans, `6 944` aux, `8 316` `A2`
  rows, `15 712` `A3` clauses, `≤ 5 124` `FR` rows — **≈ 5× the `d=3`
  instance**. The committed `d=3` run was 2.8 s over 87 orbits (311.7 s over
  all 4 096), so a `d=4` rerun with five solvers and drat-trim is a
  **minutes-scale** job.
* Level: the pipeline must run at `X_6`, not `X_4` — `EXACT = X_6` at
  `n=8, d=4` because of the new `(2,2,2,2)` stratum (2 520 words).

**Why not to fund it:** its conclusion is Corollary W38-1, which Route 1
already has for free. It would be corroboration only. And the natural
independent corroboration — Gröbner — is known infeasible at `N = 8`: the
single `N=8, d=3` case ideal attempted (81 variables, 1 932 generators)
**timed out at 3 000 s with no verdict**; per ledger practice a stopped run
carries no information, and `d=4` is strictly larger.

---

### Route 5 — GENERAL BLOCKS VIA THE BOOLEAN ABSTRACTION — **FORBIDDEN**

**W32-ABS [proved]**: on full support the `K_8` hafnian is irreducible, so
the vanishing-pattern route is permanently closed for general blocks —
"the obstruction is irreducibility, not ingenuity — do not fund another
abstraction attempt" (master-plan v68). Irreducibility does not improve at
`d = 4`. **Closed by theorem at every `d`.**

---

### Route 6 — REAIM AT `(8,5)` INSTEAD OF `(8,4)`

If the ancillary-target programme's purpose is *the cheapest new closed
registry cell at `n = 8`*, then by R4 the correct target is the **largest**
open `d`, not `d = 4`. Under PR #4661 (`D ≤ N-2`) and arXiv:2304.06407
(`d < n/√2`, simple graphs) the surface is `d ∈ {3,4,5}` and `(8,5)` is the
weakest. Its free-set ledger is **smaller** than `d=4`'s: `|Q| = 2`,
**1 024 cases in 34 orbits** (control C5). The same objection applies —
`(8,5)-diag` is also free from Lemma P — but a lane aimed at `d=5` general
blocks buys the same registry cells as `d=4` for strictly less work.

**Recommendation: retarget the ancillary programme from `(8,4)` to "the
`d ≥ 4` column at `n = 8`", which Lemma P collapses to a single statement.**

---

## 2. THE CHEAPEST FIRST THEOREM

> **Corollary W38-1: there is no block-diagonal `(8,d)` source over any
> integral domain, for any `d ≥ 3`** — one paragraph, zero compute, from
> committed Theorem 1.2 plus a Lean-formalized lemma. With W38-2 (the
> weighted edge-coloured case, which strengthens the published 2021/2022 SAT
> result at `n=8, d=4`) and W38-3 (`d ≤ N-1` for block-diagonal sources)
> alongside it.

Everything harder than that at `d = 4` is either implied by `(8,3)` or is
Route 3, whose prior is negative and whose input has not arrived.

---

## 3. PRE-LAUNCH CONTROL SUMMARY (ledger 27), per route

| route | target stated verbatim | control that tests *that* target | calibratable positive? |
|---|---|---|---|
| 1 Harvest | "no block-diagonal / edge-coloured `(8,d)` source, `d ≥ 3`" | C1 (restriction identity at random weights, 0/21 672 violations) + C3 (padded source is not a higher-`d` source) | yes at `d ≤ 3` — `(4,2)`, `(4,3)`, `(6,2)`; **none at `d = 4`** |
| 2 `n=6` reconcile | "no `(6,4)` source over ℂ" | must gate on `(6,4)`, not on `(6,3)` + argument | same |
| 3 Squeeze | the boxed six-system statement of §Route 3 | run the identical machinery on the `d=3` three-system version; it must **not** kill (W32) | **no** — ledger 29 applies in full |
| 4 Pipeline rerun | "the 87 `d=4` orbit cases are UNSAT at `X_6`" | the `N=4` positive control must remain SAT under the `d=4` encoder | `(4,3)` only |
| 5 Abstraction | — | — | forbidden by W32-ABS |

## 4. Ledger items this lane proposes

* **Ledger 30 (new).** The ordered pair `(8,4)` collides between *(sites,
  level)* and *(vertices, colours)*. Ban the bare pair; write `N = 8, level
  k = 4` or `n = 8, d = 4 colours`. See STATEMENT §0. Also collides at
  `(8,3)` and `(6,4)`.
* **Ledger 29, addendum.** The `d ≥ 4` regime has **no known source at any
  `N`** — `(4,4)` is proved impossible and no `(N,4)` source exists. Any
  `d ≥ 4` machine is uncalibratable at its own palette size by construction,
  not by accident. State this in every `d ≥ 4` lane report.
* **Bookkeeping defect (not a hazard).** The repo's open/closed ledger
  contradicts its own monotonicity checker at `(6,4)`/`(6,5)`. See
  STATEMENT §6.
