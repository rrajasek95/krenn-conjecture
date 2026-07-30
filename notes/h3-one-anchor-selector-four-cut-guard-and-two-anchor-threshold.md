# One diagonal four-cut anchor does not lower the residual cubic rank

## 1. Outcome

At the first boundary \(h=3\), a literal diagonal target coefficient does
not by itself lower the selector--Macaulay image in

\[
 Q_f=\operatorname {Sym}^5\mathbb C^2/
             f\operatorname {Sym}^2\mathbb C^2.                \tag{1}
\]

There is a fixed six-site source packet with the following simultaneous
properties.

1. All six off-diagonal physical pair rows hold.
2. The complete \(00\) diagonal tensor row is exactly \(X_0\), not merely
   one scalar specialization of that row.
3. Both endpoint stars have disjoint three-site selectors.  More strongly,
   both selectors use the same literal physical colour \(0\), and their
   selector covectors annihilate the opposite star.
4. A cut through two of the first selector sites retains the literal
   coefficient \(vX_0^D\) in the four-cut row (24) of
   curved-no-root-macaulay-and-scalar-zero-packet.md.
5. On the canonical line \(K(u,v)=uE_{01}+vI\), the clean-error coordinates
   contain \(6u^3\), while an exposed coordinate \(f\) is nonzero at the
   scalar-zero point \([0:1]\).  Hence \(6u^3\operatorname {Sym}^2\) maps
   isomorphically onto \(Q_f\), whose dimension is three.

Thus the proposed bound

\[
 \operatorname {rank}\bigl(L'\operatorname {Sym}^2\longrightarrow
 Q_f\bigr)\le2                                               \tag{2}
\]

is false with only one diagonal anchor, even after granting a much stronger
selector alignment than Hall--Rado supplies.  The packet fails exactly the
two complementary diagonal rows \(X_1,X_2\), so it is not a ternary source.

The exact local **flag-alignment** threshold is also sharper than “add
another anchor.”  Two differently labelled transported anchors fix two
common coordinate axes, but leave a relative diagonal gauge.  That gauge
can still give nonzero flag drift in the crossed cell.  The smallest
plausible next input is therefore

\[
 \boxed{\text{two differently labelled diagonal coefficients, their
 crossed target-zero coefficient, and faithful literal overlap transport.}}
                                                                  \tag{3}
\]

The two anchors fix the two-label axes, but a crossed target-zero equation is
itself invariant under relative rescaling.  The crossed row and faithful
transport are therefore a proposed mechanism for controlling that scale and
identifying the normalized cofactor with the physical one; their sufficiency
is not proved here.  No full descent or proof of the conjecture is claimed.

## 2. The fixed packet

Work in the site-square-zero algebra on

\[
 W=\{A_0,A_1,A_2,B_0,B_1,B_2\},
 \qquad V_x=\operatorname {span}\{e_0^{(x)},e_1^{(x)},e_2^{(x)}\}.
                                                                  \tag{4}
\]

For brevity write

\[
 (xy)_c=e_c^{(x)}e_c^{(y)}.
\]

Take the internal quadratic

\[
 q=(B_0B_1)_0+(A_2B_2)_0                                  \tag{5}
\]

and endpoint stars

\[
\begin{aligned}
 p_0&=e_0^{(A_0)}+e_1^{(A_1)}+e_1^{(A_2)},&
 p_1&=e_0^{(A_2)},&
 p_2&=e_0^{(B_1)},\\
 s_0&=e_0^{(A_1)},&
 s_1&=e_0^{(B_0)}+e_1^{(B_0)}
       +e_1^{(B_1)}+e_1^{(B_2)},&
 s_2&=e_0^{(B_2)}.
                                                               \tag{6}
\end{aligned}
\]

Let the direct matrix have the sole nonzero entry

\[
                              a_{01}=1.                         \tag{7}
\]

Every object in (5)--(7) is a fixed physical block coefficient; no scalar
edge is assigned independently along the later probe line.

The two summands of \(q\) are disjoint, so

\[
 q^{[2]}=(B_0B_1)_0(A_2B_2)_0,
 \qquad q^{[3]}=0.                                            \tag{8}
\]

The support of \(q^{[2]}\) leaves precisely \(A_0,A_1\).  Among all
products \(p_i s_j\), the only one having components on these two sites in
distinct slots is \(p_0s_0\), and its unique surviving component is

\[
                 e_0^{(A_0)}e_0^{(A_1)}.
\]

Consequently

\[
 \boxed{
 a_{ij}q^{[3]}+p_i s_jq^{[2]}
 =\begin{cases}
 X_0,&(i,j)=(0,0),\\
 0,&(i,j)\ne(0,0).
 \end{cases}}                                                \tag{9}
\]

