# Higher splits: the undecic singleton--double coupling at \(p=19\)

## 1. Result

Continue from the exact \(p=19\) singleton and dense-double common-lift
theorems.  Four of the nine residual families lie simultaneously on the
degree-nine singleton equality surface and the degree-eleven
dense-double equality surface.

**Theorem 1.1 (undecic singleton--double coupling).**  The following
four families are impossible:

\[
 \boxed{
  2^{11}1^{h-1},\qquad
  3\,2^9 1^h,\qquad
  3^2 2^7 1^{h+1},\qquad
  4\,2^8 1^{h+1}.}                                          \tag{1}
\]

In the \((e;a,b,u)\) notation these are

\[
 (0;0,11,-1),\quad(0;1,9,0),\quad(0;2,7,1),\quad
 (1;0,8,1).                                                   \tag{2}
\]

Together with the preceding five \(p=19\) closures, this raises the exact
ledger from \(85/94\) to

\[
                              \boxed{89/94}.                  \tag{3}
\]

Five families remain.

## 2. One grid of relation three-spaces

Let \({\mathscr D}\) be the set of exact-double values and let
\({\mathscr Q}\) be the moving-singleton pool.  Their sizes in the four
cases are

\[
\begin{array}{c|c|c|c}
(e;a,b,u)&|{\mathscr D}|&|{\mathscr Q}|&
 \text{fixed classes outside the singleton pool}\\ \hline
(0;0,11,-1)&11&2&9\\
(0;1,9,0)&9&3&8\\
(0;2,7,1)&7&4&7\\
(1;0,8,1)&8&4&7.
\end{array}                                                   \tag{4}
\]

Fix the common selected singleton layers that do not move.  For a double
pair \(\{i,j\}\subset{\mathscr D}\) and \(q\in{\mathscr Q}\), let

\[
             {\cal S}_{ij;q}\subseteq\mathbb C[z]_{\leq6},
             \qquad \dim{\cal S}_{ij;q}=3                    \tag{5}
\]

be the exact relation space of the corresponding formal selection.  The
selected-row kernel is five-dimensional in every case, by the strict
\(q=6\) gap and the already-audited exclusion of the four-dimensional
selected kernel.

Put

\[
 f_q(z)=(z-q)^2(z+q),\qquad
 g_j(z)=(z-j)^3(z+j)^2.                                      \tag{6}
\]

The singleton transport and the double transport apply to the same grid
(5):

\[
\begin{aligned}
 f_q{\cal S}_{ij;q}&\subseteq
       {\cal K}^{\rm s}_{ij}\subseteq\mathbb C[z]_{\leq9},
       &\dim{\cal K}^{\rm s}_{ij}&\leq4,\\
 g_j{\cal S}_{ij;q}&\subseteq
       {\cal K}^{\rm d}_{i;q}\subseteq\mathbb C[z]_{\leq11},
       &\dim{\cal K}^{\rm d}_{i;q}&\leq5.                  \tag{7}
\end{aligned}
\]

The first common space is independent of \(q\); the second is independent
of the moving partner \(j\).  All distinct value classes are structurally
distinct and nonopposite.  In particular the cubics and quintics used
below are pairwise coprime.  Exact-double values are nonzero; a singleton
value may be zero, but at most one is.

## 3. Exact singleton triple products

Suppose \(|{\mathscr Q}|\geq3\).  The singleton common space in (7) has
dimension four.  Indeed, if it had dimension three, all transported
three-spaces would coincide.  For three pool values that common
three-space would be divisible by three coprime cubics, while the
degree-nine multiple space is only a line.  This is impossible.  The
case of four pool values is stronger still.

Thus the transported spaces are hyperplanes in a four-space.  Any three
of them meet nontrivially, and their ambient cubic-multiple spaces meet
in exactly the degree-nine product line.  Hence, for distinct
\(q,r,s\in{\mathscr Q}\),

\[
                         f_qf_rf_s\in{\cal K}^{\rm s}_{ij}.   \tag{8}
\]

Dividing (8) by \(f_q\) gives

\[
                         f_rf_s\in{\cal S}_{ij;q}.            \tag{9}
\]

This conclusion holds for every selected double pair \(\{i,j\}\).

## 4. The two four-pool profiles

Let \({\mathscr Q}=\{q,r,s,t\}\).  For fixed \(q\), equation (9) gives
three independent members of the three-space (5).  Therefore

\[
 {\cal S}_{ij;q}=
       \langle f_rf_s,\ f_rf_t,\ f_sf_t\rangle=: {\cal V}_q. \tag{10}
\]

Crucially, the right side is independent of the selected double pair.
The independence is structural: in a linear relation among the three
pair products, evaluation at a root belonging to just one of the
pairwise-coprime cubics successively kills all three coefficients.

Let \(W_q\) be the three-polynomial Wronskian of \({\cal V}_q\).  It is
nonzero and has degree at most

\[
                         3(6+1-3)=12.                         \tag{11}
\]

