# One off-axis cell cannot repair the affine support-28 orbit

## Result

Let the diagonal part of an eight-site source have the unique affine
support-28 occurrence pattern

\[
 q^c_{uv}\ne0\quad\Longleftrightarrow\quad u_c\ne v_c.
\]

Thus all 28 physical edges are live and the three colour graphs are the
coordinate cuts of the affine cube; there are 48 nonzero diagonal cells.
Adjoin one genuine ordered off-diagonal cell

\[
                         z=A_{uv}[a,b],\qquad a\ne b.       \tag{1}
\]

Then, in either normalized target chart (`12` or `012`), the mixed source
ideal is still the unit ideal after localizing the 48 diagonal cells.  This
holds for every physical edge and every ordered colour pair: 168 one-cell
extensions in each chart.  Consequently an exact source with (1) cannot
remain on the affine diagonal torus.  It must drop at least one diagonal
cell and enter a strictly smaller diagonal-support chart.

The exact checker is
`computations/verify_n8_support28_one_offdiagonal_cell_permanent_triangle_gate.py`.

## Why the off-axis cell is invisible to the certificate

A monomial made only of diagonal cells can occur only at a word whose three
colour multiplicities are even.  If a matching monomial uses the single
off-diagonal cell (1), remove its endpoints.  The remaining three colour
classes must be matched diagonally, so their sizes are even.  Therefore the
original word has odd multiplicity in colours `a` and `b` and even
multiplicity in the third colour.  In parity notation, a one-cell monomial
has signature

\[
                             e_a+e_b\ne0.                  \tag{2}
\]

Every row in every permanent-triangle certificate has even colour
multiplicities.  Hence (1) occurs in none of those rows.  Not merely one but
all 96 permanent triangles are unchanged by every one-cell addition.

Choose any one of them.  Its three literal mixed rows still have the form

\[
 u(ae+bd),\qquad v(af+cd),\qquad w(bf+ce),                 \tag{3}
\]

with all displayed factors among the 48 localized diagonal cells.  The
unchanged identity

\[
 cvwF_1+buwF_2-auvF_3=2bcduvw                            \tag{4}
\]

has a unit right side over the intended characteristic-zero field.  Thus
the added cell cannot repair the already contradictory diagonal fibre.

## Endpoint-polarized cap interpretation

The endpoint-polarized marked comparison supplies all nine matrix
coordinates at the common physical cap pair `67`.  In particular the six
off-diagonal entries in (1) at `67` are genuine source-labelled endpoint
coordinates: they have the same parent/fine carrier and the proven
deletion/reinsertion naturality.  The present theorem is therefore not an
operation-tag or missing-word objection to those coordinates.

It says something earlier and sharper.  Turning on only one of those six
coordinates does not alter any even-parity mixed row in the affine
support-28 certificate, so the physical source equations are already
inconsistent before cap activity or the cubic cleanliness error is tested.
The endpoint-polarized evaluation remains the correct cap map, but it is not
needed to manufacture an active clean cap on this one-cell branch: the
branch exits by a literal source unit.

## Sharp scope and next atom

This is exactly a one-cell theorem.  With two off-diagonal cells, their
parity signatures can cancel.  For an even-parity row this first happens
only when the two cells have the same unordered colour pair; to occur in one
matching they must also lie on disjoint physical edges.  Thus the smallest
off-axis packet not covered here is

\[
 A_{uv}[a,b],A_{rs}[a,b]
 \quad\text{or}\quad
 A_{uv}[a,b],A_{rs}[b,a],
 \qquad \{u,v\}\cap\{r,s\}=\varnothing.                  \tag{5}
\]

Those two-cell Euler packets are the exact next bridge from the affine
diagonal closure to the unrestricted bicoloured source.  No single
off-diagonal generator can be that bridge.

## Reproduction

```text
python3 computations/verify_n8_support28_one_offdiagonal_cell_permanent_triangle_gate.py --mode structural
python3 -O computations/verify_n8_support28_one_offdiagonal_cell_permanent_triangle_gate.py --mode full
python3 -I -S computations/verify_n8_support28_one_offdiagonal_cell_permanent_triangle_gate.py --mode exhaustive
```

The checker reconstructs both affine cube-cut supports, pins the independent
permanent-triangle audit and the rank-nine endpoint-polarized evaluation,
checks all 336 one-cell extensions, and replays an explicit polynomial unit
for every extension.
