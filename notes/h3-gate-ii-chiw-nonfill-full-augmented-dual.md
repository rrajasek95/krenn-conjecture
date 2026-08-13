# The Gate-II nonfill dual is explicit but not yet a physical terminal

## Result

Assume the root-only Gate-II companion is not supplied in the identical
`C2+/C4/P2` grade.  The primitive covariant left dual on the known physical
cap--Cartan packet is explicit.

Write

\[
 \alpha=(-1,1,1,-1),\qquad
 \delta=(1,1,-1,-1).                                 \tag{1}
\]

For a local dual with values `mu_j` on the four cap corners, the committed
augmentation formula is

\[
 \mathrm{target}=-\mu,\quad W=-\mu,\quad
 \mathrm{ores}=\mu,\quad
 \mathrm{ridge}=-\alpha\cdot\mu,                    \tag{2}
\]

with `Eq=M=ainc=q=P_f=0`.  Taking `mu=delta` gives

\[
                        \alpha\cdot\delta=0.          \tag{3}
\]

Hence the primitive integer dual is

```text
local B corners        ( 1,  1, -1, -1)
target corners         (-1, -1,  1,  1)
W corners              (-1, -1,  1,  1)
ordinary residue       ( 1,  1, -1, -1)
Eq, M, ainc, q, P_f     0
ridge                   0
eta constant/u, sigma   0, 0, 0
global W, tail escape   0, 0.
```

It detects both the local `delta` face and the target-only companion
`Y=(0,-delta)` with value `4`; division by four gives the normalized rational
detector.

Checker:
[`verify_h3_gate_ii_chiw_nonfill_full_augmented_dual.py`](../computations/verify_h3_gate_ii_chiw_nonfill_full_augmented_dual.py).

## Exact cancellation on the known physical packet

The retained columns are

\[
\begin{aligned}
 r0_j&=B_j+Eq_j+\mathrm{target}_j-\mathrm{ainc},\\
 T_j&=-W_j+\mathrm{target}_j,\\
 \rho_j&=W_j+\mathrm{ores}_j,\\
 K&=\sum_j\alpha_j\mathrm{ores}_j+\mathrm{ridge}.
\end{aligned}                                        \tag{4}
\]

The displayed dual kills each column separately:

```text
r0_j     delta_j - delta_j = 0
T_j      delta_j - delta_j = 0
rho_j   -delta_j + delta_j = 0
K        alpha dot delta + 0 = 0.
```

The checker stresses all `3^4=81` assignments of the pointed `P_f` values
on the four `r0` corners.  None matters because the dual has `P_f`
coefficient zero.  It also tests the literal identity `q=M-ainc` on `27`
independent ternary packets; the dual ignores all three rows.

Equation (3) is the important simplification.  The dual has zero ridge
coefficient, so the unique ridge contractions give zero eta and sigma
coefficients.  There is no hidden terminal-ridge face on this character.
The common remote tail is also not an obstruction: the dual is supported on
the identical tail idempotent, and has zero escape coefficient.

## Why this is not yet an accepted separator or terminal

The calculation proves

\[
                 \widetilde\psi_\delta J_{\rm cap/Cartan}=0,   \tag{5}
\]

not

\[
                 \widetilde\psi_\delta J_{\rm full}=0.        \tag{6}
\]

The full map also contains the literal response/block-projector columns in
the original `Hasse[2](D,Q01)` word/fine/direction-pair grade and the
downstream word-`0102` placement.  A single additional same-grade column can
have nonzero pairing with the displayed dual.  Thus absence of a named
`Y` or `U_C4` cell from the present inventory proves neither nonmembership
in the complete image nor (6).

This dual is also not the already accepted first-flat anchor separator.
That separator is supported on a selected matching sum and physical
`ainc`; the new dual has zero anchor and nonzero mixed-target, `W`, and
labelled-residue coefficients.  Nor does it produce a physical `q`
generator, because its `q` coefficient is zero.

The exact missing extension is therefore:

> Construct the literal source-labelled map from the original
> `Hasse[2](D,Q01)` fan word/fine/direction-pair/common-tail block into an
> exhaustive AugP2/repeated physical codomain, including all response,
> local-block-projector, and downstream word-`0102` columns; then extend
> `tilde psi_delta` across those columns without changing its value on the
> selected `delta` class.

Equivalently, either prove (6) for the displayed primitive dual or find a
corrected full covector `Psi` with

\[
                 \Psi J_{\rm full}=0,\qquad
                 \Psi(i(B_\delta))=1.                \tag{7}
\]

## What happens after that extension

Once the candidate has been placed in the exhaustive same-grade physical
map, exact image/cokernel duality finishes the nonfill arm.

1. If `i(B_delta)` lies in the image, the preimage is the protected-zero
   relative filler/generator.
2. If it is outside the image, (7) is a full augmented physical terminal.

There is no third branch.  The present result computes the unique covariant
known-row extension and shows that `q`, `P_f`, and eta/sigma add no new
obstruction.  The only open point is full source-labelled same-grade
extension; a bare coefficient dual cannot bypass it.

## Scope and verification

This is exact for the canonical `h=3` cap--Cartan packet, the four target,
`W`, and residue corners, literal `q=M-ainc`, arbitrary pointed-anchor
values, the ridge contractions, and the common-tail idempotent.  It does not
prove that the selected class is outside an unconstructed exhaustive source
image.

Run:

```text
python3 computations/verify_h3_gate_ii_chiw_nonfill_full_augmented_dual.py
python3 -O computations/verify_h3_gate_ii_chiw_nonfill_full_augmented_dual.py
python3 -I -S computations/verify_h3_gate_ii_chiw_nonfill_full_augmented_dual.py
```

Frozen ledger SHA-256:

```text
124b6abd4248fadcba37ce7b0627e7675f014cc946ad4f6b8f1f7ef230b2324b
```