In particular (9) is every one of the six off-diagonal equations and the
complete \(00\) diagonal equation.  Its only discrepancies from the
full-nine system are

\[
                              0=X_1,\qquad 0=X_2.               \tag{10}
\]

## 3. The selectors are already diagonal-compatible

For the first endpoint, apply the literal colour-zero covectors at the
three sites \(A_0,A_2,B_1\).  Their pullbacks to the row-index space are

\[
 \begin{array}{c|ccc}
       &p_0&p_1&p_2\\ \hline
 (e_0^{(A_0)})^*&1&0&0\\
 (e_0^{(A_2)})^*&0&1&0\\
 (e_0^{(B_1)})^*&0&0&1.
 \end{array}                                                  \tag{11}
\]

For the second endpoint, the same colour-zero covectors at
\(A_1,B_0,B_2\) give

\[
 \begin{array}{c|ccc}
       &s_0&s_1&s_2\\ \hline
 (e_0^{(A_1)})^*&1&0&0\\
 (e_0^{(B_0)})^*&0&1&0\\
 (e_0^{(B_2)})^*&0&0&1.
 \end{array}                                                  \tag{12}
\]

The two site sets in (11)--(12) are disjoint.  Moreover every covector in
(11) kills all three \(s\)-rows at its site, and every covector in (12)
kills all three \(p\)-rows: the only potentially overlapping components
are \(s_1|_{B_1}=e_1^{(B_1)}\) and
\(p_0|_{A_1}=e_1^{(A_1)}\), both killed by \(e_0^*\).

Thus the guard does not use an oblique selector escape.  It has a literal
monochromatic separating selector partition.  Notice, however, that this
is a coefficient statement on the constant-zero word, not a mixed-word
probe: the \(X_0\) target is deliberately visible there.

## 4. The canonical line is rootless and fills \(Q_f\)

Put

\[
 K(u,v)=uE_{01}+vI,\qquad
 \sigma(K)=u,\qquad
 r(K)=up_0s_1+v(p_0s_0+p_1s_1+p_2s_2).                       \tag{13}
\]

Using the prescribed ternary target

\[
 T(K)=v(X_0+X_1+X_2),
\]

define the same cubic clean error as on a genuine canonical line,

\[
 {\cal E}(u,v)=(uq+r(K))^{[3]}-u^2v(X_0+X_1+X_2).              \tag{14}
\]

Consider the mixed word

\[
 Y=e_0^{(A_0)}e_1^{(A_1)}e_1^{(A_2)}
     e_1^{(B_0)}e_1^{(B_1)}e_1^{(B_2)}.                       \tag{15}
\]

The only contribution to this word is the cube of \(up_0s_1\).  Both
edges of \(q\) have colour zero at sites on which \(Y\) has colour one, and
the target term is pure.  The rank-one cross response has \(3!\) perfect
matchings, so

\[
                              [Y]{\cal E}=6u^3.                 \tag{16}
\]

At the scalar-zero point \([u:v]=[0:1]\), put

\[
                         R=p_0s_0+p_1s_1+p_2s_2.
\]

The all-zero word has the unique response matching

\[
 (A_0A_1)_0\mid(A_2B_0)_0\mid(B_1B_2)_0,                    \tag{17}
\]

using respectively \(p_0s_0,p_1s_1,p_2s_2\).  Hence

\[
                    [X_0]{\cal E}(0,1)=[X_0]R^{[3]}=1.        \tag{18}
\]

Let

\[
                  f(u,v)=[X_0]{\cal E}(u,v).
\]

In fact the only other all-zero matching is the \(u^2v\) matching
\[
 (B_0B_1)_0\mid(A_2B_2)_0\mid(A_0A_1)_0,
\]
and it is exactly cancelled by the \(u^2vX_0\) target term in (14).
Consequently
\[
                              f(u,v)=v^3.                       \tag{18a}
\]
In particular \(f(0,1)=1\), and therefore

\[
                         \gcd(f,u^3)=1.                        \tag{19}
\]

