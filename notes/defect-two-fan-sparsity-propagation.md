# Defect-two sparsity propagates to nine exceptional fan charts

## 1. Outcome

Let an exact ternary aggregate source satisfy

\[
                         H_B(A)=\Delta_{B,3}.
\]

Fix a center \(r\) of a good-pair fan, and let \(R\) be the global graph
whose edges are the rank-three aggregate blocks.  Put \(H=R-r\).  Consider
the fan neighbours \(u\) for which the pair chart \(\{r,u\}\) is
gauge-rigid and has defect exactly two.

The
[defect-two sparsity theorem](defect-coefficient-rank-and-two-defect-sparsity.md)
says that each such chart has a deleted-star row supported on at most two
internal sites.  This note propagates that chart-local conclusion without
trying to synchronize its defect coordinates.

**Theorem 1.1 (defect-two fan propagation).**  Let \(U_2\) be any set of
good fan neighbours whose charts are gauge-rigid and have defect exactly
two.  Then at least one of the following holds.

1. The center \(r\) has global rank-three degree at most two.
2. All but at most nine vertices of \(U_2\) have degree at most two in
   \(H=R-r\).

More precisely, if

\[
 D=\{u\in U_2:\deg_H(u)\le2\},                         \tag{1}
\]

and no global color row at \(r\) is supported on at most two sites, then

\[
 U_2\setminus D
   \subseteq \bigcup_{c:\,|S_c(r)|=3}S_c(r),
 \qquad |U_2\setminus D|\le9,                           \tag{2}
\]

where \(S_c(r)\) is the intrinsic physical-site support of color row
\(c\) at \(r\).

Consequently, if

\[
                    \deg_R(r)\ge3,\qquad \delta(R-r)\ge3,             \tag{3}
\]

then \(|U_2|\le9\).  A good fan has at least \(N-7\) members.  Therefore,
if every member is in (E2) and (3) holds, at least

\[
                              N-16                                    \tag{4}
\]

fan charts have defect at least three.  Thus exact defect two cannot
occupy a high-degree good fan except for nine charts.

The other alternative is also concrete.  A globally two-site-supported
center row occurs unchanged in a synchronized family of exact nine-row
overlap packets.  Section 4 records that packet.  It is not automatically
an extra Hessian direction or a contradiction; Section 5 gives an exact
selected-row realization.

## 2. Intrinsic rows and chart restrictions

For each color \(c\), orient the blocks incident with \(r\) toward \(r\)
and define

\[
 S_c(r)=\{x\ne r:\text{row }c\text{ of }A_{r\mid x}\text{ is nonzero}\}.
                                                                    \tag{5}
\]

This set is defined in the original source, before choosing a deleted
pair.  In the chart \(\{r,u\}\), the corresponding center row is

\[
 p_c^{(u)}=\sum_{x\notin\{r,u\}}
                  \operatorname{row}_c(A_{r\mid x}),
 \qquad
 \operatorname{supp}_s(p_c^{(u)})=S_c(r)\setminus\{u\}.              \tag{6}
\]

Write \(s_d^{(u)}\) for color row \(d\) of the other deleted star, from
\(u\) into \(B\setminus\{r,u\}\).  Every rank-three neighbour of \(u\)
inside \(H\) belongs to the support of every \(s_d^{(u)}\): an invertible
three-by-three matrix has no zero row.  Hence

\[
       |\operatorname{supp}_s(s_d^{(u)})|\le2
                  \quad\Longrightarrow\quad \deg_H(u)\le2.          \tag{7}
\]

No source cell is selected in (6)--(7).  The statements concern complete
aggregate endpoint rows and retain zero blocks, endpoint asymmetry, and
arbitrary complex cancellation.

## 3. Proof of the propagation theorem

Fix \(u\in U_2\).  The defect-two sparsity theorem supplies one row among

\[
             p_0^{(u)},p_1^{(u)},p_2^{(u)},
             s_0^{(u)},s_1^{(u)},s_2^{(u)}              \tag{8}
\]

whose site support has size at most two.

If a row \(s_d^{(u)}\) is sparse, (7) gives \(u\in D\).  Suppose instead
that \(u\notin D\).  Then a center row is sparse, so for some color \(c\),

\[
                         |S_c(r)\setminus\{u\}|\le2.                  \tag{9}
\]

If some \(|S_c(r)|\le2\), every rank-three neighbour of \(r\) lies in
that support, and therefore \(\deg_R(r)\le2\).  This is alternative 1.

Assume no center row has support at most two.  Equation (9) then forces

\[
                         |S_c(r)|=3,qquad u\in S_c(r).                \tag{10}
\]

Thus every \(u\in U_2\setminus D\) lies in one of at most three
three-element sets, proving (2) and alternative 2.  Under (3), both the
center-low-degree alternative and \(D\ne\varnothing\) are impossible, so
\(|U_2|\le9\).

Finally, a good fan has at least \(N-7\) members.  If every fan chart is
in (E2), every chart not in \(U_2\) has defect at least three.  Removing
at most nine exact-defect-two charts leaves

\[
                         (N-7)-9=N-16
\]

defect-at-least-three charts.  This proves (4). \(\square\)

