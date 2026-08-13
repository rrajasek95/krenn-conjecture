# Endpoint squares are flat; the first triangle carries residual-edge isotropy

## Exact path census

Start from the marked occurrence

```text
f=(p=0,s=1;23|45),   word 110000.
```

Each of its eight endpoint moves is represented physically by the site
transposition followed by the two-site colour-Weyl correction which restores
the word.  The length-two endpoint-path census is

```text
64 paths, 45 destinations
32 destinations with one path
12 destinations with two paths
 1 marked destination with eight backtracks.
```

For every destination, all paths induce the same operator on the full
`3^6` target-word module—not merely on the GHZ tensor.  Thus every two-step
diamond and backtrack is flat.

Checker:
[`verify_h3_endpoint_correspondence_square_triangle_holonomy_gate.py`](../computations/verify_h3_endpoint_correspondence_square_triangle_holonomy_gate.py).

## The first literal square

Move the `p` endpoint `0->2` and the `s` endpoint `1->3`.  Both orders land
at

```text
(p=2,s=3;01|45).
```

The two paths are

```text
(0,2),(1,3)   and   (1,3),(0,2).
```

Their site/Weyl operators commute on every target word, so the square has
zero full-operator commutator and zero target curvature.  This remains true
after projecting or correcting the common `C2+` target-normal line.

Consequently the rank-two private data observed after the `B-2` stage are
not a square-curvature class.  They are the independent Leibniz faces
`d(v_stage)H_endpoint` already isolated by the sequential factor theorem.

## The first nontrivial holonomy occurs at length three

There are `512` length-three paths and `88` destinations.  Every collection
of paths to a common destination still has one image of the GHZ tensor.
However, `43` destinations have more than one full target operator:

```text
45 destinations : one operator class
27 destinations : two operator classes
16 destinations : three operator classes.
```

The first marked triangles make the structure transparent.  The path

```text
(0,2),(2,3),(3,0)
```

returns to `f`, but its composite operator is the residual site
transposition `(2 3)`.  Likewise

```text
(0,4),(4,5),(5,0)
```

returns to `f` with composite `(4 5)`.  Both flips fix `110000` and every
monochromatic target word, hence fix the GHZ tensor.  They are nevertheless
nontrivial on mixed target/proper-face words:

```text
(2 3): X_001000 -> X_000100,
(4 5): X_000001 -> X_000010.
```

Thus the primitive holonomy faces are

\[
 X_{000100}-X_{001000},
 \qquad X_{000010}-X_{000001}.                       \tag{1}
\]

No rescaling of the common target cone sees (1), because the target-normal
curvature is zero.  The effect is stabilizer isotropy on the mixed
principal-parts fibre.

## Flat groupoid versus trivial local system

The endpoint correspondence does admit a flat **action-groupoid nerve**:
retain the residual-edge flips as isotropy arrows, and the triangles compose
to those arrows.  It does not admit the proposed trivial occurrence local
system in which every closed endpoint path is declared identity.

The distinction is physically load-bearing.  The flips `(2 3)` and `(4 5)`
are target-safe site permutations, but a bar based at an individual marked
occurrence requires an occurrence-local source section.  Applying a flip to
the complete response row gives an invariant aggregate, whose bar has zero
matching-centered projection.  Therefore the old complete-row group bars
do not fill (1).

After granting one physical `B-4/AugP2` occurrence-local section, the
shortest coherent extension is to require it to be equivariant over the
full endpoint action groupoid, including:

- the residual-edge isotropy bars;
- their triangle 2-simplices;
- the independent `B-2`, `B+2`, and matching PP faces.

The same `C2+` target cone handles all endpoint target projections with
ratios `1,-32/7,108/7`.  The new three-step datum is target-dark isotropy,
not a second target cone or central Eq incidence.

## Scope

This is an exact `h=3` endpoint-path census and full `3^6` target-operator
audit through length three.  It does not construct the occurrence-local
physical isotropy bars, the triangle source 2-cells, or the complete cubic
endpoint/matching totalization.

## Verification

```text
python3 computations/verify_h3_endpoint_correspondence_square_triangle_holonomy_gate.py
python3 -O computations/verify_h3_endpoint_correspondence_square_triangle_holonomy_gate.py
python3 -I -S computations/verify_h3_endpoint_correspondence_square_triangle_holonomy_gate.py
```

Frozen ledger SHA-256:

```text
f54d250fe9caafe9db445cc6e252341d786e3bddee3e500428b50da460041725
```
