# STATEMENT — the C_8 / empty-clean stratum, exactly

UNAUDITED (W31, design phase). Pinned HEAD `fc988c6a`.

---

## 1. The objects, fixed once

N = 8 sites, alphabet {0,1,2}, one 3×3 block `A_uv` per edge `uv` of K_8
(row = colour at u, column = colour at v). For a word `w ∈ {0,1,2}^8`,

    H_w(A) = Σ_{M a perfect matching of K_8} Π_{uv ∈ M} A_uv[w_u][w_v]

An **exact source** with template T: every cell occupied by T is nonzero,
every other cell is zero, `H_w = 0` on all 6,558 mixed words and `H_w ≠ 0` on
the three constant words. Krenn–Gu at N=8 (the general bicoloured statement,
`eqSystem8_no_solution_d3`) is the claim that no exact source exists.

Template vocabulary (identical to W16/W19/W20/W26/W30):

| symbol | meaning |
| --- | --- |
| `m(T)` | number of occupied blocks — the **support**; the ladder variable |
| `Σ(T)` | number of occupied cells |
| `Γ(T)` | the graph of **full** (nine-cell) blocks |
| `F(Γ)` | perfect matchings of K_8 lying inside Γ; supported at **every** word |
| `Φ_w` | Σ over `F(Γ)` of the matching monomial at `w` |
| `k(w)` | `fibre(T,w) − |F(Γ)|` = number of supported matchings outside Γ |
| effectively clean | `k(w) = 0`, i.e. `H_w ≡ Φ_w` |
| **server** | an occupied block that is not full |

**Family (R)** — the last open template family at N=8: (SC)-admissible, the
three constant fibres nonempty, Γ spanning 2-connected, and every mixed word
has fibre ≥ 3.

**(SC)**, in the form that matters here: at every site `p` and every colour
`c` there must be a block at `p` all of whose occupied cells carry colour `c`
at the far endpoint. A full block forces no far colour, so every such block
is a server; a server serves at most 2 of the 24 demands. Hence
**≥ 12 servers**, so

> **W18-E:** `|Γ| ≤ m − 12`.

Define the **slack**

>     s(T) := m − 12 − |Γ(T)| ≥ 0.

`s = 0` forces exactly 12 servers, each serving both endpoints, i.e. each a
**single cell**, forming a spanning **cubic** graph C, with all other
non-Γ blocks empty. (Verified: `results_d4.json`.)

---

## 2. The stratum

> **Definition (the C_8 / empty-clean stratum).** The set of (R) templates
> with **no effectively-clean mixed word**.

Its Γ-forced part is exactly characterised:

> **Theorem W19-K [proved, survived audit A7].** `F(Γ)` is contained in every
> fibre, so `k(w) = fibre(w) − |F(Γ)|`. (R) forces `fibre(w) ≥ 3` on mixed
> words, so `|F(Γ)| ≤ 2` ⟹ `k(w) ≥ 1` for every mixed word ⟹ the clean layer
> is **empty**, and W16-B, the k=1 route, the k=2 route and W15-A all have
> **empty input**.

Two exact facts recomputed here from scratch (`results_census.json`, controls
C1/C2: 0 mismatches against the stored W19 census on all 794 classes):

- **`|F(Γ)| ≠ 1` for every admissible Γ.** Kotzig: a connected graph with a
  unique perfect matching has a bridge; Γ is spanning 2-connected, so it has
  none. Verified: 0 of 794 classes have `|F| = 1`.
  **So the Γ-forced stratum splits exactly into `|F| = 0` and `|F| = 2`.**
- **The Γ-forced stratum is 75 of the 794 admissible Γ iso-classes**, by
  (|Γ|, |F|):

  | \|Γ\| | 8 | 9 | 10 | 11 | 12 | 13 | total |
  | --- | --- | --- | --- | --- | --- | --- | --- |
  | `|F| = 0` | – | – | 2 | 3 | 1 | – | **6** |
  | `|F| = 2` | 1 | 4 | 18 | 31 | 14 | 1 | **69** |

  `|Γ| = 8` forces Γ = C_8 (W16-C; all 2,520 spanning 2-connected 8-edge
  graphs on 8 vertices are 2-regular), which is the single class the lane is
  named after.

The **census count 214** that appears in the master plan is a different,
weaker quantity: it counts the 794 stored *representatives* (all at m = 28)
that happen to carry zero clean words. 75 of those 214 are Γ-forced; the
other 139 are representative-specific and could acquire a clean layer under a
different cell placement with the same Γ. **Both numbers are correct; they
count different things, and the distinction has not previously been written
down.** For a uniform theorem the Γ-forced 75 is the object; for
"every stored witness" the 214 is.

### The named member

