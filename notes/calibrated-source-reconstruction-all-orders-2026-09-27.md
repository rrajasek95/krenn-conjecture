# Calibrating shared Gaussian sources at every odd order

Research note, 2026-09-27. Written proofs and exact algebraic checks;
not Lean formalized or independently peer reviewed. The Krenn–Gu paper
is unchanged. This note strengthens the existing reconstruction results
by retaining the coefficients of the observed tensors, in addition to
their linear span.

## 1. All-orders recovery from a spanning family

Let `n=2m+1` be odd. A source has an `r`-dimensional mean space
`E subset direct_sum_i V_i` and shared cross-site blocks
`R=sum_(i<k)R_ik`. Its output with mean row `mu` is

$$
G(\mu,R)=[\exp(\mu+R)]_{\mathrm{full}},
$$

in the commutative site algebra `tensor_i(C direct_sum V_i)` with
`V_i V_i=0`. The subscript selects terms using every site once. Thus
`G` sums matchings, with a mean vector at each unmatched site and a
covariance block at each matched pair. For real Gaussian site vectors it
is their full cross-moment tensor.

Choose a mean basis `L_1,...,L_r`. For a multi-index `p` of odd total at
most `n`, write

$$
P_p(E,R)=\left(\prod_s\frac{L_s^{p_s}}{p_s!}\right)
\frac{R^{(n-|p|)/2}}{((n-|p|)/2)!},\qquad
W(E,R)=\mathrm{span}\{P_p(E,R)\},
$$

and let

$$
d=\sum_{\substack{k\le n\\k\ \mathrm{odd}}}\binom{k+r-1}{r-1}.
$$

**Theorem 1 (calibrated all-orders reconstruction).** Assume one of:

* `r=1`, odd `n>=5`, and every local dimension is at least three;
* `r=2`, odd `n>=5`, and every local dimension is at least three; or
* `r>=3`, odd `n>=3`, and every local dimension is at least `r+1`.

For a generic source, any labelled family of actual outputs
`T_j=G(mu_j,R)` spanning its `d`-dimensional response space determines
every actual mean row `mu_j` and every cross-site block, up to exactly

$$
\mu_{j,i}\longmapsto\lambda_i\mu_{j,i},\qquad
R_{ik}\longmapsto\lambda_i\lambda_k R_{ik},\qquad
\lambda_i\ne0,\quad\prod_i\lambda_i=1. \tag{1}
$$

The comparison includes every alternative shared-covariance model whose
mean rows span at most `r` directions. Local independence of an alternative
source is not assumed. A representative can be reconstructed by rational
operations and linear algebra.

The mean settings are unknown; the vectors `T_j` and their scales are
observed. No lower-order moments are supplied. Generic `d` settings
suffice to span `W`. The theorem makes no claim about alternatives with
more than `r` mean directions, noisy estimation, or within-site covariance
blocks, which never occur in these data.

The
[one-direction theorem](one-direction-source-reconstruction-2026-09-27.md),
[two-direction theorem](two-direction-source-reconstruction-2026-09-26.md)
and [many-direction theorem](many-direction-source-reconstruction-2026-09-27.md)
recover `E` and the covariance class

$$
R'=aQ+q(H),\qquad a\ne0,\quad H=H^t,\qquad
q(H)=\frac12\sum_{s,t=1}^r H_{st}L_sL_t, \tag{2}
$$

where `Q` is a reconstructed representative. They also allow arbitrary
site scalings because only the span is used. The new step is to use the
actual tensor coefficients to determine the free scale and mean-quadratic
correction in (2), leaving just (1).

## 2. What the response coordinates measure

Fix the recovered frame `L_s` and representative `Q`. Expand an actual
output uniquely as

$$
T=\sum_p c_pP_p(E,Q),\qquad z=(c_{e_1},...,c_{e_r}),
$$

