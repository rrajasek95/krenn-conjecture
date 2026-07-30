# Independent audit and complementary guard for the two-chart Omega problem

## 1. Outcome

The integral packet in
[the diagonal-row guard](curved-two-chart-omega-diagonal-row-guard.md)
passes an independent coefficient audit.  Its global matching tensor has
exactly nine monomials: the three constant-colour targets and six mixed
monomials.  In each of the two overlapping charts, the three diagonal
physical rows, both clean endpoints, all four good endpoint stars, the
shared four-cut identities, and the curvature minor are exact.  Each of the
six off-diagonal rows fails in exactly one mixed word.  The two displayed
Omega columns in either chart are nonzero and independent.

There is also a complementary literal-block guard.  It has two overlapping
charts with

* nonzero physical curvature;
* four rank-three endpoint stars;
* a clean unary endpoint and a clean scalar-zero binary-target endpoint in
  each chart;
* every one of the six off-diagonal physical rows in each chart; and
* no active clean point on either joining line.

One version has two independent Omega columns in both charts and fails
exactly the three diagonal target anchors

\[
                              0=X_0,\quad 0=X_1,\quad 0=X_2.       \tag{1}
\]

A stronger second version has exactly one zero Omega column in both
charts, has \(q^{[2]}\ne0\), and retains the complete unary physical row
\(X_0\).  It fails only the two complementary diagonal anchors \(X_1,X_2\).

Thus the six off-diagonal rows do **not** exclude either bad Omega stratum
without the diagonal anchors, even with literal two-chart provenance,
curvature, clean endpoints, and good stars.  Conversely, the audited
diagonal-row guard shows that the diagonal anchors do not exclude the bad
strata without the six off-diagonal rows.  A positive argument must mix the
two kinds of rows before top degree.  The natural place is an anchored
coefficient-cut/Koszul overlap class, not the uncontracted directed
six-cycle by itself.

This note does not prove the full-nine Omega-incidence lemma and does not
close Krenn's conjecture.

The audited diagonal-row note has SHA-256

    715148e06499a9bddebf0985fb490423fe0b93cd8a9928a40840ce621b6e1f4a  notes/curved-two-chart-omega-diagonal-row-guard.md

## 2. Independent audit of the diagonal-row guard

Use its site order

\[
                         S=\{p,q,a,b,c,d,r,s\}.                    \tag{2}
\]

The nonzero aggregate cells, all with equal colours at their endpoints and
all of weight one, are

\[
\begin{array}{c|l}
0&pq,\ pr,\ pa,\ qb,\ cd,\ rs,\\
1&pd,\ qs,\ ac,\ br,\\
2&pc,\ qr,\ ad,\ bs.
\end{array}                                                       \tag{3}
\]

### 2.1 The complete global matching enumeration

Put

\[
             I=\{p,a,c,d\},\qquad J=\{q,b,r,s\}.                 \tag{4}
\]

Direct perfect-matching enumeration in (3) gives one matching for every
ordered pair \((i,j)\in\{0,1,2\}^2\), and no others.  Its colour word is

\[
 Y_{ij}=\bigotimes_{x\in I}e_i^{(x)}
          \otimes\bigotimes_{y\in J}e_j^{(y)}.                   \tag{5}
\]

The nine matchings are

\[
\begin{array}{c|l}
(0,0)&pa\mid qb\mid cd\mid rs,\\
(0,1)&pa\mid qs\mid cd\mid br,\\
(0,2)&pa\mid qr\mid cd\mid bs,\\
(1,0)&pd\mid qb\mid ac\mid rs,\\
(1,1)&pd\mid qs\mid ac\mid br,\\
(1,2)&pd\mid qr\mid ac\mid bs,\\
(2,0)&pc\mid qb\mid ad\mid rs,\\
(2,1)&pc\mid qs\mid ad\mid br,\\
(2,2)&pc\mid qr\mid ad\mid bs.
\end{array}                                                       \tag{6}
\]

Each coefficient is one.  Hence the aggregate top tensor is exactly

\[
                              \sum_{i,j=0}^2Y_{ij}.               \tag{7}
\]

The terms \(Y_{00},Y_{11},Y_{22}\) are the three desired targets.  The
other six are precisely the global mixed failures.  In particular, there
is no unlisted cancellation or extra perfect matching hidden in the
packet.

