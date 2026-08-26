# PRIOR ART — everything already tried on the C_8 / empty-clean stratum

UNAUDITED (W31, design phase). Pinned HEAD `fc988c6a`. Purpose: so the attack
plan repeats nothing, and so no retracted claim is reused as an input.

---

## 0. Status ledger, one line each

| lane | what it did to this stratum | verdict now |
| --- | --- | --- |
| W16 (2026-08-15) | found the stratum's boundary condition (budget lemma W16-C: `|Γ| = 8 ⟹ C_8`); proved (R) is a large family | **stands** |
| W19 | **named** the stratum (Theorem W19-K), built the explicit C_8 member, produced the 794-class census | **stands** (audit A7 explicitly re-certified these) |
| W20 | built the stratum's only structural machinery: the L-free/R-free permanent reduction + Lemma W20-P | **stands**; a *mechanism*, not a kill |
| W21 Move 2 | attempted the kill; **produced a false kill**, caught by cross-lane contradiction | **refuted** (W21-M2 is FALSE) |
| A7 | audited W20-P: statement true, written proof step (B) replaced | **stands, strengthened** |
| W26 / W30 / A10 | Route A's joint residual theorem, m=25..28 | **does not touch the stratum** — defined only on the slack-0 geometry |
| anyone | a dedicated adversarial builder for a *stratum point* (an exact source on a stratum template) | **never run** |

---

## 1. What the retraction actually retracted (important)

The brief for this lane says W19's kill was retracted and its claims should be
treated as void. That is right for **one** result and wrong for the rest, and
the difference matters because the stratum's *definition* lives in W19.

**Retracted (master-plan v34, audit A7):** W19's m=25 Branch-B kill. Cause:
sign-flipped generators. The bug is at
`computations/unaudited-forcing-w19-2026-08-15/w19_branchB.py:243–244`,
which emits `"%s*%s+%s*%s"` — a `+` where the relation has `−`, i.e.
`μ·k_x + A03·g` instead of `μ·k_x − A03·g`. The flipped form forces `g = 0`
spuriously. A7 then built a 12-member family of exact witnesses (all cells
nonzero, every effectively-clean equation satisfied, Branch B, rank M6 = 2,
no site factoring), so **"the clean layer forces some site to factor" is
FALSE at m=25** — refuted, not merely unproved. "N=8 closed through 25"
reverted to "closed through 24". Ledger item **18** was born here: forcing
verdicts need explicit-point controls constructed **outside** the asserted
locus (W19's C5 point had all eight sites factoring — vacuous as a control),
and search minima carry no evidential weight.

**Explicitly re-certified by the same audit (v34 item 3), and therefore
usable:**
- **Theorem W19-K** and the explicit C_8 member — the stratum's definition and
  its only named inhabitant.
- **The census** — "all 794 classes now certified by explicit witnesses".
- The symmetry correction: the (R)-preserving group is `S_8 × S_3(global)`,
  order 241,920; `S_3^8` does **not** preserve (R) (per-site colour
  permutations break (SC)). The prose "576 per-site survivors, not a
  subgroup" was corrected; the operational conclusion is intact.

This lane re-derived W19-K's census consequences from scratch on an
independently typed model: `results_census.json` controls C1/C2 report
**0 mismatches** in `|F(Γ)|` and in clean-layer emptiness across all 794
stored classes, and the C_8 member reproduces W19's headline audit exactly
(control C3). Nothing in the stratum's definition depends on the retracted
computation.

---

## 2. W20 — the machinery that exists (`unaudited-lasttwo-w20-2026-08-15/`)

This is the only real handle anyone has built on the stratum.

**The L-free / R-free reduction [proved; 0 of 4,860 mismatches; re-verified
0/14,580 by W21].** On the C_8 member the 12 single cells sit inside the two
halves L = {0,1,2,3}, R = {4,5,6,7}, one diagonal cell per edge of a proper
3-edge-colouring of each K_4. Call an L-word `x` **L-free** when no L-single
is active (no `k < l` in L with `x_k = x_l = ` colour class of `kl`). A
perfect matching of K_8 uses 4, 2 or 0 cross edges, and the 2-cross and
0-cross ones consume at least one L-single and one R-single. Hence for every
`y`,

    H_(x,y) = per B(x,y),      B(x,y)[i][j] = A_{i,j}[x_i][y_j]

the 4×4 cross matrix with dead cells zeroed — only the 24 four-cross
matchings survive, and they are exactly the 24 bijections L → R. There are
**30 L-free words** (recomputed here, control F: 30 ✓) and 30 R-free ones, so
**3,960 of the 6,558 mixed equations are pure 4×4 permanent conditions on the
16 cross blocks, with the 12 single cells dropping out entirely.**

Because `per` is multilinear in the columns of B and column `j` depends only
on `y_j`, a fixed L-free `x` says exactly: **`per` vanishes identically on
`V_4^x × V_5^x × V_6^x × V_7^x`**, where `V_j^x = span{c_j^x(0), c_j^x(1),
c_j^x(2)} ≤ C^4` and `c_j^x(d)[i] = A_{i,j}[x_i][d]`.

**Lemma W20-P [proved; A7 replaced written step (B) with an induction; char ≠ 2
and through-the-origin added; exhaustive 640,000-configuration control at
n = 4 and a new fully exhaustive n = 5 verification over 2.3e8 multisets].**
For hyperplanes `V_1..V_n`, `n ≥ 3`: `per` vanishes on `V_1 × ... × V_n` iff
all of them are the **same coordinate hyperplane**. False at n = 2 and false
without the hyperplane hypothesis (explicit witnesses stored). **P4c:** three
hyperplanes plus one all-nonzero vector force `per ≠ 0`.

**What W20 derived from it, and what it did not.** Derived: every L-free word
forces some 4×3 cross matrix to have rank ≤ 2 (two dead-cell-free words force
two); the minimum box cover of the 30 L-free words is exactly 9 (+9 mirror),
each box a codimension-≥2 coincidence in a 12-line arrangement. Not derived:
a kill. **A single L-free word is provably insufficient** — the explicit
all-nonzero solution at `x = (1,1,2,2)` is stored. W20's own conclusion:
*the kill must use the full permanent conditions of at least two L-free words
simultaneously.* Verdict recorded as "NOT yet killed; conjectured dead with an
explicit obstruction ladder."

**Soft spots W20 recorded and nobody has cleared:** the rank conditions are
necessary-only; the feasibility probe is float (evidence only, ledger 18); the
Pfaffian frame (Γ is Pfaffian at 25..28 *and* at C_8, Φ = ±Pf) is noted and
**unexploited**; and *"C_8 is one of 214 stratum classes (the reduction should
generalise — unchecked over the census)"*. That last item is still unchecked.

