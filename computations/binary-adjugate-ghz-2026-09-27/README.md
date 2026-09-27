# Binary adjugate responses and same-color onset control

**Written proof with exact supporting checks; independent audit pending.**
The unrestricted square-root rate law remains open.

[Proof](../../notes/binary-adjugate-ghz-onset-2026-09-27.md) ·
[Illustrated guide](../../explainers/CRITICAL-DIRECTION-GEOMETRY.md) ·
[GHZ project](../../research/ghz-rates/README.md)

The binary adjugate contraction of a six-site output is an exact
quadratic expression in four-site responses. Its norm is at most
one half of the local squared response norm, with a sharp constant.
For an approximate binary GHZ output this gives a directly computable
amplitude/error certificate.

At a full-support single-color six-site zero, any same-color binary
edge component bounded below relative to the non-ground source norm
therefore gives fifth-power onset. Matrix rank is unrestricted.
Combined with the earlier two-arm and single-invertible-edge results,
the estimate is uniform away from thirty projective directions:
one edge cell joining different pure colors at its endpoints.

The identity uses the existing determinant mechanism from the
[older cap-adjugate note](../../notes/cap-adjugate-six-boundary-identity.md).
This package records its binary norm bound and onset application;
it does not claim priority for the rank-one determinant identity.

From the repository root, with Python 3.11 or later and the standard library:

~~~sh
python3 computations/binary-adjugate-ghz-2026-09-27/verify.py > /tmp/binary-adjugate-ghz.json
diff -u computations/binary-adjugate-ghz-2026-09-27/results.json /tmp/binary-adjugate-ghz.json
python3 -O computations/binary-adjugate-ghz-2026-09-27/verify.py > /tmp/binary-adjugate-ghz-optimized.json
diff -u /tmp/binary-adjugate-ghz.json /tmp/binary-adjugate-ghz-optimized.json
~~~

The exact replay checks:

- All 240 coefficient identities: fifteen choices of distinguished
  edge and sixteen outside words, using independent source-entry
  indeterminates and 12,960 contraction monomials.
- Negative controls for the determinant sign, adjugate transpose,
  and the two orders of each complementary pair.
- Sixty exact norm and target-sensitivity certificates on dense
  complex sources and an exact binary GHZ cycle. Square-root
  comparisons are reduced to rational inequalities.
- A sharp example for the constant $1/2$ in the local response bound.
- Forty-five rank-one single-edge fixtures seen by the same-color
  criterion, fifteen diagonal-blind invertible edges, and all thirty
  remaining different-color axes.

All acceptance checks remain active in optimized Python.
The norm inequality and compactness argument also depend on the written
proof; finite fixtures alone do not establish the general theorem.
The remaining axes have zero output, so they are not counterexamples.
Their perturbations and the required error-versus-signal bound remain open.
