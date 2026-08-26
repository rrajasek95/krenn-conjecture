# `notes/2026-08-15-conventions-and-hazards.md` — exact insertion

> **STAGED — not applied.** Drafted 2026-08-20 by lane P2-diag at pinned
> repository HEAD `5377acdc43992e8eaaf4f17f4f1068b7242dfe73`, on the
> coordinator's decision to promote the `X_k` / off-count vocabulary. One
> insertion, into §1 *Terminology collisions*. Apply together with the
> `proofs/eight-site-diagonal-obstruction.md` commit, since the terms become
> corpus vocabulary at that moment.

## Where it goes

`notes/2026-08-15-conventions-and-hazards.md` §"Terminology collisions
(qualify in every new note)" currently runs items 1–4 and ends:

### CURRENT TEXT (the tail of §1, unchanged, quoted for placement)

```markdown
3. **Two h conventions differ by one**: the old curvature-line spine
   uses N = 2h; the 2026-08-15 witness campaign uses h = N/2 - 1.
4. **"O1" collision**: `notes/route-registry.md` O1 is a legacy
   route identifier, NOT the odd-holonomy kill mechanism.
```

### NEW TEXT (items 5 and 6 appended to §1, before the "Tooling hazards" heading)

```markdown
5. **"witness" has a FOURTH sense as of the N=8 diagonal theorem.**
   Item 2 lists three; `proofs/eight-site-diagonal-obstruction.md`
   adds a fourth, unrelated one:
   - *B2 witness site* (W29/A9, 2026-08-19/20): one of the three
     sites `y_0, y_1, y_2` produced by Lemma 3.4 (W29-B2) when a
     block-diagonal source is put in the free-set-triple normal form.
     `y_c` is a site of the solved-out star at which BOTH
     `x^c_{y_c} = t^c_{z y_c} != 0` and `h_c(y_c) = haf(t^c|V'-y_c) != 0`;
     the three are forced distinct. Nothing to do with cap witnesses,
     SAT template witnesses, or the legacy `C_{u,r} = 0` sites.
   The proof document writes "B2 witness site" at every occurrence and
   never plain "witness"; new notes should do the same. If a fifth
   sense ever appears, the right move is a rename, not a fifth entry.
6. **"X_k", "off-count", "level", and "diagonal" in the N=8 campaign**
   (W28/W29/A8/A9; promoted with
   `proofs/eight-site-diagonal-obstruction.md`):
   - *off-count* of a word `w` on `N` sites is
     `off(w) = N - max_c |w^{-1}(c)|`, the number of sites outside the
     largest colour class. `off(w) = 0` exactly for constant words.
   - *`X_k`* (the *level-k system*) imposes the three constant-word
     conditions plus vanishing of ONLY those mixed words with
     `off(w) <= k`. So `X_0` is contained in `X_1` is contained in ...,
     and larger `k` is a STRONGER system. `X_k`-feasible means "has a
     solution at level k".
     **NOTATION COLLISION, pre-existing**: `X_k` / `X_4` / `X_i` are
     ALSO used across the committed corpus as ordinary indeterminates
     and series symbols in TeX — e.g. `\frac18X_4` in
     `notes/collision-cofactor-bianchi.md` (21)-(22),
     `\lambda_kX_i+\lambda_iX_k` in
     `notes/invertible-monomial-nine-cap-classification.md` (12),
     `X_k^D` in `notes/full-missing-square-cap-carrier-resonance.md`
     (15), and `X_23`/`X_45` as named quantities in
     `notes/h3-direct-free-feature-selector-index-gate.md`. 33 tracked
     files under `notes/` and `proofs/` match `X_4` or `X_k` at the
     pinned HEAD; the ONLY one using the level sense is
     `notes/2026-08-15-resolution-master-plan.md` (addenda v40 onward).
     Everywhere else the symbol is an indeterminate. So the level
     reading is safe only inside the N=8 support/diagonal campaign;
     anywhere else, write "the level-k system X_k" in full on first
     use, or avoid the symbol.
   - The level at which `X_k` becomes full exactness DEPENDS ON `N`
     and is not `4`: for block-diagonal sources it is `2` at `N = 4`,
     `4` at `N = 6` and `N = 8`, **`6` at `N = 10`**, `8` at `N = 12`.
     Reading `X_4` as "exactness" is correct only at `N <= 8`; this
     exact slip is what produced, and then refuted, the "uniform in
     even N" claim of W29 (master-plan v47, withdrawn in v50).
   - *diagonal* in this campaign means **block-diagonal**:
     `A_uv = diag(t^0_uv, t^1_uv, t^2_uv)`, i.e. three independent
     symmetric edge-weight functions, one per colour. It is STRICTLY
     WEAKER than the general bicoloured model (arbitrary `3 x 3`
     `A_uv`) and STRICTLY STRONGER than the single-cell edge-coloured
     model (at most one colour supported per pair). Do not collide it
     with the *diagonal gauge group* of `draft_gauge_lemma.md` (one
     nonzero scalar per site-colour pair), which is unrelated.
```

## Why each is worth a ledger entry

* **Item 5** is a live collision risk: the corpus already has three senses of
  "witness" (ledger item 2) and the promoted document introduces a fourth. The
  entry exists so a future lane reading "witness site" in the diagonal proof
  does not match it against the cap-witness theory.
* **Item 6's third bullet is the load-bearing one.** The `X_4 = EXACT`
  identity is a fact about `N <= 8`, not a definition, and treating it as
  uniform is precisely the error that audit A9 caught: the W29 lane reported
  "**Uniform in even N**; N=10 k=4 in flight ..., N=12 queued", which was
  refuted because at `N = 10` the exact level is `X_6` and a `k = 4` run there
  decides a strict relaxation. Recording the per-`N` table in the hazards
  ledger is cheaper than re-deriving the refutation.
* **Item 6's fourth bullet** prevents a second collision the checklist walk
  turned up: `draft_gauge_lemma.md` item J4 uses "diagonal" for a *gauge
  transformation*, not for the shape of `A_uv`.

## Cross-references, and one correction to this lane's own first draft

* **"off-count": clean.** No tracked file under `notes/`, `proofs/`,
  `README.md` or `PROOF-SKETCH.md` uses the term at the pinned HEAD
  (`git grep -l -i "off-count\|offcount"` returns nothing). It enters the
  corpus with this promotion.
* **"`X_k`": NOT clean — this lane's first draft of this patch asserted it was,
  and that was wrong.** `git grep -l "X_4\|X_k" -- notes/ proofs/` matches
  **33 tracked files** at the pinned HEAD. Inspection shows that exactly one —
  `notes/2026-08-15-resolution-master-plan.md`, the campaign record itself —
  means the level system; the other 32 use the symbol as an indeterminate or a
  series coefficient in TeX (see the collision note in item 6). So the
  promotion is introducing a
  *notation* collision, not a terminology one, and the ledger entry above is
  the mitigation. No committed file needs editing — the two readings never
  occur in the same document — but the entry must ship, or a future lane will
  read `X_4` in a Bianchi expansion as a level system.
* **No rename is proposed.** `X_k` is the vocabulary of four lanes
  (W28, W29, A8, A9) and the master-plan addenda v40–v50; renaming now would
  orphan that record. Qualifying on first use is the cheaper discipline.
