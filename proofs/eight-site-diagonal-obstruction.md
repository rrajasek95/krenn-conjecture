# The eight-site block-diagonal obstruction

> **Dependency ID `N8-DIAGONAL`** (ratified 2026-08-20), ledger record
> `SUPERSESSION-2026-08-20-01`. The result is W29-T1 (lane W29), confirmed at
> the promotion gate by audit A9; promoted by lane P2-diag on 2026-08-20 from
> staging pinned at repository HEAD `5377acdc43992e8eaaf4f17f4f1068b7242dfe73`.
>
> **Checker** `computations/verify_eight_site_diagonal_obstruction.py`,
> frozen SHA-256
> `b7540367b6c28da13b4dce5b3e9fe4658acfef162a268c4ffc7cb6d15dc51b2a`.
> **Certified commit:** recorded in `certification/SUPERSESSIONS.md`
> (`SUPERSESSION-2026-08-20-01`) in the directly linked follow-up commit.
>
> **This theorem does not resolve `eqSystem8_no_solution_d3`.** That
> `formal-conjectures` item is the *general bicoloured* statement at
> `n = 8, d = 3` and remains open; what follows is its diagonal sub-case. See
> Remark 1.4 and Section 11.

## 1. Statement

Let `N` be even and let `V` be a set of `N` named sites. A **block-diagonal
ternary weighting** of `K_N` assigns to each unordered pair `uv` a diagonal
matrix

```
    A_uv  =  diag( t^0_uv , t^1_uv , t^2_uv )     in  F^3 ⊗ F^3,
```

equivalently three symmetric edge-weight functions `t^0, t^1, t^2` on the pairs
of `V`, with values in a field `F`. For a word `w : V -> {0,1,2}` the
perfect-matching amplitude is

```
    Phi(w)  =  sum over perfect matchings M of K_N
                 of  prod_{uv in M}  A_uv( w(u), w(v) ).                  (1)
```

Because each `A_uv` is diagonal, a matching edge contributes only when its two
endpoints carry the same colour, so `Phi(w)` factorises over the colour classes
of `w`:

```
    Phi(w)  =  prod_{c=0,1,2}  haf( t^c | w^{-1}(c) ),                    (2)
```

where `haf(t | S)` is the hafnian of the symmetric weight `t` restricted to
`S`, that is, the sum over perfect matchings of `S` of the product of the
weights, with `haf(t | empty) = 1` and `haf(t | S) = 0` for `|S|` odd. The
factorisation (2) is the entire structural content of diagonality; nothing else
about the diagonal case is used below.

Call `w` **constant** if it is constant on `V`, and **mixed** otherwise.

**Theorem 1.1 (no block-diagonal exact source at `N = 8`).** Let `F` be any
field, of any characteristic. There is no block-diagonal ternary weighting of
`K_8` over `F` with

```
    Phi(c^8) = 1   for c = 0, 1, 2,        Phi(w) = 0   for every mixed w.
```

**Theorem 1.2 (amplitude-nonzero strengthening).** The same holds under the
weaker hypothesis

```
    Phi(c^8) != 0  for c = 0, 1, 2,        Phi(w) = 0   for every mixed w,
```

that is: no block-diagonal ternary weighting of `K_8` over any field produces an
**unnormalised** GHZ tensor `sum_c lambda_c e_c^{⊗8}` with all three amplitudes
`lambda_c` nonzero. No root extraction, no algebraically closed field, and no
rescaling are needed anywhere in the proof.

Theorem 1.1 is the specialisation `lambda_c = 1` of Theorem 1.2; only
Theorem 1.2 is proved below.

**Corollary 1.3 (the classical edge-coloured Krenn–Gu statement at `N = 8`).**
There is no *single-cell* (edge-coloured) ternary source on `K_8`: an
assignment of one colour and one weight to each edge of a multigraph on eight
vertices, such that every perfect matching is monochromatic with the three
constant amplitudes nonzero and all mixed amplitudes zero, does not exist.

*Proof of the corollary.* An edge-coloured source is the block-diagonal
weighting with `t^c_uv = ` (sum of the weights of the edges of colour `c` on
`uv`) and `t^d_uv = 0` for the other colours `d` — a special case of the
hypothesis of Theorem 1.2, in which additionally at most one of `t^0_uv`,
`t^1_uv`, `t^2_uv` is nonzero for each pair `uv`. Apply Theorem 1.2. `∎`

**Remark 1.4 (scope; what is *not* claimed).** The theorem is about
*block-diagonal* weightings — three independent weight functions, one per
colour. It is strictly stronger than the single-cell edge-coloured reading
(Corollary 1.3) and strictly weaker than the general bicoloured statement, in
which `A_uv` is an arbitrary `3 x 3` matrix. **The general bicoloured case
`n = 8, d = 3` remains open.** The same machine closes `N = 6` (Section 7) and
correctly *fails* at `N = 4`, where the exceptional source exists (Section 7.3).
**It does not close `N >= 10`**: see Section 9, where the earlier
"uniform in even `N`" claim is withdrawn with its refutation.

**Remark 1.5 (rings).** The proof uses only three facts about `F`: that it has
no zero divisors, that `1 != 0`, and the definition `haf(t | empty) = 1`. Every
clause validity in Section 5 is proved from those alone. Theorem 1.2 therefore
holds verbatim over any integral domain.

**Remark 1.6 (terminology guard).** Per
`notes/2026-08-15-conventions-and-hazards.md` item 2, "witness" already carries
three unrelated senses in this corpus: the *cap witness* of the clean-pair
descent, the *SAT template witness* of the support programme, and the legacy
`N = 8` sense of a site with `C_{u,r} = 0`. The sites `y_0, y_1, y_2` of
Lemma 3.4 are a **fourth**, unrelated object. They are called **B2 witness
sites** throughout, never plain "witnesses", and no statement here should be
matched against any of the other three senses. The word "clean" — which carries
its own three senses (ledger item 1: *slice-clean*, *word-clean*, *cut-clean*) —
does not occur in this document at all.

## 2. The exactness system and its level

### 2.1 Off-count and the levels `X_k`

For a word `w` write `off(w) = N - max_c |w^{-1}(c)|`, the number of sites
outside the largest colour class; `off(w) = 0` exactly for constant `w`. The
**level-`k` system** `X_k` imposes

* `Phi(c^N) != 0` for `c = 0, 1, 2`, and
* `Phi(w) = 0` for every mixed `w` with `off(w) <= k`,

and nothing else. So `X_0 ⊂ X_1 ⊂ ... `, and the full exactness system is
`X_{N}` — in the amplitude-nonzero form of Theorem 1.2 throughout. A
block-diagonal weighting satisfying `X_k` is called *`X_k`-feasible*.

**Lemma 2.1 (parity).** If some colour class of `w` has odd size then
`Phi(w) = 0` identically. *Proof.* The corresponding hafnian in (2) is a sum
over perfect matchings of an odd set, of which there are none. `∎`

So only words whose three colour classes all have even size carry any content.

**Lemma 2.2 (word bookkeeping at `N = 8`).** Of the `3^8 = 6561` words on eight
sites, `3` are constant, `4920` have a colour class of odd size (and are
vacuous by Lemma 2.1), and `1638` are mixed with all classes even. Their
off-counts are `2` (168 words) and `4` (1470 words).

*Source.* `computations/unaudited-audit-a9-2026-08-20/results_a9_07_book.json`,
key `B1_word_bookkeeping`: `n_words 6561`, `constant 3`, `odd_part 4920`,
`mixed_even 1638`, `offcount_histogram {2: 168, 4: 1470}`. Independently:
`3 * C(8,2) * 2 = 168` words of profile `(6,2,0)` up to order, and
`3 * C(8,4) = 210` of profile `(4,4,0)` plus
`3 * C(8,4) * C(4,2) = 1260` of profile `(4,2,2)`, totalling `1470`.

