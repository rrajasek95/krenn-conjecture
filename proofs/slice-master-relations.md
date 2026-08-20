# The slice master relations and the cofactor identity

> **Dependency ID `SLICE-MASTER`** (approved 2026-08-20), ledger record
> `SUPERSESSION-2026-08-20-02`. The results are W26-M / W26-M* (lane W26) and
> the cofactor identity and Q-span bound (lane W30), all independently
> re-derived and confirmed at the promotion gate by audit A10; written up by
> lane P3 on 2026-08-20 from staging pinned at repository HEAD
> `5f8ab49245bf6cde841bb4e92fbdb5781ac2f866`. The **gated** Section 5 is
> separately audited by A11 and carries its own record (see the gate banner).
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
> **Section 5 is GATED and is NOT part of `SLICE-MASTER`.** It states
> *conditional* delivery lemmas belonging to `ROUTE-A-RESIDUAL`, staged for
> record `SUPERSESSION-2026-08-20-04` and audited separately by A11. See the
> gate banner at §5.

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

## 5. GATED — the delivery lemmas

> ## ▲ GATE ▲
> **This section is NOT part of dependency `SLICE-MASTER` and is NOT certified
> by `SUPERSESSION-2026-08-20-02`.** It belongs to `ROUTE-A-RESIDUAL` and is
> staged for record `SUPERSESSION-2026-08-20-04`.
>
> Sections 1–4 and 6–8 do **not** depend on anything in this section. A reader
> may delete §5 entirely without affecting a single statement elsewhere in this
> document.
>
> Every statement below is **conditional**, with explicit hypotheses. **No
> unconditional protection statement is made here or anywhere in this
> document**, and §6 gives the objects that block one.
>
> Restaged 2026-08-20 on audit **A11**
> (`computations/unaudited-audit-a11-2026-08-20/REPORT.md`), which corrected
> the previous draft of this section in four ways: W30-Z was missing a
> hypothesis and carried a redundant one; its round-3 blind-test record **is
> not on disk and must not be cited**; W30-Y is a corollary of W30-Z rather
> than a peer; and the `m = 25` statement is a **disjunction**, because the two
> candidate theorems for it are *incomparable*.

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

**The zero-scale convention, stated because it is load-bearing.** An index
choice whose scale vanishes has `ROWS == 0`, and would therefore **deliver
vacuously** under the literal predicate. W26, W30 and A10 all skip such
choices, and this document does too. The convention is not cosmetic: it is why
a hypothesis asserting *nonzero scale* is needed twice over — once to make the
transfer map injective, and once to make the set of live index choices
non-empty at all
(`computations/unaudited-audit-a11-2026-08-20/results_t1.json`, key
`T1e_hidden_hypotheses`, field `zero_scale_convention`).

### 5.1 The governing lemma

**Lemma 5.1 (W30-Z, the governing delivery lemma).** Let `v` be a site with two
distinct firing letters `t_1 != t_2`, and let `tau` be a slice tuple at which
both clean pairs survive. Write `t_3` for the third, doubly-clean letter.
Suppose

* **(Z1)** `rank S'(tau) <= 2`, and
* **(Z2)** the doubly-clean row `S'(tau)_{t_3}` is **nonzero** — which holds
  whenever **every Gamma cell is nonzero**, since each entry
  `A_{v,s_j}[t_3][tau_j]` is then a nonzero Gamma cell.

Then `v` **delivers**.

*Proof.* Suppose `v` fails at both of the index choices realising `t_1` and
`t_2` at `tau`. Non-delivery at the choice firing `t_i` says that the firing
row `S'(tau)_{t_i}` does not lie in the span of that choice's clean rows. Taken
together over `i = 1, 2` at the *same* tuple, neither firing row lies in the
span of the remaining two rows, which forces `rank S'(tau) = 3` — **provided
`S'(tau)_{t_3} != 0`**, which is (Z2). That contradicts (Z1). `∎`

**Remark 5.2 (hypothesis (Z2) is not removable).** Without it the implication is
**false**: there are explicit rank-2 slices with a vanishing doubly-clean row at
which neither firing row lies in its clean span. A11 exhibits five
(`computations/unaudited-audit-a11-2026-08-20/results_t3.json`, key
`Z2_side_condition_necessity`, `n_counterexamples_when_S_t3_zero: 5`). This
hypothesis is A10's second correction to the retired W30-X, and the previous
statement of W30-Z **did not inherit it**.

