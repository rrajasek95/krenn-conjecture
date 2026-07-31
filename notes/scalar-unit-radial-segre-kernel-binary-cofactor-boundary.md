# The radial kernel meets the open Segre torus away from one-coordinate spikes

## 1. Outcome

Work in the clean off-target intrinsic scalar-unit
[radial normal form](scalar-unit-off-target-radial-quotient-pure-factor-normal-form.md)
on \(2h\) residual sites, \(h\geq3\).  Thus

\[
 \alpha\delta_{ia}\delta_{ja}q^{[h]}
      +R_{ij}q^{[h-1]}=\delta_{ij}X_i,
 \qquad R_{ij}=p_i s_j,
 \qquad \alpha\ne0,                                      \tag{1}
\]

\[
 Q=q^{[h]}\notin D:=\operatorname {span}\{X_a,X_b,X_c\},
 \qquad G=\alpha q+r,\qquad r=R_{aa},
 \qquad G^{[h]}=\alpha^{h-1}X_a,                         \tag{2}
\]

and, for \(j,k\in C:=\{b,c\}\),

\[
 R_{jk}rH=\lambda_{jk}Q,
 \qquad R_{jk}q^{[h-1]}=\delta_{jk}X_j.                  \tag{3}
\]

For every selected nonzero entry \(\lambda_{uv}\), the same full-nine
normal form retains the primitive-square and pure-inverse data

\[
 A_{uv}=R_{ua},\quad B_{uv}=R_{av},\qquad
 A_{uv}q^{[h-1]}=B_{uv}q^{[h-1]}=0,\qquad
 A_{uv}B_{uv}H=\lambda_{uv}Q,                            \tag{3a}
\]

\[
 C_{uv}=q^{[h-1]}+{\alpha\over\lambda_{uv}}R_{uv}H,
 \qquad rC_{uv}=X_a.                                    \tag{3b}
\]

They remain in force below.  The point of the new argument is to use the
rank-one geometry of the whole radial kernel rather than cancel any factor
in (3a)--(3b).

At the maximum-anchor representative the matrix

\[
             \Lambda=(\lambda_{jk})_{j,k\in C}          \tag{4}
\]

is nonzero.  Call it a **coordinate spike** if exactly one of its four
entries is nonzero.

> **Theorem 1.1 (open-Segre radial-kernel dichotomy).**  If \(\Lambda\)
> is not a coordinate spike, there are
> \(x=(x_b,x_c)\in(\mathbb C^*)^2\) and
> \(y=(y_b,y_c)\in(\mathbb C^*)^2\) such that
> \[
>                    x^{\mathsf T}\Lambda y=0.           \tag{5}
> \]
> Hence the rank-one matrix \(K=xy^{\mathsf T}\) lies in
> \(\ker\lambda\) and all four of its entries are nonzero.  Put
> \[
> P=x_bp_b+x_cp_c,\qquad S=y_bs_b+y_cs_c,
> \qquad W=R_K=PS.                                      \tag{6}
> \]
> Then, literally in the physical site algebra,
> \[
> \boxed{
> WrH=0,\qquad
> Wq^{[h-1]}=x_by_bX_b+x_cy_cX_c.}                       \tag{7}
> \]
> More strongly, the binary response is the sum of two common-cofactor
> pure responses on each endpoint:
> \[
> \boxed{
> \begin{array}{ll}
> p_b(Sq^{[h-1]})=y_bX_b,&p_c(Sq^{[h-1]})=y_cX_c,\\
> s_b(Pq^{[h-1]})=x_bX_b,&s_c(Pq^{[h-1]})=x_cX_c.
> \end{array}}                                           \tag{8}
> \]

Goodness makes \(P,S\ne0\); no cancellation of \(q^{[h-1]}\), \(H\),
or a star factor is used.  The cap line

\[
                         E_{aa}+zK                       \tag{9}
\]

is active for every \(z\ne0\).  Its exact clean error is stationary to
first order:

\[
 \boxed{
 \mathcal E(E_{aa}+zK)
   =\sum_{m=2}^h z^mW^{[m]}G^{[h-m]}.}                  \tag{10}
\]

