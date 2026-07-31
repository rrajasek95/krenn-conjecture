# Audit record: SUPERSESSION-2026-07-30-07

Dependency: `INACTIVE-BOUNDARY`.

Replacement commit: `e23e5c413124f77fa4b9c51d9755c01c7a60920b`.

Independent auditor: `/root/sol_ultra_audit_adaptive_diagonal`.

Outcome: **PATCHED, then PASS.**

The audit independently verified and corrected the following points.

1. A direction with `D_aa=0`, both complementary diagonal entries
   nonzero, and nonzero endpoint-ordered contraction exists exactly when
   the direct block is not `alpha E_aa`.  The explicit construction uses
   the ordered cell itself and never substitutes its transpose.
2. The direct scalar and three target coordinates give the exact physical
   activity polynomial `alpha^3 d_b d_c t u^2 (t+gamma u)`.  Its three
   reduced boundary points are distinct when `gamma!=0`.
3. For non-diagonal `D`, the ordinary determinant can have an extra active
   zero or vanish identically.  Matrix invertibility is not part of the
   physical activity definition and cannot be imported as a downstream
   hypothesis.
4. The two boundary residues have literal representatives
   `J1=K1` and `J2=-gamma K0+(h-1)K2`.  Their coefficient determinant is
   `h gamma`, their displayed inverse is exact, and each row sees all
   three labels.
5. The symmetric and chartwise certificate degree inequalities hold
   uniformly, but they remain coefficient statements.  They do not prove
   relative source saturation or a target-cancelled adjacent-power chain
   comparison.
6. The first draft overstated the global chart conclusion.  The audit
   patched the fixed-rectangle alternatives to sufficient cases, not an
   if-and-only-if obstruction, and restricted the displayed residual
   ledger to the two distinguished good charts.  Other good neighbours or
   curvature rectangles may exist.
7. An arbitrary adaptive `D` is a legal linear combination of one chart's
   nine cap rows.  No audited theorem currently preserves a nonzero
   `AU-BF` carrier or transports its jets through the source-faithful
   two-chart overlap.  The final note states this gap explicitly.

The dependency-free checker passed normally and under `python3 -O` in
under one second.  The named diagonal-routing, Rees/cap-jet, and
same-power-lock dependencies also passed in both modes, and five
adversarial mutations were rejected.

SHA-256 at the replacement commit:

```text
55f8762d196858ba57664ba8c68020d8eae19bffba346d3fb73577fa15aa741c  notes/adaptive-diagonal-uncollision-cap-routing.md
76e9a7d904de9d0182d8a45f700ce26a2e9d34ae92b46ba0aebd25166bc45d4c  computations/verify_adaptive_diagonal_uncollision_cap_routing.py
```
