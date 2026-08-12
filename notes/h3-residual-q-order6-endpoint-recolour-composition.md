# Endpoint recolouring produces two exact source cycles

## Result

Let `Theta_6` be the exact 188-term order-six residual chain and set

\[
 E=q_{01}^{01}q_{67}^{22}
      \partial_{01:11}\partial_{67:11}.
\]

The normal-ordered composition `E o Theta_6` is now computed exactly.  It
has 188 order-eight leading terms and a 157-term order-seven Weyl
correction.  All 345 terms have site-degree shift `(-1)^8`, and the full
operator annihilates

```text
H_1^2,  H_1 H_11211211,  H_11211211^2
```

coefficientwise.  More strongly, it splits into two colour-fine homogeneous
operators of 232 and 113 terms, and **each summand separately annihilates all
three products**.  Thus endpoint recolouring of the order-six chain is a
genuine source construction, not merely a projection or a forgotten-grade
cancellation.

Checker:
`computations/verify_h3_residual_q_order6_endpoint_recolour_composition.py`.

## Why the Weyl correction matters

Every selected order-six coefficient contains `01:11` either zero or one
time; 157 of the 188 terms contain it, while none contains `67:11`.  Hence
normal ordering gives exactly

\[
 E\Theta_6=
 q_{01}^{01}q_{67}^{22}\Theta_6
     \partial_{01:11}\partial_{67:11}
 +[E,\Theta_6],
\]

where `[E,Theta_6]` has 157 terms.  Each correction term has common
coefficient factor

```text
01:01, 67:22
```

and common derivative face

```text
07:11, 24:11, 67:11.
```

The first two entries of that face are the primitive order-six overlap
`07:11 wedge 24:11`; the third is precisely the source endpoint replaced by
the recolouring operator.  This gives a literal endpoint-colour-changing
source cycle in the same local packet as the one-sided overlap arm.

## What happens to the residual shadow

The complete leading Hasse pair shadow, after forgetting the two fine
grades and dividing by the selected endpoint factor, is exactly the pinned
sixteen-coordinate `-delta` residual.  But neither homogeneous summand has
that shadow by itself:

```text
leading terms       124       64
pair support        107      111
outside delta        97       97
```

The extra pair faces cancel only after the two fine grades are identified.
This is the decisive scope boundary.  Ordinary endpoint recolouring has
constructed both physical source-cycle halves, but the sum which exposes
`-delta` still lives only after forgetting their labels.

## Revised missing theorem

The remaining local object is no longer an unspecified 360-term source
correction.  It is a **relative fine-grade gluing** of the two explicit
homogeneous cycles above.  The gluing must:

1. identify their excess Hasse faces with opposite signs;
2. leave the common sixteen-coordinate residue `-delta`;
3. carry the shifted ridge class `-d Omega_v`, hence the exact eta and sigma
   terminal values; and
4. preserve zero `D`, `W`, target, and anchor readouts.

This is precisely a chart-nondiagonal Spencer/mapping-cone differential.
The construction here supplies its two horizontal source cycles and the
normal-ordering homotopy.  The terminal-ridge theorem supplies its vertical
Kähler class.  What is still missing is the single physical relative cell
which makes those two pieces one labelled object.

## Consequence for the proof strategy

The proof should not search for another matching identity or another
unrestricted order-six solve.  The next calculation is the relative
differential between these two *known* fine-grade cycles.  Once that map is
constructed, the primitive common face gives the conditional one-sided
rank repair, and the established KS landing removes the unequal-tail
five-lock/E14 self-loop.  Hall/rank completion and the global decreasing
potential remain downstream and separate.

## Scope

This theorem is exact for the two quadratic source generators and the
displayed endpoint recolouring.  It does not construct the relative
fine-grade differential, prove its eta/sigma terminal values, or promote
the resulting carrier to four-good rank.

Verification:

```text
python3 computations/verify_h3_residual_q_order6_endpoint_recolour_composition.py
python3 -O computations/verify_h3_residual_q_order6_endpoint_recolour_composition.py
python3 -I -S computations/verify_h3_residual_q_order6_endpoint_recolour_composition.py
```

Frozen ledger SHA-256:

```text
e39ce23c92e2256cf2aa8a0c4450ad0101ec4302844c98a57f1a5b1f01c86202
```