The constant nine is sharp for this support argument: three disjoint
three-site sets \(S_0,S_1,S_2\) have a nine-element union, and deleting a
member of \(S_c\) leaves that row supported on two sites.  Goodness alone
does not prohibit three independent global rows with those disjoint
supports.  Any improvement must use their exact pair or overlap equations.

## 4. The exact synchronized nine-row packet

Suppose the first alternative in the proof occurs for color \(c\), and
write

\[
                              P=S_c(r),\qquad |P|\le2.                 \tag{11}
\]

Choose distinct fan neighbours \(u,v\notin P\).  Put

\[
 W=B\setminus\{r,u,v\},\qquad |B|=2m,
\]

write \(q\) for the quadratic internal to \(W\), and write \(p_c,s_d,t_e\)
for the rows from \(r,u,v\) into \(W\).  Orient
\(b_{de}=A_{u\mid v}(d,e)\) with \(u\) first.

The complete endpoint-ordered triple equation is

\[
\begin{aligned}
 &\bigl(A_{r\mid u}(c,d)t_e+A_{r\mid v}(c,e)s_d
                       +b_{de}p_c\bigr)q^{[m-2]}\\
 &\hspace{42mm}+p_cs_dt_e q^{[m-3]}
       =\delta_{c=d=e}X_c^W.                            \tag{12}
\end{aligned}
\]

Because \(u,v\notin P\), row \(c\) of each of
\(A_{r\mid u},A_{r\mid v}\) is zero.  Thus all nine choices of \((d,e)\)
reduce exactly to

\[
 \boxed{
 p_c\left(b_{de}q^{[m-2]}+s_dt_e q^{[m-3]}\right)
       =\delta_{c=d=e}X_c^W.}                           \tag{13}
\]

The same physical row \(p_c\), supported on \(P\), appears for every
choice of \(u,v\) outside \(P\).  Its exact first-contraction equation and
the
[two-hole coordinate-anchor lemma](good-pair-fan-six-port-triple-cofactor-reduction.md#32-the-two-hole-coordinate-anchor)
imply that at least one of its local components is proportional to \(e_c\).
Equation (13) retains the direct
block, both endpoint orders, the common divided power, and the full
two-star product.  It is therefore the correct residual object, rather
than an abstract response table.

This reduction uses only the nine triple rows with color \(c\) fixed at
the center.  The other eighteen rows, the even pair-chart diagonal
equations, and Hessian rigidity remain available and cannot be omitted in
a claimed closure.

## 5. An exact selected-row guard

The nine equations (13) are consistent even when the two opposite star
triples are independent.  This prevents a contradiction based only on the
displayed packet.

Take

\[
                       W=\{x,1,2,3,4\}
\]

and fix a color \(c\).  In the site-square-zero algebra put

\[
\begin{aligned}
 p_c&=e_c^{(x)},\\
 q&=e_c^{(1)}e_c^{(2)}+e_c^{(3)}e_c^{(4)},\\
 s_d&=e_d^{(x)},\qquad t_e=e_e^{(x)},\\
 b_{de}&=\delta_{d,c}\delta_{e,c}.
\end{aligned}                                           \tag{14}
\]

Then \(s_dt_e=0\) because both factors occupy site \(x\), while divided
powers give

\[
                    q^{[2]}=e_c^{(1)}e_c^{(2)}
                              e_c^{(3)}e_c^{(4)}.        \tag{15}
\]

At \(N=8\), equation (13) becomes

\[
 p_c\left(b_{de}q^{[2]}+s_dt_e q\right)
   =\delta_{d,c}\delta_{e,c}X_c^W,                     \tag{16}
\]

which is exact for all nine \((d,e)\).  Both triples
\((s_0,s_1,s_2)\) and \((t_0,t_1,t_2)\) are linearly independent.

This is a selected-row overlap relaxation.  Its internal quadratic is not
asserted to be gauge-rigid, it does not supply the other center rows, and
it is not an exact Krenn source.  It proves only that (13), sparse support,
a coordinate anchor, and opposite-star independence do not alone give a
contradiction.

There is a complementary structural warning.  The exact rational
[all-pair missing-row model](all-pair-missing-row-countermodel.md) uses one
common aggregate quadratic for every pair, has doubly injective aggregate
stars, coherent localized row defects, normalized pure coefficients, and
all pair-chart exchange identities.  It nevertheless evades the proposed
support globalization because its mixed GHZ coefficients do not vanish.
Thus graph data, common-source reindexing, and pure normalization cannot
replace the mixed equations in (12)--(13).  That model is a guard on the
method, not a counterexample to Theorem 1.1 or to a future exact
mixed-equation propagation theorem.

## 6. Scope and audit

The theorem closes one quantifier gap: exact defect-two charts cannot fill
a high-degree good fan, and the exceptional count is the absolute constant
nine.  It does **not** prove that a sparse row creates an extra Hessian
kernel, does not exclude the center-low-degree branch, and does not solve
the synchronized packet (13).  In particular, it does not promote a
selected-row guard to a pair chart or source.

The dependency-free checker
[verify_defect_two_fan_sparsity_propagation.py](../computations/verify_defect_two_fan_sparsity_propagation.py)
audits the set-theoretic implication behind (9)--(10), the sharp maximum
nine and the \(N-16\) arithmetic, and all nine exact identities in
(14)--(16) for each choice of the target color.
