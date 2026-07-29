# Four more adjacent one-cell lines still cannot activate a fourth cut

## 1. Exact statement and scope

Keep the seven internal cells

\[
\begin{array}{c|c@{\qquad}c|c@{\qquad}c|c}
01&E_{00}&45&E_{00}&02&E_{11}\\
14&E_{11}&04&E_{22}&13&E_{22}\\
35&E_{10},
\end{array}
\]

let \(A_{23}=X\in\operatorname{Mat}_{3\times3}(\mathbb C)\) be arbitrary,
and take

\[
 A_{25}=E_{00}+tE_{cd},\qquad
 (c,d)\in\{(0,1),(0,2),(1,2),(2,1)\},\quad t\in\mathbb C.       \tag{1}
\]

Allow all \(108\) entries of the boundary stars \(i6,i7\), \(0\leq i<6\),
and all nine entries of \(A_{67}\) to be arbitrary complex numbers.  For
each of the four directions in (1), no such system satisfies the complete
quotient identities on cuts \(2,3,4\) together with cut \(0\), \(1\), or
\(5\), while retaining the three unit diagonal target fibres.

The exact checker is
[verify_three_cut_internal_23_arbitrary_block_adjacent_25_four_offdiagonal_lines_fourth_cut_obstruction.py](../computations/verify_three_cut_internal_23_arbitrary_block_adjacent_25_four_offdiagonal_lines_fourth_cut_obstruction.py).
The geometry reconnaissance for all eight possible non-base cells is
[explore_three_cut_internal_23_adjacent_25_all_directions.py](../computations/explore_three_cut_internal_23_adjacent_25_all_directions.py).

This is a local fixed-interior theorem.  It does not make \(A_{25}\)
arbitrary, does not cover the three remaining directions \(10,20,22\), and
does not prove the global Krenn conjecture.

## 2. Torus and support exhaustion

The eight fixed cells, including the base \(E_{00}\) in \(A_{25}\), impose
eight independent equations on the \(18\) internal site-colour scalars.
Their stabilizer therefore has dimension \(10\).  Its effective character
rank on the nine entries of \(X\) is five.  For every direction in (1), the
moving-cell character is independent and raises the rank to six.

The checker verifies the stronger supportwise statement: for every one of
the \(512\) supports of \(X\), adjoining the nonzero \(t\)-character raises
the rank by exactly one.  Thus every \(t\ne0\) is normalized to one without
using an \(X\)-modulus.  The honest \(X\)-modulus census remains

\[
                    328, 132, 42, 9, 1                 \tag{2}
\]

for \(0,1,2,3,4\) moduli.  The coordinate quotients below remove all but
the unique rectangle cross-ratio.  When \(t=0\), the independently audited
arbitrary-\(A_{23}\) theorem applies literally, so (1) exhausts the whole
affine parameter line rather than only its torus.

Every internal stabilizer element extends without changing the target:
take \(g_{6,c}=1\) and
\(g_{7,c}=(\prod_{i=0}^{5}g_{i,c})^{-1}\) for each colour \(c\).  This
keeps all three diagonal target coefficients equal to one, while merely
rescaling entries in the arbitrary boundary blocks by nonzero factors.

## 3. Coordinate separation

Because edges \(23\) and \(25\) share site \(2\), no perfect matching uses
both.  Every matching tensor, deleted-pair cofactor, cylinder column, and
boundary atom is separately affine in \(X\) and \(t\), with no
\(x_{ab}t\) term.  The checker verifies this by finite differences on every
even subset of the six internal sites.

For every direction, the moving-cell output block \(T_{cd}\) has \(35\)
coordinates and uses exactly the deleted pairs

\[
                         03,\qquad04,\qquad13,\qquad34.   \tag{3}
\]

It is disjoint from the fixed direct tensor \(U_+\), contains no pure target
word, and overlaps exactly three \(X\)-blocks, in nine coordinates each:

\[
\begin{array}{c|c}
(c,d)&X\text{-blocks meeting }T_{cd}\\ \hline
01,02&R_{00},R_{01},R_{02}\\
12&R_{10},R_{11},R_{12}\\
21&R_{20},R_{21},R_{22}.
\end{array}                                               \tag{4}
\]

Every omitted coefficient is tested twice: its entire projected boundary
term contribution vanishes, and its addition leaves each of the six
projected cylinder spans unchanged.  It is therefore genuinely arbitrary,
not silently specialized to zero.

