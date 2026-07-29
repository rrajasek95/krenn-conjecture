# The first three-extra response is uniformly injective

## 1. Outcome

Consider the first multiple-rescue configuration from
[live-three-zero-extra-singular-exact-frontier.md](live-three-zero-extra-singular-exact-frontier.md):

\[
 (M_{e_2},M_{e_0},M_{e_1})=(\{2\},\{0\},\{1\}),\qquad
 (r,t)=(1,0).                                                    \tag{1}
\]

There are two common-beta live sites \(u,v\), the two type-\(10\)
centres \(c,d\), and the three extra rank-two sites \(e_2,e_0,e_1\).
This note writes the complete response, including every extra-star
column and the direct term.

The shared-star theorem already gives

\[
 \operatorname {im}q_{e_0z_0}\subset\langle e_1,e_2\rangle,
 \qquad
 \operatorname {im}q_{e_1z_0}\subset\langle e_0,e_2\rangle.      \tag{2}
\]

For each fixed coordinate at \(z_0\), the response therefore has exactly
\[
 5\cdot3+2+2=19                                                  \tag{3}
\]
columns: all rows at \(u,v,c,d,e_2\), rows \(1,2\) at \(e_0\), and
rows \(0,2\) at \(e_1\).

**Proposition 1.1 (generic minimal three-extra injectivity).** The
complete 19-column response has rank 19 on a nonempty Zariski-open set
of every product of row-plane charts. In the central \(01^3\) chart, an
explicit maximal minor is

\[
\begin{aligned}
 -2^{37}3^{10}\,
 &a^7bc^8de^7f(d-f)\\
 &{}\cdot(ac+ae+ce)^2\\
 &{}\cdot(ac+ae+ce+3a+3c+3e+6)^4.                               \tag{4}
\end{aligned}
\]

Thus the first three-extra case is closed generically on all 27 chart
products. Any survivor in this chart lies on the exact divisor

\[
 abcdef(d-f)(ac+ae+ce)
 (ac+ae+ce+3a+3c+3e+6)=0.                                      \tag{5}
\]

The \(Q=ac+ae+ce+3a+3c+3e+6\) component of (5) is closed exactly in
Sections 5--7 below.  It must not be discarded merely by a
generic-kernel argument: the closure uses seven further maximal minors,
four fixed-point determinants, and three exact univariate gcds.

**Proposition 1.2 (uniform central-chart injectivity).** In the central
\(01^3\) chart, the complete response has rank 19 for every
\(a,b,c,d,e,f\in\mathbb C\) and for arbitrary scale of the direct
\(B_{01}\) term.  Sections 8--9 close the complement of \(Q=0\), first
on \(ace\ne0\) by 21 exact localized branch ideals and then on the three
coordinate planes.  The exact Plücker-cell reduction in
[live-three-zero-minimal-three-extra-boundary-cell-frontier.md](live-three-zero-minimal-three-extra-boundary-cell-frontier.md)
closes all 26 noncentral cells.  In particular, the last three placements
\(CCB,CBC,BCC\) have independent exact localized certificates in
[live-three-zero-minimal-three-extra-ccb-certificate.md](live-three-zero-minimal-three-extra-ccb-certificate.md).
Together with the central chart, this proves uniform rank \(19\) on the
complete 27-cell row-plane cover.

## 2. Normal form

Order the seven residual nonzero sites as

\[
                           V=(u,v,c,d,e_2,e_0,e_1).              \tag{6}
\]

All beta values equal the common value. Normalize it to one, and
normalize

\[
 H=\begin{pmatrix}0&1&1\\1&0&1\\1&1&0\end{pmatrix},\qquad
 P_u=P_v=I,\qquad P_c=P_d=D=\operatorname {diag}(1,1,0).         \tag{7}
\]

On the dense row-space chart whose \(01\) Pluecker coordinate is
nonzero at each extra site, choose

