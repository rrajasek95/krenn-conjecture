# Hyperbolic collision residuals are one uniform standard module

## Theorem

Fix a collision sector with one missing augmented vertex and one doubled
vertex.  Let the remaining `m` vertices be the possible two neighbours of
the doubled vertex.  For a coordinate-linear transvection from the missing
vertex to the doubled vertex, with coefficient `c_u` in direction `u`, the
collision whose two doubled-vertex neighbours are `u,v` has coefficient

\[
                              c_u+c_v.                \tag{1}
\]

The residual matching on the other `m-2` vertices does not enter (1).  Thus
the complete coefficient map is the signless vertex-edge incidence map of
`K_m`, repeated once for every perfect-matching tail.

Over characteristic zero this map has rank `m`.  Its constant vertex line
is the symmetric collision row, and the augmentation-zero vertex space maps
injectively to an `(m-1)`-dimensional centered standard module.  The
incomplete hyperbolic root is exactly the standard vector

\[
                         J(e_0-e_1).                  \tag{2}
\]

Consequently no further coordinate-linear endpoint transvection can make
the complete response tangent, even modulo the symmetric collision row,
while retaining the prescribed local root coefficients `+1,-1`.

Exact checker:
[`verify_uniform_hyperbolic_collision_standard_representation_gate.py`](../computations/verify_uniform_hyperbolic_collision_standard_representation_gate.py).

## Exact counts

There are

\[
 {m\choose2}(m-3)!!
\]

collision monomials in the sector.  In (2), the positive coordinates are
the pairs containing vertex `0` but not vertex `1`, and the negative
coordinates are the pairs containing `1` but not `0`.  Hence each sign
occurs

\[
                         (m-2)(m-3)!!                 \tag{3}
\]

times.  The squared norm is twice (3), so the primitive rational dual is

\[
 {J(e_0-e_1)\over 2(m-2)(m-3)!!}.                   \tag{4}
\]

For the eight-vertex, `h=3` response, `m=6`.  The sector has `45`
coordinates and (2) has exactly twelve `+1`, twelve `-1`, and twenty-one
zero entries.  Formula (4) is the previously isolated residual divided by
`24`.

## Proof of the rank statement

Suppose `J(c)=0`.  For all distinct `u,v`, equation (1) gives
`c_u=-c_v`.  Choosing three distinct vertices gives
`c_u=-c_v=c_w=-c_u`, hence `2c_u=0`; characteristic zero gives `c=0`.
Thus `J` is injective.

Moreover `J(1,...,1)=2*1_edges`, so the constant vertex line maps onto the
symmetric collision line.  If `sum c_u=0`, summing (1) over all neighbour
pairs and all tails gives zero.  Therefore the augmentation-zero vertex
space maps into the centered collision hyperplane and has dimension
`m-1`.  This proves the decomposition.

If `J(c)` is merely constant, then

\[
 J(c)=\lambda 1=J((\lambda/2)1).
\]

Injectivity forces `c=(lambda/2)1`.  Such a vector cannot have simultaneously
`c_0=1` and `c_1=-1`.  This proves the tangent-completion no-go.

## Consequence for the proof

The signed 24-term face is not an accidental finite-order residue.  At
every order it is the standard summand complementary to the symmetric
collision row.  Enlarging the same ordinary site/root transvection cannot
remove it: all such enlargements remain in the incidence map (1), and a
response-preserving vector there is constant.

The shortest positive object must therefore be genuinely
occurrence-dependent.  Equivalent descriptions are:

1. a source-labelled collision splitter retaining the two matching parents;
2. a higher Tate/PP cell carrying the standard collision module; or
3. a complete augmented comparison whose first boundary is (2).

The theorem is uniform and tail-independent, but it does not yet promote
the dual (4) to an accepted terminal.  That still requires propagation
through every principal-parts, word/fine, Eq, `q`, anchor, residue, `W`, and
ridge column.

## Verification

Run

```text
python3 computations/verify_uniform_hyperbolic_collision_standard_representation_gate.py
python3 -O computations/verify_uniform_hyperbolic_collision_standard_representation_gate.py
python3 -I -S computations/verify_uniform_hyperbolic_collision_standard_representation_gate.py
```

The checker verifies the exact incidence ranks and decompositions for
`m=4,6,8,10,12`, recovers the frozen `h=3` histogram and denominator, and
checks inconsistency of the prescribed-root tangent system.