**Lemma 2.3 (`EXACT = X_4` at `N = 8`).** At `N = 8` the ordered even profiles
of a mixed word are `(6,2,0)`, `(4,4,0)`, `(4,2,2)` up to reordering; their
largest parts are `6, 4, 4`, so their off-counts are `2, 4, 4`. Hence every
content-carrying exactness row has `off <= 4`, and

```
    X_4  =  EXACT   at   N = 8   for block-diagonal weightings.
```

*Sources.* `computations/unaudited-audit-a9-2026-08-20/results_a9_01_basics.json`,
key `p4_profiles.n8`: `n_even_profiles 15`, `mixed_offcounts [2, 4]`,
`max_offcount 4`, `EXACT_equals_X 4`, and the flag `N8_EXACT_IS_X4: true`. The
machine confirmation that the level filter drops nothing is
`results_a9_07_book.json`, key `B1_word_bookkeeping`:
`A2_rows_k4 1638`, `A2_rows_kNone 1638`, `A2_k4_equals_kNone true`,
`A2_k4_equals_words true` — the `k = 4` clause set and the unfiltered clause set
are the same set, and both equal the set re-derived from the raw 6561-word
enumeration. The same table gives `EXACT_equals_X 4` at `N = 6` and — the fact
that closes off the uniformity claim — `EXACT_equals_X 6` at `N = 10` and
`8` at `N = 12`.

The whole proof below therefore works at level `k = 4`, and at `N = 8` that
loses nothing.

### 2.2 The one lemma that diagonality buys

Everything downstream rests on (2): the amplitude of a word is a *product* of
three independent hafnians. Two consequences are used constantly.

* A mixed exactness row is a statement that a product of three hafnians
  vanishes; over a field, some factor vanishes.
* A constant row is a statement that a single hafnian is nonzero.

For a general bicoloured weighting neither holds, which is exactly why nothing
here transfers to the open case.

## 3. The free-set-triple normal form

This section is stated for a general even `N`; only Theorem 3.5 is used later,
and only at `N = 8`. Fix a block-diagonal weighting satisfying `X_4` — at
`N = 8` that is full exactness, by Lemma 2.3. Choose a **solve site** `z` and
put `V' = V - z` (so `|V'| = N - 1 = 7` at `N = 8`). Write

```
    x^c_y  :=  t^c_{zy}  =  haf( t^c | {z, y} )        for y in V',
    h_c(y) :=  haf( t^c | V' - y ).
```

### 3.1 The free set (W28-FREE)

For a colour `c`, the words whose `c`-class is `{z, y}` are indexed by the even
splits `V' - y = S_1 ⊔ S_2` of the remaining six sites between the other two
colours `d, e`. Their amplitudes are `x^c_y · haf(t^d|S_1) · haf(t^e|S_2)`, and
each such word is mixed with all classes even, so its amplitude vanishes.

**Definition 3.1.** The **free set** of colour `c` at `z` is

```
    F_c = { y in V' :  haf(t^d|S_1) haf(t^e|S_2) = 0
                       for every even split V' - y = S_1 ⊔ S_2 }.
```

**Lemma 3.2 (support).** `x^c_y = 0` for every `y in V' - F_c`.
*Proof.* If `y ∉ F_c` some split has `haf(t^d|S_1) haf(t^e|S_2) != 0`; the
corresponding exactness row reads
`x^c_y · haf(t^d|S_1) · haf(t^e|S_2) = 0`, and `F` has no zero divisors. `∎`

### 3.2 B1 and B2

**Lemma 3.3 (W29-B1).** If `y in F_c` then `haf(t^d | V' - y) = 0` for **both**
`d != c`.
*Proof.* Take the split `(S_1, S_2) = (V' - y, empty)` in Definition 3.1:
`haf(t^d|V' - y) · haf(t^e|empty) = haf(t^d|V' - y) · 1 = 0`. The split
`(empty, V' - y)` gives the statement for `e`. `∎`

**Lemma 3.4 (W29-B2: the B2 witness triple; see Remark 1.6).** There exist sites
`y_0, y_1, y_2 in V'`, pairwise **distinct**, with

```
    x^c_{y_c} != 0     and     h_c(y_c) != 0     for c = 0, 1, 2,
```

and moreover `F_c ⊆ {y_c} ∪ Q` where `Q = V' - {y_0, y_1, y_2}`, `|Q| = N - 4`.

*Proof.* Laplace expansion of the constant-`c` amplitude at the site `z`:

```
    Phi(c^N) = haf(t^c|V) = sum_{y in V'} t^c_{zy} · haf(t^c|V' - y)
                          = sum_{y in V'} x^c_y · h_c(y).
```

By hypothesis `Phi(c^N) != 0`, so some term is nonzero: pick `y_c` with
`x^c_{y_c} != 0` and `h_c(y_c) != 0`. By Lemma 3.2, `y_c in F_c`.

Now let `d != c`. If `y_c` were in `F_d`, Lemma 3.3 applied to `F_d` would give
`haf(t^c | V' - y_c) = h_c(y_c) = 0`, contradicting the choice of `y_c`. Hence
`y_c ∉ F_d` for every `d != c`. Since `y_d in F_d`, this forces `y_c != y_d`,
so the three B2 witness sites are distinct; and it says exactly that
`F_c ∩ {y_0,y_1,y_2} = {y_c}`, i.e. `F_c ⊆ {y_c} ∪ Q`. `∎`

Note that Lemma 3.4 is where the amplitude-nonzero strengthening enters and
where it is *sufficient*: the proof uses `Phi(c^N) != 0`, never `= 1`.

### 3.3 The normal form and the case ledger

The block-diagonal family is invariant under relabelling sites (the full `S_N`)
and under permuting the three colours (`S_3`, which permutes the constant
words among themselves). The solve site `z` was arbitrary, so relabel it to
`N - 1`; the stabiliser of `z` in `S_N` is the full symmetric group `S_{V'}`,
which acts transitively on ordered triples of distinct elements of `V'`, so
relabel `(y_0, y_1, y_2)` to `(0, 1, 2)`. We obtain:

**Theorem 3.5 (free-set-triple normal form).** Every `X_4`-feasible
block-diagonal weighting of `K_N` may be relabelled so that

```
    z = N - 1,   (y_0, y_1, y_2) = (0, 1, 2),   Q = {3, ..., N - 2},
    F_c = {c} ∪ R_c    with    R_c ⊆ Q .
```

The **case** of the weighting is the triple `(R_0, R_1, R_2)`. There are
`(2^{|Q|})^3 = 8^{N-4}` cases; at `N = 8`, `|Q| = 4` and there are
`16^3 = 4096` cases.

## 4. The case census

**Proposition 4.1 (case counts, two independent routes).**

| `N` | `\|Q\|` | cases `8^{\|Q\|}` | orbits under `S_Q x S_3` |
|---|---|---|---|
| 4  | 0 | 1 | 1 |
| 6  | 2 | 64 | 13 |
| 8  | 4 | 4,096 | **87** |
| 10 | 6 | 262,144 | 386 |
| 12 | 8 | 16,777,216 | 1,324 |

Route (a) is canonical enumeration: walk the cases, close each under the whole
group, keep one representative and the orbit size. Route (b) is Burnside's
lemma applied to the description of a case as a function `f : Q -> 2^{[3]}`,
`f(q) = {c : q in R_c}`, with `S_Q` acting on the domain and `S_3` on the
codomain:

```
    #orbits = 1/(|Q|! · 6) · sum_{sigma in S_Q, pi in S_3}
                prod_{cycles of length l in sigma} 2^{#cycles(pi^l)} .
```