\[
\begin{aligned}
 P_{e_2}&=\begin{pmatrix}1&0&a\\0&1&b\\0&0&0\end{pmatrix},\\
 P_{e_0}&=\begin{pmatrix}0&0&0\\1&0&c\\0&1&d\end{pmatrix},\\
 P_{e_1}&=\begin{pmatrix}1&0&e\\0&0&0\\0&1&f\end{pmatrix}.
\end{aligned}                                                    \tag{8}
\]

The identity pivots in (8) make every matrix rank two for all
\(a,b,c,d,e,f\in\mathbb C\); zero parameter values are not excluded.
The other row-plane charts are obtained by using pivot pairs \(12\) or
\(02\) in the corresponding two nonzero output rows.

For \(i\ne j\) in \(V\), the internal blocks are

\[
                         q_{ij}={1\over2}P_iHP_j^{\mathsf T}.     \tag{9}
\]

The direct quadratic is supported on source \(01\); retain its arbitrary
scale in the formula below.

## 3. Complete response formula

Fix an output coordinate at \(z_0\), and write \(Z_{i,r}\) for row \(r\)
of the corresponding star column. Let

\[
\begin{aligned}
 {\cal J}={}&\{(i,r):i\in\{u,v,c,d,e_2\},\ 0\le r\le2\}\\
            &{}\sqcup\{(e_0,1),(e_0,2),(e_1,0),(e_1,2)\}.         \tag{10}
\end{aligned}
\]

For a word \(w\in\{0,1,2\}^V\), let \(Q[w]\) be the scalar edge system

\[
                         Q[w]_{ij}=q_{ij}[w_i,w_j].               \tag{11}
\]

For source coordinates \(s,t\), exact expansion of the vanished cyclic
response gives

\[
\begin{aligned}
E_{w;s,t}={}&
 B_{st}\sum_{\substack{i\in V\\(i,w_i)\in{\cal J}}}
 Z_{i,w_i}\,
 \operatorname {haf}Q[w]_{V\setminus\{i\}}\\
&+\sum_{\{x,y\}\subset V}
 \bigl(P_x[w_x,s]P_y[w_y,t]+P_x[w_x,t]P_y[w_y,s]\bigr)\\
&\hspace{12mm}\cdot
 \sum_{\substack{i\in V\setminus\{x,y\}\\(i,w_i)\in{\cal J}}}
 Z_{i,w_i}\,
 \operatorname {haf}Q[w]_{V\setminus\{x,y,i\}}
=0.                                                             \tag{12}
\end{aligned}
\]

The first line is the complete direct contribution: after choosing the
star, six sites remain. The other lines retain every marked pair and
every possible star, including all three extras. No singular site has
been deleted.

## 4. Exact maximal minor

Order the columns as

\[
\begin{gathered}
 (u,0),(u,1),(u,2),(v,0),(v,1),(v,2),
 (c,0),\ldots,(e_2,2),\\
 (e_0,1),(e_0,2),(e_1,0),(e_1,2).                               \tag{13}
\end{gathered}
\]

Write a response row as \(w;st\). Select the following nineteen rows:

\[
\begin{gathered}
0000210;00,\ 0002010;00,\ 0020010;00,\\
0001010;12,\ 0010010;12,\ 0100010;12,\\
0111010;00,\ 1000010;12,\ 1011010;00,\\
1101010;00,\ 1110010;00,\ 0011010;11,\\
0011122;00,\ 0201012;11,\ 0201020;11,\\
0201110;11,\ 0201122;00,\ 0211022;00,\ 2001012;11.
                                                                    \tag{14}
\end{gathered}
\]

None uses source \(01\), so the direct scale drops out exactly. Clear the
common factor \(1/4\) contributed by the two internal edges in every
entry. Fraction-free elimination of the resulting matrix gives (4).
Hence it is invertible off (5), proving Proposition 1.1 on this chart.