**Remark 5.3 (a hypothesis that was redundant, and where it does belong).** The
earlier statement of W30-Z also assumed "`S_{t1}` not in `ker phi`". That is
**implied by non-delivery** at the first choice and is therefore redundant as a
hypothesis of the rank-`<= 2` direction: of 33 non-delivering configurations
examined, **none** had the corresponding row zero
(`results_t3.json`, key `Z2_kerphi_redundancy`,
`n_non_delivering_configs: 33`, `n_of_those_with_R_t1_zero: 0`). It is dropped
here. Where the `ker phi` condition *does* matter is in the discussion of
delivery-genuineness and of the `D2` mode — see Remark 5.4 and §6 (c).

**Remark 5.4 (the converse is FALSE).** `rank S'(tau) = 3` does **not** imply
failure. The counterexample mechanism is **`D2`**: the transfer map drops the
rank, so a site at slice rank 3 can still deliver. A11 traced eight such
objects across `m = 25, 26, 27, 28`, and in **every** one the mechanism at
every delivering index choice is `D2` — for instance an `m = 27`/`F_13` point
where `L1` sits at rank 3 and delivers at all `515` of its delivering choices,
and `L2` likewise at `268` (`results_t3.json`, key `P2_converse_traces` in
`results_t6.json`; `mechanisms: {"phi_drops_rank_(D2)": ...}` on every trace).
Consequently the "failure requires rank 3" reading of W30-Z is **not** part of
the lemma, and no document should carry it.

**Corollary 5.5 (W30-Y, the Q-span corollary).** Let `v` have two distinct
firing letters realised at a common slice tuple `tau` with nonzero scale, let
every Gamma cell be nonzero, and suppose

```
    Qspan(tau)  >=  |N(v)| - 2 .
```

Then `v` delivers.

*Proof.* By the Q-span bound (Theorem 4.3),
`rank S'(tau) <= |N(v)| - Qspan(tau) <= 2`, which is (Z1); all-cells-nonzero
gives (Z2). Apply Lemma 5.1. `∎`

So W30-Y is a **corollary of W30-Z via the Q-span bound**, not an independent
statement. Note that `|T_f| = 1` per index choice — carried as a hypothesis in
the previous draft — is not needed for Lemma 5.1, and at `m = 25` it is not
needed at all (§5.2, correction (ii)).

### 5.2 The `m = 25` disjunctive lemma

At `m = 25` the site `R6` is special for a purely structural reason, and the
statement below is the one object the two competing candidate theorems for it
both fit inside.

**Template facts at `m = 25`, `R6`** — rebuilt from the 28-entry masks alone
(`computations/unaudited-audit-a11-2026-08-20/results_t1.json`, key
`T1a_structure`):

* `N(6) = {5, 7}` **exactly**, because *both* the sigma edge `(3,6)` and the
  `R`-`R` edge `(4,6)` are absent at `m = 25`. Hence `S'` is `3 x 2` and
  `ROWS = hafL . [c_7 | 0 | c_5]`; the sigma-partner column does not arise, so
  the `GL_3` / `u_q0` conditions of Remark 3.3 never appear here at all.
* The live singles into `R6` are `(0,6) -> letter 2`, `(1,6) -> letter 1`,
  `(2,6) -> letter 1`. **Letter `0` is the target of no live single**, so
  **`T_c` is non-empty at every one of the 823 admissible index choices**
  (`letter0_always_clean: true`, `Tc_always_nonempty: true`). This is a stated
  template fact, not an assumption.
* `|T_f|` histogram over the 823 admissible choices: `{1: 671, 2: 152}`. So
  **`|T_f| = 1` is *not* available as a hypothesis** — 152 choices have
  `|T_f| = 2` — and it is not needed: the rank-1 argument of branch (B) covers
  them.
* Firing letters `{1, 2}`; six two-pair tuples.

**Lemma 5.6 (`m = 25`, `R6`; disjunctive).** Let every Gamma cell be nonzero
**(H2)**. Suppose **either**

* **(R25)** some slice tuple carries two surviving index choices with
  **different** firing letters;

**or both of**

* **(alpha)** some admissible `R6` index choice has `hafL != 0`; and
* **(beta)** at some such tuple, an untriggered word has `Q = (B, C) != 0`.

Then `R6` **delivers**.

