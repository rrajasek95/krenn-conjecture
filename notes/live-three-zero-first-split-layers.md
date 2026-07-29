# The first two split-exception layers are injective

## 1. Outcome

Continue from
[live-three-zero-two-marked-exceptional-beta.md](live-three-zero-two-marked-exceptional-beta.md)
and
[live-three-zero-all-exceptional-five-live.md](live-three-zero-all-exceptional-five-live.md).
Let the residual have \(2r-1\) live sites, two type-\(10\) centres, the
shared zero \(z_0\), and no additional nonzero singular sites.  Let \(t\)
live sites have beta value different from the common centre value
\(\mu\).

**Theorem 1.1 (first split layers).**  If

\[
                         t=r+2\quad\text{or}\quad t=r+3,           \tag{1}
\]

then the vanishing cyclic response forces every residual nonzero-to-
\(z_0\) block to vanish.  Consequently \(z_0\) is isolated in
\(G_3(q)\), a contradiction.

The first case in (1) occurs for \(r\ge3\), and the second for \(r\ge4\).
Together with the earlier cancellation-free arguments, this closes every
no-extra-singular stratum with

\[
                              0\le t\le r+3.                       \tag{2}
\]

In particular, all strata at live size \(2r-1\le7\) are now closed.
The first remaining range is \(t\ge r+4\), which can occur only for
\(r\ge5\).  Its first case \(r=5,t=9\) is closed by the coupled
incidence argument in
[live-three-zero-all-exceptional-nine-live.md](live-three-zero-all-exceptional-nine-live.md).
For arbitrary \(r\ge5\), the pairwise-distinct exceptional-beta stratum
of the boundary layer \(t=r+4\) is closed by the confluent Borchardt and
residue argument in
[live-three-zero-third-split-distinct-beta.md](live-three-zero-third-split-distinct-beta.md).
Its collision strata are closed by the initial-jet argument in
[live-three-zero-third-split-collision-beta.md](live-three-zero-third-split-collision-beta.md).
Thus the entire third split layer \(t=r+4\) is now closed.
The first case of the fourth split layer,
\(r=6,t=11\), is closed on every collision stratum in
[live-three-zero-all-exceptional-eleven-live.md](live-three-zero-all-exceptional-eleven-live.md).
The full fourth split layer \(t=r+5\) is closed uniformly in
[live-three-zero-fourth-split-layer.md](live-three-zero-fourth-split-layer.md).

## 2. Complete response and the singleton-active split

Normalize each live matrix to \(I\) and the two type-\(10\) matrices to
\(D=\operatorname {diag}(1,1,0)\).  The \(t\) exceptional sites
\(E=\{y_1,\ldots,y_t\}\), with beta values \(\nu_i\ne\mu\), have zero
star blocks:

\[
                         (\nu_i-\mu)q_{y_i z_0}=0.                 \tag{3}
\]

The possible star sites form

\[
 A=\{\text{common-beta live sites}\}
       \sqcup\{\text{two type-}10\text{ centres}\},\qquad
 |A|=2r+1-t.                                                       \tag{4}
\]

For completeness, fix a coordinate at \(z_0\), write the corresponding
active star entries as \(Z_{i,w_i}\), and let \(V=E\sqcup A\).  For a
word \(w\) and source colours \(a,b\), the entire linear star response
has the form

\[
\begin{aligned}
 E_{w;a,b}
 ={}&B_{ab}\sum_{i\in A}Z_{i,w_i}\,
       \operatorname {haf}Q[w]_{V\setminus\{i\}}\\
 &+\sum_{\{u,v\}\subset V}
   \bigl(
    (P_u)_{w_u a}(P_v)_{w_v b}
    +(P_u)_{w_u b}(P_v)_{w_v a}
   \bigr)
   \sum_{\substack{i\in A\\i\notin\{u,v\}}}
      Z_{i,w_i}\,
      \operatorname {haf}Q[w]_{V\setminus\{u,v,i\}} .             \tag{5}
\end{aligned}
\]

The first line is the direct coordinate-factor term; the second contains
every marked pair.  The proof uses \(a=b=2\).  Since \(B_{22}=0\), the
direct term in (5) vanishes exactly, rather than being omitted.

