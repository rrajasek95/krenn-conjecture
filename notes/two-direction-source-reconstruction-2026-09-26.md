# Reconstructing a two-direction matching source from its response span

Research note, 2026-09-26; seven-site check added 2026-09-27. This is separate from the Krenn–Gu paper. The statements below have written proofs and exact five- and seven-site reconstruction certificates; they are not Lean formalized. Priority in the literature has not been established.

## 1. What the data determine

The preceding [response-space note](matching-tensor-recovery-and-multiple-copies-2026-09-26.md) left two questions open: whether several mean directions can be recovered from an output family, and whether the quadratic source can then be recovered. For two mean directions, both questions admit a generic answer at every odd number of sites at least five.

A subsequent [many-direction theorem](many-direction-source-reconstruction-2026-09-27.md) treats three or more mean directions and explains why their one-edge equations have no circulation kernel.

The data here are a **linear span of outputs**, not one output tensor. The mean settings producing the outputs need not be known. This loss of the settings and their individual response labels creates specific, unavoidable ambiguities, which are included in the theorem.

Let `n >= 5` be odd, write `n = 2m+1`, and put `V_i = C^3`. We use the commutative site algebra

$$
\mathcal A=\bigotimes_{i=1}^n(\mathbb C\oplus V_i),
\qquad V_i V_i=0.
$$

Thus two vectors at the same site multiply to zero; vectors at different sites multiply as a tensor product. Its component containing one vector from every site is `V_1 tensor ... tensor V_n`.

A mean row is an element of `direct_sum_i V_i`. Fix two mean rows `L_1,L_2`, write `E = span(L_1,L_2)`, and let

$$
R=\sum_{i<j}R_{ij},\qquad R_{ij}\in V_i\otimes V_j.
$$

For nonnegative integers `a,b` with `a+b` odd and at most `n`, define

$$
P_{a,b}(E,R)=\frac{L_1^aL_2^b}{a!b!}
\frac{R^{(n-a-b)/2}}{((n-a-b)/2)!},
\qquad
W(E,R)=\mathrm{span}\{P_{a,b}(E,R)\}.
$$

Here `span` is taken over `C`; changing the basis of `E` does not change `W`. There are

$$
d=\sum_{k=0}^{m}(2k+2)=(m+1)(m+2)
$$

listed responses. They are independent for a generic source.

**Theorem 1 (generic reconstruction, all odd orders).** For each odd `n >= 5`, there is a nonempty Zariski-open set of sources `(E,R)` for which the response span `W(E,R)` determines the source up to precisely the following transformations:

1. A common change of basis of the two mean rows.
2. Independent nonzero scalar changes at the sites: `L_(s,i) -> lambda_i L_(s,i)` and `R_ij -> lambda_i lambda_j R_ij`.
3. Replacement `R -> a R + q(L_1,L_2)`, where `a != 0` and `q` is an arbitrary homogeneous quadratic in the two mean rows, interpreted in the site algebra.

More precisely, any other two-direction source with the same response span is related to the original source by these transformations. A representative can be recovered by tensor contractions, arithmetic operations, and linear algebra. Polynomial-system solving is unnecessary.

“Generic” means outside a proper algebraic subset of the parameter space. The theorem does not assert reconstruction at every degenerate source, numerical stability, or recovery from a single tensor. The unknown quadratic consists only of **cross-site** blocks; within-site covariances never occur in these data.

Each listed transformation preserves the span. A site rescaling multiplies every full-site tensor by the same scalar `product_i lambda_i`. A quadratic addition mixes the response layers triangularly, by the binomial expansion; a nonzero rescaling of `R` rescales each layer. The converse occupies the remainder of the note.

## 2. Recovering the terminal products

For `t=(t_1,t_2)`, write `L(t)=t_1L_1+t_2L_2`. The responses with no edges span

$$
U(E)=\mathrm{span}\left\{
\bigotimes_{i=1}^n(t_1L_{1,i}+t_2L_{2,i}):[t_1:t_2]\in\mathbb P^1
\right\}.
$$

