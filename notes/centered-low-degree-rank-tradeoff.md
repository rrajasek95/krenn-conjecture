# The centered low-degree branch has a sharp rank tradeoff

## 1. Outcome

Let an exact ternary source satisfy

\[
                         H_B(A)=\Delta_{B,3}.
\]

Fix a gauge-rigid deleted-pair chart \(\{r,u\}\), and let \(x,y\) be
distinct internal sites.  Assume that \(A_{rx}\) is invertible and that
\(A_{xy}\) has rank at most two.  The existing one-invertible zero-cover
lemma implies that at least two of the six endpoint rows

\[
 \{\hbox{rows of }A_{r\mid y}\}\ \cup\
 \{\hbox{rows of }A_{u\mid y}\}                         \tag{1}
\]

vanish.  This note proves the following sharper rank-two statement.

**Theorem 1.1 (rank-two spoke tradeoff).**  If

\[
 \operatorname {rank}A_{rx}=3,\qquad
 \operatorname {rank}A_{xy}=2,\qquad
 \operatorname {rank}A_{ux}\ge2,                       \tag{2}
\]

then

\[
                         A_{ry}=A_{uy}=0.                \tag{3}
\]

Thus an internal rank-two spoke from \(x\) is completely punched out at
both deleted stars as soon as the second deleted star has rank at least
two at \(x\).  Both rank thresholds are sharp:

* with \(\operatorname {rank}A_{ux}=1\), a rank-two spoke can coexist
  with invertible \(A_{ry}\) and only two missing rows at \(u\);
* with \(\operatorname {rank}A_{xy}=1\), even invertible \(A_{ux}\)
  can coexist with exactly four of the six rows in (1) nonzero.

These conclusions use the complete off-diagonal pair equations and retain
endpoint order and complex cancellation.  The sharp examples are local
mixed/gauge models, not exact Krenn sources.  They show precisely why the
remaining contradiction must use diagonal target responses or equations
which synchronize overlapping fan charts.

## 2. The endpoint-ordered local system

Delete \(r,u\), write \(q\) for the internal quadratic, and orient all
blocks with their named endpoint first.  For the deleted stars write

\[
 p_c=\sum_z p_{c,z},\qquad s_d=\sum_z s_{d,z}.
\]

Gauge rigidity and the off-diagonal pair equation give, on every internal
block \(xy\),

\[
 p_{c,x}\otimes s_{d,y}+s_{d,x}\otimes p_{c,y}
                    =\lambda_{cd,xy}A_{x\mid y},
 \qquad c\ne d.                                         \tag{4}
\]

This is the full polarized block: neither of its two terms is discarded.
Normalize the invertible block \(A_{r\mid x}\) by taking

\[
 a_c:=p_{c,x}=e_c.
\]

Put

\[
 b_d:=s_{d,x},\quad P_c:=p_{c,y},\quad S_d:=s_{d,y},
 \quad M:=A_{x\mid y}.
\]

Then (4) is the six-equation system

\[
 \boxed{\quad e_c\otimes S_d+b_d\otimes P_c
                   =\lambda_{cd}M,\qquad c\ne d.\quad} \tag{5}
\]

The rank of the matrix whose columns are \(b_0,b_1,b_2\) is exactly
\(\operatorname {rank}A_{u\mid x}\).

The general result imported from Lemma 6.6 of
[rank-three-separator-collapse.md](rank-three-separator-collapse.md),
with its
[independent audit](one-invertible-zero-cover-independent-audit.md), is:

**Lemma 2.1 (one-basis two-zero cover).**  If \(M\) has rank at most two,
then every solution of (5), with arbitrary \(b_0,b_1,b_2\), has at least
two zero vectors among

\[
                         P_0,P_1,P_2,S_0,S_1,S_2.        \tag{6}
\]

No isolation hypothesis on \(x\) is needed for this local assertion.

## 3. A rank-two block and a rank-two second star force six zeros

Assume now that \(\operatorname {rank}M=2\) and

\[
                         \dim\operatorname {span}
                         \{b_0,b_1,b_2\}\ge2.           \tag{7}
\]

Write the three rows of \(M\), in the basis \(e_0,e_1,e_2\), as
\(M_0,M_1,M_2\in V_y\).  Let

\[
 \alpha=(\alpha_0,\alpha_1,\alpha_2)\ne0,qquad
                  \alpha_0M_0+\alpha_1M_1+\alpha_2M_2=0 \tag{8}
\]

span the unique left-kernel line of \(M\), and put
\(\beta_d=\alpha(b_d)\).  Contracting (5) on its left factor by
\(\alpha\) gives

\[
                       \alpha_cS_d+\beta_dP_c=0,
                       \qquad c\ne d.                   \tag{9}
\]

Taking row \(e\ne c\) of (5) gives

\[
                       (b_d)_eP_c=\lambda_{cd}M_e.       \tag{10}
\]

