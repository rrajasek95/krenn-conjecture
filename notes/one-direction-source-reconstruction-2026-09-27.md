# One-direction response spaces and recovery from a single cross moment

Research note, 2026-09-27. Written proofs, exact reconstruction certificates,
and a separate exterior-matrix audit. Not Lean formalized or independently
peer reviewed. The Krenn–Gu manuscript is unchanged.

## 1. Results and scope

The earlier [single-output result](matching-tensor-recovery-and-multiple-copies-2026-09-26.md)
recovered local mean directions at five and seven sites. It did not recover
the covariance. The missing step admits an all-orders argument: separate
edge corrections by how many factors lie outside the mean lines, and
remove them with two linear solves.

This yields the following results for generic complex sources:

* At every odd `n>=5`, a one-direction response span determines its
  quadratic up to scale and a mean-square addition, after accounting for
  site scalings.
* On five sites of local dimension at least three, a single cross-moment
  tensor determines exactly two source classes, related by the previously
  identified covariance involution. Both have the same mean up to
  product-one site scaling.
* On seven sites of local dimension at least three, a single cross-moment
  tensor determines the entire mean row and all cross-site covariance
  blocks up to product-one site scaling.
* On five sites of local dimension at least three, two generic outputs
  with shared covariance identify the source uniquely up to those
  scalings. The number two is optimal.

The all-orders span theorem below has an analytic witness. The single-
output completion at five and seven sites additionally uses exact
nonzero-minor certificates. It is not yet proved at arbitrary odd orders.
Within-site covariance blocks are unobservable, and statistical stability
is not asserted.

## 2. Notation and the all-orders span theorem

Let `n=2m+1>=5`. At each site let `V_i` have dimension at least three.
Choose a nonzero vector `l_i`, set `L=sum_i l_i`, and let
`R=sum_(i<j) R_ij`, with `R_ij in V_i tensor V_j`. Products take place
in the commutative site algebra

$$
\mathcal A=\bigotimes_i(\mathbb C\oplus V_i),\qquad V_iV_i=0.
$$

A product with two factors at the same site is zero. The full-site
component is the tensor product of the `V_i`. Define

$$
P_{n-2k}(L,R)=\frac{L^{n-2k}}{(n-2k)!}\frac{R^k}{k!},\qquad
W(L,R)=\mathrm{span}\{P_n,P_{n-2},...,P_1\}.
$$

The actual Gaussian cross moment is `G(L,R)=sum_k P_(n-2k)`, the
full-site component of `exp(L+R)`. This notation also defines the
polynomial model for complex parameters, without requiring a complex
probability distribution.

**Theorem 1 (one-direction span reconstruction at all odd orders).**
Generically, `dim W=m+1`, and `W` determines `(L,R)` up to precisely:

1. A common nonzero rescaling of `L`.
2. Independent nonzero site scalings, acting on `l_i` and `R_ij` by
   `l_i -> lambda_i l_i`, `R_ij -> lambda_i lambda_j R_ij`.
3. `R -> aR+bL^2`, with `a!=0`.

Every alternative one-direction source with the same span is included.
The mean lines and a quadratic representative can be recovered using
linear algebra and rational operations.

These transformations visibly preserve the span: site scalings multiply
full-site tensors by a common scalar, and adding a mean square mixes the
response layers triangularly. The proof establishes that there are no
other generic ambiguities.

Choose complements `U_i` so that `V_i=C l_i direct_sum U_i`. Let `F_s`
be the space of full-site tensors with at most `s` factors from the
complements. Equivalently it is the sum of tensor-product subspaces
whose factors lie in the mean lines at all but at most `s` sites.
This latter description shows that the filtration `F_s` is independent
of the chosen complements. In particular `F_0=C P_n` and

$$
\dim F_2=1+\sum_i(\dim V_i-1)
             +\sum_{i<j}(\dim V_i-1)(\dim V_j-1).
$$

The common analytic witness is obtained from local independent vectors
`x_i,y_i,z_i` by taking

$$
l_i=x_i,\qquad R_0=\sum_{i<j}(y_i y_j+z_i z_j). \tag{1}
$$

