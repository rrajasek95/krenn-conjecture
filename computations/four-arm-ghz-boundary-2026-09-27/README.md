# GHZ onset through the loss of a star arm

**Written proofs with exact supporting checks; independent audit pending.**
The unrestricted square-root rate law remains open.

[Four-arm kernel classification and response bounds](../../notes/four-arm-star-response-2026-09-27.md) ·
[GHZ fifth-power distance theorem](../../notes/four-arm-ghz-distance-bound-2026-09-27.md) ·
[Illustrated guide](../../explainers/CRITICAL-DIRECTION-GEOMETRY.md) ·
[GHZ project](../../research/ghz-rates/README.md)

A four-arm star has zero, one, or two hidden leaf-response directions,
with a complete classification by its arm ranks and center color lines.
The one-dimensional case has a sharp square-root response-to-distance
bound. The two-dimensional case has actual five-core branches; controlling
one leaf edge removes them.

The GHZ mixed-output equations supply that extra edge control.
Near any full-support single-color six-site zero, the fifth-power
source-distance bound therefore holds whenever four non-ground arm norms
stay a fixed fraction of the total non-ground source norm. The fifth
arm may vanish, and no matrix invertibility is required.

From the repository root, with Python 3.11 or later and the standard library:

~~~sh
python3 computations/four-arm-ghz-boundary-2026-09-27/verify.py > /tmp/four-arm-ghz.json
diff -u computations/four-arm-ghz-boundary-2026-09-27/results.json /tmp/four-arm-ghz.json
python3 -O computations/four-arm-ghz-boundary-2026-09-27/verify.py > /tmp/four-arm-ghz-optimized.json
diff -u /tmp/four-arm-ghz.json /tmp/four-arm-ghz-optimized.json
~~~

The exact $\mathbb Q(\omega)$ replay checks:

- Derivative ranks and complete hidden-kernel dimensions on 24 size/palette
  fixtures, including dense leaf factors, singular rank-two arms, and all
  possible center-line patterns in the theorem.
- Explicit kernel vectors and every coefficient of their quadratic response.
- The sharp two-pair example at five rational scales and exact five-core
  branches in the common-center kernel.
- The anchored kernel inequality on 25 complex fixtures.
- All 80 mixed output coordinates with the center grounded, all 64 binary
  root-expansion coordinates, and both corresponding norm bounds.
- Cofactor selection on two full-support zero-ground fixtures, including
  the rank-25 boundary.

The universal kernel classification, neighborhood estimates, and compactness
argument depend on the written proofs. Finite fixtures do not replace them.
All acceptance checks remain active under optimized Python. Proof, code,
and dependency hashes are recorded beside this README.