If the two local vectors at every site are independent, this is an `(n+1)`-dimensional space. The displayed product tensors form a degree-`n` rational normal curve in its projectivization. The parameter `[t_1:t_2]` is shared by all sites.

Suppose `T_1,...,T_d` is any basis of the observed space `W`. Form `T(z)=sum_j z_j T_j`, flatten it into a matrix with the first site indexing the rows and all other sites indexing the columns, and expand its `2 by 2` minors as quadratics in `z`. Let `C_W` be their coefficient matrix, using monomials `z_i z_j` with `i <= j`.

Regard an element of `ker C_W` as a symmetric `d by d` matrix: its coordinate indexed by `(i,j)` is placed at both positions `(i,j)` and `(j,i)`. There is no extra factor of two in this convention.

**Lemma 2 (terminal-space extraction).** Generically,

$$
\dim\ker C_W=2n+1.
$$

The sum of the column spaces of all these symmetric matrices is exactly the coordinate space of `U(E)` inside `W`. Furthermore, the product tensors in `W` are exactly the terminal product curve.

**Proof.** Every terminal product has coordinates `z(t)` in `W` and annihilates all the flattening minors. Consequently `z(t)z(t)^t` belongs to the quadratic kernel. The span of these matrices has dimension `2n+1`: in terminal coordinates their entries are the degree-`2n` binary monomials. Their images span `U(E)`. Thus the claimed kernel dimension is a universal lower bound on the locus where the local mean maps are injective.

To prove equality on a nonempty open set, choose a basis `x_i,y_i,z_i` at each site and take the particular source

$$
L_1=\sum_i x_i,\quad L_2=\sum_i y_i,\quad
R_0=\sum_{i<j}z_i z_j. \tag{1}
$$

Identify the local bases across sites for this argument. Its response space consists of symmetric tensors with an even number of `z` factors. There is one independent coordinate `u_(a,b,2k)` for every `a+b+2k=n`; the response coefficient is the nonzero matching number `(2k-1)!!` times the corresponding symmetric count tensor.

Any quadratic monomial involving a coordinate with a positive number of `z` factors is itself a restricted flattening minor. Indeed, put a `z` in the first site of that coordinate, and put an `x` or `y` in the first site of the other coordinate. The latter is possible because `n` is odd while its number of `z` factors is even. The two cross entries of the minor have odd numbers of `z` factors, so they vanish. The two columns are distinct for the same parity reason.

The remaining quadrics are those of the binary symmetric tensor space. Its flattening minors equate all quadratic monomials with the same sum of indices. There are exactly `2n+1` such sums, from `0` to `2n`. Hence the quadratic kernel at (1) has precisely dimension `2n+1`. A nonzero rank minor proves the same equality on a nonempty open set.

On this open set, the kernel is exactly the span of the matrices `z(t)z(t)^t`, so summing their images recovers `U(E)`. If any tensor in `W` has rank one across the first-site flattening, its coordinate vector `v` satisfies `vv^t in ker C_W`; its image therefore lies in `U(E)`. Within the binary symmetric tensor space `U(E)`, first-site rank one forces a pure power, hence a terminal product. This last assertion also follows directly from the same binary flattening minors. QED.

**Lemma 3 (synchronizing the local mean spaces).** The terminal space determines `E` up to a common basis change and independent nonzero scalars at the sites.

**Proof.** Contractions of `U(E)` onto site `i` recover the local plane `E_i = span(L_(1,i),L_(2,i))`. Contractions onto two sites recover the three-dimensional image of `Sym^2 C^2` in `E_i tensor E_j`. Its annihilator is one nondegenerate bilinear form `B_ij`. A pair of local lines belongs to the terminal curve exactly when it satisfies that bilinear relation.

Choose coordinates at the first site. The relation `v^t B_(1j) w=0` determines a unique projective isomorphism from the first local line to the line at site `j`. In two-dimensional coordinates it is represented by `w = J B_(1j)^t v`, where `J` has rows `(0,-1)` and `(1,0)`. These maps synchronize all local planes. Their scalar representatives are the independent site scalars in the theorem. QED.

