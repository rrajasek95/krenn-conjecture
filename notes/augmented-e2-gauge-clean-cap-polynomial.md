# The augmented E2 gauge family as a one-variable clean-cap polynomial

## 1. Outcome

Fix a gauge-rigid deleted pair and a diagonal cap whose three diagonal
entries are nonzero.  If the six off-diagonal E2 primitives span the defect
space, then every defect vector gives an off-diagonal perturbation of that
cap.  The resulting homogeneous clean error has the exact normal form

\[
 {\cal E}(\beta)=
 \left(F_0+\Gamma_q\!\left(\beta-\frac{\sigma(\beta)}2{\bf1}\right)
 \right)^{[t]}
 -(s_0-\sigma(\beta))^{t-1}T_0,                    \tag{1}
\]

where

\[
 F_0=s_0q+r_0,\qquad
 \sigma(\beta)=\sum_{i\in W}\beta_i,\qquad
 T_0=\sum_{c=0}^2\kappa_cX_c.                      \tag{2}
\]

There is no hidden factor of \(t\) in (1): it uses exactly the pair
normalization

\[
 a_{cd}q^{[t]}+p_cs_dq^{[t-1]}=\delta_{cd}X_c,
 \qquad
 p_cs_d=\Gamma_q(\alpha_{cd}),\quad
 \sum_i\alpha_{cd,i}=-a_{cd}\quad(c\ne d).          \tag{3}
\]

Formula (1) turns the cap question into a polynomial problem on the defect
space.  On every defect line, an active clean cap exists exactly when the
coordinate polynomials of the error have a common root away from the one
possible inactive point.  In particular, it exists if the polarized error
coefficients lie in one tensor line and their scalar polynomial is
nonconstant and is not supported only at the inactive point.

Thus spanning the defect space solves the **access** problem, but not by
itself the **common-zero** problem.  The additional condition isolated here
is intrinsic: a nontrivial common polynomial divisor of the polarized
top-tensor components after removing the activity factor.

## 2. The affine family

Let \(W\) have \(2t\) sites.  Work in its site-square-zero commutative
tensor algebra, and let \(q\) be the internal quadratic.  For
\(\alpha\in\mathbb C^W\), vertex scaling is

\[
 \bigl(\Gamma_q(\alpha)\bigr)_{ij}
       =(\alpha_i+\alpha_j)q_{ij}.                   \tag{4}
\]

Every perfect matching uses every site once, hence

\[
 \Gamma_q(\alpha)q^{[t-1]}
       =\left(\sum_i\alpha_i\right)q^{[t]}.           \tag{5}
\]

Let \(K_{\rm diag}\) have fixed diagonal entries
\(\kappa_0,\kappa_1,\kappa_2\ne0\).  Write its cap data as

\[
 s_0=\sum_c\kappa_ca_{cc},\qquad
 r_0=\sum_c\kappa_cp_cs_c,\qquad
 T_0=\sum_c\kappa_cX_c.                              \tag{6}
\]

For an off-diagonal matrix \(k=(k_{cd})_{c\ne d}\), put

\[
 K=K_{\rm diag}+K_{\rm off},\qquad
 \beta(k)=\sum_{c\ne d}k_{cd}\alpha_{cd},\qquad
 \sigma(k)=\sum_i\beta(k)_i.                         \tag{7}
\]

Summing (3) with coefficients \(k_{cd}\) gives

\[
 \Delta s=\sum_{c\ne d}k_{cd}a_{cd}=-\sigma(k),
 \qquad
 \Delta r=\sum_{c\ne d}k_{cd}p_cs_d
                  =\Gamma_q(\beta(k)),\qquad
 \Delta T=0.                                         \tag{8}
\]

Consequently the entire affine family depends on \(K_{\rm off}\) only
through its defect vector:

\[
 s_\beta=s_0-\sigma(\beta),\qquad
 r_\beta=r_0+\Gamma_q(\beta),\qquad
 T_\beta=T_0.                                        \tag{9}
\]

