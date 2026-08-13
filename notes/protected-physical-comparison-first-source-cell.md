# A protected comparison exists on the physical relabeling orbit; off orbit its first missing datum is one literal mapping-cone family

## Result

Let

\[
 \Phi:L_\gamma\longrightarrow L_{h=3},\qquad
 J_{h=3}\Phi=A J_\gamma                              \tag{1}
\]

be the requested comparison on the **complete physical relative domains**.
It must be nonzero on the placed Cartan/derived direction; the formal zero
chain map is irrelevant.

There is one exact positive construction. If `gamma` is obtained from the
canonical packet by a physical site/colour relabeling which transports the
source word, fine degree, repeated `P3+K2` label, orientation, and every
protected row together, take

\[
                        \Phi=\rho_* .                  \tag{2}
\]

Physical source covariance gives (1), with `A=rho_*` on the protected
codomain. This covers the oriented physical relabeling orbit of the
canonical packet.

It does **not** construct (1) for an arbitrary exhaustive component outside
that orbit. Universal Hasse/principal-parts operations are internal to a
fixed multigraded block. A map between two distinct fixed label blocks which
intertwines their central grade idempotents is zero. A nonzero off-orbit map
therefore needs an explicit shifted label morphism realized by a physical
source cell; calling two presentation vector spaces isomorphic does not
supply one.

After using the best existing shifted PP/Hasse construction, the first
remaining physical obstruction is now exact:

> In every relevant face, construct a physical relative cell `M_v` whose
> complete literal image is the forced four-corner full-nine/Eq aggregate,
> with zero protected target rows and the prescribed eta/sigma terminal.

The complete two-chart module proves that no chart difference or Eq-only
correction supplies this image. Thus arbitrary comparison is not yet
constructed, but its first source cell is sharply specified.

Checker:
[`verify_protected_physical_comparison_first_source_cell.py`](../computations/verify_protected_physical_comparison_first_source_cell.py).

## 1. What is already positive

For a deleted odd face `v`, the physical two-chart principal-parts square
exists. Its mixed symbol is in the `pq`-direct sector on one side and the
`pr`-two-star sector on the other. Fine grading forces the unique shift

\[
                    \sigma=e_{x,0}+e_{p,0}+e_{q,0}.    \tag{3}
\]

The complete derived Hasse/Koszul filler then has

```text
source word after deleting x       1211222
fine/repeated grade                canonical labelled P3+K2
boundary                           h_v Y w
target, ordinary residue           0, 0
correcting chart face              -S_v
```

So the comparison does not stop at an abstract polar symbol. It reaches a
source-valid cell in the prolonged derived presentation with the right
shift and protected augmentation.

The Hasse coproduct theorem also means that the higher Boolean faces are
not new independent choices. Once the initial physical comparison cell and
its label map exist, their higher coherences are forced by the canonical
cosimplicial totalization.

## 2. The first off-orbit and underived obstructions

There are three successive distinctions.

### Fixed grade versus transported grade

Let `e_gamma` and `e_h3` be the central label idempotents. For
`gamma != h3`, a fixed-label degree-zero map satisfies

\[
 \Phi e_\gamma=e_\gamma\Phi,
 \qquad e_\gamma|L_\gamma=1,
 \qquad e_\gamma|L_{h=3}=0,
\]

and hence `Phi=0`. Physical relabeling avoids this conclusion because it
transports the label algebra itself. An arbitrary off-orbit component has
no such transported label map yet.

Ordinary tail multiplication is not that map. The two halves of the Kähler
ridge have site degrees

\[
 e_p+e_q\quad\hbox{and}\quad e_x+e_v,                  \tag{4}
\]

and adding the same tail preserves their difference. The shifted comparison
must keep the two labels separately; a common multiplier cannot homogenize
them.

### Old denominator complex versus shifted derived filler

Before the derived filler, coefficient reset has commutator

\[
          \omega(d_{v,m_v})=h_vY_0.                    \tag{5}
\]

The five nonzero labelled components have rank five modulo the old pure
denominator image. This is why the minimal source type is a shifted,
denominator-marked two-edge Rees square, not a bare symbol with a declared
boundary.

The prolonged Hasse/Koszul filler cancels (5) in the derived presentation.
After projection back to the underived physical source, however, its first
commutator is

\[
                         (H_0-u)e_{\rm Eq}.             \tag{6}
\]

Equation (6), not target or ordinary residue, is the first remaining
physical descent obstruction after the derived construction.

### Derived filler versus complete literal physical image

The literal audit reconstructs all five repeated `P3+K2` components. In
each component one chart has `288` independent columns. Doubling the chart
gives `576` columns of rank `288`; its kernel consists exactly of pairwise
`pq-pr` presentation differences. Every selected pure `r0` label has at
least `42` private full-nine features, so its private pivot forces

