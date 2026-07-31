# A selected-star fibre conserves the missing cross row and the scalar-unit carrier

## 1. Outcome

Work in the coloured site-square-zero algebra on \(2h\) residual sites,
over a characteristic-zero field. At an intrinsic scalar-unit pair write

\[
 \alpha\delta_{ia}\delta_{ja}q^{[h]}
      +R_{ij}q^{[h-1]}=\delta_{ij}X_i,
 \qquad R_{ij}=p_i s_j,
 \qquad \alpha\ne0.                                    \tag{1}
\]

There are two structural conclusions.

First, a nonlinear parametrization inside one residual physical-star fibre
does not produce nonlinear freedom in (1). If \(d\) is supported on one
physical star, then \(d^{[2]}=0\), and hence

\[
                 (q+d)^{[m]}=q^{[m]}+d q^{[m-1]}        \tag{2}
\]

for every \(m\geq1\). With the direct block and the selected stars fixed,
the replacement \(q\mapsto q+d\) preserves all nine rows if and only if

\[
 \boxed{
 \begin{aligned}
 R_{ij}d q^{[h-2]}&=0 &&((i,j)\ne(a,a)),\\
 \alpha d q^{[h-1]}+R_{aa}d q^{[h-2]}&=0.&&
 \end{aligned}}                                         \tag{3}
\]

It preserves the top tensor as well if and only if

\[
 d q^{[h-1]}=0,
 \qquad R_{ij}d q^{[h-2]}=0\quad(0\leq i,j\leq2).       \tag{4}
\]

Thus every fixed-star, top-preserving, one-star replacement lies in one
literal linear kernel. An arbitrary polynomial, rational, or analytic
choice of parameters in that star does not enlarge it.

Second, at \(h=3\) the known exact-cancellation \(7/9\) guard has a sharper
conservation law. In its full anchor-preserving support stratum, including
arbitrary reweighting and a two-dimensional nonlinear motion of the
selected \(p_a\)-star, the omitted selected-cross row is a nonzero scalar
multiple of the common \(bb\)-carrier:

\[
 \boxed{
 PTS\,[Y]R_{ac}q^{[2]}
       =Du\,[X_b]R_{bb}\Theta_a.}                        \tag{5}
\]

Here \(Y=X_{ccbbcb}\). The restored \(cc\)-row makes \(D,u\ne0\), while
the retained anchors and goodness make \(P,T,S\ne0\). Consequently

\[
 \boxed{R_{ac}q^{[2]}=0
          \quad\Longleftrightarrow\quad
        [X_b]R_{bb}\Theta_a=0}                           \tag{6}
\]

inside this fibre. The known nonzero exact-cancellation carrier therefore
cannot coexist with the restored selected-cross row. This is not a
rank/determinant assertion and does not cancel a matching power; both sides
of (5) are singleton physical coefficient fibres.

The boundary is sharp. A literal selected-star rewrite repairs the cross
row, keeps four mutual coordinate anchors and the aligned marked curvature,
and satisfies eight of the nine rows. It kills the common carrier and still
has exceptional residual \(0-X_a\). There is also a genuinely nonlinear
one-parameter family with exactly these eight rows. No member is an exact
source, because the exceptional row is not a target declaration: its
physical left side is literally zero.

The exceptional failure cannot be repaired inside a top-preserving star
fibre. More generally, while \(q\) has no all-\(a\) residual cell and
\(R_{aa}\) has no residual \(a\)-endpoint, every repair of the \(aa\)-row
must add an all-\(a\) perfect matching. It therefore changes \(q^{[h]}\),
and the new all-\(a\) support has star-cover number at least \(h\). For the
six-site guard, a genuine nine-row escape is necessarily cubic and cannot
be confined to fewer than three residual star centres.

This gives a rigorous obstruction to the proposed nonlinear
anchor-preserving deformation in the natural fixed-star/support fibre. It
does not obstruct a top-changing, multi-star replacement which leaves that
fibre, and it is not a proof of Krenn's conjecture.

## 2. One-star nonlinear deformations linearize exactly

Let \({\cal A}_W\) be the site-square-zero algebra. If every cell of \(d\)
meets one fixed physical site \(v\), then the product of any two cells of
\(d\) repeats \(v\). Therefore

\[
                              d^{[2]}=0.                 \tag{7}
\]

The divided-power binomial formula immediately gives (2). Subtract the
old rows (1) from the rows with \(q+d\). For a nonexceptional ordered
pair one gets

\[
 R_{ij}\bigl((q+d)^{[h-1]}-q^{[h-1]}\bigr)
                    =R_{ij}d q^{[h-2]}.                 \tag{8}
\]

For the exceptional pair one gets

