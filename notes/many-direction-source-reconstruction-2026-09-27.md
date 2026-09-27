# Source reconstruction with three or more mean directions

Research note, 2026-09-27. Written proofs and exact reconstruction certificates; no Lean formalization or claim of established publication priority. The Krenn–Gu manuscript is unchanged.

## 1. Result and scope

The [two-direction reconstruction theorem](two-direction-source-reconstruction-2026-09-26.md) identifies a generic matching source from its response span at every odd number of sites at least five. A feature of that proof is a circulation space: certain changes to the edges are invisible to the responses with one edge and must be detected using the next layer.

With three or more independent local mean directions, the circulation space disappears. A third direction isolates every edge coefficient directly. This yields a simpler reconstruction theorem, valid already at three sites.

The later [calibration theorem](calibrated-source-reconstruction-all-orders-2026-09-27.md)
uses the actual output values to remove the covariance class ambiguity at
every odd order covered here. It determines all observed mean rows and
cross-site blocks up to product-one site scalings.

Fix an odd integer `n >= 3` and an integer `r >= 3`. At each site let `V_i = C^(r+1)`. Use the commutative site algebra

$$
\mathcal A=\bigotimes_{i=1}^n(\mathbb C\oplus V_i),\qquad V_iV_i=0.
$$

Vectors at distinct sites multiply as tensor products, while two vectors at the same site multiply to zero. Let `E` be an `r`-dimensional subspace of `direct_sum_i V_i`, with basis `L_1,...,L_r`, and let `R = sum_(i<j) R_ij`, where `R_ij in V_i tensor V_j`.

For a multi-index `p=(p_1,...,p_r)` of odd total at most `n`, define

$$
P_p=\left(\prod_{s=1}^r\frac{L_s^{p_s}}{p_s!}\right)
\frac{R^{(n-|p|)/2}}{((n-|p|)/2)!},\qquad
W(E,R)=\mathrm{span}\{P_p\}.
$$

Define three dimensions:

$$
d=\sum_{\substack{k\le n\\k\ \mathrm{odd}}}\binom{k+r-1}{r-1},\qquad
u=\binom{n+r-1}{r-1},\qquad
h=\binom{2n+r-1}{r-1}.
$$

Here `d` counts all responses, `u` counts terminal responses with no edges, and `h` counts degree-`2n` monomials in the mean parameters.

**Theorem 1 (generic global reconstruction).** On a nonempty Zariski-open set of sources, `dim W(E,R)=d`, and the span `W(E,R)` determines `(E,R)` up to precisely:

1. A common basis change of `E`.
2. Nonzero site scalings `L_(s,i) -> lambda_i L_(s,i)`, `R_ij -> lambda_i lambda_j R_ij`.
3. `R -> aR+q`, where `a != 0` and `q` belongs to the image of `Sym^2 E` in the edge space.

Every other `r`-direction source with the same span is equivalent in this sense. The reconstruction uses tensor contractions, arithmetic, and linear algebra. Once `E` is recovered, the responses with one edge already determine the edge class; no quadratic correction equations are needed.

This is a theorem about a **span of output tensors**, not one tensor. Sufficiently many outputs with generic but unknown mean settings span `W`. It does not identify within-site covariances, guarantee statistical stability, or cover every degenerate source. The local dimension hypothesis here is `r+1`; the boundary case with local dimension exactly `r` is not asserted by this theorem.

The listed changes preserve `W`. Site scalings multiply each full-site tensor by `product_i lambda_i`. A mean-quadratic addition mixes the layers by binomial expansion, and scaling `R` rescales them. The following lemmas prove the converse.

## 2. Recovering the mean geometry

Write `L(t)=sum_s t_s L_s`. Its terminal products span

$$
U(E)=\mathrm{span}\left\{\bigotimes_i L_i(t):[t]\in\mathbb P^{r-1}\right\}.
$$

When all local maps `E -> V_i` are injective, these products form a degree-`n` Veronese variety: the image of the parameter space under all degree-`n` monomials. Its span has dimension `u`.

