# Why shared observations improve source calibration

Research note, 2026-09-27. Written all-orders identities and conditioning
arguments, with exact symbolic and integer-tensor checks. Not Lean
formalized or independently peer reviewed. The Krenn–Gu paper is unchanged.

## 1. Three different conditioning questions

The earlier notes prove generic source identifiability at every odd order
at least seven. The [blind-search note](blind-source-search-and-local-conditioning-2026-09-27.md)
also gives local mean-line bounds. Neither assertion supplies uniformly
stable covariance recovery.

There are three distinct effects when means have size `t` and covariance
remains of order one:

| Question | Scale | Scope |
| --- | --- | --- |
| Separating an explicit pair of inequivalent sources | Their tensors first differ at order `t^7` | An obstruction for full covariance recovery from one tensor |
| Resolving covariance calibration within one local branch | The weakest calibration singular value has order `t^5` | Also gives a lower bound on local sensitivity of full covariance recovery |
| Calibrating a shared source with separated mean settings | The corresponding calibration singular value has order `t^3` | Assumes the response frame and covariance class have been recovered |

The last row does not give a full-source noise bound: extraction of the
frame, covariance class, and mean coordinates has its own errors. The
results below isolate one source of poor conditioning and show exactly
how shared observations improve it.
All asymptotic constants may depend on the fixed order, source, and
response frame; no bound uniform in the number of sites is asserted.

## 2. The fifth-order involution at arbitrary odd orders

Let `n=2m+1`, and use the commutative site algebra, where a product
using any site twice is zero. Fix a mean direction `L=sum_i l_i` and
a cross-site quadratic `R=sum_(i<j)R_ij`. Write

$$
G(tL,R)=\sum_{q=0}^m t^{2q+1}P_{2q+1},\qquad
P_{2q+1}=\frac{L^{2q+1}}{(2q+1)!}\frac{R^{m-q}}{(m-q)!}. \tag{1}
$$

Each term uses every site once. A response degree such as seven refers
to the number of mean factors in this order-`n` tensor; it is not a
separately measured seventh-order moment. Define

$$
\mathcal I_n(\mu,R)=\left((-1)^m\mu,-R-\frac{\mu^2}{3}\right). \tag{2}
$$

This is an involution. Its block formula is
`R_ij -> -R_ij-(2/3) mu_i tensor mu_j`; the factor two comes from
the ordered terms in the square of `sum_i mu_i`.

**Theorem 1 (universal near-ambiguity).** At every odd order,

$$
G\left((-1)^m tL,-R-\frac{t^2L^2}{3}\right)
 =\sum_{q=0}^m c_q t^{2q+1}P_{2q+1}, \tag{3}
$$

where

$$
c_q=(-1)^q\sum_{j=0}^q
 \frac{(2q+1)!}{(2q+1-2j)!j!}\left(-\frac13\right)^j
 =(2q+1)![x^{2q+1}]\bigl(e^{x^2/3}\sin x\bigr). \tag{4}
$$

The first coefficients are

$$
c_0=c_1=c_2=1,\qquad
c_3=-\frac{23}{9},\quad c_4=-\frac{125}{3},\quad c_5=-\frac{1213}{3}.
$$

In particular, for `n>=7`,

$$
G(\mathcal I_n(tL,R))-G(tL,R)
 =-\frac{32}{9}t^7P_7+O(t^9). \tag{5}
$$

For seven sites this term is the entire difference. At three and five
sites the transformation preserves the entire output exactly.

**Proof.** Expand covariance powers after substituting (2). A term
using `j` copies of `L^2/3` contributes to the response with `2q+1`
mean factors. Its sign is `(-1)^(q+j)`: the covariance sign and the
odd power of the mean sign combine in this way. The factorial ratio
in (4) accounts for the extra `2j` mean factors. Summing gives the
first formula. The coefficient of `x^(2q+1)` in `exp(x^2/3) sin x`
is `sum_j (-1)^(q-j)/(3^j j! (2q+1-2j)!)`, giving the second.
Expansion through degree seven proves (5). This is a finite formal
identity in the site algebra at every order. QED.

### 2.1 The covariance separation survives the site gauge

Fix one coordinate at every site and a cycle passing through all `n`
sites. Let

$$
C(R)=\prod_{\{i,j\}\text{ in the cycle}}R_{ij}[0,0]. \tag{6}
$$

A site scaling `R_ij -> lambda_i lambda_j R_ij` multiplies this product
by `(product_i lambda_i)^2`. Hence it is invariant under the product-one
gauge of the observed tensor.

