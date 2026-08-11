# The direct genus-2 Pfaffian probe stops at a grade/Arf obstruction

## Exact 16-Pfaffian expansion

A literal rotation system for `K8` has eighteen faces: sixteen triangles and
two quadrilaterals.  Its Euler characteristic is `8-28+18=-2`, so it is a
cellular orientable genus-two embedding.  The checker constructs:

- a Kasteleyn orientation with odd disagreement on every face;
- the `11`-dimensional cocycle space and the `7`-dimensional vertex
  coboundary space;
- four quotient cocycles representing `H^1(Sigma_2,F2)`; and
- the induced quadratic refinement of matching signs.

All sixteen homology classes occur among the 105 perfect matchings.  The
quadratic refinement has nondegenerate polar form of rank four and Gauss sum
`-4`.  Fourier inversion therefore gives sixteen Arf coefficients, each
`+1/4` or `-1/4`.  Matching by matching, their signed Pfaffian sum has
coefficient `+1`; hence for arbitrary edge variables

\[
             \operatorname{haf}(K_8)
       =\sum_{\eta\in H^1(\Sigma_2;\mathbf F_2)}
             c_\eta\operatorname{Pf}(K^\eta),
       \qquad c_\eta\in\{\pm\tfrac14\}.
\]

This is also checked on a dense integral edge assignment.

## Literal two-chart/full-nine packet

The probe uses three actual decorated eight-site word coefficients:

```text
00000000                 first diagonal anchor,
11111111                 second diagonal anchor,
01222222                 crossed row.
```

For each word, split its 105 physical matchings on chart edges `01` and
`02`.  In every case the direct part has fifteen terms and the response
part ninety, and their sum is the original hafnian coefficient.  Thus all
six tested expressions are literal direct-plus-response full-nine rows of
one physical source, not anonymous Pfaffian generators.  Their decorated
site/colour multidegrees are distinct.

## Grassmann--Pluecker grade obstruction

A principal-Pfaffian quadratic has an even base set `S` and four additional
vertices.  Every term has physical-site degree

\[
                    2\mathbf 1_S+\mathbf 1_{\{i,j,k,l\}}.
\]

For `K8` the complete census is

```text
|S|=0:  70
|S|=2: 420
|S|=4:  70.
```

Only the seventy empty-base identities are squarefree.  The checker verifies
all `70*16=1,120` of them exactly; they are simply the defining four-site
Pfaffian expansions.  Multiplying one by a two-edge matching on the four-site
complement gives 210 squarefree lifts per decorated word, but each remains a
tautological expansion inside that single word.  It does not couple either
diagonal anchor to the crossed row and supplies no new residual functional.

Every nonempty-base relation already has doubled physical sites.  A
nonnegative polynomial multiplier cannot return it to the squarefree
eight-site coefficient grade.

## Buchsbaum--Eisenbud and Arf obstructions

For every odd principal set `T` and row vertex `i in T`, the standard
Buchsbaum--Eisenbud kernel row has degree two at `i`, degree one on
`T\{i}`, and degree zero outside `T`.  Exhausting sizes three, five, and
seven gives respectively

```text
168, 280, 56
```

rows, and none is squarefree.  These syzygies therefore cannot be literal
relations in the original eight-site coefficient grade without a new
division, contraction, or attaching operation.

There is an independent sector-descent failure.  Twelve physical edges have
trivial spin label in the chosen gauge and sixteen have nontrivial label,
realizing nine distinct nontrivial characters.  Multiplying a constituent
Pfaffian by such an edge twists the Arf coefficient vector by that character.
The twisted vector is never proportional to the original Arf vector.  Hence
a sectorwise Pfaffian syzygy with a nontrivial twist is not a combination of
the original hafnian rows; it requires sector-resolved equations which the
full-nine packet does not provide.

## Verdict and scope

The bounded proposal from §1.3 is mathematically sound as a 16-Pfaffian
coordinate change, but the standard Grassmann--Pluecker and
Buchsbaum--Eisenbud syzygies do not produce the missing Component-III
source-provenant annihilator on this literal packet.  They also do not reach
the weaker scalar-zero, pure-diagonal single-edge cap landing from
`a67ec1d`.  At squarefree source grade they reproduce only the wordwise
Laplace/matching identities already available in hafnian coordinates.

This is an exact counterguard to the **direct** Pfaffian-syzygy route, not an
all-order no-go for every derived Pfaffian construction.  A viable
continuation would need a source-valid cross-word/cross-sector attaching map
which removes the doubled-site grade and descends the nontrivial Arf
characters.  Constructing that map is essentially the missing provenance
problem, rather than a free consequence of Pfaffian ideal theory.

## Reproduction

```sh
.venv/bin/python computations/verify_n8_genus2_arf_fullnine_syzygy_probe.py
.venv/bin/python -O computations/verify_n8_genus2_arf_fullnine_syzygy_probe.py
```