---

## 3. W21 Move 2 — the false kill, in detail
(`unaudited-finishing-w21-2026-08-15/move2geo`, `move2sing`)

This is the single most important precedent, because it is the campaign's
canonical example of this stratum manufacturing a wrong answer.

- Sub-probe **SING** claimed a kill via "Theorem W21-M2": *`per` cannot vanish
  on products of 2-dimensional non-coordinate subspaces.* It had passed
  mutation controls and positive controls, in two independent pipelines, and
  rested on a **complete exhaustive classification over F_5**.
- Sub-probe **GEO** was tasked with building the forbidden object and
  **built it**: a Q(ω) family, ω a primitive cube root of unity.
- W21 adjudicated in exact `Q[ω]/(ω²+ω+1)`: **all 16 basis permanents vanish,
  the subspaces are non-coordinate**, and the mutation control (ω → 1) fires.
  **W21-M2 is FALSE; the kill is invalid.**
- Root cause: **F_5 has no primitive cube root of unity**, so the complete F_5
  classification was blind to the entire counterexample family. Ledger item
  **19** was born here (single-small-field exhaustive sweeps are insufficient
  for NEVER claims over Q; use at least two primes with the right residues,
  p ≡ 1 mod 3 for cube roots; **characteristic 3 is degenerate for 4×4
  permanents because 4! = 0 there**). Ledger item **20** was born here too:
  the control that worked was **cross-lane contradiction** — an independent
  lane whose only job is to BUILD the forbidden object.
- The L-free reduction itself was re-verified during the adjudication
  (0/14,580) and is untouched by the refutation.
- **Salvage, still open:** the **double-dead-column obstruction**. `x =
  (1,0,0,2)` is the unique 4-dirty L-free word with a double dead-cell column
  (at site 6); `y = (0,2,0,1)` is its mirror. The ω-family fails exactly that
  constraint. A corrected lemma using the double column may recover the kill.
  Stored: `move2sing/results_4dirty.json` (L-4-dirty words `(1,0,0,2)`,
  `(1,0,2,2)`, `(1,1,2,2)`; R-4-dirty `(0,2,0,1)`, `(0,2,0,2)`),
  `results_deadcol.json`, `results_tight.json`.
- GEO additionally **corrected W20's box-cover convention** and **proved that
  the codimension-budget and collinearity-only routes cannot close C_8**. Two
  routes are therefore already dead by proof, not by failed search.

**A stored-artifact anomaly found while reading, flagged for the compute
phase.** `move2sing/LEDGER.json` records the finite-field sweeps as
`ff5: {nsubs 840, pairs 353220, filtered 0, full_checks 0, counterexamples 0}`
and `ff7: {nsubs 3024, pairs 4573800, filtered 0, full_checks 0,
counterexamples 0}`. **Both sweeps performed zero full checks.** Either the
pre-filter is sound (and the runs are proofs) or the runs are vacuous. As
stored they establish nothing (ledger 18/21), and the F_5 "complete
classification" referenced in the master plan must therefore be traced to
`m2ff5.py`'s actual code path before any future argument leans on it.

