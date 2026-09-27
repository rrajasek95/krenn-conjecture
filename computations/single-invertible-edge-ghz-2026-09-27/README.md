# A single invertible edge and a sharp target projection

**Written proof with exact supporting checks; independent audit pending.**
The unrestricted square-root rate law remains open.

[Proof](../../notes/single-invertible-edge-ghz-onset-2026-09-27.md) ·
[Illustrated guide](../../explainers/CRITICAL-DIRECTION-GEOMETRY.md) ·
[GHZ project](../../research/ghz-rates/README.md)

Near a full-support single-color six-site zero, a single binary edge
whose smaller singular value is bounded below relative to the
non-ground source norm suffices for fifth-power GHZ onset.
All other edges may become arbitrarily small.
Together with the two-arm theorem, the estimate is uniform away
from single rank-one edge directions.

Three useful ingredients are proved:

- An exact edge-removal identity bounds GHZ amplitude by output
  error plus the product of the four-site response norm and the
  norm of edges disjoint from the selected edge.
- Two bilinear responses with a well-conditioned cross matrix
  control the output up to one rank-one matrix factor. That factor
  is a direction along which the cross matrix's determinant stays
  constant.
- Projecting away the corresponding two-dimensional tangent plane
  retains squared norm at least $1/2$ from the unnormalized binary
  GHZ tensor, whose squared norm is two. Thus at least one quarter
  of its original squared norm remains. This constant is sharp.

From the repository root, using Python 3.11 or later and the standard library:

~~~sh
python3 computations/single-invertible-edge-ghz-2026-09-27/verify.py > /tmp/single-invertible-edge-ghz.json
diff -u computations/single-invertible-edge-ghz-2026-09-27/results.json /tmp/single-invertible-edge-ghz.json
python3 -O computations/single-invertible-edge-ghz-2026-09-27/verify.py > /tmp/single-invertible-edge-ghz-optimized.json
diff -u /tmp/single-invertible-edge-ghz.json /tmp/single-invertible-edge-ghz-optimized.json
~~~

The exact replay checks:

- All 64 coordinate identities for edge removal and for cancellation
  of the large opposite-edge product, with all 960 output monomials
  represented by independent source-entry indeterminates.
- The two determinant-tangent lines, the opposite determinant sign,
  the norm-selection identity, and the sharp scalar quarter bound,
  as polynomial coefficient identities.
- Fourteen dense complex tangent planes, the sharp GHZ projection
  example, and a non-tangent plane that removes the entire target.
- Nine exact local Gram spectra and three complex tangent-compression
  identities used in the analytic estimates.
- Four auxiliary examples where a uniform whole-output bound fails
  but removing the rank-one factor restores control.
- Three polynomial identities for opposite cofactor weights and all
  fifteen distinguished edges in the rank-25 ground fixture: four
  anchored edges, ten cases with a nonzero endpoint row, and one
  case with zero endpoint rows and a four-cycle of outside anchors.

All acceptance checks survive optimized Python.
The general inequalities, compactness corollary, and GHZ theorem
also require the written proof and pinned dependencies.
Finite examples alone do not establish them.

Single rank-one edge directions and the error-versus-signal inequality
remain open. The theorem does not complete the unrestricted rate law.