where `e_s` is the `s`th unit multi-index. Define polynomials in an
auxiliary variable vector `x=(x_1,...,x_r)` by

$$
F_k(x)=\sum_{|p|=k}\binom{k}{p}c_px^p\quad(k\le n\text{ odd}),
\qquad Z(x)=z\cdot x=F_1(x).
$$

These are response-coordinate polynomials extracted from the same
order-`n` tensor. They are **not additional measurements of lower-order
moments**.

The site scalings used to align an alternative mean space with `E` may be
chosen with product one: multiply them all by a common scalar and absorb
that scalar into the mean basis. In this alignment write its actual mean
as `L(t)=sum_s t_sL_s` and its quadratic as (2). Set

$$
z=a^m t,\qquad \beta=a^{-n},\qquad K=H/a,\qquad Q_K(x)=x^tKx. \tag{3}
$$

**Lemma 2 (coordinate identities).** The odd response polynomials obey

$$
\begin{aligned}
F_3&=\beta Z^3+3ZQ_K,\\
F_5&=\beta^2Z^5+10\beta Z^3Q_K+15ZQ_K^2,\\
F_7&=\beta^3Z^7+21\beta^2Z^5Q_K
                 +105\beta Z^3Q_K^2+105ZQ_K^3,
\end{aligned} \tag{4}
$$

whenever the indicated degree is at most `n`.

**Proof.** Expand `exp(L(t)+aQ+q(H))` in powers of `Q`. The coefficient
of the response degree `2k+1` is `a^(m-k)` times the ordinary Gaussian
moment polynomial of that degree in `t,H`. A term with `ell` pairings
has coefficient

$$
\frac{(2k+1)!}{2^\ell\ell!(2k+1-2\ell)!}.
$$

Substitute `t=a^-m z` and `H=aK`. Its remaining power of `a` is
`-n(k-ell)`, giving `beta^(k-ell)`. For `k=1,2,3` this is (4). QED.

For any two nonzero output coordinate vectors `z_1,z_2`, the cubic
identities form a linear system for `beta` and the `r(r+1)/2` entries of
the common symmetric matrix `K`.

**Lemma 3 (two-output calibration).** This system has a unique solution
whenever `z_1z_1^t != z_2z_2^t`.

**Proof.** Subtract two possible solutions and divide their cubic
identities by the nonzero polynomial `Z_j`. For both `j` this gives
`delta K=-(delta beta/3)z_jz_j^t`. The hypothesis forces
`delta beta=0`, then `delta K=0`. Existence is supplied by the source.
QED.

Independent `z_1,z_2` satisfy the hypothesis. Independence is sufficient
but not necessary: different nonzero multiples work unless the multiplier
is `1` or `-1`. This calibration lemma also applies conditionally to
`r=1` if a covariance class of the form (2) is already known.

## 3. Rational recovery and global uniqueness

Let `C=Q+q(K)` and distinguish the last site. Given `beta,K` and the
degree-one vector `z_j` of each observed output, define

$$
\widehat\mu_{j,i}=
\begin{cases}
L_i(z_j),&i<n,\\
\beta^m L_n(z_j),&i=n,
\end{cases}
\qquad
\widehat R_{ik}=
\begin{cases}
\beta^{-1}C_{ik},&i<k<n,\\
\beta^{m-1}C_{in},&k=n.
\end{cases} \tag{5}
$$

**Lemma 4 (rational normal form).** Every source with the fixed
parameters `beta,K,z_j` is equivalent to (5) under (1). Formula (5)
reproduces all its observed outputs without extracting an `n`th root.

**Proof.** An aligned source has means `a^-m L(z_j)` and quadratic `aC`,
where `a^n=beta^-1`. Apply the site scalars `a^m` at sites `i<n` and
`a^(-m(n-1))` at the last site. Their product is one. The resulting mean
factors are `1` and `a^(-mn)=beta^m`. The edge factors are
`a^(2m+1)=beta^-1` and `a^(1+m(2-n))=beta^(m-1)`, respectively. This is
(5). The root `a` is used only in the proof, not by the algorithm. QED.