The three possible row-space charts at each of the three extras give
27 products. Exact modular row selection at one rational point of each
product gives rank 19 in every case. This proves generic rank 19 there,
because the selected determinant is a polynomial and is nonzero at the
displayed point. It does not prove that the 27 rank-drop loci are empty.

## 5. Direct-free minors on the \(Q\)-boundary

Put

\[
\begin{gathered}
 S=a+c+e,\qquad p=ace,\qquad G=ac+ae+ce,\qquad Q=G+3S+6,\\
 J=3p+G,\qquad L=3G+4S+3,\qquad K=3p+4G+3S,\\
 D=(a-c)(a-e)(c-e),\qquad
 P=(a+c)(a+e)(c+e).
                                                               \tag{15}
\end{gathered}
\]

The two nonsymmetric auxiliary factors needed below are

\[
 X=ac+ae+4a-2ce-2c-2e                                      \tag{16}
\]

and

\[
\begin{aligned}
 F={}&3ac^2e+3ace^2+16ace+6ac+6ae\\
    &{}-6c^2e^2-8c^2e-6c^2-8ce^2-6e^2,                       \tag{17}\\
 W={}&a^2c^2e+4a^2c^2+a^2ce^2+2a^2ce+4a^2e^2\\
    &{}+ac^2e^2+2ac^2e+2ace^2+4c^2e^2.                       \tag{18}
\end{aligned}
\]

Seven further 19-row selections give the following exact maximal
minors of the integer matrix obtained by clearing the common \(1/4\)
from every response row:

\[
\begin{array}{c|l}
\text{name}&\text{determinant}\\ \hline
\Delta _0&-2^{40}3^8a^6c^8e^5\,G L K J^2\\
\Delta _G&-2^{37}3^9a^5c^9e^8\,P L J K^2\\
\Delta _L& \phantom{-}2^{35}3^{14}a^6c^7e^7\,D G^2K^6\\
\Delta _K&-2^{40}3^{14}a^8c^9e^7\,D G^2J^4\\
\Delta _J& \phantom{-}2^{36}3^{13}a^9c^9e^8\,G^2K^4X\\
\Delta _P& \phantom{-}2^{39}3^{13}a^9c^8e^7\,G^2J^4F\\
\Delta _{p=2}&-2^{35}3^{26}a^{10}c^{11}e^{11}\,D W^2.
                                                               \tag{19}
\end{array}
\]

Every row used in (19) has source pair \(00,02,11,12\), or \(22\),
never \(01\). Hence the direct \(B_{01}\) term vanishes identically in
these rows; (19) is valid for its arbitrary scale. The selected row
sets are recorded verbatim in the exact checker. The determinants in
(19) are independent of the nuisance parameters \(b,d,f\).

## 6. Complete non-coordinate branch table on \(Q=0\)

All ideal identities in this section are in
\(\mathbb Q[a,c,e]\). The four branches produced by \(\Delta _0\) are
governed by

\[
\begin{aligned}
 (Q,G)&=(G,S+2),\\
 (Q,L)&=(G-3,S+3),\\
 (Q,K)&=(G+3S+6,p-3S-8),\\
 (Q,J)&=(G+3S+6,p-S-2),                                      \tag{20}\\
 (Q,K,J)&=(S+3,G-3,p+1),\\
 (Q,L,K)&=(S+3,G-3,p+1).
\end{aligned}
\]

Assume first that \(ace=p\ne0\). A common zero of all maximal minors
on \(Q=0\) must annihilate \(\Delta _0\), so one of
\(G,L,K,J\) vanishes. The exhaustive branch table is:

\[
\begin{array}{c|c|c|c}
\text{branch}&\text{exact residue}&\text{next minor}&\text{only fallback}\\ \hline
G=0&S=-2,\ P=-p,\ L=-5,\ J=3p,\ K=3(p-2)
    &\Delta_G&p=2\\
L=0&S=-3,\ G=3,\ K=3(p+1)
    &\Delta_L&D=0\text{ or }p=-1\\
K=0&p=3S+8
    &\Delta_K&G=0,\ J=0,\text{ or }D=0\\
J=0&p=S+2
    &\Delta_J&G=0,\ K=0,\text{ or }X=0.
                                                               \tag{21}
\end{array}
\]