If the six \(\alpha_{cd}\) span the defect space \(D_q\), the map
\(\mathbb C^6\to D_q,\ k\mapsto\beta(k)\) is surjective.  Different
coefficient vectors in its kernel give identical triples \((s,r,T)\), so
there is no quotient ambiguity in the clean equation.

Because the diagonal entries remain fixed and nonzero, the cap is active
precisely when

\[
                         s_0-\sigma(\beta)\ne0.       \tag{10}
\]

## 3. Exact homogeneous error formula

For arbitrary cap data satisfying

\[
                         sq^{[t]}+rq^{[t-1]}=T,       \tag{11}
\]

define the denominator-cleared clean error by

\[
 {\cal E}_t(s,r)=
 \sum_{j=2}^t s^{t-j}r^{[j]}q^{[t-j]}.               \tag{12}
\]

Put \(F=sq+r\).  The divided-power binomial identity and (11) give

\[
\begin{aligned}
 F^{[t]}
 &=\sum_{j=0}^t s^{t-j}q^{[t-j]}r^{[j]},\\
 {\cal E}_t(s,r)
 &=F^{[t]}-s^{t-1}T.                                 \tag{13}
\end{aligned}
\]

For (9), use \(\Gamma_q({\bf1})=2q\) and set

\[
 C(\beta)=\Gamma_q(\beta)-\sigma(\beta)q
 =\Gamma_q\!\left(\beta-\frac{\sigma(\beta)}2{\bf1}\right).       \tag{14}
\]

Then \(s_\beta q+r_\beta=F_0+C(\beta)\).  Substitution in
(13) proves (1).

As a useful normalization check, a purely off-diagonal cap has \(T=0\),
\(s=-\sigma(\beta)\), and \(r=\Gamma_q(\beta)\).  Its error is exactly

\[
 {\cal E}_{\rm off}(\beta)
 =C(\beta)^{[t]}
 =\Gamma_q\!\left(\beta-\frac{\sigma(\beta)}2{\bf1}\right)^{[t]}.
                                                               \tag{15}
\]

## 4. Polarization on a defect line

Fix \(\beta\in D_q\), abbreviate

\[
 \sigma=\sigma(\beta),\qquad C=C(\beta),
\]

and vary the accessible cap on the line \(z\beta\).  Formula (1) becomes

\[
 {\cal E}_\beta(z)
 =(F_0+zC)^{[t]}-(s_0-z\sigma)^{t-1}T_0
 =\sum_{j=0}^t z^jE_j,                               \tag{16}
\]

with exact polarized coefficients

\[
 E_j=
 C^{[j]}F_0^{[t-j]}
 -\binom{t-1}{j}s_0^{t-1-j}(-\sigma)^jT_0
 \quad(0\le j\le t-1),                               \tag{17}
\]

and

\[
 E_t=C^{[t]}.                                         \tag{18}
\]

Here the binomial coefficient in (17) is an ordinary scalar coefficient;
the products in its first term are divided powers.  At the first boundary
\(t=3\), this reads

\[
\begin{aligned}
 E_0&=F_0^{[3]}-s_0^2T_0,\\
 E_1&=CF_0^{[2]}+2s_0\sigma T_0,\\
 E_2&=C^{[2]}F_0-\sigma^2T_0,\\
 E_3&=C^{[3]}.                                        \tag{19}
\end{aligned}
\]

These four top tensors are the smallest exact data controlling the
eight-to-six augmented-gauge problem.

## 5. The common-divisor criterion

Let \({\cal V}\) be the full-site component of the tensor algebra, so
\({\cal E}_\beta(z)\in{\cal V}[z]\).  Choose any basis of \({\cal V}\),
write

\[
 {\cal E}_\beta(z)=\sum_\nu e_\nu(z)v_\nu,
\]

and let \(g_\beta\) be the greatest common divisor of the nonzero
\(e_\nu\), defined up to a nonzero scalar.  If every \(e_\nu\) is zero,
write \(g_\beta=0\).

This construction is coordinate-free.  A change of basis replaces the
list of coordinate polynomials by invertible constant linear
combinations, so it generates the same ideal in \(\mathbb C[z]\) and has
the same gcd.

