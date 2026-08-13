# The first generic `C_+` lower class is exactly `delta_+`

This note computes the first lower remainder of the generic root-even
Cartan orbit in the actual six-output order-two quotient.  It also records
why a beta-independent lower `B-4I` realization does not by itself extend
the orbit across `beta=0`.

Checker:
[`verify_h3_generic_cplus_lower_quotient_smith_gate.py`](../computations/verify_h3_generic_cplus_lower_quotient_smith_gate.py).

## 1. The diagonal input removes all generic parameters

On `alpha*beta != 0`, the two literal cap matrices satisfy the full matrix
identity

\[
 J_*=(\beta-2\alpha)J_1+(\beta+\alpha)J_2
     =-3\alpha\beta I.                                \tag{1}
\]

The cap polynomial is linear in its matrix input.  Therefore the normalized
first Cartan lower face is

\[
 \boxed{R_+=-{1\over3}(1+\rho)H_wd(P(I)).}             \tag{2}
\]

In particular (2) is independent of `alpha` and `beta`.  This is an
identity on the generic open set; it does not claim that the division by
`beta` extends integrally to the collision fibre.

## 2. The actual six-output lower quotient

The physical equivariant site-collapse comparison is already constructed
on thirteen of the fifteen trace labels.  Its complete landing is

\[
                  p=(3,2,3,3,2,3),                    \tag{3}
\]

whereas the uniform trace landing is

\[
                  t=(3,3,3,3,3,3).                    \tag{4}
\]

Thus the omitted rho-pair has total deficit

\[
 t-p=(0,1,0,0,1,0)=2v,
 \qquad v={B_1+B_4\over2}.                             \tag{5}
\]

After the divided pair normalization, the direct omitted-orbit image is
`v`.  In the same actual repeated `P3+K2` grade, the order-two
loop-resolution/product-rule coefficient is the complementary even average

\[
                 \ell={B_0+B_2+B_3+B_5\over4}.        \tag{6}
\]

Consequently the first relative lower coefficient of (2) is

\[
 \boxed{
 R_+^{\rm lower}=v-\ell
     ={(-1,2,-1,-1,2,-1)\over4}=\delta_+.}             \tag{7}
\]

Equation (7) is the desired comparison with `delta_+`.  It is exact in the
ordered `(B0,...,B5)` output quotient, not just up to rank or augmentation.
For endpoint adjacency `B_ep`,

\[
 B_{\rm ep}\delta_+=-2\delta_+,
 \qquad
 (B_{\rm ep}-4I)(-\delta_+/6)=\delta_+.                \tag{8}
\]

There is an important typing boundary.  The thirteen-label map in (3) is a
literal physical map.  The coefficient in (6) is the pinned actual-grade
loop-resolution shadow.  Equations (5)--(8) do not manufacture the missing
source cell on the omitted pair.  The separately audited natural lower
endpoint path has a nonzero mixed target-normal face and a one-endpoint
Hasse cross term.  A physical `C_+` orbit must carry those faces as well.

## 3. The first Eq faces are now explicit

There are two distinct Eq projections, and both must be retained.

First, the complete same-grade `M_v` combination realizes the lower
coefficient `delta_+`, but it ties that coefficient to the same labelled Eq
coefficient:

```text
known packet:    (lower, Eq) = (delta_+, delta_+),
required bridge: (lower, Eq) = (delta_+, 0).
```

Thus the smallest complete-column correction is

\[
                       (0,-\delta_+).                  \tag{9}
\]

For the integral vector `D6=4 delta_+`, the primitive covector

\[
 \chi_D=\sum_i(D6)_i(\operatorname{private}_i-operatorname{Eq}_i)
\]

kills every tied column and reads `12` on `(D6,0)`.  So (9) is a genuine
complete-row obligation, not an optional normalization.

Second, the root-decorated Cartan product rule requires the Spencer face

\[
       +2D_{\rm root}(H_0-u)e_{\rm Eq}\otimes v,
 \qquad D_{\rm root}=(-1,1,-1,1).                     \tag{10}
\]

Its eight nonzero coefficients are opposite to the mixed target packet
`-2 D_root tensor v`.  Algebraically, (10) is a coefficient projection of
the canonical derived reduced-Eq Koszul/Spencer cone.  Physically it is not
yet placed in the omitted-pair word/fine/repeated grade.  The old fourth
Hasse face has reduced coordinates `(Eq,w)=(1,1)`, while the desired final
boundary is `(0,1)`; their difference is the pure Eq face `(-1,0)`.

Hence no new polynomial Eq identity is needed.  What remains is the
source-labelled descent of the already identified Spencer coefficient
together with (9), the target normal, residue, protected, and Hasse faces of
one full `C_+` orbit.

## 4. A lower `B-4I` cell does not force beta saturation

It is tempting to use the beta-independence of (2), or of the lower
preimage in (8), to specialize directly to `beta=0`.  The Smith packet
shows why that is invalid.

Use rows

```text
primitive descent defect, rho0, rho2, independent lower B-4 coordinate.
```

The known unary and cap columns, with an arbitrarily granted
beta-independent lower unit, have matrix columns

\[
\begin{aligned}
 U&=(1,1,0,0),\\
 Z_1&=(0,\beta,1,0),\\
 Z_2&=(0,-\beta,2,0),\\
 W_{B-4}&=(0,0,0,1).
\end{aligned}                                          \tag{11}
\]

Its determinant is `3 beta`, and it has a unit three-minor.  Thus its Smith
form over the beta-local ring is

\[
                         (1,1,1,\beta).                \tag{12}
\]

The lower unit simply adds a free direct summand; the torsion class
`[rho0]=[D0]` survives.  Therefore a beta-independent realization of the
lower `B-4I` coefficient does **not** force an integral full-interface
extension or produce `D0`.

The exact missing special face is

\[
                   V=(1,0,0,*)                        \tag{13}
\]

with the same primitive descent defect as `U` and zero `rho0/rho2`; its
lower coordinate is harmless modulo the granted lower unit.  Then

\[
                         U-V=\rho_0=D0                 \tag{14}
\]

and `(U,V,Z1,W_B-4)` has a beta-independent unit determinant.  In a genuine
integral `C_+(beta)` orbit, (13) must be its beta-Bockstein/proper face.

## 5. Exact remaining theorem

The generic calculation has reduced the construction to one object:

> Construct a rho-even, `Q[beta]`-linear physical product-rule/Bianchi orbit
> `C_+(beta)` whose order-two restriction is the lower `B_ep-4I` family,
> whose generic complete quotient is (7) with Eq correction (9) and Spencer
> face (10), and whose beta-Bockstein is (13).

On `beta != 0`, this cell closes the first lower remainder of the generic
Cartan orbit.  Integrality makes the same cell remove the Smith torsion and
produce `D0` at the collision.  Without the full augmented cell, the lower
coefficient equality and the generic normalization do not imply either
source statement.

## Verification

```bash
python3 computations/verify_h3_generic_cplus_lower_quotient_smith_gate.py
python3 -O computations/verify_h3_generic_cplus_lower_quotient_smith_gate.py
python3 -I -S computations/verify_h3_generic_cplus_lower_quotient_smith_gate.py
```

Pinned ledger digest:
`73e79b2477cec9a9bfd077b18d07e2866ad6ef5ec70ed2311c3dd7b01c4b013a`.