Put

\[
 p=r-1,\qquad s=t-r-1,\qquad k=2r-t.
\]

In the two cases (1),

\[
             s\in\{1,2\},\qquad k=p-s,\qquad |A|=k+1.             \tag{6}
\]

Fix \(R\subset E\) with \(|R|=s\).  The complement \(E\setminus R\)
has \(r+1=p+2\) sites.  Choose

\[
 L\subset E\setminus R,\quad |L|=p,\qquad
 B=E\setminus(R\sqcup L),\quad |B|=2.                             \tag{7}
\]

Give the two sites in \(B\) colour \(2\) and read \(x_2z_2\), making
\(B\) the unique marked pair.  For a target \(i\in A\), give
\(L\sqcup\{i\}\) colour \(0\) and
\(R\sqcup(A\setminus\{i\})\) colour \(1\).  After removing \(B\) and
the target star, both shores have size \(p\).  If the star is at another
active site, the shore sizes are \(p+1\) and \(p-1\), so its coefficient
is zero.  This isolates \(Z_{i,0}\).

Define

\[
 a_\ell={1\over\nu_\ell+\mu},\qquad
 H_{\ell c}={\nu_\ell+\mu\over\nu_\ell+\nu_c}
        \quad(\ell\in L,\ c\in R).                               \tag{8}
\]

Every quantity in (8) is nonzero by the live--centre and live--live
structural equations.  Expanding the cofactor by the \(s\) columns
indexed by \(R\), while the other \(k\) columns all have beta \(\mu\),
gives the exact pivot

\[
 C_{L\mid R}
 =2h_{01}^{\,p}k!
   \left(\prod_{\ell\in L}a_\ell\right)
   \sum_{\substack{J\subset L\\|J|=s}}
       \operatorname {per}H[J,R].                                \tag{9}
\]

All terms in the cofactor are present in (9), including repeated
exceptional beta values.

Swapping binary colours isolates \(Z_{i,1}\) with the same pivot.  To
handle \(Z_{i,2}\), give \(i\) colour \(2\), retain \(B\) in colour
\(2\), and keep \(L\) and \(R\sqcup(A\setminus\{i\})\) in colours
\(0\) and \(1\).  The coefficient from marked pair \(B\) is again (9).
If \(i\) is live, marked pairs involving \(i\) contribute only already
vanishing row-one active stars or exceptional stars; if \(i\) is a
type-\(10\) centre, its third marked factor is zero.  Thus any one split
with \(C_{L\mid R}\ne0\) kills all three rows at every active site.

## 3. The layer \(t=r+2\)

Here \(s=1\).  Write \(R=\{c\}\).  Apart from the nonzero prefactor in
(9), the candidate pivot is

\[
                            G_L=\sum_{\ell\in L}H_{\ell c}.        \tag{10}
\]

Let \(N=E\setminus R\), so \(|N|=p+2\), and let \(L\) range over all
\(p\)-subsets of \(N\).  The inclusion matrix of \(p\)-subsets against
points has full column rank in characteristic zero.  If every \(G_L\)
vanished, it would force

\[
                              H_{\ell c}=0\qquad(\ell\in N),
\]

contradicting (8).  Therefore at least one isolated-star pivot is
nonzero.  This argument is uniform for every \(r\ge3\).

For \(r=4,t=6\), one has \(p=3,k=2\), and the symbolic pivot is

\[
 C_{L\mid c}
 =4h_{01}^{\,3}
   \left(\prod_{\ell\in L}{1\over\nu_\ell+\mu}\right)
   \sum_{\ell\in L}{\nu_\ell+\mu\over\nu_\ell+\nu_c}.             \tag{11}
\]

## 4. The layer \(t=r+3\)

Here \(s=2\).  Write \(R=\{c,d\}\), and for
\(\{\ell,m\}\subset N=E\setminus R\) put

\[
 f_{\ell m}
  =\operatorname {per}H[\{\ell,m\},R]
  =H_{\ell c}H_{m d}+H_{\ell d}H_{m c}.                          \tag{12}
\]

The normalized candidate pivot is