This also excludes alternative degenerate mean planes in a source with the same `d`-dimensional response span. Such an alternative must have all `d` listed responses independent. If its local mean map has rank at most one at a site, its terminal polynomial has a common linear scalar factor (or is zero), so its `n+1` terminal coefficients are dependent. Thus all its local mean maps are injective. Its terminal product curve lies in the product locus from Lemma 2, hence equals that curve. Lemma 3 then aligns its mean plane with the recovered one.

## 3. The exact ambiguity of the first edge equations

After synchronizing the mean planes, normalize them for the proof to `L_1=sum x_i`, `L_2=sum y_i`. Define the linear map

$$
\Phi_E(Q;t)=\frac{L(t)^{n-2}}{(n-2)!}Q.
$$

Its coefficients in `t` are the responses with one edge. The edge space has dimension `9 binom(n,2)`.

**Lemma 4 (cycle kernel).** For `n >= 3`, the kernel of `Q -> Phi_E(Q;t)` consists exactly of

$$
D(c)=\sum_{i<j}c_{ij}(x_i y_j-y_i x_j),\qquad
c_{ji}=-c_{ij},\qquad \sum_j c_{ij}=0.
$$

Its dimension is `binom(n-1,2)`. The coefficients `c` are precisely the circulations, or divergence-free edge flows, of the complete graph.

**Proof.** A term with two factors outside the local mean planes can be isolated by its two outside sites and must vanish. For a term with just one outside factor at site `i`, evaluating `L(t)` at `x` isolates each coefficient of `y` at any other site; evaluating at `y` isolates the corresponding coefficient of `x`. Thus these terms also vanish.

Now write the remaining edge tensor using only `x,y`. Evaluating at `x` and isolating two `y` sites kills every `y_i y_j` coefficient; evaluating at `y` kills every `x_i x_j` coefficient. Write the remaining tensor as `sum_(i != j) b_ij x_i y_j`.

For a nonempty proper set `S` of sites assigned `y`, the relevant coefficient is

$$
t_1^{n-|S|-1}t_2^{|S|-1}
\sum_{i\notin S,\ j\in S}b_{ij}.
$$

Singleton sets and their complements force all column and row sums to vanish. Two-element sets then force `b_ij+b_ji=0`. These conditions also suffice, because every cut sum of a divergence-free antisymmetric flow is zero. The circulation space of a connected complete graph has dimension `binom(n,2)-n+1 = binom(n-1,2)`. QED.

Let `K_E` denote this kernel, and put

$$
S(E,W)=\{Q:\text{every coefficient of }\Phi_E(Q;t)\text{ belongs to }W\}.
$$

This space can be obtained by a linear solve from the data and the recovered mean plane.

**Lemma 5 (first edge equations).** Generically,

$$
S(E,W)=\mathbb C R+\mathrm{Sym}^2 E+K_E,
\qquad
\dim S(E,W)=4+\binom{n-1}{2}. \tag{2}
$$

Here `Sym^2 E` means its three-dimensional image in the edge component of the site algebra.

**Proof.** The right side always lies in `S`: the first summand supplies genuine responses, the second supplies terminal responses, and the third supplies zero. For equality it suffices to exhibit maximal constraint rank at (1).

Separate `Q` by its number of `z` factors. Its one-`z` part must map to zero, since `W` has only even `z` counts; Lemma 4 makes that part zero. For its two-`z` part, membership in the symmetric response space requires the same coefficient on every pair of `z` sites, so that part is a scalar multiple of `R_0`.

For the zero-`z` part, the image under `Phi_E` must be symmetric in the sites. Average `Q` over all site permutations. The average lies in `Sym^2 E`, and equivariance shows that `Q` and its average have the same image. Their difference belongs to `K_E`. Thus (2) holds at (1), and rank openness proves it generically. QED.

At five sites, (2) explains the initial ten-dimensional edge ambiguity: one source direction, three mean-quadratic directions, and six cycle directions. The cycles are invisible to these particular equations, but are not generally invisible to the whole response space.

## 4. The next layer removes the cycles globally

Let

$$
H_E=E_1\otimes\cdots\otimes E_n
$$

be the full `2^n`-dimensional space of tensors whose every factor lies in its local mean plane. It is substantially larger than the terminal space `U(E)`.

