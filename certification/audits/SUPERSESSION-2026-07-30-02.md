# Audit record: SUPERSESSION-2026-07-30-02

Dependency: `INACTIVE-BOUNDARY`.

Replacement commit: `e9ffdf3e78562bddb839a415d9b485f725f61e03`.

Independent auditor: `/root/sol_ultra_inactive_omega_two_chart_coboundary`.

Outcome: **PASS; no patches or mathematical corrections required to the
certified replacement.**

The auditor first checked the one-sided endpoint theorem and then performed
a fresh audit after the reverse orientation and exhaustive-routing statement
were added.  The final audit independently verified the following points.

1. For `a != b`, the scalar-zero endpoint is
   `K1 = tau E_ab - alpha I`, has determinant `(-alpha)^3`, and has ternary
   target `-alpha Delta`.
2. Cleanliness at `K0` gives `E = u Psi0`; cleanliness at `K1` gives
   `E = t Psi1`.  In either orientation the residual has degree `h-1`.
3. The coefficient `E1` is both the first inward polar at `K0` and the
   order-`(h-1)` inward jet at `K1`, with the displayed boundary-polar
   identity.
4. The active locus is exactly `D(tu)`.  Therefore a nonconstant coordinate
   gcd supported on the two inactive endpoints forces at least one endpoint
   to be clean, making the two orientations exhaustive.
5. Absence of an active clean point gives the bounded certificate with
   exponent `h-1`; when both endpoints are clean, the double factor sharpens
   the degree and exponent to `h-2`.
6. The normalized odd-site residue is `-Ybar_c` for every colour and agrees
   on any overlapping off-diagonal chart using the same odd quotient.
7. Tensoring this residue with the certificate is only a coefficient-level
   reduction.  It does not construct a physical filtered correction, prove
   nonzero target survival, treat the diagonal selected line, or close the
   conjecture.

The checker passed normally and under `python3 -O` and rejects altered
coefficient, endpoint, normalization, and exhaustiveness identities.

SHA-256 at the replacement commit:

```text
3831fcf66f450b4419b2e2783c0c0268a78d259e8d320461f05c32adb7d28b14  notes/offdiagonal-base-locus-ternary-omega-residue.md
3e6ebc38c999cf5b5bbc3abef8d995fb308441d981be6549732a984eb42dc284  computations/verify_offdiagonal_base_locus_ternary_omega_residue.py
```
