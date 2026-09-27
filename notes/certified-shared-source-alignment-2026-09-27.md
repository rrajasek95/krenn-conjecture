# Certified alignment of shared sources and their observed mean spaces

Research note, 2026-09-27. Written all-orders arguments, four exact
seven-site input certificates, and a computational replay with separate
tensor and derivative calculations. Not Lean formalized or independently
peer reviewed. The Krenn–Gu manuscript is unchanged.

## 1. What this adds

The [single-output initializer](certified-full-source-initialization-2026-09-27.md)
encloses every source compatible with a noisy tensor. Each output is
recovered in its own site-scaling convention. Combining those mean
vectors directly can give the wrong shared mean space. This note bounds
the conversion to **one common convention**, using the shared covariance.
It then certifies a joint correction neighborhood and the span of the
observed mean vectors.

The alignment uses the exact matching formula already proved in
[Corollary 9 of the all-orders source theorem](single-cross-moment-all-orders-2026-09-27.md).
The additions are finite error enclosures for that formula, their
composition with the global single-output certificates, a joint
certificate with 267 free parameters, and a graph criterion explaining
when complex scaling alignment can fail.

In the example, four full tensors are processed without supplying their
true means or covariance to the proposal routines. The resulting mean
space has dimension four, although each site has only three coordinates.
The saved errors are extremely small: the first observation uses the
previous error budget of about `3.4e-41`, and the other three use about
`3.2e-50`. These perturbations are below floating precision at the chosen
sources. The result is an exact proof-chain certificate, not a practical
noise threshold or a statistical accuracy claim.

## 2. Inputs, scaling freedom, and the shared reference

There are `n=2m+1` labelled sites and `p` labelled observations.
Observation `s` has local means `mu_i^(s) in C^3`; the edge blocks
`R_ij in C^(3 by 3)` are shared. Its matching tensor is

$$
F_s(\mu^{(s)},R)_a
=\sum_M\prod_{\{i,j\}\in M}(R_{ij})_{a_i a_j}
       \prod_{i\notin V(M)}(\mu_i^{(s)})_{a_i}.
$$

Here `a` lists one coordinate in `{0,1,2}` at every site; `M` ranges
over collections of edges with disjoint endpoints; and `V(M)` is their
set of endpoints. The observed tensor is `Y_s`, with a supplied bound
`||F_s-Y_s||<=epsilon_s`. All vector and tensor norms are Euclidean
norms of their entries; edge norms are Frobenius norms. Matrix operator
norms are spectral norms.

Assume a single-output certificate supplies candidate means `u_hat_s`,
candidate edges `C_hat_s`, and bounds `e_mu,s`, `e_R,s`. Their meaning
is: **every** compatible source, after a specified product-one site
rescaling, has a representative `(u_s,C_s)` satisfying

$$
\|u_s-\widehat u_s\|\le e_{\mu,s},\qquad
\|C_s-\widehat C_s\|\le e_{R,s}.                            \tag{1}
$$

The first norm stacks all local means, and the second stacks all edges.
These are input guarantees, not a closeness assumption about the true
source. The cited initializer verifies them from the data under explicit
acceptance conditions. Its coordinate changes are now implemented in
[source_chart_certificate.py](../computations/matching-tensor-recovery-2026-09-26/source_chart_certificate.py):
for each candidate mean `(a,b,c)` with `a!=0`, use the basis with
columns `(a,b,c),e_1,e_2`, transform the observed tensor exactly, and
certify in the unit-mean chart. The product of the inverse basis norm
bounds amplifies the data budget. The largest basis norm and largest
pairwise product bound the return errors in means and edges. These
changes depend only on the candidate.

A site rescaling multiplies `u_i` by `gamma_i` and `C_ij` by
`gamma_i gamma_j`, with `product_i gamma_i=1`. It preserves the
matching output. For a truly shared source, the individual representatives
are therefore related by numbers `lambda_s,i` with

$$
\prod_i\lambda_{s,i}=1,\qquad
\lambda_{s,i}\lambda_{s,j}(C_s)_{ij}=(C_0)_{ij}.              \tag{2}
$$

Use observation zero as the reference. Its representative fixes the
remaining common rescaling. The aligned mean row is
`v_s=(lambda_s,i u_s,i)_i`, with `v_0=u_0`; its covariance is `C_0`.
The target mean space is the column space of the matrix whose columns
are these `v_s` in the direct sum of the local spaces. Its angles depend
on the fixed reference gauge. No unobserved latent mean direction is
being inferred.

