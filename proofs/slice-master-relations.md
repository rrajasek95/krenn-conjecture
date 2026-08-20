# The slice master relations and the cofactor identity

> **Dependency ID `SLICE-MASTER`** (approved 2026-08-20), ledger record
> `SUPERSESSION-2026-08-20-02`. The results are W26-M / W26-M* (lane W26) and
> the cofactor identity and Q-span bound (lane W30), all independently
> re-derived and confirmed at the promotion gate by audit A10; written up by
> lane P3 on 2026-08-20 from staging pinned at repository HEAD
> `e2123f2c006944972cefcdce1b8a3c021f9c2a18`.
>
> **Checker** `computations/verify_slice_master_relations.py`, frozen SHA-256
> `8b8385c1db6f5f1351558c7432be785b384677e9fdbb58052db44dea41681ab5`.
> **Certified commit:** recorded in `certification/SUPERSESSIONS.md`
> (`SUPERSESSION-2026-08-20-02`) in the directly linked follow-up commit.
>
> **This document proves no part of the Krenn–Gu conjecture.** It establishes
> two identities and one rank bound — machinery that the Route A residual
> programme at supports `m = 25..28` runs on. It narrows no certified
> dependency and closes nothing.
>
> **Section 5 is GATED and is NOT part of `SLICE-MASTER`.** It states a
> *conditional* lemma belonging to `ROUTE-A-RESIDUAL`, held pending lane W30's
> round 9. See the gate banner at §5.

## 1. The model, and the one structural fact

Let `N = 8` with sites `V = {0,...,7}`, alphabet `{0,1,2}`, and one `3 x 3`
block `A_uv` per edge `uv` of `K_8`. For a word `w : V -> {0,1,2}`,

```
    H_w(A, z)  =  sum over the 105 perfect matchings M of K_8
                    of  prod_{(u,v) in M}  c_uv( w_u , w_v ),
```

where an edge carrying the full mask (a **Gamma** edge) contributes
`A_uv[w_u][w_v]`, an edge carrying a one-bit mask (a **single**, at cell
`(a,b)`) contributes `z_uv` when `(w_u, w_v) = (a,b)` and `0` otherwise, and an
absent edge contributes `0`. Write

```
    Phi(w)  :=  the z-free part of H_w
            =   sum over the perfect matchings that lie inside Gamma.       (0)
```

Fix the bipartition and the pairing

```
    L = {0,1,2,3},   R = {4,5,6,7},
    sigma = ( 0 <-> 7 ,  1 <-> 4 ,  2 <-> 5 ,  3 <-> 6 ),
```

so that `Gamma` is `K_4(L)` together with the `R`-graph and the *present*
`sigma` edges. For a word `w` put

```
    l_ij  =  A_{i,j}[w_i][w_j]                    (i < j in L),
    r_ab  =  A_{a,b}[w_a][w_b]                    (a < b in R),
    d_a   =  A_{a, sigma a}[w_a][w_{sigma a}]     (a in L),

    hafL  =  l_01 l_23 + l_02 l_13 + l_03 l_12,
    hafR  =  r_45 r_67 + r_46 r_57 + r_47 r_56,
```

with the convention that any symbol whose edge is not a Gamma edge is `0`.

**Lemma 1.1 (the sigma-count decomposition).** Every Gamma perfect matching
uses `k in {0, 2, 4}` sigma edges, and

```
    Phi  =  hafL * hafR
            +  sum_{i<j in L}  l_ij * r_{sigma i, sigma j} * d_p * d_q
            +  d_0 d_1 d_2 d_3 ,                                            (1)
```

where `{p,q} = L - {i,j}` in the middle sum.

*Proof.* Partition the Gamma perfect matchings by their set of sigma edges. A
matching with no sigma edge splits into a perfect matching of `L` and one of
`R`, giving `hafL * hafR`. A matching with exactly two sigma edges, at
`p, q in L`, uses the sigma edges `d_p, d_q` and must match the remaining
`{i,j} = L - {p,q}` inside `L` and their partners `{sigma i, sigma j}` inside
`R`, giving `l_ij * r_{sigma i, sigma j} * d_p * d_q`. A matching with all four
sigma edges gives `d_0 d_1 d_2 d_3`. There is no matching with an odd number of
sigma edges, because the sigma edges are the only edges between `L` and `R`
and `|L| = |R| = 4`. `∎`