Consequently a nonzero common root of the right side is already an active
clean cap and gives the certified raw order descent.  If no such root
exists, the branch is confined to the sharply named
**rootless stationary Segre boundary**.  The only radial coefficient
pattern not entering this rank-one reduction is the
**coordinate-spike boundary**.

The spike distinction is exact.  For a diagonal spike, every member of
\(\ker\lambda\) has one complementary diagonal entry zero, so there is no
active stationary direction.  For an off-diagonal spike, active matrices
do occur in the kernel, but every rank-one kernel matrix has one
complementary diagonal entry zero.  Thus the older unrestricted kernel
direction remains available there, while the binary factorization (6)--(8)
does not.

This is a positive structural reduction, not a clean-root theorem.  In
particular, (8) does not make \(W^{[2]}G^{[h-2]}\) vanish.  Section 4 gives
an exact six-site guard satisfying eight of the nine physical rows which
shows that even goodness, the complete complementary block, both selected
primitive rows, and the carrier-kernel equation do not imply that
vanishing.  Its sole failed row is the exceptional \(aa\) target, and its
top power and entire radial jet packet are zero; hence it has no nonzero
off-target radial coefficient matrix, does not realize the hypotheses of
Theorem 1.1, and does not contradict maximum-anchor extremality.

## 2. The open-Segre intersection

Write

\[
 \Lambda=\begin{pmatrix}
 \lambda_{bb}&\lambda_{bc}\\
 \lambda_{cb}&\lambda_{cc}
 \end{pmatrix}.
\]

On the open Segre torus normalize \(x_b=y_b=1\), and put
\(x_c=s,\ y_c=t\).  Equation (5) becomes

\[
 (\lambda_{bb}+\lambda_{bc}t)
   +s(\lambda_{cb}+\lambda_{cc}t)=0.                    \tag{11}
\]

If both rows of \(\Lambda\) are nonzero, choose \(t\in\mathbb C^*\)
away from the at most two zeros of the two parentheses, and take \(s\) to
be minus their ratio.  Then \(s\ne0\) and (11) holds.  If the second row
is zero, non-spikeness says both entries of the first row are nonzero;
take \(t=-\lambda_{bb}/\lambda_{bc}\) and any \(s\ne0\).  The case in
which the first row is zero is symmetric.  This proves existence.

Conversely, if \(\Lambda\) has one nonzero entry, its value at
\((x,y)\in(\mathbb C^*)^2\times(\mathbb C^*)^2\) is one nonzero
monomial.  It cannot vanish.  Thus coordinate spikes are exactly the
hyperplanes whose intersection with the open Segre torus is empty; this
is not merely a sufficient exceptional list.

For \(K=xy^{\mathsf T}\), the physical response factors without changing
endpoint order:

\[
 \begin{aligned}
 R_K
 &=\sum_{j,k\in C}x_jy_kp_js_k\\
 &=(x_bp_b+x_cp_c)(y_bs_b+y_cs_c)=PS.                   \tag{12}
 \end{aligned}
\]

Contracting (3) by \(K\) gives (7).  Keeping one endpoint uncontracted
instead gives (8); for example

\[
 p_bSq^{[h-1]}
   =y_bR_{bb}q^{[h-1]}+y_cR_{bc}q^{[h-1]}=y_bX_b.       \tag{13}
\]

The other three identities are identical.  These are equalities after
all aggregate parallel cells and all complex cancellations have already
been summed.

Because \(K_{bb}=x_by_b\ne0\) and \(K_{cc}=x_cy_c\ne0\), (9) has all
three nonzero diagonal target coordinates for \(z\ne0\), and is active.
The
[full normal-jet identity](scalar-unit-full-normal-jet-unary-anchor-ledger.md)
at the clean unary cap has first coefficient

\[
             R_K\Theta=WrH=\lambda(K)Q=0.              \tag{14}
\]

The powers of \(\alpha\) in this cancellation are essential.  Directly
from the definition of the clean error and (7),