At each of \(r,s,t\), two of the three displayed sections contain the
corresponding cubic.  If that value is nonzero, its order-two root forces
local vanishing sequence at least \((0,2,3)\), of Wronskian weight two.
If it is zero, \(f_0=z^3\) forces at least \((0,3,4)\), of weight four.
Thus the three singleton values contribute at least six units in total.

Now fix any double value \(v\).  Choose a selected double pair not
containing \(v\), which is possible because \(b\geq7\).  Then \(v\) is
an exact order-two complementary row of the same space \({\cal V}_q\).
After multiplication by its local regular unit, the coefficient of order
two vanishes on the whole three-space, so its Wronskian vanishes at
\(v\).  Multiplication by a unit changes the Wronskian only by the
nonzero cube of that unit.  Varying the selected pair therefore puts all
\(b\) distinct double values on this one fixed Wronskian.

The forced Wronskian weight is at least

\[
                              6+b\geq13,                      \tag{12}
\]

contradicting (11).  This closes both four-pool profiles, including every
possible zero-singleton branch.

## 5. The three-pool profile

Let \({\mathscr Q}=\{q,r,s\}\).  For fixed \(q\), put

\[
                              F_q=f_rf_s.                     \tag{13}
\]

Equation (9) says that \(F_q\in{\cal S}_{ij;q}\) for every double pair.
Fix \(i\) and \(q\).  The dense common space in (7) consequently contains

\[
                              F_qg_j
        \qquad(j\in{\mathscr D}\setminus\{i\}).              \tag{14}
\]

In ascending powers of \(z\), the coefficient vector of \(g_x\) is

\[
             ( -x^5, x^4, 2x^3, -2x^2, -x, 1),          \tag{15}
\]

which is a nonsingular diagonal rescaling and reversal of
\((1,x,\ldots,x^5)\).  For six distinct values \(x_1,\ldots,x_6\), its
determinant is, up to sign,

\[
                    4\prod_{a<b}(x_b-x_a)\ne0.               \tag{16}
\]

Thus any six of the quintics \(g_j\) are linearly independent.
Multiplication by the nonzero polynomial \(F_q\) preserves independence.
Here \(b-1=8\), so (14) puts six independent polynomials in the
at-most-five-space \({\cal K}^{\rm d}_{i;q}\), a contradiction.  This
closes \(3\,2^9 1^h\).  This step needs only distinct double values; the
stronger structural nonopposition remains available throughout.

## 6. The two-pool profile

It remains to close \(2^{11}1^{h-1}\).  Write
\({\mathscr Q}=\{q,r\}\).

### 6.1 Every dense pair intersection is a line

For a fixed double pair \(\{i,j\}\), the two singleton transports in
(7) meet in dimension at least two.  Their ambient intersection is

\[
 f_qf_r\mathbb C[z]_{\leq3}.
\]

After division by \(f_q\), there is consequently a plane

\[
 f_r{\cal L}_{ij}\subseteq{\cal S}_{ij;q},
              \qquad {\cal L}_{ij}\subseteq
                    \mathbb C[z]_{\leq3},\quad
              \dim{\cal L}_{ij}=2.                           \tag{17}
\]

Fix \(i,q\), abbreviate \({\cal K}^{\rm d}_{i;q}\) to \({\cal K}\),
and put \({\cal T}_j=g_j{\cal S}_{ij;q}\).  First,
\(\dim{\cal K}\ne3\): otherwise all \({\cal T}_j\) would coincide, and
three moving partners would force a nonzero degree-eleven polynomial to
be divisible by three coprime quintics.  If \(\dim{\cal K}=4\), every
pair intersection is the full ambient pencil

\[
                  {\cal T}_j\cap{\cal T}_k
                      =g_jg_k\mathbb C[z]_{\leq1}.            \tag{18}
\]

For fixed \(j\), division by \(g_j\) would put both
\(g_k\mathbb C[z]_{\leq1}\) and
\(g_\ell\mathbb C[z]_{\leq1}\) in the three-space
\({\cal S}_{ij;q}\), for two distinct partners \(k,\ell\).  These two
planes have zero intersection in degree six, because a common member
would be divisible by the degree-ten product \(g_kg_\ell\).  This is
also impossible.  Hence

\[
                             \dim{\cal K}=5.                  \tag{19}
\]

Two transported three-spaces in this five-space meet in at least a line.
Their ambient intersection is the pencil in (18).  It cannot be the
full pencil: after division by \(g_j\), the three-space
\({\cal S}_{ij;q}\) would contain both the plane in (17) and the plane
\(g_k\mathbb C[z]_{\leq1}\).  Those planes must meet inside a
three-space, but their ambient intersection is zero because
\(\deg(f_rg_k)=8>6\).  Therefore every pair intersection is exactly

\[
 {\cal T}_j\cap{\cal T}_k
       =\langle g_jg_k\ell_{jk}\rangle,
       \qquad 0\ne\ell_{jk}\in\mathbb C[z]_{\leq1}.        \tag{20}
\]

The projective linear factor \(\ell_{jk}=\ell_{kj}\) is intrinsic to
the unordered pair.

### 6.2 Singleton first-jet compatibility

Put

