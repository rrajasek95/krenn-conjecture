# Independent audit of the one-invertible isolate zero cover

## 1. Verdict

The strengthened local assertion in Lemma 6.6 of
[rank-three-separator-collapse.md](rank-three-separator-collapse.md) is
correct. One invertible deleted star, an entirely arbitrary second deleted
star, and an internal block of rank at most two force at least two of the
six rows at the other endpoint to vanish. If the second star is also
invertible and the internal block has rank two, all six rows vanish.

The proof below was reconstructed directly from the Hessian gauge
equations. It covers ranks zero, one, and two for the internal block and
makes no nonvanishing or rank assumption on the second star in the first
assertion.

There is one hypothesis-scope qualification, not a mathematical gap. The
local conclusions

\[
 \#\{P_0,P_1,P_2,S_0,S_1,S_2\text{ nonzero}\}\leq4
 \quad\hbox{and}\quad
 A_{py}=A_{qy}=0
\]

use only the fixed gauge-rigid deletion chart. The further graph conclusion
\(N_S(y)=\{x\}\) uses the rank-two boundary cap in other deletion charts,
and therefore needs the surrounding **all-pair** gauge-rigidity hypothesis.
That hypothesis is in force in Section 6 of the main note, but it must be
retained if Lemma 6.6 is quoted standalone.

The independent verifier is
[verify_one_invertible_zero_cover_audit.py](../computations/verify_one_invertible_zero_cover_audit.py).

## 2. Re-derivation of the local block equations

Delete \(p,q\), let \(W=B\setminus\{p,q\}\), write \(|W|=2r\), and let
\(q_0\) be the internal quadratic. With factorial normalization, put

\[
 Q={q_0^r\over r!},\qquad
 \mathcal H_{q_0}(Z)={Zq_0^{r-1}\over(r-1)!}.
\]

Then \(\mathcal H_{q_0}(q_0)=rQ\). For \(c\ne d\), the exact target has
zero \((c,d)\) two-deletion slice, so the pair equation is

\[
 \mathcal H_{q_0}(p_cs_d)+a_{cd}Q=0.
\]

Consequently

\[
 p_cs_d+{a_{cd}\over r}q_0\in\ker\mathcal H_{q_0}.       \tag{1}
\]

Gauge rigidity says that (1) is a vertex-expansion gauge. On an oriented
internal block \(xy\), it gives

\[
 p_{c,x}\otimes s_{d,y}+s_{d,x}\otimes p_{c,y}
       =\lambda_{cd,xy}A_{x\mid y},\qquad c\ne d.        \tag{2}
\]

This uses the complete mixed product: both star matchings occur, with no
termwise inference. The scalar in (2) is
\(\alpha_x+\alpha_y-a_{cd}/r\), though its value will not matter.

Assume \(A_{px}\) is invertible and set

\[
 a_c=p_{c,x},\quad b_d=s_{d,x},\quad
 P_c=p_{c,y},\quad S_d=s_{d,y},\quad A=A_{x\mid y}.
\]

The vectors \(a_0,a_1,a_2\) form a basis of \(V_x\), while the \(b_d\)'s
are arbitrary, including zero. Equation (2) becomes

\[
 \boxed{\quad a_c\otimes S_d+b_d\otimes P_c
                    =\lambda_{cd}A,\qquad c\ne d.\quad} \tag{3}
\]

Thus only a three-dimensional linear-algebra statement remains.

## 3. One basis forces two zero rows

Assume \(\operatorname{rank}A\le2\). Suppose for contradiction that at
least five of the six vectors \(P_c,S_d\) are nonzero.

### 3.1 All six rows are nonzero and \(\operatorname{rank}A=2\)

Let \(\alpha\ne0\) annihilate the two-dimensional left image of \(A\), and
write

\[
 \alpha_c=\alpha(a_c),\qquad \beta_d=\alpha(b_d).
\]

Contracting (3) on the left gives

\[
                 \alpha_cS_d+\beta_dP_c=0,
                 \qquad c\ne d.                         \tag{4}
\]

Every \(\alpha_c\) is nonzero. If \(\alpha_k=0\), the two equations
\((k,d)\), \(d\ne k\), first give \(\beta_d=0\). Equations using those two
values of \(d\) then give the other two \(\alpha\)'s zero, contrary to
\(\alpha\ne0\). Equation (4) now also forces every \(\beta_d\ne0\).

Thus \(S_d\) and \(P_c\) are proportional whenever \(c\ne d\). The
bipartite incidence graph \(K_{3,3}\) with its diagonal matching deleted is
connected, so all six right vectors lie on one line. Every left side of
(3) has matrix rank at most one. Since \(A\) has rank two, every
\(\lambda_{cd}=0\). For fixed \(d\), the two zero equations make \(b_d\)
proportional to each of two distinct basis vectors \(a_c\), \(c\ne d\),
which is impossible.

