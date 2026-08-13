# The shared repairs close by an anchor-fibre generator/separator alternative

## Result

The two missing equivariant shared-label images do not require an explicit
protected-zero cell in order to close the finite Gate-I alternative.

For each of the four target-orbit choices from the shared-loop census, the
complete old target/residue cone constructs a target-normalized near-hit

\[
 x_v=R_v-T_v-\rho_v+d_{{\rm ores},v}
    =(\operatorname{low}=v,\operatorname{ainc}=-1,
      W=\operatorname{tgt}=\operatorname{ores}=0).       \tag{1}
\]

The desired repair is

\[
 U_v=(\operatorname{low}=v,\operatorname{ainc}=0,
      W=\operatorname{tgt}=\operatorname{ores}=0).       \tag{2}
\]

Thus (U_v-x_v) is a pure physical-anchor element of the protected kernel.
If physical anchor incidence is nonzero on that kernel, it normalizes to the
existing relative generator.  If it is zero, the primitive physical
covector

\[
              \nu=\sum_{i=0}^{5}\operatorname{low}_{B_i}
                         +\operatorname{ainc}             \tag{3}
\]

descends and detects every (U_v).  With the already physical Cartan column
adjoined, the anchor-dark bordered theorem refines this second outcome to a
target-dark separator, an external-cokernel separator, or a unit-Cartan
kernel.  There is no unclosed linear branch.

## Complete generous cone

The checker works on the 25 rows

```text
lower_B0..B5,
ainc,
W_B0..B5,
target_B0..B5,
ores_B0..B5.
```

It grants more columns than the literal placement requires:

- all six `r0`, `T`, `rho`, and labelwise pure-ordinary-residue columns;
- all fifteen clean collision differences;
- all fifteen placements of the literal four-corner (M_v) alpha packet;
- all fifteen endpoint-odd Cartan alpha-residue packets.

The resulting column space has exact rank 24.  Its primitive integral
cokernel is (3).  Granting every labelwise pure-residue companion and every
possible (M_v)/Cartan placement makes this a stronger no-go: failure in
this cone implies failure in the actual smaller inventory.

The four normalized equivariant repair directions are

\[
 e_1,qquad e_4,qquad {e_0+e_5\over2},qquad
 {e_2+e_3\over2}.                                    \tag{4}
\]

Each has lower augmentation one and is fixed by the target involution.  For
every direction (v) in (4), the checker verifies (1),

\[
                    \nu(x_v)=0,qquad \nu(U_v)=1,      \tag{5}
\]

and adjoining (U_v) raises the projected rank from 24 to 25.

## Physical typing of the dual

Equation (3) is not merely an occurrence covector.  In the augmented
differential convention, `lower_B` is minus the sum of the six literal
private matching-feature rows selected by the canonical first-flat theorem.
Therefore

\[
             \nu=-\Lambda,qquad
 \Lambda=\sum_{j=1}^{6}m_j-\operatorname{ainc}.       \tag{6}
\]

The pinned first-flat audit proves that (Lambda) is physical and kills:

- all 288 complete repeated columns;
- the complete 8,580-column first-flat operator block;
- all absolute higher extensions, doubled-chart kernels, and natural Tate
  kernels;
- the listed physical stabilizers; and
- the exact endpoint-odd relative alpha cell.

It has primitive value one on a protected-zero anchor direction.  Thus the
separator branch of (5) is physically typed, not presentation-only.

## Fibre dichotomy

Let (J_0) retain the six lower rows and all (W), target, and ordinary
residue rows, and let (q) be physical anchor incidence.  Corrections of
(x_v) form the affine fibre

\[
                         x_v+\ker J_0.                 \tag{7}
\]

There are two possibilities.

1. If (q(k)\ne0) for some (k\in\ker J_0), normalize (k) to anchor
   value (-1).  This is exactly the physical relative generator from the
   committed indeterminacy theorem.  Equivalently, rescaling (k) adjusts
   (x_v) to (U_v).
2. If (q\) kills (ker J_0), row-space/kernel duality makes (q) factor
   through (J_0), and (3) is the primitive physical separator of the
   repair fibre.

After adjoining the placed Cartan column, the bordered anchor-dark theorem
is exhaustive: incompatibility with the anchor factorization gives a
normalized target-dark separator; a compatible external column leaves an
ordinary cokernel separator; and a compatible internal column gives a
unit-Cartan kernel.  Hence an explicit (U_v) is unnecessary for the
finite alternative.

## Scope

This closes the fixed and paired shared-repair fibres on the normalized
canonical faces-((3,5)) target/anchor projection, conditional on the
granted labelwise pure-residue companions and the already physical Cartan
packet.  It does not assert cyclic propagation, inactive-grade extension,
or the full conjecture.

## Verification

Run:

```text
python3 computations/verify_h3_cut_swap_shared_repair_anchor_fibre_dichotomy.py
python3 -O computations/verify_h3_cut_swap_shared_repair_anchor_fibre_dichotomy.py
python3 -I -S computations/verify_h3_cut_swap_shared_repair_anchor_fibre_dichotomy.py
```

Frozen ledger digest:

```text
8f16b223034005dec511a380645b24a70d575e136f3e8b3b83f6eda259f09a86
```
