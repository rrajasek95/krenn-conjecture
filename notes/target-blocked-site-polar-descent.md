# Two blocked sites expose a physical dark matching

## 1. Outcome

Work on the six residual sites \(W\).  Let

\[
 q\in {\cal A}_{W,2},\qquad
 \beta=LS,\qquad
 \beta q^{[2]}=\sum_{c=0}^2\lambda_cX_c,                 \tag{1}
\]

where \({\cal A}_W=\bigotimes_{x\in W}(\mathbb C\oplus V_x)\) is the
site-square-zero algebra.  Put

\[
 H_x=\operatorname{span}(L_x,S_x),\qquad
 B_e=\{x:e_e^{(x)}\in H_x\}.                              \tag{2}
\]

The set \(B_e\) is the target-blocking set for an active colour
\(e\), meaning \(\lambda_e\ne0\).  The exact coefficient cut is stronger
than the earlier conclusion that *some* blocked site must occur:

> **Two-site blocked-target descent.**  If \(|B_e|\le2\), choose distinct
> \(x,y\) containing \(B_e\), and put \(R=W\setminus\{x,y\}\).  Let
> \(\pi_z:V_z\to V_z/H_z\) be the quotient map.  Then
>
> \[
> \boxed{
>  \beta_{xy}(e_e^*,e_e^*)\,
>  \left(\pi_Rq_R\right)^{[2]}
>    =\lambda_e\bigotimes_{z\in R}\pi_z(e_e^{(z)})\ne0.} \tag{3}
> \]

Thus the cap has a nonzero literal coefficient on \(xy\), and the
physical \(q\)-blocks on the four complementary cap-dark quotients have a
perfect matching.  In particular the dark coefficient cut gives a
nonzero physical four-cycle differential for the *same cap* \(\beta\).
The distinguished edge may have moved from the curvature coefficient
used to select \(\beta\), but the cap itself has not changed.

Consequently failure of every physical dark cut has the sharp necessary
condition

\[
 \boxed{|B_e|\ge3\quad\hbox{for every }e\hbox{ with }\lambda_e\ne0.}
                                                               \tag{4}
\]

There is no cancellation between two active diagonal targets in (3): the
two retained endpoint slots are contracted by the **physical coordinate
covector** \(e_e^*\).  It evaluates to zero on every \(e_f\), \(f\ne e\),
before the other four sites are quotiented.

On the double-zero packet one additionally has

\[
 L_{x,\delta}=S_{x,\delta}=0,\qquad
 H_x\subseteq E_x=\operatorname{span}(e_a,e_b).          \tag{4a}
\]

For a binary missing-label target with active colours \(a,b\), (4) and
(4a) leave only two coordinate-free geometries.

1. \(B_a\cap B_b\ne\varnothing\).  At every site in the intersection,
   \(H_x\) is the entire missing plane
   \(E_x=\operatorname{span}(e_a,e_b)\).
2. \(B_a\cap B_b=\varnothing\).  Then the two sets are complementary
   triples, and

   \[
       H_x=\mathbb Ce_a\quad(x\in B_a),\qquad
       H_x=\mathbb Ce_b\quad(x\in B_b).                 \tag{5}
   \]

This is a structural reduction, not a proof of the conjecture.  The
rank-two-overlap and rigid \(3+3\) line-field alternatives in (5) are the
remaining target-incidence gates.  They must be coupled to the unused
full-nine diagonal rows, the other chart, or the curvature grade.

## 2. Proof of the two-site cut

For \(z\in R\), quotient the local space by \(H_z\).  Every coefficient
of a cap edge meeting \(R\) dies, because that edge has a local factor
\(L_z\) or \(S_z\).  After also taking the \(e\)-coordinate at \(x,y\),
the only surviving cap edge in the left side of (1) is \(xy\).  Since it
occupies both retained sites, both \(q\)-edges must lie entirely on \(R\).
This gives the left side of (3), with no factorial: the powers in (1) are
divided matching powers.

On the right side, \(e_e^*(e_f)=\delta_{ef}\), so every target except the
\(e\)-target dies.  Because \(x,y\) contain \(B_e\), every site of \(R\)
is \(e\)-visible and

\[
                 \pi_z(e_e^{(z)})\ne0\qquad(z\in R).    \tag{6}
\]

A tensor product of nonzero vectors over a field is nonzero.  This proves
(3), including the two asserted nonvanishings.

Dualizing \(V_z/H_z\) identifies its dual with

\[
                         K_z=H_z^\perp.                  \tag{7}
\]

The nonzero four-site tensor \((\pi_Rq_R)^{[2]}\) contains at least one
nonzero perfect-matching summand.  Hence some two complementary physical
blocks of \(q\) are nonzero on the corresponding \(K_z\)'s.  Taking one
of them together with the nonzero cap coefficient in (3) is exactly the
literal dark-cut construction.

The proof actually shows why one retained site cannot suffice.  If one
contracts a site \(x\) by \(e_e^*\) and quotients all other sites by their
\(H_z\)'s, every cap edge still meets a quotient site and dies.  Therefore
an active target cannot have \(|B_e|\le1\).  The two-site cut is the first
place a cap edge can survive, and it then gives (3).

