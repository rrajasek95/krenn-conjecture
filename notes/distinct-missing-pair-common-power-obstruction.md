# Distinct missing pairs cannot be a six-site common power

## 1. Outcome

Let $U$ be a six-site set, let $P_0,P_1,P_2$ be three distinct
unordered pairs of sites, and let

\[
 F_i=\bigotimes_{u\in U\setminus P_i}e_i^{(u)}.
\]

Over a field of characteristic different from two, and in particular over
the complex numbers, there is no quadratic $q$ in the site-square-zero
algebra for which

\[
 q^{[2]}=\lambda _0F_0+\lambda _1F_1+\lambda _2F_2,
 \qquad q^{[3]}=0,\qquad \lambda _0\lambda _1\lambda _2\ne0.       \tag{1}
\]

The disjoint-pair and path-plus-disjoint-pair cases were already proved in
[`invertible-monomial-base-locus-common-power-obstruction.md`](invertible-monomial-base-locus-common-power-obstruction.md)
and independently checked in
[`invertible-monomial-base-locus-common-power-obstruction-independent-audit.md`](invertible-monomial-base-locus-common-power-obstruction-independent-audit.md).
This note closes the other three support graphs: $P_4$, $K_{1,3}$, and
$K_3$.  The arguments retain arbitrary endpoint-ordered tensor blocks;
no edge block is assumed to be a coordinate cell, decomposable, nonzero,
or generic.

The result is deliberately a power-only statement.  It does not use star
rows or any of the nine products from the coordinate-monomial cap model.
Distinctness is essential: the repeated-pair ternary $K_4$ construction
in the cited notes is an exact solution of the two common-power equations.

## 2. Setup and the five support graphs

Work in

\[
 \mathcal R_U=\bigotimes_{u\in U}(\mathbb F\oplus V_u),
 \qquad V_uV_u=0,
\]

and write $q_{uv}\in V_u\otimes V_v$ for the block on the unordered
edge $uv$.  Products are reordered into the named site order.  Matching
powers are unordered sums, so

\[
                         q q^{[2]}=3q^{[3]}.              \tag{2}
\]

Equation (1) therefore gives

\[
                  \sum_{i=0}^2\lambda_i q_{P_i}F_i=0.   \tag{3}
\]

For $i\ne j$, there is a site outside $P_i\cup P_j$.  At every such
site the two summands in (3) use the distinct coordinate lines
$\mathbb F e_i$ and $\mathbb F e_j$.  Their coordinate-word supports
are disjoint.  Since tensoring by a nonzero pure tensor is injective,

\[
                         q_{P_0}=q_{P_1}=q_{P_2}=0.       \tag{4}
\]

There are exactly five unlabeled simple graphs with three edges and no
repeated edge:

\[
 3K_2,\qquad P_3\sqcup K_2,\qquad P_4,\qquad K_{1,3},\qquad K_3. \tag{5}
\]

The first two are the previously audited cases.  Sections 3--5 treat the
last three.

We repeatedly use the following elementary crossing fact.  If nonzero
tensors on the four sides of a rectangle satisfy

\[
 X_{AE}Y_{BF}=-X_{AF}Y_{BE},                            \tag{6}
\]

then all four tensors have matrix rank one, their two factors at each
named space lie on fixed local lines, and (6) reduces to one scalar
relation.  This follows by flattening (6) first across
$(A\otimes E)|(B\otimes F)$ and then across
$(A\otimes F)|(B\otimes E)$.

## 3. The path $P_4$

Take

\[
 P_0=ab,\qquad P_1=bc,\qquad P_2=cd,
\]

and call the unused sites $e,f$.  Equation (4) first gives

\[
                         q_{ab}=q_{bc}=q_{cd}=0.          \tag{7}
\]

The zero four-site coefficients on $abcd,abce,abcf$ are respectively