The scalar coordinate \(f\) is selector-exposed: already at \(A_0\), the
local \(X_0\)-axis is the selected \(p_0\)-axis.  Choose a scalar-coordinate
basis beginning with \(f\), and put \(6u^3\) into the complementary span
\(L'\).  If

\[
                       u^3h=fk,\qquad h,k\in S_2,
\]

then (19) gives \(f\mid h\), which is impossible unless \(h=k=0\), since
\(\deg h<\deg f\).  Thus

\[
 u^3S_2\ \cap\ fS_2=0.                                      \tag{20}
\]

Both summands have dimension three inside the six-dimensional space
\(S_5\).  Consequently

\[
                fS_2\oplus u^3S_2=S_5,                        \tag{21}
\]

and multiplication by the single remaining coordinate \(6u^3\) induces
an isomorphism

\[
                  S_2\xrightarrow{\ \sim\ }Q_f.              \tag{22}
\]

This also makes the nonreduced-divisor interpretation explicit.  The
divisor \(V(f)=V(v^3)\) is the length-three point \([1:0]\).  On the chart
\(u\ne0\), with \(t=v/u\), the three shifts of \(u^3\) become
\[
                              1,\quad t,\quad t^2
\]
modulo \(t^3\).  They fill all principal parts at that point.  Therefore
none of evaluation, first derivative, or second divided derivative gives a
nonzero functional on \(Q_f\) annihilating the residual image.

This is the desired decisive failure of (2): the residual image has rank
three, not at most two.  Equivalently, the clean coordinates are coprime,
as witnessed already by \(f\) and \(6u^3\).

## 5. The literal diagonal coefficient survives a selector cut

Cut at

\[
                         x=A_0,\qquad y=A_2,
\]

and select physical colour zero at both sites.  These are the first two
rows of the monochromatic selector (11); its third row at \(B_1\) remains
in the four-site complement

\[
                         D=\{A_1,B_0,B_1,B_2\}.                \tag{23}
\]

In the notation of the audited four-cut formulas (24)--(26), write

\[
 z=(B_0B_1)_0,\qquad \nu=e_0^{(B_2)}.
\]

For the selected \(00\) coefficient of \(q\), one has

\[
                 t_0=0,\qquad v_0=\nu,\qquad U_{00}=0.         \tag{24}
\]

For \(F=uq+r(K)\), the selected coefficient at \(x\) is

\[
 L_0=u\,s_1|_D+v e_0^{(A_1)},                                 \tag{25}
\]

and the double coefficient is \(M_{00}=0\).  Substitution into the
physical row (24) of the four-cut ledger leaves

\[
                         P_{00}=L_0\nu z.                      \tag{26}
\]

Every component of \(s_1|_D\) is supported at \(B_0,B_1\), or \(B_2\), so
it collides with \(\nu z\).  The other summand gives

\[
 \boxed{P_{00}=v\,e_0^{(A_1)}e_0^{(B_0)}
                   e_0^{(B_1)}e_0^{(B_2)}=vX_0^D.}            \tag{27}
\]

This is exactly the literal diagonal target coefficient
\(\kappa_0(K)X_0^D\), since \(\kappa_0(K)=K_{00}=v\).  Thus the failure of
the rank bound cannot be attributed to losing the anchor during the cut,
using different selector colours, or placing the third selector direction
on the cut.  The target cancels in
\(\epsilon_{00}=C_{00}-u^2P_{00}\), but (27) creates no relation on the
independent coordinate (16).

## 6. What selector incidence is actually required

For an endpoint star \(P:\mathbb C^3\to\bigoplus_xV_x\), define the
fixed-colour row matroid by

\[
 \rho_x^{(c)}=(e_c^{(x)})^*P_x\in(\mathbb C^3)^*.              \tag{28}
\]

Hall--Rado supplies distinct sites and arbitrary local covectors whose
pullbacks are independent.  A literal coefficient of \(X_c\), however,
forces the covector \((e_c^{(x)})^*\) at every selected site.  Therefore a
three-site selector compatible with one literal diagonal word requires
the additional incidence

\[
 \exists c,\ x_0,x_1,x_2\text{ distinct}:\qquad
       \rho_{x_0}^{(c)}\wedge\rho_{x_1}^{(c)}
             \wedge\rho_{x_2}^{(c)}\ne0.                      \tag{29}
\]

For a two-site cut it is enough to require rank two on the cut and a third
independent fixed-colour row on its complement.  Neither injectivity nor
the arbitrary-covector Hall--Rado selector theorem implies (29).  For
example, placing \(p_i=e_i\) at three different sites gives an injective
star and an arbitrary-colour selector, but every fixed-colour family in
(28) has rank one.

The present guard satisfies the stronger condition (29) with \(c=0\), by
(11).  Hence (29) is a necessary routing hypothesis, not the missing
rank-loss mechanism.

For the mixed own-edge route, even (29) is not the complete incidence
ledger.  Put
\[
 L_x^P=\operatorname {im}(P_x^*:V_x^*\to(\mathbb C^3)^*),
 \qquad
 L_x^S=\operatorname {im}(S_x^*:V_x^*\to(\mathbb C^3)^*),
\]
and let \(\rho_P,\rho_S\) be the two Rado-matroid rank functions.  On the
six-site ground set, a partition into disjoint \(P\)- and \(S\)-selector
bases exists if and only if
\[
             \rho_P(A)+\rho_S(A)\ge |A|
             \qquad\text{for every }A\subseteq W.              \tag{29a}
\]
This is the matroid-union criterion; separate endpoint selectors do not
imply it.  After (29a), one still has to choose representatives which
annihilate the opposite star and lie on a mixed target-zero word.

Finally, if
\[
 \Phi:\text{probe space}\longrightarrow
       \mathbb C^{\binom62}\oplus\mathbb C^3,\qquad
 \Phi=(Q,G_0,G_1,G_2),
\]
then a pure own-edge lift at an edge \(e\) is exactly the column-membership
condition
\[
                  (\mathbf e_e,0,0,0)\in\operatorname {im}d\Phi. \tag{29b}
\]
Neither (29), (29a), nor a nonzero Hall permanent implies (29b).  Thus a
proof through the Riccati identity must establish (29a), shore separation,
and (29b), or state them as hypotheses.  The counterguard above grants
disjoint monochromatic shore-separated selectors, so its failure is not
caused by the first two gates; its constant-zero selector word is
deliberately outside the mixed own-edge chart.

## 7. Two anchors fix axes but not the crossed first jet

The next threshold can be stated without assuming selector alignment.
Let \(G,H\in\operatorname {GL}_3\) be the two selector matrices, and let
\(r\ne s\).  If the two transported target tensors

\[
 G^{-\mathsf T}E_{rr}H^{-1},\qquad
 G^{-\mathsf T}E_{ss}H^{-1}                                  \tag{30}
\]

are nonzero diagonal matrices, then each is rank one on one coordinate
axis.  Independence of the \(r,s\) columns of \(G^{-\mathsf T}\) and
\(H^{-\mathsf T}\) forces the two axes to be distinct.  Thus two anchors
recover a common fixed-coordinate two-label flag.  One anchor fixes only
one common axis and leaves an arbitrary oblique complementary two-plane.

Two anchors do not yet make that flag horizontal.  After the axes in (30)
have been relabelled, the exact one-parameter stabilizer

\[
\begin{aligned}
 G(t)&=\operatorname {diag}(g_r(t),g_s(t),1),\\
 H(t)&=\operatorname {diag}(g_r(t)^{-1},g_s(t)^{-1},1)
                                                               \tag{31}
\end{aligned}
\]

with (g_r(0)=g_s(0)=1),

fixes both \(E_{rr}\) and \(E_{ss}\) under the action in (30).  But it sends
the crossed matrix unit to

\[
           G(t)^{-\mathsf T}E_{rs}H(t)^{-1}
              ={g_s(t)\over g_r(t)}E_{rs}.                     \tag{32}
\]

Infinitesimally, if
\(\lambda_r=g_r'(0)/g_r(0)\) and
\(\lambda_s=g_s'(0)/g_s(0)\), then for a direct crossed entry
\(a_{rs}=\alpha\ne0\),

\[
                      \xi C_{rs}=\alpha(\lambda_s-\lambda_r).  \tag{33}
\]

This can be arbitrary while both diagonal anchors remain fixed.  In the
Riccati--leakage identity

\[
                   \Lambda_{rs}=F(\alpha^2-\xi C_{rs}),        \tag{34}
\]

the anchors alone therefore do not imply \(\xi C_{rs}=0\).  Nor do they
identify the normalized cofactor with the literal physical cofactor, so
they do not imply \(\Lambda_{rs}=0\).

Equation (32) identifies the missing label coupling exactly, but a zero target
row remains zero under the relative character \(g_s/g_r\).  Consequently a
coefficient of a crossed target-zero row can control that character only
through additional faithful physical overlap information.  The overlap
equation must be injective on the relevant source-provenant correction module
to identify normalized and physical cofactors.  Merely knowing that a common
power is nonzero is insufficient in the site-square-zero algebra.

Accordingly, two differently labelled anchors are the threshold for
partial flag alignment, but the next defensible exactness target is the
three-row packet

\[
        (r,r;r,r),\qquad(s,s;s,s),\qquad(r,r;s,s),              \tag{35}
\]

or its endpoint-transposed version, retained before the common power is
discarded.  The third entry is a four-index coefficient row, not literally
the endpoint matrix unit (E_{rs}) in (32).  It is precisely the pattern
which drives the audited two-dark-colour four-cut obstruction under its
stronger coefficient-dark hypotheses.  What remains open is to construct
from (35), on the active selector-overlap chart, either

* an actual evaluation/jet functional on \(Q_f\) supported on \(V(f)\), or
* simultaneous equations \(\xi C_{rs}=\Lambda_{rs}=0\).

An abstract rank bound on \(Q_f\) would only restate the common-root claim;
the source-provenant functional or the crossed first-jet equations are the
genuinely new content still required.

The dependency-free checker
[verify_h3_one_anchor_selector_four_cut_guard.py](../computations/verify_h3_one_anchor_selector_four_cut_guard.py)
enumerates the pair rows and all \(3^6\) clean coordinates, verifies both
selector matrices, and checks (16), (18a), and (27) over the integers.