**Corollary 2 (a full covariance-recovery obstruction).** For a generic
fixed source with `C(R)!=0` and `P_7!=0`, the two source families in (5)
have tensor distance of order `|t|^7`, while

$$
C\left(-R-t^2L^2/3\right)-C(R)\longrightarrow-2C(R)\ne0.
$$

An inverse recovering this gauge-invariant covariance quantity therefore
cannot have a uniformly bounded Lipschitz constant on these families.
The ratio of covariance error to tensor error grows at least as a
constant times `|t|^-7`.

**Proof.** The cycle has odd length, so changing every edge sign changes
its product's sign. The `t^2` correction disappears in the limit, and
(5) gives the tensor distance. Both nonvanishing conditions are generic.
Intersect the generic identifiability open set with its image under the
invertible polynomial map (2). Generic choices meet this intersection
for all but finitely many nonzero `t`, so the comparison can be made
between identifiable sources. QED.

The example stays in a bounded set of real source parameters. Both
sets of cross-site blocks can be completed to positive definite Gaussian
covariance matrices by choosing sufficiently large within-site diagonal
blocks. Those blocks do not affect the observed cross moment. Thus the
obstruction requires neither a negative variance nor a complex probability
distribution.

## 3. Local sensitivity is fifth order

Use the response coordinates from the
[calibration theorem](calibrated-source-reconstruction-all-orders-2026-09-27.md).
For one mean direction these include

$$
F_1=z,\qquad F_3=\beta z^3+3zk,\qquad
F_5=\beta^2z^5+10\beta z^3k+15zk^2, \tag{7}
$$

where `beta` is the remaining covariance scale parameter and `k` its
mean-square correction. These are coefficients of the same order-`n`
observation in a fixed response basis.

**Theorem 3 (local fifth-order obstruction).** At `z=t`, `beta=1`,
`k=0`, a source perturbation that changes a gauge-invariant covariance
quantity at order one can change its tensor at only order `t^5`.
The norm of the local covariance inverse is therefore at least a constant
times `|t|^-5`, generically for every odd `n>=7`.

**Proof.** Keep `z=t` and choose `k=(1-beta)t^2/3`. This holds both
`F_1` and `F_3` fixed. The general odd-coordinate formula gives

$$
\left.\frac{dF_{2q+1}}{d\beta}\right|_{\beta=1}
 =-\frac23q(q-1)t^{2q+1}. \tag{8}
$$

The first nonzero derivative is `-4t^5/3`. A corresponding actual
source path near `beta=1` is

$$
\mu(\beta)=\beta^{m/n}tL,\qquad
R(\beta)=\beta^{-1/n}
 \left(R+\frac{1-\beta}{6}t^2L^2\right). \tag{9}
$$

The roots specify a smooth real local path, not an inverse algorithm.
The derivative of (6) is `-C(R)+O(t^2)`, whereas (8) gives tensor
derivative `-(4/3)t^5 P_5+O(t^7)`. Both leading coefficients are
generically nonzero. Their ratio proves the claim. QED.

Within calibration itself, fifth order is sufficient locally. The
Jacobian of `(F_1,F_3,F_5)` with columns `(z,k,beta)` has determinant
`-4t^6`. Its scale component satisfies

$$
\delta\beta=-\frac{3\delta F_5}{4t^5}
             +\frac{5\delta F_3}{2t^3}
             -\frac{15\delta F_1}{4t},
$$

and the remaining components have no worse growth. Thus its inverse
has norm `O(|t|^-5)`. Adding higher response
coordinates does not change the exponent: the direction
`(delta z,delta k,delta beta)=(0,-t^2/3,1)` gives the matching upper
bound on the least singular value. Thus this singular value is
`Theta(|t|^5)` for every fixed odd order at least five. This upper
conditioning statement concerns calibration in a fixed frame, not the
entire unknown-source inverse.

## 4. Shared observations separate the mirror branch at cubic order

Let the recovered mean frame have dimension `r`. For output `j`, let
`z_j` be its degree-one coefficient vector and `Z_j(x)=z_j^t x`.
The remaining common parameters obey

$$
F_{3,j}(x)=\beta Z_j(x)^3+3Z_j(x)x^tKx. \tag{10}
$$

Here `K` is one common symmetric matrix. Assume the response basis is
independent; then coefficient norm and observed-tensor norm are equivalent
with fixed constants.

