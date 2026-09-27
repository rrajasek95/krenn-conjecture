# Two invertible arms and GHZ onset

**Written proof with exact supporting checks; independent audit pending.**
The unrestricted square-root rate law remains open.

[Proof](../../notes/two-invertible-arm-ghz-bound-2026-09-27.md) ·
[Illustrated guide](../../explainers/CRITICAL-DIRECTION-GEOMETRY.md) ·
[GHZ project](../../research/ghz-rates/README.md)

At a full-support single-color six-site zero, two binary non-ground
arms at one vertex suffice for fifth-power GHZ onset when both smaller
singular values are bounded below relative to the non-ground source norm.
Other blocks are unrestricted, no prior closeness to a star is needed,
and the center cofactor row may vanish.
One invertible arm also suffices if one of its endpoints has a nonzero
ground cofactor row and the second arm has comparable norm.

The proof uses a singular-value estimate for a sum of two tensor
products with different pairings of the sites. The estimate transfers
a controlled attachment at a core leaf to both its companion attachment
and a product involving the outside arm. It also gives a complete
classification of the two-arm attachment kernel.

From the repository root, with Python 3.11 or later and the standard library:

~~~sh
python3 computations/two-arm-ghz-onset-2026-09-27/verify.py > /tmp/two-arm-ghz-onset.json
diff -u computations/two-arm-ghz-onset-2026-09-27/results.json /tmp/two-arm-ghz-onset.json
python3 -O computations/two-arm-ghz-onset-2026-09-27/verify.py > /tmp/two-arm-ghz-onset-optimized.json
diff -u /tmp/two-arm-ghz-onset.json /tmp/two-arm-ghz-onset-optimized.json
~~~

The exact replay checks:

- All 960 monomials in 64 six-site matching identities and all 432
  monomials in 144 attachment and outside-edge quartet identities.
- Fourteen two-arm response maps over one, two, and three colors,
  including six explicit vectors spanning the predicted hidden kernels
  in the dense common-direction examples.
- Twenty singular-value inequality examples, using exact rational
  singular values and exact complex unitary changes of basis.
- Three sharp smaller-singular-value examples and the limiting rank-one
  example where the response vanishes despite nonzero blocks.
- All 24 core-and-center choices without internal ground cofactors
  in the rank-25 fixture: twelve have a zero center row. The replay
  exercises twelve center-anchor and twenty-four leaf-anchor selections.
  With only one arm invertible, it verifies the additional endpoint-row
  condition in 40 of the 48 placements, retaining the eight uncovered cases.

All acceptance checks remain active under optimized Python. The general
matrix inequality, kernel classification, and uniform GHZ estimates
depend on the written proof and pinned dependencies. Finite examples
do not replace these arguments.

The remaining onset shapes are single edges and two-arm stars with a
rank-one arm. The error-versus-signal bound required for the universal
square-root law remains open, including on the families now controlled.
