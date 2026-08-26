# The cofactor identity and the Q-span rank bound

> **UNAUDITED STAGING — not spine, not committed.** Drafted 2026-08-20 by lane
> **P3** at pinned repository HEAD
> `e2123f2c006944972cefcdce1b8a3c021f9c2a18`. Staged on the verdict of audit
> **A10** (`computations/unaudited-audit-a10-2026-08-20/REPORT.md`), whose
> "Promotion-ready" list names "the cofactor identity Phi(w|v=t) =
> <S'(tau)_t, Q(w)>" and "the Q-span bound".
>
> Origin: **W30** (`computations/unaudited-exclusion-w30-2026-08-19/`, pinned
> `021b1a30...`) as step (3) of Theorem W30-X and as the Q-span law of Theorem
> W30-Y. **A10** (pinned `f9a3bd6b...`) re-derived both on the **augmented**
> slice matrix `S'` and re-verified them.
>
> **Two corrections from A10 are built into this document and are not
> optional.**
> 1. The object is `S'`, the **augmented** slice matrix over *all* Gamma
>    neighbours of `v` (the sigma-partner column carrying `d`), never W30's
>    `S`. W30's prose said `S`; **W30's code already used `S'`**
>    (A10 verdict T2).
> 2. A10 **D8**: "step (3) reproves `det M = 0`" is trivial-or-empty and is
>    dropped. See §5.

Notation is that of `draft_master_relations.md` §1, which this document
assumes.

## 1. The augmented slice matrix `S'`

**Definition 1.1.** Let `v` be a site and let

```
    N(v)  =  { s :  vs is a Gamma edge }
```

be its Gamma-neighbourhood, listed in a fixed order `s_1 < ... < s_n`,
`n = |N(v)|`. Let `tau = (tau_1, ..., tau_n)` be a **slice tuple**: an
assignment of a letter to each neighbour. The **augmented slice matrix** is the
`3 x n` matrix

```
    S'(tau)[t][j]  =  A_{v, s_j} [t] [tau_j] ,      t in {0,1,2}.
```

*Source:* `computations/unaudited-audit-a10-2026-08-20/a10_t2.py`,
`Sprime()` (lines 76–81): `"""S'(tau)[t][col] = A_{v,s}[t][tau_col] over ALL
Gamma-neighbours."""`, and the module docstring, line 8: "the AUGMENTED slice
matrix S'(tau) whose columns are indexed by ALL Gamma-neighbours of v (**the
sigma-partner column being d**)".

**Remark 1.2 (why augmented, and why this is a correction).** W30's `S` was the
`3 x 3` matrix over the *slice* neighbours only, i.e. omitting the
sigma-partner column. A10's audit found that W30's reduction from `ROWS` to `S`
— step (1) of W30-X — is **false as written**: the claimed `GL_3` map has
determinant `0`. The repair is not a repair of the mathematics but of the
prose: the correct object is `S'`, and W30's *code* already computed `S'`.
A10, verdict T2:

> **CONFIRMED IN SUBSTANCE; step (1) false as written and unnecessary** (the
> GL_3 map has det 0; correct object = the AUGMENTED slice matrix S' over all
> Gamma-neighbours; W30's CODE already uses S' — prose wrong only).

(`computations/unaudited-audit-a10-2026-08-20/REPORT.md`, lines 13–17.)

The relation between the two objects, for the record: `ROWS[t] = P . S'(tau)[t]`
where `P` is the `3 x |N(v)|` matrix whose column at a present slice neighbour
`s_j` is `sc * e_j` and whose column at the sigma partner is `u`. Transfer of
rank or of span-membership through `P` needs `P` **injective**, i.e.
`|N(v)| <= 3` together with `u[j0] != 0` at the absent slice column `j0`
(automatic when all Gamma cells are nonzero, since `u[j0] = d_{q0} * l_ij`).
*Source:* `a10_t2.py`, module docstring lines 11–16. **Nothing below uses this
transfer** — it is recorded because it is what W30-X's step (1) was trying to
be, and because the `S1_transfer` control tests it.