**Proof of Theorem 1.** Let an alternative have mean rank `r'<=r`.
Mean rank zero makes every odd output zero and cannot span the observed
space. Thus `r'>=1`.
Its response span contains all the observed tensors, hence has dimension
at least `d`. The response count is strictly increasing with `r`, so
`r'<r` is impossible. For `r'=r`, the alternative has at most `d`
responses, so they are all independent and its response span is exactly
`W`. The global span-reconstruction theorems therefore align its mean
space and put its quadratic into the class (2). In particular, they
exclude local degeneracies of the alternative source.

The coordinate matrix of the spanning observations has row rank `d`.
Its `r` rows of degree one have rank `r`, so for `r>=2` two of its
nonzero columns are independent. If `r=1`, there must instead be two
nonzero degree-one scalars with different squares: otherwise all nonzero
mean settings differ only by sign, and all observed tensors are signed
copies of one tensor, contradicting `dim W=(n+1)/2>=3`.
Lemma 3 uniquely determines the common
`beta,K`. Lemma 4 then identifies every alternative with the same normal
form. All operations used are rational in a suitable nonzero-minor chart.
The only remaining freedom is (1), which always preserves each tensor.
QED.

This is an all-orders consequence of the already proved span theorems.
It does not depend on extending the two-observation exterior-matrix rank
calculation beyond five sites.

## 4. One calibrated output: the threshold is seven sites

Suppose the response span and the class (2) are already known. Let `T`
be one actual nonzero output, so `Z!=0`. Define

$$
S=\frac{F_3}{3Z}=Q_K+\frac\beta3Z^2.
$$

This is a quadratic polynomial. Substituting `Q_K=S-beta Z^2/3` in
(4) gives exact identities

$$
F_5=15ZS^2-\frac23\beta^2Z^5, \tag{6}
$$

$$
F_7=105ZS^3-14\beta^2Z^5S+\frac{16}{9}\beta^3Z^7. \tag{7}
$$

**Theorem 5 (calibration thresholds within a recovered class).** Assume
all listed responses are independent, the local mean maps are injective,
and alternatives are restricted to the recovered class (2), allowing
the site and frame changes of the span theorem. Modulo product-one
site scalings, one nonzero actual output leaves:

* at `n=3`, a one-parameter family of calibrations;
* at `n=5`, exactly two calibrations;
* at every odd `n>=7`, exactly one calibration, recoverable rationally.

**Proof.** At order three, `S` is determined and any nonzero `beta`
gives `Q_K=S-beta Z^2/3`. These are all possible choices.

At order five, (6) fixes a nonzero scalar

$$
B_2=\frac32\frac{15ZS^2-F_5}{Z^5}=\beta^2.
$$

There are exactly two choices of `beta` over `C`; both give the same
degrees one, three, and five. At order seven, (7) also fixes

$$
B_3=\frac9{16}\frac{F_7-105ZS^3+14B_2Z^5S}{Z^7}=\beta^3,
\qquad \beta=B_3/B_2. \tag{8}
$$

Thus `K` and (5) are uniquely determined, regardless of any additional
higher response degrees. The displayed quotients are constant
polynomials for data from the model. They can be evaluated at any `x`
with `Z(x)!=0`, while `S` is obtained by polynomial division or a linear
coefficient solve.

Distinct values of `beta` give distinct gauge classes. Indeed, a site
scaling preserving the aligned mean space has the same scalar `c` at
every site, since all local mean maps are injective and the synchronization
is fixed. Product one forces `c^n=1`. It changes `a` to `c^2a` and
therefore preserves `beta=a^-n`. Lemma 4 accounts for every representative
with a fixed `beta,K`. QED.

The prerequisite is essential: one output suffices **to calibrate a known
response space** at seven sites and above. This does not prove that a
single output recovers the response space itself.

