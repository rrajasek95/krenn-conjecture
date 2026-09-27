# Response certificates for multiple requirements and uncertain cores

September 26, 2026. **Written research with exact rational certificates;
awaiting independent audit.**

[Guide](../explainers/METHOD-UTILITY.md) ·
[Replay and optimizer](../computations/method-utility-2026-09-26/README.md)

## 1. Two output requirements remain exactly optimizable

Fix an odd core of squared norm \(a>0\). Write its response as \(H=Lz\)
and \(K=L^*L\). Let \(0\preceq P_j\preceq I\) be output observables, with
requirements

\[
 \frac{H^*P_jH}{\|H\|^2}\ge f_j
 \quad\hbox{or}\quad
 \frac{H^*P_jH}{\|H\|^2}\le f_j.
\]

Examples are fidelity with any prescribed pure state, probability in an
allowed output subspace, or an upper bound on selected unwanted events.
Set \(C_j=s_j(L^*P_jL-f_jK)\), with \(s_j=1\) for a lower requirement
and \(s_j=-1\) for an upper requirement. For \(n=2m\), define

\[
 c_m(a)=\frac{(m-1)^{m-1}}{m^m a^{m-1}}.
\]

**Theorem.** With at most two requirements and a nonzero feasible output,
the best normalized rate is exactly

\[
 c_m(a)\max\{\operatorname{tr}(KX):X\succeq0,
               \operatorname{tr}X=1,
               \operatorname{tr}(C_jX)\ge0\}.          \tag{1}
\]

**Proof.** Scale any unit incident direction to squared norm \(a/(m-1)\),
as in the earlier response optimization. The matrix feasible set is compact
and convex. A linear objective attains its maximum at an extreme point of
that set. If such an extreme point has rank \(r\ge2\), Hermitian
perturbations on its support have real dimension \(r^2\ge4\). At most
three linear equations preserve trace and all active constraints. There is
a nonzero perturbation obeying them. Both sufficiently small signs preserve
positive semidefiniteness and all inactive strict inequalities. This contradicts
extremality. Hence an optimal extreme point has rank one, \(X=vv^*\), and
is an actual incident direction. Its objective is positive because a nonzero
feasible output was assumed. \(\square\)