Note `n = |N(v)|` is **not** always `3`. A10's structural census
(`results_smoke.json`, key `C3_structure`, `vertexinfo`) records, for example,
`n_gamma_nbrs = 2` at `R6` when `m = 25` and `n_gamma_nbrs = 4` at every `L`
vertex from `m = 25` on; at `m = 28` every vertex has `4` Gamma neighbours
(`log_smoke.txt`, `C3 m=28 ... deg={0: 4, 1: 4, ..., 7: 4}`). The `n = 4` case
is exactly where the old mechanism evaporates, and the bounds below are stated
uniformly in `n` for that reason.

## 2. The cofactor identity

**Theorem 2.1 (cofactor identity).** Fix a site `v` and a word `w`. Let
`tau = (w(s_1), ..., w(s_n))` be the slice tuple that `w` induces on `N(v)`,
and define the **cofactor vector**

```
    Q(w)_j  =  haf_{Gamma - {v, s_j}} (w)
```

— the Gamma-hafnian of the word `w` restricted to the six sites other than `v`
and `s_j`. Then, for every letter `t`,

```
    Phi( w | v = t )  =  < S'(tau)_t , Q(w) >
                      =  sum_{j=1..n}  S'(tau)[t][j] * Q(w)_j .          (C)
```

*Proof (A10's sketch, made explicit).* `Phi(w|v=t)` is a sum over the Gamma
perfect matchings of `K_8`. Every such matching covers `v` by exactly one edge
`v s_j` with `s_j in N(v)`. Partition the sum by that edge. The block of the
partition indexed by `s_j` contributes

```
    A_{v, s_j}[t][w(s_j)]  *  ( sum over Gamma perfect matchings of the
                                remaining six sites of the product of their
                                cells )
      =  S'(tau)[t][j]  *  Q(w)_j .
```

Summing over `j` gives (C). **Hafnians are permanent-like: there are no
signs**, so no sign bookkeeping arises. A10's verdict on this step: "Step (3)
exact (hafnian expansion along v; no sign issue)"
(`computations/unaudited-audit-a10-2026-08-20/REPORT.md`, line 17). `∎`

**Hypotheses: none.** (C) is an identity in the block entries, valid at every
point, over any commutative ring, at every support, at every site, for every
`t`. It assumes no cleanness, no off-stratum condition, no nonvanishing. This
is exactly what the verification in §4 was designed to test.

*Source of the statement:* `a10_t2.py`, module docstring line 22:
`Phi(w|v=t) = <S'(tau)_t, Q(w)>, Q_s = haf_{Gamma-{v,s}}(w).` Implementation:
`Qvec()` (lines 83–103), which computes each `Q_s` by **raw enumeration of the
15 perfect matchings of the remaining six vertices** — no memo, no recursion,
nothing shared with `Phi`'s own routine.

## 3. The Q-span rank bound

**Corollary 3.1 (`S'.Q = 0` at untriggered words).** Let `w` be a word at a
clean point that is *untriggered* at `v` — that is, `Phi(w|v=t) = 0` for all
three letters `t`. Then by (C)

```
    S'(tau) . Q(w)  =  0 ,
```

so `Q(w)` lies in the kernel of `S'(tau)`.

**Theorem 3.2 (the Q-span bound).** For a slice tuple `tau`,

```
    rank S'(tau)  <=  |N(v)|  -  dim span{ Q(w) : w untriggered with
                                           slice tuple tau } .           (QB)
```

*Proof.* By Corollary 3.1 every such `Q(w)` lies in `ker S'(tau)`, so
`dim span{Q(w)} <= dim ker S'(tau) = |N(v)| - rank S'(tau)` by rank–nullity on
the `3 x |N(v)|` matrix. `∎`

Write `Qspan(tau) := dim span{Q(w) : w untriggered with slice tuple tau}` and
`threshold := |N(v)| - 2`, the value of `Qspan` at which (QB) forces
`rank S'(tau) <= 2`.

W30's own phrasing of the same bound, for the record:

> rank S(tau) <= |N(v)| - dim span{Q(w) : w untriggered with tuple tau}
> (from S.Q = 0 at untriggered words)

(`computations/unaudited-exclusion-w30-2026-08-19/REPORT.md`, lines 93–95 —
**note W30 writes `S` where the correct object is `S'`**; A10's form is the one
above.)

**Remark 3.3 (the bound is one-directional).** (QB) bounds the rank *from
above* using the cofactor vectors. It gives no lower bound on `rank S'` and no
statement at all when `Qspan(tau) = 0`. In particular it is **not** a
protection statement, and §5 records why it cannot be turned into one.

## 4. Verification record

### 4.1 The identity, at random non-clean blocks

The decisive control: (C) is claimed to be an *identity*, so it must be tested
where cleanness fails, or a passing test would be evidence only about the
solution locus.

Control `S3_identity` (`a10_t2.py`, lines 312–342):

```
    4 supports (m = 25, 26, 27, 28)
      x 3 fields (Q with Fraction blocks, F_13, F_31)
      x 8 sites v
      x 8 random words w
      x 3 letters t
    ------------------------------------------------
    tests      = 2,304
    violations = 0
```

`Phi(w|v=t)` on the left-hand side is computed by `A.phi_raw`, the raw
enumeration of all 105 perfect matchings of `K_8` — **not** by any route that
shares code with `S'` or `Q`.

Sources: `computations/unaudited-audit-a10-2026-08-20/results_t2.json`, key
`S3_identity`: `{"tests": 2304, "violations": 0, "sample": [], "ok": true,
"note": "cofactor identity on RANDOM blocks -- an identity, no cleanness
assumed"}`; `computations/unaudited-audit-a10-2026-08-20/log_t2.txt`, line 1:
`S3 identity on random blocks: violations=0`.

### 4.2 Mutation control on the identity

A control that cannot fail is worthless. `MUT` (`a10_t2.py`, lines 344–381)
perturbs **one cell** of one Gamma block (`b2[e0][0][0] += 1` at `m = 27`,
`p = 31`, `v = 5`), recomputes `S'` and `Q` from the perturbed blocks, and
requires the identity to **break** against the *unperturbed* `Phi`:

```
    baseline_identity_holds  = true
    mutation_breaks_identity = true
```

Source: `results_t2.json`, key `MUT`, note "one perturbed cell must make the
cofactor identity fail against the unperturbed Phi"; `log_t2.txt`, line 2:
`MUT: base=True detected=True`.

### 4.3 The Q-span bound, at real points

Control `Y1_kernel_bound` (lane target 4,
`computations/unaudited-audit-a10-2026-08-20/a10_t4.py`) evaluates (QB) at
every `(point, vertex, tuple)` of A10's point corpus:

```
    Y1_kernel_bound :  { "violations": 0, "n_points": 92, "ok": true }
```

Source: `computations/unaudited-audit-a10-2026-08-20/results_t4.json`, key
`Y1_kernel_bound`. The per-point traces in the same file's `points` array carry
`bound_violations: 0` at every one of the 8 vertices of every point; the run
log echoes `bviol=0` on each line
(`computations/unaudited-audit-a10-2026-08-20/log_t4.txt`), and the closing
line reads `T4 DONE bound_viol=0 law_viol=0 escapes=2`.

The 92 points span `m = 25, 26, 27, 28`, fields `F_13`, `F_31` and `Q`, and
four provenances: W30's 17 re-verified refutation points (`verify#0..16`),
W30's hunter output (`hunt|...`), A10's own wide `Q` corpus
(`wide25|`, `wide26|`, `wide27|`) and stored W21 objects. A10 states the
scanned total as "9,802 records re-scanned, 0 violations"
(`computations/unaudited-audit-a10-2026-08-20/REPORT.md`, §"Controls run",
covering `Y1/Y2/Y4/Y5` jointly).

### 4.4 Mutation control on the bound

`Y5_mutation` requires the kernel-bound checker to be falsifiable: at a
**non-clean** random point the untriggered words no longer annihilate `S'`, so
the bound must break. It does:

```
    Y5_mutation : { "bound_violations_on_random_point": 57, "ok": true }
```

with the note "on a NON-clean random point the untriggered words no longer
annihilate S', so the kernel bound must be violated — the checker is not
vacuously true" (`results_t4.json`, key `Y5_mutation`; `log_t4.txt`:
`Y5 mutation: bound violations on random non-clean point = 57`).

