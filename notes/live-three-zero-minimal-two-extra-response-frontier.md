# The first two-extra response is uniformly injective

## 1. Outcome

Consider the first two-extra rescue family in the exact missed-axis census:

\[
             (M_{e_2},M_{e_0})=(\{2\},\{0\}),\qquad
             (r,t)=(2,0).                                      \tag{1}
\]

Parity gives three live sites, all with the common beta value.  Order the
seven residual nonzero sites as

\[
                    V=(u_0,u_1,u_2,c,d,e_2,e_0),                \tag{2}
\]

where \(c,d\) are the two type-\(10\) centres.  Both extra singular sites
remain in every marked-pair sum and every matching cofactor.

The shared-star theorem gives

\[
 \operatorname{im}q_{e_0z_0}\subset
       \operatorname{im}P_{e_0}=\langle e_1,e_2\rangle,          \tag{3}
\]

while \(q_{e_2z_0}\) is the sole block still eligible to have rank three.
Thus the complete star-column set is

\[
\begin{aligned}
\mathcal J={}&
 \{(i,j):i\in\{u_0,u_1,u_2,c,d,e_2\},\ 0\le j\le2\}\\
 &{}\sqcup\{(e_0,1),(e_0,2)\},
\end{aligned}                                                    \tag{4}
\]

and has the exact size

\[
                              6\cdot3+2=20.                     \tag{5}
\]

No singular site has been deleted.  In particular, (3) removes one star
row, not the site \(e_0\) or its internal matching edges.

**Proposition 1.1.** The complete retained response has rank \(20\) for
every pair of rank-two source row planes and every direct \(B_{01}\) scale.
Sections 3--5 give the disjoint nine-cell proof.

## 2. Complete retained response

Normalize the common beta value to one and put

\[
 H=\begin{pmatrix}0&1&1\\1&0&1\\1&1&0\end{pmatrix},\qquad
 P_{u_i}=I,\qquad P_c=P_d=\operatorname{diag}(1,1,0).            \tag{6}
\]

The image planes of the extras are fixed, but their two source rows are
arbitrary rank-two row planes:

\[
 P_{e_2}=\begin{pmatrix}R_{e_2}\\0\end{pmatrix},\qquad
 P_{e_0}=\begin{pmatrix}0\\R_{e_0}\end{pmatrix},\qquad
 R_{e_2},R_{e_0}\in\operatorname{Gr}(2,3).                      \tag{7}
\]

For distinct \(i,j\in V\), write

\[
                         q_{ij}=\frac12P_iHP_j^{\mathsf T}.      \tag{8}
\]

For a word \(w\in\{0,1,2\}^V\), let \(Q[w]\) be the scalar edge
system \(Q[w]_{ij}=q_{ij}[w_i,w_j]\).  If \(Z_{i,j}\) is row \(j\)
of the star block toward \(z_0\), exact expansion of the vanished response
at source coordinates \(s,t\) is

\[
\begin{aligned}
E_{w;s,t}={}&
 B_{st}\sum_{\substack{i\in V\\(i,w_i)\in\mathcal J}}
 Z_{i,w_i}\operatorname{haf}Q[w]_{V\setminus\{i\}}\\
&+\sum_{\{x,y\}\subset V}
 \bigl(P_x[w_x,s]P_y[w_y,t]+P_x[w_x,t]P_y[w_y,s]\bigr)\\
&\hspace{12mm}\cdot
 \sum_{\substack{i\in V\setminus\{x,y\}\\(i,w_i)\in\mathcal J}}
 Z_{i,w_i}
 \operatorname{haf}Q[w]_{V\setminus\{x,y,i\}}
=0.                                                             \tag{9}
\end{aligned}
\]

The first line retains the direct term.  The remaining six sites contribute
three internal edges.  In the marked term, four sites remain after choosing
the marked pair and star, and contribute two internal edges.  Formula (9)
therefore retains every extra-star column and every occurrence of both
extra sites in the matching cofactors.

## 3. Generic chart certificate and first divisor

Use the three standard affine charts \(01,12,02\) on each row plane in
(7).  At the deterministic parameter point \((a,b,c,d)=(2,3,5,7)\),
direct-free response rows have rank \(20\) in every one of the nine chart
products.  Reduction modulo \(1000003\) gives a nonzero maximal minor in
each case, and therefore certifies that the corresponding integer
determinant is not the zero polynomial over \(\mathbb Q\).

In the central \(01\times01\) chart, fraction-free elimination over
\(\mathbb Z[a,b,c,d]\) gives one selected maximal minor exactly:

\[
 2^{44}3^7a^9c^{10}(b-d)
       (ac+3a+3c+6)^5.                                        \tag{10}
\]