Whenever \(\alpha_c\ne0\), the two rows \(M_e\), \(e\ne c\), are
independent: otherwise there would be a row relation whose coefficient at
\(c\) is zero, independent of (8).  Hence (10), for both complementary
rows, implies

\[
 \lambda_{cd}=0;qquad
 P_c\ne0\Longrightarrow b_d\in\mathbb C e_c
                         \quad(d\ne c).                 \tag{11}
\]

In the latter case, writing \(b_d=t_de_c\), the row \(c\) equation is

\[
                              S_d=-t_dP_c.               \tag{12}
\]

We now exhaust the support of the unique relation \(\alpha\).

### 3.1 Three nonzero coordinates

Suppose all \(\alpha_c\ne0\).  If \(P_c\ne0\), equations
(11)--(12) apply to both \(d\ne c\).  Let \(k\) be the third colour,
distinct from \(c,d\).  The \((k,d)\) equation becomes

\[
 t_d\bigl(-e_k\otimes P_c+e_c\otimes P_k\bigr)
                              =\lambda_{kd}M.            \tag{13}
\]

Its left image lies in the coordinate plane
\(\operatorname {span}(e_c,e_k)\).  The left image of \(M\) is
\(\ker\alpha\), which is not that coordinate plane because every
coordinate of \(\alpha\) is nonzero.  Rank two therefore forces
\(\lambda_{kd}=0\).  If \(t_d\ne0\), independence of \(e_c,e_k\)
in (13) gives \(P_c=0\), a contradiction.  Hence both columns
\(b_d\), \(d\ne c\), vanish.  This contradicts (7).  Thus every
\(P_c=0\), and (5), rank one versus rank two, gives every \(S_d=0\).

### 3.2 Exactly two nonzero coordinates

Relabel so that

\[
                  \alpha_0\alpha_1\ne0,\qquad\alpha_2=0. \tag{14}
\]

Suppose \(P_0\ne0\).  Then

\[
 b_1=t_1e_0,\quad b_2=t_2e_0,qquad
 S_1=-t_1P_0,\quad S_2=-t_2P_0.                         \tag{15}
\]

The \((2,1)\) equation has left image in
\(\operatorname {span}(e_0,e_2)\), whereas the left image
\(\ker\alpha\) of \(M\) is a different plane.  Thus its right-hand
scalar is zero, and \(t_1\ne0\) would force \(P_0=0\).  Hence
\(t_1=0\).  Similarly the \((1,2)\) equation compares
\(\operatorname {span}(e_0,e_1)\) with \(\ker\alpha\) and gives
\(t_2=0\).  Then \(b_1=b_2=0\), contrary to (7).  Therefore
\(P_0=0\); symmetrically \(P_1=0\).

Equations with \(c=0,1\) now kill all three \(S_d\).  If \(P_2\ne0\),
the \((2,0)\) and \((2,1)\) equations, whose left sides have rank at
most one, force \(b_0=b_1=0\).  Again (7) fails.  Hence \(P_2=0\).

### 3.3 Exactly one nonzero coordinate

Relabel so that \(\alpha_2\ne0\) and \(\alpha_0=\alpha_1=0\).  Then

\[
                       M_2=0,qquad M_0,M_1
                       \text{ are independent}.         \tag{16}
\]

If \(P_2\ne0\), equations (11)--(12) give
\(b_0=t_0e_2,b_1=t_1e_2\).  The \((1,0)\) equation has left image in
\(\operatorname {span}(e_1,e_2)\), different from
\(\operatorname {im}_L M=\operatorname {span}(e_0,e_1)\), and hence
forces \(t_0=0\).  The \((0,1)\) equation similarly forces \(t_1=0\).
This violates (7), so \(P_2=0\).  Equations with \(c=2\) then give
\(S_0=S_1=0\).

The \((0,1)\) and \((1,0)\) equations now say

\[
                            b_1P_0=0,qquad b_0P_1=0.     \tag{17}
\]

If both \(P_0,P_1\) were nonzero, only \(b_2\) could survive, contrary
to (7).  If, say, only \(P_0\ne0\), then \(b_1=0\); the \((1,2)\)
equation kills \(S_2\), and the \((0,2)\) equation kills \(b_2\), again
leaving rank at most one.  The case with only \(P_1\ne0\) is symmetric.
Thus \(P_0=P_1=0\), after which (5) also gives \(S_2=0\).

All support cases of \(\alpha\) give (6) with all six vectors zero.  In
the physical notation this is exactly (3), proving Theorem 1.1.

## 4. Fan-level centered export

Let \(F\) be a good fan centered at \(r\), and suppose its relevant
pairs lie in (E2), so each chart is gauge-rigid.  Fix \(x\ne r\) with
\(A_{rx}\) invertible.  For an endpoint \(v\) define

\[
 z_v(y)=\#\{c:\text{row }c\text{ of }A_{v\mid y}\text{ is zero}\}.
\]

For every \(u\in F\setminus\{x\}\) and every
\(y\notin\{r,u,x\}\) with \(\operatorname {rank}A_{xy}\le2\),
Lemma 2.1 gives