\[
 q_{ac}q_{bd}=0,\qquad q_{ac}q_{be}=0,\qquad
 q_{ac}q_{bf}=0.                                        \tag{8}
\]

If $q_{ac}\ne0$, then all three blocks at the other factor in (8)
vanish, which kills the required nonzero coefficient on $abef$.
Consequently $q_{ac}=0$.  The zero coefficients on $bcde,bcdf$ now
give

\[
                         q_{bd}q_{ce}=q_{bd}q_{cf}=0.     \tag{9}
\]

If $q_{bd}\ne0$, these equations kill the required coefficient on
$cdef$, so $q_{bd}=0$.  Finally the zero coefficients on $acde,acdf$
give $q_{ad}q_{ce}=q_{ad}q_{cf}=0$; the same nonzero $cdef$ target
forces $q_{ad}=0$.  Thus every block internal to $\{a,b,c,d\}$
vanishes.

Put

\[
 E_x=q_{xe},\qquad G_x=q_{xf},\qquad
 [x,y]=E_xG_y+G_xE_y                                  \tag{10}
\]

for $x,y\in\{a,b,c,d\}$.  The remaining six equations are

\[
\begin{array}{lll}
 [a,b]=\lambda_2e_2^{\otimes4},&
 [a,d]=\lambda_1e_1^{\otimes4},&
 [c,d]=\lambda_0e_0^{\otimes4},\\
 [a,c]=0,&[b,c]=0,&[b,d]=0,
\end{array}                                             \tag{11}
\]

where each displayed pure tensor is on its four named sites.

Record at a row $x$ whether $E_x$ alone, $G_x$ alone, or both are
nonzero.  No row is empty because the three nonzero brackets in (11)
cover all four rows.  In a zero bracket, the two tensor products are
either both zero or both nonzero: exactly one nonzero tensor product
cannot sum to zero.  Among the three nonempty row states, this says that
a zero bracket can join only two equal states.  The zero-bracket graph

\[
                         a-c-b-d                         \tag{12}
\]

is connected, so all four states agree.  They cannot all be $E$-only
or all be $G$-only because the first line of (11) is nonzero.  Every one
of the eight blocks in (10) is therefore nonzero.

Apply the crossing fact (6) on the three edges of (12).  Connectivity
gives a common line $\mathbb F u\subset V_e$, a common line
$\mathbb F v\subset V_f$, and at each row a line
$\mathbb F r_x\subset V_x$, with

\[
 E_x\in\mathbb F^*(r_xu),\qquad
 G_x\in\mathbb F^*(r_xv).                               \tag{13}
\]

The nonzero bracket $[a,b]$ in (11) forces
$\mathbb F r_a=\mathbb F e_2^{(a)}$, whereas $[a,d]$ forces
$\mathbb F r_a=\mathbb F e_1^{(a)}$.  The coordinate lines are
distinct.  This excludes $P_4$.

## 4. The triangle $K_3$

Take

\[
 P_0=ab,\qquad P_1=bc,\qquad P_2=ca,
\]

and put $D=\{d,e,f\}$.  The three triangle blocks vanish by (4).  For
two triangle vertices $x,y$ and two distinct sites $u,v\in D$, the
four-set $xyuv$ is not a target support.  Its coefficient is

\[
                 q_{xu}q_{yv}+q_{xv}q_{yu}=0.           \tag{14}
\]

Let

\[
                         R_x=\{u\in D:q_{xu}\ne0\}.
\]

Each $R_x$ is nonempty because the target on $x\cup D$ is nonzero.
Equation (14) says, at the level of nonzero supports,

\[
 u\in R_x, v\in R_y
       \quad\Longleftrightarrow\quad
 v\in R_x, u\in R_y                                  \tag{15}
\]

for all distinct $u,v\in D$.  Two nonempty subsets of a three-set
satisfying (15) are equal: if $u\in R_x\setminus R_y$, choose
$v\in R_y$, and (15) gives the contradiction $u\in R_y$.  Hence