Here the identity

\[
                   P=SG-p                                   \tag{22}
\]

was used in the first row. Each fallback in (21) closes as follows.

### 6.1. The \(G=0\) branch

If \(p=2\), the three parameters are the roots of

\[
                         z^3+2z^2-2.                          \tag{23}
\]

Its discriminant is \(-44\), and exact reduction modulo
\((S+2,G,p-2)\) gives

\[
                         D^2=-44,\qquad W=24.                 \tag{24}
\]

Thus \(\Delta _{p=2}\ne0\). If \(p\ne2\), then every factor of
\(\Delta_G\) displayed in the first row of (21) is nonzero. The
omitted case \(p=0\) is coordinate and is handled in Section 7. In
fact its elementary cubic is \(z^2(z+2)\), so its set of points is
exactly the three coordinate endpoints listed there.

### 6.2. The \(L=0\) branch

The condition \(p=-1\) makes the elementary cubic

\[
             z^3+3z^2+3z+1=(z+1)^3,                           \tag{25}
\]

so \((a,c,e)=(-1,-1,-1)\). If \(D=0\), take the repeated
coordinate to be \(x\) and the third coordinate to be \(y\). The
exact elimination identity, the same in each of the three
orientations, is

\[
             \operatorname {Res}_y(Q(x,x,y),L(x,x,y))
             =-15(x+1)^2.                                    \tag{26}
\]

This again gives only the all-one point. At that point a direct-free
maximal minor is the nonzero constant

\[
                         -2^{40}3^{22}.                        \tag{27}
\]

### 6.3. The \(K=0\) branch

The overlap \(G=0\) was just closed. By (20), the overlap \(J=0\)
is the all-one point. Away from those overlaps, \(\Delta_K\) can
vanish only when \(D=0\). For a repeated coordinate \(x\), exact
elimination gives

\[
 \operatorname {Res}_y(Q(x,x,y),K(x,x,y))
 =-3(x+1)^2(x^2+4x+6).                                      \tag{28}
\]

The \(x=-1\) solution is all-one. On

\[
             h=x^2+4x+6=0,\qquad y=-{2x+8\over3},             \tag{29}
\]

the numerator remainders of \(F\) modulo \(h\) are

\[
\begin{array}{c|c|c}
\text{repeated pair}&F\bmod h&\gcd(h,F\bmod h)\\ \hline
a=c&-48(x+7)&1\\
a=e&-48(x+7)&1\\
c=e&-144(x+1)&1.
                                                               \tag{30}
\end{array}
\]

The other factors of \(\Delta_P\) are nonzero by the branch
assumptions, so (30) closes every non-all-one solution of (28).

### 6.4. The \(J=0\) branch

The overlap \(G=0\) is closed, and the overlap \(K=0\) is all-one by
(20). Otherwise \(\Delta_J\) can vanish only when \(X=0\). At such
a point \(\Delta_L\) can vanish only when \(D=0\). For a repeated
coordinate \(x\), exact elimination now gives

\[
 \operatorname {Res}_y(Q(x,x,y),J(x,x,y))
 =-3x(x+1)^2(x+4).                                           \tag{31}
\]

The corresponding third coordinates are

\[
 (x,y)=(0,-2),\quad(-1,-1),\quad(-4,-2/5).                    \tag{32}
\]

The first is coordinate and the second is all-one. In the three
orientations the exact restrictions of \(X\) are

\[
 X|_{a=c}=X|_{a=e}=(x+2)(x-y),\qquad
 X|_{c=e}=-2(x+2)(x-y).                                      \tag{33}
\]

