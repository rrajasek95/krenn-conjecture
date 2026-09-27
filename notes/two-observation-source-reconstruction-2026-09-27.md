# Recovering a shared Gaussian source from two cross-moment tensors

Research note, 2026-09-27. Written proof with exact finite-field rank
certificates and a separate implementation of the decisive matrix audit.
Not Lean formalized or independently peer reviewed. This is separate from
the Krenn–Gu proof paper, which is unchanged.

## 1. Result and observed data

The [response-span reconstruction theorem](two-direction-source-reconstruction-2026-09-26.md)
recovers a source from the span of sufficiently many outputs, with a
specific covariance ambiguity. Here two individually observed outputs
recover that entire span and then remove the covariance ambiguity.

There are five labelled sites, each with a four-dimensional vector space
`V_i`. At each of two experimental settings `j=1,2`, suppose the site
vectors have mean vectors `mu_(j,i)` and share the same cross-site
covariance blocks `R_ik`. The observed data are the two full cross moments

$$
T_j=\mathbb E[X_{j,1}\otimes\cdots\otimes X_{j,5}],\qquad j=1,2.
$$

Only these two tensors are used. Their means, covariance blocks, and
lower-order moments are not supplied. The tensors are separately labelled
and have known coefficients, including their overall scales. There is no
mixture of the two distributions. In the algebraic formulation all
parameters can be complex, and the expectation means the Wick polynomial
defined below; it does not require a complex probability measure.

**Theorem 1 (generic reconstruction from two observations).** For a
nonempty Zariski-open set of pairs of mean rows and shared cross-site
quadratics on five four-dimensional sites, `(T_1,T_2)` determines both
mean rows and every cross-site quadratic block up to exactly

$$
\mu_{j,i}\longmapsto\lambda_i\mu_{j,i},\qquad
R_{ik}\longmapsto\lambda_i\lambda_kR_{ik},\qquad
\lambda_i\ne0,\quad\prod_{i=1}^5\lambda_i=1. \tag{1}
$$

Every alternative complex source producing the same two tensors is
included in this conclusion, even if initially allowed to have zero or
locally dependent mean vectors. A representative is recoverable using
rational arithmetic, tensor contractions, and linear algebra. Root
extraction is unnecessary.

The transformations (1) are unavoidable: every term in a full cross
moment uses each site exactly once. Within-site covariance blocks do not
occur in these moments and are not identifiable. The theorem is a generic
exact-data result; it makes no assertion about numerical conditioning or
estimation from a finite sample.

There are `40+160=200` source parameters: two sets of five four-component
means and ten `4 by 4` covariance blocks. The ambiguity (1) has dimension
four and acts freely on this generic set. Thus the generic image of this
two-observation model has dimension `196`.

## 2. Matching expansion and the missing response space

For the arguments that do not depend on the number five, let `n=2m+1` be
odd. Use the commutative site algebra

$$
\mathcal A=\bigotimes_{i=1}^n(\mathbb C\oplus V_i),\qquad V_iV_i=0.
$$

The last relation says that any product using a site twice is zero.
Products using every site once are naturally tensors in
`V=V_1 tensor ... tensor V_n`. For a mean row `mu=sum_i mu_i` and
`R=sum_(i<k)R_ik`, let `G(mu,R)` be the full-site component of
`exp(mu+R)`. Explicitly, sum over all matchings: an unmatched site supplies
its mean, and a matched pair supplies its cross-site block. This is the
ordinary Gaussian cross-moment formula.

Choose a basis `L_1,L_2` of the two-dimensional span `E` of the two mean
rows. A generic pair projects to two independent local vectors at every
site. Set

$$
P_{a,b}(E,R)=\frac{L_1^aL_2^b}{a!b!}
\frac{R^{(n-a-b)/2}}{((n-a-b)/2)!},\qquad
W(E,R)=\mathrm{span}\{P_{a,b}:a+b\le n\text{ odd}\}.
$$

These are full-site tensors. For `L(t)=t_1L_1+t_2L_2`,

$$
G(L(t),R)=\sum_{a+b\le n\text{ odd}}t_1^at_2^bP_{a,b}(E,R).
$$

Generically the responses are independent and their number is
`d=(m+1)(m+2)`. At five sites `d=12`, although only two outputs are
observed. The edge-free responses span the terminal space

