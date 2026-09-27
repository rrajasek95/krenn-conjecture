# Recovering mean directions by two commutator kernel conditions

Research note, 2026-09-27. Written all-orders proof, rational reconstruction,
and exact computational certificates. Not Lean formalized or independently
peer reviewed. The Krenn–Gu manuscript is unchanged.

## 1. Result and relation to the earlier inverse

**Theorem 1 (constructive generic mean recovery).** Let `n>=3` be odd,
and let each local vector space have dimension at least three. A generic
complex monomer–dimer source has all its local mean lines determined by
its single full cross-moment tensor, among **all** source representations
of that tensor. No alternative representation has a zero mean.
The lines can be recovered by matrix inversion, multiplication, and two
kernel computations, followed by factoring a rank-one tensor. No root
search or polynomial-system solver is required on the specified open set.

For local dimension three, the matrices have order `N=3^(n-1)`.
The resulting dense algorithm uses `O(N^3)` field operations and
`O(N^2)` memory. This is polynomial in the size of the full observed
tensor, but exponential in the number of sites. It is not an algorithm
for recovering the source from only the smaller collection of scalar
[product measurements](product-measurement-source-recovery-2026-09-27.md).

Combining this theorem with the existing
[covariance inverse](quadratic-size-source-inverse-2026-09-27.md)
gives an explicit rational full-source inverse at every odd order at
least seven on a nonempty Zariski open set. Five sites still have the
two covariance classes described by the
[calibration theorem](calibrated-source-reconstruction-all-orders-2026-09-27.md).
Three sites have the continuous ambiguity described in Proposition 9
below, even though their mean lines are generically identifiable.

The new proof replaces the earlier
[mean-direction attachment induction](mean-direction-recovery-all-orders-2026-09-27.md)
with one nine-dimensional calculation and its tensor powers. It also
extends the lower threshold from five to three sites. The
[recorded nonlinear-search failure](blind-source-search-and-local-conditioning-2026-09-27.md)
at nine sites is now recovered exactly by this different algorithm,
including every cross-site covariance block. The failed numerical run
is preserved; its convergence properties have not changed.

## 2. Definitions and the observable matrices

First set `V_i=C^3`, with sites `i=0,...,n-1`. Fix coordinate vectors
`e_0,e_1,e_2` at each site. A source consists of mean vectors
`mu_i in V_i` and cross-site blocks `R_ij in V_i tensor V_j` for `i<j`.
The observed tensor is

$$
T=G(\mu,R)=\sum_M
 \left(\bigotimes_{\{i,j\}\in M}R_{ij}\right)
 \otimes\left(\bigotimes_{i\text{ unmatched in }M}\mu_i\right). \tag{1}
$$

Here `M` ranges over all matchings of the sites, including the empty
matching; each term is placed in the original site order. For a Gaussian
vector, (1) is the full cross moment. Algebraically, the blocks may be
arbitrary complex matrices. Within-site covariance blocks do not occur
in this observation and are not recovery targets.

A **mean line** is the one-dimensional subspace `C mu_i`. It records
direction, without choosing a magnitude. A **product tensor** is a
nonzero tensor of the form `u_0 tensor ... tensor u_(n-1)`.

Let `epsilon_abc` be the alternating symbol with `epsilon_012=1`.
For a tensor `D` on any number `s` of these sites, define its exterior
matrix by

$$
\mathcal A_s(D)_{r,t}
 =\sum_c D_c\prod_{i=1}^{s}\epsilon_{r_i t_i c_i},
 \qquad r,t,c\in\{0,1,2\}^s. \tag{2}
$$

Thus each row and column is indexed by a coordinate word. This is the
tensor product of the local exterior-product maps, expressed in volume
coordinates: a standard tensor-product Koszul flattening. It is symmetric
for even `s` and skew-symmetric for odd `s`.

**Lemma 2 (product kernel and local quotients).** For nonzero `u_i`,
write `q_i:V_i -> V_i/Cu_i` for the quotient map. Then

$$
\mathcal A_n(T)(u_0\otimes\cdots\otimes u_{n-1})=0
 \quad\Longleftrightarrow\quad
 (\bigotimes_i q_i)T=0. \tag{3}
$$

For an odd-order matching tensor with all means nonzero, (3) holds with
`u_i=mu_i`.

