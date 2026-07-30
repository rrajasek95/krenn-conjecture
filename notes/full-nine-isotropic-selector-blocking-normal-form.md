# Full-nine selectors turn target blocking into direct-form alignment

## 1. Outcome

Work on six residual sites \(W\), with the literal full-nine equations

\[
 d_{ij}q^{[3]}+p_i s_jq^{[2]}=\delta_{ij}X_i,
 \qquad 0\leq i,j\leq2.                                  \tag{1}
\]

At a site \(x\), let

\[
 \mathsf P_x\xi=\sum_i\xi_i(p_i)_x,
 \qquad
 \mathsf S_x\eta=\sum_j\eta_j(s_j)_x                  \tag{2}
\]

be the two local endpoint-star maps.  For a target colour \(e\), orient
the physical colour space by

\[
 u^{\mathsf T}J_ev=\det(u,v,e_e),
 \qquad
 N_{x,e}=\mathsf P_x^{\mathsf T}J_e\mathsf S_x.          \tag{3}
\]

The unused rows in (1) give a structural escape from both binary residues
in the
[blocked-site descent](target-blocked-site-polar-descent.md).  One should
vary the full three-colour selector, rather than keep varying a selector
inside the two-dimensional missing-colour plane.

> **Full-nine selector escape.**  Suppose
> \(d\in\operatorname {Mat}_{3\times3}(\mathbb C)\) has rank at least
> two, and put
>
> \[
>  T_e=\{x\in W:N_{x,e}\in\mathbb C d\}.                 \tag{4}
> \]
>
> There is a rank-one direct-zero selector
> \((\xi,\eta)\), with \(\xi_e\eta_e\ne0\), for which the target
> \(e\) is blocked only at sites in \(T_e\).  The selector here is chosen
> separately for each target \(e\); simultaneous visibility for several
> colours from one common selector is not claimed.  Consequently, if
> \(|T_e|\leq2\), the two-site descent gives a nonzero physical dark
> cut for the literal cap
>
> \[
>  \beta=p(\xi)s(\eta),\qquad
>  \beta q^{[2]}=\sum_c\xi_c\eta_cX_c.                  \tag{5}
> \]
>
> If every such dark cut fails, then
>
> \[
>                         \boxed{|T_e|\geq3.}             \tag{6}
> \]

When \(d\) is invertible, (4) simplifies to

\[
                         T_e=\{x:N_{x,e}=0\},             \tag{7}
\]

because \(N_{x,e}\) has rank at most two.  Thus invertibility does not
make the residue disappear, but it turns it into three literal vanishing
endpoint-wedge matrices for every colour.

There are exact versions for lower-rank direct blocks.  If \(d=0\), use

\[
                         T_e=\{x:N_{x,e}=0\};             \tag{8}
\]

again.  If \(d=ab^{\mathsf T}\ne0\), the direct-zero selector variety has
the two rulings

\[
 \mathscr Q_L=\{a^{\mathsf T}\xi=0\},\qquad
 \mathscr Q_R=\{b^{\mathsf T}\eta=0\}.                 \tag{9}
\]

On every target-active ruling define

\[
\begin{aligned}
 T^L_e&=\{x:N_{x,e}=a w_x^{\mathsf T}
                    \text{ for some }w_x\},\\
 T^R_e&=\{x:N_{x,e}=w_x b^{\mathsf T}
                    \text{ for some }w_x\}.
\end{aligned}                                             \tag{10}
\]

The same conclusion holds with \(T_e^L\) or \(T_e^R\): a ruling with at
most two aligned sites supplies a physical dark cut, while failure on an
eligible ruling forces at least three aligned sites.  The left ruling is
eligible for \(e\) exactly when \(a\notin\mathbb C e_e\), and the right
ruling is eligible exactly when \(b\notin\mathbb C e_e\).

This is a strict further normal form, not a completion of the conjecture.
It replaces the cap-dependent alternatives

