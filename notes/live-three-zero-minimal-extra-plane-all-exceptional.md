# The minimal extra-plane response is triangular

## 1. Outcome

Retain the cyclic three-zero branch.  Let \(c,d\) be the two residual
type-\(10\) centres and let \(e\) be the sole additional nonzero singular
site.  The shared-star reduction shows that the only extra site which can
be a rank-three neighbour of \(z_0\) has

\[
                 \operatorname {im}P_e=\langle e_0,e_1\rangle .
                                                                    \tag{1}
\]

Consider the smallest parity-compatible residual: besides \(c,d,e\), it
has two live sites \(u,v\).  Suppose both live sites are exceptional,
with beta values \(\nu_0,\nu_1\ne\mu\).

**Theorem 1.1 (minimal extra-plane injectivity).**  The complete
nine-column response at \(z_0\), indexed by the three rows of each of
\(q_{c z_0},q_{d z_0},q_{e z_0}\), has rank nine.  Hence all three
blocks vanish.  The exceptional live-star blocks vanish structurally,
so \(z_0\) has no rank-three neighbour.

The proof is a triangular coefficient table.  It retains an arbitrary
kernel of \(P_e\), repeated live beta values, and the entire direct-plus-
marked response.  Every selected row has a diagonal source, so the
rank-two direct term vanishes exactly rather than being discarded.

## 2. Normal form and response formula

Independent local changes normalize

\[
             P_u=P_v=I,\qquad P_c=P_d=D=\operatorname {diag}(1,1,0).
                                                                    \tag{2}
\]

Diagonal source rescaling and the harmless common scaling of \(H\) and
the beta values put

\[
 H=\begin{pmatrix}0&1&1\\1&0&1\\1&1&0\end{pmatrix},
 \qquad \mu=1.                                                     \tag{3}
\]

Explicitly, first replace \(H,\beta_i\) by
\(H/\mu,\beta_i/\mu\), which leaves every structural quotient unchanged.
Then choose nonzero \(s_0,s_1,s_2\) with
\(s_is_j=h_{ij}/\mu\) and reparameterize the source by
\(\operatorname {diag}(s_0,s_1,s_2)\).  Such scalars exist over
\(\mathbb C\).  Local diagonal output changes restore the matrices in
(2).  The direct quadratic remains a nonzero multiple of \(x_0x_1\);
its scalar is not normalized or used below.

The structural nonzero denominators are

\[
                 \nu_0+1,\qquad \nu_1+1,\qquad \nu_0+\nu_1.        \tag{4}
\]

Because (1) has rank two, a local output change at \(e\) puts \(P_e\)
in one of the three row-reduced charts

\[
\begin{aligned}
 A_{01}(a,b)&=\begin{pmatrix}1&0&a\\0&1&b\\0&0&0\end{pmatrix},&
 A_{12}(a,b)&=\begin{pmatrix}a&1&0\\b&0&1\\0&0&0\end{pmatrix},\\
 A_{02}(a,b)&=\begin{pmatrix}1&a&0\\0&b&1\\0&0&0\end{pmatrix}.     \tag{5}
\end{aligned}
\]

These charts cover every two-dimensional row space.  No condition is
placed on \(a,b\).

Fix a coordinate at \(z_0\), and write \(Z_{i,j}\) for row \(j\) of
the corresponding star column at \(i\in\{c,d,e\}\).  A response row is
specified by a word

\[
                 w=(w_u,w_v,w_c,w_d,w_e)\in\{0,1,2\}^5
\]

and a diagonal source \(ss\).  Its complete coefficient is

\[
\begin{aligned}
 E_{w;s,s}
 =2\sum_{\{x,y\}\subset\{u,v,c,d,e\}}
   &(P_x)_{w_xs}(P_y)_{w_ys}\\
   {}\times&
   \sum_{\substack{i\in\{c,d,e\}\\i\notin\{x,y\}}}
       Z_{i,w_i}\,
       q_{jk}[w_j,w_k],
\quad
 \{j,k\}=V\setminus\{x,y,i\}.                                  \tag{6}
\end{aligned}
\]

