# The literal source ansatz does not construct the Eq filler (K)

## Result

The formal cap calculation uniquely requires a cell

\[
 dK=(H_0-u)e_{\mathrm{Eq}}
\]

with proper faces in the occurrence-local objects

\[
 0112/q_{23{:}21},\qquad 0121/q_{45{:}12}.
\]

The smallest literal fixed-grade source ansatz does not contain such a cell.
The failure precedes the augmented coefficient solve: it is an operation
idempotent obstruction.

The exact checker is
`computations/verify_h3_physical_eq_filler_k_source_ansatz_terminal_gate.py`.

## 1. The source-provenant ansatz

The ansatz contains only operations already defined in the physical source:

- divided Taylor--Spencer trigger, deletion, and reinsertion cells in the
  response corner (e_RAe_R);
- the canonical endpoint-even Reynolds sections for the two root objects
  `AB` and `AC` (coefficient (1/2));
- cap `r0`, `T`, `rho`, `K_Eq`, and `AugP2` cells in (e_CAe_C); and
- deleted-factor, ambiguous-lcm, and naturality mapping cylinders whose input
  maps already exist.

Endpoint averaging changes the twelve ordered cap-parent coordinates into a
six-dimensional even quotient and removes a six-dimensional odd kernel.  It
does not join the response and cap operation corners.  The two exact
endpoint-even root Hom covectors remain

```text
omega_AB^Hom, omega_AC^Hom.
```

Consequently

\[
 e_CAe_R=0
\]

in the literal ansatz.  In operation coordinates, the existing diagonal
idempotents have rank two.  Adding the desired off-diagonal matrix unit

\[
 e_C\Phi_{KS,r0}e_R
\]

raises the rank to three.  A standard mapping cylinder is functorial in a
previously specified map; it cannot create this input matrix unit.  Thus an
arbitrary “mixed cylinder” at this point would be precisely the prohibited
formal retagging grant.

## 2. Normalization is unique but does not give existence

After forgetting the physical tags, the response and cap two-term complexes
have the unique normalized chain-map shape

\[
 \Phi_1(\epsilon_s)=r_0,
 \qquad
 \Phi_0(c_f)=-(H_0-u)e_{\mathrm{Eq}}.
\]

Equivalently, the universal HPL repair is `-K`; its higher terms vanish.  The
physical retraction kills that formal (K).  Hence the scalar and signs are
settled conditional on a physical mixed mate, but the current physical
solution space is zero.

## 3. Every literal projection sees the same missing constructor

The obstruction is not an artifact of the operation coordinate.  Its forced
faces give independent exact rank witnesses:

| projection | current rank | after required face |
|---|---:|---:|
| complete first PP, then selected `db01` | 1 | 2 |
| presentation-safe graph, then selected `db01` | 2 | 3 |
| central Eq incidence | 3 | 4 |
| strongest four-root/six-label covariance span | 23 | 24 |
| complete protected local output | 126 | 127 |

For the parent

\[
 M=01\,23\,45\,67,
 \qquad N=07\,12\,34\,56,
\]

the response-side Taylor--Spencer branch contains the right two coarse
coefficient faces:

```text
q23 response face -> B1,
q45 response face -> B4.
```

What is absent is the decorated landing

```text
0112/q23:21 -> B1,
0121/q45:12 -> B4.
```

Across four oriented root paths and six labels, the edge skeleton has rank
72 and (H^1)-dimension 24.  Even the strongest label/root covariance
relations have rank 23.  The remaining (D=(-1,1,-1,1))-oriented class is
detected with normalized value one and no existing mixed face fills it.

## 4. Protected rows and forced lower faces

The complete local protected codomain has 127 rows.  It retains

```text
B, Eq,
18 direction flags, 24 tail PP flags,
target, q, anchor/ainc/P_f, W, ordinary residue,
ridge, eta, sigma.
```

