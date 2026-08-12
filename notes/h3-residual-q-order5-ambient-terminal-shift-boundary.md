# The ambient direct edge adds syzygies, not the full residual cell

## Outcome

The order-five source repair was first constructed using the forty decorated
cells occurring in its two complete generators.  Allowing every one of the
`28*9=252` ambient decorated physical cells produces exactly one additional
coefficient in either required commutator fine shift:

```text
36:11
```

Here `36` is the direct-free pair omitted from both complete rows.  It
supports `180` eligible fifth-order operators.  Their literal source image
has rank only `28`, so they contain a `152`-dimensional exact kernel.

This is a genuine new source syzygy block, but it does not construct the
desired physical residual-`q` comparison.  Total direct activation and the
pure-minus-mixed shift both vanish on the kernel.  Every eligible term still
uses only colours `1,2`, and none uses a marked `p/x` colour-`2` cell, so the
natural eta and sigma characters remain zero.

Checker:
`computations/verify_h3_residual_q_order5_ambient_terminal_shift_boundary.py`.

## The exact two-term kernel class

The proved codimension-two `-delta` shadow defines a scalar functional on
the direct-edge operator block.  It does not factor through the rank-28
source image: adjoining it raises rank to `29`.  Exact elimination produces
the integral two-term source cycle

\[
\begin{aligned}
 36{:}11\,\partial_{02{:}11,16{:}11,34{:}11,35{:}11,67{:}11}
 -36{:}11\,\partial_{02{:}11,13{:}11,37{:}11,46{:}11,56{:}11}.
                                                               \tag{1}
\end{aligned}
\]

It has literal source boundary zero on all three pair generators and scalar
pairing one with the selected codimension-two shadow.  Its frozen solution
digest is

```text
314c8fca1206b7196d6ffa12c415b77d7aecc0d4d3e4c5eecd200c844b970326.
```

Equation (1) is useful evidence that the omitted direct edge is the correct
overlap location.  It is nevertheless an operator syzygy, not a net direct
activation: the two coefficients are `+1,-1`, and the total direct-edge
augmentation vanishes on the entire kernel.

## Why scalar detection is not construction

The full codimension-two shadow has sixteen signed coordinates.  Augmenting
the direct-edge source columns by every two-cell lower face gives rank `135`.
Adjoining the exact sixteen-coordinate `-delta` vector raises rank to `136`.
Therefore

\[
 -\delta\notin\operatorname{im}
   (\text{direct-edge order-five source+shadow map}).          \tag{2}
\]

Exact quotient reduction also gives a small dual witness to (2).  In the
chosen deterministic pivot order it has support on fourteen literal source
outputs and twelve lower-face coordinates, pairs to one with `-delta`, and
annihilates all 180 direct-edge columns.  The source part consists of ten
pure `A_0^2` matching outputs and four `A_0A_1` outputs, all retaining the
new `36:11` edge.  Thus the rank jump is not a numerical artefact: it has an
exact rational separator inside this bounded block.

This separator is deliberately not promoted to a physical terminal
functional.  It uses output-row coordinates as well as the lower shadow,
depends on the bounded direct-edge presentation, and has not been extended
across the complete relative source map.  Its role is to identify the
missing relative attachment, not to invoke the global Fredholm alternative.

The two-term class (1) is merely detected by the scalar pairing with
`-delta`; its whole lower-face tensor is not `-delta`.  This distinction is
the same source-versus-terminal distinction seen in the physical mapping
cone: a nonzero pairing can define homology or an obstruction without being
the required chain boundary.

## Consequence for the attack

Enlarging the ordinary polynomial order-five ansatz is now exhausted in the
fixed commutator grade:

* `180,360` unique ambient terms were audited;
* exactly `16,488` have one of the two allowed fine shifts;
* the only new coefficient is `36:11`;
* its source kernel has dimension `152` but no eta/sigma character; and
* its complete lower-face image misses the exact residual target by one
  rank.

Thus the already constructed 248-term source homotopy cannot acquire its
terminal packet by simply admitting more ordinary coefficient cells.  The
next object must be a genuinely shifted relative/Spencer or overlap cell,
with the physical module shift carrying the eta and sigma faces.  The
direct-edge syzygy (1) is the closest polynomial shadow of that object and a
useful guide for its boundary, not the object itself.

## Scope and verification

This is exhaustive for linear-coefficient fifth-order differential
operators on the two pair generators.  It does not enumerate new relative
module generators or disprove their existence.

Run:

```text
python3 computations/verify_h3_residual_q_order5_ambient_terminal_shift_boundary.py
python3 -O computations/verify_h3_residual_q_order5_ambient_terminal_shift_boundary.py
python3 -I -S computations/verify_h3_residual_q_order5_ambient_terminal_shift_boundary.py
```

Frozen ledger SHA-256:

```text
631b248ef3ef5cd0d2eee73ae982cb867d16d04a9623d8f177e4634d183116de
```
