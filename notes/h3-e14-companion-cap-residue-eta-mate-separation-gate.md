# `z_cap` and the eta mate do not supply the E14 companion

## Verdict

The canonical E14 first-hit functional sees exactly

```text
(p1_0_1 s1_1_1) u05_01 v13_01 v24_11
```

and assigns zero to the promoted decorated-core term containing
`u05_01*v34_10`.  Neither part of the primitive-cap repair creates the
visible companion:

1. after the physical `K_Eq` lift,

   \[
       z_{\rm cap}=p+n=(Q=0,\operatorname {ores}_{\rm cap}=-1);
   \]

   the entire decorated matching companion has canceled; and
2. the proposed `Omega`/rootless eta mate is a protected terminal readout
   with value `+(5+u_z/t)` on `eta_z`.  It is not a principal unary/`G11`
   boundary in E14 word `000101`.

Thus cap residue and eta compensation do not cancel the first-hit class,
even if both are granted physically.

Checker:
[`verify_h3_e14_companion_cap_residue_eta_mate_separation_gate.py`](../computations/verify_h3_e14_companion_cap_residue_eta_mate_separation_gate.py).

## Exact direct-sum obstruction

Quotient the 269-column E14 first-hit image and retain three coordinates:

```text
E14 first-hit class, scalar cap ores, Omega/rootless eta terminal.
```

The strongest separate grant has

```text
z_cap   = (0,1,0),
etaMate = (0,0,1),
target  = (1,0,0).
```

Therefore the candidate rank is two and adjoining the E14 target raises it
to three. Restoring the old E14 image gives the literal count

```text
269 + 2 = 271  ->  272.
```

The surviving covector `(1,0,0)` is the old 22-support first-hit seed. This
is not merely an abstract word mismatch. The cap class is pure augmented
residue after `K_Eq`; it has no principal `Q` monomial to promote. The eta
mate corrects a kernel readout and likewise has no E14 coefficient.

## Target-normal debt is independent

The generic first-hit pairing is concentrated on the visible companion:
target coefficient `-1`, dual coefficient `+1`. The decorated core has dual
coefficient zero.

If the `q13` chord is silent, that visible monomial vanishes, but the target
still raises the specialized old rank

```text
211 -> 212.
```

Its reduced representative is one target-normal class supported on nine
pure unary-target coordinates. On `q04=q13=0`, the corresponding figures
are

```text
185 -> 186, with support eight.
```

Hence a cap/Omega repair which carries scalar residue but no target-normal
face cannot close the strict silent branch. The obstruction migrates; it
does not disappear.

## Shortest positive cell and dual

The next source theorem is one genuinely mixed augmented comparison cell.
It must have:

1. a word-changing E14 principal boundary with nonzero 22-support pairing
   (generically the `u05*v13*v24` companion class);
2. scalar cap face `z_cap` in word `01211222`, fine degree `t*q_(v,N)` and
   repeated grade `P3+K2`; and
3. the unary target-normal proper face exposed above.

The `Omega`/rootless eta mate remains necessary for terminal compatibility,
but it is a fourth readout condition on this mixed cell, not a substitute
for its E14 boundary.

Failure has two independent seeds which must be extended simultaneously:

- scalar cap residue, whose terminal extension requires the eta-compatible
  `Omega`/rootless mate; and
- the 22-support E14 functional, whose silent specialization is the
  nine-coordinate (or eight-coordinate) target-normal residual.

Only after these are extended over the complete common-grade physical map
does the nonmembership arm become a Fredholm terminal. The present rank
calculation does not claim that promotion.

## Scope

This is exact for the selected h=3 cap aggregate and canonical E14 first-hit
block. It rules out separate use of `z_cap` and the eta mate, including the
strong grant that both are already physical. It does not rule out the mixed
augmented endpoint-word-change cell just specified.

Run:

```text
python3 computations/verify_h3_e14_companion_cap_residue_eta_mate_separation_gate.py
python3 -O computations/verify_h3_e14_companion_cap_residue_eta_mate_separation_gate.py
python3 -I -S computations/verify_h3_e14_companion_cap_residue_eta_mate_separation_gate.py
```

Frozen ledger SHA-256:

```text
4844f563352246a30ce9691045bedbed5e95270a2af2bb1864b91c98cd2db72f
```
