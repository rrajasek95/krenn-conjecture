# The all-common minimal extra-plane response is injective

## 1. Outcome

Retain the minimal extra-plane residual from
[live-three-zero-extra-singular-shared-star-reduction.md](live-three-zero-extra-singular-shared-star-reduction.md).
It has two live sites (u,v), the two type-(10) centres (c,d), and
the unique possible rank-three extra neighbour (e), where

\[
                  \operatorname {im}P_e=\langle e_0,e_1\rangle . \tag{1}
\]

Suppose both live sites have the common beta value.  Thus all five residual
nonzero sites have the same beta value.

**Theorem 1.1 (all-common minimal extra-plane injectivity).**
The complete fifteen-column response at the shared zero (z_0), indexed by
all three rows of the five blocks (q_{i z_0}), has rank fifteen.  Hence
every nonzero-shore block at (z_0) vanishes and (z_0) is isolated in
(G_3(q)).

Together with the all-exceptional and one-exceptional triangular lemmas,
this closes every beta stratum of the smallest parity-compatible residual
containing the extra plane (1).

## 2. Normalization and exact response

Order the sites as

\[
                            (u,v,c,d,e).
\]

The normalization already justified in the all-exceptional note gives

\[
 P_u=P_v=I,\qquad P_c=P_d=D=\operatorname {diag}(1,1,0),\qquad
 H=\begin{pmatrix}0&1&1\\1&0&1\\1&1&0\end{pmatrix},             \tag{2}
\]

and the common beta value is (1).  Therefore

\[
                         q_{ij}={1\over2}P_iHP_j^{\mathsf T}.     \tag{3}
\]

Row-reducing the two nonzero rows of (P_e) gives the three charts

\[
\begin{aligned}
 A_{01}(a,b)&=\begin{pmatrix}1&0&a\\0&1&b\\0&0&0\end{pmatrix},&
 A_{12}(a,b)&=\begin{pmatrix}a&1&0\\b&0&1\\0&0&0\end{pmatrix},&
 A_{02}(a,b)&=\begin{pmatrix}1&a&0\\0&b&1\\0&0&0\end{pmatrix}.
                                                                    \tag{4}
\end{aligned}
\]

Fix one coordinate at (z_0), and let (Z_{i,j}) be row (j) of its
star block at site (i).  For a word
(w=(w_u,w_v,w_c,w_d,w_e)) and a diagonal source (ss), the complete
marked response is

\[
 E_{w;s,s}=2\sum_{\{x,y\}\subset V}(P_x)_{w_xs}(P_y)_{w_ys}
 \sum_{i\in V\setminus\{x,y\}} Z_{i,w_i}
 q_{jk}[w_j,w_k],                                                  \tag{5}
\]

where (V=\{u,v,c,d,e\}) and
({j,k}=V\setminus\{x,y,i\}).  This contains every marked-pair term.
The direct quadratic contributes nothing because its diagonal coefficients
are zero.  Thus every minor below is independent of the direct-term scale.

Write (w;ss) for a row of (5), and order the fifteen columns first by
row (j=0,1,2), then by (i=u,v,c,d,e).

## 3. The (01)-chart

For (P_e=A_{01}(a,b)), take the following three ordered sets of fifteen
rows:

\[
\begin{aligned}
\mathcal L_A={}&(00000;00,00010;00,00011;00,00012;00,00020;00,\\
 &00100;00,00110;11,00200;00,01000;00,01010;11,01100;11,\\
 &01111;11,02000;00,10000;00,20000;00),\\[2mm]
\mathcal L_B={}&(00010;00,00011;00,00012;00,00100;00,00110;00,\\
 &00111;11,00120;00,00210;00,01000;00,01010;00,01100;00,\\
 &01110;11,02010;00,10010;00,20010;00),\\[2mm]
\mathcal L_C={}&(00001;00,00010;00,00011;00,00012;00,00021;00,\\
 &00100;00,00101;00,00110;00,00201;00,01000;00,01001;00,\\
 &01110;11,02001;00,10001;00,20001;00).
                                                                    \tag{6}
\end{aligned}
\]

Direct expansion of (5) gives, up to the displayed nonzero integer
constants,

\[
\begin{aligned}
 \det R_{\mathcal L_A}&=2125764\,a^{11},\\
 \det R_{\mathcal L_B}&=108(a+3)^{10}(2a+3)(b+3),\\
 \det R_{\mathcal L_C}&=-708588(a+3)(4a+3)(b+1)^6
                              (a+3b+3)^2.                          \tag{7}
\end{aligned}
\]

These minors have no common zero.  If (a\ne0), the first is nonzero.
If (a=0) and (b\ne-3), the second is nonzero.  At the sole remaining
point (a=0,b=-3), every factor of the third is nonzero.  Hence the
response has rank fifteen throughout the (01)-chart.

## 4. The other charts

For (P_e=A_{12}(a,b)), use

\[
\begin{aligned}
\mathcal L_{12}=(
 &00000;00,00010;00,00011;00,00012;00,00020;00,00100;00,\\
 &00110;11,00200;00,01000;00,01010;11,01100;11,01110;11,\\
 &02000;00,10000;00,20000;00).
                                                                    \tag{8}
\end{aligned}
\]

Its determinant is the parameter-independent integer

\[
                         \det R_{\mathcal L_{12}}=57395628.        \tag{9}
\]

Swapping source axes (0,1), and independently swapping the corresponding
output rows at (u,v,c,d), sends (A_{02}(a,b)) to (A_{12}(a,b)).
It preserves (H,D), and the diagonal-source response.  Equivalently, the
transformed row set is

\[
\begin{aligned}
\mathcal L_{02}=(
 &11110;11,11100;11,11101;11,11102;11,11120;11,11010;11,\\
 &11000;00,11210;11,10110;11,10100;00,10010;00,10000;00,\\
 &12110;11,01110;11,21110;11),                                    \tag{10}
\end{aligned}
\]

and its determinant is again (57395628).  Thus all three charts in (4)
are injective.

## 5. Graph contradiction and audit

Theorem 1.1 kills all five residual nonzero-shore blocks at (z_0).  The
two removed type-(22) ports are singular, and the zero--zero blocks vanish
by beta parity.  Hence (z_0) has no rank-three neighbour, contradicting
the standing minimum-degree condition.

[verify_live_three_zero_minimal_extra_plane_common.py](../computations/verify_live_three_zero_minimal_extra_plane_common.py)
constructs (5) exactly over \(\mathbb Q(a,b)\), checks all five determinants
in (7), (9), and (10), and verifies the empty-common-zero case split in the
(01)-chart.
