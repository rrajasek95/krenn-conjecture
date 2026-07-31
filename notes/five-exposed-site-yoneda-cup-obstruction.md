# The five-exposed-site ledger does not yet define a Yoneda product

## 1. Outcome

Fix an off-diagonal selected pair cell

\[
 a\ne b,\qquad \alpha=A_{pq}(a,b)\ne0,\qquad
 \tau=\operatorname {tr}A_{pq},
 \qquad K_*=\tau E_{ab}-\alpha I.                 \tag{1}
\]

Let the canonical pair cap leave a set \(W\) of \(2h\) sites, with
\(h\ge3\).  Choose three distinct sites \(r,s,x\in W\).  Thus the five
exposed sites are

\[
                         p,q,r,s,x.                       \tag{2}
\]

The exact four-site comparison on \(W\setminus\{r,s\}\) is

\[
 \boxed{
 \kappa\bigl(zZ_1-(h-1)Z_0\bigr)
 +Dv\bigl(zZ_2-(h-2)Z_1\bigr)=0,}             \tag{3}
\]

where

\[
 Z_0=z^{[h-1]},\qquad Z_1=z^{[h-2]},\qquad
 Z_2=z^{[h-3]},\qquad
 D=At-By,\qquad \kappa=AU-BF.                 \tag{4}
\]

The structural branch of interest has \(\kappa\ne0\); when nonvanishing of
the output matters, also fix a label \(c\) with
\(\overline Y_c\ne0\).  No other direct entry or star form is assumed
invertible.

The normalized scalar-zero cap is the literal target-bearing row

\[
 Qq^{[h-1]}=-\Delta_{2h,3},\qquad
 Q=\alpha^{-1}R,                               \tag{5}
\]

and its odd residue at \(x,c\) is

\[
                    \rho_c(Q)=-\overline Y_c.              \tag{6}
\]

The normalization in a putative secondary pairing is therefore forced:

\[
                     \kappa\rho_c(Q)=-\kappa\overline Y_c.
                                                               \tag{7}
\]

This note proves that (7) is **not** the value of an ordinary
source-faithful Yoneda or cup product furnished by the presently listed
connection, normal, curvature, direct-double, and anchor rows.

There are three precise reasons.

1. In the formal two-chart comparison cone defined in Section 3, (3) is
   the expanded boundary of the four-cut comparison cell.  If that cone is
   enhanced by a chain-level cup product satisfying Leibniz, its product
   with the augmented cap cycle (5) is again a boundary.  Hence its
   ordinary homology class in that enhancement is zero.  Neither the cone
   bookkeeping nor this conditional argument constructs such a cup
   product.
2. The site degrees do not even permit ordinary multiplication to realize
   (7).  Formula (3) has top site degree \(2h-2\) on
   \(W\setminus\{r,s\}\).  Multiplication by the quadratic \(Q\) has
   degree \(2h\) on only \(2h-2\) sites and is identically zero in the
   site-square-zero algebra.  The desired class instead has degree
   \(2h-1\) on the different set \(W\setminus\{x\}\).  Any successful
   operation must account for that net support and degree change.  A
   restriction--insertion correspondence is one natural way to do so, but
   the degree count does not prove that every possible secondary
   construction factors that way.
3. Every presently listed target-cancelling anchor on the same complement
   is a same-power quadratic row.
   Its target coefficient and odd residue lie on the graph
   \((\lambda,\lambda\overline Y_c)\).  Thus an anchor with target
   \(+\kappa\Delta\) has residue \(+\kappa\overline Y_c\) and cancels
   both coordinates of \(\kappa(Q,-\Delta)\).  The target-zero result has
   residue zero, not (7).

The all-label five-site anchor formula is written out below.  It does not
repair the problem: it is the next coefficient of the same literal cap
row, and therefore still obeys the target--residue graph.  It does show
the complete direct/star coefficient which one natural five-site
correspondence would have to retain; it does not classify every possible
secondary construction.

