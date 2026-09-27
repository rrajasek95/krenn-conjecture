# Shared edge and mean-space recovery with visible data noise

Research note, 2026-09-27. Conditional theorems, an exact four-observation
certificate, and a computational audit. Not Lean formalized or independently
peer reviewed. The Krenn–Gu paper is unchanged.

## 1. Result and scope

The [composed single-source bounds](composed-source-error-bounds-2026-09-27.md)
now work through changes of candidate coordinates, shared-covariance
alignment, and the joint correction theorem. Four seven-site tensors
recover a common covariance and a rank-four space of observed global
mean vectors. Every one of their 8,748 noisy entries differs from its
clean value in binary64, and every noisy entry is exactly representable
in binary64.

The resulting joint source-error bound is `1.719e-11`. The sine of the
largest principal angle between the recovered and true observed mean
spaces is at most `5.508e-11`. These bounds hold for **every** compatible
shared source in the common gauge, including complex alternatives.
Existence of such a source is a premise of this interpretation. The
test separately checks existence; acceptance alone is not a test for
the shared-source model.

The contribution is the quantitative integration and its exact example.
The underlying conditional theorems are consequences of the existing
[shared-source alignment](certified-shared-source-alignment-2026-09-27.md)
and [composed inverse](composed-source-error-bounds-2026-09-27.md).
The matching formula for alignment was already proved in
[Corollary 9 of the source theorem](single-cross-moment-all-orders-2026-09-27.md).
No new general identifiability theorem or new interval-arithmetic method
is claimed here.

Noise remains small and the certificate is point-dependent. This does
not establish experimental-noise robustness, uniform stability, or a
validated floating-point correction iteration. It uses all tensor entries.

The subsequent [output-validation note](validated-source-correction-2026-09-27.md)
now certifies the exact stored values of three numerical correction outputs.
It bounds the selected binary64 output's distance to the exact fixed point
by `4.29e-16`, without assuming that the floating trajectory is exact.

## 2. What is shared, and what is recovered

There are `n=2m+1>=7` sites and `p` observations. Observation `s` has
means `mu_i^(s) in C^3`; the matrices `R_ij in C^(3 by 3)` are common
to every observation. The matching tensor is

$$
\mathcal F_s(\mu^{(s)},R)_a
=\sum_M\prod_{\{i,j\}\in M}(R_{ij})_{a_i a_j}
             \prod_{i\notin V(M)}(\mu_i^{(s)})_{a_i}.
$$

Here `a` is a word in `{0,1,2}^n`, `M` ranges over sets of edges with
disjoint endpoints, and `V(M)` is their set of endpoints. Each observation
`Y_s` has a supplied Euclidean error bound `epsilon_s`.
Source norms concatenate mean entries and one copy of each edge entry.
Edge-matrix norms are Frobenius norms; linear-map norms are spectral norms.

For each observation, site scalings preserve its tensor when their
product is one:

$$
\mu_i^{(s)}\longmapsto\gamma_i\mu_i^{(s)},\qquad
R_{ij}\longmapsto\gamma_i\gamma_jR_{ij},\qquad
\prod_i\gamma_i=1.
$$

Recovering observations separately chooses different scalings. Alignment
uses the common edges to put all recovered means into the first
observation's convention. In that convention, concatenate the local means
into `v_s in C^(3n)` and form the matrix `V=[v_0 ... v_(p-1)]`.
The recovered mean space is its column space. It is a space of global
mean vectors in a direct sum, not a local subspace at one site and not
the span of tensor products of means. Its rank can exceed three.
Unobserved latent mean directions are not inferred.

## 3. Transferring the sharper certificate through candidate coordinates

The composed initializer takes a candidate whose means are all `e_0`.
For an arbitrary candidate mean `u_i=(a_i,b_i,c_i)` with `a_i!=0`, set

$$
K_i=\begin{pmatrix}a_i&0&0\\b_i&1&0\\c_i&0&1\end{pmatrix}.
$$

It maps `e_0` to the candidate mean. Apply `K_i^(-1)` to each local
tensor factor and replace the candidate edge by
`K_i^(-1) C_ij K_j^(-t)`. The superscript `t` is ordinary transpose;
this is a change of tensor coordinates, not a Hermitian covariance
transformation. All changes depend only on the candidate.

**Lemma 1 (coordinate-transfer bounds).** Suppose certified norm bounds
are `a_i^->=||K_i^(-1)||` and `a_i^+>=||K_i||`. The transformed data
budget is at most

$$
\epsilon_s'=\epsilon_s\prod_i a_i^-.
$$

If the composed initializer proves a global transformed source bound
`E_s'`, then in the original coordinates valid bounds are