Additional local coordinates, if present, have zero coefficients at this
witness. Its `m+1` responses are independent: their numbers of outside-
mean factors are respectively `0,2,...,2m`.

## 3. Extracting the mean lines and the first edge constraints

**Lemma 2 (unique terminal product).** Generically, the only product
line in `W` is `C P_n`, and it can be recovered by linear algebra.

**Proof.** Expand first-site `2 by 2` flattening minors of a general
tensor in `W` as quadratics in its `m+1` coefficients. The resulting
coefficient matrix always has a kernel containing the square of the
terminal product's coordinate vector.

At (1), any quadratic monomial involving a nonterminal response is itself
a nonzero multiple of one such minor. Choose an entry of that response
with an outside factor at the first site, and an entry of the other
response with `x` at the first site. The latter is possible since `n`
is odd. The crossed entries have an odd number of outside factors and
vanish. Entries with all their outside factors equal to `y` have nonzero
matching coefficients, so the two selected entries can always be chosen
nonzero. Their tail words have different outside parity and are distinct.

Thus the quadratic kernel at (1) is exactly the one-dimensional space
spanned by the square of the terminal coordinate. Rank openness proves
the same generic equality. Interpreting the kernel vector as a symmetric
matrix recovers the terminal coordinate line from any nonzero column.
Factoring that product tensor recovers the local mean lines. QED.

An alternative source with the same full response dimension cannot have
a zero local mean, since its terminal response would then vanish. Its
terminal product belongs to `W`, so Lemma 2 aligns all its mean lines
with the recovered ones.

Define the one-edge map

$$
\Phi_L(Q)=\frac{L^{n-2}}{(n-2)!}Q.
$$

Normalize `l_i=x_i` after choosing local bases. Every edge tensor in
the kernel of `Phi_L` has the form `D_1+D_0`, where

$$
D_1=\sum_{i\ne j}v_{ij}x_j,\qquad
v_{ij}\in U_i,\quad\sum_{j\ne i}v_{ij}=0, \tag{2}
$$

$$
D_0=\sum_{i<j}d_{ij}x_ix_j,\qquad\sum_{i<j}d_{ij}=0. \tag{3}
$$

Call these spaces `K_1` and `K_0`. Their dimensions are
`(n-2)sum_i(dim V_i-1)` and `binom(n,2)-1`, respectively.

**Lemma 3 (first edge ambiguity).** The map `Phi_L` surjects onto `F_2`
and has kernel `K_1 direct_sum K_0`. Generically,

$$
W\cap F_2=\mathrm{span}\{P_n,P_{n-2}\},\qquad
\{Q:\Phi_L(Q)\in W\}=\mathbb C R+\mathbb C L^2+K_1+K_0. \tag{4}
$$

**Proof.** An output entry with two outside factors isolates one edge
coefficient. An entry with one outside factor at site `i` reads the sum
over its possible partner sites, yielding the row-sum condition (2).
The entry with no outside factors reads the total in (3). These three
types of entries can be prescribed independently, proving surjectivity
and the kernel description.

The terminal and one-edge responses always lie in `F_2`. At (1), all
other responses have at least four outside factors, so the intersection
has exactly dimension two there and generically. Taking its inverse
image under `Phi_L` gives (4). QED.

## 4. Two projections remove both edge kernels

For brevity write `M=L^(n-4)/(n-4)!`.

**Lemma 4 (detecting the one-outside corrections).** Generically the map

$$
D_1\longmapsto [M R D_1]\quad\text{modulo }W+F_2 \tag{5}
$$

is injective on `K_1`.

**Proof.** At (1), `M R_0 D_1` has exactly three outside factors. The
witness response space has only even outside counts, and `F_2` has at
most two, so (5) vanishes precisely when that three-outside tensor does.

Fix its outside sites `i,j,k`. Its coefficient tensor is

$$
u_i\otimes R_{0,jk}+u_j\otimes R_{0,ik}
                         +u_k\otimes R_{0,ij},\qquad
u_i=-(v_{ij}+v_{ik}), \tag{6}
$$

