# Higher splits: the \(p=28\) two-quartic \(q=5\) grid closure

## 1. Result and scope

Continue from the independently audited
[singleton-swap cap](live-three-zero-higher-split-p28-two-quartic-singleton-swap-q6-cap.md).
At \(p=h+k=28\), the two remaining \(d\leq2\) profiles have symbolic
tuples

\[
                    (e,a,b,u)=(2,7,0,1),(2,7,1,-1)              \tag{1}
\]

and moving-triple restored complement

\[
                              4^2 3^7 1.                         \tag{2}
\]

**Theorem 1.1 (two-quartic \(q=5\) grid closure).**  Neither tuple in
(1) can occur in the live-three-zero formal-selection setup.

The proof uses the full rectangular family of exact selections.  The
singleton-swap theorem says that each fixed-triple row of the rectangle
has at most one six-dimensional entry.  Pairwise transport of the
remaining five-dimensional entries produces a fixed cubic pencil.  An
all-five-dimensional singleton column then produces seven planes in a
four-space of degree-seven polynomials.  A characteristic-zero
classification of those seven planes forces the four-space to be

\[
                    (\alpha+\beta z)\mathbb C[z^2]_{\leq3},     \tag{3}
\]

which is incompatible with even one of the exact order-three rows at a
nonzero triple value.

This closes precisely the two \(4^2 3^7 1\) tuples in the \(p=28\),
\(d\leq2\) frontier.  It is not a closure of the unrestricted \(p=28\)
ledger and is not, by itself, the missing uniform all-even theorem.

## 2. The five-dimensional singleton grid

Let \(Y\) be the set of ordinary singleton values.  Its size is

\[
 |Y|=N=\begin{cases}h+1,&(2,7,0,1),\\ h-1,&(2,7,1,-1).
 \end{cases}                                                   \tag{4}
\]

Fix one of the seven exact-triple values \(i\).  Give that triple role
two, give the exact double role two in the second tuple, and leave the
ordinary singleton \(s\in Y\) complementary.  The relation complement is

\[
                          4^2 3^6 1_i1_s.                        \tag{5}
\]

Write \(q_{i,s}\) for the selected-row-kernel dimension.  The audited
singleton-swap theorem gives

\[
 q_{i,s}\in\{5,6\},\qquad
 \#\{s\in Y:q_{i,s}=6\}\leq1.                                \tag{6}
\]

When \(q_{i,s}=5\), the row-relation theorem gives a three-space

\[
             {\cal S}_{i,s}\subseteq\mathbb C[z]_{\leq6},
             \qquad \dim {\cal S}_{i,s}=3.                      \tag{7}
\]

Indeed, the relation dimension is \(q-2=3\), and (5) has ten value
classes, so the uniform target degree is \(10-4=6\).

## 3. Pairwise singleton transport gives a common pencil

Fix \(i\), and let \(s,t\in Y\) be two distinct choices with
\(q_{i,s}=q_{i,t}=5\).  Put

\[
              f_s=(z-s)^2(z+s),\qquad
              f_t=(z-t)^2(z+t).                                \tag{8}
\]

Distinctness and nonopposition make these cubics coprime, including when
one value is zero.  Exact moving-singleton transport, with the moving and
complementary indices in the correct order, gives

\[
 f_t{\cal S}_{i,s},\ f_s{\cal S}_{i,t}
       \subseteq {\cal K}_{i;s,t}\subseteq\mathbb C[z]_{\leq9}. \tag{9}
\]

The restored baseline is

\[
                         4^2 3^6 1_i1_s1_t.                     \tag{10}
\]

A hypothetical five-space in the common kernel would have forced
Wronskian weight

\[
       2(5-4)+6(5-3)+3(5-1)=26                         \tag{11}
\]

against the degree-nine cap \(5(10-5)=25\).  The standard exact-row gcd
correction is nonnegative.  Explicitly, if the common gcd has order
\(g\leq m\) at an exact order-\(m\) row, division lowers the cap by
\(5g\) and leaves weight \(\max(0,5-m+g)\), whose sum is at least
\(\max(0,5-m)\); if \(g>m\), the cap loss alone is larger.  Therefore