*Proof of branch (R25) — the shared-letter pigeonhole.* `R6`'s firing letters
are `{1, 2}`, so the two clean pairs are `{0, 2}` and `{0, 1}`, which **share
the letter `0`**. If both choices failed, both pairs would be rank 1; sharing a
letter, that forces all three rows parallel, i.e. `rank S' = 1`. But then every
pair has rank `1 = rank S'`, so every choice delivers — contradiction. `∎`

*Proof of branch (alpha)+(beta) — the `3 x 2` rank chain.* By the cofactor
identity (Theorem 4.1) specialised to `N(6) = {5,7}`,
`Phi(w | y_6 = t) = <S'_t, Q(w)>` with the two-term cofactor vector
`Q = (B, C)`. An untriggered word gives `S' . Q = 0`; by **(beta)** some such
`Q != 0`, so `rank S' <= 1`. By **(H2)** the rows are nonzero, so
`rank S'|_P = rank S' = 1` and the firing row lies inside the clean span. By
**(alpha)** a surviving (live) choice exists, so the delivery is realised.
`∎`

**Correction record (A11's four statement corrections), all incorporated
above.**

| # | correction | where |
|---|---|---|
| (i) | `T_c` non-empty is a needed **template fact**, not a hypothesis — letter `0` is no live single's target, verified at all **823** choices | template facts, third bullet |
| (ii) | **`|T_f| = 1` is NOT needed at `m = 25`** — `152/823` choices have `|T_f| = 2`, and the rank-1 argument of branch (B) covers them | template facts, fourth bullet; the lemma assumes no `T_f` size |
| (iii) | the **zero-scale convention is load-bearing**: (alpha) is needed **twice** — to make `P` injective *and* to make the live-choice set non-empty | §5.0, closing paragraph; branch (B)'s last step |
| (iv) | **(H1) clean and (H3) off-stratum are NEVER USED** — the implication holds at random non-clean and at vanishing-stratum points; "`=> pure row`" is a **control, not a step** | stated as Remark 5.7 |

**Remark 5.7 ((H1) and (H3) are inert).** Cleanness and off-stratum-ness appear
in the ambient setting of this programme but are **not used** by Lemma 5.6:
A11 verified the implication at random **non-clean** points and at
**vanishing-stratum** points and found it holds there too
(`computations/unaudited-audit-a11-2026-08-20/results_t7.json`, keys
`G1_non_clean_points`, `G2_vanishing_stratum`). They are recorded as inert so
that no future statement carries them as though they were doing work. Likewise
the implication "`R6` delivers `=> ` pure row" is a **control on the delivery
engine**, not a step of the proof.

**Remark 5.8 (why a disjunction, and not either branch alone).** The two
branches are **incomparable**, so neither theorem supersedes the other:

| | (R25) branch | (alpha)+(beta) branch | disjunction |
|---|---|---|---|
| corpus points covered | 28 / 32 | 32 / 32 | **32 / 32** |
| points where the hypothesis fails | **4 / 32** | **0 / 32** | 0 / 32 |

(R25) fails at 4 of the 32 corpus points — including the `Q` point seed
`925024` and the round-10 `alpha_13` object — while (beta) fails at none of
them. Conversely, (beta) *can* fail: A11 re-verified a stored `F_13` hunt point
(`results_hunt_m25_13_b.json|s1073|R5,R7,L3`; clean, all cells nonzero, `2,124`
nonzero words) where `Q == 0` on whole tuple classes and **`R6` still delivers
at 695 of 743 live index choices**. That object refutes the *strong* reading of
the (beta) branch but **not hypothesis (beta) itself**, which holds there via
the `y_7 != 2` tuples. Sources:
`computations/unaudited-audit-a11-2026-08-20/results_t10.json`, keys
`W2_escape_object` and `W3_supersession` (`W36_strictly_supersedes: false`).

### 5.3 Structural note — the `m = 25` closure is an `n = 2` phenomenon

The pigeonhole of branch (R25) is **not** a general fact about slice matrices.
It works at `m = 25` because `|N(6)| = 2`, so the three rows live in `K^2`, and
two rank-1 pairs sharing a letter must collapse the whole matrix to rank 1. At
`|N(v)| = 3` the rows live in `K^3` and the argument **provably fails**.

| | `n = 2` (`3 x 2`, `m = 25` `R6`) | `n = 3` (`3 x 3`) |
|---|---|---|
| both clean pairs can fail? | **never** | **yes, typically** |
| evidence | **exhaustive**: all `2,985,984` all-nonzero `3 x 2` matrices over `F_13`; `both_choices_fail = 0` | sampled: `183,176` of `200,000` random all-nonzero `3 x 3` matrices have both pairs failing |
| non-vacuity | `456,192` matrices have exactly **one** of the two choices failing (`228,096 + 228,096`), so the test is not constant-true | — |

Sources: `computations/unaudited-audit-a11-2026-08-20/results_t10.json`, keys
`W1_pigeonhole_n2` (`matrices 2985984`, `both_choices_fail 0`,
`outcome_hist {"(False, False)": 2529792, "(False, True)": 228096,
"(True, False)": 228096}`) and `W1_fails_at_n3_control`
(`samples 200000`, `both_fail 183176`, with an explicit example matrix).

**This is exactly why `m = 26` and `m = 27` retain a `Q` hypothesis `(Q3)` and
`m = 25` does not.** At those supports the protected sites have `|N| = 3`, the
pigeonhole is unavailable, and something must supply `rank <= 2` — which is what
`(Q3)` does, through the Q-span bound. The asymmetry is structural, not an
artefact of how hard anyone looked.

### 5.4 Verification record for §5

**Checker.** `computations/verify_delivery_lemmas.py`, frozen SHA-256
`9289423bd6cc6814701f21ec1de128f0a486e18928f5c6211a8d48aba600670f`. Standard
library only, no import from any `computations/unaudited-*` directory, house
raising `require()` and no bare `assert`. Eight steps; the run record is
`checker_run_delivery_log.txt` and `results_delivery_checker.json`.

| step | check | result |
|---|---|---|
| 1 | `m = 25`/`R6` template facts rebuilt from the masks | `N(6) = {5,7}`; **823** admissible; `\|T_f\|` histogram `{1: 671, 2: 152}`; `T_c` never empty |
| 2 | **branch (R25), EXHAUSTIVELY at `n = 2`** | all **2,985,984** all-nonzero `3 x 2` matrices over `F_13`: **both-fail 0**; exactly-one-fail **456,192** (non-vacuous) |
| 3 | **branch (alpha)+(beta), the rank step, exhaustively** | rank `<= 1`: **20,736/20,736** have every row in every other row's span; rank 2: **2,965,248/2,965,248** have a failing pair |
| 4 | the same pigeonhole at `n = 3` | **183,113 / 200,000** (91.6 %) have both pairs failing — it fails, as §5.3 requires |
| 5 | Lemma 5.1 (W30-Z) synthetic, random `n in {2,3,4}` over `F_31` | **6,910** of 20,000 configurations meet the hypothesis; **0 violations** |
| 6 | **MUT-Z2**: dropping (Z2) must falsify the implication | **3** constructed + **19,774** random `(Z2)`-less counterexamples |
| 8 | **calibration** against A11's two named objects | **2/2** reproduce A11's recorded flags |
| 7 | coverage at the stored corpora | **36** stored points: disjunction **36/36**; (R25) failures **1**; (beta) failures **0** |

```
    RUN 1  python3         --wide 30 --hunt 3 --strict    ALL PASS    EXIT 0
    RUN 2  python3 -O      --wide 30 --hunt 3 --strict    ALL PASS    EXIT 0
    RUN 3  python3 -I -S   --wide 30 --hunt 3 --strict    ALL PASS    EXIT 0
    RUN 4  NEGATIVE CONTROL  admissible census corrupted   FAILS      EXIT 1
    RUN 5  NEGATIVE CONTROL  (R25) with |T_f|=1 dropped    FAILS      EXIT 1
```

Steps 2 and 3 reproduce A11's exhaustive counts **exactly**, recomputed from
the template masks on an independent implementation rather than copied.

**Step 7 is not a reproduction of A11's `4/32`.** The stored subset and A11's
32-point corpus differ, so the checker reports what it measured over the
points that exist on disk — `36/36` covered, one (R25) failure, no (beta)
failure — and excludes the unstored members **loudly** (the
`unstored_excluded` field of `results_delivery_checker.json`) rather than
interpolating them.

**Step 8, and why it exists.** (R25) retains W36's `|T_f| = 1` condition.
A11's correction (ii) — "`|T_f| = 1` is not needed at `m = 25`" — applies to
the *(alpha)+(beta)* branch, whose rank-1 argument covers the 152 choices with
`|T_f| = 2`; it does **not** loosen (R25). Dropping the condition there makes
(R25) hold at seed `925024`, where A11 records it **failing** — which would
erase the very asymmetry that makes the promotion object a disjunction. That
error was made while writing this checker and was caught by step 8; RUN 5
re-injects it and confirms the guard still fires.

**Ledger 21/31 discipline.** The checker's `ok` field is written by exactly one
function, which appends to `_controls_run` in the same call; the run ends by
asserting declared-equals-run and by re-scanning every emitted block for an
`ok` whose control never ran. This checker cannot produce the
`ok: true` / `_controls_run: []` pattern that ledger 31 was added for.

---

Beyond the checker: only counts that A11 **re-derived on its own engine**, or
that come from **stored** point corpora, are quoted below. Three classes of number are
deliberately excluded, and each exclusion is a finding in its own right:

* **W30's round-3 blind-test record (`124/126`, `112/114`) is NOT ON DISK** and
  cannot be re-traced. Per A11: *do not carry it as evidence.* It appears
  nowhere in this document.
* **`[::7]`-stride samples labelled as censuses.** `w30_indep.py` and
  `w36_escobj.py` evaluate only every seventh untriggered word, so round 10's
  "123 `Q = 0` words" and W36's word counts are **1-in-7 samples**, not
  censuses. A11's full enumeration over all `376` template-untriggered words is
  quoted instead (`results_t2.json`, key `V6_Q_sampling_control`).
* **Counts from unstored points.** The "32/33 independent family" is not
  re-derivable because those points were never stored, and round 10's most
  informative exception object is lost. No figure from them is used.

| control | result | source (`computations/unaudited-audit-a11-2026-08-20/`) |
|---|---|---|
| W30-Z implication, synthetic | `40,000` tests over `F_31`, random `n in {2,3,4}`, random transfer map `P`; `violations_with_S_t3_nonzero = 0` | `results_t3.json`, `Z2_implication` |
| (Z2) necessity | `5` explicit counterexamples when `S'_{t3} = 0` | `Z2_side_condition_necessity` |
| redundancy of the dropped hypothesis | `33` non-delivering configs, `0` with the row zero | `Z2_kerphi_redundancy` |
| **W30-Z blind test (A11's, replacing the lost record)** | `58` points, `4,720` measurements, `183` point-vertex pairs; **deliver at rank `<= 2`: 115/115**; `n_W30Z_counterexamples = 0`; rank histogram `{1: 800, 2: 2090, 3: 1830}` | `Z3_blind_test` |
| the converse, reported separately | `fail_at_rank3 = 51/68`; all `17` exceptions are `D2` | `Z3_blind_test`; traces in `results_t6.json`, `P2_converse_traces` |
| protected-set negative control | "two firing letters AND `\|N\| <= 3`" selects **exactly** `{25_R6, 26_R5, 26_R6, 27_R5}` | `results_t3.json`, `Z1_negative_control` |
| `m = 25` rank chain, exhaustive | all `2,985,984` all-nonzero `3 x 2` matrices over `F_13`: of the `20,736` with rank `<= 1`, **all** have every row in every other row's span | `results_t1.json`, `T1d_rank_chain` |
| its non-vacuity control | the other `2,965,248` (rank 2) **all** have a failing pair | `T1d_nonvacuity_control` |
| two-term cofactor closed form | `864` tests at random blocks, `0` mismatches: `B = hafL*r45 + l03*d1*d2`, `C = hafL*r47 + l23*d0*d1` | `T1c_two_term_cofactor` |
| its mutation control | `30/30` perturbations detected | `T1c_mut_control` |
| `ROWS = hafL.[c7\|0\|c5]` | `864` tests at random blocks, `0` violations | `T1b_rows_form` |
| lemma verification | `90` point-tuple pairs over the stored `Q` family (all rank 1) + `16` new A11-generated points; `26` points with `n_alpha = n_beta = n_conclusion = 26`, `violations: []` | `results_t2.json`, `V1`–`V3` |
| the mathematical core | `(beta)` at a tuple forces `rank S' <= 1`: no point where it fails | `V4_rank1_iff_beta` |
| delivery-engine positive control | `25` of `26` points have **some** failing vertex (`R5` 20, `L3` 12, `R7` 7, `L0` 5, `R4` 1) — the engine is not vacuously affirmative | `V5_positive_control` |
| pigeonhole, `n = 2` vs `n = 3` | `2,985,984` exhaustive / `0` both-fail; `183,176`/`200,000` at `n = 3` | `results_t10.json`, `W1_*` |

**A11's engine independence.** A11 wrote `a11_lib.py` from scratch — stdlib
only, raw 105-matching `Phi`, its own `S'`/`Q`/`ROWS` built from the committed
spine, **zero imports from `w26`, `w30`, `a10` or `w36`**. Its self-test is in
§7 of this document, where it serves as a third independent confirmation of the
identities of §§2 and 4.

**A11's own failed search, stated as such.** A11's ledger-20 adversarial build
produced `177` new clean points with `0` failures and `0` escapes. That is a
**failed search** and is not evidence for anything (hazards-ledger item 18);
A11 reported it as such and so does this document.

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

**(c) No converse.** Rank `3` does **not** imply failure, and nothing in this
document asserts that it does. A verified clean off-stratum point over `Q`,
with all 144 Gamma cells nonzero, has `R6` at rank `3` at all 81 tuples and
delivers nonetheless. The mechanism is `D2` — the transfer map drops the rank —
and it accounts for **every** traced counterexample: see Remark 5.4, where
eight objects across `m = 25, 26, 27, 28` are traced and each delivering index
choice at each of them is `D2`. Any statement of the form "failure requires
rank 3" is outside this document's scope and is not supported by it.

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

**Independent corroboration — two further engines.** Every step above
reproduces results obtained on **two** other implementations, each written from
scratch and each importing nothing from the lanes it checks.

*Audit A10* (`computations/unaudited-audit-a10-2026-08-20/results_{smoke,t2,t4}.json`):
`C2_master_relation` (`violations 0`), `S3_identity`
(`tests 2304, violations 0`, note "cofactor identity on RANDOM blocks -- an
identity, no cleanness assumed"), `Y1_kernel_bound`
(`violations 0, n_points 92`), `MUT` (`base=True detected=True`),
`Y5_mutation` (`bound_violations_on_random_point 57`).

*Audit A11* (`computations/unaudited-audit-a11-2026-08-20/results_t0.json`) —
`a11_lib.py`, stdlib only, raw 105-matching `Phi`, own `S'`/`Q`/`ROWS`, **zero
imports from `w26`, `w30`, `a10` or `w36`**:

| control | result |
|---|---|
| `S0_census` — structure rebuilt from the 28-entry masks alone | `mismatches: []` |
| `S1_phi_two_routes` | `288` tests, `0` violations |
| **`S2_master_relation`** | **`2,592` tests, `0` violations** — random blocks, no cleanness, LHS by raw 105-matching |
| **`S3_cofactor_identity`** | **`2,592` tests, `0` violations** — random (hence non-clean) blocks, LHS raw |
| `S4_mutA_cofactor` | `36/36` perturbations detected |
| `S5_mutB_master` | `36/36` perturbations detected |
| `S6_wrong_slice_negative_control` | of `144` mangled-slice variants, only `1` still satisfied (C) — the identity test is not vacuous |

So the two identities of §§2 and 4 now stand on **three** independent
implementations (A10, A11, and this checker), agreeing at every test, with
working mutation controls on each.

## 8. Provenance

| lane | role | directory | pinned HEAD |
|---|---|---|---|
| **W26** | origin of W26-M / W26-M*; symbolic on 16 `(m,vertex)` pairs, mutation controls 8/8; engine reproduced 39/39 stored verdicts against `w21_core`/`w24_core` | `computations/unaudited-blockers-w26-2026-08-16/` | `dee2ca3293f5f0c12831b374f6cf521aa2c02e14` |
| **W30** | origin of the cofactor identity and the Q-span law; built the slice machinery on the relations | `computations/unaudited-exclusion-w30-2026-08-19/` | `021b1a307e8edb10b964fadefd4b823bdb589035` |
| **W36** | origin of the `m = 25` shared-letter pigeonhole (branch (R25) of Lemma 5.6) | `computations/unaudited-routea-w36-2026-08-20/` | — |
| **A10** | the promotion-gate audit for §§1–4: from-scratch engine, own 105-matching `Phi`, own admissibility, own slice rows from an independent hand re-derivation, **zero imports** from `w26`/`w30` code | `computations/unaudited-audit-a10-2026-08-20/` | `f9a3bd6b93417a43d86ad782d1f76b62f14bc50a` |
| **A11** | the audit of §5: W30 rounds 7–10 and W36; own engine `a11_lib.py`, **zero imports** from `w26`/`w30`/`a10`/`w36` | `computations/unaudited-audit-a11-2026-08-20/` | `14f53e7` |
| **P3** | this write-up and the checker | `computations/unaudited-promotion-p3-2026-08-20/` | `5f8ab49245bf6cde841bb4e92fbdb5781ac2f866` |

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
