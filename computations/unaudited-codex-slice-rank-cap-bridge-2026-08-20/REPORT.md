# Slice-rank to cap bridge audit

Status: **UNAUDITED exact local lemma and exact counterexample.**  No spine or
certified file was edited.  Only certified Sections 1--4 and 6--8 of
`proofs/slice-master-relations.md` were used; its gated delivery section was
not imported.

## Verdict

The proposed `3 x n` abstraction has one valid half and one false half.

> **Packet-rank lemma.**  Let the rows of a `3 x n` slice matrix be
> `s_0,s_1,s_2`.  If a matched X4 packet has a live singleton spike at colour
> `c`, cofactor vector `Q`, and live spike coefficient `U`, then
>
> ```text
> <s_a,Q> = <s_b,Q> = 0,       <s_c,Q> = -U != 0.
> ```
>
> Hence the slice has row-rank three.  Equivalently, the row-rank-at-most-two
> stratum is a Laurent-unit contradiction.

The proof is one line: if the rank were at most two, the spike row would lie
in the span of the two clean rows, whose pairing with `Q` is zero.

This recovers the `m=25` obstruction because its site-6 slice has only two
columns and therefore can never have row-rank three.  For `n>=3`, however,
the packet forces the complementary full-rank branch; it does **not** produce
a cap.  `Q` is an `n`-component neighbour-cofactor vector, while a physical
cap `K` has nine endpoint-pair coordinates.  The certified slice master
relations supply no map `Q -> K` and no implication from row-rank three to
the four carrier activity row-space tests.

An exact `m=26/F_13` construction shows that this missing implication is
real, not merely an absent proof: two live singleton packet triples vanish,
the `3 x 3` slice determinant is one, but every one of the 728 star/triangle
carrier criteria is blocked.

## 1. Independent re-audit of the five-row `m=25` certificate

The checker restates the raw 28 endpoint masks and rebuilds each word
polynomial with a fresh recursive subset-hafnian engine.  It does not import
the previous `m=25` script or a stored perfect-matching ledger.

For the mixed X4 generators

```text
00001000, 00001010, 00001020,
10200000, 10200010,
```

the independently expanded five-row identity again has zero residual and
right side

```text
x06_02 x07_10 x13_00^2 x25_00 x26_21 x45_00 x47_10 x56_00.
```

This is a Laurent unit on the 129-cell open support.  Transposing the raw
endpoint bit convention moves nine singleton cells, including the two
load-bearing spikes.  Thus the original `m=25` closure survives a genuinely
independent raw audit.

## 2. What changes for a `3 x n` packet

At a centre `v`, partition the raw word amplitude by the Gamma edge covering
`v`.  For a packet in which the only incident singleton firing is a target
cell at centre colour `c`, this is literally

```text
H_t = <s_t,Q> + delta_(t,c) U.
```

All three `H_t` are mixed X4 generators.  Their vanishing therefore gives the
packet-rank lemma above.  Notice two necessary corrections to the suggested
dichotomy:

1. The contradictory branch is **row-rank at most two**, meaning that all
   `3 x 3` minors vanish.  One deficient chosen minor is insufficient when
   `n=4`.  Over `F_13`, for example,

   ```text
   S = [1 1 1 10;
        1 1 2  9;
        1 1 1  1],       Q=(1,1,1,1)
   ```

   has minors `(0,0,4,4)` and packet pairings `(0,0,4)`: two minors vanish,
   row-rank remains three, and the spike packet is consistent.

2. Full row rank is an open slice condition, not a carrier condition.  The
   carrier matrix `L_C` consists of nine-cap-coordinate response rows, and
   activity additionally requires all four forms
   `K_00,K_11,K_22,<K,A_pq>` to remain nonzero on `ker L_C`.  None of these
   statements follows from the rank of `S`.

## 3. Exact packet census on the named testbeds

The finite census exhausts every centre, incident singleton target, and all
`3^7` assignments on the other sites.  It requires three mixed-X4 words,
the target as the only incident spike, a monomial nonzero spike cofactor, and
records the number of effective full-neighbour cofactor columns.

| support | two columns | three columns | four columns | packets | paired spike keys |
|---:|---:|---:|---:|---:|---:|
| `m=25` | 248 | 1,123 | 818 | 2,189 | 79 |
| `m=26` | 0 | 1,036 | 949 | 1,985 | 134 |
| `m=27` | 0 | 0 | 999 | 999 | 95 |
| `m=28` | 0 | 0 | 0 | 0 | 0 |

