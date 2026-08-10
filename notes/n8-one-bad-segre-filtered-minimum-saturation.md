# Exact closure of the minimum filtered one-bad layer

## Result

Fix the normalized six-site source `H` and the off-01 cocharacter used in
`n8-one-bad-segre-off01-filtered-response-frontier.md`.  The certified
associated-graded support shadow has positive-q grades

\[
62\cdot 1+14\cdot 2,
\]

minimum positive support six, and exactly twenty minimum supports.  Every one
of those twenty coefficient envelopes is empty over `QQ`.

More precisely, for each minimum support we keep

* all six displayed positive-grade q coordinates;
* all 24 grade-zero face coordinates;
* all 21 grade-zero diagonal q coordinates; and
* all 24 endpoint-star coordinates

as arbitrary variables, while every other positive-grade q coordinate is set
to zero.  Nineteen ordinary source rows already generate 1.  The identity uses
no localization, so it remains valid when any of the six displayed coordinates
vanishes.  Consequently, any source in this fixed-H filtered chart must use at
least seven positive-grade q coordinates.

This is an exact coefficient statement, not a support-only refutation.

## The 19-row cores

There are four transported row families.  The first consists of the six top
rows

```
000000 000001 000100 000101 001001 001100
```

and the thirteen `p1s1` rows

```
010011 010110 010111 011011 011110 011111
110010 110011 110110 110111 111011 111110 111111.
```

The other three cores are literal site/colour transports of this list.  Each
minimum support is checked against its transported rows directly; the proof
does not infer a unit merely from a claimed symmetry.

Every retained diagonal response row depends on the four literal star
coordinates through one common scalar, for example

\[
A=p_1(1)s_1(4)+p_1(4)s_1(1).
\]

The checker first verifies the two literal copies term by term, replaces this
common scalar by an auxiliary variable `astar`, and computes an exact
`liftstd` identity in the smaller ring.  Substitution of the displayed literal
star expression recovers an ordinary identity in the original source rows.
All nineteen rows occur in every reconstructed identity.

## Verification

Run

```bash
.venv/bin/python computations/verify_n8_one_bad_segre_filtered_minimum_saturation.py
PYTHONOPTIMIZE=1 .venv/bin/python computations/verify_n8_one_bad_segre_filtered_minimum_saturation.py
```

The checker pins the upstream minimum-support list, reconstructs all top and
four response tensors from the physical matching formula, verifies the common
star factor, and checks `matrix(I)*L=1` over `QQ` for every support.  It records
the full row streams and exact source-lift hashes in a deterministic ledger.

## Scope

This closes the complete minimum-six coefficient layer only after the fixed-H
off-01 normalization.  It does not cover supports with seven or more positive
q coordinates, and it does not prove that an arbitrary projection-degenerate
one-bad packet admits this normalization.  Those are the remaining filtered
normalization gates; no global Krenn contradiction is claimed here.
