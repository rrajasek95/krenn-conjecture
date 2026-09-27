# Balanced responses and rank-free ground-cofactor tests

**Written proof with exact supporting checks; independent audit pending.**
The unrestricted square-root rate law remains open.

[Proof](../../notes/balanced-response-ghz-onset-2026-09-27.md) ·
[Illustrated guide](../../explainers/CRITICAL-DIRECTION-GEOMETRY.md) ·
[GHZ project](../../research/ghz-rates/README.md)

After balancing two endpoint row norms, a bilinear response map has
at most one weak input direction. On its perpendicular complement,
the singular value is at least the balanced row norm divided by
the square root of two. This constant is sharp, independently of
the number of row pairs or finite local dimensions.

Refined mixed-output equations control the remaining direction in
the GHZ application. A common anchored neighbor or a four-cycle of
outside ground-cofactor anchors now proves fifth-power onset for
an edge of any matrix rank, including a pure different-color cell.
This includes every case with both endpoint cofactor rows zero.
For the displayed exact ground fixture, the cofactor tests leave
sixteen of the previous thirty projective directions. This is not
a universal count or a completed rate-law proof.

From the repository root, with Python 3.11 or later:

~~~sh
python3 -B computations/balanced-response-ghz-2026-09-27/verify.py > /tmp/balanced-response-ghz.json
diff -u computations/balanced-response-ghz-2026-09-27/results.json /tmp/balanced-response-ghz.json
python3 -B -O computations/balanced-response-ghz-2026-09-27/verify.py > /tmp/balanced-response-ghz-optimized.json
diff -u /tmp/balanced-response-ghz.json /tmp/balanced-response-ghz-optimized.json
~~~

The standard-library replay checks:

- Ninety formal Hermitian Gram entries in square and rectangular
  dimensions, plus the binary characteristic polynomial.
- Complete exact complex eigenbases in seven fixtures, including
  rank loss, rectangular spaces, a near-kernel, and the sharp gap.
- Perpendicular error estimates, the zero cross-Gram case, and
  negative controls for omitted balancing or conjugation.
- Every coefficient in the product-plus-remainder expansion and
  polynomial certificates for the scalar estimates in the proof.
- All 240 mixed quartet words: three leading matchings and twelve
  remainder matchings each, with the required internal binary edge.
- The inherited formal edge-removal and opposite-pair cancellation
  identities, and the exact cofactor graph of the ground fixture.

Acceptance checks remain active under optimized Python.
The dimension-independent norm inequalities, absorption estimates,
and compactness argument are written proofs; these finite checks
support them and do not substitute for an independent audit.
