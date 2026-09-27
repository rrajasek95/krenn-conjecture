# Recovering source parameters with quadratic-size linear systems

Research note, 2026-09-27. Written argument and exact finite-field
reconstruction certificates. Not Lean formalized or independently peer
reviewed. The Krenn–Gu paper is unchanged.

## 1. What the algorithm takes as input

The [all-orders identifiability proof](single-cross-moment-all-orders-2026-09-27.md)
establishes generic recovery of a Gaussian source from one cross-moment
tensor at every odd order at least seven. This note implements its
covariance step and reduces the ranks that an individual reconstruction
needs to check.

The inputs here are the observed tensor and its local mean **lines**.
A line specifies a direction without specifying the length of the mean.
The algorithm recovers every cross-site covariance block and the actual
mean scales, up to product-one site scalings. It does not implement the
earlier theorem that extracts the mean lines from the tensor.

In particular, the nine-site computation below is not a fully blind
nine-site inverse. It is a complete implementation of the next stage,
using no supplied covariance entries, response span, or lower moments.
The new observation is that its linear systems need only quadratically
many columns, rather than the cubically many columns of the sufficient
rank condition in the all-orders proof.

The subsequent [blind-search program](blind-source-search-and-local-conditioning-2026-09-27.md)
supplies the missing mean lines numerically on examples, verifies them
exactly, and recovers a complete nine-site source over the rationals.
Its search has no global convergence guarantee; the implementation in
this note continues to take mean lines as input.

The later [slice-commutator algorithm](slice-commutator-mean-recovery-2026-09-27.md)
supplies those lines by exact linear algebra on a nonempty open set at
every odd order from three onward. Combined with this note's inverse,
it gives a generic full-source algorithm from order seven and completes
the retained nine-site example where the earlier numerical search failed.

## 2. Definitions and the two ranks

Let `n>=7` be odd, and let each local space have dimension three.
Choose a nonzero representative `x_i` of the supplied mean line and
an outside complement `U_i`. Write `L=sum_i x_i` in the commutative
site algebra, where a product using any site twice is zero. Put

$$
k=\frac{L^n}{n!},\qquad
\Phi(Q)=\frac{L^{n-2}}{(n-2)!}Q,\qquad
M=\frac{L^{n-4}}{(n-4)!}.
$$

A cross-site quadratic `Q` is a collection of edge blocks `Q_ij`.
The space `F_2` consists of tensors with outside factors at at most
two sites. Its dimension is

$$
d_2=1+2n+4\binom n2=2n^2+1.
$$

The map `Phi` is onto `F_2`. Its kernel is `K_1 direct_sum K_0`, where

$$
K_1=\left\{\sum_{i\ne j}v_{ij}x_j:
 v_{ij}\in U_i,\ \sum_{j\ne i}v_{ij}=0\right\},
\qquad \dim K_1=2n(n-2),
$$

$$
K_0=\left\{\sum_{i<j}d_{ij}x_ix_j:
 \sum_{i<j}d_{ij}=0\right\},
\qquad \dim K_0=\binom n2-1.
$$

Thus `K_1` redistributes one-outside edge entries without changing their
sum at each vertex, and `K_0` redistributes pure-mean entries without
changing their total sum.

For the observed tensor `T`, use the exterior map

$$
A(T)_{a,b}=\sum_c T_c\prod_i\epsilon_{a_i b_i c_i}.
$$

Here `epsilon` is the alternating symbol on the three local coordinates.
The copy identity says that the source's response layers lie in its
kernel. First check

$$
\dim(\ker A(T)\cap F_2)=2. \tag{1}
$$

Choose the nonterminal kernel vector `e`, so this kernel is `span(k,e)`,
and choose any lift `Q_0` with `Phi(Q_0)=e`. Suppose every two-outside
block of `e` is nonzero. Choose a basis `D_1,...,D_f` of `K_1`, where
`f=2n(n-2)`, and a column basis `B` of `A(T)(F_2)`. Define

$$
J_1=\left[
 A(T)(MQ_0D_1)\ \cdots\ A(T)(MQ_0D_f)\ B
\right]. \tag{2}
$$

The second rank check is

$$
\mathrm{rank}(J_1)=f+d_2-2=4n(n-1)-1. \tag{3}
$$

This formulation removes the two nuisance null columns before solving.
Equivalently, (3) states that `D -> A(T)(MQ_0D)` is injective modulo
`A(T)(F_2)`. Changing the lift of `e` does not change this condition:
the difference lies in `K_1+K_0`, whose product with `D in K_1`,
after multiplying by `M`, lies in `F_2`.

## 3. A certificate that avoids the three-outside rank test

