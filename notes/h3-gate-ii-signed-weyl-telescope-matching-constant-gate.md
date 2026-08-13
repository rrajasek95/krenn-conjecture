# The signed-Weyl telescope fixes the target but remains matching-constant

## Result

Pair all even-order sites and choose a colour plane `(c,i)`.  On one site
let the signed Weyl operator be

\[
          w e_c=-e_i,\qquad w e_i=e_c,
          \qquad w e_k=e_k
\]

for the third colour `k`.  On the `j`th site pair put `W_j=w_xw_y` and let
`h_j` be its physical Cartan homotopy.  The standard telescope

\[
 H_W=\sum_j P_{j-1}h_j,
 \qquad P_j=W_1\cdots W_j
\]

satisfies

\[
                  dH_W+H_Wd=P_m-1.                 \tag{1}
\]

Each pair operator exchanges `cc` and `ii` with positive sign and fixes
`kk`.  Hence `P_m` fixes the ternary diagonal tensor and (1) is target-safe.

This is a useful positive theorem: the marked-pair term supplies the pure
root character `chi_w`, while the other pair terms provide its global
target companion.  It does **not** construct the Gate-II pointed
comparison.

Checker:
[`verify_h3_gate_ii_signed_weyl_telescope_matching_constant_gate.py`](../computations/verify_h3_gate_ii_signed_weyl_telescope_matching_constant_gate.py).

## The exact quotient mismatch

Every local colour action preserves the underlying site matching, matching
index, repeated-edge label, and second-Hasse chart tag.  Thus the marked
root character supplied by the telescope has tensor form

\[
                         \chi_w\otimes\mathbf1_{105}. \tag{2}
\]

Gate II needs

\[
              \chi_w\otimes L_{01},\qquad
 L_{01}=(2A-B-C)H,                                  \tag{3}
\]

where `L01` is matching-centered.  Exact enumeration gives

\[
                   \langle\mathbf1_{105},L_{01}\rangle=0. \tag{4}
\]

Already on the three chart factors, (2) and (3) are

```text
telescope matching factor       (1, 1, 1)
endpoint-odd Cartan factor       (0, 1,-1)
Gate-II root-even factor         (2,-1,-1).
```

These three lines are independent.  The telescope provides the first, not
the third.

The downstream test is equally sharp.  In the word-`0102` twelve-occurrence
block, the telescope again has constant factor `1_12`.  The private detector

\[
                         e_0^*+e_3^*-e_1^*-e_6^*
\]

reads zero on `1_12` and `-13/6` on the required private face.  Therefore
the pair companions do not manufacture the `0102` occurrence section or
its `dq23` reinsertion.

## Why multiplication by the centered projector is circular

The complete Cartan rectangles over all perfect matchings cancel pairwise.
Projecting one rectangle or multiplying `H_W` by `L01/P_f` selects a proper
matching-occurrence component of that cancelling complete prism.  Such a
selection is source-provenant only after a physical occurrence/block
splitter has been constructed.

That splitter is precisely the open Gate-II carrier comparison

\[
                 d\Gamma_L=t_L-L_{01},\qquad
                 d\Gamma_R=t_R-R_{01}.
\]

Using `L01` to localize the telescope before this comparison would assume
the object being sought.

## Consequence

The signed-Weyl telescope removes a separate difficulty: once the
matching-centered carrier is physically landed, it supplies its target-safe
`chi_w` colour decoration.  The remaining problem is purely the carrier
landing, including its `R01/L01`, first-PP, `0102`, `q/dq`, labelled
`Q/ores`, `W`, and ridge faces.

This is exact for the canonical `K8` occurrence quotient and the literal
`0102` block.  It does not claim a physical centered carrier.  Frozen
ledger SHA-256:

```text
68ba278b9683c123a69f263e7ef8ce8750bb3354c6e29c893fc8751dede178ea
```
