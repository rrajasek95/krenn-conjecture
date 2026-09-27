# Aggregate cancellation and the exact fixed-core rate frontier

September 26, 2026. **Written research with exact supporting certificates;
awaiting independent audit.** The earlier pinned packages are unchanged.

[Explainer](../explainers/RATE-DESIGN-FRONTIER.md) ·
[Replay and optimizer](../computations/rate-design-frontier-2026-09-26/README.md) ·
[Prism optimum](prism-optimal-rate-2026-09-26.md) ·
[Singular boundary](singular-kernel-rate-exclusion-2026-09-26.md)

## 1. The square-root bound needs only aggregate cancellation control

Use the 180 mixed even-count receiving words \(\mathcal W\) from the
[preceding rate theorem](rate-sharpness-followup-2026-09-26.md).
For an arbitrary complex six-site source, put

\[
 P_w=\sum_M|a_{M,w}|,\qquad
 e_W^2=\sum_{w\in\mathcal W}|H_w|^2,\qquad
 p_W^2=\sum_{w\in\mathcal W}P_w^2.
\]

When \(p_W>0\), define \(\kappa_2=e_W/p_W\). It lies in \([0,1]\).
For \(p_W=0\), set \(\kappa_2=1\); the positive matching certificate then
forces the product of the pure amplitudes to vanish, so a nonzero source
cannot have fidelity greater than \(2/3\).

The existing positive cover, applied to the magnitudes of the source, gives

\[
 |\tau_a\tau_b\tau_c|\le\sqrt{41/1440}\,S^3p_W
 =\frac{\sqrt{41/1440}}{\kappa_2}\,S^3e_W .       \tag{1}
\]

The second equality requires \(\kappa_2>0\). Repeating the target-overlap
estimate from the preceding note proves, for \(F>2/3\),

\[
 R\le\frac{\sqrt{123/160}}{\kappa_2}
 \frac{\sqrt{1-F}}{[\sqrt F-\sqrt{2(1-F)}]^3}.     \tag{2}
\]

If the three complex pure amplitudes are exactly equal, replace the cubed
bracket by \(F^{3/2}\). The physical Gaussian conversion has the same
assumptions as before. No new source model is introduced here.

The old minimum ratio \(\kappa\) satisfies \(\kappa_2\ge\kappa\).
More precisely, \(\kappa_2^2\) is the average of the squared per-word
ratios with weights \(P_w^2/\sum_vP_v^2\). A tiny output with complete
cancellation can make the old minimum zero without spoiling this average.
This is a strict extension of the condition, not a changed exponent.

### An exact high-fidelity example missed by the minimum test

Start with the prism having internal weights one and vertical weights
\(t=1/10\). Add three diagonal color-b cells

\[
 A_{23}(b,b)=u^2,\quad A_{24}(b,b)=u,\quad
 A_{35}(b,b)=-u,\qquad u=1/10000.
\]

The word \(aabbbb\) has contributions \(u^2-u^2=0\), so the old
\(\kappa=0\). All three pure amplitudes remain \(t\).
The exact replay verifies \(F>9999/10000\) and \(\kappa_2>99/100\).
Thus (2) is useful even though the source contains complete cancellation.
The unrestricted limit \(\kappa_2\to0\) remains outside this theorem.

## 2. Optimize all edges incident to one site

Fix a five-site core \(Q\), of squared source norm \(a>0\), and choose
the remaining root. The exact response map from the earlier boundary note is
\(T_Q:\mathbb C^{15}\to\mathbb C^{243}\). Stack the three root-color
rows into \(z\in\mathbb C^{45}\), and write

\[
 H=Lz,\quad L=I_3\otimes T_Q,\quad K=L^*L,\quad
 g=\Delta/\sqrt3,\quad U=L^*gg^*L.
\]

Then

\[
 F(z)=\frac{z^*Uz}{z^*Kz},\qquad
 R(z)=\frac{z^*Kz}{(a+\|z\|^2)^3}.                \tag{3}
\]