### 4.5 Independent transfer check

`S1_transfer` checks that the delivery predicate computed *through* `S'` agrees
with the one computed through `ROWS`, at **every** index choice, and that `P` is
injective exactly when `|N| <= 3` and `u[j0] != 0`. Aggregated over the 78
points of the target-2 run: `transfer_violations 0`, `P_not_injective 0`,
`u_absent_zero 0` (`log_t2.txt`, closing line `T2 DONE {...}`;
`results_t2.json`, `S1_transfer`).

## 5. What is **not** claimed

**(a) `det M = 0` is not reproved here — A10 correction D8.** W30 reported that
step (3) "is also a short independent proof of W26's `det M = 0`"
(`computations/unaudited-exclusion-w30-2026-08-19/REPORT.md`, line 44). A10:

> D8: "step (3) reproves det M = 0" is trivial-or-empty; drop.

(`computations/unaudited-audit-a10-2026-08-20/REPORT.md`, line 49.) The claim
is dropped and is not restated anywhere in this package. `det S'(tau) = 0` for
`|N(v)| = 3` follows from (C) only when `Q(w) != 0`, and `Q != 0` is not
supplied by the identity — it is an extra hypothesis on the point.

**(b) No protection statement.** (C) and (QB) are an identity and an upper
bound. Neither says that any vertex delivers, at any support, under any
hypothesis on cleanness alone. The conditional statement that *does* draw a
delivery conclusion is Lemma W30-Y, stated with its hypotheses in
`draft_lemma_w30y.md`; and even there the conclusion is conditional. A10's line
is binding: "NOT promotion-ready: any unconditional protection statement."