A nonzero value (7) cannot come from the ordinary operations audited here;
it would require additional **secondary or filtered data**.  Section 7
states one concrete candidate architecture: a Rees-type extension and a
five-site restriction--insertion/Leibniz cell.  The current calculation
does not prove that this architecture is necessary.  If the goal is a
single-valued pairing, that construction would also need zero odd-residue
indeterminacy; a secondary operation explicitly valued modulo
indeterminacy would have a different well-definedness requirement.  None
of these extra data is implied by the existing equalities.  No Massey or
Bockstein operation is claimed to exist here.

The conclusion is unchanged when \(\tau=0\), and it is unchanged on the
direct-free boundary \(A_{pr}=0\).  At \(\tau=0\), (5) remains a legal
relation-level cap cycle but is not an extension out of the radial
generator \(q\).  On the direct-free boundary, \(D=At\) and
\(\kappa=AU\ne0\); the triangular row remains target-zero and radial, so it
does not by itself supply any such secondary comparison.

Accordingly the off-diagonal filtered comparison remains **OPEN**.

## 2. The full all-label five-site anchor row

This section fixes the source degrees and records the complete fifth-site
coefficient of the two canonical cap presentations.  It rules out a
silently omitted term in those presentations, but it does not classify
arbitrary higher chain operations.

Put

\[
                         D_5=W\setminus\{r,s,x\},
 \qquad |D_5|=2h-3,                                      \tag{8}
\]

and write \(z\) for the internal quadratic on \(D_5\).  For fixed physical
labels \(i,j,k,\ell,c\), use the endpoint stars

\[
                         x_i,y_j,t_k,v_\ell,w_c             \tag{9}
\]

from \(p,q,r,s,x\), respectively, into \(D_5\).  Write the ten
endpoint-ordered direct entries as

\[
\begin{array}{c|cccccccccc}
\text{pair}&pq&pr&ps&px&qr&qs&qx&rs&rx&sx\\ \hline
\text{entry}&P&R&E&G&T&F&H&U&V&J.
\end{array}                                                \tag{10}
\]

Thus, for example, \(P=P_{ij}\), \(R=R_{ik}\),
\(F=F_{j\ell}\), and \(V=V_{kc}\).  Every symbol in (10) is one
fixed scalar entry; there is no matrix multiplication in the formulas
below.

The restriction of the canonical \(pq\)-cap and its one- and two-site
coefficients are

\[
\begin{aligned}
 C_{pq}&=h x_i y_j+Pz,\\
 L_r&=h(Ry_j+Tx_i)+Pt_k,\\
 L_s&=h(Ey_j+Fx_i)+Pv_\ell,\\
 L_x&=h(Gy_j+Hx_i)+Pw_c,\\
 M_{rs}&=h(RF+ET)+PU,\\
 M_{rx}&=h(RH+GT)+PV,\\
 M_{sx}&=h(EH+GF)+PJ.                         \tag{11}
\end{aligned}
\]

Take \(z^{[n]}=0\) for \(n<0\).  The coefficient at
\((r,k),(s,\ell),(x,c)\) of the literal cap row is

\[
\boxed{
\begin{aligned}
 {\cal A}_{pq}^{ij;k\ell c}={}&
 C_{pq}\Big((Uw_c+Vv_\ell+Jt_k)z^{[h-3]}
                 +t_kv_\ell w_cz^{[h-4]}\Big)\\
 &+L_r\Big(Jz^{[h-2]}+v_\ell w_cz^{[h-3]}\Big)\\
 &+L_s\Big(Vz^{[h-2]}+t_kw_cz^{[h-3]}\Big)\\
 &+L_x\Big(Uz^{[h-2]}+t_kv_\ell z^{[h-3]}\Big)\\
 &+(M_{rs}w_c+M_{rx}v_\ell+M_{sx}t_k)z^{[h-2]}.
                                                        \tag{12}
\end{aligned}}
\]

Every summand has site degree \(2h-3\) on \(D_5\).  At \(h=3\), only
the displayed \(z^{[h-4]}\) term is absent; no exceptional coefficient is
inserted.  In that specialization the odd residue set
\(D_x=W\setminus\{x\}\) has five sites, while the common set after all five
physical exposures has three.  This is a useful diagnostic instance of the
uniform formulas, not a separate five-site case proof.

