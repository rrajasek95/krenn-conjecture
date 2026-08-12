# Order six supplies the complete residual source shadow

## Outcome

The primitive face missed by every linear-coefficient order-five operator is
not an all-order obstruction.  In the first quadratic-coefficient order-six
layer, the correctly graded operators containing

```text
07:11 wedge 24:11
```

already contain an exact rational chain whose literal source boundary is
zero and whose complete codimension-two shadow is precisely the required
sixteen-coordinate `-delta` tensor.

Thus the lower source problem is solved one order later than expected.  The
remaining local theorem is no longer to invent the residue lift.  It is to
place this explicit order-six source-shadow chain in the physical repeated
relative grade and glue its still-zero eta/sigma character to the prescribed
terminal packet.

Checker:
`computations/verify_h3_residual_q_order6_missing_face_probe.py`.

## The bounded order-six module

Start with the same three pair generators

```text
A0^2, A0*A1, A1^2
```

used by the order-five repair.  Consider operators

\[
                         xy\,\partial_T,\qquad |T|=6,
\]

where `xy` is a physical two-edge matching on the four sites doubled by the
six derivative directions.  The coefficient colours are forced by one of
the four commutator fine shifts.  Restrict first to operators for which `T`
contains the primitive missing face `07:11 wedge 24:11`.

The exact inventory is

```text
sixth-derivative keys:             242,808
eligible missing-face operators:    8,580
literal source output rows:             305
source rank:                            295
source-kernel lower bound:            8,285.
```

For every operator retain all fifteen two-direction Hasse faces.  The
source-plus-shadow rank is `783`.  Adjoining the exact `-delta` target leaves
rank `783`, and rational elimination gives a solution with

```text
188 nonzero operators,
denominators 1,2,3,
zero literal source outputs,
exactly the 16 nonzero -delta shadow coordinates.
```

The frozen solution digest is

```text
85b642ad725e7fc9cea5e33f7abe078606b37794fa3af2c677481532525242dc.
```

This is stronger than merely killing the singleton separator.  A two-term
source cycle already does that, but its other faces move the obstruction to
another quotient direction.  The 188-term combination cancels all of those
extra faces and reconstructs the whole target tensor exactly.

## What it changes

The previous order-five conclusion remains correct in its scope: no
linear-coefficient fifth-order chain supplies the primitive face.  The new
result shows exactly how the proof escapes that obstruction—use a quadratic
coefficient and one additional derivative order.

This also supplies a clean pattern for the proposed relative Spencer cell:

1. order four gives the covariance-curvature principal symbol;
2. order five cancels its literal pair-generator defect;
3. order six supplies the missing full codimension-two residue shadow; and
4. the physical relative comparison must totalize these pieces with the eta
   primitive and sigma correction.

The order-six solution still uses no colour-zero coefficient cell and no
marked `p/x` colour-two coefficient cell.  Its natural eta and sigma
characters therefore remain zero, just like the order-five repair.  The
terminal fiber-product gluing has not disappeared; it is now the only local
datum not constructed on the source-shadow side.

## Scope guard

This is an exact statement in the bounded `R`-linear pair-generator module.
It does not yet prove that the 188-term operator combination is a physical
cell in the labelled repeated `P3+K2` relative complex.  It also does not
audit every higher proper Spencer face, physical `W`, target, anchor
incidence, or the eta/sigma terminal equations.  In particular it is not yet
the global Fredholm map or the active-rank overlap.

Run:

```text
python3 computations/verify_h3_residual_q_order6_missing_face_probe.py
python3 -O computations/verify_h3_residual_q_order6_missing_face_probe.py
python3 -I -S computations/verify_h3_residual_q_order6_missing_face_probe.py
```

Frozen ledger SHA-256:

```text
78fabcce9541b559b3778cf06f70f207c802dbf615cd19262afc50866cb92bad
```