\[
                         R_a=R_b=R_c=:R.                 \tag{16}
\]

There are three cases.

* If $|R|=1$, every target on $x\cup D$ is the product of its sole
  spoke block and the same internal block on the other two sites of $D$.
  Nonzero purity forces that shared internal block to have color $1$,
  $2$, and $0$, respectively, at both endpoints.  This is impossible.

* If $|R|=3$, apply the crossing fact to (14) for any two rows.  All six
  blocks have fixed row and column factor lines, so after removing those
  factors (14) says
  
  \[
       r_{x,u}r_{y,v}+r_{x,v}r_{y,u}=0\qquad(u\ne v),    \tag{17}
  \]
  
  with every scalar nonzero.  The ratios
  $\rho_u=r_{x,u}/r_{y,u}$ obey
  $\rho_u=-\rho_v$ for all three pairs.  The first two relations make
  two ratios equal, while the third makes them negatives; this contradicts
  characteristic different from two.

* If $|R|=2$, the one crossing equation for each pair of rows again
  gives fixed factor lines.  Write the two nonzero scalar coefficients in
  row $x$ as $(r_x,s_x)$.  The three row pairs obey
  
  \[
                         r_xs_y+s_xr_y=0.                \tag{18}
  \]
  
  The orthogonal complement of a full-support vector $(r,s)$ for this
  hyperbolic form is the line spanned by $(r,-s)$.  The other two rows
  must both lie on that line, but its self-pairing is $-2rs\ne0$,
  contradicting their mutual equation in (18).

Thus $K_3$ is impossible.

## 5. The star $K_{1,3}$

Take

\[
 P_0=ab,\qquad P_1=ac,\qquad P_2=ad,
\]

with common centre $a$ and remaining sites $e,f$.  Set the $a$-site
to zero.  Equation (1) descends to the five-site algebra on
$b,c,d,e,f$, where

\[
 q^{[2]}=\lambda_0e_0^{(c)}e_0^{(d)}e_0^{(e)}e_0^{(f)}
         +\lambda_1e_1^{(b)}e_1^{(d)}e_1^{(e)}e_1^{(f)}
         +\lambda_2e_2^{(b)}e_2^{(c)}e_2^{(e)}e_2^{(f)}. \tag{19}
\]

For each \(x\in\{b,c,d\}\), choose a covector
\(\ell_x:V_x\to\mathbb F\) which takes the value one on all three
coordinate axes, and use the local algebra homomorphism

\[
 \mathbb F\oplus V_x\longrightarrow
 \mathbb F\oplus\mathbb F\varepsilon_x,\qquad
 v\longmapsto\ell_x(v)\varepsilon_x,\qquad
 \varepsilon_x^2=0.
\]

Tensor these maps with the identity at \(e,f\).  This retains one
square-zero generator at each contracted site; it does not evaluate a
nilpotent vector as a ground-field scalar.  Matching powers commute with
the homomorphism, so a solution above would give one below.  Suppress the
fixed generators \(\varepsilon_b,\varepsilon_c,\varepsilon_d\) in the
coefficient notation.
Write

\[
\begin{array}{lll}
 A=q_{cd},&B=q_{bd},&C=q_{bc},\\
 X_x=q_{xe}\in V_e,&Y_x=q_{xf}\in V_f&(x=b,c,d),\\
 H=q_{ef}\in V_e\otimes V_f,
\end{array}                                             \tag{20}
\]

where $A,B,C$ are now scalars.  Put
$D_i=e_i^{(e)}\otimes e_i^{(f)}$.  Literal matching expansion gives two
vector equations

\[
 CX_d+BX_c+AX_b=0,\qquad
 CY_d+BY_c+AY_b=0,                                      \tag{21}
\]

and three matrix equations