\[
                              z_r(y)+z_u(y)\ge2.          \tag{18}
\]

Consequently:

* \(z_r(y)=0\) forces \(\operatorname {rank}A_{uy}\le1\) for every
  eligible fan endpoint \(u\);
* \(z_r(y)=1\) forces every such \(A_{uy}\) to be singular;
* \(z_r(y)\ge2\) already gives \(\operatorname {rank}A_{ry}\le1\);
* if \(\operatorname {rank}A_{xy}=2\) and
  \(\operatorname {rank}A_{ux}\ge2\), Theorem 1.1 gives the literal
  holes \(A_{ry}=A_{uy}=0\).

If \(x\) is supplied by centered defect stability, then
\(\deg_{R-r}(x)\le2\).  Therefore (18) applies, in every fan chart, to
all but at most two rank-three neighbours of \(x\) (and the deleted site
itself).  This is a genuine centered normal form even when \(rx\in R\)
and the global rank-three degree of \(x\) is three.

## 5. Exact sharp witnesses

All vectors below are written in the standard bases at \(x,y\), and
the multiplier order is

\[
                             (01),(02),(10),(12),(20),(21). \tag{19}
\]

### 5.1 A rank-two spoke with a rank-one second star

Take

\[
 \begin{aligned}
 (b_0,b_1,b_2)&=(0,0,(1,1,0)),\\
 M&=\begin{pmatrix}-1&-1&0\\-1&0&0\\0&0&0\end{pmatrix},\\
 (P_0,P_1,P_2)&=((1,0,0),(-1,-1,0),(1,1,1)),\\
 (S_0,S_1,S_2)&=(0,0,(0,1,0)),\\
 (\lambda_{01},\lambda_{02},\lambda_{10},
   \lambda_{12},\lambda_{20},\lambda_{21})
   &=(0,-1,0,1,0,0).
 \end{aligned}                                           \tag{20}
\]

Then \(M\) has rank two, the \(b\)-matrix has rank one, and the matrix
with rows \(P_0,P_1,P_2\) is invertible.  Every equation (5) holds, while
exactly \(S_0,S_1\) vanish.  Thus neither the rank-one threshold in (2)
nor the all-six conclusion can be improved.

### 5.2 A rank-one spoke with two invertible deleted stars

Take

\[
 \begin{aligned}
 (b_0,b_1,b_2)&=(e_0,e_0+e_2,e_0+e_1),\\
 M&=e_0e_0^T,\\
 (P_0,P_1,P_2)&=(0,e_0,e_0),\\
 (S_0,S_1,S_2)&=(0,-e_0,-e_0),\\
 (\lambda_{01},\lambda_{02},\lambda_{10},
   \lambda_{12},\lambda_{20},\lambda_{21})
   &=(-1,-1,1,1,1,1).
 \end{aligned}                                           \tag{21}
\]

The \(b\)-matrix is invertible, \(M\) has rank one, all equations (5)
hold, and exactly \(P_0,S_0\) vanish.  Hence even two invertible deleted
stars do not improve the general two-zero cover on a rank-one spoke.

## 6. The remaining exact gate

The proof above uses only off-diagonal pair cells after passing through
the gauge kernel.  It does not use the three diagonal equations

\[
 a_{cc}q^{[t]}+p_cs_cq^{[t-1]}=X_c,qquad c=0,1,2,       \tag{22}
\]

where \(|B\setminus\{r,u\}|=2t\).  The witnesses (20)--(21) certify
that a single-chart continuation which uses no more than the local mixed
blocks cannot close the centered branch.

Alternatively choose two fan endpoints \(u,v\), put
\(W=B\setminus\{r,u,v\}\), and let \(q\) be the quadratic on \(W\).
If \(|B|=2m\), the complete common-complement compatibility system is

\[
 \boxed{
 \bigl(A_{r\mid u}(c,d)t_e+A_{r\mid v}(c,e)s_d
             +A_{u\mid v}(d,e)p_c\bigr)q^{[m-2]}
       +p_cs_dt_eq^{[m-3]}
       =\delta_{c=d=e}X_c^W.}                            \tag{23}
\]

There are 27 endpoint-ordered equations in (23).  They couple the same
physical block \(A_{u\mid v}\), with its required transpose under reversed
orientation, to both overlapping pair charts.  Eliminating the sharp
rank-one survivors now requires (22), (23), or an equivalent complete
cofactor identity; raw row counts, rank-three degree, and the six local
off-diagonal equations are exhausted.

## 7. Exact audit

The dependency-free checker
[verify_centered_low_degree_rank_tradeoff.py](../computations/verify_centered_low_degree_rank_tradeoff.py)
uses exact rational arithmetic to verify the ranks, zero-row counts, and
all six equations for both sharp witnesses.  The uniform implication in
Theorem 1.1 is the support-case proof of Section 3; the checker is only a
small algebra audit, not a finite substitute for that proof.
