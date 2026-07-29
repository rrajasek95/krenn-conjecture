# The adjacent \(E_{22}\) line has a full-cylinder fourth-cut obstruction

## 1. Status and scope

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
                         A_{25}=E_{00}+tE_{22}.            \tag{1}
\]

The exact verifier excludes a fourth complete cut
\(z\in\{0,1,5\}\) for every \(X,t\), with both boundary stars and
\(A_{67}\) arbitrary.  Every normal used in the successful argument is an
unprojected cylinder intersection.  An
[independent clean-room reconstruction](three-cut-internal-23-arbitrary-block-adjacent-25-22-fourth-cut-obstruction-independent-audit.md)
has rebuilt the endpoint-ordered geometry, torus cover, rank certificates,
exceptional normals, and all exact ideals under different orderings.  The
result is therefore promoted as an audited local theorem.

This remains a local statement for the displayed fixed six-site interior.
It does not allow arbitrary \(A_{25}\), and it does not prove the global
Krenn conjecture.

The consolidated primary verifier is

- [the \(E_{22}\) exact verifier](../computations/verify_three_cut_internal_23_arbitrary_block_adjacent_25_22_fourth_cut_obstruction.py).

Its supporting certificate generators are

- [the \(x_{00}\)-open full-cylinder minors](../computations/derive_three_cut_internal_23_adjacent_25_22_x00_open_line_minors.py);
- [the \(x_{00}\)-open symbolic star ideal](../computations/test_three_cut_internal_23_adjacent_25_22_x00_open_symbolic_star_ideal.py);
- [the five \(x_{00}=0\) line-chart minors](../computations/derive_three_cut_internal_23_adjacent_25_22_x00_zero_line_minors.py);
- [their five symbolic star ideals](../computations/test_three_cut_internal_23_adjacent_25_22_x00_zero_line_chart_star_ideals.py);
- [the uniform cut-\(5\) ten-space argument](../computations/derive_three_cut_internal_23_adjacent_25_22_cut5_line.py);
- [the eight exceptional-locus true-normal checks](../computations/verify_three_cut_internal_23_adjacent_25_22_exceptional_locus.py).

## 2. Geometry and the discarded quotient route

Let \(R_{ab}\) be the \(35\)-coordinate output block belonging to
\(x_{ab}\), and let \(T_{22}\) be the analogous block belonging to the
moving \(E_{22}\) cell on edge \(25\).  Exact endpoint-ordered enumeration
gives

\[
 |T_{22}|=35,\qquad
 |T_{22}\cap R_{20}|=|T_{22}\cap R_{21}|=|T_{22}\cap R_{22}|=9, \tag{2}
\]

with no other \(R_{ab}\)-overlap and no fixed-direct-tensor overlap.  The
affected deleted pairs are \(03,04,13,34\), and

\[
 [0^6],[1^6]\notin T_{22},\qquad [2^6]\in T_{22}.         \tag{3}
\]

Edges \(23\) and \(25\) share site \(2\), so all tensors, cofactors,
boundary atoms, and cylinder columns are affine separately in \(X,t\),
with no \(x_{ab}t\) term.  The \(t\)-character is independent of the
\(X\)-characters on every support.  Thus \(t\ne0\) can be normalized to
one without consuming an \(X\)-modulus.  The case \(t=0\) is the already
audited arbitrary-\(A_{23}\) theorem.

An earlier eleven-chart coordinate quotient is not part of the proof.
Its first-\(x_{01}\) chart has a nonunit compact basis of size \(4182\)
(size \(11525\) before compaction), and its \(x_{00}=0,x_{11}\ne0\)
chart has a nonunit compact basis of size \(4667\).  The first chart even
has the exact quotient point

\[
\begin{array}{c|cccc}
&p^0&q^0&p^1&q^1\\ \hline
\text{nonzero endpoint}&(2,0)&(3,0)&(3,1)&(5,1).
\end{array}                                               \tag{4}
\]

In the unreduced equations its ordered \(01\)-fibre leaves the single
residual word

\[
                              [220221]                    \tag{5}
\]

with coefficient one.  That word was killed with \(R_{02}\).  Hence (4)
is a quotient artifact, not an actual repair.  The successful proof below
was deliberately rebuilt with full cylinder normals.

## 3. Exact torus cover, including special complex coefficients

Assume \(t=1\).  The \(256\) supports with \(x_{00}\ne0\) form one
symbolic chart: normalize \(x_{00}=1\) and leave the other eight entries of
\(X\) as unrestricted polynomial variables.

Now set \(x_{00}=0\) and order the five entries