## 5. A universal fifth-order ambiguity and optimality of two observations

The order-five ambiguity has a direct expression without any recovered
frame or genericity assumption.

**Proposition 6 (fifth-order covariance involution).** On five sites, for
arbitrary mean row `mu` and cross-site quadratic `R`,

$$
G(\mu,R)=G\left(\mu,-R-\frac13\mu^2\right). \tag{9}
$$

In block coordinates the replacement is

$$
R_{ik}\longmapsto-R_{ik}-\frac23\mu_i\otimes\mu_k. \tag{10}
$$

**Proof.** The full-site fifth-degree expression is

$$
G(\mu,R)=\frac{\mu^5}{120}+\frac{\mu^3R}{6}+\frac{\mu R^2}{2}.
$$

Substitute `-R-mu^2/3` for `R`. The added terms in `mu^5` cancel and
the coefficient of `mu^3R` is again `1/6`. All three terms are therefore
unchanged. Applying the replacement twice returns `R`. QED.

The two quadratics are generically distinct. If every `mu_i` is nonzero,
a site scaling fixing this mean row has every `lambda_i=1`; it cannot
relate the two distinct quadratics. Thus one fifth-order cross moment
cannot determine the generic quadratic, even if its mean is supplied.
The involution also preserves any response span whose mean space
contains `mu`, since it only rescales `R` and adds a mean quadratic.

For real sources, both collections of cross-site blocks admit positive
definite completions by separately choosing sufficiently large within-site
diagonal blocks. Those blocks are unobserved in this model. Full
homogeneous moment data would constrain them as well; that is a different
identifiability question.

