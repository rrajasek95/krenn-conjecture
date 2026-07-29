# The first sole-plane high-split layer closes uniformly

## 1. Outcome

The finite closure of \((r,t)=(3,6)\) in
[live-three-zero-sole-plane-first-high-closure.md](live-three-zero-sole-plane-first-high-closure.md)
comes from a mechanism that is uniform in \(r\).

**Theorem 1.1 (uniform first-high-layer closure).**  Suppose there is one
extra singular site of eligible type \(M_e=\{2\}\), the live shore has size
\(2r\), and

\[
                         r\ge3,\qquad t=r+3.                    \tag{1}
\]

Then the complete residual response at the shared zero is injective for
every structurally admissible collection of exceptional beta values and
every source-side row plane at \(e\).  Repetitions of arbitrary
multiplicity and singleton beta value zero are allowed.  The direct
\(B_{01}\) scale is arbitrary.

Consequently the remaining sole-plane frontier is

\[
                         r\ge4,\qquad r+4\le t\le2r.             \tag{2}
\]

In particular, the next point \((r,t)=(4,7)\) is not a new finite-profile
obstruction.  The first point not reached by this theorem is \((4,8)\).

## 2. Uniform permanent pivots

Normalize \(\mu=1\) and

\[
 H=\begin{pmatrix}0&1&1\\1&0&1\\1&1&0\end{pmatrix},\qquad
 P_i=I\ (i\text{ live}),\qquad
 P_c=P_d=D=\operatorname {diag}(1,1,0).                         \tag{3}
\]

Let \(E\) be the exceptional live set.  Under (1),

\[
                         |E|=r+3.                               \tag{4}
\]

There are \(r-3\) common-beta live sites.  Together with \(c,d\), put

\[
              A=(U\setminus E)\sqcup\{c,d\},\qquad |A|=r-1.    \tag{5}
\]

The active response sites are \(A\sqcup\{e\}\), hence there are \(3r\)
columns.  Every exceptional star is already zero because
\((\nu_i-1)q_{i z_0}=0\).

For tuples of length \(r\), write

\[
 \mathcal C_r(X\mid Y)
       =\operatorname {per}\left({1\over x_i+y_j}\right)_{i,j=1}^r.
                                                                    \tag{6}
\]

Only two pivot families are needed.  First choose

\[
 m\in E,\qquad E\setminus\{m\}=L\sqcup\{x,y\},\qquad |L|=r,
\]

and put

\[
 P_{m;L\mid x,y}
   =\mathcal C_r\bigl(\nu_L\mid
          (\underbrace{1,\ldots,1}_{r-2},\nu_x,\nu_y)\bigr).    \tag{7}
\]

Second choose

\[
 B\subset E,\quad |B|=2,\qquad
 E\setminus B=L\sqcup\{o\},\quad |L|=r,
\]

and put

\[
 S_{B;L,o}
   =\mathcal C_r\bigl(\nu_L\mid
          (\underbrace{1,\ldots,1}_{r-1},\nu_o)\bigr).          \tag{8}
\]

At \(r=3\), these are the earlier \(P\) and two-equal-common \(S\)
families.  The opposite-common \(R\) family from the finite certificate is
valid but redundant: (8) performs both extra-star and third-row cleanup.

## 3. The \(S_r\) family never vanishes simultaneously

Put

\[
             a_i={1\over\nu_i+1},\qquad
             h_i(o)={\nu_i+1\over\nu_i+\nu_o}.                  \tag{9}
\]

All these numbers are structurally nonzero.  Expanding (8) along its sole
exceptional column gives

\[
 S_{B;L,o}=(r-1)!\left(\prod_{i\in L}a_i\right)
                         \sum_{i\in L}h_i(o).                   \tag{10}
\]

Fix \(o\).  Then \(N=E\setminus\{o\}\) has size \(r+2\), and varying the
marked pair \(B\subset N\) makes \(L=N\setminus B\) run over every
\(r\)-subset.  If all pivots (10) vanished, every \(r\)-subset sum of the
\(r+2\) numbers \(h_i(o)\) would vanish.  The fixed-size subset incidence
matrix has full point-column rank in characteristic zero, so every
\(h_i(o)\) would be zero.  This is impossible.  Thus

\[
                         \boxed{\text{some }S_{B;L,o}\ne0}.      \tag{11}
\]

This argument uses no equality-profile or nonzero-beta assumption beyond
the actual structural denominators.

