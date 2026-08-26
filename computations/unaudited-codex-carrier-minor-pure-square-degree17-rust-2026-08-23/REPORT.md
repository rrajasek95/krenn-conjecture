# Exact separation survives the second pure-normalization step

Status: **UNAUDITED exact characteristic-zero nonmembership theorem**.

## The theorem

For the canonical carrier minor `Delta` and pure colour-0 amplitude
`F_00000000`,

```text
F_00000000^2 * Delta
    notin (all mixed X5 amplitudes)_17 over Q.
```

Thus the direct homogeneous obstruction survives the second pure
multiplication step.  This is stronger than the earlier minimal-shell
obstruction: it covers the complete degree-17 translate universe in the
target fine grade.

## Fine-grade exhaustiveness

The target weight is

```text
sites 0,1,2 : (3,0,0)
sites 3,4,5 : (5,0,0)
site  6     : (3,1,1)
site  7     : (2,3,0).
```

Exactly six amplitude words are compatible:

```text
00000000 (pure; excluded from the homogeneous mixed-X5 ideal)
00000001  00000010  00000011  00000020  00000021.
```

The Rust crossing scan uses all five mixed words and all degree-13
monomial multipliers implicitly, by exhaustively dividing every live dual
coordinate by each of the 105 matching terms of each word.

## Rust closure and Python-prefix replay

The sparse Rust implementation reproduces the exact Python ordering:

```text
matching and generator order
64 reserved nonzero target seeds
column assignment
pivot order
crossing-label order
on-demand target coefficient oracle.
```

It asserts eight frozen Python checkpoints through round 109, including

```text
round 109:
  rank    5,711
  columns 391,585
  fill    12,135,624
  dual    214.
```

The continued run terminalized at the global zero-crossing scan:

```text
growth rounds               : 129
terminal scan               : 130
rank                        : 14,979
tracked columns             : 817,554
basis nonzero entries       : 284,356,921
terminal modular dual support: 102
manifest wall time          : 192 seconds.
```

The run remained within the fixed 20-minute/16-GB envelope.

## Exact rational reconstruction

The terminal residues reconstruct uniquely with denominators `{1,2}`.
Clearing denominator 2 and removing the common gcd gives a primitive
102-term integer functional with coefficient set

```text
{-8,-6,-4,-2,-1,1,2,3,4,6,10}.
```

Exactly 177 mixed-X5 translates can touch its support:

```text
00000001 : 35
00000011 : 67
00000021 : 75
00000010 :  0
00000020 :  0.
```

Every literal integer row pairing is zero.  The exact target coefficient
oracle, built independently from the 6,900-term `Delta` and 5,250-term
`F_00000000^2`, gives

```text
separator(F_00000000^2 * Delta) = 28.
```

Hence this is a characteristic-zero certificate, not a one-prime
inference.  It also works in characteristics not dividing 28.  The exact
separator digest is

```text
87497e038f9f2415be97095ca81ff1c1f187fcacdefd4fae5159472e29055f2e.
```

## Meaning and guard

The first two pure cones are now both exactly separated:

```text
degree 13: F_00000000   * Delta  separated (pairing 2)
degree 17: F_00000000^2 * Delta  separated (pairing 28).
```

This establishes persistence through `k=2`, but not an all-`k` recurrence.
It also does not prove radical nonmembership or a statement using the
inhomogeneous normalization equation `F_00000000-1` directly.

## Replay

Exact source replay:

```bash
python3 computations/unaudited-codex-carrier-minor-pure-square-degree17-rust-2026-08-23/audit_pure_square_separator_exact.py --check-results
python3 -O computations/unaudited-codex-carrier-minor-pure-square-degree17-rust-2026-08-23/audit_pure_square_separator_exact.py --check-results
python3 -I -S computations/unaudited-codex-carrier-minor-pure-square-degree17-rust-2026-08-23/audit_pure_square_separator_exact.py --check-results
```

The hostile mutation `--mutate-separator` fails on literal `00000011` and
`00000021` translates.

To rebuild the modular discovery:

```bash
cd computations/unaudited-codex-carrier-minor-pure-square-degree17-rust-2026-08-23
rustc -O -C target-cpu=native pure_square_cegar.rs -o pure_square_cegar
./pure_square_cegar
```

Frozen exact logical digest:
`7842e5c59841096ab87ee6aa89c6c85855ee57940ad0ee71a0b56fc6d8fc250b`.
