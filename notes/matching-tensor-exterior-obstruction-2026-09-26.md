# Exterior-rank obstructions for odd monomer-dimer tensors

Date: 2026-09-26.

**Status:** new research note, with a written all-orders proof and exact computational examples. Not Lean-formalized, independently peer reviewed, or claimed to be a literature-first result. The existing Krenn–Gu paper is unchanged.

## 1. Outcome and scope

The copy-reflection identity has a target-independent extension: **all fixed-monomer-count tensors from the same source pair to zero under the product of local exterior pairings.** This supplies a common kernel for a matrix constructed directly from the output tensor.

For an odd number `n = 2m + 1` of three-dimensional sites, every monomer-dimer tensor, and more generally every linear combination of its monomer-count layers, satisfies

$$
\mathrm{rank}\, A(T)
\leq 3^n-\left(2\left\lfloor\frac{n+1}{4}\right\rfloor+1\right).
$$

The matrix `A(T)` is defined in Section 4. The bound holds for arbitrary complex edge and monomer weights, including degenerate sources. It also holds on the closure of the model, so a violation excludes limiting representations as well as exact ones.

Two explicit applications are recorded below:

* A positive five-site, three-state Potts interaction tensor has exterior rank **242**, above the model bound **240**.
* A seven-site tensor satisfies the elementary product-vector kernel condition, but has exterior rank **2184**, above the higher-response bound **2182**. Thus the hierarchy gives a strictly stronger obstruction than that elementary condition.

These are fixed-site statements. They do not rule out representations with additional hidden vertices or other enlarged computational resources. This is not a characterization of all matching tensors or a hardness theorem for general counting algorithms.

## 2. Definitions

Let `n = 2m + 1` be odd. At site `i`, let `V_i` be a finite-dimensional complex vector space with a chosen basis. Write

$$
\mathcal V=\bigotimes_{i=1}^n V_i.
$$

A **monomer** is an unmatched site, with vector of weights `l_i` in `V_i`. A **dimer** is an edge joining two different sites `i,j`, with weight tensor `R_ij` in `V_i ⊗ V_j`. No symmetry between the two endpoint colours is required; the edge is interpreted with its endpoints in their fixed order.

For each odd `k` between `1` and `n`, define `P_k` in `mathcal V` by summing over all matchings with exactly `k` unmatched sites. Its coefficient at a word `a = (a_1,...,a_n)` is

$$
(P_k)_a=
\sum_{\substack{M\text{ a matching on }[n]\\n-2|M|=k}}
\left(\prod_{i\text{ unmatched in }M}l_i(a_i)\right)
\left(\prod_{\{i,j\}\in M,\ i<j}R_{ij}(a_i,a_j)\right).
$$

Each matching occurs once. The full **monomer-dimer tensor** is

$$
T_{\rm MD}=P_1+P_3+\cdots+P_n.
$$

The theorem also allows arbitrary complex scalars `c_k` and the output

$$
T=\sum_{k\text{ odd}}c_kP_k.
$$

All the layers in this sum must use the **same** `l_i` and `R_ij`. Allowing a different source for each layer is a different model.

For comparison with the existing proof, use its commutative site algebra, in which multiplying two coordinates at the same site gives zero. Put `L = sum_i l_i` and `R = sum_(i<j) R_ij`. Then

$$
P_k=\frac{L^k}{k!}\frac{R^{(n-k)/2}}{((n-k)/2)!}
=\frac{H_k(L)}{k!}.
$$

This algebraic expression is shorthand for the matching sum, not ordinary polynomial multiplication without the site relations.

Define the **local exterior pairing**

$$
\mathcal B:\mathcal V\times\mathcal V
\longrightarrow\bigotimes_{i=1}^n\Lambda^2 V_i
$$

by bilinear extension of

$$
\mathcal B(u_1\otimes\cdots\otimes u_n,
v_1\otimes\cdots\otimes v_n)
=\bigotimes_{i=1}^n(u_i\wedge v_i).
$$