Existence of a common source compatible with the budgets is an assumption
of the enclosure theorem. The example separately verifies existence by
reconstructing a shared source and all its noisy data. Passing the
alignment inequalities alone does not test this model assumption.

## 3. Matching formulas with complex disc bounds

For an edge `ij`, choose a coordinate functional `ell_ij` of norm one.
Use the same functional on `C_s` and `C_0`. Require

$$
|\ell_{ij}((\widehat C_0)_{ij})|>e_{R,0}.                    \tag{3}
$$

The reference denominator cannot then vanish for any compatible source.
The ratio

$$
q_{s,ij}=\frac{\ell_{ij}((C_s)_{ij})}
                   {\ell_{ij}((C_0)_{ij})}
         =\frac1{\lambda_{s,i}\lambda_{s,j}}                 \tag{4}
$$

is enclosed by dividing the discs centered at the corresponding
candidate entries with radii `e_R,s` and `e_R,0`. A disc with center
`a` and radius `r` means `{z in C: |z-a|<=r}`. For discs centered
at `a,b`, multiplication uses radius
`|a|r_b+|b|r_a+r_a r_b`; a reciprocal uses radius
`r_a/(|a|(|a|-r_a))` when `|a|>r_a`. These rules cover complex
alternatives even though the saved centers are real rationals.

Let `H` be the graph of edges satisfying (3). Say that `H` is
*factor-critical* if deleting any vertex leaves a graph with a perfect
matching, that is, disjoint edges covering every remaining vertex.
The complete graph on an odd number of vertices has this property.

**Lemma 1 (certified scaling from a complementary matching).** For
each site `i`, choose a perfect matching `M_i` of `H` with `i` deleted.
Then

$$
\lambda_{s,i}=\prod_{jk\in M_i}q_{s,jk}.                    \tag{5}
$$

Multiplying the ratio discs encloses every compatible value of
`lambda_s,i` in a disc `D(l_s,i,r_s,i)`, where `l_s,i` is its computed
center and `r_s,i` its radius. No complex root choice is needed.

**Proof.** Each vertex except `i` occurs exactly once in the matching.
The product in (4) is the reciprocal of
`product_(j!=i) lambda_s,j`, which equals `lambda_s,i` by (2).
Disc arithmetic preserves inclusion at each multiplication. QED.

This is the earlier exact alignment formula with its errors retained.
Different matchings give separate valid enclosures; the implementation
enumerates them at seven sites and chooses the smallest radius. It
chooses the largest-magnitude candidate reference coordinate on each
edge. No claim of optimal matching selection at arbitrary size is made.

**Theorem 2 (global aligned-source enclosure).** Under (1)–(3), suppose
all the complementary matchings exist. Define

$$
\widehat v_{s,i}=l_{s,i}\widehat u_{s,i},\qquad
E_s=\max_i(|l_{s,i}|+r_{s,i})e_{\mu,s}
 +\sqrt{\sum_i r_{s,i}^2\|\widehat u_{s,i}\|^2}              \tag{6}
$$

for `s>0`, and put `v_hat_0=u_hat_0`, `E_0=e_mu,0`.
Every compatible shared source, in the reference convention, satisfies

$$
\|v_s-\widehat v_s\|\le E_s,\quad
\|C_0-\widehat C_0\|\le e_{R,0},\quad
\|\Theta-\widehat\Theta\|\le
 E:=\sqrt{e_{R,0}^2+\sum_s E_s^2},                           \tag{7}
$$

where `Theta` lists all aligned mean entries and one copy of the common
covariance. The same covariance can also be estimated from each aligned
`C_hat_s`, with explicit bounds given below.

**Proof.** Write the mean difference at site `i` as
`lambda_s,i(u_s,i-u_hat_s,i)+(lambda_s,i-l_s,i)u_hat_s,i`.
The first term over all sites is bounded by the maximum modulus in
the discs times `e_mu,s`; the second has the displayed squared norm
bound. Combine the observations and retain the reference covariance
bound. This comparison applies to every compatible shared model because
(1) and (2) hold for each one. QED.

For the additional covariance estimate, multiply the two site discs
to enclose `lambda_s,i lambda_s,j` in `D(l_ij,r_ij)`. Then

