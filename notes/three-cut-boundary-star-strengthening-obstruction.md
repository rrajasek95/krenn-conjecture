# Boundary-star obstructions beyond the three-cut countermodel

## 1. Result and exact scope

Start from the repaired fourteen-source family in
[the three-cut countermodel](three-adjacent-five-cut-complete-quotient-countermodel.md),
whose independent reconstruction is
[here](three-adjacent-five-cut-complete-quotient-countermodel-independent-audit.md).
Fix one boundary site \(q\in\{6,7\}\).  Keep every aggregate edge block
not incident to \(q\) exactly as in that repaired family, but replace all
seven blocks incident to \(q\) by arbitrary endpoint-ordered tensors:

\[
             A_{qj}\in V_q\otimes V_j\qquad(j\ne q).      \tag{1}
\]

Thus (1) has \(7\cdot 3^2=63\) arbitrary complex cell coefficients.  It
is not a formal tensor relaxation: every choice is realized by at most one
decorated source per nonzero cell, with that cell coefficient as its
weight.  Parallel sources and cancellations aggregate to exactly the same
family.

Two exact obstructions hold.

1. No member of either the \(q=6\) or \(q=7\) family satisfies the complete
   quotient identity on any fourth adjacent cut
   \(z\in\{0,1,5\}\).  The target-defect dimensions on those cuts remain
   \((3,3,1)\), respectively, because changing a boundary star does not
   alter any internal five-set cofactor.
2. If the first repaired mixed word is required to remain killed, then no
   member can also kill even the first of the three new debt words while
   retaining the original complete cuts.  More precisely, the \(q=7\)
   family cannot have the cut \(z=3\) complete together with

   \[
       [e_{00210012}]H_B=[e_{12120012}]H_B=0,             \tag{2}
   \]

   and the \(q=6\) family cannot have the cut \(z=2\) complete together
   with (2).  Hence a cumulative vanishing of all four old and repaired
   mixed words is impossible in either one-star family.

The proof is by small support identities, not a bounded weight scan.  It
holds for arbitrary complex values of all 63 cells.  It is nevertheless a
fixed-background obstruction: changing an internal block, or changing
nonstar boundary blocks on both stars simultaneously, leaves this theorem's
scope.  No global four-cut theorem is inferred.

The standalone exact audit is
[`verify_three_cut_boundary_star_strengthening_obstruction.py`](../computations/verify_three_cut_boundary_star_strengthening_obstruction.py).

## 2. Fixed background and notation

Put \(S=\{0,1,2,3,4,5\}\).  Before freeing a star, the repaired family has
the cells

\[
\begin{array}{c|c@{\qquad}c|c}
01&E_{00}&45&E_{00}\\
02&E_{11}&14&E_{11}\\
36&E_{11}&57&E_{11}\\
04&E_{22}&13&E_{22}\\
27&E_{22}&56&E_{22}\\
25&E_{00}&35&E_{10}\\
23&E_{21}&67&-E_{12}.
\end{array}                                               \tag{3}
\]

Every unlisted nonstar block remains zero.  For a full word
\(w\in\{0,1,2\}^8\), write

\[
                         h_w=[e_w]H_B.                    \tag{4}
\]

The relevant mixed words are

\[
\begin{aligned}
 w_0&=00210012,\\
 w_1&=12120012,\\
 w_2&=11111012,\\
 w_3&=22022012.                                           \tag{5}
\end{aligned}
\]

The repaired tensor has \(h_{w_0}=0\) and
\(h_{w_1}=h_{w_2}=h_{w_3}=-1\).

For \(z\in S\), retain the notation

\[
 U_z=S\setminus\{z\},\qquad C_z=(z,6,7),\qquad
 \mathcal S_{U_z}=\sum_{u\in U_z}V_u\otimes
                          H_{U_z\setminus\{u\}},
 \qquad K_{U_z}=\mathcal S_{U_z}^{\perp}.                 \tag{6}
\]

