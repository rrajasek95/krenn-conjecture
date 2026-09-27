# Single-output covariance recovery from a restricted exterior kernel

Research note, 2026-09-27. Written proofs and exact modular rank
certificates. Not Lean formalized or independently peer reviewed.
The Krenn–Gu manuscript is unchanged.

**Subsequent closure:** the [all-orders induction](single-cross-moment-all-orders-2026-09-27.md)
now proves this note's rank hypothesis at every odd order at least seven.
Thus the single-output source theorem holds at all those orders, while
the nine-site certificate below remains a concrete finite witness.

## 1. Main result

**Theorem 1 (one-output recovery at nine sites).** For nine sites of
local dimensions at least three, one generic complex Gaussian cross-
moment tensor determines the actual mean row and every cross-site
covariance block, up to the unavoidable transformations

$$
\mu_i\mapsto\lambda_i\mu_i,\qquad
R_{ij}\mapsto\lambda_i\lambda_jR_{ij},\qquad
\prod_i\lambda_i=1.
$$

The comparison includes exceptional alternative source representations.
A representative is rational in the observed tensor on suitable charts.
Within-site covariances remain unobservable.

This is a generic uniqueness theorem, with its remaining rank input
certified by a nonzero minor modulo `1009`. The supplied program checks
that rank input; it is not a full blind nine-site reconstruction program.
The mean-direction step is supplied by the analytic
[all-orders induction](mean-direction-recovery-all-orders-2026-09-27.md).

The main structural improvement is independent of the number nine.
It replaces the proposed reconstruction of the whole exterior kernel
by a rank condition on a subspace with only

$$
1+2n+4\binom n2+8\binom n3
$$

columns. The unrestricted exterior matrix has `3^n` columns. Once
this smaller rank condition holds, two linear correction systems recover
the covariance class directly, without completing the response space.

## 2. Notation and the rank criterion

Let `n=2m+1>=5` and first take `V_i=C^3`. Use the matching tensor

$$
T=G(L,R),\quad L=\sum_i l_i,\quad R=\sum_{i<j}R_{ij},\qquad
P_{n-2k}=\frac{L^{n-2k}}{(n-2k)!}\frac{R^k}{k!},
$$

with the same commutative site algebra as in the
[one-direction note](one-direction-source-reconstruction-2026-09-27.md).
Thus `T=sum_k P_(n-2k)`. The copy identity gives
`P_(n-2k) in ker A(T)` for every `k`.

The [mean-direction theorem](mean-direction-recovery-all-orders-2026-09-27.md)
now recovers the lines `C l_i` generically at every such order. Let
`F_s` be the intrinsic space of tensors having mean-line factors at
all but at most `s` sites. In local coordinates `l_i=x_i`, its basis
consists of words with at most `s` nonzero colours. In particular,

$$
d_3:=\dim F_3=1+2n+4\binom n2+8\binom n3.
$$

The terminal response `P_n` and the one-edge response `P_(n-2)` are
generically independent and always lie in `F_2`. The sufficient condition
is

$$
\ker A(T)\cap F_3=\mathrm{span}\{P_n,P_{n-2}\}. \tag{1}
$$

Equivalently, the observable restricted map `A(T)|_(F_3)` has rank
`d_3-2`. This is an observable test after the mean lines are recovered;
the response vectors on the right of (1) need not be supplied.

**Theorem 2 (generic rank criterion).** Fix an odd `n>=5`. Suppose
there exists a source with nonzero means and two independent terminal
and one-edge responses for which `rank(A(T)|_(F_3))=d_3-2`.
Then a generic source at that order has the following full single-output
fiber, modulo product-one site scalings:

* at five sites, exactly two sources, related by
  `R -> -R-L^2/3`, with the same actual mean;
* at every odd order at least seven, exactly one source, recoverable
  rationally on charts.

The other nondegeneracy conditions used below have already been proved
to hold on nonempty open sets at every odd order. Thus a witness for
(1) is the only order-dependent hypothesis left in this theorem.

