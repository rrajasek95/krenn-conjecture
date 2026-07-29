# Five zero-cross witnesses do not close a live component

## 1. Outcome

The five-witness theorem and the complete-live-component propagation admit
an exact common counterconfiguration at every even order \(n\ge 10\).
It is stronger than a bare incidence example.  For one deleted pair
\(p,q\), it has:

1. the exact row--column-avoiding four-plane of quotient relations;
2. a connected, spanning, nonbipartite rank-three graph;
3. one complete live component \(U\), separated through literal
   two-star-zero sites;
4. all six deleted-star rows supported on at least three sites;
5. nonzero internal top power \(Q\);
6. vanishing Hessian response for all nine products \(p_cs_d\); and
7. for every live edge \(ij\subset U\), exactly the same outside set
   \(Z\) is its zero-cross witness set, with \(|Z|\ge5\).

Thus no counting or overlap argument based only on the five-witness sets
can exclude a live component, even when all those sets coincide.  The
construction fails the full target precisely at the three diagonal cap
values: its nine product Hessians vanish, whereas the three pure target
tensors are independent.  This confirms that a uniform closure must use
the values in the diagonal identities, not another witness count.

## 2. Common algebra

Fix

\[
 \Delta=\operatorname {diag}(2,3,5),\qquad
 H=\begin{pmatrix}0&1&2\\1&0&3\\2&3&0\end{pmatrix}.
                                                               \tag{1}
\]

Both matrices are invertible, \(H\) is symmetric and zero diagonal, and

\[
 T_\Delta(M)=M\Delta+\Delta M^{\mathsf T},\qquad
 {\mathscr D}=T_\Delta^{-1}(\mathbb C H)\subset Z_0            \tag{2}
\]

define the standard four-dimensional relation space.  It avoids every
coordinate row and column two-plane.

On the internal site set \(W=B\setminus\{p,q\}\), choose a partition

\[
                            W=U\sqcup Z.                       \tag{3}
\]

Put

\[
 P_u=I,\quad S_u=\Delta\quad(u\in U),\qquad
 P_z=S_z=0\quad(z\in Z).                                     \tag{4}
\]

Every one of the six star rows therefore reaches exactly \(|U|\) sites.
The block graph and site signs will be chosen so that

\[
 q_{uv}=H/2\quad(u,v\in U,\ u\ne v),                         \tag{5}
\]

while every other nonzero block equals \(H\).  All unlisted blocks are
zero.

For \(M\in{\mathscr D}\), write \(T_\Delta(M)=tH\).  Assign a sign
\(\epsilon_x\in\{+1,-1\}\) to each internal site and put
\(\alpha_x=t\epsilon_x\).  We choose the graph so that

\[
 \epsilon_u=+1\quad(u\in U),\qquad
 \sum_{x\in W}\epsilon_x=0,                                \tag{6}
\]

and every non-\(U\) edge joins opposite signs.  Then, on every site pair,

\[
 P_iMS_j^{\mathsf T}+S_iM^{\mathsf T}P_j^{\mathsf T}
                 =(\alpha_i+\alpha_j)q_{ij}.                \tag{7}
\]

On a \(U\)-pair this is \(tH=2t(H/2)\); away from \(U\) both sides
vanish.  The weights in (6) sum to zero, so (7) is an honest vertex
gauge.  Conversely, restriction to any \(U\)-edge shows that a
zero-diagonal combination can be a gauge only if
\(T_\Delta(M)\in\mathbb C H\).  Hence (2) is the exact relation
four-plane, not merely a selected subspace.

Every \(U\)-edge is live.  Every other displayed rank-three edge is dead:
its relation-line image is zero.  This is exactly the zero-cut normal form
from the live-component theorem.

## 3. All orders \(n\ge12\)

Write

\[
                  |W|=2r,\qquad |U|=|Z|=r\ge5,
 \qquad U=\{u_1,\ldots,u_r\},\quad Z=\{z_1,\ldots,z_r\}.    \tag{8}
\]

Give every \(u_i\) sign \(+1\), every \(z_i\) sign \(-1\), retain the
complete \(U\)-graph (5), and add only the \(r\) blocks