Thus `m=26` and `m=27` contain many honest higher-column packet entries, but
every such entry forces full row rank rather than a unit.  At `m=28` the
dense support gives no packet with a monomial spike cofactor under these
hypotheses; its singleton coefficient always has multiple live matchings or
the isolation conditions fail.

This census is template-specific.  The support fact that 27 pure-matching
charts possess an intersecting/coincident forced response occurrence does
not by itself supply two singleton spikes, monomial cofactors, or these X4
packet words.  A chart-to-packet entry lemma remains separate and unproved.

## 4. Raw `m=26/F_13` counterexample to full-rank-to-carrier

All 138 occupied cells of the `m=26` endpoint support are nonzero.  At centre
`6`, with neighbour colours `(w_3,w_5,w_7)=(0,0,0)`, the edge-`06` and
edge-`26` packet triples are

```text
00001000, 00001010, 00001020,
10200000, 10200010, 10200020.
```

All six raw hafnians vanish.  Their cofactor vectors and spike units are

```text
Q06=(8,8,12), U06=11,       Q26=(7,4,12), U26=11.
```

On columns `36,56,67`, the three slice rows are

```text
(1,3,6), (1,9,2), (1,10,8),       determinant = 1 mod 13.
```

For the natural cap pair `02` and response-star centre `6`, the literal
90-by-9 forbidden-response matrix has rank nine.  Hence its kernel is zero;
all four activity forms belong to its row space and no active carrier cap
exists.

The stronger exact census is:

```text
168 star carriers:        rank 9,
558 triangle carriers:    rank 9,
  2 triangle carriers:    rank 8,
active star/triangle carriers: 0.
```

The checker retains every source block in `results.json`.  It also audits an
exceptional rank-eight triangle directly.  For pair `05`, triangle `246`,
the kernel vector

```text
K=(0,0,1,0,0,11,0,0,1)
```

has activity values `(K_00,K_11,K_22,s)=(0,0,1,0)`.  Every forbidden response
row annihilates `K`, and a literal evaluation of the cubic cap-error formula
on all 729 residual words gives zero nonzero coefficients.  This is an exact
**clean but inactive** cap control: error cleanliness and activity are not
being conflated.

## 5. Scope guard and consequence for the 27 charts

The counterexample is deliberately local.  It fails 4,508 of the 4,878 mixed
X4 rows and has pure amplitudes `(4,4,0)` in `F_13`.  It therefore does not
refute a theorem that uses the remaining global X4 equations and nonzero pure
amplitudes to couple a full-rank slice to cap coordinates.

It does refute the proposed **local** terminal

```text
matched packet + live singleton cofactors + full slice rank
    => active clean star/triangle carrier.
```

Accordingly, the 27 non-dangerous pure-matching charts are not closed by the
rank dichotomy.  A valid repair needs two new source-level ingredients:

1. a chart-to-packet entry lemma in endpoint-cell coordinates; and
2. an explicit identity mapping the global X4 consequences of a full-rank
   slice into the nine-dimensional carrier kernel and proving all four
   activity forms nonzero there.

A rank count or an inverse slice matrix is not such a map.  Any proposed
repair should be run against the stored `m=26/F_13` point: if it uses only the
six packet rows and slice invertibility, it must incorrectly predict a
carrier and is therefore false.

## 6. Replay

Standard, optimized, and isolated/no-site runs agree on core digest

```text
34778a8f79757cf312074c752c356bcf51543bad52aa7e30ec79bae093022291
```

Replay from the repository root:

```sh
python3 computations/unaudited-codex-slice-rank-cap-bridge-2026-08-20/audit_slice_rank_cap_bridge.py
python3 -O computations/unaudited-codex-slice-rank-cap-bridge-2026-08-20/audit_slice_rank_cap_bridge.py
python3 -I -S computations/unaudited-codex-slice-rank-cap-bridge-2026-08-20/audit_slice_rank_cap_bridge.py
```

Artifacts:

* `audit_slice_rank_cap_bridge.py` — independent raw checker, packet census,
  counterexample constructor, 728-carrier census, and literal error audit;
* `results.json` — exact source blocks and all ledgers above.
