# Reconstructing a connected source graph and removing the quadratic ambiguity

Research note, 2026-09-27. This develops the [many-direction reconstruction theorem](many-direction-source-reconstruction-2026-09-27.md). It contains written proofs and exact computational certificates, but no Lean formalization or established priority claim. The Krenn–Gu paper is unchanged.

## 1. Main statement

The response span can recover more than a source modulo mean-quadratic additions. If the source graph is not complete, a missing edge fixes that addition. The graph need not be supplied to the reconstruction algorithm.

Let `G` be a connected simple support graph on `n >= 3` labeled sites, and let `nu` be its maximum matching size. Assume

$$
2\nu<n. \tag{1}
$$

Every connected graph of odd order satisfies (1). Even-order graphs without a perfect matching also satisfy it. The condition permits a large matching deficiency; near-perfect matchings are not required.

At each site let `dim V_i >= r+1`, with `r >= 3`. Let `E` be an `r`-dimensional space of mean rows in `direct_sum_i V_i`, with independent local projections at every site. Choose a basis `L_1,...,L_r` and an edge tensor

$$
R=\sum_{ij\in E(G)} R_{ij},\qquad R_{ij}\in V_i\otimes V_j.
$$

Use the commutative site algebra, in which products of two vectors at the same site vanish. Define responses

$$
P_p=\left(\prod_{s=1}^r\frac{L_s^{p_s}}{p_s!}\right)
\frac{R^{(n-|p|)/2}}{((n-|p|)/2)!},
$$

where `|p| <= n` and `|p|` has the parity of `n`. The output span `W(E,R)` is the span of all these tensors. An edge is a whole block `R_ij`; the support graph records which blocks are nonzero.

Since no matching has more than `nu` edges, all layers with more than `nu` edges vanish. Write

$$
d_G=\sum_{k=0}^{\nu}\binom{n-2k+r-1}{r-1},\qquad
u=\binom{n+r-1}{r-1},\qquad
h=\binom{2n+r-1}{r-1}.
$$

**Theorem 1 (reconstruction on connected deficient support graphs).** For each `G` satisfying (1), a nonempty Zariski-open subset of its source parameters has `dim W=d_G` and admits reconstruction from `W` by arithmetic, contractions, and linear algebra. Among sources whose mean directions are independent at every site, all sources with this span differ only by common mean-basis changes, nonzero site scalings, and

$$
R\longmapsto aR+q,\qquad a\ne0,\quad q\in\mathrm{Sym}^2E. \tag{2}
$$

Here `Sym^2 E` means its image in the edge component of the site algebra. Site scalings act by `L_(s,i) -> lambda_i L_(s,i)` and `R_ij -> lambda_i lambda_j R_ij`.

**Theorem 2 (unknown sparse graph).** If `G` is not complete, the same generic data determine `G` itself. Among locally independent mean sources whose support graph is not complete, the ambiguity `q` in (2) is zero. After aligning the mean frames, only a nonzero overall scale of `R` remains.

Neither theorem assumes that `G` is given to the inverse procedure. The first treats the source class modulo (2); the second uses the additional promise that some edge is absent. Alternative representations in these statements are required to retain local mean independence. This hypothesis is part of the model, including for nongeneric alternatives.

## 2. A matching observation supplies the witness

**Lemma 3 (a vertex covered by one maximum matching and missed by another).** A connected graph satisfying (1) has a vertex with this property.

**Proof.** Take a maximum matching `M` and an unmatched vertex `v`. Connectedness gives a neighbor `w`. The vertex `w` is matched, since otherwise adding `vw` would enlarge `M`; let its matching partner be `i`. Replace `wi` by `vw`. The new matching has the same size and misses `i`, which the original matching covered. QED.

This is an elementary alternating-path argument. It is used here to choose tensor coefficients; no new matching-theoretic assertion is claimed.

Choose local mean basis vectors `x_(1,i),...,x_(r,i)` and one further vector `z_i`. Consider

