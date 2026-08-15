# The intrinsic paths have one coefficient shadow, not two protected augmentations

## Result

The literal selected `h=3` carrier does not yet have separately defined
protected `B` and `Eq` augmentations.  It has one source-derived coefficient
augmentation.

For `q=23,45`, the two canonical composites

\[
 I_cD_c\Phi d,
 \qquad
 dI_c\Phi_{\widehat q}D_r
\]

are equal on every official EqSystem relation.  Their marked P2 restrictions,
followed by the literal lower coefficient map

```text
0112/q23:21 -> B1,       0121/q45:12 -> B4,
```

give the common six-label value

\[
 \delta_+={c_1^++c_4^+\over8}
 =\tfrac14(-1,2,-1,-1,2,-1).                         \tag{1}
\]

This is a theorem in the occurrence-labelled source.  But its output type is
one module `U_common`; neither `B` nor `Eq` is an edge, relation, matching,
root, restriction, or reinsertion label in that module.  Therefore the
literal operators do not yet define either protected copy separately.

The exact checker is
[`verify_h3_intrinsic_paths_protected_augmentation_factorization_gate.py`](../computations/verify_h3_intrinsic_paths_protected_augmentation_factorization_gate.py).

## Why the existing values do not settle the lift

After protected copies are adjoined, three familiar lifts of (1) can be
written:

```text
tied       (delta_plus,delta_plus),
B-only     (delta_plus,0),
Eq-only    (0,delta_plus).
```

For

\[
 D_6=(-1,2,-1,-1,2,-1),
 \qquad \Omega=(D_6,-D_6),
\]

their detector values are respectively `0,3,-3`.  The intrinsic source
operators cannot choose among these vectors because their codomain precedes
the copy split.

This is not a physical counterexample: the three vectors are possible lifts
in an enriched codomain, not three constructed source maps.  In particular,
the normalized solutionwise projection to the `B` top is a quotient map, and
the internally tied cap `r0` is a genuine cap column, but neither fact proves
that the selected source carrier lands in that cap column.  Treating either
lift as the answer would assume the comparison being tested.

## The first physical obstruction

The first attempt to relate the source occurrence path to the cap Eq path is
the pointed `P_f/K_Eq/D4` naturality square.  Its four objectwise edges are

```text
P_f bottom, K_Eq left, K_Eq right, D4 top.
```

Their boundary has rank three and the primitive cycle

\[
                         (1,-1,1,-1)                  \tag{2}
\]

generates `H1 = Z`.  In the typed quotient

```text
rows                       R_E14, central E, mixed-square incidence
available edge rank        2
rank with comparison       3
primitive detector         (0,0,1).
```

Thus the coefficient shadows `R_E14+E` add correctly only after the mixed
operation-incidence coordinate has been forgotten.  Restoring literal source
types exposes a missing two-cell.  There is no unequal physical `B/Eq` face
before this point: separate readouts are not defined because the comparison
is not yet a morphism in the source category.

If mixed incidence is granted formally, the first literal proper-face test is

\[
 \text{each marked D3 occurrence}
 \longmapsto -(B_1+B_4)=-2d_{\rm even}                \tag{3}
\]

in the physical repeated `P3+K2` grade.  The D4 boundary signs
`(-1,+1,-1,+1)` then transport (3) to the required hidden root-lower face
`-E`.

## The smallest exact extra datum

Put

\[
 D_{\rm root}=(-1,1,-1,1),\qquad
 d_{\rm even}={B_1+B_4\over2},\qquad
 E=2D_{\rm root}\otimes d_{\rm even}.
\]

Normalize one nonzero component of `E` and order rows as

```text
top R, root lower, root Eq, word-resolved ores.
```

The missing source-labelled section must have

\[
                     (R,-E,0,+E).                    \tag{4}
\]

The existing internal cap face has

\[
                     (0,+E,+E,-E).                   \tag{5}
\]

Their sum is

\[
                     (R,0,+E,0).                     \tag{6}
\]

Consequently (4), together with the already physical cap identity (5), is
exactly the same-normalization factorization: the source top coefficient and
the cap Eq coefficient agree, while the hidden lower `-E` and labelled
ordinary-residue `+E` faces cancel their internal cap mates.

The minimal new datum is therefore one **monic source-labelled mixed
mapping-cylinder/Tate two-cell**

\[
                         \kappa_{\rm orb,Eq},          \tag{7}
\]

or one pointed AugP2 schema containing it.  It must have boundary (2), the
proper faces (3)--(4), the invisible physical `K_Eq` cap face, and the literal
face-3/face-5 transport to `B4/B1`.  Monicity at the top and evenness of the
alternating augmented right side fix the factor two in `E`.

One cell is minimal: (2) is a primitive free rank-one obstruction.  A formal
Eq coordinate, the coefficient equality alone, or either hidden face by
itself leaves its mixed-incidence detector nonzero.  Conversely one monic
two-cell kills that `H1`; its typed proper faces then give (6).

## Consequence and scope

If (7) is physically constructed, the protected augmentations factor through
the two equal intrinsic paths with the same normalization.  Hence `B=Eq` on
the selected carrier, while the requested balanced `B`-only boundary has
detector value `3`; the balanced branch closes.

This note proves the exact missing-cell criterion, not existence of (7).  It
covers the official EqSystem paths, the marked q23/q45 coefficient shadow,
the integral first mapping square, and the hidden lower/Eq/ores packet.  It
does not turn the protected copy split into original source data, construct
the later shifted ridge, or prove a full Fredholm terminal.

## Verification

```text
python3 computations/verify_h3_intrinsic_paths_protected_augmentation_factorization_gate.py --mode structural
python3 -O computations/verify_h3_intrinsic_paths_protected_augmentation_factorization_gate.py --mode full
python3 -I -S computations/verify_h3_intrinsic_paths_protected_augmentation_factorization_gate.py --mode exhaustive
```

Frozen ledger SHA-256:

```text
b09443bf779cc04f5f72972a5b66d07968913a38707cc6e9b205c4b9b9782f68
```
