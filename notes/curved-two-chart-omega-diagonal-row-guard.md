# Two diagonal-complete curved charts can have independent Omega pencils

## 1. Outcome

At the first \(8\to6\) boundary, the interpolation

\[
 {\cal E}(tK_0+uK_1)=tu(t\Omega _0+u\Omega _1)                 \tag{1}
\]

does not couple two overlapping charts merely from physical curvature,
literal source provenance, good endpoint stars, and all three diagonal
pair rows.  There is an integral eight-site aggregate packet with two
overlapping pairs \(pq,pr\) such that, in both charts,

1. all three diagonal physical rows are exactly \(X_0,X_1,X_2\);
2. \(K_0=E_{00}\) is a clean unary point with direct scalar one;
3. \(K_1=E_{00}-I\) is scalar-zero, has the complete binary row
   \(-X_1-X_2\), and is clean;
4. both deleted endpoint-star maps have rank three;
5. the charts share their literal four-cut data and the physical minor is
   
   \[
                         AU-BF=1;                              \tag{2}
   \]
6. both pairs \((\Omega _0,\Omega _1)\) are linearly independent.

Consequently neither joining line has an active clean point.  The packet
is not an exact ternary source: in either chart, each of the six
off-diagonal pair rows has one nonzero mixed-word coefficient instead of
zero.  Thus the guard isolates the remaining input exactly.  The full-nine
route must use the six off-diagonal common-power annihilator equations;
the physical scalar \(AU-BF\) is not, and cannot be substituted for, a
minor of the two-column top-tensor matrix
\((\Omega _0\ \Omega _1)\).

Section 8 states the smallest remaining lemma as the emptiness of a finite
family of saturated rank strata.  It also records the necessary domain
hypothesis: a common divided power may be cancelled only when its
multiplication map is injective on the particular source-provenant module.
Nonvanishing of that power is not enough in the site-square-zero algebra.

## 2. The integral aggregate packet

Work in the site-square-zero algebra

\[
 {\cal R}(S)=\bigotimes_{x\in S}(\mathbb C\oplus V_x),
 \qquad V_xV_x=0,                                               \tag{3}
\]

with three coordinate vectors \(e_0^{(x)},e_1^{(x)},e_2^{(x)}\)
at every site.  Write

\[
                       (xy)_c=e_c^{(x)}e_c^{(y)}.                \tag{4}
\]

Take

\[
                    S=\{p,q,a,b,c,d,r,s\}.                     \tag{5}
\]

All displayed aggregate entries have weight one and have the same colour
at their two endpoints:

\[
\begin{array}{c|l}
\text{colour}&\text{physical pairs}\ \\ \hline
0&pq,\ pr,\ pa,\ qb,\ cd,\ rs,\\
1&pd,\ qs,\ ac,\ br,\\
2&pc,\ qr,\ ad,\ bs.
\end{array}                                                     \tag{6}
\]

Every undisplayed aggregate cell is zero.  Thus (6) is a literal family
of endpoint-ordered source blocks; endpoint order happens to be invisible
because every nonzero cell in the guard has equal endpoint colours.

The three four-edge sets

\[
\begin{aligned}
 M_0&=pa\mid qb\mid cd\mid rs,\\
 M_1&=pd\mid qs\mid ac\mid br,\\
 M_2&=pc\mid qr\mid ad\mid bs                              \tag{7}
\end{aligned}
\]

are the three intended constant-colour matchings.  The extra colour-zero
cells \(pq,pr\) supply the two direct scalars and the curvature square.
They do not occur in an intended matching.

For a deleted pair \(x,y\), write \(q_{xy}\) for the internal quadratic,
\(P_i^{xy},S_j^{xy}\) for its two endpoint-star rows, and
\(a_{ij}^{xy}=A_{xy}(i,j)\).  At six residual sites the nine physical rows
would be

\[
 a_{ij}^{xy}q_{xy}^{[3]}
   +P_i^{xy}S_j^{xy}q_{xy}^{[2]}=\delta_{ij}X_i.                 \tag{8}
\]

The next two sections verify exactly the three diagonal instances of (8),
including every residual word.

## 3. The \(pq\)-chart

On \(W_{pq}=\{a,b,c,d,r,s\}\), the internal quadratic is

