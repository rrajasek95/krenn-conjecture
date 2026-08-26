# Exact characteristic-zero audit of the full profile-`7+1` terminal matrix

Status: **UNAUDITED exact separator PASS.**  The coned holonomy target is
not in the `Q`-span of the complete `closure22 + profile71` terminal matrix.
This conclusion is verified over `Z`; it is not inferred from a modular run.

## Scope correction and terminal input

The earlier file named `plus_profile71` contained only 29 word generators:
the 22 closure words plus seven selected `7+1` words.  It was not the full
orbit and is not used here.

The corrected inputs contain

```text
closure22 words                                  22
complete profile-(7,1) orbit                     48
intersection                                      8
distinct retained word generators                62.
```

Independent Rust runs at `p=32003` and `p=32009` have identical 38-round
candidate/add/rank ledgers.  Both stop at

```text
terminal rank                                314,887
terminal dual support                            196
terminal remainder terms                      13,636
target reduced to zero                         false.
```

Those modular facts guided the small certificate extraction, but they are
not the characteristic-zero proof.

## Small exact matrix

Let `S` be the 196-column support of the terminal modular dual.  A translated
word row can pair with a functional supported on `S` only if one of its terms
lands in `S`.  The checker therefore enumerates, for every one of the 62
literal projected word generators, every nonnegative degree-nine joint
translation obtained as

```text
q = s - term,  s in S.
```

It then restricts the whole translated row to `S`.  This is exhaustive for a
certificate supported on `S`: every other translated row has zero pairing
for support reasons.  The large terminal block collapses exactly to

```text
abstract translations examined                   1,843
distinct restricted integer rows                    387
columns                                              196
maximum nonzeros in one row                            9.
```

The row nonzero histogram is

```text
nnz       2    3   4   5  6  7  8  9
rows    252   54  48  22  5  4  1  1.
```

Thus no CRT over the 314,887-row echelon matrix is needed.  The smallest
exact problem is only `387 x 196`.

## Exact-Q rank and integer separator

Seven modular guards all give row/augmented ranks `195/196`, at

```text
31991, 32003, 32009, 32749, 65521, 1000003, 1073741827.
```

The checker selects 195 independent rows and repeats elimination with exact
`Fraction` arithmetic.  It obtains

```text
rank_Q(A)                                           195
rank_Q([A; target])                                 196
nullity_Q(A)                                          1.
```

The rational null vector has denominator two.  Clearing it and taking the
primitive integer vector gives a separator `lambda` with

```text
support                                             196
minimum coefficient                                 -8
maximum coefficient                                  8
max |lambda(row)| over all 387 rows                   0
lambda(target)                                        2.       (1)
```

The exact separator-vector digest is

```text
f7305b89a68af92f9440bc75cc2fcca251e8e90fed10963f8e3ce33ca5566243.
```

Flipping its first coefficient makes six restricted row pairings nonzero,
providing a hostile mutation guard.  A separately produced rational-dual
artifact is byte-independent and contains the same 196 column/coefficient
pairs and target pairing two.

Equation (1) is an exact characteristic-zero separator.  Therefore

```text
coned holonomy target notin span_Q(
    every degree-nine translation of closure22 + all profile71 words).
```

## Consequence and guard

The provisional statement that `closure22 + profile71` proves the coned
holonomy target lies in full `X5` is false at this terminal joint-semigroup
level.  The full 48-word orbit kills earlier small duals but leaves this new
196-column exact separator.

This does not separate the target from all 6,558 mixed `X5` word types.
Other profiles can cross the functional, just as `profile71` crossed the
earlier closure22 separator.  The precise conclusion is only that the
62-word packet is insufficient; another source-word family or a genuinely
different triangle/incidence relation is required.

## Replay

The dependency-free checker is
[`audit_full_profile71_terminal_char0.py`](audit_full_profile71_terminal_char0.py),
and the full 196-entry certificate is stored in
[`results_full_profile71_terminal_char0.json`](results_full_profile71_terminal_char0.json).
The exact gate completes in a few seconds and refuses support over 256 or
more than 1,024 restricted rows.

```sh
python3 computations/unaudited-codex-profile71-terminal-char0-2026-08-23/audit_full_profile71_terminal_char0.py --check-results
python3 -O computations/unaudited-codex-profile71-terminal-char0-2026-08-23/audit_full_profile71_terminal_char0.py --check-results
python3 -I -S computations/unaudited-codex-profile71-terminal-char0-2026-08-23/audit_full_profile71_terminal_char0.py --check-results
```

Pinned corrected terminal SHA-256 values:

```text
p32003  fa12b6726b7dbc7f448f860d6afc6ea0dd870d1dff0c2604712d4e9f513d7d0d
p32009  d03211f12cac5cd713f620a22024c5e9bf925d29f3809800897d19c2c393f163
```

Logical certificate SHA-256:
`6a8e00fa771a76b1479fa9eba236dbcb3393450b2aa459c91af5e0aeac9fb69e`.