Here `Lambda^2 V_i` is the exterior square, whose product obeys `u wedge v = -v wedge u`. Since `n` is odd, `mathcal B(S,T) = -mathcal B(T,S)`.

## 3. Universal layer identity

**Lemma 1 (pairwise vanishing of matching layers).** For any odd `k,l` in `{1,3,...,n}`,

$$
\mathcal B(P_k,P_l)=0.
$$

**Proof by copy reflection.** Give ordinary formal symbols `X_(i,a)` their prescribed symmetric Wick pairing table `R`. Introduce a symbol `g` paired with `X_(i,a)` by `l_i(a)`, and paired with itself by zero. Duplicate the entire family into two copies with zero cross-copy pairings. A moment with `k` copies of `g` is the raw response `H_k = k! P_k`.

Fix two different coordinates `alpha_i,beta_i` at every site and form

$$
\Delta_i=X_{i,\alpha_i}Y_{i,\beta_i}
-X_{i,\beta_i}Y_{i,\alpha_i}.
$$

The orthogonal reflection fixing `s g_1 + t g_2` negates every `Delta_i`. It preserves the replicated pairing table. Therefore

$$
\left\langle(sg_1+tg_2)^{k+l}\prod_i\Delta_i\right\rangle=0.
$$

Extracting `s^k t^l` gives a nonzero binomial factor times the selected coordinate of `mathcal B(H_k,H_l)`. All its coordinates vanish. The argument first takes place over `C(s,t)`; the resulting identity is polynomial and holds everywhere. Dividing by `k! l!` proves the claim. No positivity, invertibility of a covariance matrix, or target sparsity is used. QED.

**Independent combinatorial proof.** Expand a coordinate of `mathcal B(P_k,P_l)` as a signed sum of two coloured matching configurations. Overlay their two matchings. Every connected component is an alternating even cycle, a doubled edge, a path, or an isolated vertex. Because there are an odd number of vertices, some component has an odd number of vertices. Such a component must be a path, including a single isolated vertex as a path of length zero.

Choose the odd component containing the smallest possible vertex. Exchange the two copies along this component: swap the ownership of its dimer edges and swap the two local colour assignments at all of its vertices. A nontrivial odd-vertex path has one monomer endpoint in each copy, so each copy's monomer count is preserved. An isolated vertex likewise has one monomer in each copy. Edge and monomer weights are preserved because the copies use identical parameters. The exterior sign changes by `(-1)` to the odd number of swapped vertices, hence changes sign. The operation is an involution, and its chosen component is unchanged by the operation. Terms cancel in pairs. QED.

This is a direct instance of double-dimer switching. It identifies a classical combinatorial foundation for the copy argument; duplication alone is not a new principle.

**Corollary 2 (common kernel).** Let `W` be the span of `P_1,P_3,...,P_n`. For every `T` in `W`,

$$
W\subseteq\ker\bigl(S\longmapsto\mathcal B(S,T)\bigr).
$$

**Lemma 3 (generic independence).** If every `V_i` has dimension at least two, the `m+1` tensors `P_1,P_3,...,P_n` are linearly independent for parameters in a nonempty Zariski-open set.

**Proof.** Choose two basis vectors `e_0,e_1` at each site. Let every monomer vector be `e_0`. Use only the disjoint edges `(1,2),(3,4),...,(2m-1,2m)`, each with weight `e_1 tensor e_1`. The layer `P_(n-2r)` is nonzero and supported on words with exactly `2r` occurrences of `e_1`. The layers have disjoint supports and are independent. Thus one of their maximal minors is a nonzero polynomial in the parameters. QED.

**Theorem 4 (target-independent exterior-rank bound).** Assume every `V_i` has dimension at least two, and put `D = product_i dim(V_i)`. For every source and every choice of scalars `c_k`, the tensor `T = sum_k c_k P_k` satisfies