Every cofactor in (6) lies entirely inside \(S\), so freeing either
boundary star changes neither \(\mathcal S_{U_z}\) nor \(K_{U_z}\).

## 3. Why no fourth cut can be activated

Let \(\epsilon_{0,z}\in V_{U_z}^*\) be coordinate evaluation at the
all-zero word.  The fixed pure-zero internal edges in \(S\) are only

\[
                            01,\qquad45,\qquad25.         \tag{7}
\]

For \(z=0\) or \(z=1\), the pure-zero graph induced on \(U_z\) has only
\(45\) and \(25\), which share site \(5\).  For \(z=5\), it has only
\(01\).  After deleting any insertion site \(u\), none can perfectly match
the other four vertices.  Hence every cofactor-insertion column has zero
all-zero coordinate, and

\[
            \epsilon_{0,z}\in K_{U_z}qquad(z=0,1,5).     \tag{8}
\]

Next consider a hypothetical all-zero full matching after an arbitrary
star at \(q\) has been chosen.  The matching pairs \(q\) with one site
\(j\).  If \(j\) is not the other boundary site, that other boundary site
must be matched through a fixed nonstar edge.  At site \(6\), the only such
edges are \(36=E_{11}\) and \(56=E_{22}\); at site \(7\), they are
\(57=E_{11}\) and \(27=E_{22}\).  None has colour zero there.  If \(j\)
is the other boundary site, the remaining six sites are \(S\), and the
three edges in (7) have no perfect matching of \(S\).  Therefore

\[
                   h_{00000000}=0                         \tag{9}
\]

for every assignment of all 63 cells on either star.

The complete quotient identity on \(C_z\mid U_z\), evaluated at
\(\epsilon_{0,z}\), has target \(e_0^{\otimes C_z}\).  Equivalently, in
the common-residual form, the \(C_z\)-row of
\(H_B-\Delta_{8,3}\) at \(e_0^{\otimes C_z}\) must be annihilated by
\(\epsilon_{0,z}\).  Equations (8)--(9) give instead

\[
 \epsilon_{0,z}\!\left(
 [e_0^{\otimes C_z}](H_B-\Delta_{8,3})\right)=-1,         \tag{10}
\]

a contradiction.  Thus no fourth cut \(z=0,1,5\) is complete.  This does
not even require assuming that cuts \(2,3,4\) remain complete.

## 4. The site-7 cumulative-repair invariant

Free the entire site-\(7\) star.  Denote by

\[
 x=[E_{22}^{27}]A_{27},\qquad
 y=[E_{12}^{67}]A_{67}                                   \tag{11}
\]

the two indicated final aggregate cell coefficients.  Enumeration of
compatible fixed nonstar matchings gives

\[
       h_{22222222}=x,\qquad
       h_{w_0}=x+y,\qquad
       h_{w_1}=y.                                        \tag{12}
\]

Indeed, the all-two word has the unique fixed completion
\(04,13,56\), so its star edge is \(27\).  The word \(w_0\) has exactly
the two completions

\[
               01,27,36,45
       \quad\text{and}\quad
               01,23,45,67,                              \tag{13}
\]

while \(w_1\) has only

\[
                         02,13,45,67.                     \tag{14}
\]

All other star cells are irrelevant to these three coefficients.  Thus
every member of the 63-parameter family obeys the support identity

\[
               \boxed{h_{22222222}-h_{w_0}+h_{w_1}=0.}   \tag{15}
\]

On \(U_3=(0,1,2,4,5)\), coordinate evaluation
\(\epsilon_{2,3}\) at the all-two word belongs to \(K_{U_3}\): no
four-site internal cofactor has an all-two perfect matching there.  Indeed,
the only compatible internal edge is \(04=E_{22}\), so after any one site
is deleted there cannot be two compatible disjoint edges.  Its
target value is \(e_2\).  Consequently the complete cut \(z=3\) forces

