# Recovering source directions and testing auxiliary coupling dimension

Date: 2026-09-26.

**Status:** research extension with written proofs and exact computational certificates. Not Lean-formalized or externally reviewed. No literature-first claim. The Krenn–Gu manuscript is unchanged.

This follows [the exterior-rank note](matching-tensor-exterior-obstruction-2026-09-26.md). It develops three further uses of the response identities:

1. Generically recover the local monomer directions from a single five- or seven-site output tensor.
2. Extend the rank obstruction to arbitrarily many hidden vertices when their visible coupling rows span one dimension; give a counterexample when that dimension is two.
3. Use `r+1` formal copies for a source with `r` mean directions. For `r=2`, this gives a cubic test for several outputs of a shared source.

The exact matrix construction has been identified in prior literature: it is the multi-factor Koszul flattening `K_(1,...,1)` of Hauenstein–Oeding–Ottaviani–Sommese, Section 5.1, equation (6), in [*Homotopy techniques for tensor decomposition and perfect identifiability*](https://arxiv.org/abs/1501.00090). Their Section 5.2 also develops recovery from flattening kernels. Our matrix and the general kernel-recovery strategy must be attributed to this existing theory. The matching-response subspaces and the particular conclusions below require their own comparison with prior work.

## 1. Notation and the observable matrix

At each of `n` sites use `V_i = C^3`. A monomer weight is a vector `l_i` in `V_i`; an edge weight is a tensor `R_ij` in `V_i tensor V_j`. Let `P_k` be the matching tensor with exactly `k` unmatched sites, using these same weights at every layer. For odd `n`, the full monomer-dimer tensor is

$$
T=P_1+P_3+\cdots+P_n.
$$

Its terminal layer is the product tensor

$$
P_n=l_1\otimes\cdots\otimes l_n.
$$

A **product tensor** means a nonzero tensor of the form `u_1 tensor ... tensor u_n`. Its line determines the individual lines `[u_i]` uniquely. These lines are called the local directions; their magnitudes are not determined by the product's projective class.

For words `a,b,c` in `{0,1,2}^n`, define the matrix

$$
A(T)_{a,b}=\sum_c T_c\prod_i\epsilon_{a_i b_i c_i},
$$

where `epsilon_(012)=1` is the alternating symbol. The earlier note proves that every `P_k` is in `ker A(T)`. It also gives rank bounds `240` at five sites and `2182` at seven sites.

Thus an observable output tensor supplies a linear space that contains the product of its hidden monomer vectors.

## 2. A kernel criterion that recovers all local directions

Let `K = ker A(T)` have basis `K_1,...,K_d`. Form the tensor depending linearly on unknown coordinates `z_1,...,z_d`:

$$
U(z)=\sum_{j=1}^d z_jK_j.
$$

Arrange `U(z)` as a `3` by `3^(n-1)` matrix, separating the first site from the others. Every product tensor has matrix rank one in this arrangement. Hence all its `2` by `2` minors vanish. Those minors are homogeneous quadratic polynomials in the `z_j`.

Let `C_K` be the matrix of their coefficients, with columns indexed by the `d(d+1)/2` monomials `z_i z_j`, `i <= j`. This is a second linear-algebra problem, much smaller than the first.

**Lemma 1 (unique product from quadratic restrictions).** Suppose `K` contains a product tensor and

$$
\mathrm{rank}\,C_K=\frac{d(d+1)}2-1.
$$

Then `K` contains exactly one product-tensor line. That line can be recovered using linear algebra and a rank-one factorization of a `d` by `d` symmetric matrix.

**Proof.** The quadratic coefficient matrix has a one-dimensional kernel. For any product tensor `U(z)`, the vector of monomials `(z_i z_j)_(i<=j)` lies in this kernel. A known-to-exist product tensor shows that its generator can be arranged as a nonzero rank-one symmetric matrix, proportional to `z z^t`. This determines `[z]` uniquely. A nonzero column of that symmetric matrix determines `[z]` without choosing a square root. Recover `U(z)` and factor its individual sites. QED.

The flattening across the first site is used as a necessary condition for being a product at all sites. The known product in `K` and the one-dimensional quadratic kernel make this necessary condition sufficient to isolate that particular line. No claim is made that arbitrary rank-one first-site flattenings are fully decomposable tensors.

**Lemma 2 (zero monomer vectors cannot hide a different representation).** If `ker A(T)` contains exactly one product-tensor line and `T` has a monomer-dimer representation, every monomer vector in that representation is nonzero. Its monomer directions are the factors of the unique product line.

**Proof.** If all monomer vectors are nonzero, `P_n` gives the required line. Suppose instead that some of them vanish. Replace each zero monomer vector by `t u_i`, leaving the other source parameters fixed. Let `s` be the number of zero monomer vectors. The terminal product is `t^s U`, where the factors of `U` at the zero sites are arbitrary nonzero `u_i`. For nonzero `t`, the universal identity gives `A(T(t))U=0`, after division by `t^s`. Taking the polynomial limit at zero gives `A(T)U=0`. Varying a factor at any zero site produces multiple product lines, contrary to the assumption. QED.

The argument also applies to outputs `sum c_k P_k`, for fixed arbitrary layer coefficients, because the terminal product lies in the kernel of every such output.

**Theorem 3 (generic recovery at five and seven sites).** For a nonempty Zariski-open set of five-site monomer-dimer sources, and likewise of seven-site sources, the output tensor determines every local monomer direction uniquely, among all monomer-dimer representations of that output. The directions can be recovered from the output alone by Lemma 1.

**Proof with exact genericity certificates.** The all-orders rank theorem bounds `dim ker A(T)` below by `3` and `5`, respectively. The supplied integer-parameter witnesses, reduced modulo `1009`, attain these dimensions and give:

| Sites | Exterior rank | Kernel dimension `d` | Quadratic columns | Quadratic coefficient rank | Nonzero square-minor residue |
|---|---:|---:|---:|---:|---:|
| 5 | 240 | 3 | 6 | 5 | 256 |
| 7 | 2182 | 5 | 15 | 14 | 665 |

The witnesses specify the source parameters, the selected quadratic minors, their coefficient rows, and the deleted coefficient column. All arithmetic is exact.

A nonzero modular minor is a certificate of a nonzero polynomial over the integers. On a chart where the exterior rank is maximal, a kernel basis is a rational function of the source parameters. Clearing its nonvanishing pivot denominators converts the second rank witness into another nonzero polynomial condition. Consequently, both rank properties hold on a nonempty Zariski-open set over `C`. The terminal product exists on the open set where the monomer vectors are nonzero. Lemmas 1 and 2 then establish the conclusion, including uniqueness against exceptional alternative representations. QED.

The verifier constructs `T`, then calls the recovery routine **without providing the source or its layers**. Only after recovery does it compare the result with the generating monomer vectors. All five and all seven directions are recovered exactly in their respective witnesses.

### Statistical interpretation and limits

For jointly Gaussian three-dimensional vectors `X_1,...,X_n`, the tensor

$$
T=\mathbb E[X_1\otimes\cdots\otimes X_n]
$$

has the monomer-dimer expansion, with `l_i = E[X_i]` and `R_ij` equal to the cross-covariance blocks. The theorem therefore gives a generic method to recover **mean directions from a single cross-moment tensor**, at orders five and seven, without being supplied lower moments.

This statement concerns exact moments and nonzero generic means. It does not recover mean magnitudes, covariance blocks, or Gaussian mixtures, and it is not yet a noise-stability guarantee. Within-block covariance entries never appear in this cross-moment and cannot be recovered from it.

The real positive-definite Gaussian setting is not vacuous: arbitrary real off-diagonal blocks can be completed to a positive-definite covariance matrix by choosing sufficiently large diagonal blocks. Those diagonal blocks do not change this cross-moment.

## 3. Arbitrarily many auxiliary vertices with one coupling direction

Consider a perfect-matching graph with visible sites and `h` additional scalar hidden vertices. Contracting a fixed local covector at a hidden coloured vertex reduces it to this scalar model. Let:

* `R` be the quadratic on the visible sites;
* `H` be the symmetric matrix of hidden-hidden edge weights;
* `L_alpha` be the row of weights joining hidden vertex `alpha` to all visible sites and their colours.

The **visible coupling dimension** is the dimension of the span of the rows `L_alpha` in `direct_sum_i V_i`. It counts independent rows, not the number of nonzero hidden edges.

**Theorem 4 (one-direction auxiliary stability).** If all the rows are proportional, `L_alpha = lambda_alpha L`, the resulting odd-site output is a linear combination of monomer layers from one common source `(L,R)`. Hence all the exterior-rank bounds of the previous note apply, for any number of hidden vertices and any hidden-hidden weights.

**Proof.** Group a perfect matching by the set `S` of hidden vertices matched to visible vertices. The remaining hidden vertices contribute `haf H[S^c]`. The cross edges contribute `(product_(alpha in S) lambda_alpha) L^|S|`. The remaining visible vertices are paired using `R`. Thus

$$
T=\sum_{k\text{ odd}}c_kP_k,\qquad
c_k=k!\sum_{\substack{S\subseteq[h]\\|S|=k}}
\mathrm{haf}(H[S^c])\prod_{\alpha\in S}\lambda_\alpha.
$$

The hafnian of an odd-size matrix is interpreted as zero, and that of the empty matrix as one. Terms with more cross edges than visible sites vanish. This is exactly the earlier layer model. QED.

**Corollary 5.** The positive five-site Potts tensor in the earlier note cannot be represented using any number of scalar auxiliary vertices with visible coupling dimension at most one. Any auxiliary-vertex representation of it must have visible coupling dimension at least two.

This does not assert that dimension two suffices to realize that Potts tensor.

**Proposition 6 (the one-direction hypothesis matters).** There is a perfect-matching source with five visible three-dimensional sites and three scalar hidden vertices, whose visible coupling dimension is two and whose output has exterior rank `242`.

**Exact certificate.** The supplied source is parameterized by two row vectors and three pairs of coefficients, so its coupling dimension is at most two over `C`. A nonzero coupling minor modulo `1009` proves equality. For its output, the `242` by `242` principal exterior minor obtained by omitting the all-zero word has determinant

$$
350\pmod{1009}.
$$

Thus the complex exterior rank is `242`, contradicting the one-direction upper bound `240`. The certificate is checked by a determinant and an independent Pfaffian computation. When lifting the parameters to integers, the coupling rows must be formed as **unreduced** linear combinations of the listed basis rows; reduction is used only for certificate arithmetic.

For comparison, a source with the same visible and hidden internal edges and one coupling direction has exterior rank `240` in the finite-field test.

## 4. More copies for more coupling directions

The failure at coupling dimension two does not end the symmetry method. It changes the kind of identity available.

Let `n` be odd, let `R` be a fixed quadratic on the visible sites, and let `L_1,...,L_r` be fixed rows. For a multi-index `p = (p_1,...,p_r)` with odd total `|p| <= n`, define the response tensor

$$
P_p=\left(\prod_{s=1}^r\frac{L_s^{p_s}}{p_s!}\right)
\frac{R^{(n-|p|)/2}}{((n-|p|)/2)!}.
$$

Products are in the commutative site algebra, where two factors at the same site multiply to zero. Equivalently, `P_p` assigns exactly `p_s` monomers to row type `s` and sums all remaining pairings. Let `W_r` be the span of these tensors. Arbitrary hidden graphs whose visible rows lie in the same `r`-dimensional row space produce outputs in `W_r`, by the same grouping argument as Theorem 4.

For `q` tensors define the multilinear exterior operation

$$
\mathcal B_q(T^{(1)},...,T^{(q)})
\in\bigotimes_{i=1}^n\Lambda^q V_i
$$

by taking the exterior product of their `q` local factors at each site and extending multilinearly. Since `n` is odd, this operation is alternating in the `q` tensor arguments.

**Theorem 7 (multiple-copy identity).** Put `q = r+1`. For all `T^(1),...,T^(q)` in `W_r`,

$$
\mathcal B_{r+1}(T^{(1)},...,T^{(r+1)})=0.
$$

This is informative only if the local dimensions are at least `r+1`.

**Proof.** Introduce `r` auxiliary formal symbols `g_s`, paired with the site variables by `L_s` and with every auxiliary symbol by zero. Take `q` identical copies of this full Wick family. For each `s`, introduce an arbitrary copy-space vector `t_s` in `C^q` and the linear form `sum_a t_(s,a) g_(s,a)`.

Generically the `r` vectors `t_s` span a nondegenerate hyperplane in `C^(r+1)`. The orthogonal reflection in that hyperplane fixes all `r` linear forms. It preserves the replicated pairing table and negates each local `q` by `q` determinant. A product of an odd number of these determinants therefore has zero moment when multiplied by arbitrary powers of the fixed auxiliary linear forms.

Extracting a monomial in the independent coefficients `t_(s,a)` assigns a prescribed multi-index of auxiliary insertions to each copy. Its coefficient is a nonzero multinomial factor times a coordinate of `mathcal B_q` applied to the corresponding responses. These coordinates all vanish. Polynomial extension removes the generic hyperplane restriction, and multilinearity gives the statement for the entire span `W_r`. QED.

For `r=1`, this is the two-copy identity and common-kernel result from the earlier note. For `r=2`, the conclusion is a three-copy identity; it does not require `W_2` to lie in the kernel of `A(T)` for each `T`. Thus there is no contradiction with Proposition 6.

**Lemma 8 (generic response-space size).** If each local dimension is at least `r+1`, then generically

$$
\dim W_r=\sum_{\substack{k\leq n\\k\text{ odd}}}\binom{k+r-1}{r-1}.
$$

**Proof.** The right side counts the responses, so it is an upper bound. For a witness, choose the `r` mean rows to use `r` different basis colours, and let `R` use only disjoint edges in one additional colour. A response's multi-index fixes its counts of the mean colours; the number of extra-colour sites fixes its number of dimers. Different responses have disjoint supports, and every response is nonzero. Independence therefore holds on a nonempty open set. QED.

At five sites with two mean directions, this space has dimension `2+4+6=12`. Consequently the three-copy identity is not merely the statement that three outputs lie in a two-dimensional linear space.

## 5. A cubic test for several outputs of one source

For three-dimensional sites, the three-copy exterior operation is scalar after choosing the local volume forms. Define

$$
\Omega(T_1,T_2,T_3)
=\sum_{a,b,c}(T_1)_a(T_2)_b(T_3)_c
\prod_i\epsilon_{a_i b_i c_i}
=T_1^t A(T_3)T_2.
$$

**Corollary 9 (joint coupling-dimension witness).** Suppose several odd-site outputs share the same visible quadratic `R` and their visible coupling rows all belong to a common two-dimensional space. Internal hidden graphs and the numbers of hidden vertices may vary. Then every triple of outputs satisfies `Omega = 0`. A triple with nonzero `Omega` excludes every such shared-source explanation.

This is a statement about a **common** quadratic and a **common** coupling-row space. It does not restrict three unrelated experiments whose sources may change arbitrarily.

Exact checks modulo `1009` give:

| Visible sites | Two-direction response-space dimension | Distinct response triples tested | Nonzero values |
|---|---:|---:|---:|
| 3 | 6 | 20 | 0 |
| 5 | 12 | 220 | 0 |

The zeros are proved by Theorem 7; the calculations check the implementation. For explicit sources using three mean directions and the same visible quadratic, the three root-response tensors instead give `Omega = 729` at three sites and `Omega = 594` at five sites, modulo `1009`. Those nonzero residues certify obstructions over `C` to any alternative two-direction shared-source representation, even one using nonlinear response layers and arbitrarily many auxiliaries.

## 6. Reproduction, attribution, and next questions

From the repository root:

```sh
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python computations/matching-tensor-recovery-2026-09-26/verify.py
PYTHONDONTWRITEBYTECODE=1 python3 computations/matching-tensor-recovery-2026-09-26/multi_copy.py
```

The first command uses the existing `python-flint` installation. The second uses only the standard library. Both print JSON and do not modify the source files.

Saved certificates include explicit source parameters:

* [Recovery and auxiliary-vertex certificates](../computations/matching-tensor-recovery-2026-09-26/certificate.json).
* [Multiple-copy checks and joint-model obstructions](../computations/matching-tensor-recovery-2026-09-26/multi-copy-certificate.json).

Besides the exact Koszul-flattening precedent cited above, relevant primary literature includes:

* Aizenman–Laínz Valcázar–Warzel, [*Pfaffian Correlation Functions of Planar Dimer Covers*](https://arxiv.org/abs/1609.02824), for the switching foundation of the two-copy identity.
* Améndola–Faugère–Sturmfels, [*Moment Varieties of Gaussian Mixtures*](https://arxiv.org/abs/1510.04654), for the algebraic study of Gaussian moments.
* Kothari–Moitra–Wein, [*Overcomplete Tensor Decomposition via Koszul-Young Flattenings*](https://arxiv.org/abs/2411.14344), for current use of flattenings in constructive tensor recovery. Its decomposition model and guarantees differ from the monomer-direction problem here.

These connections narrow any defensible novelty claim. The tools are established; the model-specific kernel theorem, recovered parameters, and coupling-dimension identities are what would need a priority review.

The first two questions below are now answered generically for two mean directions at every odd number of sites at least five; see the separate [source reconstruction proof](two-direction-source-reconstruction-2026-09-26.md), including the complete ambiguity classification. They remain useful questions outside that scope.

The directions identified in this note were:

1. **Recover several mean directions from an output family.** In `W_r`, the terminal products `(sum_s t_s L_s)^n/n!` form a structured family of product tensors. Determine when the product tensors in `W_r` recover the original mean-row space. The `r=1`, five- and seven-site result above is a first case; the subsequent note treats `r=2` generically in all odd orders at least five.
2. **Recover the quadratic source after recovering monomer directions.** The single-output theorem here does not identify `R`. The subsequent note classifies and reconstructs its equivalence class from a complete two-direction response span.
3. **Develop target-independent hypotheses for the corrected-insertion/divisibility argument.** The results here use reflection and exterior structure. They do not yet give a second application of the more specialized endpoint rigidity argument in the Krenn–Gu proof.