$$
\mathrm{rank}\bigl(S\longmapsto\mathcal B(S,T)\bigr)
\leq D-(m+1).
$$

**Proof.** On the nonempty open parameter set of Lemma 3, Corollary 2 supplies `m+1` independent kernel vectors. Every minor of order `D-m` is therefore zero there. Each such minor is a polynomial in the source parameters and the `c_k`, hence vanishes identically. This proves the bound also when the actual layers become dependent or vanish. QED.

The polynomial-extension step is necessary: independence is generic, not asserted for every source.

## 4. Three-dimensional sites

Now let every `V_i = C^3`, with basis indexed by `0,1,2`. Choose the volume form with `epsilon_(012)=1`; `epsilon_(abc)` is the alternating symbol, zero if two indices coincide.

Use this volume form to identify `Lambda^2 C^3` with `(C^3)^*`. The exterior pairing becomes the following `3^n` by `3^n` matrix, indexed in lexicographic word order:

$$
A(T)_{a,b}=\sum_{c\in\{0,1,2\}^n}
T_c\prod_{i=1}^n\epsilon_{a_i b_i c_i}.
$$

There is at most one nonzero summand for fixed `a,b`. It is zero if `a_i=b_i` anywhere; otherwise `c_i` is the third element of `{0,1,2}`. This makes the construction explicit and sparse.

For odd `n`, `A(T)` is skew-symmetric. Its rank is even and its nullity is odd. Also `A(T)T=0` for every tensor `T`, whether representable or not.

**Corollary 5 (odd three-dimensional bound).** For the model of Section 2,

$$
\mathrm{rank}\,A(T)
\leq3^n-\delta_n,
\qquad
\delta_n=2\left\lfloor\frac{n+1}{4}\right\rfloor+1.
$$

**Proof.** Theorem 4 gives nullity at least `m+1`. Round this up to the smallest odd integer, since the matrix size is odd and its rank even. QED.

| Sites `n` | Matrix size | Proven rank upper bound |
|---|---:|---:|
| 3 | 27 | 24 |
| 5 | 243 | 240 |
| 7 | 2187 | 2182 |
| 9 | 19683 | 19678 |

**Corollary 6 (closure and basis invariance).** These bounds hold on the affine and projective closures of the model, and are unchanged by invertible changes of basis at individual sites.

**Proof.** The rank condition is the vanishing of homogeneous minors (equivalently suitable Pfaffians), so it defines a closed cone. Under local basis maps `g_i`, the exterior map is transformed by invertible maps on its domain and codomain. Its rank is unchanged. QED.

In particular, this is a border obstruction. It does not address the harder task of distinguishing a model from its own boundary points.

## 5. A positive Potts interaction tensor excluded by the bound

For five three-state variables define

$$
T_{a_1a_2a_3a_4a_5}
=\prod_{1\leq i<j\leq5}
\bigl(1+J_{ij}\,[a_i=a_j]\bigr),
$$

where the bracket is `1` for equality and `0` otherwise, and the couplings are

| Edge | 12 | 13 | 14 | 15 | 23 | 24 | 25 | 34 | 35 | 45 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `J_ij` | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |

This is the unnormalized configuration-weight tensor of an inhomogeneous ferromagnetic three-state Potts model on five labelled vertices. All entries are positive integers, at most `11! = 39916800`.

**Proposition 7 (exact rank certificate).** This tensor satisfies `rank A(T) = 242` over `C`.

**Proof with exact computation.** Delete the row and column indexed by `(0,0,0,0,0)` from `A(T)`. The resulting integer skew matrix `B` has order `242`. Exact modular elimination gives:

| Prime | `det B` modulo prime | `Pf B` modulo prime |
|---:|---:|---:|
| 101 | 6 | 39 |
| 1009 | 817 | 62 |
| 10007 | 3946 | 2213 |