\[
                         \dim {\cal K}_{i;s,t}\leq4.             \tag{12}
\]

The two transported three-spaces in (9) consequently meet in dimension
at least two.  Coprimality gives the exact ambient intersection

\[
 f_t\mathbb C[z]_{\leq6}\cap f_s\mathbb C[z]_{\leq6}
                       =f_sf_t\mathbb C[z]_{\leq3}.              \tag{13}
\]

Define

\[
 {\cal U}_{i,s}:=\{u\in\mathbb C[z]_{\leq3}:f_su\in{\cal S}_{i,s}\}.
                                                                    \tag{14}
\]

Equations (9)--(13) say exactly that

\[
 f_t{\cal S}_{i,s}\cap f_s{\cal S}_{i,t}
       =f_sf_t({\cal U}_{i,s}\cap{\cal U}_{i,t}),
 \qquad
 \dim({\cal U}_{i,s}\cap{\cal U}_{i,t})\geq2.                  \tag{15}
\]

We next retain the exact local unit, since this is where a spurious
\(s\)-dependent Robin row could otherwise enter.  Put

\[
                       H_Y(z)=\prod_{y\in Y}(z+y).                \tag{16}
\]

For the selection with complementary singleton \(s\), its selected
singleton product is \(H_Y/(z+s)\).  At the other simple complementary
root \(i\), write
\(A_{i,s}=C_i(z)(z-i)(z-s)\), where \(C_i\) and the repeated-root gcd
are independent of \(s\).  The relation identity then has local unit

\[
 U_{i,s}(z)
   =V_i(z){H_Y(z)/(z+s)\over(z-s)^2}
   ={V_i(z)H_Y(z)\over f_s(z)},
 \qquad V_i(i)H_Y(i)\ne0,                                     \tag{17}
\]

where \(V_i\) is independent of \(s\).  This follows directly from
\(g/A^2\): the simple factor \(z-s\) occurs twice in \(A^2\), not in
\(g\), while the selected plus-pole factor omits precisely \(z+s\).
Thus, on \(S=f_su\), the exact simple row becomes

\[
                 (U_{i,s}S)'(i)=(V_iH_Yu)'(i)=0.                \tag{18}
\]

It is the **same** nonzero Robin functional on \(u\) for every \(s\).
Let its kernel in \(\mathbb C[z]_{\leq3}\) be the three-space
\({\cal H}_i\).  Then every \({\cal U}_{i,s}\) lies in \({\cal H}_i\).

A family of subspaces of a three-space, each of dimension at least two
and with pairwise intersections of dimension at least two, contains a
common plane.  Indeed, if one member is a plane, (15) puts that plane in
every member; if every member is the whole three-space, choose any plane.
We have therefore proved:

\[
 \boxed{\text{For each fixed }i\text{ there is a plane }{\cal L}_i
 \subseteq\mathbb C[z]_{\leq3}\text{ with }
 f_s{\cal L}_i\subseteq{\cal S}_{i,s}
 \text{ for every }q_{i,s}=5.}                                \tag{19}
\]

## 4. An all-\(q=5\) column gives seven degree-seven planes

There are at most seven \(q=6\) entries in the full seven-by-\(N\) grid.
Consequently at least \(N-7\), namely at least sixteen or fourteen,
singleton columns have all seven entries equal to five.  Fix one such
column \(s\).

For a triple value \(i\), put

\[
                         B_i=(z-i)^2(z+i)^2.                     \tag{20}
\]

The moving-triple transport into the restored baseline (2) gives

\[
                  B_i{\cal S}_{i,s}\subseteq
                  {\cal K}_s\subseteq\mathbb C[z]_{\leq10}.     \tag{21}
\]

By (19), every \(f_sB_i{\cal L}_i\) lies in \({\cal K}_s\).  Divide this
common factor only on their span.  The simple row at \(s\) becomes
automatic because \(f_s\) has a double zero there; at every repeated
node it is a local unit.  Hence