**Proof.** The map with entries `sum_b epsilon_abc u_b` has kernel
`Cu` and rank two, so it factors as the quotient followed by an injective
map. Tensoring these factorizations proves (3). Every matching on an odd
number of sites leaves a mean factor unmatched. Projecting out every
mean line therefore kills every term of (1). QED.

Separate site zero and write

$$
T=\sum_{a=0}^{2}e_a\otimes T_a,\qquad
B_a=\mathcal A_{n-1}(T_a),\qquad N=3^{n-1}. \tag{4}
$$

The three `B_a` are observable symmetric `N` by `N` matrices, and

$$
\mathcal A_n(T)=
\begin{bmatrix}
 0&B_2&-B_1\\
 -B_2&0&B_0\\
 B_1&-B_0&0
\end{bmatrix}. \tag{5}
$$

On the coordinate chart where `B_0` is invertible, put

$$
A=B_0^{-1}B_1,\qquad B=B_0^{-1}B_2,\qquad
C=AB-BA,\qquad Z(T)=\ker C\cap\ker(CA). \tag{6}
$$

The letter `C` in (6) denotes a commutator matrix, not a covariance.
If a different slice is invertible, permute the site-zero coordinates
before using these formulas.

## 3. An observable uniqueness certificate

**Lemma 3 (two-kernel criterion).** Suppose `B_0` is invertible and
`dim Z(T)=1`. There is at most one tensor line of the form `u tensor v`
in `ker A_n(T)`, where `u in C^3` and `v in C^N` are nonzero.
If one exists, it is recovered by (6) and scalar ratios. In particular,
the assertion does not assume that `v` factors over the remaining sites.

**Proof.** Write `u=(u_0,u_1,u_2)`. The last two block equations in
(5) are

$$
u_0B_1v=u_1B_0v,\qquad u_0B_2v=u_2B_0v. \tag{7}
$$

If `u_0=0`, invertibility of `B_0` forces `u_1=u_2=0`, a contradiction.
Consequently

$$
Av=\alpha v,\quad Bv=\beta v,\qquad
\alpha=u_1/u_0,\quad\beta=u_2/u_0. \tag{8}
$$

These equations imply `Cv=CAv=0`, so `v` lies in the one-dimensional
space `Z(T)`. They then determine `alpha,beta`, and hence the line of
`u`. Conversely, any common eigenvector in (8) satisfies all three block
equations with `u=(1,alpha,beta)`. QED.

The same argument excludes infinitesimal multiplicity when the product
line exists. On the chart `u_0=1`, the equations (8) imply the linear
equations `Cv=CAv=0` as polynomial consequences. Those linear equations
cut out one reduced projective point; `alpha,beta` are then fixed.
Intersecting with the product-tensor variety retains that reduced point.

**Corollary 4 (all representations share the recovered mean lines).**
If `T` is a matching tensor satisfying Lemma 3, and a nonzero product
tensor in its exterior kernel is exhibited, then every matching-source
representation of `T` has nonzero local means and the same mean lines.

**Proof.** Lemmas 2 and 3 handle representations with nonzero means.
For a representation with zero means at a nonempty set `S`, replace
each such mean by `t w_i`, keeping all other parameters fixed. The
universal product-kernel identity for the perturbed source is divisible
by `t^|S|`. Dividing and setting `t=0` shows that

$$
\left(\bigotimes_{i\in S}w_i\right)
 \otimes\left(\bigotimes_{i\notin S}\mu_i\right)
 \in\ker\mathcal A_n(T)
$$

for every choice of nonzero `w_i`. Varying one such line contradicts
Lemma 3. QED.

For a rational input, this is an exact, input-specific global uniqueness
certificate for mean lines. It is stronger than checking only that the
quotient equations have an injective derivative at the proposed answer.
The rank condition alone, for an arbitrary tensor, does not assert that
a common eigenvector or a product tensor exists; existence is checked
separately or follows from the source hypothesis.

## 4. The fixed two-site calculation

Identify `C^3 tensor C^3` with three-by-three matrices, writing
`e_ab=e_a tensor e_b`. For a three-by-three tensor `D`, write
`Phi(D)=A_2(D)`. Define

