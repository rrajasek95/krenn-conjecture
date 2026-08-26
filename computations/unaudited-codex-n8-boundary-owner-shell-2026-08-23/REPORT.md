# Chart-1 boundary: exact private-owner attachment shell

## Result

There is no closed finite polarization/Koszul/C4 recurrence on the accepted
round-6--12 dual/killer packet.  The exact replacement is a private-owner
Schur (equivalently algebraic Morse) lemma: relative to the frozen
2,613-column/125,328-row interface, every one of the 4,903 accepted round-7--12
repair columns owns a beyond-interface row occurring in no other column **of
that accepted shell**.  Choosing one shell-private owner per column gives a
diagonal matrix with nonzero integer diagonal, so this repair shell is
split-injective over `Q`.  No nonzero combination of those enumerated columns
can land back in the old target interface.  Equivalently, for the matrix
containing exactly the old columns and the round-7--12 shell, the old cokernel
injects into the enlarged cokernel: the target class is conserved across this
finite attachment.  This is the source-labelled lemma that replaces all six
incremental rank tests.

The pending round-13 shell has the same *shell-relative* form: all 1,186
violating columns have a private new owner within that shell (58,234 new rows,
54,575 of shell-ownership degree one).  The full incident replay gives the
decisive scope correction: previously unselected D12 columns also own/cross
these rows.  Therefore shell privacy is not global privacy and cannot produce
a full separator.  A terminal argument must adjoin the external owner shell.
The present result is not a terminal degree-12 membership, saturation, or
atlas-boundary theorem.

The lex-first exact round-13 counterowner is already large enough to kill the
naive separator lift:

```text
shell column       (code 4, multiplier 0a52b8ee)
shell-private row  0a12515291c1e5eb, coefficient +1, target coefficient 0
outside column     (code 4, multiplier 0a12515291c1e5eb), coefficient +1
```

The outside column is unselected, and the row has 91 incident column orbits in
the full provider.  Hence it is a literal counterguard, not merely a warning
that future attachments might exist.

## Literal source start and transition census

The round-6 dual frozen in `checkpoint_d12_lazy_cegar.json` is the singleton

```text
0d55b8ee = A02[11] A14[11] A36[11] A57[11].
```

Its 42 accepted invariant killing-column representatives are one profile-44
word orbit (`11221122`) with 42 multipliers: 24 two-edge matchings and 18
three-edge matchings.  This source replay is a useful scope correction: the
profiles 62 and 422 begin in the next accepted shell, not in these 42 frozen
representatives.

| round | columns | word profiles | physical multiplier skeletons |
|---:|---:|---|---|
| 6 | 42 | 44:42 | 2-edge matching:24; 3-edge matching:18 |
| 7 | 523 | 422:238, 62:162, 44:123 | matching on 6:247; matching on 8:276 |
| 8 | 639 | 422:291, 62:198, 44:150 | matching on 6:441; matching on 8:198 |
| 9 | 708 | all 9 mixed profiles | 2-edge matching:88; C4:112; two parallel doubles:508 |
| 10 | 2,025 | all 9 mixed profiles | 2-edge matching:24; C4:836; parallel doubles:112; P3+P2:1,053 |
| 11 | 969 | 422:411, 62:324, 44:234 | perfect matching:969 |
| 12 | 39 | 422:18, 62:12, 44:9 | perfect matching:39 |

Thus a C4-exchange description is not stable: rounds 9--10 force collision
and path-forest owners outside the matching packet, and rounds 11--12 return
to matchings before round 13 expands again.  The accepted rank increment equals
the accepted column count in every round 7--12, with no zero column.

## Smallest source-labelled counterguard

The lex-first accepted repair is

```text
column  (word code 4, multiplier 0a51b7ea)
term    125191eb, coefficient +1
owner   0a12515191b7eaeb.
```

The owner is absent from the old interface and every other accepted repair,
but is not asserted private against all unselected D12 columns.
This single literal attachment already prevents a complex confined to the old
dual rows and killing-column heads from being closed.

## Archive guard

The durable ledger freezes the round-7--12 dual support **sizes**
`8,9,22,45,29,1`, but not their row labels.  Reconstructing those historical
dual supports byte-for-byte would require replaying the modular rank solves,
which was excluded here.  The killing-column list, literal attachment outputs,
and the private-owner complex are fully frozen and replayed without a solve.

## Replay

Run:

```sh
python3 audit_boundary_owner_shell.py
python3 -O audit_boundary_owner_shell.py
python3 -I -S audit_boundary_owner_shell.py
python3 audit_boundary_owner_shell.py --mutate  # must fail
```

Inputs are pinned by digest in `results_boundary_owner_shell.json`.  The
underlying exhaustive literal ownership replay is
`../unaudited-codex-n8-chart1-boundary-a0200-2026-08-23/results_d12_private_ownership.json`
(logical SHA-256 `224bf26bbc8523b4c4f55d63d8b44236af63360063d8b1f1e403ae9fb79d88a1`).
