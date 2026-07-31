# Restoring the second diagonal does not couple the exact-cancellation carrier

## 1. Outcome

Work in an intrinsic scalar-unit chart on \(2h\) residual sites,
\(h\geq3\), and put

\[
 r=\alpha^{-1}R_{aa},\qquad q_t=q+tr,
 \qquad F_{jk}(t)=R_{jk}q_t^{[h-1]}.
\tag{1}
\]

Here and below \(j,k\in C=\{b,c\}\) whenever \(F_{jk}\) is used.

On the clean coordinate-monomial one-hole branch,

\[
 Z_{bb}=-\alpha^{h-1}X_b,
 \qquad Z_{bc}=Z_{cb}=Z_{cc}=0,
\tag{2}
\]

the complete complementary rows are exactly the two endpoint conditions

\[
 \boxed{
 F(0)=\begin{pmatrix}X_b&0\\0&X_c\end{pmatrix},
 \qquad
 F(1)=\begin{pmatrix}0&0\\0&X_c\end{pmatrix}.}
\tag{3}
\]

The common physical carrier and the Segre square give the all-order
derivative identity

\[
 \boxed{
 F'_{jk}(t)=R_{jk}r q_t^{[h-2]}
   =\alpha^{-1}R_{ja}R_{ak}q_t^{[h-2]}.}
\tag{4}
\]

Thus the whole first normal packet is the literal path integral of the
two-step squares:

\[
 Z_{jk}=\alpha^{h-1}\int_0^1F'_{jk}(t)\,dt.
\tag{5}
\]

Eliminating the endpoint constraints in (3) gives the sharp uniform
normal form

\[
 \boxed{
 \begin{aligned}
 F_{bb}(t)&=(1-t)X_b+t(t-1)U_{bb}(t),\\
 F_{cc}(t)&=X_c+t(t-1)U_{cc}(t),\\
 F_{bc}(t)&=t(t-1)U_{bc}(t),\\
 F_{cb}(t)&=t(t-1)U_{cb}(t),
 \end{aligned}}
\tag{6}
\]

where every \(U_{jk}\) is an arbitrary tensor-valued polynomial of degree
at most \(h-3\), as far as the endpoint data are concerned.  In
particular the restored \(cc\) row only says that
the zeroth moment of its square in (4) is zero.  It imposes no relation on
the cancelling \(bb\) square.  There is no determinant or rank-one
consequence: the four restrictions in (4) are restrictions of one physical
bilinear carrier, and such a restriction can have rank two.

This endpoint decoupling is sharp in the literal site-square-zero algebra.
Section 3 gives a rational six-site packet with good endpoint stars,
literal \(R_{ij}=p_i s_j\), all Segre identities, and the **entire restored
complementary block** in (3).  It has

\[
 F_{bb}(t)=(1-t)X_b,\qquad F_{cc}(t)=X_c,
 \qquad F_{bc}(t)=F_{cb}(t)=0.                         \tag{7}
\]

The cancelling term is a marked matching of weight \(-1\).  Its marked
\(R_{aa}\)-orientation equals the corresponding coefficient of \(q\), so

\[
                  \alpha q_e-(R_{aa}^{\rightarrow})_e=0.          \tag{8}
\]

Thus the restored \(cc\) row and the common Segre carrier do **not** force
the relevant \(H_a\)-supported orientation to have nonzero curvature.

The guard is not full nine.  Its first failures are exact and named:

* the exceptional \((a,a)\) row is \(0-X_a\); and
* one selected-cross mixed-word row has
  \([X_{ccbbcb}]R_{ac}q^{[2]}=1\).

Every other original pair row holds, including the restored \(cc\) row and
both complementary cross rows.  Therefore a positive theorem under the
actual full-nine hypothesis must use the exceptional target together with
a selected-cross **mixed-word cohafnian identity**.  Simultaneous \(bb/cc\)
diagonal rows, the complementary cross rows, endpoint values, or the Segre
factorization alone cannot supply that coupling.  This is an exact no-go
for the proposed ninth-row-only inference, not a full-source guard or a
proof of Krenn's conjecture.

There is a sharper local statement.  If the displayed sparse stars and
the displayed \(cc\)-matching channel \(14|35\) are retained, then imposing
the failed \(ac\) row moves its residual into the already-good \(ba\) row.
Consequently that channel cannot be repaired to full nine.  The exact
equations force the \(cc\) target to reroute through \(13|45\).  They do
not yet rule out the rerouted channel; Section 4 records the resulting
mixed-coefficient chain and the precise missing constraint.