**(1) is the entire structural input to this document.** Everything below is
(1) together with one expansion of `hafL`.

**Machine check.** `Phi` computed by (1) and by raw enumeration of the perfect
matchings of `K_8` lying inside Gamma agree on all tests: `80` tests over four
supports and two fields, `0` mismatches (checker STEP 2;
`computations/unaudited-audit-a10-2026-08-20/results_smoke.json`, key
`C1_phi_two_routes`, `mismatches 0`).

## 2. The master relations

**Theorem 2.1 (W26-M, the R-vertex master relation).** Let `v in R`, put
`p = sigma^{-1}(v) in L`, and vary *only* the letter `t` at `v`, holding the
other seven coordinates fixed. Then

```
    hafL * Phi(t)  =  sum_{q in L - {p}}  B_q * ROW(t)[q] ,                 (M)

    B_q       =  hafL * r_{sigma i, sigma j}  +  l_pq * d_i * d_j ,
    ROW(t)[q] =  d_p(t) * ( d_q * l_ij )  +  hafL * r_{v, sigma q}(t) ,
```

with `{i,j} = L - {p,q}` in both lines. Here `d_p(t) = A_{p,v}[w_p][t]` and
`r_{v, sigma q}(t) = A_{v, sigma q}[t][w_{sigma q}]` are the only symbols
carrying `t`; every other symbol is constant in `t`.

*Proof.* Collect (1) by the two occurrences of `v` — the sigma edge `pv` and
the `R`-edges `v s`:

```
    Phi(t)  =  sum_{q != p}  r_{v, sigma q}(t) * B_q  +  d_p(t) * A,
    A       =  sum_{q != p}  l_ij * r_{sigma i, sigma j} * d_q
               +  prod_{q != p} d_q .
```

Multiply through by `hafL`. For the `A` term use the **three-pairing
identity**

```
    hafL * prod_{q != p} d_q  =  sum_{q != p}  l_pq * l_ij * d_i * d_j * d_q ,
                                                    {i,j} = L - {p,q},      (2)
```

which is the expansion `hafL = l_pq l_ij + l_pi l_qj + l_pj l_qi` multiplied by
`d_i d_j d_q` and re-indexed: each of the three terms of `hafL` pairs `p` with
one `q != p`, and the complementary pair `{i,j}` supplies `l_ij`. Regrouping
the result by `q` gives exactly (M). `∎`

**Theorem 2.2 (W26-M*, the L-dual).** Let `p in L` and vary only the letter `s`
at `p`. Then

```
    hafR * Phi(s)  =  sum_{a in L - {p}}  X_a * ROW(s)[a] ,                (M*)

    X_a       =  hafR * l_bc  +  r_{sigma p, sigma a} * d_b * d_c ,
    ROW(s)[a] =  d_p(s) * ( d_a * r_{sigma b, sigma c} )  +  hafR * l_{p,a}(s),
```

with `{b,c} = L - {p,a}` in both lines.

*Proof.* The same computation with the roles of `L` and `R` exchanged; the
sigma pairing makes that exchange an involution of (1). `∎`

### 2.1 Hypotheses, stated because they are load-bearing

**(H1) These are identities in the block entries.** (M) and (M*) hold at *every*
assignment of the blocks, over any commutative ring. They are not properties of
clean points, of off-stratum points, or of any solution locus. The verification
in §7 tests exactly this by working at **random** blocks: a check confined to
the solution locus could not distinguish an identity from a coincidence there.

**(H2) Each relation carries information only where its scale is nonzero.** The
scale of (M) is `hafL`; the scale of (M*) is `hafR`. Where the scale vanishes,
both sides are `0 = 0` and the relation says nothing about `Phi`. This is not a
defect: it is the mechanism behind the escape phenomena of §5.1 and behind the
`m = 28` `L2` exception of §5.4.

**(H3) No hypothesis on the point.** Cleanness, off-stratum-ness,
all-cells-nonzero and the vanishing stratum are not used. They enter only in
the *consumers* of the relations, never in the relations.

**(H4) The letter ranges over the whole alphabet.** Nothing is assumed about
which letters are clean, triggered or firing; that bookkeeping belongs to the
delivery predicate (§5.0), not to the identity.