with the factors placed at their labelled sites. The formula for `u_i`
uses the zero row sum in (2), since the mean endpoint of its edge must
avoid the other two outside sites.

The map from `(u_i,u_j,u_k)` to (6) is injective. For example, the entry
with `y` at site `i` and `z` at the other two sites is exactly the `y`
coefficient of `u_i`. Interchanging `y,z` reads its `z` coefficient.
Any extra local coordinate is isolated at its own site in the same way.
Permuting the sites reads all coefficients of all three vectors.

Hence `v_ij+v_ik=0` for every distinct triple. At a fixed site `i`,
there are at least three other sites; comparing three pairs forces
every `v_ij=0` in characteristic zero. This proves injectivity at (1).

The quotient has a rational matrix chart on the generic locus from
Lemma 3: `dim(W+F_2)=dim W+dim F_2-2`. A nonzero maximal minor therefore
extends injectivity to a nonempty open set. QED.

**Lemma 5 (detecting the pure-mean corrections).** Generically the map

$$
D_0\longmapsto [M R D_0]\quad\text{modulo }W \tag{7}
$$

is injective on `K_0`.

**Proof.** At (1), the tensor has exactly two outside factors. For the
outside pair `i,j`, its coefficient is `R_(0,ij)` times
`sum_(k<l outside {i,j}) d_kl`. Membership in `W` means this scalar is
the same constant `c` for every pair, since the two-outside part of `W`
is the line spanned by `P_(n-2)`.

Let `s_i=sum_(j!=i)d_ij`, with `d_ji=d_ij`. The total sum of the `d_ij`
is zero, so the complement sum is `d_ij-s_i-s_j`. Thus
`d_ij=s_i+s_j+c`. Summing over `j!=i` gives

$$
(n-3)s_i+\sum_k s_k+(n-1)c=0.
$$

Since `n>=5`, all `s_i` are equal. Their sum is twice the total edge
sum and is zero. Hence all `s_i`, then `c`, and then all `d_ij` vanish.
Rank openness proves the generic statement. QED.

**Proof of Theorem 1.** Align the alternative mean lines and use (4) to
write `R'=aR+bL^2+D_1+D_0`. If `a=0`, every alternative edge has at
most one outside factor. Every response then lies in `F_m`. The generic
original response space contains a nonzero component with `2m=n-1`
outside factors, so the spans cannot be equal. Thus `a!=0`.

Use the allowed scale and mean-square addition to reduce to
`R'=R+D_1+D_0`. Both two-edge responses lie in `W`; their difference is

$$
M\left(R(D_1+D_0)+\frac{(D_1+D_0)^2}{2}\right). \tag{8}
$$

Every term other than `MRD_1` lies in `F_2`. Lemma 4 therefore forces
`D_1=0`. Now `MD_0^2` lies in `F_0 subset W`; Lemma 5 forces `D_0=0`.
This is a global argument, with no small-perturbation assumption. All
rank conditions hold at the same analytic witness (1). QED.

**Corollary 6 (two linear correction solves).** After recovering the
mean lines, choose
`Q_0 in Phi_L^-1(W)` outside `C L^2+K_1+K_0`. First solve

$$
[M Q_0 D_1]=-[M Q_0^2/2]\quad\text{modulo }W+F_2.
$$

The discarded `D_1^2` term lies in `F_2`, so the system is linear and
has a unique solution. Set `Q_1=Q_0+D_1`. Next solve

$$
[M Q_1 D_0]=-[M Q_1^2/2]\quad\text{modulo }W.
$$

Here `D_0^2` lies in `F_0 subset W`. This system is also linear with a
unique solution. The corrected quadratic is an `aR+bL^2` representative.
Injectivity and consistency follow from Lemmas 4–5 and the decomposition
of `Q_0` in (4).

This extends the same exact error-removal argument used for the
two-direction circulation kernel. The additional filtration step removes
corrections that are not confined to the mean lines.

## 5. Recovering the response space from one tensor

Now take `V_i=C^3`. For an observed tensor `T`, use the tensor-product
Koszul exterior matrix