$$
e_{\mu,s}=\max_i a_i^+ E_s',\qquad
e_{R,s}=\max_{i<j}(a_i^+a_j^+)E_s'.                         \tag{1}
$$

They apply to every compatible source after a product-one scaling.
For each site except the last, its first mean coordinate then equals
the corresponding candidate coordinate `a_i`.

**Proof.** Tensor product and pairwise operator norms give the data and
edge bounds; the direct sum of the local maps gives the mean bound.
The first coordinate of `K_i^(-1)mu_i` is `(mu_i)_0/a_i`, so the
unit-mean chart's gauge fixes exactly the stated original coordinate.
Scalar site rescalings commute with these linear coordinate changes.
Thus both the global quantifier and the product-one gauge transfer.
QED.

The implementation bounds each matrix norm by the square root of its
maximum absolute row sum times its maximum absolute column sum.
Numerical square roots are replaced by rational upper bounds.
The certificate of [Theorem 7 of the composed-error note](composed-source-error-bounds-2026-09-27.md)
is then replayed in the transformed coordinates. No transformed error
is silently reused in the original norm.

## 4. Alignment and a joint error theorem

Write `(u_s,C_s)` for a compatible source in its individual gauge,
and `(u_hat_s,C_hat_s)` for the candidate. Lemma 1 bounds their mean
and edge differences by `e_mu,s` and `e_R,s`. Shared-source existence
gives true alignment factors `lambda_s,i` satisfying

$$
\lambda_{s,i}\lambda_{s,j}(C_s)_{ij}=(C_0)_{ij},\qquad
\prod_i\lambda_{s,i}=1.                                    \tag{2}
$$

Choose one coordinate of each useful reference edge with magnitude
strictly larger than `e_R,0`. Divide its candidate-coordinate discs to
bound `q_s,ij=(C_s)_ij/(C_0)_ij` at that coordinate. If a perfect
matching `M_i` covers every site except `i`, then

$$
\lambda_{s,i}=\prod_{jk\in M_i}q_{s,jk}.                   \tag{3}
$$

The equality follows because every vertex except `i` occurs once in
the product and the alignment factors have product one. All divisions
require their denominator discs to exclude zero. Multiplying discs
gives `|lambda_s,i-l_s,i|<=r_s,i`, where `l_s,i` and `r_s,i` denote
the computed center and radius. These are the exact formulas of the
earlier alignment theorem, including their finite-error bounds.

Define `v_hat_s=(l_s,i u_hat_s,i)_i`, with `v_hat_0=u_hat_0`, and put

$$
\begin{aligned}
E_0&=e_{\mu,0},\\
E_s&=\max_i(|l_{s,i}|+r_{s,i})e_{\mu,s}
       +\sqrt{\sum_i r_{s,i}^2\|\widehat u_{s,i}\|^2}quad(s>0),\\
E_{\rm out}&=\sqrt{e_{R,0}^2+\sum_s E_s^2}.                \tag{4}
\end{aligned}
$$

The common candidate covariance is `C_hat_0`. Let `Theta_hat` list
it and all aligned candidate means. In the joint mean gauge, only the
first observation has fixed first mean coordinates at sites `i<n-1`;
all later means are free. The joint forward map stacks the `p` tensors,
and its derivative at the candidate is `J`.

Certify that `J` has full column rank, `||J^dagger||<=g`, and that the
Hessian norm is at most `L` on the unit source ball. Let

$$
r=\min\{1,(2gL)^{-1}\},\quad
\epsilon=\sqrt{\sum_s\epsilon_s^2},\quad
\rho\ge\|\mathcal F(\widehat\Theta)-Y\|.                  \tag{5}
$$

**Theorem 2 (shared recovery with composed input bounds).** Suppose
each transformed single-source certificate passes, all alignment
denominators and complementary matchings are certified, `E_out<r`,
and `g rho<=r/2`. Every compatible shared source, in the first
observation's gauge, satisfies

$$
\|\Theta-\widehat\Theta\|\le E_*:=2g(\epsilon+\rho).        \tag{6}
$$

The exact-arithmetic iteration
`Theta_(k+1)=Theta_k+J^dagger(Y-F(Theta_k))` converges throughout the
closed radius-`r` ball to a unique fixed point `Theta_infty`, with

$$
\|\Theta_\infty-\Theta\|\le2g\epsilon.                    \tag{7}
$$