## 2. Uniform endpoint elimination

The full-nine rows at \(t=0\) give

\[
 F_{bb}(0)=X_b,\quad F_{cc}(0)=X_c,\quad
 F_{bc}(0)=F_{cb}(0)=0.                                \tag{9}
\]

Since

\[
 (\alpha q+R_{aa})^{[h-1]}
       =\alpha^{h-1}q_1^{[h-1]},                       \tag{10}
\]

equation (2) gives the four values at \(t=1\) in (3).  No matching power
has been cancelled.

For any polynomial \(P\) of degree at most \(h-1\), prescribed values at
zero and one leave precisely a multiple of \(t(t-1)\).  Applying this
entrywise proves (6), including the degree bound.  Conversely every table
in (6) has exactly the endpoints (3), so the normal form is sharp.

Differentiating divided powers and using the physical square gives

\[
 \begin{aligned}
 F'_{jk}(t)
  &=R_{jk}r q_t^{[h-2]}\\
  &=\alpha^{-1}(p_js_k)(p_as_a)q_t^{[h-2]}\\
  &=\alpha^{-1}(p_js_a)(p_as_k)q_t^{[h-2]}\\
  &=\alpha^{-1}R_{ja}R_{ak}q_t^{[h-2]},
 \end{aligned}                                         \tag{11}
\]

which proves (4).  Integrating (11), then using the definition of
\(\Theta_a\), proves (5).  In particular

\[
 \int_0^1F'_{bb}(t)\,dt=-X_b,qquad
 \int_0^1F'_{cc}(t)\,dt=0.                             \tag{12}
\]

These are two values of the common carrier on two different endpoint
arguments.  A bilinear form can take them independently.  Multiplying the
two top-degree values is zero in the physical site algebra and is not a
legal way to manufacture a determinant identity.

For comparison, the unary top path \(A(t)=q_t^{[h]}\) obeys

\[
 A(1)=\alpha^{-1}X_a,qquad
 A(0)+A'(0)=\alpha^{-1}X_a                              \tag{13}
\]

only after the exceptional row and unary cleanliness are imposed.  The
endpoint system (3) has no implication toward (13).  The physical guard
below deliberately fails (13); that failure cannot be repaired by
declaring an abstract \(X_a\), because the mixed-word rows must be realized
by the same quadratic \(q\).

## 3. A restored-\(cc\), exact-cancellation physical guard

Take \(h=3\), \(\alpha=1\), labels \(a=0,b=1,c=2\), and residual sites
\(0,1,\ldots,5\).  Write \(e^d_{uv}=x_u^dx_v^d\), and set

\[
 \begin{aligned}
 q={}&2e^b_{23}+e^b_{45}-e^b_{34}+e^b_{25}
       +e^c_{14}+e^c_{35},\\
 p_a={}&x_3^b,&s_a={}&-x_4^b,\\
 p_b={}&x_0^b,&s_b={}& x_1^b,\\
 p_c={}&x_2^c,&s_c={}& x_0^c.
 \end{aligned}                                         \tag{14}
\]

The two star triples are linearly independent.  Put \(R_{ij}=p_i s_j\),
so

\[
 R_{aa}=-e^b_{34},\qquad R_{bb}=e^b_{01},
 \qquad R_{cc}=e^c_{02},\qquad R_{bc}=0.               \tag{15}
\]

The \(b\)-subgraph on the complement of \(\{0,1\}\) is the four-cycle
with its two perfect matchings

\[
       23|45\quad\hbox{of weight }2,qquad
       34|25\quad\hbox{of weight }-1.                  \tag{16}
\]

Hence

\[
 R_{bb}q^{[2]}=X_b.                                     \tag{17}
\]

Along \(q_t=q+tR_{aa}\), the marked edge \(34\) has weight
\(-(1+t)\).  Therefore its matching changes from \(-1\) to
\(-(1+t)\), while the other matching stays \(2\), and

\[
                         R_{bb}q_t^{[2]}=(1-t)X_b.      \tag{18}
\]

For the \(c\)-row, the cap \(02\) and the two cells \(14,35\) give the
unique compatible matching, so

