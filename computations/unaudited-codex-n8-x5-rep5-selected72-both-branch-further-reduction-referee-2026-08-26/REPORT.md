# Independent rep5 four-subchart referee

Verdict: **PASS design-only**.  The four sources are literal, exhaustive
subcharts of the two sealed parent branches.

For the `q=1` parent, `D(a04_20)` divides exactly 486 wholly divisible
generators and adjoins `a04_20*inv=1`; `V(a04_20)` is literal specialization.
Both generated ideals were reproduced polynomial-for-polynomial.  For the
`q=0` parent, all equations are homogeneous for the recorded primitive weight,
the grading rank is 71 at two primes and the explicit nullvector gives exact
Q-nullity one.  Thus normalizing `a35_21=1` on its open branch is root-free;
the zero branch is literal.

The upstream `D(a37_20)/V(a37_20)` parent cover and its referee manifests also
replay.  Consequently every point of both parents lies in one of the four
sources, without asserting an implication between the parents.

The smallest finite syntax target is
`sources/closed_q0_V_a35_21_Q_design.sing`: 71 variables, 6,075 generators,
192,489 expanded terms, degree mass 963,540.  A source-level symbolic reduction
census should precede any solver; if none is found, this is the smallest held
solver chart.  No Singular run or mathematical closure is claimed.
