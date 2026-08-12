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

## A canonical antisymmetric choice

The initial 188-term solution was selected by an arbitrary sparse-basis
solve, so its two homogeneous pieces need not visibly respect tail-colour
symmetry.  Let `tau` simultaneously swap colours 1 and 2 at sites 2 and 5.
The three source products are invariant as a set under `tau`, while the
residual changes sign.  Therefore

\[
                 \Theta_6^-={1\over2}(\Theta_6-\tau\Theta_6)
\]

is again a zero-source lift of the same `-delta` shadow.

This antisymmetrized solution has 372 terms.  After endpoint recolouring it
splits into two fine-grade cycles `Z_0,Z_1`, each with exactly 341 terms,
and the checker verifies the literal identity

\[
                         \tau Z_0=-Z_1.                 \tag{1}
\]

Thus the missing gluing is no longer between unrelated source cycles.  It
is the relative/bar differential for one explicit physical colour
involution.  Equation (1) does not by itself make the gluing a boundary in
the physical source complex: that requires a source-labelled Spencer or
mapping-cone homotopy for the symmetry action.  But it fixes the desired
homotopy's endpoints exactly and removes arbitrary sparse-solution choices
from the frontier.

## Revised missing theorem

The remaining local object is no longer an unspecified 360-term source
correction.  It is a **relative fine-grade gluing** of the two explicit,
signed-symmetric cycles above.  The gluing must:

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
5926845f9f18a0dc6ad6f95a71ef6acbbe10d539b58c100b6a1c15c5aeabf80b
```