## 3. The augmented slice matrix

**Definition 3.1.** For a site `v` let

```
    N(v)  =  { s :  vs is a Gamma edge } ,
```

listed in a fixed order `s_1 < ... < s_n`, `n = |N(v)|`. For a **slice tuple**
`tau = (tau_1, ..., tau_n)` — one letter per neighbour — the **augmented slice
matrix** is the `3 x n` matrix

```
    S'(tau)[t][j]  =  A_{v, s_j} [t] [tau_j] ,      t in {0,1,2} .
```

The columns run over **all** Gamma neighbours of `v`; when the sigma edge at
`v` is present, its column is the `d` column.

**Remark 3.2 (`n` is not always 3).** At `m = 25` the site `R6` has `n = 2`;
every `L` site has `n = 4` from `m = 25` on; at `m = 28` every site has
`n = 4`. The statements below are therefore written with `n` symbolic. Machine
census: checker STEP 1 rebuilds the Gamma degrees from the templates alone and
matches the recorded table
(`computations/unaudited-audit-a10-2026-08-20/results_smoke.json`, key
`C3_structure`) — `m = 25` degrees `(4,4,4,3,3,3,2,3)`, `m = 28` degrees
`(4,4,4,4,4,4,4,4)`.

**Remark 3.3 (a superseded predecessor, recorded so it is not revived).** An
earlier formulation used a `3 x 3` matrix `S` over the *slice* neighbours only,
omitting the sigma-partner column, and claimed a reduction `ROWS = psi(S)` with
`psi in GL_3`. **That claim is false: the map has determinant `0`.** The correct
object is `S'`. For the record, the true relation is `ROWS[t] = P . S'(tau)[t]`
with `P` the `3 x n` matrix whose column at a present slice neighbour `s_j` is
`sc * e_j` and whose column at the sigma partner is `u`; transferring rank or
span-membership through `P` requires `P` injective, i.e. `n <= 3` together with
`u[j0] != 0` at the absent slice column `j0`. **Nothing in this document uses
that transfer.** Only the *linearity* of `P` is ever consumed, which is why the
statements here are uniform in `n` and in `m`; the three conditions
(`GL_3`, `u[j0] != 0`, `n <= 3`) survive only inside the rank bound of §4.2,
where they govern how much the bound yields rather than whether it applies.

## 4. The cofactor identity and the Q-span bound

**Theorem 4.1 (cofactor identity).** Fix a site `v` and a word `w`. Let `tau`
be the slice tuple `w` induces on `N(v)`, and define the **cofactor vector**

```
    Q(w)_j  =  haf_{Gamma - {v, s_j}} (w) ,
```

the Gamma-hafnian of `w` restricted to the six sites other than `v` and `s_j`.
Then for every letter `t`

```
    Phi( w | v = t )  =  < S'(tau)_t , Q(w) >
                      =  sum_{j=1..n}  S'(tau)[t][j] * Q(w)_j .              (C)
```

*Proof.* By (0), `Phi(w|v=t)` is a sum over the Gamma perfect matchings of
`K_8`. Each such matching covers `v` by exactly one edge `v s_j` with
`s_j in N(v)`; partition the sum by that edge. The block indexed by `s_j`
contributes

```
    A_{v,s_j}[t][w(s_j)]  *  ( sum over Gamma perfect matchings of the
                               remaining six sites of the product of cells )
      =  S'(tau)[t][j]  *  Q(w)_j .
```

Summing over `j` gives (C). Hafnians are permanent-like — there are no signs —
so no sign bookkeeping arises. `∎`

**Hypotheses: none.** (C) is an identity in the block entries, valid at every
point, over any commutative ring, at every support, at every site, for every
letter.

**Corollary 4.2 (`S' . Q = 0` at untriggered words).** Call `w` **untriggered
at `v`** if `Phi(w | v = t) = 0` for all three letters `t`. Then by (C),
`S'(tau) . Q(w) = 0`, i.e. `Q(w) in ker S'(tau)`.

**Theorem 4.3 (the Q-span bound).** For a slice tuple `tau`,

```
    rank S'(tau)  <=  |N(v)|
                      -  dim span{ Q(w) : w untriggered at v with tuple tau }.
                                                                           (QB)
```