\[
 {\cal M}:=\operatorname {span}_{i=1}^7 B_i{\cal L}_i
       \subseteq {\cal J}_s\subseteq\mathbb C[z]_{\leq7},       \tag{22}
\]

where \({\cal J}_s\) obeys two exact order-four rows and seven exact
order-three rows.  A five-space in degree seven would have forced weight

\[
                       2(5-4)+7(5-3)=16                         \tag{23}
\]

against cap \(5(8-5)=15\).  Again the gcd correction cannot weaken the
inequality, by the same \(5g+\max(0,5-m+g)\) calculation used above, so

\[
                              \dim{\cal J}_s\leq4.               \tag{24}
\]

For distinct \(i,j\), a polynomial in both
\(B_i\mathbb C[z]_{\leq3}\) and
\(B_j\mathbb C[z]_{\leq3}\) would be divisible by the degree-eight
product \(B_iB_j\), yet have degree at most seven.  Thus those two
four-spaces meet only in zero.  The two planes
\(B_i{\cal L}_i\) and \(B_j{\cal L}_j\) already span a four-space.
Equations (22)--(24) force

\[
 \dim{\cal M}=4,
 \qquad
 \dim\bigl({\cal M}\cap B_i\mathbb C[z]_{\leq3}\bigr)\geq2
 \quad(1\leq i\leq7).                                        \tag{25}
\]

## 5. Classification of the seven planes

We use the following standalone characteristic-zero lemma.

**Lemma 5.1 (seven double-square planes).**  Let
\(a_1,\ldots,a_7\) be distinct scalars.  If a four-space
\({\cal M}\subseteq\mathbb C[z]_{\leq7}\) satisfies

\[
 \dim\left({\cal M}\cap
       (z^2-a_j)^2\mathbb C[z]_{\leq3}\right)\geq2
       \quad(1\leq j\leq7),                                  \tag{26}
\]

then for some nonzero affine polynomial \(\ell(z)=\alpha+\beta z\),

\[
                         {\cal M}=\ell(z)\mathbb C[z^2]_{\leq3}.\tag{27}
\]

*Proof.*  Put \(t=z^2\), \(R=\mathbb C[t]_{\leq3}\), and

\[
 E_a=(t-a)^2\mathbb C[t]_{\leq1}\subset R.                    \tag{28}
\]

The parity decomposition identifies \(\mathbb C[z]_{\leq7}\) with
\(R\oplus zR\), and the four-space in (26) with \(E_a\oplus zE_a\).
Let \(F\subseteq R\) be the even projection of \({\cal M}\), let
\(r=\dim F\), and let

\[
 K=\{q\in R:zq\in{\cal M}\},\qquad \dim K=4-r.               \tag{29}
\]

Projection of each intersection in (26) gives

\[
       \dim(F\cap E_a)+\dim(K\cap E_a)\geq2.                  \tag{30}
\]

If \(r=3\), every \(a_j\) must have either \(E_{a_j}\subset F\) or
\(K\subset E_{a_j}\).  The first event occurs for at most one value,
because \(E_a\cap E_b=0\) for \(a\ne b\); the second also occurs for at
most one, because a nonzero cubic cannot have two distinct double roots.
This excludes \(r=3\), and the symmetric argument excludes \(r=1\).

Suppose \(r=2\).  Apart from at most two values for which \(F=E_a\) or
\(K=E_a\), equation (30) requires \(F\cap E_a\ne0\).  For a basis of
\(F\), write its Pluecker coordinates as \(p_{uv}\), in coefficient
order \(1,t,t^2,t^3\).  Since

\[
 (t-a)^2=(a^2,-2a,1,0),\qquad
 t(t-a)^2=(0,a^2,-2a,1),                                    \tag{31}
\]

the incidence determinant is, up to a nonzero scalar,

\[
 \Delta_F(a)=p_{01}+2p_{02}a+(3p_{03}+p_{12})a^2
                    +2p_{13}a^3+p_{23}a^4.                    \tag{32}
\]

