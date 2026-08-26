# THEOREM W37-PER — the permanent collapse of the cap error

**UNAUDITED probe output (lane W37, 2026-08-20).** Pinned HEAD in
`PINNED_HEAD.txt`. Nothing outside this directory was modified; nothing was
committed. Verification is two-family (this lane's engine `w37_core.py`,
written from the statements in `proofs/clean-pair-cap-exact-descent.md`, and
W25's independent `w25_core.cap_error`), with the negative controls recorded
below actually firing.

Terminology (hazards ledger, terminology items 1/2/5): *witness* here is
**sense (1)** — the descent input, an active clean cap `(p,q,K)` with
`s·kappa_0·kappa_1·kappa_2 != 0` and `E_pq(K) = 0`.

---

## 1. Statement

Let `A` be a ternary source on `N = 2h + 2` sites `V`, let `p != q` in `V`
with `A_pq != 0`, and put `U = V - {p,q}`. Suppose `U` splits as
`U = P + Q` with `|P| = |Q| = h` and

* **(S1)** `A_{p,x} = 0` for every `x` in `P`;
* **(S2)** `A_{q,y} = 0` for every `y` in `Q`;
* **(S3)** `A_{q,x} = alpha_x (x) beta_x` for `x` in `P`, and
  `A_{p,y} = gamma_y (x) delta_y` for `y` in `Q` (rank at most one);
* **(S4)** `A_{x,y} = c_{xy} · (beta_x (x) delta_y)` for `x` in `P`,
  `y` in `Q` — the `P`–`Q` blocks are rank at most one and *aligned* with
  the vectors of (S3). (`c_{xy} = 0`, i.e. no `P`–`Q` edge at all, is the
  special case (S4-0).)

Then for every cap covector `K`,

```
    E_pq(K)  =  Phi(K) · Theta,
    Theta    =  (x)_{x in P} beta_x  (x)  (x)_{y in Q} delta_y ,
```

where `Phi` is a single polynomial of degree at most `h` in the nine cap
unknowns. Under (S4-0),

```
    Phi(K) = per M(K),        M(K)_{x,y} = gamma_y^T K alpha_x    (h x h).
```

At `h = 2` (`N = 6`), (S2) and (S4) are **not needed** — the cap error has
only its top term there, so (S1) and (S3) alone give the collapse.
At `h >= 4` the mixed matchings need one further hypothesis (`P` or `Q`
independent); `h = 2, 3` are what this lane verified.

**Corollary (witness criterion).** Under the hypotheses, the whole
`3^{2h}`-component cap system is equivalent to the single equation
`Phi(K) = 0`, so `(p,q)` is a witness iff `Phi` has a zero with
`K_00 K_11 K_22 != 0` and `<K, A_pq> != 0` — or `Theta = 0`, in which case
`E` vanishes identically and every admissible cap is a witness.

**Corollary (the antisymmetric cap is the canonical solution).** Suppose in
addition the blocks of (S3) are single cells with pairwise distinct colours
on each side (the edge-coloured / Latin situation): `alpha_x = e_{c(x)}`,
`gamma_y = e_{d(y)}` with `c` and `d` injective. Then `M(K)` is `K` read
through two colour bijections, so `Phi = per K` (up to row/column
relabelling), and

```
    K = I + E_{xy} - E_{yx}          (x != y)
```

has `per K = 0`, `K_00 K_11 K_22 = 1 != 0`. It is admissible whenever the
`pq` cell is one of the five nonzero cells of that `K` — in particular
always when `A_pq` is a diagonal single cell and `{x,y}` is chosen to be
the two colours other than the `pq` colour. This is exactly the
antisymmetric cap of **W25-U3**, and it is exactly the cap the exact
decider returns at the stored `N = 6` rigid points.

---

## 2. Proof

Write `R_{ab}` for the effective edge of `proofs/clean-pair-cap-exact-descent.md`,

```
    R_ab[c_a][c_b] = sum_ij K_ij ( A_{p,a}[i][c_a] A_{q,b}[j][c_b]
                                 + A_{q,a}[j][c_a] A_{p,b}[i][c_b] ),
```

and expand `E_pq(K)` by the definition: a term for each perfect matching
`M` of `U` and each subset `J` of `M` with `|J| >= 2`, of weight
`s^{h-|J|} · prod_{f in J} R_f · prod_{f in M-J} A_f`.

**(a) `R` vanishes inside `P` and inside `Q`.** For `a,b` in `P` both
summands of `R_ab` contain a factor `A_{p,a}` or `A_{p,b}`, zero by (S1);
for `a,b` in `Q` both contain `A_{q,a}` or `A_{q,b}`, zero by (S2).

**(b) Mixed matchings die (at `h = 3`).** Let `M` have `m > 0` edges inside
`P`; since `|P| = |Q|` it then has `m` edges inside `Q` and `h - 2m` cross
edges. By (a), a nonzero term needs `J` inside the cross edges, so
`|J| <= h - 2m`. At `h = 3` and `m >= 1` this is `<= 1 < 2`: no term
survives. (At `h = 2`, `m >= 1` forces `m = 1` and `h - 2m = 0`, likewise
nothing survives; this uses only (S1) via `R_{p'p''} = 0`.)

**(c) The cross `R`s are rank one and share their factors.** For `x` in
`P`, `y` in `Q`, the first summand of `R_xy` dies by (S1) and

```
    R_xy[u][v] = sum_ij K_ij alpha_x[j] beta_x[u] gamma_y[i] delta_y[v]
               = ( gamma_y^T K alpha_x ) · beta_x[u] delta_y[v]
               = M(K)_{x,y} · (beta_x (x) delta_y)[u][v].
```

**(d) Cross matchings.** A cross matching is a bijection `sigma : P -> Q`.
Its `J = M` term is `prod_x M_{x,sigma(x)} · prod_x (beta_x (x)
delta_{sigma(x)})`, and the tensor factor equals `Theta` **for every
`sigma`**, because each `beta_x` sits at site `x` and each `delta_y` at
site `y` regardless of the pairing. Summing over `sigma` gives
`per M(K) · Theta`.

Its terms with `|J| < h` carry a factor `A_{x,sigma(x)}` with `x` in `P`,
`sigma(x)` in `Q`; under (S4-0) these vanish, and under (S4) they equal
`c_{x,sigma(x)} (beta_x (x) delta_{sigma(x)})`, again a factor of `Theta`.
Hence every surviving term is a scalar times `Theta`, and

```
    Phi(K) = sum over sigma, over J subset of M with |J| >= 2, of
             s^{h-|J|} prod_{x in J} M_{x,sigma(x)}
                       prod_{x not in J} c_{x,sigma(x)} ,
```

a polynomial of degree at most `h` in `K` (degree exactly `h`, equal to
`per M(K)`, when all `c_{xy} = 0`). QED

---

## 3. What it explains

**(i) The `N = 6` rigid-stratum law — the task-3 question "why exactly 9".**
W27's stored census (`results_t3_x3decomp.json`) records 51 rigid `X_3`
points at `N = 6`, each with exactly 9 witnesses. Re-reading that file
here shows the 9 are always **exactly the nine cross pairs** of a
bipartition of the six sites into a triple `T` and its complement, with all
three pairs inside `T` dead and the live pairs inside `V - T` blocked
(51/51, two counting views: 38 points with 3 dead + 3 live-blocked, 13 with
4 dead + 2 live-blocked). For `p` in `T` and `q` outside, `T` independent
gives (S1) with `P = T - {p}`, and the cross blocks are rank one, so
Theorem W37-PER applies at `h = 2` and the pair is a witness via the
antisymmetric cap on the two colours complementary to the `pq` colour —
which is precisely the cap the decider returns. The count is
`|T| · |V - T| = 3 · 3 = 9`.

**(ii) The `N = 8` template.** The same collapse holds at `h = 3` and the
same antisymmetric cap solves it, so the aligned-split stratum is a
**witness-guaranteed region of `X_3` at `N = 8`** — the first
witness-existence statement at the open order that is a theorem rather than
a measurement.

**(iii) Why the falsifier is all-blocked.** The collapse needs `p` to miss
all of `P` and `q` to miss all of `Q`: at `N = 8` that is 6 prescribed dead
pairs in a prescribed shape. `W25-F8` has exactly 7 dead pairs —
`(0,2),(0,3),(0,6),(2,4),(2,5),(3,5),(4,6)` — and an exhaustive check of
all `(p,q)` and all `3+3` splits finds **no split at all**: sites 0 and 2
each miss exactly three sites, but no partner `q` misses the complementary
triple. So no collapse mechanism is available anywhere on F8, which is
consistent with its 21/21 blockage and is the structural reason for it.

---

## 4. Verification record

| check | result |
|---|---|
| identity, `h = 2`, random rank-one configs, own engine | 40/40 |
| identity, `h = 2`, cross-family (W25 `cap_error`) | 15/15 |
| identity, `h = 3` (S4-0), own engine | 25/25 |
| identity, `h = 3` (S4-0), cross-family | 12/12 |
| identity, `h = 3`, (S1)(S2) with dense `P`–`P`, `Q`–`Q` | 20/20 |
| identity, `h = 3`, cross-family, same | 8/8 |
| identity, `h = 3`, aligned (S4) with all nine `c_xy != 0` | 10/10 |
| **control** — drop (S4)/(S4-0): dense `P`–`Q` blocks | fails 12/12 |
| **control** — non-aligned rank-one `P`–`Q` blocks, `h = 3` | fails 10/10 |
| **control** — drop (S3): a rank-2 block among the four used | fails |
| explicit admissible `per`-zero caps built at `h = 3` | 12/12 |
| prediction vs the exact Singular decider | 8/8, no contradiction |
| non-degeneracy of the stratum (`h = 3`, dense `P`–`P`/`Q`–`Q`) | 5,070 of 6,561 words have `H_w != 0` |

Files: `run_b1_n6theorem.py`, `run_b2_permanent.py`,
`results_b1_n6theorem.json`, `results_b2_permanent.json`, `log_b2.txt`.

## 5. Honest scope

* `h = 4` and above are **not** verified; the mixed-matching step (b) needs
  an extra hypothesis there and this lane did not test it.
* The corollary's admissibility argument is stated for the single-cell
  Latin situation. For general rank-one blocks the criterion is "the
  degree-`h` form `Phi` has an admissible zero"; whether that can fail is
  exactly the residual question, and the answer is yes in principle (it
  fails iff `Phi` is, up to scalar, a product of the four admissibility
  linear forms `K_00, K_11, K_22, s`).
* The theorem is a **sufficient** condition for a witness. It does not
  bear on sources with no split — including every stored `N = 8` object
  other than the aligned-split ones constructed here.
