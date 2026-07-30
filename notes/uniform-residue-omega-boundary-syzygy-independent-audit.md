# Independent audit: uniform residue--Omega boundary syzygy

Audit date: 2026-07-29.

## Verdict

**PASS AFTER TWO CORRECTIONS.**  The divided-power expansion, odd-site
quotient identity, gauge invariance, degree-\((h-2)\) torus certificate,
convolution equations, and the conditional two-chart transport all have
the stated normalization for every \(h\geq3\).

Two scope defects were found and corrected in the source note during this
audit.

1. The formal guard originally chose an arbitrary map \(D:V\to C\) and
   then assumed that
   \(D(\Pi_\nu-A)=\sigma_\nu^{h-1}\zeta\) was solvable.  The source now
   takes \(C\) one-dimensional and \(D\) surjective, which makes the
   displayed choice of \(\Pi_\nu\) valid.
2. The one-chart Omega packet uses the diagonal scalar-zero endpoint
   \(K_{\rm diag}=E_{00}-I\), whereas the general common-coloop residual
   previously isolated in the project naturally uses an off-diagonal
   contraction \(K_*=\tau E_{ab}-\alpha I\).  Those responses cannot be
   identified.  Section 8 now states only a conditioned intersection
   target: the exact diagonal response must already be the Omega endpoint
   and must already carry a visible common-coloop corner with
   \(c\in\{1,2\}\) and \(K_{{\rm diag},cc}\ne0\).

The proposed equality in Section 8 remains unproved.  The corrected note
does not close the general off-diagonal common-coloop residual, produce two
overlapping diagonal charts, or route an arbitrary selected curvature line
into its hypotheses.

## 1. Divided-power and activity normalization

Write the clean error in the diagonal normalization as

\[
 {\cal E}(t,u)
  =(tF+uR)^{[h]}
   -(t\sigma)^{h-1}(tX_0-uX_1-uX_2).
\]

Polarization in divided powers gives

\[
 (tF+uR)^{[h]}
   =\sum_{j=0}^{h}t^{h-j}u^jR^{[j]}F^{[h-j]}
\]

with no ordinary binomial coefficients.  The \(j=0\) coefficient vanishes
by \(F^{[h]}=\sigma^{h-1}X_0\), the \(j=h\) coefficient vanishes by
\(R^{[h]}=0\), and the only mixed target correction is

\[
 \sigma^{h-1}(X_1+X_2)
       =-\sigma^{h-1}Rq^{[h-1]}
\]

at \(j=1\).  Hence

\[
 {\cal E}(t,u)=tu\sum_{j=1}^{h-1}
        t^{h-1-j}u^{j-1}E_j,
\]

\[
 E_1=R(F^{[h-1]}-\sigma^{h-1}q^{[h-1]}),\qquad
 E_j=R^{[j]}F^{[h-j]}\quad(2\leq j\leq h-1).
\]

Thus \(\Omega\) has degree \(d=h-2\), and
\(\Omega(1,0)=E_1\).  At \(h=3\) these are exactly the two usual Omega
columns; at larger \(h\) the intermediate coefficients are genuine and
cannot be discarded.

The cap matrix on this line is

\[
 tE_{00}+u(E_{00}-I)=\operatorname {diag}(t,-u,-u).
\]

Because \(\sigma\ne0\), the direct scalar is nonzero precisely when
\(t\ne0\), and all three fixed target coordinates are nonzero precisely
when \(tu\ne0\).  Activity is therefore exactly the projective torus
\(D(tu)\).  This statement is conditional on this diagonal normalization;
it is not an activity calculation for \(K_*=\tau E_{ab}-\alpha I\).

## 2. Domains of the quotient, polar, and residue

On \(K=W\setminus\{x\}\), with \(|K|=2h-1\),

\[
 A=q_0^{[h-1]}\in{\cal R}_{2h-2}(K),\qquad
 B=q_0^{[h-2]}\in{\cal R}_{2h-4}(K).
\]

Consequently

\[
 C_{q_0}
  ={\cal R}_{2h-1}(K)\big/{\cal R}_1(K)A
\]

is degree-consistent, and \(\pi_{q_0}\) is the quotient map from the top
component \({\cal R}_{2h-1}(K)\).  For a quadratic \(Z\) and a linear
form \(T\) on \(K\), the product \(TZB\) has top degree, so

\[
 \operatorname {res}_{q_0}(Z;T)=\pi_{q_0}(TZB)
\]

is well-defined.  The coefficient map \(\partial_{x,c}\) sends a top
tensor on \(W\) to this same top component on \(K\), so every occurrence
of \(\pi_{q_0}\partial_{x,c}\) in the note has the correct domain.