*Proof.* By Corollary 4.2 every such `Q(w)` lies in `ker S'(tau)`, so
`dim span{Q(w)} <= dim ker S'(tau) = |N(v)| - rank S'(tau)` by rank–nullity on
the `3 x n` matrix `S'(tau)`. `∎`

Write `Qspan(tau)` for that dimension. The value `|N(v)| - 2` is the threshold
at which (QB) forces `rank S'(tau) <= 2`.

**Remark 4.4 (the bound is one-directional).** (QB) bounds the rank from above
and gives no lower bound, and it says nothing when `Qspan(tau) = 0`. It is not
a protection statement; see §6.

## 5. GATED — conditional Lemma W30-Y

> ## ▲ GATE ▲
> **This section is NOT part of dependency `SLICE-MASTER` and is NOT certified
> by `SUPERSESSION-2026-08-20-02`.** It belongs to `ROUTE-A-RESIDUAL` and is
> **HELD** pending lane W30's round 9, which may upgrade the `m = 25` story and
> so change both what is promoted here and how it is stated.
>
> Sections 1–4 and 6–8 do **not** depend on anything in this section. A reader
> may delete §5 entirely without affecting a single statement elsewhere in this
> document.
>
> The lemma below is **conditional**, with seven explicit hypotheses. **No
> unconditional protection statement is made here or anywhere in this
> document**, and §6 gives the three objects that block one.

### 5.0 The predicate, named

Every statement in this section is about one predicate, and reports that do not
name theirs are not comparable:

> at an index choice (letters on the seven coordinates other than `v`) let
> `T_f` be the set of letters at which some LIVE single into `v` fires, and
> `T_c` the rest. The site `v` **DELIVERS** at that index choice iff
> `ROW(t_f) in span{ROW(t) : t in T_c}` for every `t_f in T_f`; it **FAILS**
> iff it delivers at **no** admissible index choice.

Call this predicate **`FAIL_primary`**. An alternative rank phrasing `(*)`
appears in earlier prose; it is a *consequence* of `FAIL_primary` valid only
where a coefficient is forced nonzero, and at `m = 28` **nothing is forced**.
The two come apart completely there: under `FAIL_primary` co-failing pairs
exist (1,657 distinct instances of one pair over `F_31`), while under `(*)`
**no** `m = 28` point exhibits any co-failing pair at all, because the
individual sites violate `(*)` wholesale (`R5` at `380/472` live index choices,
`L2` at `436/508`).

### 5.1 The lemma

**Lemma 5.1 (W30-Y, conditional).** Let `P` be a **clean** point at which
**every Gamma cell is nonzero**, and let `v` be a site. Suppose:

* **(Y1)** `v` has two distinct firing letters;
* **(Y2)** those two letters are realised at a **common** slice tuple `tau` by
  index choices each having `|T_f| = 1` and **nonzero scale** (`hafL != 0` at an
  `R`-site, `hafR != 0` at an `L`-site);
* **(Y3)** `Qspan(tau) >= |N(v)| - 2`.

Then `v` **delivers** — it does not `FAIL_primary` — and the delivery yields a
genuine pure row.

*Proof.* By (Y3) and Theorem 4.3, `rank S'(tau) <= |N(v)| - Qspan(tau) <= 2`.

Suppose `v` fails. Then it fails at both index choices of (Y2). Each has
`|T_f| = 1`, so each asserts exactly one thing: its single firing row
`S'(tau)_{t_f}` does not lie in the span of the clean rows at that choice. The
two choices have distinct firing letters `t_1 != t_2` at the *same* tuple
`tau`, so neither of `S'(tau)_{t_1}`, `S'(tau)_{t_2}` lies in the span of the
other two rows. Hence `rank S'(tau) = 3`, **provided the doubly-clean row
`S'(tau)_{t_3}` is itself nonzero** — and it is, entry by entry, because every
entry `A_{v,s_j}[t_3][tau_j]` is a Gamma cell and all Gamma cells are nonzero
by hypothesis. This contradicts `rank S'(tau) <= 2`. So `v` delivers.

That the delivery yields a genuine pure row rather than a vacuous
span-membership is the audit's `HGAP` control, which reports
`n_deliver_no_pure = 0` across its corpus. `∎`

