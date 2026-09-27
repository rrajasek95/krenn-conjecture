# Two-arm GHZ onset beyond matrix invertibility

**Written proof with exact supporting checks; independent audit pending.**
The unrestricted square-root rate law remains open.

[Proof](../../notes/transverse-two-arm-ghz-onset-2026-09-27.md) ·
[Illustrated guide](../../explainers/CRITICAL-DIRECTION-GEOMETRY.md) ·
[GHZ project](../../research/ghz-rates/README.md)

Near a full-support single-color six-site zero, the fifth-power estimate
$|\lambda|\le C\varepsilon+C\delta^5$ holds whenever the two-arm attachment
map has smallest singular value bounded below relative to the non-ground
source norm. Here $\lambda$ is the GHZ amplitude, $\varepsilon$ is output
error, and $\delta$ is source distance to the fixed zero.
This covers one invertible arm without an endpoint-cofactor condition,
and two rank-one arms with different center lines.

Near two rank-one arms sharing a center line, the proof instead gives
$|\lambda|\le C\varepsilon+C\delta^5+Ct\beta^2$, where $t$ is the
non-ground source norm and $\beta$ is the norm of the edge between the
two leaves. The extra term is controlled if $\beta=O(\delta^2)$ or
$\beta^2=O(\varepsilon)$.

The proof rescales a weak closing edge to obtain a nondegenerate triangle.
A mixed-output bound involving only the leaf quartet retains the correct
small scale. A local projection removes a potentially larger product
output while retaining a fixed part of the GHZ signal. At shared-center
pairs, a complementary response map bounds the remaining contribution.

From the repository root, with Python 3.11 or later and the standard library:

~~~sh
python3 computations/transverse-two-arm-ghz-2026-09-27/verify.py > /tmp/transverse-two-arm-ghz.json
diff -u computations/transverse-two-arm-ghz-2026-09-27/results.json /tmp/transverse-two-arm-ghz.json
python3 -O computations/transverse-two-arm-ghz-2026-09-27/verify.py > /tmp/transverse-two-arm-ghz-optimized.json
diff -u /tmp/transverse-two-arm-ghz.json /tmp/transverse-two-arm-ghz-optimized.json
~~~

The exact replay checks:

- Two-arm maps over one, two, and three colors, including shared-center
  kernels, complementary-map injectivity, and a wrong-sign negative control.
- Rescaling weights for all 960 six-site binary matching monomials and
  720 quartet monomials.
- All three leaf-quartet expansions: 144 leading and 576 mixed-remainder
  terms, with neither strong arm in the remainder.
- A complex 64-coordinate projected permanent identity, twelve binary
  GHZ projection identities, and removal of a shared-direction permanent.
- All 24 core-and-center choices with zero internal cofactors in the
  rank-25 ground fixture. The common-anchor argument covers all 48
  one-invertible-arm placements, including the eight omitted by the
  earlier endpoint-row condition.
- Four exact members of an auxiliary family whose product output has
  order $\delta^{19/4}$ and is killed by the local projection. It is
  not a GHZ counterexample.

All acceptance checks survive optimized Python. The uniform inequalities
and general classification rely on the written proof and pinned
dependencies; finite checks do not replace those arguments.

The remaining onset shapes at these full-support single-color limits
are single edges and pairs of rank-one arms sharing a center line.
The error-versus-signal inequality required for the unrestricted rate
law remains open even on the families whose onset is controlled.
