# Two boundary stars transport all four recorded debts at once

## 1. Result

The cumulative mixed-word strengthening of the repaired three-cut model is
still insufficient.  There is an integral endpoint-decorated family whose
complete active cuts are exactly

\[
                             z=2,3,4,                      \tag{1}
\]

with target-defect dimensions \((1,1,2)\), and for which all four
previously recorded debt coefficients vanish:

\[
\begin{aligned}
 [e_{00210012}]H_B&=0,&[e_{12120012}]H_B&=0,\\
 [e_{11111012}]H_B&=0,&[e_{22022012}]H_B&=0.              \tag{2}
\end{aligned}
\]

Its exact tensor is instead

\[
             H_B=e_1^{\otimes8}+e_2^{\otimes8}
                         +e_{00210021}.                    \tag{3}
\]

Thus simultaneous changes on both boundary stars move the debt to a new
word, rather than merely repairing the three words one at a time.

This is an actual decorated-source realization with shared star cells, not
the formal relaxation in which every bilinear product of a site-\(6\) cell
and a site-\(7\) cell is independent.  It is not a Krenn counterexample:
colour zero occurs on sources, but

\[
 [e_0^{\otimes8}]H_B=0\ne1,                              \tag{4}
\]

and the mixed coefficient in (3) is one.  No fourth cut is complete.

The standalone exact verifier is
[`verify_three_cut_two_boundary_star_cumulative_repair_countermodel.py`](../computations/verify_three_cut_two_boundary_star_cumulative_repair_countermodel.py).

## 2. Thirteen exact sources

Retain the nine internal cells on \(S=\{0,1,2,3,4,5\}\)

\[
\begin{array}{c|c@{\qquad}c|c@{\qquad}c|c}
01&E_{00}&45&E_{00}&02&E_{11}\\
14&E_{11}&04&E_{22}&13&E_{22}\\
25&E_{00}&35&E_{10}&23&E_{21},
\end{array}                                               \tag{5}
\]

and use the following four boundary cells:

\[
             56:E_{11},\qquad37:E_{11},\qquad
             26:E_{22},\qquad57:E_{22}.                  \tag{6}
\]

Every displayed source has weight one; every omitted aggregate block is
zero.  Endpoint order is literal.  In particular, \(35:E_{10}\) means
colour one at site \(3\) and colour zero at site \(5\), while
\(23:E_{21}\) means colours two and one at sites \(2\) and \(3\).

The cell \(23:E_{21}\) is retained because the family is a simultaneous
two-star escape from the repaired fixed-interior background.  It affects
internal cofactor spaces even though it lies in no supported full matching.

## 3. Full tensor expansion

Of the \(105\) perfect matchings on eight sites, exactly three are
supported:

\[
\begin{array}{c|c|c}
\text{matching}&\text{site-ordered word}&\text{weight}\\ \hline
01,26,37,45&00210021&1\\
02,14,37,56&11111111&1\\
04,13,26,57&22222222&1.
\end{array}                                               \tag{7}
\]

Equation (3) follows immediately.  It proves all four equalities in (2),
the exact diagonal coefficients

\[
 h_{0^8}=0,\qquad h_{1^8}=h_{2^8}=1,                    \tag{8}
\]

and the unique remaining mixed coefficient
\(h_{00210021}=1\).  No cancellation or support inference is used: these
are the complete rational coefficients.

At the level of the full tensor, (7) is the original twelve-source
three-cut countermodel with boundary sites \(6\) and \(7\) transposed; the
extra internal \(23\) cell is full-matching-inert.  This explains why a
list of nonsymmetric debt coordinates can always miss the transported
word.

## 4. Three explicit complete quotients

Let

\[
              D=H_B-\Delta_{8,3}
                =e_{00210021}-e_0^{\otimes8}.             \tag{9}
\]

The internal cofactors used in the original construction remain

\[
 H_{0145}=e_{0000},\qquad
 H_{0135}=e_{0010},\qquad
 H_{0125}=e_{0000}.                                      \tag{10}
\]

Restoring all named site slots gives the following literal insertion-space
decompositions.  On \(C_2=(2,6,7)\),

