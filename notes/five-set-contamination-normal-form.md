# Triple-shore contamination and its finite normal form

## 1. Outcome

Fix an even vertex set and a three-vertex shore
`B=C disjoint-union U`.  The exposed shore `U` is odd.  Every matching
crosses the cut one or three times, so split

\[
                         H_B(A)=T_1+T_3.                  \tag{1}
\]

The failure of the odd-shore response criterion has a completely explicit
row-space description.  Write the coefficient rows of `T_3` on the exposed
odd shore as `h_a`, where `a` is a coloring of `C`, and let `M_U` be the span
of the rows whose coloring is mixed.  Then

\[
 \mathcal G_C\cap\operatorname {LS}_C(T_3)\ne0
 \quad\Longleftrightarrow\quad
 h_{r^C}\notin M_U\text{ for at least one }r.             \tag{2}
\]

More precisely, the entire intersection is dual to the span of the three
constant-row residue classes in `V_U/M_U`.  This is an exact
characterization, not merely a sufficient test, and it retains all
cancellation in the complete three-crossing sector.

The one-crossing sector is a sum of exactly three slices whose complementary
factors are the three internal edge matrices of `C`, at every even order.
If all three constant rows of this sector survive modulo `M_U`, three-slice
rigidity gives a finite normal form.  According to the dimension of the
surviving diagonal space:

* dimension three forces the three internal edges to be nonzero pure
  same-color edges of three distinct colors;
* dimension two forces all deviation from those three pure edges through
  one shared tensor.  If the unique equation of the diagonal plane uses two
  colors, one internal edge is pure and the other two share a one-vertex
  leakage vector.  If it uses all three colors, the leakage is a single
  rainbow cell;
* dimension one permits cancellation only on pairwise intersections of the
  three center planes, with an explicit three-transfer normal form.

Thus an order-minimal realization reduces to the following exact finite
alternative on every triple: either a named
constant-row degeneracy occurs, or its three internal edge matrices have
one of the displayed coordinate normal forms.  This does not yet prove that
the degeneracy alternatives imply the all-triple-zero hypothesis, but it
isolates precisely the missing implication.

There is also a bounded product-cap version.  The mixed-row space has
dimension at most nine, independently of `|B|`.  Every nonzero diagonal
contamination direction can therefore be witnessed by a linear combination
of at most ten coordinate-word covectors on `U`; if all three diagonal
colors are required simultaneously, at most twelve suffice.  Each summand
is an explicit three-cross vector-permanent response.

## 2. Coefficient rows and the exact quotient

Use the word basis `e_a=bigotimes_(c in C)e_(a_c)` of `V_C`, and write

\[
 T_3=\sum_{a\in\{0,1,2\}^C}e_a\otimes h_a,
 \qquad
 T_1=\sum_{a\in\{0,1,2\}^C}e_a\otimes \ell_a,            \tag{3}
\]

with `h_a,ell_a in V_U`.  Put

\[
 \operatorname {Mix}(C)=
 \{0,1,2\}^C\setminus\{0^C,1^C,2^C\},
 \qquad
 M_U=\operatorname {span}\{h_a:a\in\operatorname {Mix}(C)\}. \tag{4}
\]

Since the target has zero coefficient at every mixed word, exactness gives

\[
                         h_a=-\ell_a
                 \quad(a\in\operatorname {Mix}(C)),      \tag{5}
\]

so the same space is obtained by spanning the mixed rows of `T_1`.
Let

\[
 Q_U=V_U/M_U,
 \qquad \bar h_r=[h_{r^C}],\quad
 \bar\ell_r=[\ell_{r^C}],\quad
 \bar\gamma_r=[e_r^{\otimes U}].                         \tag{6}
\]

The constant rows of the target give the three identities

\[
                         \bar\gamma_r=\bar\ell_r+\bar h_r.
                                                                    \tag{7}
\]

**Theorem 2.1 (constant-row quotient formula).**  With
`g_r=e_r^(tensor C)`, one has

\[
 \boxed{
 \mathcal G_C\cap\operatorname {LS}_C(T_3)
   =\left\{\sum_{r=0}^2\varphi(\bar h_r)g_r:
                         \varphi\in Q_U^*\right\}.}       \tag{8}
\]

In particular,