**Lemma 6 (cycle detection).** Generically, the following linear map on `K_E` is injective:

$$
D\longmapsto
\left[\frac{L(t)^{n-4}}{(n-4)!}RD\right]
\quad\text{in}\quad
\big(\bigotimes_i V_i\big)/(W+H_E), \tag{3}
$$

where all coefficients in `t` are retained.

**Proof.** Again use (1). A tensor in (3) has exactly two `z` factors. Fix their sites `i,j`. The tensor on the remaining `n-2` sites is `Phi_(E restricted)(D restricted;t)`. Its symmetrization on those sites is zero, since every summand of `D` is antisymmetric under exchange of its two endpoints. In contrast, the two-`z` part of `W` is symmetric on those sites. Thus membership in `W+H_E` forces this restricted tensor to be zero for every removed pair `i,j`.

By Lemma 4, the restriction of the circulation to the remaining sites has zero divergence. Using zero divergence on the full graph, this says

$$
c_{ki}+c_{kj}=0\qquad(k\notin\{i,j\}).
$$

For a fixed `k`, choosing any three distinct other vertices forces all its incident coefficients to vanish, in characteristic zero. Hence `D=0`.

To justify rank openness for this quotient, note that `U(E)` is always contained in `W intersection H_E`. At (1) the intersection is exactly `U(E)`, by the number of `z` factors. Consequently `W+H_E` has its maximal dimension `d+2^n-(n+1)` at the same witness. Its quotient admits a rational matrix chart on a nonempty open set, and injectivity of (3) is a nonzero-minor condition there. QED.

**Proof of Theorem 1.** Lemmas 2–3 recover and align the mean plane of any alternative source. By Lemma 5, its edge tensor has the form `R' = aR+q+D`, with `q in Sym^2 E` and `D in K_E`. If `a=0`, all its edges and means lie in the local mean planes, so its full response space is contained in `H_E`. The generic original response space is not. Thus `a != 0`.

Use the allowed scaling and mean-quadratic change to reduce to `R'=R+D`. Both sources' responses with two edges belong to the same `W`. Their difference is

$$
\frac{L(t)^{n-4}}{(n-4)!}
\left(RD+\frac{D^2}{2}\right).
$$

The `D^2` term belongs to `H_E`, since all its factors are in the mean planes. Passing to the quotient by `W+H_E` removes it **exactly**, with no small-perturbation assumption. Lemma 6 then forces `D=0`. This proves global uniqueness modulo the stated transformations.

All required rank conditions hold at the same explicit source (1), so their common nonempty open set exists. QED.

**Corollary 7 (linear reconstruction after extracting the terminal space).** Compute `S(E,W)` from the one-edge equations and choose

$$
Q_0\in S(E,W)\setminus(\mathrm{Sym}^2 E+K_E).
$$

Write a correction `D` in a known circulation basis. The two-edge condition for `Q_0+D`, after quotienting by `W+H_E`, becomes

$$
\left[\frac{L(t)^{n-4}}{(n-4)!}Q_0D\right]
=-\left[\frac{L(t)^{n-4}}{(n-4)!}\frac{Q_0^2}{2}\right].
$$

This is a consistent linear system with a unique solution. Indeed, modulo `H_E`, multiplication by `Q_0` on `K_E` agrees with a nonzero scalar times multiplication by `R`. The recovered `Q_0+D` is a representative of the correct edge class.

## 5. Exact five-site reconstruction

The implementation is [two_direction.py](../computations/matching-tensor-recovery-2026-09-26/two_direction.py); its saved output is [two-direction-certificate.json](../computations/matching-tensor-recovery-2026-09-26/two-direction-certificate.json). Run from the repository root:

```sh
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python computations/matching-tensor-recovery-2026-09-26/two_direction.py
```

The command requires the existing `python-flint` installation. It prints JSON and writes no files. It generates source parameters using seed `72109` and works modulo `1009`.

The recovery routines receive twelve output tensors, without the source parameters or mean-setting labels. For reproducible input generation only, the settings are `(t_1,t_2)=(j,j^7)` for `j=1,...,12`. The resulting evaluation matrix has determinant `159` modulo `1009`, so the outputs span all twelve responses.

