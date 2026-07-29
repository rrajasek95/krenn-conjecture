# Four singular cross blocks cannot form a transversal matching

## 1. Result

Let the two shores of the two-(K_4) chart be indexed by
({0,1,2,3}), and let (B_{ij}) be the (3\times3) cross block from
left site (i) to right site (j).

**Theorem 1.1.**  There is no exact two-(K_4) realization for which

\[
                  \det B_{ii}=0\quad(0\le i<4),
 \qquad            \det B_{ij}\ne0\quad(i\ne j).        \tag{1}
\]

Thus the exactly-four-singular position orbit which is a (4\times4)
perfect matching is closed for arbitrary singular ranks and arbitrary
entries.  The proof is field-uniform in characteristic zero and uses the
actual mixed two-/four-cross equations.  No projective-row relaxation,
dead-slab equation, or target normalization at a constant block word is
needed.

The new ingredient is an eight-cell strengthening of the pair-Hessian
erasure lemma.  Each of its two stars may have one arbitrary singular
site, provided the two exceptional sites are distinct.  Vanishing on the
eight input cells outside one prescribed cell still forces the effective
quadratic to vanish.

## 2. Separated-defect eight-cell erasure

Let

\[
 \mathcal R=\bigotimes_{i=0}^3(\mathbb C\oplus V_i),
 \qquad V_i^2=0,
 \qquad \dim V_i=3.                                    \tag{2}
\]

Let (U,V) be three-spaces, let

\[
 P_i:U\longrightarrow V_i,
 \qquad S_i:V\longrightarrow V_i,                      \tag{3}
\]

and put

\[
 p(x)=\sum_iP_ix,
 \qquad s(y)=\sum_iS_iy.                               \tag{4}
\]

For (q\in\mathcal R_2), its pulled-back pair Hessian is

\[
                         \beta_q(x,y)=q,p(x)s(y)\in\mathcal R_4.  \tag{5}
\]

**Lemma 2.1 (separated-defect eight-cell erasure).**  Fix distinct sites
(r,s).  Suppose

\[
 P_i\text{ is invertible for }i\ne r,
 \qquad S_i\text{ is invertible for }i\ne s,            \tag{6}
\]

with no hypothesis on (P_r,S_s).  If nonzero covectors
(ell\in U^*,m\in V^*) satisfy

\[
                 \beta_q(x,y)=0
       \quad\hbox{whenever}\quad \ell(x)m(y)=0,         \tag{7}
\]

then (q=0).

In coordinates with (ell=x_0) and (m=y_0), condition (7) erases the
eight cells ((a,b)\ne(0,0)).  Unlike the six-cell lemma, neither star is
required to be invertible at all four sites.

### 2.1 The square-free Koszul calculation

Put (K=\ker\ell) and (T=\{0,1,2,3\}\setminus\{r\}).  We first use
only the six cells (K\times V).  The following elementary calculation is
the separated-defect form of the usual three-site Koszul kernel:

\[
 \left\{q:q,p(x)s(y)=0\ (x\in K,y\in V)\right\}
 =\begin{cases}
     0,&P_rK\ne0,\\[1mm]
     \mathbb C\Omega_{K,T},&P_rK=0.
   \end{cases}                                          \tag{8}
\]

Here, for a basis (u,v) of (K), the only nonzero blocks of
(Omega_{K,T}) are the three edges of (T=\{i,j,k\}):

\[
\begin{aligned}
 (\Omega_{K,T})_{ij}
   &=-\bigl(P_iu\otimes P_jv-P_iv\otimes P_ju\bigr),\\
 (\Omega_{K,T})_{ik}
   &= \phantom{-}\bigl(P_iu\otimes P_kv-P_iv\otimes P_ku\bigr),\\
 (\Omega_{K,T})_{jk}
   &=-\bigl(P_ju\otimes P_kv-P_jv\otimes P_ku\bigr).
                                                               \tag{9}
\end{aligned}
\]

The simultaneous sign is immaterial.

For completeness, (8) can be checked without a genericity assumption.
Apply inverse duals at the three regular (S)-sites and expand first in a
basis of (V), then in (u,v).  The coefficients split as follows:

\[
\begin{array}{c|c|c}
\text{quadratic blocks}&\text{number of coordinates}&
                         \text{kernel after elimination}\\ \hline
\text{three edges meeting }r&27&0\\
\text{three edges inside }T&27&\bigwedge^2K\\
\text{compatibility at }r&1&
       0\text{ if }P_rK\ne0.
\end{array}                                             \tag{10}
\]

On the middle row, the three remaining equations are precisely the
length-three Koszul equations.  Their common solution is (9).  Inserting
the fourth site gives (P_rx) times that common exterior coefficient and
therefore kills it unless (P_rK=0).  Every elimination in the first row
uses one of the isomorphisms in (6); the possibly singular map (S_s)
only contributes already-eliminated terms.  This proves (8).  It also
directly verifies

\[
                         \Omega_{K,T}p(x)=0\qquad(x\in K).           \tag{11}
\]

This is a coefficient proof over every characteristic-zero field, not a
rank-at-a-generic-point argument.

### 2.2 The last two cells kill the Koszul residual

If the first case of (8) holds, there is nothing left to prove.  Suppose
(P_rK=0) and (q=\lambda\Omega_{K,T}).  Choose (x_0\notin K).  The
component of
(Omega_{K,T}p(x_0)) with hole (r) is the nonzero alternating tensor

\[
 \operatorname {Alt}
       (P_iu\otimes P_jv\otimes P_kx_0)                 \tag{12}
\]

on the three sites of (T).  It is nonzero because every (P_t),
(t\in T), is invertible and (u,v,x_0) is a basis.

The plane (S_r(\ker m)) has dimension two, while (P_rx_0) spans at
most a line.  Choose (y\in\ker m) and
(eta\in V_r^*) such that

\[
                         \eta(P_rx_0)=0,
 \qquad                  \eta(S_ry)\ne0.               \tag{13}
\]

This uses (r\ne s), so (S_r) is invertible.  Contract
(Omega_{K,T}p(x_0)s(y)) at site (r) by (eta).  Terms in which
(p(x_0)) occupies (r) vanish by the first equation in (13).  The
hole-(r) term (12) is multiplied by the nonzero second scalar in (13).
Thus

\[
                         \Omega_{K,T}p(x_0)s(y)\ne0.     \tag{14}
\]

But (m(y)=0), so (7) says that (14) must vanish.  Hence
(lambda=0), proving Lemma 2.1.

## 3. The effective quadratic of one left factor edge

Let (kappa(ab)) be the colour of an internal (K_4) edge.  Its pure
internal weight is nonzero; denote the left weight by (lambda_{ab}) and
the right weights by (ho_{uv}).  Fix a left factor edge (ab), put

\[
                         c=\kappa(ab),
 \qquad \{r,s\}=\{0,1,2,3\}\setminus\{a,b\}.            \tag{15}
\]

On the four right sites define the row stars

\[
                         p_{i,x}=\sum_{j=0}^3
                           \operatorname {row}_x(B_{ij})^{(j)}       \tag{16}
\]

and the weighted right-shore quadratic

\[
                         q_R=\sum_{uv}\rho_{uv}
                                  E_{\kappa(uv),\kappa(uv)}^{(uv)}.  \tag{17}
\]

Set

\[
                         q_{\rm eff}
                 =\lambda_{ab}q_R+p_{a,c}p_{b,c}.       \tag{18}
\]

Fix the left colours at (a,b) to (c), and let the colours at (r,s)
be (x,y).  Direct grouping of matchings gives the exact identity

\[
 \boxed{\quad
   \beta_{q_{\rm eff}}(p_{r,x},p_{s,y})
      =\text{the complete two-/four-cross coefficient on the right shore}.
      \quad}                                             \tag{19}
\]

The (q_R) term chooses the right internal edge and hence the two-cross
sector; the product term supplies all four cross edges.

If ((x,y)\ne(c,c)), the left word is nonconstant and (ab) is its only
compatible internal edge.  It has neither a zero-cross contribution nor
a target coefficient.  Therefore the actual matching-tensor equations
give

\[
                 \beta_{q_{\rm eff}}(p_{r,x},p_{s,y})=0
                         \qquad((x,y)\ne(c,c)).          \tag{20}
\]

This is the full eight-cell hypothesis, not a dead-word relaxation.

## 4. Application to the diagonal singular support

