# Why the interpolation counterexample does not directly clone to matchings

Let

\[
 S=\{(i,j,4-i-j):0\leq i,j\leq2\}
\tag{1}
\]

be the nine-term support of the exact counterexample in
`tight-free-lagrange-counterexample.md`.  There are two distinct obstacles
to turning (1) into a perfect-matching incidence support by simply cloning
its symbols at edge endpoints.

## 1. Perfect-matching fibers occur in identical endpoint pairs

For a support `P=PM(G)` and an incident edge occurrence `e=uv`, define its
local fiber

\[
 F_{v,e}=\{M\in P:e_v(M)=e\}.
\tag{2}
\]

Endpoint consistency gives the exact identity

\[
                         F_{v,e}=F_{u,e}.
\tag{3}
\]

Thus every nonempty local-symbol fiber of a perfect-matching support occurs
verbatim at a second mode.

No fiber of (1) repeats.  The first-coordinate fibers are the three rows of
the `3 x 3` grid, the second-coordinate fibers are its three columns, and
the third-coordinate fibers are its five antidiagonals, of sizes
`1,2,3,2,1`.  The size-three antidiagonal is not a row or column, and all
the other cases are immediate.  Therefore (1) itself cannot be isomorphic
to a perfect-matching incidence support.

## 2. Literal duplication forces Cartesian completion

The smallest way to repair (3) is to duplicate all three modes and use

\[
 S^{\mathrm{dup}}
 =\{(i,i,j,j,k,k):(i,j,k)\in S\}.
\tag{4}
\]

Suppose (4) were the full perfect-matching support of a graph on these six
modes.  Every fiber in (4) occurs at exactly two modes.  By (3), the partner
endpoint of the edge representing either copy must carry a fiber identical
to it; the unique other copy is therefore that partner endpoint.  Thus the
two occurrences of `i` are the two endpoints of one edge, and similarly for
`j` and `k`.  Hence the graph
contains three bundles of parallel edge occurrences, one on each of three
fixed disjoint vertex pairs.  But any choice of one occurrence from each
bundle is then a perfect matching.  The full support must contain the
Cartesian completion

\[
 \{(i,i,j,j,k,k):i\in\{0,1,2\},\ j\in\{0,1,2\},
                         \ k\in\{0,1,2,3,4\}\},
\tag{5}
\]

with 45 terms, rather than only the nine terms satisfying `i+j+k=4`.
This is a support-level contradiction independent of coefficients.

Parallel sources do remove a different, purely local obstruction.  If an
interpolation column is `a_i in K^3`, then the desired two-site diagonal
column

\[
 \operatorname{diag}(a_i)=\sum_r (a_i)_r e_r\otimes e_r
\tag{6}
\]

can be implemented by three parallel edge occurrences.  Thus one should
not claim that endpoint rank-one factorization alone forbids dense columns.
What (5) shows is that independent parallel bundles lose the global
correlation `k=4-i-j`; their matching tensor factors across the three pair
blocks and has flattening rank one between those blocks.

Any genuine simulation must therefore add connector edges/vertices that
enforce the sum relation.  Alternating-cycle switching then creates hybrid
perfect matchings, so those hybrids must be canceled rather than omitted.
The first degree-four connector candidate, the octahedral graph on six
vertices, is ruled out exactly in
`notes/octahedral-incidence-obstruction.md` by a rank-four flattening.