## 3. The two invisible edge corrections

We recall the elementary edge decomposition, to make the use of (1)
explicit. Normalize the local mean representatives to `x_i`, and choose
outside spaces `U_i` of dimension two. The map

$$
\Phi(Q)=\frac{L^{n-2}}{(n-2)!}Q
$$

surjects from cross-site quadratics onto `F_2`. Its kernel is the direct
sum of the following two spaces:

$$
K_1=\left\{\sum_{i\ne j}v_{ij}x_j:
       v_{ij}\in U_i,\ \sum_{j\ne i}v_{ij}=0\right\}, \tag{2}
$$

$$
K_0=\left\{\sum_{i<j}d_{ij}x_ix_j:
                         \sum_{i<j}d_{ij}=0\right\}. \tag{3}
$$

Their dimensions are `2n(n-2)` and `binom(n,2)-1`. The surjectivity
and kernel follow by reading entries with two, one, and zero outside
factors, respectively.

Since (1) also gives the intersection with `F_2`,

$$
\{Q:A(T)\Phi(Q)=0\}
       =\mathbb C R+\mathbb C L^2+K_1+K_0. \tag{4}
$$

Write `M=L^(n-4)/(n-4)!`.

**Lemma 3 (generic detection of the one-outside correction).** At
every odd `n>=5`, the map

$$
K_1\longrightarrow F_3/F_2,\qquad D_1\longmapsto[MRD_1] \tag{5}
$$

is generically injective.

