# Three-arm GHZ onset and weighted extension control

**Written proof with exact supporting checks; independent audit pending.**
The unrestricted square-root rate law remains open.

[Proof](../../notes/three-arm-ghz-distance-bound-2026-09-27.md) ·
[Illustrated guide](../../explainers/CRITICAL-DIRECTION-GEOMETRY.md) ·
[GHZ project](../../research/ghz-rates/README.md)

At a full-support single-color six-site zero, three non-ground arms at
one vertex, each bounded below relative to the non-ground source norm,
suffice for the fifth-power onset estimate
$|\lambda|\le C_1\|E\|+C_2\|A-A_0\|^5$.
Matrix rank loss, vanishing remaining arms, and an entirely zero center
cofactor row are permitted. No prior closeness to a flat star is needed.

The reusable tool is a weighted five-site extension estimate. It
controls the product of an outside arm and the internal leaf
perturbation, together with the other attachments. Separate scalings
make the weights explicit. A ground-cofactor constraint excludes the
complete flat five-site source that could otherwise evade the estimate.

From the repository root, with Python 3.11 or later and the standard library:

~~~sh
python3 computations/three-arm-ghz-onset-2026-09-27/verify.py > /tmp/three-arm-ghz-onset.json
diff -u computations/three-arm-ghz-onset-2026-09-27/results.json /tmp/three-arm-ghz-onset.json
python3 -O computations/three-arm-ghz-onset-2026-09-27/verify.py > /tmp/three-arm-ghz-onset-optimized.json
diff -u /tmp/three-arm-ghz-onset.json /tmp/three-arm-ghz-onset-optimized.json
~~~

The replay checks:

- All 240 monomials in the 80 five-site extension coordinates.
- All 960 monomials in the 64 refined six-site splitting coordinates.
- The 384 remainder monomials in 32 selected mixed-output coordinates,
  including their restriction to the relevant leaf edges.
- Thirteen full-rank attachment maps across one, two, and three colors.
  A two-arm negative control verifies failure of this linear step.
- Separate internal-leaf and outside-arm scalings of every response
  coordinate and all seven weighted anchor residuals, in three examples.
- Three examples showing the leaf-only response is necessary, and three
  complete cube-root branches showing the anchor constraint is necessary.
- Forty-eight ground-anchor selections on all 24 nontrivial three-arm
  choices in the rank-25 ground example. Twenty of these choices have
  an entirely zero center cofactor row.

Acceptance checks remain active under optimized Python. The compactness
argument establishing the general weighted inequality, its neighborhood
application, and the resulting uniform GHZ theorem depend on the written
proof and pinned dependencies. Finite checks do not replace those arguments.

The remaining full-support single-color onset shapes are a single edge
and a two-arm star. The error-versus-signal estimate for the unrestricted
square-root law remains open, including on the families now controlled.