$$
H=\Phi(I_3),\quad E=e_{01}+e_{10},\quad F=e_{02}+e_{20},
\quad A_*=H^{-1}\Phi(E),\quad B_*=H^{-1}\Phi(F),
\quad C_*=[A_*,B_*]. \tag{9}
$$

**Lemma 5 (nine-dimensional witness).** The following identities hold:

$$
H(X)=\mathrm{tr}(X)I_3-X^t,\qquad \det H=-2, \tag{10}
$$

$$
\det(zI-C_*)=z^3(z^2+1)(z^2+4)^2,
\qquad C_*^5+5C_*^3+4C_*=0. \tag{11}
$$

In particular, `C_*` is diagonalizable and has eigenvalues in
`{0,i,-i,2i,-2i}`. Its kernel is

$$
U=\mathrm{span}\{v,u_1,u_2\},\qquad
v=e_{00},\quad u_1=e_{21}-e_{12},\quad u_2=e_{11}+e_{22}. \tag{12}
$$

Moreover,

$$
C_*A_*v=0,\quad C_*A_*u_1=e_{01}-e_{10},\quad
C_*A_*u_2=2(e_{02}+e_{20}). \tag{13}
$$

Thus `ker(C_* A_*|_U)=Cv`, and the image in (13) is contained in
`im C_*`, which is complementary to `U`.

**Proof.** Substituting the alternating symbols into (2) gives (10).
For a short exact verification of the remaining identities, form
`A_*,B_*` by (9), multiply, and evaluate the two polynomials in (11).
The saved certificate gives all entries of `H,2A_*,2B_*` and the three
columns in (12)–(13). A further nonzero rank witness is the minor of
the stacked matrix `[C_*;C_*A_*]` at zero-based row indices
`[1,2,3,4,5,6,10,11]` and column indices `[1,2,3,4,5,6,7,8]`:
its determinant is `8`. These are fixed rational calculations, reproduced
independently by the audit program. The annihilating polynomial in (11)
has distinct complex roots, proving diagonalizability and the stated
direct sum. QED.

## 5. One explicit witness for every odd order

Let `n=2m+1`. Pair the sites other than zero as `(2k+1,2k+2)`, for
`k=0,...,m-1`. Give every site mean `e_0`. Set the covariance within
each pair equal to `diag(0,1,1)`, and all blocks between distinct pairs
equal to zero. For either site `j` in pair `k`, take

$$
R_{0j}=3^k e_1\otimes e_1+e_2\otimes e_2. \tag{14}
$$

For a nine-dimensional operator `D`, let `D^(k)` mean that it acts
on pair `k` and as the identity on all other pairs.

**Lemma 6 (paired witness).** For the source (14), `B_0` is invertible
and `Z(T)=C v^(tensor m)`. More precisely,

$$
T_0=I_3^{\otimes m},\qquad
T_1=\sum_{k=0}^{m-1}3^k I_3^{\otimes k}\otimes E\otimes
 I_3^{\otimes(m-1-k)},\qquad
T_2=\sum_{k=0}^{m-1}I_3^{\otimes k}\otimes F\otimes
 I_3^{\otimes(m-1-k)}, \tag{15}
$$

$$
B_0=H^{\otimes m},\qquad
A=\sum_k3^k A_*^{(k)},\quad B=\sum_k B_*^{(k)},\quad
C=\sum_k3^k C_*^{(k)}. \tag{16}
$$

**Proof.** In the zero-coordinate slice, site zero is a monomer and
each remaining pair contributes `e_00+diag(0,1,1)=I_3`. In either
other slice, site zero is joined to exactly one pair. Joining to either
endpoint leaves the other endpoint as a monomer and contributes `E`
or `F`. All remaining pairs contribute `I_3`. This proves (15).
The exterior map respects tensor products. Operators at different
pairs commute, giving (16).

By Lemma 5, all eigenvalues of `C` have the form

$$
\mathrm{i}\sum_{k=0}^{m-1}3^k\delta_k,
\qquad\delta_k\in\{-2,-1,0,1,2\}. \tag{17}
$$

If `j` is the largest index with `delta_j` nonzero, its contribution
has absolute value at least `3^j`, while the sum of the absolute values
of all lower contributions is at most
`2 sum_(k<j)3^k=3^j-1`. Therefore (17) vanishes only when every
`delta_k=0`. It follows that

$$
\ker C=U^{\otimes m},\qquad \dim\ker C=3^m. \tag{18}
$$