\[
                            q_{u_i z_i}=H.                   \tag{9}
\]

The rank-three graph is a clique with one leaf at every clique vertex.  It
is connected, spanning, and nonbipartite.  Its unique perfect matching is
\(\{u_i z_i:1\le i\le r\}\), so

\[
                              Q=q^r/r!\ne0.                 \tag{10}
\]

Deleting any two vertices of \(U\) isolates their two matched leaves.
Consequently the complement of every pair in \(U\) has no perfect matching.
Since every product \(p_cs_d\) is supported on \(U\)-pairs, this proves

\[
                         {\mathcal H}_q(p_cs_d)=0
                         \qquad(0\le c,d\le2).              \tag{11}
\]

Now re-delete a live edge \(u_i u_j\).  The original deleted sites \(p,q\)
give, for each color \(c\), invertible conjugates of the rank-two
alternating matrix \(K_c\); they are not witnesses.  A third site
\(u_k\in U\setminus\{u_i,u_j\}\) likewise gives

\[
        (H/2)K_c(H/2)^{\mathsf T},
\]

which has rank two.  At a leaf \(z_k\), at most one of
\(q_{u_i z_k},q_{u_j z_k}\) is nonzero.  Hence

\[
 q_{u_i z_k}K_cq_{u_j z_k}^{\mathsf T}=0
 \qquad\text{for every }c,                                 \tag{12}
\]

and therefore

\[
                              \Omega_{u_i u_j}=Z.           \tag{13}
\]

All live edges have the same \(r\ge5\) triple-witness sites.  There is no
incidence expansion as the live edge varies.

## 4. The sharp order-ten case

For \(n=10\), the internal set has eight sites.  Take

\[
 U=\{u_0,u_1,u_2\},\qquad
 Z=\{z_0,z_1,z_2,z_3,z_4\},                               \tag{14}
\]

with signs

\[
 (\epsilon_{u_0},\epsilon_{u_1},\epsilon_{u_2})=(1,1,1),
 \qquad
 (\epsilon_{z_0},\ldots,\epsilon_{z_4})=(-1,-1,-1,-1,1).
                                                                  \tag{15}
\]

Besides the \(U\)-triangle, put \(H\) on

\[
 u_0z_0,\quad u_1z_1,\quad u_2z_2,\quad u_0z_3,\quad z_3z_4.
                                                                  \tag{16}
\]

Every edge in (16) joins opposite signs, so (7) still holds and the
zero-sum condition follows from (15).  The graph is connected, spanning,
and nonbipartite.  It has the unique perfect matching

\[
                         u_0z_0\mid u_1z_1\mid
                         u_2z_2\mid z_3z_4,                 \tag{17}
\]

so again \(Q\ne0\).  Removing any two vertices of \(U\) destroys every
perfect matching, proving (11).  Each \(z_k\) is adjacent to at most one
vertex of \(U\), so the same calculation as (12) gives

\[
                         \Omega_{u_i u_j}=Z,\qquad |Z|=5.  \tag{18}
\]

This realizes equality in the uniform five-witness bound.

## 5. Exact boundary exposed

Take the direct \(p q\) block to have zero off-diagonal entries.  Equations
(11) then satisfy all six off-diagonal cap equations.  The three diagonal
equations would instead read

\[
                              a_{cc}Q=X_c
                              \qquad(c=0,1,2).              \tag{19}
\]

Because \(Q\ne0\) and the three \(X_c\) are independent, (19) is
impossible.  Thus the example does not claim a target realization.
It proves the sharper negative statement needed for the propagation route:
the exact relation geometry, common-power combinatorics, nonzero top power,
dense rows, and all five-witness overlaps remain mutually consistent.
Only the diagonal target values see the contradiction.

The exact audit is
[verify_live_component_five_witness_counterconfiguration.py](../computations/verify_live_component_five_witness_counterconfiguration.py).
It checks the relation four-plane and row--column avoidance, every gauge
block, graph connectivity and oddness, uniqueness of the top perfect
matching, absence of every Hessian complement matching, and the exact
witness equality (13) for orders \(10,12,14,16,18\).
