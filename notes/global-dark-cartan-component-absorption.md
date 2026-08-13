# Use every Cartan projection at once: bright component, typed exit, or global kernel

## Result

The exact component-splitter cokernel shows that a complete physical Cartan
row cannot generally be cut down to one matching component.  That splitter
is unnecessary for the basic interference alternative.

Decompose the complete literal incidence presentation—using source word,
matching tail, endpoint orientation, and fine-grade labels—into its connected
critical blocks

\[
                         M=\bigoplus_\Gamma M_\Gamma.   \tag{1}
\]

Any physical column touching two proposed blocks joins them, so after taking
actual connected components (1) is block diagonal.  Let `G` be the **whole**
placed physical Cartan column and write `g_Gamma` for its analytical
projection to one block.  Suppose each zero-holonomy block has corank one,
with left charge `ell_Gamma`.

Then exactly one of the following happens.

Assume that every block tested by the bright alternative is
**anchor-critical**: its coherent right-kernel mode has nonzero pure-anchor
charge.  Then:

1. For some component,

   \[
                       \ell_\Gamma^Tg_\Gamma\ne0.      \tag{2}
   \]

   The pure anchor charge is nonzero, so the Schur formula gives a localized
   source unit.
2. Every component is dark.  Solve

   \[
                              M_\Gamma y_\Gamma=g_\Gamma. \tag{3}
   \]

   If the current saturated inventory omits a nonzero coordinate of `G-Cy`,
   that coordinate is a literal typed exit and joins another component.
3. Every component is dark and the inventory is exhaustive.  The potentials
   in (3) assemble to

   \[
                              G=Cy.                    \tag{4}
   \]

   Hence `(-y,1)` is a unit-coefficient kernel class of the **complete**
   physical map.

No partial matching sum is asserted to be a source generator.  Component
projections are used only to decide (2) or solve (3); the physical Cartan
chain remains intact throughout.

Checker:
[`verify_global_dark_cartan_component_absorption.py`](../computations/verify_global_dark_cartan_component_absorption.py).

## Proof

For a corank-one block, left-row duality gives

\[
                  \ell_\Gamma^Tg_\Gamma=0
       \quad\Longleftrightarrow\quad
                  g_\Gamma\in\operatorname{im}M_\Gamma. \tag{5}

Thus (3) exists on every dark block.  Taking their direct sum gives

\[
       \bigoplus_\Gamma M_\Gamma y_\Gamma
          =\bigoplus_\Gamma g_\Gamma.                  \tag{6}

If the projections exhaust every complete label, their direct sum is
faithful and (6) is exactly (4).  If they do not, the difference is supported
in the complementary labels.  Fine-label saturation makes a nonzero such
coordinate a genuine exit rather than an omitted internal row.

The bright branch uses the already proved Schur identity

\[
 \det\begin{pmatrix}M_\Gamma&g_\Gamma\\
                     h_\Gamma^T&\alpha\end{pmatrix}
 =-\kappa_\Gamma(h_\Gamma^Tc_\Gamma)
                     (\ell_\Gamma^Tg_\Gamma).          \tag{7}

The anchor-critical hypothesis makes the first charge nonzero.  The uniform
Cartan placement theorem makes the connector source-provenant and nonzero in
its exact marked label.  Hence (2) makes (7) a source unit.  A component not
yet known to carry such an anchor row is not called bright here; placing
arbitrary source components into an anchor-critical cover remains part of
the global entry theorem.

## Why this bypasses the component-projector obstruction

Known complete group bars are constant in the matching-occurrence factor and
cannot span a matching-centered cut.  That prevents replacing `G` by one
`g_Gamma` as a physical chain.  Equations (3)--(6) do nothing of the sort:
they compare every component of the single complete equality simultaneously.

The two statements are compatible:

```text
component-supported physical Cartan boundary     generally unavailable;
all component projections dark simultaneously   one global kernel class.
```

This is the same distinction as solving a block-diagonal linear equation by
components without asserting that the coordinate projections of its right
side are independently generated.

## The dark terminal branch

Once (4) holds in the protected augmented complex, the terminal-safe theorem
applies to `k=(-y,1)`.

* If the physical terminal detects `k`, normalize it to the relative
  generator.
* If it kills `k`, cancel this unit direction from the augmented
  presentation without changing image, cokernel, or the terminal image of
  the remaining kernel.
* Another terminal-visible kernel class is the generator.
* If the physical terminal kills the entire protected kernel, row-space
  duality produces the physical Fredholm separator.

Thus the all-dark outcome has no unresolved linear rank case.  Its only
remaining hypothesis is construction/transport of the physical terminal in
the common exhaustive grade.

## Finite enlargement and the proposed global potential

Every nonzero complementary residual adds at least one previously unjoined
literal fine label to the saturated incidence component.  The ambient source
has finitely many occupied scalar cells and finitely many labels in the
selected packet.  Therefore repeated residual enlargement terminates in
either a bright component or the exhaustive global-kernel branch.

This gives a more robust leading potential than matching flip distance:

\[
  \bigl(\#\text{unjoined occupied fine labels},
         \dim\text{relative correction domain}\bigr).       \tag{8}
\]

A typed residual lowers the first coordinate by joining its label.  A
terminal-dark unit cancellation lowers the second.  Schur unit, relative
generator, and separator terminate.  Active/Hall exits still need a theorem
showing that their physical reselections do not increase the first coordinate.

## Scope

The theorem assumes an exhaustive connected-component decomposition of the
complete selected presentation, corank-one zero-holonomy blocks, and a
nonzero pure-anchor charge on every block to which the Schur-unit conclusion
is applied.  It does not show that every arbitrary source enters such an
anchor-critical cover, construct the physical rootless/inactive terminal on
the global kernel, or land every typed exit at four-good rank.  Its advance
is logical: a new occurrence-local physical bar is **not** required to
assemble dark Cartan potentials.

## Verification

Run:

```text
python3 computations/verify_global_dark_cartan_component_absorption.py
python3 -O computations/verify_global_dark_cartan_component_absorption.py
python3 -I -S computations/verify_global_dark_cartan_component_absorption.py
```

Frozen ledger SHA-256:

```text
60547efc8b6d06b2bea0d55932fbe85e6227b99e16b138de43c8a02b4ee87880
```