Hence every chart product is generically injective, and any central-chart
survivor lies on the explicit divisor

\[
                ac(b-d)(ac+3a+3c+6)=0.                         \tag{11}
\]

The four components in (11) are closed exactly in the next section.

## 4. Uniform closure of the central cell

Restricted direct-free maximal-minor ideals close the four branches

\[
\begin{array}{c|c|c}
\text{branch}&\text{free variables}&
 \text{additional finite-field row selectors}\\ \hline
a=0&(b,c,d)&12\text{ over }\mathbf F_{17}\\
c=0&(a,b,d)&9\text{ over }\mathbf F_{17}\\
b=d&(a,b,c)&1\text{ over }\mathbf F_{17},
                 \ 2\text{ over }\mathbf F_{23}\\
Q:=ac+3a+3c+6=0&(a,b,d)&3\text{ over }\mathbf F_{17}.
\end{array}                                                     \tag{12}
\]

On \(Q=0\), solve

\[
                         c=-\frac{3(a+2)}{a+3}.
\]

The denominator is automatically nonzero on this branch, since
\(Q|_{a=-3}=-3\).  After adjoining the row-denominator localization,
the exact restricted ideal is \((1)\).  The other three rows of (12)
also give exact unit ideals, without localization.

The finite-field coordinates in (12) only select response-row labels.
Every selected determinant is reconstructed over \(\mathbb Q\), restricted
symbolically to its branch, replaced by its squarefree support, and included
in an exact rational unit-ideal computation.  The four branches exhaust
(11).  Therefore the complete response has rank \(20\) at every point of
the central \(01\times01\) chart.

## 5. Disjoint boundary-cell census

For either row plane, write

\[
 C=\{p_{01}\ne0\},\qquad
 B=\{p_{01}=0,\ p_{12}\ne0\},\qquad
 E=\{(p_{01}:p_{02}:p_{12})=(0:1:0)\}.                         \tag{13}
\]

The two ordered row planes therefore have the disjoint nine-cell cover

\[
\begin{array}{c|c|c}
\text{cell}&\text{dimension}&\text{uniform status}\\ \hline
CC&4&\text{closed}\\
CB&3&\text{closed}\\
CE&2&\text{closed}\\
BC&3&\text{closed}\\
BB&2&\text{closed}\\
BE&1&\text{closed}\\
EC&2&\text{closed}\\
EB&1&\text{closed}\\
EE&0&\text{closed}.
\end{array}                                                     \tag{14}
\]

This table is ordered: the first letter belongs to \(e_2\), whose star
has three retained rows, and the second belongs to \(e_0\), whose star has
two.  The binary-axis swap \(0\leftrightarrow1\) fixes the
\(\{2\}\)-extra and transfers the whole calculation to the census mate
\(\{2\}+\{1\}\); it does not exchange the two factors in (14).  Thus no
\(CB/BC\), \(CE/EC\), or \(BE/EB\) identification is used.  For the fixed
family (1), the nine displayed products are nine separate cell orbits under
the proved stabilizer.

The eight ordered noncentral cells have independent exact unit-minor
certificates in
[live-three-zero-minimal-two-extra-boundary-certificate.md](live-three-zero-minimal-two-extra-boundary-certificate.md).
Together with Section 4, this proves uniform rank \(20\) on the complete
nine-cell cover, with arbitrary direct \(B_{01}\) scale.  This closes only
the first case (1); larger live shores and the other \(t\)-strata in the
two-extra family remain open.

## 6. Exact audit

[verify_live_three_zero_minimal_two_extra_complete.py](../computations/verify_live_three_zero_minimal_two_extra_complete.py)
runs the retained response, central branch, and ordered boundary audits in
one clean default replay.

[verify_live_three_zero_minimal_two_extra_frontier.py](../computations/verify_live_three_zero_minimal_two_extra_frontier.py)
checks the 20-column set, verifies that all selected rows avoid source
\(01\), certifies rank \(20\) on all nine chart products, and reconstructs
(10) exactly.

[verify_live_three_zero_minimal_two_extra_central_uniform.py](../computations/verify_live_three_zero_minimal_two_extra_central_uniform.py)
reconstructs every branch determinant and verifies all four exact unit
ideals in (12).

[verify_live_three_zero_minimal_two_extra_boundary_cells.py](../computations/verify_live_three_zero_minimal_two_extra_boundary_cells.py)
checks the eight ordered noncentral unit-minor certificates.  The response
generator and deterministic row selections are in
[explore_live_three_zero_minimal_two_extra_response.py](../computations/explore_live_three_zero_minimal_two_extra_response.py).
