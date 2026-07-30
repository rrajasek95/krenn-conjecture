# Common-label repair on the double-zero two-chart packet

## 1. Outcome

Retain the double-hafnian-zero branch of the
[two-chart synchronization theorem](two-chart-hamming-one-gamma-synchronization.md).
Fix the pure colour \(\delta\), write the other two physical labels as

\[
                              E=\{\alpha,\beta\},
\]

and put

\[
\begin{aligned}
 A&=I_{pq}^{c},& B&=J_{pq}^{c},& C&=P_{A,B}\ne0,\\
 A'&=I_{pr}^{c},& B'&=J_{pr}^{c},& C'&=R_{A',B'}\ne0.
\end{aligned}                                                   \tag{1}
\]

All four complements are nonempty subsets of \(E\).  This note closes the
formal common-label ledger up to one sharp projective boundary.

1. A label \(e\in E\) is detected by a compression \(C\) exactly when
   \(e\in A\cap B\) and \(C\) is not proportional to \(E_{ee}\).
2. If the two nonempty detector sets are disjoint, then, after exchanging
   \(\alpha,\beta\), they are \(\{\alpha\}\) and \(\{\beta\}\).  Each
   compression has one of only three forms: a row hook, a column hook, or
   the opposite diagonal unit.
3. Every hook can be repaired by adjoining one literal diagonal row from
   the same full-nine system.  The repaired functional is rank one, kills
   the complete direct block, and exports a unary cap with the label
   detected on the other chart.  Hence every hook mismatch gives a
   source-valid asymmetric version of the same-label cubic.
4. Crossed coordinate cells admit the same rank-one repair.  A diagonal
   coordinate cell gives instead a binary direct-zero normal row or a
   radial row with nonzero direct scalar.
5. The only compression-level obstruction to a common direct-zero normal
   label is a pair of nonzero pure diagonal cells on opposite missing
   labels.  If no entry outside those cells is available in the full direct
   blocks, then
   \(P\in\mathbb C^*E_{\beta\beta}\) and
   \(R\in\mathbb C^*E_{\alpha\alpha}\).  The selected curvature is then
   necessarily in the selected-entry-zero, trace-only orientation
   \(B_0=0\), \(\kappa=A_0U_0\ne0\).

The conclusion is a reduction, not a contradiction.  In particular, no
factor \(z^{[h-2]}\) is cancelled below.

## 2. Exact detector classification

For nonempty \(A,B\subseteq E\), regard \(C\ne0\) as an element of
\(\operatorname {Mat}_{A,B}\).  Define its detector set by

\[
 \mathscr D_{A,B}(C)=
 \left\{e\in E:\begin{array}{c}
   \text{there is }\ell\in\operatorname {Mat}_{A,B}^{*}\text{ with}\\[-1mm]
   \ell(C)=0\text{ and }\ell((E_{ee})_{A,B})\ne0
 \end{array}\right\}.                                      \tag{2}
\]

**Lemma 2.1 (dual-separation criterion).**

\[
 \boxed{\mathscr D_{A,B}(C)
   =\{e\in A\cap B:(E_{ee})_{A,B}\notin\mathbb C C\}.}       \tag{3}
\]

**Proof.**  If \(e\notin A\cap B\), the restricted diagonal unit is zero.
If \(e\in A\cap B\), a functional annihilating \(C\) but not
\(E_{ee}\) exists exactly when \(E_{ee}\) does not lie in the line
\(\mathbb C C\).  This is ordinary dual separation in the finite-dimensional
space \(\operatorname {Mat}_{A,B}\).  \(\square\)

Because \(|E|=2\), (3) has a short structural normal form.

**Corollary 2.2 (singleton normal forms).**  Suppose
\(\mathscr D_{A,B}(C)=\{\alpha\}\).  Exactly one of the following holds:

\[
\begin{array}{c|c|c}
\text{type}&(A,B)&\text{required compression entry}\ \\ \hline
\text{row hook}&(\{\alpha\},E)&C_{\alpha\beta}\ne0,\\
\text{column hook}&(E,\{\alpha\})&C_{\beta\alpha}\ne0,\\
\text{opposite diagonal}&(E,E)&C=\gamma E_{\beta\beta},\quad\gamma\ne0.
\end{array}                                                   \tag{4}
\]

The corresponding normalized detector may be chosen as

\[
\begin{array}{c|c}
\text{type}&\ell_\alpha\\ \hline
\text{row hook}&
 \epsilon_{\alpha\alpha}
  -\dfrac{C_{\alpha\alpha}}{C_{\alpha\beta}}
       \epsilon_{\alpha\beta},\\[3mm]
\text{column hook}&
 \epsilon_{\alpha\alpha}
  -\dfrac{C_{\alpha\alpha}}{C_{\beta\alpha}}
       \epsilon_{\beta\alpha},\\[3mm]
\text{opposite diagonal}&\epsilon_{\alpha\alpha}.
\end{array}                                                   \tag{5}
\]

Here \(\epsilon_{ij}\) denotes coordinate evaluation.  Every matrix in
(5) has rank one, and

\[
 \ell_\alpha(C)=0,qquad
 \ell_\alpha(E_{\alpha\alpha})=1,qquad
 \ell_\alpha(E_{\beta\beta})=0.                             \tag{6}
\]

**Proof.**  If \(A\cap B=\{\alpha\}\), the only two grids larger than the
single cell \((\alpha,\alpha)\) are the displayed row and column hooks.
Detection requires the other hook coordinate to be nonzero.  If
\(A\cap B=E\), then \(A=B=E\); failure to detect \(\beta\) says precisely
that \(C\) is a nonzero multiple of \(E_{\beta\beta}\).  The formulas in
(5) prove (6) directly.  \(\square\)

The empty detector set is equally rigid.

**Corollary 2.3 (coordinate-cell boundary).**
\(\mathscr D_{A,B}(C)=\varnothing\) exactly in one of the following cases.

1. \(A\cap B=\varnothing\).  Then \(A,B\) are opposite singletons and
   \(C\) is their sole off-diagonal coordinate cell.
2. \(A\cap B=\{k\}\) and \(C=\gamma E_{kk}\), \(\gamma\ne0\).

If \(A=B=E\), at least one missing label is always detected.  In
particular, if two detector sets are nonempty and disjoint, then after
renaming the missing labels they are \(\{\alpha\}\) and
\(\{\beta\}\), and Corollary 2.2 applies to each chart.  There is no
larger case census hidden here.

## 3. Source constraints and the unary caps

Let \(D=\mathcal V\setminus\{p,q,r\}\), and use
\(x_i,y_j,t_k\) for the three endpoint stars on \(D\).  Superscript
\(\delta\) below means scalarization of every site of \(D\) at the pure
colour \(\delta\).  Directly from the definitions of the four channel
sets,

\[
\begin{aligned}
 i\in A
   &\Longleftrightarrow x_i^\delta=0\text{ and }R_{i\delta}=0,&
 i\in A'
   &\Longleftrightarrow x_i^\delta=0\text{ and }P_{i\delta}=0,\\
 j\in B
   &\Longleftrightarrow y_j^\delta=0\text{ and }T_{j\delta}=0,&
 k\in B'
   &\Longleftrightarrow t_k^\delta=0\text{ and }T_{\delta k}=0.
                                                               \tag{7}
\end{aligned}
\]

Suppose the detector sets are \(\{\alpha\}\) on the \(pq\)-chart and
\(\{\beta\}\) on the \(pr\)-chart.  Since
\(\alpha\in A\cap B\) and \(\beta\in A'\cap B'\), (7) gives