**Proposition 4 (cubic separation).** Suppose `z_j=t zeta_j`, with
nonzero fixed `zeta_j`, and at least two matrices `zeta_j zeta_j^t`
differ. At the reference source `beta=1,K=0`, no candidate with
`beta=-1` and one common `K` matches every cubic response. Its best
cubic discrepancy has order `|t|^3`. So does the best full-observation
discrepancy within this mirror family, holding degree-one vectors fixed.

**Proof.** Matching (10) for both signs requires
`K=(2/3)z_jz_j^t` for every `j`, which the hypothesis excludes.
Write `K=t^2 H`; for nonzero `t` this allows every `K`. All cubic
residuals are `t^3` times fixed affine linear functions of `H` with
no common zero. Their least-squares residual has a positive minimum,
since the finite-dimensional linear image is closed. Higher responses
at a fixed minimizing `H` are `O(t^5)`, and independence of the
response basis prevents cancellation of the cubic discrepancy. QED.

For two settings in one direction, take `z_1=t`, `z_2=alpha t`,
with `alpha!=0,1,-1`. The Jacobian of the two linear and two cubic
coordinates, with columns `(z_1,z_2,k,beta)`, has determinant

$$
3z_1z_2(z_2^2-z_1^2)=3\alpha(\alpha^2-1)t^4. \tag{11}
$$

Its inverse has norm `O(|t|^-3)`. A perturbation in `beta` with
common `k` correction of order `t^2` gives the matching opposite
inequality. The least singular value is therefore `Theta(|t|^3)`,
even with all higher odd coordinates retained. This quantifies the
earlier two-output calibration lemma.
For example, subtracting the two linearized cubic equations after
division by `z_j` gives

$$
\delta\beta=
\frac{\delta F_{3,1}/z_1-\delta F_{3,2}/z_2
       -3z_1\delta z_1+3z_2\delta z_2}{z_1^2-z_2^2},
$$

which exhibits the claimed bound even when the degree-one coefficients
are perturbed.

## 5. A sharp sensitivity formula for many shared outputs

For the remaining statements the mean coordinates are real. Fix the
nonzero vectors `z_j` and put

$$
M_j=z_jz_j^t,\qquad
S_j=\frac{F_{3,j}}{3Z_j}=K+\frac\beta3M_j. \tag{12}
$$

The quotient means the symmetric matrix of the quadratic polynomial.
With noisy cubic data it can instead be computed by linear least squares.
For `p` outputs, define

$$
\overline M=\frac1p\sum_j M_j,\qquad
V=\sum_j\|M_j-\overline M\|_F^2. \tag{13}
$$

**Theorem 5 (optimal sensitivity from divided cubic data).**
If `V>0`, the least-squares estimates from the matrices `S_j` are

$$
\widehat\beta=
 \frac{3\sum_j\langle M_j-\overline M,S_j\rangle_F}{V},\qquad
\widehat K=\overline S-\frac{\widehat\beta}{3}\overline M. \tag{14}
$$

For errors `E_j` in `S_j`, let `epsilon^2=sum_j ||E_j||_F^2`. Then

$$
|\delta\beta|\le\frac{3\epsilon}{\sqrt V},\qquad
\|\delta K\|_F\le\frac\epsilon{\sqrt p}
                +\frac{\|\overline M\|_F}{3}|\delta\beta|. \tag{15}
$$

The constant `3/sqrt(V)` is sharp for recovering `beta`, with `K`
unrestricted.

**Proof.** Minimizing over `K` centers the matrices, leaving a
one-parameter linear regression with normal equation (14).
Cauchy–Schwarz gives (15). For sharpness, change `beta` by `delta`
and `K` by `-delta Mbar/3`. The data change by
`delta(M_j-Mbar)/3`, with total norm `|delta|sqrt(V)/3`. Every exact
inverse must distinguish these choices. Formula (14) attains the bound.
QED.

The denominator vanishes precisely when all mean outer products coincide.
In one real direction, all nonzero settings then have the same absolute
amplitude. A sign reversal alone adds no cubic calibration information.

**Lemma 6 (cost of cubic division).** On real symmetric tensors with
Frobenius norm, the map `S -> 3 Sym(z tensor S)` has least singular
value at least `sqrt(3)||z||`. Thus a cubic error `E_3` induces a
least-squares error in `S` of at most `||E_3||/(sqrt(3)||z||)`.
Here `Sym` averages over tensor permutations, and the Frobenius norm
is the square root of the sum of squared tensor entries.