\[
                       x_{pq}+x_{pr}=0.                 \tag{7}
\]

The same sum controls the physical Eq, target, anchor, and chart-neutral
terminal values. Hence a chart difference cancels its own entire physical
column; it cannot retain the cap contribution needed by (6).

Across all `75` choices of four pure labels, the endpoint-odd aggregate has
exactly `360` literal matching features. A single new image direction is
sufficient and forced. Writing

\[
                   \alpha=(-1,1,1,-1)=-\delta,
\]

its required signature is

```text
literal full-nine boundary          sum_j alpha_j B_j
four Eq rows                        (-1,+1,+1,-1)
ordinary residue                    0
D, W, target, anchor incidence      0
eta_z                               1 + delta_(1,z) u_z/t
sigma                               -q_pq^22
```

Call this image `J(M_v)`. Adding it makes the desired full fiber target lie
in the augmented image. Without it, the doubled charts plus a projected
Eq-only column fail an explicit primitive separator. This is an exact
one-cell **membership criterion**, not a construction of `M_v`.

For the complete domain, the missing datum is one source-provenant
equivariant family `M_v` over the five labelled faces, or five compatible
instances. Rank five in (5) says that all five associated-graded components
must occur; it does not prove that five unrelated physical generators are
necessary.

## 3. Why exact terminal equality is no longer part of this task

Suppose (1) is constructed on the complete domains. The physical terminal
rows `q_gamma` and `q_h3` need not agree identically.

If

\[
                (q_\gamma-q_{h=3}\Phi)|_{\ker J_\gamma}\ne0,
\]

a kernel witness `x` has `Phi x in ker J_h3`, and at least one of
`q_gamma(x)` or `q_h3(Phi x)` is nonzero. Because both rows are physical on
their complete relative domains, `x` or `Phi x` is the existing relative
generator. If the defect vanishes, it factors through `J_gamma`, transports
`q` on the kernel, and feeds the existing Fredholm alternative.

Thus construction of (1) is the whole live comparison problem. Requiring
exact terminal equality would impose a stronger condition than the proof
needs.

## 4. Domain/codomain audit for the two tempting shortcuts

The objects used nearby have different types:

| object | type | physical meaning |
|---|---|---|
| `e_s^*` | `X^*` | literal coordinate of a marked source occurrence |
| `h_phys` | `X^*` | reduced pure/target anchor row; not generally `e_s^*` |
| `G` | new generator in `X plus kG` | complete physical Cartan source chain |
| `b=J(G)` | protected codomain `Y` | full Cartan column |
| `lambda` | `Y^*` | left separator of an external full column |
| `q` | `(X plus kG)^*` | physical terminal on the relative domain |
| `Phi` | `Hom(L_gamma,L_h3)` | protected source comparison |

This resolves both shortcuts precisely.

First, the marked `h=e_s^*` in the frame lift is a genuine literal source
coordinate. If its lift fails and `lambda^T M=e_s^*`, the marked old source
column is a coloop/pivot, so that separator branch is a source-unit exit.
But `e_s^*` is not the physical anchor `h_phys`; a successful marked kernel
still needs the anchor pairing or its dual.

Second, for the full augmented Cartan column there is always

```text
b in im J       -> (-y,1) is a unit-coordinate kernel;
b not in im J   -> lambda J=0 and lambda b=1.
```

Here `G` is the adjoined source generator, while `b=J(G)` is its codomain
column. On the external branch `lambda` is a codomain-dual Fredholm
separator detecting the new Cartan column. It is not automatically the
domain terminal `q`, the physical anchor, or a localized unit isolating an
old optical occurrence. The full-column alternative therefore does not
remove the marked-anchor or protected-comparison work.

## Sharp frontier

The shortest comparison attack is now:

```text
component in physical relabeling orbit
        -> transport every label -> protected Phi exists

arbitrary off-orbit exhaustive component
        -> shifted PP/Hasse derived filler
        -> literal M_v image membership in each labelled face
        -> higher coherences forced by Hasse totalization
        -> protected Phi
        -> q defect nonzero: generator
           q defect zero: Fredholm
```

The immediate theorem to prove is therefore not arbitrary-tail naturality
and not exact terminal equality. It is physical membership of the one-cell
image above, together with an oriented word/fine/repeated label morphism
from the placed exhaustive component to the canonical packet.

## Verification

```text
python3 computations/verify_protected_physical_comparison_first_source_cell.py
python3 -O computations/verify_protected_physical_comparison_first_source_cell.py
python3 -I -S computations/verify_protected_physical_comparison_first_source_cell.py
```

Frozen ledger SHA-256:

```text
6f1144c07c2eadc14eeb5244759802c110db8874a78a7e4814e727f304d15c3e
```
