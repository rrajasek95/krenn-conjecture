# Adaptive diagonal directions remove every non-intrinsic collision

## 1. Outcome

Fix \(h\ge3\), work over a characteristic-zero field, and retain the
endpoint ordering of a physical pair block \(A=A_{pq}=(a_{ij})\).  Select

\[
                         \alpha=a_{aa}\ne0,
\]

and write \(\{a,b,c\}=\{0,1,2\}\).  For a literal contraction matrix
\(L\), use

\[
 \sigma(L)=\sum_{i,j}L_{ij}a_{ij},\qquad
 T(L)=\sum_iL_{ii}X_i.                                      \tag{1}
\]

Suppose that \(D\) satisfies

\[
 D_{aa}=0,\qquad d_b:=D_{bb}\ne0,\qquad d_c:=D_{cc}\ne0,
 \qquad \gamma:=\sigma(D)\ne0.                              \tag{2}
\]

Put

\[
 K_0=E_{aa},\qquad K_1=\gamma E_{aa}-\alpha D,\qquad
 K_2=K_1-\gamma K_0=-\alpha D.                              \tag{3}
\]

Then \(K_1\) is scalar-zero, and the physical activity polynomial of
\(K(t,u)=tK_0+uK_1\) is

\[
 \boxed{\operatorname {Act}(t,u)
   =\alpha^3d_bd_c\,t u^2(t+\gamma u).}                      \tag{4}
\]

Thus (2) gives three distinct reduced inactive boundary points and has no
collision stratum.  If \(\rho_i\) denotes the ordinary odd cap residue of
\(K_i\), the two normalized boundary jets are

\[
 \boxed{Z_1=\gamma\rho_0+\rho_2,\qquad
        Z_2=-\gamma\rho_0+(h-1)\rho_2.}                      \tag{5}
\]

Their coefficient determinant is \(h\gamma\ne0\), with inverse

\[
 \rho_2={Z_1+Z_2\over h},\qquad
 \rho_0={(h-1)Z_1-Z_2\over h\gamma}.                        \tag{6}
\]

Each jet separately sees every surviving physical label, and both jets
have division-free literal full-nine representatives.  The symmetric and
chartwise coefficient-routing certificates also carry over with
\(t+\gamma u\) as the third boundary factor.

There is an exact direction-selection criterion:

\[
 \boxed{\text{A matrix \(D\) satisfying (2) exists}
 \iff A\ne\alpha E_{aa}.}                                   \tag{7}
\]

Equivalently, this is exactly the criterion for the existence of a
scalar-zero cap \(K_*\in\ker\sigma\) whose three diagonal entries are all
nonzero.  For the displayed construction one may take \(K_*=K_1\).

This includes an extra entry in either endpoint-ordered off-diagonal
orientation.  Hence the adaptive direction removes every non-intrinsic
diagonal collision.

One caveat is essential.  For non-diagonal \(D\), \(\det K(t,u)\) can
have an additional zero which is not an activity boundary.  The activity,
clean-root, coefficient-routing, cap-residue, and source-legality proofs
do not use matrix invertibility.  A downstream result which does require
\(K^{-1}\) cannot be imported without another hypothesis.

The intrinsic block \(A_{pq}=\alpha E_{aa}\) remains conjecture-level.
Neither the certified curvature selection nor the power-free overlap
identities currently force a replacement good chart.  Section 6 gives
the current global selection ledger and two sharp guards; it does not
claim an exact eight-site counterexample or an adaptive-\(D\)
curvature-transport theorem.

## 2. Existence and endpoint order

Let

\[
                  U_a=\{D\in\operatorname {Mat}_3:D_{aa}=0\}.
\]

The restriction of \(\sigma\) to \(U_a\) is nonzero exactly when some
\(a_{ij}\), \((i,j)\ne(a,a)\), is nonzero.  Over an infinite field, the
product

\[
                         D_{bb}D_{cc}\sigma(D)
\]

is then a nonzero polynomial on \(U_a\), so it is nonzero at some point.
This proves (7).

The equivalent scalar-zero-cap formulation follows in both directions.
The constructed

\[
                 K_1=\gamma E_{aa}-\alpha D
\]

