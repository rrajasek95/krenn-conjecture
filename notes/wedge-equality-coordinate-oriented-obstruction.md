# A conditional obstruction on the wedge equality stratum

## 1. Scope and outcome

This note isolates the last common-power chart of the rank-budget equality
frontier in
[`full-rank-site-response-invisibility-countermodel.md`](full-rank-site-response-invisibility-countermodel.md).
It is deliberately **conditional**.  It does not close the full
\((1,4,1)\) wedge geometry, because the three omission-pair blocks of the
quadratic are still assumed zero.

**Current status.**  The later primary
[unconditional hole-block resolution](wedge-equality-hole-block-resolution.md)
removes those three assumptions and claims closure of the wedge equality
geometry; its exact checker passes.  At this audit it still needs a
clean-room line proof before conservative route-registry promotion.  The
present note is retained as the shorter conditional matching/Segre core and
as the typed-grid derivation of its five cofactor zeros.

Let the six sites be

\[
                         U=\{a,b,c,d,e,f\},
\]

and let the three distinct omission pairs be

\[
              B_0=ab,\qquad B_1=bc,\qquad B_2=de.       \tag{1}
\]

Thus the coordinate endpoint spaces on the equality stratum have ranks

\[
\begin{array}{c|cccccc}
u&a&b&c&d&e&f\\ \hline
W_u&\langle e_1,e_2\rangle&\langle e_2\rangle&
\langle e_0,e_2\rangle&\langle e_0,e_1\rangle&
\langle e_0,e_1\rangle&\langle e_0,e_1,e_2\rangle .
\end{array}                                               \tag{2}
\]

Write \(q_{uv}\in V_u\otimes V_v\) for the endpoint-ordered block of an
arbitrary quadratic \(q\) in the site-square-zero algebra, put

\[
                         F=q^{[2]},
\]

and write \(F_{uv}\) for the four-site component missing \(u,v\).

The chart treated here has one extra common-power feature.

1.  The three omission-pair blocks themselves vanish:

    \[
                         q_{ab}=q_{bc}=q_{de}=0.          \tag{3}
    \]

The response equations themselves force the following five cofactor
zeros, as proved in Section 5.  They remain **literal hypotheses** of the
standalone algebraic theorem so its input is completely explicit:

    \[
       F_{ac}=F_{ae}=F_{be}=F_{bd}=F_{cd}=0.             \tag{4}
    \]

The diagonal response hypotheses are

\[
\begin{aligned}
 F_{ab}&=\lambda _0 e_0^{(c)}e_0^{(d)}e_0^{(e)}e_0^{(f)},\\
 F_{bc}&=\lambda _1 e_1^{(a)}e_1^{(d)}e_1^{(e)}e_1^{(f)},\\
 F_{de}&=\lambda _2 e_2^{(a)}e_2^{(b)}e_2^{(c)}e_2^{(f)},
\end{aligned}
\qquad \lambda _0\lambda _1\lambda _2\ne0.             \tag{5}
\]

**Theorem 1.1 (conditional wedge obstruction).**  Over a field of
characteristic different from two, equations (3)--(5) are incompatible
with

\[
                             q^{[3]}=0.                  \tag{6}
\]

All edge blocks in this theorem are arbitrary tensors.  No block is
assumed decomposable, scalar, nonzero, or generic.  Complex cancellation
is retained inside every four-site cofactor.

The simple coordinate rows which make (4)--(5) transparent are

\[
\begin{array}{lll}
 p_0=e_0^{(a)},&p_1=e_1^{(b)},&p_2=e_2^{(d)},\\
 s_0=e_0^{(b)},&s_1=e_1^{(c)},&s_2=e_2^{(e)}.
\end{array}                                               \tag{7}
\]

Indeed, the five distinct-site off-diagonal products select precisely the
five cofactors in (4); the remaining off-diagonal product \(p_1s_0\)
collides at \(b\) and is automatically zero.  The three diagonal products
select (5).  Condition (3), however, does **not** follow merely from these
coordinate rows.  It is the sole additional hole-edge-free chart
hypothesis left after the typed quotient-grid argument in Section 5.  This
is exactly the limitation which keeps Theorem 1.1 from being a closure of
the whole wedge stratum.

## 2. The matching ledger

Products are reordered into site order, and \(q^{[j]}\) denotes the
unordered \(j\)-edge matching sum.  The three nonzero target cofactors in
(5), after using (3), are

