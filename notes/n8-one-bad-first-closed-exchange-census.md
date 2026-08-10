# The first closed one-bad exchanges are all coefficient-empty

## Result

Start from either of the two sharp seven-cell one-bad packets and allow a
decorated cell only when it participates in the complete six-site top/four
response matching system.  A support is *closed* when every forbidden live
fibre has either zero or at least two matchings.  At minimum added-cell
cardinality the complete census is

| sharp orbit | added cells | total cells | labelled closures |
|---:|---:|---:|---:|
| 0 | 12 | 19 | 1 |
| 1 | 30 | 37 | 8 |

These claims are not native-solver verdicts.  Four frozen deletion-free RUP
proofs certify that caps 11 and 29 are impossible and that blocking the
displayed cap-12/cap-30 supports leaves an unsatisfiable CNF.  The checker
reconstructs the CNFs from the matching semantics and replays every RUP
addition through the empty clause.

None of the nine closures is coefficient-consistent on its localized torus.
The unique orbit-0 closure has an odd five-row Laurent character circuit.
Every orbit-1 closure has 54 plus-binomial rows of exponent rank 24, and
exact pivot-ordered reduction sends a forbidden source polynomial to one
nonzero Laurent monomial.  Thus all eight give ordinary localized units;
their first normal-form coefficients lie in `{1,-1,2,-2}`.

## The fan dichotomy

The carrier sites are `{0,1}`.  The diagonal response pairs are

```text
b: 24,   c: 35.
```

For sharp orbit 0, the two cross responses yield zero pairs `25,34`, while
the two top edges yield `23,45`.  These four pairs form a `C4`; every right
vertex supports a shared two-zero fan.  The unique closure is exactly the
19-cell `K_{2,4}` rectangle from
`n8-one-bad-even-cycle-rectangle-obstruction.md`.

For sharp orbit 1, reversing the ordered `c` holes makes the cross response
pairs equal the top pairs:

```text
cross zeros = top zeros = {23,45}.
```

They are disjoint.  Consequently orbit 1 supplies the first exact
fan-avoiding no-singleton exchange closure.  It is not a coefficient point:
the Laurent one-class certificate kills every one of its eight minimum
supports.  This is the requested counterguard to the claim that every first
closure must quotient to the shared-zero fan.

## Meaning and remaining gate

The local matching-potential route now has a precise termination boundary.
At the first closed layer it never produces a coefficient survivor, but the
reason is not uniform across the two sharp orbits:

```text
orbit 0: shared two-zero fan / odd character,
orbit 1: fan-avoiding one-class Laurent unit.
```

The reusable next theorem should therefore say that any coefficient-feasible
nonminimum completion must preserve a nonzero residual after the full
plus-binomial character quotient.  This audit deliberately does not
enumerate arbitrary larger supersets, so it does not yet close the reduced
one-bad algebra support-independently.

## Reproduction

```sh
uv run python computations/verify_n8_one_bad_first_closed_exchange_census.py
PYTHONOPTIMIZE=1 uv run python computations/verify_n8_one_bad_first_closed_exchange_census.py
```

Both modes must print

```text
75300194ded544c190ef16b0c048edff4ebf606cc02917a9a7b9bb0305bc5dbc
```