\[
\begin{aligned}
 AH+X_cY_d+X_dY_c&=\lambda_0D_0,\\
 BH+X_bY_d+X_dY_b&=\lambda_1D_1,\\
 CH+X_bY_c+X_cY_b&=\lambda_2D_2.                        \tag{22}
\end{aligned}
\]

These equations have no solution.  First suppose $A,B,C\ne0$.  Eliminate
$X_b,Y_b$ from (21), put
$M=X_cY_d+X_dY_c$, and use the first equation in (22) to eliminate
$H$.  The other two equations become

\[
\begin{aligned}
 2(BM+C X_dY_d)&=B\lambda_0D_0-A\lambda_1D_1,\\
 2(CM+B X_cY_c)&=C\lambda_0D_0-A\lambda_2D_2.           \tag{23}
\end{aligned}
\]

The first right side has rank two, with column and row spaces
$\langle e_0,e_1\rangle$.  Its left side has column space contained in
$\langle X_c,X_d\rangle$ and row space contained in
$\langle Y_c,Y_d\rangle$; both spans must therefore equal the indicated
coordinate plane.  The second line of (23) instead forces the same spans
to equal $\langle e_0,e_2\rangle$, a contradiction.

Next suppose exactly one triangle scalar vanishes, say $A=0$, while
$B,C\ne0$.  Equations (21) make

\[
 X_d=-(B/C)X_c,\qquad Y_d=-(B/C)Y_c.                   \tag{24}
\]

The first equation of (22) is nonzero pure, so $X_c,Y_c$ lie on the
two color-zero coordinate lines.  Put
$N=X_bY_c+X_cY_b$.  The last two equations in (22) give

\[
 {2B\over C}N={B\over C}\lambda_2D_2-\lambda_1D_1.     \tag{25}
\]

Quotient both $V_e,V_f$ by their color-zero lines.  The left side dies,
whereas the right side remains a nonzero rank-two diagonal matrix.  This
is impossible.  The other choices of the vanishing scalar are symmetric.

If at least two, but not all three, of $A,B,C$ vanish, (21) kills the
two vectors needed by one of the nonzero targets in (22).  For example,
$B=C=0,A\ne0$ gives $X_b=Y_b=0$, making both the second and third
left sides of (22) zero.  The other cases are symmetric.

It remains that $A=B=C=0$.  Then (22) says

\[
 X_cY_d+X_dY_c=\lambda_0D_0,\qquad
 X_bY_d+X_dY_b=\lambda_1D_1,\qquad
 X_bY_c+X_cY_b=\lambda_2D_2.                            \tag{26}
\]

No row $x$ can have only $X_x\ne0$: its two incident nonzero matrices
would then have the same column line, although their target coordinate
lines differ.  Likewise no row can have only $Y_x\ne0$, and no row can
be empty.  Thus all six vectors are nonzero.

A sum $x\otimes y'+x'\otimes y$ of two nonzero simple matrices can have
rank one only if $x,x'$ are proportional or $y,y'$ are proportional.
Apply this to each edge of the triangle in (26), marking the edge $X$
or $Y$ according to one such proportional pair.  Two of the three edges
receive the same mark and share a vertex.  Proportionality then makes their
two target column lines, or their two target row lines, equal.  Those
targets have different coordinate colors, a final contradiction.

This excludes $K_{1,3}$.

## 6. Consequence and exact scope

The five graph types in (5) are exhaustive.  Combining Sections 3--5 with
the two previously audited cases proves the theorem in Section 1: three
distinct monomial four-site lifts can never be the second matching power
of one six-site quadratic whose third matching power vanishes.

The theorem does not exclude repeated missing pairs; the exact repeated
$K_4$ model shows that such a statement would be false.  It also makes
no assertion about a common multiplier whose four-site components are
sums of several target tensors, or about non-monomial star rows.  Those
are separate global-descent problems.

The exact companion checker is
[`verify_distinct_missing_pair_common_power_obstruction.py`](../computations/verify_distinct_missing_pair_common_power_obstruction.py).