**Proof.** Rotate and rescale to `z=e_1`. Write
`S=a e_1e_1^t+e_1v^t+ve_1^t+C`, with `v,C` outside the first
coordinate. Before multiplying by three, squared output norm is
`a^2+(4/3)||v||^2+(1/3)||C||_F^2`; squared input norm is
`a^2+2||v||^2+||C||_F^2`. Their ratio is at least `1/3`. QED.

For common norm `rho`, (15) yields
`|delta beta| <= sqrt(3) epsilon_3/(rho sqrt(V))` for joint cubic
data error of norm `epsilon_3`. With `z_j=t zeta_j` this has order
`|t|^-3`, as in (11). Errors in the recovered frame and in `z_j`
are outside this conditional bound.

## 6. Setting design is a frame-potential problem

**Corollary 7 (equal-norm design).** Suppose `||z_j||=rho` for every
setting and put `d=min(p,r)`. Then

$$
V=p\rho^4-\frac1p\left\|\sum_j z_jz_j^t\right\|_F^2
 \le p\rho^4\left(1-\frac1d\right). \tag{16}
$$

Equality holds exactly when the sum of outer products has rank `d`
and all its nonzero eigenvalues equal `p rho^2/d`.

**Proof.** Expand (13). The positive semidefinite sum of outer products
has trace `p rho^2` and rank at most `d`. Cauchy–Schwarz for its
nonzero eigenvalues gives both the bound and its equality condition. QED.

If `p<=r`, orthogonal settings attain the bound. If `p>=r`, equality
is the tight-frame condition `sum_j z_jz_j^t=(p rho^2/r)I`.
Repetitions of an orthogonal basis attain it when `p` is a multiple
of `r`. For `r=1`, the equal-norm bound is zero, so amplitudes must vary.

This is the classical frame potential:
`||sum_j z_jz_j^t||_F^2=sum_(j,k)(z_j^t z_k)^2`.
Its tight-frame minimizers are established theory, due to
[Benedetto and Fickus](https://link.springer.com/article/10.1023/A:1021323312367).
Here it optimizes the sharp covariance-scale bound (15), under the
stated noise model for divided cubic matrices. It is not an
optimal-design theorem for every stage of blind source recovery.

## 7. Exact checks, attribution, and remaining work

Run from the repository root:

```sh
OPENBLAS_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 .venv/bin/python computations/matching-tensor-recovery-2026-09-26/source_calibration_conditioning.py
```

The [program](../computations/matching-tensor-recovery-2026-09-26/source_calibration_conditioning.py)
and [certificate](../computations/matching-tensor-recovery-2026-09-26/source-calibration-conditioning-certificate.json)
check (4) through degree thirteen, (8) through degree eleven, and the
exact local Jacobian determinants. At seven and nine sites every tensor
entry of a rational source and its transformed source is checked against
(3), after clearing denominators. Direct differentiation of the matching
recurrence also checks the actual source path in Theorem 3 entry by entry.
A separate matching recurrence checks
both integer tensors with a modulus larger than twice a proved absolute
bound. These are characteristic-zero equality checks.

A four-setting, two-direction example attains both the design bound
(16) and the sharp noise bound (15). Numerical singular values at orders
seven, nine, and eleven illustrate the proved exponents; they are not
used to infer them. At `t=1/32`, the eleven-site ratios
`sigma_single/t^5` and `sigma_pair/t^3` are approximately `1.33333`
and `2.68338`, consistent with their limits `4/3` and `6/sqrt(5)`
for settings `t,2t`.

Gaussian moment formulas are standard; see
[Pereira–Kileel–Kolda](https://arxiv.org/abs/2202.06930).
The fifth-order involution and shared cubic calibration were proved
in the earlier repository note. The new deductions here are their
all-orders near-ambiguity identity, the gauge-invariant conditioning
obstructions, and the sharp shared-calibration design criterion. No
exhaustive priority claim is made.

Shared-covariance Gaussian mixtures use a related but different observation
model; see [Agostini–Améndola–Ranestad](https://arxiv.org/abs/1905.05141).
The data here are labelled multilinear cross moments of individual mean
settings, rather than a mixture's full moment sequence.

The subsequent [full-source stability note](full-source-local-stability-2026-09-27.md)
uses the joint forward derivative to give finite local bounds for every
mean and covariance parameter, with explicit neighborhood certificates.
It also proves additive covariance information after eliminating unknown
means, a local correction iteration, and stability of the observed mean
span. These results avoid conditioning the bound on an exactly recovered
intermediate frame or covariance class. Their constants depend on the
source and do not remove the information-loss mechanisms proved here.
Global initialization and the earlier nonlinear search failure remain
unresolved.
