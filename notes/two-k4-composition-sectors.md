# Two-K4 composition: sector reduction and an equivariant obstruction

Consider two standard four-site ternary equality gadgets on shores
`L={0,1,2,3}` and `R={4,5,6,7}`.  Every one of the sixteen cross pairs may
carry an arbitrary `3 by 3` matrix.  The exact checker for this note is

```text
computations/verify_two_k4_composition_sectors.py
```

The final full-matrix step remains open.  This note gives a coordinate-free
sector formula for that step, an exact finite reduction of its cross-only
part, and a complete obstruction to the seven-parameter AGL-equivariant
subchart.

## 1. The 0/2/4-crossing formula

Label each four-site shore by `F_2^2`; the internal edge `uv` has colour
`kappa(uv) in {0,1,2}` corresponding to the nonzero difference `u+v`.
Allow its pure cell to have arbitrary weight `lambda_uv` on the left and
`rho_uv` on the right.  For shore words `a,b in {0,1,2}^4`, put

\[
 E(a)=\{uv:a_u=a_v=\kappa(uv)\},
 \qquad X(a,b)_{ui}=B_{ui}[a_u,b_i].
\]

Directly grouping the 105 perfect matchings by their number of cross edges
gives `(9,72,24)` matchings in the `(0,2,4)` sectors and the exact coefficient

\[
\begin{aligned}
F(a,b)={}&\operatorname {per}_4 X(a,b)\\
 &+\sum_{e\in E(a)}\sum_{f\in E(b)}
   \lambda_e\rho_f\,
   \operatorname {per}_2 X(a,b)[\bar e,\bar f]\\
 &+Z_L(a)Z_R(b).                                      \tag{1}
\end{aligned}
\]

Here `Z_L(a)` is zero unless `a` is constant; for `a=c^4` it is the
product of the two left internal weights in colour-`c`'s one-factor, and
similarly on the right.  Formula (1) remains valid when internal weights
vanish and is therefore the promised full-chart sector decomposition.

## 2. Thirty dead words and the 51-dimensional boundary

Among the 81 shore words, the compatibility census is

\[
 \#\{|E(a)|=0,1,2\}=(30,48,3).
\]

The three double-compatible words are exactly the constants.  If `E(a)` is
empty, the last two lines of (1) vanish for every `b`.  Any realization of
the target must consequently satisfy

\[
 \operatorname {per}_4X(a,b)=0
 \quad\text{for all 30 dead }a\text{ and all 81 }b,     \tag{2}
\]

and the transposed `81 by 30` family as well.  Thus the full four-crossing
tensor is supported on the `51 by 51` live coordinate rectangle.

There is an exact useful normal form for this support statement.  For each
of the six internal edges, take an arbitrary nine-entry response on the two
remaining sites and extend it by the edge-colour indicator.  These 54 edge
cylinders span *every* function supported on the 51 live words; their
incidence matrix has rank 51 and a three-dimensional kernel.  This turns
(2) into a finite edge-response decomposition without assuming symmetry or
nonzero internal weights.  What is still missing for the full chart is a
use of the fact that its 51-by-51 response comes from one common system of
four-by-four permanents and their complementary two-minors, rather than an
arbitrary edge-cylinder tensor.

## 3. Exact death of the AGL-equivariant chart

For unit internal cells, simultaneous `AGL(2,2)` equivariance leaves seven
cross parameters `a,b,c,d,e,f,g`, as in
`computations/explore_k4_k4_equivariant.py`.  Exact enumeration reduces all
6561 target equations to 288 distinct integer polynomials `P_w`.

Four equation differences suffice to split the system.  Two are

\[
\begin{aligned}
P_{00120000}-P_{00110000}
  &=-(d-g)^2(2f^2+1),\\
P_{00001200}-P_{00001100}
  &=-(e-g)^2(2f^2+1).                                  \tag{3}
\end{aligned}
\]

If `2f^2+1` is nonzero, (3) gives `d=e=g`.  After that substitution,

\[
\begin{aligned}
P_{00221111}-P_{00001111}&=-2bg-2g^2-1,\\
P_{02021111}-P_{00001111}&=-4bg-4g^2-1.
\end{aligned}
\]

Twice the first equation minus the second is `-1=0`, a contradiction.

It remains to treat `2f^2+1=0`.  Reduce the 288 equations in

\[
 R=\mathbb Q[a,b,c,d,e,f,g]/(2f^2+1).
\]

They involve exactly 190 reduced monomials.  Their `288 by 190` rational
coefficient matrix has rank 172, unchanged after adjoining the constant
row `1`.  Hence `1` belongs to their rational linear span in `R`.  Exact RREF
produces a certificate using 165 equations; the checker reconstructs that
coefficient vector and verifies all 190 columns over `Q`.  This is a linear
certificate in the quadratic quotient, not a probabilistic or modular
Groebner calculation.

Therefore the seven-parameter AGL-equivariant two-K4 chart has no complex
point.  Numerical complex searches agree, stopping at maximum residual about
`0.59`, but are not used in the proof.

## 4. Frontier

The full 144-parameter unit-cross chart showed only a diverging numerical
border trajectory (one representative run ended at loss about `1.50015`,
maximum residual one, and norm about `1018`).  Equations (1)--(2) are exact
for that full chart and for arbitrary internal pure-cell weights, but the
51-dimensional permanent/minor compatibility has not yet been converted to
a contradiction.  The subsequent exact dead-slice analysis in
[`two-k4-dead-slice-determinantal-boundary.md`](two-k4-dead-slice-determinantal-boundary.md)
does prove that every putative point lies on
`product_(i,j) det(B_ij)=0`; in particular the full all-invertible stratum is
empty.  The later singular-boundary analysis proves more: every putative
point has at least two singular blocks; if it has exactly two, neither has
rank two, the pair `11` is impossible, and a remaining pair `10` has the
positional row/column support listed in
[`two-k4-exact-two-low-rank-normal-forms.md`](two-k4-exact-two-low-rank-normal-forms.md).
Thus this note closes the natural equivariant target and isolates the
nonlinear compatibility still needed on the sparse singular-block boundary;
it does not claim a full-chart proof.
