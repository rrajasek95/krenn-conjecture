# The bridge orbit leaves one aggregate comparison class

## Result

The canonical symbolic order-six covariance--Spencer grade bridge lands on the
repeated-component edge `(3,5)` in the cyclic face order

```text
1 -> 3 -> 5 -> 2 -> 4 -> 1.
```

Transport by this residual-site cycle produces all five adjacent edges.  In
the face basis `(1,3,5,2,4)`, their boundaries are

\[
 e_3-e_1,\quad e_5-e_3,\quad e_2-e_5,\quad
 e_4-e_2,\quad e_1-e_4.                              \tag{1}
\]

The integral span of (1) is the saturated sum-zero lattice of rank four.
Its cokernel is the primitive aggregate

\[
                         \varepsilon=e_1+e_3+e_5+e_2+e_4. \tag{2}
\]

One face vertex completes the rank to five.  Thus the five physical
endpoint gluings should not be attacked independently: the orbit of one
covariance--Spencer comparison handles every edge, and the only remaining
comparison datum is one normalized `H0`/aggregate class.

Checker:
`computations/verify_h3_order6_covariance_bridge_cyclic_aggregate.py`.

## Explicit orbit

The canonical degree shift is

\[
 q_{13}^{00}q_{45}^{00}\partial_{07:11}
\]

with local `0<->1` transports at sites `0,2,6,7`.  Under the five cyclic
powers, the arm `07:11` remains fixed, the two-edge internal tail rotates,
and the one moving internal colour-transport site follows

```text
2 -> 4 -> 1 -> 3 -> 5 -> 2.
```

This gives five labelled versions of the same bridge theorem rather than
five new constructions.

## Meaning for the proof

The local comparison now has the cellular shape

```text
five face vertices
   -- five covariance-Spencer edges (rank 4) -->
one aggregate H0 class.
```

The edge part specifies where the order-six principal-parts direction and
repeated `P3+K2` grading must meet.  For the endpoint-recoloured physical
class these edges are required comparison-cell incidences, not literal
matching-edge derivatives; see
`h3-endpoint-recoloured-primitive-face-grade.md`.  The aggregate part is the
normalized `H0` which neither a covariance cube nor the `C5` collision
incidence can kill by itself.  This identifies the last local comparison
theorem more sharply:

> Construct one physically typed aggregate vertex, or show that its class
> survives in the exhaustive augmented cone.  In the first case all five
> comparisons propagate along (1).  In the second, the physical terminal
> must either detect the class and normalize it to the relative generator,
> or descend to the Fredholm separator.

This is the same generator-or-annihilator alternative already needed in the
rootless proof, but now with a canonical one-dimensional source rather than
five unrelated endpoint choices.

## Scope

The theorem is exact for the cyclic symbolic grading and incidence orbit of
the pinned unrecoloured bridge.  It does not yet construct the physical augmented edge
chains, the aggregate vertex, or the terminal/anchor readout.  In
particular, rank four in (1) is not by itself a physical comparison theorem.

Run:

```text
python3 computations/verify_h3_order6_covariance_bridge_cyclic_aggregate.py
python3 -O computations/verify_h3_order6_covariance_bridge_cyclic_aggregate.py
python3 -I -S computations/verify_h3_order6_covariance_bridge_cyclic_aggregate.py
```

Frozen ledger SHA-256:

```text
7f46d103e1f06a6573a56631de15114b80dfdb8fb51b9b42d334e9cf274b74fc
```
