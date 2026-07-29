# Parabolic star tangents do not enlarge the three-hole gauge kernel

## Outcome

The large local parabolic stabilizer of one equation

\[
                         F_q(z_r)=e_r^{\otimes J}         \tag{1}
\]

does not automatically put an actual star solution on the extra-kernel
branch of the three-hole dichotomy.  At the quotient site `j`, its only
fixed-map infinitesimal action applies an endomorphism of
`bar V_j=V_j/Ce_r` to the barred `j` factor of the kernel vector (7) in
`fixed-star-three-hole-gauge-dichotomy.md`.  The expansion-gauge image is
closed under every such endomorphism.  Explicitly,

\[
 \bar L\,\mathcal G_{j,r}(w)
       =\mathcal G_{j,r}((\bar Lw_i)_{i\ne j}).           \tag{2}
\]

Thus, if the original star vector is an expansion gauge, all of its local
parabolic derivatives are expansion gauges too.  If it is not, the original
vector already witnesses the stated extra-kernel branch; the parabolic does
not create a new automatic escape.

Parabolic changes at sites other than `j` vary `Psi_(j,r)` itself.  Their
derivatives therefore do not lie in the kernel of the fixed map: after the
natural source/target trivialization they are merely changes of basis.  For
the three simultaneous rows, the common local stabilizer is only diagonal,
namely the already-known target torus.

## 1. The fixed-map parabolic action

Fix `j,r`, and abbreviate the kernel vector supplied by the star equation as

\[
 K_{j,r}(q,z_r)=
 \left(
   \bar z_{j,r},
   \bigl(z_{i,r}\otimes\bar q_{jk}
          +\bar q_{ji}\otimes z_{k,r}\bigr)_{i<k}
 \right).                                                \tag{3}
\]

Let `P^1_(j,r)` be the subgroup of `GL(V_j)` fixing the vector `e_r`.
It is still a large parabolic: in a splitting `V_j=Ce_r+U`, its matrices
have block form

\[
                         \begin{pmatrix}1&\phi\\0&G\end{pmatrix},       \tag{4a}
\]

with arbitrary `phi` and `G in GL(U)`.  Act on every factor of `q` and
`z_r` at site `j`, and act nowhere else.  This preserves (1) exactly.  The
larger line stabilizer adds a scalar on `e_r`; after compensating that scalar
on another site or by rescaling `z_r`, its visible quotient action is still
an arbitrary endomorphism of `bar V_j`, so it gives no additional case.

Neither `C_j` nor any `D_ijk` contains site `j`.  Consequently
`Psi_(j,r)` is unchanged by this source transformation.  If `bar g` is the
endomorphism induced by `g in P^1_(j,r)` on `bar V_j`, direct inspection of
(3) gives

\[
 K_{j,r}(gq,gz_r)=\bar g\,K_{j,r}(q,z_r),                \tag{4}
\]

where `bar g` acts on the unique barred `j` factor in every domain summand.
For an infinitesimal generator `L` with `Le_r in Ce_r`, differentiation
therefore gives the genuine fixed-map kernel vector

