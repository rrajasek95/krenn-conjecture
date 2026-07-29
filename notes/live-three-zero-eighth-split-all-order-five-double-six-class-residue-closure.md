# The eighth split: all-order five-double six-class residue closure

## 1. Uniform result

Fix \(h=8\) and any common-pole order \(k\geq1\).  A no-extra-singular
collision profile is impossible whenever

\[
                  C=11,\qquad n_2\geq8,\qquad n_1\geq1, \tag{1}
\]

where \(C\) is the number of distinct exceptional value classes and
\(n_i\) counts classes of multiplicity \(i\).

The proof extends the all-order mixed-role construction to its natural
all-repeated endpoint: select five exact double classes, each at formal role
two.  The selected role is ten, every pair drop has role eight, and no
singleton layer is selected.  The kernel and duality remain independent of
\(k\).  Condition (1) makes the complement a six-class profile containing
at least three doubles and one simple root.  Varying which five double
classes are selected yields the contradiction.

At \(k=5\), this theorem closes

\[
                              3^2 2^8 1,                 \tag{2}
\]

the sole profile left open by the current fifth-order ledger.

## 2. The five-double kernel

Let the five selected double values be \(x_1,\ldots,x_5\), and put

\[
                         q_i(z)=z^2-x_i^2.               \tag{3}
\]

Lowering two formal layers leaves a five-class Hermite core with residual
degree at most two.  Multiplication by the two quadratic lift factors gives
ten nonzero pair lifts in

\[
                 W\subseteq\mathbb C[z]_{\leq6}.        \tag{4}
\]

Let \(K\) be the common kernel of the five exact order-two selected rows.
For a hypothetical \(m\)-dimensional kernel, forced Wronskian weight minus
the polynomial degree cap is

\[
              5(m-2)-m(7-m)=m^2-2m-10>0
                         \qquad(m\geq5).                 \tag{5}
\]

The same local gcd corrections as in the mixed-role theorem only strengthen
this inequality, so \(\dim K\leq4\).

Put \(U_i=W\cap q_i\mathbb C[z]\).  Four coprime neighbor quadratics have
total degree eight, greater than six, so \(\dim U_i\geq2\).  This also gives
\(\dim W\geq3\): a two-space would equal every \(U_i\), forcing the
degree-ten product of all five \(q_i\) to divide every member.

Suppose \(\dim W=3\).  The parity minors of a basis vanish at all ten points
\(\pm x_i\).  They are odd of degree at most eleven, so each is a constant
multiple of

\[
                         \Delta(z)=z\prod_{i=1}^5(z^2-x_i^2).         \tag{6}
\]

In vector form, \({\bf P}(z)\times{\bf P}(-z)=\Delta(z){\bf c}\).
Dotting with \({\bf P}(z)\) makes \({\bf c}\ne0\) a constant relation
among a basis, hence \({\bf c}=0\).  After removing the pencil gcd,

\[
                         W=G(z){\cal E}(z^2),
                         \qquad\dim{\cal E}=3.           \tag{7}
\]

Write \(g=\deg G\) and let \({\cal E}\subseteq\mathbb C[y]_{\leq m}\).
Then \(g+2m\leq6\) and \(m\geq2\).  If \(m=2\), then
\({\cal E}=\mathbb C[y]_{\leq2}\), while \(g\leq2\).  At least one of the
five nodes has \(G(-x_i)\ne0\).  In the exact selected row

\[
                         (B_iP)''(-x_i)=0,               \tag{8}
\]

the coefficient of \(E''(x_i^2)\), for \(P=G E(z^2)\), is

\[
                         4x_i^2B_i(-x_i)G(-x_i)\ne0.     \tag{9}
\]

Thus (8) cannot annihilate the full quadratic space.

If \(m=3\), then \(g=0\).  At every one of the five distinct squares
\(x_i^2\), equation (8) is a nonzero relation among the first three jets of
the three-space \({\cal E}\).  Hence all five squares divide its Wronskian,
whose degree is at most

\[
                         3(3+1-3)=3.                    \tag{10}
\]

Both cases are impossible.  Therefore

\[
                         \boxed{W=K,\qquad\dim K=4}.     \tag{11}
\]

## 3. Endpoint duality

Five selected rows on the seven-dimensional space in (4) have rank three
by (11), hence a two-dimensional relation space.  If
\(Q(z)=\prod_{i=1}^5(z+x_i)\), its distinct-principal-part numerators have
degree at most

\[
                         3\deg Q-7-1=7.                 \tag{12}
\]

Let \(A\) be the complementary polynomial, of total degree \(k+8\), let
\(c\) be its number of distinct roots, and put

\[
 g_A=\prod_{A(a)=0}(z-a)^{\operatorname{ord}_a(A)-1},
 \quad R=A/g_A,\quad D_A=A'/g_A.                        \tag{13}
\]