\[
 q=q_{pq}
  =(cd)_0+(rs)_0+(ac)_1+(br)_1+(ad)_2+(bs)_2.                  \tag{9}
\]

The endpoint rows selected from (6) are

\[
\begin{array}{c|ccc}
 &0&1&2\\ \hline
 p&e_0^{(a)}+e_0^{(r)}&e_1^{(d)}&e_2^{(c)}\\
 q&e_0^{(b)}&e_1^{(s)}&e_2^{(r)}.
\end{array}                                                     \tag{10}
\]

Both triples are linearly independent.  Put

\[
 x=P_0^{pq}S_0^{pq}=(ab)_0+(br)_0,
 \qquad D_1=(ds)_1,
 \qquad D_2=(cr)_2.                                            \tag{11}
\]

The two summands of \(x\) share site \(b\), so

\[
                              x^{[2]}=0.                         \tag{12}
\]

There is no perfect matching in the physical support of (9).  Indeed,
site \(a\) must be matched to \(c\) or \(d\); after either choice the other
of \(c,d\) is isolated among the four remaining sites.  Hence

\[
                              q^{[3]}=0.                         \tag{13}
\]

The three response cofactors are unique:

\[
\begin{array}{c|c|c}
\text{response}&\text{surviving internal matching}&\text{output}\\ \hline
(ab)_0&(cd)_0(rs)_0&X_0,\\
(br)_0&\text{none}&0,\\
(ds)_1&(ac)_1(br)_1&X_1,\\
(cr)_2&(ad)_2(bs)_2&X_2.
\end{array}                                                     \tag{14}
\]

Therefore, as identities in the complete top component of
\({\cal R}(W_{pq})\),

\[
             xq^{[2]}=X_0,\qquad
             D_1q^{[2]}=X_1,\qquad
             D_2q^{[2]}=X_2.                                  \tag{15}
\]

The direct block \(pq\) has \(a_{00}^{pq}=1\) and
\(a_{11}^{pq}=a_{22}^{pq}=0\).  Equations (13)--(15) prove all
three diagonal rows of (8).

For \(K_0=E_{00}\), the effective quadratic is

\[
                              F_0=q+x.                           \tag{16}
\]

Using (12)--(15),

\[
                         F_0^{[3]}=q^{[3]}+xq^{[2]}=X_0.         \tag{17}
\]

Thus \(K_0\) is clean.  For

\[
 K_1=E_{00}-I=\operatorname {diag}(0,-1,-1),
 \qquad R=-D_1-D_2,                                            \tag{18}
\]

the direct scalar is zero and (15) gives

\[
                         Rq^{[2]}=-X_1-X_2.                     \tag{19}
\]

The response \(R\) has only the two disjoint edges \(ds,cr\), so

\[
                         R^{[2]}=D_1D_2,\qquad R^{[3]}=0.        \tag{20}
\]

Hence the scalar-zero binary point is clean as well.

## 4. The overlapping \(pr\)-chart

On \(W_{pr}=\{q,a,b,c,d,s\}\), the same aggregate cells give

\[
 q'=q_{pr}
   =(qb)_0+(cd)_0+(qs)_1+(ac)_1+(ad)_2+(bs)_2.                 \tag{21}
\]

The endpoint rows are

\[
\begin{array}{c|ccc}
 &0&1&2\\ \hline
 p&e_0^{(a)}+e_0^{(q)}&e_1^{(d)}&e_2^{(c)}\\
 r&e_0^{(s)}&e_1^{(b)}&e_2^{(q)}.
\end{array}                                                     \tag{22}
\]

Again both triples are injective.  Put

\[
 x'=(as)_0+(qs)_0,
 \qquad D'_1=(bd)_1,
 \qquad D'_2=(cq)_2.                                           \tag{23}
\]

The terms of \(x'\) share \(s\), so \((x')^{[2]}=0\).  As in the
first chart, \(a\) must use \(ac\) or \(ad\) in any hypothetical internal
perfect matching, after which the other of \(c,d\) is isolated.  Thus

\[
                             (q')^{[3]}=0.                       \tag{24}
\]

The unique cofactor products are

\[
\begin{aligned}
 x'(q')^{[2]}&=(as)_0(qb)_0(cd)_0=X_0,\\
 D'_1(q')^{[2]}&=(bd)_1(qs)_1(ac)_1=X_1,\\
 D'_2(q')^{[2]}&=(cq)_2(ad)_2(bs)_2=X_2.                       \tag{25}
