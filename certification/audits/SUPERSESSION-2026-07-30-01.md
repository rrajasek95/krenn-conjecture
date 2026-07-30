# Audit record: SUPERSESSION-2026-07-30-01

Dependency: `LOCAL-INVERTIBLE`.

Replacement commit: `b04cc6430d7b70ed4bbbba2f97243bbe6a88a2b4`.

Independent auditor: `/root/sol_ultra_audit_invertible_one_hole_descent`.

Outcome: **PASS; no patches or mathematical corrections required.**

The auditor independently rederived the following points.

1. `2L+C>=3` forces at least two distinct doubly aligned sites, and at
   least one lies on the five-site overlap because only the cross site is
   excluded.
2. The two-target local geometry has exactly the stated physical-channel
   hole or total-wedge alternatives.
3. The coefficient cut has degree-four terms `A`, degree-three terms `B`,
   and the displayed divided-power coefficients and physical labels.
4. Division occurs only by the nonzero scalar `g_c`.  The `g_c=0` branch
   is genuinely membership in `Ann_3(lambda)`, with a zero representative
   recorded only as an unsuspended lower row.
5. The off-diagonal isotropic selector and the coincident-curvature
   corollary are valid.  Curvature is not claimed to decide other sites or
   colours.
6. No common site factor is cancelled, no scalar target is substituted for
   a pure target, and the conjecture remains open.

The checker passed normally in approximately 0.40 seconds and failed closed
under `python3 -O`.

SHA-256 at the replacement commit:

```text
f1c46626ad7d68d4a86be5baf758d11337702d793ff68bc9cd274a98e3211da0  notes/invertible-complete-anchor-one-hole-filtered-descent.md
4be6c2add51e8da4c144f0332f6ad7b1cc2f3dadaf7b49629d08d56dd0227c8d  computations/verify_invertible_complete_anchor_one_hole_filtered_descent.py
```
