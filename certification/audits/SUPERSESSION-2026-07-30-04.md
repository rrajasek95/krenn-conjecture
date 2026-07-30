# Audit record: SUPERSESSION-2026-07-30-04

Dependency: `INACTIVE-BOUNDARY`.

Replacement commit: `f57ee88f3dce38b3770bd2a08b2f005be782cb30`.

Independent auditor: `/root/sol_ultra_audit_diagonal_three_boundary`.

Outcome: **PASS; no patches or mathematical corrections required.**

The auditor independently verified the following points.

1. The diagonal cap line has activity polynomial, up to the displayed
   nonzero scalar, `t u^2 (t+beta u)`.  When `beta!=0` its reduced boundary
   has three distinct points; when `beta=0` the scalar-zero and binary
   points collide to give the unary--complementary packet.
2. Cleanliness at each boundary point is equivalent to divisibility by its
   displayed linear equation, so factoring the distinct clean points and
   the remaining scalar coordinate gcd is exhaustive.
3. The symmetric three-boundary and sharper chartwise two-boundary
   certificates have the stated degrees.  The chartwise construction
   divides only the full scalar coordinate-gcd multiplicity of the third
   boundary factor.
4. The two generic normalized jets are
   `Z1=beta*rho0+rho2` and `Z2=-beta*rho0+(h-1)*rho2`; their determinant is
   `h*beta`.  Every coefficient in either jet is nonzero when `beta!=0`,
   so minimum-order survival supplies a detected colour without an extra
   generic colour-choice assumption.
5. At collision, the complementary residue can be blind to the selected
   colour.  Minimum-order survival alone does not remove this exception.
6. The result is coefficient-level.  It neither proves source-filtered
   third-factor saturation and jet transport nor constructs a physical
   middle correction or an active clean point.

The dependency-free checker passed normally and under `python3 -O`; its
geometry and jet tampering checks fail as intended.

SHA-256 at the replacement commit:

```text
b4daf03fd6ae82dbf091369dd3bdf4760683262e5a8e8d2687ad65d0edfae478  notes/diagonal-three-boundary-inactive-routing.md
6a2a8673fbaf99a112a30319e35be7bf3e1c9408b62d8f60e924e164df4ccd6f  computations/verify_diagonal_three_boundary_inactive_routing.py
```