For an actual common normal \(N_z=C_2\cap C_3\cap C_4\cap C_z\) and a
coordinate quotient \(\pi\), only the safe containment

\[
 \pi N_z\subseteq
 \pi C_2\cap\pi C_3\cap\pi C_4\cap\pi C_z=\overline N_z \tag{5}
\]

is used.  A unit ideal modulo the larger \(\overline N_z\) is a valid
contradiction for the original problem.

## 4. All \(512\) supports and all continuous moduli

The \(32\) supports on the old five-cell locus

\[
                 \{x_{00},x_{01},x_{02},x_{11},x_{21}\}  \tag{6}
\]

are covered by the five audited interval quotients.  The other \(480\)
supports split by first nonzero cell \(x_{10},x_{12},x_{20},x_{22}\) as

\[
                         256+128+64+32.                    \tag{7}
\]

They give \(27\) finite quotient charts.  In every chart the projected
common normals for final cuts \(0,1,5\) agree exactly, contain the projected
direct tensor, and leave the selected two pure targets unabsorbed.  Their
dimensions are

\[
\begin{array}{c|cccc}
\text{direction}&x_{10}&x_{12}&x_{20}&x_{22}\\ \hline
01,02,12&2&1&2&1\\
21&3&1&3&1.
\end{array}                                               \tag{8}
\]

The sole dependent retained support is the rectangle

\[
                 \{x_{11},x_{12},x_{21},x_{22}\},         \tag{9}
\]

normalized by

\[
 x_{12}=x_{11}=x_{22}=t=1,\qquad
 \lambda=x_{21}={x_{12}x_{21}\over x_{11}x_{22}}.         \tag{10}
\]

For all four directions, independently spanning the cylinders at
\(\lambda=0,1\) gives the same two-dimensional safe plane structure

\[
                         \langle e,H_S(0)\rangle,
 \qquad e=[002100].                                       \tag{11}
\]

Moreover \(H_S(\lambda)=H_S(0)+\lambda e\).  For every raw cylinder column
on each possible fourth cut, the constant, linear, and quadratic
coefficients of

\[
             \ell_\lambda=[002100]^*-\lambda[001100]^*    \tag{12}
\]

vanish.  Hence the actual intersection is locked inside the direct-tensor
line for every complex \(\lambda\).  The resulting ideals live in the
ordinary polynomial ring \(\mathbb Q[\lambda,p^1,p^2,q^1,q^2]\), so no
exceptional complex cross-ratio is omitted.

## 5. Exact shared-star ideals

For boundary colours \(a,b\), literal endpoint-ordered matching expansion
is

\[
\begin{aligned}
 H_{ab}={}&r_{ab}H_S(X,t)+\beta_{X,t}(p^a,q^b),\\
 \beta_{X,t}(p,q)={}&
 \sum_{i<j}\sum_{c,d}
 (p_{i,c}q_{j,d}+p_{j,d}q_{i,c})
 e_c^{(i)}e_d^{(j)}\otimes H_{S\setminus\{i,j\}}(X,t).
\end{aligned}                                             \tag{13}
\]

The checker compares (13) with a direct eight-site matching enumeration,
using distinct nonzero rational values for every \(X\)-entry, \(t\), all
\(108\) shared-star entries, and all nine \(A_{67}\)-entries, separately for
each direction.  The nine boundary slices agree exactly.

Each obstruction ideal retains two diagonal fibres and both ordered cross
fibres, using \(72\) of the shared star variables.  Any solution of the full
\(108\)-variable system restricts to this packet.  The arbitrary \(A_{67}\)
term is absorbed because the projected direct tensor belongs to every safe
normal.

There are exactly

\[
 4\bigl(5\text{ old-locus}+27\text{ finite}+1\text{ symbolic}\bigr)
 =132                                                        \tag{14}
\]

exact ideal jobs.  Hash deduplication finds \(102\) distinct raw Singular
program templates: directions \(01\) and \(02\) share \(30\) templates,
while their three remaining old-locus templates differ; every other
pairwise direction intersection is empty.  All \(132\) jobs were replayed
independently, and every reduced characteristic-zero standard basis is
\([1]\).

In the finite tables below, each \(x_{10}\) or \(x_{20}\) row is ordered