Given any observed basis `T_1,...,T_d` of `W`, flatten `T(z)=sum_j z_jT_j` across the first site. Expand its `2 by 2` minors as quadratics in `z`, and let `C_W` be their coefficient matrix, with columns indexed by `z_i z_j`, `i <= j`.

**Lemma 2 (terminal-space extraction).** Generically `dim ker C_W=h`. View a quadratic-kernel vector as a symmetric `d by d` matrix by placing its `(i,j)` coordinate in both symmetric positions, without a factor of two. The sum of these matrices' column spaces recovers `U(E)`. The product tensors in `W` are exactly the terminal Veronese variety.

**Proof.** The coordinate vector `z(t)` of each terminal product satisfies `z(t)z(t)^t in ker C_W`. These matrices span an `h`-dimensional space because their entries are all degree-`2n` mean monomials. Their images span `U(E)`.

For equality, choose local bases `x_(1,i),...,x_(r,i),z_i` and the common witness

$$
L_s=\sum_i x_{s,i},\qquad R_0=\sum_{i<j}z_i z_j. \tag{1}
$$

After identifying the local bases, `W(E,R_0)` has one coordinate for each symmetric count tensor with an even number of `z` factors. The matching coefficients `(2k-1)!!` are nonzero, so all `d` responses are independent.

Every quadratic monomial involving a coordinate with a positive number of `z` factors is a restricted first-site minor. Put a `z` first in that coordinate and a mean colour first in the other. A mean colour is available because `n` is odd. The two cross entries have odd `z` counts and vanish. The two column labels are distinct by parity.

For the remaining, purely mean coordinates, the ordinary symmetric flattening minors equate all products `v_alpha v_beta` with fixed total multi-index `alpha+beta`. Any two decompositions of that total into degree-`n` multi-indices are connected by exchanging one colour at a time between the two factors; each exchange is such a minor. Therefore the quadratic quotient has one coordinate per degree-`2n` monomial, exactly `h` coordinates. Equality at (1) proves generic equality by a nonzero rank minor.

On this open set, the quadratic kernel is exactly the span of `z(t)z(t)^t`. Summing its matrix images recovers `U`. Any first-site rank-one tensor with coordinate vector `v` has `vv^t` in this kernel, so `v` lies in `U`. A symmetric tensor whose first-site flattening has rank one is a pure power: invariance under swapping the first factor with each other factor forces the same line at every factor. Hence the only product tensors in `W` are the terminal products. QED.

**Lemma 3 (linear synchronization).** The recovered `U(E)` determines `E` up to its common basis change and site scalars, using linear algebra.

**Proof.** Contracting onto individual sites recovers the `r`-dimensional local spaces `E_i`. Contracting onto sites `1,i` recovers the `r(r+1)/2`-dimensional image of `Sym^2 E` in `E_1 tensor E_i`.

Choose bases of these local spaces. Its annihilator is a space of bilinear-form matrices `A`. An unknown synchronization matrix `B:E_1 -> E_i` must satisfy

$$
x^tABx=0\quad\text{for all }x\text{ and all such }A.
$$

These are linear equations in the entries of `B`: the symmetric part of `AB` must vanish. In true synchronized coordinates the condition says `x tensor Bx` is symmetric for every `x`. Thus `Bx` is proportional to `x` for every `x`, forcing `B` to be a scalar matrix. In arbitrary coordinates, the solution space is consequently one-dimensional and its nonzero matrices are invertible. It recovers the synchronization up to a site scalar. QED.

An alternative source with the same `d`-dimensional response span must also have injective local mean maps. Otherwise a nonzero parameter vector killed at a site gives a nonzero pure power in the kernel of its terminal coefficient map, making its `u` terminal responses dependent and its full response dimension less than `d`. Its terminal Veronese variety therefore has dimension `r-1`; being contained in the product variety of Lemma 2, it equals that variety. Lemma 3 aligns its mean space with the original one.

## 3. Why a third direction removes the cycle ambiguity

For an arbitrary edge tensor `Q`, define

$$
\Phi_E(Q;t)=\frac{L(t)^{n-2}}{(n-2)!}Q.
$$

This records all responses containing exactly one edge of `Q`.