* one site with \(H_x\) equal to the missing-colour plane; and
* complementary \(3+3\) coordinate-line fields

by source-level identities involving the complete endpoint stars and the
literal direct block.  Good endpoint-star injectivity is retained but is
not needed for the reduction.

The curvature conclusion is existential at the pair produced by the
two-site cut.  It needs no separate curvature-open hypothesis, because a
nonzero cap coefficient forces one of the two oriented transitions in
(21) to be detected.  It does not retain a preassigned curvature cell or
orientation, and it does not synchronize the chosen pair with a second
chart.

## 2. The selector family is source-provenant

Contract all nine rows of (1) against the rank-one matrix
\(\ell=\xi\eta^{\mathsf T}\).  This gives

\[
 (\xi^{\mathsf T}d\eta)q^{[3]}
   +p(\xi)s(\eta)q^{[2]}
      =\sum_c\xi_c\eta_cX_c.                            \tag{11}
\]

On the isotropic hypersurface

\[
 \mathscr Q_d=\{([\xi],[\eta])\in\mathbf P^2\times\mathbf P^2:
                     \xi^{\mathsf T}d\eta=0\},           \tag{12}
\]

equation (11) is exactly (5).  There is no cancellation of \(q^{[2]}\),
no replacement of the physical \(q\), and no abstract cap added by hand.
Every selector is a linear combination of the same nine literal source
rows.

The target-active part

\[
 \mathscr Q_{d,e}^{\circ}
   =\{([\xi],[\eta])\in\mathscr Q_d:\xi_e\eta_e\ne0\}   \tag{13}
\]

is nonempty unless \(d\) is a nonzero scalar multiple of \(E_{ee}\).
Indeed, if \(d=\gamma E_{ee}\), \(\gamma\ne0\), isotropy kills
\(\xi_e\eta_e\).  Conversely, unless \(d\) has that form, one can choose
\(\eta_e\ne0\) so that either \(d\eta=0\) or \(d\eta\) is not a multiple
of \(e_e\), and then choose \(\xi_e\ne0\) perpendicular to \(d\eta\).

For rank at least two, \(d\) cannot be a coordinate matrix unit, so (13)
is nonempty for every \(e\).  If a previously selected missing-plane cap
has two active colours \(a,b\), its isotropy already proves that neither
of those two labels has the coordinate-unit obstruction, in every rank.

## 3. Universal determinant zeros

For a selector in (12), put

\[
 L_x=\mathsf P_x\xi,\qquad S_x=\mathsf S_x\eta,
 \qquad H_x=\operatorname {span}(L_x,S_x).                \tag{14}
\]

The exact local determinant is

\[
 F_{x,e}(\xi,\eta)
   =\det(L_x,S_x,e_e)
   =\xi^{\mathsf T}N_{x,e}\eta.                          \tag{15}
\]

If \(F_{x,e}\ne0\), then \(e_e\notin H_x\); in particular \(x\) is not
target-blocking.  This one-way implication is all that is needed and does
not make the false dependent-vector equivalence rejected by the earlier
[rank-drop audit](target-blocked-incidence-rank-drop-audit.md).

Assume first that \(\operatorname {rank}d\ge2\).  The bilinear form
\(\xi^{\mathsf T}d\eta\) is irreducible.  Since \(F_{x,e}\) has the same
bidegree, it vanishes identically on \(\mathscr Q_d\) exactly when

\[
                         N_{x,e}=\lambda_xd.              \tag{16}
\]

For every \(x\notin T_e\), the condition \(F_{x,e}\ne0\) cuts out a
nonempty Zariski-open subset of the irreducible hypersurface
\(\mathscr Q_d\).  Intersect those finitely many opens with (13).  The
intersection is nonempty over \(\mathbb C\).  At its selectors every
blocked site lies in \(T_e\), proving the first assertion of the theorem.