\[
                  a_x={g_x'(r)\over g_x(r)}
                      ={5r+x\over r^2-x^2}.                  \tag{21}
\]

All denominators are nonzero by structural nonopposition, even when
\(r=0\).  Divide (20) by \(g_j\).  The polynomial
\(g_k\ell_{jk}\) belongs to \({\cal S}_{ij;q}\), so it obeys the exact
first-order row at the complementary singleton \(r\).  It cannot vanish
at \(r\): if it did, that row would force its derivative to vanish as
well, whereas \(g_k(r)\ne0\) and a nonzero linear polynomial cannot have
a double root.  Division by its value is therefore legitimate.

For fixed \(j\), the singleton row has one local unit independent of
\(k\).  Hence there is a scalar \(\lambda_j\) such that

\[
             a_k+{\ell_{jk}'(r)\over\ell_{jk}(r)}=\lambda_j
                         \qquad(k\ne i,j).                    \tag{22}
\]

Using the same intrinsic factor from the \(k\)-side gives

\[
             \lambda_j+a_j=\lambda_k+a_k.                    \tag{23}
\]

The complete partner graph is connected, so these quantities have one
common value \(\Lambda\).  Normalize \(\ell_{jk}(r)=1\).  Equations
(22)--(23) determine every pair factor exactly:

\[
 \boxed{
  \ell_{jk}(z)=1+d_{jk}(z-r),\qquad
  d_{jk}=\Lambda-a_j-a_k.}                                   \tag{24}
\]

No division by a possibly zero structural value was used in deriving
(24).

### 6.3 The bidegree-six clique obstruction

Fix a tested double value \(v\ne i\), and put

\[
                \Omega={\mathscr D}\setminus\{i,v\},
                \qquad |\Omega|=9.                           \tag{25}
\]

The exact second-order row of \({\cal K}\) at \(v\) has the form

\[
                            (UT)''(v)=0,\qquad U(v)\ne0,      \tag{26}
\]

with one unit independent of the pair \(j,k\in\Omega\).  Define

\[
\begin{aligned}
 A_x&={g_x'(v)\over g_x(v)}={5v+x\over v^2-x^2},\\
 R_x&={g_x''(v)\over g_x(v)}
       ={4(5v^2+2vx-x^2)\over(v^2-x^2)^2},\\
 u&={U'(v)\over U(v)},\qquad c={U''(v)\over U(v)},\\
 d_{xy}&=\Lambda-a_x-a_y,\\
 P_{xy}&=u+A_x+A_y,\\
 Q_{xy}&=c+R_x+R_y+2u(A_x+A_y)+2A_xA_y.                     \tag{27}
\end{aligned}
\]

Apply (26) to the pair-intersection generator
\(g_xg_y[1+d_{xy}(z-r)]\).  Exact product-rule expansion gives

\[
 E(x,y):=Q_{xy}\bigl(1+(v-r)d_{xy}\bigr)
                     +2P_{xy}d_{xy}=0                       \tag{28}
\]

for every distinct \(x,y\in\Omega\).

Clear the structural denominator

\[
 D(x,y)=(r^2-x^2)(r^2-y^2)
              (v^2-x^2)^2(v^2-y^2)^2.                       \tag{29}
\]

Then \(N(x,y)=D(x,y)E(x,y)\) is a polynomial of degree at most six in
each variable.  Every factor in (29) is nonzero on the off-diagonal
\(\Omega\)-grid by structural nonopposition.  For fixed
\(x\in\Omega\), the polynomial has the other eight values
of \(\Omega\) as distinct roots in \(y\), so it vanishes identically in
\(y\).  Each of its coefficient polynomials in \(x\), also of degree at
most six, consequently vanishes at all nine elements of \(\Omega\).
Therefore

\[
                              N(x,y)\equiv0.                  \tag{30}
\]

This identity is structurally impossible, not merely generically so.
The exact double-pole coefficient at \(y=v\) is

\[
 \lim_{y\to v}(v-y)^2E(x,y)
       =6\left[1+(v-r)(\Lambda-a_x-a_v)\right].              \tag{31}
\]

Equation (30) would make (31) identically zero.  Clearing the remaining
denominator \(r^2-x^2\), and writing
\(K=1+(v-r)(\Lambda-a_v)\), gives

\[
             K(r^2-x^2)-(v-r)(5r+x)\equiv0.                 \tag{32}
\]

The coefficient of \(x\) is \(-(v-r)\ne0\), because a tested double and
a singleton are distinct value classes.  This contradiction closes the
two-pool profile and completes the proof.

## 7. Exact audit

[verify_live_three_zero_higher_split_p19_undecic_singleton_double_coupling_closure.py](../computations/verify_live_three_zero_higher_split_p19_undecic_singleton_double_coupling_closure.py)
reconstructs the four-profile census and the \(89/94\) ledger, checks both
common-kernel degree bounds and every dimension branch, verifies the
singleton triple products, the universal four-pool Wronskian count, the
quintic Vandermonde determinant, the pair-line and first-jet
compatibilities, and the exact bidegree-six numerator and double-pole
obstruction.
