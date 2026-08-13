# A selected zero two-cycle cannot terminate in the diagonal `2+2` switch

## Result

The diagonal `2+2` family isolated by the equal-partition classification is
a genuine source geometry, but it is not a terminal obstruction for a
**selected active OO two-cycle**.

After spectator factorization, the normalized two-cycle is the core
relation

\[
                              U+V=0.                    \tag{1}
\]

The ninety diagonal spectator decorations split into 72 physical `C4`
switches and 18 same-skeleton colour swaps.  Tensor them with all `486`
ordered four-site core rows `(word,U,V)`.  The exact split is

```text
42,120  U or V contains an off-diagonal core cell,
 1,620  both U and V are entirely diagonal.
```

In the second branch the core word is necessarily monochromatic.  Indeed,
on four sites a non-monochromatic word has at most one diagonal perfect
matching; two distinct matchings `U,V` can both be diagonal only when every
site has the same colour.

The selected curved OO matching class contains its fixed nonzero
off-diagonal direct cell.  In a diagonal spectator rectangle that cell must
therefore occur in `U` or `V`.  Hence every selected instance belongs to the
42,120 off-diagonal branch and enters the bidirectional private-site fan
theorem.  The 1,620 entirely diagonal rectangles cannot contain the selected
class.

Checker:
[`verify_oo_selected_zero_two_cycle_offdiagonal_exit.py`](../computations/verify_oo_selected_zero_two_cycle_offdiagonal_exit.py).

## Interference landing

A nonzero off-diagonal core cell forces the two transposed private-site
identities.  They give active fans with distinct centre heads at the two
ends of the cell.

* An off-anchor fan is already a distinct-head active four-good overlap.
* If both fans are anchor-contained, they enter the bidirectional five-lock
  endpoint holonomy.

The second branch was formerly conditional on constructing a residual-q
Kodaira--Spencer lift.  Physical endpoint-odd Cartan descent now constructs
that lift in the canonical `h=3` repeated grade.  Its terminal-visible
branch is the normalized relative generator; its zero-indeterminate branch
adjoins the endpoint difference and kills the unequal-tail charge.

Thus the diagonal `2+2` family is eliminated from the **selected literal
two-row** frontier.  The beautiful mechanism is exactly interference: a
purely diagonal even switch can survive in isolation, but once it carries
the selected off-diagonal amplitude, conjugate private-site fans attach it
to the Cartan endpoint difference.

## Exact remaining scope

This is not yet the arbitrary-SCC theorem.  In a larger connected critical
module, a diagonal two-cycle can occur away from the selected vertex.  The
missing global statement is now sharply graph-theoretic and source-typed:

> Starting from the selected off-diagonal matching class, every surviving
> zero-holonomy charge is reached by a chain of literal complete-row
> transitions; the first transition that changes the normalized decorated
> core either enters the off-diagonal Cartan/fan route, has odd holonomy, or
> gives a complete-column support deletion.

Once that source-exhaustivity statement is proved, the literal two-cycle
classification above removes its smallest even terminal.  Transverse
physical rank/support landing remains separate: endpoint holonomy closure
does not by itself create an active clean cap.

## Verification

Run

```text
python3 computations/verify_oo_selected_zero_two_cycle_offdiagonal_exit.py
python3 -O computations/verify_oo_selected_zero_two_cycle_offdiagonal_exit.py
python3 -I -S computations/verify_oo_selected_zero_two_cycle_offdiagonal_exit.py
```

Frozen ledger SHA-256:

```text
792bee9611258262b25343eb97b08b4a06feb049f4801f2610c199436c684b33
```