lies in \(\ker\sigma\) and has diagonal
\((\gamma,-\alpha d_b,-\alpha d_c)\) in the \(a,b,c\) ordering.  Conversely,
if \(A=\alpha E_{aa}\), then \(\sigma(K)=\alpha K_{aa}\), so every
scalar-zero \(K\) has \(K_{aa}=0\) and cannot see all three target labels.

There is also a division-free explicit choice.  Start with
\(D_{bb}=D_{cc}=1\) and all other entries zero.

* If \(a_{bb}+a_{cc}\ne0\), stop.
* If \(a_{bb}+a_{cc}=0\) and \(a_{bb}\ne0\), replace
  \(D_{bb}=1\) by \(D_{bb}=2\); the new contraction is \(a_{bb}\).
* Otherwise \(a_{bb}=a_{cc}=0\).  Choose a nonzero off-diagonal
  \(a_{ij}\) and set \(D_{ij}=1\); the contraction is \(a_{ij}\).

The last step uses the same ordered cell.  If \(a_{ij}\ne0\) but
\(a_{ji}=0\), it is \(D_{ij}\), not \(D_{ji}\), which detects it.  An
arbitrary off-diagonal \(D\) is source-legal because it is simply a scalar
linear combination of the nine endpoint-ordered physical rows.

The old generic diagonal direction is recovered by

\[
                    D=I-E_{aa},\qquad
                    \gamma=\sigma(D)=\operatorname {tr}A-\alpha.
                                                                    \tag{8}
\]

The adaptive construction changes this direction only when the
contraction in (8) vanishes.

## 3. Activity and the determinant audit

Equations (1)--(3) give

\[
\begin{aligned}
 \sigma(K(t,u))&=\alpha t,\\
 T(K(t,u))&=(t+\gamma u)X_a
           -\alpha u(d_bX_b+d_cX_c).                         \tag{9}
\end{aligned}
\]

Physical activity is the product of the direct scalar and these three
fixed target coefficients, proving (4).  Its reduced boundary is

\[
\begin{array}{c|c|c|c}
 &\text{factor}&\text{matrix}&\text{inactive coordinate}\\ \hline
 P_0&u&K_0&b,c\text{ targets},\\
 P_1&t&K_1&\sigma(K_1)=0,\\
 P_2&t+\gamma u&K_2&a\text{ target}.
\end{array}                                                   \tag{10}
\]

At \(P_1\), all three target coefficients are nonzero.  At \(P_2\),
\(\sigma(K_2)=-\alpha\gamma\ne0\) and both complementary targets are
nonzero.  The multiplicity two of \(u\) records two missing targets at
\(K_0\), but gives only one reduced clean-error factor.

Off-diagonal entries of \(D\) do not occur in (9), but they do occur in
the ordinary matrix determinant.  Put

\[
 \delta=\det D_{\bar a,\bar a}
       =D_{bb}D_{cc}-D_{bc}D_{cb}.
\]

Changing only the \(aa\)-entry of \(-\alpha uD\) gives

\[
 \boxed{\det K(t,u)=\alpha^2u^2
   \bigl(\delta(t+\gamma u)-\alpha u\det D\bigr).}           \tag{11}
\]

When \(\delta\ne0\), the last linear factor is generally a fourth
projective point and may lie in the active locus.  It can also make
\(K_1\) singular while every diagonal target coefficient of \(K_1\) is
nonzero.  If \(\delta=\det D=0\), the whole pencil is matrix-singular.
None of these cases changes (4): the exact target is controlled by
\(\operatorname {diag}K\), not by \(\det K\).

The clean error remains a homogeneous tensor polynomial of degree \(h\).
In the all-inactive-clean branch every common root is one of (10).  An
additional determinant-zero point outside (10) is physically active, so it
is either dirty and irrelevant or clean and already supplies the desired
active clean cap.  A determinant root which coincides with (10), such as a
singular \(K_1\), is merely one of the existing inactive points.  Thus (11)
adds no clean-error/root-routing boundary.  It only forbids an unqualified
appeal to an invertible-cap lemma.

## 4. Cap residues, jets, and source legality

Write the normalized full-nine rows on the complement of \(p,q\) as

\[
 {\cal P}_{ij}=a_{ij}q+h p_i s_j,\qquad
 {\cal P}_{ij}q^{[h-1]}=h\delta_{ij}X_i.                     \tag{12}
\]

For any literal matrix \(L\), set

\[
 {\cal P}(L)=\sum_{i,j}L_{ij}{\cal P}_{ij}
             =\sigma(L)q+h r(L).
\]