Regard (x\mapsto p_{r,x}) and (y\mapsto p_{s,y}) as the two stars in
Lemma 2.1.  At right site (j), their component maps are the row maps of
(B_{rj}) and (B_{sj}).  Under (1),

* the first star is invertible at every (j\ne r), with arbitrary
  singular component at (r);
* the second is invertible at every (j\ne s), with arbitrary singular
  component at (s).

The defects are separated because (r\ne s).  Equation (20), with
(ell=m=e_c^*), and Lemma 2.1 now force

\[
                              q_{\rm eff}=0.             \tag{21}
\]

This is impossible.  At a fixed right site (j), the endpoint images of
the three incident blocks of (lambda_{ab}q_R) are the three distinct
coordinate lines

\[
                         \mathbb Ce_{\kappa(jk)}
                              \qquad(k\ne j),             \tag{22}
\]

and all three coefficients are nonzero.  They span (V_j).  Every block
of (p_{a,c}p_{b,c}), on the other hand, has its endpoint-(j) image in

\[
 \operatorname {span}\bigl(operatorname {row}_c(B_{aj})^{\mathsf T},
                            \operatorname {row}_c(B_{bj})^{\mathsf T}\bigr),
                                                               \tag{23}
\]

which has dimension at most two.  Equality (21) would put all three lines
in (22) inside (23), a contradiction.  This proves Theorem 1.1.

## 5. Exact-five corollary and exact-six frontier

The erasure theorem also removes the whole exactly-five-singular stratum.
First combine Proposition 5.1 of
[`two-k4-exact-four-nonmatching-obstruction.md`](two-k4-exact-four-nonmatching-obstruction.md)
with its transpose.  Five singular positions must meet all four block rows
and all four block columns: if a row were empty, one of the other three
rows would have degree at most one, giving a completely invertible row
paired with a row having at most one singular block.  Thus both degree
partitions are

\[
                              (2,1,1,1).                 \tag{24}
\]

Among the three singleton rows, two have their singular blocks in distinct
columns.  Otherwise one column would contain all three and violate the
column partition (24).  Use those two singleton rows as the complementary
rows (r,s) in Section 3.  Their unique singular components are at
distinct right sites, so Lemma 2.1 applies and gives the same contradiction
(21)--(23).  Hence

\[
          \boxed{\#\{(i,j):\det B_{ij}=0\}\ge6.}          \tag{25}
\]

For the next boundary, impose only the one-defect and separated-defect
erasure consequences, on rows and columns.  Exact enumeration of the
(\binom{16}{6}=8008) supports leaves (256) labelled supports in three
(S_4\times S_4\times C_2) orbits:

\[
\begin{array}{c|c|c|c|l}
 &\text{orbit size}&\text{row degrees}&\text{column degrees}&
                                  \text{representative}\\ \hline
E_0&16 &(3,1,1,1)&(3,1,1,1)&
  00,01,02,13,23,33\\
E_1&144&(2,2,2,0)&(2,2,1,1)&
  00,01,10,11,22,23\\
E_2&96 &(2,2,2,0)&(2,2,2,0)&
  00,01,10,12,21,22.
\end{array}                                             \tag{26}

Here (E_0) is a disjoint (K_{1,3}\sqcup K_{3,1}), (E_1) is a
(K_{2,2}) plus a two-edge star and an empty row, and (E_2) is a
six-cycle with one empty row and column.  Equation (26) is a position
classification only.  These three supports are the sharply isolated
exact-six residual for the next mixed-sector analysis.

## 6. Exact audit

[`verify_two_k4_four_singular_matching_hessian_obstruction.py`](../computations/verify_two_k4_four_singular_matching_hessian_obstruction.py)
constructs the (54)-column erased-Hessian coefficient map.  It verifies
rank (54) for every canonical zero/rank-one/rank-two separated-defect
case, checks the one-dimensional six-cell Koszul residual and its removal
by the last two cells, and exhibits a (54\times54) minor of determinant
(-1) in the maximally defective specialization.  It also checks all
(729) coefficients of (19) for an exact diagonal-singular block array
and audits the final three-lines-versus-two-plane obstruction.  Finally it
enumerates every exact-five and exact-six support, verifies that no
exact-five support survives, and reconstructs the three orbits (26).