There is a useful chart-free form.  Let

\[
\begin{aligned}
 {\cal S}_5={}&
 \bigl[x_i(TJ+FV+HU)+y_j(RJ+EV+GU)\\
 &\quad+t_k(PJ+EH+GF)+v_\ell(PV+RH+GT)\\
 &\quad+w_c(PU+RF+ET)\bigr]z^{[h-2]}\\
 &+\bigl[Pt_kv_\ell w_c+Ry_jv_\ell w_c+Ey_jt_kw_c
          +Gy_jt_kv_\ell\\
 &\quad+Tx_iv_\ell w_c+Fx_it_kw_c+Hx_it_kv_\ell
          +Ux_iy_jw_c+Vx_iy_jv_\ell+Jx_iy_jt_k\bigr]z^{[h-3]}\\
 &+x_iy_jt_kv_\ell w_cz^{[h-4]}.                 \tag{13}
\end{aligned}
\]

The fifteen terms in the first bracket are two exposed direct edges and
one exposed star; the ten terms in the second bracket are one direct edge
and three stars; the last term uses five stars.  Direct expansion of (12),
using only

\[
 z z^{[h-3]}=(h-2)z^{[h-2]},\qquad
 z z^{[h-4]}=(h-3)z^{[h-3]},                  \tag{14}
\]

gives

\[
                         {\cal A}_{pq}^{ij;k\ell c}
                              =h{\cal S}_5.                \tag{15}
\]

The \(pr\)-cap is obtained by exchanging \((q,j,y,P,F,H)\) with
\((r,k,t,R,U,V)\), with the direct entry \(T=A_{qr}(j,k)\) unchanged.
Its expansion gives the same \(h{\cal S}_5\).  Consequently

\[
 {\cal A}_{pq}^{ij;k\ell c}
   ={\cal A}_{pr}^{ik;j\ell c}
   =h\,\mathbf1_{i=j=k=\ell=c}\,Y_i^{D_5}.       \tag{16}
\]

This is the full all-label five-exposed-site mapping-cone row.  Its two
targets agree literally, including the factor \(h\), so their oriented
difference is target-zero.  Formula (16) is a source identity, not a
cancelled common-power assertion.

## 3. The curvature/direct-double ledger is a mapping-cone boundary

Before exposing \(x\), put \(C_4=W\setminus\{r,s\}\).  It has
\(2h-2\) sites.  The oriented \(pq\)-presentation minus the
\(pr\)-presentation of the complete four-cut coefficient has the five
literal contributions

\[
\begin{aligned}
 &-(h-1)\kappa Z_0,&&\text{direct-double},\\
 &-(h-1)DvZ_1,&&\text{normal difference},\\
 &+DvZ_1+\kappa zZ_1,&&\text{curvature},\\
 &+DzvZ_2,&&\text{power-free connection}.          \tag{17}
\end{aligned}
\]

Their sum is (3).  The signs follow the orientation
\(pq-pr\).  In particular, the coefficient of the selected curvature is
\(+\kappa\), and its direct-double companion is
\(-(h-1)\kappa\).  The connection-normal bracket has coefficient
\(-(h-2)Dv\).  No factorial other than the two divided-power
multiplication factors occurs.

For the ordinary-cup diagnostic, now form the formal two-chart
source-presentation comparison cone.  Let \({\bf b}_{pq}\) and
\({\bf b}_{pr}\) denote the two source presentation symbols for the same
four-cut coefficient, and let \({\bf g}_{pq,pr}\) be their comparison
cell.  By definition of this cone,

\[
          d{\bf g}_{pq,pr}={\bf b}_{pq}-{\bf b}_{pr}.      \tag{18}
\]

Expanding the right side by its direct-double, normal, curvature, and
connection filtration gives exactly (17), hence (3).  Therefore the
displayed adjacent-power ledger is a **filtered boundary** in this formal
comparison cone.  This is a bookkeeping construction, not a claim that
the listed polynomial rows already carry a cup product or a Rees
connecting morphism.  The boundary may define a connecting symbol in a
separately specified filtered quotient, but the evaluated identity (3)
alone does not do so.