\[
                         R_{cc}q_t^{[2]}=X_c            \tag{19}
\]

for every \(t\).  Direct enumeration of physical complements gives both
cross rows zero.  Equations (18)--(19) prove (7) coefficientwise, not only
on the three target coordinates.

Since \(R_{aa}^{[2]}=0\),

\[
 H_a=q+\tfrac12R_{aa},\qquad
 \Theta_a=(q+R_{aa})^{[2]}-q^{[2]}=R_{aa}H_a=R_{aa}q.   \tag{20}
\]

The sole \(bb\)-carrier term is

\[
 R_{bb}R_{aa}e^b_{25}=-X_b,                             \tag{21}
\]

while the contributing forward orientation at \(e^b_{34}\) is

\[
 (R_{aa}^{\rightarrow})_{34}=-1=q_{34}^b,qquad
 \kappa_{34}^{\rightarrow}=q_{34}^b-
        (R_{aa}^{\rightarrow})_{34}=0.                 \tag{22}
\]

This is the promised aligned exact cancellation.

The complete original-row audit is

\[
\begin{array}{c|ccc}
 &a&b&c\\ \hline
a&0&0&X_{ccbbcb}\\
b&0&X_b&0\\
c&0&0&X_c.
\end{array}                                             \tag{23}
\]

The desired table has \(X_a\) in the \(aa\)-cell and zeros off diagonal.
Thus precisely the \(aa\) and \(ac\) rows fail.  The mixed residual in
(23) comes from the cap \(R_{ac}=x_3^bx_0^c\) together with the two cells
\(e^c_{14}\) and \(e^b_{25}\).  It is exactly the first cross-word
cohafnian coefficient omitted by the endpoint table.

## 4. The first failed cross word forces a \(cc\)-channel reroute

The \(ac\) residual can be chased one step further without cancelling a
matching power.  Keep the sparse stars in (14), but temporarily allow
arbitrary decorated coefficients in \(q\).  Write
\(q_{uv}^{de}\) for the coefficient having colour \(d\) at site \(u\)
and colour \(e\) at site \(v\).

The exact jet equations are injective on the unique remaining physical
pair.  Namely,

\[
 \begin{aligned}
 Z_{bb}=-X_b
 &\quad\Longrightarrow\quad
 q_{25}^{bb}=1,\qquad q_{25}^{de}=0\quad((d,e)\ne(b,b)),\\
 Z_{cc}=0
 &\quad\Longrightarrow\quad
 q_{15}^{de}=0\quad\hbox{for every }d,e.
 \end{aligned}                                               \tag{24}
\]

For the failed word

\[
                 \omega=(c,c,b,b,c,b),
\]

the three matchings on the complement of the \(ac\)-cap \(30\) give

\[
 \begin{aligned}
 [X_\omega]R_{ac}q^{[2]}
   &=q_{12}^{cb}q_{45}^{cb}
     +q_{14}^{cc}q_{25}^{bb}
     +q_{15}^{cb}q_{24}^{bc}\\
   &=q_{12}^{cb}q_{45}^{cb}+q_{14}^{cc}.              \tag{25}
 \end{aligned}
\]

Thus the visible term \(q_{14}^{cc}q_{25}^{bb}\) need not vanish
termwise: \(12|45\) is a legal complex cancellation mate.  It does not
use the marked coefficient \(q_{34}^{bb}\), so (25) alone has no
curvature consequence.

The already-good \(ba\) row detects that mate.  At
\(\eta=(b,c,b,c,b,c)\), its cap is \(-e_{04}^b\), and

\[
 \begin{aligned}
 [X_\eta]R_{ba}q^{[2]}
   &=-\left(
       q_{12}^{cb}q_{35}^{cc}
       +q_{13}^{cc}q_{25}^{bc}
       +q_{15}^{cc}q_{23}^{bc}\right)\\
   &=-q_{12}^{cb}q_{35}^{cc}.                          \tag{26}
 \end{aligned}
\]

If the displayed \(cc\) channel is retained, so that
\(q_{14}^{cc}q_{35}^{cc}\ne0\), equation (26) forces
\(q_{12}^{cb}=0\), and then the \(ac\) equation (25) forces
\(q_{14}^{cc}=0\), a contradiction.  Hence the guard cannot be repaired
inside its displayed \(14|35\) channel.

