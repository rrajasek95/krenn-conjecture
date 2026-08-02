# Full-Jacobian rank on the exact rank-53 chart

The full `256 x 112` GHZ8 Jacobian has rank exactly 84 over the Laurent
function field of the 26-parameter rank-53 chart. Consequently every
`85 x 85` minor vanishes identically on that chart, while an `84 x 84`
minor is nonzero at the rational seed. Thus the Jacobian has constant rank
84 on a Zariski neighbourhood of the seed inside the chart.

This is an exact Laurent identity, not an interpolation claim.

## Two extra kernel vectors

The chart derivatives give 26 independent kernel vectors: the chart's 26
chosen parameter cells form an identity block in those derivatives. Exact
Laurent elimination constructs two additional vectors with fixed supports
of 24 and 17 cells.

For the 24-cell support, 23 columns admit successive monomial pivots. Taking
the active cell `(1,6,0,0)` as the free coordinate gives a Laurent-polynomial
kernel vector whose `(4,7,1,1)` coordinate is nonzero.

For the 17-cell support, 15 columns admit successive monomial pivots. The
remaining equation has the form

\[
                 a\,z_{1600}+b\,z_{5600}=0,
\]

where \(a,b\) are nonzero two-term Laurent polynomials. Taking the remaining
coordinates to be \((b,-a)\) and back-substituting gives a second
Laurent-polynomial kernel vector. Its `(5,6,0,0)` coordinate is nonzero.
No non-monomial division occurs in either construction.

Both distinguishing cells are absent from the chart support, and each is
absent from the other extra vector. The two vectors are therefore independent
modulo the 26 chart tangents. The full Jacobian has nullity at least 28 over
the Laurent function field, hence rank at most \(112-28=84\). Its exact rank
at the rational specialization is 84, proving equality over the function
field and the asserted local constant-rank statement.

The checker
[verify_binary_ghz8_rank53_chart_jacobian.py](../computations/verify_binary_ghz8_rank53_chart_jacobian.py)
performs both monomial eliminations, verifies the 28 kernel identities against
all 256 Jacobian rows, and rechecks rank 84 at the rational seed using only
exact arithmetic.

## Formal-local consequence

This constant-rank result closes the higher-order gap left by the
[second-order normal obstruction](binary-ghz8-rank53-second-order-normal-obstruction.md).
Let \(A(t)\) be a formal arc in the full 112-cell GHZ8 fibre through the
rational seed. Use its 26 parameter-cell coordinates to form the unique chart
arc \(C(t)\), and put \(Z(t)=A(t)-C(t)\). If \(Z\ne0\), let \(t^kZ_k\) be its
first nonzero term.

An `84 x 84` Jacobian minor stays invertible in the completed local ring of
the chart, while all 85-minors vanish there. Hence each of the three seed
left-cokernel functionals used in the quadratic obstruction extends formally
along \(C(t)\) while continuing to annihilate \(J(C(t))\). The coefficient of
order \(k\) first puts \(Z_k\) in the seed kernel. Its parameter coordinates
are zero, so the 28-vector kernel basis above puts it in the span of the two
normal directions.

Apply the three extended cokernel functionals to

\[
 F(C(t)+Z(t))-F(C(t)).
\]

The linear term vanishes identically. At order \(2k\), the first surviving
term is the seed quadratic form on \(Z_k\); the already verified diagonal
\(a^2,ab,b^2\) obstruction forces both normal coefficients to vanish. This
contradicts the choice of \(Z_k\). Therefore \(Z=0\): every formal arc through
the rational seed in the full GHZ8 fibre is a chart arc.

## Scope

The rank need not be 84 at every chart specialization; it may drop where all
84-minors vanish. The result is local at the rational seed and does not rule
out distant components, rank-53 sources away from this chart, or rank 54/55
elsewhere.
