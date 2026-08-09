# Reciprocal pair rows have a pure-anchor Hasse--Bianchi identity

## Exact identity

Let

```text
Q      = q^[h],
r_ij   = p_i s_j,
R_ij   = r_ij q^[h-1],
K_ij;kl = r_ij r_kl q^[h-2].
```

For a direct pair block `d`, the complete pair-row defects are

```text
E_ij = d_ij Q + R_ij - delta_ij X_i.                     (1)
```

Use the Hasse direction which changes the residual quadratic form by
`q -> q+t r_kl`, while keeping the ports and direct block fixed.  Then

```text
D_kl E_ij = d_ij R_kl + K_ij;kl.                         (2)
```

Because multiplication of the source-labelled port quadratics is
commutative,

```text
K_ij;kl = K_kl;ij.
```

Antisymmetrizing (2) and substituting the complete target rows at the base
source gives the exact typed Bianchi identity

```text
D_kl E_ij - D_ij E_kl
  = d_ij R_kl - d_kl R_ij
  = d_ij delta_kl X_k - d_kl delta_ij X_i.               (3)
```

The quadratic `q^[h-2]` channel cancels exactly in (3).  This is the
smallest coefficient-complete identity linking `q^[h]`, all nine first
responses, and the quadratic port insertion.

## Reciprocal coordinate block

Suppose the reciprocal pair is the literal coordinate cell

```text
d = lambda E_ab.
```

If `a!=b`, take `(ij)=(a,b)` and `(kl)=(c,c)`.  Equation (3) gives

```text
D_cc E_ab - D_ab E_cc = lambda X_c                  for c=0,1,2.  (4)
```

Thus an off-diagonal reciprocal cell exposes every pure target anchor.  If
`a=b`, the same formula exposes the two anchors with `c!=a`; the target with
`c=a` cancels antisymmetrically.  This exactly matches the reciprocal
selector-accessibility table by a different, source-typed calculation.

At `N=8`, all terms in (2) are literal six-site top tensors:

```text
Q has degree 6,
R_ij has degree 6,
K_ij;kl = p_i p_k s_j s_l q^[1] has degree 6.
```

No projection or output-only invariant is used.

## The remaining logical gate

Equation (3) is **not** yet an ideal-membership contradiction.  The source
equations say `E_ij=0` at the given source point.  They do not say that the
residual source variations `q -> q+t r_kl` are tangent to the GHZ fibre.
Consequently one cannot set the two Hasse derivatives on the left of (3) to
zero merely because their base defects vanish.

This is exactly what the two reciprocal insertion guards exhibit:

1. a nonzero `K` can be the derivative defect while all original port-arm
   cofactors are dead; and
2. all nonzero mixed permanents can lie on zero `q^[h-2]` cofactors even
   when the three diagonal first-response cofactors are active.

The pure anchor in (4) proves that at least one of the two Hasse directions
is non-tangent.  It does not select an active good rank-one overlap or a cubic
pair without a theorem identifying the non-tangent derivative with an
original source deformation.

## Precise next lemma

A uniform reciprocal closure can now be stated sharply:

> **Hasse lift target.** For one diagonal row `cc` accessible to a reciprocal
> coordinate cell `ab`, construct source variations lifting both residual
> directions `r_cc` and `r_ab` modulo target gauge, with correction terms
> supported on active original port arms.  Their commutator must either be
> tangent, contradicting (4), or expose an active doubly-injective rank-one
> overlap / adjacent-cubic pair.

Any proposed proof must explicitly produce these corrected source variations.
Ordinary differentiation of equations at a point, the algebraic permanent
no-go, or support incidence alone does not do so.

Equivalently, the open datum is a Kodaira--Spencer/connection lift from the
residual `q`-direction to the full source fibre.  The right-hand side of (4)
is its exact curvature.

## Scope

This note supplies a source-faithful typed identity and isolates the precise
tangent-lift obstruction.  It neither proves the reciprocal branch nor gives
an exact Krenn counterexample.  An exact GHZ source-level counterexample to
the Hasse lift would itself be highly consequential and is not constructed
here.

## Reproduction

```text
python3 computations/verify_reciprocal_response_hasse_bianchi.py
python3 -O computations/verify_reciprocal_response_hasse_bianchi.py
```
