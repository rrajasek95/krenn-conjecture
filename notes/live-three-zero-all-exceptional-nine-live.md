# The all-exceptional nine-live three-zero response is injective

## 1. Outcome

The first two split layers were closed uniformly in
[live-three-zero-first-split-layers.md](live-three-zero-first-split-layers.md).
The next case is

\[
              r=5,\qquad |U|=9,\qquad t=9=r+4,                   \tag{1}
\]

so all nine live sites are exceptional and the only common-beta residual
sites are the two type-\(10\) centres.

**Theorem 1.1 (all-exceptional nine-live injectivity).**  On the full
structurally admissible locus, including repeated live beta values, the
complete six-column zero-star response has rank six.  Hence every
residual nonzero-to-\(z_0\) block vanishes and \(z_0\) is isolated in
\(G_3(q)\), a contradiction.

The proof combines two exact incidence transforms.  The first couples
all choices of the exceptional three-set and is certified by an integer
matrix of size \(1260\times840\).  The second is the elementary
permanental-rank obstruction for a \(6\times3\) matrix with no zero
entries.  No generic minor or distinct-beta assumption occurs.

## 2. Isolated-centre pivots

Let \(E=\{y_1,\ldots,y_9\}\) be the exceptional live sites, with beta
values \(\nu_i\ne\mu\), and let \(c_1,c_2\) be the type-\(10\) centres.
Normalize \(P_{y_i}=I\) and

\[
                  P_{c_1}=P_{c_2}
                     =D=\operatorname {diag}(1,1,0).
\]

Every exceptional star block is already zero:

\[
                         (\nu_i-\mu)q_{y_i z_0}=0.                \tag{2}
\]

Fix disjoint sets

\[
                  R,L,B\subset E,\qquad
                  |R|=3,\quad |L|=4,\quad |B|=2,                \tag{3}
\]

whose union is \(E\).  Give \(B\) colour \(2\) and read the diagonal
source \(x_2z_2\), so \(B\) is the unique marked pair.  To isolate row
zero at a target centre, give \(L\) and the target colour \(0\), while
giving \(R\) and the other centre colour \(1\).  Removing the marked
pair and target star leaves balanced shores of size four.  Moving the
star to the other centre instead leaves shore sizes five and three, so
that coefficient vanishes.

Put

\[
 a_\ell={1\over\nu_\ell+\mu},\qquad
 H_{\ell c}={\nu_\ell+\mu\over\nu_\ell+\nu_c}
             \quad(\ell\in L,\ c\in R).                         \tag{4}
\]

All entries in (4) are nonzero by the live--centre and live--live
structural equations.  Expanding the balanced cofactor along its single
common-beta column gives the exact isolated pivot

\[
 C_{L\mid R}
 =2h_{01}^{\,4}
   \left(\prod_{\ell\in L}a_\ell\right)G_{L\mid R},              \tag{5}
\]

where

\[
 G_{L\mid R}
 =\sum_{\substack{J\subset L\\|J|=3}}
       \operatorname {per}H[J,R].                               \tag{6}
\]

Swapping binary colours gives the row-one pivot.  Giving the target
centre colour \(2\) gives row two with the same pivot: a type-\(10\)
centre has neither a third marked factor nor a nonzero third internal
row.  Thus the six selected rows form the exact minor

\[
                          M_{L\mid R}=C_{L\mid R}I_6.             \tag{7}
\]

The direct coordinate-factor term is absent from these rows because
\(B_{22}=0\).  It remains present in the complete response for
off-diagonal sources and is included in the exact audit.

## 3. Coupling all exceptional three-sets

Suppose, toward rank drop, that every candidate pivot (5) vanishes.
The prefactor outside \(G_{L\mid R}\) is structurally nonzero, so every
equation (6) vanishes.

For disjoint triples \(J,R\subset E\), define

\[
 F_{\{J,R\}}
 =\left(\prod_{c\in R}(\nu_c+\mu)\right)
      \operatorname {per}H[J,R]
 =\left(\prod_{i\in J\sqcup R}(\nu_i+\mu)\right)
      \operatorname {per}
       \left({1\over\nu_i+\nu_c}\right)_{i\in J,\ c\in R}.       \tag{8}
\]

The last expression shows that the index is an unordered pair: its
Cauchy permanent is invariant under transpose.  Every rescaling factor
in (8) is structurally nonzero.  There are

\[
 {1\over2}\binom93\binom63=840                                  \tag{9}
\]

such variables.  For each ordered triple \(R\) and each possible marked
pair \(B\subset E\setminus R\), equation (6), with
\(L=E\setminus(R\sqcup B)\), is

\[
 {1\over\prod_{c\in R}(\nu_c+\mu)}
             \sum_{\substack{J\subset E\setminus(R\sqcup B)\\
                             |J|=3}}
                    F_{\{J,R\}}=0.                              \tag{10}
\]

There are

\[
                         \binom93\binom62=1260                   \tag{11}
\]

equations.  Let \({\cal I}_9\) be their \(0\)-\(1\) coefficient matrix.
Exact row reduction gives

