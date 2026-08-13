# The universal response shear first fails on a toric rectangle

## Exact result

The universal centered occurrence deformation is algebraically trivial on
the free ninety-coordinate occurrence space.  For an augmentation-zero
parameter `z`,

\[
 M_z=I-\mathbf1z^{\mathsf T},\qquad
 M_z^{-1}=I+\mathbf1z^{\mathsf T},\qquad
 \det M_z=1,
\]

and

\[
 \mathbf1^{\mathsf T}M_zu=R-90z^{\mathsf T}u.       \tag{1}
\]

Thus the obstruction isolated by the universal KS family is not abstract
flatness or existence of a free occurrence-space augmentation.  It is the
failure of this rank-one shear to lift through the physical monomial map

\[
 u_{i,j,M}=p_i s_j\prod_{e\in M}q_e.                 \tag{2}
\]

Checker:
[`verify_h3_universal_occurrence_shear_toric_lift_gate.py`](../computations/verify_h3_universal_occurrence_shear_toric_lift_gate.py).

## The first literal obstruction

Fix endpoint sites `0,1` and the residual matchings

```text
x=23|45,   y=24|35.
```

Put `A=p0*s1` and `B=p1*s0`.  The four occurrence monomials form a rank-one
rectangle

\[
 \begin{pmatrix}Ax&Ay\\Bx&By\end{pmatrix}.
\]

Their exponent vectors satisfy the exact toric relation

\[
                 u_{Ay}u_{Bx}-u_{Ax}u_{By}=0.        \tag{3}
\]

The infinitesimal rank-one shear is constant on the four occurrence
coordinates.  Differentiating (3) on that constant vector gives

\[
 Bx+Ay-By-Ax
 =(B-A)(x-y)
 =(p_1s_0-p_0s_1)
   (q_{23}q_{45}-q_{24}q_{35}).                      \tag{4}
\]

Equation (4) is the first physical-presentation proper face.  It is the
unique endpoint-orientation by residual-matching interaction character on
this four-corner block.  Rows depending only on the endpoint orientation or
only on the matching aggregate kill it, in agreement with the pinned
physical-`q` audit.

## Exact local fork

For all three residual matchings write the block as

\[
 \begin{pmatrix}
  Ax_0&Ax_1&Ax_2\\
  Bx_0&Bx_1&Bx_2
 \end{pmatrix}.
\]

The three defining-minor differentials on the constant shear are

\[
                   (B-A)(x_j-x_k),\qquad j<k.        \tag{5}
\]

Over the characteristic-zero theorem field, all three vanish exactly when

\[
                  \boxed{A=B\quad\text{or}\quad
                         x_0=x_1=x_2.}               \tag{6}
\]

The first arm is endpoint-orientation dark; the second is
residual-matching-standard dark.  These are precisely the two coefficient
modules already exposed by the endpoint-parity and matching-semidir-ect
audits.  Formula (6) does not itself provide their physical word/fine/`q`
landing.

## The aggregate response equation does not force the fork

There is an exact point of the selected response hypersurface with

```text
p=(1,1,0,0,0,0),
s=(-1,1,0,0,0,0),
all q_e=1 except q24=2.
```

At this point the complete ninety-term response is zero and the marked
occurrence `p0*s1*q23*q45` equals one.  The Jacobian of the ninety physical
occurrence monomials with respect to the twelve endpoint and fifteen edge
variables has rank `12`.  Adjoining the constant occurrence shear raises
the rank to `13`.  Hence the shear is not a physical `p,s,q` tangent, even
on the aggregate response fibre.

This is a response-fibre guard, not a complete GHZ source counterexample.
It proves that the aggregate source row alone cannot manufacture the
required connection.

## Consequence

The highest-leverage local theorem is now sharper:

> Construct one physical PP/Hasse lift of the centered occurrence shear
> whose proper faces include every mixed endpoint-by-matching toric
> differential (4), or show that the first nonzero such differential lands
> in an already typed determinant/private-site fan or Fredholm terminal.

The free universal family supplies the coefficient connection, endpoint
and matching covariance, and flat D4 transport.  What remains is exactly
the lift of that connection through (2), with the toric conormals,
word/fine/repeated degree, cap, ridge, and physical `q` retained.

## Scope

The rank-one trivialization, toric binomial, local tangent criterion, and
response-fibre rank jump are exact at `h=3`.  The result does not claim that
the displayed response point satisfies every GHZ source equation, promote
the conormal (4) to a physical terminal, or construct the AugP2/E14 landing.

Run normally, optimized, and isolated/no-site.  Frozen ledger SHA-256:

```text
113f412026d6ae9f5907d8ed9075ca85a76bcda2b33c5c3f5288f7d2c578a2c2
```
