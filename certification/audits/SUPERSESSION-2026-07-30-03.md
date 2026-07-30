# Audit record: SUPERSESSION-2026-07-30-03

Dependency: `INACTIVE-BOUNDARY`.

Replacement commit: `779e5bfc7d21dfe40fa167b5ed120ded78ae4314`.

Independent auditor: `/root/sol_ultra_two_site_collision`.

Outcome: **PATCHED, then PASS.**

The first draft contained a real quantifier error: it chose a
minimum-order exact ternary source without restricting the order, even
though exact ternary sources exist on four sites.  The auditor patched the
statement and proof to minimize only in the forbidden range `|B|>=6`.
The proved six-site obstruction then makes the selected source have order
at least eight, so its two-site reduction remains in the forbidden range.
The patch also repaired TeX corruption and expanded the checker to retain
the finite aggregate-to-decorated-source ledger and the order-four
exception explicitly.

After patching, the auditor independently verified the following points.

1. If all three classes vanish in
   `R_(2h-1)(D)/(R_1(D) q0^[h-1])`, there are linear forms `z_c` with
   `z_c q0^[h-1]=Y_c`.
2. With `rho=sum_c e_c^(x) z_c`, every term of `rho` uses `x`, so
   `rho^[2]=0`; site count gives `q0^[h]=0` on `2h-1` sites.
3. The divided-power identity therefore has no binomial coefficient and
   gives `(q0+rho)^[h]=sum_c X_c` exactly.
4. Expanding the quadratic blocks realizes this identity by finitely many
   endpoint-ordered decorated degree-two sources, with arbitrary complex
   coefficients and parallel cells retained.  Each of the three colours
   occurs because its constant-word coefficient is one.
5. In the minimum forbidden-order setup the constructed source has
   `|B|-2>=6` sites and contradicts minimality; the allowed four-site
   one-factorization is outside this argument.
6. At an off-diagonal scalar-zero endpoint all three target coefficients
   are `-alpha`, with `alpha!=0`, so every possible surviving colour gives
   a nonzero normalized odd residue.
7. The lemma does not supply the physical filtered correction or an active
   clean point, and no such closure is claimed.

The dependency-free checker passed normally and under `python3 -O`.

SHA-256 at the replacement commit:

```text
27ef0bdf8c9e4a00e41864700b91be5e005980923ccc088a8fcac61e24e61a40  notes/odd-residue-minimality-survival.md
73858538030cb2a94e8a4c1841d36520fb15720582478663ea55c47e7bd32dc9  computations/verify_odd_residue_minimality_survival.py
```