*Sources.* `computations/unaudited-audit-a9-2026-08-20/results_a9_02_orbits.json`:
each row carries `burnside_orbits`, `burnside_remainder 0`, and for
`|Q| <= 4` also `brute_orbits`, `orbit_size_sum` (which equals `8^{|Q|}`) and
`AGREE: true`. The same file records `w29_case_orbit_reps_N8`:
`n_orbits 87`, `size_sum 4096` — the theorem lane's own orbit routine
(`computations/unaudited-diagclose-w29-2026-08-19/w29_t1i.py`,
`case_orbit_reps`), agreeing with both audit routes
(`N8_orbit_counts_match: true`). Regenerated in this package by
`certified_package/orbit_ledger.py`, which prints both routes and refuses to
proceed unless they agree.

**Remark 4.2 (the orbit reduction is a convenience, not a dependency).** The
lane W28 had previously found that an orbit reduction on a *different* stratum
would have been unsound, because "the colour action moves the systems"
(`notes/2026-08-15-resolution-master-plan.md`, v44 addendum). Here the
reduction is sound — relabelling `Q` fixes `z` and the `y_c`, and a colour
permutation followed by the matching relabelling of `{0,1,2} ⊂ V'` carries the
case `(R_0,R_1,R_2)` to `(R_{pi^{-1}(0)}, R_{pi^{-1}(1)}, R_{pi^{-1}(2)})` —
but the `N = 8` verdict does not rest on it: the refutation was run **both** on
all 4,096 cases and on the 87 orbit representatives, with identical outcome
(Section 6). Only the shipped replay uses the 87.

## 5. The vanishing-pattern abstraction

For a fixed case, introduce one Boolean per hafnian:

```
    p(c, S)   ==   "haf(t^c | S) != 0"        (c in {0,1,2}, S ⊆ V, |S| even)
```

together with auxiliary Booleans `g(c, S, w, u)` for the Laplace clauses. Every
clause family below is a **one-line implication valid at every point of every
case over every field**. Nothing forces a hafnian to be nonzero from support
information, so **cancellation is fully allowed**: an assignment in which a
hafnian vanishes although all its edges are nonzero is not excluded by the
encoding. Consequently the abstraction is a *relaxation*, and

```
    UNSAT  =>  the case has no point over any field, in any characteristic.
```

`SAT` is never read as a realisation.

The polarity above is the audit encoder's
(`computations/unaudited-audit-a9-2026-08-20/a9_enc.py`); the theorem lane's
encoder (`computations/unaudited-diagclose-w29-2026-08-19/w29_van.py`) uses the
opposite convention `z(c,S) == "haf(t^c|S) = 0"`, deliberately, so that a sign
slip in either encoder shows up as a disagreement (Section 8.2).

### 5.1 The clause families and their soundness

The encoder names **nine** families — `A0 A1 A2 A3 C0 Cnz Ch FR XF`, exactly
the `use` tuple of
`computations/unaudited-audit-a9-2026-08-20/a9_enc.py`. The lane reports say
"eight clause families", grouping the three case-hypothesis families
(`C0`, `Cnz`, `Ch`) differently; the content is identical, and the enumeration
below is the encoder's.

**A0** — `p(c, empty)`, for each `c`.
*Sound:* `haf(t^c | empty) = 1 != 0`.

**A1** — `p(c, V)`, for each `c`.
*Sound:* this is the hypothesis `Phi(c^N) != 0` of Theorem 1.2. **This is the
only place the constant rows are used, and only their nonvanishing.**

**A2** — `¬p(0, S_0) ∨ ¬p(1, S_1) ∨ ¬p(2, S_2)` for every ordered partition
`V = S_0 ⊔ S_1 ⊔ S_2` into even parts with `max_c |S_c| != N` and
`off <= k`. (Empty parts contribute no literal, by A0.)
*Sound:* by (2) the amplitude of the corresponding mixed word is the product of
the three hafnians and vanishes; a field has no zero divisors, so one factor
is `0`.

**A3 (Laplace)** — for each `c`, each even `S` with `|S| >= 4`, and each
`w in S`:

```
    ¬p(c, S)  ∨  OR_{u in S - w}  g(c, S, w, u),
    ¬g(c,S,w,u) ∨ p(c, {w,u}),        ¬g(c,S,w,u) ∨ p(c, S - w - u).
```

*Sound:* `haf(t^c|S) = sum_{u in S - w} t^c_{wu} · haf(t^c | S - w - u)`, an
identity. If every term has a vanishing factor — `t^c_{wu} = haf(t^c|{w,u}) = 0`
or `haf(t^c|S-w-u) = 0` — then the sum is `0`, i.e. `¬p(c,S)`. Note this is
*strictly stronger* than "some perfect matching of `S` survives", because it is
stated on the abstract Booleans of the smaller sets, which cancellation may
switch on or off freely.

**C0 (free support)** — `¬p(c, {z, y})` for every `y in V' - F_c`.
*Sound:* Lemma 3.2, using the case hypothesis that `F_c = {y_c} ∪ R_c`.

**Cnz (B2 witness support)** — `p(c, {z, y_c})`.
*Sound:* Lemma 3.4, `x^c_{y_c} != 0`.

**Ch (B2 witness cofactor)** — `p(c, V - z - y_c)`.
*Sound:* Lemma 3.4, `h_c(y_c) != 0`.

**FR (free rows)** — `¬p(d, S_1) ∨ ¬p(e, S_2)` for each `c`, each `y in F_c`
and each even split `V' - y = S_1 ⊔ S_2` with `off <= k`.
*Sound:* this is Definition 3.1 read forwards: the case *hypothesises*
`y in F_c`, and membership in `F_c` says precisely that
`haf(t^d|S_1) haf(t^e|S_2) = 0`; the field has no zero divisors. The case ledger
of Theorem 3.5 is exhaustive, so hypothesising the free sets is a complete case
split, not an assumption.

**XF (excess-free biconditional)** — for each `c` and each odd
`S_0 ⊆ V'` with `S_0 ∩ F_c = {y_c}`:

```
    p(c, S_0 ∪ {z})   <->   p(c, S_0 - y_c) .
```

*Sound:* Laplace at `z` inside the class `S_0 ∪ {z}` gives
`haf(t^c | S_0 ∪ {z}) = sum_{y in S_0} x^c_y · haf(t^c | S_0 - y)`. By
Lemma 3.2 every term with `y ∉ F_c` drops, and by hypothesis the only `y in S_0`
that survives is `y_c`. So

```
    haf(t^c | S_0 ∪ {z})  =  x^c_{y_c} · haf(t^c | S_0 - y_c),
```

a single product with `x^c_{y_c} != 0` (Lemma 3.4). Hence the two sides vanish
together — the biconditional, not merely one implication. The licence for the
`<-` direction is exactly `x^c_{y_c} != 0`, which comes from the *true point*
via B2, not from the abstraction.

**Remark 5.1 (`FR` rows are exactness rows).** Every `FR` row is the amplitude
of a genuine mixed all-even word — colour `c` on `{z, y}`, `d` on `S_1`, `e` on
`S_2` — so `FR` adds no hypothesis beyond `X_4`; it is a *rearranged* subset of
the same system. Machine check:
`computations/unaudited-audit-a9-2026-08-20/results_a9_07_book.json`, key
`B2_free_rows`: `free_rows 480`, `malformed 0` (checked on the maximal case
`R_c = Q` for all `c`, where `|F_c| = 5`; `3 · 5 · 32 = 480`, `32` being the
even splits of a six-set).

**Remark 5.2 (level filtering is a relaxation).** Restricting `A2` and `FR` to
rows with `off <= k` imposes *fewer* consequences and so cannot manufacture
UNSAT. At `N = 8`, `k = 4` in fact drops nothing (Lemma 2.3, and
`A2_k4_equals_kNone: true` above; every `FR` row at `N = 8` has
`off in {2,4}` by construction).

### 5.2 The abstraction really does allow cancellation

Two independent checks, structural and operational.