### 3.2 All six rows are nonzero and \(\operatorname{rank}A\le1\)

Let \(L\) be the left image of \(A\), and pass to
\(\overline V_x=V_x/L\). This quotient has dimension at least two, and
(3) becomes

\[
 \bar a_c\otimes S_d+\bar b_d\otimes P_c=0,
 \qquad c\ne d.                                         \tag{5}
\]

If some \(\bar a_k=0\), the two equations \((k,d)\), \(d\ne k\), give
\(\bar b_d=0\); equations with those two \(d\)'s then give the other two
\(\bar a\)'s zero. This is impossible because the images of the basis
\(a_0,a_1,a_2\) span \(\overline V_x\).

Hence every \(\bar a_c\ne0\). Simple-tensor uniqueness in (5) makes
\(\bar a_c\) proportional to \(\bar b_d\) for every \(c\ne d\). The same
connected incidence graph puts all three \(\bar a_c\)'s on one line,
contradicting that they span a quotient of dimension at least two.

### 3.3 Exactly one row is zero

First suppose \(P_k=0\). For each \(d\ne k\), equation (3) is

\[
                       a_k\otimes S_d=\lambda_{kd}A.
\]

Its left side is nonzero of rank one. Hence \(A\) has rank one and its
left image is \(\mathbb F a_k\). Quotienting by this line, the two
equations \((c,k)\), \(c\ne k\), make the single vector \(\bar b_k\)
proportional to each of the two independent vectors \(\bar a_c\), a
contradiction.

It remains to suppose \(S_k=0\). If \(A\) has rank two, use
\(\alpha_c,\beta_d\) from (4). The two equations with \(d=k\) give
\(\beta_k=0\). If \(\alpha_k=0\), the other four incidences successively
give \(\beta_i=\beta_j=\alpha_i=\alpha_j=0\), impossible. Thus
\(\alpha_k\ne0\). Equation (4) now puts

\[
                 P_0,P_1,P_2,S_i,S_j
\]

on one right line, where \(\{i,j,k\}=\{0,1,2\}\). The \((k,i)\) and
\((j,i)\) left sides in (3) have rank at most one, so their lambdas vanish.
The resulting equations make \(b_i\) proportional to both \(a_k\) and
\(a_j\), a contradiction.

Finally, if \(\operatorname{rank}A\le1\), quotient by its left image. The
two equations with \(d=i\) say that \(\bar a_k,\bar a_j\) are either both
zero or proportional; those with \(d=j\) say the same about
\(\bar a_k,\bar a_i\). Thus the three \(\bar a_c\)'s span at most a line,
contrary to the quotient having dimension at least two.

All possibilities with five or six nonzero rows are excluded. Therefore
at least two of \(P_0,P_1,P_2,S_0,S_1,S_2\) vanish. No step assumed
anything about the rank or support of the \(b_d\)'s.

## 4. A second basis forces all six rows to vanish in rank two

Assume now that \(b_0,b_1,b_2\) are also a basis and
\(\operatorname{rank}A=2\). Express

\[
 b_d=\sum_e C_{ed}a_e,
\]

where \(C\) is invertible, and write
\(A=\sum_e a_e\otimes A_e\). In every row \(e\ne c\), equation (3) reads

\[
                         C_{ed}P_c=\lambda_{cd}A_e.       \tag{6}
\]

Let \(\alpha\) span the unique relation
\(\sum_e\alpha_eA_e=0\). If \(\alpha_c\ne0\), the two rows \(A_e\),
\(e\ne c\), are independent; otherwise all three rows of \(A\) would span
a line. Hence (6) rules out \(\lambda_{cd}\ne0\) for either \(d\ne c\).
If \(P_c\ne0\), (6) puts both columns of \(C\) indexed by \(d\ne c\) on
the same coordinate line \(\mathbb F e_c\), contradicting invertibility.
Therefore

\[
                         \alpha_c\ne0\Longrightarrow P_c=0. \tag{7}
\]

There are three support cases for \(\alpha\).

* If all three entries of \(\alpha\) are nonzero, (7) kills every \(P_c\).
  Equation (3), comparing rank one with rank two, then kills every \(S_d\).
* If \(\operatorname{supp}\alpha=\{i,j\}\), then \(P_i=P_j=0\). For every
  \(d\), choose \(c\in\{i,j\}\) with \(c\ne d\); equation (3) kills \(S_d\).
  A remaining equation with \(c=k\notin\{i,j\}\) then kills \(P_k\).
