# The rootless bar and E14 first-hit obstruction share one decorated 2K2 core

The exact all-derivation companion left by the one-face rootless bar is

\[
 q_{1,23\mid45}=a_{23}^{21}a_{45}^{12}.
\]

It is not merely graph-isomorphic to one of the nine E14 unary S-pair
orbits.  Apply the site relabelling

\[
 2\mapsto0,\quad3\mapsto5,\quad4\mapsto3,\quad5\mapsto4
\]

and interchange colours (0\leftrightarrow2), fixing colour (1).  Then

\[
 a_{23}^{21}a_{45}^{12}longmapsto
 u_{05}^{01}v_{34}^{10}.                              \tag{1}
\]

The restrictions of the source words agree on these four sites: the rootless
word `01211222` restricts to `2112`, while the canonical E14 unary word
`000101` restricts, after (1), to `0110`.

## Canonical row test

For chart `(1,1)`, factor the canonical unary row at the pivot
`u35_11`:

\[
 U=u_{35}^{11}(-1+v_{04}^{00})+B.
\]

The complete literal remainder contains, with coefficient (+1),

\[
                         u_{05}^{01}v_{34}^{10}.       \tag{2}
\]

After the private multiplier and endpoint label are restored, (2) is the
first-hit companion coordinate

\[
 (p_{1,0}^{1}s_{1,1}^{1}v_{24}^{11})
 u_{05}^{01}v_{34}^{10}.                              \tag{3}
\]

Thus the rootless companion is exactly the mixed decorated core required by
one canonical representative of the `000101` E14 orbit.  Conditional on a
source-labelled promotion from the ordinary-residue bar module to the E14
endpoint module, multiplication by the displayed parenthesis cancels (3)
with unit coefficient.  This is the common attachment theorem supported by
the two exact packets.

## Why this does not yet supply the attachment

The equality is at the decorated-core level, not at the full physical-cell
level.  The marked rootless cube has squarefree site profile

```text
(1,1,1,1,1,1,1,1),
```

whereas the five factors of (3) have profile

```text
(2,1,1,1,2,1,1,1).
```

No vertex or colour relabelling identifies those full cells.  More
importantly, the rootless term is an ordinary-residue companion of the
physical source word `01211222`; (3) belongs to the unary/G11 endpoint
S-pair based at `000101`.  Polynomial multiplication supplies the extra
factors but does not change that source-row label.

The convergence therefore sharpens the common missing datum: one physical
grade/word-changing comparison must transport the rootless (2K_2) core into
the endpoint response module.  Another bar shuffle or another internal E14
support face does not provide this transport.

Verified by
[`verify_h3_rootless_e14_companion_core_identification.py`](../computations/verify_h3_rootless_e14_companion_core_identification.py).