**Proof.** Lemma 1 supplies global input enclosures. Equations (2)–(4)
and the alignment theorem place every compatible shared representative
inside the ball, without assuming closeness beforehand. Derivative
variation there is at most `Lr<=1/(2g)`. Applying `J^dagger` to the
integrated forward difference gives the lower Lipschitz bound underlying
(6). The iteration derivative has norm at most one half; its center
displacement is at most `g rho`. It is therefore a contraction of the
ball into itself. Comparing its fixed point with a compatible source
gives (7). This is the earlier joint theorem with sharper input bounds,
so no change to its proof is required. QED.

The program uses the stronger `E_out<r/2`. The common covariance alone
and the collection of all means each have error at most `E_*`, because
each is a subvector of the joint source. The fixed point solves the
projected equations; it need not minimize the full tensor residual.

## 5. The recovered mean space

Let `V_hat` have the aligned candidate mean columns. Certify full column
rank and choose

$$
0<\sigma_0\le\sigma_{\min}(\widehat V),\qquad
\sigma_0=\frac1{\sqrt{\mathrm{tr}((\widehat V^*\widehat V)^{-1})}}
\quad\hbox{before downward rounding}.                       \tag{8}
$$

The asterisk denotes conjugate transpose. Gram inversion is exact for
the rational candidate; an upper square-root bound in the denominator
produces a valid rational lower bound.

**Corollary 3 (observed rank and angle).** If `E_*<sigma_0`, every
compatible shared source has observed mean rank `p`. If `P` and
`P_hat` are the orthogonal projections onto its mean space and the
candidate mean space, respectively, then

$$
\|(I-P)P_{\widehat V}\|\le E_*/\sigma_0.                  \tag{9}
$$

**Proof.** The Frobenius norm of `V-V_hat` is at most `E_*`. Hence
`sigma_min(V)>=sigma_0-E_*>0`. For an orthonormal basis `Q_hat` of
the candidate space, write `Q_hat=V_hat B` with `||B||<=1/sigma_0`.
Then `(I-P)Q_hat=(I-P)(V_hat-V)B`, proving (9). The same argument
also bounds its Frobenius norm by `E_*/sigma_0`, as used in the audit.
QED.

