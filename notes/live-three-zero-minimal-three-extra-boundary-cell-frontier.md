# The minimal three-extra boundary has nine exact cell orbits

## 1. Outcome

The central \(01^3\) response is uniformly injective by
[live-three-zero-minimal-three-extra-response-frontier.md](live-three-zero-minimal-three-extra-response-frontier.md).
This note makes the complement of that affine chart disjoint and exact.
For one extra row plane write

\[
 C=\{p_{01}\ne0\},\qquad
 B=\{p_{01}=0,\ p_{12}\ne0\},\qquad
 E=\{(p_{01}:p_{02}:p_{12})=(0:1:0)\}.                         \tag{1}
\]

The 26 noncentral products split into nine site-permutation orbits.
Exact direct-free maximal-minor ideals close all nine of them:

\[
 EEE,\quad BEE,\quad CEE,\quad BBE,\quad CBE,\quad BBB,
 \quad CBB,\quad CCE,\quad CCB.                                \tag{2}
\]

This is all 26 individual noncentral cells.  Together with the central
\(CCC\) certificate, it is a disjoint exact cover of all 27 products.

## 2. Why these are the exact boundary cells

For a two-row matrix \(R\), order its Plücker coordinates as
\((p_{01},p_{02},p_{12})\).  The three row-reduced forms used by the
response generator have coordinates

\[
\begin{array}{c|c|c}
\text{chart}&\text{rows}&(p_{01},p_{02},p_{12})\\ \hline
01&(1,0,a),(0,1,b)&(1,b,-a)\\
12&(a,1,0),(b,0,1)&(-b,a,1)\\
02&(1,a,0),(0,b,1)&(b,1,a).
                                                               \tag{4}
\end{array}
\]

Thus \(C\) is exactly chart \(01\).  On its complement, chart \(12\)
with \(b=0\) gives the affine line \(B\); its one missing point is chart
\(02\) at \(a=b=0\), namely \(E\).  Consequently every ordered triple
of row planes lies in one and only one word in \(\{C,B,E\}^3\).
There is no overlap bookkeeping left.

The complete census is

\[
\begin{array}{c|c|c|c}
\text{orbit}&\text{cell dimension}&\text{number of cells}&\text{status}\\ \hline
CCC&6&1&\text{closed}\\
CCB&5&3&\text{closed}\\
CCE&4&3&\text{closed}\\
CBB&4&3&\text{closed}\\
CBE&3&6&\text{closed}\\
BBB&3&1&\text{closed}\\
CEE&2&3&\text{closed}\\
BBE&2&3&\text{closed}\\
BEE&1&3&\text{closed}\\
EEE&0&1&\text{closed}.
                                                               \tag{5}
\end{array}
\]

## 3. Exact low-cell unit-minor certificates

On every closed cell, maximal rows are selected only from source pairs
\(00,02,11,12,22\), never \(01\).  Hence all determinants are
independent of the arbitrary direct \(B_{01}\) scale.

For the six low-dimensional orbits other than CBB, the checker:

1. specializes the structural zero parameters defining its \(B\) and
   \(E\) letters;
2. computes the determinant by fraction-free FLINT elimination;
3. replaces it by its squarefree support, which has the same zero set;
   and
4. verifies that the exact Gröbner basis of all supports over
   \(\mathbb Q\) contains \(1\).

The number of selection points per cell is

\[
\begin{array}{c|rrrrrr}
\text{orbit}&EEE&BEE&CEE&BBE&CBE&BBB\\ \hline
\text{selection points}&1&2&4&5&27&17.
                                                               \tag{6}
\end{array}
\]

All but one are rational points.  The final \(BBB\) row set is selected
at \((a,c,e)=(86,51,65)\) modulo \(101\).  This modular value is used
only to choose a row set; its determinant and the final unit ideal are
then reconstructed exactly over \(\mathbb Q[a,c,e]\).

Therefore the complete response has rank 19 everywhere on those 17 cells,
for every value of their free parameters and every direct scale.  The
additional three CBB cells use the localized six-branch certificate linked
below.

## 4. Exact audit

[verify_live_three_zero_minimal_three_extra_boundary_low_cells.py](../computations/verify_live_three_zero_minimal_three_extra_boundary_low_cells.py)
reconstructs all selected rows deterministically, checks every exact
restricted determinant, and verifies the unit ideals for every permutation
of the six low-dimensional orbit types listed above.

The common response and chart generator is
[explore_live_three_zero_minimal_three_extra_response.py](../computations/explore_live_three_zero_minimal_three_extra_response.py).
The CBB branch cover is audited separately in
[live-three-zero-minimal-three-extra-cbb-certificate.md](live-three-zero-minimal-three-extra-cbb-certificate.md).
The CCE unit ideals are audited in
[live-three-zero-minimal-three-extra-cce-certificate.md](live-three-zero-minimal-three-extra-cce-certificate.md).
The final CCB orbit is audited in
[live-three-zero-minimal-three-extra-ccb-certificate.md](live-three-zero-minimal-three-extra-ccb-certificate.md).
Thus the census (5) now contains 27 closed cells and no open cell.