On this subspace, all terms of `CA` involving two distinct pair indices
vanish: the `C_*` factor kills its `U` factor. Consequently

$$
CA\big|_{U^{\otimes m}}
 =\sum_k3^{2k}(C_*A_*)^{(k)}\big|_{U^{\otimes m}}. \tag{19}
$$

The image of summand `k` lies in
`U tensor ... tensor im C_* tensor ... tensor U`, with `im C_*`
in position `k`. These spaces form a direct sum because
`C^9=U direct_sum im C_*`. There can therefore be no cancellation
between different summands in (19). Their common kernel is

$$
\bigotimes_k\ker(C_*A_*|_U)=(\mathbb Cv)^{\otimes m},
$$

by (13). This proves the lemma. QED.

**Proof of Theorem 1 in dimension three.** The condition `det B_0!=0`
is open in source space. On that chart, the entries in (6) are rational
functions. The condition that `[C;CA]` have rank at least `N-1` is
also open after clearing denominators. Lemma 6 supplies an explicit
point satisfying both conditions at every odd order. On the dense
open set with nonzero means, Lemma 2 gives a nonzero product tensor
in the common kernel, so its dimension is exactly one. Lemma 3 and
Corollary 4 prove uniqueness among all representations. A one-dimensional
kernel is computed rationally on any chart with a nonzero maximal minor;
the scalar ratios in (8) and the factors of a product tensor are also
rational. QED.

**Corollary 7 (larger local spaces and unknown response coefficients).**
Theorem 1 extends to arbitrary local dimensions at least three.
Generic local mean-line recovery also holds if the matching layers
with different numbers of edges have generic unknown coefficients.

**Proof.** For larger spaces, first retain coordinates `0,1,2` at
each site. Then, for each extra coordinate `a` at site `i`, retain
coordinates `0,1,a` there and the baseline triples elsewhere. Every
such projection maps the source parameter space surjectively onto
the three-dimensional source space. Thus the preimages of the good
open sets in Theorem 1 have nonempty finite intersection. Require also
that every coordinate-zero mean entry be nonzero. The projected lines
then recover all coordinate ratios using their shared coordinate zero.
Alternative representations are covered by the same projected uniqueness.

For unknown layer coefficients, Lemma 2 remains true term by term.
The witness with all coefficients equal to one lies in this enlarged
parameter space, so the same open-rank argument applies. This does
not remove the covariance calibration ambiguities of that model. QED.

## 6. A consequence for tensors beyond matching sources

Given lines `l_i in P(V_i)`, define the linear space

$$
\mathcal F(l)=\ker(\bigotimes_i q_{l_i})
 =\sum_i V_0\otimes\cdots\otimes l_i\otimes\cdots\otimes V_{n-1}.
 \tag{20}
$$

Thus a tensor is in `F(l)` precisely when removing these local directions
annihilates it. Call such a tuple `l` a **compression center** here; this
is a tuple of lines, not a selected source representation. In dimension
three, `dim F(l)=3^n-2^n`. The union of these spaces is denoted `X_n`.
No matching decomposition is assumed in this definition.

**Theorem 8 (generic compression-center recovery).** For every odd
`n>=3`, a generic tensor in `X_n` has a unique compression center,
recovered by (6). Moreover,

$$
\dim X_n=3^n-2^n+2n,\qquad
\mathrm{codim}_{(\mathbb C^3)^{\otimes n}}X_n=2^n-2n. \tag{21}
$$

The incidence map from pairs `(l,T)` with `T in F(l)` to `X_n` is
birational.

**Proof.** The incidence is a vector bundle of rank `3^n-2^n` over
`(P^2)^n`, hence is irreducible of dimension `3^n-2^n+2n`. It is
closed in the product of this projective base with tensor space.
Projection to tensor space is proper, so its image `X_n` is closed
and irreducible. Every incidence point supplies a product tensor in
the exterior kernel by Lemma 2's equivalence, which did not use (1).
The paired witness is an incidence point satisfying the observable
rank condition. That condition defines a nonempty open set in `X_n`.
Lemma 3 makes each fiber over this set a single center, and its explicit
rational reconstruction gives a rational inverse to the incidence map.
The dimension and codimension follow. QED.