**Remark 5.2 (uniform in `m`).** The lemma is stated with `|N(v)|` symbolic and
so covers the `n = 4` sites of `m = 28` (threshold `2`) on the same footing as
`m = 25`/`R6` (`n = 2`, threshold `0`, where (Y3) is automatic once (Y2)
holds). The predecessor formulation needed `n <= 3`, a `GL_3` map and
`u_q0 != 0`; by Remark 3.3 none of those is used by the argument, and dropping
them is exactly what makes the lemma uniform.

## 6. What is not claimed

**(a) No unconditional protection, at any support.** Lemma 5.1 is an
implication whose hypotheses fail at real points. Three independent escape
objects are on record:

| object | why the hypotheses fail | does the site still deliver? |
|---|---|---|
| `m = 27` / `F_13`, site `R5`: clean, all Gamma cells nonzero, off-stratum (1,107 nonzero words), `hafL` vanishing on **36 of 81** `L`-words and covering **all 12** two-pair tuples | (Y2)'s scale half fails at every realising tuple | **yes** — all eight sites deliver |
| `m = 25` / `Q`, site `R6`: all cells nonzero | six two-letter tuples but **zero** with two *surviving* firing letters | **yes** — delivers at 264 of 264 surviving index choices |
| `m = 27` / `F_31`, site `L2` | escape geometry co-occurs with a genuine failure | **no** |

At every escape point where the sites do deliver, they deliver **for a reason
this machinery does not supply**. Identifying that reason is an open problem,
not a gap in the statements above.

**(b) In particular, `m = 25`/`R6` is not unconditional.** At `n = 2` the
threshold is `0`, so (Y3) is free — but (Y2) still has to hold, and at the
`Q` point above it does not.

**(c) No converse.** Rank `3` does not imply failure: a verified clean
off-stratum point over `Q`, with all 144 Gamma cells nonzero, has `R6` at rank
`3` at all 81 tuples and delivering nonetheless.

**(d) `det M = 0` is not reproved here.** `det S'(tau) = 0` for `n = 3` follows
from (C) only when `Q(w) != 0`, and `Q != 0` is an extra hypothesis on the
point, not a consequence of the identity. The earlier remark that the cofactor
step gives an independent proof of that determinant law is trivial-or-empty and
is withdrawn.

**(e) `Qspan` is not a proxy for failure.** A site with `Qspan = 0`, where (QB)
is vacuous, can still deliver, and does.

**(f) Characteristic.** (1), (M), (M*), (C) and (QB) hold over any commutative
ring and are untouched by every `F_p` refutation in this corpus; verification
was carried out over `Q`, `F_13` and `F_31`.

**(g) Nothing here is a positive closure.** Per the ledger's standing rule,
this document is machinery for a negative programme; it closes no case of the
Krenn–Gu conjecture and narrows no certified dependency.

## 7. Verification and replay

The checker is `computations/verify_slice_master_relations.py` — standard
library only, no import from any `computations/unaudited-*` directory, house
raising `require()` and no bare `assert`, so it is equally strict under
`python3 -O`. Seven steps; five runs of record.

| step | what it checks | result |
|---|---|---|
| 1 | structure rebuilt from the template masks alone — Gamma edges, live singles, clean words, Gamma perfect matchings, Gamma degrees — matched against the recorded census at all four supports | census matched |
| 2 | `Phi` by raw enumeration vs the decomposition (1) | **80** tests, `0` mismatches |
| 3 | (M) and (M*) at **random** blocks, four supports x two fields x eight sites x six words x three letters | **1,152** tests, `0` violations |
| 4 | the cofactor identity (C) at random **non-clean** blocks over `Q`, `F_13`, `F_31`, LHS by the raw 105-matching route | **2,304** tests, `0` violations, **12** witnessed non-clean block sets |
| 5 | the Q-span bound (QB) at stored `F_p` points | **6** points, **3,373** tuples, **50,564** untriggered words, `0` violations |
| 6 | **MUT-A**: a load-bearing one-cell perturbation must break (C) against the unperturbed `Phi` | **32/32** fired |
| 7 | **MUT-B**: with a real point's untriggered word sets but randomised blocks, (QB) must be violated | **344/345** tuples violate |

Runs (`checker_run_log.txt`):