## 4. The \(P_r\) deletion system

Fix distinct labels \(x,y\in E\), put

\[
 N=E\setminus\{x,y\},\qquad |N|=r+1,
\]

and define, for \(i\in N\),

\[
 u_i={\nu_i+1\over\nu_i+\nu_x},\qquad
 v_i={\nu_i+1\over\nu_i+\nu_y}.                                \tag{12}
\]

Expanding the two exceptional columns of (7), with
\(L=N\setminus\{m\}\), gives a structurally nonzero factor times

\[
 Q_L=\sum_{\substack{i,j\in L\\i\ne j}}u_i v_j
     =\sum_{\{i,j\}\subset L}f_{ij},\qquad
 f_{ij}=u_iv_j+u_jv_i.                                         \tag{13}
\]

Suppose every \(P_r\) pivot vanishes.  For fixed \(x,y\), all \(r+1\)
one-point deletions \(Q_{N\setminus\{m\}}\) vanish.  Put

\[
 T=\sum_{\{i,j\}\subset N}f_{ij},\qquad
 s_m=\sum_{j\ne m}f_{mj}.                                      \tag{14}
\]

The deletion equation is \(T-s_m=0\).  Summing it over \(m\) gives
\((r-1)T=0\), because \(\sum_m s_m=2T\).  Hence

\[
                              T=s_m=0\quad(m\in N).              \tag{15}
\]

Let

\[
 U=\sum_{i\in N}u_i,\qquad V=\sum_{i\in N}v_i,qquad
 w_i={1\over\nu_i+1}.
\]

Dividing the row-sum equation in (15) by \(u_iv_i\ne0\) yields

\[
 (U+V-2)+\bigl(V(\nu_y-1)+U(\nu_x-1)\bigr)w_i=0
                         \qquad(i\in N).                        \tag{16}
\]

We now exclude all possible equality patterns.

### 4.1 Repeated values

First suppose all exceptional beta values equal \(\nu\).  Every term of
(7) is the same, so

\[
 P_{m;L\mid x,y}
   ={r!\over(\nu+1)^{r-2}(2\nu)^2}\ne0.                         \tag{17}
\]

Otherwise, if some value repeats, one can choose two equal labels \(x,y\)
so that \(N\) still contains at least two beta values.  Indeed, choose a
repeated class of maximal multiplicity: removing two copies either leaves
that class and another class, or, if its multiplicity is two, at least two
other classes remain.  Thus the numbers \(w_i\) in (16) take at least two
values, forcing both affine coefficients to vanish:

\[
 U+V=2,qquad V(\nu_y-1)+U(\nu_x-1)=0.                           \tag{18}
\]

But \(\nu_x=\nu_y\ne1\), so the second equation is
\((\nu_x-1)(U+V)=0\), contradicting the first.

### 4.2 All values distinct

It remains to suppose all \(\nu_i\) are distinct.  Write
\(x=\nu_x,y=\nu_y\).  Solving (18) gives

\[
 U={2(1-y)\over x-y}.                                           \tag{19}
\]

For fixed \(x\), put

\[
 T_x=\sum_{i\in E\setminus\{x\}}{\nu_i+1\over\nu_i+x}.
\]

Since \(U=T_x-(y+1)/(x+y)\), equation (19) says that

\[
 T_x=F_x(y):={y+1\over x+y}+{2(1-y)\over x-y}                  \tag{20}
\]

for every \(y\ne x\).  Direct subtraction gives

\[
 F_x(y)-F_x(z)=
 -{(x-1)(y-z)\bigl(x^2+3x(y+z)+yz\bigr)
    \over (x-y)(x+y)(x-z)(x+z)}.                                \tag{21}
\]

Every displayed factor outside the quadratic is structurally nonzero.
Hence

\[
                         x^2+3x(y+z)+yz=0                       \tag{22}
\]

for every two labels \(y,z\ne x\).  Choose three distinct such values
\(y,z,q\).  Subtracting (22) for \((y,z)\) and \((y,q)\) gives
\((z-q)(3x+y)=0\), so \(y=-3x\).  Repeating with \(z\) in place of
\(y\) gives \(z=-3x\), contradicting \(y\ne z\).

Thus simultaneous vanishing was impossible in every equality pattern:

\[
                         \boxed{\text{some }P_{m;L\mid x,y}\ne0}.\tag{23}
\]

Unlike the finite profile ideals at \(r=3\), (23) does not need the
heavy-class bound at all.