**Lemma 4 (edge isolation).** Suppose `r >= 3` and every local mean map is injective. Then `Q -> Phi_E(Q;t)` is injective. This assertion does not require generic edge weights or odd `n`.

**Proof.** Complete the local mean vectors to local bases, so the same mean labels `1,...,r` are available at all sites. Fix an edge `ij` and two endpoint basis labels `a,b`. Choose a mean label `c` different from both `a,b`; three mean directions suffice. Evaluate `t` at the `c`th coordinate vector, and extract the tensor coefficient having colours `a,b` at sites `i,j` and colour `c` at every other site.

The two non-`c` sites must both be occupied by the sole edge. Hence the only contributing edge is `ij`, and the extracted coefficient is exactly `Q_ij(a,b)`. Every edge coefficient is recovered in this way. QED.

The same extraction fails for two mean directions when the two endpoint colours exhaust them. The circulation kernel in the earlier note is exactly the resulting residual ambiguity.

Let

$$
S(E,W)=\{Q:\text{all coefficients of }\Phi_E(Q;t)\text{ lie in }W\}.
$$

**Lemma 5 (complete edge ambiguity).** Generically,

$$
S(E,W)=\mathbb C R+\mathrm{Sym}^2 E,
\qquad \dim S(E,W)=1+\frac{r(r+1)}2. \tag{2}
$$

**Proof.** The right side always lies in `S`. At witness (1), split `Q` into terms with zero, one, or two `z` factors. Its one-`z` part must have zero image, because `W` has no odd `z` count; Lemma 4 makes this part zero. Its two-`z` part must have equal coefficients at every pair of `z` sites, because its image is symmetric, so it is a scalar multiple of `R_0`.

The zero-`z` part has symmetric image. Average it over all site permutations. The average belongs to `Sym^2 E`, and its image agrees with the original image. Their difference is zero by Lemma 4. Thus (2) holds at (1). A maximal nonzero constraint minor proves equality on a nonempty open set. QED.

**Proof of Theorem 1.** Lemmas 2–3 recover and align the mean spaces of all alternative representations of the same response span. Any alternative edge tensor lies in `S(E,W)`, so Lemma 5 gives `R'=aR+q`. If `a=0`, every response of the alternative source is a terminal mean tensor. Its span would have dimension at most `u<d`, a contradiction. Therefore `a != 0`, as required. All rank conditions hold at the same witness (1), so the common generic set is nonempty. QED.

**Corollary 6 (direct reconstruction).** After recovering `E`, solve the linear membership equations defining `S(E,W)`, compute its known subspace `Sym^2 E`, and choose any vector outside that subspace. The chosen vector is an edge representative of the correct equivalence class.

**Corollary 7 (larger, unequal local spaces).** Theorem 1 remains valid when the local dimensions are arbitrary integers at least `r+1`, and may differ between sites.

**Proof.** Place witness (1) inside an `(r+1)`-dimensional subspace at every site. The terminal and quadratic ranks are unchanged. Any additional edge coefficient has an endpoint outside one of these subspaces. The extraction in Lemma 4 isolates it in an output coordinate outside the witness's tensor support. Membership in the witness response span therefore forces that coefficient to vanish. Thus the first-edge solution space at the witness still has exactly the dimension in (2), and the same rank-open argument applies to the larger parameter space. QED.

## 4. Exact blind reconstructions

The implementation [many_direction.py](../computations/matching-tensor-recovery-2026-09-26/many_direction.py) takes the observed output tensors into the reconstruction routines without their generating source or parameter labels. Source parameters are used only to generate the inputs and independently compare the recovered answer. The [saved certificate](../computations/matching-tensor-recovery-2026-09-26/many-direction-certificate.json) contains all source parameters, recovered representatives, selected nonzero minors, and explicit equivalence transformations.

Run from the repository root:

```sh
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python computations/matching-tensor-recovery-2026-09-26/many_direction.py
```

The script uses `python-flint`, seed `270927`, and modulus `1009`. It prints JSON and writes no files. Input mean settings are `t_s=j^((n+1)^(s-1))`, with `j=1,...,d`; their evaluation matrices are invertible in the recorded cases.