```
    RUN 1  python3         --npoints 6 --strict     ALL PASS      EXIT 0
    RUN 2  python3 -O      --npoints 6 --strict     ALL PASS      EXIT 0
    RUN 3  python3 -I -S   --npoints 6 --strict     ALL PASS      EXIT 0
    RUN 4  NEGATIVE CONTROL  --strict, corpus absent  FAILS       EXIT 1
    RUN 5  NEGATIVE CONTROL  census mutated           FAILS       EXIT 1
```

**Why steps 4, 6 and 7 are the ones that matter.** (C) and (QB) would both be
satisfied vacuously by a checker that only ever looked at clean points or that
could not fail. Step 4 therefore works at random **non-clean** blocks and
verifies explicitly that at least one block set *is* non-clean; step 6 shows a
single perturbed cell breaks (C); step 7 shows that randomising the blocks
under a real point's untriggered word sets breaks (QB) almost everywhere. Runs
4 and 5 show the checker's own gates work: the optional-but-loud point-corpus
step cannot silently skip when demanded, and the structural census in step 1 is
live — it caught a wrong value during authoring (the `m = 27` Gamma
perfect-matching count, guessed as 13, true value 12).

**Independent corroboration.** Every step above reproduces a result of audit
A10, computed on a different engine written from scratch: A10's
`C2_master_relation` (`violations 0`), `S3_identity`
(`tests 2304, violations 0`, note "cofactor identity on RANDOM blocks -- an
identity, no cleanness assumed"), `Y1_kernel_bound`
(`violations 0, n_points 92`), `MUT` (`base=True detected=True`) and
`Y5_mutation` (`bound_violations_on_random_point 57`). Sources:
`computations/unaudited-audit-a10-2026-08-20/results_{smoke,t2,t4}.json`.

## 8. Provenance

| lane | role | directory | pinned HEAD |
|---|---|---|---|
| **W26** | origin of W26-M / W26-M*; symbolic on 16 `(m,vertex)` pairs, mutation controls 8/8; engine reproduced 39/39 stored verdicts against `w21_core`/`w24_core` | `computations/unaudited-blockers-w26-2026-08-16/` | `dee2ca3293f5f0c12831b374f6cf521aa2c02e14` |
| **W30** | origin of the cofactor identity and the Q-span law; built the slice machinery on the relations | `computations/unaudited-exclusion-w30-2026-08-19/` | `021b1a307e8edb10b964fadefd4b823bdb589035` |
| **A10** | the promotion-gate audit: from-scratch engine, own 105-matching `Phi`, own admissibility, own slice rows from an independent hand re-derivation, **zero imports** from `w26`/`w30` code | `computations/unaudited-audit-a10-2026-08-20/` | `f9a3bd6b93417a43d86ad782d1f76b62f14bc50a` |
| **P3** | this write-up and the checker | `computations/unaudited-promotion-p3-2026-08-20/` | `e2123f2c006944972cefcdce1b8a3c021f9c2a18` |

**A10's verdict on the promotable material**, verbatim from
`computations/unaudited-audit-a10-2026-08-20/REPORT.md`:

> **Promotion-ready (A10's list)**
> W26-M/M* identities; the cofactor identity Phi(w|v=t) =
> <S'(tau)_t, Q(w)>; the Q-span bound; the CONDITIONAL Lemma W30-Y
> (S'-form, |T_f| = 1 explicit, no step (1)); the sampling
> correction + pure-row observation as record corrections. NOT
> promotion-ready: any unconditional protection statement.

The corrections A10 required are discharged as follows: the object is `S'` and
the `GL_3` step is struck (§3, Remark 3.3); only linearity of the transfer map
is used, which is why the statements are uniform in `m` (Remark 3.3, Remark
5.2); the determinant remark is withdrawn (§6 (d)); "`m = 25`/`R6`
unconditional" is struck (§6 (b)); `|T_f| = 1` and the nonzero-scale condition
are explicit hypotheses (Lemma 5.1 (Y2)); and the predicate is named in every
statement that consumes it (§5.0). The remaining corrections are records rather
than mathematics and are carried in the companion note on the Route A residual
corrections.

**One open item in the provenance.** W26 reports its symbolic verification as
covering "16 `(m,vertex)` pairs" without saying which 16 of the 32. The
standing of Theorems 2.1 and 2.2 does not depend on the answer: A10 checked all
32 pairs numerically over two fields, and the checker of §7 re-checks all 32
independently.
