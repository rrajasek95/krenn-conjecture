# Independent audit: the adjacent \(E_{22}\) fourth-cut obstruction

## 1. Verdict and exact scope

The local result in
[the primary \(E_{22}\) note](three-cut-internal-23-arbitrary-block-adjacent-25-22-fourth-cut-obstruction.md)
passes a clean-room exact reconstruction.  Keep the seven internal cells

\[
\begin{array}{c|c@{\qquad}c|c@{\qquad}c|c}
01&E_{00}&45&E_{00}&02&E_{11}\\
14&E_{11}&04&E_{22}&13&E_{22}\\
35&E_{10},
\end{array}
\]

let \(A_{23}=X\) be an arbitrary complex \(3\times3\) matrix, and put

\[
                         A_{25}=E_{00}+tE_{22}.             \tag{1}
\]

Even with both boundary stars and \(A_{67}\) arbitrary, the complete
cylinder identities for cuts \(2,3,4\) cannot coexist with the identity for
cut \(0\), \(1\), or \(5\), while the diagonal target fibres remain units.
No flaw or exceptional complex counterexample was found.

The independent checker is
[verify_three_cut_internal_23_arbitrary_block_adjacent_25_22_fourth_cut_obstruction_independent_audit.py](../computations/verify_three_cut_internal_23_arbitrary_block_adjacent_25_22_fourth_cut_obstruction_independent_audit.py).
It imports no project module and reads no primary matrix, projection, normal,
chart program, or certificate.  The result is deliberately local: it does
not make \(A_{25}\) arbitrary, free another fixed block, or prove Krenn's
conjecture.

## 2. Independent endpoint-ordered reconstruction

Perfect matchings are generated recursively by pairing the greatest
remaining vertex, and every edge is stored with its smaller endpoint first.
Thus \(35:E_{10}\), every \(23:x_{ab}\), and \(25:E_{22}\) retain their
literal endpoint order.  For each cut, the audit regenerates all \(45\) raw
full-cylinder columns in the reversed order

\[
   \text{hole decreasing},\qquad
   \text{hole colour decreasing},\qquad
   \text{cut colour decreasing}.
\]

Numerical subspace intersections use greatest-coordinate sparse
Gauss--Jordan elimination and the exact identity

\[
                         (U\cap V)^\perp=U^\perp+V^\perp. \tag{2}
\]

This is independent of the primary echelon route.  Symbolic rank matrices
also reverse the comparison-cut, row, and raw-column orders and discard the
earlier, rather than the later, member of each of the three literal duplicate
pairs in \(C_2\).

With distinct rational values assigned to all nine entries of \(X\), a
non-binary \(t\), all \(108\) entries of the two boundary stars, and all nine
entries of \(A_{67}\), direct eight-site matching enumeration agrees in all
nine boundary-colour fibres with

\[
\begin{aligned}
H_{ab}&=r_{ab}H_S(X,t)+\beta_{X,t}(p^a,q^b),\\
\beta_{X,t}(p,q)
 &=\sum_{i<j}\sum_{c,d}
   \left(p_{i,c}q_{j,d}+p_{j,d}q_{i,c}\right)
   e_c^{(i)}e_d^{(j)}\otimes H_{S\setminus\{i,j\}}(X,t).
                                                               \tag{3}
\end{aligned}
\]

Equation (3) also follows directly by separating an eight-site perfect
matching according to whether it uses \(67\) or uses two boundary-star
edges.  Hence the rational replay is an endpoint-order audit of a polynomial
identity, not a finite sampling assumption.  It checks both ordered
off-diagonal fibres, reuse of the same star entries among fibres, all three
diagonal target fibres, and arbitrary \(A_{67}\).

## 3. \(t\)-normalization and the exact \(512\)-support cover