\[
\begin{aligned}
 q_{cd}q_{ef}+q_{ce}q_{df}
    &=\lambda _0 e_0^{(c)}e_0^{(d)}e_0^{(e)}e_0^{(f)},   \tag{8}\\
 q_{ad}q_{ef}+q_{ae}q_{df}
    &=\lambda _1 e_1^{(a)}e_1^{(d)}e_1^{(e)}e_1^{(f)},   \tag{9}\\
 q_{ac}q_{bf}
    &=\lambda _2 e_2^{(a)}e_2^{(b)}e_2^{(c)}e_2^{(f)}.  \tag{10}
\end{aligned}
\]

For reference, the five no-rerouting equations (4) expand to

\[
\begin{aligned}
q_{bd}q_{ef}+q_{be}q_{df}&=0,                           \tag{11}\\
q_{bd}q_{cf}+q_{bf}q_{cd}&=0,                           \tag{12}\\
q_{ac}q_{df}+q_{ad}q_{cf}+q_{af}q_{cd}&=0,              \tag{13}\\
q_{ac}q_{ef}+q_{ae}q_{cf}+q_{af}q_{ce}&=0,              \tag{14}\\
q_{ae}q_{bf}+q_{af}q_{be}&=0.                           \tag{15}
\end{aligned}
\]

They occur in the order \(F_{ac},F_{ae},F_{be},F_{bd},F_{cd}\).
The proof below only needs the middle two equations (13)--(14), but all
five hypotheses are displayed literally so that the exact response chart
is unambiguous.

There is a short Bianchi-type matching identity.  Under (3), direct
enumeration of the eight surviving perfect matchings gives

\[
 q^{[3]}=q_{be}F_{be}+q_{bd}F_{bd}
          +q_{bf}\bigl(q_{ad}q_{ce}+q_{ae}q_{cd}\bigr). \tag{16}
\]

Each term on the right has all six sites, so (16) is an equality in
\(V_a\otimes\cdots\otimes V_f\), not a scalar support heuristic.  Equations
(4), (6), and the injectivity of tensoring by the nonzero block \(q_{bf}\)
from (10) yield the crossing identity

\[
                         q_{ad}q_{ce}+q_{ae}q_{cd}=0.    \tag{17}
\]

This is the point where the cubic common-power equation supplies
information absent from the quotient response table.

## 3. Crossing factorization

We first record why none of the four blocks in (17) vanishes.  If
\(q_{ad}=0\), equation (9) says that \(q_{ae}q_{df}\) is the nonzero pure
color-one tensor.  Hence both blocks are nonzero and, in particular, the
two local factor lines of \(q_{df}\) are the color-one lines.  Equation
(17) then gives \(q_{cd}=0\).  Equation (8) says that
\(q_{ce}q_{df}\) is the nonzero pure color-zero tensor, forcing those same
two local factor lines of \(q_{df}\) to be the distinct color-zero lines,
a contradiction.  The case \(q_{ae}=0\) is symmetric, using
\(q_{ad}q_{ef}\) and \(q_{cd}q_{ef}\).

Thus \(q_{ad},q_{ae}\ne0\).  If one of \(q_{cd},q_{ce}\) vanished, (17)
would make the other vanish as well, after which (8) would have zero left
side.  Therefore all four blocks in (17) are nonzero.

We use the elementary rectangle factorization lemma: if nonzero tensors

\[
 X\in A\otimes D,\quad Y\in C\otimes E,\quad
 X'\in A\otimes E,\quad Y'\in C\otimes D
\]

satisfy \(XY+X'Y'=0\), then all four have matrix rank one and use common
factor lines at each named space.  To prove it, flatten the equality first
across \((A\otimes D)\mid(C\otimes E)\).  The first product has flattening
rank one, while the reshuffled second product has rank
\(\operatorname{rank}(X')\operatorname{rank}(Y')\); hence \(X',Y'\)
both have rank one.  Flattening across
\((A\otimes E)\mid(C\otimes D)\) similarly makes \(X,Y\) rank one.
Uniqueness of the four factors of a nonzero decomposable tensor gives the
common local lines.

Applying this lemma to (17), there are nonzero vectors

\[
 A_a\in V_a,\quad C_c\in V_c,\quad D_d\in V_d,
 \quad E_e\in V_e
\]

and nonzero scalars \(x_d,x_e,y_d,y_e\) such that

\[
\begin{array}{ll}
 q_{ad}=x_dA_aD_d,&q_{ae}=x_eA_aE_e,\\
 q_{cd}=y_dC_cD_d,&q_{ce}=y_eC_cE_e,
\end{array}                                               \tag{18}
\]

with

\[
                         x_dy_e+x_ey_d=0.                \tag{19}
\]

## 4. The Segre-secant contradiction