$$
L_s=\sum_i x_{s,i},\qquad
R_0=\sum_{ij\in E(G)}z_i z_j. \tag{3}
$$

At this witness, each response has a specified number `2k` of `z` factors and specified mean-colour counts. Different responses therefore have disjoint supports. Every response with `k <= nu` is nonzero: choose a `k`-edge matching, put `z` at its endpoints, and assign the mean colours on the remaining sites. Its coefficient counts perfect matchings on those endpoints and is a positive integer. Thus all `d_G` listed nonzero responses are independent.

## 3. The terminal mean space is still identifiable

Let

$$
U(E)=\mathrm{span}\left\{\bigotimes_i L_i(t):
L(t)=\sum_s t_sL_s\right\}.
$$

This is the `u`-dimensional terminal space, whose product tensors form a Veronese variety. Given a basis of `W`, form the coefficient matrix `C_W` of the `2 by 2` minors of **all single-site flattenings**. The particular useful site from Lemma 3 need not be known to the algorithm.

**Lemma 4 (terminal extraction on sparse support).** Generically, `dim ker C_W=h`. Interpreting its vectors as symmetric matrices and summing their images recovers `U(E)`. The product tensors in `W` are exactly the terminal products.

**Proof.** The terminal products always supply the `h`-dimensional quadratic-kernel subspace described in Lemma 2 of the preceding note. It suffices to show that no extra kernel remains at (3).

Fix the vertex `i` from Lemma 3. Every nonterminal response coordinate, with `k >= 1` edges, has a nonzero tensor entry containing `z` at site `i`: take a `k`-edge submatching of a maximum matching covering `i`, retaining its incident edge. Every response coordinate also has a nonzero tensor entry containing a mean colour at `i`: take a submatching of a maximum matching missing `i`. Condition (1) ensures there is at least one mean factor even in the lowest layer.

For a quadratic monomial involving a nonterminal coordinate, put its `z` entry in one diagonal position of a first-site minor at `i`, and the other coordinate's mean entry in the other diagonal position. Both cross entries have odd `z` counts and vanish throughout `W`. This minor is therefore a nonzero scalar times the desired quadratic monomial.

The remaining quadratic quotient is the classical Veronese quotient on terminal coordinates: one coordinate for each total degree-`2n` mean monomial. Its dimension is `h`. This proves equality at (3), and maximal rank is an open condition.

The kernel-image recovery and product-locus argument now apply exactly as in the preceding note: the quadratic kernel is spanned by outer squares of terminal coordinate vectors; any product vector must lie in their common image span `U`; a symmetric rank-one tensor in `U` is a pure power. QED.

Local contractions of `U` recover the mean planes. Two-site contractions recover their symmetric pair spaces and synchronize the local frames by a linear solve, as proved in Lemma 3 of the preceding note.

## 4. Edge recovery needs only the one-edge responses

For an arbitrary candidate edge tensor `Q`, including blocks outside `G`, put

$$
\Phi_E(Q;t)=\frac{L(t)^{n-2}}{(n-2)!}Q,\qquad
S(E,W)=\{Q:\text{all coefficients of }\Phi_E(Q;t)\text{ belong to }W\}.
$$

**Lemma 5 (the same complete ambiguity).** On a nonempty open set in the support-`G` model,

$$
S(E,W)=\mathbb C R+\mathrm{Sym}^2E. \tag{4}
$$

**Proof.** The right side always lies in `S`. Work at (3), first in the selected `(r+1)`-dimensional local spaces. A candidate with exactly one `z` factor must have zero image because `W` has only even `z` counts. It is zero by the edge-isolation lemma: a third mean colour isolates any prescribed edge coefficient in `Phi_E`.

For the two-`z` part of `Q`, inspect the coefficient with all other sites in the first mean colour. The corresponding part of `W` has exactly one response coordinate and its pair coefficients are those of `R_0`. Therefore this part of `Q` is proportional to `R_0`, including zero on every nonedge.

The zero-`z` part has its image in the terminal symmetric tensor space. Average that part over all site permutations. The average is in `Sym^2 E`, and has the same image. Injectivity of the edge-isolation map makes the original candidate equal its average.