Since every summand of
\(\rho=\sum_c e_c^{(x)}t_c\) uses \(x\), \(\rho^2=0\) and

\[
 q^{[h-1]}=A+\rho B.
\]

The identity defining \(E_1\) gives, before quotienting,

\[
 RF^{[h-1]}-\Omega(1,0)
       =\sigma^{h-1}Rq^{[h-1]}.
\]

Writing \(R=r+\sum_c e_c^{(x)}n_c\), its \((x,c)\)-coefficient is

\[
 \sigma^{h-1}(n_cA+rt_cB).
\]

The first summand lies in \({\cal R}_1(K)A\), while the second is exactly
the odd residue.  Therefore

\[
 \sigma^{h-1}\operatorname {res}_{q_0}(r;t_c)
  =\pi_{q_0}\partial_{x,c}
      (RF^{[h-1]}-\Omega(1,0)).
\]

The physical scalar-zero row gives

\[
 n_cA+rt_cB
   =-\delta_{c1}Y_1-\delta_{c2}Y_2,
\]

and hence the displayed defect is

\[
 -\sigma^{h-1}
   (\delta_{c1}\overline Y_1+\delta_{c2}\overline Y_2).
\]

No factor \(h\) or \(h-1\) is missing.  Raw canonical caps multiply both
the quadratic and its target by \(h\); the sole multiplication formula
needed in the quotient is

\[
 q_0B=(h-1)A.
\]

At no point is \(A\), \(B\), or \(q_0^{[h-2]}\) cancelled.

## 3. Gauge invariance

For the genuine vertex-gauge quadratic

\[
 (Z_{q_0}^{\beta})_{yz}=(\beta_y+\beta_z)(q_0)_{yz},
\]

coefficientwise matching enumeration gives

\[
 Z_{q_0}^{\beta}Tq_0^{[h-2]}
 =\left(\left(\sum_{y\in K}\beta_y\right)T
                 -\beta\mathbin\cdot T\right)q_0^{[h-1]}.
\]

For a top monomial, \(T\) occupies the unique unmatched site and the
distinguished matching edge contributes the sum of the vertex weights on
all remaining sites.  The right side is in
\({\cal R}_1(K)A\), so every such gauge has zero residue.

It follows that

\[
 \pi_{q_0}\partial_{x,c}
   (RF^{[h-1]}-\Omega(1,0))
\]

is unchanged when the off-site scalar-zero response is changed by a
genuine vertex gauge.  The note correctly does not claim that either
\(RF^{[h-1]}\) or \(\Omega(1,0)\) separately descends to this quotient.

## 4. The uniform torus certificate

Let \(f_i\in\mathbb C[t,u]_d\) be scalar coordinates of the nonzero vector
polynomial \(\Omega\).  For binary homogeneous forms, a common projective
root is the same as a common linear factor.  If there is no common root
in \(D(tu)\), every common factor is supported at an endpoint, so

\[
 \gcd(f_i)=t^au^b,\qquad a,b\geq0,\quad a+b\leq d.
\]

Zero scalar coordinates cause no problem: the gcd is taken over the
nonzero coordinates, and \(\Omega\ne0\) guarantees that this collection is
nonempty.  After division, the forms
\(\widehat f_i\) have common degree

\[
 e=d-a-b
\]

and gcd one.

If \(e>0\), two linear combinations \(F,G\) of the
\(\widehat f_i\) can be chosen coprime: choose one nonzero \(F\), and
avoid in the second combination the finitely many proper subspaces
corresponding to the irreducible factors of \(F\).  Then \(F,G\) form a
binary complete intersection of degrees \(e,e\), whose quotient has
socle degree \(2e-2\).  Thus \((F,G)\) contains every binary form of
degree at least \(2e-1\).  If \(e=0\), the reduced ideal is already the
unit ideal.

Now

\[
 {(tu)^d\over t^au^b}=t^{d-a}u^{d-b}
\]

has degree \(2d-a-b\), and

\[
 2d-a-b\geq2(d-a-b)-1=2e-1.
\]

It therefore belongs to \((F,G)\), with both homogeneous multipliers of
degree

\[
 (2d-a-b)-e=d.
\]

Multiplication by \(t^au^b\) proves

\[
 (tu)^d\in I_\Omega.
\]

Conversely, this membership immediately excludes a common zero with
\(tu\ne0\).  By the projective Nullstellensatz, absence of such a zero is
also equivalent to \(I_\Omega:(tu)^\infty=\mathbb C[t,u]\).  Hence all four
conditions in Theorem 5.1 are equivalent, including the endpoint cases
\(a=0\), \(b=0\), \(a+b=d\), and \(e=0\).

Writing

\[
 H=\sum_{r=0}^dt^{d-r}u^rH_r,\qquad
 \Omega=\sum_{k=0}^dt^{d-k}u^kE_{k+1},
\]