**(c) `Qspan` is not a proxy for failure.** W30 round 4 refuted side condition
(c) as a *necessity*: "R5 Q-span driven to 0 at m=27/F_13 (and m=26 both
vertices) — still delivers, rank 1"
(`computations/unaudited-exclusion-w30-2026-08-19/REPORT.md`, lines 186–188).
A vertex with `Qspan = 0` — where (QB) is vacuous — can still deliver, and does.

**(d) Characteristic.** (C) and (QB) hold over any commutative ring; they are
untouched by every `F_p` refutation in the corpus (hazards ledger item 24).
Their *verification* was carried out over `Q`, `F_13` and `F_31`.

## 6. Artifact paths

| item | path |
|---|---|
| statement of (C), `S'`, and the `P`-transfer | `computations/unaudited-audit-a10-2026-08-20/a10_t2.py`, module docstring lines 7–38 |
| implementations `Sprime` / `Qvec` | same file, lines 76–103 |
| identity verification (2,304 tests, random blocks) | `computations/unaudited-audit-a10-2026-08-20/results_t2.json`, key `S3_identity`; `log_t2.txt` |
| mutation control on the identity | same file, key `MUT` |
| Q-span bound verification (92 points, 0 violations) | `computations/unaudited-audit-a10-2026-08-20/results_t4.json`, key `Y1_kernel_bound`; `log_t4.txt` |
| mutation control on the bound (57 violations at a non-clean point) | same file, key `Y5_mutation` |
| transfer / predicate agreement | `results_t2.json`, key `S1_transfer` |
| W30's origin phrasing (in the superseded `S` notation) | `computations/unaudited-exclusion-w30-2026-08-19/REPORT.md`, lines 30–34 and 93–95 |
| A10's green light and D8 | `computations/unaudited-audit-a10-2026-08-20/REPORT.md`, lines 49 and 65–70 |
| master-plan context | `notes/2026-08-15-resolution-master-plan.md`, v53 and v57 addenda |

**Standing.** An identity and an upper bound; no closure, no narrowing of any
certified dependency, no protection claim.
