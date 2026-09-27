# Critical cores, star responses, and a GHZ normal form

**Written proofs with exact supporting checks; independent audit pending.**
These results have not been Lean-verified. The unrestricted square-root
rate law remains open.

- [Five-clique classification and stability](../../notes/flat-four-response-five-clique-2026-09-27.md).
- [Sharp star identity and binary four-core rigidity](../../notes/star-response-identity-and-binary-flat-cores-2026-09-27.md).
- [Critical support classification at rank 25](../../notes/rank25-critical-directions-2026-09-27.md).
- [Quantitative GHZ normal form and distance bounds](../../notes/ghz-critical-direction-normal-form-2026-09-27.md).
- [Illustrated guide](../../explainers/CRITICAL-DIRECTION-GEOMETRY.md) and
  [GHZ project](../../research/ghz-rates/README.md).

From the repository root, using Python 3.11 or later and its standard library:

~~~sh
python3 computations/flat-core-rigidity-2026-09-27/verify.py > /tmp/flat-core-check.json
diff -u computations/flat-core-rigidity-2026-09-27/results.json /tmp/flat-core-check.json
python3 -O computations/flat-core-rigidity-2026-09-27/verify.py > /tmp/flat-core-optimized.json
diff -u /tmp/flat-core-check.json /tmp/flat-core-optimized.json
~~~

The replay uses exact arithmetic in $\mathbb Q(\omega)$ and checks:

| Check | Scope |
| --- | --- |
| Five-clique core | Every four-site output, nontrivial local-vector fixtures, a nonzero derivative minor, insertion rank, and derivative ranks at five and six sites in one to three colors. |
| Binary four-core | Zero outputs, six invertible blocks, derivative ranks at four to six sites, and the four-site lemma with both rank-one and invertible remaining star arms. |
| Stars | Every coefficient of the Hermitian norm identity in eight size/palette cases, independent complex output fixtures, sharp cycles, and binary derivative ranks. |
| Rank-25 directions | All 2048 allowed supports, the three-leaf polynomial identity, and exact scalar realizations of all 116 surviving supports. |
| GHZ application | All 300 mixed output coordinates in a dense complex fixture, checked by two matching enumerations; cubic expansions at all three critical families. |
| Negative controls | Wrong core coefficients and signs, a forbidden outside edge, and a false stronger star constant are rejected. |

The all-size classifications and local analytic stability estimates depend
on the written proofs; finite arithmetic checks alone do not establish
them. The fifth-power distance estimate is restricted to the specified
smooth critical families. The sixth-power estimate requires quantitatively
dense five-site non-ground support.

All acceptance checks use explicit exceptions and remain active under
Python optimization. The saved receipt records code and proof hashes;
dependencies are pinned separately. No numerical search is an acceptance
input.