\[
\begin{aligned}
\mathcal E(E_{aa}+zK)
={}&G^{[h]}+zWG^{[h-1]}
       +\sum_{m=2}^h z^mW^{[m]}G^{[h-m]}\\
 &-\alpha^{h-1}
       \bigl(X_a+z(x_by_bX_b+x_cy_cX_c)\bigr)\\
={}&zW\bigl(G^{[h-1]}-\alpha^{h-1}q^{[h-1]}\bigr)
       +\sum_{m=2}^h z^mW^{[m]}G^{[h-m]}\\
={}&zWrH+\sum_{m=2}^h z^mW^{[m]}G^{[h-m]}.
\end{aligned}                                           \tag{14a}
\]

Here \(s(E_{aa}+zK)=\alpha\), so the target subtraction really is
\(\alpha^{h-1}T(E_{aa}+zK)\).  Equation (14) removes the first term in
(14a) and gives (10) for arbitrary nonzero \(\alpha\), not only after
normalizing \(\alpha=1\).  No implication about the common roots of the
remaining vector coefficients follows.

## 3. Exact residual after the reduction

The theorem leaves two disjoint algebraic boundaries.

1. **Coordinate spike.**  The rank-one torus misses \(\ker\lambda\).
   A diagonal spike also removes every active kernel direction; an
   off-diagonal spike retains active rank-two directions but no active
   rank-one direction.
2. **Rootless stationary Segre boundary.**  Equations (7)--(8) hold with
   all four coefficients nonzero, but the vector polynomial
   \[
        \sum_{m=2}^h z^{m-2}W^{[m]}G^{[h-m]}            \tag{15}
   \]
   has no common nonzero root.

The second boundary is substantially narrower than an arbitrary radial
kernel.  It carries two decomposable one-site factors, two pure target
coefficients, both common-cofactor tables (8), and every higher coefficient
in (15) comes from divided powers of the same literal \(PS\).  Nevertheless
the common-cofactor equations live at top degree.  Multiplying or cancelling
their \(q^{[h-1]}\) factor is illegal, and they do not determine
\(W^{[2]}G^{[h-2]}\).

The primitive-square and pure-inverse relations (3a)--(3b) also remain
available.  They do not remove either boundary: on a coordinate spike they
are precisely the surviving selected primitive packet, while on the
non-spike branch they coexist with (7)--(8).  Turning \(rC_{uv}=X_a\) into a
split factor would require killing its multiplication-kernel class; the
open-Segre construction neither assumes nor proves that cancellation.

Maximum-anchor extremality enters only in the already certified assertion
\(\Lambda\ne0\).  Goodness enters only to keep the two complementary star
planes injective and hence \(P,S\ne0\).  Anchor counts do not make a root
of (15), and no same-order pivot follows unless all the required higher
coefficients actually vanish.  If a nonzero root does occur, one uses the
ordinary active clean-pair descent, not cancellation of any carrier.

## 4. An eight-of-nine physical guard

Take \(h=3,\ \alpha=1\), residual sites \(0,\ldots,5\), and labels
\(a,b,c\).  Write \(x_i^d\) for colour \(d\) at site \(i\), and set

\[
 \begin{aligned}
 q={}&x_1^bx_2^b+x_4^bx_5^b
       +x_0^cx_1^c+x_3^cx_4^c,\\
 p_a={}&x_1^a,&p_b={}&x_0^b,&p_c={}&x_5^c,\\
 s_a={}&x_4^a,&s_b={}&x_3^b,&s_c={}&x_2^c.
 \end{aligned}                                          \tag{16}
\]

Both endpoint triples are linearly independent.  Put \(R_{ij}=p_is_j\),
\(r=R_{aa}=x_1^ax_4^a\),

\[
 H=q+\tfrac12r,\qquad G=q+r.                            \tag{17}
\]

The four cells of \(q\) are the two residual pieces of an alternating
binary eight-cycle.  Direct complement enumeration gives

\[
 R_{bb}q^{[2]}=X_b,\qquad R_{cc}q^{[2]}=X_c,
 \qquad R_{ij}q^{[2]}=0\quad(i\ne j),                  \tag{18}
\]