\[
 \dim\bigl(\mathcal G_C\cap\operatorname {LS}_C(T_3)\bigr)
       =\dim\operatorname {span}\{\bar h_0,\bar h_1,\bar h_2\},
                                                                    \tag{9}
\]

and the response criterion fails exactly when at least one `bar h_r` is
nonzero, equivalently when at least one `h_(r^C)` is outside `M_U`.

**Proof.**  A covector `beta in V_U^*` contracts (3) to

\[
             (\operatorname{id}\otimes\beta)T_3
                         =\sum_a\beta(h_a)e_a.             \tag{10}
\]

This is in `G_C` exactly when `beta` annihilates all mixed rows, i.e. when
`beta in M_U^perp=Q_U^*`.  Its three remaining coefficients are then the
evaluations of `bar h_r`, proving (8).  The map in (8) is the dual of

\[
 \mathbb C^3\longrightarrow Q_U,
 \qquad (x_0,x_1,x_2)\longmapsto\sum_rx_r\bar h_r,
\]

so the two maps have the same rank.  This proves (9) and (2). `QED`

The same proof simultaneously records the other two diagonal contractions:

\[
\begin{aligned}
 \mathcal G_C\cap\operatorname {LS}_C(T_1)
   &=\left\{\sum_r\varphi(\bar\ell_r)g_r:\varphi\in Q_U^*\right\},\\
 (\operatorname{id}\otimes\beta)\Delta_{B,3}
   &=\sum_r\varphi(\bar\gamma_r)g_r
       \qquad(\beta\leftrightarrow\varphi\in Q_U^*).     \tag{11}
\end{aligned}
\]

Thus (7) is the coefficientwise identity `D=F_1+F_h` on the exact kernel
of all mixed rows.

**Corollary 2.2 (one maximally supported witness).**  Define

\[
 R_h=\{r:\bar h_r\ne0\},\qquad
 R_1=\{r:\bar\ell_r\ne0\},\qquad
 R_\Delta=\{r:\bar\gamma_r\ne0\}.                       \tag{12}
\]

There is one `varphi in Q_U^*` for which all three contractions in (11)
have supports exactly `R_h,R_1,R_Delta`, respectively (where the last
symbol denotes `R_Delta=R_\Delta`).

**Proof.**  For each nonzero residue vector, its annihilator is a proper
hyperplane in `Q_U^*`.  A finite union of proper linear subspaces cannot
cover a vector space over `C`.  Choose `varphi` outside the union of these
at most nine hyperplanes. `QED`

Consequently every failed triple shore has a single diagonal contamination
witness which is nonzero in every color not ruled out by an explicit
row-span membership.  In particular, either all three one-crossing colors
are simultaneously active, or

\[
                         \ell_{r^C}\in M_U               \tag{13}
\]

for a named color `r`.

The row membership has a useful dual form which retains the matching
sectors, rather than only their quotient classes.

**Corollary 2.3 (pure three-cross selector).**  For a fixed color `r`,

\[
                         \ell_{r^C}\in M_U               \tag{13a}
\]

if and only if there is a covector `Theta in V_C^*` such that

\[
 \Theta(g_s)=\delta_{rs}\quad(0\le s\le2),
 \qquad (\Theta\otimes\operatorname{id})T_1=0.           \tag{13b}
\]

For every such covector, exactness gives the pure three-cross response

\[
                  (\Theta\otimes\operatorname{id})T_3
                              =e_r^{\otimes U}.           \tag{13c}
\]

**Proof.**  If (13a) holds, write
`ell_(r^C)=sum_(a mixed) mu_a ell_a` and define `Theta` to have coefficient
one at `r^C`, coefficient `-mu_a` at each mixed word, and coefficient zero
at the other two constant words.  Equations (3) give (13b).  Conversely,
expanding a covector satisfying (13b) in the word-dual basis expresses
`ell_(r^C)` as a linear combination of the mixed rows, proving (13a).
Finally apply `Theta` to `T_1+T_3=Delta_(B,3)`; (13b) kills `T_1` and the
three prescribed constant values leave exactly the right side of (13c).
`QED`

Thus a row-degenerate triple shore carries an entangled three-site selector
which annihilates the complete one-crossing sector and turns the complete
three-crossing sector into a nonzero pure tensor on the exposed odd shore.
This is stronger data than the degeneracy color label alone.

