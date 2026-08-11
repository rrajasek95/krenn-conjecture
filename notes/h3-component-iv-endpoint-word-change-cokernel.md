# Endpoint bars kill the ridge but retain a primitive response companion

Research boundary only.  This does not construct (n_c), prove the unified
overlap theorem, or prove Krenn's conjecture.

## The obstruction is exactly the same (Omega_v)

The physical descent obstruction for the formal face chain was

\[
 \Omega_v=(a_{pq}^{22}-a_{pq}^{00})
       -(a_{xv}^{0m_v}-a_{xv}^{00}).                    \tag{1}
\]

The complete endpoint-color inventory contains a standard normalized bar
with precisely this boundary.  In the (pq) color square, either path

\[
 22\longrightarrow02\longrightarrow00,
 \qquad
 22\longrightarrow20\longrightarrow00
\]

has boundary (a_{pq}^{00}-a_{pq}^{22}); their difference is the ordinary
Bianchi square.  The (xv) interval has boundary
(a_{xv}^{00}-a_{xv}^{0m_v}).  Combining them gives

\[
                         dE_v^{\rm bar}=-\Omega_v.      \tag{2}
\]

Thus (1) is not merely analogous to an old bar obstruction.  It is exactly
the four labelled endpoint ridges of the existing bar/Bianchi complex.

## Source provenance forces a companion

Equation (2) forgets the contragredient source endpoint of local color
covariance.  Retain it and fix one of the three perfect matchings (N) of
(F_v).  Every one of the (2^4) output/source covariance corners has the
same literal coefficient

\[
                 q_{v,N}=\prod_{ij\in N}a_{ij}^{m_im_j}.
\]

Therefore the actual source-labelled route column is

\[
                         b_{v,N}=(-\Omega_v,q_{v,N}),   \tag{3}
\]

not ((-Omega_v,0)).  Completing the response on all four residual sites
makes the physical target zero: the seven acted input colors contain both
1 and 2.  It does not remove (q_{v,N}), which is the all-derivation
endpoint and the normalized ordinary-residue class.

There are fifteen distinct monomials (q_{v,N}).  With five ridge
coordinates and fifteen companion coordinates, the fifteen columns (3)
have rank fifteen in rank twenty.  Matching switches, both bar orders, and
all (pq) Bianchi squares remain in that rank-fifteen span.  The cokernel
is torsion-free:

\[
 \operatorname{coker}\langle b_{v,N}\rangle\cong\mathbb Z^5.
\]

Primitive separators are

\[
 \boxed{\lambda_v=\Omega_v+
             \sum_{N\in\operatorname{PM}(F_v)}q_{v,N}.} \tag{4}
\]

They kill every available source-labelled route and take value (-1) on a
clean repair ((-Omega_v,0)).  Consequently no rational, integral,
matching-averaged, or equivariant combination constructs an (E_v) with
both boundary (-Omega_v) and zero ordinary residue.  In particular, the
equivariant sum does not finish the five (	au_v) or (n_c).

## Complete natural inventory and chart 25

This module includes both (pq) endpoint orders, the (xv) interval, all
three matching routes on every face, every matching Bianchi difference,
and the complete target-killing residual response.  Selector localization
only rescales these columns and does not change (4).

The chart-25 relative trace does not add a compatible ridge cell.  Its
four-sum has the local (4D) projection only after discarding at least 818
off-fibre rows, retains four distinct target labels, and has the product-
anchor endpoint grade rather than the selected repeated response grade.
It is a mapping-cylinder projection, not a source-labelled endpoint
homotopy.

## Next attaching datum

The first genuinely new cell is a reduced relative ridge augmentation
(A_{v,N}) whose selected associated-grade boundary has

\[
 \operatorname{ridge}=0,qquad
 \operatorname{target}=0,qquad
 \operatorname{cap\ boundary}=0,qquad
 \operatorname{companion}=-q_{v,N}.                    \tag{5}
\]

Adding (5) to (3) produces the clean endpoint repair.  One equivariant
family may package the fifteen matching labels, but its image must pair
nontrivially with all five primitive functionals (4).  A normalized bar,
another Bianchi shuffle, or chart-25 projection cannot supply it.

The checker
[`verify_h3_component_iv_endpoint_word_change_cokernel.py`](../computations/verify_h3_component_iv_endpoint_word_change_cokernel.py)
reconstructs the endpoint paths, all 240 covariance corners, the fifteen
target-zero source routes, the integral cokernel and separators, and the
chart-25 scope guard.  It uses no non-source calibration or invented
ordinary-residue map.