$$
\|C_0-(l_{ij}(\widehat C_s)_{ij})_{ij}\|
\le\max_{ij}(|l_{ij}|+r_{ij})e_{R,s}
 +\sqrt{\sum_{ij}r_{ij}^2\|(\widehat C_s)_{ij}\|_F^2}.       \tag{8}
$$

The candidate scaled covariances need not agree exactly and the
candidate site factors need not have product exactly one. They are
estimates enclosed about a common true model, not a claim of exact
consistency of noisy estimates. For (7) and the joint forward check,
the program chooses the reference candidate as the common covariance.

## 4. The observed mean space and a joint correction theorem

Let `V_hat` be the `3n` by `p` matrix with columns `v_hat_s`, and put
`E_mu=(sum_s E_s^2)^(1/2)`. Suppose `V_hat` has full column rank and
`sigma_min(V_hat)>=s_0>E_mu`. A computable lower bound is

$$
s_0=\frac1{\sqrt{\mathrm{tr}((\widehat V^*\widehat V)^{-1})}}, \tag{9}
$$

rounded downward. The saved calculation uses exact rational Gram
inversion and a rational upper bound for the square root in its
denominator.

**Corollary 3 (certified observed mean span).** Every compatible
shared source has observed mean rank `p`. If `P` is the orthogonal
projection onto its mean space and `P_hat` is the projection onto
the candidate space, then

$$
\|(I-P)P_{\widehat V}\|\le E_\mu/s_0.                       \tag{10}
$$

This is the sine of the largest principal angle between the two
`p`-dimensional spaces.

**Proof.** Equation (7) gives `||V-V_hat||_F<=E_mu`, so the smallest
singular value of `V` is positive. Its rank is `p`. Projecting `V_hat`
onto the orthogonal complement of `V` gives norm at most `E_mu`.
Multiplication by the right inverse of `V_hat` bounds the projection
of its entire column space by `E_mu/s_0`. Bound (9) follows by
bounding the largest eigenvalue of a positive inverse Gram matrix
by its trace. QED.

If the observed mean rank is known in advance to be at most `r<p`,
the same argument applies to a supplied rank-`r` approximation `Z`
to `V_hat`: replace the error by `E_mu+||V_hat-Z||_F` and `s_0`
by a lower bound for `sigma_r(Z)`. An error below `s_0` forces
rank exactly `r`. Without this prior rank bound, arbitrarily small
additional directions prevent certification of an exact rank below
`p` from noisy data. The four-column example needs no such prior.

For joint correction, fix the first coordinate of observation zero's
mean at every site except the last to its candidate value. All other
mean entries and every covariance entry are free. In the saved example
these fixed values are one. There are

$$
d=3np+9\binom n2-(n-1)                                      \tag{11}
$$

free parameters. Stack the forward maps as
`F_joint=(F_0,...,F_(p-1))`. At the assembled candidate `Theta_c`,
let `J=D F_joint(Theta_c)` and certify `g>=||J^dagger||`.
Let `L` bound the Hessian norm on the unit parameter ball, as in
the [local source theorem](full-source-local-stability-2026-09-27.md).
The smaller-matching derivative formulas are unchanged. In observation
zero use singleton weights two except weight three at the last site;
in every other observation use weight three at every singleton. Edge
weights are nine. Sum the squared majorants over observations. Set

$$
r=\min\{1,(2gL)^{-1}\},\qquad
\epsilon=\sqrt{\sum_s\epsilon_s^2},\quad
\rho\ge\|F_{\rm joint}(\Theta_c)-Y\|.                       \tag{12}
$$

**Theorem 4 (global entry into joint correction).** If (7) gives
`E<r` and `g rho<=r/2`, then every compatible shared source, in the
reference gauge, satisfies

$$
\|\Theta-\Theta_c\|\le2g(\epsilon+\rho).                    \tag{13}
$$

The exact-arithmetic frozen left-inverse iteration

$$
\Theta_{k+1}=\Theta_k+J^\dagger(Y-F_{\rm joint}(\Theta_k))    \tag{14}
$$

is a contraction of factor at most one half on that ball. Its limit
is within `2g epsilon` of every compatible shared source. The improved
bound (13) may replace `E_mu` in Corollary 3.