Substitute (18) into (8)--(9).  Uniqueness of the exposed factors at
sites \(c\) and \(a\) gives

\[
 \mathbb F C_c=\mathbb F e_0^{(c)},\qquad
 \mathbb F A_a=\mathbb F e_1^{(a)}.                    \tag{20}
\]

After absorbing nonzero scalars, put

\[
 T_D=D_dq_{ef},\qquad T_E=E_eq_{df},                    \tag{21}
\]

as tensors on \(d,e,f\).  Equations (8)--(9) become

\[
\begin{pmatrix}y_d&y_e\\x_d&x_e\end{pmatrix}
\begin{pmatrix}T_D\\T_E\end{pmatrix}
=
\begin{pmatrix}\mu_0U_0\\\mu_1U_1\end{pmatrix},
\qquad
 U_i=e_i^{(d)}e_i^{(e)}e_i^{(f)},\quad \mu_0\mu_1\ne0. \tag{22}
\]

The coefficient matrix is invertible.  Indeed, if its rows were
proportional, (19) would become twice a product of nonzero scalars.  More
explicitly, (19) gives

\[
 y_dx_e-y_ex_d=2y_dx_e\ne0.                             \tag{23}
\]

Solving (22) shows

\[
\begin{aligned}
 T_D&=(x_e\mu_0U_0-y_e\mu_1U_1)/(y_dx_e-y_ex_d),\\
 T_E&=(-x_d\mu_0U_0+y_d\mu_1U_1)/(y_dx_e-y_ex_d).       \tag{24}
\end{aligned}
\]

Every coefficient displayed in (24) is nonzero.  But \(T_D=D_dq_{ef}\)
has flattening rank at most one across

\[
                         V_d\mid(V_e\otimes V_f).        \tag{25}
\]

The first line of (24) has rank two across (25): its two left factors
\(e_0^{(d)},e_1^{(d)}\) are independent, and its two right factors
\(e_0^{(e)}e_0^{(f)},e_1^{(e)}e_1^{(f)}\) are independent, with both
coefficients nonzero.  This is the elementary Segre-secant fact that the
line through the two coordinate pure tensors \(U_0,U_1\) meets the
rank-one flattening locus only at its endpoints.  The contradiction proves
Theorem 1.1.

## 5. Typed quotient grids close the path and triangle

The physical-pair quotient graph forgets an important part of the double
quotient: a rank-one endpoint space has a two-dimensional quotient, with
one typed direction for each missing color.  Retaining those typed
directions closes the path and triangle equality types and forces all five
cofactor zeros (4) on the wedge.

For a missing-color mode \(\xi=(u,i)\), package the response coefficients as

\[
 P_\xi=(p_{0,u,i},p_{1,u,i},p_{2,u,i})^{\mathsf T},\qquad
 S_\xi=(s_{0,u,i},s_{1,u,i},s_{2,u,i})^{\mathsf T},      \tag{26}
\]

and write \(x_\xi=(P_\xi,S_\xi)\).  Define

\[
 \Phi(x_\xi,x_\eta)=P_\xi S_\eta^{\mathsf T}
                       +P_\eta S_\xi^{\mathsf T}.       \tag{27}
\]

On an omission pair \(B_i=uv\), the purified double-quotient identity gives
the complete typed grid

\[
 \Phi(x_{u,\alpha},x_{v,\beta})
   =\theta_i\delta_{\alpha i}\delta_{\beta i}E_{ii}
 \quad(\alpha\text{ missing at }u,\ 
       \beta\text{ missing at }v),                      \tag{28}
\]

after a harmless common rescaling.  Thus (28) contains one nonzero target
corner and a literal zero at every other typed corner.

We use the crossed-target lemma from
[n8-clean-nearperfect-paircap-obstruction.md](../proofs/n8-clean-nearperfect-paircap-obstruction.md).
If nonzero points \(A,B,C,D\) satisfy

\[
 \Phi(A,B)\in\mathbb F^*E_{ii},\qquad
 \Phi(C,D)\in\mathbb F^*E_{jj},\qquad
 \Phi(A,D)=\Phi(C,B)=0,\quad i\ne j,                    \tag{29}
\]

then all four points are pure: each has either \(P=0\) or \(S=0\).  The
two zero pairs have the same purity type, and the endpoints of each target
pair have opposite types.  The proof is the rank-one equality
\(PS'^{\mathsf T}=-P'S^{\mathsf T}\): a zero pair is either equally pure
or an antipodal mixed pair, and the mixed alternatives make the two
distinct coordinate targets proportional.

### The triangle