Then

\[
                  {\cal P}(L)q^{[h-1]}=hT(L).               \tag{13}
\]

After exposing one residual site and passing to the standard odd quotient,
the corresponding coefficient of (13) gives

\[
                  \operatorname {CapRes}_i(L)
                         =L_{ii}\overline Y_i.                \tag{14}
\]

This holds for arbitrary off-diagonal entries of \(L\): their target in
(13) is zero, and the radial term dies in the quotient.  Therefore

\[
\begin{aligned}
 \rho_0&=(\overline Y_a,0,0),\\
 \rho_1&=(\gamma\overline Y_a,-\alpha d_b\overline Y_b,
                              -\alpha d_c\overline Y_c),\\
 \rho_2&=(0,-\alpha d_b\overline Y_b,
                              -\alpha d_c\overline Y_c),
                                                                  \tag{15}
\end{aligned}
\]

and \(\rho_1=\gamma\rho_0+\rho_2\).

The boundary-polar calculation uses only (9).  If
\(F=F(K_0)\), \(R=F(K_1)=r(K_1)\), and
\({\cal E}=\sum_jt^{h-j}u^jC_j\), then

\[
 RF^{[h-1]}-C_1
   =\alpha^{h-1}\bigl(\gamma X_a
          -\alpha(d_bX_b+d_cX_c)\bigr).                       \tag{16}
\]

Its normalized odd residue is \(Z_1=\rho_1\).  At \(P_2\), use
\(v=t+\gamma u,w=u\).  Then

\[
 s=\alpha(v-\gamma w),\qquad
 T=vX_a-\alpha w(d_bX_b+d_cX_c).                             \tag{17}
\]

Put \(G=F(K_2)\).  The target contribution to the coefficient of
\(vw^{h-1}\) is

\[
 Q_2=\alpha^{h-1}(-\gamma)^{h-2}
       \bigl(-\gamma X_a+(h-1)T(K_2)\bigr).                  \tag{17a}
\]

Thus the difference between \(FG^{[h-1]}\) and the corresponding clean
error coefficient is exactly \(Q_2\).  Dividing by the known nonzero scalar
\(\alpha^{h-1}(-\gamma)^{h-2}\)—which uses only
\(\alpha\ne0\) and \(s(K_2)=-\alpha\gamma\ne0\)—gives

\[
                         Z_2=-\gamma\rho_0+(h-1)\rho_2.       \tag{18}
\]

Equations (5)--(6) follow.  Componentwise,

\[
\begin{array}{c|cc}
 &i=a&i\in\{b,c\}\\ \hline
 Z_{1,i}/\overline Y_i&\gamma&-\alpha D_{ii}\\
 Z_{2,i}/\overline Y_i&-\gamma&-(h-1)\alpha D_{ii}.
\end{array}                                                   \tag{19}
\]

Every displayed scalar is nonzero, proving label visibility.

Both jets have literal representatives:

\[
 J_1=K_1=\gamma K_0+K_2,\qquad
 J_2=-\gamma K_0+(h-1)K_2.                                  \tag{20}
\]

Indeed, \(\operatorname {CapRes}(J_r)=Z_r\), and

\[
\begin{array}{c|c|c}
 &\sigma&T\\ \hline
 J_1&0&\gamma X_a-\alpha(d_bX_b+d_cX_c)\\
 J_2&-h\alpha\gamma&-\gamma X_a
                -(h-1)\alpha(d_bX_b+d_cX_c).
\end{array}                                                   \tag{21}
\]

Using an off-diagonal entry of \(D\) to make \(\gamma\ne0\) therefore
neither relabels (19) nor creates an untracked target.

## 5. Coefficient routing and its limitation

Let \(Z\subseteq\{0,1,2\}\) be the distinct clean boundary points and put

\[
 p_0=u,\qquad p_1=t,\qquad p_2=t+\gamma u,\qquad
 P_Z=\prod_{i\in Z}p_i,\qquad {\cal E}=P_Z\Omega_Z.           \tag{22}
\]

Assume that the line has a clean point and every clean point is inactive.
The active locus of (4) is nonempty, so \({\cal E}\not\equiv0\).  If
\(d=\deg\Omega_Z\), all common roots of its nonzero coordinates are among
the three points (10).  Hence their gcd is

