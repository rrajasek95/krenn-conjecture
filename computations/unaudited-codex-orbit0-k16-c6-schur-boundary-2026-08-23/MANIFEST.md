# Manifest

- `audit_k16_c6_schur_boundary.py`: seed, direct-page, and corrected signed
  deterministic Schur provider.
- `results_k16_c6_schur_boundary.json`: exact 28 blockers and 1,114 incident
  column orbits; logical `1d893557...`.
- `boundary_incident_interface.json`: exact unreduced 24,922-row page; logical
  `82072e05...`.
- `boundary_schur_interface.json`: corrected signed 28,777-row page; logical
  `260dd9e7...`.
- `verify_k16_c6_signed_projection.py`: canonical-representative guard,
  exact-Q rank, augmented-rank, and target-certificate replay.
- `results_k16_c6_signed_projection.json`: terminal direct-page projection;
  logical `e1361165...`.
- `audit_k16_c6_direct_lift_compare.py`: exact lift, source-ledger replays,
  general cycle normalization, and affine residual comparison.
- `results_k16_c6_direct_lift_compare.json`: terminal comparison; logical
  `3cace6c9...`.
- `k16_c6_direct_lift_residual.tsv` and
  `k16_c6_direct_certified_residual.tsv`: exact pre- and post-cycle-normalized
  direct exterior residuals.
- `lift_k16_884_singleton_certificate.py`: deterministic exact singleton
  certificate extraction and one bounded full K<=16 lift.
- `results_k16_884_singleton_lift.json`: 884-column lift result; exterior
  support 12,052; logical `d67bf127...`.
- `k16_884_singleton_certificate.tsv`: exact 884-column rational certificate.
- `k16_884_singleton_lift_residual.tsv`: unreduced 12,052-row exterior.
- `audit_k16_c6_blocker_types_and_invariant.py` and its result are retained
  only as a retracted counterguard demonstrating the raw/canonical mismatch;
  the rank-zero theorem is invalid.
- `../unaudited-codex-orbit0-k16-coloured-necklace-referee-2026-08-23/`
  contains the exact backward critical-pair rank-28 projection and one lifted
  3,713-row exterior residual.