\end{aligned}
\]

The other summand \((qs)_0\) of \(x'\) has no internal cofactor.  Since
the direct block \(pr\) also has only its \(00\)-cell, equations
(24)--(25) prove all three diagonal physical rows.  They also give

\[
 (q'+x')^{[3]}=X_0,\qquad
 R'(q')^{[2]}=-X_1-X_2,\qquad
 (R')^{[3]}=0,                                                \tag{26}
\]

where

\[
                              R'=-D'_1-D'_2.                    \tag{27}
\]

Thus the unary and scalar-zero binary endpoints in the \(pr\)-chart are
both clean.

## 5. Literal four-cut curvature data

Expose \(p,q,r,s\), all in colour zero, and put

\[
                              D=\{a,b,c,d\}.                    \tag{28}
\]

In the standard endpoint-ordered notation,

\[
 (A,B,C,E,F,U)=(1,1,0,0,0,1).                                 \tag{29}
\]

Indeed \(qs\) exists only in colour one, so its \((0,0)\)-cell is zero.
Consequently the physical curvature coordinate is

\[
                              \kappa=AU-BF=1.                   \tag{30}
\]

The common interior and selected star rows on \(D\) are

\[
 z=(cd)_0+(ac)_1+(ad)_2,
 \qquad \xi=e_0^{(a)},\quad \eta=e_0^{(b)},\quad t=v=0.         \tag{31}
\]

The two coordinate-cap interiors and their shared coefficients are

\[
\begin{aligned}
 f&=z+(ab)_0,&g&=z,\\
 L&=e_0^{(b)},&H&=0,&N&=e_0^{(a)},&M&=1.                       \tag{32}
\end{aligned}
\]

They satisfy the literal curvature identities.  For example,

\[
 Uf+tH-Fg-\eta N=f-(ab)_0=z=\kappa z.                          \tag{33}
\]

They also satisfy both selected clean rows:

\[
 Mf^{[2]}+LHf=X_0^D,
 \qquad
 Mg^{[2]}+LNg=X_0^D.                                          \tag{34}
\]

Here \(f^{[2]}=(ab)_0(cd)_0=X_0^D\), while \(g^{[2]}=0\) and
\(LNg=(ab)_0(cd)_0\).  Thus the guard retains the literal shared
\((L,M)\) packet; the two chart presentations are not unrelated formal
copies.

## 6. Both residual Omega pairs are independent

For either chart the scalar at \(K_0\) is \(\sigma=1\).  Since the
response \(x\) at \(K_0\) has square zero, the complementary-row tensors
specialize to

\[
 \Omega _0=Rq x,
 \qquad
 \Omega _1=R^{[2]}(q+x).                                      \tag{35}
\]

In the \(pq\)-chart, equations (9)--(11) and (20) leave exactly one
matching in each tensor:

\[
\boxed{
 \begin{aligned}
 \Omega _0^{pq}&=-(ds)_1(ac)_1(br)_0,\\
 \Omega _1^{pq}&= +(ds)_1(cr)_2(ab)_0.
 \end{aligned}}                                                \tag{36}
\]

The two displayed monomials are different residual colour words, so

\[
                 \Omega _0^{pq}\wedge\Omega _1^{pq}\ne0.      \tag{37}
\]

Likewise, in the \(pr\)-chart,

\[
\boxed{
 \begin{aligned}
 \Omega _0^{pr}&=-(bd)_1(ac)_1(qs)_0,\\
 \Omega _1^{pr}&= +(bd)_1(cq)_2(as)_0,
 \end{aligned}}                                                \tag{38}
\]

and therefore

\[
                 \Omega _0^{pr}\wedge\Omega _1^{pr}\ne0.      \tag{39}
\]

On each joining line,

\[
 tK_0+uK_1=\operatorname {diag}(t,-u,-u).                       \tag{40}
\]

The direct scalar and all three diagonal coordinates are nonzero exactly
when \(tu\ne0\).  Equations (1), (37), and (39) show that neither line
has a residual projective kernel, hence neither line has an active clean
point.

This also separates the two kinds of minors.  The scalar \(\kappa=1\) in
(30) is a determinant of four physical block entries.  The quantities in
(37), (39) lie in exterior squares of two different 729-dimensional top
tensor spaces.  They are not scalar \(2\times2\) minors of the matrix
whose determinant is \(AU-BF\).  The guard has all three quantities
nonzero simultaneously.

## 7. The six off-diagonal rows are the exact failure

The packet is not a ternary source.  In the \(pq\)-chart,
\(a_{ij}^{pq}=0\) for \(i\ne j\) and \(q^{[3]}=0\), so every off-diagonal
instance of (8) is required to vanish.  Instead, each has one surviving
matching.  The table lists the surviving response component and its
internal complement; endpoint colours on a response edge are written in
their displayed order.

\[
\begin{array}{c|c|c}
(i,j)&\text{response component}&\text{internal complement}\\ \hline
(0,1)&(as)_{0,1}&(cd)_0(br)_1,\\
(0,2)&(ar)_{0,2}&(cd)_0(bs)_2,\\
(1,0)&(db)_{1,0}&(ac)_1(rs)_0,\\
(1,2)&(dr)_{1,2}&(ac)_1(bs)_2,\\
(2,0)&(cb)_{2,0}&(ad)_2(rs)_0,\\
(2,1)&(cs)_{2,1}&(ad)_2(br)_1.
\end{array}                                                     \tag{41}
\]

Every product in (41) has coefficient one and gives a different mixed
word.  All other response components either collide or have no internal
cofactor.  Thus precisely the six off-diagonal rows fail.  The \(pr\)-chart
reindexes the same six global mixed perfect matchings and fails its six
off-diagonal presentations as well.

At \(h=3\), it is useful to write a genuine full-nine off-diagonal row as

\[
 C_{ij}=3P_iS_j+a_{ij}q,
 \qquad C_{ij}q^{[2]}=0\quad(i\ne j),                            \tag{42}
\]

because \(qq^{[2]}=3q^{[3]}\).  Thus the missing six rows say that six
literal source-provenant quadratics lie in

\[
                            \operatorname {Ann}(q^{[2]}).       \tag{43}
\]

The response matrix \(P_iS_j\) still obeys its rank-one rectangle
identities before multiplication, and the corresponding quadratics in the
overlapping chart obey the literal Bianchi/curvature connection.  These
annihilator and overlap constraints are exactly what (6) omits.  The
diagonal rows, curvature square, and clean endpoints cannot replace them,
by (36)--(41).

## 8. The smallest remaining lemma and its saturation hypotheses

The remaining statement can be made finite and scheme-theoretically
exact.  Let \({\cal P}\) be the affine parameter space of three-colour
aggregate blocks on eight fixed sites.  Let \(I_9\) be the coefficient
ideal of all nine tensor equations (8) in one fixed pair chart.  Those
nine rows are the complete global top-tensor equality, so on literal
aggregate blocks they imply the nine presentations in every other chart.

Add to \(I_9\):

* cleanliness of \(E_{00}\) and \(E_{00}-I\) in both \(pq,pr\) charts;
* the two scalar-zero equations
  \(a_{11}^{pq}+a_{22}^{pq}=a_{11}^{pr}+a_{22}^{pr}=0\).

Call the resulting ideal \(I_{\rm phys}\).  Work on the open locus where

\[
 A=a_{00}^{pq}\ne0,\qquad B=a_{00}^{pr}\ne0,
 \qquad \kappa=AU-BF\ne0,                                     \tag{44}
\]

and the four endpoint-star maps have rank three.  The last condition is a
finite union of standard opens; on one such open let \(\gamma\) be the
product of four chosen nonzero \(3\times3\) coordinate minors.

For a chart \(\chi\in\{pq,pr\}\), choose a basis of its top tensor space
and form the two-column matrix

\[
                         \Phi_\chi=(\Omega_{\chi0}\ \Omega_{\chi1}). \tag{45}
\]

Its no-active locus is the following constructible set:

\[
\begin{aligned}
 N_\chi={}&
 \bigcup_{\lambda<\mu}
 D\!\left(
  \Omega_{\chi0,\lambda}\Omega_{\chi1,\mu}
 -\Omega_{\chi0,\mu}\Omega_{\chi1,\lambda}
 \right)\\
 &\ \cup
 \left(V(\Omega_{\chi0})\cap
       \bigcup_\lambda D(\Omega_{\chi1,\lambda})\right)\\
 &\ \cup
 \left(V(\Omega_{\chi1})\cap
       \bigcup_\lambda D(\Omega_{\chi0,\lambda})\right).     \tag{46}
\end{aligned}
\]

The first line is tensor independence; the other two lines are the two
endpoint-degenerate cases.  Formula (46) is basis independent even though
it is written on coordinate opens.

The exact missing lemma is now

> **Full-nine Omega-incidence lemma.**  On the locus (44) with four good
> endpoint stars,
> 
> \[
>                V(I_{\rm phys})\cap N_{pq}\cap N_{pr}=\varnothing. \tag{47}
> \]

This is strictly narrower than a general common-root theorem: the order is
fixed at eight, both known endpoints and their activity divisor are fixed,
and the only alternatives in (46) are rank two or one zero column.  The
guard proves that replacing \(I_9\) by its three diagonal rows makes (47)
false, even with every other open condition retained.

There is a finite exact saturation formulation of (47).  For each chart,
choose one of the three lines of (46).  In an endpoint-degenerate branch,
add every coordinate of the zero column to the ideal and choose one
coordinate \(w_\chi\) of the other column as a nonzero witness.  In the
independent branch, choose one nonzero wedge coordinate as \(w_\chi\).
Then (47) is equivalent to the finite family of certificates

\[
  1\in
  \bigl(I_{\rm phys}+Z_{pq}+Z_{pr}\bigr):
       (AB\kappa\gamma w_{pq}w_{pr})^\infty,                    \tag{48}
\]

over all choices of good-star coordinate charts, bad-stratum types, and
nonzero witnesses.  Here \(Z_\chi=0\) in an independent branch and is the
coordinate ideal of the asserted zero column in an endpoint-degenerate
branch.  This formulation neither assumes irreducibility nor silently
discards endpoint components.

Equivalently, at a fixed complex point put

\[
 {\mathfrak l}_\chi=
  \left(t\Omega_{\chi0,\lambda}
       +u\Omega_{\chi1,\lambda}:\lambda\right)
       \subset\mathbb C[t,u].                                  \tag{49}
\]

Then

\[
 {\mathfrak l}_\chi:(tu)^\infty\ne(1)                          \tag{50}
\]

if and only if the line has an active clean point.  Indeed, independent
columns give the ideal \((t,u)\) after scalar row reduction; exactly one
zero column gives \((t)\) or \((u)\); saturation by \(tu\) makes all three
ideals unit.  Two nonzero dependent columns have a kernel with both
coordinates nonzero, and two zero columns make every point clean.

Two cautions are essential in using (48)--(50).

1. Saturation in the parameter ring and specialization to a physical
   point need not commute.  A proof may use the finite rank stratification
   (46)--(48), or it must establish the flatness/base-change statement
   needed for a universal incidence saturation.  Merely computing one
   generic saturated ideal does not cover endpoint-specialized fibres.
2. Localizing at the scalar \(AB\kappa\gamma w_{pq}w_{pr}\) is legitimate
   and requires no domain assumption: that scalar becomes a unit on the
   chosen standard open.  By contrast, from an identity
   
   \[
                         Zq^{[j]}=0                             \tag{51}
   \]
   
   one may conclude only
   \(Z\in\operatorname {Ann}(q^{[j]})\).  The algebra (3) is not a
   domain, and every positive-degree element has zero divisors.  Cancelling
   \(q^{[j]}\) requires the explicit hypothesis that multiplication by
   \(q^{[j]}\) is injective on the particular source-provenant submodule
   containing \(Z\), or an independently proved description of its
   annihilator.  Nonvanishing of \(q^{[j]}\), a cofactor, or a hafnian does
   not supply that hypothesis.

Thus (42)--(48), rather than a determinant comparison, are the precise
remaining bridge.  The physical minor \(AU-BF\) can be inverted as a
scalar on (44), but no identity in the source equations identifies it with
any wedge coordinate in (46).  The integral guard (6) makes that logical
separation explicit while locating the missing information in exactly the
six off-diagonal full-nine annihilator rows.