The determinant and Pfaffian routines are separate algorithms and satisfy `det B = (Pf B)^2` in each field. Already the residue `6 mod 101` proves that the integer determinant is nonzero. Thus the complex rank is at least `242`. Skew-symmetry in dimension `243` gives the reverse bound. QED.

**Corollary 8 (Potts representation obstruction).** This Potts tensor is not a five-site monomer-dimer tensor, not an arbitrary linear combination of layers from a single such source, and not a limit of these tensors, even when all representing parameters are complex.

The obstruction is `242 > 240`. This makes no claim about adding hidden vertices. It also does not say that pairwise-interaction models in general cannot realize the tensor: the displayed Potts product is itself a pairwise-interaction model. The excluded model is specifically a **sum over disjoint pairs and singleton sites**.

The tensor is not a disguised diagonal GHZ target under invertible local basis changes. For the five-site diagonal three-term tensor, the same exterior rank is `3 * 2^5 - 4 = 92`. To see this, binary mixed words form `3(2^5-2)` independent off-diagonal directions; the three constant words contribute a skew block of rank `2`; words using all three colours give zero columns. Local basis invariance separates ranks `92` and `242`.

**Limitation of this example.** At five sites the bound can also be obtained from the terminal product vector `P_5`, together with `A(T)T=0` and parity, followed by polynomial extension. Thus this example demonstrates usefulness of the exterior obstruction, but does not by itself show that the intermediate response layers add strength.

## 6. Seven sites: intermediate layers give additional strength

We supply a separate exact test of that issue. It uses an explicitly generated integer tensor `S` on seven three-dimensional sites.

Enumerate words `a` lexicographically, with indices `0,...,2186`. Start an unsigned 32-bit state at `1729`. For **every** index, update it in order by

```
state ^= state << 13
state ^= state >> 17
state ^= state << 5
```

with unsigned 32-bit truncation after each operation. Set

$$
S_a=\begin{cases}
1+(\text{state}\bmod100),&a\text{ contains a zero},\\
0,&\text{otherwise}.
\end{cases}
$$

This deterministic rule is a compact specification of an integer tensor, not a probabilistic existence claim.

**Proposition 9 (separation from the elementary kernel test).** The tensor `S` satisfies `A(S)e_0^{tensor 7}=0`, but has complex exterior rank `2184`. Hence it violates the matching-layer bound `2182`.

**Proof.** In the column indexed by `0^7`, a nonzero exterior coefficient would require a tensor entry whose seven colours are all nonzero. All such entries of `S` vanish. Thus that entire column is zero. Independently, `A(S)S=0` holds for every odd-order tensor. The vectors `S` and `e_0^{tensor 7}` are independent. Skew-symmetry in odd dimension therefore gives nullity at least `3`, or rank at most `2184`.

Delete rows and columns numbered `0,1,2` from `A(S)`. For the resulting `2184` by `2184` integer matrix, the certificate gives

$$
\mathrm{Pf}(B)=27\pmod{101},\qquad
\det(B)=22\pmod{101}.
$$

A C implementation computes the Pfaffian. A separate Python/FLINT construction and determinant computation verifies the determinant residue. Nonvanishing gives rank at least `2184`, proving equality. Theorem 4 and parity require rank at most `2182` for seven-site layer combinations. QED.

This also has a direct algebraic interpretation. The support restriction on `S` puts it in the ideal generated by the seven local vectors `e_(i,0)`. Thus it passes the condition that comes merely from having local linear factors somewhere in each term. The common quadratic source needed to generate all matching layers imposes an additional obstruction.

The example is a separation certificate, not a claim that this particular generated tensor has an independent physical application.

## 7. Reproduction and verification scope

From the repository root:

```sh
python3 computations/matching-tensor-exterior-2026-09-26/verify.py --extended
cc -O3 -std=c99 computations/matching-tensor-exterior-2026-09-26/seven_site.c -o /tmp/krenn-exterior-seven
/tmp/krenn-exterior-seven
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python computations/matching-tensor-exterior-2026-09-26/verify_seven_flint.py
```