$$
A(T)_{a,b}=\sum_c T_c\prod_i\epsilon_{a_i b_i c_i},
\qquad a,b,c\in\{0,1,2\}^n,
$$

with `epsilon_(012)=1`. The two-copy identity gives
`W(L,R) subset ker A(T)` when `T=G(L,R)`.

The existing exact certificates establish, generically, kernel dimensions
`3` at five sites and `5` at seven sites, with a unique product line
in each kernel. They also rule out zero local means in any alternative
representation: perturbing a zero mean would put an entire family of
product tensors into the kernel. Thus the observed kernel recovers the
mean lines for every alternative source, not just generic alternatives.

Let

$$
\pi=\bigotimes_i\bigl(V_i\longrightarrow V_i/\mathbb C l_i\bigr).
$$

Every odd-site matching term contains a monomer, so

$$
W(L,R)\subseteq\ker\pi=F_{n-1}. \tag{9}
$$

**Lemma 7 (one-output completion at five and seven sites).** Generically
at either of these two orders,

$$
W(L,R)=\ker A(T)\cap\ker\pi. \tag{10}
$$

At five sites `ker A` already has the correct dimension three. At seven
sites the restriction of `pi` to its five-dimensional kernel has rank
one, leaving the correct dimension four.

**Proof.** The five-site assertion follows from the universal inclusion
and the two equal dimensions. At seven sites, the exact witness in
Section 8 gives a nonzero entry `14` modulo `1009` in the restricted
map, while the four-dimensional response span is universally killed.
It therefore has rank exactly one at the witness and on a nonempty
open set. All rank and mean-recovery conditions hold simultaneously
at that source. QED.

The condition (9) removes the parity-forced extra exterior-kernel
direction. It uses only mean lines already recovered from `T`.

**Theorem 8 (complete single-output fibers).** Generically, for local
dimension three:

* At five sites, one output has exactly two source classes, modulo
  product-one site scaling. They have the same actual means and
  quadratics `R` and `-R-L^2/3`.
* At seven sites, one output has exactly one such source class. The
  mean row and all cross-site blocks are recoverable rationally.

**Proof.** Complete `W` by Lemma 7 and reconstruct its source class using
Theorem 1. To compare with an arbitrary alternative representation of
this one tensor, let `W'` denote its possibly deficient response span.
Its mean lines have already been aligned by the unique-product argument.
The copy identity and (9) give `W' subset W`.

The first-edge argument still places its quadratic in
`aR+bL^2+K_1+K_0`. If `a=0`, its actual tensor lies in `F_m`. Exclude
this on the open set where the observed tensor has a nonzero component
with `n-1` outside factors, as the certificate verifies. Thus `a!=0`.
Removing its scale and mean-square addition preserves `W'`, even if
the responses are dependent. The two correction arguments (8) therefore
apply to `W' subset W` and put every alternative in the class `aR+bL^2`.

