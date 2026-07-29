# One exceptional live site also makes the minimal extra-plane response triangular

## 1. Outcome

Continue from
[live-three-zero-minimal-extra-plane-all-exceptional.md](live-three-zero-minimal-extra-plane-all-exceptional.md).
The minimal residual has two live sites, the two type-\(10\) centres
\(c,d\), and the sole possible rank-three extra site \(e\), with

\[
                   \operatorname {im}P_e=\langle e_0,e_1\rangle .
                                                                    \tag{1}
\]

Suppose now that exactly one live site is exceptional.  Normalize its
beta value to \(\nu\ne1\), while the other live site and all three
singular sites have beta value \(1\).

**Theorem 1.1 (one-exceptional minimal extra-plane injectivity).**
The complete twelve-column response at \(z_0\), indexed by the common
live site and \(c,d,e\), has rank twelve.  Thus every possible
nonzero-shore block to \(z_0\) vanishes, and \(z_0\) is isolated in
\(G_3(q)\).

As in the all-exceptional case, the proof works in all three kernel
charts for \(P_e\), retains its arbitrary kernel parameters, and uses
only structurally nonzero pivots.  Every selected source is \(00\),
\(11\), \(22\), \(02\), or \(12\); the direct quadratic has support
only on \(01\), so its contribution is identically zero in every proof
row.

## 2. Normalization

Order the five residual nonzero sites as

\[
                  (y,u,c,d,e),
\]

where \(y\) is exceptional and \(u\) has the common beta value.  Use the
same normalization as in the preceding note:

\[
\begin{gathered}
 P_y=P_u=I,\qquad P_c=P_d=\operatorname {diag}(1,1,0),\\
 H=\begin{pmatrix}0&1&1\\1&0&1\\1&1&0\end{pmatrix},
 \qquad(\beta_y,\beta_u,\beta_c,\beta_d,\beta_e)
                  =(\nu,1,1,1,1).                                \tag{2}
\end{gathered}
\]

The only denominator used below is

\[
                              \alpha={2\over\nu+1}\ne0.            \tag{3}
\]

At \(e\), use one of the row-reduced matrices
\(A_{01},A_{12},A_{02}\) from equation (5) of the preceding note.
Fixing one coordinate at \(z_0\), denote the twelve star variables by

\[
              Z_{u,j},Z_{c,j},Z_{d,j},Z_{e,j},
              \qquad 0\le j\le2.                                 \tag{4}
\]

The exceptional block \(q_{y z_0}\) is already zero structurally.

## 3. Three triangular tables

A table entry \(w;st\to Z\,[\gamma]\) means that, after the variables in
earlier entries have vanished, the response coefficient with local word
\(w=(w_y,w_u,w_c,w_d,w_e)\) and source \(st\) is
\(\gamma Z\).  The exact checker also records all earlier-column terms.

For \(P_e=A_{01}(a,b)\), use

\[
\begin{array}{c|c|c}
w;st&\text{pivot}&\text{coefficient}\\ \hline
02012;00&Z_{e,2}&1\\
02021;00&Z_{d,2}&1\\
02201;00&Z_{c,2}&1\\
02011;11&Z_{c,0}&\alpha\\
02101;11&Z_{d,0}&\alpha\\
12010;00&Z_{d,1}&\alpha\\
12100;00&Z_{c,1}&\alpha\\
22000;00&Z_{u,2}&3\alpha\\
02110;11&Z_{e,0}&\alpha\\
12001;00&Z_{e,1}&\alpha\\
20011;11&Z_{u,0}&\alpha\\
21001;00&Z_{u,1}&\alpha .
\end{array}                                                       \tag{5}
\]

For \(P_e=A_{12}(a,b)\), a triangular order is

\[
\begin{array}{c|c|c}
02012;00&Z_{e,2}&1\\
10121;11&Z_{d,2}&1\\
10211;11&Z_{c,2}&1\\
00110;11&Z_{u,0}&3\alpha\\
01010;11&Z_{c,0}&3\alpha\\
01100;11&Z_{d,0}&3\alpha\\
10011;02&Z_{d,1}&\alpha\\
10101;02&Z_{c,1}&\alpha\\
11001;02&Z_{u,1}&\alpha\\
22010;11&Z_{u,2}&\alpha\\
02111;11&Z_{e,1}&\alpha\\
22010;22&Z_{e,0}&1 .
\end{array}                                                       \tag{6}
\]

For \(P_e=A_{02}(a,b)\), use

\[
\begin{array}{c|c|c}
00121;00&Z_{d,2}&1\\
00211;00&Z_{c,2}&1\\
02012;00&Z_{e,2}&1\\
00111;12&Z_{u,0}&\alpha\\
01011;12&Z_{c,0}&\alpha\\
01101;12&Z_{d,0}&\alpha\\
10010;00&Z_{d,1}&3\alpha\\
10100;00&Z_{c,1}&3\alpha\\
11000;00&Z_{u,1}&3\alpha\\
22010;00&Z_{u,2}&\alpha\\
12001;00&Z_{e,1}&\alpha\\
22010;22&Z_{e,0}&1 .
\end{array}                                                       \tag{7}
\]

Every diagonal entry in (5)--(7) is nonzero by (3), and none depends
on \(a,b\).  The three response matrices are therefore triangular and
invertible.  This proves Theorem 1.1.

## 4. Graph contradiction and audit

The exceptional live block is zero because
\((\nu-1)q_{y z_0}=0\).  Tables (5)--(7) kill the common live block and
all three singular blocks.  As before, the removed type-\(22\) blocks
are singular ports and the zero--zero blocks vanish.  Hence \(z_0\)
has no rank-three neighbour.

[verify_live_three_zero_minimal_extra_plane_one_exceptional.py](../computations/verify_live_three_zero_minimal_extra_plane_one_exceptional.py)
builds the full marked response over
\(\mathbb Q(a,b,\nu)\), retains a symbolic direct-term scale, and checks
that the ordered rows (5)--(7) are triangular with the displayed
diagonal entries.