\[
 \begin{aligned}
 &\alpha\bigl((q+d)^{[h]}-q^{[h]}\bigr)
  +R_{aa}\bigl((q+d)^{[h-1]}-q^{[h-1]}\bigr)\\
 &\hspace{35mm}=\alpha d q^{[h-1]}+R_{aa}d q^{[h-2]}.
 \end{aligned}                                         \tag{9}
\]

This proves (3), both necessity and sufficiency. Top preservation is
exactly \(d q^{[h-1]}=0\); substituting it into (9) proves (4).

This is stronger than a tangent calculation. Let
\(d=d(t_1,\ldots,t_r)\) be any nonlinear map into the same physical-star
space. Equation (7) holds for its total value at every parameter point, so
(2)--(4) are exact finite identities. Higher powers of the parameters
cannot provide a hidden correction.

Anchor preservation is also linear for a mutual anchor whose unique edge
lies outside \(q\), as for the four selected-star anchors below. An internal
direction is then anchor-safe precisely when it has no cell incident to the
residual anchor coordinate. Intersecting those coordinate hyperplanes with
(4) gives the exact top-preserving kernel preserving those fixed anchors.
For an anchor carried by an internal cell of \(q\), rescaling that same
cell is an additional open possibility and is not classified by this
sentence. No support-decreasing vector is asserted.

The common carrier has an equally explicit finite update. Recall

\[
 H_a(q)=\sum_{\ell=0}^{h-2}{1\over\ell+1}
       \alpha^{h-2-\ell}q^{[h-2-\ell]}R_{aa}^{[\ell]},
 \qquad \Theta_a=R_{aa}H_a.                             \tag{10}
\]

Equation (2), term by term, gives

\[
 \boxed{
 H_a(q+d)-H_a(q)=dJ_a,\qquad
 J_a=\sum_{\ell=0}^{h-3}{1\over\ell+1}
       \alpha^{h-2-\ell}q^{[h-3-\ell]}R_{aa}^{[\ell]}.} \tag{11}
\]

Hence

\[
                         \Delta\Theta_a=R_{aa}dJ_a.     \tag{12}
\]

For a marked oriented internal cell \(e\), with

\[
             \kappa_e^{\rightarrow}=\alpha q_e
                         -(R_{aa}^{\rightarrow})_e,     \tag{13}
\]

the fixed-star deformation changes its curvature by exactly
\(\alpha d_e\). In particular a deformation avoiding \(e\) preserves the
marked curvature literally. Equations (11)--(13) track the common carrier
and the marked orientation separately; one may vanish without the other.

## 3. The complete anchor-preserving support fibre at six sites

Set \(h=3\), \(\alpha=1\), use residual sites \(0,\ldots,5\), and let
\(\{a,b,c\}\) be the three labels. Write
\(e^d_{rs}=x_r^dx_s^d\). Consider the whole coefficient family

\[
 \begin{aligned}
 q={}&x e^b_{23}+y e^b_{45}+z e^b_{34}+w e^b_{25}
                   +u e^c_{14}+v e^c_{35},\\
 p_a={}&A x_3^b+B x_5^b,&s_a={}&Sx_4^b,\\
 p_b={}&P x_0^b,&s_b={}&Tx_1^b,\\
 p_c={}&C x_2^c,&s_c={}&Dx_0^c.
 \end{aligned}                                         \tag{14}
\]

Assume \(P,T,C,D,S,u,v\ne0\) and \((A,B)\ne(0,0)\). Both endpoint star
triples are then linearly independent. The following four cells are
mutual coordinate anchors throughout the family:

\[
 (p,b)\!-\!(0,b),\quad(q,b)\!-\!(1,b),\quad
 (p,c)\!-\!(2,c),\quad(q,c)\!-\!(0,c).                  \tag{15}
\]

Each displayed selected coordinate has only its displayed star cell, and
the residual coordinate at the other end occurs in no internal or
opposite-star cell. The new \(Bx_5^b\) component does not meet these four
coordinate channels.

Put \(R_{ij}=p_i s_j\). Direct physical matching expansion gives the
complete nine-row table

\[
\boxed{
\begin{array}{c|ccc}
 &a&b&c\\ \hline
a&0&0&Du(Aw+Bx)Y\\
b&0&PT(xy+zw)X_b&0\\
c&0&0&CDuvX_c.
\end{array}}                                             \tag{16}
\]

There are no suppressed mixed terms in (16). After the \(ac\)-cap uses
\(x_3^b x_0^c\), the unique completion of \(Y\) is
\(e^c_{14}e^b_{25}\), of weight \(uw\). After it uses
\(x_5^b x_0^c\), the unique completion is
\(e^c_{14}e^b_{23}\), of weight \(ux\). These are the two terms in the
same literal coefficient fibre \(Du(Aw+Bx)Y\).