The eight fixed-cell characters have rank \(8\) in the \(18\) internal
site-colour exponents, leaving a ten-dimensional stabilizer.  The nine
\(X\)-characters have rank \(5\).  For every one of the \(512\) supports of
\(X\), adjoining the \(25:E_{22}\) character raises the supported-character
rank by exactly one.  Thus \(t\ne0\) can be normalized independently of the
remaining \(X\)-orbit data.

The action extends across the boundary by taking \(g_{6,c}=1\) and

\[
             g_{7,c}=\left(\prod_{i=0}^{5}g_{i,c}\right)^{-1}. \tag{4}
\]

Every pure target is fixed exactly, while entries of the arbitrary boundary
stars are merely rescaled.  Full row rank of the relevant integer character
matrix gives the required surjection of complex tori; roots cause no problem
over \(\mathbb C\).

For \(x_{00}\ne0\), normalize \(x_{00}=t=1\) and retain the other eight
entries as unrestricted variables.  This covers \(256\) supports.  On
\(x_{00}=0\), take the first nonzero entry in

\[
                         x_{02},x_{10},x_{12},x_{20},x_{22}. \tag{5}
\]

Normalize that entry and \(t\) to one, set only its predecessors in (5) to
zero, and leave all other entries symbolic.  These five charts cover

\[
                         128+64+32+16+8=248               \tag{6}
\]

supports, including every special complex value of every later coefficient.
The remaining support lies in \(\{x_{01},x_{11},x_{21}\}\).  Its supported
characters together with the \(t\)-character are independent for each of the
eight subsets, so every nonzero coefficient can be normalized to one.  The
complete count is therefore

\[
                         256+128+64+32+16+8+8=512.         \tag{7}
\]

The checker additionally verifies coefficientwise that there is no \(x_{ab}t\)
term in the six-site tensor, every deleted-pair cofactor, or any of the \(270\)
raw cylinder columns.  A separate dense rational \(X\) replay at \(t=0,1,2\)
verifies affine interpolation.  This is forced combinatorially because edges
\(23\) and \(25\) share endpoint \(2\).

When \(t=0\), (1) is literally the fixed-\(A_{25}=E_{00}\) family already
checked in
[the independent arbitrary-\(A_{23}\) audit](three-cut-internal-23-arbitrary-block-fourth-cut-obstruction-independent-audit.md).
No limiting argument is used.

## 4. Uniform full-cylinder line certificates

For each chart and final cut, the audit forms the simultaneous-representation
matrix for \(C_2,C_3,C_4,C_z\).  After independently removing the three
literal duplicates in \(C_2\), it has \(177\) columns.  The following
constant minors have rank \(176\):

\[
\begin{array}{c|c|c|c|c}
\text{chart}&z&\text{matrix}&\text{minor nonzeros}&\det\\ \hline
x_{00}&0&453\times177&272& 1\\
x_{00}&1&436\times177&293& 1\\
x_{00}&5&514\times177&277&-1\\
x_{02}&0&433\times177&280&-1\\
x_{02}&1&416\times177&292&-1\\
x_{10}&0&416\times177&263&-1\\
x_{10}&1&401\times177&284&-1\\
x_{12}&0&391\times177&268& 1\\
x_{12}&1&379\times177&283& 1\\
x_{20}&0&369\times177&258& 1\\
x_{20}&1&362\times177&273&-1\\
x_{22}&0&350\times177&257&-1\\
x_{22}&1&343\times177&267&-1
\end{array}                                                \tag{8}
\]

Each determinant is the literal constant shown while every unnormalized
chart parameter remains an indeterminate.  The kernel of the relation matrix
has dimension at most one.  Direct expansion along the cut reconstructs the
same nonzero \(H_S\) from every raw cylinder, supplying a nonzero kernel
relation.  Therefore the actual common full-cylinder intersection is exactly
\(\langle H_S\rangle\).  This argument neither projects the cylinders nor
assumes a generic parameter value.

The independent rank ledger, including the cut-\(5\) certificate below, is

    57277268d226e1b7b6b0469f2bacdda63700ed693d7c439d618ac2cf6543b84b