\[
(d,b)=(0,0),(0,1),(2,0),(2,1),(4,0),(4,1),(6,0),(6,1),    \tag{15}
\]

the \(x_{12}\) row omits \((6,1)\), and the \(x_{22}\) row uses only the last
four entries.  The exact generator counts are

\[
\begin{array}{c|c|l}
\text{direction}&\text{family}&\text{generator counts}\\ \hline
01,02&x_{10}&360,464,444,548,472,576,556,660\\
&x_{12}&364,468,448,552,476,580,560\\
&x_{20}&388,492,472,576,500,604,584,688\\
&x_{22}&416,520,500,604\\ \hline
12&x_{10}&380,484,432,536,492,596,544,648\\
&x_{12}&384,488,436,540,496,600,548\\
&x_{20}&440,544,492,596,552,656,604,708\\
&x_{22}&496,600,548,652\\ \hline
21&x_{10}&424,492,508,576,504,572,588,656\\
&x_{12}&432,500,516,584,512,580,596\\
&x_{20}&452,520,536,604,532,600,616,684\\
&x_{22}&488,556,572,640.
\end{array}                                               \tag{16}
\]

The five old-locus counts and the symbolic \(\mathbb Q[\lambda]\) count are

\[
\begin{array}{c|c|c}
\text{direction}&\text{five old-locus counts}&\mathbb Q[\lambda]\\ \hline
01,02&284,300,536,516,620&660\\
12&292,376,612,560,664&648\\
21&312,400,600,616,684&660.
\end{array}                                               \tag{17}
\]

The generated-program ledgers have SHA-256 hashes

\[
\begin{array}{c|l}
01&\texttt{d93f7fb5193e21208405229f372ebbc289796947fc5ba448f6f8c6b059c88c67}\\
02&\texttt{3847216772aa78b9570c656dcd2babfa14acb51adfb1575e8e6693221167d0f5}\\
12&\texttt{c05a76ce4d969850335cee96bd7502eeadc3e1933245af3025bce15a8b287b4c}\\
21&\texttt{8eec1a312d973e9b50f8c73572b00bff0db81f216059e440e10930793c5931fd}.
\end{array}                                               \tag{18}
\]

The combined ledger hash is

    e9d1bd6f2fbe5f1f4a106cd8251ec6f3c9a38725000e441080def5c49fab3f75

and is asserted by the checker before Singular is invoked.

## 6. Reproduction

From the repository root, run

    uv run python computations/verify_three_cut_internal_23_arbitrary_block_adjacent_25_four_offdiagonal_lines_fourth_cut_obstruction.py --workers 8

The locked-environment run on 2026-07-27 ended with

    four off-diagonal A25 lines fourth-cut obstruction: PASS
    t=0 inherited arbitrary-A23 theorem; t!=0 normalized: PASS
    4*(5 old + 27 finite + 1 Q[lambda]) unit ideals: PASS
    all supports, arbitrary killed coefficients, and literal fibres: PASS
    direction=01 exact_wall_max=47.052s certificate_hashes=33
    direction=02 exact_wall_max=47.127s certificate_hashes=33
    direction=12 exact_wall_max=48.605s certificate_hashes=33
    direction=21 exact_wall_max=50.536s certificate_hashes=33
    parallel exact-Q wall time: 352.476s
    certificate ledger SHA256: e9d1bd6f2fbe5f1f4a106cd8251ec6f3c9a38725000e441080def5c49fab3f75

## 7. What remains

This closes every off-diagonal direction except \(E_{10}\) and \(E_{20}\),
and combines with the earlier \(E_{11}\) theorem.  Reconnaissance isolates
the remaining three cells sharply:

1. For \(E_{10}\) and \(E_{20}\), the moving character already lies in the
   five-dimensional \(X\)-character span.  Nonzero \(t\) therefore creates
   extra torus invariants, and several old quotient charts no longer have a
   common final-cut normal.
2. For \(E_{22}\), the moving character is independent and the
   \(\mathbb Q[\lambda]\) lock survives, but \(T_{22}\) contains the pure
   target word \([2^6]\).  The present \(x_{10}\), \(x_{20}\), and two
   old-locus quotients leave only one usable target colour and cannot certify
   a contradiction.

These are failures of this elimination template, not countermodels to the
local statement.  No system satisfying a fourth cut was found or claimed
for \(10,20,22\); they remain the exact next frontier.
