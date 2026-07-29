# Adjacent five-cut compatibility stops at a two-star Hessian boundary

## 1. Outcome

Let (S) be a six-set, let (R) be a disjoint pair, and for (zin S)
put

\[
 U_z=S\setminus\{z\},\qquad K_z=\ker {\cal B}_{U_z}.
\]

The most direct way to compare the high-crossing identities on adjacent
five-sets is to ask for one six-site functional whose two curries lie in
the two cofactor kernels.  This note gives the exact boundary of that idea.

Define

\[
 L_z=V_z^*\otimes K_z\subseteq V_S^*,\qquad
 E_z=V_z\otimes {\cal S}_{U_z}\subseteq V_S.             \tag{1}
\]

Then (L_z=E_z^\perp).  If there is

\[
 \eta\in\bigcap_{z\in S}L_z,
 \qquad
 \delta_S(\eta)=\sum_{r=0}^2\eta(e_r^{\otimes S})e_r\ne0,              \tag{2}
\]

the order-eight ternary GHZ equation is impossible.  The proof is
division-free: the six one-crossing sectors vanish under (eta), their
exact sum is (6T_0+2T_2), and (eta) also kills (T_0).  Thus (2) is a
genuine sufficient overlap criterion.

It is not automatic, even for two adjacent five-sets.  A sparse integral
six-site family below has

\[
 W_{U_2}=\delta_{U_2}(K_2)=\langle e_2\rangle,
 \qquad
 W_{U_3}=\delta_{U_3}(K_3)=\langle e_1\rangle,             \tag{3}
\]

so both individual defect spaces are nonzero, as required by the universal
five-set theorem, but

\[
                     L_2\cap L_3\subseteq\ker\delta_S.    \tag{4}
\]

Thus the precise proposed overlap lemma

> two target-active adjacent cofactor kernels always have a target-active
> common six-site extension

is false.  Shared four-site cofactors alone cannot provide the comparison;
one must use the actual three-crossing response maps in addition to the
spaces (K_U\twoheadrightarrow W_U).

The exact audit is
[`verify_adjacent_five_cut_hessian_intersection_countermodel.py`](../computations/verify_adjacent_five_cut_hessian_intersection_countermodel.py).

## 2. Lifted kernels are annihilators of star Hessian images

Recall

\[
 {\cal S}_{U_z}=\sum_{u\in U_z}V_u\otimes
                H_{S\setminus\{z,u\}}(A).               \tag{5}
\]

Because the factor (V_z) is unrestricted,

\[
 \begin{aligned}
 E_z
 &=\sum_{u\ne z}V_z\otimes V_u\otimes
                   H_{S\setminus\{z,u\}}(A),\\
 E_z^\perp
 &=V_z^*\otimes {\cal S}_{U_z}^\perp
   =V_z^*\otimes K_z=L_z.                                \tag{6}
 \end{aligned}
\]

The space (E_z) is exactly the (z)-star part of the source Hessian
image: its summand indexed by (zu) replaces the edge (A_{zu}) by an
arbitrary tensor and retains the four-site cofactor on the other vertices.
Consequently, for any (Z\subseteq S), finite-dimensional duality gives

\[
 \left(\bigcap_{z\in Z}L_z\right)^\perp
                      =\sum_{z\in Z}E_z.                 \tag{7}
\]

Writing

\[
 {cal G}_S=\langle e_0^{\otimes S},e_1^{\otimes S},
                         e_2^{\otimes S}\rangle,          \tag{8}
\]

there is a target-active common extension precisely when

\[
             {\cal G}_S\not\subseteq\sum_{z\in Z}E_z.     \tag{9}
\]

This is the exact Hessian-cokernel content of the common-extension route;
no ranks or divisions have been used.

## 3. A common six-cut defect would exclude order eight

Let (B=S\mathbin{\dot\cup}R), with (|S|=6) and (|R|=2).  Relative to
the even cut (S|R), write (T_0,T_2) for the sectors having zero and two
crossing edges.  For (z\in S), let (T_{1,z}) be the one-crossing sector
for the odd cut

\[
                    (R\cup\{z\})\mid U_z.                \tag{10}
\]

Every matching in (T_0) is counted in all six tensors (T_{1,z}).  In a
matching in (T_2), the two vertices of (R) have two partners in (S),
and exactly those two choices of (z) make (10) a one-crossing cut.  Hence,
atom by atom and with arbitrary endpoint tensors,

\[
                     \boxed{\ \sum_{z\in S}T_{1,z}=6T_0+2T_2.\ }       \tag{11}
\]

Now take (eta\in\bigcap_zL_z).  For a fixed (z), every curry of
(eta) in the (z)-slot belongs to (K_z).  The cofactor-wise
factorization of the one-crossing sector therefore gives

\[
               (\eta\otimes\operatorname{id}_R)T_{1,z}=0.             \tag{12}
\]

Also, expansion of the internal six-site tensor at (z) gives

\[
 H_S(A)=\sum_{u\ne z}A_{zu}\otimes
                   H_{S\setminus\{z,u\}}(A)\in E_z.     \tag{13}
\]

Thus (eta(H_S)=0), and since (T_0=A_R\otimes H_S),