This is an application of established complex SDP rank theory:
[Huang--Zhang (2007)](https://pubsonline.informs.org/doi/10.1287/moor.1070.0268).
The extension here makes the workspace response optimizer target-independent
and allows a second physical output requirement.

Nonnegative multipliers \(\mu_j\) and a rational \(c\) satisfying

\[
 cI-K-\sum_j\mu_j C_j\succeq0                       \tag{2}
\]

give an upper bound \(c_m(a)c\). Any vector meeting all requirements and
having positive output gives a lower bound. These statements require no
Slater condition. Equality with an attained dual optimum requires additional
regularity; singular endpoints can need a limiting multiplier or direct
restriction to the feasible subspace. The checker validates explicit upper
and lower certificates instead of assuming dual attainment.

The saved six-site example allows all 45 complex root entries, requires GHZ
fidelity at least \(99/100\), and bounds the probability of \(a^6\) by
\(29/100\). Both constraints affect the solution. Its exact upper/lower
interval has relative gap below \(1/10000\). The implemented observables are
arbitrary sparse pure targets and projectors onto sets of output words.

## 2. Three requirements can have a relaxation gap

The restriction to two has mathematical content. For a two-dimensional
complex vector, take the Pauli matrices \(\sigma_x,\sigma_y,\sigma_z\),
\(K=3I-\sigma_x-\sigma_y-\sigma_z\succ0\), and require
\(v^*\sigma_jv\ge0\) for all three \(j\), with \(\|v\|=1\).

A pure vector has a Bloch vector \(r\) of length one. In the positive
octant, \(r_x+r_y+r_z\ge1\), so its objective is at most two, attained
on a coordinate axis. The relaxed matrix \(X=I/2\) has objective three
and satisfies every constraint. Taking all three dual multipliers equal to
one gives zero slack at upper value three. Thus the relaxation gap is exact.

This is a counterexample for the general response optimization theorem,
not an assertion that every matching instance with three requirements has
a gap. It can also be written with bounded output observables after choosing
\(L=K^{1/2}\) and \(P_j=I/2+K^{-1/2}\sigma_jK^{-1/2}/2\).
The replay checks the Pauli identities and the displayed primal/dual witnesses.

## 3. A certificate can cover a ball of complex cores

For six sites let \(Q_0\) be the fixed five-site core, and suppose
\(\|Q-Q_0\|\le\rho\). Assume rational numbers \(l,u,o\) satisfy

\[
 0\le\rho<l\le\|Q_0\|\le u,\qquad \|L_{Q_0}\|\le o.
\]

The output observables and thresholds stay fixed as the core varies.
Then

\[
 \|L_Q-L_{Q_0}\|\le
 \sqrt{15}(u\rho+\rho^2/2)
 \le\beta:=4(u\rho+\rho^2/2).                       \tag{3}
\]

To see this, each four-site hafnian tensor changes by at most
\(u\rho+\rho^2/2\). Expand its three matchings: Cauchy--Schwarz bounds
the cross terms by the product of the source and perturbation norms, and
AM--GM bounds the quadratic perturbation by half its squared norm.
The five omitted-site responses each occur in three orthogonal local-color
columns of \(T\); hence its squared Frobenius change is at most fifteen
times the squared bound. Finally \(L=I_3\otimes T\) has the same operator
norm as \(T\).

For a dual certificate (2) at \(Q_0\), define

\[
 b=\left|1-\sum_j\mu_j s_j f_j\right|+\sum_j\mu_j,
 \qquad d=b(2o\beta+\beta^2).
\]

The output operator \(B=I+\sum_j\mu_js_j(P_j-f_jI)\) has norm at most
\(b\). Thus \(L_Q^*BL_Q\preceq(c+d)I\), by expanding its difference
from \(L_{Q_0}^*BL_{Q_0}\). Since \(\|Q\|\ge l-\rho\), every qualifying
source with a core in this ball obeys

\[
 \boxed{R\le\frac{4(c+d)}{27(l-\rho)^4}.}            \tag{4}
\]

This covers arbitrary complex changes in all 90 core cells, not just changes
in its original support. The saved radius is \(10^{-6}\). The checker
verifies \(l^2\le a\le u^2\), \(o^2I-K\succeq0\), and every rational
quantity in (4). The cofactor perturbation estimate is the analytic argument
above. Finite differences are not used as evidence for the ball bound.

This is useful for robust exclusion and eventual subdivision of the core
search space. The single saved ball is not a covering of that space or a
global architecture certificate.

## 4. A target-independent singular-response criterion

The preceding singular-boundary proof has a reusable form. Suppose a local
response has leading part

\[
 Y=Lv+M(k,u)
\]

with a bilinear \(M\). Let \(P\) project onto \(\operatorname{im}L\), and
assume

\[
 \|Lv\|\ge\sigma\|v\|,\quad
 \|M(k,u)\|\le b\|k\|\|u\|,\quad
 \|(I-P)M(k,u)\|\ge d\|k\|\|u\|,
\]

where \(\sigma,d>0\). Suppose a unit target \(g\) has overlap at most
\(r<1\) with the whole span of \([L,M]\), and the remainder satisfies

\[
 \|H-Y\|\le\eta(A\|v\|+B\|k\|\|u\|).
\]

Projection and the triangle inequality give
\(\|k\|\|u\|\le\|Y\|/d\) and
\(\|v\|\le(1+b/d)\|Y\|/\sigma\). Put

\[
 \theta=\eta\left[\frac{A(1+b/d)}\sigma+\frac Bd\right].
\]

For \(\theta<1\), every nonzero output then obeys

\[
             F_g(H)\le\left(\frac{r+\theta}{1-\theta}\right)^2. \tag{5}
\]

It gives a strict exclusion when \(r+2\theta<1\). If \(Y=0\), the same
estimates force \(H=0\). The former concrete proof is the instance
\((\sigma,b,d,A,B,r)=(2,2,1,46,1,3/4)\), so \(\theta=70\eta\).

The product lower bound can be checked by a positive matrix after partial
transposition, as in the earlier package. This lemma applies to any local
response with the stated estimates, including other targets. It does not
show that arbitrary singular responses satisfy those hypotheses.
