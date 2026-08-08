# Two-cell character-orbit feasibility at the anchored N=8 four-cut gate

## Outcome

The arbitrary-weight one-cell elimination does **not** extend to a finite
two-cell orbit list.  The diagonal torus reduces most two-cell additions to
one exact representative, but 1,873 of the 27,730 unordered pairs retain
genuine continuous coefficient moduli.

The finite stratum can nevertheless be closed exactly.  All 25,857 pairs
whose two quotient characters are independent are simultaneously normalized
to weights \((1,1)\).  Exact source reconstruction finds that all retain the
three pure anchors, 89 retain the three complete active cuts \(z=2,3,4\), and
none of those 89 acquires a complete active cut in \(z=0,1,5\).

Thus there is no arbitrary-nonzero-weight two-cell four-cut repair in the
zero-dimensional character-orbit stratum.  This is not a theorem for the
remaining positive-dimensional strata.

## Exact character census

Let \(L\subset\mathbb Q^{24}\) be the span of the sixteen characters in the
anchored support and the three characters imposing stabilization of the
three pure target terms.  Exact sparse row reduction gives

\[
                              \dim L=15.
\]

For an absent endpoint-colour coordinate \(x\), let
\(\bar\chi_x\in\mathbb Q^{24}/L\) be its quotient character.  Among the 236
absent coordinates, six have zero quotient character and 230 have nonzero
quotient character.  The nonzero characters occupy 73 projective lines:

| coordinates on a projective line | number of lines |
|---:|---:|
| 1 | 10 |
| 2 | 46 |
| 6 | 2 |
| 7 | 8 |
| 8 | 6 |
| 12 | 1 |

For two distinct absent coordinates \(x,y\), the rank of
\(\{\bar\chi_x,\bar\chi_y\}\) gives the dimension of their torus orbit inside
\((\mathbb C^\*)^2\).  The exact pair census is

| quotient rank | pair type | pairs | coefficient-quotient dimension |
|---:|---|---:|---:|
| 2 | two independent nonzero lines | 25,857 | 0 |
| 1 | one zero and one nonzero character | 1,380 | 1 |
| 1 | two characters on the same nonzero line | 478 | 1 |
| 0 | two zero characters | 15 | 2 |
| | **total** | **27,730** | |

The checker verifies every pair rank in two independent exact ways: by
projective normal forms modulo \(L\), and by directly adjoining both
characters to a rational row basis.

Pairs using the same coordinate twice are not omitted source families: their
two weights aggregate into one coordinate and are already covered by the
arbitrary-weight one-cell theorem.  Likewise, the boundary of
\((\mathbb C^\*)^2\), where one added weight is zero, is covered by that
theorem.

## Why only rank two is a finite search

For quotient rank two, the stabilizing torus maps onto a two-dimensional
subtorus of the two coefficient coordinates.  Over \(\mathbb C\), both
nonzero weights can therefore be normalized simultaneously to one.  Testing
one representative per coordinate pair is exhaustive, not a coefficient
sample.

For quotient rank one, a character relation leaves one invariant monomial in
the two weights.  In the zero-plus-nonzero case, the coefficient of the
zero-character cell itself is invariant.  Rank-zero pairs retain both
coefficients.  These are one- and two-dimensional algebraic families,
respectively.  A finite symmetry of the anchored source may identify some
families, but cannot turn a positive-dimensional coefficient quotient into a
finite set.

Consequently, testing weights such as \(\{-1,0,1\}\), or enlarging such a
grid, would not be a mathematically exhaustive next step.

## Exact finite-stratum search

For each of the 25,857 rank-two pairs, the checker:

1. adds both unit representatives to the literal finite decorated source;
2. rebuilds the full eight-site perfect-matching tensor;
3. checks the three pure coefficients;
4. reconstructs both crossing sectors and all labelled five-site cofactor
   spaces on cuts \(2,3,4\); and
5. for the 89 surviving triples, checks the complete source-faithful packet
   on cuts \(0,1,5\).

The exact census is

\[
\begin{array}{c|r}
\text{rank-two representatives} & 25{,}857\\
\text{retain }(1,1,1) & 25{,}857\\
\text{also retain complete cuts }2,3,4 & 89\\
\text{also acquire a fourth complete cut} & 0.
\end{array}
\]

Because the test retains lower-sector and cofactor provenance, its empty
result is a finite-realizability statement on this stratum, not an
output-only obstruction that would also apply to the border construction.

## Stopping decision

Local finite enumeration should stop here.  The unresolved set is not large
because the integer grid was too small; it is large because 1,873 coordinate
pairs parameterize positive-dimensional algebraic quotients.  More sampled
weights cannot close them.

A further rigorous attack needs a structural four-cylinder identity, or an
equivalent symbolic certificate, which treats the surviving parameters
uniformly.  A bounded version would express the four cut-membership
conditions as polynomial identities in the one or two invariant parameters
and derive either a common contradiction or a finite list of exceptional
parameter values.  Without such a reduction, pair-by-pair coefficient
enumeration has reached its stopping rule.

## Reproduction

    python3 computations/verify_n8_four_cut_two_cell_orbit_feasibility.py
    python3 -O computations/verify_n8_four_cut_two_cell_orbit_feasibility.py
    python3 -I computations/verify_n8_four_cut_two_cell_orbit_feasibility.py
    python3 -S computations/verify_n8_four_cut_two_cell_orbit_feasibility.py

The checker uses only the Python standard library and exact rational sparse
row reduction.  It uses raising checks throughout, so optimized mode does not
weaken the audit.