This is a standard singular-subspace perturbation estimate. For the
classical general setting, see P.-Å. Wedin, *Perturbation bounds in
connection with singular value decomposition*, BIT **12** (1972),
99–111 ([publisher page](https://link.springer.com/article/10.1007/BF01932678)).
Verified preconditioning and derivative enclosures likewise use established
methods; see S. M. Rump, *Verification methods*, Acta Numerica **19**
(2010), 287–449 ([corrected author text](https://www.tuhh.de/ti3/paper/rump/Ru10.pdf)).
The proofs above make the specific estimates used here explicit.

## 6. The four-observation certificate

All observations share the seven-site covariance of the earlier
initializer. Observation zero has all means `e_0`. For `s=1,2,3`, double
the zero-coordinate mean at site `s-1`, starting from means `e_0`.
In observation one, add `1/16` to coordinate one at every site. In
observation two, add `1/16` to coordinate two at every site. In
observation three, at site `i`, add `(i mod 3-1)/16` and
`(2(i mod 2)-1)/16` to coordinates one and two. These are example-generation
parameters, not inputs to the numerical proposal.

Independent random signs perturb every entry. The proposal receives
only the raw noisy tensor and returns candidate means and edges by
floating arithmetic and rational approximation. Its error is then
certified. Archived certificates provide untrusted matrix proposals;
all required products, ranks, and inequalities are checked anew.

| Observation | Entrywise noise magnitude | Supplied tensor budget |
| --- | ---: | ---: |
| 0 | `2^-46` | `47/2^46`, about `6.67910e-13` |
| 1 | `2^-46` | `47/2^46`, about `6.67910e-13` |
| 2 | `2^-48` | `47/2^48`, about `1.66978e-13` |
| 3 | `2^-49` | `47/2^49`, about `8.34888e-14` |

There are 2,187 entries per tensor and `sqrt(2187)<47`. Noise signs
use seed `275346` for observation zero and `275400+s` for the other
observations. All noisy entries are exactly binary64-representable,
and every noisy value differs from its clean value in binary64.
The certificate does not impose a denominator bound on compatible sources.

| Joint quantity | Approximate value |
| --- | ---: |
| Free source parameters | 267 |
| Free mean parameters | 78 |
| Shared edge parameters | 189 |
| Global aligned source enclosure `E_out` | `1.18562e-9` |
| Certified joint inverse derivative norm bound `g` | `4.47345` |
| Joint correction radius `r` | `5.47740e-7` |
| Stacked noise budget `epsilon` | `9.62840e-13` |
| Joint forward residual bound `rho` | `9.58033e-13` |
| Final joint source error `E_*` | `1.71859e-11` |
| Exact-arithmetic correction error (7) | `8.61441e-12` |
| Candidate mean singular-value lower bound `sigma_0` | `0.312047666` |
| Observed mean rank | 4 |
| Principal-angle sine upper bound | `5.50744e-11` |

The table's decimals are descriptive; acceptance uses the stored rational
bounds. In particular, rounding a displayed radius is not an acceptance
test. The four-dimensional mean space lies in the 21-dimensional direct
sum of the seven local spaces.

The initial tests at `2^-46` entrywise noise rejected observations two
and three. Observation three also rejected `2^-48`: its outer enclosure
was about `1.55e-5`, just above half its individual correction radius
of about `3.00e-5`. These are failures of sufficient tests. The saved
joint certificate retains tests at one, two, four, and eight times each
accepted observation's candidate-centered tensor radius in its unit chart:

| Observation | Multipliers passing the individual half-ball test |
| --- | --- |
| 1 | 1, 2 |
| 2 | 1 |
| 3 | 1 |

All failures and bounds are retained, including propagation failures if
any occur. No optimal threshold or information-theoretic impossibility
is inferred from them.

## 7. Exact replay and a distinct compatible source

Run from the repository root using the existing NumPy, SciPy, SymPy,
and python-flint research environment:

```sh
OPENBLAS_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 .venv/bin/python \
  computations/matching-tensor-recovery-2026-09-26/verify_composed_shared_source_noise.py
```

The replay checks the hashes and exact acceptance of all four inputs,
with numerical proposal functions disabled. It separately constructs
clean tensors, exterior columns, the individual full-source and mean
compression Jacobians, their point curvature, and every joint derivative
entry. It independently enumerates the joint curvature bound, replays
alignment and radius tests, and rejects zero-containing alignment
denominators. A separate symbolic calculation makes 3,360 exact value,
gradient, and Hessian comparisons for the calibration formulas.

The audit also constructs a **different** shared source by perturbing
every free mean coordinate and every common edge entry by a signed
`2^-62`. Exact matching evaluation verifies that it fits all four noisy
observations within their budgets. Its joint parameter error is about
`3.54e-18`, and the Frobenius norm of its principal-angle sines is about
`2.84e-18`. Rational orthogonal projectors verify that this latter error
is nonzero and below (9). This tests the full sequence of bounds on an
actual compatible model, rather than only checking the planted center.
It is a test, not a proof of the universally quantified theorem.

The artifacts are:

- [Joint certificate](../computations/matching-tensor-recovery-2026-09-26/composed-shared-source-certificate.json)
  and [audit](../computations/matching-tensor-recovery-2026-09-26/composed-shared-source-audit.json).
- [Observation zero](../computations/matching-tensor-recovery-2026-09-26/composed-source-noise-certificate.json),
  [one](../computations/matching-tensor-recovery-2026-09-26/composed-shared-observation-1.json),
  [two](../computations/matching-tensor-recovery-2026-09-26/composed-shared-observation-2.json),
  and [three](../computations/matching-tensor-recovery-2026-09-26/composed-shared-observation-3.json).
- [Generator and coordinate wrapper](../computations/matching-tensor-recovery-2026-09-26/composed_shared_source_noise.py)
  and [replay](../computations/matching-tensor-recovery-2026-09-26/verify_composed_shared_source_noise.py).

To regenerate the new observations, choose an output directory and run
the generator with `--observation 1 --noise-bits 46`,
`--observation 2 --noise-bits 48`, and
`--observation 3 --noise-bits 49`, each with
`--output-dir /path/to/output`. Then run it with only that output-directory
argument and redirect stdout to the joint certificate. Observation zero
is the separately published composed single-source certificate.

The replay shares the inequality code and exact arithmetic libraries
with the generator. It is a computational audit with separate
constructions, not an independent mathematical review. Floating-point
proposal and exact acceptance remain distinct. The main paper and its
Lean formalization are unchanged.

## 8. Remaining work

The arbitrary-candidate coordinate wrapper and shared-source integration
are now tested at visible noise. A later
[a posteriori certificate](validated-source-correction-2026-09-27.md)
also validates a numerical correction output on this example. What remains
includes useful larger noise budgets, guarantees for general floating-point
trajectories, compressed measurements, and classification of nongeneric sources.
The [known near-ambiguity families](shared-calibration-and-near-ambiguity-2026-09-27.md)
still rule out uniform stability without additional restrictions. The
[sparse complex alignment ambiguity](certified-shared-source-alignment-2026-09-27.md)
also remains relevant when the certified covariance graph does not
support unique alignment. None of these boundaries is removed by this
complete-graph example.