They are nonzero at \((-4,-2/5)\), so (33) eliminates the last
possibility. This completes every non-coordinate row of (21).

## 7. Coordinate curves and their endpoints

It remains to remove \(a=0\), \(c=0\), or \(e=0\) on \(Q=0\).
Each coordinate section is an entire rational curve:

\[
\begin{array}{c|c}
a=0&e=-(3c+6)/(c+3)\\
c=0&e=-(3a+6)/(a+3)\\
e=0&c=-(3a+6)/(a+3).
                                                               \tag{34}
\end{array}
\]

No point is lost to a denominator in (34), since substituting the
putative pole gives respectively
\(Q|_{a=0,c=-3}=Q|_{c=0,a=-3}=Q|_{e=0,a=-3}=-3\).

For \(a=0\), three direct-free maximal minors have the following
squarefree numerator supports after the first parametrization in
(34), up to nonzero rational units:

\[
\begin{aligned}
A_0={}&c(c+2)(c^2+3c+3)(3c^2+8c+6)(4c^2+9c+3),\\
A_3={}&c(c+2)(c^2-6c-24)(c^2+6c+6)(3c^2+8c+6),\\
A_{11}={}&c(c+2)(c^2-6)(c^2-6c-24)\\
          &\hspace{17mm}{}\cdot(c^2+3c+3)(c^2+6c+6),\\
\gcd(A_0,A_3,A_{11})={}&c(c+2).                              \tag{35}
\end{aligned}
\]

For \(c=0\), three such supports are

\[
\begin{aligned}
C_0={}&a(a+2)(a^2-6a-24)(a^2+3a+3)(a^2+6a+6)
          (3a^2+8a+6),\\
C_1={}&a(a+2)(a^2-6a-24)(a^2+6a+6)
          (3a^2+8a+6)(4a^2+9a+3),\\
C_5={}&a(a+2)(a^2+3a+3)(4a^2+9a+3),\\
\gcd(C_0,C_1,C_5)={}&a(a+2).                                 \tag{36}
\end{aligned}
\]

For \(e=0\), the corresponding supports are

\[
\begin{aligned}
E_0={}&a(a+2)(a^2+3a+3)(3a^2+8a+6),\\
E_1={}&a(a+2)(a^2+12a+12)(3a^2+8a+6)(4a^2+9a+3),\\
E_5={}&a(a+2)(a^2-6)(a^2+3a+3)(4a^2+9a+3),\\
\gcd(E_0,E_1,E_5)={}&a(a+2).                                 \tag{37}
\end{aligned}
\]

Thus the only common zeros on the three coordinate curves are

\[
                    (-2,0,0),\qquad(0,-2,0),\qquad(0,0,-2).    \tag{38}
\]

At these points, respectively, three further direct-free maximal
minors, again independent of \(b,d,f\), are the constants

\[
                 -2^{65}3^{18},\qquad
                  2^{66}3^{18},\qquad
                  2^{66}3^{18}.                               \tag{39}
\]

Equations (19)--(39) prove that the rank is 19 at every point of
\(Q=0\) in the central \(01^3\) chart. There is no \(Q\)-boundary
survivor.

## 8. The complement of \(Q=0\) away from the coordinate planes

Two more direct-free, nuisance-independent maximal minors close all
points with \(aceQ\ne0\). Put

\[
\begin{aligned}
 U&=6p+3G+S,\\
 V&=4a^2ce+a^2c+4a^2e-ac^2+3ace-c^2e.
                                                               \tag{40}
\end{aligned}
\]

Exact fraction-free elimination gives

\[
\begin{array}{c|l}
\text{name}&\text{determinant}\\ \hline
N_{99}&2^{39}3^7a^6c^8e^5(c+e)(a+c)(S+3)KQ^2\\
N_{98}&2^{41}3^7a^7c^7e^6J^4UV.
                                                               \tag{41}
\end{array}
\]

Thus, after localizing at \(aceQ\), their squarefree supports may be
replaced by

