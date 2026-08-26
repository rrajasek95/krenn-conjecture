# k5/k6 recursive selected-term boundary routing

Status: **UNAUDITED exact finite B4 covariance census; no algebraic solve.**

## Outcome

Every proper `c=0` boundary of the branch0 k5 and k6 selected-term interiors
has been routed through the frozen 729-state recursive graph.

- k5: 31 labelled nonempty zero-`c` subsets give 13 canonical B4 states.
  Twelve are genuinely new joint `(B,T,D)` faces; the sole aligned terminal
  `0:1:0` is an exact-Q unit in the frozen 50-chart aligned census.
- k6: 63 labelled nonempty zero-`c` subsets give 10 canonical B4 states.
  Nine are genuinely new; the sole aligned terminal `0:0:0` is an exact-Q
  aligned unit.
- The two proper families are disjoint as canonical state sets. None of the
  21 nonaligned states is B4-equivalent to a frozen branch0 all-offdiagonal
  k<=3 exact stratum or to one of the four exact/pairwise-closed cycle
  boundary keys.

This is a routing theorem, not an emptiness theorem.

## Minimal broad boundary attack

If a first face is attacked *without* localizing any of its remaining
`c`-numerators, that one broad result covers its entire descendant subgraph.
Under that convention the boundary antichain is:

| parent | canonical face | support | labelled multiplicity |
|---|---|---|---:|
| k5 `0:63:31` | `0:31:15` | triangle + pendant | 4 |
| k5 `0:63:31` | `0:31:30` | four-cycle | 1 |
| k6 `0:63:63` | `0:31:31` | `K4` minus one edge | 6 |

The k6 boundary residual `0:31:31` has two codimension-two first faces:
`0:15:15` (triangle + pendant, multiplicity 12) and `0:30:30`
(four-cycle, multiplicity 3).

Thus the minimal still-open structural list is:

1. the full k5 interior `0:63:31`;
2. the full k6 interior `0:63:63`;
3. the two k5 first-boundary charts `0:31:15`, `0:31:30`;
4. the single k6 first-boundary chart `0:31:31`.

The exact `P26=0` theorem for the ordinary triangle-plus-pendant chart is
recorded only as a partial determinant-subbranch result. It does not close
the new joint face `0:31:15`, nor the ordinary `P26!=0` lane.

A first bounded attack on `0:31:15` is now frozen. Its literal normalized
12-row square reverse core uses raw rows `7,8,12,...,21` and the full exact
live product. The sole `p=1073741827` native-F4SAT run timed out at 300.268
seconds with zero output, so the state remains open with no modular status or
component signature. See
`../unaudited-codex-face03115-modular-lead-2026-08-21/REPORT.md`.

An exact structural follow-up eliminates `a2` between core raw 16 and the
cheapest omitted cofactor raw 11. Its pivot coefficient is
`b4*(d2-1)`, with `b4` already declared live, and it proves
`A*raw11-C*raw16=R` for an irreducible 29-term degree-six `R`. Hence the
only new split is `d2=1`: the open branch reduces raw11 to `R=0`, while the
closed branch retains the explicit residual
`a5*(d1+1)*(b4-1)+b4+1=0`. This reduces the face structurally but closes
neither branch. Logical digest:
`724c1879dfcedfa714335541ab98246d1e47bcbff3938a865e7ea9530ffc9325`.

The smaller `d2=1` side now has a frozen exact full-source interface: raw16
is solved through `raw16=K*(b4-1)+2`, and all remaining 15 literal rows plus
every surviving original live factor are restored. Its sole characteristic-
zero gate reached the 600-second cap with zero-byte output and no sentinel.
It remains an exact ten-variable residual, not a closure. The `R=0` side was
not touched.