\[
                 x_{02},x_{10},x_{12},x_{20},x_{22}.     \tag{6}
\]

If one is nonzero, take the first nonzero entry in (6), normalize it to
one, force only the preceding entries in (6) to zero, and leave every
other entry symbolic.  The five charts contain

\[
                         128+64+32+16+8=248              \tag{7}
\]

supports.  This is not a binary specialization: later entries in (6) and
all of \(x_{01},x_{11},x_{21}\) remain arbitrary complex parameters in
both the rank minors and the star ideals.  Consequently all cancellations
at special complex values are covered by the constant minors and
polynomial unit certificates.

The remaining coordinate subspace is

\[
 x_{00}=x_{02}=x_{10}=x_{12}=x_{20}=x_{22}=0,\qquad
 \operatorname{supp}(X)\subseteq\{x_{01},x_{11},x_{21}\}. \tag{8}
\]

For every subset of those three cells, its nonzero character rows together
with the \(t\)-row have full row rank.  Over \(\mathbb C^*\), all nonzero
coefficients can therefore be normalized independently to one.  The eight
support patterns in (8) are exact torus representatives, with no continuous
modulus left.

Thus the complete \(t\ne0\) support count is

\[
                 256+128+64+32+16+8+8=512.               \tag{9}
\]

## 4. Full-cylinder normal certificates

### 4.1 The \(x_{00}\)-open chart

For \(z=0,1,5\), form the simultaneous-representation matrix for
\(C_2,C_3,C_4,C_z\).  Each cylinder has \(45\) ordered raw columns.
In \(C_2\), columns \(7=9\), \(22=24\), and \(37=39\) identically, so
three duplicates are omitted.  A constant \(176\times176\) minor gives

\[
\begin{array}{c|c|c|c}
z&\text{matrix}&\text{minor nonzeros}&\det\\ \hline
0&453\times177&292&1\\
1&436\times177&290&-1\\
5&514\times177&277&-1.
\end{array}                                               \tag{10}
\]

The representation kernel has dimension at most one, while the nonzero
direct matching tensor \(H_S\) supplies a common vector.  Hence every
normal in this chart is exactly \(\langle H_S\rangle\).

### 4.2 The five \(x_{00}=0\) charts for cuts \(0,1\)

The same full-cylinder construction, with all unnormalized entries
symbolic, gives:

\[
\begin{array}{c|cc|cc}
\text{pivot}&\multicolumn{2}{c|}{z=0}&\multicolumn{2}{c}{z=1}\\
&\text{matrix}&\det&\text{matrix}&\det\\ \hline
x_{02}&433\times177&-1&416\times177&1\\
x_{10}&416\times177&-1&401\times177&-1\\
x_{12}&391\times177&1&379\times177&-1\\
x_{20}&369\times177&-1&362\times177&-1\\
x_{22}&350\times177&1&343\times177&1.
\end{array}                                               \tag{11}
\]

Every minor is \(176\times176\) and is literally constant, not merely
nonzero at a sampled parameter value.  Therefore the cut-\(0\) and
cut-\(1\) normals are \(\langle H_S\rangle\) throughout all five charts.

### 4.3 A uniform cut-\(5\) argument

The cut-\(5\) raw presentation changes rank on special \(X\), so a naive
generic minor would miss exactly the dangerous degenerations.  Instead,
leave all nine entries of \(X\) symbolic and define

\[
 e_{ab}=[00ab00],\qquad
 T=[121200]+[111110]+[220220]+[222222].                   \tag{12}
\]

The nine \(e_{ab}\) are literal columns of both \(C_2\) and \(C_3\), and
the direct tensor is

\[
                         H_S(X)=\sum_{a,b}x_{ab}e_{ab}+T. \tag{13}
\]

A constant rank-\(77\) minor of the \(108\times87\)
simultaneous-representation matrix has \(89\) nonzeros and determinant
one.  It follows that

\[
 C_2\cap C_3
 =W:=\operatorname{span}\{e_{00},\ldots,e_{22},T\}.       \tag{14}
\]

Project the \(45\) raw \(C_5\) columns to the ten coordinates consisting
of the nine \(e_{ab}\)-coordinates and \([121200]\).  Exactly one column,
ordered column \(12\), survives, and its restriction is

\[
                 (x_{00},x_{01},x_{02},x_{10},x_{11},
                    x_{12},x_{20},x_{21},x_{22},1).       \tag{15}
\]

If \(\sum y_{ab}e_{ab}+sT\in W\cap C_5\), equation (15) forces
\(y_{ab}=s x_{ab}\) for every \(a,b\).  Conversely \(H_S\) belongs to every
cylinder.  Therefore, uniformly through every rank jump,

