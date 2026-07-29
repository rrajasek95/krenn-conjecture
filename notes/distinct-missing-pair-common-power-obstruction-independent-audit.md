# Independent audit of the distinct-missing-pair common-power obstruction

## 1. Verdict

This is a clean-room, line-by-line audit of
[the primary note](distinct-missing-pair-common-power-obstruction.md).
The theorem and all three new graph cases are correct over a field of
characteristic different from two. In particular, the arguments allow
arbitrary endpoint tensors: no block is silently assumed decomposable,
nonzero, or coordinate-valued before an equation proves that fact.

I found no countermodel and no substantive gap. There is one point worth
making explicit when reading the star proof: contraction at \(b,c,d\) is
an algebra map to a **one-dimensional square-zero local factor** at each
site. It is not evaluation of a nilpotent local vector as a scalar in the
ground field. With the square-zero generators retained and then suppressed
from notation, equations (21)--(22) of the primary note are exactly the
projected matching equations.

The standalone
[independent checker](../computations/audit_distinct_missing_pair_common_power_obstruction_independent.py)
imports no project code and does not import the primary checker. It
independently verifies the five-graph census, colour-word separation, all
Boolean support propagations, odd-characteristic scalar checks, and formal
syzygies behind the star elimination. Those finite checks are bookkeeping
audits; the arbitrary-tensor proof is reconstructed below.

## 2. Common first step and the five graphs

Let

\[
 \mathcal R_U=\bigotimes_{u\in U}(\mathbb F\oplus V_u),
 \qquad V_uV_u=0,
\]

and let \(q_{uv}\in V_u\otimes V_v\) denote the block on edge \(uv\).
The unordered matching powers satisfy

\[
                         q q^{[2]}=3q^{[3]}.             \tag{A1}
\]

Indeed, a fixed three-edge matching occurs once for each choice of its
distinguished edge. Therefore \(q^{[3]}=0\) and the asserted formula for
\(q^{[2]}\) imply

\[
                 \sum_{i=0}^2\lambda_i q_{P_i}F_i=0.   \tag{A2}
\]

Only \(q_{P_i}\) can multiply \(F_i\) without repeating a site. For two
distinct two-subsets \(P_i,P_j\subset U\), their union has at most four
sites, so there is a site outside it. At that site \(q_{P_i}F_i\) has
fixed colour \(i\), while \(q_{P_j}F_j\) has fixed colour \(j\). Thus the
three full-support word spaces are pairwise disjoint. Since every
\(\lambda_iF_i\) is nonzero and tensoring with a nonzero tensor is
injective,

\[
                         q_{P_0}=q_{P_1}=q_{P_2}=0.      \tag{A3}
\]

This inference does not divide by \(3\), so it is valid even in
characteristic three. The later triangle and star contradictions are
where characteristic two is excluded.

A simple graph of three distinct edges has precisely one of the following
non-isolated component-degree signatures:

\[
\begin{array}{c|c|c}
\text{type}&\text{component degree sequences}&\text{labelled count on six sites}\\ \hline
3K_2&(1,1),(1,1),(1,1)&15\\
P_3\sqcup K_2&(1,1,2),(1,1)&180\\
P_4&(1,1,2,2)&180\\
K_{1,3}&(1,1,1,3)&60\\
K_3&(2,2,2)&20
\end{array}
\]

The counts total \(\binom{15}{3}=455\). The already audited result cited
by the primary note proves the \(3K_2\) case directly and proves the
\(P_3\sqcup K_2\) coefficient obstruction without using the nine-product
table. Thus it is legitimate to reuse both as power-only statements.

## 3. Reconstruction of the \(P_4\) argument

Put

\[
 P_0=ab,\qquad P_1=bc,\qquad P_2=cd,
\]

with unused sites \(e,f\). Equation (A3) gives
\(q_{ab}=q_{bc}=q_{cd}=0\). The complete matching coefficients used to
kill the other three internal blocks are as follows:

\[
\begin{array}{c|c|c}
\text{support}&\text{coefficient after known zeros}&\text{consequence}\\ \hline
abcd&q_{ac}q_{bd}&q_{ac}q_{bd}=0\\
abce&q_{ac}q_{be}&q_{ac}q_{be}=0\\
abcf&q_{ac}q_{bf}&q_{ac}q_{bf}=0
\end{array}
\]