### 2.2 The \(pq\)-chart

On \(W_{pq}=\{a,b,c,d,r,s\}\), the internal quadratic and stars are

\[
\begin{aligned}
q={}&(cd)_0+(rs)_0+(ac)_1+(br)_1+(ad)_2+(bs)_2,\\
(P_0,P_1,P_2)={}&
 (e_0^{(a)}+e_0^{(r)},e_1^{(d)},e_2^{(c)}),\\
(S_0,S_1,S_2)={}&
 (e_0^{(b)},e_1^{(s)},e_2^{(r)}).
\end{aligned}                                                    \tag{8}
\]

The two star triples are independent.  The graph of \(q\) has no perfect
matching: after \(a\) uses \(ac\) or \(ad\), the other of \(c,d\) is
isolated.  Thus \(q^{[3]}=0\).

Write

\[
 x=P_0S_0=(ab)_0+(br)_0,\quad
 D_1=P_1S_1=(ds)_1,\quad D_2=P_2S_2=(cr)_2.             \tag{9}
\]

The two terms of \(x\) meet at \(b\), so \(x^{[2]}=0\).  There is one
cofactor matching in each diagonal row:

\[
 xq^{[2]}=X_0,\qquad D_1q^{[2]}=X_1,\qquad
 D_2q^{[2]}=X_2.                                                \tag{10}
\]

Since the direct block has only \(a_{00}=1\), (10) proves all three
diagonal physical equations.  It also gives

\[
 (q+x)^{[3]}=X_0,\qquad
 Rq^{[2]}=-X_1-X_2,\qquad R^{[3]}=0,
 \quad R=-D_1-D_2.                                               \tag{11}
\]

Thus both advertised endpoints are clean, and the second is a complete
scalar-zero binary row.

For the six off-diagonal cells, direct enumeration gives

\[
\begin{array}{c|c}
(i,j)&P_iS_jq^{[2]}\\ \hline
(0,1)&e_0^{(a)}e_1^{(b)}e_0^{(c)}e_0^{(d)}e_1^{(r)}e_1^{(s)},\\
(0,2)&e_0^{(a)}e_2^{(b)}e_0^{(c)}e_0^{(d)}e_2^{(r)}e_2^{(s)},\\
(1,0)&e_1^{(a)}e_0^{(b)}e_1^{(c)}e_1^{(d)}e_0^{(r)}e_0^{(s)},\\
(1,2)&e_1^{(a)}e_2^{(b)}e_1^{(c)}e_1^{(d)}e_2^{(r)}e_2^{(s)},\\
(2,0)&e_2^{(a)}e_0^{(b)}e_2^{(c)}e_2^{(d)}e_0^{(r)}e_0^{(s)},\\
(2,1)&e_2^{(a)}e_1^{(b)}e_2^{(c)}e_2^{(d)}e_1^{(r)}e_1^{(s)}.
\end{array}                                                       \tag{12}
\]

Every coefficient is one, every word is different, and every other
cofactor product collides.  Because the off-diagonal direct cells and
\(q^{[3]}\) vanish, (12) is the exact list of the six failed rows.

The complementary-row coefficients are

\[
\begin{aligned}
 \Omega_0^{pq}&=-(ds)_1(ac)_1(br)_0,\\
 \Omega_1^{pq}&= +(ds)_1(cr)_2(ab)_0.
\end{aligned}                                                    \tag{13}
\]

They are distinct nonzero coordinate words and hence independent.

### 2.3 The \(pr\)-chart and curvature

Deleting \(p,r\) gives