This is also a statement about established osculating geometry.
The projectivization of `F(l)` is the `(n-1)`-st osculating space
of the Segre variety at `l_0 tensor ... tensor l_(n-1)`:
derivatives of the product parametrization of order at most `n-1`
change at most `n-1` local factors, leaving at least one fixed factor.
This identifies (20) with a standard construction; it is not a claim
to have introduced compression or osculating spaces.

**Proposition 9 (the three-site source ambiguity).** At three sites,
the matching-tensor image is exactly `X_3`, of affine dimension 25.
For a generic tensor in this image, its source representations modulo
product-one site scalings form `C^* times C^8` after choosing local
representatives of the uniquely determined lines. In particular,
recovering the mean lines does not recover a unique three-site source.

**Proof.** Fix representatives `l_0,l_1,l_2`, and write
`k=l_0 tensor l_1 tensor l_2`. The map

$$
\Psi_l(Q)=l_0\otimes Q_{12}+l_1\otimes Q_{02}+l_2\otimes Q_{01}
 \tag{22}
$$

uses site order in each term. It maps a 27-dimensional edge space
onto the 19-dimensional space `F(l)`, so its kernel has dimension
eight. Every `T in F(l)` equals `k+Psi_l(Q)` for some `Q`, proving
one inclusion of the image equality. Nonzero-mean matching sources
give the other inclusion by Lemma 2; sources with zero means are
limits, and `X_3` is closed.

By Corollary 4, all representations of a generic such `T` have means
`mu_i=t_i l_i` with `t_i!=0`. Put `tau=t_0 t_1 t_2` and
`Q_ij=R_ij/(t_i t_j)`. These are exactly the invariants of
product-one site scaling, and (1) becomes

$$
\Psi_l(Q)=\tau^{-1}T-k. \tag{23}
$$

Every `tau in C^*` is allowed, with an affine eight-dimensional space
of solutions for `Q`. Choose fixed lifts of `T` and `k` through
`Psi_l` to trivialize this family as `C^* times C^8`. Equation (21)
gives `27-8+6=25`. A separate 25-by-25 source-Jacobian minor in the
certificate provides a computational check of this dimension. QED.

## 7. Algorithm, characteristic-zero acceptance, and examples

The exact algorithm in local dimension three is:

1. Construct the three matrices (4), and choose an invertible reference.
2. Form `A,B,C` as in (6), and compute a basis matrix `K` for `ker C`.
3. Compute `ker(CAK)`. If it has dimension one, let `v=Kz` for a
   nonzero vector `z` in that kernel.
4. Verify that `Av` and `Bv` are scalar multiples of `v`, and that
   `v` is a product tensor over the remaining sites. Recover the
   first line by (8) and the other lines from any nonzero tensor entry.
5. For full-source recovery at orders at least seven, apply the
   [restricted covariance inverse](quadratic-size-source-inverse-2026-09-27.md)
   and coefficient calibration, checking their rank hypotheses too.

The implementation uses the prime `1000003`. A modular invertible
slice certifies rational invertibility. Computing a `k`-dimensional
commutator kernel and a nonzero `(k-1)`-minor of `CAK` proves that
the stacked system `[C;CA]` has rank `N-1` modulo the prime. Clearing
the invertible-slice denominators promotes this to a lower rank bound
over the rationals. Bounded rational reconstruction proposes the mean
ratios; a separate integer tensor contraction verifies the proposed
product-kernel equation over the integers. Together these checks give
exactly a one-dimensional common kernel in characteristic zero.

The fixed-prime implementation can reject an input because its chart
is bad modulo that prime or because its rational coordinates exceed
the lifting bound. Such rejection is not evidence of nonidentifiability.
General rational implementation may require changing coordinates,
larger primes, Chinese remaindering, or rational linear algebra.

The [saved certificate](../computations/matching-tensor-recovery-2026-09-26/slice-mean-recovery-certificate.json)
contains the following exact tests:

| Input | Slice order | `dim ker C` | `dim Z(T)` | Recovery checked |
| --- | ---: | ---: | ---: | --- |
| Three-site integer source | 9 | 3 | 1 | Mean lines; source-image rank 25 |
| Five-site integer source | 81 | 3 | 1 | Mean lines |
| Seven-site integer source | 729 | 5 | 1 | Full rational source |
| Seven-site paired witness | 729 | 27 | 1 | Mean lines; all-orders witness formula |
| Retained nine-site nonlinear-search failure | 6561 | 5 | 1 | Full rational source |