Taking the \((x,c)\)-coefficient of (18) gives the comparison of the two
rows in (16).  Thus the all-label fifth-site row is the next coefficient
of the same mapping-cone boundary; it does not turn (3) into an ordinary
cycle class.

## 4. The scalar-zero cap is an augmented relation cycle

For a matrix \(L=(L_{ij})\), put

\[
 \sigma(L)=\sum_{i,j}L_{ij}A_{pq}(i,j),\qquad
 r(L)=\sum_{i,j}L_{ij}p_i s_j.                            \tag{19}
\]

The canonical contraction is

\[
 \mathcal P(L)=\sigma(L)q+h r(L),\qquad
 \mathcal P(L)q^{[h-1]}=h\sum_iL_{ii}X_i.                \tag{20}
\]

For \(\widehat K=\alpha^{-1}K_*\),

\[
 \sigma(\widehat K)=0,\qquad
 \operatorname {diag}(\widehat K)=(-1,-1,-1),            \tag{21}
\]

because \(a\ne b\).  Dividing (20) only by \(h\) gives (5), with

\[
                         Q=r(\widehat K)=\alpha^{-1}R.    \tag{22}
\]

Expose \(x\), put \(D_x=W\setminus\{x\}\), and write

\[
 q=q_0+\sum_c e_c^{(x)}t_c,\qquad
 Q=\overline Q+\sum_c e_c^{(x)}n_c.                       \tag{23}
\]

With

\[
 A_0=q_0^{[h-1]},\qquad B_0=q_0^{[h-2]},\qquad
 C_{q_0}={{\cal R}_{2h-1}(D_x)\over {\cal R}_1(D_x)A_0}, \tag{24}
\]

the literal \((x,c)\)-row is

\[
                         n_cA_0+\overline Q t_cB_0=-Y_c. \tag{25}
\]

It is convenient to make the target coordinate part of the differential.
Define

