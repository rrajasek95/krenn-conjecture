# Filtered `-R8'*E0*E1*E2` reduction through K24

## Outcome

A source-faithful restartable reducer is implemented in
`filtered_k24_reducer.py`.  It preserves exact `H`-orbit masses, streams the
factorized full input without materializing the `104^3` error packet, and
reduces collected buckets in ascending K-degree.  No full seed or K24 run was
launched.

The exact recurrence is triangular in K:

```text
collected Kd row / mixed K0 anchor pivot
    -> K(d+2) tails (12)
     + K(d+3) tails (32)
     + K(d+4) tails (60).
```

At each later-degree canonical `H` orbit, the safe implementation expands its
labelled orbit, assigns coefficient `orbit_mass/orbit_size`, averages over all
literal dividing mixed K0 pivots, canonicalizes every child, and recollects
exact `Fraction` orbit masses.  Buffers flush to sorted runs; checkpoints pin
the input byte offset/seed cursor, processed records, and per-degree run
counts.  Runs are externally mergeable before the next degree.

## Direct-input layers and the K16 scope correction

For each R8' H-slice the direct full product has:

```text
K14: 2+2+2       1,728 terms
K15: 2+2+3      13,824 terms
K16: 2+2+4      25,920 terms
K16: 2+3+3      36,864 terms
```

Therefore the frozen 1,848,174-orbit K16 artifact is **not the full filtered
K16 bucket**.  It is only the irreducible K2-tail response obtained while
cancelling the leading K14 `-R8'*E0_2E1_2E2_2` block.  A full run must collect
that incoming component together with the 62,784 direct K16 terms per R8
H-slice before reducing K16.

The bounded must-pass gate pins and re-hashes that isolated reference exactly:

- byte SHA `28a648a2625d208cc86948b27a06f52f38245fe2ebe130c583e619d1d24b9189`;
- logical SHA `8eb9f7dbb220afd759533c10a4881a502a43bdb3bfa28c36e3b89cf98a4ee58c`;
- 1,848,174 H-orbits / 701,717,184 labelled rows;
- 4,096 boundary semantic sentinels are K16 and K0-irreducible.

A fresh recomputation of all 838,080 K14 cancellations did not finish within
the bounded gate and was stopped/escalated; it produced no artifact because
`--write-results` was absent.  Thus the digest statement above is an exact
frozen-result replay/reference check, not a new independent full recomputation.

## Pivot ambiguity beyond K16

The K14 collector's “valid pivot” subset is defined by the frozen 25-signature
K16 cover.  That cover supplies no canonical rule at later degrees.  Averaging
over all dividing pivots is H-equivariant and is the implemented convention,
but it is a choice, not a pivot-independence theorem.

The checker finds a literal first obstruction already at a K16 parent with
anchor signature

```text
(2,0,0, 2,0,0, 2,0,0, 0,1,1).
```

Both words `00000011` and `00000022` divide it, but their K2-tail reductions
give different four-support canonical K18 signature multisets.  Hence choosing
one pivot, the other, or their average gives different chain representatives.
Critical-pair/confluence data are required before any claim that the eventual
K24 normal form is policy-independent.

## Scope

This package specifies and implements the factorized seed streamer, exact run
merge, restart checkpoints, and degree reducer.  It does not launch the roughly
`485*104^3` seed traversal, does not solve a source matrix, and makes no
membership or K24-closure claim.

Bounded design/reference logical SHA:
`a403d64513d7b7adc3ab3962f1d2844ee80614e5a0c7a1db125648ffc4d2e2f6`.
