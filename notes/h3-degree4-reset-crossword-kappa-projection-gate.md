# The five reset Eq residuals are off the cross-word kappa rows

## Verdict

The canonical degree-four reset does not force a nonzero

\[
             \delta\cdot Eq(\kappa_{AB})
       \quad\hbox{or}\quad
             \delta\cdot Eq(\kappa_{AC}).              \tag{1}
\]

For each deletion site `v=1,...,5`, the derived Hasse/Koszul filler has

\[
 d n_v=h_vYw,qquad
 \operatorname{tgt}(n_v)=\operatorname{ores}(n_v)=0,   \tag{2}
\]

and literal underived descent leaves

\[
                    h_v(H_0-u)e_{Eq}.                  \tag{3}
\]

The `Eq` symbol in (3) is the central conormal row.  It is not any of the
four corner-resolved rows `Eq_0,...,Eq_3` in

\[
                       \chi=\delta\cdot(B-Eq),
 \qquad \delta=(1,1,-1,-1).                            \tag{4}
\]

Moreover, the raw coefficient `h_v` has squarefree `2K2` site type, while a
physical cross-word mixed-naturality cell lies in the repeated `P3+K2`
grade and carries an `A/B` or `A/C` root label plus one of the four `DQ/PS`
operation-parent labels.  Thus all five literal reset cells have zero direct
projection to both `kappa` blocks.

An operation-blind formal placement of the central Eq row would send it to
the constant vector `(1,1,1,1)`, which is still dark:

\[
                    \delta\cdot(1,1,1,1)=0.            \tag{5}
\]

Only the missing physical `K_Eq`/cross-word comparison could assign a
nonconstant corner vector.  If it sends `e_Eq` to `e_kappa`, the exact value
on the `v`-th reset face is

\[
             \boxed{\chi_v=-h_v\,\delta\cdot e_\kappa.} \tag{6}
\]

No numeric value for (6) is currently proved.

Exact checker:
[`verify_h3_degree4_reset_crossword_kappa_projection_gate.py`](../computations/verify_h3_degree4_reset_crossword_kappa_projection_gate.py).

## 1. The five mixed reset coefficients

At internal word `12112`, the five denominator faces are the complementary
four-site hafnians

\[
\begin{aligned}
h_1&=x_{23}x_{45}+x_{24}x_{35}+x_{25}x_{34},\\
h_2&=x_{13}x_{45}+x_{14}x_{35}+x_{15}x_{34},\\
h_3&=x_{12}x_{45}+x_{14}x_{25}+x_{15}x_{24},\\
h_4&=x_{12}x_{35}+x_{13}x_{25}+x_{15}x_{23},\\
h_5&=x_{12}x_{34}+x_{13}x_{24}+x_{14}x_{23}.
\end{aligned}                                           \tag{7}
\]

Their fifteen matching monomials are pairwise distinct.  Every monomial uses
four internal sites once, so its raw site type is `2K2`.  The full augmented
word is already `01211222`, but word equality alone does not identify a
repeated fine-grade summand.

The complete Hasse four-cube constructs (2) in the derived presentation.  It
also fixes the chart face: the uncorrected external face is `+S_v`, and the
subtracted filler contributes `-S_v`.  Target and ordinary residue vanish.
The remaining failure is not one of those augmentation rows; it is physical
source descent of the central conormal in (3).

## 2. Why the corner projection is literally zero

The two objects have different complete labels:

| datum | reset residual | `kappa_AB/kappa_AC` |
|---|---|---|
| index | deletion site `v` | root `AB` or `AC` |
| word | `01211222` | response-to-`01211222` word arrow |
| repeated grade | raw squarefree `2K2` | repeated `P3+K2` |
| operation parent | central reset/Eq | one of four `DQ/PS` mates |
| Eq row | scalar `e_Eq` | corner-resolved `Eq_j` |
| next face | physical descent open | mixed naturality, then shifted ridge |

With the word/fine/repeated, root, operation-parent, and augmented-row
idempotents retained, these are different direct summands.  Hence

```text
Pi_kappa_AB(h_v*(H0-u)*e_Eq) = 0,
Pi_kappa_AC(h_v*(H0-u)*e_Eq) = 0
```

for every `v` in the currently constructed physical map.

This is an off-grade statement, not a claim that the reset residual has
`B=Eq`.  It is `Eq`-only in its own central conormal module.  Conflating that
module with `Eq_j` would silently adjoin precisely the missing comparison.

## 3. The strongest symmetry-forced placement is still dark