If \(q_{ac}\ne0\), tensor-product injectivity kills
\(q_{bd},q_{be},q_{bf}\), and every matching on the required support
\(abef\) then has a zero factor. Hence \(q_{ac}=0\). Next the zero
coefficients on \(bcde,bcdf\) reduce to
\(q_{bd}q_{ce}=q_{bd}q_{cf}=0\). If \(q_{bd}\ne0\), these zeros kill the
required \(cdef\) coefficient, so \(q_{bd}=0\). Finally \(acde,acdf\)
reduce to \(q_{ad}q_{ce}=q_{ad}q_{cf}=0\), and the same \(cdef\) target
forces \(q_{ad}=0\). All six blocks internal to \(abcd\) are therefore
zero. No step infers termwise vanishing from a multi-term cancellation.

Write

\[
 E_x=q_{xe},\qquad G_x=q_{xf},\qquad
 [x,y]=E_xG_y+G_xE_y.
\]

The three targets and three nontargets give

\[
 [a,b]\ne0,\quad [a,d]\ne0,\quad [c,d]\ne0,
 \qquad [a,c]=[b,c]=[b,d]=0.                            \tag{A4}
\]

Every row \(x\) has at least one of \(E_x,G_x\) nonzero because the
nonzero brackets cover all four rows. In a zero bracket, either both
crossed tensor products vanish or both are nonzero: exactly one nonzero
tensor cannot sum to zero. For nonempty row states

\[
 E\text{-only},\qquad G\text{-only},\qquad\text{both},
\]

the equality of those two Boolean product indicators holds exactly when
the endpoint states agree. The zero-bracket graph \(a-c-b-d\) is
connected, so every row has the same state. A target bracket rules out
either one-sided state, and consequently all eight spoke blocks are
nonzero.

On every zero-bracket edge,

\[
                         E_xG_y=-G_xE_y.                 \tag{A5}
\]

Flattening (A5) first as
\((V_x\otimes V_e)|(V_y\otimes V_f)\) and then as
\((V_x\otimes V_f)|(V_y\otimes V_e)\) proves that all four blocks are
rank-one tensors and identifies their factor lines at each named site.
Because the three zero edges form a connected path, decomposable-tensor
uniqueness propagates a single line at \(e\), a single line at \(f\), and
a line \(r_x\subset V_x\) for each row:

\[
 E_x\in\mathbb F^*(r_xu),\qquad
 G_x\in\mathbb F^*(r_xv).                              \tag{A6}
\]

The nonzero target \([a,b]\) makes \(r_a\) the colour-two coordinate line,
whereas \([a,d]\) makes the same \(r_a\) the colour-one coordinate line.
Those lines are distinct, giving the claimed contradiction. Possible
scalar cancellation in a target bracket causes no issue: the target is
nonzero, so its total scalar is nonzero and its local factor lines are
still those in (A6).

## 4. Reconstruction of the \(K_3\) argument

Take \(P_0=ab,P_1=bc,P_2=ca\) and \(D=\{d,e,f\}\). The triangle blocks
vanish by (A3). For distinct triangle vertices \(x,y\) and distinct
\(u,v\in D\), the nontarget support \(xyuv\) gives exactly

\[
                 q_{xu}q_{yv}+q_{xv}q_{yu}=0.           \tag{A7}
\]

Set \(R_x=\{u:q_{xu}\ne0\}\). Each \(R_x\) is nonempty: every target
\(x\cup D\) needs a matching containing a spoke from \(x\). Since a
product on disjoint sites is nonzero precisely when both factors are,
(A7) gives

\[
 (u\in R_x\ \&\ v\in R_y)
 \Longleftrightarrow
 (v\in R_x\ \&\ u\in R_y).                             \tag{A8}
\]

If \(u\in R_x\setminus R_y\), choose \(v\in R_y\); then \(v\ne u\), and
the left side of (A8) is true while its right side is false. Interchanging
\(x,y\) proves equality. Thus \(R_a=R_b=R_c=:R\).

All three cardinalities are genuinely covered:

* If \(|R|=1\), say \(R=\{d\}\), the target on \(xdef\) is the product
  \(q_{xd}q_{ef}\). Equality to a nonzero pure coordinate tensor forces
  the shared block \(q_{ef}\) to have colour \(0\), colour \(1\), and
  colour \(2\) at each endpoint as \(x\) ranges over the three triangle
  vertices. This is impossible.

