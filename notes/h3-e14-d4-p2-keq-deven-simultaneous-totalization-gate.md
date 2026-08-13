# E14 D4/P2/K_Eq/d_even simultaneous totalization gate

## Result

The apparent `K_Eq`/`d_even` dependency is a nonsingular rational feedback
problem, not a formal circularity.  On the complete quotient

\[
  W=\mathbb Q^4_{\rm root}\otimes
    \mathbb Q^6_{B_0,\ldots,B_5},
  \qquad D=(-1,1,-1,1),
\]

use the rooted insertion and normalized alternating face retraction

\[
 L(d)=2D\otimes d,
 \qquad
 F_D(x)_j={1\over 8}\sum_{r=0}^3D_r x_{r,j}.
\]

Then

\[
 F_DL=I_6,
 \qquad
 LF_D=P_D\otimes I_6,
 \qquad
 P_D={DD^t\over4}.
\]

Thus `LF_D` is a rank-six projector and

\[
 \operatorname{rank}(I+LF_D)=24,
 \qquad
 \det(I+LF_D)=2^6=64,
 \qquad
 (I+LF_D)^{-1}=I-\tfrac12 LF_D.
\]

There is no circularity over `Q`.  There is, however, a load-bearing
normalization condition: on every labelled alternating root line the system
is `2 K_D=RHS_D`.  The actual augmented right side must therefore be twice
the desired normalized packet.  This evenness, and a source-valid realization
of `F_D`, are not proved by the current inventory.

## Sign audit

Write the coupled construction as

\[
 K=A+X+Ld,
 \qquad z=C-K,
 \qquad d=Fz.
\]

Substitution gives

\[
 K=A+X+LF(C-K)=A+X+LFC-LFK,
\]

and hence

\[
 (I+LF)K=A+X+LFC.
\]

The plus sign is essential.  With the normalized alternating retraction, the
opposite operator `I-LF_D` has rank 18 and its kernel is precisely the six
labelled `D`-lines.

The factor `1/8` in `F_D` is also forced by the selected normalization: the
alternating average contributes `1/4`, the face-3/face-5 extraction contributes
`1/2`, and `L` carries the factor `2`.  Consequently `F_DL=I_6`.

## Why the aggregate calculation is misleading

If one first forgets root labels with

\[
 F_\Sigma(x)_j={1\over4}\sum_r x_{r,j},
\]

then `F_Σ L=0` because `sum(D)=0`.  The resulting `LF_Σ` has rank six but is
square-zero, so `det(I+LF_Σ)=1`.  This is not the complete physical quotient:
it has forgotten the four word-labelled residue copies whose separate
vanishing is one of the protected conditions.  It therefore cannot be used
to claim an integral or physical closure.

## D4 and the remaining source map

The oriented last boundary of the D4 Boolean cell, in lexicographic D3-face
order `(012),(013),(023),(123)`, is exactly

\[
 (-1,+1,-1,+1)=D.
\]

For

\[
 v=(B_1+B_4)/2,
 \qquad E=2D\otimes v,
\]

the hidden face `-E` would follow if each marked D3 occurrence had the
physical image

\[
 -(B_1+B_4)=-2v
\]

in the canonical eight-site repeated `P3+K2` grade.  The committed D4 orbit
theorem supplies the signs and marked top `R`, but not this occurrence-to-
label map, its factor two, or its physical fine-grade normalization.

Conditionally, the main readout identity is

\[
 (-E,0,0)+(E,E,-E)+(0,0,E)=(0,E,0)
\]

in `(lower/private, Eq, labelled ores)` rows.  Including the marked top gives

\[
 (R,-E,0,E)+(0,E,E,-E)=(R,0,E,0).
\]

The old unary `U` then supplies the `T12` proper face once the source-labelled
central placement `(R,Eq)=(1,1)` exists.

## Cap rewrite and the precise frontier

At each selected cap face,

\[
 p=(-Q,-ores),\qquad n=(Q,0),\qquad z_{cap}=p+n=(0,-ores).
\]

If `z_cap` is supplied as a primitive transported cap input, the two labelled
face formulas

\[
 z_3\mapsto-B_4,
 \qquad
 z_5\mapsto-B_1
\]

give

\[
 d_{even}=-\tfrac12(-B_4-B_1)=(B_1+B_4)/2.
\]

This rewrite removes the old presentation in which `n` was first extracted
from the clean `K_Eq` being constructed.  It does **not** by itself prove the
physical construction: the actual coupled system still requires a literal
source map `F_D` on complete augmented packets and the factor-two condition on
`A+X+LF_DC`.

The shortest remaining lemma is therefore:

> Construct one pointed, source-labelled AugP2 D3/cap section in the canonical
> repeated grade whose top is `R`, whose D3 boundary is `-(B1+B4)`, whose
> face-3/5 restrictions realize the normalized `F_D`, and whose augmented
> right side is even on all six alternating root-label lines.

The same section must preserve the flat shifted-Kähler connection
`-d(q_xv^01)` (terminal-dark under the fixed-frame eta/sigma readouts) and
enter the existing physical-q transport-versus-generator alternative.

## Scope

The sign, root-by-label matrices, ranks, determinant, and conditional readout
identities are exact for the canonical `h=3` silent E14/root-even packet.  This
does not construct the missing source-labelled section and does not promote
the rational inverse to an integral/source-normalized physical chain.

## Verification

Run:

```text
python3 computations/verify_h3_e14_d4_p2_keq_deven_simultaneous_totalization_gate.py
python3 -O computations/verify_h3_e14_d4_p2_keq_deven_simultaneous_totalization_gate.py
python3 -I -S computations/verify_h3_e14_d4_p2_keq_deven_simultaneous_totalization_gate.py
```

Expected headline:

```text
D-character transfer: rank(LF)=6, det(I+LF)=64
rational circularity: NO; normalization/evenness guard: OPEN
```