**Proof.** This is the outside-degree part of Lemma 4 in the
[one-direction span proof](one-direction-source-reconstruction-2026-09-27.md#4-two-projections-remove-both-edge-kernels).
For completeness, use the common witness
`R_0=sum_(i<j)(y_i y_j+z_i z_j)`.
On an outside triple `i,j,k`, the three-outside coefficient of `MR_0D_1`
is

$$
u_iR_{0,jk}+u_jR_{0,ik}+u_kR_{0,ij},\qquad
u_i=-(v_{ij}+v_{ik}).
$$

The entry with `y` at `i` and `z` at `j,k` reads the `y` component
of `u_i`; interchanging the colours reads its `z` component. The same
holds at the other sites. Hence every pair sum `v_ij+v_ik` is zero.
Three other sites are available at each `i`, so all `v_ij` are zero.
A nonzero maximal minor proves generic injectivity. QED.

**Lemma 4 (detection of the pure-mean correction).** Assume (1) and
that every outside block `R_ij|_(U_i tensor U_j)` is nonzero. If
`D_0 in K_0` and `MRD_0 in ker A(T)`, then `D_0=0`.

**Proof.** The tensor `MRD_0` belongs to `F_2`. By (1) it is a
combination of `P_n,P_(n-2)`. Compare its two-outside part on edge
`ij`. The outside block of `R_ij` is multiplied by the sum of `d_kl`
over edges disjoint from `ij`. These sums must be a common scalar `c`.

Set `s_i=sum_(j!=i)d_ij`. Since the total edge sum is zero, the
complement sum is `d_ij-s_i-s_j`, giving `d_ij=s_i+s_j+c`. Summing
over `j!=i` yields

$$
(n-3)s_i+\sum_k s_k+(n-1)c=0.
$$

All `s_i` are equal, and their sum is twice the zero total edge sum.
Thus all `s_i`, then `c`, then every `d_ij` vanish. QED.

## 4. Global uniqueness without reconstructing the whole kernel

**Proof of Theorem 2.** Work on the common nonempty open set where
the mean-direction theorem, (1), Lemma 3, nonzero outside blocks,
independence of the full response list, and a nonzero `n-1`-outside
component of `T` all hold. Such an intersection is nonempty because
the source parameter space is irreducible and each condition defines
a nonempty open set. For (1), the hypothesized rank witness supplies
the nonempty open set. The remaining conditions have all-orders
witnesses in this note and the cited span proof.

The alternative means must be nonzero and have the same local lines.
Use product-one site scalings to align an alternative mean row with a
common scalar multiple of `L`; this is possible over `C` by choosing
an `n`th root of the product of the alignment factors. This root is
used to compare representations, not as a step of the rational inverse.

Every alternative response is annihilated by the same observed `A(T)`.
Equation (4) therefore puts its quadratic in the form

$$
R'=aR+bL^2+D_1+D_0.
$$

If `a=0`, every alternative edge has at most one outside factor. An
odd matching uses at most `m` edges, so its whole output belongs to
`F_m`. This contradicts the observed nonzero component with `n-1=2m`
outside factors. Hence `a!=0`.

Rescaling the alternative quadratic and subtracting a mean square
preserves its response span and therefore preserves the fact that all
its responses are in `ker A(T)`. Reduce to `R'=R+D_1+D_0`.
The difference of the two-edge responses is

$$
\Delta=M\left(R(D_1+D_0)+\frac{(D_1+D_0)^2}{2}\right). \tag{6}
$$

It belongs to `ker A(T)`. It also belongs to `F_3`. By (1), it lies
in `F_2`. Its three-outside part is exactly that of `MRD_1`, so
Lemma 3 forces `D_1=0`. The remaining square term `MD_0^2/2` lies
in the terminal line and is already annihilated. Lemma 4 then forces
`D_0=0`.

Thus every alternative quadratic belongs to `aR+bL^2`, globally,
including exceptional alternatives and dependent alternative response
lists. No equality of the entire exterior kernel with a response
space was used.

Generate the response space from any recovered representative in this
class and expand the actual tensor in its independent responses. The
[calibration theorem](calibrated-source-reconstruction-all-orders-2026-09-27.md#4-one-calibrated-output-the-threshold-is-seven-sites)
then gives exactly two classes at five sites and one at odd orders at
least seven. The latter calibration is rational. Combined with rational
mean-line recovery and the linear construction below, this proves the
rationality assertion. QED.

## 5. Constructive correction systems

**Corollary 5 (linear recovery of a covariance representative).** Once
the mean lines and the observed tensor are given on the above open set,
a representative of `aR+bL^2` is obtained by linear algebra, without a
basis for the full exterior kernel.

**Proof and construction.** Solve `A(T)Phi(Q)=0`, and use (4) to
choose `Q_0` outside `C L^2+K_1+K_0`. Find `D_1 in K_1` and a
nuisance tensor `H in F_2` satisfying

$$
A(T)\left(MQ_0D_1+H\right)
       =-A(T)\left(MQ_0^2/2\right). \tag{7}
$$

This is linear. It is consistent because the correction removing the
actual `K_1` part of `Q_0` makes its two-edge response agree, modulo
`F_2`, with a response in the recovered covariance class. The square
of the correction lies in `F_2` and is absorbed by `H`.

If two solutions have different `D_1`, their difference gives a tensor
`MQ_0 delta D_1+delta H` in `ker A(T) cap F_3`. Equation (1) puts
that tensor in `F_2`. The outside-degree-three map for `Q_0` is a
nonzero scalar multiple of (5), so `delta D_1=0`. The nuisance `H`
may differ by the two-dimensional annihilated subspace of `F_2`.

Set `Q_1=Q_0+D_1`. Next find `D_0 in K_0` from

$$
A(T)(MQ_1D_0)=-A(T)(MQ_1^2/2). \tag{8}
$$

Again the discarded square lies in the terminal line. Consistency
comes from the source, and uniqueness is Lemma 4; the added mean-square
and pure-mean terms in `Q_1` do not affect that injectivity. Then
`Q_1+D_0` is the required representative. QED.

The subsequent [quadratic-size inverse](quadratic-size-source-inverse-2026-09-27.md)
implements (7)–(8) at seven and nine sites, with the local mean lines
supplied. It verifies every recovered tensor entry and aligns four
nine-site outputs with a shared covariance. Its observable rank
certificate checks smaller correction matrices directly, without
constructing the `F_3` matrix. A subsequent
[blind search](blind-source-search-and-local-conditioning-2026-09-27.md)
supplies the mean lines on examples and verifies complete seven- and
nine-site sources over the rationals; it has no global convergence
guarantee.

## 6. Exact rank witnesses and the nine-site corollary

The [program](../computations/matching-tensor-recovery-2026-09-26/three_outside_certificate.py)
uses means `l_i=(1,0,0)`, seed `271940`, and unrestricted three-by-three
cross blocks, all modulo `1009`. It builds only columns of `A(T)`
indexed by `F_3`, and records a full-rank square minor.

| Sites | `dim F_3` | Restricted rank | Minor residue | One-outside flow rank | Flow minor |
| --- | ---: | ---: | ---: | ---: | ---: |
| 5 | 131 | 129 | 973 | 30 | 8 |
| 7 | 379 | 377 | 429 | 70 | 374 |
| 9 | 835 | 833 | 964 | 126 | 108 |

The [certificate](../computations/matching-tensor-recovery-2026-09-26/three-outside-certificate.json)
includes all source blocks and selected row and column indices. The
program rebuilds every entry of each selected minor using a separate
alternating-symbol construction and checks its determinant. It also
checks the two universal null vectors, the flow map of Lemma 3, and
a nonzero top-outside entry. Matching enumeration checks representative
input entries against the recursive moment construction.

A nonzero modular minor proves that its characteristic-zero polynomial
is nonzero. The two independent universal null vectors give the matching
upper rank bound. Hence (1) holds generically at all three listed orders.
Run:

```sh
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python computations/matching-tensor-recovery-2026-09-26/three_outside_certificate.py
```

**Proof of Theorem 1.** The nine-site rank witness and Theorem 2 give
the assertion for local dimension three. For larger, possibly unequal
local dimensions, use overlapping three-coordinate views, with one or
two extra coordinates replacing coordinate `2` at a time. Each view
recovers its source up to product-one site scalings. A common nonzero
mean coordinate at every site aligns those scalings; single replacements
cover means and double replacements cover every covariance entry.
The finitely many projected generic conditions hold simultaneously on
a nonempty open set. This is the same projection argument as Corollary 9
of the earlier one-direction note, now applied at nine sites. QED.

The subsequent [all-orders proof](single-cross-moment-all-orders-2026-09-27.md)
establishes (1) by a two-site induction. It closes the generic
single-output identifiability question at every odd order at least seven.
The full kernel-completion equality is a stronger, unnecessary target;
this restricted map requires far fewer columns. Efficient implementation
and noise conditioning remain separate questions.

## 7. Structured probes and attribution

The companion [structured probes](../computations/matching-tensor-recovery-2026-09-26/single_kernel_probes.py)
and [saved data](../computations/matching-tensor-recovery-2026-09-26/single-kernel-probes.json)
record some unsuccessful witnesses as well as smaller useful tests.
For example, full cycle support gives completed full-kernel dimensions
four and five at five and seven sites, rather than the response
dimensions three and four. A path introduces much larger kernels.

Restricting the exterior map only to `F_2` can behave differently.
With means fixed to colour zero and outside covariances equal to
independent scalar multiples of the two-by-two identity on each edge,
the tested five-, seven-, and nine-site `F_2` kernels all have dimension
two. Giving every edge the *same* outside identity instead leaves
dimensions eight, seventeen, and thirty. These computations motivate
separating mean recovery, low-degree annihilation, and full-kernel
completion; they do not establish an all-orders rank claim.

The exterior flattening and kernel strategy are established tools of
Hauenstein–Oeding–Ottaviani–Sommese,
[*Homotopy techniques for tensor decomposition and perfect identifiability*](https://arxiv.org/abs/1501.00090),
Sections 5.1–5.2. This note uses the model-specific copy identity,
the previously proved edge-kernel decomposition, and Gaussian moment
calibration cited above. Its additional step is the observation that
the difference (6) has at most three outside factors. No new general
theory of Koszul flattenings or claim of literature priority is made.
