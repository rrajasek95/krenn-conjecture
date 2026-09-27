# Uniform GHZ onset at every full-support single-color zero

**Written proof with exact supporting checks; independent audit pending.**
The unrestricted square-root rate law remains open.

[Proof](../../notes/full-support-ghz-onset-2026-09-27.md) ·
[Illustrated guide](../../explainers/FULL-SUPPORT-ONSET.md) ·
[GHZ project](../../research/ghz-rates/README.md)

Every full-support single-color six-site ground zero now has a
uniform fifth-power GHZ source-distance onset bound in every nearby
source direction, including all matrix-rank losses. No selected
cofactor, arm-size, or non-ground support condition is imposed.
The constants may depend on the fixed ground source.

One reusable ingredient is an exact identity: a flat four-cycle
whose four edge blocks have unit norm has attachment-response
Gram matrix equal to twice the identity. It works in arbitrary
finite local color dimensions. A product-one site scaling reveals
this geometry in a core whose edges originally have very different
sizes. Quartet-specific output equations then control both outside
attachments after an absorption step. This settles the two-triangle
bridge configuration.

A separate projection at a large outside edge settles any anchored
four-cycle, including a vanishing complementary edge. Together
with the existing cofactor-graph arguments, this completes the
full-support single-color onset theorem. The stronger
error-versus-signal bound and the unrestricted rate law remain open.

From the repository root, with Python 3.11 or later:

~~~sh
python3 -B computations/full-support-ghz-onset-2026-09-27/verify.py > /tmp/full-support-ghz-onset.json
diff -u computations/full-support-ghz-onset-2026-09-27/results.json /tmp/full-support-ghz-onset.json
python3 -B -O computations/full-support-ghz-onset-2026-09-27/verify.py > /tmp/full-support-ghz-onset-optimized.json
diff -u /tmp/full-support-ghz-onset.json /tmp/full-support-ghz-onset-optimized.json
~~~

The standard-library checker verifies formal unit-phase Gram
cancellations, exact complex response isometries for palettes of
sizes one through three, negative controls for the cancellation
sign and omitted balancing, all site-scale factors used in the
proof, dense complex output invariance, all sixty-four matching
splits, scalar absorption identities, and all twelve choices of
the residual root edge and largest outside edge. It also checks
the outside-edge projection, including zero complementary edges,
rank-one and rank-two projected blocks, and a negative control
showing that the projection cut matters.

Checks remain active under optimized Python. General norm estimates,
compactness, and their application to arbitrary source perturbations
are supplied by the written proof and await independent audit.