and also \(R_{aa}q^{[2]}=0\).  Since \(q^{[3]}=0\), the complete row table
is

\[
\begin{array}{c|ccc}
 &a&b&c\\ \hline
a&0&0&0\\
b&0&X_b&0\\
c&0&0&X_c.
\end{array}                                             \tag{19}
\]

Thus (19) satisfies eight of the nine scalar-unit rows and fails only the
exceptional equation \(0=X_a\).  In particular both selected primitive
rows

\[
                  R_{ba}q^{[2]}=R_{ac}q^{[2]}=0         \tag{20}
\]

are literal.

Take the all-ones rank-one complementary matrix

\[
 K=\begin{pmatrix}1&1\\1&1\end{pmatrix}=xy^{\mathsf T},
 \qquad x=y=(1,1),                                     \tag{21}
\]

and put

\[
 P=p_b+p_c,\qquad S=s_b+s_c,\qquad W=PS.               \tag{22}
\]

Then the full binary common-cofactor packet is exact:

\[
 \begin{array}{ll}
 p_b(Sq^{[2]})=X_b,&p_c(Sq^{[2]})=X_c,\\
 s_b(Pq^{[2]})=X_b,&s_c(Pq^{[2]})=X_c,
 \end{array}
 \qquad Wq^{[2]}=X_b+X_c.                              \tag{23}
\]

Every complementary radial jet vanishes by physical collision, so in
particular

\[
                              WrH=0.                    \tag{24}
\]

But the first uncontrolled higher coefficient is nonzero.  With

\[
 Y=x_0^bx_1^ax_2^cx_3^bx_4^ax_5^c,
\]

one has

\[
                  W^{[2]}=2x_0^bx_2^cx_3^bx_5^c,
 \qquad W^{[2]}G=2Y\ne0,\qquad W^{[3]}=0.              \tag{25}
\]

Indeed the \(q\)-part collides with \(W^{[2]}\), while \(r\) occupies its
two missing sites.  The literal cap error of this guard is therefore

\[
             (G+zW)^{[3]}-(X_a+zX_b+zX_c)
                    =-X_a+2z^2Y,                       \tag{26}
\]

which has no common root.  Equation (26) is not a counterexample to the
clean-unary theorem: its constant defect is exactly the sole missing row
in (19).  It proves the sharp logical boundary

\[
 \boxed{
 \text{goodness + eight rows + primitive rows + (23)--(24)}
 \not\Longrightarrow W^{[2]}G=0.}                      \tag{27}
\]

The guard also has \(q^{[3]}=0\) and an identically zero radial jet packet,
so it has no nonzero off-target \(\Lambda\); maximum-anchor extremality is
the other visibly absent hypothesis.  Supplying a nonzero radial entry and
the exceptional target simultaneously is precisely what a positive
continuation must exploit; neither can be replaced by the binary top
response alone.

## 5. Scope and audit

The open-Segre theorem uses all four complementary rows, the complete
radial quotient, and the clean unary normal jet.  The exceptional row is
retained in (3b), but is not used again after the normal form has been
assumed; the guard shows that omitting it from a proposed higher-coefficient
argument is material.  Maximum-anchor extremality is used only to exclude
the zero radial packet.  No conclusion is drawn termwise from a zero
aggregate coefficient, so parallel decorated cells and arbitrary complex
cancellation remain allowed.

The dependency-free checker
[`verify_scalar_unit_radial_segre_kernel_binary_cofactor_boundary.py`](../computations/verify_scalar_unit_radial_segre_kernel_binary_cofactor_boundary.py)
constructs an open-torus kernel point for every non-spike integer
\(2\times2\) matrix in a fixed exhaustive box, checks the exact spike
classification, and audits every coefficient of (16)--(26), both star
ranks, all nine Segre squares, all nine physical rows, the common-cofactor
packet, and deterministic mutations.  It uses explicit exceptions and
runs unchanged under `python -O`.

This note isolates a rank-one stationary reduction and two sharply named
boundaries.  It is not an active-clean-cap theorem, an exact same-order
pivot, a raw order descent on the rootless boundary, or a proof of Krenn's
conjecture.