The pure \(cc\) target coefficient makes the surviving alternative
explicit:

\[
 q_{13}^{cc}q_{45}^{cc}
 +q_{14}^{cc}q_{35}^{cc}
 +q_{15}^{cc}q_{34}^{cc}=1.
                                                               \tag{27}
\]

Using (24), full \(ac\) and \(ba\) rows force the second product in
(27) to vanish, and therefore

\[
                         \boxed{q_{13}^{cc}q_{45}^{cc}=1.}       \tag{28}
\]

This is a genuine advance over the endpoint table: a hypothetical
full-nine extension of this sparse-star sector must reroute the restored
diagonal through \(13|45\).  It is not yet a contradiction.  For example,
the \(ba\) word \((b,c,b,c,b,b)\) then requires

\[
 \rho_{ba}^{\mathrm{rer}}
   :=q_{12}^{cb}q_{35}^{cb}+q_{13}^{cc}=0,                       \tag{29}
\]

while the off-target \(bb\) word \((b,b,b,b,c,c)\) requires

\[
 \rho_{bb}^{\mathrm{rer}}
   :=q_{23}^{bb}q_{45}^{cc}
       +q_{24}^{bc}q_{35}^{bc}=0.                               \tag{30}
\]

These are new mixed cancellation channels, not equations in the marked
\(q_{34}^{bb}\) coefficient.

The exceptional \(aa\) row supplies no mate on the first word.  In the
literal guard,

\[
 [X_\omega]\left(q^{[3]}+R_{aa}q^{[2]}\right)=0+0.               \tag{31}
\]

The first zero holds because \(q\) has no site-\(0\) cell.  The second
holds because \(R_{aa}\) has colour \(b\) at site \(4\), whereas
\(\omega_4=c\).  Its actual failure is the distinct constant-\(a\) word
\(-X_a\).  Combining that constant-word defect with (25), (29), or (30)
would require a source-faithful mixed-word transport identity.  Multiplying
top equations or choosing one term of a hafnian would be illegal.

As a sharp one-word audit, adding
\(q_{12}^{cb}=1\) and \(q_{45}^{cb}=-1\) cancels (25) while leaving
\(q_{34}^{bb}=(R_{aa}^{\rightarrow})_{34}\) unchanged.  Equation (31)
also stays zero, but (26) becomes \(-1\).  Thus the repair transports the
residual from \(ac\) to \(ba\); the \(aa\) equation does not absorb it.

## 5. Exact scope

The theorem does not say that the branch (2) occurs in a full exact source.
Such a physical full-nine realization would be far stronger.  The guard
instead proves the following sharp logical boundary:

\[
 \boxed{\text{restored }cc+\text{all complementary rows}
   +\text{Segre}+\text{exact cancellation}
   \not\Longrightarrow
   \text{relevant oriented curvature}.}
\tag{32}
\]

The selected \(ac\) and already-good \(ba\) rows do force the local
reroute (28), but the precisely named residual equations
\(\rho_{ba}^{\mathrm{rer}}=\rho_{bb}^{\mathrm{rer}}=0\) remain compatible
with complex cancellation.  The exact missing constraint is a
source-faithful identity coupling that rerouted mixed-cohafnian chain
either to a selected constant-\(a\) matching in the exceptional row or
back to the marked \(q_{34}^{bb}\) coefficient.

The admissible global input is the all-word full-nine cohafnian equation

\[
 P_\omega^{\mathsf T}H(Q_\omega)S_\omega
      =-\operatorname{haf}(Q_\omega)\alpha E_{aa}
\tag{33}
\]

for a word such as \(\omega=ccbbcb\), together with the exceptional unary
row.  A successful proof must show that the marked \(bb\) carrier forces a
nonzero left side outside the \(aa\)-cell, or transport the resulting class
through a source-faithful four-cut operation.  Equation (6) shows why no
endpoint resultant can do this.

The dependency-free checker
[`verify_scalar_unit_restored_cc_exact_cancellation_selected_cross_guard.py`](../computations/verify_scalar_unit_restored_cc_exact_cancellation_selected_cross_guard.py)
audits every tensor coefficient in (14)--(31), all nine Segre squares,
the star ranks, the endpoint polynomial table, the aligned orientation,
the one-word repair/transport, and sign/carrier mutations.  It uses
explicit failures and remains active under `python -O`.