## 3. The three-shore slice family at every order

Write `C={x,y,z}`.  The high sector is just `T_3` at every order, since
more than three crossing edges cannot leave a three-vertex shore.  The
one-crossing factorization is

\[
 T_1=A_{yz}\otimes R_x+A_{xz}\otimes R_y+A_{xy}\otimes R_z, \tag{14}
\]

with slots put back in the order `x,y,z,U`, where

\[
 R_x=\sum_{u\in U}A_{xu}\otimes H_{U\setminus\{u\}}(A)
       \in V_x\otimes V_U                              \tag{15}
\]

and similarly for `R_y,R_z`.  For `varphi in Q_U^*=M_U^perp`, set

\[
 Z_x(\varphi)=(\operatorname{id}_{V_x}\otimes\varphi)R_x,
 \quad Z_y(\varphi)=(\operatorname{id}_{V_y}\otimes\varphi)R_y,
 \quad Z_z(\varphi)=(\operatorname{id}_{V_z}\otimes\varphi)R_z. \tag{16}
\]

Then

\[
 Z_x(\varphi)\otimes A_{yz}
 +Z_y(\varphi)\otimes A_{xz}
 +Z_z(\varphi)\otimes A_{xy}
       =\sum_{r=0}^2\varphi(\bar\ell_r)e_r^{\otimes C}.   \tag{17}
\]

Let

\[
 S_1=\{(\varphi(\bar\ell_0),\varphi(\bar\ell_1),
                  \varphi(\bar\ell_2)):\varphi\in Q_U^*\}
       \subseteq\mathbb C^3.                              \tag{18}
\]

Its dimension is the rank of the three one-crossing constant-row residues.

**Theorem 3.1 (three-shore normal form).**  Assume

\[
                         \bar\ell_0,\bar\ell_1,
                         \bar\ell_2\ne0.                 \tag{19}
\]

After one simultaneous color permutation and a permutation of `x,y,z`,
there are nonzero linear forms `lambda_0,lambda_1,lambda_2` on `Q_U^*`
such that

\[
 Z_x(\varphi)=\lambda_0(\varphi)e_0,
 \quad Z_y(\varphi)=\lambda_1(\varphi)e_1,
 \quad Z_z(\varphi)=\lambda_2(\varphi)e_2.               \tag{20}
\]

Moreover the three entries

\[
 a_0=(A_{yz})_{00},\qquad
 a_1=(A_{xz})_{11},\qquad
 a_2=(A_{xy})_{22}                                      \tag{21}
\]

are nonzero and, if `b_r(varphi)=varphi(bar ell_r)`, then

\[
                         b_r=a_r\lambda_r.                \tag{22}
\]

Define tensors on `V_x tensor V_y tensor V_z` by

\[
\begin{aligned}
 E_0&=a_0^{-1}e_0^{(x)}\otimes A_{yz}-e_0^{\otimes C},\\
 E_1&=a_1^{-1}e_1^{(y)}\otimes A_{xz}-e_1^{\otimes C},\\
 E_2&=a_2^{-1}e_2^{(z)}\otimes A_{xy}-e_2^{\otimes C}.
                                                               \tag{23}
\end{aligned}
\]

Then

\[
                 \sum_{r=0}^2b_rE_r=0\qquad(b\in S_1),  \tag{24}
\]

and this has the following three exact forms.

1. If `dim S_1=3`, then `E_0=E_1=E_2=0`; equivalently
   \[
      A_{yz}=a_0e_0e_0^T,\qquad
      A_{xz}=a_1e_1e_1^T,\qquad
      A_{xy}=a_2e_2e_2^T.                                \tag{25}
   \]

