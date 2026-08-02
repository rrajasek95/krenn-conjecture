# One- and two-cell tangent isolation at the rational rank-53 seed

This is a local first-order statement at one exact binary GHZ8 source. It is
not a global support classification and does not exclude higher-order or
distant components.

Let (A^ast) be the rational rank-53 source from
[binary-ghz8-exact-rank53-source.md](binary-ghz8-exact-rank53-source.md), and
let (C) be its set of 45 nonzero cells. Write (J_C) for the Jacobian of all
256 binary GHZ8 coefficient equations restricted to those cells. Exact
elimination over (mathbb Q) gives

\[
                      \operatorname{rank}J_C=19.
\]

There are 67 cells outside (C). The complete exact census gives

\[
 \operatorname{rank}[J_C\mid J_x]=20
       \quad\text{for every missing cell }x,
\]

and

\[
 \operatorname{rank}[J_C\mid J_x\mid J_y]=21
       \quad\text{for every one of the }\binom{67}{2}=2211
       \text{ missing pairs }\{x,y\}.
\]

The corresponding kernel dimensions are all 26, exactly the kernel dimension
of (J_C). Hence every tangent vector supported on (C) together with at
most two missing cells has zero coordinate on the added cells. No one- or
two-cell support mutation opens at first order at (A^ast).

## Exact quotient calculation

The checker
[verify_binary_ghz8_rank53_two_cell_tangent_isolation.py](../computations/verify_binary_ghz8_rank53_two_cell_tangent_isolation.py)
reconstructs the exact source and builds the full `256 x 112` Jacobian from
six-site matching cofactors, and row-reduces the 45 active columns while
applying the same operations to all missing columns. Below the 19 active pivot
rows, the 67 resulting column tails represent the missing-cell columns modulo
the active image.

The checker proves exactly that:

* none of the 67 quotient columns is zero;
* no two quotient columns are proportional;
* all 2,211 unordered pairs are therefore independent; and
* the 67-column quotient matrix has rank 65, agreeing with full Jacobian rank
  (19+65=84).

It uses only standard-library `Fraction` arithmetic and passes normal,
optimized, and isolated Python.

## Scope warning

This calculation concerns ordinary tangent vectors only. It does not rule out
a curve whose added cells first appear at second or higher order, a component
whose closure does not pass through (A^ast), or a distant exact solution on
one of the enlarged supports. In particular, constrained numerical solves can
reach machine-residual GHZ points after moving away from the seed; that does
not contradict the tangent census. No rank-54 or rank-55 conclusion follows
from this local calculation.
