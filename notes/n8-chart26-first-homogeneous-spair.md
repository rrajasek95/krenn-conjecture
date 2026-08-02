# The first homogeneous chart-26 Buchberger cell

## Exact outcome

After support normalization, homogenize every mixed coefficient to degree
four with a new variable (t), ordered after all 240 normalized variables.
The 6,558 original leading monomials are distinct squarefree monomials of
degree four, but the original generators are **not** a Groebner basis.

The lexicographically first overlapping pair has word codes (1,2),

\[
 (00000001),\qquad (00000002),
\]

and leading monomials `0948c6f4` and `0948c6f5`.  Their LCM has degree five.
The resulting homogeneous S-polynomial is already reduced by every original
leading monomial.  It has exactly 180 terms,

\[
 120\text{ of }y\text{-degree }5,
 \quad48\text{ of }y\text{-degree }4,
 \quad12\text{ of }y\text{-degree }3,
\]

with 90 coefficients (+1) and 90 coefficients (-1).  The missing degree
is the exponent of (t).  Its new leading monomial is

\[
                         \mathtt{0948cfebf5},
\]

which is squarefree and has (t)-exponent zero.

The chart-support stabilizer gives four source identities.  Exact reduction
of the whole orbit by the original 6,558 generators has remainder sizes

\[
                         180,0,180,0.
\]

The two nonzero reduced cells have distinct squarefree, (t)-free leading
monomials `0948cfebf5` and `0948d0eaf9`.  Thus the first Groebner extension
still has squarefree minimal leading terms, although this does not yet prove
that the completed initial ideal is squarefree.

## Combinatorial form

This cell is the universal Laplace star-minor transport relation described
in `hafnian-star-minor-buchberger-identity.md`.  In the present pair, the
two words differ only at vertex (7), while their leading matchings share
the three edges on the other six vertices.  Cross-multiplying the two last
star entries cancels the common leading product.  Laplace expansion leaves
six cofactor directions, each carrying the corresponding (2\times2) star
minor; this is the structural explanation of the census

\[
                              180=6\cdot15\cdot2.
\]

The same-star critical pairs are governed by the usual Pluecker/Eagon--
Northcott syzygies.  The genuinely new compatibility problem is therefore
between cells based at different vertices or different deleted-word data.

## Verification

Run

```text
python3 computations/verify_n8_chart26_first_homogeneous_spair.py
```

The checker reconstructs all normalized generators, verifies the distinct
degree-four leading monomials, forms the source-labelled S-polynomial,
performs exact homogeneous division, expands the full stabilizer orbit, and
freezes the complete 180-term remainder by SHA-256.

This is a first Groebner cell, not a completed Groebner basis and not yet a
membership or radical-membership result for the pure target.
