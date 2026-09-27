# Flat-support classification and a rank-independent star bound

**Written proofs with exact supporting checks; independent audit pending.**
The unrestricted GHZ square-root law remains open.

[Support classification](../../notes/four-site-flat-support-classification-2026-09-27.md) ·
[Star bound and GHZ consequence](../../notes/rank-free-star-response-bound-2026-09-27.md) ·
[Illustrated guide](../../explainers/CRITICAL-DIRECTION-GEOMETRY.md) ·
[GHZ project](../../research/ghz-rates/README.md)

For every palette and site count, four-site-flat sources are stars,
sources on at most four active sites satisfying the four-site equation,
or isolated cube-root five-cores. A quantitative estimate controls all
leaf blocks of a star with at least five nonzero arms using only arm
norms, with no matrix-invertibility requirement.

This extends the first critical-direction support reduction to every
full-support single-color six-site zero, and extends the fifth-power
source-distance bound through matrix rank loss in spanning stars.
The constants can still deteriorate as an arm disappears.

From the repository root, with Python 3.11 or later and the standard library:

~~~sh
python3 computations/flat-support-structure-2026-09-27/verify.py > /tmp/flat-support.json
diff -u computations/flat-support-structure-2026-09-27/results.json /tmp/flat-support.json
python3 -O computations/flat-support-structure-2026-09-27/verify.py > /tmp/flat-support-optimized.json
diff -u /tmp/flat-support.json /tmp/flat-support-optimized.json
~~~

The replay checks, in exact $\mathbb Q(\omega)$ arithmetic:

- The tensor-lifting identity and every step of its norm inequalities on
  six fixtures with identity, rank-one, and mixed-rank arms.
- A six-leaf complex fixture for the all-size coefficient.
- Symmetric tensor norms against an independently computed Gram permanent.
- The full star derivative rank on five one- or two-color fixtures,
  including stars whose every arm has rank one.
- All 32768 six-site support graphs and exact scalar constructions for
  every one of the 348 surviving supports.
- A four-leaf counterexample to extending the rank-independent estimate
  below its stated five-leaf threshold.

The universal claims depend on the written proofs as well as these finite
checks. The support rejection rules implement the graph lemmas; they are
not an independent algebraic solver. All checks remain active under
optimized Python. Code, proof, and dependency hashes are recorded beside
this README.