The `R=0` side is now structurally reduced without an ideal solver. Exact
substitution of `a2=-B/[b4(d2-1)]` leaves 14 source numerators plus `R`; its
shortest consistency row has seven terms. A binomial split
`J=a4*b4*d3-b3` solves `b5` when `J!=0` and leaves a four-term equation when
`J=0`. Both subbranches remain open.

The smaller `J=0,U=0` side has now been tested with a faithful full-source
exact characteristic-zero gate. All 15 post-substitution literal rows and
all surviving original live numerators are present. The sole run timed out at
600.555 seconds with zero-byte output and no sentinel, so it remains open.
The untouched `J!=0` side can solve `b5` and is the next smallest reverse
target.

The `J!=0` side has now used raw 9 to solve `b5` and has a faithful
ten-variable full-source characteristic-zero gate. Its sole run also timed
out at 600.688 seconds with zero-byte output and no sentinel. Thus all three
current `0:31:15` subbranches (`d2=1`, `J=0,U=0`, `J!=0`) remain exact
timeout residuals rather than closures or nonunit witnesses.

The untouched k5 full interior `0:63:31` now has a structural source export
only. The canonical gauge `b0=b1=b2=d0=1` leaves 13 variables; all 16 literal
rows survive with rank 16, and the exact live product has 2,992 terms. The
shortest pivot is raw 8:
`raw8=(d1-d2)(a1+a2*b5^2)+a5*b5(d1+d2)-b5^2-2*b5+1`.
No solver was launched; both `d1=d2` and `d1!=d2` remain open.

## Full canonical boundary lists

k5 proper states by remaining both-live degree:

```text
k=4  0:31:15  0:31:30
k=3  0:15:7   0:15:11  0:15:13  0:30:14
k=2  0:7:3    0:11:3   0:13:5   0:13:12
k=1  0:3:1    0:12:4
k=0  0:1:0    [exact aligned unit]
```

k6 proper states:

```text
k=5  0:31:31
k=4  0:15:15  0:30:30
k=3  0:7:7    0:11:11  0:13:13
k=2  0:3:3    0:12:12
k=1  0:1:1
k=0  0:0:0    [exact aligned unit]
```

Every nonterminal key displayed above is a new joint-face residual under the
frozen exact-key comparison. This label means “not already covered by the
listed B4-covariant exact ledgers,” not “has a solution.”

## Source-faithful covariance ledger

`audit_k56_recursive_boundary_routing.py` independently reconstructs:

- all `3^6=729` labelled ternary edge states;
- the 384 listed `C2^4 semidirect S4` actions;
- the 66 canonical state orbits and degree histogram
  `{0:11,1:14,2:18,3:14,4:6,5:2,6:1}`;
- the boundary rule `(B,T,D) -> (B,T xor Z,D minus Z)` for every nonempty
  zero-`c` subset `Z`;
- an explicit switches/permutation witness for each of the 94 labelled k5
  and k6 boundary subsets.

The producer checks every key, transition, and orbit size against the frozen
729-node interface. Result logical digest:
`4c2175b1f2afd7b6fb868117afbbc1d31fe930d9d58e6823273c659b9489f00a`.

An independent referee reconstructs each raw boundary state and replays its
stored B4 witness. It has must-fire controls for forgetting the `D`-edge
removal and for falsely downgrading an exact aligned terminal. Three modes
pass:

```text
standard  d6f293623fc59f0b1961f8fd93e4a5c4b5a4d72e4b1eb55c59a41dcec8fc55a3
-O        7e0509fc3f4e09e3c5dc604277d3043766fb0015d3107454fca7ee26c3cff1d3
-I-S      b178a5bc58ea27d1f3fef8a3e758f61d3a3dc71073c8aa5066a56dc2de613d0e
```

## Scope guard

No Groebner basis, rank solve, or emptiness test was run. A first-face result
only covers descendants if it is proved on the broad face without inverting
the remaining `c` factors. Conversely, a result proved only on a
remaining-`c`-nonzero interior must be combined with the deeper nodes listed
in the JSON ledger.