**Theorem 5.1 (active defect-line criterion).**  Put
\(h_\beta(z)=s_0-z\sigma\).  If \(h_\beta\) is identically zero, the
entire line is inactive.  Otherwise, the line \(z\beta\) contains an
active clean cap if and only if either

1. \(g_\beta=0\); or
2. after removing from \(g_\beta\) every factor proportional to
   \(h_\beta\), the remaining polynomial has positive degree.

Equivalently, if \(I_\beta\) is the ideal generated by the coordinate
polynomials, then

\[
 I_\beta:h_\beta^\infty
\]

is a proper ideal with a nonempty zero set.

**Proof.**  If \(h_\beta=0\), activity fails at every point.  Suppose
\(h_\beta\ne0\).  A value \(z\) is clean exactly when all coordinate
polynomials vanish there, equivalently \(g_\beta(z)=0\).  It is active
exactly when \(h_\beta(z)\ne0\).  If the vector polynomial vanishes
identically, every \(z\) is clean and the nonzero polynomial \(h_\beta\)
cannot vanish everywhere.
Otherwise, unique factorization in \(\mathbb C[z]\) says that saturation
removes precisely the multiplicity of the possible inactive root from
the gcd.  The residual polynomial has a complex root exactly when it has
positive degree.  \(\square\)

The theorem gives a concrete structural sufficient condition.

**Corollary 5.2 (one-dimensional polarized error).**  Suppose

\[
                  \dim\operatorname{span}\{E_0,\ldots,E_t\}\le1.  \tag{20}
\]

If \(s_0-z\sigma\) is identically zero, this line has no active cap.  If
all \(E_j\) vanish and \(s_0-z\sigma\) is not identically zero, there is
an active clean cap.  In the remaining case, choose a nonzero tensor
\(R\) on their common line and write

\[
                         {\cal E}_\beta(z)=e(z)R.      \tag{21}
\]

An active clean cap exists under either of the following conditions:

* \(\sigma=0\), \(s_0\ne0\), and \(e\) is nonconstant;
* \(\sigma\ne0\), \(e\) is nonconstant, and
  \(e\) is not proportional to a positive power of
  \(s_0-z\sigma\).

**Proof.**  If the error is identically zero and the activity polynomial
is nonzero, choose a point away from its at most one root.  Otherwise, a
nonconstant complex polynomial has a root.  When \(\sigma=0\), activity
is the constant condition \(s_0\ne0\).  When
\(\sigma\ne0\), the only inactive value is \(z=s_0/\sigma\).  Every root
of \(e\) lies at that value exactly when \(e\) is a nonzero scalar
multiple of a positive power of \(s_0-z\sigma\).  \(\square\)

Condition (20) is basis-free and finite: it asks for the vanishing of all
two-by-two wedges \(E_i\wedge E_j\).  More generally, Theorem 5.1 asks
for a common divisor among the tensor components, not for the much
stronger collapse to one tensor line.

## 6. What remains

The spanning hypothesis on the six E2 primitives is used exactly once:
it makes every \(\beta\in D_q\) accessible.  It imposes no visible
common-divisor relation on the tensors (17)--(18).  Therefore the next
positive bridge is to derive, from physical provenance or overlap
relations, one of the following:

1. a defect direction satisfying the one-dimensional condition (20);
2. a weaker forced common factor in the coordinate ideal of (16); or
3. a higher-dimensional defect subspace on which the analogous saturated
   ideal has a zero.

This note does not claim that defect spanning is logically insufficient:
that stronger negative statement would require an exact gauge-rigid
physical pair-chart countermodel.  It instead isolates the extra
polynomial structure sufficient to finish the cap step, while retaining
arbitrary complex cancellation, endpoint order, and all defect
components.  In particular, Corollary 5.2 is a sufficient criterion
conditional on error-line collinearity; neither (20) nor any common
factor is being inferred from \(\operatorname{span}\{\alpha_{cd}\}=D_q\).
