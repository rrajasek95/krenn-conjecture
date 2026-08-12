# The order-six higher faces are the forced Hasse lift, not new errors

## Outcome

The exact 188-term order-six residual chain has now been expanded on every
positional subset of its six derivative directions.  Let `L_k` be its
unsigned `k`-face incidence counter.  Then

```text
L_0 = 0,
L_1 = 0,
L_2 = the exact sixteen-coordinate -delta tensor,
```

and every higher layer satisfies the exact divided-incidence law

\[
               \operatorname{down}(L_{k+1})=(6-k)L_k.
\]

In particular

\[
                     \operatorname{down}(L_3)=4L_2.
\]

Therefore a nonzero pair shadow with a zero triple layer is impossible in
characteristic zero.  The hundreds of nonzero higher faces are not
contamination to eliminate; they are the necessary coherent Hasse lift of
the residual pair face.

Checker:
`computations/verify_h3_residual_q_order6_complete_hasse_incidence.py`.

## Exact inventory

For layers `k=0,...,6`, the numbers of nonzero faces are

```text
0, 0, 16, 401, 916, 697, 166.
```

Their coefficient sums are all zero.  Their `l1` sizes are

```text
0, 0, 16, 826, 1946, 1480, 344.
```

The down-incidence identities hold exactly over the rational solution, with
multiplicity when a derivative direction repeats.

## Why the first attempted totalization test was wrong

It is tempting to demand that the order-six kernel retain `L_2=-delta` and
kill every layer above it.  A modular solve correctly rejects that demand,
but the rejection is formal: `down(L_3)=4L_2` already makes it impossible.
The proof should totalize the complete tower, not truncate it at pairs.

This shifts the remaining work in a favorable way.  We do not need a new
source correction for each of the 401 triple faces.  We need one physical
comparison which recognizes the already coherent tower as a labelled
repeated-grade Hasse/Spencer cell.

## Revised local end game

There are now two explicit pieces:

1. the complete order-six Hasse tower, with zero literal pair-generator
   source and pair projection `-delta`;
2. the canonical terminal relative class `-dOmega_v`, whose eta and sigma
   contractions are exactly the missing terminal packet.

The remaining theorem is to place these two pieces in the same physical
labelled repeated grade and verify the alternating Spencer/augmented
differential.  The primitive face `07:11 wedge 24:11` supplies the common
attachment and, under compatible labels, the one-sided `(2,3)->(3,3)` rank
arm.

## Scope

The checker proves the complete **unsigned positional Hasse incidence** of
the bounded differential-operator solution.  It does not prove physical
source typing, the alternating Spencer signs, target/ores/anchor
compatibility, or the repeated-grade lift.

Verification:

```text
python3 computations/verify_h3_residual_q_order6_complete_hasse_incidence.py
python3 -O computations/verify_h3_residual_q_order6_complete_hasse_incidence.py
python3 -I -S computations/verify_h3_residual_q_order6_complete_hasse_incidence.py
```

Frozen ledger SHA-256:

```text
6e30806247614d5e622c79d1b904ab6ebe115c64b4cfce7d77c8ff4011c9f2ef
```