**Proof.** Theorem 2 first puts every compatible representative in the
ball. The bound `||D F_joint-J||<=Lr<=1/(2g)` gives a lower
Lipschitz bound `||F_joint(A)-F_joint(B)||>=||A-B||/(2g)` by
integration along the segment. It proves (13). The derivative of
(14) is bounded by one half, and the candidate moves by at most
`g rho<=r/2`, so the ball is invariant. The contraction principle
and comparison to a compatible source prove the limit bound. QED.

The iteration solves projected equations, and need not find a
least-squares stationary point. The certificate verifies its hypotheses;
it does not run the iteration or bound floating-point iteration errors.
Its smaller inverse bound is compared at a fixed total stacked noise
norm. It does not imply statistical averaging or cancellation of
coherent errors as more observations are added.

**Corollary 5 (generic shared initialization at every odd order).**
For every odd `n>=7` and every fixed finite number of observations,
a generic shared source has a positive, source-dependent measurement
neighborhood in which sufficiently accurate proposals pass the preceding
checks. Thus all compatible shared mean rows and edge blocks can be
enclosed in one common scaling convention and placed in a joint
correction neighborhood. No relation between the number of observations
and local dimension three is required for parameter recovery.

**Proof.** The single-output rank and calibration conditions hold
simultaneously on a nonempty open set of shared source parameters,
as in the exact shared-source theorem. Generic edge blocks are nonzero,
so one can select nonzero reference coordinates on every edge and use
the complete graph for Lemma 1. The rational matching formulas have
nonzero denominators on this open set; their disc radii, and then (7),
tend to zero with the input error bounds.

The joint derivative is injective after fixing the reference gauge.
Indeed, single-output generic recovery implies that a zero output
variation is an infinitesimal site rescaling. For two observations their
scaling differences `t_i` satisfy `t_i+t_j=0` at every nonzero edge.
On the complete graph with at least three vertices this forces every
`t_i=0`. Thus all observations have the same infinitesimal rescaling.
The fixed nonzero reference mean coordinates kill it at the first
`n-1` sites, and the product-one condition kills it at the last.
Consequently the joint correction radius is positive. For sufficiently
small noise and proposal error, (7) is below that radius and the joint
forward residual meets (12). The single-output initializer supplies the
needed proposals on fixed inverse charts with sufficient precision.
QED.

For the observed mean span, Corollary 3 applies when the columns are
independent, or with a specified rank bound and approximation as described
there. This does not impose a local independence assumption on the mean
rows. In particular, the global mean rank can exceed three.
The fixed double precision and denominator cutoff in the example are
not a general implementation of this corollary's sufficient-precision
strategy.

## 5. What sparse covariance graphs allow

The matching formula is sufficient, but not necessary, for unique
alignment. The following elementary criterion distinguishes the two.
Here use edge ratios `c_ij=lambda_i lambda_j`, the reciprocals of (4).
All mentioned edge entries are nonzero, and the graph is connected.

**Theorem 6 (complex alignment on a connected graph).** Suppose
`n` is odd and the edge ratios are consistent with nonzero vertex
scales whose product is one.

- If the graph is not bipartite, the scales are unique and are Laurent
  monomials in the edge ratios.
- If the graph is bipartite with parts `A,B`, put `q=|A|-|B|`.
  There are exactly `|q|` complex scaling solutions. They are unique
  precisely when `|q|=1`, and in that case are Laurent monomials.

A Laurent monomial is a product with integer exponents, possibly
negative. In particular, the unique cases admit rational alignment
without selecting roots. For real, consistent, nonzero edge ratios
on an odd connected graph the solution is unique even in the other
bipartite cases, because `q` is odd; taking an odd root may then be
necessary. The finite ambiguity in the second item concerns complex
sources.

**Proof.** Ratios of two solutions satisfy `g_i g_j=1` on edges and
`product_i g_i=1`. Starting at a vertex, these ratios alternate
between `t` and `t^(-1)` along paths. An odd cycle forces `t^2=1`;
then all ratios equal `t`, and odd `n` forces `t=1`. On a bipartite
graph no additional edge condition arises; the product condition is
`t^q=1`. Since odd `n` makes `q` a nonzero odd integer, this has
exactly `|q|` distinct complex solutions and one real solution.

For explicit rational formulas, choose a rooted spanning tree. Let
`sigma_i` be `1` or `-1` according to its bipartition, with the root
having sign one. Tree propagation gives