*Structural.* Every positive `p`-literal in the encoding sits in a clause that
also carries a negative literal (i.e. it is the conclusion of an implication
*from* a nonvanishing), except for the four licensed unit clauses `A0`, `A1`,
`Cnz`, `Ch` — respectively the definition `haf(t^c|empty) = 1`, the hypothesis
`Phi(c^N) != 0` of Theorem 1.2, and the two conclusions of Lemma 3.4. Nothing
else in the encoding asserts a hafnian to be nonzero.
Machine check: `results_a9_07_book.json`, key `B3_polarity`,
`unconditional_positive_clauses: []`, `PASS: true`. The same key records the
clause census for the case `R = ((3,4), (5,), ())`:

```
    A0 3 | A1 3 | A2 1638 | A3 1368 | A3g 10416 | C0 15 | Cnz 3 | Ch 3
    | FR 192 | XF 112
```

*Operational.* The abstraction admits models in which a 4-set hafnian vanishes
although all six of its edges are nonzero — the vanishing pattern of a genuinely
cancelling point. Machine check: same file, key `B4_cancellation`,
`k3_R(3, 4, 5, 6): true`, `k3_R(): true`, `PASS: true`.

## 6. The refutation, and its proof-checking chain

### 6.1 The verdicts at `N = 8`

**Theorem 6.1.** At `N = 8`, level `k = 4`, the abstraction of Section 5 is
UNSAT in **every** one of the 4,096 cases, and in every one of the 87 orbit
representatives.