## 3. The one-site polar: incidence factors but does not cancel

Continue under the double-zero channel condition (4a).  Every top monomial
of \(\beta q^{[2]}\) uses one cap edge, whose two endpoint factors have zero
\(\delta\)-coordinate.  Hence the cap identity itself forces
\(\lambda_\delta=0\).

The local calculation explains why using a blocked site positively is
natural.  Delete \(x\), write \(U=W\setminus\{x\}\), and decompose

\[
 q=q_0+q_x,\qquad L=L_0+L_x,\qquad S=S_0+S_x,            \tag{8}
\]

where \(q_x\in V_x\otimes{\cal A}_{U,1}\).  The coefficient of the
\(x\)-slot in (1) is the exact five-site normal row

\[
 (L_xS_0+S_xL_0)q_0^{[2]}
       +L_0S_0q_xq_0
   =\sum_c\lambda_ce_c^{(x)}X_c^U.                     \tag{9}
\]

The last summand on the left is the physical \(q\)-incidence term.  It
does not vanish merely because the target is blocked.

Suppose \(H_x=E_x\), and write

\[
 L_x=l_ae_a+l_be_b,\qquad S_x=s_ae_a+s_be_b,\qquad
 D=l_as_b-l_bs_a\ne0.                                  \tag{10}
\]

Decompose the missing-plane component of \(q_x\) as
\(L_xz_L+S_xz_S\).  Comparing the two missing-plane coordinates in (9)
gives

\[
\begin{aligned}
 S_0\bigl(q_0^{[2]}+L_0z_Lq_0\bigr)
   &= {\lambda_as_b\over D}X_a^U
      -{\lambda_bs_a\over D}X_b^U,\\
 L_0\bigl(q_0^{[2]}+S_0z_Sq_0\bigr)
   &=-{\lambda_al_b\over D}X_a^U
      +{\lambda_bl_a\over D}X_b^U.                    \tag{11}
\end{aligned}
\]

The component transverse to \(E_x\) is

\[
                         L_0S_0z_\perp q_0=0.           \tag{12}
\]

Thus blocking absorbs the incidence into the opposite linear factor; it
does **not** cancel it.  For a unary target, either nonzero line of (11)
forces the pure five-site target into the top-degree ideal of \(S_0\) or
\(L_0\).  Equivalently, the opposite factor is target-coordinate at some
other site.  Indeed, in top multidegree,
\[
 ({\cal A}_U)_5/S_0({\cal A}_U)_4
       \simeq\bigotimes_{z\in U}(V_z/\mathbb CS_z),
\]
so a pure target belongs to the ideal precisely when one local \(S_z\)
spans its coordinate line; the \(L_0\) statement is symmetric.  For a
binary target, (11) leaves a genuine toric ratio instead of forcing a
coordinate factor.

For example, if every local \(S_z\), including \(S_x\), has two nonzero
missing coordinates, quotienting the first line of (11) by the five
lines \(\mathbb CS_z\), \(z\ne x\), gives

\[
              \prod_{z\in W}{S_{z,a}\over S_{z,b}}
                         =-{\lambda_a\over\lambda_b}.   \tag{13}
\]

The corresponding statement holds for \(L\).  Equation (13) is the dense
binary residue of the blocked-site polar.

## 4. What the full-nine companion rows add

Now assume the complete source rows

\[
 d_{ij}q^{[3]}+p_is_jq^{[2]}=\delta_{ij}X_i.            \tag{14}
\]

Fix a selector \(\eta\), put

\[
 S=s(\eta),\qquad v=d\eta,\qquad
 Y_c^S=\bigotimes_{x\in W}
       \left(e_c^{(x)}\bmod\mathbb CS_x\right).        \tag{15}
\]

For every \(u\in v^\perp\), contraction of (14) against
\(u\eta^{\mathsf T}\) has zero direct coefficient and therefore gives

\[
                      p(u)S q^{[2]}=\sum_cu_c\eta_cX_c. \tag{16}
\]

Quotienting every site by the line \(\mathbb CS_x\) kills the complete
left side.  Hence

\[
                  \sum_cu_c\eta_cY_c^S=0
                         \qquad(u\in v^\perp).          \tag{17}
\]

Elementary linear algebra now gives one tensor \(Z_S\) such that

\[
                         \boxed{\eta_cY_c^S=v_cZ_S
                                      \quad(c=0,1,2).}  \tag{18}
\]

Indeed, if \(v=0\), (17) holds for every \(u\) and every
\(\eta_cY_c^S\) is zero.  Otherwise choose \(v_k\ne0\), use
\(u=v_ke_c-v_ce_k\) in (17), and take
\(Z_S=(\eta_kY_k^S)/v_k\).  Transposing (14) gives, for
\(w=d^{\mathsf T}\xi\),

