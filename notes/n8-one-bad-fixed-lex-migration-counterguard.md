# A fixed target-word lex order cannot orient one-bad matching exchange

## Outcome

The lexicographic increase seen in the twelve-successor singleton map is not
a uniform matching-exchange theorem.  Replaying the already frozen one-bad
counterguards under the fixed orders

```text
sites   0 < 1 < 2 < 3 < 4 < 5,
colours 0 < 1 < 2
```

gives both directions immediately:

| frozen exchange audit | forward targets | backward targets |
|---|---:|---:|
| first response mate | 5 | 7 |
| second top mate | 265 | 251 |

All 528 targets in this table are source-reconstructed private monomials, so
they are terminal units in those bounded charts.  They nevertheless disprove
the proposed universal direction: the same matching-exchange mechanism can
export a lexicographically smaller or larger target in both sharp orbits.

The obstruction is not an artefact of those examples.  In the canonical
twelve-successor map, the first migration is

```text
000102 -> 002101.
```

It is forward.  Simultaneously swapping sites 2 and 5—an exact symmetry of
the source equations—transports it to

```text
002100 -> 001102,
```

which is backward.  Therefore no order on absolute site labels can make the
canonical observation invariant under source relabelling.

## First equal-target nonunit guard

There is also an exact failure of the proposed “equality implies odd or
parallel unit” alternative.  Take the first independent physical matching
square on eight sites:

```text
M00 = 01|23|45|67      M10 = 03|12|45|67
M01 = 01|23|47|56      M11 = 03|12|47|56.
```

The occurrence vectors satisfy

\[
                  \chi_{00}+\chi_{11}
                = \chi_{10}+\chi_{01}.                \tag{1}
\]

Decorate all four matchings by the same mixed target word `00112201`.
Give every localized cell value 1 except the cells on physical edges `03`
and `47`, which have value -1.  Then

```text
(M00, M10, M11, M01) = (1, -1, 1, -1).
```

Every adjacent exchange pair cancels.  The four exponent displacements are
distinct, their sum is zero by (1), and their character product is
`(-1)^4=+1`.  Thus this is a source-faithful equal-target, coefficient-
consistent matching square with neither an odd dependency nor a parallel
opposite-character pair.  Equivalently, its four-term union fibre vanishes
at the displayed nonzero Laurent point.

This is a local matching-exchange counterguard, not a full Krenn point.  The
complete orbit-0 rectangle containing the relevant even-cycle mechanism is
still empty: its shared-two-zero tensor fan has unit ideal over `QQ`.  The
eight orbit-1 first closures likewise retain their committed one-class units.
The distinction is load-bearing: the full contradiction comes from coupling
several target tensors, not from ordering their word labels.

## Missing invariant

A target word records endpoint colours but forgets which perfect matching
carried them.  Matching exchanges occur inside one fibre, where the word is
literally unchanged, and absolute lex direction also changes under site
symmetry.  A viable termination datum must therefore retain at least one of

- the source-labelled matching/circuit character inside each fibre;
- a global vector of boundary debts across all target labels; or
- the tensor quotient data that kills the orbit-0 even square.

The fixed word alone cannot distinguish the equal square and cannot orient
the backward transports.  This explains precisely why the ordered DAG of
the sixteen canonical singleton contaminants does not automatically extend
to arbitrary matching exchanges or to the 173 double-cell tails.

## Verification

Run

```bash
uv run python computations/verify_n8_one_bad_fixed_lex_migration_counterguard.py
uv run python -O computations/verify_n8_one_bad_fixed_lex_migration_counterguard.py
```

The checker pins and replays the first- and second-arrow audits, the sixteen
canonical target migrations, the independent commuting square, the nine
first closed orbit-0/orbit-1 packets, and the orbit-0 tensor fan.  It freezes
the exact backward-transition counts, the relabelled canonical edge, the
explicit Laurent point on the equal square, and the separate full-packet
units.  Its ledger digest is

```text
a91d5517358192349ed38b0c534bb5be061095c52a357a76908b9a06ae76ccd9
```