Every selected-label hash differs from the primary ledger, and the displayed
sparsities also visibly differ in the first two \(x_{00}\) cases, as expected
from the independent ordering.

## 5. Uniform cut \(5\), including all rank jumps

Leave all nine entries of \(X\) symbolic, set \(t=1\), and define

\[
 e_{ab}=[00ab00],\qquad
 T=[121200]+[111110]+[220220]+[222222].                    \tag{9}
\]

Fresh enumeration gives

\[
                         H_S(X)=T+\sum_{a,b}x_{ab}e_{ab}. \tag{10}
\]

Each \(e_{ab}\) is a literal raw column of both \(C_2\) and \(C_3\), while
direct cut expansion puts \(H_S\) in both cylinders; hence \(T\) also lies in
both.  The ten displayed vectors are independent.  The reversed
\(108\times87\) relation matrix for \(C_2,C_3\) has a constant
\(77\times77\) minor with \(88\) nonzeros and determinant \(-1\).  Its
relation kernel has dimension at most ten, so

\[
             C_2\cap C_3
             =W:=\operatorname{span}\{e_{00},\ldots,e_{22},T\}. \tag{11}
\]

Restrict to the ten coordinates \(e_{00},\ldots,e_{22},[121200]\).  This
restriction is injective on \(W\).  Among the independently ordered \(45\)
raw \(C_5\) columns, only zero-based column \(8\), labeled
\((\text{hole},\text{hole colour},\text{cut colour})=(4,0,0)\), has a
nonzero restriction, namely

\[
                         (x_{00},\ldots,x_{22},1).         \tag{12}
\]

Thus the restriction of any vector in \(W\cap C_5\) is a multiple of (12),
and injectivity on \(W\) makes the vector itself a multiple of \(H_S\).
Conversely direct expansion puts \(H_S\) in \(C_5\).  Hence, as a polynomial
identity valid at every special complex cancellation and rank jump,

\[
                         C_2\cap C_3\cap C_5=\langle H_S\rangle. \tag{13}
\]

Adding \(C_4\) preserves this line.  This proves the cut-\(5\) claim uniformly
for all \(X\), including the exceptional supports.

## 6. The eight exceptional true normals

On the coordinate locus supported in \(\{x_{01},x_{11},x_{21}\}\), the audit
constructs the unprojected common cylinder intersection separately for every
support and every final cut.  Greatest-coordinate double-annihilator
elimination gives

\[
\begin{array}{c|ccc}
\text{support}&\dim N_0&\dim N_1&\dim N_5\\ \hline
\varnothing&1&1&1\\
\text{each of the other seven supports}&2&2&1.
\end{array}                                                \tag{14}
\]

For every support, \(N_0=N_1\) exactly, \(H_S\in N_z\), and the two retained
pure targets \([0^6]\) and \([1^6]\) lie outside \(N_z\).  Moreover
\(N_5=\langle H_S\rangle\), in agreement with (13).  The plane normals in
(14), rather than a sampled line or a quotient normal, are used in the
exceptional star ideals.

The independently reconstructed ambient-coordinate and generator counts are

\[
\begin{array}{c|r|r|r}
\text{support}&\text{coordinates}&N_0=N_1\text{ generators}&N_5\text{ generators}\\ \hline
\varnothing&134&412&412\\
x_{01}&160&488&492\\
x_{11}&155&476&480\\
x_{01}x_{11}&181&496&500\\
x_{21}&151&476&480\\
x_{01}x_{21}&177&500&504\\
x_{11}x_{21}&172&504&508\\
x_{01}x_{11}x_{21}&198&508&512
\end{array}                                                \tag{15}
\]

## 7. Shared-star ideals and independent exact certificates

The six open-chart programs retain all symbolic later coefficients, the
same \(72\) entries of the two stars, two diagonal fibres, and both ordered
off-diagonal fibres.  The direct \(A_{67}\) term is a multiple of \(H_S\), so
it is absorbed by every normal.  Any solution of the full three-colour,
nine-fibre system restricts to this four-fibre packet; a unit packet ideal is
therefore a valid contradiction.

