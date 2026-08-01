# A rational binary GHZ8 chart is sharply capped at residual rank 53

Research calibration only. Krenn's conjecture remains open, no rank-55
binary source is constructed here, and no certified dependency changes.

## Exact outcome

There is a rational binary eight-site source with matching tensor

\[
\Psi(A)=e_0^{\otimes 8}+e_1^{\otimes 8}
\]

and a deleted endpoint pair, `(3,4)`, whose six-site differential has

\[
\operatorname{rank}d\Psi_M=53,
\qquad
\operatorname{rank}d\Psi_M^{\mathrm{mixed}}=51.
\]

Both statements are exact over \(\mathbb Q\). This improves the maximum among
the previously inventoried exact binary GHZ8 sources from 31 to 53, but it is
still two ranks short of the required full/mixed pair `(55,53)`.

The source has 45 nonzero cells. It lies in an explicit rational chart with
26 freely chosen nonzero parameters and 19 cells determined triangularly.
The chart is not inferred from a floating rank test: a sparse Laurent-
polynomial calculation verifies all 256 matching-tensor identities
identically in the 26 parameters. A small rational specialization, with
numerators and denominators no larger than 24 bits, supplies the rank witness.

There is also an exact chart-wide upper bound:

\[
 \operatorname{rank}d\Psi_{M(\mathbf t)}\le 53
 \quad\text{at deletion }(3,4)
\]

identically in the 26 parameters. Thus no specialization of this rational
chart can provide the missing rank 54 or 55.

## Why the whole chart is capped

Write the deleted vertices as \(p=3,q=4\), the residual set as
\(R=(0,1,2,5,6,7)\), and let \(U^a,V^b\) be their endpoint-vector families.
The literal chart support gives, for every parameter value in its 45-cell
open set,

* \(U^0\) is supported only at residual centre 7, where
  \(U^0_7=x_{3700}e_0\);
* \(U^1\) and \(V^0\) are both supported only at residual vertex 0, so their
  symmetric pair packet is identically zero; and
* the deleted edge \(34\) is zero.

Consequently the two adjusted endpoint packets have the exact form

\[
 P=x_{3700}S(e_0),\qquad Q=0,
 \qquad S(\ell)_{r7}=V^1_r\ell^{\mathsf T}.
\]

The level-two identity gives \(d\Psi_M S(e_0)=0\). Direct factorization of a
star differential is

\[
 d\Psi_M S(\ell)(w)=\ell[w_7]F_{V^1}(w|_{R\setminus\{7\}}).
\]

Since the left side vanishes for the nonzero column \(e_0\), the common factor
\(F_{V^1}\) vanishes, and therefore \(d\Psi_M S(e_1)=0\) as well. These are
two kernel directions in addition to the five universal trace-zero vertex
gauges.

The formal checker verifies all seven kernel identities as Laurent-polynomial
identities. Their independence at the rational specialization proves
independence over the Laurent function field, hence every \(54\times54\)
minor vanishes identically. The support argument also makes independence
transparent throughout the open chart: the off-star live graph is connected
and contains the triangle `0-1-2-0`, so no nonzero gauge can be supported only
on the 7-star. This proves the chart-wide rank cap, while the specialization
of rank 53 proves it is sharp.

## Complete deletion census

For the displayed specialization, exact Gaussian elimination over
\(\mathbb Q\) gives the following histogram over all 28 endpoint deletions:

| full/mixed rank | number of deletions |
|---:|---:|
| 14/12 | 1 |
| 23/21 | 3 |
| 27/25 | 1 |
| 28/26 | 2 |
| 29/27 | 2 |
| 32/30 | 2 |
| 33/31 | 1 |
| 35/33 | 1 |
| 36/34 | 1 |
| 39/37 | 1 |
| 40/38 | 1 |
| 42/40 | 4 |
| 43/41 | 1 |
| 45/43 | 2 |
| 46/44 | 2 |
| 51/49 | 2 |
| **53/51** | **1** |

Every deletion loses exactly the two pure-output directions when restricted
to the mixed rows. Thus the endpoint-completion incidence condition holds
with the expected rank drop throughout the census.

The exact checker is
[verify_binary_ghz8_exact_rank53_source.py](../computations/verify_binary_ghz8_exact_rank53_source.py).
It uses only the standard library and passes normal, optimized, and isolated
Python. It verifies:

1. the 26-parameter chart identically over a Laurent function field;
2. five formal gauge kernels and two formal star-column kernels, proving the
   chart-wide rank-53 cap;
3. all 256 coefficients at the rational specialization;
4. all 28 full and mixed differential ranks; and
5. the complete expected rank histogram, including the unique `(3,4)`
   deletion of rank `53/51`.

## Numerical conditioning and attempts to open rank 54

Floating replay of the exact rational point has GHZ residual
`2.22e-16`. At deletion `(3,4)`, the end of the full singular spectrum is

```text
s[49:56] =
  6.36e-3, 4.71e-3, 1.37e-4, 1.36e-5,
  8.50e-16, 6.11e-16, 2.94e-16.
```

So the exact rank-53 conclusion is also well separated numerically; its proof
does not rely on that separation.

The support pattern alone is not the obstruction. Four deterministic random
assignments on the same support, without imposing the GHZ equations, all give
residual rank 55. The two missing ranks therefore come from the matching-
tensor equations on the sampled chart, not from structural zero rows or
columns.

Targeted numerical searches did not open either missing singular direction:

* 40 scale-normalized tangent predictions on the 45-cell component corrected
  back to GHZ residual at most `3.11e-15`; every corrected point had rank at
  most 53.
* 120 fixed-support random restarts produced 116 solutions with residual below
  `1e-10`; their rank histogram was
  `{47:1, 48:10, 50:1, 51:6, 52:6, 53:92}`.
* A smaller deterministic replay included in the repository accepts all 20
  tangent corrections at machine precision and all 24 nonlinear restarts;
  its largest attempted `s[53]` is numerical noise (`5.45e-14`).

[search_binary_ghz8_rank54_from_rank53.py](../computations/search_binary_ghz8_rank54_from_rank53.py)
replays all 28 numerical singular gaps by default and runs these smaller
deterministic controls with `--stress`.

The failed searches are evidence only, but the rank-53 cap on this rational
chart is now exact. Nothing here proves a cap on the unrestricted binary GHZ8
fibre. The remaining exact question is whether a different component or
support can raise the full/mixed pair from `(53,51)` to `(55,53)`.