\[
 \xi_cY_c^L=w_cZ_L,\qquad
 Y_c^L=\bigotimes_x(e_c^{(x)}\bmod\math CL_x).          \tag{19}
\]

These are genuine full-nine companion consequences: the \(q^{[3]}\)
incidence is removed by taking the direct-zero hyperplane, rather than by
cancelling a matching power.  They sometimes force a coordinate factor.
For example, if \(\eta_\delta=0\), \(\eta_e\ne0\), and
\((d\eta)_\delta\ne0\), the \(\delta\)-equation in (18) gives \(Z_S=0\),
then \(Y_e^S=0\).  Thus

\[
                         S_x\in\mathbb C^*e_e
                  \quad\hbox{for some }x.              \tag{20}
\]

The same conclusion holds when \(d\eta=0\), and (19) gives the transposed
criterion for \(L\).

There is also an exact escape.  Suppose \(\eta_\delta=0\),
\(\eta_a\eta_b\ne0\), all six \(S_x\)'s have both missing coordinates
nonzero, and \(v_\delta=0\).  Then (18) necessarily forces
\(v_av_b\ne0\), and it is equivalent to

\[
       \prod_x{S_{x,a}\over S_{x,b}}
          ={\eta_av_b\over\eta_bv_a}.                  \tag{21}
\]

For the selected isotropic pair \(\xi^{\mathsf T}d\eta=0\), with both
diagonal target coefficients active, (21) becomes

\[
       \prod_x{S_{x,a}\over S_{x,b}}
          =-{\xi_a\eta_a\over\xi_b\eta_b}
          =-{\lambda_a\over\lambda_b}.                \tag{22}
\]

This is exactly (13).  Hence the apparently stronger same-factor
companion quotient collapses to selector isotropy on the dense blocked
branch.  It supplies a useful forced-factor criterion off that branch,
but it does not eliminate either residual geometry after (5).

## 5. Sharp audit by the one-row guard

The guard from
[the rank-drop audit](target-blocked-incidence-rank-drop-audit.md) has

\[
\begin{aligned}
 L&=x_{0,a}+x_{2,a}+x_{4,a},\\
 S&=x_{1,a}+x_{2,b}+x_{4,b},\\
 q&=x_{2,a}x_{3,a}+x_{4,a}x_{5,a},
 \qquad LSq^{[2]}=X_a.                                  \tag{23}
\end{aligned}
\]

Its complete blocking set is

\[
                         B_a=\{0,1,2,4\}.               \tag{24}
\]

The earlier note highlighted the two rank-two sites \(2,4\), but the
coordinate-line sites \(0,1\) are blocked as well.  Thus the guard does
not contradict (3); every pair leaves an \(a\)-blocked complement site.
At site \(2\), the \(q_0^{[2]}\) term in (11) is zero and the incidence
term alone equals \(X_a^{W\setminus2}\).  This is a literal witness that a
one-site proof cannot discard \(q_xq_0\).

Use the displayed good-star extension

\[
 (p_a,p_b,p_\delta)=(L,x_{3,b},x_{5,\delta}),\qquad
 (s_a,s_b,s_\delta)=(S,x_{3,b},x_{5,\delta}),           \tag{25}
\]

and direct matrix \(d=E_{bb}\).  An exact replay shows that the selected
\((a,a)\) row and all six off-diagonal rows in (14) hold.  The packet
fails exactly the other two diagonal rows:

\[
 q^{[3]}+p_bs_bq^{[2]}=0\ne X_b,\qquad
 p_\delta s_\delta q^{[2]}=0\ne X_\delta.              \tag{26}
\]

Thus the four-blocked residue survives the selected row, nonradial
curvature algebra, good endpoint extensions, and every off-diagonal
companion.  It is not a full-nine source precisely because the two unused
diagonal anchors are missing.  Any continuation beyond (4) must genuinely
couple one of those anchors (or an equivalent second-chart row) to the
selected cap; same-factor polarization and the six off-diagonal rows do
not suffice.

The dependency-free checker
[verify_target_blocked_site_polar_descent.py](../computations/verify_target_blocked_site_polar_descent.py)
audits the universal two-site coefficient cut over finite fields, the
companion proportionality lemma, the local blocking dichotomy, the
incidence-only guard row, and the exact seven-row/full-nine failure ledger
(25)--(26).

## 6. Exact scope

The proved outputs are:

* the source-valid four-site quotient identity (3), using only the selected
  diagonal cap row;
* the obstruction \(|B_e|\ge3\) for every active target whenever all
  physical dark cuts fail;
* under the double-zero channel condition, the rank-two-overlap versus
  complementary-\(3+3\) classification (5);
* the full-nine same-factor proportionalities (18)--(19), including the
  forced coordinate factor (20) and the exact toric escape (22).

Nothing here excludes a rank-two blocking site or the \(3+3\) coordinate
line field.  Nor does (3) put the relocated cap edge back into the original
literal curvature cell, identify the physical \(q\) with a vertex-factor
\(K_6\) base, or produce the clean-cap/Macaulay annihilator.  Those are
still separate grade-transport and full-nine coupling problems.