\[
                  g=t^ru^s(t+\gamma u)^w,\qquad r+s+w\le d.
                                                                    \tag{23}
\]

After dividing by \(g\), the reduced coordinate degree is
\(e=d-r-s-w\), while the divided target
\(\bigl(tu(t+\gamma u)\bigr)^d/g\) has degree
\(3d-r-s-w\ge2e-1\).  The binary complete-intersection bound gives

\[
 \boxed{H\in V^*\otimes k[t,u]_{2d},\qquad
   \langle H,\Omega_Z\rangle
                  =\bigl(tu(t+\gamma u)\bigr)^d.}             \tag{24}
\]

The sharper chartwise version is unchanged.  In a chart containing a
clean boundary point, remove the full coordinate-gcd multiplicity of the
third boundary factor.  If the remaining vector \(\Xi\) has degree \(e\),
then

\[
 \boxed{H_{\rm sat}\in V^*\otimes k[x,y]_e,\qquad
                  \langle H_{\rm sat},\Xi\rangle=(xy)^e.}    \tag{25}
\]

If \(P_0\) or \(P_1\) is clean, take \((x,y)=(t,u)\), remove the full
\((t+\gamma u)\)-gcd multiplicity, and use the \(Z_1\) boundary channel.
If \(P_2\) is the only clean point, take
\((x,y)=(t+\gamma u,u)\), remove the full \(t\)-gcd multiplicity, and use
the \(Z_2\) channel.  These orientations include multiple boundary roots
and are exhaustive.

These are coefficient theorems.  Division by the third factor in (25)
lifts through the literal source quotient only when the transverse
principal parts belong to the literal boundary submodule, rather than
merely to the kernel of evaluation.  Also, the same-power
target/residue lock says that a quadratic companion cancelling a target
in (21) cancels its ordinary odd residue as well.  The adaptive direction
solves collision and label visibility; it does not prove the relative
saturation membership or construct the target-cancelled adjacent-power
homotopy.

## 6. Intrinsic residue and the global-selection audit

If \(A=\alpha E_{aa}\), then

\[
                         \sigma(D)=\alpha D_{aa}=0
\]

for every \(D\) with \(D_{aa}=0\).  Choosing
\(D_{bb}D_{cc}\ne0\) now gives \(\gamma=0\),
\(K_1=K_2=-\alpha D\), and

\[
 \operatorname {Act}(t,u)=\alpha^3d_bd_c\,t^2u^2.            \tag{26}
\]

The two generic rows collapse:

\[
                         J_2=(h-1)J_1,\qquad
                         (J_1)_{aa}=(J_2)_{aa}=0.             \tag{27}
\]

The complementary target begins in transverse order \(h-1\), while the
selected \(a\)-target begins in order \(h\).  The unary cap \(K_0\) sees
\(\overline Y_a\), but it lies outside the collided boundary-polar span.
Thus the selected-colour blindness is intrinsic to this block, not an
artifact of \(I-E_{aa}\).

Now audit what the global curvature selection supplies.  The two
distinguished good charts in its selected rectangle are \(pq\) and \(pr\),
and with \(a=b\) that rectangle is

\[
 \kappa=\alpha U-BF\ne0,\qquad
 B=A_{pr}(a,c),\quad F=A_{qs}(a,d),\quad U=A_{rs}(c,d).       \tag{28}
\]

A nonzero \(3\times3\) block admits either an off-diagonal selected cell
or the adaptive diagonal construction exactly when it is not a scalar
diagonal matrix unit.  Consequently, as a bare good cap chart, an
intrinsic \(pq\)-chart can be avoided whenever \(A_{pr}\) is nonzero and
is not of the form \(\lambda E_{ee}\).

Keeping the base cell from the same displayed rectangle gives two
immediate sufficient same-cell escapes:

\[
 B\ne0,\ c\ne a;\qquad\text{or}\qquad
 B\ne0,\ c=a,\ A_{pr}\ne B E_{aa}.                           \tag{29}
\]

The first selects the off-diagonal cell \(B\); the second applies the
adaptive construction to the selected diagonal cell \(B\).  In both cases
the unary base \(K_0\) is still the literal cell occurring in (28).
Equation (29) is a list of sufficient cases visible from this fixed
rectangle, not an if-and-only-if obstruction to all other choices.

