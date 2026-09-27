# Triangle attachments and GHZ onset

**Written proof with exact supporting checks; independent audit pending.**
The unrestricted square-root rate law remains open.

[Proof](../../notes/triangle-attachment-ghz-bound-2026-09-27.md) ·
[Illustrated guide](../../explainers/CRITICAL-DIRECTION-GEOMETRY.md) ·
[GHZ project](../../research/ghz-rates/README.md)

Near every full triangle critical direction at a full-support single-color
six-site zero, the GHZ signal satisfies
$|\lambda|\le C_1\|E\|+C_2\|A-A_0\|^5$.
This includes all matrix and triangle-response rank loss.
The remaining shapes for this onset estimate are stars with at most
three arms. The error-versus-signal inequality needed for the rate law
is a separate open question.

Two ideas make the proof work. A missing cofactor-anchored edge obstructs
an exactly flat five-site extension, giving control of products of
attachment sizes. Two outside sites also share an anchored core component.
Their remaining hidden directions have a fixed local factor; an
orthogonal projection removes their output while retaining unit norm
from the binary GHZ target.

From the repository root, using Python 3.11 or later and the standard library:

~~~sh
python3 computations/triangle-ghz-onset-2026-09-27/verify.py > /tmp/triangle-ghz-onset.json
diff -u computations/triangle-ghz-onset-2026-09-27/results.json /tmp/triangle-ghz-onset.json
python3 -O computations/triangle-ghz-onset-2026-09-27/verify.py > /tmp/triangle-ghz-onset-optimized.json
diff -u /tmp/triangle-ghz-onset.json /tmp/triangle-ghz-onset-optimized.json
~~~

The exact replay checks:

- All 960 monomials in 64 six-site splitting identities.
- All 432 monomials in 144 pair-attachment quartet identities and all
  144 monomials in 48 single-attachment identities.
- Eleven triangle response fixtures over one, two, and three colors,
  with all 33 maps obtained by fixing a core component. They include
  full-response kernels of dimensions zero, one, and two.
- The common-anchor selection on all eight zero-cofactor triangles in
  a full-support ground example, and the required five-site anchors.
- The local-factor cancellation on all 64 coordinates of a dense
  complex output and the GHZ projection norm in four local directions.
- Exact output, response, anchor, and norm calculations for an auxiliary
  family at four rational parameter values. This illustrates why
  controlling the entire output from the auxiliary bounds would fail.

Acceptance checks remain active under optimized Python. The general
pair coercivity, singular-value neighborhood estimates, and compactness
arguments depend on the written proof and its pinned dependencies.
These finite checks do not replace those arguments.