\[
 d_c(\ell,Q',\lambda)
       =\ell A_0+Q't_cB_0-\lambda Y_c.                    \tag{26}
\]

Then

\[
                         {\bf e}_{*,c}=(n_c,\overline Q,-1)
                                                               \tag{27}
\]

is a cycle.  Passing to (24) gives (6).  If its representative is changed
without changing the target coordinate \(-1\), the difference is a
targetless same-power row, and its residue is zero.  Thus the cap residue
itself is representative-independent.

This is a cycle attached to the **relation** \(\widehat K\in\ker\sigma\).
It is not automatically an extension out of \(q\).  If \(\tau\ne0\), the
difference of the two normalized cap lifts of \(q\) has response
\(R/(\alpha\tau)\).  If \(\tau=0\), both terms in the cap syzygy lift
zero and there is no radial transition at all.  Therefore the present cap
row does not furnish an extension of \(q\) on which a genuine Yoneda
product could have the claimed uniform value, especially at \(\tau=0\).

## 5. Any Leibniz cup on the comparison cone gives zero

Suppose the full source mapping cone is enhanced by a bilinear chain
product \(\smile\) which includes the augmented target coordinate and
satisfies the Leibniz identity

\[
 d(u\smile v)=du\smile v+(-1)^{|u|}u\smile dv.            \tag{28}
\]

Equations (18) and (27) then give

\[
\begin{aligned}
 (d{\bf g}_{pq,pr})\smile {\bf e}_{*,c}
   &=d({\bf g}_{pq,pr}\smile {\bf e}_{*,c})
     -(-1)^{|{\bf g}_{pq,pr}|}
       {\bf g}_{pq,pr}\smile d{\bf e}_{*,c}\\
   &=d({\bf g}_{pq,pr}\smile {\bf e}_{*,c}).             \tag{29}
\end{aligned}
\]

Thus, under the stated enhancement hypothesis, the ordinary cup of the
four-cut ledger with the cap cycle is a boundary.  Its homology class in
that enhanced comparison cone is zero in every characteristic-zero
specialization, independently of \(\tau\).  Equation (29) proves this
conditional implication; it does not assert existence of the product.

There is also a literal site-degree check.  Every term in (3) belongs to
\({\cal R}_{2h-2}(C_4)\), the top component on \(C_4\).  Hence

\[
        Q|_{C_4}\cdot (\text{left side of (3)})
          \in {\cal R}_{2h}(C_4)=0.                       \tag{30}
\]

The desired class \(-\kappa\overline Y_c\), however, belongs to the
degree-\((2h-1)\) quotient on \(D_x\).  The two sets are related by

\[
 D_5=C_4\setminus\{x\}=D_x\setminus\{r,s\}.              \tag{31}
\]

One natural way to get from the source site set in (30) to the target site
set in (7) is to take the \(x\)-coefficient and then insert the two missing
sites \(r,s\), with all physical labels and all direct/star alternatives.
Formula (13) is the physical five-site sum relevant to that route, but it
is a boundary row, not a canonical inverse or Gysin map.  The degree audit
forces net site-degree \(+1\) and the change from \(C_4\) to \(D_x\); it
does not force this particular factorization through \(D_5\).  No ordinary
multiplication in the site algebra has the required source and target
degrees.

The current data therefore prove two precise no-go statements: literal
ordinary multiplication is zero by (30), and any Leibniz cup satisfying
the hypotheses above is a boundary by (29).  They do not classify
secondary, bivariant, or higher products built from additional data.  No
presently defined operation gives the nonzero value (7).

## 6. The listed same-power anchors lie on the target--residue graph

The obstruction is visible without choosing a chart presentation.  If an
arbitrary literal same-power quadratic row satisfies

\[
                         \Theta q^{[h-1]}
                           =\sum_c\lambda_cX_c,             \tag{32}
\]

then its \((x,c)\)-coefficient and (24) give

\[
                         \rho_c(\overline\Theta)
                              =\lambda_c\overline Y_c.       \tag{33}
\]

Thus the target--residue projection of every cap or diagonal anchor lies
in

\[
          \mathcal G_c=\{(\lambda,\lambda\overline Y_c):
                                    \lambda\in\mathbb C\}. \tag{34}
\]

The connection, normal, curvature, and direct-double rows have zero
physical target.  In the ordinary totalized cone their complete
combination is the boundary (18).  After horizontal projection, its sole
same-power internal carrier is the radial term \(\kappa z\), whose ordinary
odd residue is zero; the \(Dv\)-piece is the connection--normal horizontal
boundary, not an independent target-bearing quadratic response.  Thus the
class induced by the complete overlap packet has target--residue pair
\((0,0)\), also in \(\mathcal G_c\).  Formula (16) is obtained from the
same cap equation (20), so retaining every label and every five-site
coefficient does not enlarge (34).

In units of \(\overline Y_c\), the scalar-zero cap has pair

\[
                         (-1,-1).                           \tag{35}
\]

Multiplying by \(\kappa\) gives \((-\kappa,-\kappa)\).  Any existing
anchor which cancels its target has pair \((+\kappa,+\kappa)\).  Their
sum is

\[
                              (0,0),                        \tag{36}
\]

whereas the requested secondary output would have pair

\[
                              (0,-\kappa).                  \tag{37}
\]

If \(\kappa\overline Y_c\ne0\), (37) is not in \(\mathcal G_c\).  This
proves that no linear combination of the presently available same-power
anchors and ordinary-residue overlap rows supplies the requested
target-cancelled class.

## 7. One possible five-site architecture

The calculation above does not rule out a secondary filtered operation.
It also does not prove that every such operation must use the following
factorization.  The site sets in (31) only force a net map from top degree
on \(C_4\) to odd degree on \(D_x\).  Factoring it as restriction at \(x\)
followed by insertion at \(r,s\) is a natural source-faithful proposal,
not a necessity theorem.  A direct correspondence, a different filtered
enhancement, or a higher operation could in principle realize the same
net degree if separately constructed and checked.

Let \({\mathscr C}_{\mathrm{lit}}\) denote the full all-label source
mapping cone, filtered by the direct-double/normal/curvature/connection
grades in (17), and augmented by the physical target module as in (26).
The following are the data demanded by this proposed route.  If their
domains, compositions, and chain compatibilities were fully constructed,
they would furnish the desired fixed-input value.  No sufficiency theorem
for a globally defined secondary operation is claimed here.

1. **A relative Rees extension.**  Specify a short exact
   sequence of filtered cone quotients in which the filtered boundary
   (18) defines a connecting class with leading coefficient \(+\kappa\).
   Exactness or relative saturation is essential for this Bockstein-style
   realization; the evaluated identity (3) alone does not define a
   Bockstein.
2. **A five-site restriction--insertion cell.**  Specify a bilinear
   chain operation \(\smile_5\), of the correspondence degree dictated by
   the chosen factorization of (31), and a literal five-site chain
   \({\bf H}_{*,c}\) satisfying

   \[
   \partial_{x,c}:{\cal R}_{2h-2}(C_4)\longrightarrow
       {\cal R}_{2h-3}(D_5),\qquad
   I_{rs}:{\cal R}_{2h-3}(D_5)\longrightarrow
       {\cal R}_{2h-1}(D_x).                              \tag{37a}
   \]

   This proposed site correspondence has bidegree \((-1,+2)\), hence net
   site-degree \(+1\); it is not the degree-\(+2\) ordinary multiplication
   by \(Q\).  The insertion \(I_{rs}\) must be defined all-label and must
   use the literal direct/star alternatives in (13), rather than an
   undeclared inverse to coefficient extraction.  The candidate schematic
   chain row for this route is

   \[
   \boxed{
   d{\bf H}_{*,c}
      =(d{\bf g}_{pq,pr})\smile_5{\bf e}_{*,c},
   \qquad
   \operatorname {tgt}(\operatorname {gr}{\bf H}_{*,c})=0,
   \qquad
   \operatorname {ores}_c(\operatorname {gr}{\bf H}_{*,c})
       =-\kappa\overline Y_c.}                            \tag{38}
   \]

   Here \(\operatorname {ores}_c\) is the specified odd associated-grade
   map, not the ordinary residue of the total zero row.  The first equality
   is the proposed Leibniz/nullhomotopy row; the last two equalities fix the
   target sign and the forced normalization, conditional on this operation
   extending the cap residue.  Its connection-normal
   part must send
   \(Dv(zZ_2-(h-2)Z_1)\) to a horizontal boundary.
3. **Conditional uniqueness.**  If the intended output is a
   single-valued pairing, then one must additionally prove that, for every
   other chain \({\bf H}_{*,c}'\) satisfying the same source/target
   requirements,

   \[
       \operatorname {ores}_c
          \bigl(\operatorname {gr}({\bf H}_{*,c}-
          {\bf H}_{*,c}')\bigr)=0.                         \tag{39}
   \]

   Equivalently, for a single-valued operation the odd associated-grade map
   must vanish on the relevant homology of the space of five-site
   nullhomotopy choices.  Without (39), this route gives at best a
   choice-dependent value or an indeterminacy coset.  That may be suitable
   for a deliberately set-valued secondary operation, but it is not the
   claimed scalar pairing unless its indeterminacy is separately controlled.

Equation (38) is a concrete candidate chain-level row, not one more scalar
polynomial consequence of (3): it would supply a push--pull between the
different site sets in (31), retain the physical target augmentation, and
choose a filtered nullhomotopy.  Equation (39) is the corresponding
condition for zero indeterminacy when a single-valued output is required.
The rows (11)--(18), together with all diagonal anchors, prove neither
existence nor uniqueness for this proposal, and they do not prove that
this proposal is the only possible architecture.

Notice that a same-power target companion cannot by itself serve as
\({\bf H}_{*,c}\): by (33) it changes the last coordinate in (38) by
\(+\kappa\overline Y_c\) and forces (36).  Likewise, merely declaring the
left side of (3) to be a Bockstein skips item 1, and multiplying it by the
cap quadratic gives zero by (30).

## 8. Trace zero and the direct-free boundary

### Trace zero

When \(\tau=0\),

\[
                         \widehat K=-I.                    \tag{40}
\]

Equations (21)--(27) remain valid: the cap target is \(-\Delta\), and its
residue is \(-\overline Y_c\) for every label.  Thus the target--residue
graph obstruction and the forced conditional value (7) do not degenerate.

What degenerates is the radial interpretation.  The off-diagonal and
trace terms in the original cap syzygy both have radial symbol zero after
the \(\tau\)-weight is inserted.  There is no transition out of \(q\), and
division by \(\tau\) is unavailable.  Hence at \(\tau=0\) the second input
supplied by the presently listed cap rows is only the relation-level
augmented cycle (27), not an extension out of \(q\).  Calling that cycle an
ordinary extension of \(q\), and then taking a Yoneda product, is
incorrect.  A relation-level secondary operation, perhaps the route (38)
with whatever uniqueness its intended notion requires, could still be
uniform at \(\tau=0\), but it has not been constructed.

### Direct-free boundary

If the second direct block \(A_{pr}\) is zero, the selected entries obey

\[
                         B=0,\qquad D=At,qquad
                         \kappa=AU\ne0.                    \tag{41}
\]

The adjacent-power boundary becomes

\[
 AU\bigl(zZ_1-(h-1)Z_0\bigr)
 +Atv\bigl(zZ_2-(h-2)Z_1\bigr)=0.             \tag{42}
\]

All signs and powers are unchanged.  The power-free triangular identity
(where \(\mathcal C_4\) denotes the curvature-row carrier, not the site set
\(C_4\)) is

\[
                  \mathcal C_4-Dv=AUz                       \tag{43}
\]

has target zero, and its right side is radial.  Therefore its ordinary odd
residue is zero.  It supplies neither the restriction--insertion operation
in (38) nor the indeterminacy vanishing in (39).  The graph obstruction is
now the nonzero class

\[
                              -AU\,\overline Y_c.           \tag{44}
\]

No activity or division on the direct-free chart was used.  Thus the
one-sided boundary still requires some additional secondary mechanism to
produce a nonzero value.  The architecture in Section 7 could be
specialized with \(\kappa=AU\), but the calculation does not prove it is
the unique route.  Direct-freeness is not by itself an escape from the
ordinary-operation no-go.

## 9. Exact scope

The proved statements are:

* the complete all-label five-site cap formula (12)--(16), uniformly for
  \(h\ge3\);
* the exact signs and divided-power factors in (17), and the identification
  of (3) as a boundary in the formal comparison cone (18);
* the site-degree obstruction (30)--(31) to ordinary multiplication;
* the conditional Leibniz-cup implication (29): if the comparison cone is
  given the stated chain product, the product class is zero;
* the same-complement target--residue graph obstruction (32)--(37),
  including every presently listed same-power anchor, with a nonzero no-go
  only when \(\kappa\overline Y_c\ne0\); and
* the unchanged \(\tau=0\) and direct-free ledgers.

The unproved statements are existence of any secondary filtered operation,
existence of the particular Rees and five-site restriction--insertion route
(38), and, if a single-valued operation is intended, the indeterminacy
vanishing (39).  The bidegree \((-1,+2)\) factorization is not proved
necessary.  Therefore the forced number
\(-\kappa\overline Y_c\) remains conditional, not a constructed Yoneda,
Bockstein, or Massey value.

The dependency-free checker
[`verify_five_exposed_site_yoneda_cup_obstruction.py`](../computations/verify_five_exposed_site_yoneda_cup_obstruction.py)
audits the exact all-label five-site cap expansion in both pair charts,
the 15/10/1 matching split, the adjacent-power signs, the conditional
ordinary boundary-cup implication, the target--residue graph, the
\(\tau=0\) cap normalization, and the direct-free specialization.  The
displayed algebraic proofs, not its finite loop in \(h\), are uniform.

The normalization and sign dependencies used here are independently
audited by
[`verify_offdiagonal_same_power_target_residue_lock.py`](../computations/verify_offdiagonal_same_power_target_residue_lock.py),
[`verify_residue_chain_map_radial_transgression.py`](../computations/verify_residue_chain_map_radial_transgression.py),
and
[`verify_adjacent_power_euler_colon_hankel_type.py`](../computations/verify_adjacent_power_euler_colon_hankel_type.py).