**Theorem 1 (covariance class from two observable ranks).** Assume the
tensor comes from a source with nonzero means in the supplied lines.
Suppose (1), (3), and the nonzero outside-block condition hold, and that
`T` has a nonzero component with `n-1` outside factors. Then the
covariance class is determined by two linear correction systems.
Every alternative source with those mean lines has the same class,
up to site scalings, a nonzero covariance scale, and addition of a
multiple of `L^2`.

If the response layers and Gaussian calibration are also nondegenerate,
the actual tensor fixes the covariance and mean scales up to
product-one site scalings. These hypotheses hold on the generic open
set of the all-orders theorem.

**Proof.** Normalize an actual source's means to a common scalar
multiple of `L` by product-one site scalings. This is a comparison of
representations over the complex numbers; it does not require root
extraction by the inverse algorithm.

By (1), its covariance quadratic has the form

$$
R=aQ_0+bL^2+D+E,\qquad D\in K_1,\ E\in K_0.
$$

The coefficient `a` is nonzero. Otherwise every edge has at most one
outside factor, so no matching could produce the observed component
with `n-1` outside factors. Rescaling the covariance and subtracting a
mean square preserve its response space and its annihilation by `A(T)`.
We can therefore compare normalized representatives

$$
Q_0+D+E,\qquad D\in K_1,\ E\in K_0.
$$

Their two-edge response equation implies

$$
A(T)(MQ_0D+H)=-A(T)(MQ_0^2/2),\qquad H\in F_2. \tag{4}
$$

Indeed, all remaining terms in the square have at most two outside
factors. Equation (4) is consistent because an actual source exists.
Condition (3) makes `D` unique. Using `B` for the nuisance image turns
it into an ordinary full-column-rank linear system with matrix `J_1`.

Set `Q_1=Q_0+D`. The remaining correction `E in K_0` satisfies

$$
A(T)(MQ_1E)=-A(T)(MQ_1^2/2). \tag{5}
$$

The discarded square `ME^2/2` lies in the terminal line and is
annihilated. Consistency again follows from the source. Lemma 2 below
makes (5) injective. Thus every normalized alternative has the same
representative `Q_1+E`. This proves the global covariance-class
assertion, including alternatives with dependent response lists.

Generate that representative's response layers and express `T` in
them. The [Gaussian calibration formulas](calibrated-source-reconstruction-all-orders-2026-09-27.md)
use the coefficients at mean degrees one, three, five, and seven to
recover the remaining scales rationally. Independence of the response
layers and nonzero calibration denominators are explicit regularity
checks. QED.

**Lemma 2 (the last correction is automatically injective).** Under
(1) and the nonzero outside-block condition, the map

$$
K_0\longrightarrow\mathrm{im}(A(T)),\qquad E\longmapsto A(T)(MQ_1E)
$$

is injective for every `Q_1` with `Phi(Q_1)=e`.

**Proof.** If its value is zero, `MQ_1E` lies in `ker A(T) cap F_2`,
hence in `span(k,e)`. Write `E=sum_(i<j)d_ij x_i x_j` and
`s_i=sum_(j!=i)d_ij`. Comparing the two-outside block at edge `ij`
gives

$$
\sum_{\{k,l\}\cap\{i,j\}=\varnothing}d_{kl}=c
$$

for one scalar `c`, because every corresponding block of `Q_1` is
nonzero. Since the total edge sum is zero, this becomes
`d_ij-s_i-s_j=c`. Summing over `j!=i` gives
`(n-3)s_i+sum_k s_k+(n-1)c=0`.
All `s_i` coincide; their sum is twice the zero total edge sum.
Therefore every `s_i`, then `c`, then every `d_ij` is zero. QED.

**Corollary 3 (generic applicability at all odd orders at least seven).**
The two ranks above hold generically at every odd `n>=7`.

**Proof.** The all-orders theorem supplies
`ker A(T) cap F_3=span(k,e)`, which implies (1). If
`A(T)(MQ_0D+H)=0`, with `D in K_1` and `H in F_2`, the expression
inside `A(T)` lies in `F_3`. The rank theorem puts it in `F_2`.
Its three-outside part is a nonzero scalar multiple of the injective
map in Lemma 3 of the
[low-degree criterion](single-output-covariance-low-degree-2026-09-27.md).
Thus `D=0`; the chosen columns of `B` are independent, proving (3).
The other generic conditions have the witnesses already given in
those notes. QED.

This is a sufficient certificate on an individual input; failure of
one of its ranks does not prove nonidentifiability. We do not claim
that its conditions are equivalent to the full `F_3` condition, or
that an example separating the two has been established.

## 4. Implementation and exact checks