For a unit vector \(v\), put \(z=\sqrt t\,v\). Fidelity is independent
of \(t\), while rate is \((v^*Kv)t/(a+t)^3\).
Differentiation gives the unique positive maximizing scale

\[
 \boxed{t=a/2,\qquad
 R_{\rm best}(v)=\frac4{27a^2}v^*Kv.}             \tag{4}
\]

Thus the optimum allocates one third of the total squared source norm to the
root edges. At \(n=2m\) sites the same calculation gives \(t=a/(m-1)\)
and factor \((m-1)^{m-1}/(m^m a^{m-1})\).
This is an optimization of normalized matching strength, not of the full
Gaussian probability determinant.

## 3. A matrix optimization with no relaxation gap

For a feasible fidelity floor \(f\), set \(C_f=U-fK\). The best
fixed-core rate is

\[
 \boxed{R_Q(f)=\frac4{27a^2}
 \max\{\operatorname{tr}(KX):X\succeq0,
          \operatorname{tr}X=1,\ \operatorname{tr}(C_fX)\ge0\}.}  \tag{5}
\]

Although the matrix formulation drops \(X=vv^*\), it is exact over complex
vectors. Here is a short rank reduction proof. If a feasible matrix has rank
\(r\ge2\), Hermitian perturbations on its support form a real space of
dimension \(r^2\ge4\). The three linear equations preserving
\(\operatorname{tr}X,\operatorname{tr}(KX),\operatorname{tr}(C_fX)\)
therefore admit a nonzero perturbation. Move along it until reaching the
boundary of the positive cone. Rank drops while all three values stay fixed.
Iteration reaches rank one, proving (5).

This uses established complex quadratic-optimization machinery, not a new
general SDP theorem; see [Huang–Zhang (2007)](https://pubsonline.informs.org/doi/10.1287/moor.1070.0268).
The application here is the exact matching response and its source-norm scale.

The exact feasibility ceiling is

\[
 F_{\max}(Q)=\tfrac13\sum_{h=a,b,c}\|P_{\operatorname{im}T_Q}h^5\|^2.
                                                               \tag{6}
\]

Test this first: a zero-output vector in \(\ker K\) formally satisfies
the matrix constraint but does not make an impossible fidelity feasible.
If \(f>F_{\max}\), no nonzero output qualifies. If \(0\le f<F_{\max}\),
strict feasibility gives the equivalent one-parameter dual

\[
 R_Q(f)=\frac4{27a^2}\inf_{\mu\ge0}
              \lambda_{\max}(K+\mu C_f).          \tag{7}
\]

At \(f=F_{\max}\), directly optimize \(K\) on \(\ker C_f\);
the dual infimum need not be attained by a finite multiplier.

### Exact, reviewable upper and lower certificates

A rational \(\mu\ge0\) and rational \(c\) with
\(cI-K-\mu C_f\succeq0\) prove the upper bound \(4c/(27a^2)\).
Any nonzero Gaussian-rational vector \(v\) with \(v^*C_fv\ge0\) and
\(v^*Kv>0\) proves the attainable lower bound
\(4(v^*Kv)/(27a^2\|v\|^2)\).
Schur pivots and these inequalities can all be checked with rational arithmetic.
Numerical eigenvalues only propose certificates; they never certify one.

The saved example fixes the prism's five-site core at vertical parameter
\(t=1/10\), while allowing all 45 complex root entries. Its exact fidelity
ceiling is \(\frac13(2+1/(1+t^4))\), and its core energy is \(201/50\).

| Fidelity floor | Certified best normalized strength, approximately |
|---|---:|
| 0.9 | 0.00025674945 |
| 0.99 | 0.00015970583 |
| 0.999 | 0.00014308421 |
| 0.9999 | 0.00013840053 |

Every saved upper/lower pair has relative gap below \(5\times10^{-8}\).
The exact rational intervals, rather than these rounded values, are the
certificates. A complex-phase variant is also checked.

This eliminates the incident-edge optimization exactly for a fixed core.
Optimizing the core itself remains a larger nonlinear problem; these local
certificates are not global optimality certificates over all architectures.