The [calibration theorem](calibrated-source-reconstruction-all-orders-2026-09-27.md#4-one-calibrated-output-the-threshold-is-seven-sites)
now applies with one mean direction. It gives exactly two covariance
choices at five sites and one at seven. At five sites the two choices
are the universal involution `R -> -R-L^2/3`, with the actual mean
unchanged. At seven sites its rational calibration formula gives the
unique representative. QED.

The proof has now recovered the response space as well as calibrated it.
Thus the seven-site conclusion uses only **one observed cross moment**;
the span is not supplied as extra data.

## 6. Larger local spaces and two five-site observations

**Corollary 9 (local dimensions at least three).** The conclusions of
Theorem 8 hold when the local dimensions are arbitrary integers at least
three, including unequal dimensions.

**Proof.** Use baseline coordinate projections `{0,1,2}` at each site.
In additional views, replace coordinate `2` by one extra coordinate at
one site or two sites. Each source projection is surjective onto the
three-dimensional source parameter space; hence the inverse images of
the generic conditions in Theorem 8 have a nonempty common open set.
Also require the mean's coordinate `0` to be nonzero at every site.

At seven sites, recover every view and align its mean anchors with those
in the baseline. The anchor ratios determine site scalars of product one.
Single replacements cover all mean entries; double replacements cover
all edge entries. Thus the aligned views recover the full source and
exclude every alternative.

At five sites, both candidates in every view have the same mean, so the
same anchor alignment is unambiguous. Choose an edge-anchor coefficient
not fixed by the involution, for example require
`R_12(0,0) != -(1/3)l_1(0)l_2(0)`. That coefficient occurs in every
view and forces the same branch everywhere. Every alternative is
therefore either the original full quadratic or its full involution.
Both indeed produce the original tensor. QED.

**Corollary 10 (two five-site observations, local dimension three).**
For five sites of local dimensions at least three, two generic actual
outputs with a shared quadratic determine both means and the quadratic
up to common product-one site scalings. Two observations are necessary.

**Proof.** For each output separately, Theorem 8 and Corollary 9 give
two covariance possibilities, after site scaling:

$$
R_j^+=R,\qquad R_j^-=-R-\frac23\mu_{j,i}\otimes\mu_{j,k}
\quad\text{on edge }ik.
$$

For alternatives from the two outputs to share a quadratic, their blocks
must be proportional on every edge. Choose an edge with `rank R_ik>=3`
and with the two mean outer products nonzero and unequal; these are
nonempty generic conditions.

A plus block cannot be proportional to a minus block: the resulting
equation would make a nonzero scalar multiple of a rank-at-least-three
matrix equal to a rank-one matrix. Nor can the two minus blocks be
proportional: unless the proportionality scalar is one, the equation
makes a rank-at-least-three matrix a sum of two rank-one matrices.
For scalar one it would equate the two distinct mean outer products.
Hence only the two plus branches are compatible.

Their two sets of site scalars agree. Their ratio `g_i` satisfies
`g_i g_k=1` on every edge and `product_i g_i=1`. On a complete graph,
the first condition makes all `g_i` equal to `1` or all equal to `-1`;
the odd number of sites excludes the latter. The ambiguity is precisely
one common product-one site scaling.

For construction, test the four candidate pairings for blockwise
proportionality. If two compatible representatives obey
`R^(2)_ik=c_ik R^(1)_ik`, their site factors are recovered without a
root choice: for each `i`, choose a perfect matching `M_i` of the other
four sites and set `g_i=(product_(jk in M_i)c_jk)^-1`. Check all
`c_ik=g_i g_k`, then rescale the second mean accordingly. Finally, the
universal fifth-order involution rules out generic recovery from one
observation, proving optimality. QED.

## 7. The remaining all-orders question

The span-reconstruction theorem now covers one mean direction as well
as the previously treated two and many directions. A remaining route
to recovery from one actual output is the generic completion (10) at
arbitrary odd orders.

The universal copy identity and the monomer constraint always give the
inclusion in (10). The subsequent
[all-orders mean-direction theorem](mean-direction-recovery-all-orders-2026-09-27.md)
now proves unique mean-line recovery at every odd `n>=5`, by a two-site
attachment argument. Once equality in (10) is also established at an
odd `n>=7`, Theorem 1 and the calibration formulas give full single-output
source recovery at that order. No new covariance uniqueness argument is
needed. The five- and seven-site computations do not prove that linear
kernel equality at larger orders. The subsequent
[restricted-kernel criterion](single-output-covariance-low-degree-2026-09-27.md)
bypasses that equality and proves covariance rigidity from a smaller map.
Its [all-orders induction](single-cross-moment-all-orders-2026-09-27.md)
now gives full generic single-output recovery at every odd order at least
seven. The larger kernel equality is no longer a prerequisite.

## 8. Exact certificates and reproduction

The [single-output reconstruction](../computations/matching-tensor-recovery-2026-09-26/single_source.py)
uses source seed `90127`, the same source as the earlier mean-direction
certificate. Its inverse procedure receives only one tensor and its shape.
All arithmetic is modulo `1009`.

| Check | Five sites | Seven sites |
| --- | ---: | ---: |
| Exterior matrix rank | 240 | 2182 |
| Selected principal determinant | 210 | 471 |
| Exterior kernel dimension | 3 | 5 |
| Terminal quadratic coefficient rank | 5 | 14 |
| Selected terminal determinant | 858 | 188 |
| All-outside restriction rank | 0 | 1 |
| Completed response dimension | 3 | 4 |
| First-edge constraint rank | 49 | 97 |
| Selected first-edge determinant | 55 | 784 |
| One-outside correction rank | 30 | 70 |
| Selected one-outside determinant | 292 | 741 |
| Pure-mean correction rank | 9 | 20 |
| Selected pure-mean determinant | 490 | 811 |
| Number of calibrated covariance classes | 2 | 1 |

At five sites the squared calibration parameter is `501`, with roots
`276,733`. The two reconstructed means coincide. Independent comparison
identifies one covariance with the original and the other with its
fifth-order involution; both reproduce every tensor entry. The comparison
site scalars are `[580,314,972,917,204]`, with product one.

At seven sites the calibration gives `beta^2=374`, `beta^3=1008`, and
`beta=375`. The recovered mean and covariance agree with the source
under scalars `[56,420,741,179,57,265,790]`, again of product one.
Every entry of the original tensor is reproduced.

The [certificate](../computations/matching-tensor-recovery-2026-09-26/single-source-certificate.json)
contains source and recovered parameters, selected minor indices, and
both five-site candidates. Run:

```sh
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python computations/matching-tensor-recovery-2026-09-26/single_source.py
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python computations/matching-tensor-recovery-2026-09-26/audit_single_source.py
```

The [second implementation](../computations/matching-tensor-recovery-2026-09-26/audit_single_source.py)
uses matching enumeration to regenerate moments, rather than the recursive
moment routine used to generate inputs for reconstruction. It constructs
the exterior matrix directly from complementary local colours and checks
the selected determinants by Pfaffian elimination, rather than FLINT
determinants. Its [audit record](../computations/matching-tensor-recovery-2026-09-26/single-source-audit.json)
is saved alongside the reconstruction certificate.

The [two-output check](../computations/matching-tensor-recovery-2026-09-26/two_from_single.py)
keeps the five-site quadratic and independently varies the mean. Exactly
one of the four candidate pairings is compatible. The recovered shared
quadratic and both means match the original with common product-one
scalars. The selected source edge has determinant `902`, verifying the
rank-three hypothesis. Its
[certificate](../computations/matching-tensor-recovery-2026-09-26/two-from-single-certificate.json)
records both reconstruction reports and the candidate comparisons. Run:

```sh
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python computations/matching-tensor-recovery-2026-09-26/two_from_single.py
```

The universal identities supply rank bounds; the nonzero modular minors
certify nonempty open sets in characteristic zero after clearing the
nonzero reconstruction-chart denominators. The separate all-orders
span proof uses the analytic witness (1), not extrapolation from these
finite examples.

## 9. Attribution

The exterior matrix is an established tensor-product Koszul flattening,
as described in Section 5.1 of Hauenstein–Oeding–Ottaviani–Sommese,
[*Homotopy techniques for tensor decomposition and perfect identifiability*](https://arxiv.org/abs/1501.00090).
Their Section 5.2 develops kernel-based recovery. Neither the matrix nor
the general kernel-recovery strategy is claimed as new here.

The Gaussian polynomial model and its moment identities are standard;
see Pereira–Kileel–Kolda,
[*Tensor Moments of Gaussian Mixture Models: Theory and Applications*](https://arxiv.org/abs/2202.06930),
and Blomenhofer,
[*Gaussian Mixture Identifiability from Degree 6 Moments*](https://arxiv.org/abs/2307.03850),
Table 1 and Section 2. Their moment-variety setting supplies useful
context but differs from the multilinear cross-site observations here.
In particular, within-site covariance information is absent here.

The model-specific steps are the complete classification of the
one-direction span ambiguity, its removal by two outside-factor
projections, and the use of the compulsory monomer to complete the
single-output response space. These require comparison with further
literature before any priority claim. Numerical stability, minimal local
dimensions, and single-output completion at higher orders remain open.