The \(bb\)-row has the two physical completions \(23|45\) and \(34|25\),
while the \(cc\)-row has the unique completion \(14|35\). Every other
off-diagonal complement either contains site \(0\), where \(q\) has no
cell, or has no two-cell matching. Finally \(q^{[3]}=0\) because \(q\)
has no cell at site \(0\), and \(R_{aa}q^{[2]}=0\) because every cell of
\(R_{aa}\) meets site \(4\) and its complement still contains site \(0\).
This proves all of (16) without termwise reasoning in a multi-term zero
fibre.

The two restored complementary targets are exactly

\[
                         PT(xy+zw)=1,\qquad CDuv=1.      \tag{17}
\]

They may be imposed along an arbitrary nonlinear coefficient path.

## 4. Cross/carrier conservation and marked curvature

In (14),

\[
 R_{aa}=S(Ae^b_{34}+Be^b_{54}),\qquad R_{aa}^{[2]}=0.   \tag{18}
\]

Therefore the cubic full-normal carrier and first comparison are

\[
 H_a=q+\tfrac12R_{aa},\qquad
 \Theta_a=R_{aa}H_a=R_{aa}q.                            \tag{19}
\]

The \(bb\)-restriction again has two singleton placements:

\[
 \boxed{R_{bb}\Theta_a=PTS(Aw+Bx)X_b.}                 \tag{20}
\]

Comparing (20) with the \(ac\)-entry of (16) proves (5). Under (17), all
four scalar factors in that comparison are nonzero. This proves (6).

The marked \(34\)-orientation is

\[
                         \kappa_{34}^{\rightarrow}=z-AS. \tag{21}
\]

Thus the aligned exact-cancellation condition \(z=AS\) is independent of
the conservation factor \(Aw+Bx\). One may keep (21) equal to zero while
cancelling \(Aw+Bx\); what disappears is the total common carrier, by
cancellation against the new \(54\)-path. The marked orientation itself
does not become curved.

Equation (6) therefore does not say that the restored cross row forces
nonzero marked curvature. It says the opposite sharp thing in this fibre:
restoring that row kills the nonzero carrier which made the aligned marked
edge relevant.

## 5. The guard, its sharp repair, and a genuinely nonlinear boundary family

The \(7/9\) guard is the specialization

\[
 \begin{gathered}
 x=2,\quad y=w=u=v=P=T=C=D=A=1,\\
 z=-1,\quad S=-1,\quad B=0.                             \tag{22}
 \end{gathered}
\]

Equations (16)--(21) give

\[
 R_{bb}q^{[2]}=X_b,\quad R_{cc}q^{[2]}=X_c,\quad
 [Y]R_{ac}q^{[2]}=1,\quad R_{bb}\Theta_a=-X_b,\quad
 \kappa_{34}^{\rightarrow}=0.                           \tag{23}
\]

The other five off-diagonal rows vanish and the exceptional row is zero.
Along \(q_t=q+tR_{aa}\), the \(bb\)-value changes from \(X_b\) to zero,
whereas the \(cc\)-value remains \(X_c\). This is precisely the known
nonzero exact-cancellation carrier.

Now retain every coefficient in (22) except set

\[
                              B=-\tfrac12.               \tag{24}
\]

Then \(Aw+Bx=0\). The selected-cross row is repaired and all other
nonexceptional rows remain exact, but (20) becomes zero. The four anchors,
both good star triples, and the marked equality \(z=AS=-1\) remain
unchanged. The sole tensor residual is now

\[
                              0-X_a.                     \tag{25}
\]

This is a literal physical \(8/9\) packet, not an exact source.

There is genuine nonlinear freedom inside this sharp boundary. Over the
function field in \(t\), or at any specialization with \(1+t^2\ne0\), take

\[
 \begin{aligned}
 x&=2,&w=u=v=P=T=C=D&=1,&S&=-1,\\
 A&=1+t^2,&B&=-\frac{1+t^2}{2},\\
 z&=-(1+t^2),&y&=1+\frac{t^2}{2}.
 \end{aligned}                                         \tag{26}
\]

Then

\[
 xy+zw=1,\qquad CDuv=1,\qquad Aw+Bx=0,\qquad z-AS=0.    \tag{27}
\]

Consequently all eight nonexceptional rows, the four anchors, goodness,
and the aligned marked curvature are preserved along a coefficient family
with nonzero second finite difference. Yet

\[
 q_t^{[3]}=0,\qquad R_{aa}(t)q_t^{[2]}=0,\qquad
 R_{bb}\Theta_a(t)=0.                                  \tag{28}
\]

Thus nonlinearity by itself neither restores the exceptional target nor
retains the carrier. Family (26) is a sharpness witness for the
conservation law, not a curve of exact sources.

## 6. The exceptional colour-degree barrier