All 138 literal projected columns span rank 126 and are annihilated by the
integral covector

\[
 \delta\cdot(B-\mathrm{Eq}),
 \qquad \delta=(1,1,-1,-1),
\]

transported through every restriction/reinsertion flag.  Private-only and
Eq-only controls each raise the rank to 127, with normalized values (+1)
and (-1); the tied (B=\mathrm{Eq}) packet has value zero.  Thus external
target, (q), (W), residue, or ridge decoration cannot repair the missing
line.

If the mixed mate is granted, the simultaneous `D4/P2/K_Eq/d_even` system is
nonsingular, of rank 24 and determinant 64.  Its characteristic-zero cap
coefficient is

\[
 (B_1+B_4)/2.
\]

Before that mate, the exact remaining row debt in order
`(R,lower,Eq,ores)` is

\[
 (0,-1,0,+1),
\]

meaning root lower (-E) and word-resolved ordinary residue (+E).  The
root-even cap top itself has

\[
 (\mathrm{Eq},Yw,W,\mathrm{target},\mathrm{ainc})=(E,E,E,0,0).
\]

The two protected target faces have pairing matrix

\[
 \begin{pmatrix}2&0\\0&2\end{pmatrix}
\]

on words `00211122` and `00111222`.  They are the forced `T23/T45` cone
faces, not equations to be set to zero, but their source-labelled occurrence
placement is not constructed either.

Finally, once the q23 occurrence landing is supplied, the literal Leibniz
rule forces the endpoint-even `0102/dq23:21` conormal.  Its augmentation and
ordinary-residue aggregate vanish, while

\[
 (+e_0+e_3-e_1-e_6)(dq_{23}\text{-face})=35/72.
\]

Sigma gives the `0121/dq45:12` mate with the same value.

## 5. Minimal genuinely new constructor

The minimal new primitive is not a hand-added (K).  It is one normalized,
source-labelled mixed Taylor--Spencer-to-`AugP2` mate

\[
 \Phi_{KS,r0}\in e_CAe_R,
\]

natural in the marked one-root object and separately instantiated at the two
endpoint-even root sections.  Its full fixed grade is

```text
response word   11110000,
cap word        01211222,
fine            the six literal t*q_(v,N) 24-coordinate degrees,
repeated        P3+K2,
operation       response-to-AugP2 mixed orbit/K_Eq,
window          2345 with parent occurrence retained,
root            AB and AC,
parity          endpoint-even.
```

It must carry the selected `db01`, the two q23/q45 occurrence landings, their
dq faces, the hidden lower/ores pair, the target cone faces, and the protected
cap/q/W/residue/ridge/eta/sigma rows.  Once this one mate exists, its ordinary
functorial mapping cylinder and product with `K_Eq` construct the uniquely
normalized (K).  Without it, no permitted constructor in the present source
ansatz does.

## Scope

This is an exact rational terminal for the literal (h=3) constructor
ansatz, the canonical `M/N/q01` packet, both endpoint-even root sections, all
four oriented root paths and six labels in the mixed-square test, and the
full 127-row protected local codomain.  It does not prove that an unmodeled
physical mixed mate cannot exist, and it is not an all-(h) theorem.

Run all modes:

```bash
python3 computations/verify_h3_physical_eq_filler_k_source_ansatz_terminal_gate.py --mode all
python3 computations/verify_h3_physical_eq_filler_k_source_ansatz_terminal_gate.py --mode typing
python3 computations/verify_h3_physical_eq_filler_k_source_ansatz_terminal_gate.py --mode faces
python3 computations/verify_h3_physical_eq_filler_k_source_ansatz_terminal_gate.py --mode protected
python3 computations/verify_h3_physical_eq_filler_k_source_ansatz_terminal_gate.py --mode constructor
```

Frozen ledger:

```text
4cdd1dc9dd890be0828878743d7ca6ba2f6154c57b3966337c14ea6055ef0d07
```
