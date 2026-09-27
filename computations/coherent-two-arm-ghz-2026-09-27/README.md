# Two comparable arms: GHZ onset through the last attachment rank loss

**Written proof with exact supporting checks; independent audit pending.**
The unrestricted square-root rate law remains open.

[Proof](../../notes/coherent-two-arm-ghz-onset-2026-09-27.md) ·
[Illustrated guide](../../explainers/CRITICAL-DIRECTION-GEOMETRY.md) ·
[GHZ project](../../research/ghz-rates/README.md)

Near a full-support single-color six-site zero, two non-ground edges at
one center suffice for fifth-power GHZ onset whenever each edge norm
is at least a fixed fraction of the non-ground source norm.
Their matrix ranks and all other blocks are unrestricted.

The previous proof treated injective two-arm attachment maps.
This package treats the remaining shared-center rank-one pairs.
It retains the individual outside-arm sizes in the error bounds
and uses the two attachments controlled by ground equations.
If a hidden third attachment is large, the pair equations force the
other two center arms to be small. Otherwise the earlier rescaled
triangle argument applies.

Consequently, the fifth-power onset estimate is uniform away from
single-edge directions. This concerns source distance at the stated
limits; it does not give the error-versus-signal estimate needed for
the unrestricted square-root rate law.

From the repository root, with Python 3.11 or later and the standard library:

~~~sh
python3 computations/coherent-two-arm-ghz-2026-09-27/verify.py > /tmp/coherent-two-arm-ghz.json
diff -u computations/coherent-two-arm-ghz-2026-09-27/results.json /tmp/coherent-two-arm-ghz.json
python3 -O computations/coherent-two-arm-ghz-2026-09-27/verify.py > /tmp/coherent-two-arm-ghz-optimized.json
diff -u /tmp/coherent-two-arm-ghz.json /tmp/coherent-two-arm-ghz-optimized.json
~~~

The replay checks:

- Five multivariate polynomial identities certifying the scalar
  inequality steps under their listed sign hypotheses. In particular,
  the large-attachment absorption is an exact identity, not a numerical
  sample. A negative control shows why its threshold is needed.
- Polynomial coefficient identities with arbitrary block entries:
  48 single-attachment coordinates, 96 pair-response coordinates,
  the complete 64-coordinate matching split, and 64 local-factor
  identities explaining the projection. The arm entries are independent
  indeterminates, so these checks include perturbations where the
  selected singular vector is not an exact kernel vector. A dense complex fixture
  also checks the Hermitian projection and its GHZ norm.
- All 24 core-and-center choices with zero internal cofactors in the
  rank-25 ground: twelve select center anchors and twelve select leaf
  anchors. The latter have sixteen available leaf selections.
- All 45 supports consisting of two disjoint edges and all 15
  three-edge matchings, each with uncancelled four-site output.
  Thirty single-edge fixtures of both binary matrix ranks remain flat.

The analytic inverse estimates, uniform constants, and general theorem
depend on the written proof and pinned dependencies. The finite tensor
fixtures do not establish those assertions on their own.
All acceptance checks remain active in optimized Python.
