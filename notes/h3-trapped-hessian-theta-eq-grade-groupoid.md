# The transpose grade defect is a flat two-object groupoid

## Result

Let `g` be the canonical faces-`(3,5)` repeated fine grade and let
`gT=theta(g)`, where

```text
theta = (P <-> S and response-head transpose) followed by (0 <-> 1).
```

The endpoint-polarization theorem showed that `theta` completes the
sixteen-term Hessian symbol but sends the physical six-term row `Lambda` to
the conjugate row `LambdaT`.  Keeping the two grades as separate objects
resolves this defect exactly:

```text
              theta                 theta
       g ----------------> gT ----------------> g,
                       theta^2 = id.
```

This is not another `pq/xv` Kähler obstruction.  The `pq/xv` transition is
the nonconstant ratio `U=u/t`, so its first jet contains the mandatory
diagonal `dU`.  Here `theta` is a constant finite permutation.  Hence

\[
 J^1(\theta)=
 \begin{pmatrix}\theta&0\\0&\theta\end{pmatrix},
 \qquad d\theta=0,
 \qquad J^1(\theta)^2=1.                              \tag{1}
\]

There is no first-principal-parts diagonal and no residual fine-grade
holonomy on the two-edge loop.  The remaining open class is the physical
reduced-Eq attachment itself, not transport between `g` and `gT`.

Checker:
[`verify_h3_trapped_hessian_theta_eq_grade_groupoid.py`](../computations/verify_h3_trapped_hessian_theta_eq_grade_groupoid.py).

## 1. The minimal grade category

The literal 24-coordinate degrees differ only in two coordinates:

\[
                  g^T-g=e_{(0,1)}-e_{(1,1)}.           \tag{2}
\]

Thus a one-object fixed-grade model is false.  Applying `theta` again
returns `g`, so two objects are sufficient.  The six canonical private
matching features and their six transposes are disjoint, and `theta` pairs
them bijectively.  This is the minimal groupoid retaining the actual fine
labels.

Equation (1) is load-bearing.  A chart-ratio model would manufacture a
spurious `dU` diagonal and a logarithmic residue.  Neither occurs for this
literal source automorphism.  The apparent “grade holonomy” in a
single-component presentation is precisely the omitted second object; it
does not survive in the correct two-object category.

## 2. Physical q and terminal compatibility

Write `F_g` and `F_gT` for the two six-element feature sets.  The physical
readouts are

\[
 \Lambda_g=\sum_{F_g}F-\operatorname{ainc},\qquad
 \Lambda_{g^T}=\sum_{F_{g^T}}F-\operatorname{ainc}.    \tag{3}
\]

The protected marked product, hence `ainc`, is fixed by `theta`.  Exact
feature transport gives

\[
                  \Lambda_{g^T}\circ\theta=\Lambda_g. \tag{4}
\]

Therefore the physical-q cocycle is zero before taking any quotient; no
new protected-row homotopy is needed for the grade arrow.

The other augmented rows are compatible in the same objectwise sense:

- target and `W` are fixed;
- word is fixed on the equal-colour endpoint corner orbit;
- ordinary residue is transported between its two labelled copies;
- `eta_0` and `eta_1` are exchanged (the remaining eta labels transport
  with their sites);
- the unordered external `P-S` sigma edge is fixed.

This is equivariance, not an assertion that the two labelled ordinary
residue coordinates were already the same coordinate.  Collapsing the two
objects before applying `theta` would reintroduce exactly the false
fine-grade identification that the groupoid avoids.

## 3. Composition with the central reduced-Eq cone

Let

\[
 E=(H_0-u)e_{\rm Eq},\qquad
 K_{\rm Eq}(\beta)\longmapsto E.                       \tag{5}
\]

The formal cone is central under `theta`: the global target homogenizer,
the Eq label, and `beta` are fixed.  Objectwise there are two transported
copies

```text
K_Eq(beta)_g  -> E_g,
K_Eq(beta)_gT -> E_gT,
```

and their square with `theta` commutes.  Going around the two-object loop
is the identity on both `K_Eq` and `E`.  Thus composing with the central
cone leaves **no** fine-grade holonomy class.

The division of labour is exact:

1. `theta` transports `LambdaT` back to `Lambda` and carries all physical
   terminal labels equivariantly;
2. `K_Eq(beta)` cancels the reduced-Eq boundary objectwise;
3. `K_Eq(beta)` cannot itself serve as the grade arrow, because its central
   boundary has no private matching-feature component.

Consequently it is enough to construct one source-labelled
response-to-Eq attachment in the complete augmented word/fine/repeated
complex at `g`.  Applying the physical involution constructs the conjugate
attachment at `gT` automatically.  Conversely, the formal cone (5) alone
does not prove that such a physical source cell exists.

## Scope

This is an exact theorem about the two literal fine grades, the paired
private matching features, first principal parts, the physical
`sum-six-ainc` readout, and the augmented terminal permutation.  It removes
the proposed extra grade-holonomy obligation.  It does not construct the
source-valid reduced-Eq/response mapping-cone generator; that remains the
single descent datum.

Run:

```text
python3 computations/verify_h3_trapped_hessian_theta_eq_grade_groupoid.py
python3 -O computations/verify_h3_trapped_hessian_theta_eq_grade_groupoid.py
python3 -I -S computations/verify_h3_trapped_hessian_theta_eq_grade_groupoid.py
```

Frozen ledger SHA-256:

```text
79a575e9fbd4794eb1dd92f088ccb8c69f90eea1bd854facf996200935bc712e
```
