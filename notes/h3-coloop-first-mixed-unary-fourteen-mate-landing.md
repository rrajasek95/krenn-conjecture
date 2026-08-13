# All fourteen first mixed-unary mates leave the localized coloop guard

## Exhaustive split

The first omitted equation from `44cdd15` is

\[
 H_0[000011]=0,
\]

and its already nonzero private term is

\[
 q_{01}^{00}q_{23}^{00}q_{45}^{11}.                 \tag{1}
\]

Therefore one of the other fourteen perfect-matching monomials must be
nonzero.  Exhaustive decorated enumeration gives

```text
2  all-diagonal mates
8  two-cross-colour mates with a current endpoint closure
4  two-cross-colour mates with no current endpoint closure.
```

Checker:

```text
computations/verify_h3_coloop_first_mixed_unary_fourteen_mate_landing.py
```

## The two diagonal mates destroy coloopness

They are

```text
02:00 | 13:00 | 45:11
03:00 | 12:00 | 45:11.
```

The base coloop cofactor already has `q45[00]!=0`.  Hence either mate also
makes one of

```text
02:00 | 13:00 | 45:00
03:00 | 12:00 | 45:00
```

a nonzero pure-zero matching.  Both avoid the claimed coloop edge `01`.
Thus these branches are strict pure-support/coloop escapes, not trapped
diagonal completions.

## Eight mates have literal response closures

The nonzero endpoint cells in the guard close exactly the physical edges

```text
01 from f/f,   04 from f/g,   14 from g/g.
```

Eight offdiagonal mates contain one of these edges.  Delete it and insert
the corresponding already nonzero `p1,s1` cells.  This gives a literal
mixed `R11` occurrence, with exact output split

```text
closure 01: 2 occurrences in R11[110011]
closure 04: 3 occurrences in R11[100011]
closure 14: 3 occurrences in R11[010011].
```

Every retained tail has its original `00/01/11` decorations and endpoint
orientation.  Every resulting response term omits `q01`; its target value
is zero.  The checker records all eight terms, heads, words, tails, and
their `f/f`, `f/g`, or `g/g` endpoint provenance.

Each mate also contains two nonzero offdiagonal cells in the physical zero
mixed unary row.  The pinned target-augmented private-site theorem therefore
produces a source-provenant distinct-head active fan, and complete pure
supports route it to four-good or a literal pure-colour coloop.

## The four head-dark mates are one smaller rectangle

The mates with no current endpoint closure are exactly

```text
02:00 | 15:01 | 34:01
03:00 | 15:01 | 24:01
05:01 | 12:00 | 34:01
05:01 | 13:00 | 24:01.
```

This is the sharp pre-fan trapped configuration: a zero-zero edge and a
two-edge cross-colour matching, no edge among `01,04,14`, no endpoint head,
and zero `q01` incidence.  It is smaller than an arbitrary matching packet.
It does not survive as a new proof branch, however.  Each of its cross cells
lies in the same zero physical unary row, so the private-site fan theorem
applies without first constructing an endpoint closure.  It again yields
four-good or a literal pure-colour coloop.

## No selected occurrence minor is created directly

None of the fourteen mates adds `q01[11]`, `q14[11]`, or a second-head
endpoint coefficient.  Consequently all four selected `f,g` minors from
`44cdd15` remain zero.  The exact landing is instead

```text
2 diagonal mates     -> pure-zero matching avoiding the coloop
12 offdiagonal mates -> physical active fan -> four-good or literal coloop.
```

The remaining literal-coloop outcome returns to the already isolated
active-fan coloop normalization/pointed-comparison theorem.  This result
does not claim that arbitrary coloop landing—or physical `P_f`—is thereby
closed.

## Verification

Run

```text
python3 computations/verify_h3_coloop_first_mixed_unary_fourteen_mate_landing.py
python3 -O computations/verify_h3_coloop_first_mixed_unary_fourteen_mate_landing.py
python3 -I -S computations/verify_h3_coloop_first_mixed_unary_fourteen_mate_landing.py
```

Frozen ledger SHA-256:

```text
736d919f789df3b87f1fc84e16ec6d03c996859b9e02ca237af9b7a579f6d4b7
```