\[
\begin{aligned}
q'={}&(qb)_0+(cd)_0+(qs)_1+(ac)_1+(ad)_2+(bs)_2,\\
(P'_0,P'_1,P'_2)={}&
 (e_0^{(a)}+e_0^{(q)},e_1^{(d)},e_2^{(c)}),\\
(T_0,T_1,T_2)={}&
 (e_0^{(s)},e_1^{(b)},e_2^{(q)}).
\end{aligned}                                                    \tag{14}
\]

The same perfect-matching check gives the three diagonal targets, the six
mixed failures obtained from (12) by the corresponding relabelling, and

\[
\begin{aligned}
 \Omega_0^{pr}&=-(bd)_1(ac)_1(qs)_0,\\
 \Omega_1^{pr}&= +(bd)_1(cq)_2(as)_0.
\end{aligned}                                                    \tag{15}
\]

Again the columns are independent.

At the all-zero four-cut \(p,q,r,s\), with common complement
\(D=\{a,b,c,d\}\), the six direct entries are

\[
                 (A,B,C,E,F,U)=(1,1,0,0,0,1),                   \tag{16}
\]

so \(AU-BF=1\).  The displayed data in the primary note give

\[
 z=(cd)_0+(ac)_1+(ad)_2,\quad
 f=z+(ab)_0,\quad g=z,\quad L=e_0^{(b)},\quad
 N=e_0^{(a)},\quad M=1,                                        \tag{17}
\]

with \(H=t=v=0\).  Direct multiplication gives both connection equations,
the curvature equation, and

\[
 Mf^{[2]}+LHf=X_0^D,\qquad
 Mg^{[2]}+LNg=X_0^D.                                           \tag{18}
\]

This completes the independent audit: the diagonal guard is exact on all
claimed data, and its failure is exactly the six off-diagonal rows.

## 3. What the directed cycle actually supplies

For one six-site chart put

\[
 z_{ij}=p_i s_j,\qquad b_{ij}=a_{ij}/3,\qquad
 B_{ij}=z_{ij}+b_{ij}q.                                        \tag{19}
\]

The normalized full-nine equations are

\[
                    B_{ij}q^{[2]}=\delta_{ij}X_i.               \tag{20}
\]

Thus the six off-diagonal \(B_{ij}\) lie in
\(\operatorname{Ann}(q^{[2]})\).  Source factorization gives the primitive
hexagon identity

\[
                  z_{01}z_{12}z_{20}=z_{02}z_{21}z_{10}.        \tag{21}
\]

It is the only primitive relation among the six off-diagonal products:
their incidence graph is the cycle
\(K_{3,3}\setminus\{00,11,22\}\).

Suppose now that the unary and scalar-zero endpoints also satisfy their
physical rows, so the simplified Omega formulas are valid.  With

\[
                 x=z_{00},\qquad R=-z_{11}-z_{22},\qquad
                 F_0=\sigma q+x,                               \tag{22}
\]

the rank-one response rectangles imply

\[
 xz_{11}=z_{01}z_{10},\qquad xz_{22}=z_{02}z_{20}.               \tag{23}
\]

Consequently

\[
 \boxed{
 \Omega_0
  =-\left(\sigma q+\frac{x}{2}\right)
       \left(z_{01}z_{10}+z_{02}z_{20}\right).}                 \tag{24}
\]

This is the useful exact two-cycle form of the first Omega column.  The
second is

\[
                         \Omega_1=R^{[2]}F_0.                   \tag{25}
\]

Equation (21) does not make (24) proportional to (25).  At six residual
sites both (20) and (21) already live in top degree.  Multiplying either
by another positive-degree class loses all information.  Expanding (21)
in the normalized cells and using only the six relations
\(B_{ij}q^{[2]}=0\) leaves

\[
\begin{aligned}
0={}&B_{01}B_{12}B_{20}-B_{02}B_{21}B_{10}\\
&-q\bigl(
 b_{01}B_{12}B_{20}+b_{12}B_{01}B_{20}+b_{20}B_{01}B_{12}\\
&\hspace{42mm}
 -b_{02}B_{21}B_{10}-b_{21}B_{02}B_{10}-b_{10}B_{02}B_{21}
 \bigr)\\
&-6(b_{01}b_{12}b_{20}-b_{02}b_{21}b_{10})q^{[3]}.              \tag{26}
\end{aligned}
\]

The last notation merely converts the ordinary cube \(q^3\) to
\(6q^{[3]}\).  Formula (26) still contains the uncontrolled top classes
\(B B B\) and \(qBB\).  In particular it is not a linear annihilator
rectangle and contains no diagonal target anchor.  To make (21) interact
with (20), one must first take a literal site coefficient; the product rule
then exposes the overlap/four-cut first jets.  This is the precise degree
at which an anchored Koszul argument has to operate.

## 4. A complementary two-chart off-diagonal guard

We now give literal integral aggregate blocks for which all those
off-diagonal equations hold in both charts while the bad Omega strata
survive.

Use the eight sites

\[
                         \{p,q,r,a,b,c,d,s\}.                    \tag{27}
\]

Every displayed cell is diagonal in its two endpoint colours.  For the
first version take

\[
\begin{array}{c|l}
\text{colour}&\text{pair:weight}\\ \hline
0&pq:6,\ pr:6,\ pa:1,\ pb:1,\ pc:1,\ qr:1,\ qd:1,
   \ qs:6,\ rd:2,\ rs:3,\\
1&pa:1,\ qr:1,\\
2&pb:1,\ qd:1,\ rd:1.
\end{array}                                                       \tag{28}
\]

All undisplayed cells are zero.  Multiple displayed colours on one pair
are simply different diagonal entries of that pair's \(3\times3\) block.

### 4.1 The \(pq\)-chart

On \(W_{pq}=\{r,a,b,c,d,s\}\), one has

\[
\begin{aligned}
 q={}&2(rd)_0+3(rs)_0+(rd)_2,\\
 (P_0,P_1,P_2)={}&
 (e_0^{(a)}+e_0^{(b)}+e_0^{(c)}+6e_0^{(r)},
   e_1^{(a)},e_2^{(b)}),\\
 (S_0,S_1,S_2)={}&
 (e_0^{(r)}+e_0^{(d)}+6e_0^{(s)},
   e_1^{(r)},e_2^{(d)}),\\
 a_{00}^{pq}={}&6,
 \qquad a_{ij}^{pq}=0\quad((i,j)\ne(0,0)).
\end{aligned}                                                    \tag{29}
\]

All terms of \(q\) meet at \(r\), hence

\[
                              q^{[2]}=q^{[3]}=0.                 \tag{30}
\]

The two endpoint triples have rank three.  For instance, the \(c,0\)
coordinate occurs only in \(P_0\), and after its coefficient is killed the
remaining \(P_1,P_2\) lie on different physical axes.  The \(s,0\)
coordinate gives the analogous check for the second endpoint.

Put

\[
 x=P_0S_0,\qquad F_0=6q+x.                                     \tag{31}
\]

Partition the residual sites as

\[
                  A=\{a,b,c\},\qquad B=\{r,d,s\}.              \tag{32}
\]

Every term of \(F_0\) is either an \(A\)-to-\(B\) edge or a
\(B\)-to-\(B\) edge.  A perfect matching on the balanced shores cannot use
a \(B\)-to-\(B\) edge: all three sites of \(A\) would still require three
different sites of \(B\).  The surviving \(A\)-to-\(B\) matrix has row
weights \((1,1,1)\) and column weights \((1,1,6)\).  Its permanent is

\[
                         3!\,(1\cdot1\cdot1)(1\cdot1\cdot6)=36.
                                                                    \tag{33}
\]

Therefore

\[
                         F_0^{[3]}=36X_0=6^2X_0.                \tag{34}
\]

The point \(K_0=E_{00}\) is clean.  At

\[
                    K_1=E_{00}-I=\operatorname{diag}(0,-1,-1)
                                                                    \tag{35}
\]

the direct scalar is zero and the response is

\[
                         R=-(ar)_1-(bd)_2.                       \tag{36}
\]

It has only two edges, so \(R^{[3]}=0\); the scalar-zero binary-target
endpoint is clean.  Notice that this sentence asserts cleanliness, not its
physical binary row.

Because of (30), every off-diagonal physical equation is exact:

\[
             a_{ij}q^{[3]}+P_iS_jq^{[2]}=0
             \qquad(i\ne j).                                  \tag{37}
\]

Indeed, the same left side is zero on the diagonal.  The only failed pair
equations are exactly the three nonzero target equations in (1).

Since the physical scalar-zero row is intentionally absent, use the
unsimplified two-root polarization.  With

\[
                         T_1=-X_1-X_2,                           \tag{38}
\]

it is

\[
 {\cal E}(tK_0+uK_1)
      =t^2u\,\Omega_0+tu^2\,\Omega_1,
 \quad
 \Omega_0=RF_0^{[2]}-36T_1,
 \quad
 \Omega_1=R^{[2]}F_0.                                         \tag{39}
\]

Define the residual coordinate monomials

\[
\begin{aligned}
 Y_1&=(ar)_1e_0^{(b)}e_0^{(c)}e_0^{(d)}e_0^{(s)},\\
 Y_2&=(bd)_2e_0^{(a)}e_0^{(c)}e_0^{(r)}e_0^{(s)},\\
 Z&=(ar)_1(bd)_2(cs)_0.
\end{aligned}                                                    \tag{40}
\]

The same balanced-shore count used in (33) gives exactly

\[
 \boxed{
 \Omega_0^{pq}=36X_1+36X_2-12Y_1-12Y_2,
 \qquad
 \Omega_1^{pq}=6Z.}                                            \tag{41}
\]

The first tensor has nonzero pure coordinates; the second is one mixed
coordinate.  They are nonzero and independent.

### 4.2 The \(pr\)-chart

Deleting \(p,r\) gives

\[
\begin{aligned}
 q'={}&(qd)_0+6(qs)_0+(qd)_2,\\
 (P'_0,P'_1,P'_2)={}&
 (e_0^{(a)}+e_0^{(b)}+e_0^{(c)}+6e_0^{(q)},
   e_1^{(a)},e_2^{(b)}),\\
 (T_0,T_1,T_2)={}&
 (e_0^{(q)}+2e_0^{(d)}+3e_0^{(s)},
   e_1^{(q)},e_2^{(d)}).
\end{aligned}                                                    \tag{42}
\]

Again \((q')^{[2]}=0\), both stars have rank three, and the balanced
cross matrix has column-weight product \(1\cdot2\cdot3=6\).  Thus

\[
                         (6q'+P'_0T_0)^{[3]}=36X_0.             \tag{43}
\]

The scalar-zero response is

\[
                         R'=-(aq)_1-(bd)_2,                     \tag{44}
\]

so \((R')^{[3]}=0\).  All six off-diagonal rows hold and precisely the
three diagonal targets fail.

With the evident primed versions of (40), direct multiplication gives

\[
 \boxed{
 \Omega_0^{pr}=36X_1+36X_2-12Y'_1-6Y'_2,
 \qquad
 \Omega_1^{pr}=3Z'.}                                           \tag{45}
\]

These columns are independent as well.

### 4.3 Curvature and absence of an active clean point

Expose \(p,q,r,s\) in colour zero.  The direct six-tuple is

\[
                         (A,B,C,E,F,U)=(6,6,1,0,6,3),           \tag{46}
\]

and hence

\[
                              AU-BF=18-36=-18\ne0.              \tag{47}
\]

All shared connection and four-cut identities hold automatically because
(28) is one literal aggregate packet, not two independently chosen chart
presentations.  The endpoint-star maps have already been checked in both
charts.

On either line, the direct scalar is \(6t\) and the target coordinates are
\((t,-u,-u)\).  Activity is exactly \(tu\ne0\).  Equations (41) and
(45) show that \(t\Omega_0+u\Omega_1\) cannot vanish for such a point.
Thus neither chart has an active clean point.

## 5. A stronger exactly-one-zero variant

The endpoint-degenerate version can retain a nonzero common-power row and
the unary diagonal target.  Use the following literal rational cells:

\[
\begin{array}{c|l}
\text{colour}&\text{pair:weight}\\ \hline
0&pq:6,\ pr:6,\ pa:1,\ pb:1,\ pc:1,\ qr:1,\ qd:1,
   \ qs:6,\ rd:-1,\ rs:-6,\ ab:-1/12,\\
1&pa:1,\ qr:1,\\
2&pb:1,\ qr:1.
\end{array}                                                       \tag{48}
\]

All other cells vanish.  In the \(pq\)-chart,

\[
 q=-\frac1{12}(ab)_0-(rd)_0-6(rs)_0,
 \qquad
 q^{[2]}=\frac1{12}(ab)_0(rd)_0
             +\frac12(ab)_0(rs)_0\ne0.                         \tag{49}
\]

The endpoint rows are

\[
\begin{aligned}
(P_0,P_1,P_2)&=
 (e_0^{(a)}+e_0^{(b)}+e_0^{(c)}+6e_0^{(r)},
   e_1^{(a)},e_2^{(b)}),\\
(S_0,S_1,S_2)&=
 (e_0^{(r)}+e_0^{(d)}+6e_0^{(s)},
   e_1^{(r)},e_2^{(r)}).
\end{aligned}                                                    \tag{50}
\]

Every monomial of \(q^{[2]}\) contains \(a,b,r\).  Hence every
off-diagonal response product meets it: the \(P_0S_1,P_0S_2\) rows meet
\(r\), the \(P_1S_j\) rows meet \(a\), and the \(P_2S_j\) rows meet
\(b\).  Therefore all six off-diagonal equations hold.  Also
\(q^{[3]}=0\).

The unary row is exact, not merely clean.  The two terms of (49) leave,
respectively, the response edges \((cs)_0\) and \((cd)_0\).  Their
coefficients are

\[
             \frac1{12}\cdot6=\frac12,
 \qquad
             \frac12\cdot1=\frac12.
\]

Thus

\[
                              P_0S_0q^{[2]}=X_0.                \tag{51}
\]

Moreover, in \(F_0=6q+P_0S_0\), the \(rd\) and \(rs\) coefficients
cancel:

\[
       6(-1)+6(1)=0,\qquad 6(-6)+6(6)=0.                        \tag{52}
\]

The remaining graph consists of the complete \(A\)-to-\(B\) response
with column weights \((1,1,6)\), together with the \(A\)-internal edge
\(-\tfrac12(ab)_0\).  A perfect matching cannot use that internal edge
because there is no \(B\)-internal edge.  Hence

\[
                              F_0^{[3]}=36X_0.                  \tag{53}
\]

In the \(pr\)-chart,

\[
 q'=-\frac1{12}(ab)_0+(qd)_0+6(qs)_0,
 \qquad
 (q')^{[2]}=-\frac1{12}(ab)_0(qd)_0
             -\frac12(ab)_0(qs)_0.                             \tag{54}
\]

The second endpoint rows are

\[
 (T_0,T_1,T_2)=
 (e_0^{(q)}-e_0^{(d)}-6e_0^{(s)},e_1^{(q)},e_2^{(q)}).
\]

The same collision proof gives the six off-diagonal rows.  The two terms
of (54), completed by \((cs)_0\) of weight \(-6\) and \((cd)_0\) of
weight \(-1\), again contribute \(1/2+1/2\), so the unary physical row is
\(X_0\).  The \(qd,qs\) terms cancel from \(6q'+P'_0T_0\), and the
surviving cross matrix has column-weight product
\(1\cdot(-1)\cdot(-6)=6\).  Thus its clean unary value is again
\(36X_0\).

The scalar-zero responses are

\[
 R=-(ar)_1-(br)_2,\qquad R'=-(aq)_1-(bq)_2.                     \tag{55}
\]

Their terms meet at \(r\), respectively \(q\).  Consequently

\[
 R^{[2]}=(R')^{[2]}=0,
 \qquad
 \Omega_1^{pq}=\Omega_1^{pr}=0,
 \qquad
 \Omega_0^{pq}\ne0,\quad\Omega_0^{pr}\ne0.                    \tag{56}
\]

The nonvanishing follows already from the unchanged pure component
\(36X_1+36X_2\) of \(\Omega_0\).  The two missing diagonal responses
annihilate (49), respectively (54), so the only failed pair equations are
the \(X_1\) and \(X_2\) anchors.

Finally, the all-zero four-cut data are

\[
                 (A,B,C,E,F,U)=(6,6,1,0,6,-6),
 \qquad AU-BF=-72\ne0.                                        \tag{57}
\]

Thus even nonzero \(q^{[2]}\), the unary diagonal target, all six
off-diagonal rows, two-chart curvature, and four good stars do not exclude
the exactly-one-zero Omega stratum.  The missing inputs are specifically
the two complementary diagonal targets comprising the scalar-zero binary
row.

## 6. Complementarity of the two exact guards

The two packets establish the following sharp comparison.

| retained datum | diagonal-row guard | independent off-diagonal guard | endpoint-degenerate guard |
|---|---:|---:|---:|
| literal overlapping aggregate blocks | yes | yes | yes |
| nonzero \(AU-BF\) | yes | yes | yes |
| four rank-three endpoint stars | yes | yes | yes |
| both clean endpoints in both charts | yes | yes | yes |
| nonzero \(q^{[2]}\) | yes | no | yes |
| unary physical target row | yes | no | yes |
| binary diagonal target rows | yes | no | **no** |
| six off-diagonal physical rows | **no** | yes | yes |
| independent Omega columns | yes | yes | no |
| exactly one zero Omega column | not tested | no | yes |

Consequently neither the diagonal ideal nor the off-diagonal ideal,
localized at curvature, good stars, and the clean endpoints, contains the
bad-Omega locus set-theoretically.  Only their anchored interaction can do
so.  At the six-site boundary this interaction cannot be obtained by
multiplying the uncontracted top equations: all such products are already
beyond top degree.  A proof must take a site coefficient first and retain
the resulting diagonal target term through the overlap connection.

## 7. Is this the same anchored Koszul \(H^1\) obstruction?

At the structural level, **yes**.  At the level needed for a proof, the
identification is not yet complete.

There are three exact similarities.

1. The six off-diagonal labels form the bipartite six-cycle
   \(K_{3,3}\setminus\{00,11,22\}\).  Its primitive toric/Koszul
   one-cycle is (21).  The three omitted diagonal cells are exactly the
   fixed physical anchors.
2. On an overlap of pair charts, the normalized quadratic representatives
   obey the literal connection

   \[
    B_{pq}^{ij}t_k-B_{pr}^{ik}y_j
       ={a_{pq}^{ij}t_k-a_{pr}^{ik}y_j\over3}\,z.                \tag{58}
   \]

   Homogeneous corrections therefore form a Cech/Koszul one-cocycle, and
   the four-cut curvature is its first two-dimensional coefficient.
3. Under oblique endpoint gauges \(G,H\in\operatorname{GL}_3\), the target
   rows transform as

   \[
    \widetilde B_{kl}q^{[2]}
        =\sum_iG_{ki}H_{li}X_i.                                 \tag{59}
   \]

   Thus the off-diagonal system alone allows flag drift, whereas the three
   diagonal anchors fix the physical coordinate flags.  This is the same
   gauge freedom measured by the normalized matrix
   \(C=G^{-\mathsf T}aH^{-1}\) in the cross-word Riccati--leakage identity.

So the diagonal rows kill the same **oblique flag gauge** that appears in
the cross-word guard.  What has not been proved is that a simultaneous bad
pair \((\Omega_0,\Omega_1)\) defines a nonzero class in that overlap
\(H^1\), or that the coefficient-cut map from the Omega pencil into this
class is injective on the curvature open set.  The two guards show exactly
why this missing chain map matters:

* the diagonal-row guard has the anchors but its six putative
  annihilator representatives are not cycles; and
* the independent off-diagonal guard has the cycles, but \(q^{[2]}=0\)
  removes every diagonal anchor and makes the annihilator module maximally
  nonfaithful; and
* the endpoint-degenerate guard has \(q^{[2]}\ne0\) and the unary anchor,
  but still survives until the two binary diagonal anchors are imposed.

Accordingly, it would be premature to state that the Omega obstruction
*is already proved to be* the cross-word \(H^1\) class.  The defensible
statement is sharper: both problems are manifestations of the same
anchored gauge complex, and the missing theorem is the injective
coefficient-cut comparison between them.

One sufficient next lemma is therefore:

> **Anchored overlap-injectivity lemma.**  On the open locus with
> \(AB(AU-BF)\ne0\) and four good endpoint stars, take the literal first
> site coefficients of the six relations
> \(B_{ij}q^{[2]}=0\), transport them by (58), and retain the three
> diagonal coefficients \(B_{ii}q^{[2]}=X_i\).  The resulting anchored
> overlap class cannot contain two simultaneous independent Omega pencils
> or an endpoint-degenerate Omega pencil in both charts.

Unlike an assertion based only on the hexagon, this lemma uses exactly the
information separated by the two guards.  Proving it would establish the
full-nine Omega-incidence lemma and hence give an active clean point on at
least one of the two lines.  No such injectivity proof is supplied here.

The lightweight standard-library verifier
[`verify_curved_two_chart_anchor_complementarity.py`](../computations/verify_curved_two_chart_anchor_complementarity.py)
expands only the displayed sparse packets.  It checks all chart rows, four
star ranks, both clean endpoints, both Omega strata, and the two curvature
values over `fractions.Fraction`; it performs no support search or symbolic
elimination.