\[
 D=e_{221}^{C_2}\otimes
       \bigl(e_1^{(3)}\otimes H_{0145}\bigr)
   -e_{000}^{C_2}\otimes
       \bigl(e_0^{(3)}\otimes H_{0145}\bigr).            \tag{11}
\]

On \(C_3=(3,6,7)\),

\[
 D=e_{121}^{C_3}\otimes
       \bigl(e_2^{(2)}\otimes H_{0145}\bigr)
   -e_{000}^{C_3}\otimes
       \bigl(e_0^{(2)}\otimes H_{0145}\bigr).            \tag{12}
\]

On \(C_4=(4,6,7)\),

\[
 D=e_{021}^{C_4}\otimes
       \bigl(e_2^{(2)}\otimes H_{0135}\bigr)
   -e_{000}^{C_4}\otimes
       \bigl(e_0^{(3)}\otimes H_{0125}\bigr).            \tag{13}
\]

Each right side belongs to
\(E_z=V_{C_z}\otimes\mathcal S_{U_z}\).  By the exact equivalence between
the common-residual cylinder condition and the complete high-sector
quotient identity, cuts \(2,3,4\) are complete.

The internal constant-word intersections are unchanged from the repaired
model:

\[
\begin{array}{c|c|c}
z&\mathcal G_{U_z}\cap\mathcal S_{U_z}&\dim W_{U_z}\\ \hline
2&\langle0^{U_2},2^{U_2}\rangle&1\\
3&\langle0^{U_3},1^{U_3}\rangle&1\\
4&\langle0^{U_4}\rangle&2.
\end{array}                                               \tag{14}
\]

Hence all three quotients are target-active.

## 5. No fourth cut

Exact row reduction on all six cuts gives

\[
\begin{array}{c|cccccc}
z&0&1&2&3&4&5\\ \hline
\text{complete}&\text{no}&\text{no}&\text{yes}&\text{yes}&
                  \text{yes}&\text{no}\\
\dim W_{U_z}&3&3&1&1&2&1.
\end{array}                                               \tag{15}
\]

There is also a direct obstruction on each inactive cut.  For
\(z=0,1,5\), all-zero coordinate evaluation belongs to \(K_{U_z}\), while
the all-zero full coefficient is zero by (8).  The complete quotient would
require that contraction to equal the nonzero colour-zero target.  Thus no
fourth cut is hidden by the row calculation.

## 6. The new debt has the same one-cell repair

The transported word is not a terminal exceptional coordinate.  Append the
single source

\[
                         A_{67}\mathrel{+}=-E_{21}.       \tag{16}
\]

The matching \(01,23,45,67\) then has word \(00210021\) and weight
\(-1\), so it cancels the mixed term in (3).  The same \(67\) cell pairs
with the other three terms of the exact internal six-site tensor, giving

\[
\begin{aligned}
 H'_B={}&e_1^{\otimes8}+e_2^{\otimes8}\\
       &-e_{12120021}-e_{11111021}-e_{22022021}.          \tag{17}
\end{aligned}
\]

All four suffix-\(12\) words in (2), as well as \(00210021\), now vanish.
Exact row reduction again leaves precisely cuts \(2,3,4\) complete and
their defect dimensions equal to \((1,1,2)\).  Equation (17) is the
boundary-transposed analogue of the original two-source repair.  It proves
that the new word belongs to the same debt-transport mechanism rather than
creating a new obstruction.

## 7. Consequence for the route

The four coordinates in (2) do not constitute a coupled mixed sector:
they all distinguish the boundary suffix \(12\), while the simultaneous
two-star change transports the same structural debt to suffix \(21\).
A useful positive continuation must either control a permutation-stable
family of mixed coordinates, impose a genuinely whole-sector equation, or
activate a fourth cut.  This countermodel says nothing about arbitrary
Krenn instances beyond refuting this particular three-cut-plus-four-word
relaxation.

The
[independent audit](three-cut-two-boundary-star-cumulative-repair-countermodel-independent-audit.md)
reconstructs the endpoint-ordered expansion, both debt ledgers, all six
cuts, and all target defects with a separate dense rational implementation.