\[
                         G_L=\sum_{\{\ell,m\}\subset L}f_{\ell m}.
                                                                    \tag{13}
\]

Again \(|N|=p+2\) and \(|L|=p\).  The inclusion matrix
\(W_{p,2}(p+2)\) is square after identifying a row with the two-point
complement of \(L\).  Its three eigenvalues are

\[
                    \binom{p}{2},\qquad -(p-1),\qquad 1,          \tag{14}
\]

so it is invertible in characteristic zero.  If every \(G_L\) vanished,
(13) would force every \(f_{\ell m}=0\).

This is impossible for the nonzero two-component row vectors of \(H\).
Indeed, define

\[
                         \rho_\ell={H_{\ell c}\over H_{\ell d}}\ne0.
\]

Equation (12) becomes

\[
                 f_{\ell m}
                   =H_{\ell d}H_{m d}(\rho_\ell+\rho_m).          \tag{15}
\]

For any three indices, pairwise vanishing would say
\(\rho_1+\rho_2=\rho_1+\rho_3=\rho_2+\rho_3=0\), whose coefficient
matrix has determinant \(-2\).  Thus all three nonzero ratios would have
to vanish, a contradiction.  Some \(G_L\), and hence some pivot (9), is
nonzero.  This proves the second case of Theorem 1.1 uniformly.

At \(r=4,t=7\), \(p=3,k=1\), and the corresponding pivot is

\[
 C_{L\mid\{c,d\}}
 =2h_{01}^{\,3}
  \left(\prod_{\ell\in L}{1\over\nu_\ell+\mu}\right)
  \sum_{\{\ell,m\}\subset L}
     \operatorname {per}H[\{\ell,m\},\{c,d\}].                   \tag{16}
\]

## 5. Rank-drop classification and repeated values

Individual pivots may vanish on the hypersurfaces \(G_L=0\).  Sections
3--4 show that the common zero locus of all candidate pivots is empty
after localizing at the structural factors

\[
 h_{01}\prod_i(\nu_i+\mu)
          \prod_{i\ne j}(\nu_i+\nu_j).                            \tag{17}
\]

For \(s=1\), the inclusion transform would force a structurally nonzero
entry \(H_{\ell c}\) to vanish.  For \(s=2\), it would force pairwise
orthogonality of at least three vectors with two nonzero coordinates,
which is impossible for the swap bilinear form.  These are exact
common-rank-drop classifications, not generic-minor arguments.

No distinct-value limit is used.  If some \(\nu_i=\nu_j\), the
corresponding rows of \(H\) repeat and the same incidence and ratio
arguments remain valid.  Borchardt's identity is therefore unnecessary.

## 6. The next kernel

For later layers it is useful to set

\[
                         x_i={\nu_i-\mu\over\nu_i+\mu}.
\]

Then

\[
 \nu_i+\nu_j
 ={2\mu(1-x_ix_j)\over(1-x_i)(1-x_j)},\qquad
 H_{ij}={1-x_j\over1-x_ix_j}.                                    \tag{18}
\]

After removing nonzero column factors, the normalized cofactor is a
permanent of

\[
                              K_{ij}={1\over1-x_ix_j},             \tag{19}
\]

with each common-beta \(\mu\) column represented by \(x=0\), hence by
an all-one column.  For the next layer \(t=r+4\), the inclusion transform
acts on three-subset permanents.  It now has a nontrivial abstract
kernel, so the rational-curve constraints among the rows of (19), rather
than incidence rank alone, must be used.

## 7. Exact audit

[verify_live_three_zero_first_split_layers.py](../computations/verify_live_three_zero_first_split_layers.py)
checks the inclusion ranks for \(3\le r\le10\), verifies the permanent
expansion (9) over an abstract rational-function field, and checks the
ratio obstruction (15).

For \(r=4,t=6\), it reconstructs the complete selected \(9\times9\)
response minor, including row-two off-mark terms, as a lower triangular
matrix with diagonal (11).  For \(r=4,t=7\), it reconstructs the
selected \(6\times6\) minor with diagonal (16).  The complete
direct-plus-marked response evaluator is checked over exact rational
data, including a separate off-diagonal-source row whose direct term is
nonzero.
