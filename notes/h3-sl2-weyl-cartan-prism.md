# The two order-six grades have a canonical `SL2` Cartan prism

## Exact universal construction

The two source-cycle halves of the endpoint-recoloured order-six operator
are exchanged, up to sign, by the simultaneous colour Weyl action at sites
2 and 5.  This action has an explicit chain homotopy on every Cartan/Spencer
complex; no new abstract higher operation is required.

On one colour plane let

\[
 E=x\partial_y,\qquad F=y\partial_x,
 \qquad L_E=[d,\iota_E],\quad L_F=[d,\iota_F].          \tag{1}
\]

The root unipotents satisfy

\[
 e^{\pm L}-1=dH_{\pm L}+H_{\pm L}d,
 \qquad
 H_{\pm L}=\pm\iota_X\sum_{n\geq0}{(\pm L)^n\over(n+1)!}. \tag{2}
\]

All sums are finite on a homogeneous polynomial representation.  The signed
Weyl element is

\[
 w=e^{L_E}e^{-L_F}e^{L_E},qquad x\mapsto-y,quad y\mapsto x. \tag{3}
\]

If `x=e^{L_E}` and `y=e^{-L_F}`, the product-prism formula gives

\[
 H_w=xyH_x+xH_y+H_x,qquad w-1=dH_w+H_wd.             \tag{4}
\]

For the two commuting sites the tensor-product prism is obtained by the
same product formula.  The order-six audit has already shown that every
term has even diagonal sign parity, so this signed simultaneous Weyl action
is exactly the displayed unsigned tail-colour transport on the selected
cycles.

The checker `computations/verify_h3_sl2_weyl_cartan_prism.py` verifies (1)--
(4) exactly over `Q` on every polynomial differential form of polynomial
degree at most six.  The formulas prove the unbounded statement.

## Exact grading refinement

Let

```text
p = deg(11111111),
m = deg(11211211)
```

and let `s_0,s_1` be the two exact operator fine shifts.  The amended
endpoint-composition audit proves

\[
                            s_0+p=s_1+m.                \tag{5}
\]

Thus the two pieces are not in incompatible physical source-module degrees.
They are two weight components of one homogeneous map after the free
source-row summands receive their natural word degrees.  The need for a
relative cell comes from the distinct word labels, not from an ordinary
multidegree mismatch.

## What remains physical

Equations (2)--(4) identify the missing comparison more narrowly:

> descend the two root contractions `i_E,i_F` to the complete physical
> word-labelled source/correction complex, with zero `D`, `W`, target,
> ordinary-residue, and anchor readouts after totalization.

If those contractions descend, (4) gives the chart-nondiagonal gluing of the
two 341-term source cycles automatically.  Tensoring with the commuting
ridge class `-dOmega_v` then supplies the required eta/sigma packet.

If they do not descend, their failure is the connecting class in the
relative physical cone.  The augmented interchange alternative remains the
right conclusion: a terminal-visible failure is the normalized relative
generator, while terminal-zero failure allows the comparison to descend
after homological perturbation.

This formulation also explains the older covariance no-go.  A horizontal
identity `D_xT=L_xT` supplies the Lie derivative `L_x`, not the interior
operator `i_x`.  The missing datum was precisely the Cartan contraction,
which only exists in a principal-parts/relative resolution.  More
covariance rows alone cannot replace it.

## Scope

The theorem constructs the universal Weyl prism and proves source-module
grade compatibility.  It does not prove that the physical relative source
complex contains the root contractions, nor that their induced terminal
readouts have the required physical interpretation.

Verification:

```text
python3 computations/verify_h3_sl2_weyl_cartan_prism.py
python3 -O computations/verify_h3_sl2_weyl_cartan_prism.py
python3 -I -S computations/verify_h3_sl2_weyl_cartan_prism.py
```

Frozen ledger SHA-256:

```text
bde6a55fb7061024ff741b38acd22f02d2299d7e77f704eebeb9298b7b5abbb2
```