**Corollary 7 (two observations are optimal at five sites).** For five
sites with local dimensions at least three, the
[improved two-observation theorem](one-direction-source-reconstruction-2026-09-27.md#6-larger-local-spaces-and-two-five-site-observations)
uses the minimum possible number of separately observed full cross-moment
tensors for generic recovery of unrestricted shared cross-site covariances.

**Proof.** That theorem supplies generic recovery from two observations;
Proposition 6 rules out generic recovery from one. QED.

## 6. Exact checks and provenance

The [calibration program](../computations/matching-tensor-recovery-2026-09-26/calibrated_span.py)
uses the frames and edge representatives from the existing blind
reconstruction certificates. It regenerates their actual outputs from
the recorded input settings, computes the response coordinates, and
performs calibration using only the reconstructed frame, representative,
and tensor values. The original source is used afterwards to check the
result.

| Sites | Mean directions | Local dimension | Outputs reproduced | Calibration determinant | `beta` |
| --- | --- | --- | --- | --- | --- |
| 5 | 2 | 3 | 12 | 620 | 715 |
| 7 | 2 | 3 | 20 | 119 | 35 |
| 3 | 3 | 4 | 13 | 914 | 176 |
| 3 | 4 | 5 | 24 | 230 | 856 |
| 5 | 3 | 4 | 34 | 895 | 916 |

All numerical entries are exact residues modulo `1009`. Every actual
mean and covariance block agrees with the original source after site
scaling, and each product of site scalars is one. A different recursive
moment evaluation checks every entry of every reconstructed tensor.

At seven sites, the one-output procedure obtains `beta^2=216` and
`beta^3=497`, hence `beta=35`, and its entire covariance correction
agrees with the two-output procedure. No seventh root is computed;
indeed `35^144=302 != 1` modulo `1009`, so the equation
`a^7=35^-1` has no solution in this finite field. The rational normal
form nevertheless recovers a source over the field itself.

At both five-site examples, (10) preserves the first tensor entry by
entry and changes the second. At both three-site examples, choosing a
different nonzero `beta` reproduces the first tensor, verifying the
one-parameter ambiguity. The coefficient identities (6)–(7) and (9)
are also checked symbolically over the rational numbers by expanding
the Gaussian moment formulas, not only by finite-field substitution.

The [certificate](../computations/matching-tensor-recovery-2026-09-26/calibrated-span-certificate.json)
records the calibration minors, source-comparison scalars, and hashes
of the prior certificates on which the examples depend. Run:

```sh
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python computations/matching-tensor-recovery-2026-09-26/calibrated_span.py
```

The all-orders calibration statements are proved by the displayed
identities. The fixed-size checks verify the implementation and its
integration with the earlier span reconstructions.

## 7. Literature and remaining work

Gaussian moment polynomials are classical. The degree-three, five, and
seven formulas used here appear explicitly in Table 1 of Alexander
Taveira Blomenhofer's
[*Gaussian Mixture Identifiability from Degree 6 Moments*](https://arxiv.org/abs/2307.03850),
also available as an [author manuscript](https://ir.cwi.nl/pub/33276/33276.pdf).
Section 2 distinguishes decomposition of points on a moment variety
from statistical parameter recovery. The present problem observes
separate cross-moment tensors and leaves within-site covariances free;
it is not a Gaussian-mixture decomposition problem.

The fixed-covariance connection to Veronese geometry is explicit in
Améndola–Ranestad–Sturmfels,
[*Algebraic Identifiability of Gaussian Mixtures*, Remark 22](https://arxiv.org/html/1612.01129v2#S4).
The shared unknown covariance is also central to
Agostini–Améndola–Ranestad,
[*Moment Identifiability of Homoscedastic Gaussian Mixtures*](https://arxiv.org/abs/1905.05141),
with a different observed model. Pereira–Kileel–Kolda,
[*Tensor Moments of Gaussian Mixture Models: Theory and Applications*](https://arxiv.org/abs/2202.06930),
provide tensor versions of the moment formulas.

The calibration and involution calculations are elementary consequences
of those formulas. Their use after reconstructing an unknown response
space is the application developed here. No exhaustive priority claim
is made.

The generic observation-count question is now settled at odd orders at
least five, for local dimensions at least three. Five sites require
exactly two actual outputs for full
shared-source recovery. The subsequent
[all-orders single-output theorem](single-cross-moment-all-orders-2026-09-27.md)
recovers the actual means and covariance from one tensor at every odd
order at least seven, and aligns any finite generic family with shared
covariance. It combines mean-direction recovery, a restricted-kernel rank
induction, and the calibration formulas here. Numerical conditioning,
statistical sample complexity, and efficient all-orders implementation
are not established.

For further work on the matrix rank, the
[structured-source experiment](../computations/matching-tensor-recovery-2026-09-26/structured_pair.py)
records exact small cases with canonical means `L_1=sum_i e_(0,i)` and
`L_2=sum_i e_(1,i)`, observed at settings `(1,0)` and `(0,1)`.

| Covariance family | Kernel at 3 sites | Kernel at 5 sites |
| --- | ---: | ---: |
| Same symmetric block on every edge | 14 | 398 |
| Independent diagonal blocks on the complete graph | 10 | 32 |
| Independent blocks preserving the mean plane and its complement | 6 | 12 |
| Independent full blocks on a cycle | 6 | 12 |
| Independent blocks preserving the two planes, on a cycle | 6 | 12 |
| Independent full blocks on a path | 14 | 106 |

The response dimensions are respectively `6` and `12` in every row.
Here a block preserving the two planes means its entries between local
coordinates `{0,1}` and `{2,3}` vanish. The
[certificate](../computations/matching-tensor-recovery-2026-09-26/structured-pair-certificate.json)
records the seeds and ranks. These cases show that mean–complement
cross-covariances are not necessary for saturation, and that making a
witness exchangeable or removing an edge from the cycle can introduce
large extra kernels. They suggest studying cycle-supported sources, but
do not prove saturation at any larger order. Replay with:

```sh
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python computations/matching-tensor-recovery-2026-09-26/structured_pair.py
```
