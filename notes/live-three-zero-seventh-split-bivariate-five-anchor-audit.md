# Independent audit of the seventh-split bivariate five-anchor closure

## 1. Outcome

The bivariate five-anchor argument is valid.  This independent audit checks
the bidegree and interpolation threshold, both endpoint reductions including
all extracted factors and signs, the signed quartet-certificate subtraction,
the nonzero cubic selection polynomial, and the zero-safe extension to a
collision profile with at least seventeen distinct value classes and a
selected double-class anchor whose mate remains a singleton row class.

No unproved DR4 rigidity statement is used.  Only the proved linear quartet
certificate from
[live-three-zero-sixth-split-distinct-closure.md](live-three-zero-sixth-split-distinct-closure.md)
is invoked.

## 2. The cleared bivariate determinant

Use nodal coordinates \(t_i=-s_i\) for five fixed, distinct, nonzero anchor
values \(F\).  The moving variables \(x,y\) remain in the exceptional-beta
coordinate used in the sixth-split nodal row.  Put

\[
                         D_i(z)=z^2-t_i^2.                   \tag{1}
\]

After the two moving contributions are separated from the fixed translation
\(U_i(F)\), the cleared Robin row on a quartic \(q\) is

\[
\begin{split}
 \mathcal R_i(x,y)q={}&D_i(x)D_i(y)
       \bigl(q'(t_i)+U_i(F)q(t_i)\bigr)\\
 &-(x-3t_i)D_i(y)q(t_i)
  -(y-3t_i)D_i(x)q(t_i).                                   \tag{2}
\end{split}
\]

This follows from

\[
 \psi(-t_i,z)=-{z-3t_i\over z^2-t_i^2}.                    \tag{3}
\]

Every coefficient of the row (2) has degree at most two in \(x\) and at
most two in \(y\).  Therefore the determinant of the five rows on the five
quartic coefficients is a polynomial

\[
                         P_F(x,y),\qquad
 \deg_xP_F\le10,\quad\deg_yP_F\le10.                         \tag{4}
\]

The checker constructs (2) on the ascending quartic basis and verifies these
bidegrees directly.  It also expands a complete specialized \(5\times5\)
determinant as an independent implementation check.

## 3. Off-diagonal grid interpolation

Let \(A\) be the set of distinct exceptional values outside \(F\), and put
\(M=|A|\).  In the all-distinct stratum there are \(p+9\) exceptional
values, so

\[
                         M=p+4\ge12                           \tag{5}
\]

because seventh-split feasibility gives \(p\ge8\).

For distinct \(x,y\in A\), the seven selected columns
\(R=F\cup\{x,y\}\) represent seven value classes.  The Hermite reduction
gives a nonzero quartic residual, and its five fixed-anchor equations force

\[
                             P_F(x,y)=0.                      \tag{6}
\]

No row-clearing factor vanishes on this grid.  A moving value differs from
every anchor, its negative is excluded by the structural pair-sum condition,
and a possible moving value zero is harmless because every fixed anchor is
nonzero.

Fix \(y\in A\).  As a polynomial in \(x\), \(P_F(x,y)\) has the
\(M-1\ge11\) roots \(A\setminus\{y\}\), strictly more than its degree ten.
Thus it is zero for every \(x\).  Repeating in \(y\), or applying this to
the coefficient polynomials in \(x\), gives

\[
                              \boxed{P_F\equiv0}.             \tag{7}
\]

The strict cardinality is essential.  The checker constructs, on an
eleven-point grid, the Lagrange diagonal kernel

\[
                         K(x,y)=\sum_{v\in A}L_v(x)L_v(y),    \tag{8}
\]

which has bidegree \((10,10)\), vanishes at every off-diagonal grid point,
and equals one on the diagonal.  Hence eleven values would not justify
(7); twelve do.

## 4. Endpoint factor extraction

Fix \(a\in F\).  At the two symbolic endpoints of the \(y\)-variable, the
\(a\)-row of (2) is

\[
\begin{array}{c|c}
y=t_a&2t_aD_a(x)q(t_a),\\
y=-t_a&4t_aD_a(x)q(t_a).
\end{array}                                                   \tag{9}
\]

Both coefficients have the displayed positive sign.  They are nonzero
polynomials because \(t_a\ne0\).  Restrict the remaining rows to

\[
                             q(z)=(z-t_a)r(z),qquad\deg r\le3. \tag{10}
\]

For \(j\ne a\), exact substitution into (2) gives

\[
\begin{split}
 \mathcal R_j(x,t_a)((z-t_a)r)
  ={}&(t_j-t_a)(t_a^2-t_j^2)\\
 &\quad\cdot\left[D_j(x)\bigl(r'(t_j)+V_{aj}^+r(t_j)\bigr)
              -(x-3t_j)r(t_j)\right],\\
 V_{aj}^+={}&U_j(F)-{2\over t_a+t_j}.
\end{split}                                                   \tag{11}
\]

and

\[
\begin{split}
 \mathcal R_j(x,-t_a)((z-t_a)r)
  ={}&(t_j-t_a)(t_a^2-t_j^2)\\
 &\quad\cdot\left[D_j(x)\bigl(r'(t_j)+V_{aj}^-r(t_j)\bigr)
              -(x-3t_j)r(t_j)\right],\\
 V_{aj}^-={}&U_j(F)-{1\over t_a+t_j}-{1\over t_j-t_a}.
\end{split}                                                   \tag{12}
\]

The common factor in (11)--(12) is nonzero: the nodes are distinct and no
pair sum vanishes.  Expanding the determinant after the basis split (10),
(9)--(12) show that \(P_F(x,\pm t_a)\) is a nonzero scalar and a nonzero
factor \(D_a(x)\) times the corresponding four-anchor DR4 determinant.
Since (7) holds in the polynomial ring, both four-anchor determinants are
identically zero in \(x\).

## 5. Signed quartet subtraction

Let \(J=F\setminus\{a\}\).  For translations \(V_j\) on this quartet,
write the proved linear certificate as

\[
 \mathcal K_J(V)=
 \sum_{j\in J}V_j\prod_{\ell\in J\setminus\{j\}}(t_j+t_\ell). \tag{13}
\]

Equations (11)--(12) and the quartet certificate give

\[
                         \mathcal K_J(V^+)=
                         \mathcal K_J(V^-)=0.                \tag{14}
\]

The translations cancel on subtraction, and the sign is

\[
 V_{aj}^+-V_{aj}^-
 =-{1\over t_a+t_j}+{1\over t_j-t_a}
 ={2t_a\over t_j^2-t_a^2}.                                 \tag{15}
\]

Consequently (14) forces

\[
 \boxed{
 S_a(F):=2t_a\sum_{j\in F\setminus\{a\}}
 {\displaystyle\prod_{\ell\in F\setminus\{a,j\}}(t_j+t_\ell)
  \over t_j^2-t_a^2}=0.}                                   \tag{16}
\]

The checker constructs both quartet functionals from (11)--(12) and verifies
their difference equals the right side of (16) exactly.  In particular, the
factor is \(+2t_a\), not its negative.

## 6. The four-core selection polynomial

Fix four nonzero nodes

\[
                              Q=\{a,b,c,d\}                  \tag{17}
\]

and let \(e\) be a prospective fifth node.  Define

\[
                         H_a(e)=(e^2-a^2)S_a(Q\cup\{e\}).    \tag{18}
\]

For the three summands of (16) indexed by \(b,c,d\), multiplication by
\(e^2-a^2\) leaves a factor linear in \(e\); the summand indexed by \(e\)
becomes the product of three linear factors.  Hence

\[
                              \deg_eH_a\le3.                 \tag{19}
\]

At the two cleared endpoints, all terms except the moving-\(e\) term vanish:

\[
\begin{split}
 H_a(a)&=2a(a+b)(a+c)(a+d),\\
 H_a(-a)&=2a(b-a)(c-a)(d-a).                                \tag{20}
\end{split}
\]

Both are nonzero under the structural assumptions.  In particular,

\[
                 \boxed{H_a(a)=2a\prod_{q\in Q\setminus\{a\}}(a+q)\ne0,} \tag{21}
\]

so \(H_a\) is not the zero polynomial.

There are at most one zero exceptional value and at least seventeen distinct
values.  Choose \(Q\) nonzero.  Even in the worst case, after excluding its
four nodes and the unique possible zero there are at least

\[
                              17-4-1=12                      \tag{22}
\]

nonzero candidates for \(e\).  Every candidate is different from \(\pm a\),
so (18) and (16) would make it a root of \(H_a\).  A nonzero cubic cannot
have twelve roots.  This contradicts the assumption that all isolated-star
pivots vanish.

## 7. Collision extension and zero audit

The same proof applies when the exceptional multiset has at least seventeen
distinct value classes and one selected fixed anchor \(a\) belongs to a
double class.  Selecting one of its two labels in every
\(R=F\cup\{x,y\}\) leaves its mate as a singleton class in every complement
\(N_{x,y}\).  This is the precise meaning here of a repeated class being
retained as a singleton.  It supplies the hypothesis of the simultaneous
Hermite singleton-row lemma uniformly across the off-diagonal grid.

The seven selected labels still have seven distinct values, so the residual
degree is four and (2) applies.  Other fixed or moving classes may themselves
be repeated; selecting one label changes their anchor translation but not the
uniform moving term (3).  The fixed double value \(a\) is necessarily
nonzero, because a repeated zero violates the structural pair-sum condition.

The remaining zero bookkeeping is exact:

- choose the four-core and fifth fixed anchor among nonzero classes;
- in the worst case there are still twelve choices for the fifth anchor;
- after fixing five anchors there are twelve moving value classes;
- if the unique zero class exists, it lies in that moving pool and is not a
  pole of any cleared row;
- an off-diagonal pair uses it at most once, while the unselected mate of
  \(a\) remains a singleton regardless.

Thus every profile with at least seventeen distinct value classes and such a
retained double-class singleton is closed by the same contradiction.

## 8. Exact post-closure residual census

The triple-containing residuals from the collision-frontier census have
fewer than seventeen distinct value classes, so this new closure does not
alter them:

\[
\begin{array}{c|l}
p&(q,d,s)\\ \hline
8&(3,4,0),(3,3,2),(3,2,4),(3,1,6),(2,5,1),(2,3,5)\\
9&(6,0,0),(3,4,1),(3,2,5)\\
12&(7,0,0).
\end{array}                                                   \tag{23}
\]

For a double/single profile \((2^d,1^s)\), the number of distinct value
classes is

\[
                         d+s=p+9-d.                          \tag{24}
\]

The bivariate extension therefore closes exactly the previously residual
profiles satisfying \(p+9-d\ge17\).  Combining this with the earlier
quadratic-moving boundary gives the following exact remaining values of
\(d\), with \(s=p+9-2d\):

\[
\begin{array}{c|l}
p&d\\ \hline
8&1,2,3,4,5,6,7,8\\
9&2,3,4,5,6,7,8,9\\
10&3,4,5,6,7,8,9\\
11&4,5,6,7,9,10\\
12&5,6,7,10\\
13&6,7\\
14&7.
\end{array}                                                   \tag{25}
\]

There are no remaining double/single residuals for \(p\ge15\).  Every entry
in (23) and (25) remains open; this audit makes no further closure claim.

## 9. Reproducible check

[verify_live_three_zero_seventh_split_bivariate_five_anchor_audit.py](../computations/verify_live_three_zero_seventh_split_bivariate_five_anchor_audit.py)
constructs the cleared quartic rows, checks bidegree \((10,10)\), exhibits
the sharp eleven-point interpolation counterexample, verifies both endpoint
factorizations and translation signs, verifies the signed quartet
subtraction and both values in (20), audits all worst-case zero counts, and
recomputes the exact post-closure residual table (25).