* If \(\operatorname{supp}\alpha=\{k\}\), then \(A_k=0\), the other two
  rows of \(A\) are independent, and \(P_k=0\). Equations \((k,d)\),
  \(d\ne k\), kill the two \(S_d\)'s. The two cross equations among the
  remaining colors kill their \(P\)'s, and one last equation kills \(S_k\).

Thus all six endpoint rows vanish. In the original notation,

\[
                         A_{py}=A_{qy}=0.                \tag{8}
\]

The assumption that the second star is a basis is essential for this
sharpening; Section 6 gives an exact sharp example without it.

## 5. The cover and the neighborhood conclusion

If \(x\) is isolated in the rank-three graph of the fixed internal chart,
then every \(y\ne x\) has \(\operatorname{rank}A_{xy}\le2\). Applying
Section 3 separately to each such \(y\) says exactly that the six global
zero sets based at \(p,q\) cover \(W\setminus\{x\}\) with multiplicity at
least two.

For completeness, assume all-pair gauge rigidity, both \(A_{px}\) and
\(A_{qx}\) invertible, and \(\operatorname{rank}A_{xy}=2\). By (8), all
six rows at \(y\) vanish, while all six corresponding rows at \(x\) are
nonzero. Fix \(t\notin\{p,x,y\}\), delete \(p,t\), and apply (2) on \(yx\).
A zero \(p\)-row at \(y\) reduces the left side to one simple tensor.
Rank one versus the rank-two block \(A_{yx}\) makes the gauge scalar and
that simple tensor zero. The two off-color \(t\)-rows at \(y\) vanish, so
\(\operatorname{rank}A_{ty}\le1\). Hence

\[
                         N_S(y)\subseteq\{p,x\}.
\]

Repeating from \(q\) gives \(N_S(y)\subseteq\{q,x\}\). Since \(xy\in S\),
their intersection yields \(N_S(y)=\{x\}\). This last paragraph is where
deletion charts other than the fixed \((p,q)\) chart enter.

## 6. Independent exact search

The verifier encodes (3) as 54 homogeneous scalar equations in the 18
entries of \(P_c,S_d\) and six lambdas. It uses two exact reductions.

1. A right change of basis is transitive on matrices \(A\) having a fixed
   left image, so one representative for each rank-zero, rank-one, or
   rank-two image space suffices.
2. A nonzero rescaling of one \(b_d\) can be absorbed by rescaling \(S_d\)
   and \(\lambda_{cd}\), preserving which endpoint rows vanish. Thus only
   the zero vector and projective representatives for each \(b_d\) are
   needed.

For each linear solution space, the verifier records a row as active if it
is nonzero in some solution. If five row projections were active over an
infinite field, a generic linear combination would make all five
simultaneously nonzero. The computed stronger bound is that no class even
has more than four active row projections.

The exhaustive results are:

* over \(\mathbb F_2\): 7,680 arbitrary-second-star/rank-at-most-two
  classes, with maximum active-row count four;
* over \(\mathbb F_3\): 74,088 such classes, again with maximum four;
* in the double-invertible rank-two subcase: all endpoint projections
  vanish in all 1,176 \(\mathbb F_2\) classes and all 18,252
  \(\mathbb F_3\) classes.

There is also an exact bounded rational audit of 74,088 normalized classes
whose selected projective data have entries in \(\{-1,0,1\}\). It computes
ranks modulo \(2^{61}-1\), but this proves the corresponding rational
ranks, rather than giving a probabilistic test: every integer equation row
has Euclidean norm at most \(\sqrt3\), so Hadamard bounds every relevant
minor by

\[
                         3^{12}=531441<2^{61}-1.
\]

The same maximum of four occurs, and all 19,188 bounded rational
double-invertible rank-two classes have zero endpoint projection.

Finally, the following rational solution shows that two zeros is sharp
when the second star is singular. Take \(a_c=e_c\), let the columns
\((b_0,b_1,b_2)\) be

\[
       (0,0,0),\quad(0,0,0),\quad(1,1,0),
\]

and set

\[
 A=\begin{pmatrix}-1&-1&0\\-1&0&0\\0&0&0\end{pmatrix},
\]

which has rank two. In pair order
\((01),(02),(10),(12),(20),(21)\), choose

\[
\begin{aligned}
 (P_0,P_1,P_2)&=((1,0,0),(-1,-1,0),(1,1,1)),\\
 (S_0,S_1,S_2)&=((0,0,0),(0,0,0),(0,1,0)),\\
 (\lambda_{01},\lambda_{02},\lambda_{10},
   \lambda_{12},\lambda_{20},\lambda_{21})&=(0,-1,0,1,0,0).
\end{aligned}
\]

Direct multiplication verifies all six equations (3), and exactly four
endpoint rows are nonzero. Thus the multiplicity-two conclusion is sharp,
and the second invertibility hypothesis is genuinely needed for the
all-six-zero sharpening.