`Γ = C_8`, the Hamilton cycle `0–4–3–6–1–7–2–5–0`, template
`C8_MEMBER` in `w20_core.py:370`. Recomputed audit (control C3, all match
W19's headline): `m = 28`, `Σ = 148`, `|Γ| = 8`, `|F| = 2`, minimum mixed
fibre 6, **minimum k over mixed words = 4**, **0 effectively-clean words**,
(SC) ✓, Γ spanning 2-connected ✓, `in_R` ✓.

Block profile (control D5): 8 full cross blocks (Γ), 8 **fat** cross blocks
of 8 cells each, 12 single cells inside the halves forming K_4 ⊔ K_4.
**Slack = 8.**

---

## 3. Why the stratum escapes the joint residual theorem

The joint residual theorem (W26, as amended by W30/A10) reads:

> the full degree-≤1 residual system is inconsistent-or-forcing at every
> **off-vanishing-stratum clean point with nonzero Γ cells**.

All three named hypotheses, plus the frame they live in, behave as follows.

**(a) The frame itself — the decisive failure.** Every object in the theorem
is defined relative to `geom(m)` (`w30_lib.py:126`, `w26_core.py:15–26`): a
**single template per support**, with L = {0,1,2,3}, R = {4,5,6,7}, a matching
σ, `Γ = K_4(L) ∪ R-graph ∪ σ-edges`, and **the twelve non-σ cross edges each
carrying one cell**. That is precisely `|Γ| = m − 12`, i.e. **slack 0**:
m=25 ⟹ |Γ|=13, m=26 ⟹ 14, m=27 ⟹ 15, m=28 ⟹ 16. The residual system is
linear in exactly those 12 unknowns; `hafL`, `hafR`, the slice matrix
`S(τ)`, the cofactor vector `Q(w)`, the eight vertices L0–L3/R4–R7, the
triggers and the index choices are all functions of that geometry.

The Γ-forced stratum has **slack ≥ 3** at m = 28 (slack = 16 − |Γ| with
|Γ| ≤ 13; the 214 stored no-clean representatives reach down to slack 2 at
|Γ| = 14), and slack 8 at the C_8 member. Its non-Γ servers are fat 8-cell blocks, so the
residual system is **not** linear in 12 unknowns; it has degree up to 4 in 76
cell variables. **No object in the theorem's statement is defined on the
stratum.** This is a stronger failure than a hypothesis being false.

**(b) "Clean point" — vacuous, and therefore useless.** The clean variety is
cut out by `{Φ_w = 0 : w effectively clean}`. With no clean words, the clean
variety is the whole space: every point is trivially clean. But the theorem's
*mechanism* consumes clean words as input — the delivery predicate is
"every firing row lies in span{clean rows}", and `span{} = {0}`. The
hypothesis is satisfied and the machine still has nothing to eat. This is the
same emptiness W19-K identified for W16-B/k=1/k=2/W15-A.

**(c) "Nonzero Γ cells" — satisfiable, not the obstruction.** The C_8
member's 72 Γ cells are all occupied and may all be nonzero.

**(d) "Off the vanishing stratum" — fails identically for the canonical
bipartition, but is not the real obstruction.** `vanishing_stratum`
(`w30_lib.py:330`) tests whether `hafL` and `hafR` — the hafnians of Γ's
cells inside L and inside R — vanish identically. For the C_8 member Γ is a
*cross* Hamilton cycle: **Γ has no edge inside L or inside R**, so
`hafL ≡ hafR ≡ 0` at every point, and `slice_data` returns `None`
everywhere. But this is bipartition-dependent, and the honest computation
(`results_census.json`, key `E_c8_member_frame`) says: **6 of the 35
bipartitions are nondegenerate** for the C_8 member. Across the whole
Γ-forced stratum: the 6 classes with `|F| = 0` have **0** nondegenerate
splits (they cannot: two half-matchings would compose into a perfect matching
of Γ), and each of the 69 classes with `|F| = 2` has **5 or 6**. So the
vanishing-stratum hypothesis is *recoverable* by re-choosing the split; the
frame (a) is not, because a nondegenerate split of a stratum Γ gives
`Γ|_L` two edges, never K_4's six.

**What does survive.** The **cofactor identity** — expanding `Φ` in the
letter at a vertex `v`,

    Φ(w | v = t)  =  Σ_{s ∈ N_Γ(v)}  A_{v,s}[t][w_s] · haf_{Γ − {v,s}}(w)
                  =  ⟨ S(τ)_t , Q(w) ⟩

— is pure hafnian multilinearity and holds for **any** Γ. On the C_8 member
every vertex has `deg_Γ(v) = 2`, so `S` is 3×2, which is exactly the
favourable `|N(v)| = 2` shape that made m=25/R6 unconditional in W30-X. What
is missing is not the identity but its **input**: W30 gets the relations
`S·Q = 0` from *untriggered/clean* words, and the stratum has none. See
ATTACK-PLAN route R3.

---

## 4. New this phase: the slack separation

> **Lemma W31-1 [probe-proved, exact, unaudited].** Let T be an (R) template
> with slack 0 (equivalently `m = |Γ| + 12`; equivalently every non-Γ
> occupied block is a single cell). Then T has **at least 824 effectively
> clean mixed words**. In particular
>
>     slack 0  ⟹  the clean layer is nonempty  ⟹  T is not in the stratum,
>
> at **every** support m.

*Proof (finite, exhaustive, exact).* At slack 0 every supported matching
outside `F(Γ)` uses one of the 12 single cells, so a mixed word activating no
single has fibre exactly `|F(Γ)|` and is effectively clean. The 12 singles
sit on a spanning cubic graph C and their cells are given by a bijection
`σ_u : {edges at u} → {0,1,2}` at every site (6^8 placements per labelled C —
the count W19's census reports independently). `w31_slack.py` enumerates the
labelled cubic graphs on 8 vertices (**19,355**, matching the external ground
truth and equal to Σ 8!/|Aut| over the six iso-classes — control D1), and
computes, by exact branch and bound over all placements with the global S_3
gauge fixed, the maximum number of mixed words the 12 singles can cover:

| cubic class (triangles, 4-cycles, matchings) | max coverage | ⟹ clean words ≥ |
| --- | --- | --- |
| (0, 4, [12,42,44,7]) | 5,734 | **824** |
| (0, 6, [12,42,44,9]) — Q_3 = K_{4,4} − PM | 5,733 | 825 |
| (1, 3, [12,42,43,6]) | 5,726 | 832 |
| (2, 2, [12,42,42,5]) | 5,718 | 840 |
| (4, 2, [12,42,40,5]) | 5,700 | 858 |
| (8, 6, [12,42,36,9]) — K_4 ⊔ K_4 | 5,660 | 898 |

Global maximum 5,734 < 6,558. ∎

**Positive control D4 (decisive).** The template W26/W30 actually work with at
m=28 *is* slack 0, its 12 singles form Q_3, its placement satisfies the (SC)
bijection at every site, and the number of mixed words activating no single
is **2,152 — exactly the stored effectively-clean count**. The engine
reproduces the object it describes.

Consequences:

- **The stratum requires slack ≥ 1**: surplus servers (fat or thin blocks
  beyond the 12 mandatory singles) are not an accident of the C_8 member, they
  are *forced* by having no clean words. The C_8 member spends slack 8 on 8
  fat 8-cell cross blocks, which is exactly what plugs the ≥ 898-word coverage
  gap left by its singles K_4 ⊔ K_4.
- **Route A's frame and the stratum are disjoint by a theorem**, not by
  convention.
- A quantitative handle appears: *coverage budget*. See ATTACK-PLAN R1.

---

## 5. What "closing the stratum" means for Route A's completeness

Route A's ladder is verdict-complete through m = 19; m ≤ 24 is closed;
m = 25, 26, 27, 28 are open and are being attacked **on the slack-0 template
alone** — one template per support.

W16's own headline, never retracted, states the gap:

> "Killing W8's 25..28 does NOT close N=8 — closure must be uniform over (R)."
> (Lemma W16-D, W16 REPORT, PROVED-HERE.)

At m = 28 the arithmetic of that gap is now explicit: slack = 16 − |Γ|, so
**slack 0 ⟺ |Γ| = 16 ⟺ 6 of the 794 admissible Γ classes** (the six cubic
complements, `|F| ∈ {14,16,24}` — reproduced here, and matching W16-D's
"Gamma PM-counts 14/16/24"). The other **788** classes carry slack ≥ 1 and
lie outside the joint theorem's frame. Of the stored representatives, 214
have no clean layer; 75 classes have it forced by Γ.

So the completeness picture at m = 25..28 is three-layered:

1. **slack-0 templates** — Route A's current target. Proved at m=26; m=25/27
   reduced to realisation side conditions; m=28 is one determinantal
   disjunction. Lemma W31-1 guarantees these always have ≥ 824 clean words,
   so the machinery always has input here.
2. **slack ≥ 1 with a nonempty clean layer** — 500-odd classes. The
   mechanisms (W16-B and the k=1/k=2 routes) have input, but their forcing
   hypothesis ("the clean layer forces some site to factor") was **refuted**
   at m=25 (A7) and m=28 (W21); the replacement is W21's residual linear test
   and W26/W30's joint theorem, both of which are formulated on the slack-0
   geometry only. Transporting them is open and unstudied.
3. **the empty-clean stratum** — 75 Γ-forced classes (214 stored reps). Here
   every proved mechanism has **empty input**. This lane's target.

Closing the stratum therefore does **not** by itself close N=8; it removes the
one layer where the campaign's arsenal is not merely unproved but *undefined*,
and it is a precondition for any uniform-over-(R) statement. Conversely, if a
Krenn–Gu counterexample exists at N=8, this stratum is where the campaign has
never had an instrument pointed at it.

**Exact open statement of the residue:**

> **(W31-OPEN)** Let T be an (R) template with `|F(Γ(T))| ≤ 2` (equivalently:
> no effectively-clean mixed word, in the Γ-forced sense). Then the system
> `{H_w = 0 : w mixed}` together with `{H_w ≠ 0 : w constant}` and
> `{cell ≠ 0 : cell occupied by T}` has no solution over C.
>
> Known: nothing. Not proved for a single member, including the C_8 member.
> Best evidence: a float feasibility probe whose signature is
> indistinguishable from two proved-dead calibration templates (W20 — evidence
> only, ledger 18). One claimed proof existed and was **refuted** (W21-M2).