\[
 \dot K_{j,r}(L)=\bar L K_{j,r}(q,z_r)
                         \in\ker\Psi_{j,r}.              \tag{5}

The unipotent part mapping `bar V_j` into `Ce_r` induces zero on the
quotient.  The only visible part is the arbitrary two-by-two endomorphism
`bar L`.

## 2. Closure of the expansion gauges

Recall

\[
 \mathcal G_{j,r}(w)=
 \left(\sum_{i\ne j}w_i,
       (-(w_i+w_k)^{(j)}\otimes q_{ik})_{i<k}\right).     \tag{6}

Since every `q_ik` in (6) avoids `j`, applying `bar L` to its barred factor
gives exactly

\[
\begin{aligned}
 \bar L\,\mathcal G_{j,r}(w)
 &=\left(\sum_{i\ne j}\bar Lw_i,
       (-(\bar Lw_i+\bar Lw_k)^{(j)}\otimes q_{ik})_{i<k}\right)\\
 &=\mathcal G_{j,r}(\bar Lw),                            \tag{7}
\end{aligned}

which proves (2).

**Proposition 2.1 (parabolic audit).**  Suppose (1) holds.  For fixed
`j,r`, either `K_(j,r)(q,z_r)` is already outside
`im G_(j,r)`, or every infinitesimal fixed-map kernel direction generated
from it by the local line parabolic lies in `im G_(j,r)`.

**Proof.**  In the first case the kernel is already larger than the gauge
image.  In the second write `K=G(w)` and combine (5) with (7). `QED`

If `G_(j,r)` is injective and

\[
 \rho=\dim\operatorname {span}\{w_i:i\ne j\}\le2,       \tag{8}

then the parabolic directions in (5) have dimension exactly `2 rho`.
Indeed, the kernel of the map
`End(bar V_j)->(bar V_j)^(J\setminus{j})`,
`L mapsto (Lw_i)_i`, consists of the endomorphisms vanishing on the
`rho`-dimensional span, and has dimension `2(2-rho)`.  These `0`, `2`, or
`4` directions are already inside the `2(|J|-1)`-dimensional expansion
gauge space.

## 3. Why the other-site parabolics do not give fixed kernel vectors

Let a local transformation act at a site `ell!=j`.  Now `C_j` and some of
the `D_ijk` transform at `ell`, so the map `Psi_(j,r)` varies.  There are
natural representations on its domain and codomain for which

\[
 \Psi_{j,r}(gq)\,\rho_{\rm dom}(g)
   =\rho_{\rm out}(g)\,\Psi_{j,r}(q),                    \tag{9}
\]

and the star vector obeys

\[
 K_{j,r}(gq,gz_r)=\rho_{\rm dom}(g)K_{j,r}(q,z_r).       \tag{10}


Differentiating `Psi(t)K(t)=0` without trivializing gives

\[
 \Psi(0)\dot K(0)=-\dot\Psi(0)K(0),                     \tag{11}

not `Psi(0) dot K(0)=0`.  After pulling domain and codomain back by the
representations in (9), both the map and vector are constant.  Hence an
other-site parabolic supplies no additional vector in the kernel of the
fixed `Psi_(j,r)`.  Treating `dot K` alone as one would omit the right side
of (11) and create a spurious kernel direction.

## 4. The simultaneous stabilizer is not parabolic

For one row `r`, the stabilizer of the pure tensor in (1) is a product of
line parabolics (with one scalar-product constraint).  But the same change
of `q` must preserve all three equations

\[
                         F_q(z_r)=e_r^{\otimes J}
                         \qquad(r=0,1,2).                 \tag{12}

A local linear map preserving all three target lines `Ce_0,Ce_1,Ce_2` is
diagonal.  The connected simultaneous stabilizer is therefore

\[
 \{(g_v):g_v\text{ diagonal},\ prod_v(g_v)_{rr}=1
                    \text{ for }r=0,1,2\},              \tag{13}

of dimension `3(|J|-1)`.  This is exactly the diagonal target stabilizer,
not an additional parabolic family.  Off-diagonal one-row parabolics do not
give automatic tangents to the simultaneous system; producing compensating
solutions in the other two rows would be an extra cofactor-surjectivity
condition, not a symmetry consequence.

## 5. Exact small-order audit

The verifier
`computations/verify_fixed_star_parabolic_gauge.py` uses the five-site
quadratic

\[
 q_{12}=e_0e_0-e_1e_2,\qquad
 q_{02}=e_0e_2,\qquad q_{34}=e_0e_0,                     \tag{14}
\]

with

\[
 z_0=e_0^{(0)}+e_1^{(1)}.                               \tag{15}

Complete exact matching expansion gives

\[
             z_0{q^2\over2}=e_0^{\otimes5};             \tag{16}

\]

the two nonconstant terms cancel.  At `j=1`, the nonzero vector (3) is the
expansion gauge with `w_0=bar e_1` and all other `w_i=0`.  The checker builds
the integer `Psi_(1,0)`, applies a basis of all four endomorphisms of
`bar V_1`, and verifies both

\[
 \bar L K=\mathcal G_{1,0}(\bar Lw),
 \qquad \Psi_{1,0}(\bar L K)=0                           \tag{17}
\]

coefficient by coefficient.  Exact rational matrix ranks show that the
parabolic span has dimension two in this example and that adjoining it does
not increase the expansion-gauge rank.

This audit leaves the assessment of the three-hole route unchanged: an
actual star solution is not forced onto the extra-kernel locus merely by
its local parabolic symmetries.