*Sources.* `computations/unaudited-audit-a9-2026-08-20/results_a9_03_sat.json`,
key `n8k4`: `orbits {n_cases 87, n_sat 0, n_unsat 87, secs 2.8}`,
`all {n_cases 4096, n_sat 0, n_unsat 4096, secs 311.7}`,
`VERDICT_all_unsat: true`; first-case size `5592` variables, `13740` clauses.
The theorem lane reached the same verdict independently
(`computations/unaudited-diagclose-w29-2026-08-19/REPORT.md`: "N=8 k=4 UNSAT on
all 4096 cases AND all 87 orbits (run twice)").

*Proof of Theorem 1.2 from Theorem 6.1.* Suppose a block-diagonal weighting of
`K_8` over a field `F` satisfies the hypotheses of Theorem 1.2. By Lemma 2.3 it
satisfies `X_4`. By Theorem 3.5 it may be relabelled into the normal form, and
it then belongs to exactly one of the 4,096 cases. Every clause of that case's
formula is valid at the point (Section 5.1), so the assignment
`p(c,S) := [ haf(t^c|S) != 0 ]`, `g(c,S,w,u) := [ t^c_{wu} != 0 and
haf(t^c|S-w-u) != 0 ]` satisfies the formula. That contradicts Theorem 6.1. `∎`

### 6.2 Five solvers

All 87 orbit formulas were re-solved by five independent engines, all reporting
UNSAT on all 87: `cadical195` (7.3 s), `minisat22` (5.6 s), `glucose42`
(6.4 s), `maplesat` (7.3 s), `lingeling` (12.0 s). Source:
`results_a9_03_sat.json`, key `multi`.

### 6.3 Proof checking

*Own RUP checker (theorem lane).* W29 wrote its own RUP replayer and used it on
the extracted cores and on every orbit:
`computations/unaudited-diagclose-w29-2026-08-19/results_d3_rup_singleton.json`
(`core`: `n_lemmas 1668`, `all_lemmas_RUP true`, `empty_clause_derived true`,
`VERIFIED_UNSAT true`; `full`: `n_lemmas 702`, likewise), together with
`results_d4_rupall_n8.json` (all 87 orbits) and `results_d4_rupall_n6.json`.
The checker itself was calibrated on accept/reject/**truncation** controls —
the ledger-item-5 hazard — and one unit-seeding bug was found and fixed in the
process (`computations/unaudited-diagclose-w29-2026-08-19/REPORT.md`).

*Third-party drat-trim (audit lane).* Every orbit formula was re-solved by an
external CaDiCaL emitting a solver-native DRAT proof, and each proof verified by
Marijn Heule's `drat-trim`, required to print the literal string
`s VERIFIED`. Source:
`computations/unaudited-audit-a9-2026-08-20/results_a9_06_drat.json`:

```
    n8_k4_orbits : n_cases 87, unsat 87, verified 87, failures []   PASS
    n6_k4_all    : n_cases 64, unsat 64, verified 64, failures []   PASS
```

*Proof-checker controls (ledger item 5).* A checker that verifies anything is
worthless, so three deliberately broken proofs were submitted and had to be
**rejected**, and one satisfiable instance had to come back SAT. Same file, key
`controls`: `base_verdict UNSAT`, `base_verified true`, `proof_lines 13831`,
`truncated_verified false`, `corrupted_verified false`,
`crosscase_verified false`, `k3_verdict SAT`, `PASS true`.

*Reproduced in this package.* `certified_package/replay.sh` re-ran the whole
chain at the staged HEAD: controls PASS (`proof_lines 13831`, all three broken
proofs rejected, `k3_verdict SAT`), `87/87` UNSAT and `87/87` drat-trim
`s VERIFIED` in 7.1 s, `64/64` at `N = 6` in 2.6 s; and the regenerated CNFs are
**byte-identical** to the audit lane's stored files (SHA-256 spot-checked on
orbits 0–4). See `certified_package/replay_results.json` and
`certified_package/replay_log.txt`.

### 6.4 Which clauses do the work

Adding the families in order, on the 87 orbit representatives:

| formula | orbits SAT |
|---|---|
| CASE only (`A0 A1 A2 A3 C0 Cnz Ch`) | 87 / 87 |
| CASE + `FR` | 54 / 87 |
| CASE + `FR` + `XF` (the full formula) | **0 / 87** |

Drop-one analysis on the full formula (an entry `> 0` means the family is
load-bearing on at least that many orbits):

| dropped | orbits SAT |
|---|---|
| `A0` | 0 |
| `A1` | 28 |
| `A2` | 87 |
| `A3` | 87 |
| `C0` | 0 |
| `Cnz` | 0 |
| `Ch` | 2 |
| `FR` | 55 |
| `XF` | 54 |

Source: `results_a9_03_sat.json`, key `ablate`. Two readings. First, the kill
is a genuine three-way interaction: neither the case hypothesis alone nor the
case plus the free rows suffices; the `XF` biconditional is what closes it.
Second, `A0`, `C0` and `Cnz` are *not* load-bearing at `N = 8` in the sense that
removing them leaves the formula UNSAT — they are cheap and sound and are kept
because they are needed at other orders and because their presence is what makes
the `XF` derivation legible.

No formula in the chain contains an empty clause at construction, so no case is
refuted by a bookkeeping accident (`a9_enc.py` asserts this for `FR`:
`assert cl, "empty FREE clause -- would be a kill"`).

### 6.5 Minimal unsatisfiable cores

The theorem lane extracted a group-level minimal core for the singleton case
`R = ((), (), ())`: **361 constraint groups / 1,226 clauses over 666 variables**,
with every group deletable-tested, composed of `A3 74`, `A2 174`, `CASEh 3`,
`CASE0 9`, `FREE 32`, `XF 69`
(`computations/unaudited-diagclose-w29-2026-08-19/results_d2_core2_singleton.json`;
a coarser earlier pass gave 158 groups / 11,991 clauses,
`results_d1_core_singleton.json`). The audit lane extracted clause-level cores
for three cases (`computations/unaudited-audit-a9-2026-08-20/results_a9_12.json`,
key `cores`): singleton `13740 -> 3568` clauses, full (`R_c = Q`)
`13932 -> 857`, mixed `13767 -> 3366`; all three `verdict UNSAT`,
`verified true`. **These cores are the hand-proof target; no hand proof exists
yet.** The shipped core artifacts are in `certified_package/cores/`.

**Frame of the minimality claims (hazard-ledger item 15).** The two core
statements above are minimal in *different frames* and are not comparable
numerically:

* the theorem lane's **361 groups / 1,226 clauses** is minimal at the level of
  *constraint groups* — a group is a whole clause family instance (one Laplace
  expansion, one partition row, one free row), and "minimal" means every
  remaining group was individually deletion-tested and found necessary, in the
  encoding of `w29_van.py` at case `R = ((), (), ())`;
* the audit lane's **3,568 / 857 / 3,366 clauses** are *clause-level* cores as
  reported by drat-trim on the `a9_enc.py` encoding of three named cases — an
  unsatisfiable subset, not a claim of clause-level minimality.

Neither statement is a claim about the *smallest possible* refutation of the
case in any other encoding, and neither is a claim about the algebraic system.

## 7. Small orders

### 7.1 `N = 6` closes the same way

At `N = 6`, `|Q| = 2`, there are 64 cases in 13 orbits, and `EXACT = X_4`
again (`results_a9_01_basics.json`, `p4_profiles.n6`). The abstraction is UNSAT
on all 64 cases and all 13 orbit representatives
(`results_a9_03_sat.json`, key `n6`: `k4_all {n_cases 64, n_sat 0, n_unsat 64}`,
`k4_orbits {n_cases 13, n_sat 0, n_unsat 13}`, `VERDICT_k4_all_unsat: true`;
sizes `726` variables, `1734` clauses), and every one of the 64 proofs is
drat-trim verified (`results_a9_06_drat.json`, `n6_k4_all`). This is a
re-derivation of something already committed: the six-site theorem
(`proofs/six-site-arbitrary-complex-obstruction.md`, Theorem 1.1) forbids an
exact ternary source on six sites with **arbitrary** complex endpoint-ordered
matrices, of which the block-diagonal ones are a special case. It is reported
here not as a new result but as the **calibration of the machine on a case
whose answer is independently known** — the strongest kind of positive control
available short of `N = 4`.

### 7.2 Gröbner corroboration at `N = 6`

The same case ideals were built algebraically — generators
`FREE`, `XFREE`, `MIXED`, `CONST`, `NORM`/`RAB` as in
`computations/unaudited-diagclose-w29-2026-08-19/w29_t1i.py` — and decided by
Gröbner basis in Singular. All **13 of 13** case ideals are the unit ideal
(`dim = -1`) in **five characteristics**: `0, 2, 3, 7, 32003`. Source:
`computations/unaudited-audit-a9-2026-08-20/results_a9_09_n10.json`, key
`n6_all_13_groebner`: `n_orbits 13`, `not_unit []`, `PASS true`, with the
per-case generator counts (90 to 210 generators). The theorem lane ran the same
computation independently, on its own generators, in **four** characteristics —
`0`, `32003`, `32029`, `1000003`, the last two both `1 mod 3` per hazard-ledger
item 19 — with `13/13` unit and `n_not_unit 0`
(`computations/unaudited-diagclose-w29-2026-08-19/results_c5_caseideal_n6.json`,
whose `VERDICT` field reads: "ALL CASES UNIT -- no diagonal exact source at N=6,
by Groebner, independently of the SAT abstraction").

This is an *algebraically independent* confirmation: it decides the actual
polynomial system, not a Boolean relaxation of it.

**Honest limitation.** The Gröbner route uses the torus normalisation
`h_c(y_c) = 1` in place of a Rabinowitsch relation, which is licensed over an
algebraically closed field (a cube root is needed and is available there in
every characteristic; see the docstring of `Case` in `w29_t1i.py`). The SAT
route of Sections 5–6 uses no such normalisation and needs no closure — which is
why Theorem 1.2 is stated over *any* field, and the Gröbner run is corroboration
rather than the proof of record.

**The `N = 8` Gröbner corroboration does not exist.** The single `N = 8` case
ideal attempted (the maximal case, `81` variables, `1932` generators) **timed
out** at 3000 s in char 32003 with no verdict
(`computations/unaudited-diagclose-w29-2026-08-19/results_c5_caseideal_n8.json`:
`error: ... timed out after 3000 seconds`, `UNIT: false` meaning *no unit
verdict was obtained*, not that the ideal is non-unit). Per ledger practice a
stopped run carries no information. The `N = 8` result therefore rests on the
SAT chain alone, with `N = 4` and `N = 6` as the algebraically corroborated
calibration points.

### 7.3 `N = 4`: the machine correctly fails

At `N = 4` there is one case, and the abstraction is **SAT** at every level —
`k = 2` and unfiltered (`results_a9_03_sat.json`, key `n4`:
`MUST_BE_SAT: true`; `60` variables, `138` clauses). The Gröbner route agrees:
the `N = 4` case ideal is **not** unit, `dim 3`, in char 0 and char 32003
(`results_a9_08_t1h_gb.json`, key `link7_groebner_n6.n4_control`:
`isunit "0"`, `dim "3"`, `PASS true`). This is the decisive positive control:
the exceptional `K_4` source exists, and the machine does not kill it. A method
that refuted `N = 4` would be refuting something true.

Moreover the real `N = 4` exceptional source was pushed through the encoder
end-to-end at every solve site and every level, with **zero clause violations**
(`results_a9_04_controls.json`, key `p1`: `n_pms 3`, `exact_violations 0`, and
for each of the four solve sites at `k = 2` and unfiltered,
`B1_inside: true`, `n_violations 0`, `abstraction_SAT: true`, `PASS: true`).

## 8. Controls, mutation ledger, and independent confirmation

### 8.1 Hafnian engines

Three implementations of the hafnian exist in the chain: W28's recursion with a
value memo, W25's bitmask DP, and W29's explicit perfect-matching enumeration
(`computations/unaudited-diagclose-w29-2026-08-19/w29_core.py`). W29's
cross-check `check_haf_agreement` compares its engine against W28's on random
exact inputs over `Q` and over `Q(omega)`: **100/100 agreements**
(`computations/unaudited-diagclose-w29-2026-08-19/results_f1_controls.json`,
`haf_engine_disagreements: 0`). The audit lane wrote two more from scratch — a
bitmask-memoised Laplace recursion and a direct matching enumeration
(`computations/unaudited-audit-a9-2026-08-20/a9_haf.py`, routes `R1` and
`R2`) — and compared again: **60 trials, 0 disagreements**
(`results_a9_01_basics.json`, key `p1_engines`). Its third route `R3` is the
raw block-matrix matching sum used in §8.2.

### 8.2 The product formula, from scratch

The factorisation (2) was never assumed by the audit: it was checked against a
raw evaluation of definition (1), summing over all `105` perfect matchings of
`K_8` with full `3 x 3` blocks, on all `6561` words and `50` random
block-diagonal weightings of mixed density (0.35 / 0.7 / 1.0):
**0 disagreements** (`results_a9_01_basics.json`, key
`p2_product_formula`: `n_sources 50`, `n_words 6561`, `n_pm 105`,
`disagreements 0`, `PASS true`, `45.5 s`). A planted **non**-diagonal
perturbation makes the two disagree in all 6 trials (`p3_mutation_nondiagonal`:
`trials 6`, `fired 6`) — so the check discriminates.

### 8.3 Real `X_3` sources pass the encoder (the repaired control)

Real block-diagonal sources satisfying `X_3` do exist at `N = 8`, and every
clause of the `k = 3` encoding must hold at them. Two runs:

* **Theorem lane (W29), as originally reported and now qualified.** `150` real
  `X_3` sources, `1,200` site checks, `0` violations
  (`computations/unaudited-diagclose-w29-2026-08-19/results_g2_x3mass.json`:
  `objects 150`, `site_checks 1200`, `violations 0`, `PASS true`). **A9's
  correction:** all `1,200` of those checks land in the *single* case orbit
  `R = (Q, Q, Q)` — the same file records
  `cases_seen: {"[[3,4,5,6],[3,4,5,6],[3,4,5,6]]": 1200}`. As a control over
  the case ledger it is therefore one case, not 1,200 independent probes. The
  audit reproduced the same single-case clustering on its own generator
  (`results_a9_04_controls.json`, key `p2`: `objects 60`, `site_checks 480`,
  all 480 in `[[3,4,5,6],[3,4,5,6],[3,4,5,6]]`).
* **The replacement, with case spread.** A generator built to vary the free
  sets: `40` objects, `320` site checks across **37 distinct cases**, `0`
  violations, `0` normal-form failures
  (`results_a9_04_controls.json`, key `p3`: `distinct_cases 37`,
  `violations 0`, `normal_form_failures 0`, `PASS true`, with the per-case
  histogram in the file).

Both runs also confirm the normal form itself on real objects: `B1` and `B2`
hold at every checked site, and the derived `F_c` always sits inside
`{y_c} ∪ Q`.

### 8.4 Per-family validity at real points

Sampled directly against real sources
(`results_a9_04_controls.json`, key `p4`):

| family | checks | failures |
|---|---|---|
| `A3` Laplace | 337 | 0 |
| `XF` identity | 400 | 0 |
| `FR` support + `B1` + `B2` | 200 site checks | 0 support, 0 `B1`, 0 `B2` |

### 8.5 Mutation ledger

Seven deliberate breakages plus an unmutated baseline, each with the detector
that is supposed to catch it
(`computations/unaudited-audit-a9-2026-08-20/results_a9_05_mut.json`; the
detector rule is stated in `run_a9_05_mut.py`: "the detector for an UNSOUND
clause is always 'a REAL object violates it'; the detector for a MISSING
restriction is 'the verdict changes at a level where objects exist'"):

| mutation | detector fires |
|---|---|
| `MU0` baseline (unmutated) | 0 / 128 — **must not fire** |
| `MU1` flip `FR` polarity | 128 / 128 |
| `MU2` flip `A2` polarity | 128 / 128 |
| `MU3` free set too big | 26 / 26 |
| `MU4` wrong Laplace cofactor | 128 / 128 |
| `MU5` `XF` without the `y_c` deletion | 128 / 128 |
| `MU6` remove the `k`-filter at `k = 3` | verdict flips on all 4 probes: SAT with the filter, UNSAT without |
| `MU7` artefact detector: add bogus rows demanding `haf(t^c\|V) = 0` | `N = 4` correctly dies (`n4_still_sat: false`) — the pipeline is sensitive |

All eight entries pass (`PASS: true`). A ninth mutation `MU8` (drop `A1`) is
coded in `run_a9_05_mut.py` but was not recorded in the results file; its
content is covered by the drop-one row for `A1` in §6.4 (`28/87` SAT).

**Honest record of a repaired control.** The audit's *first* mutation battery
(`results_a9_04_controls.json`, key `p5`) reported `PASS: false`: two of its
five mutants were silent — `M1_flip_FREE_polarity` (`CAUGHT: false`, the
formula stayed UNSAT under the flip, so a *verdict-change* detector could not
see it) and `M3_wrong_case` (`fired 0/5`, because all five probe objects lay in
the maximal case, where shrinking `F_0` changed nothing). The audit did not
paper over this: it rebuilt the battery with the correct detector pairing and
with objects chosen to spread across cases, which is the `MU0`–`MU7` run above,
where the same two mutations fire `128/128` and `26/26`. The withdrawn `p5`
block remains in the lane record.

Further firing negatives on the theorem-lane side
(`computations/unaudited-diagclose-w29-2026-08-19/results_f1_controls.json`):
the hazard-ledger batteries for items 13 (Singular identifier shadowing),
6 (stdout `?` scan) and 22 (denominator guard) each fire when provoked
(`ledger13_shadow_guard_fires`, `ledger6_question_scan_fires`,
`ledger22_denominator_guard_fires`, all `true`).

### 8.6 Two independent encoders agree exactly

The audit encoder was written without importing anything from the theorem lane,
with a different variable layout (bitmask-keyed) and the **opposite polarity**.
Compared clause-set to clause-set after normalisation, on four cases spanning
the ledger:

| case | clauses (audit) | clauses (W29) | only in W29 | only in audit |
|---|---|---|---|---|
| `((), (), ())` | 13740 | 13740 | 0 | 0 |
| `((), (3,), (4,5,6))` | 13776 | 13776 | 0 | 0 |
| `((3,), (3,4), (3,4,5))` | 13790 | 13790 | 0 | 0 |
| `((3,4,5,6),)*3` | 13932 | 13932 | 0 | 0 |

and the verdicts agree on all 87 orbits (`agree 87`, `disagreements []`).
Source: `computations/unaudited-audit-a9-2026-08-20/results_a9_10_diff.json`.

### 8.7 The retired predecessor (W29-A1)

The route this theorem replaced was the "T1h" free-site ideal of lane W28, whose
Gröbner run had timed out. W29 proved that ideal is **not** the unit ideal, by
exhibiting an explicit 21-parameter rational family inside its variety: on 40
sampled points of the family **all 96 generators vanish**
(`computations/unaudited-audit-a9-2026-08-20/results_a9_08_t1h_gb.json`, key
`link6_T1h`: `points 40`, `nonzero_generators 0`, `n_generators 96`,
`rab_ok 38`, `PASS true`). The timeout was a *formulation* artefact: T1h kept
only the `|S_0| = 1` rows. The family is **not** a counterexample to
Theorem 1.2: its free sets are `F_0 = {0,3,4,5,6}`, `F_1 = {1,3,4,5,6}`,
`F_2 = {2,3,4,5,6}` — the maximal case `R_c = Q` — which the `k = 4` formula
kills (same file, `family_free_sets`). The retirement is therefore correct, and
is recorded in `notes/2026-08-15-resolution-master-plan.md`, v47 and v49.

## 9. Scope: what is proved, and what is open

1. **Block-diagonal only.** Theorem 1.2 covers `A_uv = diag(t^0,t^1,t^2)` —
   three independent weight functions, i.e. weights supported on `i = j`, the
   classical monochromatic-edge model. It strictly contains the single-cell
   edge-coloured reading (Corollary 1.3) and is strictly contained in the
   general bicoloured model, where `A_uv` is an arbitrary `3 x 3` matrix.
   **The general bicoloured `n = 8, d = 3` case is untouched**; the product structure (2) is precisely
   what diagonality buys and precisely what a general `A_uv` destroys. The
   sigma non-diagonal slice remains search-silent
   (`computations/unaudited-diagclose-w29-2026-08-19/REPORT.md`).
2. **`N = 6` and `N = 8` are closed. `N >= 10` is open for this machine.**
   The claim "uniform in even `N`" made in the theorem lane's first report
   (`computations/unaudited-diagclose-w29-2026-08-19/REPORT.md`, headline item
   3: "Uniform in even N; N=10 k=4 in flight ..., N=12 queued") and repeated in
   `notes/2026-08-15-resolution-master-plan.md` v47 is **WITHDRAWN**. The audit
   refuted it:
   * At `N = 10` the exact level is `X_6`, not `X_4`: the even profile
     `(4,4,2)` has off-count `6`
     (`results_a9_01_basics.json`, `p4_profiles.n10`: `mixed_offcounts
     [2,4,6]`, `EXACT_equals_X 6`; and `8` at `N = 12`). So an `N = 10` run at
     `k = 4` is a **strict relaxation** of exactness, not a decision of it.
   * That relaxation is mostly satisfiable anyway: `35` of `42` sampled orbits
     SAT at `k = 4` (`results_a9_09_n10.json`, key `n10_k4_spot`:
     `checked 42`, `n_sat 35`).
   * **Preliminary, in-flight sampling at the true level `k = 6` also found
     satisfiable orbits.** Of `7` orbits attempted, `2` came back SAT —
     including the singleton case `R = ((), (), ())` and the maximal case
     `R = (Q,Q,Q)` (`results_a9_12.json`, key `n10_k6`; instance sizes
     `35826` variables, `~92,500` clauses; individual solve times up to
     `3099 s`). **This sample is small and was still running when the audit
     closed** — A9's report lists it as "In flight at close ... sharpens the
     N=10 refutation only; cannot change gate items". It is reported as
     supporting evidence, not as a verdict on `N = 10`, and **the withdrawal
     in this section does not rest on it**: the withdrawal follows from the
     level computation alone, which is a proof and not a sample.
   * The `k = 3` calibration at `N = 10` behaves as it must: `386/386` orbits
     SAT (`results_a9_09_n10.json`, key `n10_k3`), and real `X_3` objects at
     `N = 10` pass the encoder with `0` violations (key `n10_x3_objects`:
     `objects 6`, `site_checks 60`, `violations 0`).

   The honest statement is therefore: **the Boolean abstraction of Section 5 is
   strong enough to decide `N = 6` and `N = 8` and is demonstrably *not* strong
   enough at `N = 10`.** Whatever closes `N >= 10` needs strictly more than
   these nine clause families. The `N = 12` case was never run.
3. **The `N = 8` verdict is SAT-based.** Its algebraic corroboration exists at
   `N = 4` and `N = 6` only (Section 7.2); the `N = 8` Gröbner attempt timed
   out and carries no information.
4. **No hand proof.** The minimal cores of Section 6.5 (361 groups / 1,226
   clauses, or 857 clauses at the clause level in the maximal case) are the
   target for a human-readable argument. None exists yet.
5. **What this does *not* say about the conjecture.** Krenn–Gu at `n = 8,
   d = 3` in the general bicoloured model is not closed by this theorem, and
   nothing here is a positive closure of any part of the conjecture. It removes
   the block-diagonal stratum at the smallest open order — the order stays
   open, one stratum of it does not.

   In particular, **the `formal-conjectures` registry item
   `eqSystem8_no_solution_d3` is not resolved by this theorem.** That item is
   the general bicoloured statement (its Lean edge type carries both endpoint
   colour indices; §11), it remains open, and it remains this programme's
   target. Theorem 1.2 is its diagonal sub-case.

## 10. Verification status and replay

### 10.1 Provenance

| lane | role | directory | pinned HEAD |
|---|---|---|---|
| **W28** | the predecessor: symmetric case, the `DEC`/`FREE` reduction | `computations/unaudited-x4empty-w28-2026-08-18/` | — |
| **A8** | independent audit of W28 and of the diagonal chain | `computations/unaudited-audit-a8-2026-08-19/` | `0016ec56` |
| **W29** | the theorem lane: normal form, abstraction, refutation | `computations/unaudited-diagclose-w29-2026-08-19/` | `0016ec56a6f72d51391f67354f287ca6eb6febb2` |
| **A9** | the promotion-gate audit of W29-T1 | `computations/unaudited-audit-a9-2026-08-20/` | `10eeae24d29ad6b4b64d9a30810a0e3b318b2e86` |
| **P2-diag** | this write-up and the replay package | `computations/unaudited-promotion-diag-2026-08-20/` | `5377acdc43992e8eaaf4f17f4f1068b7242dfe73` |

**A9's verdict**, verbatim from
`computations/unaudited-audit-a9-2026-08-20/REPORT.md`:

> **W29-T1 CONFIRMED — and slightly stronger than stated. Committable
> as spine.** Independently re-derived, re-encoded (inverted polarity,
> own layout), re-solved by 5 engines, drat-trim proof-checked
> (87/87 + 64/64 s VERIFIED).

and its recommendation:

> COMMIT as spine with three repairs in the write-up: (i) strike
> uniform-in-N / N=10 / N=12 claims; (ii) qualify the 1,200-check
> control as single-case, cite the 37-case replacement; (iii) state
> block-diagonal scope + the amplitude-nonzero strengthening.
> Nothing in the proof chain itself needs repair.

All three repairs are discharged here: (i) Section 9.2 and Remark 1.4;
(ii) Section 8.3; (iii) Theorem 1.2, Corollary 1.3, Remark 1.4, Section 2.2.

**A8's relevant verdict**, verbatim from
`computations/unaudited-audit-a8-2026-08-19/REPORT-FINAL.md`:

> => **W28-T1's computational core CONFIRMED AT FULL SCALE** on an
> independent implementation (previously only 15 sampled cases).

and, on the route this theorem replaced:

> NOTE (manager): A8's framing
> "T1h in char 0 is the one computation that would commit the
> diagonal chain" is superseded — W29-A1 proved the T1h ideal is NOT
> unit (explicit 21-parameter family; formulation artifact), and the
> diagonal theorem now rides on W29-T1's normal-form route, gated by
> audit A9.

A8 also recorded that its missing-profile repair item for W28's sweep — the
size profiles `(5,6,6)` and `(6,6,6)`, never run — is **subsumed** by this
theorem, whose abstraction covers the cancellation stratum entirely
(`computations/unaudited-diagclose-w29-2026-08-19/REPORT.md`, closing paragraph:
"A8's missing-profile repair item for W28's sweep is SUBSUMED by this theorem
(cancellation fully covered)."; also
`notes/2026-08-15-resolution-master-plan.md`, v47 item 2).

### 10.2 Hazard-ledger items consumed

Against `notes/2026-08-15-conventions-and-hazards.md`:

* **Item 5 (pysat + cadical `get_proof()` silently truncates DRUP files).**
  Consumed and controlled. The proofs of record are **solver-native**: the
  external CaDiCaL binary writes the DRAT file itself, never `pysat`'s
  `get_proof()`. Truncation is tested explicitly — a proof truncated to half
  its length is **rejected** by drat-trim
  (`results_a9_06_drat.json`, `truncated_verified: false`), alongside a
  corrupted proof and a cross-case proof. The theorem lane's own RUP checker
  passes the same accept/reject/truncation battery, after one unit-seeding bug
  that the battery caught.
* **Item 16 (proof-system mismatch: RUP-only checkers reject legitimate DRAT
  proofs with RAT steps from lingeling inprocessing).** Consumed. The
  certificate chain of record pairs **CaDiCaL** with **drat-trim**, a
  DRAT-capable checker — the pairing the ledger prescribes. `lingeling`
  appears only in the five-solver *verdict* agreement of Section 6.2, where no
  proof file of its is consumed. The lane's own RUP checker is applied to
  CaDiCaL proofs only.
* **Item 19 (characteristic caveats: a single small field can produce false
  kills; use at least two primes with the relevant residues, or eliminate over
  `Q`).** Consumed in the corroboration layer: the `N = 6` Gröbner sweep runs
  **char 0** and four positive characteristics `2, 3, 7, 32003`, and the
  theorem lane's own sweep independently ran char 0 plus `32003`, `32029` and
  `1000003` (the last two `1 mod 3`). More
  fundamentally, the item does not bind the main argument at all: the Boolean
  abstraction is characteristic-free by construction (Section 5), so its UNSAT
  is not a single-field verdict but a statement over every field at once.
* **Item 13/6/11/14/22 (Singular hygiene).** Relevant only to the Gröbner
  corroboration. The no-shadowing guard (`zz*` prefixes), the stdout-`?` scan,
  and the denominator guard are implemented in `w29_core.run_singular` /
  `w29_t1i.emit` and all three fire when provoked
  (`results_f1_controls.json`, Section 8.5).
* **Item 18 (explicit-point controls for forcing verdicts must live outside
  the asserted locus) and item 20 (adversarial-builder control).** The `N = 4`
  SAT control (Section 7.3) is the outside-locus point of record: the machine
  is run at an order where the forbidden object *exists*, and does not kill it.
  The adversarial builder assigned to build the forbidden object at `N = 6/8`
  was calibrated at `N = 4` (3 hits at `1.1e-16`) and stayed silent at
  `N = 6/8` (`computations/unaudited-diagclose-w29-2026-08-19/REPORT.md`); it
  was stopped as moot on A9's verdict
  (`notes/2026-08-15-resolution-master-plan.md`, v50).
* **Item 21 (control files must fail loudly if a control never runs).**
  Consumed: the withdrawn `p5` mutation block of Section 8.5 is exactly a
  control failing loudly, and being replaced rather than hidden.

### 10.3 Replay

```text
computations/certificates/n8_diagonal/replay.sh
computations/certificates/n8_diagonal/replay.sh --smoke
computations/certificates/n8_diagonal/replay.sh --verify-only
```

The default run reproduces the case ledger by both routes, runs the
broken-proof controls, then regenerates, solves and drat-trim-verifies all 87
`N = 8` orbit formulas and all 64 `N = 6` formulas. `--verify-only` re-checks
the 87 shipped CNF/DRAT pairs in place and validates `SHA256SUMS.txt`.

Exact tool builds used for every recorded run:

```text
CaDiCaL     computations/unaudited-hygiene-h1-2026-08-15/tools/cadical/build/cadical
            `cadical --version`  ->  3.0.1
drat-trim   computations/unaudited-hygiene-h1-2026-08-15/tools/drat-trim/drat-trim
            invoked as `drat-trim CNF DRAT -f`; required to print `s VERIFIED`
Python      3.13.12 (stdlib only for the replay driver)
```

Both are overridable through the `CADICAL` and `DRATTRIM` environment
variables. The five-engine agreement of Section 6.2 additionally needs the
`python-sat` package and is *not* part of the replay.

### 10.4 Status labels

| statement | status |
|---|---|
| Theorem 1.2 (`N = 8`, block-diagonal, any field, amplitudes nonzero) | **[P]** — proved; machine-checked certificates; two independent audits (A8 upstream, A9 at the gate) |
| Corollary 1.3 (classical edge-coloured Krenn–Gu at `N = 8`) | **[P]** — immediate specialisation |
| `N = 6` closure by the same machine | **[P]** — SAT chain plus `13/13` unit case ideals in five characteristics |
| `N = 4` non-closure (positive control) | **[P]** — SAT, and `dim 3` non-unit ideal |
| `N = 8` Gröbner corroboration | **[O]** — attempted, timed out, no verdict |
| Hand proof from the minimal core | **[O]** |
| `N >= 10` for this machine | **[O]** — and *refuted* as an immediate consequence of these clause families (Section 9.2) |
| General bicoloured `n = 8, d = 3` | **[O]** — untouched |

## 11. Related and concurrent work

The attribution below follows `README.md` and `references/REFERENCES.md`; no
novelty is claimed against any of it (hazard-ledger item 10).

* **I. Bogdanov's** matching-index theorem underlies the unweighted case: a
  graph on at least six vertices in which every perfect matching is
  monochromatic admits at most two colours on its edge set. The present theorem
  is about *complex-weighted* block-diagonal sources with arbitrary
  cancellation, which Bogdanov's argument does not cover; on the nonnegative /
  constructively-interfering stratum his theorem already gives the conclusion.
* **L. S. Chandran and R. Gajjala**, with co-authors, proved the sparse and
  bounded-degree cases (arXiv:2202.05562, arXiv:2407.00303) and, with
  **Illickan**, the conjecture for vertex connectivity at most `2` and
  unconditionally for maximum degree at most `3` — the latter already for
  complex weights and bicoloured multigraphs. Those results are incomparable
  with this one: they constrain the *graph*, this constrains the *matrix shape*.
* **DeepMind's AlphaProof Nexus** (arXiv:2605.22763) resolved the many-colour
  regime `n = d in {4, 6, 10}`; `eqSystem8_no_solution_d3` remains listed open
  in `formal-conjectures`.

  **This theorem does not close that registry item, and the distinction is
  exact rather than rhetorical.** Read against the Lean source
  (`google-deepmind/formal-conjectures`,
  `FormalConjectures/Paper/MonochromaticQuantumGraph.lean`), the registry's
  statement is the **general bicoloured** one: its edge type `EdgeN` carries
  *both* endpoint colour indices `i j : Fin D`, and the matching sum evaluates
  `W (mkEdge v u (ι v) (ι u))` — the weight depends on the colours at both
  endpoints — with the constant words normalised by `pmSum = 1`. Theorem 1.2
  is the **diagonal sub-case**: the weights supported on `i = j`, which is the
  classical monochromatic-edge model of Krenn's original formulation. So:

  | | |
  |---|---|
  | `eqSystem8_no_solution_d3` | general bicoloured at `n = 8, d = 3` — **open**, and the programme's remaining target |
  | Theorem 1.2 | its diagonal sub-case, at the same (smallest open) order — **proved here** |

  In one direction the comparison is favourable: the registry statement
  normalises the constant words to `1`, whereas Theorem 1.2 assumes only that
  the three constant amplitudes are **nonzero**, so on the diagonal sub-case
  this result covers the registry's normalisation *a fortiori*.

  A concrete consequence worth recording: the certificates shipped with this
  document would support a Lean pull request adding a **proved diagonal
  variant** statement to that file, in the registry's own idiom — the file
  already carries variant statements alongside the headline one (for instance
  `eqSystem8_no_solution_d3_trinary_int`), so a diagonal variant would be an
  addition in the established style, not a change to the open problem. That is
  a suggestion for future work, not a claim: no Lean development exists here.
* **algal's independent Lean 4 certificate for `(6,3)`**
  (`formal-conjectures` PR #4610): a complete formal proof of the normalized
  `(6,3)` fibre over `C`, developed concurrently and independently. This
  repository's six-site theorem
  (`proofs/six-site-arbitrary-complex-obstruction.md`) keeps the
  palette-uniform general statement, and the two censuses are genuinely
  different decompositions — corroboration, not duplication. The solver-free
  `D <= N-2` anchor lemma of PR #4661 subsumes both projects' forced-column
  lemmas and is the right citation for that step.
* A tensor-algebraic no-go theorem by **Krenn, Firsching, Tsoukalas, Gajjala,
  Gu, and Chaudhuri** is announced as in preparation.

For a reader arriving from the formal-conjectures side, the reference list
carried by `MonochromaticQuantumGraph.lean` itself is `Krenn2017`, `MO2018`,
`Gu2019`, `Krenn2019`, `Chandran2022`, `Chandran2024`. Everything cited above
is either in that list or is the concurrent work named in `README.md`;
`Krenn2017` is the origin of the monochromatic-edge (diagonal) model that
Theorem 1.2 refutes at `N = 8`.

Within this repository, the six-site theorem
(`proofs/six-site-arbitrary-complex-obstruction.md`) is the general-bicoloured
statement at `N = 6`; the present theorem is the block-diagonal statement at
`N = 8`. They are the two ends of the same programme's current reach, and the
gap between them — general bicoloured at `N = 8` — is the open case.

One internal overlap should be stated so Corollary 1.3 is not read as more reach
than it has. `notes/finite-obstruction.md` Corollary 7.2 already gives, for
every even `n >= 6` and with **no** diagonal or monomial hypothesis, that "no
collection of arbitrary aggregate matrices whose nonzero underlying support
graph is 3-regular can satisfy `Phi(A) = Delta`". At `N = 8` that is the
3-regular sub-case of Corollary 1.3, and it is the stronger statement there
(arbitrary matrices, not single cells). Corollary 1.3 adds the edge-coloured
sources of every *other* support degree at `N = 8`; it does not improve on
Corollary 7.2 where the two meet.