$$
\lambda_i=t^{\sigma_i}\kappa_i(c),\qquad
\kappa_0=1,\quad\kappa_j=c_{ij}/\kappa_i
\quad\hbox{along a parent edge }ij.
$$

Each `kappa_i` is a Laurent monomial. Write
`K=product_i kappa_i` and `q=sum_i sigma_i`, so `t^q=K^(-1)`.
If the graph is bipartite and `q=1` or `-1`, this determines `t`
rationally. Otherwise, in a nonbipartite graph choose an edge `uv`
joining equal tree signs. Then

$$
d=\left(\frac{c_{uv}}{\kappa_u\kappa_v}\right)^{\sigma_u}
=t^2,\qquad t=K^{-1}d^{(1-q)/2}.                            \tag{15}
$$

The exponent is an integer because `q` is odd. This supplies the
claimed monomials in every nonbipartite case. QED.

The relevant exponent matrix has one column `e_i+e_j` per edge,
with the additional product-one relation. This is the unsigned graph
incidence matrix. Its rank and integer normal form are classical; see
Grossman, Kulkarni and Schochetman,
[On the minors of an incidence matrix and its Smith normal form](https://doi.org/10.1016/0024-3795(93)00173-W),
*Linear Algebra and its Applications* 218 (1995), 213–224.
The proof above is self-contained; no new graph-matrix theory is claimed.

The [integer character checker](../computations/matching-tensor-recovery-2026-09-26/alignment_graph_characters.py)
constructs the monomials for odd paths and stars with an added triangle,
from 3 through 19 vertices. It verifies each exponent row `a_i` by
checking

$$
\sum_e(a_i)_e(e_{u(e)}+e_{v(e)})-e_i=k_i\mathbf1
\quad\hbox{for an integer }k_i.                             \tag{16}
$$

Equation (16) is an exact identity of characters after imposing
`product_j lambda_j=1`. These finite checks support the formulas;
they do not replace the all-graph proof.

**Corollary 7 (a sparse shared-mean ambiguity).** A seven-site star
has a nontrivial fifth-root scaling stabilizer over `C`. Consequently
shared outputs on that graph need not determine a common observed
mean space, even when every supported covariance block is nonzero.

**Proof.** Let `zeta` be a nontrivial fifth root of unity. Give the
center scale `zeta` and every leaf scale `zeta^(-1)`. Every supported
edge product equals one, and the site product is `zeta^(-5)=1`.
This rescaling preserves both the covariance and each output.
It may therefore be applied to just one mean setting.

To see that the span can change, take a first mean row equal to `e_0`
at every site, and a second row equal to the first plus `e_1` at the
center and one leaf. After rescaling only the second row, the two
added coordinates have ratio `zeta^2`, whereas every vector in the
original two-dimensional span has equal coefficients at those two
outside coordinates. Since `zeta^2!=1`, the new row is outside the
original span. Both collections retain the same covariance and
labelled outputs. A common scaling taking one covariance/mean-space
pair to the other would have to send the first row, which has no
outside coordinates, to a multiple of itself: it is the only such
line in either span. Thus all site factors would equal one scalar.
Preserving the nonzero covariance and having product one at seven
sites forces that scalar to be one. Hence even the two covariance/
mean-space pairs are inequivalent under a common scaling. QED.

This is an obstruction in the complex matching model, not a real
fifth-root ambiguity. It explains why a statement for arbitrary sparse
sources needs graph hypotheses. The graph fails the complementary
matching test, as it should. Conversely, an odd path is bipartite with
part imbalance one: it has unique rational scaling alignment even
though it is not factor-critical. The present noisy driver implements
Lemma 1; it does not yet implement interval propagation through every
alternative monomial in (15).

## 6. Four-observation certificate and reproducibility

All four observations have the same dense rational edge blocks as the
seven-site source in the single-output initializer. Observation zero
reuses that published certificate. Its means are all `e_0`, its noise
entries are signed `2^-140`, and its budget is `47/2^140`.

For `s=1,2,3`, start all first mean coordinates at one and change the
coordinate at site `s-1` to two. The outside coordinates are:

| Observation | Coordinate 1 at site `i` | Coordinate 2 at site `i` |
| --- | --- | --- |
| 1 | `1/16` | zero |
| 2 | zero | `1/16` |
| 3 | `((i mod 3)-1)/16` | `(2(i mod 2)-1)/16` |

Each of their tensor coordinates receives signed noise `2^-170`, with
random seeds `275171`, `275172`, and `275173`. Each budget is
`47/2^170`. The blind numerical proposal receives only those noisy
entries, and rounds its proposed source entries to fractions with
denominator at most 64. Acceptance does not assume a denominator bound
on true sources. In this example the proposals equal the true sources
in their separate gauges. Their alignment is nontrivial: in observation
`s>0`, the scale at site `s-1` is two and that at the last site is one
half. The others equal one.

| Quantity | Certified bound or recorded value, rounded for display |
| --- | ---: |
| Number of observations and sites | 4 and 7 |
| Free mean and shared edge parameters | 78 and 189 |
| Global joint error before local sharpening | `2.181e-38` |
| Joint inverse bound `g` | `4.474` |
| Joint correction radius | approximately `5.47740e-7` |
| Refined global joint error | `6.019e-40` |
| Exact-arithmetic correction limit error | `3.017e-40` |
| Candidate mean-matrix smallest singular value lower bound | greater than `0.3120` |
| Observed mean rank | 4 |
| Refined largest principal-angle sine bound | `1.929e-39` |

The [manifest and joint certificate](../computations/matching-tensor-recovery-2026-09-26/shared-source-noise-certificate.json)
references each input certificate by filename and SHA-256 hash and
stores all scalar discs, matching choices, integer preconditioners, and
rational error bounds. The three new observation certificates sit next
to it. Generation uses the stored observation-zero certificate; the
full replay verifies all four input certificates again.

The [replay](../computations/matching-tensor-recovery-2026-09-26/verify_shared_source_noise.py)
disables numerical proposal routines. It reconstructs every clean
entry by a separate scalar matching calculation, checks every exact
noise entry and budget, separately assembles the exterior matrices,
and checks every single-output local derivative and every joint
derivative. It rebuilds the joint curvature bound by enumerating
matchings and parameter supports and replays every stored inequality.
It also rejects reference denominator discs containing zero.

To avoid testing alignment only at zero actual source error, separate
checks at 3, 5, 7, and 9 sites perturb every candidate mean and edge
entry by signed `2^-30`, independently across four observations.
Their supplied source-error enclosures are checked exactly. The replay
then verifies the true scale and mean errors, and computes nonzero
subspace angles through rational projector identities. These checks
test the conditional alignment inequalities; the three- and five-site
checks are not single-output recovery claims at those orders.

The [saved audit](../computations/matching-tensor-recovery-2026-09-26/shared-source-noise-audit.json)
passes. It shares bound-acceptance code and exact arithmetic libraries
with the generator; it is not an independent mathematical proof review.

Run from the repository root:

```sh
OPENBLAS_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 .venv/bin/python computations/matching-tensor-recovery-2026-09-26/shared_source_noise_recovery.py --output-dir /tmp/krenn-shared-reproduction > /tmp/krenn-shared-reproduction.json
OPENBLAS_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 .venv/bin/python computations/matching-tensor-recovery-2026-09-26/verify_shared_source_noise.py
```

The first command writes three new observation records to the specified
directory and emits the manifest to standard output. The second reads
the committed records. NumPy, SciPy, and python-flint are required.

## 7. Attribution and remaining scope

The exact matching alignment is from the earlier repository theorem.
Complex disc arithmetic and residual verification are established
methods; see Rump,
[Verification methods: rigorous results using floating-point arithmetic](https://www.tuhh.de/ti3/paper/rump/Ru10.pdf),
*Acta Numerica* (2010). The span estimate is an elementary instance of
classical singular-subspace perturbation; see Wedin,
[Perturbation bounds in connection with singular value decomposition](https://link.springer.com/article/10.1007/BF01932678),
*BIT* 12 (1972), 99–111. The graph criterion is proved by elementary
propagation and sits within classical unsigned-incidence theory.

This note supplies the previously missing certified shared alignment
and joint initialization step on the stated generic open set. Remaining
targets include useful noise thresholds, a validated finite-precision
correction method, efficient inversion from compressed measurements,
and source classes where the present single-output rank conditions
fail. An arbitrary nongeneric shared-source recovery theorem is
impossible without additional hypotheses, as Corollary 7 illustrates.
The examples do not estimate latent mean dimensions that the chosen
observations do not span.