* If \(|R|=3\), every tensor in (A7) is nonzero. Repeated use of the two
  flattenings from (A5), followed through the connected \(3\times3\)
  incidence array, gives fixed row and column factor lines. After removing
  those factors, two rows \(x,y\) have nonzero scalar entries
  \(r_{x,u},r_{y,u}\) satisfying

  \[
   r_{x,u}r_{y,v}+r_{x,v}r_{y,u}=0\quad(u\ne v).
  \]

  The nonzero ratios \(\rho_u=r_{x,u}/r_{y,u}\) obey
  \(\rho_u=-\rho_v\) for all three pairs. From the pairs \(de,df\) one
  gets \(\rho_e=\rho_f\), while the pair \(ef\) gives
  \(\rho_e=-\rho_f\). Hence \(2\rho_e=0\), contrary to
  \({\rm char}(\mathbb F)\ne2\).

* If \(|R|=2\), the sole crossing equation for each row pair again fixes
  all relevant local lines. Write a row's two nonzero scalar entries as
  \(v_x=(r_x,s_x)\). Every pair is orthogonal for
  \(B((r,s),(r',s'))=rs'+sr'\). For fixed full-support \(v_x\), its
  orthogonal complement is the line through \((r_x,-s_x)\). The other
  two nonzero rows lie on that line, but its self-pairing is
  \(-2r_xs_x\ne0\). They therefore cannot be mutually orthogonal.

This exhausts \(K_3\), including every zero pattern of its spoke blocks.

## 5. Validity of the star quotient and its equations

Let \(P_0=ab,P_1=ac,P_2=ad\). First quotient the \(a\)-site to zero.
For each \(x\in\{b,c,d\}\), choose a covector
\(\ell_x:V_x\to\mathbb F\) satisfying
\(\ell_x(e_0)=\ell_x(e_1)=\ell_x(e_2)=1\), and define the local algebra map

\[
 \mathbb F\oplus V_x\longrightarrow
 \mathbb F\oplus\mathbb F\varepsilon_x,
 \qquad v\longmapsto\ell_x(v)\varepsilon_x,
 \qquad\varepsilon_x^2=0.                              \tag{A9}
\]

Tensor these maps with the identity at \(e,f\). Matching powers commute
with this algebra homomorphism. Thus an original solution would give a
solution of the projected equations; proving that the projected equations
are inconsistent is a valid obstruction. Suppress the fixed generators
\(\varepsilon_b,\varepsilon_c,\varepsilon_d\) from now on.

With

\[
 A=q_{cd},\quad B=q_{bd},\quad C=q_{bc},\quad
 X_x=q_{xe},\quad Y_x=q_{xf},\quad H=q_{ef},
\]

the two nontarget supports \(bcde,bcdf\) give

\[
 CX_d+BX_c+AX_b=0,\qquad
 CY_d+BY_c+AY_b=0.                                     \tag{A10}
\]

The only three target supports are \(cdef,bdef,bcef\), and their three
perfect matchings give, literally,

\[
\begin{aligned}
 AH+X_cY_d+X_dY_c&=\lambda_0D_0,\\
 BH+X_bY_d+X_dY_b&=\lambda_1D_1,\\
 CH+X_bY_c+X_cY_b&=\lambda_2D_2,
\end{aligned}                                          \tag{A11}
\]

where \(D_i=e_i^{(e)}\otimes e_i^{(f)}\). These five supports exhaust all
four-subsets of the five surviving sites. The third matching power there
is automatically zero because only five sites remain, so no projected
condition has been omitted.

## 6. Every star scalar branch

Put \(M=X_cY_d+X_dY_c\).

### 6.1 All of \(A,B,C\) are nonzero

Eliminate \(X_b,Y_b\) with (A10). Rather than trust a division-based
calculation, the two identities in the primary note have the following
cleared-denominator syzygy certificates. If \(T_i\) denotes the left side
of the \(i\)-th equation in (A11), and \(L_X,L_Y\) the two left sides in
(A10), then

\[
\begin{aligned}
 BT_0-AT_1-2(BM+CX_dY_d)&=-L_XY_d-X_dL_Y,\\
 CT_0-AT_2-2(CM+BX_cY_c)&=-L_XY_c-X_cL_Y.               \tag{A12}
\end{aligned}
\]

Thus (A10)--(A11) imply exactly

