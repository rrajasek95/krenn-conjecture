# Independent audit of the common-coloop \(A\)-to-\(D(z)\) overlap attack

## 1. Verdict

**PASS, with the stated limited scope.**  I independently checked
[the overlap attack](common-coloop-a-to-D-overlap-attack.md) against
[the controlling affine-fibre identity](common-coloop-clean-cap-affine-fibre.md).
The projected equation, the attainable-scalar obstruction, both rational
coefficients in the guard, and the consecutive-power realization are exact.
The guard really does disprove the proposed missing-row
\(A\)-to-second-polar transfer.

It does **not** prove or disprove the literal full-nine common-coloop lemma.
In particular, it supplies only the missing diagonal row, not the two other
diagonal target rows or the second-chart overlap data.  Its effect on the
proof frontier is therefore negative but useful: a proof cannot infer
\(\rho_t\bar r^{[2]}=0\) from the displayed \(A\)-annihilations and the
missing curvature anchor alone.

The audited source hashes were

```text
485c7f6648436b99a0cd907ab36ef658c23fd1b31e2d375e7169b894c68c23b9  common-coloop-a-to-D-overlap-attack.md
755ed1eef492e558a5fa9f9fbc7279957fbfdde8f6a74edb84ce752c61d86150  common-coloop-clean-cap-affine-fibre.md
```

## 2. Projection and coupling check

The controlling clean error is

\[
 \mathcal E(K_0+L)
  =(z\rho+\chi+w)D_{\bar K}(z)
       -z^{h-1}\bar r\rho q_0^{[h-2]},
\]

where

\[
 D_{\bar K}(z)=
 \sum_{j=1}^{h-1}z^{h-1-j}\bar r^{[j]}q_0^{[h-1-j]}.
\]

In the aligned one-corner branch, \(w_t=0\).  The \(j=1\) summand in
\(z\rho_tD_{\bar K}(z)\) is exactly
\(z^{h-1}\rho_t\bar r q_0^{[h-2]}\), so it cancels the physical-target
term with coefficient one.  The remaining missing-axis equation is therefore

\[
 \Theta_t(z)=\chi_tD_{\bar K}(z)
   +\rho_t\sum_{j=2}^{h-1}
       z^{h-j}\bar r^{[j]}q_0^{[h-1-j]}.
\]

No ordinary binomial coefficient is missing.  At \(h=3\), this gives

\[
 D_{\bar K}(z)=z\bar r q_0+\bar r^{[2]},\qquad
 \Theta_t(z)=\chi_tD_{\bar K}(z)+z\rho_t\bar r^{[2]}.
\]

Under \(\chi_t=0\), the claimed reduction
\(\Theta_t(z)=z\rho_t\bar r^{[2]}\) follows exactly.  The theorem using
the attainable set \(Z_{\rm att}\) is only a one-way obstruction, as the
source says.  It never treats \(z\) and \(w\) as independent: \(z\) remains
the affine functional

\[
 z=\sigma_0+c^{\mathsf T}a\eta+\xi^{\mathsf T}ad,
\]

and \(w=u\bar S(\eta)+\bar P(\xi)v\).  Thus the projection is valid even
though it forgets the remaining coupled equations.

The fixed diagonal equation also checks:

\[
 (z\rho_t+\chi_t)A+\rho_t\bar r q_0^{[h-2]}
     =\kappa_t^0Y_t.
\]

If the scalar varies on the fibre, its coefficient indeed forces
\(\rho_tA=0\).  If the scalar is fixed, the attack does not make that
inference and instead assumes the needed vanishing in its conditional
subcase.

## 3. Exact rational guard audit

Work on the five odd sites and retain the distinction between the axes
\(a_i\) and \(x_i\).  For

\[
 q_0=x_0x_1+x_0x_2+x_0x_3+x_0x_4+a_1a_2
\]

the only disjoint pairs of displayed edges are
\((x_0x_3,a_1a_2)\) and \((x_0x_4,a_1a_2)\).  Consequently

\[
 A=q_0^{[2]}=x_0a_1a_2x_3+x_0a_1a_2x_4.
\]

With

\[
 \ell=-x_0-x_1-x_2-x_3+x_4,
 \qquad \rho_t=-x_1-x_2,
\]

the first term of \(A\) can only be completed by \(+x_4\), while the
second can only be completed by \(-x_3\).  Hence \(\ell A=0\).
Both terms of \(A\) already occupy sites \(1,2\), so \(\rho_tA=0\).
Thus \(pA=sA=\rho_tA=0\) for \(p=\ell/4\) and \(s=\ell\).