\[
                    \operatorname {rank}_{\mathbb F_{1009}}
                       {\cal I}_9=840.                           \tag{12}
\]

Because \({\cal I}_9\) is an integer matrix, (12) exhibits an
\(840\times840\) minor whose determinant is nonzero modulo \(1009\);
that determinant is therefore a nonzero integer.  Hence
\({\cal I}_9\) has full column rank over \(\mathbb Q\) and over
\(\mathbb C\).  Equations (10) force

\[
                  \operatorname {per}H[J,R]=0
       \quad\text{for every pair of disjoint triples }J,R.       \tag{13}
\]

This coupled transform is the step unavailable when one freezes \(R\):
for a fixed \(R\), the ordinary \(4\)-subset-versus-\(3\)-subset
incidence matrix has a five-dimensional kernel.

## 4. A nonzero \(6\times3\) matrix cannot satisfy (13)

Fix one triple \(R\).  Its complement contains six exceptional sites,
and (13) says that every \(3\times3\) row permanent of the matrix

\[
                         \bigl(H_{ic}\bigr)_{
                              i\in E\setminus R,\ c\in R}         \tag{14}
\]

vanishes.  Every entry of (14) is nonzero.  Scale each row by its
nonzero third entry and write it as

\[
                              (u_i,v_i,1).
\]

For a triple \(\{i,j,k\}\), its permanent is

\[
 f_{ij}+f_{ik}+f_{jk},\qquad
 f_{ij}=u_iv_j+u_jv_i.                                          \tag{15}
\]

The inclusion matrix of triples against pairs on six points has size
\(20\times15\) and full column rank over characteristic zero.  Thus
vanishing of every expression in (15) forces every \(f_{ij}=0\).

Set \(\rho_i=u_i/v_i\ne0\).  Then

\[
                         f_{ij}=v_iv_j(\rho_i+\rho_j).            \tag{16}
\]

For any three rows, pairwise vanishing in (16) gives

\[
 \begin{pmatrix}
 1&1&0\\
 1&0&1\\
 0&1&1
 \end{pmatrix}
 \begin{pmatrix}\rho_1\\\rho_2\\\rho_3\end{pmatrix}=0.
\]

The determinant is \(-2\), so all three ratios would be zero,
contradicting their definition.  Therefore (13) is impossible, and at
least one pivot (5) is nonzero.  This proves Theorem 1.1.

The argument does not use a Cauchy determinant or Borchardt's identity.
Repeated beta values merely repeat rows or columns in (14); all entries
remain nonzero and the same contradiction applies.

## 5. Exact rank-drop classification

An individual diagonal minor (7) drops rank exactly on the cancellation
hypersurface \(G_{L\mid R}=0\), apart from the explicitly forbidden
factors

\[
 h_{01}\prod_i(\nu_i+\mu)
       \prod_{i\ne j}(\nu_i+\nu_j)=0.                            \tag{17}
\]

The common vanishing of all such minors would first force (13) by
(12), then force all pair forms (15) to vanish, and finally force a
nonzero coordinate ratio to be zero.  Thus the common rank-drop locus is
empty after localizing away from (17).  This is an exact classification
of the full admissible locus.

## 6. Graph contradiction and scope

The six-column injectivity holds independently for all three coordinates
at \(z_0\), so both type-\(10\)-centre star blocks vanish.  Equation (2)
kills all nine live-star blocks.  The zero--zero blocks at \(z_0\)
vanish because all literal-zero beta values are \(-\mu\), and its blocks
to the removed type-\(22\) centres are singular coordinate ports.
Therefore \(z_0\) is isolated in \(G_3(q)\).

This closes the \(s=3\), no-extra-singular branch through live size nine.
For the uniform layer \(t=r+4\) at larger \(r\), the fixed-\(R\)
incidence kernel persists and the coupled incidence map is no longer
injective as an abstract map.  Additional Cauchy-kernel structure is
needed there.  The pairwise-distinct exceptional-beta stratum is now
closed uniformly by
[live-three-zero-third-split-distinct-beta.md](live-three-zero-third-split-distinct-beta.md);
the collision/Hermite strata for \(r\ge6\) are closed by
[live-three-zero-third-split-collision-beta.md](live-three-zero-third-split-collision-beta.md).
The next all-exceptional case \(r=6,t=11\) is handled in
[live-three-zero-all-exceptional-eleven-live.md](live-three-zero-all-exceptional-eleven-live.md).

## 7. Exact audit

[verify_live_three_zero_all_exceptional_nine_live.py](../computations/verify_live_three_zero_all_exceptional_nine_live.py)
constructs \({\cal I}_9\) and certifies (12), verifies the
\(20\times15\) rank used in Section 4 over \(\mathbb Q\), and checks
the symbolic permanent expansion (5)--(6).

It also evaluates the complete direct-plus-marked zero-star response at
an admissible exact rational specialization.  The six proof rows form
the diagonal minor (7), and a separate off-diagonal-source row audits
the nonzero direct contribution.