\[
\begin{aligned}
2(BM+CX_dY_d)&=B\lambda_0D_0-A\lambda_1D_1,\\
2(CM+BX_cY_c)&=C\lambda_0D_0-A\lambda_2D_2.             \tag{A13}
\end{aligned}
\]

The first right side has rank two, with column plane
\(\langle e_0,e_1\rangle\), whereas its left side has column space inside
\(\langle X_c,X_d\rangle\), whose dimension is at most two. Hence those
planes are equal. The second equation makes the same span equal
\(\langle e_0,e_2\rangle\). The coordinate planes are distinct. This
contradiction uses \(2\ne0\); the identical row-space argument is available
but not needed.

### 6.2 Exactly one of \(A,B,C\) is zero

By simultaneous permutation of \(b,c,d\) and the three target equations,
it suffices to take \(A=0\), \(B,C\ne0\). Equation (A10) gives

\[
 X_d=-(B/C)X_c,\qquad Y_d=-(B/C)Y_c.                   \tag{A14}
\]

The first target equation is therefore

\[
             -2(B/C)X_cY_c=\lambda_0D_0.               \tag{A15}
\]

All displayed scalars are nonzero, so \(X_c,Y_c\) lie respectively on the
colour-zero coordinate lines. Set \(N=X_bY_c+X_cY_b\). A second exact
syzygy, before division, is

\[
 BT_2-CT_1-2BN
   =-X_b(BY_c+CY_d)-(BX_c+CX_d)Y_b.                    \tag{A16}
\]

It yields

\[
 {2B\over C}N={B\over C}\lambda_2D_2-\lambda_1D_1.     \tag{A17}
\]

Quotient \(V_e,V_f\) by their colour-zero lines. Each summand of \(N\)
dies, one through its row factor and one through its column factor. The
right side survives as a rank-two diagonal tensor on the independent
colour-one and colour-two lines. Contradiction. The simultaneous
permutation noted above covers the other two choices of zero scalar.

### 6.3 Exactly two of \(A,B,C\) are zero

For example, \(B=C=0,A\ne0\) makes (A10) force
\(X_b=Y_b=0\). The second and third target equations then have zero left
sides and nonzero right sides. Relabeling covers all three patterns. This
uses no division and also shows that the phrase "at least two, but not all"
in the primary note contains no hidden scalar branch.

### 6.4 All of \(A,B,C\) are zero

The three target equations become

\[
 X_cY_d+X_dY_c=\lambda_0D_0,
 \quad X_bY_d+X_dY_b=\lambda_1D_1,
 \quad X_bY_c+X_cY_b=\lambda_2D_2.                     \tag{A18}
\]

No row \((X_x,Y_x)\) is empty. If it were \(X\)-only, its two incident
nonzero matrices would both have column line \(\mathbb F X_x\), although
their diagonal targets have two different coordinate column lines. The
\(Y\)-only case is the row-space analogue. Hence all six vectors are
nonzero.

For nonzero \(x,x',y,y'\), a matrix
\(x\otimes y'+x'\otimes y\) can have rank one only if \(x,x'\) are
proportional or \(y,y'\) are proportional. Otherwise its restriction
between the two-dimensional spans has rank two. Mark each edge of the
triangle in (A18) by one available dependence, \(X\) or \(Y\). Two of
three edges share the same mark, and every two triangle edges meet. Two
incident \(X\)-marked edges force their distinct diagonal targets to have
the same column line; two incident \(Y\)-marked edges force the same false
equality of row lines. This contradiction remains valid if an edge admits
both marks: choose either mark and apply the same pigeonhole argument.

The four cases above exhaust all \(2^3\) zero/nonzero patterns of
\((A,B,C)\).

## 7. Characteristic and exact scope

The \(P_4\) proof works in every characteristic. The \(K_3\) cases
\(|R|=2,3\) and the star branches (A13), (A15), and (A17) use
\(2\ne0\), exactly matching the theorem's hypothesis. No proof step needs
positivity, algebraic closure, or a normalized target weight; it uses only
\(\lambda_0\lambda_1\lambda_2\ne0\) and independence of the three
coordinate axes.

Combining these three cases with the previously audited \(3K_2\) and
\(P_3\sqcup K_2\) cases proves the stated result for every triple of
distinct missing pairs. The theorem remains deliberately limited to
three single coordinate-monomial four-site targets. It neither handles
repeated missing pairs nor a four-site component that is itself a sum of
several target tensors, so it is not by itself the missing global descent
for route U1.
