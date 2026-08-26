# Branch0 all-offdiagonal support-stratum audit

Status: all four canonical proper `Cprod=0` boundary types are now closed
exactly/pairwise; the true cycle interior and the corrected `k=5,6` interiors
remain unresolved.
This lane stratifies the six edges on which both diagonal
entries `a_e,d_e` are nonzero after solving the permanent equation as
`c_e=-(1+a_e*d_e)/b_e`.  It retains the `c_e=0` boundary: only pure `H`, all
six `b_e`, and the selected `a_e*d_e` products are localized.  For hard
complement strata the true all-offdiagonal selected-term interior also
localizes `product(1+a_e*d_e)`, equivalently all selected `c_e`.  Its
complement is a union of partial `c_e=0` faces.  Each face changes the live
permanent term only on those edges and therefore needs its own joint
`(branch,term)` orbit reduction; it is not automatically an all-six aligned
chart.  Results proved without this fourth localizer are stronger.

No conclusion is inferred from a timed-out Gröbner calculation.

## Exact routing interfaces

`build_support_strata_interface.py` rebuilds the literal branch-0 packet for
the 11 `S4`-orbits of both-live edge supports.  Its current logical digest is
`96cc31f95394eb49f6008998336144ee9c6dda00055cb7c77cdcf939cd1aa351`.

`build_recursive_joint_face_interface.py` corrects the earlier boundary
overclaim.  A state records cofactor branch `B`, selected permanent term `T`,
and remaining both-live support `D`.  The exact boundary move is
`(B,T,D) -> (B,T xor e,D-e)`.  The 729 labelled ternary edge states have 66
`B4` orbits, with both-live-degree histogram
`{0:11,1:14,2:18,3:14,4:6,5:2,6:1}`.  The four hard starts
`15,30,31,63` reach 43 joint orbits including themselves; only four of those
are aligned terminals.  Logical digest:
`a3a6fbc330aa06791417a3c06e1779de7c15b070ca734b657f4ed0c9b1311ac7`.

## Exact units through degree four

The independently checked lower-support results are:

- `k=1`, both `k=2` types, and the `k=3` star have exact serialized source
  lifts in root's frozen easy-strata artifact
  `results_branch0_both_live_easy_strata.json` (result digest
  `71896910025164afcb24015d655cb252bd9e911cdaa744555a16b6f438553bea`).
- The `k=3` path has an exact-Q unit basis there, but no serialized source
  multiplier lift.
- The `k=3` triangle has a smaller independent exact certificate after the
  lossless site-torus gauge.  Ten literal source rows plus only the all-`b`
  localizer have basis `[1]`; `H`, selected `a*d`, and every `c` factor are
  not localized.  Deleting raw row 6 fires modulo 1009.  The result digest is
  `507614bf88c7a84fb693403a4357246b012966e0429b4675e5f14b0ea8b1ce54`.
- The `k=4` triangle-plus-pendant support is UNIT modulo both 1009 and 1013
  using all 16 surviving literal rows and only the all-`b` localizer.  The
  direct exact-Q calculation timed out at 300 seconds, so this remains a
  modular lead, not a characteristic-zero theorem.  The source-rebuilt
  three-mode artifact has logical digest
  `0459ac0ed7b8954cce1fbf87e1da8c02961bddce2024485b3b2486d5f9241ff3`.
  Its bounded single-deletion census has 10 UNIT deletions, one exact
  finite-field NONUNIT deletion (row 6), and five timeouts (logical digest
  `2b0d0ed5604e61705fdc54ef02584faab95074fd7773ca627bac5f17ef23bc73`).

## Four-cycle boundary and unresolved interiors

The displayed characteristic-zero four-cycle family was independently
replayed from a different raw row map: all 22 packet rows vanish, `H=4`, and
all four selected `1+a_e*d_e` vanish.  Exactly this all-four-zero face maps
to aligned `(branch,term)=(0,33)` (16 actions).  Result digest:
`1382e568152ab07573b4db10efe35d83aa0c42db5813d1c26398fe2562e950c1`.