Let the three rank-one sites be

\[
 A:\{0,2\},\qquad B:\{0,1\},\qquad C:\{1,2\},
 \qquad B_0=AB,\ B_1=BC,\ B_2=CA.                       \tag{30}
\]

Apply (29) to the color-zero target \(A_0B_0\) and the color-one target
\(B_1C_1\), using the zero corners \(A_0B_1\) and \(B_0C_1\).  It makes
\(A_0,B_1\) pure of one type and \(B_0,C_1\) pure of the opposite type.
Apply it again to \(B_1C_1\) and the color-two target \(C_2A_2\).  The zero
corners \(B_1C_2\) and \(C_1A_2\) make \(B_1,C_2\) one type and
\(C_1,A_2\) the opposite type.  Hence \(A_2\) and \(B_1\) are nonzero pure
points of opposite types, so \(\Phi(A_2,B_1)\ne0\).  But this is a zero
corner of the \(AB\) grid (28), a contradiction.  Thus the \((3,0,3)\)
triangle is impossible from the typed response equations alone.

### The three-edge path

Normalize the missing-color sets and omission pairs as

\[
 A:\{0\},\quad B:\{0,1\},\quad C:\{1,2\},\quad D:\{2\},
 \qquad B_0=AB,\ B_1=BC,\ B_2=CD.                       \tag{31}
\]

The color-zero and color-one targets, with zero corners \(A_0B_1\) and
\(B_0C_1\), make \(A_0,B_1\) pure of one type and \(B_0,C_1\) pure of the
opposite type.  The color-one and color-two targets, with zero corners
\(B_1C_2\) and \(C_1D_2\), make \(B_1,C_2\) the first type and
\(C_1,D_2\) the second.  The central grid corner \(B_0C_2\) therefore joins
two nonzero pure points of opposite types and is nonzero, contradicting its
required zero in (28).  This closes the \((2,2,2)\) path.

### The wedge forces the five no-rerouting cofactors

Return to (1)--(2), and denote the missing-color modes by

\[
 A_0,\quad B_0,B_1,\quad C_1,\quad D_2,\quad E_2.       \tag{32}
\]

The \(AB\) and \(BC\) grids and (29) make \(A_0,B_1\) pure of one type and
\(B_0,C_1\) pure of the opposite type.  Consequently
\(\Phi(A_0,C_1)\ne0\).  The double quotient on the non-omission pair \(AC\)
is

\[
                         \Phi(A_0,C_1)\otimes F_{AC}=0,
\]

so \(F_{AC}=0\).

If \(F_{BD}\ne0\), every typed entry of its zero-response quotient would
give

\[
                         \Phi(B_0,D_2)=\Phi(B_1,D_2)=0. \tag{33}
\]

Because \(B_0,B_1\) are nonzero pure points of opposite types, (33) forces
both components of \(D_2\) to vanish.  This contradicts the nonzero target
\(\Phi(D_2,E_2)\in\mathbb F^*E_{22}\).  Hence \(F_{BD}=0\), and the same
argument gives \(F_{BE}=0\).

Globally interchange \(P,S\), and interchange \(D,E\), if necessary, so
that \(A_0,B_1\) are \(P\)-pure, \(B_0,C_1\) are \(S\)-pure, and the
nonzero color-two target has \(P_{D_2}S_{E_2}^{\mathsf T}\ne0\).  Then

\[
                         \Phi(C_1,D_2)\ne0,\qquad
                         \Phi(A_0,E_2)\ne0.             \tag{34}
\]

The zero-response double quotients on \(CD\) and \(AE\) force respectively
\(F_{CD}=0\) and \(F_{AE}=0\).  Together with \(F_{AC},F_{BD},F_{BE}=0\),
these are exactly the five literal equations (4).

Therefore the typed-grid argument reduces the equality-budget frontier to
the wedge-plus-disjoint geometry, and within that geometry Theorem 1.1
needs only the three additional hole-block vanishings (3).  The later
[unconditional primary resolution](wedge-equality-hole-block-resolution.md)
proves those vanishings are unnecessary.  Conditional on its pending
clean-room audit, rank budget strictly above twelve, not the
rank-budget-twelve wedge, is the surviving frontier.

The companion checker
[`verify_wedge_equality_coordinate_oriented_obstruction.py`](../computations/verify_wedge_equality_coordinate_oriented_obstruction.py)
enumerates every four- and six-site matching, verifies (8)--(16) as formal
identities, audits the five row-selected pairs, checks the exact rank-two
Segre minor, and exhausts the purity-type constraints for the wedge, path,
and triangle typed grids.