The independent Singular programs reverse star, fibre, word, and generator
orders.  Their sizes and hashes are

\[
\begin{array}{c|r|r|r|l}
\text{chart}&\text{variables}&\text{coordinates}&\text{generators}
&\text{program SHA-256}\\ \hline
x_{00}&84&341&1320&\texttt{4a545d066b00339f7177b5325053c4cd4c091d4b31cb7625739e65dbf1ec48d2}\\
x_{02}&83&315&1216&\texttt{3f12cfd67d236c02b5194bea9fa1d9d1b7f8fe3f55b9e9e4b0d01bff788fcb91}\\
x_{10}&82&294&1124&\texttt{730d3c12308c5f0df0e43f2ec752e67a674716354e4e5224b9306c101acd3105}\\
x_{12}&81&266&1000&\texttt{7ef842f2a863fc210fe2f21cf663dc20cd96a812e00ea37d2c40e6a381b03cf8}\\
x_{20}&80&243&912&\texttt{403a3831bb4f8c62a5a75fa17f40db383e46ee9bd23561d4d293b64034e95831}\\
x_{22}&79&218&780&\texttt{56d2e75861227c3c11124c901fb4733d286968ab64fbfd6e1a95b39782902b7f}
\end{array}                                                \tag{16}
\]

All six reduce to \([1]\) over characteristic zero.  On the exceptional
locus, annihilators of the actual line or plane impose membership directly,
without auxiliary normal scalars.  Generator counts range from \(412\) to
\(512\).  The \(24\) support/cut jobs yield \(15\) distinct programs: cuts
\(0,1\) agree on each support, while cut \(5\) uses (13).  Every program also
reduces to \([1]\).

In total, the audit checks \(30\) chart/cut jobs and \(21\) distinct exact
programs.  Its frozen ideal ledger is

    57bca13bbcf440d4b1a3425e0fe52988aa037a9a08ed1138eeb734454d646d36

The primary ideal ledger is different because its variable and generator
orders are different.  A unit ideal over \(\mathbb Q\) remains unit after
extension of scalars to \(\mathbb C\).

## 8. Reproduction and conclusion

From the repository root, run

    .venv/bin/python -m py_compile computations/verify_three_cut_internal_23_arbitrary_block_adjacent_25_22_fourth_cut_obstruction_independent_audit.py
    .venv/bin/python computations/verify_three_cut_internal_23_arbitrary_block_adjacent_25_22_fourth_cut_obstruction_independent_audit.py --workers 8

The clean replay on 2026-07-27 ended with

    independent adjacent-E22 full-cylinder audit: PASS
    t=0 inherited literally; t!=0 normalized without an X modulus: PASS
    512 supports covered exactly as 256+128+64+32+16+8+8: PASS
    13 constant rank-176 minors and all-X cut-5 rank-77/probe: PASS
    eight true exceptional normals for cuts 0,1,5: PASS
    all nine literal boundary fibres, shared stars, arbitrary A67: PASS
    30 chart/cut jobs and 21 exact characteristic-zero units: PASS
    rank ledger SHA256: 57277268d226e1b7b6b0469f2bacdda63700ed693d7c439d618ac2cf6543b84b
    ideal ledger SHA256: 57bca13bbcf440d4b1a3425e0fe52988aa037a9a08ed1138eeb734454d646d36
    maximum Singular time: 9.382s
    parallel Singular wall time: 9.383s
    independent total wall time: 43.012s

The previously misleading coarse quotients play no role in this audit.
Every successful normal is a full, unprojected cylinder intersection; every
later chart coefficient remains symbolic; the exceptional planes are used
at their true dimension; and the cut-\(5\) identity is uniform through all
complex cancellations.  Subject to the narrow scope in Section 1, the
primary \(E_{22}\) closure candidate is therefore independently certified.