This does **not** close a general `Cprod=0` boundary.  A proper subset of
zero `c_e` leaves a nonempty both-live support and follows the 66-orbit
recursive interface above.  The true cycle interior with all selected `c_e`
nonzero remains unresolved; direct single-factor and product saturation
attempts timed out.  The corrected `k=5` and `k=6` interiors also have no
exact or modular verdict yet.  No result is inferred from those timeouts.

## Canonical proper boundary types

`build_recursive_face_charts.py` independently rebuilds the four canonical
proper cycle-boundary charts directly from all 22 raw packet rows, specializes
their permanent terms, and applies only a lossless site-torus gauge.  Each
chart retains 16 nonzero literal source rows.  Logical digest:
`3719f6b82980f3f2b968c9f8402658de125bce97176dafac4849741de97064d1`.

Three of the four priority types are now closed exactly over `Q`:

- `(0,13,1)` is empty after localizing only its selected base terms and its
  remaining `c` numerators.  The homogeneous source ideal contains `t^6`;
  a 14-term literal source multiplier ledger is serialized.  Neither `H` nor
  the both-live `a*d` product is localized.
- `(0,15,3)` is empty under the same stronger localization.  Its homogeneous
  source ideal contains `t^8`, while `t^7` has nonzero remainder.  The full
  multiplier lift timed out at 300 seconds and is explicitly not claimed;
  the exact basis/remainder theorem is rebuilt from all 16 labelled rows.
  Both unit results are three-mode stable with common logical digest
  `1adc0b76fcce32afb9f0f400c2247a8753e278b60cd11360f96e18a188001141`.
- `(0,30,12)` is not empty.  The full localized 16-row ideal is exactly equal
  (mutual exact Gröbner reductions) to a nine-relation presentation plus the
  unchanged localization equation; both bases have size 16 and dimension 1.
  It is the rational `r`-family with
  `q=r^2-2r-1`, open set `r*(r-2)*q != 0`, and `H=4*r*(r-2)`.
  The generic signature has `|X|=16`, `|C|=12`, and all 16 `Q` coordinates
  live.  Therefore compatibility forces every `Q` coordinate of an arbitrary
  mate to zero; the independently rebuilt polarized pure-`H` identity then
  forces the mate's `H` to zero.  Classification logical digest
  `b21d9ee4cc4b1a68bd6acc99809186ea4cb4099e69dc253da7d6caca192299c5`;
  signature/mate digest
  `d4263fffea8545c4921f04c2b3a8ff2bce8907d081f567c1c40061c23f00b4e3`.

The fourth and final proper type, `(0,31,13)`, is now empty over
characteristic zero.  The canonical coefficient-first input uses raw rows
`7,8,12,...,21` and the explicit Rabinowitsch equation

```
s*a5*b3*b4*(1+a0)*(1+a2*d2)*(1+a3*d3)-1.
```

Thus it localizes only the selected base terms and the three remaining
`c`-numerators; neither `H` nor the both-live `a*d` product is localized.
msolve 0.10.1 returns exactly `[-1]:`, parsed as an empty degree-zero result
in twelve variables.  Every source row and the expanded Rabinowitsch row are
independently replayed from both the literal strings and rational term ledger
under standard, `-O`, and `-I-S` modes.  The exact input SHA-256 is
`652183de1427c09053bdb5aeb1fbd67c619321f88c0da5fbb418acd3d1159f9e`;
the output SHA-256 is
`0333251e6ebb3890ef547f522ec55f27f0cef9a860998757e31f3e1b819e7490`;
the msolve manifest logical digest is
`091f7f6545494efaffb2291a63c83263b578d3b599bc9974f634449070369138`;
and the three replay digests are
`48617e0ab6931d9481eaee55fddaca57fc6efe0263d881426e531cffdda5470c`,
`fc5bc8b436cb637d36c4e7c246b097212137f1ba17a6cb073a159db999af2ba4`,
and `b442419864ad0e2b322c3ea976d5df1265509b35fdfd6b5e978eb1cca8ec5483`.
The full ledger is
`computations/unaudited-codex-face03113-reverse-2026-08-21/REPORT.md`.

Consequently all four canonical proper boundary types are closed in the
pairwise packet problem: `(0,13,1)` and `(0,15,3)` are empty, `(0,30,12)` is
the exact rational family whose full `Q`-support forces every mate's `H` to
zero, and `(0,31,13)` is empty over characteristic zero.  This statement is
only about the proper recursive `Cprod=0` faces; it does not close the true
all-`c`-nonzero cycle interior or the `k=5,6` interiors.