the coefficient of \(t^{2d-n}u^n\) in
\(\langle H,\Omega\rangle\) is

\[
 \sum_{r+k=n}H_r(E_{k+1}).
\]

It equals the corresponding coefficient of \((tu)^d\), namely
\(\delta_{n,d}\).  This proves all \(2d+1\) convolution identities with no
index or degree shift.  For \(d=1\), they are equivalent to the familiar
alternative that \(E_1,E_2\) are independent or exactly one is zero.

As lightweight edge checks, at arbitrary \(d\)

\[
 \Omega=t^dA+u^dB,\qquad
 H=u^d\alpha,\quad \alpha(A)=1,\ \alpha(B)=0
\]

gives \(\langle H,\Omega\rangle=(tu)^d\); and the endpoint-osculating case
\(\Omega=u^dA\) is certified by
\(H=t^d\alpha\).  These test respectively \(a=b=0\) and the extreme
\(a=0,b=d,e=0\) boundary.

## 5. Two-chart transport and the diagonal/off-diagonal distinction

For two overlapping charts which are both already in normalization
\(K_{\rm diag}=E_{00}-I\), the common odd restriction \(q_0\) gives one
quotient \(C_{q_0}\).  The power-free cap connection, followed only by
multiplication by \(B\), transports the fixed-target residue.  Equivalently,
the complete scalar-zero row on either chart gives

\[
 \operatorname {res}_{q_0}(r_\nu;t_{\nu,c})
  =\zeta_c
  =-\delta_{c1}\overline Y_1-\delta_{c2}\overline Y_2.
\]

Combining this with the one-chart identity and using the explicitly
assumed \(\sigma_\nu\ne0\) gives

\[
 \zeta_c
 =\sigma_\nu^{1-h}\pi_{q_0}\partial_{\nu,c}
   (R_\nu F_\nu^{[h-1]}-\Omega_\nu(1,0)).
\]

Thus the power \(\sigma_\nu^{1-h}\), the sign, and the common quotient in
the two-chart formula are correct.  The transport preserves the defect;
it supplies no equation making it zero.

This statement has no selected-six-site step.  The ambient chart has
\(2h\) sites, the odd quotient has \(2h-1\), and all coefficients of the
degree-\((h-2)\) Omega polynomial are retained.

The normalization is not automatic on the common-coloop branch.  For a
general scalar-zero cap matrix \(K\), the residue is

\[
 \operatorname {res}_{q_0}(\overline R_K;t_c)
     =K_{cc}\overline Y_c.
\]

The established off-diagonal common-coloop choice
\(K_*=\tau E_{ab}-\alpha I\), \(a\ne b\), has
\(K_{*,cc}=-\alpha\) for all three labels.  In contrast,
\(K_{\rm diag}=E_{00}-I\) has diagonal \((0,-1,-1)\): it sees labels
\(1,2\) and is blind to label \(0\).  No scaling, gauge change, flat
connection, or Bianchi identity identifies these two cap directions.

## 6. Abstract guard and remaining proof obligation

After the correction, the abstract guard is internally consistent:
surjectivity of \(D:V\to C\) makes it possible to choose every
\(\Pi_\nu\) satisfying

\[
 D(\Pi_\nu-A)=\sigma_\nu^{h-1}\zeta.
\]

The independent vectors \(A,B\) make
\(\Omega_\nu=t^dA+u^dB\) torus-root-free, and
\(u^d\alpha\) is an exact bounded certificate.  Hence the abstract
certificate plus flat defect transport really permits arbitrary nonzero
\(\zeta\).  The guard expressly does not realize consecutive powers or
the full-nine source equations, so it is a guard against a formal
deduction, not a graph counterexample.

The corrected Section 8 lemma is now precise as a **conditioned
intersection target**.  It assumes:

* two literal overlapping diagonal charts with common \(q_0\);
* the exact \(E_{00}-I\) response as the scalar-zero Omega endpoint in
  each chart;
* a specified compatible common-coloop residual with a surviving visible
  label \(c\in\{1,2\}\);
* nonzero curvature, the required endpoint-star conditions, and all nine
  literal pair rows; and
* the two finite all-\(h\) certificates.

Its conclusion is one scalar equality which contradicts the already
proved nonzero boundary defect.  This is strictly narrower than the
conjecture and does not assume a six-site extraction or cancel a common
power.  It is nevertheless unproved.  In particular, the current project
still needs a comparison/routing theorem for the general off-diagonal
common-coloop residual, or a separate argument which closes that residual
without entering the diagonal Omega packet.

No repository computation was needed beyond the displayed exact boundary
checks.  The whitespace/error check passes for the corrected source and
this audit.
