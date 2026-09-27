# Source recovery from products of local scalar measurements

Research note, 2026-09-27. Application of established algebraic measurement
theorems, with written proofs of the model-specific consequences and exact
local certificates. Not Lean formalized or independently peer reviewed.
The Krenn–Gu paper is unchanged.

## 1. What information is actually needed?

The [all-orders inverse](single-cross-moment-all-orders-2026-09-27.md)
uses a full Gaussian cross-moment tensor. At `n` sites with three
coordinates per site, that tensor has `3^n` entries. Its source has only

$$
d=3n+9\binom n2-(n-1) \tag{1}
$$

effective parameters: means and cross-site covariance entries, less the
product-one site-scaling freedom. An existing theorem of
[Gesmundo–Grosdos–Uschmajew](https://arxiv.org/abs/2505.24328), Theorem 1.1,
allows the full tensor to be replaced, for generic identifiability, by
`d+1` products of local scalar measurements. The measurements themselves
belong to a structured family; they need not be arbitrary dense linear
functionals on the tensor.

| Sites | Full tensor entries | Effective source parameters `d` | Generic identifiability: `d+1` scalar data | Preserve all tensor distinctions: `2d` scalar data |
| --- | --- | --- | --- | --- |
| 7 | 2187 | 204 | 205 | 408 |
| 9 | 19683 | 343 | 344 | 686 |
| 11 | 177147 | 518 | 519 | 1036 |

The `d+1` statement is an application of established theory, not a new
general measurement theorem. The `2d` statement below uses the standard
geometry of differences of model tensors. These counts concern exact
scalar expectations. They are not sample-complexity bounds, counts of
experimental trials, or polynomial-time reconstruction algorithms.

The computation establishes full local source rank using these small
data sets and finite local noise bounds using `2d` probes. It takes the
source as input. It neither recovers an unknown source blindly nor proves
global injectivity of the particular finite probe lists saved on disk.

## 2. Product measurements and the dimension of the source model

Let site `i` have vector space `V_i=C^(d_i)`, with `d_i>=3`, and let
`n>=7` be odd. Put `V=V_0 tensor ... tensor V_(n-1)`. A source consists
of means `mu_i in V_i` and edge blocks `R_ij in V_i tensor V_j`.
Its output `T=F(mu,R) in V` is the Gaussian matching sum: each matching
contributes its edge blocks and the means at unmatched sites.

A **product measurement** chooses one covector `u_i in V_i^*` at each
site and records

$$
\ell_u(T)=\langle u_0\otimes\cdots\otimes u_{n-1},T\rangle
=\mathbb E\left[\prod_{i=0}^{n-1}u_i(X_i)\right]. \tag{2}
$$

The right side has its usual meaning for real Gaussian variables; in the
complex model it denotes the same polynomial matching expression.
The pairing is bilinear, with no complex conjugation. Multiplying a
measurement covector by a known nonzero scalar does not change its
identifying power, so local normalization is possible.

Let `X` be the complex Zariski closure of all output tensors: the smallest
algebraic set containing their polynomial image. It includes limiting
model tensors, whether or not a particular limit has a finite source
representation. For `p` labelled outputs with common covariance, define
`X_p` similarly in `C^p tensor V`. Write

$$
D=\sum_i d_i,\qquad E=\sum_{i<j}d_i d_j.
$$

**Lemma 1 (model dimensions and scaling).** The varieties `X` and `X_p`
are irreducible cones and have dimensions

$$
\dim X=D+E-(n-1),\qquad
\dim X_p=pD+E-(n-1). \tag{3}
$$

If the matrix of flattened mean vectors has rank at most `r`, where
`1<=r<=min(D,p)`, the corresponding closed output model has dimension

$$
d_{p,r}=r(D+p-r)+E-(n-1). \tag{4}
$$

Here a cone means that every scalar multiple of a tensor is again in
the variety. These varieties span their full ambient tensor spaces and
are nonlinear for the stated orders and dimensions.

**Proof.** The source spaces are irreducible. In the rank-constrained
case the means form the irreducible variety of `D by p` matrices of
rank at most `r`, of dimension `r(D+p-r)`; the covariance entries are
independent parameters. The generic fibers of the full-output source
map have dimension `n-1`, by the earlier common-source recovery theorem:
they consist precisely of the common product-one site scalings. This
remains true with the mean-rank constraint. For any one labelled setting,
the projection from the rank-constrained mean family onto its mean vector
is dominant. Hence the finitely many single-output generic conditions
hold simultaneously on a nonempty open set. Site scaling preserves the
rank of the mean matrix. Alignment of the gauges uses the generic
covariance, so it does not require independent mean columns. The
fiber-dimension formula gives (3) and (4).

Scaling every mean by `t` and every covariance block by `t^2` scales
every matching term by `t^n`. Over `C` this gives every output scalar
multiple, so the closures are cones. Setting covariance to zero and
using a nonzero mean only in one labelled setting gives an arbitrary
pure tensor in that block. Such tensors span the ambient space and
already use a mean matrix of rank one. The dimensions in (3) and (4)
are strictly below the ambient dimension for `n>=7` and `d_i>=3`.
An irreducible linear cone spanning its ambient space would be the whole
space; thus these models are nonlinear. QED.

For shared outputs, an allowed structured linear functional is

$$
\ell_{a,u}(T_1,\ldots,T_p)=
\sum_{s=1}^p a_s\langle u_0\otimes\cdots\otimes u_{n-1},T_s\rangle.
\tag{5}
$$

The coefficient vector `a` is part of the known measurement design.
The measurement covectors in (2) or (5), including zero, form an
irreducible algebraic cone and span the entire dual space. This follows
either from their multilinear parameterization or from the usual
description of rank-one tensors. Spanning also follows directly by
choosing coordinate covectors.

Equation (5) is a linear combination of labelled observations. Computing
one such scalar may require measurements at several mean settings. The
algebraic count does not treat that combination as a free physical
experiment or bound the number of samples required to estimate it.

## 3. Almost minimal generic identification

**Theorem 2 (product measurements identify generic sources).** Let `d_X`
be the applicable dimension from (3) or (4). For a generic choice of
`d_X+1` measurements from (2) or (5), a generic source is determined
up to the common product-one site scalings. Alternative source
representations, including exceptional ones, are excluded whenever they
were excluded by the full-tensor theorem.

More precisely, for any fixed tensor in the closed model, a generic
tuple of `d_X+1` product measurements identifies that tensor among all
points of the model. The open set of good measurement tuples in this
fixed-tensor statement may depend on the tensor.

**Proof.** Apply Theorem 1.1 of
[Gesmundo–Grosdos–Uschmajew](https://arxiv.org/abs/2505.24328)
to the model variety and the irreducible, spanning measurement family
described above. It identifies the output tensor. The earlier source
theorem then identifies its generic source class. The corresponding
generic-measurement, generic-source statement follows from the same
incidence argument, or by taking the generic fibers of the bad-pair
incidence set. QED.

The quantifiers matter: `d_X+1` generic measurements for a fixed tensor
do not supply one measurement list identifying every tensor at once.
The next section gives a sufficient uniform count.

**Proposition 3 (sharpness of the generic complex threshold).** For
these nonlinear conical models over `C`, `d_X` generic product
measurements have more than one preimage at a generic output. Thus
`d_X+1` is the smallest generic measurement count giving generic
identifiability. Special measurement choices can behave differently;
the proposition does not assert a lower bound for all adaptive designs.

**Proof.** Let `Z` be the projectivization of the model. It has dimension
`d_X-1`. For any nonzero tensor, some product covector evaluates
nontrivially. Intersecting with a generic measurement hyperplane therefore
lowers the dimension of every remaining positive-dimensional component.
Equivalently, a bad-incidence dimension count shows that `d_X` generic
measurement hyperplanes have no common point on `Z`.
The resulting linear projection from the affine cone to `C^(d_X)` is
finite. Its degree is the projective degree of `Z`, by the standard
degree formula for a linear projection whose center misses the variety.
That degree exceeds one because the irreducible model is nonlinear.
In characteristic zero the generic fiber consists of that many distinct
points. The full-tensor exceptional set has smaller dimension, so a
generic such fiber consists of ordinary identifiable model tensors,
giving distinct source classes. QED.

This is the degree argument used in algebraic compressed sensing; see
[Breiding–Gesmundo–Michałek–Vannieuwenhoven](https://arxiv.org/abs/2108.13208),
Question 7 and its proof. Here the product measurement family still
permits a projection center disjoint from `Z`. Over the real numbers,
some additional complex preimages may be nonreal; only the complex
sharpness is claimed. Fewer than `d_X` scalar data cannot locally
identify a generic source over either field, by dimension.

**Corollary 3.1 (many candidates from a square subsystem).** If the
ambient tensor space has dimension `N`, a generic system of `d_X`
product measurements has at least `N-d_X+1` distinct complex source
classes over a generic measured value. For one output in local dimension
three this lower bound is `3^n-d+1`: it is 1984, 19341, and 176630
at seven, nine, and eleven sites, respectively.

**Proof.** The model is irreducible and spans the ambient space.
The classical degree bound for a nondegenerate projective variety gives
`degree(Z)>=1+codimension(Z)=N-d_X+1`; see the opening degree inequality
in [Eisenbud–Green–Hulek–Popescu](https://eisenbud.github.io/papers/pdfs/2006-002.pdf).
Combine this with the generic fiber degree in Proposition 3 and generic
source identifiability for each full tensor. QED.

This is an obstruction to the strategy of enumerating **all** complex
solutions of a generic square subsystem and then using an extra
measurement to choose one. Its candidate count grows exponentially
with `n`. It is not a lower bound for every reconstruction algorithm,
and it does not assert that those extra candidates are real. An
overdetermined solver using all measurements need not enumerate them.

## 4. One measurement design preserving all tensor distinctions

Define the closed difference cone

$$
\Delta=\overline{\{T-T':T,T'\in X\}}, \tag{6}
$$

with the appropriate shared-source model substituted for `X` if needed.
The bar is Zariski closure. Its dimension is at most `2d_X`, because
the difference map has domain `X times X`. Its projectivization has
dimension at most `2d_X-1`.

**Theorem 4 (uniform tensor separation).** A generic choice of `2d_X`
product measurements gives a linear map `A` whose kernel intersects
`Delta` only at zero. In particular, `A` is injective on the entire
closed tensor model. For any such fixed map there is a positive constant
`alpha_A` such that

$$
\alpha_A\|T-T'\|\le\|A T-A T'\|
\le\|A\|\,\|T-T'\|\qquad(T,T'\in X). \tag{7}
$$

The norm is the Euclidean norm of complex or real tensor coordinates.

**Proof.** Let `S` be the projective product-covector variety, of
dimension `s`. For each nonzero `z`, the measurement equation
`ell(z)=0` cuts a proper subvariety of `S`, of dimension at most
`s-1`, since `S` spans the dual space. The incidence of a direction
`[z] in P Delta` and `k` measurements annihilating it has dimension
at most `2d_X-1+k(s-1)`. At `k=2d_X` this is smaller than `ks`.
All varieties in this incidence are projective, so its image in `S^k`
is closed and proper. Its complement consists of the required designs.
Finally, the unit-norm vectors in `Delta` form a compact set, and
`||A z||` has a strictly positive minimum there. That minimum gives
the first inequality in (7); the second is the operator-norm bound. QED.

The secant/difference-cone principle is standard; compare Question 9 and
Example 9 of
[Algebraic compressed sensing](https://arxiv.org/abs/2108.13208).
The proof above checks its application to products of local covectors.
It does not compute `alpha_A`, assert a useful numerical distortion,
or certify that a particular small-integer probe list is in the good set.

This uniform result concerns **tensor distinctions**, not uniform
stability of the nonlinear map from sources to tensors. The previously
proved [source near-ambiguities](shared-calibration-and-near-ambiguity-2026-09-27.md)
remain: nearly equal full tensors also have nearly equal compressed
measurements, by the upper bound in (7).

**Corollary 5 (uniform threshold at the checked orders).** At local
dimension three and `n=7,9,11`, the difference cone has dimension
exactly `2d`. Consequently `2d` is the generic complex threshold for
one product-measurement design that distinguishes every model tensor.

**Proof.** The exact minors described below exhibit rank `2d` for
the derivative of `A(F(theta)-F(theta'))` at a pair of sources.
Thus the uncompressed difference map has rank at least `2d`; (6)
gives the matching upper bound. To see generic failure at `2d-1`
measurements, intersect `P Delta`, now of dimension `2d-1`, with
their hyperplanes. The intersection is nonempty by projective dimension.
The actual nonzero differences contain a dense open subset of `P Delta`.
Its exceptional complement has dimension at most `2d-2`; the same
incidence count as above shows that generic `2d-1` product
hyperplanes avoid that complement. Hence an actual nonzero difference
is annihilated. Fewer measurements cannot repair that collision. QED.

This corollary is limited to the three certified orders. The all-orders
upper bound in Theorem 4 does not need nondefectivity of the difference
cone. Neither corollary asserts global injectivity of the saved designs.

## 5. Evaluation, derivatives, and local noise without a full tensor

For one probe put

$$
b_i=u_i^t\mu_i,\qquad C_{ij}=u_i^tR_{ij}u_j.
$$

Define scalar matching values on subsets of sites by

$$
h(\varnothing)=1,\qquad
h(S)=b_i h(S\setminus\{i\})+
\sum_{j\in S\setminus\{i\}}C_{ij}h(S\setminus\{i,j\}). \tag{8}
$$

The measured value is `h(all sites)`. The smaller-response identity gives

$$
\frac{\partial\ell_u(F)}{\partial\mu_i[a]}
=u_i[a]h([n]\setminus\{i\}),\qquad
\frac{\partial\ell_u(F)}{\partial R_{ij}[a,b]}
=u_i[a]u_j[b]h([n]\setminus\{i,j\}). \tag{9}
$$

Here `[n]` denotes all `n` sites. No full tensor is needed to evaluate
these expressions. A subset recurrence for `k` probes uses at most
`O(k n 2^n)` arithmetic operations and `O(k 2^n)` stored scalar values.
The forward evaluation is still exponential in `n`; a polynomial number
of measured scalars does not establish an efficient global inverse.

The local certificates use real parameters and the same covariance gauge as the
[full-source stability note](full-source-local-stability-2026-09-27.md):
hold `(R_0j)[0,0]` fixed and nonzero. The free parameter dimension is
then (1). The saved probes have local rows `(1,+/-1,+/-1)`.

**Lemma 6 (compressed curvature bound).** On the unit parameter ball
around a supplied source, replace `b_i` in (8) by `|b_i|+2` and
`C_ij` by `|C_ij|+3`, and denote the positive recurrence by `h_u^+`.
A squared Hessian-norm bound for the stacked measured map is

$$
L_A^2=\sum_u\sum_{2\le |U|\le4}
w(U)\,h_u^+([n]\setminus U)^2, \tag{10}
$$

where `w(U)` is `18` for two sites, `150` or `162` for three sites,
and `432` or `486` for four sites. In the latter two cases use the
first value when site zero is in `U`, and the second otherwise.

**Proof.** The squared insertion weight of a mean block is three.
For an edge block it is nine, except for a fixed-star block, whose
one fixed coordinate leaves weight eight. Their square roots are
bounded by two and three, proving the majorant on the unit ball.
Two differentiations with overlapping site supports give zero.
For disjoint supports, the second derivative is the product of the
insertion coefficients and the complementary matching value.
For two removed sites the ordered-support weight is `2*3*3=18`.
For three sites it is six times the sum of their three edge weights.
For four sites it is twice the sum of the products of edge weights
over the three perfect matchings. These give exactly (10). Summing
squared second partials bounds the squared Hessian operator norm. QED.

Apply the integer preconditioner test of the full-source note to
`J_A=D(A F)` and its Gram matrix, using (10) for curvature. Its finite
noise theorem and frozen left-inverse iteration then apply to the
compressed data directly. No intermediate recovered mean frame or
full tensor is assumed. The constants concern the raw signed products
in (2); normalized probes change the data scale and the constants.

## 6. Exact certificates and their limits

The [program](../computations/matching-tensor-recovery-2026-09-26/product_measurements.py)
and [saved certificate](../computations/matching-tensor-recovery-2026-09-26/product-measurement-certificate.json)
use distinct probe codes specifying the local sign rows. Sources have
integer entries in `{-2,-1,1,2}`. At each order, the first `d` rows
already have a nonzero `d by d` derivative minor modulo `1000003`:

| Sites | Source derivative rank | Minor residue | Difference derivative rank | Difference minor residue |
| --- | --- | --- | --- | --- |
| 7 | 204 | 447910 | 408 | 136323 |
| 9 | 343 | 970422 | 686 | 970658 |
| 11 | 518 | 620000 | 1036 | 50341 |

Since these are minors of integer matrices, nonzero residues prove the
same ranks over the rationals, reals and complex numbers. The certificate
also records the second source used for the difference derivative.
The `d`, `d+1`, and `2d` local rank checks refer to nested probe lists.
They illustrate why local rank and global uniqueness must be kept separate:
a square nonsingular derivative does not eliminate distant alternatives.

For `2d` probes, exact integer preconditioner witnesses and (10) give
finite source-error and local-iteration bounds. The certified inverse
derivative bounds are smaller than `0.009244`, `0.000536`, and
`0.000042`, respectively; the corresponding parameter radii are about
`9.68e-6`, `1.35e-6`, and `1.56e-7`. These conservative absolute
constants do not establish useful noise tolerance at any particular
experimental sample budget.

Generate the examples from the repository root:

```sh
OPENBLAS_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 .venv/bin/python computations/matching-tensor-recovery-2026-09-26/product_measurements.py
```

Replay the saved exact witnesses:

```sh
OPENBLAS_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 .venv/bin/python computations/matching-tensor-recovery-2026-09-26/verify_product_measurements.py
```

The [replay](../computations/matching-tensor-recovery-2026-09-26/verify_product_measurements.py)
uses a separate Python-integer recurrence, removing the largest site
first, to check every scalar measurement and every derivative entry at
both sources. It reconstructs curvature coefficients by enumerating free
parameter pairs. All minors and saved preconditioner residuals are checked
exactly. The replay constructs no full tensor and uses no numerical
eigensolver. The generator separately compares four probe contractions
against full tensors and their Jacobians at seven and nine sites only.

The finite sign lists are not continuously generic samples. The tests
certify their local behavior and provide difference-dimension witnesses;
they do not certify the global hypotheses of Theorems 2 or 4 for those
specific lists. The generic theorems are proved separately over the full
product-covector family.

## 7. Consequences for shared directions and remaining work

For four shared outputs at seven sites, (3) gives `d_X=267`; 268
generic mixed product scalars therefore determine the generic common
source. If the global mean matrix is known to have rank at most two,
(4) reduces that dimension to 229 and the scalar count to 230.
These are applications of the written theorem, not additional numerical
recoveries in the certificate. Local dimension three imposes no barrier
to recovering four observed global directions.

The new conclusion is that the exponential number of full-tensor entries
is not an information requirement for generic source recovery. Existing
algebraic measurement theory gives the reduction once the copy-based
source theorem supplies the correct model and dimension. The response
identities then give direct scalar derivatives and local certificates.
No priority claim is made for the underlying measurement or perturbation
machinery.

The remaining practical tasks are global inversion from compressed data,
certification of particular probe designs beyond local rank, sharper
noise bounds, and statistical accuracy of the product-moment estimates.
The existing blind full-tensor search failure is not resolved by the
measurement-count theorem. All-orders nondefectivity of the difference
cone, which would make the uniform `2d_X` threshold sharp at every order,
also remains unproved here.