## 5. Noncoordinate row planes

Let \(R_e=\operatorname {row}P_e\ne\langle e_0,e_1\rangle\), and choose
\(p=(p_0,p_1,p_2)\in R_e\) with \(p_2\ne0\).  Give \(m\) colour two,
contract \(e\) to \(p\), and use source \(22\).  The unique marked pair is
\(\{m,e\}\), with coefficient \(2p_2\).

Choose a nonzero pivot (7).  For a target \(a\in A\), put the target and
the labels of \(L\) on one binary shore, and put
\((A\setminus\{a\})\sqcup\{x,y\}\) on the other.  Removing the target
leaves \(r\) sites on each shore; moving the star to another member of
\(A\) leaves \(r+1\) and \(r-1\).  Therefore the literal singleton is

\[
                         2p_2P_{m;L\mid x,y}Z_{a,0}=0.           \tag{24}
\]

Binary colour swap kills \(Z_{a,1}\).  For \(a=c,d\), replacing the target
by its zero local third row gives the same singleton and kills
\(Z_{a,2}\).  Thus every binary row in \(A\) and every centre third row
vanishes.

Choose a nonzero pivot (8).  Give \(B\) colour two, give \(L\) colour zero,
and give \(A\sqcup\{o\}\) colour one.  Contract \(e\) by an arbitrary
output covector \(\eta\).  The star at \(e\) has coefficient \(2S_{B;L,o}\):

\[
                         2S_{B;L,o}\eta^{\mathsf T}q_{e z_0}=0. \tag{25}
\]

All contamination lies in the already-vanishing binary rows of \(A\).
Thus the complete extra block vanishes.  Finally replace one common live
site by its genuine third row in (24).  The target coefficient is unchanged;
additional marked pairs land only in already-vanishing active columns.
This triangularly kills all \(r-3\) remaining third rows.

## 6. The coordinate row plane

If \(R_e=\langle e_0,e_1\rangle\), an output change puts \(P_e=D\).  There
are now \(r\) symmetric active sites \(A\sqcup\{e\}\).  Choose a nonzero
\(S\) pivot.  For any target, put the target and \(L\) on one binary shore,
and put every other active site together with \(o\) on the other.  The
source-\(22\) marked pair is exactly \(B\), and only the target star is
balanced.  Thus

\[
                            2S_{B;L,o}Z_{a,j}=0\qquad(j=0,1),    \tag{26}
\]

where both orientations follow by binary colour swap.

For each D-type target \(c,d,e\), replace its local row by the zero third
row while retaining the same shore counts.  Every off-target cofactor now
contains that zero row, while the target coefficient remains \(2S\).  This
kills their third rows literally.  Finally give a common live target its
nonzero third row.  The marked pair \(B\) still gives target coefficient
\(2S\); the extra marked pairs involving the target contaminate only binary
active columns already killed by (26).  This kills every common-live third
row and completes the coordinate plane.

All selected rows use source \(22\), so the arbitrary direct \(B_{01}\)
scale has coefficient zero identically.  The same three-chart cover as in
the finite \((3,6)\) note splits the \(01\) chart into
\(a\ne0\), \(a=0,b\ne0\), and the coordinate point \((a,b)=(0,0)\), while
the \(12\) and \(02\) charts are noncoordinate.  This proves Theorem 1.1.

## 7. Exact audit

[verify_live_three_zero_sole_plane_first_high_layer_uniform.py](../computations/verify_live_three_zero_sole_plane_first_high_layer_uniform.py)
checks the fixed-size incidence ranks, the two-column expansion, the
one-point deletion row-sum identity, the repeated-value affine
contradiction, the exact rational identity (21), and the elementary
selection lemma for repetition profiles.  It then reconstructs the literal
marked-matching response at \(r=3,4,5\), using exact fractions and a stress
profile with a singleton zero beta and repeated nonzero values.  Every
D-type target is tested with its actual zero local row, every common-live
I-type third row is tested with all triangular contamination retained, and
both coordinate orientations are included.  A nonzero direct scale is kept
throughout.

[explore_live_three_zero_sole_plane_second_high_permanents.py](../computations/explore_live_three_zero_sole_plane_second_high_permanents.py)
is independent finite-profile reconnaissance at \((4,7)\).  Its localized
ideals agree with the theorem on the tested profiles, but the proof above
uses neither that census nor a Gröbner computation.
