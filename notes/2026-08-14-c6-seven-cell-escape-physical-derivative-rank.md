# The cap-avoiding escape is a new physical state; the killed cap sector deletes

## Outcome

The decisive derivative test on the sharp seven-cell `C6` cap packet is
completely finite.  After imposing the mixed-row equation, the complete
physical derivative tensors of all three live cap cells vanish on **all 729
output words**.  Every minimal cap-avoiding pure escape has a derivative
supported on `111111`, so it is outside the cap-derivative span and raises
rank exactly

\[
                              0\longrightarrow1.          \tag{1}
\]

The source-natural support reduction therefore goes in the opposite direction
from the hoped-for deletion: remove the three killed cap cells.  More strongly,
the augmented packet has exactly the pure-one matching tensor, and it reduces
without changing any coefficient to the three cells of the chosen escape
matching.  The escape is the surviving transfer state.

There is a useful qualification.  Against the derivatives of **all seven**
old cells, rather than the jointly linear three-cell cap block, eight escapes
are tangent-dependent because they share one old residual cell; the four
disjoint escapes remain independent.  That larger tangent dependence does
not authorize the affine cut-cell move: the old and new cells occur together
multiplicatively.  The exact three-cell support reduction is checked directly
in all twelve cases.

The checker is
`computations/verify_uniform_c6_seven_cell_escape_physical_derivative_rank.py`.

## 1. The seven-cell packet and its forced equation

Use cap edge `34`, with all three diagonal cap colours live, and the two
colour-one residual matchings

```text
core : 05|12,                 mate : 01|25.                (2)
```

Choose coefficients

```text
q34^00=q34^11=q34^22=1,
q05^11=q12^11=q01^11=1,       q25^11=-1.                  (3)
```

The common residual is

\[
 H=q_{05}^{11}q_{12}^{11}+q_{01}^{11}q_{25}^{11}
  =1-1=0.                                                   \tag{4}
\]

Before (4), the three nonzero coefficient shapes are

\[
 q_{34}^{00}H\,e_{111001},\qquad
 q_{34}^{11}H\,e_{111111},\qquad
 q_{34}^{22}H\,e_{111221}.                                \tag{5}
\]

The first and third are mixed rows.  Since their cap cells are live, exact
mixed vanishing forces (4).  It then kills the cap-containing contribution to
the pure row as well, so pure normalization requires a matching avoiding
`34`.

At the point (3)--(4), the seven-cell packet itself has zero matching tensor.
This is not a formal cancellation in an auxiliary presentation: the checker
expands all fifteen `K6` matchings in every word and obtains the zero vector in
the original `Q^729` coefficient space.

## 2. Complete cap derivatives

Let `D_c` be the physical derivative with respect to `q34^cc`.  Because every
cap-containing occurrence uses exactly one cap cell, these three variables are
jointly linear, and their universal shapes are exactly

\[
 D_0=H e_{111001},\qquad
 D_1=H e_{111111},\qquad
 D_2=H e_{111221}.                                        \tag{6}
\]

Modulo the forced equation `H=0`,

\[
                 D_0=D_1=D_2=0\quad\text{in }\mathbb Q^{729}. \tag{7}
\]

Thus their physical rank is zero, not three and not one.  In the universal
coefficient ring their pure-one image is the submodule

\[
                            (H)e_{111111}.                 \tag{8}
\]

The normalized escape is `e_111111`.  Membership in (8) would require the
illegal multiplier `1/H`.  Localizing at `H` contradicts the live mixed-row
equation `H=0`.  After specialization, the cap image drops to zero while the
escape remains nonzero.  This is the exact non-flat span obstruction.

## 3. All twelve cap-avoiding escapes

There are fifteen perfect matchings on six sites and three contain `34`, so
there are twelve cap-avoiding candidates.  Relative to the seven-cell support:

```text
8 candidates share one old residual cell and need 2 new cells;
4 candidates are disjoint from the old residual and need 3 new cells.     (9)
```

For each candidate the checker adds precisely its missing colour-one cells
and normalizes that matching monomial to one.  Complete expansion then gives

\[
                         H_{\rm augmented}=e_{111111}       \tag{10}
\]

on all 729 coordinates.  There are no other pure or mixed output words.