It is not identically zero.  Otherwise all coefficients in (32) would
vanish, and the Pluecker relation

\[
                  p_{01}p_{23}-p_{02}p_{13}+p_{03}p_{12}=0    \tag{33}
\]

would give \(-3p_{03}^2=0\), forcing every \(p_{uv}=0\).  Thus a fixed
plane meets at most four of the \(E_{a_j}\), whereas after the two
exceptions above it would have to meet at least five.  This excludes
\(r=2\).

If \(r=0\), then \({\cal M}=zR\), which is (27).  It remains to treat
\(r=4\).  The even projection is now an isomorphism, so

\[
                    {\cal M}=\{e(t)+zT(e)(t):e\in R\}           \tag{34}
\]

for an endomorphism \(T\) of \(R\).  Condition (26) says
\(T(E_{a_j})\subseteq E_{a_j}\).  Let

\[
 v_0(a)=(a^2,-2a,1,0)^T,\quad
 v_1(a)=(0,a^2,-2a,1)^T,                                    \tag{35}
\]

and let \(J(a)\) have rows
\((1,a,a^2,a^3)\) and \((0,1,2a,3a^2)\).  The four entries of

\[
                         J(a)Tv_0(a),\qquad J(a)Tv_1(a)         \tag{36}
\]

have degree at most five in \(a\).  They vanish at seven distinct
values, hence identically.  Coefficient comparison in the first pair
puts \(T\) in the form

\[
 T=\begin{pmatrix}
 \lambda&0&0&A\\ c&\lambda&0&B\\0&c&\lambda&C\\0&0&c&D
 \end{pmatrix}.                                               \tag{37}
\]

The second pair gives \(A=B=C=c=0\) and \(D=\lambda\).  Thus
\(T=\lambda I\), and (34) becomes
\({\cal M}=(1+\lambda z)R\).  This proves the lemma. \(\square\)

Structural nonopposition makes the seven squares \(a_i=i^2\) distinct,
so Lemma 5.1 applies to (25).

## 6. The exact triple row is impossible

We have obtained

\[
                     {\cal M}=\ell(z)\mathbb C[z^2]_{\leq3}    \tag{38}
\]

for a nonzero affine \(\ell\).  At most one of the seven distinct
nonzero triple values is a root of \(\ell\).  Choose \(i\) with
\(\ell(i)\ne0\).

After division by \(f_s\), the exact order-three row at \(i\) in
\({\cal J}_s\) has the form

\[
                         (G_iP)^{(3)}(i)=0,
                         \qquad G_i(i)\ne0.                     \tag{39}
\]

But the member

\[
                  P_i(z)=\ell(z)(z^2-i^2)^3\in{\cal M}         \tag{40}
\]

has exactly order three at \(z=i\).  Therefore

\[
 (G_iP_i)^{(3)}(i)
      =3!\,G_i(i)\ell(i)(2i)^3\ne0,                           \tag{41}
\]

contradicting (39).  This proves Theorem 1.1.

## 7. Exact audit

[verify_live_three_zero_higher_split_p28_two_quartic_q5_grid_closure.py](../computations/verify_live_three_zero_higher_split_p28_two_quartic_q5_grid_closure.py)
checks both formal ledgers at all six splits, every relation and degree
count, the two common-kernel one-unit gaps, the exact singleton-unit
cancellation, the Pluecker quartic and its nonidentity, the fifteen
independent graph constraints forcing a scalar endomorphism, and the
nonzero terminal order-three derivative.

The
[independent characteristic-zero audit](live-three-zero-higher-split-p28-two-quartic-q5-grid-closure-independent-audit.md)
reconstructs the moving/complementary indexing, the full \(g/A_s^2\) and
\(H_s\) cancellation including \(s=0\), every projection-rank branch of
Lemma 5.1, the scalar graph calculation, and the surviving exact
order-three coefficient after division by \(f_s\).  Its standalone
[checker](../computations/verify_live_three_zero_higher_split_p28_two_quartic_q5_grid_closure_independent_audit.py)
does not import the primary executable.
