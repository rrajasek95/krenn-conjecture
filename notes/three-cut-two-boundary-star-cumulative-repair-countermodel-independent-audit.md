# Independent audit: cumulative repair on both boundary stars

## 1. Verdict and scope

The construction in
[the primary note](three-cut-two-boundary-star-cumulative-repair-countermodel.md)
passes an independent endpoint-ordered reconstruction over
\(\mathbb Q\).  Its thirteen-source family has

\[
 H_B=e_1^{\otimes8}+e_2^{\otimes8}+e_{00210021},           \tag{A1}
\]

the complete active cuts are exactly \(z=2,3,4\), and their target
defect dimensions are \((1,1,2)\).  All four previously recorded
suffix-\(12\) debts vanish.  Adding the one cell

\[
                           A_{67}\mathrel{+}=-E_{21}
\]

cancels \(00210021\), creates exactly the three stated suffix-\(21\)
debts, and leaves the same three active complete cuts and defects.

No algebraic or scope error was found.  Neither family is a Krenn
counterexample: the constant-zero coefficient is missing, and each
family retains mixed words.  The result refutes only the sufficiency of
the three-cut condition together with the four named mixed-coordinate
equations.

## 2. Endpoint-ordered matching expansion

For an edge \(u<v\), a cell \(E_{ab}\) places colour \(a\) at site \(u\)
and colour \(b\) at site \(v\).  The aggregate matching tensor is

\[
 H_X(A)=\sum_{M\in\operatorname {PM}(X)}
             \bigotimes_{uv\in M}A_{uv},                    \tag{A2}
\]

with tensor factors restored to increasing named-site order.  Expanding
the blocks in (A2) chooses one decorated cell on each matching edge,
retains endpoint order, and multiplies its weight.  This establishes the
source-level expansion without a symmetry assumption on \(35:E_{10}\)
or \(23:E_{21}\).

For the thirteen cells in the primary note, enumeration of all
\(7\cdot5\cdot3=105\) perfect matchings leaves exactly

\[
\begin{array}{c|c|c}
01,26,37,45&00210021&1\\
02,14,37,56&11111111&1\\
04,13,26,57&22222222&1.
\end{array}                                                \tag{A3}
\]

The internal cell \(23:E_{21}\) occurs in no supported full matching.
Equation (A3) proves (A1), including

\[
 h_{0^8}=0,\qquad h_{1^8}=h_{2^8}=1,
\]

and proves directly that the four old debt coordinates

\[
 00210012,\quad12120012,\quad11111012,\quad22022012
\]

are zero.

## 3. The three complete residual cylinders

Put

\[
 D=H_B-\Delta_{8,3}=e_{00210021}-e_0^{\otimes8}.           \tag{A4}
\]

Independent four-site expansion gives

\[
 H_{0145}=e_{0000},\qquad
 H_{0135}=e_{0010},\qquad
 H_{0125}=e_{0000}.                                       \tag{A5}
\]

Restoring every named slot in (A5) reproduces the primary decompositions

\[
\begin{aligned}
D={}&e_{221}^{(2,6,7)}
 \otimes(e_1^{(3)}\otimes H_{0145})
-e_{000}^{(2,6,7)}
 \otimes(e_0^{(3)}\otimes H_{0145}),\\
D={}&e_{121}^{(3,6,7)}
 \otimes(e_2^{(2)}\otimes H_{0145})
-e_{000}^{(3,6,7)}
 \otimes(e_0^{(2)}\otimes H_{0145}),\\
D={}&e_{021}^{(4,6,7)}
 \otimes(e_2^{(2)}\otimes H_{0135})
-e_{000}^{(4,6,7)}
 \otimes(e_0^{(3)}\otimes H_{0125}).
                                                               \tag{A6}
\end{aligned}
\]

Each internal factor is a literal cofactor insertion, so

\[
                           D\in E_2\cap E_3\cap E_4.        \tag{A7}
\]

The common-residual equivalence established for the earlier three-cut
model then gives the complete high-sector quotient identity on all
three cuts.  The audit also rebuilt every insertion matrix in the
\(3^5\)-word basis.  Its exact constant-word memberships are

\[
\begin{array}{c|c|c}
z&{\cal G}_{U_z}\cap{\cal S}_{U_z}&\dim W_{U_z}\\ \hline
0&0&3\\
1&0&3\\
2&\langle0^{U_2},2^{U_2}\rangle&1\\
3&\langle0^{U_3},1^{U_3}\rangle&1\\
4&\langle0^{U_4}\rangle&2\\
5&\langle1^{U_5},2^{U_5}\rangle&1.
\end{array}                                                \tag{A8}
\]

Dense rational rank comparison of each residual slice against its
insertion matrix gives

\[
\begin{array}{c|cccccc}
z&0&1&2&3&4&5\\ \hline
\text{complete}&\mathrm{no}&\mathrm{no}&\mathrm{yes}&
\mathrm{yes}&\mathrm{yes}&\mathrm{no}.
\end{array}                                                \tag{A9}
\]

For \(z=0,1,5\), the all-zero coordinate functional belongs to
\(K_{U_z}\).  Since \(h_{0^8}=0\), contraction cannot equal the
nonzero colour-zero target.  This independently explains the three
negative entries in (A9); no fourth cut is hidden by a rank convention.

## 4. The one-cell repair

The internal six-site tensor of the nine fixed cells is

\[
 H_S=[002100]+[121200]+[111110]+[220220].                   \tag{A10}
\]

Pairing its four matchings with \(67:-E_{21}\) produces

\[
\begin{array}{c|c}
00210021&-1\\
12120021&-1\\
11111021&-1\\
22022021&-1.
\end{array}                                                \tag{A11}
\]

The first row cancels the mixed term in (A1).  Together with the two
unchanged diagonal matchings, the complete repaired tensor is therefore

\[
 H'_B=e_1^{\otimes8}+e_2^{\otimes8}
      -e_{12120021}-e_{11111021}-e_{22022021}.              \tag{A12}
\]

Equation (A12) kills all four suffix-\(12\) debts and
\(00210021\).  Rebuilding, rather than reusing, every repaired insertion
space gives exactly the cut table (A9) and defects (A8).  This confirms
the existential debt transport claimed in the primary note.

It does not prove that arbitrary mixed equations are repairable, that
debt transport can continue indefinitely, or that a permutation-stable
whole-sector constraint cannot close the route.

## 5. Independent executable audit

[verify_three_cut_two_boundary_star_cumulative_repair_countermodel_independent_audit.py](../computations/verify_three_cut_two_boundary_star_cumulative_repair_countermodel_independent_audit.py)
imports none of the primary checker.  It enumerates the endpoint-ordered
matchings and uses independent dense rational matrices for every
insertion-space membership, cut, and defect computation.