The [inverse program](../computations/matching-tensor-recovery-2026-09-26/restricted_source_inverse.py)
has a reconstruction function with signature `recover(tensor, mean_lines)`.
Its source generator and comparison with the planted source are separate
from that function. The mean-line inputs have their first coordinate
normalized to one, so the actual mean magnitudes are not supplied.

The program changes to mean-adapted coordinates, computes the two-dimensional
kernel on `F_2`, chooses a fixed lift through `Phi`, solves (4) and (5),
and calibrates. It checks every row of both correction equations. Every
recovered tensor entry is then checked with a separate matching recursion,
and every mean and edge entry is compared with the planted source after
solving for the site scalars. Their product must be one.

The exterior application uses sparse columns: a column has at most
`2^n` nonzero entries, one for each choice of the other local colour.
The program never constructs the full `3^n` by `3^n` matrix or the
restricted `F_3` matrix. The `F_2` rank minor is rebuilt entry by entry
with a separate alternating-symbol routine before its determinant is
checked. Response layers are generated by a subset recurrence carrying
the number of matched edges; summing them is checked against the
independent ordinary-moment recurrence.

The largest correction system has `4n(n-1)-1` columns. The observed
tensor still has `3^n` entries, and the implementation keeps dense
output rows. This is a reduction in linear-system width, not a
polynomial-in-`n` bound on the full computation or a conditioning result.

Run from the repository root:

```sh
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python computations/matching-tensor-recovery-2026-09-26/restricted_source_inverse.py
```

The [saved certificate](../computations/matching-tensor-recovery-2026-09-26/restricted-source-inverse-certificate.json)
records the source, supplied mean lines, recovered source, selected minors,
calibration, and shared-covariance alignment, over the field of order `1009`.
It covers one seven-site output and four nine-site outputs sharing one
covariance.

| Sites | `F_2` columns | `F_2` rank | First correction columns/rank | Last correction columns/rank |
| --- | ---: | ---: | ---: | ---: |
| 7 | 99 | 97 | 167 | 20 |
| 9 | 163 | 161 | 287 | 35 |

At nine sites this reconstructs all `9 binom(9,2)=324` cross-site
covariance entries and verifies all `3^9=19683` observed entries per
output. These are finite examples of the stated algorithm, not a
numerical extrapolation used to prove the all-orders result.

## 5. Recovering a shared mean space larger than the local spaces

**Corollary 4 (alignment of the recovered sources).** When several
outputs share a generic nonzero covariance and their individual inverses
succeed, their recovered sources align uniquely up to one common
product-one site scaling. The span of their actual mean rows is then
determined. No inequality between that span's dimension and a local
dimension is required.

**Proof.** Let `c_ij` be the ratio of corresponding covariance blocks
between two recovered representatives. They have the form `g_i g_j`
with `product_i g_i=1`. A perfect matching of the vertices other than
`i` gives

$$
g_i=\left(\prod_{\{j,k\}\ \text{in that matching}}c_{jk}\right)^{-1}.
$$

Thus alignment is rational and uses only recovered covariances.
Uniqueness also follows because two alignments differ by factors
`h_i h_j=1` on all edges; these factors are a common sign, and product
one excludes the negative sign when `n` is odd. Align the means with
the same factors and take their span. QED.

In the nine-site certificate the four global mean rows have rank four,
while their projections at every site have rank three. All four sources
are recovered independently, then aligned using only the covariance
block ratios. The aligned means agree with the planted means under one
common site scaling. This exercises the all-orders shared-source
corollary outside the dimensional hypotheses of the earlier
many-direction response-span theorem. It still uses supplied local mean
lines for each observation; it does not claim an implemented blind
recovery of that four-dimensional space from raw tensors alone.

## 6. Attribution and remaining work

The exterior map and the use of its kernel in tensor reconstruction are
established tools; see Hauenstein–Oeding–Ottaviani–Sommese,
[*Homotopy techniques for tensor decomposition and perfect identifiability*](https://arxiv.org/abs/1501.00090),
Sections 5.1–5.2. Gaussian moment formulas and implicit computations are
also established; see Pereira–Kileel–Kolda,
[*Tensor Moments of Gaussian Mixture Models: Theory and Applications*](https://arxiv.org/abs/2202.06930).
Their observations and inverse problems differ from this single
multilinear cross-moment problem.

The correction equations are from the earlier low-degree note. The
contribution here is their smaller observable rank certificate, their
execution beyond seven sites, and an exact shared-source example with
more global mean directions than local coordinates. No exhaustive
priority claim is made.

The unresolved algorithmic step is a reliable global mean-line inverse
at arbitrary odd orders. The subsequent numerical search verifies its
successful outputs exactly and provides local mean-line conditioning
bounds, but also records a failed search. Global convergence, full-source
noise bounds, statistical sample complexity, and nongeneric source
classification remain separate tasks.
