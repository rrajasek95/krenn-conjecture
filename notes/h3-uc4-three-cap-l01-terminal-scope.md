# Capping the invariant C4 tail leaves the pointed chart scalar

## Verdict

The protected-zero augmented signature of

```text
U_C4[D,Q01;2345] -> H2345
```

does not make `U_C4` a physical relative source cell. Its normalized
three-matching occurrence augmentation is one, but source provenance is a
domain statement, not another output coordinate.

The exact cap/reinsertion test leaves the already isolated scalar

\[
 L_{01}=(2Dq_{01}-p_0s_1-p_1s_0)
        (q_{23}q_{45}+q_{24}q_{35}+q_{25}q_{34}).     \tag{1}
\]

Checker:
[`verify_h3_uc4_three_cap_l01_terminal_scope.py`](../computations/verify_h3_uc4_three_cap_l01_terminal_scope.py).

## The three-cap calculation

Write

\[
 A=Dq_{01},\qquad B=p_0s_1,\qquad C=p_1s_0,
 \qquad H=H_{2345}.
\]

A lower symmetric-C4 section capped in the three endpoint charts would give
cells with degree-zero boundaries `AH,BH,CH`. Their complete and centered
combinations are

\[
 C_R=C_A+C_B+C_C,\qquad C_L=2C_A-C_B-C_C,
\]

and hence

\[
                  dC_R=R_{01},\qquad dC_L=L_{01}.     \tag{2}
\]

Thus a source-valid covariant three-cap family would indeed solve the
pointed scalar. It is not supplied by the lower `U_C4` signature: equation
(2) is exactly the missing construction.

The product rule exposes why. Even for the `A` cap,

\[
 d(AU)=A\,dU+(dA)U,
 \qquad dA=(dD)q_{01}+D(dq_{01}).                    \tag{3}
\]

The lower values `target=ainc=q=Eq=W=ores=ridge=0` say nothing about the two
new faces in (3). Combining the three caps gives the endpoint-even first-PP
packet `(2,2,-1,-1,-1,-1)`, not zero.

## Exact complete-row and Euler obstruction

The checker reconstructs all 105 perfect matchings of the physical response
`K8`. The local three-cap block contains nine terms and its complement has
96. It verifies

```text
rank(edge/matching incidence)                   21
rank(incidence + complete response)             21
rank(incidence + L01)                           22.
```

Therefore neither the complete response nor any constant coordinate Euler
field constructs (1). The exact twelve-occurrence covector from the fixed-
chart reset kills all 28 Euler rows and the complete response but reads one
on `L01`.

A single capped `DQ` section also does not suffice. The identity

\[
                        L_{01}=3AH-R_{01}             \tag{4}
\]

requires isolation of the nine-term local response block. In the full
polynomial, `R=R01+Rrest` with 96 terms in `Rrest`; projecting them away is
not a source operation.

## Chart swaps retain rather than kill the scalar

The presentation-safe chart graph uses

\[
 B-A-u_1=0,\qquad C-A-u_2=0.                         \tag{5}
\]

Modulo (5),

\[
                         [L_{01}]=-[u_1+u_2]H.        \tag{6}
\]

Setting `u1=u2=0` makes the raw chart action contract the scalar, but it
also imposes `A=B=C` and collapses the two-dimensional response fibre. The
honest endpoint groupoid therefore organizes the three caps; it does not
provide their pointed fixed-chart totalization.

The logarithmic Euler, raw chart-fold, and lower-tail shortcuts all stop at
the same datum. This is not three separate gates.

## The coloop-unit pivot does not remove the pointed face

The stronger coloop equations are

\[
 dC+U=1,\qquad \alpha C+V=0,\qquad \alpha C_c=1,
 \qquad \alpha U-dV=\alpha.                          \tag{7}
\]

Inverting `alpha` removes a denominator, but differentiating the last
identity in two chart directions `x,y` gives

\[
\begin{aligned}
0={}&\alpha U_{xy}-dV_{xy}
 +\alpha_xU_y+\alpha_yU_x+\alpha_{xy}(U-1)\\
 &-d_xV_y-d_yV_x-d_{xy}V.                            \tag{8}
\end{aligned}
\]

The differentiated coloop equation controls the analogous `alpha/Cc`
terms. It does not control `U_x,U_y,V,V_x,V_y`, nor does it select the
nine-term `R01` block inside `U` or `V`. Thus the pivot can provide the
leading common-tail coefficient only together with the same product-rule
faces already exposed by the three-cap audit.

There is an integrated sharp guard, not just a tangent warning. Take

```text
alpha=1, d=C=V=0, Cc=1, U=1,
f=1/2+t, g=1/2-t, U=f+g.
```

All four identities (7) hold polynomially in `t`, so every Hasse derivative
of them vanishes. Nevertheless `df/dt=1`. Hence the unit pivot plus its full
Hasse tower still does not manufacture a selected occurrence or the `R01`
projector. A physical chart/Hasse totalization must retain this redistribution
face; dividing by `alpha` cannot erase it.

## Augmented signature and terminal scope

The exact signatures at the two stages must be kept separate:

```text
lower U_C4:
  occurrence augmentation  1
  target, ainc, q, Eq       0,0,0,0
  W, ores, ridge            0,0,0

centered cap face L01:
  occurrence augmentation  0
  target                    0
  ainc/q/Eq/W/ores/ridge    undefined before physical placement.
```

Target zero follows from `3*(2-1-1)=0`; it does not set the other augmented
rows. In particular, one must not transfer the lower column's zero `ainc/q`
values through (3) without a physical chain map.

After a literal source-labelled response-to-relative placement in the same
word, fine, repeated and `Hasse[2](DQ,PS,PS)` grade, the committed augmented
dual theorem is exhaustive:

```text
L01 in the protected physical image  -> protected-zero filler;
L01 outside that image               -> augmented terminal.
```

For local cap-corner values `mu_j`, the terminal extension is

```text
q=ainc=Eq=0,
target_j=W_j=-mu_j,
ores_j=mu_j,
ridge=-sum_j alpha_j*mu_j,  alpha=(-1,1,1,-1).
```

There is no third branch. But this alternative is not available before the
same-grade inclusion is constructed: the coefficient covector then has no
physical domain provenance.

## Shortest remaining theorem

Construct one source-labelled covariant three-cap/endpoint-even `C+`
totalization whose centered boundary is `L01` and whose first PP faces retain
the actual word/fine/repeated grade, physical `q`, anchor, `W`, labelled
ridge, eta and sigma. This single object simultaneously supplies the local
block projector and caps the symmetric `C4` lower seed. The existing
filler-or-terminal theorem then closes it automatically.

This result rules out construction from the named complete-row, constant
Euler, raw chart-swap, or uncapped lower-tail data. It does not exclude a
higher non-diagonal Spencer construction of the required three-cap family.

Run normally, optimized, and isolated/no-site. The checker pins every input
and records a frozen ledger digest.