If local dimensions are larger, the same edge isolation forces every coefficient outside the chosen local subspaces to vanish. Thus (4) holds at the witness in all stated dimensions. A nonzero maximal constraint minor proves it generically. QED.

**Proof of Theorem 1.** Terminal extraction and synchronization recover the mean geometry. An alternative locally independent mean source of the same dimension has its terminal Veronese variety inside the recovered product locus, with the same dimension, so the two terminal varieties coincide. Align their mean frames.

Its edge tensor then belongs to `S(E,W)`, yielding (2) by Lemma 5. If `a=0`, its entire response span is terminal and has dimension at most `u`. But `d_G>u`, since a connected graph on at least three sites has an edge. Hence `a != 0`. All required generic conditions hold at witness (3). QED.

## 5. Locating the missing edges fixes the quadratic addition

Let `E_i` be the recovered local mean plane, with synchronized injective frame `A_i:C^r -> E_i`, and let `Q` be any edge representative outside `Sym^2 E` in (4). At a pair `ij`, define the subspace of blocks generated by global mean quadratics,

$$
\mathcal Q_{ij}=\{A_i H A_j^t:H=H^t\}.
$$

The quotient class

$$
\overline Q_{ij}\in
(V_i\otimes V_j)/\mathcal Q_{ij}
$$

is unaffected by a mean-quadratic addition. On the generic set used here, every genuine edge has a nonzero quotient class. This holds at witness (3), so it is a nonempty open condition on the support-`G` parameter space.

Consequently the graph can be read off directly:

$$
ij\in E(G)\quad\Longleftrightarrow\quad\overline Q_{ij}\ne0. \tag{5}
$$

This identifies the part of each block that cannot be produced by adding a global mean quadratic. A sparsity promise then identifies its unique sparse representative. Testing the larger quotient by `E_i tensor E_j` would also suffice on the generic set with an extra local coordinate, but the smaller subspace `mathcal Q_ij` additionally detects antisymmetric coefficients within the aligned mean planes.

**Proof of Theorem 2.** Write `Q=aR+q`. At any missing edge `ij`, the block `Q_ij` is just the block of `q`. If `A_i:C^r -> E_i` are the synchronized injective mean maps, write that block as

$$
Q_{ij}=A_i H A_j^t,
$$

where `H` is a symmetric matrix. Left inverses of `A_i,A_j` recover `H` uniquely. Subtracting `A_k H A_l^t` at every pair removes `q` globally and recovers `aR`.

Moreover, a nonzero symmetric `H` gives a nonzero block `A_i H A_j^t` at **every** pair, because both mean maps are injective. Adding such a term fills every original nonedge. It cannot cancel any original edge, whose quotient class in (5) is nonzero. Thus every alternative with `q != 0` has complete support. The promise that at least one edge is absent forces `q=0`. QED.

The reconstructed graph is a pair-source graph, or a graph of nonzero **cross-covariance** blocks in the Gaussian interpretation. It is not a graph of nonzero entries of a precision matrix, so no conditional-independence interpretation is asserted.