**The Singular blocker, documented and unresolved**
(`move2sing/results_blocker.json`). Root cause, verbatim: *"the gauge-fixed
CELL systems are massively positive-dimensional before saturation (every
partial all-zero degeneration is a component), so std must build the whole
Groebner basis of a big positive-dimensional ideal."* Measured: the fixed-y
slice `y = 0101` (30 quartic permanents, 43 cells, 15-edge gauge tree, 28 free
vars) **TIMES OUT at 300 s** in char 32003; the `(2,2,2,2)` all-sites-rank-2
branch **times out at 240 s**; every chart orbit with at least one dim-3 site
is **UNIT in 0.05–0.11 s**. So the hard case is exactly the all-four-sites-
2-dimensional configuration — which is exactly where the ω counterexample
lives. Any elimination route must dispose of the degeneration components
before it starts, or it will time out for the same reason.

---

## 4. Everything else that has touched the stratum

- **W16-C (budget lemma)** — `2β + h ≥ 24`, `8 ≤ |Γ| ≤ 16`, and `|Γ| = 8`
  forces C_8 because all 2,520 spanning 2-connected 8-edge graphs on 8
  vertices are 2-regular. This is where "C_8" as a name comes from, and it is
  where the thickness shortcut is recorded as failing.
- **W16-D** — the construction that made (R) large: 12 single cells on any
  properly 3-edge-coloured cubic graph C plus full blocks on `Γ = K_8 \ C`.
  This is exactly the slack-0 family (see STATEMENT §4), with Γ PM-counts
  14/16/24 over the six cubic classes — reproduced here.
- **W19 census sub-probe** — 794 admissible Γ classes, all inhabited; `|Γ|=8`
  forced to C_8 exhaustively; `|Γ|=16` completely classified; external ground
  truths A008406, 19,355 and 2,520 all reproduced (this lane independently
  reproduced 19,355 as control D1).
- **W20's feasibility probe** — floats, evidence only: the C_8 member's
  signature (0.248 residual, no convergence, cells collapse) is
  indistinguishable from two proved-dead calibration templates and clearly
  unlike the feasible control (8e-30). This is the *only* evidence that the
  stratum is dead, and under ledger 18 it is not evidence of impossibility at
  all — only of a failed search.
- **W26 / W30 / A10** — no contact with the stratum. Their `geom(m)` is one
  slack-0 template per support; `hafL`/`hafR` for the canonical bipartition of
  the C_8 member are identically zero, and `slice_data` returns `None` there.
  W30's Q-span law, W30-Z, the escape objects and the m=28 refutation points
  are all off-stratum objects. They are still useful to this lane — as
  **calibration negatives**, not as inputs.
- **The adversarial builder question (ledger 20).** W21's GEO lane was an
  adversarial builder for the **lemma** (it built permanent-null subspace
  configurations) and it worked. **No lane has ever run an adversarial builder
  for a stratum *point*** — i.e. an attempt to construct an exact source on a
  stratum template, over Q, over Q(ω), or over an extension. W20's attempt was
  float-only and did not converge; W30's `adv`/`adv2` builders target survivor
  stars on the slack-0 geometry, a different object. This is a gap in the
  control structure, not just an unexplored route.

---

## 5. Objects this lane must test any new target against
(the standing pre-launch rule; all exist on disk at the pinned HEAD)

| object | where | what it kills if ignored |
| --- | --- | --- |
| the Q(ω) permanent-null family | `move2geo/results_final.json:char0_pernull_example`; adjudicated in `move2sing` | any revival of W21-M2 or of "per cannot vanish on 2-dim non-coordinate subspaces" |
| the p=3 permanent-null examples (268) | `move2sing/results_ff3.json` | any characteristic-free permanent-vanishing claim (4! = 0 in char 3) |
| the all-nonzero single-L-free-word solution `x = (1,1,2,2)` | W20 §residual 2 | any claim that one L-free word suffices |
| GEO's four degeneracy witnesses (all-8, R456/L012, R45/L01, generic control) with collinearity levels 4/3/2/0 | `move2geo/results_witness.json` | any claim about how many sites can be simultaneously degenerate |
| the box-cover / codimension-budget no-go and the collinearity-only no-go | `move2geo` (proved) | re-running two already-dead routes |
| A7's m=25 refutation family; W21's m=28 zero-factoring clean points | A7 / W21 lanes | any resurrected "clean layer forces a site to factor" |
| W30/A10's escape objects and the F_31/F_13 m=28 co-failure points | `unaudited-exclusion-w30-2026-08-19/points_*.json` | off-stratum, but the campaign's standing calibration negatives |
