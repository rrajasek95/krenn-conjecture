# Independent direct-K19 permutation and conservation referee

## Outcome

The historical direct-K19 producer is wrong, and the corrected recurrence now
passes the exact charge-conservation check for its actual bounded input.

In `merge_and_charge_k19.rs`, the three `high` iterations select the K3 tail
from factor families `[1,0,0]`: factor 0 is duplicated and factor 2 is omitted.
All factor families have the same K3/K4 cardinalities, so both the wrong and
right loops enumerate `3*32*60*60` rows per R8prime record.  This explains why
the historical full and irreducible row counts were unchanged.

The full recomputation gives:

| direct K19 | full | irreducible | pivotable |
|---|---:|---:|---:|
| historical | `202278912` | `141570048` | `60708864` |
| corrected | `174465024` | `126418944` | `48046080` |
| delta | `-27813888` | `-15151104` | `-12662784` |

The exact signed child full charges are

```text
K21 D19|R:2  = -170514432
K22 D19|R:3  = +228446208
K23 D19|R:4  =   -9885696
sum           =  +48046080.
```

Thus the corrected local identity

```text
parent full - parent irreducible = sum(child full)
```

holds exactly.  The historical local residual was `+12662784`.

## Terminal-versus-local distinction

The terminal K14--K24 ledger contains the K19 **irreducible** charge, not the
pivotable difference.  Its correction is therefore `-15151104`, not
`-12662784`:

```text
19715328 - 15151104 = 4564224.
```

An independent literal enumeration of all 27 ordered direct packet types of
the frozen input

```text
P = -R8prime*E0*E1*E2
```

gives degree-bucket charges

```text
K14  +230092800
K15  -539203584
K16  +388502016
K17   +53763072
K18  -272994816
K19  +174465024
K20   -30060288
sum     +4564224.
```

The corrected terminal ledger therefore conserves the charge of its actual
input exactly.  There is no remaining scalar conservation defect.

## Theorem scope and conjecture status

The earlier zero-baseline classification was invalid for this bounded stream.
The 77-functional pairs zero with the complete structured `a*T`, but the
recurrence input above is built from the sparse `R8prime`, which represents
`T` only modulo `I_mix+K^9`.  The cutoff certificate explicitly retains an
omitted K9 tail and warns that the displayed `a*R8prime` calculation is not the
full `a*T` stream.  Hence `P` is not entitled to the complete-target zero
baseline; its independently computed charge is `+4564224`.

This repair validates only scalar charge conservation for the frozen
orbit-zero `P` recurrence.  It does not reconstruct the missing source-faithful
`a*T` K9-tail stream, produce the literal K24 row-orbit residual and relative
span certificate, cover the other chart orbits, or decide the general
bicoloured `n=8,d=3` or all-even Krenn--Gu conjecture.

## Replay

Run from the repository root:

```text
python3 computations/unaudited-codex-orbit0-k19-direct-permutation-referee-2026-08-24/audit_k19_permutation_conservation.py
```

The audit pins the historical producer/result, both corrected recomputation
transcripts, the three D19 child manifests, the prior K24 arithmetic result,
and the exact theorem/cutoff scope files.  It writes
`results_k19_permutation_conservation_referee.json` and fails closed on every
source-pattern or arithmetic mismatch.
