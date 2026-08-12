# The order-six tower and the terminal ridge jet commute exactly

## Outcome

The two pieces of the proposed final local Spencer square act on disjoint
physical coordinate variables.

For every face `v`, the terminal ridge uses only

```text
q_pq:22, q_pq:00, q_xv:0m_v, q_xv:00.
```

Across all 8,580 eligible order-six missing-face operators, neither a
quadratic coefficient nor any of the six derivative directions is one of
these coordinates.  This holds simultaneously for all five faces.

Consequently, coefficientwise on the polynomial ring and its universal
first-principal-parts module,

\[
 [\Theta_6,M_x]=0,
 \qquad
 [\Theta_6,dx]=0
\]

for every coordinate `x` in `Omega_v`.  Hence

\[
                         [\Theta_6,-d\Omega_v]=0.
\]

Checker:
`computations/verify_h3_residual_q_order6_ridge_jet_commutation.py`.

## Why this matters

The final local construction was phrased as an interchange homotopy between
the order-six source/Hasse correction and the terminal Kähler class.  At the
coefficient-ring level no further interchange correction is needed: the
square commutes strictly.  The complete unsigned Hasse tower may be tensored
with `-dOmega_v` without creating new mixed source faces.

This removes another possible family of higher obstructions.  The remaining
theorem is purely the physical comparison:

> place the already commuting tensor product in the chart-nondiagonal,
> labelled repeated `P3+K2` grade and verify its augmented `W`, target,
> residue, anchor, eta, and sigma readouts.

The source/residual rows and terminal rows are already correct on the two
factors separately.

## Why disjointness is expected

The order-six block is built from the two complete source words whose
marked endpoint colours are in the `1/2` sector.  The eta ridge needs
colour-zero endpoint coordinates, while the sigma face needs the marked
`p/x` colour-two coordinates.  The exact fine shift excludes both types
from every eligible coefficient.  The derivative directions come from the
same source-word monomials and avoid the four ridge coordinates as well.

## Scope

This is an exact polynomial/Kähler commutation theorem for the entire
eligible order-six block.  It does not identify the formal tensor product
with a physical source cell, construct the chart-nondiagonal mapping cone,
or prove the augmented rank landing.

Verification:

```text
python3 computations/verify_h3_residual_q_order6_ridge_jet_commutation.py
python3 -O computations/verify_h3_residual_q_order6_ridge_jet_commutation.py
python3 -I -S computations/verify_h3_residual_q_order6_ridge_jet_commutation.py
```

Frozen ledger SHA-256:

```text
0e59923eccd279e7e75599d98ba77c338bd4491470ddc42d58f08c742091df76
```
