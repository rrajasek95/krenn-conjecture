# Attachments to four-site cores and GHZ onset

**Written proof with exact supporting checks; independent audit pending.**
The unrestricted square-root rate law remains open.

[Proof](../../notes/four-core-attachment-ghz-bound-2026-09-27.md) ·
[Illustrated guide](../../explainers/CRITICAL-DIRECTION-GEOMETRY.md) ·
[GHZ project](../../research/ghz-rates/README.md)

At a flat four-site core that is not a star, every attachment to a new
site is detected linearly, except at a coherent cube-root core.
There the kernel has one degree of freedom per new-site color, and
fixing any one attachment block removes it. The classification allows
any finite palette and arbitrary internal singularities.

In the six-site GHZ problem, ground-cofactor constraints provide the
extra control. This gives a fifth-power source-distance onset bound
near every such core. Combined with the star result, the estimate is
uniform away from triangles and stars with at most three arms.
It is not the error-versus-signal estimate required for the rate law.

From the repository root, using Python 3.11 or later and the standard library:

~~~sh
python3 computations/four-core-attachments-2026-09-27/verify.py > /tmp/four-core-attachments.json
diff -u computations/four-core-attachments-2026-09-27/results.json /tmp/four-core-attachments.json
python3 -O computations/four-core-attachments-2026-09-27/verify.py > /tmp/four-core-attachments-optimized.json
diff -u /tmp/four-core-attachments.json /tmp/four-core-attachments-optimized.json
~~~

The exact replay checks:

- All coefficients in the six-variable attachment determinant identity.
- Attachment ranks in 26 fixtures over one, two, and three colors,
  including missing edges, arbitrary extra diagonal blocks, invertible
  cores, and rank-one blocks with different local directions.
- Explicit exceptional kernel vectors and all 24 single-block augmented
  rank checks, including dense complex local directions.
- All coefficients in 64 six-site splitting identities (960 monomials)
  and 96 outside-edge quartet identities (288 monomials).
- A dense complex evaluation of the tensor identity and its norm bound.
- Both attachment anchors in two four-site subsets of the rank-25
  ground example with no usable internal cofactor.

All acceptance checks remain active under optimized Python. The general
attachment classification, neighborhood estimates, and compactness argument
depend on the written proof and its pinned dependencies; finite rank
fixtures do not replace them. No internal smoothness classification is claimed.
