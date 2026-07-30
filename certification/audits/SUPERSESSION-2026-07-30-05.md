# Audit record: SUPERSESSION-2026-07-30-05

Dependency: `INACTIVE-BOUNDARY`.

Replacement commit: `bcb7ddf6bc17140fc37a8fc049b9cb9d2eba5fa0`.

Independent auditor: `/root/sol_ultra_audit_same_power_bockstein`.

Outcome: **PATCHED, then PASS.**

The audit independently re-derived and checked the following points.

1. The canonical cap syzygy has response `alpha^-1 R` and target
   `-Delta`, with the displayed factors of `h` and `alpha`.
2. The cap terms compare radial symbols `tau q`, not `q`.  A per-`q`
   transition uses `tau^-1` only where `tau` is a unit; at `tau=0` the
   displayed terms have zero radial symbol and define no such transition.
3. For any same-complement row
   `Q q^[h-1]=sum_c lambda_c X_c`, exposed-site coefficient extraction
   gives `rho_c(Qbar)=lambda_c Ybar_c`.  The proof is uniform over a scalar
   parameter ring, with localization only at the selected nonzero entry.
4. A same-power companion cancelling the scalar-zero diagonal target
   therefore cancels its odd response exactly.  Flat ordinary residue
   transport between charts does not evade this lock.
5. The four contributions from the direct-double, normal, curvature, and
   power-free connection rows have the signs displayed in (35), and reduce
   to the two adjacent divided-power identities in (36).
6. The first draft called this ledger a constructed Gauss--Manin/Bockstein
   class and assigned it a Yoneda value.  The auditor patched that
   overclaim: (35) is an exact adjacent-power source syzygy.  A chain
   complex, well-defined connecting operation, representative independence,
   and the conditional value in (38) all remain unproved.

The dependency-free checker passed normally and under `python3 -O`; its
divided-power, target-sign, and curvature-orientation tampering checks fail
as intended.

SHA-256 at the replacement commit:

```text
5bc962bcd6fcca0b5e449e698fbb7016714352c499cc2d444f3d217fa6fd5623  notes/offdiagonal-same-power-target-residue-lock.md
055de2778ac1ce343772474e55e9ca2f37380690176683e25fb2f06b16fa8309  computations/verify_offdiagonal_same_power_target_residue_lock.py
```
