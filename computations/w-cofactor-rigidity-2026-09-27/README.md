# Cofactor rigidity and W optimality near maximum response

**Written proofs with exact supporting checks; independent audit pending.**
The unrestricted exact W optimum remains open.

[Proof](../../notes/w-cofactor-rigidity-2026-09-27.md) ·
[Illustrated guide](../../explainers/W-GLOBAL-GUARANTEE.md) ·
[W project](../../research/w-state-design/README.md)

For every even count from six onward, the sharp zero-hafnian cofactor
bound has only the known complete odd-core equality family, up to root
choice, scale, and site phases.
The scalar harmonic response cost has a strict local minimum at that
family. Compactness therefore excludes every sufficiently high-efficiency
ground source from improving the known W rate, with all colored completions
allowed. No explicit efficiency threshold is supplied.

The proof also gives a quantitative inequality measuring how nearly
disjoint the ground and cofactor strengths must become near maximum response.

From the repository root, with Python 3.11 or later and the standard library:

~~~sh
python3 computations/w-cofactor-rigidity-2026-09-27/verify.py > /tmp/w-cofactor-rigidity.json
diff -u computations/w-cofactor-rigidity-2026-09-27/results.json /tmp/w-cofactor-rigidity.json
python3 -O computations/w-cofactor-rigidity-2026-09-27/verify.py > /tmp/w-cofactor-rigidity-optimized.json
diff -u /tmp/w-cofactor-rigidity.json /tmp/w-cofactor-rigidity-optimized.json
~~~

The exact replay checks:

- Every four-cycle incidence count through twelve sites and the positive
  AM--GM allocations through eighty sites.
- All 32,768 six-site edge sets for the property that each perfect matching
  meets the set exactly once; precisely the six stars survive.
- The four-site scope exception, where complementary triangles also survive.
- Eleven exact cofactor-complementarity fixtures, including sharp and
  nonuniform complex cancellation sources.
- Twelve exact constrained Taylor expansions through twelve sites, checking
  the full complex quadratic response-cost formula, phase and scale
  zero modes, and the root modes.
- Positive coefficients for every tested even count from six to eighty,
  and the negative four-site root coefficient.

These checks support the written all-size proof; finite enumeration and
Taylor fixtures do not prove the general classification or compactness step.
The proof uses the established Roos subhafnian inequality.
All acceptance checks remain active under optimized Python.