This distinction follows the established covariance-graph terminology; see Drton–Richardson, [*Graphical Methods for Efficient Likelihood Inference in Gaussian Covariance Models*](https://www.jmlr.org/papers/v9/drton08a.html). Their likelihood model observes ordinary Gaussian data. The present reconstruction theorem instead specifies a family of cross-moment or matching-amplitude tensors as its input.

The missing-edge correction itself does not require an extra local coordinate. It needs an already reconstructed class (2) and nonzero edge classes modulo `mathcal Q_ij`. These conditions also make sense when the local dimension equals `r`; the all-orders witness for terminal and edge-class recovery is the part that currently uses the extra coordinate.

**Corollary 6 (control dimension, and matching size under the sparsity promise).** On the same generic set, the number `r` is obtained as the local rank of the recovered terminal space. Under the sparse-source promise in Theorem 2, the strictly increasing dimension formula `d_G` then determines the maximum matching size `nu` of the recovered graph.

The control dimension is also unique among locally independent competitors. A larger control dimension would give a terminal product variety of larger dimension inside the recovered product locus. A smaller dimension is excluded even by output counts: for `r' <= r-1`, the total number of all possible response coefficients is strictly less than

$$
\sum_{k=0}^{n}\binom{k+r-2}{r-2}
=\binom{n+r-1}{r-1}=u\le d_G.
$$

The strict inequality comes from retaining only one parity of `k`. Thus the theorem can be interpreted with unknown `r`. Computing the full flattening coefficient matrix does not require `r` in advance; the implementation uses it to stop once the proved maximal rank is reached.

**Example 7 (why a sparsity promise is needed).** A generic four-site star with three mean directions has response dimension `15+6=21`, since its maximum matching size is one. Add a nonzero mean quadratic `q` to its edge tensor. This fills all missing edges and preserves the response span, but the new complete support graph has a perfect matching. Its nominal twenty-second response is dependent: since the original star has `R^2=0`, the new zero-mean response is `Rq+q^2/2`, a combination of the old one-edge and terminal responses. Thus response dimension alone does not exclude a nongeneric complete representative with a larger graph matching number. Theorem 2 excludes it using the stated sparsity promise.

## 6. Exact examples and limitations

The implementation is [sparse_direction.py](../computations/matching-tensor-recovery-2026-09-26/sparse_direction.py). It generates test observations from a graph, then gives only the observed tensors to the mean and edge reconstruction. Its separate graph-recovery function receives only the recovered mean frame and edge class. The original graph is consulted after recovery to check the answer.

```sh
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python computations/matching-tensor-recovery-2026-09-26/sparse_direction.py
```

The [certificate](../computations/matching-tensor-recovery-2026-09-26/sparse-direction-certificate.json) uses `r=3`, local dimension `4`, seed `270927`, and modulus `1009`.

| Source graph | Sites | Maximum matching size | Response dimension | Terminal dimension | Edge-class ambiguity before sparsity | After sparsity and mean alignment |
|---|---:|---:|---:|---:|---:|---|
| Star | 5 | 1 | 31 | 21 | 7 | One overall scale |
| Cycle | 5 | 2 | 34 | 21 | 7 | One overall scale |
| Star | 4 | 1 | 21 | 15 | 7 | One overall scale |

In every example the algorithm recovers precisely the original edges, corrects all absent-edge blocks to zero, and independently verifies that all six mean-quadratic comparison coefficients vanish. The four-site case checks the even-order extension, and the five-site star checks a source with matching deficiency larger than one.

There are also exact witnesses for stars on four and five sites with **three-dimensional**, rather than four-dimensional, local spaces. The [minimal-local certificate](../computations/matching-tensor-recovery-2026-09-26/minimal-local-sparse-certificate.json) records quadratic ranks `186,430` and edge-constraint ranks `47,83`; the selected nonzero minors are respectively `386,363` and `369,340`, modulo `1009`. These rank witnesses and the comparison proof establish generic sparse reconstruction for each of these two support formats. They do not establish the minimal-local statement for arbitrary connected graphs or arbitrary order. Replay them with:

```sh
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python computations/matching-tensor-recovery-2026-09-26/sparse_direction.py --minimal-local
```

Certificate site indices start at zero. All five recorded sparse examples also recover the maximum matching size from the response dimension and check it against the reconstructed graph.

The all-order assertion follows from the common witness and the proofs above. These examples verify the implementation and provide independently replayable exact source comparisons. They do not establish numerical stability under noisy measurements.

The flattening and Veronese tools have the classical precedents discussed in the [preceding note](many-direction-source-reconstruction-2026-09-27.md#5-relation-to-earlier-work-and-remaining-boundaries). The added conclusions here are reconstruction on graph support strata and the complete removal of the mean-quadratic ambiguity by an unknown missing edge. A search for earlier work on this exact observed-span inverse problem remains necessary before making a novelty claim.