I also recomputed the two nontrivial products in the site-square-zero
algebra.  Every surviving degree-five term has to occupy all five sites,
and the \(a_1a_2\) edge cannot survive multiplication by \(\rho_t\).
For the four all-\(x\) star edges, the contributions to
\([\rho_t\ell^2q_0]_{Y_t}\) are respectively

\[
                         2,\quad2,\quad4,\quad-4,
\]

whose sum is \(4\).  The factor \(1/4\) in \(\bar r=ps=\ell^2/4\)
therefore gives

\[
                         \rho_t\bar r q_0=Y_t.
\]

For the second divided power,

\[
 \bar r^{[2]}={\bar r^2\over2}={\ell^4\over32}.
\]

Choosing the \(\rho_t\) term at site \(1\) or site \(2\) contributes
\(24\) in each case, so

\[
 [\rho_t\ell^4]_{Y_t}=48,
 \qquad
 \rho_t\bar r^{[2]}={48\over32}Y_t={3\over2}Y_t.
\]

This is a full tensor equality, not merely a selected coefficient check:
all nonzero products have degree five on five sites and use only the
\(x_i\) axes.  An independent sparse-dictionary multiplication reproduced
exactly

```text
A              = x0 a1 a2 x3 + x0 a1 a2 x4
ell*A          = 0
rho_t*A        = 0
bar_r*A        = 0
rho_t*bar_r*q0 = Y_t
rho_t*bar_r^[2]= (3/2) Y_t
```

Finally, \(Y_t\notin\mathcal R_1A\): every monomial in the image retains
the occupied axes \(a_1,a_2\) at sites \(1,2\), whereas \(Y_t\) has
\(x_1,x_2\) there.  Cancellation cannot create a coordinate that is absent
from every image monomial.

## 4. Consecutive-power and physical-row check

After adjoining the exposed site and putting

\[
 q=q_0+\epsilon\rho_t,
\]

the site-square-zero identities give

\[
 q^{[2]}=A+\epsilon\rho_tq_0,
 \qquad
 q^{[3]}=q_0^{[3]}+\epsilon\rho_tA=0.
\]

Here \(q_0^{[3]}=0\) by site count and \(\rho_tA=0\).  Moreover
\(\bar rA=(\ell^2/4)A=0\), since \(\ell A=0\).  Hence the decomposable
endpoint response supplies the literal missing diagonal row

\[
 \bar r q^{[2]}=\epsilon\rho_t\bar r q_0
     =\epsilon Y_t=X_t.
\]

For \(F_z=zq+\bar r\), the divided-power expansion is

\[
 F_z^{[3]}=z^2\bar r q^{[2]}+zq\bar r^{[2]}+\bar r^{[3]}.
\]

The last term and the off-site part \(q_0\bar r^{[2]}\) vanish by site
count.  Therefore

\[
 F_z^{[3]}-z^2X_t
   =z\epsilon\rho_t\bar r^{[2]}
   ={3\over2}zX_t.
\]

The only clean scalar is \(z=0\), which is inactive.  In an aligned
common-coloop fibre, a tangent response has no \(e_t^{(x)}\)-component, so
it cannot cancel this defect.  If \(\sigma|_{\mathcal T}\ne0\), all
scalars are attainable; if it vanishes, the unique attainable scalar is
either inactive or excluded.  These two cases exhaust the affine image.

## 5. Falsification attempts and exact logical effect

The following possible failure modes were checked and do not invalidate
the note.

1. **Divided-power normalization:** the factors \(1/4\) and \(1/32\)
   give coefficients \(1\) and \(3/2\) exactly; no hidden factorial is
   missing.
2. **Unlisted monomials:** site count and the death of the \(a_1a_2\)
   edge against \(\rho_t\) leave only \(Y_t\) in both guarded products.
3. **Fake common powers:** \(A\), \(q^{[2]}\), and \(q^{[3]}\) are the
   literal consecutive divided powers of the displayed single quadratic.
4. **Fake endpoint response:** \(\bar r=ps\) is a genuine product of the
   displayed endpoint linear forms.
5. **Free scalar/tangent choice:** the theorem uses only the necessary
   missing-axis projection at the same attainable \(z\); it does not solve
   for an arbitrary \((z,w)\).
6. **Overpromotion to full nine:** the note explicitly withholds the two
   other diagonal target rows, a complete direct matrix, and the
   second-chart overlap constraints.  Those omitted hypotheses could still
   force the needed second-polar relation.

Thus the attack does not shorten the positive proof spine by closing a
branch.  It closes one proposed shortcut and sharpens the remaining task:
any successful common-coloop argument must use the omitted full-nine or
two-chart data **before** reducing everything to multiplication by \(A\).