2. If `dim S_1=2`, write `S_1=ker(theta_0,theta_1,theta_2)`.
   There is a tensor `Z` such that
   \[
                              E_r=\theta_rZ.              \tag{26}
   \]
   The support of `theta` has size at least two, and
   \[
      Z\in\bigcap_{r:\theta_r\ne0}\mathcal S_r,\qquad
      \mathcal S_0=e_0^{(x)}\otimes V_y\otimes V_z,
      \quad\mathcal S_1=V_x\otimes e_1^{(y)}\otimes V_z,
      \quad\mathcal S_2=V_x\otimes V_y\otimes e_2^{(z)}. \tag{27}
   \]
   Hence a two-coordinate `theta`, for example
   `theta_0 theta_1 != 0, theta_2=0`, gives
   \[
   \begin{aligned}
      A_{yz}/a_0&=e_0e_0^T+\theta_0e_1w^T,\\
      A_{xz}/a_1&=e_1e_1^T+\theta_1e_0w^T,\\
      A_{xy}/a_2&=e_2e_2^T                              \tag{28}
   \end{aligned}
   \]
   for one `w in V_z`, with the evident endpoint ordering.  If all three
   `theta_r` are nonzero, then
   \[
                         Z=\mu e_0^{(x)}\otimes
                                e_1^{(y)}\otimes e_2^{(z)}, \tag{29}
   \]
   so each edge has only its pure cell and its corresponding cyclic
   rainbow leakage cell.

3. If `dim S_1=1`, let `b=(b_0,b_1,b_2)` span `S_1`; all `b_r` are
   nonzero.  There are transfer tensors
   \[
       Z_{01}\in\mathcal S_0\cap\mathcal S_1,\quad
       Z_{02}\in\mathcal S_0\cap\mathcal S_2,\quad
       Z_{12}\in\mathcal S_1\cap\mathcal S_2             \tag{30}
   \]
   such that
   \[
   \begin{aligned}
       b_0E_0&= Z_{01}+Z_{02},\\
       b_1E_1&=-Z_{01}+Z_{12},\\
       b_2E_2&=-Z_{02}-Z_{12}.                            \tag{31}
   \end{aligned}
   \]

**Proof.**  By (19), a dense open subset of `Q_U^*` has all three entries
of `b(varphi)` nonzero.  Equation (17) is then a decomposition of a full
three-party diagonal tensor as three slices centered at `x,y,z`.  The
three-slice center lemma forces the three center vectors `Z_x,Z_y,Z_z` to
lie on three distinct coordinate axes.

For each fixed center, every product of two different coordinate entries of
`Z_x(varphi)` vanishes on that dense open set.  It is a polynomial in
`varphi`, so it vanishes identically.  Since the coordinate ring of the
vector space `Q_U^*` is a domain, at most one coordinate linear form of
`Z_x` is nonzero.  Thus its whole image lies in one fixed coordinate line.
The three fixed lines are distinct, which gives (20) after relabeling.

At the word `000`, only the `x`-centered term in (17) can contribute.
Hence `b_0=a_0 lambda_0`.  The form `b_0` is nonzero, so both factors on the
right are nonzero.  The words `111,222` give the other two instances of
(21)--(22).  Substitution in (17) gives (24).

If `S_1=C^3`, (24) immediately gives (25).  If `S_1=ker theta`, the linear
map `b mapsto sum_r b_rE_r` factors through the one-dimensional quotient
`C^3/ker theta`; this is exactly (26).  Each `E_r` lies in `S_r`, so every
nonzero `theta_r` forces `Z in S_r`.  Condition (19) says that `ker theta`
is not a coordinate plane, hence `theta` has at least two nonzero entries.
Intersections of the coordinate slice spaces give (28)--(29).

Finally let `S_1=C b`.  Put `X_r=b_rE_r`.  The relation
`X_0+X_1+X_2=0` and the coordinate supports `X_r in S_r` imply that a
nonzero coefficient can occur only where at least two slice spaces meet.
Resolve each such coefficient between one chosen pair; at the one triple
intersection choose any two transfers.  This gives (30)--(31)
coordinatewise. `QED`

**Corollary 3.2 (invertible-edge staircase).**  Under (19), every internal
edge in the `dim S_1>=2` branches has matrix rank at most two.  Therefore,
if even one of `A_xy,A_xz,A_yz` is invertible, then `dim S_1=1`.

In that case the transfers in (30) have unique vector forms

\[
 Z_{01}=e_0^{(x)}e_1^{(y)}\otimes u,
 \quad Z_{02}=e_0^{(x)}\otimes v\otimes e_2^{(z)},
 \quad Z_{12}=w\otimes e_1^{(y)}e_2^{(z)}                \tag{32a}
\]