$$
U(E)=\mathrm{span}\left\{\bigotimes_iL_i(t):t\in\mathbb C^2\right\},
\qquad\dim U(E)=n+1.
$$

Its product tensors form a degree-`n` rational normal curve `C(E)` in
projective space. Each local projection of this curve onto the line space
of `E_i=span(L_(1,i),L_(2,i))` is an isomorphism. In particular, fixing the
line at any one site fixes the point of the curve.

## 3. A matrix made from the two observations

For `q` tensors, let `B_q` denote the multilinear operation that wedges
their `q` local vectors at each site. Its value lies in
`tensor_i exterior^q V_i`. For example,

$$
B_2(\otimes_i u_i,\otimes_i v_i)=\bigotimes_i(u_i\wedge v_i).
$$

**Lemma 2 (three-copy response identity).** For odd `n`,

$$
B_3(S_1,S_2,S_3)=0\qquad(S_1,S_2,S_3\in W(E,R)). \tag{2}
$$

**Proof.** This is the two-direction case of the
[multiple-copy theorem](matching-tensor-recovery-and-multiple-copies-2026-09-26.md#4-more-copies-for-more-coupling-directions).
One can prove it directly with three independent formal Gaussian copies.
Their mean settings supply two vectors in the three-dimensional copy
index space. Generically an orthogonal reflection fixes both vectors.
It preserves the means and the covariance table, which is the same in
each copy and zero between copies. Thus it preserves every Wick moment.
At each site it negates the determinant of the three copy vectors.
The product of an odd number of these determinants has zero moment.
Its coordinates are `B_3` of the three Gaussian outputs. Polynomial
extension removes the generic restriction on the settings; coefficient
extraction in their six independent parameters gives (2). QED.

When `V_i=C^4`, fix an ordered local basis and its alternating volume
tensor `epsilon`, with `epsilon_(0123)=1`. The two observed tensors define
a square matrix of order `4^n`:

$$
A(T_1,T_2)_{a,b}
=\sum_{c,d}(T_1)_c(T_2)_d
  \prod_{i=1}^n\epsilon_{a_i b_i c_i d_i}. \tag{3}
$$

Here `a,b,c,d` are words of length `n` in `{0,1,2,3}`. The matrix is skew
symmetric because `n` is odd. Up to the volume identifications
`exterior^3 V_i = V_i^*`, its kernel is the kernel of
`S -> B_3(T_1,T_2,S)`. Lemma 2 therefore gives

$$
W(E,R)\subseteq\ker A(T_1,T_2). \tag{4}
$$

**Lemma 3 (five-site response completion).** Generically, for five
four-dimensional sites,

$$
\mathrm{rank}\,A(T_1,T_2)=1012,\qquad
\ker A(T_1,T_2)=W(E,R),\qquad\dim W(E,R)=12. \tag{5}
$$

**Proof.** Independence of the twelve responses is a nonempty open
condition. On that set (4) bounds the matrix rank by `1024-12=1012`.
The exact source in Section 7 has twelve independent responses and a
principal `1012 by 1012` minor of (3) with determinant `782` modulo
`1009`. Thus this minor is a nonzero polynomial in characteristic zero.
The upper bound and this witness prove (5) on a nonempty open set. QED.

This is the one step presently proved by a fixed-format computational
witness. An all-orders proof that (4) is generically an equality is not
known here.

## 4. Excluding degenerate alternative sources

The response-span theorem recovers `E` from `W`: expand the `2 by 2`
flattening minors of a general tensor of `W`, take the kernel of their
quadratic coefficient matrix, and sum the images of its symmetric
matrices. This recovers `U(E)`. Local and pairwise contractions synchronize
the local mean planes. The same theorem shows that the product locus in
`W` is exactly `C(E)`. Its larger-local-space extension applies here.

To compare with an arbitrary alternative source, it is insufficient to
assume that its twelve responses are independent. That assumption must
be avoided.

**Lemma 4 (one output selects its terminal product).** For generic
two-direction sources at any odd `n>=3`, the restriction

$$
B_2(G(\mu,R),\cdot)|_{U(E)}
$$

has rank `n` and kernel `C (tensor_i mu_i)`, for a generic nonzero
`mu in E`.

**Proof.** Every matching term in an odd-site output has a monomer. At
that site, wedging the term with `tensor_i mu_i` gives zero. This supplies
the asserted kernel line and an upper rank bound `n`.

For equality, use independent local vectors `x_i,y_i,z_i`, take
`L_1=sum_i x_i`, `L_2=sum_i y_i`, `R=sum_(i<k)z_i z_k`, and `mu=L_1`.
In `B_2(G(mu,R),tensor_i(sx_i+ty_i))`, project the first site onto the
`x_1 wedge y_1` coordinate and each other site onto
`span(z_i wedge x_i,z_i wedge y_i)`. Only matching terms with the first
site as their sole monomer survive. The result is the nonzero matching
number `(n-2)!!` times

$$
t(x_1\wedge y_1)\otimes
\bigotimes_{i=2}^n\bigl(s(z_i\wedge x_i)+t(z_i\wedge y_i)\bigr).
$$

Its `n` coefficient tensors, indexed by the number of `y` factors, are
independent. Rank openness proves the generic assertion. Interchanging
`x,y` supplies the same assertion for a second independent mean at the
same witness. QED.

**Lemma 5 (alternative means cannot degenerate).** Suppose the observed
pair satisfies (5), the product locus of its kernel is `C(E)`, and the two
restrictions in Lemma 4 have distinct product kernel lines. Every
alternative source `(mu'_1,mu'_2,R')` producing the same observations has
nonzero and independent local mean vectors at every site. Its terminal
curve equals `C(E)`.

**Proof.** First,

$$
\ker B_2(T_j,\cdot)\subseteq\ker A(T_1,T_2), \tag{6}
$$

because wedging a zero two-fold exterior tensor with the other output
gives zero in the three-fold exterior operation.

Fix an alternative mean row `mu'_j`. If a subset `Z` of its local means
vanishes, replace those means by `epsilon u_i`. The identity
`B_2(G(mu'_j(epsilon),R'),tensor_i mu'_(j,i)(epsilon))=0` holds for every
`epsilon`. Divide by `epsilon^|Z|` and set `epsilon=0`. Consequently all
products with the original nonzero local factors and arbitrary factors
`u_i` at the zero sites belong to the left side of (6). At least one
original factor is nonzero: if all means vanished, an odd-site Gaussian
output would be zero, whereas `T_j` is nonzero. Fixing its local line
specifies one point of `C(E)`; freely varying another local line is
incompatible with membership in this curve. Thus `Z` is empty.

It follows that `tensor_i mu'_(j,i)` is a nonzero product in `W`, hence
in `U(E)`. Lemma 4 forces it to be the unique product line belonging to
`T_j`. The two selected lines are distinct. Their local projections are
distinct at every site, so the two alternative local means are independent.

Let `E'=span(mu'_1,mu'_2)` and let `W'=W(E',R')`, without assuming its
dimension. Lemma 2 gives `W' subset ker A=W`. Its terminal curve is a
rational normal curve contained in the product locus `C(E)`, so it equals
`C(E)`. The mean-space synchronization argument then aligns `E'` with
`E`, up to site scalars and a common basis change. QED.

## 5. Recovering the covariance class without assuming alternative rank

Write `H_E=tensor_i E_i`. The all-orders response-span proof establishes,
on a nonempty open set,

$$
\left\{Q:\text{coefficients of }
\frac{L(t)^{n-2}}{(n-2)!}Q\text{ lie in }W\right\}
=\mathbb C R+\mathrm{Sym}^2 E+K_E. \tag{7}
$$

Here `Sym^2 E` means the image of the quadratic mean polynomials in the
edge component of the site algebra. The circulation space `K_E` consists
of

$$
D=\sum_{i<k}c_{ik}(L_{1,i}L_{2,k}-L_{2,i}L_{1,k}),\qquad
c_{ki}=-c_{ik},\quad\sum_k c_{ik}=0.
$$

It has dimension `binom(n-1,2)`. The same proof shows that the map

$$
D\longmapsto\left[
\frac{L(t)^{n-4}}{(n-4)!}RD\right]
\quad\text{modulo }W+H_E \tag{8}
$$

is injective on `K_E` for generic sources with odd `n>=5`, retaining all
coefficients in `t`.

For the alternative source in Lemma 5, align its mean plane with `E`.
The aligning site scalars can be chosen with product one: multiply all
of them by a common scalar and absorb it into the common mean basis.
Thus the observed tensor values are preserved under the alignment.

Since `W' subset W`, (7) gives `R'=aR+q+D`. If `a=0`, all of its means
and edges lie in the local mean planes, forcing both observed tensors
into `H_E`. This is excluded on our open set. Therefore `a!=0`.
Removing `q` and rescaling `a` preserve `W'`, even if its responses were
dependent. Comparing its two-edge layer with the one for `R` gives

$$
\frac{L(t)^{n-4}}{(n-4)!}\left(RD+\frac{D^2}{2}\right)\in W.
$$

The `D^2` term lies in `H_E`, so (8) forces `D=0`. Consequently every
alternative source lies in the same covariance class

$$
R'=aQ+q(H),\qquad
q(H)=\frac12\sum_{s,t=1}^2H_{st}L_sL_t,
\quad a\ne0,\quad H=H^t, \tag{9}
$$

where `Q` is any reconstructed representative. The edge-class recovery
algorithm uses (7), followed by one linear circulation correction using
(8). It receives the completed space `ker A`, not the original source.

## 6. Two output values calibrate the class rationally

Express each observed tensor in the independent basis `P_(a,b)(E,Q)`.
Write its coefficients as `c_(j,a,b)`, and let

$$
z_j=(c_{j,1,0},c_{j,0,1}).
$$

If its actual mean is `L(t_j)` and its quadratic is (9), expansion of
`exp(L(t_j)+aQ+q(H))` gives, with `n=2m+1`,

$$
z_j=a^m t_j,\qquad \beta=a^{-n},\qquad K=H/a. \tag{10}
$$

Define a binary cubic from the response coefficients by

$$
F_j(x_1,x_2)=\sum_{u+v=3}\binom3u c_{j,u,v}x_1^ux_2^v.
$$

The degree-three coefficient identity is

$$
F_j(x)=\beta(z_j\cdot x)^3
             +3(z_j\cdot x)(x^tKx). \tag{11}
$$

This is a linear system for the four unknowns `beta,K_11,K_12,K_22`.
For example, the `(2,1)` response coefficient equals
`beta z_1^2 z_2 + K_11 z_2 + 2K_12 z_1`, where subscripts on `z` here
indicate its two components.

**Lemma 6 (unique two-output calibration).** If `z_1,z_2` are independent,
the system (11) has at most one solution.

**Proof.** For the difference of two solutions, divide the polynomial
identity by the nonzero linear polynomial `z_j dot x`. It gives
`delta K = -(delta beta/3) z_j z_j^t` for each `j`. Independence of the
two vectors forces `delta beta=0` and then `delta K=0`. QED.

Existence follows from (9). In particular `beta!=0`. Put `C=Q+q(K)` and
distinguish site `n`. Define the following source directly, using only
rational operations:

$$
\widehat\mu_{j,i}=
\begin{cases}
L_i(z_j),&i<n,\\
\beta^mL_n(z_j),&i=n,
\end{cases}
\qquad
\widehat R_{ik}=
\begin{cases}
\beta^{-1}C_{ik},&i<k<n,\\
\beta^{m-1}C_{in},&k=n.
\end{cases} \tag{12}
$$

**Lemma 7 (rational representative and exact uniqueness).** Formula (12)
reproduces both observations. Every source of the form (9) reproducing
them differs from (12) by the product-one site scalings (1).

**Proof.** For a source in (9), (10) gives its mean as `a^-m L(z_j)` and
its quadratic as `aC`, with `a^n=beta^-1`. Apply the site scalings

$$
\lambda_i=a^m\quad(i<n),\qquad
\lambda_n=a^{-m(n-1)}.
$$

Their product is one. The resulting means are exactly those in (12).
For an edge away from the last site, its scale becomes
`a^(2m+1)=beta^-1`; for an edge incident to the last site, it becomes
`a^(1+m(2-n))=beta^(m-1)`. Thus its quadratic also equals (12).
Lemma 6 makes the same `beta,K` necessary for every alternative source.
Although `a` was used to prove the equivalence, (12) never computes it.
QED.

**Proof of Theorem 1.** Complete the response space by Lemma 3, extract
its terminal space and mean planes, and apply Lemmas 4–5 to every
alternative source. Equations (7)–(8) reduce all its possible quadratics
to (9). Lemmas 6–7 identify the remaining ambiguity exactly as (1).
All required rank conditions are nonempty open conditions. They hold
together at the exact witness below, so this proves a nonempty generic
case rather than an inconsistent list of assumptions. QED.

**Corollary 8 (all-orders conditional version).** For any odd `n>=5` with
four-dimensional sites, the same proof and rational reconstruction work
whenever (4) is an equality, the response-span reconstruction conditions
hold, the two terminal restrictions have rank `n` with distinct kernel
lines, and the two tensors are not both in `H_E`. The unresolved
all-orders step is generic equality in (4). Lemma 4 and the response-span
conditions themselves have analytic all-orders witnesses.

**Corollary 9 (any larger local dimensions).** The generic uniqueness and
rational reconstruction conclusion of Theorem 1 holds on five sites
with any finite local dimensions `d_i>=4`, including unequal dimensions.

**Proof.** Choose local coordinates numbered from zero. Use the baseline
four-coordinate projection `{0,1,2,3}` at each site. In additional views,
replace coordinate `3` by one extra coordinate at either one site or two
sites. There are finitely many views, and each full-source-to-projected-
source parameter map is surjective. Thus the inverse image of the open
set from Theorem 1 is nonempty and open for each view. Their finite
intersection is nonempty. Also require the first mean's coordinate `0`
to be nonzero at every site.

Apply Theorem 1 to the baseline view of a generic source and any
alternative source giving the same full tensors. It supplies scalars
`lambda_i` of product one. Every other view contains coordinate `0` at
every site, so the first mean's value at that coordinate forces its
comparison scalar to be exactly the same `lambda_i`. Single replacements
cover every mean entry and every block entry with at most one extra
coordinate. Double replacements cover every edge entry with two extra
coordinates. Hence the same product-one scalars relate the entire
sources.

For reconstruction, recover each view separately. Align its first-mean
anchor coordinates with those in the baseline reconstruction, using their
ratios as site scalars. The preceding argument proves that their product
is one and that all overlaps agree. Merge the recovered coordinates.
Every step is rational. If `e_i=d_i-4`, at most
`1+sum_i e_i+sum_(i<k)e_i e_k` four-coordinate reconstructions are needed.
QED.

## 7. Exact certificate and independent replay

The [reconstruction program](../computations/matching-tensor-recovery-2026-09-26/pair_observation.py)
uses two mean directions and arbitrary `4 by 4` cross-site blocks
generated with seed `281927`, modulo `1009`. The two settings are
`(1,2)` and `(3,5)`. Their values are used only to generate the observations;
the inverse routines receive just the tensors and their shape.

The [saved certificate](../computations/matching-tensor-recovery-2026-09-26/pair-observation-certificate.json)
includes both observed tensors, source and recovered parameters, and
selected minor indices.

| Check | Result modulo 1009 |
| --- | ---: |
| Pair exterior matrix rank | 1012 of 1024 |
| Selected principal determinant | 782 |
| Independently calculated Pfaffian | 109; its square is 782 |
| Completed response dimension | 12 |
| Terminal quadratic constraints | rank 67 of 78 |
| Selected terminal constraint determinant | 902 |
| Extracted terminal dimension | 6 |
| Two single-output terminal restrictions | rank 5 each |
| Their selected determinants | 554 and 20 |
| First-edge constraints | rank 150 of 160 |
| Selected first-edge determinant | 539 |
| Cycle correction | rank 6; determinant 979 |
| Calibration | rank 4; determinant 431 |
| Dimension of `H_E` after adjoining both observations | 34, versus 32 |

The solved coefficients are `beta=692` and
`K=[[45,589],[589,465]]`. Formula (12) reproduces every entry of both
input tensors. Independent comparison with the generating source finds
the site scalars `[278,121,71,538,506]`, whose product is one modulo `1009`,
and checks every mean and edge coordinate under (1).

Run from the repository root:

```sh
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python computations/matching-tensor-recovery-2026-09-26/pair_observation.py
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python computations/matching-tensor-recovery-2026-09-26/audit_pair_observation.py
```

The first command requires NumPy and `python-flint`. The
[second implementation](../computations/matching-tensor-recovery-2026-09-26/audit_pair_observation.py)
uses NumPy only and imports none of the reconstruction code. It regenerates
the original and recovered moments by a direct recursion, constructs the
entire exterior matrix entry by entry using complementary local indices,
and evaluates the selected Pfaffian by skew elimination. Its
[saved output](../computations/matching-tensor-recovery-2026-09-26/pair-observation-audit.json)
records the nonzero result. The reconstruction instead forms the matrix
by tensor contractions and computes its determinant with FLINT.

The [projection reconstruction program](../computations/matching-tensor-recovery-2026-09-26/projection_observation.py)
also checks Corollary 9 on sites of dimensions `(5,5,4,4,4)`, using seed
`291927`. Its four overlapping views all have pair-matrix rank `1012`,
with principal determinants `981,849,580,847` modulo `1009`. Every overlap
agrees after anchor alignment, and the assembled source reproduces both
full `1600`-entry tensors. Its comparison site scalars are
`[968,529,232,478,260]`, with product one. The
[projection certificate](../computations/matching-tensor-recovery-2026-09-26/projection-observation-certificate.json)
includes the source, recovered parameters, view choices, and alignment
scalars. Replay it with:

```sh
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python computations/matching-tensor-recovery-2026-09-26/projection_observation.py
```

These are exact computations, not floating-point rank estimates.
All source-to-moment expressions are polynomials over the integers; all
denominators used by reconstruction charts are nonzero modulo `1009`.
Consequently the recorded nonzero minors certify nonzero characteristic-
zero polynomials after clearing those denominators. Universal identities
give the necessary rank upper bounds. This establishes the claimed
nonempty Zariski-open set; it does not establish the same matrix rank at
uncomputed numbers of sites.

For real Gaussian sources, the same open conditions give generic recovery
of the means and cross-site covariance blocks. Arbitrary real cross-site
blocks can be completed to a positive definite covariance by choosing
sufficiently large within-site diagonal blocks. Those unobserved blocks
remain free.

## 8. Relation to established methods and remaining work

The exterior operations, flattening minors, and Gaussian moment formulas
are established tools. The result here uses the shared-source identity
to complete the unobserved response space from two tensors, then uses
their coefficients to remove the response-span ambiguity.

* Hauenstein, Oeding, Ottaviani, and Sommese,
  [*Homotopy techniques for tensor decomposition and perfect identifiability*](https://arxiv.org/abs/1501.00090),
  Section 5 of the [authors' manuscript](https://academicweb.nd.edu/~jhauenst/preprints/hoosTensor.pdf),
  give tensor products of Koszul exterior maps and kernel-based recovery.
  The linear map `B_2(T,.)` is of that type. The matrix (3) composes local
  exterior multiplication using two observed tensors and volume forms;
  no new exterior-algebra operation is being claimed.
* Améndola, Ranestad, and Sturmfels,
  [*Algebraic Identifiability of Gaussian Mixtures*, Remark 22](https://arxiv.org/html/1612.01129v2#S4),
  explicitly identify fixed-covariance Gaussian moment varieties with
  Veronese varieties after a linear coordinate change. Their coordinates
  include all moments through a given order. Here the covariance is
  unknown and only two full cross moments of one order are observed.
* Agostini, Améndola, and Ranestad,
  [*Moment Identifiability of Homoscedastic Gaussian Mixtures*](https://arxiv.org/abs/1905.05141),
  study identifiability with an unknown covariance shared by Gaussian
  mixture components. The present observations are separately labelled
  tensors, so their mixture identifiability results do not directly
  answer this inverse problem.
* Pereira, Kileel, and Kolda,
  [*Tensor Moments of Gaussian Mixture Models: Theory and Applications*](https://arxiv.org/abs/2202.06930),
  develop Gaussian tensor-moment formulas. Equation (11) is the usual
  cubic mean–covariance formula applied to recovered response
  coordinates. The formula itself is not new.

This is a targeted comparison, not an exhaustive priority claim. The
remaining questions are an analytic all-orders kernel-rank proof,
identifiability from fewer observations or smaller local dimensions,
and numerical stability near the exceptional rank loci. None is settled
by the five-site certificate.