This is the full marked-pair expansion.  The direct term is zero because
\(B_{ss}=0\).

## 3. The \(01\)-kernel chart

Put

\[
       \delta={2\over\nu_0+\nu_1},\qquad
       \epsilon={2\over\nu_1+1}.                                  \tag{7}
\]

For \(P_e=A_{01}(a,b)\), the following nine rows have exactly the one
displayed star variable:

\[
\begin{array}{c|c|c|c}
w&ss&\text{variable}&\text{coefficient}\\ \hline
02011&11&Z_{c,0}&\delta\\
02101&11&Z_{d,0}&\delta\\
02110&11&Z_{e,0}&\delta\\
12100&00&Z_{c,1}&\delta\\
12010&00&Z_{d,1}&\delta\\
12001&00&Z_{e,1}&\delta\\
02201&00&Z_{c,2}&\epsilon\\
02021&00&Z_{d,2}&\epsilon\\
22012&22&Z_{e,2}&1
\end{array}                                                       \tag{8}
\]

Thus (8) is a diagonal \(9\times9\) response minor with determinant
\(\delta^6\epsilon^2\ne0\).

## 4. The other two kernel charts

For \(P_e=A_{12}(a,b)\), eight singleton rows are

\[
\begin{array}{c|c|c|c}
w&ss&\text{variable}&\text{coefficient}\\ \hline
02010&11&Z_{c,0}&\delta\\
02100&11&Z_{d,0}&\delta\\
12101&22&Z_{c,1}&2/(\nu_0+1)\\
12011&22&Z_{d,1}&2/(\nu_0+1)\\
02111&11&Z_{e,1}&\delta\\
01211&11&Z_{c,2}&2/(\nu_0+1)\\
01121&11&Z_{d,2}&2/(\nu_0+1)\\
02012&00&Z_{e,2}&\epsilon .
\end{array}                                                       \tag{9}
\]

After these eight variables vanish, row \(02110;11\) is

\[
             \delta\bigl(Z_{e,0}+Z_{c,1}+Z_{d,1}\bigr)
                         =\delta Z_{e,0}.                          \tag{10}
\]

Hence this chart is triangular with nonzero diagonal.

For \(P_e=A_{02}(a,b)\), use

\[
\begin{array}{c|c|c|c}
w&ss&\text{variable}&\text{coefficient}\\ \hline
02011&22&Z_{c,0}&2/(\nu_0+1)\\
02101&22&Z_{d,0}&2/(\nu_0+1)\\
12100&00&Z_{c,1}&\delta\\
12010&00&Z_{d,1}&\delta\\
12001&00&Z_{e,1}&\delta\\
00211&00&Z_{c,2}&1\\
00121&00&Z_{d,2}&1\\
02012&00&Z_{e,2}&\epsilon .
\end{array}                                                       \tag{11}
\]

The final row \(12000;00\) is

\[
             \delta\bigl(Z_{e,0}+Z_{c,0}+Z_{d,0}\bigr)
                         =\delta Z_{e,0}.                          \tag{12}
\]

This proves Theorem 1.1 in all three charts.  Notice that \(a,b\) cancel
from every diagonal pivot; no kernel alignment or genericity hypothesis
has entered.

## 5. Graph contradiction and exact audit

The live beta values are exceptional, so

\[
                  q_{u z_0}=q_{v z_0}=0.
\]

Theorem 1.1 kills the remaining three nonzero-shore blocks.  The blocks
from \(z_0\) to the two removed type-\(22\) centres are singular
coordinate ports, and its zero--zero blocks vanish by beta parity.
Therefore \(z_0\) is isolated in \(G_3(q)\), a contradiction.

[verify_live_three_zero_minimal_extra_plane_all_exceptional.py](../computations/verify_live_three_zero_minimal_extra_plane_all_exceptional.py)
constructs the complete response (6) over
\(\mathbb Q(a,b,\nu_0,\nu_1)\), checks every singleton in
(8)--(9) and (11), and verifies the two triangular rows (10), (12).
