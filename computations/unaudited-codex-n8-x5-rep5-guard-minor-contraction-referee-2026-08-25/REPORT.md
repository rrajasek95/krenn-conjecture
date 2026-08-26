# Independent rep5 guard-minor contraction referee

Verdict: **PASS_INDEPENDENT_EXACT_DESIGN_NO_IDEAL_RUN**.  The referee does not import the producer and invokes no computer-algebra system.  It independently regenerates the 105 perfect matchings, the rep5 support and its 12 supported matchings, and the full 6561-row semantic digest.  The fixed-identity equations force the indexed orientations `A36[i,j]=-sum_k A37[i,k]A26[j,k]`, `A06*A37^T=0`, and `(I-A17*A26)*A37^T=0`; the cap-03/star-center-4 enumeration independently leaves precisely the switched `A06/A35` and direct `A06/A37` terms, hence the stated carrier `A06^T*K*[A35|A37]`.

The exact Cramer formulas were replayed as polynomial dictionaries for every minor and target-row case (12 identities): `A06*v=0` and `A06*w=d*abar*e_i`.  Both y- and z-pivot programs were then regenerated in memory.  Their byte counts and SHA-256 hashes match the producer exactly; for the z chart, the solved A37 column is absent from the free-source set and from its own substitution expressions before `v`, `d`, `A36`, and saturation are formed.  The single saturation is `abar*beta*A37[p,q]*d*sat-1`.

The independent bookkeeping is exact: `100/6586 -> 91/6577`, with 6561 X5 equations, six non-tautological `A06*A37^T` equations, nine second-guard equations, and one saturation.  The raw 972 charts quotient into 162 free S3 orbits of size six, split 81 y / 81 z.

Scope is deliberately narrow: no ideal was run, no rep5 closure or transport is claimed.  `HELD_MODULAR_PILOT.json` specifies one p=32003 y-chart lane with direct Darwin libproc RSS observation, atomic logs/telemetry, 180/190-second and 8-GiB gates, manager clearance, and stop after any outcome.  It was not launched.