\[
                    C_2\cap C_3\cap C_5=\langle H_S\rangle. \tag{16}
\]

Adding \(C_4\) does not change this line.  This proves the cut-\(5\) normal
claim for all \(X\), not just the five open charts or binary supports.

### 4.4 The exceptional locus for cuts \(0,1\)

On the zero support in (8), the true normal is a line.  On each of the
seven nonzero supports it is a plane for \(z=0,1\).  These planes are used
directly; no quotient normal or generic-line assumption is made.

The frozen rank-certificate ledger is

    d167275b9c85c03c04e1455e752f0fbd38c6bf43cecb41a9468e448686a87825

## 5. Exact shared-star ideals

Retain target colours \(0,1\), both ordered off-diagonal fibres, and the
same \(72\) endpoint-ordered star variables.  The arbitrary \(A_{67}\)
term in each fibre is a multiple of \(H_S\), hence is absorbed by every
normal above.  A solution of the full three-colour system would restrict
to this two-colour packet.

The six symbolic normal-line programs are:

\[
\begin{array}{c|r|r|r|l}
\text{chart}&\text{variables}&\text{coordinates}&\text{generators}
&\text{program SHA256}\\ \hline
x_{00}&84&341&1320&08424bb178d088ea608ca643511d9c74e09f2d4587787eb0c989ebc877b9d84c\\
x_{02}&83&315&1216&a61f860b7c3cc1ab1f3ced4f90e6b71518fcb18d4a43279d0ddf38f8dc7744d8\\
x_{10}&82&294&1124&72fb09cb9a37f5d90d90c8aae80c87d5b0d3cc527f80e62051baeb0e2b45e3d6\\
x_{12}&81&266&1000&4e9d0a952f851637a27b53bdb3b2439c533d6d3ea570b2b6d7900000b96d71fc\\
x_{20}&80&243&912&670a31224f48d833d20980bc043a624b239e80c2eab34f6130d0520c7849cd6c\\
x_{22}&79&218&780&1c45aadc8a7f09c45e9a4a586e7d67a7a1d63d2317b0f3dcb8337abec118baf7
\end{array}                                               \tag{17}
\]

Every one has reduced basis \([1]\) over characteristic zero.

For the eight exceptional supports, the verifier builds the actual
unprojected normal separately for \(z=0,1,5\).  The \(24\) chart/cut jobs
reduce to \(15\) distinct programs: cuts \(0\) and \(1\) have the same
program on each support, while cut \(5\) uses the line (16).  All are unit.
Their generator counts range from \(412\) to \(512\), and each uses the
same \(72\) star variables.

Altogether the verifier records \(30\) chart/cut jobs and \(21\) distinct
Singular programs.  The frozen ideal ledger is

    58c54259ed83211c25704d2987900d405e40af507b96fa041d0975c0bb667efa

The literal eight-site endpoint-order audit assigns disjoint rational
values to all nine entries of \(X\), the moving coefficient, all \(108\)
star entries, and all nine entries of \(A_{67}\).  Direct matching
enumeration agrees with the four-fibre formula used to generate the
ideals.  A unit ideal over \(\mathbb Q\) remains unit after scalar extension
to \(\mathbb C\).

## 6. Reproduction and audit status

From the repository root, run

    uv run python computations/verify_three_cut_internal_23_arbitrary_block_adjacent_25_22_fourth_cut_obstruction.py

The default run recomputes all constant minors and probe identities,
regenerates and hashes all \(30\) ideal jobs, and reruns all \(21\) distinct
characteristic-zero programs.  It must end with

    A23 arbitrary plus A25=E00+tE22 local fourth-cut obstruction: PASS
    t=0 inherited; t!=0 torus cover 256+128+64+32+16+8+8: PASS
    full unprojected normals for cuts 0,1,5: PASS
    30 chart/cut ideals, all exact characteristic-zero units: PASS
    endpoint order, shared stars, ordered fibres, arbitrary A67: PASS

The final clean primary run on 2026-07-27 took \(49.689\) seconds in total;
its parallel Singular phase took \(6.794\) seconds, with a \(6.784\)-second
maximum individual program time.

The independent audit reruns the torus cover, the constant minors, the
cut-\(5\) probe identity, every exceptional normal, and all unit ideals from
fresh endpoint-ordered enumeration.  The remaining adjacent one-cell lines
are \(E_{10}\) and \(E_{20}\); unlike \(E_{22}\), each retains a torus
cross-ratio on its fully nonzero stratum.