The three-site example uses slice one after slice zero is found singular.
The nine-site mean step took about 215 seconds in the recorded run.
Its input tensor hash is compared to the old failed-search record before
the recovery is attempted. The algorithm receives only the tensor;
planted means and edges are used afterward to compare the output.
Every full reconstructed tensor entry is checked over the rationals,
and every recovered parameter is compared modulo product-one site gains.

The independent audit rebuilds every input entry by a separate scalar
matching recurrence, all slice entries by a separate alternating-symbol
construction, and the rational source outputs after clearing denominators.
It also checks the recovered lines using quotient matrices, independently
of the generator's exterior contraction. The full audit includes the
nine-site slice ranks. It shares the exact linear-algebra library with
the generator; it is not a Lean formalization or an external review.
The [saved full audit](../computations/matching-tensor-recovery-2026-09-26/slice-mean-recovery-audit.json)
passes all five cases, including the retained nine-site input.

From the repository root:

```sh
OPENBLAS_NUM_THREADS=1 .venv/bin/python computations/matching-tensor-recovery-2026-09-26/slice_mean_recovery.py
OPENBLAS_NUM_THREADS=1 .venv/bin/python computations/matching-tensor-recovery-2026-09-26/verify_slice_mean_recovery.py --full
```

The generator's `--quick` omits the nine-site example. Omitting `--full`
from the auditor still checks every saved input, quotient equation, and
full-source output, but replays slice ranks only through seven sites.

## 8. Attribution and remaining limits

The exterior matrices are instances of established tensor-product
Koszul flattenings. See Hauenstein, Oeding, Ottaviani, and Sommese,
[Homotopy techniques for tensor decomposition and perfect identifiability](https://arxiv.org/abs/1501.00090),
Section 5.1, for the multilinear exterior construction and Section 5.2
for recovery using its kernels. Their tensor-decomposition problem
differs from recovery of a matching source.

Testing for common eigenvectors by commutator kernels is classical.
Shemesh's [Common eigenvectors of two matrices](https://www.sciencedirect.com/science/article/pii/0024379584900855)
appeared in *Linear Algebra and its Applications* 62 (1984), 11–18.
Theorem 1.1 of Jamiołkowski and Pastuszak,
[Generalized Shemesh criterion](https://arxiv.org/abs/1306.0083),
records the criterion using the intersection of `ker[A^j,B^k]`
over `1<=j,k<=N-1`. The two conditions (6) are not a replacement
for that general criterion. They suffice on our stated open set because
Lemma 6 proves a one-dimensional intersection and the source or
compression hypothesis supplies an actual product eigenvector.

Compression by local hyperplanes is already studied in tensor geometry;
see Landsberg and Michałek,
[Abelian tensors](https://people.tamu.edu/~jml/LMabten4-21.pdf),
Section 7.5, for the three-factor terminology and its additional
genericity hypotheses. The osculating-space description is standard;
see Araujo, Massarenti, and Rischter,
[On non-secant defectivity of Segre-Veronese varieties](https://arxiv.org/abs/1611.01674),
Section 2. Theorem 8 above is proved here by our explicit witness and
incidence argument, rather than being asserted as a theorem of either
reference. No priority claim is made for the geometric consequence.

The specific contribution relative to earlier work in this repository
is the all-orders paired witness, its two-condition recovery certificate,
the explicit mean-line algorithm, and its consequences for the larger
compression model. The fixed witness replaces elimination in the
generic exact-data mean step. It does not give a complete classification
of nongeneric sources, an efficient inverse from compressed scalar data,
or a globally initialized algorithm with measurement-noise guarantees.
The existing [local stability bounds](full-source-local-stability-2026-09-27.md)
remain relevant to a separate correction iteration near a known source.

The subsequent [observable noisy-mean certificate](observable-noisy-mean-recovery-2026-09-27.md)
now stacks the two kernel equations and bounds perturbations from tensor
noise, approximate solves, and a proposed null vector. It certifies mean
directions for every compatible tensor in the stated data-error ball,
without a nearby source guess. Exact noisy-data certificates cover three,
five, and seven sites. A certified covariance and scale initializer,
and compressed-data inversion, remain unresolved.
