# X4 all-blocked adversarial builder — report

Status: **UNAUDITED exact structured sublemma; no all-blocked X4 source was
constructed.** This is not evidence for the universal `X4 => active clean
cap` target.

## Terminal result

Let `A` be W40's integral level-4 point. In the 252 endpoint-ordered source
coordinates, the raw level-4 Jacobian at `A` has rank 240 over `Q`. A stored
240-by-240 minor has determinant `2^33`. The normalized diagonal-gauge orbit
has tangent rank 12 (a rank minor has determinant `-1`), and direct exact
multiplication gives `Jacobian * gauge_tangent = 0`. Thus over characteristic
zero the level-4 scheme is smooth of dimension 12 at `A`, and its local germ
is the gauge orbit. Since active-cap existence is gauge invariant, no local
level-4 deformation of this point can be an all-blocked falsifier.

The stronger fixed-cell transversal calculation also has full rank: after
holding the 20 nonzero cells of `A` fixed, the Jacobian on all 232 zero-cell
coordinates has rank 232, with minor determinant `-2^33`. In particular, none
of the 232 one-coordinate support extensions survives even infinitesimally.

These rank claims hold in characteristic zero and every odd characteristic;
characteristic 2 is not decided by the displayed minors.

## Mandatory calibrations

- W25-F8 was evaluated on all 6,561 words by explicit-matching and bitmask-DP
  engines. It has pures `(1,1,1)`, passes X3, fails X4 in 78 level-4 rows,
  and all 21 live pairs are cap-blocked by exact Qbar Rabinowitsch saturation.
- W40-B was independently evaluated on all 6,561 words by the same two raw
  engines. It passes all 4,881 level-4 rows and fails only three off-count-5
  rows. Exact Qbar saturation gives 7 active and 10 blocked live pairs;
  `(67, K=I_3)` has activity product one and zero clean-error polynomial.
- The must-fire mutation `q26=-1 -> +1` breaks four raw level-4 rows over Q.
- Both Jacobian engines agree; all declared controls executed.

The precise residual is therefore: an all-blocked X4 falsifier over `C`, if
one exists, must occur on a different irreducible component or at a remote or
singular locus; it cannot be obtained by locally deforming the known W40
point. Full machine-readable results and every per-pair Qbar decision are in
`results_builder.json`.