\[
\begin{gathered}
 x_\alpha^\delta=x_\beta^\delta=0,qquad
 R_{\alpha\delta}=0,qquad P_{\beta\delta}=0,\\
 y_\alpha^\delta=0,qquad t_\beta^\delta=0,qquad
 T_{\alpha\delta}=T_{\delta\beta}=0.                         \tag{8}
\end{gathered}
\]

There are also exact hook exits.  A \(pq\) row hook has
\(A=\{\alpha\}\), so \(\beta\notin A\); (7) and
\(x_\beta^\delta=0\) force

\[
                              R_{\beta\delta}\ne0.             \tag{9}
\]

A \(pr\) row hook similarly forces \(P_{\alpha\delta}\ne0\).
For a column hook the corresponding statement is the literal alternative

\[
 y_\beta^\delta\ne0\text{ or }T_{\beta\delta}\ne0,qquad
 t_\alpha^\delta\ne0\text{ or }T_{\delta\alpha}\ne0.          \tag{10}
\]

Thus the mismatch is compatible with the shared \(p\)-endpoint only through
specific visible cross cells or non-\(\delta\) star data.  Injectivity of
the four full decorated endpoint-star maps does not make the pure
\(\delta\) rows in (8) nonzero; goodness can be supplied in the other local
colours.

Now use the literal full-nine equations on the \(pq\)-chart,

\[
 P_{ij}q_{pq}^{[h]}+p_i s_jq_{pq}^{[h-1]}=\delta_{ij}X_i.
                                                               \tag{11}
\]

Applying the functional (5), with no contraction of a common power, gives

\[
 \left(\sum_{i,j}(\ell_\alpha)_{ij}p_i s_j\right)
              q_{pq}^{[h-1]}=X_\alpha.                         \tag{12}
\]

This is a unary rank-one cap.  The analogous detector on the \(pr\)-chart
exports a unary rank-one cap with target \(X_\beta\).  Merely observing
these two different targets does not permit their normal rows to be
subtracted.  The hook repair below supplies the missing same target.

## 4. Rank-one hook repair

Assume first that the \(pr\)-compression, whose detector is \(\beta\), is
a row hook.  Thus

\[
 A'=\{\beta\},\qquad B'=E,qquad R_{\beta\alpha}\ne0.
\]

Adjoin the literal \((\alpha,\alpha)\) diagonal row and define

\[
 \widehat\ell'_\alpha
   =\epsilon_{\alpha\alpha}
      -{R_{\alpha\alpha}\over R_{\beta\alpha}}
         \epsilon_{\beta\alpha}.                             \tag{13}
\]

Then

\[
 \widehat\ell'_\alpha(R)=0,qquad
 \widehat\ell'_\alpha(E_{\alpha\alpha})=1,qquad
 \widehat\ell'_\alpha(E_{cc})=0\quad(c\ne\alpha).           \tag{14}
\]

Its endpoint-star contraction is visibly rank one:

\[
 \sum_{i,k}(\widehat\ell'_\alpha)_{ik}p_i t_k
  =\left(p_\alpha-{R_{\alpha\alpha}\over R_{\beta\alpha}}
                    p_\beta\right)t_\alpha.                  \tag{15}
\]

Consequently the complete \(pr\) full-nine system gives a second unary cap
with target \(X_\alpha\).  For a column hook, use instead

\[
 \widehat\ell'_\alpha
   =\epsilon_{\alpha\alpha}
      -{R_{\alpha\alpha}\over R_{\alpha\beta}}
         \epsilon_{\alpha\beta},                              \tag{16}
\]

whose star contraction is
\(p_\alpha(t_\alpha-\rho t_\beta)\).  Equations (13) and (16) mix one
diagonal row with one mandatory off-diagonal row of the same physical
source.  They are not abstract changes of basis on a \(2\times2\) matrix.

It follows immediately that every nonempty disjoint-detector packet with a
hook on at least one chart has a common unary target:

* if the \(pr\)-chart is a hook, repair it to the \(pq\)-target
  \(\alpha\);
* if the \(pr\)-chart is opposite diagonal and the \(pq\)-chart is a hook,
  repair the \(pq\)-chart to the \(pr\)-target \(\beta\).

The only nonempty mismatch not covered is therefore

\[
 A=B=A'=B'=E,qquad
 C=\gamma E_{\beta\beta},qquad
 C'=\gamma' E_{\alpha\alpha}.                               \tag{17}
\]

## 5. The correctly normalized asymmetric cubic

The repair remains source-valid after exposing the third site.  The literal
27-row identity on \(D\) is

\[
 (P_{ij}t_k+R_{ik}y_j+T_{jk}x_i)z^{[h-1]}
   +x_i y_j t_kz^{[h-2]}
   =\mathbf1_{i=j=k}X_i^D.                                   \tag{18}
\]

Let \(\lambda\) be any functional on the \(P\)-block and \(\mu\) any
functional on the \(R\)-block.  Put

\[
\begin{aligned}
 c&=\lambda(P),&
 U&=\sum_{i,j}\lambda_{ij}x_i y_j,&
 L_k&=\sum_{i,j}\lambda_{ij}(R_{ik}y_j+T_{jk}x_i),\\
 c'&=\mu(R),&
 U'&=\sum_{i,k}\mu_{ik}x_i t_k,&
 L'_j&=\sum_{i,k}\mu_{ik}(P_{ij}t_k+T_{jk}x_i).
                                                               \tag{19}
\end{aligned}
\]

Applying the two functionals to (18) gives the exact normal rows

\[
\begin{aligned}
 (ct_k+L_k)z^{[h-1]}+Ut_kz^{[h-2]}
   &=\lambda(E_{kk})X_k^D,\\
 (c'y_j+L'_j)z^{[h-1]}+U'y_jz^{[h-2]}
   &=\mu(E_{jj})X_j^D.                                      \tag{20}
\end{aligned}
\]

Suppose for one physical label \(e\) that

\[
                         \lambda(E_{ee})=\mu(E_{ee})=1.       \tag{21}
\]

No equality of the other diagonal response coefficients is required here.
For fixed exposed label \(e\), the right side of the first normal row is
\(\lambda(E_{ee})X_e^D\), and the right side of the second is
\(\mu(E_{ee})X_e^D\).  Values on \(E_{ff}\), \(f\ne e\), occur only in
the distinct \(f\)-normal rows.  Thus even when the complete caps are
binary, (21) aligns the two literal \(e\)-row targets exactly.

Subtract the two \(e\)-rows and use only the divided-power identity

\[
                         zz^{[h-2]}=(h-1)z^{[h-1]}.
\]

One obtains

\[
 \boxed{
 \left(
    Ut_e-U'y_e
    +{ct_e+L_e-c'y_e-L'_e\over h-1}z
 \right)z^{[h-2]}=0.}                                      \tag{22}
\]

This is the correctly normalized general comparison.  For two direct-zero
functionals, \(c=c'=0\), it becomes

\[
 \boxed{
 \left(Ut_e-U'y_e+{L_e-L'_e\over h-1}z\right)
             z^{[h-2]}=0.}                                  \tag{23}
\]

Taking \(\lambda\) to be a compression detector and \(\mu\) to be one of
(13) or (16) is the promised asymmetric replacement for the same-label
cubic.  Equation (22) also records the radial terms needed on a diagonal
cell boundary.  Both equations were formed from the literal rows before
the common power; neither licenses cancellation of \(z^{[h-2]}\).

## 6. Coordinate-cell boundaries

The coordinate cases in Corollary 2.3 can be incorporated without hiding
their loss of provenance.

### 6.1 Crossed cell

Suppose \(C=\gamma E_{uv}\), where \(u\ne v\).  For either missing label
\(e\in\{u,v\}\), define

\[
 \widehat\ell_e
   =\epsilon_{ee}-{P_{ee}\over\gamma}\epsilon_{uv}.          \tag{24}
\]

Then \(\widehat\ell_e(P)=0\),
\(\widehat\ell_e(E_{ee})=1\), and the two cells in (24) share a row or a
column.  Thus (24) is rank one and exports a unary cap.  A crossed
coordinate cell is an obstruction only if one insists that the functional
remain inside the original one-cell compression.

### 6.2 Diagonal cell

Suppose \(C=\gamma E_{kk}\) and \(A\cap B=\{k\}\).  For the other label
\(f\),

\[
 \widehat\ell_f
   =\epsilon_{ff}-{P_{ff}\over\gamma}\epsilon_{kk}           \tag{25}
\]

kills \(P\) and detects the \(f\)-normal row.  Its complete cap has target

\[
                         X_f-{P_{ff}\over\gamma}X_k,          \tag{26}
\]

so it is binary unless \(P_{ff}=0\).  To use the \(k\)-normal row with
\(\epsilon_{kk}\), one has the nonzero direct scalar \(c=\gamma\) and
must retain the radial term in (22).  If any other nonzero coordinate of
the full block \(P\) is available, the two-coordinate construction in
(24), with that coordinate in place of \((u,v)\), also kills the direct
scalar.

More invariantly, after adjoining at most one literal diagonal coordinate
to the compression support, define

\[
 \widehat{\mathscr D}(C)=\{e\in E:C\notin\mathbb C E_{ee}\}. \tag{27}
\]

For every \(e\in\widehat{\mathscr D}(C)\), choose a nonzero coordinate
\(C_{uv}\) with \((u,v)\ne(e,e)\) and use

\[
 \epsilon_{ee}-{P_{ee}\over C_{uv}}\epsilon_{uv}.            \tag{28}
\]

Two extended detector sets fail to meet exactly when the compressions are
nonzero pure diagonal cells on opposite labels.  Here ``meet'' means that
both charts have a direct-zero functional normalized to one on the same
single \(e\)-normal row; it does not assert that their complete cap target
vectors agree or that either cap is unary.  The paragraph after (21) is
what makes this weaker normalization sufficient for (22).

If entries outside the compressions are permitted, the same statement with
\(C,C'\) replaced by the full blocks \(P,R\) shows that the sole obstruction
to a common direct-zero normalized \(e\)-normal comparison is

\[
                  P=\rho E_{\beta\beta},\qquad
                  R=\rho' E_{\alpha\alpha},qquad
                  \rho\rho'\ne0.                             \tag{29}
\]

Indeed, Lemma 2.1 applied in the full nine-dimensional matrix space says
that a fixed missing label \(e\) admits such a functional on a nonzero
block \(S\) exactly when \(S\notin\mathbb C E_{ee}\).  If the two resulting
two-label sets are disjoint, each must be a singleton.  Therefore one block
is a pure \(\alpha\alpha\) unit and the other a pure \(\beta\beta\) unit.
Conversely those two units plainly give the two opposite singleton sets.
This proves (29) as a statement about normalized individual normal rows;
the binary-cap warning following (26) remains in force.

This includes both the opposite-diagonal normal form (17) and its
coordinate-cell variants.

## 7. The opposite-pure-diagonal survivor

Assume (29), oriented so the selected nonzero curvature entry is

\[
                         A_0=P_{ab}\ne0.
\]

Then \(a=b=\beta\).  Since the only nonzero row of \(R\) is row
\(\alpha\ne\beta\),

\[
                         B_0=R_{ac}=R_{\beta c}=0.
\]

The selected curvature therefore reduces exactly to

\[
                         \boxed{\kappa=A_0U_0\ne0.}           \tag{30}
\]

Thus \(U_0\ne0\), and the survivor is the selected-entry-zero,
trace-only \(B_0=0\) orientation already isolated by the
[tilted-chart theorem](tilted-second-chart-activity-and-zero-block-boundary.md).
This is not that theorem's intrinsic direct-free boundary: here the full
second direct block is \(R=\rho'E_{\alpha\alpha}\ne0\).
Goodness does not exclude (29): the full endpoint-star maps can acquire
their missing ranks from common-site coefficients in non-\(\delta\) colours.

For target \(\alpha\), the \(pq\) coordinate functional has direct scalar
zero while the \(pr\) coordinate functional has direct scalar \(\rho'\).
Their two expansions are the very same \((\alpha,\alpha,\alpha)\) member
of (18), so (22) is identically zero.  The same holds at \(\beta\).  Hence
the raw radial comparison does not manufacture a transverse correction on
this boundary.

## 8. Exact eight-site guard and scope

The following guard shows why the diagonal anchors, goodness, curvature,
and synchronized pure data do not by themselves force a common compression
label.  Use sites

\[
                         (p,q,r,a,b,c,d,e)
\]

and the following unit cells, with every unlisted cell zero:

\[
\begin{array}{c|l}
0&(pa;00),(qb;00),(rc;00),(de;00),\\
1&(qr;11),(pe;11),(ab;11),(cd;11),\\
2&(qr;22),(pd;22),(ac;22),(be;22),\\
\text{extra}&(pq;12),(pq;10),(pr;21),(pr;20).
\end{array}                                                   \tag{31}
\]

For the pure colour \(\delta=0\), the four channel sets are

\[
 (I_{pq},J_{pq})=(\{0,2\},\{0\}),\qquad
 (I_{pr},J_{pr})=(\{0,1\},\{0\}).                            \tag{32}
\]

Consequently

\[
 C=P_{\{1\},\{1,2\}}=(0,1),\qquad
 C'=R_{\{2\},\{1,2\}}=(1,0),                               \tag{33}
\]

and the detector sets are exactly \(\{1\}\) and \(\{2\}\).  All four
deleted endpoint-star maps have rank three.  Both pure residual hafnians
and every Hamming-one internal coefficient vanish, while the cross tensor
is \(E_{000}\).  Taking the fourth site to be \(c\) and selected labels
\((a,b,c,d)=(1,2,0,0)\) gives \(\kappa=1\).

Exact perfect-matching enumeration gives the three pure words and eight
mixed words

\[
\begin{gathered}
00000000,\quad11111111,\quad22222222,\\
01102112,\quad02202112,\quad10011000,\quad12011000,\\
12211111,\quad20020200,\quad20120200,\quad21122222.
                                                               \tag{34}
\end{gathered}
\]

Therefore all three diagonal fibres are exact on both the \(pq\)- and
\(pr\)-charts, but every one of the six off-diagonal rows fails.  The two
unary caps are nevertheless present.  This guard does **not** satisfy the
full-nine antecedent and is not a counterexample to the conjecture.  Its
precise role is to rule out any common-label argument using the diagonal
anchors, goodness, synchronized pure data, and curvature without mixing in
the off-diagonal rows.  The hook repair in Section 4 performs exactly that
missing mix.

The dependency-free checker
[`verify_double_zero_common_label_repair.py`](../computations/verify_double_zero_common_label_repair.py)
exhausts every nonzero \(\{-1,0,1\}\)-valued compression on every
two-label grid, audits the exact rank-one hook formulas, and verifies the
complete matching enumeration (31)--(34).

## 9. Remaining gate

The common-label issue is therefore no longer a nine-pattern case split.

* Every row or column hook, and every crossed coordinate cell, supplies a
  source-valid repaired anchor and the asymmetric cubic (22).
* A diagonal coordinate cell supplies the binary/radial version of (22).
* After using every available direct coordinate, the sole algebraic
  obstruction to the normalized one-row cubic is the
  opposite-pure-diagonal, selected-entry-zero packet (29)--(30).  Diagonal cells
  reached through (25) retain a separate binary-cap provenance loss.

Closing that last packet still requires the diagonal anchor to interact
with a nonisotropic off-diagonal curvature row before quotienting by the
common power.  Nothing proved here permits cancellation of
\(z^{[h-2]}\), and the conjecture remains open.