| Sites `n` | Directions `r` | Local dimension | Response dimension `d` | Terminal dimension `u` | Quadratic rank | Quadratic nullity `h` | Edge parameters | Edge ambiguity dimension |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 3 | 3 | 4 | 13 | 10 | 63 | 28 | 48 | 7 |
| 3 | 4 | 5 | 24 | 20 | 216 | 84 | 75 | 11 |
| 5 | 3 | 4 | 34 | 21 | 529 | 66 | 160 | 7 |

The selected quadratic coefficient minors are `926`, `866`, and `212`, respectively. The selected edge-constraint minors are `243`, `76`, and `584`. In all three cases the raw one-edge map has full column rank, the recovered source generates exactly the observed span, and an independent comparison finds only the proved basis, site, scaling, and mean-quadratic changes.

These are exact checks of the implemented reconstruction. The proof for all stated `n,r` is the analytic argument above, not an extrapolation from this table.

## 5. Relation to earlier work and remaining boundaries

Veronese equations and reconstruction from tensor kernels are established algebraic tools. Pucci's *The Veronese Variety and Catalecticant Matrices*, J. Algebra 202 (1998), 72–95, concerns the determinantal description. Bernardi's [*Ideals of varieties parameterized by certain symmetric tensors*](https://arxiv.org/abs/0705.1942) reviews that description and develops its Segre–Veronese extension. Lemma 2 includes the short monomial-exchange argument needed here, without claiming a new Veronese ideal theorem.

There is also a closer Gaussian precedent than just the existence of moment varieties: Remark 22 of Améndola–Ranestad–Sturmfels, [*Algebraic Identifiability of Gaussian Mixtures*](https://arxiv.org/html/1612.01129v2#S4), identifies fixed-covariance Gaussian moment varieties with Veronese varieties after a linear coordinate change. That result concerns the full moment vector through a specified order. Here the data are the span of one cross-site moment tensor as an unknown mean varies in a common linear subspace; cross-site covariance is unknown and is recovered modulo the span-preserving transformations. This is a difference in observed model, not a claim that Gaussian–Veronese geometry is new.

The response hierarchy came from the Krenn–Gu investigation, but the reconstruction proof itself does not invoke the multiple-copy vanishing theorem. It uses the resulting matching-source model, classical tensor geometry, and the model-specific edge isolation and ambiguity classification. A full priority review of this precise inverse problem remains outstanding.

The [support-graph extension](sparse-source-graph-reconstruction-2026-09-27.md) now treats generic connected support graphs without a perfect matching, including even orders. It also identifies a sparse graph and removes the mean-quadratic ambiguity without being told which edge is missing. Incomplete output spans and one mean direction remain open here. The two-direction case has a different mechanism and is treated generically for odd `n >= 5` in the preceding note. These notes do not establish stability under measurement noise.

## 6. Exact results with no extra local coordinate

**Corollary 8 (two minimal local formats).** With three mean directions and three-dimensional local spaces, generic reconstruction modulo the transformations of Theorem 1 holds at `n=3` and at `n=5`.

**Proof.** The terminal extraction, synchronization, edge-isolation, and global comparison arguments above only require local injectivity and the two stated rank conditions. The extra local coordinate supplied the all-orders witness; it was not used in the reconstruction argument itself. For these two formats, the [exact certificate](../computations/matching-tensor-recovery-2026-09-26/no-extra-coordinate-certificate.json) supplies alternative witnesses. At three sites the quadratic coefficient rank is `63` and the edge-constraint rank is `20` out of `27` edge parameters. At five sites these ranks are `529` and `83` out of `90`. Thus the quadratic kernels have the required dimensions `28` and `66`, and the edge ambiguity has dimension `7` in both cases. The selected nonzero quadratic minors are `91,866`; the edge minors are `963,873`, modulo `1009`. Clearing the rational chart denominators gives nonzero characteristic-zero polynomial minors, proving a nonempty open set in each format. The global comparison proof then applies. QED.

These are fixed-format generic results, not a proof that the extra coordinate can be removed at every order. Reproduce both blind reconstructions with:

```sh
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python computations/matching-tensor-recovery-2026-09-26/many_direction.py --minimal-local
```