for `u in V_z,v in V_y,w in V_x`, and (31) becomes the cyclic staircase

\[
\begin{aligned}
 A_{yz}/a_0&=E_{00}+b_0^{-1}(e_1u^T+ve_2^T),\\
 A_{xz}/a_1&=E_{11}+b_1^{-1}(-e_0u^T+we_2^T),\\
 A_{xy}/a_2&=E_{22}+b_2^{-1}(-e_0v^T-we_1^T).            \tag{32b}
\end{aligned}
\]

In particular,

\[
\begin{aligned}
 \det(A_{yz}/a_0)&=b_0^{-2}u_1v_2,\\
 \det(A_{xz}/a_1)&=-b_1^{-2}u_0w_2,\\
 \det(A_{xy}/a_2)&=b_2^{-2}v_0w_1.                       \tag{32c}
\end{aligned}
\]

**Proof.**  In (25) every edge has rank one.  In (26), stripping the fixed
center factor from `Z` shows that every edge is its pure rank-one cell plus
at most one further rank-one matrix, hence has rank at most two.  Thus an
invertible edge leaves only the third branch.  The three pairwise slice
intersections in (30) are exactly the spaces displayed in (32a).
Substitution in (31) gives (32b), and direct `3 by 3` expansion gives
(32c). `QED`

Each staircase matrix in (32b) is supported on the union of one row, one
column, and one additional diagonal cell.  After a simultaneous permutation
of its row and column colors, this is one of the six upper-triangular
supports.  Equivalently, the directed graph of its nonzero off-diagonal
cells is acyclic.  In particular it has at most six supported cells.  This
gives a useful source-level test.

**Corollary 3.3 (dense invertible pair forces row degeneracy).**  Let `pq`
be an invertible aggregate edge which is not permutation-similar to a
triangular matrix.  For example, it is enough that its off-diagonal support
contains a directed cycle, and hence enough that it has at least seven
nonzero matrix entries.
For every third vertex `x`, with `C={p,q,x}`, at least one color satisfies

\[
                         \ell_{r^C}\in M_{B\setminus C}.  \tag{32d}
\]

Among the `|B|-2` choices of `x`, at least
`ceil((|B|-2)/3)` choices satisfy (32d) for the same color; in particular,
there are two at order eight.

**Proof.**  If all three `bar ell_r` were nonzero, Corollary 3.2 would put
the invertible edge `A_pq` in one of the staircase charts (32b), after
permuting colors, vertices, and possibly transposing its displayed endpoint
order.  Every such chart is supported in a permuted triangular matrix,
contrary to the hypothesis.  Thus (13) holds.  The last assertion is the pigeonhole
principle for `|B|-2` vertices and three colors. `QED`

The same chart interfaces directly with the all-triple-zero theorem.  Let
`K_0,K_1,K_2` denote the three cross-product matrices, so that a vertex
`s` is triple-zero for a pair `p,q` when

\[
                     A_{ps}K_rA_{qs}^T=0\qquad(0\le r\le2). \tag{32e}
\]

**Corollary 3.4 (a staircase site is not triple-zero).**  Suppose `A_pq`
is invertible and use the triple `C={p,q,s}`.  If none of the three
one-crossing constant rows belongs to `M_{B\setminus C}`, then `s` is not a
triple-zero site for `p,q`.  Equivalently, if every outside site is
triple-zero for an invertible pair `p,q`, then every triple `C={p,q,s}`
has a row degeneracy (32d).

**Proof.**  With no row degeneracy, (19) holds.  Invertibility of `A_pq`
and Corollary 3.2 put the triangle in (32b).  Identify the displayed
vertices `(x,y,z)` there with `(p,q,s)`.  After harmless nonzero rescaling,
the row of `A_{qs}=A_{yz}` indexed by color zero has the form `(1,0,*)`,
while the row of `A_{ps}=A_{xz}` indexed by color one has the form
`(0,1,*)`.  Both
are nonzero and they are not proportional.  Thus the two matrices do not
have a common one-dimensional row space.  The triple-zero classification
then says that not all three matrices in (32e) vanish. `QED`

## 4. The three-cross vector-permanent response

The rows `h_a` have an exact cubic description.  Work in the square-free
commutative tensor algebra