For \(d=0\), the same argument runs on the irreducible
\(\mathbf P^2\times\mathbf P^2\), and a bilinear form vanishes everywhere
exactly when its matrix is zero.  This proves (8).

Finally let \(d=ab^{\mathsf T}\ne0\).  On the irreducible left ruling,

\[
 F_{x,e}|_{\mathscr Q_L}\equiv0
 \quad\Longleftrightarrow\quad
 N_{x,e}=a w_x^{\mathsf T},                               \tag{17}
\]

because every column of \(N_{x,e}\) must annihilate \(a^\perp\).  The
right-ruling statement is the transpose.  The target-active open on the
left is nonempty exactly when \(a^\perp\) contains a vector with nonzero
\(e\)-coordinate, namely when \(a\notin\mathbb C e_e\); the right criterion
is identical with \(b\).  Finite intersection of the remaining nonempty
opens proves (10).

## 4. From at most two universal sites to a literal dark cut

Choose the selector furnished above and let

\[
 B_e=\{x:e_e\in H_x\}.                                   \tag{18}
\]

Equations (15)--(17) give \(B_e\subseteq T_e\), or the corresponding
ruling set.  If its size is at most two, choose two sites \(x,y\) that
contain it and quotient every other local colour space by \(H_z\).  The
two-site blocked-target identity gives

\[
 \beta_{xy}(e_e^*,e_e^*)
    \bigl(\pi_{W\setminus\{x,y\}}q\bigr)^{[2]}
   =\xi_e\eta_e
      \bigotimes_{z\ne x,y}\pi_z(e_e)\ne0.              \tag{19}
\]

Thus the cap has a nonzero literal \((e,e)\)-coefficient on \(xy\), and
the complementary physical \(q\)-blocks contain a nonzero dark perfect
matching.  This is exactly the physical dark cut; (6) follows by
contraposition.

The same coefficient automatically carries a nonradial physical
transition.  If \(u=(A_{xy})_{e,e}\), and \(H^\rightarrow,H^\leftarrow\)
are the two endpoint-star products at that decorated edge, put

\[
 K^\rightarrow=ud-H^\rightarrow,
 \qquad K^\leftarrow=ud-H^\leftarrow.                    \tag{20}
\]

The cap coefficient in (19) is

\[
 \ell(H^\rightarrow+H^\leftarrow)
   =-\ell(K^\rightarrow)-\ell(K^\leftarrow),             \tag{21}
\]

because \(\ell(d)=0\).  Its nonvanishing forces one of the two literal
\(AU-BF\) transitions to be detected by the same source-provenant cap.
Hence moving out of the missing plane does not reopen the curvature-carrier
gate.

## 5. Exact residue left for the two original active colours

Let \(a,b\) be the active colours of the binary missing-plane cap in the
blocked-site descent.  If \(\operatorname {rank}d\ge2\) and every
full-nine selector dark cut fails, define the two source-level alignment
sets \(T_a,T_b\) by (4).  Then

\[
                         |T_a|,|T_b|\ge3.                 \tag{22}
\]

Consequently exactly the following coarse incidence alternative remains:

1. \(T_a\cap T_b\ne\varnothing\), so at one site two different physical
   endpoint-wedge matrices are both proportional to the same direct form;
2. \(T_a\cap T_b=\varnothing\), in which case they are complementary
   triples.

For rank one, choose any eligible ruling for each of \(a,b\) and use the
corresponding sets in (10); the same alternative holds.  This resembles
the earlier blocked-set dichotomy, but is strictly more source-relative:
it constrains the full endpoint-star matrices, not merely the two selected
local vectors.  A second chart can now be compared through literal direct
forms and local wedge matrices.  No such comparison is claimed here.

The dependency-free
[checker](../computations/verify_full_nine_isotropic_selector_blocking_normal_form.py)
exhausts the bilinear identity classifications and prescribed-target
criterion over \(\mathbb F_2\), and audits the transition identity over
\(\mathbb F_5\).  It performs no matching-support census.