## k5/k6 recursive boundary reduction

The complete proper-boundary routing for the k5 and k6 starts is now frozen
without running an algebraic solve. All 31 labelled k5 zero-`c` subsets give
13 B4 states; all 63 labelled k6 subsets give 10 states. Only the aligned
leaves `0:1:0` and `0:0:0` respectively map to already exact-Q units. None
of the other 21 states is B4-equivalent to a frozen easy all-offdiagonal
k<=3 stratum or one of the four exact/pairwise cycle-boundary keys.

For broad-face attacks, the minimal k5 boundary antichain is `0:31:15`
(triangle-plus-pendant support, labelled multiplicity 4) and `0:31:30`
(four-cycle, multiplicity 1). The unique k6 first boundary is the new k5
chart `0:31:31` (multiplicity 6), whose next split is `0:15:15`
(triangle-plus-pendant, multiplicity 12) and `0:30:30` (four-cycle,
multiplicity 3). The full k5/k6 interiors `0:63:31`, `0:63:63` remain open.
The exact ordinary TP `P26=0` result is only a determinant subbranch and is
not counted as closure of any new joint face.

The full 94-entry covariance ledger, all descendant keys, and explicit B4
witnesses are in
`../unaudited-codex-k56-boundary-routing-2026-08-21/REPORT.md`; producer
logical digest
`4c2175b1f2afd7b6fb868117afbbc1d31fe930d9d58e6823273c659b9489f00a`.

The first bounded gate on the minimal k5 TP-type face `0:31:15` used its
literal torus-normalized 12-row square reverse core and the complete exact
live-factor product. Native F4SAT at `p=1073741827` timed out after 300.268
seconds with zero basis output. No UNIT/NONUNIT, dimension, or component
claim is made, and no second formulation was run. The exact source and
timeout ledger are in
`../unaudited-codex-face03115-modular-lead-2026-08-21/REPORT.md`.

## Frozen file hashes

- `results_support_strata_interface.json`:
  `d08a06e5db49c37070b8e9b9ad3801d3cc76efc3f73ad8d2b149fc519cf00138`
- `results_recursive_joint_face_interface.json`:
  `b347c3eafde2e242c6052300e404696ef93a633736836ef4cb2a70debdce03d3`
- `results_triangle_compact_unit_referee.json`:
  `57d5488deab0986e0560c7c776ddb9de0e293894af4cbba52d32ef772603bac1`
- `results_cycle_boundary_family_referee.json`:
  `c59a5452b1af050d68674d5d36c28d5c425b6f048b5ccc7e5c7bc1b50b0be81c`
- `results_k4_triangle_pendant_modular_lead.json`:
  `22c488638a3e62a26f8e3023d8229b4d8655bef9aa45c0ffdef26e9132dc08aa`
- `results_recursive_face_charts.json`:
  `772696c89c9c482c418c93daf0750819be86a23ab847fcf40edb03d1597587cf`
- `results_recursive_face_exact_units.json`:
  `a56cc060448d8601a68cecebb2acbb208f14f4e9ac491f8703b7864876909a85`
- `results_face_03012_component_classification.json`:
  `afe08f7824d66eeb654da6a9e3594c7b54054c8e316ecb03c49665f349476a2d`
- `results_face_03012_component_signature.json`:
  `f1fe8f0d675f40e204c027b2ef97a1395a17d6fafde9078da295c487323bedcd`
- `results_face_03113_modular_lead.json`:
  `9bc9bcd69427c0cd5a7fe624646aabbbc2c99fe3a7ae33cea6a4ec36495d24f1`
- exact `(0,31,13)` characteristic-zero input:
  `652183de1427c09053bdb5aeb1fbd67c619321f88c0da5fbb418acd3d1159f9e`
- exact `(0,31,13)` empty output:
  `0333251e6ebb3890ef547f522ec55f27f0cef9a860998757e31f3e1b819e7490`
- exact `(0,31,13)` msolve logical manifest:
  `091f7f6545494efaffb2291a63c83263b578d3b599bc9974f634449070369138`
