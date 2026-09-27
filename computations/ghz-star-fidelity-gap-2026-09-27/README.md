# Star fidelity gaps and necessary boundary support

**Written proof with exact supporting checks; independent audit pending.**
The unrestricted square-root rate law remains open.

[Proof](../../notes/ghz-star-fidelity-gap-2026-09-27.md) ·
[Illustrated guide](../../explainers/GHZ-STAR-FIDELITY-GAP.md) ·
[GHZ project](../../research/ghz-rates/README.md)

Extracting the highest coefficient of the existing approximate rotation
identity gives an explicit error-versus-signal bound whenever a same-color
star product is nonzero. It excludes all full-support single-color zeros
as high-fidelity limits, at every even size at least four.

A further necessary condition applies to arbitrary endpoint-color blocks:
at every root, for each pair of receiving colors, some incident block must
have both receiving columns zero in any high-fidelity limit. This condition
is not sufficient for approaching perfect fidelity.

From the repository root, with Python 3.11 or later:

~~~sh
python3 -B computations/ghz-star-fidelity-gap-2026-09-27/verify.py > /tmp/ghz-star-fidelity-gap.json
diff -u computations/ghz-star-fidelity-gap-2026-09-27/results.json /tmp/ghz-star-fidelity-gap.json
python3 -B -O computations/ghz-star-fidelity-gap-2026-09-27/verify.py > /tmp/ghz-star-fidelity-gap-optimized.json
diff -u /tmp/ghz-star-fidelity-gap.json /tmp/ghz-star-fidelity-gap-optimized.json
~~~

The standard-library checker uses exact Gaussian and Eisenstein rational
arithmetic. It verifies highest-degree identities with complex phases,
literal divided response coefficients at four, six, and eight sites,
the six star products of the rank-25 ground fixture, support-test controls,
and the fidelity certificate on exact sources. A perfect four-site GHZ
source passes the necessary support test, while a zero-output off-color
star shows why checking only diagonal cells is weaker. Incorrect rotation
and complex-denominator factors and singleton factorials are rejected.

The inequalities and limit arguments for arbitrary sources and all even
sizes are proved in the note. Finite fixtures are supporting checks.
No new independent audit or Lean certification is claimed. Prior dated
packages remain unchanged.