There is a further source-provenance distinction in the second case.
An arbitrary adaptive \(D\) is a legal linear combination of the nine
\(pr\)-chart rows, but no audited theorem currently says that contracting
the two-chart overlap packet against that \(D\) preserves a nonzero
\(AU-BF\) term or transports the adaptive boundary jets.  Thus retaining
the curvature-selected base cell is not yet a source-faithful
curvature-preserving adaptive pencil.  If \(B=0\), another entry of
\(A_{pr}\) can give a good active candidate chart, but the original minor
supplies no nonzero curvature coefficient anchored at that new entry.  A
different minor or comparison may still work; no certified relocation
theorem currently provides one.

At the level of these two distinguished charts and this fixed rectangle,
this exhausts what follows automatically.  Goodness concerns the two
deleted endpoint-star maps and places no rank or support condition on the
direct block.  The other curvature cells \(F\) and \(U\) live on \(qs\)
and \(rs\), which are not guaranteed good pairs.  Even if one is
off-diagonal, moving the main chart there can lose the good-pair input.
The selected-two-chart ledger not covered by the existing cap
constructions is therefore

\[
 A_{pq}=\alpha E_{aa},\qquad
 A_{pr}=0\ \text{or}\ A_{pr}=\lambda E_{ee}.                 \tag{30}
\]

Equation (30) places no condition on any additional good neighbour of
\(p\).  The good-fan theorem can supply such neighbours, but no certified
selection result currently forces one of their direct blocks to be
non-intrinsic or couples it to the chosen nonzero rectangle.

The cases not covered by the fixed-rectangle same-cell test (29) include
every \(B=0\) case, as well as \(c=a\) with
\(A_{pr}=B E_{aa}\).  This is an uncovered ledger, not a claim that no
other curvature rectangle or comparison exists.  Equation (28) does not
contradict these cases.  For example,

\[
                         B=F=0,\qquad \alpha U\ne0            \tag{31}
\]

has nonzero curvature.  Taking \(c=d\) lets the visible \(U\)-cell be
diagonal and intrinsic as well.  Minimum entry support is used upstream
to obtain a nonzero transition; it does not say that either direct block
on the resulting good fan has two entries.

Two complementary guards make the logical boundary sharp.

1. The exact \(K_4\) three-one-factor source is entry-minimal and has
   \(A=U=1\), \(B=F=0\), so \(\kappa=1\), while every nonzero physical
   block is a diagonal coordinate unit.  Removing any one cell destroys
   the unique matching for one target, proving entry-minimality.  Its
   selected pairs are not good—the deleted endpoint-star maps have a
   missing colour—and it has \(h=1\).  Thus exactness, entry-minimality,
   and curvature alone do not force a replacement.
2. The literal eight-site aggregate packet in
   curved-two-chart-omega-diagonal-row-guard.md has
   \(A_{pq}=A_{pr}=E_{00}\), four good endpoint stars,
   \(AU-BF=1\), clean unary and scalar-zero binary endpoints in both
   charts, all three diagonal full-nine rows, and the complete power-free
   overlap/four-cut packet.  Every nonzero block is a diagonal coordinate
   unit, so it has no off-diagonal or adaptive replacement chart.  It
   fails exactly the six off-diagonal common-power rows and is not an
   exact GHZ source.

The first guard retains exact minimum support but not the high-order good
pair; the second retains the high-order good/overlap packet but not the
complete exact target.  No existing example retains both, which would be
a counterexample to the intended theorem.  Conversely, no certified
result yet combines the omitted off-diagonal common-power rows with
minimum support and goodness to exclude (30), much less constructs the
anchored relocation missing when \(B=0\).

The proved reduction is therefore:

* every non-intrinsic selected diagonal block admits a legal uncollided
  three-boundary pencil, two visible literal jets, and the scalar routing
  above;
* non-diagonal determinant singularities add no physical boundary, but
  forbid unqualified use of invertible-cap lemmas.

One remaining selected-two-chart statement is to exclude (30) with the
complete full-nine common-power system and overlap.  A global alternative
is a new theorem relocating to another good chart while retaining a
nonzero curvature anchor.  Even off (30), proof closure still requires the
relative saturation/target-cancelled comparison from Section 5; for a
non-diagonal adaptive \(D\), it also requires the source-faithful
two-chart transport just distinguished above.  Curvature and the currently
isolated overlap identities do not supply those steps.