\[
 N_{99}^{\circ}=(c+e)(a+c)(S+3)K,\qquad
 N_{98}^{\circ}=JUV.                                          \tag{42}
\]

Suppose that all nine minors in (19) and (41) vanish.  The factor
\(GLKJ\) in \(\Delta _0\) gives the first split.  If \(G=0\), then
\(P=SG-p=-p\ne0\) and \(J=3p\ne0\); hence \(\Delta_G\) forces
\(L=0\) or \(K=0\), while \(\Delta_{p=2}\) forces \(D=0\) or
\(W=0\).  If \(G\ne0\), the remaining minors give the exhaustive
split

\[
\begin{array}{c|l}
\text{case}&\text{forced subbranches}\\ \hline
G=0&(G,L,D),(G,L,W),(G,K,D),(G,K,W)\\
G\ne0,\ K=J=0&(K,J,D),(K,J,W)\\
G\ne0,\ K=0,\ J\ne0&(K,F,D)\\
G\ne0,\ K\ne0,\ J=0&(J,X,D)\\
G K J\ne0&(L,X,F,D).
                                                               \tag{43}
\end{array}
\]

For each \(D=0\) branch, substitute in turn

\[
 (a,c,e)=(x,x,y),\qquad(x,y,x),\qquad(y,x,x).                  \tag{44}
\]

Adjoin \(N_{99}^{\circ}\), \(N_{98}^{\circ}\), and the localization
equation \(1-\tau aceQ\).  On the \(G\ne0\) families also put \(G\)
in the localizer.  Exact Gröbner reduction gives the unit ideal for
each of the following 21 localized branch ideals:

\[
\begin{array}{c|c}
\text{branch family}&\text{orientations}\\ \hline
(G,L,D)&ac,\ ae,\ ce\\
(G,K,D)&ac,\ ae,\ ce\\
(K,J,D)&ac,\ ae,\ ce\\
(K,F,D)&ac,\ ae,\ ce\\
(J,X,D)&ac,\ ae,\ ce\\
(L,X,F,D)&ac,\ ae,\ ce\\
(G,L,W),\ (G,K,W),\ (K,J,W)&\text{no repeated-pair split}.
                                                               \tag{45}
\end{array}
\]

Therefore no common zero of the certified maximal minors lies in
\(aceQ\ne0\).

## 9. The three coordinate planes

It remains to treat \(ace=0\), now without imposing \(Q=0\).  The
whole planes are used, so their pairwise intersections and the origin
are included. Define

\[
\begin{gathered}
 R_a=ae+2a+2e,\qquad R_c=ac+2a+2c,\qquad R_e=ce+2c+2e,\\
 Y=ac-2ae-2a+ce+4c-2e.
                                                               \tag{46}
\end{gathered}
\]

Three initial direct-free maximal minors factor exactly as

\[
\begin{array}{c|l}
\text{plane witness}&\text{determinant}\\ \hline
A_{\rm pl}&2^{38}3^9c^9e^8G^2K^4R_aR_cY\\
C_{\rm pl}&2^{37}3^9a^8e^7G^2K^4R_cXR_e^2\\
E_{\rm pl}&2^{37}3^9a^8c^7G^2K^4R_aXR_e^2.
                                                               \tag{47}
\end{array}
\]

Combine these with the coordinate-curve and endpoint minors from
Section 7 and with independently selected axis and origin minors.
Taking squarefree restricted supports, nine witnesses on each plane
have the following exact lexicographic Gröbner bases:

\[
\begin{array}{c|l}
\text{plane}&\text{basis}\\ \hline
a=0&
91c+112e^2+283e+300,\quad (e+2)(7e^2+12e+9)\\
c=0&a+2,\quad e+2\\
e=0&a+2,\quad c+2.
                                                               \tag{48}
\end{array}
\]

The apparent quadratic residue on \(a=0\) is removed by one further
direct-free minor.  Its squarefree support on that plane is, up to a
nonzero rational unit,