The main Python verifier uses only the standard library. It reconstructs the five-site tensor and checks the listed principal minor using two exact algorithms. It also checks all pairs of monomer layers for deterministic samples at three, five, and seven sites. Sampled layer ranks are `2,3,4`; every exterior product is zero. The sampled full monomer-dimer exterior ranks at three and five sites are `24` and `240`, respectively. Together with the proved upper bounds, the five-site sample shows sharpness of that bound. The final command is an additional independent check that requires `python-flint`, available in the repository's virtual environment.

The samples check indexing, signs, and normalization. They are not the proof of the all-orders result. That proof is in Sections 3–4.

Machine-readable outputs:

* [Five-site certificate and sample checks](../computations/matching-tensor-exterior-2026-09-26/certificate.json).
* [Seven-site certificate](../computations/matching-tensor-exterior-2026-09-26/seven-site-certificate.json).
* [Independent seven-site determinant check](../computations/matching-tensor-exterior-2026-09-26/seven-site-flint-certificate.json).

## 8. Literature comparison and novelty assessment

1. **Double-dimer switching is established.** Aizenman, Laínz Valcázar, and Warzel, [*Pfaffian Correlation Functions of Planar Dimer Covers*](https://arxiv.org/abs/1609.02824), explicitly allow complex weights and prove switching relations on general graphs before using planarity for later consequences. Lemma 1's combinatorial proof belongs to this tradition. We should not claim that complex weights or nonplanarity make the switching step itself novel.

2. **The exact flattening construction is established.** The map here is `K_(1,...,1)` in Hauenstein–Oeding–Ottaviani–Sommese, Section 5.1, equation (6), [*Homotopy techniques for tensor decomposition and perfect identifiability*](https://arxiv.org/abs/1501.00090). Their Section 5.2 also treats recovery from flattening kernels. See also Landsberg and Ottaviani, [*Equations for secant varieties of Veronese and other varieties*](https://arxiv.org/abs/1111.4567). We do not claim to invent either this matrix or the general flattening method.

3. **Matchgate identities concern a different precise representation problem.** Cai and Gorenstein, [*Matchgates Revisited*](https://theoryofcomputing.org/articles/v010a007/v010a007.pdf), characterize planar deletion signatures; their nonplanar character theory uses Pfaffian data. The coloured fixed-site monomer-dimer tensors here should not be silently identified with those signatures or characters.

4. **Gaussian moment varieties are established.** Améndola, Faugère, and Sturmfels, [*Moment Varieties of Gaussian Mixtures*](https://arxiv.org/abs/1510.04654), study algebraic relations among Gaussian moments. Our full monomer-dimer tensor is the squarefree cross-moment tensor of a formal shifted Gaussian family, with one variable chosen at each site. The note gives equations on that selected tensor. Formal complex parameters are broader than a positive-semidefinite real Gaussian model.

The specific contribution established here is the chain

```
common monomer-count layers
    -> pairwise exterior vanishing
    -> generically independent common kernel
    -> universal closed rank condition
    -> explicit representation obstructions.
```

The limited literature review did not identify this exact all-odd layer-rank statement. That is not a novelty certificate. A targeted comparison with monomer-dimer bilinear identities, Gaussian moment equations, and multi-factor exterior flattenings remains necessary before claiming priority.

The result does show that the reflection argument can be separated from the GHZ hypotheses and used for a different target. It does not yet generalize the more specialized corrected-insertion/divisibility step of the Krenn–Gu argument.

A [follow-up note](matching-tensor-recovery-and-multiple-copies-2026-09-26.md) proves generic monomer-direction recovery at five and seven sites, extends the obstruction to arbitrary numbers of auxiliaries with one coupling direction, and gives an `r+1`-copy identity for `r` mean directions.