\[
              \mathscr S_U=\bigotimes_{u\in U}(\mathbb C\oplus V_u),
       \qquad q=\sum_{u<v\in U}A_{uv}.                    \tag{33}
\]

For `c in C` and `alpha in V_c^*`, define the degree-one star row

\[
 p_c(\alpha)=\sum_{u\in U}
        (\alpha\otimes\operatorname{id}_{V_u})A_{cu}
       \in(\mathscr S_U)_1.                               \tag{34}
\]

**Lemma 4.1 (polarized cubic formula).**  For `C={x,y,z}`,

\[
 (\alpha\otimes\beta\otimes\gamma
             \otimes\operatorname{id}_{V_U})T_3
       =\bigl[p_x(\alpha)p_y(\beta)p_z(\gamma)e^q\bigr]_U. \tag{35}
\]

**Proof.**  The three degree-one factors choose distinct partners in `U`
for `x,y,z`; a repeated endpoint vanishes in the square-free algebra.  The
remaining top-support component of `e^q` is the matching tensor on the
unused even subset of `U`.  This is exactly the matching decomposition of
the three-crossing sector. `QED`

Thus a cap `K in V_U^*` produces the trilinear response

\[
 \tau_K(\alpha,\beta,\gamma)
   =K\!\left(\bigl[p_x(\alpha)p_y(\beta)p_z(\gamma)e^q\bigr]_U\right).
                                                                    \tag{36}
\]

It is diagonal precisely when its `24` mixed basis values vanish.  Exactness
and the one-crossing factorization sharpen this: those `24` equations have
row rank at most nine.  Indeed, let

\[
 \rho_{x,a}=(e_a^*\otimes\operatorname{id})R_x,
 \quad \rho_{y,b}=(e_b^*\otimes\operatorname{id})R_y,
 \quad \rho_{z,c}=(e_c^*\otimes\operatorname{id})R_z.    \tag{37}
\]

Taking the `(a,b,c)` coefficient of (14) gives

\[
 \ell_{abc}=(A_{yz})_{bc}\rho_{x,a}
             +(A_{xz})_{ac}\rho_{y,b}
             +(A_{xy})_{ab}\rho_{z,c}.                  \tag{38}
\]

Consequently

\[
                    M_U\subseteq
       \operatorname{span}\{\rho_{x,a},\rho_{y,b},\rho_{z,c}:
                              0\le a,b,c\le2\},
       \qquad \dim M_U\le9.                              \tag{39}
\]

This rank bound turns an arbitrary entangled contamination cap into a
bounded sum of product caps.

**Proposition 4.2 (ten-word contamination certificate).**  If the
intersection in (8) is nonzero, there are at most ten colorings
`sigma_j:U -> {0,1,2}` and scalars `c_j` such that

\[
 K=\sum_{j=1}^{t}c_j e_{\sigma_j}^*,\qquad t\le10,        \tag{40}
\]

annihilates every mixed row and contracts `T_3` to a nonzero diagonal
tensor.  If all three residues `bar h_0,bar h_1,bar h_2` are nonzero, `K`
may be chosen so that all three diagonal coefficients are nonzero with
`t<=12`.

**Proof.**  Put `d=dim M_U<=9` and choose a basis `m_1,...,m_d` of `M_U`.
If, say, `bar h_r!=0`, the affine system

\[
                  K(m_i)=0\ (1\le i\le d),\qquad K(h_{r^C})=1 \tag{41}
\]

is consistent.  The coordinate-word covectors form a basis of `V_U^*`.
Apply the linear map which records the `d+1` values in (41) to that basis;
some at most `d+1` of its image columns span the desired value vector.
Their preimages give (40).  The contraction is diagonal by Theorem 2.1 and
nonzero by (41).

If all three residues are nonzero, first choose `K in M_U^perp` outside
their three annihilator hyperplanes.  Record its three nonzero diagonal
values as well as the `d` zero mixed-span values.  The same column-basis
argument reproduces these values using at most `d+3<=12` coordinate-word
covectors. `QED`

For completeness, each word cap in (40) is a literal vector-permanent
response.  Given `sigma:U->{0,1,2}`, put

