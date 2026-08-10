# The concentrated unary-top identity lifts through order five

## Exact result

The reachable-tail Schur lift from
[`n8-lemma-e-unary-top-order4-reachable-schur.md`](n8-lemma-e-unary-top-order4-reachable-schur.md)
continues one layer farther.  With all 135 internal cells retained and the
concentrated response holes fixed at `(01),(23)`, the literal source ideal
`I` satisfies

\[
 F_{01}(1111)F_{23}(2222)H(000000)
 \in I+\mathcal F^{\geq6}.                              \tag{1}
\]

This is exact over `QQ`.  It covers arbitrary internal support and aggregate
cancellation.  It remains a concentrated-spoke filtered theorem, not full
ideal membership and not the multisite one-bad theorem.

## Reachable order-five quotient

Minimum-order-five source columns first give

```text
order-five rows:              18,988
direct source columns:        26,452
direct rank:                  18,040
direct quotient dimension:       948.
```

The checker then carries only these 948 quotient coordinates through the
already-certified order-four graph.  Dependencies among the 30,812 direct
order-four columns and the 20,064 low-kernel columns generate rank 884 in the
order-five quotient.  Its new cokernel therefore has dimension 64.

The actual corrected target has 939 nonzero quotient coordinates before this
reachable reduction and remainder zero.  Thus its vanishing is a property of
the particular source-provenant tail, not a claim that every order-five
monomial can be rewritten.

The complete truncated matrix through order five has

```text
rows:                 44,723
literal columns:      88,446
rank over QQ:         44,638
cokernel over QQ:         85
  inherited at order4:    21
  new at order5:          64.
```

## Characteristic-zero certificate

The modular Schur pivots exhibit rank at least 44,638 over `QQ`.  The checker
reconstructs the 21 inherited and 64 new left-cokernel vectors over `ZZ`.
All their nonzero coefficients are `+1` or `-1`.  It verifies their pairing
with all 88,446 literal truncated source columns exactly over the integers,
so they give the matching rank upper bound.  It then pairs all 85 with the
target and obtains zero.  Completeness of the rational left cokernel proves
(1).

The new 64 annihilators have supports between 12 and 43; their complete
ordered support ledger and coefficient hash are frozen by the checker.  The
small supports are useful structurally: the remaining cokernel again consists
of signed incidence classes, while the target tail lies in the reachable
image.

## Scope and stopping point

Orders six and seven remain.  This cycle deliberately stops before order six:
the requested bounded question was whether order five produces the first
exact obstruction, and it does not.  Repeating the hierarchy would require
carrying the order-six quotient through 44,638 pivots; that should be a
separate resource decision.

Even eventual concentrated membership would not alone close the one-bad
packet.  The fixed singular spokes must still be polarized over physical
response holes with their endpoint-star coefficients, preserving common
source provenance.  No conclusion about a counterexample or the full `N=8`
conjecture follows from (1) alone.

Run

```text
.venv/bin/python computations/verify_n8_lemma_e_unary_top_order5_reachable_schur.py
.venv/bin/python -O computations/verify_n8_lemma_e_unary_top_order5_reachable_schur.py
```

Frozen hashes:

```text
matrix:
b3aa200868fe0b2bb2268253b14eea43544f1e38629cf1d1ee638fe9725c29c7

integral cokernel:
3f34028ebf06ff1ee286d176e0bb8b5dbea9a16c33aee9bd82971d9f384e98a9

ledger:
5014b520ee5396b8505ae478aed1bbe33f3d042e094ef7d20a626b553354a569
```