\[
               (\eta\otimes\operatorname{id}_R)T_0=0.                 \tag{14}
\]

Contracting (11) and using (12)--(14) kills (T_2) as well.  Therefore

\[
               (\eta\otimes\operatorname{id}_R)H_B(A)=0.              \tag{15}
\]

If (H_B(A)=\Delta_{8,3}), the left side is instead

\[
 \sum_{r=0}^2\eta(e_r^{\otimes S})e_r^{\otimes R},       \tag{16}
\]

which is nonzero exactly when (delta_S(\eta)\ne0).  This proves the
sufficient criterion (2).

## 4. Exact adjacent-pair countermodel

Take (S=\{0,1,2,3,4,5\}).  Put one coordinate cell on each edge in the
following three one-factors, and put every omitted block equal to zero:

\[
\begin{array}{c|c|c}
 r&M_r&A_{uv}\text{ on }uv\in M_r\\ \hline
0&01,23,45&E_{00}\\
1&02,14,35&E_{11}\\
2&03,15,24&E_{22}.
\end{array}                                                \tag{17}
\]

There are four supported decorated perfect matchings, and direct expansion
gives

\[
 H_S=e_0^{\otimes6}+e_1^{\otimes6}+e_2^{\otimes6}
       +e_0^{(0)}e_0^{(1)}e_2^{(2)}e_1^{(3)}
                       e_2^{(4)}e_1^{(5)}.                \tag{18}
\]

The following three four-site cofactors are private:

\[
 H_{0145}=e_0^{\otimes\{0,1,4,5\}},\qquad
 H_{1345}=e_1^{\otimes\{1,3,4,5\}},\qquad
 H_{1245}=e_2^{\otimes\{1,2,4,5\}}.                     \tag{19}
\]

They give the exact Hessian-column identities

\[
\begin{aligned}
 e_0^{\otimes S}&=E_{00}^{(23)}\otimes H_{0145}\in E_2,\\
 e_1^{\otimes S}&=E_{11}^{(02)}\otimes H_{1345}\in E_2,\\
 e_2^{\otimes S}&=E_{22}^{(03)}\otimes H_{1245}\in E_3.
\end{aligned}                                             \tag{20}
\]

Hence

\[
                    {\cal G}_S\subseteq E_2+E_3.          \tag{21}
\]

Equations (7)--(9) now prove (4): every common extension in
(L_2\cap L_3) is target-zero.

This is not caused by either individual five-set losing its universal
defect.  The adjacent sets are

\[
 U_2=(0,1,3,4,5),\qquad U_3=(0,1,2,4,5),\qquad
 U_2\cap U_3=(0,1,4,5).                                  \tag{22}
\]

For (U_2), the first two constant tensors lie in
({\cal S}_{U_2}), using respectively the first two cofactors in (19).
The sparse functional

\[
 \beta_2=e_{22222}^*-e_{00121}^*
 \quad\text{(site order }0,1,3,4,5\text{)}               \tag{23}
\]

annihilates all fifteen cofactor-insertion columns and has
(delta_{U_2}(\beta_2)=e_2).  Therefore

\[
 {cal G}_{U_2}\cap {\cal S}_{U_2}
     =\langle e_0^{\otimes U_2},e_1^{\otimes U_2}\rangle,
 \qquad W_{U_2}=\langle e_2\rangle.                      \tag{24}
\]

Similarly, for site order (0,1,2,4,5),

\[
 \beta_3=e_{11111}^*-e_{00221}^*\in K_3,
 \qquad \delta_{U_3}(\beta_3)=e_1,                       \tag{25}
\]

while the color-zero and color-two constants lie in
({\cal S}_{U_3}).  Hence

\[
 {cal G}_{U_3}\cap {\cal S}_{U_3}
     =\langle e_0^{\otimes U_3},e_2^{\otimes U_3}\rangle,
 \qquad W_{U_3}=\langle e_1\rangle.                      \tag{26}
\]

All assertions use only zero-one edge entries and exact coefficient
identities.  The checker also independently reconstructs every cofactor
column and verifies (23)--(26) by rational row reduction.

## 5. Consequence for the high-crossing route

The universal five-set theorem supplies (W_U\ne0) separately on every
cut.  Equations (3)--(4) show that this does not supply even a target-active
common extension for one adjacent pair.  Therefore an overlap proof cannot
first choose compatible elements of the kernels and only afterward compare
their three-crossing images.

The live datum is the full family of quotient maps

\[
 K_U\longrightarrow W_U,
 \qquad
 (T_{3,U})^\flat\big|_{K_U}=\iota_{B\setminus U}\delta_U\big|_{K_U},   \tag{27}
\]

with the same cross-edge entries appearing in the maps for neighboring
five-sets.  A stronger adjacent-cut lemma must use those maps themselves
(or their edge-factorized syzygies).  It cannot be a statement about the
cofactor kernels, the defect spaces, or their lifted intersections alone.

The countermodel in Section 4 concerns the shared internal six-site edge
family; it is not an eight-site family satisfying both equations (27).
Accordingly it rules out the kernel-only overlap lemma, not a stronger
lemma that assumes the two complete high-crossing restriction identities.