The same exact differentiation as in the mixed-role theorem gives

\[
 {d\over dz}{(z+\mu)^{k+1}N\over A}
 ={(z+\mu)^kg_A\over A^2}
 \left[R\bigl((z+\mu)N'+(k+1)N\bigr)-(z+\mu)D_AN\right].              \tag{14}
\]

For \(\deg N\leq7\), the leading coefficient is again \(\deg N-7\).
Selected-pole contact supplies the degree-ten divisor \(Q^2\), so (14)
maps the relation space injectively to

\[
                         {\cal S}\subseteq
                         \mathbb C[z]_{\leq c-4},
                         \qquad\dim{\cal S}=2.           \tag{15}
\]

This proves an all-order five-double duality statement; no complementary
closure has yet been used.

## 4. Six complementary classes

Under (1), selecting any five doubles leaves exactly

\[
                              c=C-5=6                   \tag{16}
\]

complementary roots.  Thus \({\cal S}\) is a plane in
\(\mathbb C[z]_{\leq2}\).  Choose a simple complementary root \(r\).  Its
exact residue is one nonzero Robin functional on the quadratic space, so
\({\cal S}\) equals that functional's kernel.  In particular,

\[
                              (z-r)^2\in{\cal S}.         \tag{17}
\]

Choose eight of the double classes and call their values \({\cal D}\).
Fix an anchor \(u\in{\cal D}\).  Any additional double classes are held
fixed in the complement.  For every pair \(v,w\in{\cal D}\setminus\{u\}\),
select the other five values in \({\cal D}\).  At the complementary double
\(u\), insert (17) in (14).  The square cancels the simple-root denominator,
and the residue becomes

\[
                              C_{u;v,w}''(u)=0,           \tag{18}
\]

where all common-pole, nondouble, and fixed complementary-double factors
are independent of the varying pair \(\{v,w\}\).

Put

\[
 \Phi_u(t)={2\over u+t}+{3\over u-t}
           ={5u+t\over u^2-t^2},\qquad
 \Psi_u(t)={2\over(u+t)^2}+{3\over(u-t)^2}.             \tag{19}
\]

Writing the logarithmic first and second derivatives of \(C_{u;v,w}\) as

\[
 {C'\over C}(u)=A_u-\Phi_u(v)-\Phi_u(w),\qquad
 \left({C'\over C}\right)'(u)=B_u+\Psi_u(v)+\Psi_u(w), \tag{20}
\]

equation (18) is

\[
 (A_u-p_v-p_w)^2+B_u+\Psi_u(v)+\Psi_u(w)=0,
                         \qquad p_t=\Phi_u(t).           \tag{21}
\]

Define \(h_t=p_t^2+\Psi_u(t)-2A_up_t\).  Then (21) reads

\[
                         h_v+h_w+2p_vp_w+C_u=0.          \tag{22}
\]

Compare (22) for \((v,w)\) and \((v,x)\).  If
\(p_w\ne p_x\), all five choices
\(v\in{\cal D}\setminus\{u,w,x\}\) have the same value of \(p_v\).  This
is impossible because every fibre of \(\Phi_u\) is cut out by the nonzero
polynomial

\[
                         \lambda(u^2-t^2)-5u-t,          \tag{23}
\]

of degree at most two.  Hence \(p_w=p_x\) for every pair \(w,x\), putting
all seven values in one such fibre, again impossible.  This proves (1).

## 5. Exact census effect and audit

On the baseline higher-collision residual ledger, criterion (1) occurs
exactly in

\[
\begin{array}{c|l}
k&\text{profiles}\\ \hline
1&2^8 1^3\\
2&2^9 1^2\\
3&3\,2^8 1^2,\ 2^{10}1\\
4&3\,2^9 1\\
5&3^2 2^8 1.
\end{array}                                               \tag{24}
\]

The first four rows are recoveries of existing closures.  The last row is
the new closure (2), and empties the current \(k=5\) residual ledger.
This list is finite for a structural reason.  A baseline residual containing
a singleton has \(\lambda_1+\lambda_2\leq7\).  With eleven classes, at
least eight doubles, and at least one singleton, this bounds the total
profile size by 24, hence \(k\leq6\); the exact sixth-order row is empty.

[verify_live_three_zero_eighth_split_all_order_five_double_six_class_residue_closure.py](../computations/verify_live_three_zero_eighth_split_all_order_five_double_six_class_residue_closure.py)
checks the endpoint kernel dimensions, saturated parity refinement, both
square-space cases, all dual degrees at symbolic \(k\), the simple-root
kernel identity, both logarithmic signs, the pair-comparison argument,
quadratic fibre bound, the uniform size cap, and the exact census (24).
