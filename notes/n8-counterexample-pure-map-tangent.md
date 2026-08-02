# The pure-map tangent at the eight-site mixed torus

## Outcome

Let

\[
  \pi:V(I_{\mathrm{mix}})\longrightarrow\mathbb A^3,
  \qquad
  x\longmapsto(H_0(x),H_1(x),H_2(x))
\]

be the pure-coefficient map.  On the five-parameter torus family of
`aa4a731`, its value is \((0,0,1)\).  The exact generic tangent calculation
gives

\[
  \operatorname{rank}J_{\mathrm{mix}}=196,
  \qquad \dim T V(I_{\mathrm{mix}})=252-196=56,
\]

and

\[
  \boxed{\operatorname{rank}
  (d\pi|_{T V(I_{\mathrm{mix}})})=1.}
\]

The image of the tangent map is the \(H_2\)-axis.  Neither missing pure
coefficient can turn on to first order along any deformation preserving all
mixed equations.

## Exact Kähler-differential certificate

Write \(H_w\) for the coefficient with colour word \(w\).  At every generic
point of the Laurent family, direct differentiation of the 105 matching
terms gives the covector identities

\[
  dH_0=e\,dH_{00000010},
  \qquad
  dH_1=a^{-1}dH_{11000111}.
\]

Both words on the right are mixed.  Hence, in the cotangent quotient by the
mixed conormal,

\[
  [dH_0]=[dH_1]=0.
\]

The four coordinates appearing in \(dH_2\) are

```text
0722 1422 2322 5622
```

and every mixed differential has zero entry in all four of these columns.
Each corresponding standard coordinate direction is therefore a mixed
tangent vector, while \(dH_2\) evaluates to one on it.  Thus
\([dH_2]\ne0\), proving that the rank is exactly one rather than zero.

It follows immediately that every \(2\times2\) pure wedge vanishes in the
mixed cotangent quotient:

\[
  [dH_0\wedge dH_1]
  =[dH_0\wedge dH_2]
  =[dH_1\wedge dH_2]=0.
\]

This is the requested local Kähler/Fitting certificate.  It is an exact
identity on the whole five-parameter family, not merely a modular rank
observation.

## Why the Jacobian rank is generic

At the rational specialization \(a=b=c=d=e=1\), only 1,312 of the 6,558
mixed Jacobian rows are nonzero.  Sparse rational elimination gives rank
196 exactly, with a \(\{\pm1\}\)-valued row basis.

The checker also reconstructs port weights for each of the five parameters.
Every Laurent exponent on a nonzero coordinate is a sum

\[
  \lambda_{u,a}+\lambda_{v,b}.
\]

Thus varying \(a,b,c,d,e\) is a subtorus of the 24-port torus action.  By
multihomogeneity,

\[
  J_{\mathrm{mix}}(t\cdot x)
  =D_{\mathrm{rows}}(t),
   J_{\mathrm{mix}}(x),
   D_{\mathrm{columns}}(t),
\]

where both diagonal matrices are invertible.  The rank 196 and tangent
dimension 56 are therefore constant at every generic point of the Laurent
family.

## The relevant pure-product saturation on this stratum

The boundary-product radical containment is false, but the conjecturally
relevant question is instead whether

\[
  H_0H_1H_2\in\sqrt{I_{\mathrm{mix}}}.
\]

On the exceptional 18-extra coordinate torus itself, this stronger
three-pure saturation is empty for a very short reason.  After zeroing all
coordinates outside its support, one has the literal polynomial identity

\[
  H_{00000000}=H_{21000012}.
\]

The right side is a mixed generator.  Therefore localizing this stratum at
\(H_0H_1H_2\) makes the mixed ideal the unit ideal.  The parametrized torus
chooses the branch where \((H_0,H_1,H_2)=(0,0,1)\); colour-permuted copies
give analogous one-pure strata.

This does **not** yet prove the pure-product radical containment on the
entire 60-edge chart, much less in the full 252-variable ring.  It proves it
on the exact torus stratum that defeated the boundary-product shortcut.

## Geometric interpretation

The five displayed parameters are port-torus directions, not five new
intrinsic moduli of the mixed fibre.  The full mixed tangent space is much
larger, of dimension 56, yet both zero pure coefficients are conormally
locked.  Any branch through this family on which all three pure
coefficients become nonzero would have to turn on \(H_0\) and \(H_1\) only
at second or higher order.  In particular, there is no first-order gluing
of this family to an all-pure branch.

The tangent calculation does not decide whether the colour-permuted
one-pure tori belong to a common larger irreducible component.  It sharply
narrows the next test: compute second-order obstructions, or saturate the
whole 60-edge mixed ideal by \(H_0H_1H_2\).  A first-order search cannot
find the desired all-pure deformation here.

## Reproduction

```sh
python3 computations/verify_n8_counterexample_pure_tangent.py
python3 -O computations/verify_n8_counterexample_pure_tangent.py
python3 -I computations/verify_n8_counterexample_pure_tangent.py
python3 -S computations/verify_n8_counterexample_pure_tangent.py
```

The frozen ledger contains the exact Jacobian rank, port weights, two
conormal identities, four surviving \(H_2\) tangent columns, wedge rank, and
the local pure-product saturation identity.