\[
                         h_{22222222}=1.                  \tag{16}
\]

Equations (15)--(16) are incompatible with
\(h_{w_0}=h_{w_1}=0\).  In particular, arbitrary reweighting and arbitrary
new decorated sources anywhere on the site-\(7\) star cannot accomplish a
cumulative repair.

## 5. The site-6 cumulative-repair invariant

The other star has an analogous, slightly less diagonal certificate.  Put

\[
 p=[E_{11}^{36}]A_{36},\qquad
 r=[E_{01}^{46}]A_{46},\qquad
 y=[E_{12}^{67}]A_{67},                                  \tag{17}
\]

and define

\[
                         v=12120111.                      \tag{18}
\]

The compatible-match enumeration is

\[
 h_{11111111}=p,qquad h_v=r,qquad
 h_{w_0}=p+r+y,qquad h_{w_1}=y.                         \tag{19}
\]

Hence

\[
        \boxed{h_{11111111}+h_v-h_{w_0}+h_{w_1}=0.}      \tag{20}
\]

In the site order \(U_2=(0,1,3,4,5)\), let

\[
 \beta_6=[11111]^*+[12201]^*.                            \tag{21}
\]

Direct evaluation on every insertion column gives
\(\beta_6\in K_{U_2}\).  This can also be seen without row reduction.
At the word \(11111\), the only compatible internal edge is
\(14=E_{11}\); at the word \(12201\), the only compatible internal edge is
\(13=E_{22}\).  A four-site cofactor needs two disjoint compatible edges,
so both coordinate functionals separately annihilate every insertion
column.  The only constant-word value of \(\beta_6\) is
\(\beta_6(11111)=1\), so its target is \(e_1\).  In the
\(C_2=(2,6,7)\) row \(111\), the two selected full words are precisely
\(11111111\) and \(v\).  A complete cut \(z=2\) therefore forces

\[
                         h_{11111111}+h_v=1.              \tag{22}
\]

Again (20)--(22) contradict \(h_{w_0}=h_{w_1}=0\).

## 6. Literal versus cumulative vanishing

There is a necessary logical distinction in interpreting “kill all three
mixed words in the repaired tensor.”  If only the three currently nonzero
words \(w_1,w_2,w_3\) are constrained, while the already killed word
\(w_0\) is allowed to return, the strengthening has an immediate exact
countermodel: append

\[
                         A_{67}\mathrel{+}=E_{12}.        \tag{23}
\]

This cancels the repaired cell \(-E_{12}^{67}\).  The source on \(23\)
then remains visible to internal cofactors but belongs to no supported full
matching.  Exact expansion gives

\[
 H_B=e_1^{\otimes8}+e_2^{\otimes8}+e_{w_0},              \tag{24}
\]

so \(h_{w_1}=h_{w_2}=h_{w_3}=0\), but \(h_{w_0}=1\).  All three complete
cuts \(z=2,3,4\) remain active, with defect dimensions \((1,1,2)\).

Thus merely replacing the old debt by its predecessor adds no strength.
The meaningful coupled system retains the old equation
\(h_{w_0}=0\) while imposing the three new equations.  Sections 4--5 prove
that this cumulative system cannot be realized by changing only one
boundary star.

## 7. Consequence for the route

The first viable escapes are now sharply localized.  Escaping the
no-fourth-cut theorem requires leaving the chosen one-star family—for
example by changing an internal block or changing both boundary stars—so
that the formerly impossible all-zero full coefficient can become nonzero.
It is not necessary for the all-zero internal coordinate to enter the
insertion space: a complete identity may instead force
\(h_{00000000}=1\) while \(\epsilon_{0,z}\) remains in \(K_{U_z}\).
A cumulative mixed-word repair likewise requires internal changes or
simultaneous changes on both boundary stars; arbitrary sources on either
single star are insufficient.  These are route constraints for the repaired
sparse family, not consequences for an arbitrary Krenn instance.
