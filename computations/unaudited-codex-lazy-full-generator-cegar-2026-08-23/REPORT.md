# Lazy all-generator CEGAR is an exact membership algorithm

Status: **UNAUDITED exact linear-algebra theorem with full-profile71 replay**.

## The theorem

Let `E` be finite-dimensional over a field `k`, let `R` be the complete
finite pool of translated generator rows, put `W=span(R)`, and fix a target
`t`.  Start with any `V_0 subseteq W`; in particular `V_0=0` is allowed.
At round `i`:

1. if `t in V_i`, return membership;
2. otherwise choose `lambda_i` with `lambda_i(V_i)=0` and
   `lambda_i(t)!=0`;
3. add every `r in R` for which `lambda_i(r)!=0`.

Then:

```text
stall  <=> lambda_i(R)=0
       <=> lambda_i(W)=0 while lambda_i(t)!=0,
```

so a stall is a genuine separator of `t` from the span of **all** rows.
Conversely, every crossing row lies outside `V_i`, since `lambda_i`
annihilates `V_i`; hence every nonstall round strictly increases dimension.
There can be at most `dim(W)-dim(V_0)` such rounds.  Therefore the only two
terminal outcomes are

```text
target remainder zero  <=> t in W,
separator stall         <=> t notin W.
```

No target-touching initialization is required.  Such a seed is solely a
performance heuristic.

## Necessary scope guards

- `V_0` must lie in `W`.  Extraneous initial rows decide membership in
  `W+V_0`, not in `W`.
- The crossing scan must cover every row in the claimed pool.  A partial
  scan certifies only its own span.
- The statement is field-by-field.  A modular result needs characteristic-
  zero replay: a modular separator becomes a `Q` certificate only after an
  exact rational/integer dual is verified against every row.
- The translation degree/universe must be finite and fixed.  If higher
  degrees are part of the claim, they belong in `R`.

## Exact full-profile71 replay from an empty seed

The checker restricts the stored 62-word/full-profile71 translation universe
to the 196 columns supporting its exact characteristic-zero dual.  It
enumerates every translated row that is nonzero on those columns:

```text
translation quotients touching support   1,843
distinct restricted eager rows             387
restricted target columns                     3
eager rank                                  195
eager target remainder terms                  1.
```

Starting from `V_0=0`, the lazy algorithm has 12 growth rounds with ranks

```text
11,22,36,50,64,74,82,111,152,182,192,195
```

and its thirteenth scan has zero crossing rows.  The eager and lazy spans
therefore coincide (both have rank 195 in 196 columns), and the lazy terminal
functional is the stored exact full-profile71 separator up to a nonzero
scalar.  Its target pairing is `2`.  A positive control with target
`row_0+2 row_1` reaches remainder zero from the same empty seed.

This restricted replay is deliberately small, but it is exhaustive on its
196-column quotient and tests both implications of the theorem.

## Target-name reconciliation

The correctness theorem uses no symmetry, but two archived stabilizer counts
refer to different targets:

```text
unconed literal holonomy:
  Stab = S2({3,4}) x S3({5,6,7}), order 12, trivial character;

holonomy coned by the fixed pure matching 01|23|45|67:
  Stab = {id,(6 7)}, order 2, trivial character.
```

The cone breaks the order-12 stabilizer to its order-2 intersection with the
cone stabilizer.  This distinction does not affect lazy CEGAR.

## Replay

```bash
python3 computations/unaudited-codex-lazy-full-generator-cegar-2026-08-23/audit_lazy_full_generator_cegar.py --check-results
python3 -O computations/unaudited-codex-lazy-full-generator-cegar-2026-08-23/audit_lazy_full_generator_cegar.py --check-results
python3 -I -S computations/unaudited-codex-lazy-full-generator-cegar-2026-08-23/audit_lazy_full_generator_cegar.py --check-results
```

Frozen logical digest:
`29357661248ed727373c73c086b953ad545e7bee11de38ac3e1cc73d1497a007`.