The obstruction to the ninth row is uniform. Suppose \(q\) contains no
all-\(a\) residual cell and \(R_{aa}\) has no \(a\)-coloured residual
endpoint. Let \(z=q+d\), and let \(d_a\) be the all-\(a\) projection of
\(d\). Pure-colour projection is an algebra homomorphism, so

\[
 \boxed{
 [X_a]\bigl(\alpha z^{[h]}+R_{aa}z^{[h-1]}\bigr)
                 =\alpha[X_a]d_a^{[h]}.}                \tag{29}
\]

The response term cannot contribute: its residual endpoints already have
colours different from \(a\). Therefore the exceptional target row forces

\[
                         [X_a]d_a^{[h]}=\alpha^{-1}\ne0. \tag{30}
\]

Expanding the finite sum in (30), at least one all-\(a\) perfect matching
in the support of \(d\) has nonzero product. This conclusion is
cancellation-safe: it uses only that a finite sum is nonzero, not that the
other summands vanish.

Two consequences are immediate.

1. Since the old top has zero \(X_a\)-coefficient, every such repair
   changes \(q^{[h]}\). It cannot satisfy the top-preserving replacement
   condition.
2. If \(d\) is supported on a union of \(k<h\) residual physical stars,
   (30) is impossible. Every edge of a putative perfect matching must meet
   one of the \(k\) star centres, and its \(h\) disjoint edges would require
   \(h\) distinct centres. Equivalently, the all-\(a\) repair support has
   vertex-cover (star-cover) number at least \(h\).

For the guard, \(h=3\). A fixed-star repair of (25) must therefore add
three disjoint all-\(a\) cells and changes top degree through a cubic
perturbation term. A one-star or two-star nonlinear deformation cannot do
it. The four anchors in (15) use residual \(b/c\)-coordinates, so adding
all-\(a\) cells does not automatically destroy them. Anchor persistence is
therefore not the remaining obstruction; simultaneous control of the new
mixed top and adjacent-power fibres is.

## 7. Exact boundary and residual dependency

The proved negative boundary is

\[
 \boxed{
 \begin{gathered}
 \text{fixed direct block and selected stars}
 +\text{ one residual star fibre}
 +\text{ top preservation}\\
 \Longrightarrow\text{the linear kernel (4), with no nonlinear escape},\\[1mm]
 \text{displayed anchor-preserving cancellation support}
 +\text{ restored }cc+ac\\
 \Longrightarrow [X_b]R_{bb}\Theta_a=0,\\[1mm]
 \text{exceptional }aa\text{ repair in the same residual-colour sector}
 \Longrightarrow\text{top change across at least }h\text{ stars}.
 \end{gathered}}                                        \tag{31}
\]

This does not classify arbitrary coordinated changes of \(q,p_i,s_j\), and
does not rule out a deformation which introduces new support outside (14).
The exact residual may be named the **top-changing multi-star nine-row
extension problem**:

> Add an all-\(a\) perfect matching (or permit \(R_{aa}\) to acquire an
> \(a\)-near-perfect channel), add a second physical completion of the
> \(Y\)-fibre or otherwise leave the conservation stratum, and satisfy all
> nine tensor rows while preserving the four split anchors and transporting
> a nonzero common carrier or a relocated marked curvature class.

Such a replacement must be checked with the general nine-row difference
system, not only with \(z^{[h]}=q^{[h]}\). In the fixed-star case that
system is

\[
 \begin{aligned}
 R_{ij}\bigl(z^{[h-1]}-q^{[h-1]}\bigr)&=0
                                      &&((i,j)\ne(a,a)),\\
 \alpha\bigl(z^{[h]}-q^{[h]}\bigr)
 +R_{aa}\bigl(z^{[h-1]}-q^{[h-1]}\bigr)&=0.             \tag{32}
\end{aligned}
\]

This is structurally the same general nine-row difference-system interface
already isolated for replacements in the binary residual-target branch:
both allow the exceptional row to trade a top change against an
adjacent-power change. Neither problem reduces to the other, because the
present boundary also retains a marked common carrier and a selected-cross
singleton fibre, while the binary branch imposes its own target-support
and Hamilton ledger. A common top-changing replacement lemma could address
both interfaces, but none is proved here.

No solution of this residual problem is constructed here. In particular,
the note supplies neither a same-order exact descendant nor an active clean
cap.

The dependency-free checker
[verify_scalar_unit_nine_row_star_fibre_carrier_conservation_boundary.py](../computations/verify_scalar_unit_nine_row_star_fibre_carrier_conservation_boundary.py)
audits the full coefficient table (16), the conservation identity (5), the
four anchors, both star ranks, the marked orientation, the original and
repaired guards, the nonlinear family (26), the exact one-star formulas
(2)--(4), the carrier update (11), and the sharp \(h\)-star perfect-matching
threshold. It uses exact rational arithmetic, explicit runtime failures,
and runs unchanged under optimized Python.