| Computation | Exact result modulo 1009 |
|---|---:|
| Observed response dimension | 12 |
| Quadratic coefficient matrix columns | 78 |
| Quadratic coefficient matrix rank | 67 |
| Selected 67 by 67 coefficient minor | 623 |
| Extracted terminal dimension | 6 |
| Recovered local mean dimensions | 2 at every site |
| First edge constraint rank, out of 90 parameters | 80 |
| Selected 80 by 80 minor in the blind reconstruction | 803 |
| Cycle correction system rank | 6 |
| Selected 6 by 6 cycle correction minor | 462 |

The program verifies the reconstructed response span and independently compares the reconstructed source with the generating source, finding exactly the allowed basis change, site scalings, and four quadratic freedoms. It also checks directly that the six cycle directions vanish under the first edge map. Selected minor rows and columns, source parameters, recovered parameters, and the explicit comparison coefficients are saved in the certificate.

The all-orders theorem above is proved by the analytic witness (1); it does not rely on extrapolating these five-site numbers.

The same program also completes blind reconstruction at seven sites:

```sh
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python computations/matching-tensor-recovery-2026-09-26/two_direction.py 7
```

The [seven-site certificate](../computations/matching-tensor-recovery-2026-09-26/two-direction-seven-certificate.json) records twenty observations, quadratic coefficient rank `195` out of `210` columns, terminal dimension `8`, and first-edge constraint rank `170` out of `189` parameters. The remaining `19` directions consist of the expected four freedoms and fifteen cycle directions. The cycle correction has rank `15`, and the final source comparison again finds exactly the proved transformations. The selected quadratic, first-edge, and cycle-correction minors are respectively `691`, `833`, and `60` modulo `1009`. The observation evaluation determinant is `642`.

## 6. Interpretation and attribution

For a jointly Gaussian family of three-component vectors `X_i`, the cross moment `E[X_1 tensor ... tensor X_n]` has exactly the matching expansion used here: singleton factors are the means and pairs are cross-site covariances. If the mean varies in a common two-dimensional linear space while cross-site covariances stay fixed, sufficiently many generic settings span `W(E,R)`. The theorem recovers that mean geometry and the stated covariance equivalence class from the span. It neither treats a mixture distribution nor uses all moments up to a specified order. No claim about estimation from noisy empirical moments is made.

The reconstruction uses established tools: flattening minors, symmetric tensor geometry, rational normal curves, circulation spaces, and rank arguments. The model-specific conclusions are the complete generic ambiguity classification and the exact elimination of the quadratic cycle correction by quotienting out `H_E`.

Relevant primary precedents include:

* Hauenstein–Oeding–Ottaviani–Sommese, [*Homotopy techniques for tensor decomposition and perfect identifiability*](https://arxiv.org/abs/1501.00090), especially Section 5 of the [authors' manuscript](https://academicweb.nd.edu/~jhauenst/preprints/hoosTensor.pdf), for Koszul flattenings and extracting geometric information from kernels. The earlier note's exterior matrix is an instance of their tensor-product Koszul construction. The present extraction uses ordinary flattening minors; it does not introduce a new type of flattening.
* Améndola–Faugère–Sturmfels, [*Moment Varieties of Gaussian Mixtures*](https://arxiv.org/abs/1510.04654), for the algebraic treatment of Gaussian moment models.
* Agostini–Améndola–Ranestad, [*Moment Identifiability of Homoscedastic Gaussian Mixtures*](https://arxiv.org/abs/1905.05141), for recovery questions with an unknown covariance shared by Gaussian components. Their observed model is a mixture, which differs from the span of separately varying cross moments considered here.
* Pereira–Kileel–Kolda, [*Tensor Moments of Gaussian Mixture Models: Theory and Applications*](https://arxiv.org/abs/2202.06930), for Gaussian tensor-moment formulas and covariance removal when a common covariance is known. Here the cross-site quadratic is initially unknown and is recovered only modulo the equivalence class appropriate to response-span data.

This literature check identifies neighboring methods and models. It is not an exhaustive priority review, so the result should not yet be described as the first theorem of its kind.