The derivative with respect to every new cell is a nonzero scalar multiple
of `e_111111`.  Across the twelve completions this gives 28 new-cell
derivative instances.  Each has the literal witness labels

```text
word                111111,
operation           cap_avoiding_escape_physical_derivative,
fine                the selected cap-avoiding perfect matching,
cap-window status   avoid:34,
new decorated cell  uv;11.                                (11)
```

Every instance raises the cap-block rank from zero to one.  Hence the escape
is not in the span of the cut/cap derivatives.

## 4. The exact support-deleting move

Since the complete derivatives in (7) are zero and the tensor is jointly
linear in the three entries of the physical block `A34`, set

\[
             q_{34}^{00}=q_{34}^{11}=q_{34}^{22}=0.        \tag{12}

The checker verifies for each of the twelve augmented packets that (12)
changes none of the 729 output coefficients.  This deletes three occupied
cells while retaining the normalized escape.

There is a stronger direct reduction.  Delete every cell except the three
colour-one cells of the selected escape matching.  The remaining source is a
single matching occurrence of weight one, so its complete tensor is still
exactly (10).  The reduction deletes six cells in each two-new-cell case and
seven in each three-new-cell case.

This is an exact coefficient-support reduction, not an `N -> N-2` descent and
not a full ternary source.  It says that, inside this local channel, the
seven-cell cap sector is support-redundant once the forced escape arrives.

## 5. Why all-seven tangent span is not the cut span

For completeness, compute derivatives with respect to all seven old cells in
the augmented packet.

* If the escape shares one old residual cell, differentiating that shared
  product already exposes `e_111111`.  The old derivative rank is two and a
  new escape derivative raises it by zero.  This occurs for eight matchings,
  giving sixteen dependent new-cell derivative instances.
* If the escape is disjoint, the seven old derivatives span only

  \[
             e_{111001}+e_{111111}+e_{111221}.             \tag{13}
  \]

  Their rank is one; the escape raises it to two.  The covector

  \[
             \delta_{111111}-\delta_{111001}               \tag{14}
  \]

  kills (13) and evaluates to one on the escape.  This occurs for four
  matchings, giving twelve independent new-cell derivative instances.

The full histograms are therefore

```text
old seven-cell derivative rank       1:4, 2:8,
new derivative rank increase         0:16, 1:12.            (15)
```

This does not weaken (1).  Minimality's affine kernel move requires the
varied variables to occur jointly linearly.  The three entries of one cap
block have that property.  A shared old residual cell and a new escape cell
occur in the same matching monomial, so their tangent dependence does not
give an exact straight-line coefficient deformation.  The support reduction
in section 4 is instead verified by direct equality of complete tensors.

## 6. Structural consequence

For the sharp seven-cell cap sector, the forced outside channel is not a
redundant copy of the killed cap transfer.  It is the unique surviving
physical direction after the mixed equation.  Thus a support-minimal exact
source containing this local pattern cannot retain the isolated cap sector
exactly as displayed: either

1. it deletes that sector by (12),
2. additional cap-containing occurrences change the complete derivatives
   in (6), or
3. the escape attaches to a larger boundary component and must be followed
   as a genuinely new state.

Alternative 2 is the precise place where the present finite theorem stops.
In a larger source, new complement matchings using `34` can make `D_c`
nonzero even after the original two-term `H` cancels.  The next recurrence
measure should therefore count the rank of the **complete cap derivative
module**, not the number of local support cells or the nonzero pure escape
coefficient.

## Scope

This theorem is exact for the diagonal seven-cell cap packet, all twelve
minimal colour-one cap-avoiding completions, every derivative of every old
and new cell, and all `3^6` physical output words.  It is not a complete
ternary GHZ source: (10) is one pure target channel.  It does not prove that
arbitrary larger completions retain the zero cap derivatives, contract two
sites, or produce an active clean cap.

Run:

```text
python3 computations/verify_uniform_c6_seven_cell_escape_physical_derivative_rank.py --mode structural
python3 -O computations/verify_uniform_c6_seven_cell_escape_physical_derivative_rank.py --mode full
python3 -I -S computations/verify_uniform_c6_seven_cell_escape_physical_derivative_rank.py --mode exhaustive
```

Frozen ledger SHA-256:

```text
acedfcdbce4e9c44a5a9e8d71954733f95b4229b7e8731baa583d2a249b1f610
```