\[
 X_u=(\operatorname{id}_{V_x}\otimes e_{\sigma(u)}^*)A_{xu},
 \quad Y_u=(\operatorname{id}_{V_y}\otimes e_{\sigma(u)}^*)A_{yu},
 \quad Z_u=(\operatorname{id}_{V_z}\otimes e_{\sigma(u)}^*)A_{zu},
                                                                    \tag{42}
\]

and `q_uv=A_uv(sigma(u),sigma(v))`.  Directly from (35),

\[
 \mathcal R_C(\sigma)=
 \sum_{\substack{u,v,w\in U\\u,v,w\ \mathrm{distinct}}}
   \operatorname {Haf}\bigl(q|_{U\setminus\{u,v,w\}}\bigr)
        X_u\otimes Y_v\otimes Z_w.                       \tag{43}
\]

Equation (40) says that a sum of at most ten tensors (43) is diagonal and
nonzero; in the full three-color case a sum of at most twelve is a
nondegenerate diagonal tensor.

One must not apply the one-slice covering lemma directly to (43).  Grouping
by a shore mode produces many singleton factors at the *same* mode, not one
slice centered at each of three different modes; interpolation cancellation
among those factors is possible.  Thus (40)--(43) are a bounded
vector-permanent certificate, but do not alone force a coordinate column in
an individual cross edge.  That missing monomialization is precisely where
anchor compatibility still has to enter.

## 5. Consequences for simultaneous failure

Choose a realization of minimum even order above six.  If some triple
`C` had zero intersection in (8), the odd-shore response criterion would
replace `C` by one aggregate vertex and give an exact realization on
`|B|-2` vertices, contrary to minimality.  Hence every triple requires at
least one `bar h_r != 0`.  Theorem 3.1 gives the exact
alternative

\[
 \boxed{\quad
 \text{some }\ell_{r^C}\in M_U,
 \quad\text{or the internal triangle }C
       \text{ has one of (25), (26), (31).}\quad}         \tag{44}
\]

The full-rank branch (25) cannot occur for every triple when `|B|>=6`.
Indeed, an
internal edge appearing in (25) is a nonzero pure coordinate edge and
therefore has a unique color.  If every triple had form (25), these colors
would give a three-edge-coloring in which every triangle is rainbow.  At a
fixed vertex, any two incident edges lie in a triangle and must have
different colors, so its degree would be at most three.  This is impossible
on any complete graph with at least five vertices.

Thus simultaneous failure on every triple necessarily reaches at least one
of the following finite boundary strata:

* a constant one-crossing row belongs to the mixed-row span `M_U`;
* the surviving one-crossing diagonal space has dimension at most two,
  with the shared-leakage forms (26)--(31).

There is no contradiction with the forced-anchor theorem at the level of
the intersections alone.  The explicit eight-vertex source in
`notes/total-sector-six-reduction.md` has active coordinate anchors and

\[
             \mathcal G_C\cap\operatorname {LS}_C(T_3)\ne0
\]

for all `56` triples `C` (the intersection has dimension two or three).
That source is rejected by a mixed coefficient, so it does not satisfy
(5).  Conversely, the occurrence relaxation in
`notes/six-bag-incidence-reduction.md` satisfies the exact target and has
maximal diagonal contamination, but deliberately omits recombination of a
shared aggregate edge across matchings.  These models show that a further
argument must use both ingredients simultaneously: the mixed-row identity
(5) and shared-edge incidence.  Anchor counting by itself cannot eliminate
the simultaneous intersections.

What remains to connect this result to the existing all-triple-zero theorem
is a source-global propagation lemma: one must show that the row-span
degeneracy or shared leakage on overlapping triples either produces a clean
pair cap or makes all three cross matrices at every outside site vanish for
some invertible pair.  Neither conclusion follows from slice rank alone,
and neither is asserted here.

## 6. Exact audit

Run

```text
.venv/bin/python computations/verify_five_set_contamination_normal_form.py
```

The checker uses exact rational arithmetic to verify the quotient-rank
identity, all rank-three/rank-two/rank-one coordinate normal forms, the
staircase determinant and support formulas, and a non-triple-zero staircase
instance.  Independently, it enumerates all `105` perfect matchings of a
deterministic arbitrary-matrix eight-vertex source, verifies that the `24`
mixed one-cross rows have rank at most nine, and checks the word-cap
vector-permanent formula (43) coefficient by coefficient.
