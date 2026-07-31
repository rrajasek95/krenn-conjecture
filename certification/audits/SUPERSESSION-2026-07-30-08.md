# Audit record: SUPERSESSION-2026-07-30-08

Dependency: `INACTIVE-BOUNDARY`.

Replacement commit: `7f0a212c8cb4e4ec8c2502052c0b93f537e39c0d`.

Independent auditor: `/root/sol_ultra_audit_scalar_normal_jet`.

Outcome: **PATCHED, then PASS.**

The audit independently verified and corrected the following points.

1. For `K=x E_aa+D`, `D_aa=0`, contraction of all nine physical rows gives
   `R_D q^[h-1]=T_D`.  Expanding the divided power and retaining the target
   therefore gives the displayed full normal form with no omitted factorial
   or matching-power cancellation.
2. The divided difference has the exact coefficient `1/(ell+1)`, so
   `Theta_a=R_aa H_a`.  The endpoint-ordered response factors satisfy the
   literal Segre identity `R_ij R_aa=R_ia R_aj`; the equality does not assert
   that the resulting product is nonzero.
3. Multiplication by `G_a` gives
   `G_a Theta_a=h U_a+(h-1) alpha^(h-1) R_aa q^[h-1]` with the stated
   divided-power constants.
4. If `U_a=Theta_a=0`, the exceptional row and all eight remaining pair rows
   make every response slice with `p`-endpoint colour `a` zero as a whole
   tensor.  Deleting the complete `p_a` aggregate row preserves the exact
   matching tensor after arbitrary complex cancellation, while good-pair
   injectivity makes that row nonzero.  This contradicts minimum entry
   support and proves `(U_a,Theta_a)!=(0,0)`.
5. The first draft had widespread stripped inline TeX delimiters; the audit
   restored them and clarified that the deletion is at source-row level,
   not termwise inside a cancelled response.
6. A vector polynomial with no common nonzero root need not have a zero
   Taylor coefficient.  The final theorem does not infer `Theta_a=0` from
   the absence of an active clean cap, and does not claim a clean point or
   a source-faithful overlap transport.
7. The checker was memoized to remain lightweight.  It passed normally and
   under `python3 -O`; the clean-pair exact-descent, adaptive-diagonal,
   intrinsic-guard, and same-power-lock dependencies also passed in both
   modes.

SHA-256 at the replacement commit:

```text
a40064cfba52c4df551bf6ed0aec989cd926c50855cfc59c2be617f8eda5607d  notes/scalar-unit-full-normal-jet-unary-anchor-ledger.md
f9debc5f966a218fee0f94b7bf710dbdfd3aa3c7796f61ffaed0b70c0a1360e4  computations/verify_scalar_unit_full_normal_jet_unary_anchor_ledger.py
```
