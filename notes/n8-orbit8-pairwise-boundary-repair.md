# Multi-term repairs of the orbit-8 pairwise-Hamilton boundary

Let `T8` be `sparse_seed(orbit=8)` and adjoin

```
26;21 26;22 27;21 36;12 37;11 37;12
46;21 47;21 47;22 56;11 56;12 57;12.
```

Call the resulting support `B24`.  Exact enumeration gives 24 cells, pure
fibre sizes `(1,2,2)`, and exactly 22 nonempty mixed fibres, all binomial.
Their Laurent lattice is inconsistent and contains exactly twelve unit
three-row odd circuits.

The search and independent checker are

```
computations/search_n8_orbit8_pairwise_boundary_repair.py
computations/verify_n8_orbit8_pairwise_boundary_repair.py
```

The checker enumerates all 105 perfect matchings and all `3^8` colourings.

## Minimum repair of the twelve seed circuits

For every binomial appearing in a seed triangle, introduce a selector for
each possible third matching and imply all cells missing from `B24`.  Every
triangle requires at least one such selector.  Exact SAT gives UNSAT with
one, two, or three additional cells and SAT with four.  Thus four is the
minimum number of new cells that can break all twelve original triangles.

A particularly symmetric minimum cover is

```
04;11 05;22 12;11 13;22.
```

Its mixed-fibre histogram is `{1:4,2:40,4:6}`.  The four singleton fibres
already rule it out, but its quotient structure is informative: the forty
binomial rows are consistent, and all six four-term remainders have two
quotient classes with coefficients of equal absolute value.

The full lazy completion formula, which also forbids every newly created
singleton, is UNSAT at total-cell caps 28 and 30.  Thus no extension by at
most six cells can simultaneously remove mixed singletons and break the
twelve seed circuits.  These two bounds are exact solver-replay results; no
portable DRUP trace is claimed for them.

## Exact quotient-binomial closure

Suppose a consistent signed Laurent quotient reduces one mixed coefficient
to

\[
 aX^u+bX^v,
 \qquad |a|=|b|\ne0.
\]

Its vanishing is exactly the additional Laurent equation

\[
 X^{u-v}=-b/a.
\]

The right side is `-1` when `a,b` have the same sign and `+1` otherwise.
The search adjoins every such equation, recomputes the signed row-HNF, and
iterates to a fixed point.  This operation is necessary for every torus
solution, so inconsistency, a one-monomial remainder, or a zero reduced pure
product is an exact obstruction.

On the symmetric four-cell cover, the six quotient binomials give only two
distinct new equations after deduplication.  Their joint extension is
consistent, but the reduced product of the three pure fibres is zero.
More sharply, each of the first three four-term fibres has a majority of
`1` entries, and adjoining its quotient binomial alone kills the pure-colour-1
sum; each of the remaining three similarly kills pure colour 2.
Thus even ignoring its four singletons, the balanced chart cannot normalize
all three pure coefficients.

## A different 34-cell no-singleton completion

The first no-singleton support on this boundary with a consistent initial
binomial quotient is `B24` plus

```
03;01 06;01 06;02 07;01 07;02
14;02 16;01 16;02 17;01 17;02.
```

It has mixed histogram `{2:54,4:8}`.  Each of its eight four-term fibres
reduces to a single torus monomial with coefficient `+2` or `-2`, already an
exact obstruction.  There is an even smaller pure-fibre certificate.  The
complete mixed fibre `10112111` is

\[
x_{02}^{11}x_{14}^{02}
\left(x_{36}^{11}x_{57}^{11}+x_{37}^{11}x_{56}^{11}\right)=0.
\]

The complete pure-colour-1 fibre is

\[
x_{02}^{11}x_{14}^{11}
\left(x_{36}^{11}x_{57}^{11}+x_{37}^{11}x_{56}^{11}\right).
\]

All displayed cell weights are nonzero on the support torus.  The mixed
binomial therefore forces the pure coefficient to vanish, contradicting its
required value one.  The quotient computation independently minimizes the
zero-product certificate to precisely this one mixed row and colour 1.

Several further cap-34 completions found so far have the same one-row mechanism
with colour 1 or colour 2.  The dedicated CEGAR retains fibres of arbitrary
size, iterates quotient-binomial closure, and learns exact pure-zero or
one-monomial support cuts.  No exact toric survivor has appeared.  These are
bounded chart obstructions, not a global proof of Krenn's conjecture.