Suppose, only as a coefficient-level test, that the central Eq row is placed
without choosing a root or operation corner.  Operation-parent symmetry then
forces the constant vector

\[
                         Eq=(1,1,1,1).                 \tag{8}
\]

Equation (5) shows that its `delta` augmentation is zero.  The generic-even
formal shadow is also dark: its four-entry root vector is

\[
                         D=(-1,1,-1,1),qquad
                         \delta\cdot D=0.              \tag{9}
\]

Those identities do not construct a physical diagonal lift.  They show that
even the strongest operation-blind formal identification cannot force a
bright `kappa` value.

The other dark control is any tied packet:

\[
                        (B,Eq)=(q,q)
       \quad\Longrightarrow\quad \chi=0.               \tag{10}
\]

Thus the reset family remains either off-grade, operation-blind dark, or
tied dark until a source-labelled map makes its corner incidence
nonconstant.

## 4. Complete intersection prevents a unit shortcut

The five polynomials (7) form a height-five complete intersection in the ten
internal edge variables.  Their minimal resolution is Koszul, with Betti
numbers

```text
1, 5, 10, 10, 5, 1.
```

Every denominator-only first syzygy is generated by

\[
                         h_i e_j-h_j e_i.              \tag{11}
\]

Therefore every such syzygy coefficient lies in the proper ideal
`(h_1,...,h_5)`.  It cannot supply a unit face coefficient or force a
primitive aggregate corner vector.

If a future physical comparison assigns one common `e_kappa`, the aggregate
reset value is

\[
 \chi\left(\sum_v n_v\right)
      =-\left(\sum_vh_v\right)\delta\cdot e_\kappa.     \tag{12}
\]

The complete-intersection theorem rules out deriving a universal unit
multiple of `delta.e_kappa` from denominator-only Bianchi/Koszul operations.
A cross-word/full-source cell is still necessary.

## 5. Physical augmentation that the missing map must carry

The common polynomial conormal

\[
                          E=(H_0-u)e_{Eq}               \tag{13}
\]

has exact odd, generic-even, and beta-zero coefficient shadows.  They are
not one physical cell: their parity, word, endpoint, repeated-label, ridge,
and protected-row data differ.

To turn (3) into a statement about either `kappa` block, a source-labelled
`K_Eq(beta)`/cross-word mapping cone must preserve simultaneously:

- the response-to-cap word arrow and cap word `01211222`;
- the repeated `P3+K2` fine degree;
- the `A/B` versus `A/C` root label;
- the correct `DQ/PS` operation parent;
- private and corner-resolved reduced-`Eq` occurrence rows;
- target and `W`;
- physical `q` and anchor;
- scalar and labelled ordinary residue;
- the shifted ridge and its `-d(q_xv^01)` connection; and
- eta and sigma.

The derived reset already has target and ordinary residue zero.  That useful
augmentation fact does not supply the missing word/grade/corner map or its
ridge face.

After both word sections are formally granted, the cross-word rank audit
identifies the mixed reduced-`Eq` naturality square as the first augmented
obstruction and the shifted ridge as the second.  The degree-four reset
provides a polynomial coefficient for the same formal conormal, but it
neither constructs that mixed square nor decides (6).

## Exact remaining fork

```text
no physical K_Eq/cross-word comparison
    -> all five reset-to-kappa projections are literally zero/off-grade;

physical comparison with delta.e_kappa = 0
    -> reset faces remain chi-dark;

physical comparison with delta.e_kappa != 0
    -> chi_v=-h_v*delta.e_kappa, but denominator-only CI/Koszul
       does not produce a primitive unit aggregate.
```

So the reset does not force a nonzero `delta.Eq`.  It narrows the open datum
to the same two root-labelled mixed Eq lifts already isolated by the
four-site exhaustiveness decomposition.

## Scope and verification

This is exact for the canonical `h=3` degree-four reset, the five-denominator
complete intersection, the derived Hasse/Koszul filler, the three formal
reduced-Eq projections, and the typed private-minus-Eq quotient.  It does not
construct or assign a numeric value to the missing physical `K_Eq` lift.

Run:

```text
python3 computations/verify_h3_degree4_reset_crossword_kappa_projection_gate.py
python3 -O computations/verify_h3_degree4_reset_crossword_kappa_projection_gate.py
python3 -I -S computations/verify_h3_degree4_reset_crossword_kappa_projection_gate.py
```

Frozen ledger SHA-256:

```text
f193da45cec98df29ef60c808ba7ba728bd3466df620aa51b59fa84a5ea2bb2f
```
