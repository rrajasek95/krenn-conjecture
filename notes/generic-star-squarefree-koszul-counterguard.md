# The generic-star Koszul complex is exact but not source-faithful

## Outcome

After fixing a site \(v\) and a generic covector \(\alpha\), the zero
one-slice remainder does have the proposed pairwise antisymmetric Koszul
form.  The statement is exact once zero routes are omitted.

It does **not** supply a support-reducing source deformation.  The Koszul
coefficients are constructed only after contraction by \(\alpha\), generally
have negative degree in incident-star coordinates, and factor the artificial
remainders rather than the actual matching cofactors.  A four-site exact
tensor counterguard shows a contracted Koszul cancellation whose full
source-row residual is nonzero.  This freezes outcome (b), not a Krenn
counterexample.

## 1. Subtracting the three pure lifts

Fix \(v\) and use the active rank-one witnesses from
`generic-covector-segre-rankone-incidence-audit.md`.  For color \(a\), write

\[
 A_{v u_a}=c_a\otimes e_a^{(u_a)},\qquad
 p_{u_a}(\alpha)=\lambda_a e_a,qquad \lambda_a=\alpha(c_a).
\]

On the generic open set where every \(\lambda_a\ne0\), put

\[
 P_{u_a}=\frac{\alpha(e_a)}{\lambda_a}
          e_a^{\otimes(B\setminus\{v,u_a\})}.              \tag{1}
\]

Set \(R_{u_a}=C_{u_a}-P_{u_a}\), and set \(R_u=C_u\) on every
other active route.  The contracted star identity becomes

\[
                       \sum_{u}p_u^{(u)}R_u=0.             \tag{2}
\]

The denominators in (1) are already a warning: this is a localized identity,
not a polynomial deformation of the source.

## 2. Exact square-free Koszul lemma

Let \(I\) be the set of retained routes, with each \(p_u\in V_u\) nonzero.
For

\[
 C_1=\bigoplus_{u\in I}\bigotimes_{x\ne u}V_x,
 \qquad C_0=\bigotimes_xV_x,
\]

define

\[
 \delta_1((R_u))=\sum_up_uR_u.                            \tag{3}
\]

Then \(\ker\delta_1\) is the image of the pairwise map

\[
 R_u=\sum_{w\ne u}p_wD_{uw},\qquad D_{uw}=-D_{wu},         \tag{4}
\]

where \(D_{uw}\in\bigotimes_{x\ne u,w}V_x\).

To see this, choose \(V_u=\langle p_u\rangle\oplus Q_u\) and split by the
set \(S\) of sites using a \(Q\)-factor.  If \(k=|I\setminus S|\), the
corresponding block of (3) is the summation map from \(k\) copies of the
same coefficient space.  Its kernel has dimension \(k-1\) and is exactly
the image of the oriented edge-incidence matrix of the complete simplex on
those \(k\) copies.  This is (4).  Tensor factors at sites outside \(I\) are
passive coefficients, so the proof also covers inactive physical sites.

Zero routes must be omitted.  If \(p_z=0\) but the \(z\)-summand is retained,
an arbitrary \(R_z\) in the product of the \(Q_w\)'s is killed by
\(\delta_1\) and is not divisible by any active \(p_w\).  The resulting
homology has dimension \(\prod_w\dim Q_w\) (equal to \(2^{|I|}\) in the
ternary case).  For generic \(\alpha\), every nonzero active incident map
avoids its kernel; identically zero or cofactor-zero routes contribute no
summand and are omitted.

The checker reconstructs these simplex ranks through eight active sites and
audits the zero-route homology exactly.

## 3. Why \(D_{uw}\) is not a matching cofactor

The actual cofactor

\[
                  C_u=H_{B\setminus\{v,u\}}(A)            \tag{5}
\]

contains no block incident to \(v\).  It has star multidegree zero with
respect to every \(A_{vw}\).  In contrast, \(p_w(\alpha)\) has positive
degree in \(A_{vw}\).  Thus a polynomial identity

\[
                       C_u=\sum_wp_wD_{uw}                 \tag{6}
\]

with nonnegative star degrees cannot hold multihomogeneously unless the
relevant component is zero.  A localized Koszul solver evades this only by
putting inverse incident coordinates into \(D_{uw}\).  Scaling
\(A_{vw}\mapsto tA_{vw}\) leaves (5) fixed but forces the corresponding
numeric divisor to scale as \(D_{uw}\mapsto t^{-1}D_{uw}\).

There are two further mismatches:

* (4) factors the remainders \(R_u\), not the actual \(C_u\); the witness
  remainders contain the artificial denominators (1); and
* entry-minimality needs a full tensor relation
  \(\sum_u\delta A_{vu}\otimes C_u=0\) before contracting the \(V_v\)
  factor.  Equation (2) lies only in its image under \(\alpha\).

## 4. Exact contraction counterguard

Take four tensor sites \(0,1,2,3\), fix
\(\alpha=(1,1,1)\) at site 0, and use

\[
                 p_1=e_0,qquad p_2=e_1,qquad p_3=e_2.
\]

With \(D_{12}=e_2^{(3)}\), put

\[
 R_1=e_1^{(2)}e_2^{(3)},\qquad
 R_2=-e_0^{(1)}e_2^{(3)},\qquad R_3=0.                    \tag{7}
\]

These are an exact pairwise Koszul cancellation.  Adding the three pure
lifts gives cofactors

\[
\begin{aligned}
 C_1&=e_0^{(2)}e_0^{(3)}+e_1^{(2)}e_2^{(3)},\\
 C_2&=e_1^{(1)}e_1^{(3)}-e_0^{(1)}e_2^{(3)},\\
 C_3&=e_2^{(1)}e_2^{(2)}.
\end{aligned}                                             \tag{8}
\]

The contracted star is exactly \(\Delta_3\).  Now restore independent left
factors \(e_0,e_1,e_2\) at site 0.  The full star tensor is

\[
 \Delta_4+(e_0-e_1)^{(0)}e_0^{(1)}e_1^{(2)}e_2^{(3)}.     \tag{9}
\]

The residual in (9) is nonzero, although \(\alpha\) kills it.  Hence the
contracted Koszul relation is not a full source-row relation and supplies no
entry-removing deformation.  This example is an exact tensor counterguard
to the inference; it is not asserted to satisfy the full matching-cofactor
provenance and is not a Krenn counterexample.

## 5. Verdict and reproduction

The square-free Koszul classification is a correct description of the
generic contracted remainder.  Its arbitrary \(D_{uw}\)'s forget exactly
the two data needed for descent: independence of cofactors from the incident
star and the uncontracted color at \(v\).  A continuation would need a
simultaneous three-covector Koszul compatibility theorem whose divisors have
nonnegative source multidegree and lie in the smaller hafnian-cofactor image.

```sh
python3 computations/verify_generic_star_squarefree_koszul_counterguard.py
python3 -O computations/verify_generic_star_squarefree_koszul_counterguard.py
```