\[
 ce(c-e)(c+e)(c+e+3)
 (ce+3c+3e+6)(3ce+c+e).                                      \tag{49}
\]

Adding (49) changes the first basis in (48) to \(c+2,e+2\).
Consequently the only possible coordinate-plane survivors are

\[
 (a,c,e)=(0,-2,-2),\qquad(-2,0,-2),\qquad(-2,-2,0).            \tag{50}
\]

At these three points, respectively, direct-free response determinants
restrict identically in the nuisance parameters \(b,d,f\) to

\[
                  2^{68}3^9,\qquad
                  2^{66}3^{12},\qquad
                  2^{66}3^{12}.                               \tag{51}
\]

They are nonzero.  Together with Sections 5--8, this proves
Proposition 1.2.

## 10. Exact scope

The minimal multiple-rescue problem has therefore been reduced as
follows:

1. equations (2) remove exactly two structurally forbidden rows;
2. equation (12) is the full remaining 19-column system;
3. every one of the 27 row-plane chart products is generically
   injective;
4. the entire central \(01^3\) chart is uniformly injective, including
   all zero-parameter and divisor values within that affine chart;
   and
5. all 26 noncentral boundary cells are uniformly closed by exact
   direct-free maximal-minor certificates.

Therefore the complete 27-cell response has rank \(19\) everywhere for the
minimal multiple-rescue configuration (1), with arbitrary direct
\(B_{01}\) scale.  This statement is specific to that first
three-extra configuration: it does not close the two-extra frontier, the
sole-extra high-\(t\) frontier, larger three-extra profiles, or the
nonrescue families.

## 11. Exact audit

[verify_live_three_zero_minimal_three_extra_frontier.py](../computations/verify_live_three_zero_minimal_three_extra_frontier.py)
reconstructs the rows (14) from (12), proves the factorization (4) over
\(\mathbb Q[a,b,c,d,e,f]\), and checks generic rank 19 in all 27 chart
products.

[verify_live_three_zero_minimal_three_extra_q0.py](../computations/verify_live_three_zero_minimal_three_extra_q0.py)
reconstructs every direct-free maximal minor in (19), (27), and (39),
checks all ideal identities in (20), all resultants and remainders in
(24)--(33), and every squarefree support and gcd in (35)--(37). The
row generator is
[explore_live_three_zero_minimal_three_extra_response.py](../computations/explore_live_three_zero_minimal_three_extra_response.py).

[verify_live_three_zero_minimal_three_extra_central_uniform.py](../computations/verify_live_three_zero_minimal_three_extra_central_uniform.py)
re-runs that \(Q=0\) audit, reconstructs (41) and (47), checks all 21
localized unit ideals in (45), computes the three plane ideals (48)--(49),
and verifies the nuisance-independent endpoint constants (51).

[verify_live_three_zero_minimal_three_extra_boundary_low_cells.py](../computations/verify_live_three_zero_minimal_three_extra_boundary_low_cells.py)
checks the 17 uniformly closed noncentral cells and the exact reduced
cell census described in the companion boundary note.

[verify_live_three_zero_minimal_three_extra_cbb_cells.py](../computations/verify_live_three_zero_minimal_three_extra_cbb_cells.py)
checks all three CBB placements by exact localized branch covers, and
[verify_live_three_zero_minimal_three_extra_cce_cells.py](../computations/verify_live_three_zero_minimal_three_extra_cce_cells.py)
checks exact unit-minor ideals on all three CCE placements.  Finally,
[verify_live_three_zero_minimal_three_extra_ccb_cells.py](../computations/verify_live_three_zero_minimal_three_extra_ccb_cells.py)
runs the exact localized branch cover independently on CCB, CBC, and BCC.
Finite-field points in that audit select row labels only; every determinant
and every final unit-ideal computation is reconstructed over \(\mathbb Q\).
