# The \(h=3\) four-hole compound is a tagged normal extension of the Hamming-one polar

## 1. Outcome

Work on six residual sites \(W\) in the complete full-nine system

\[
 a_{ij}q^{[3]}+p_i s_jq^{[2]}=\delta_{ij}X_i .          \tag{1}
\]

Fix an off-diagonal row \((a,b)\), a physical colour \(c\), and put

\[
 \alpha=a_{ab},\qquad R=p_as_b.
\]

On the pure \(c^6\) slice write \(u_x=p_{a,x}(c)\),
\(v_x=s_{b,x}(c)\), and \(Q_{xy}=q_{xy}(c,c)\).  The missing
four-hole layer from the
[rank-two hafnian update](h3-pure-nine-rank-two-hafnian-update-boundary.md)
has an exact marked-site expression.  For every \(x\in W\), there is a
linear functional \(\rho_x^{ab;c}\) on the off-\(x\) linear forms and a
distinguished **response incidence** \(\beta_x^{ab;c}\) such that

\[
 \boxed{
 [X_c]R^{[2]}q={1\over4}\sum_{x\in W}
       \rho_x^{ab;c}(\beta_x^{ab;c}).}                  \tag{2}
\]

With \(K_Q\) normalized as in that note,

\[
 (u^{\{2\}})^{\mathsf T}K_Qv^{\{2\}}
       ={1\over8}\sum_{x\in W}
          \rho_x^{ab;c}(\beta_x^{ab;c}),               \tag{3}
\]

because

\[
 [X_c]R^{[2]}q
       =2(u^{\{2\}})^{\mathsf T}K_Qv^{\{2\}}.          \tag{4}
\]

Thus a convention which calls the divided coefficient itself the
``compound'' absorbs the factor two between (2) and (3).

The ordinary Hamming-one second-polar map is only the pullback of the
same functional along the physical \(q\)-incidence map:

\[
 \boxed{
 \Gamma_x(e)_{ab}
   =\rho_x^{ab;c}(\iota_x^q(e)).}                        \tag{5}
\]

Consequently a sitewise physical incidence lift is sufficient to turn
(2) into a literal contraction of the complete Hamming-one maps:

\[
 \beta_x^{ab;c}=\iota_x^q(\lambda_x)
 \quad\Longrightarrow\quad
 [X_c]R^{[2]}q={1\over4}\sum_x
                  \Gamma_x(\lambda_x)_{ab}.            \tag{6}
\]

The value is independent of the chosen sitewise lift.  A strictly weaker
aggregate condition is already sufficient for the same scalar formula:

\[
 \sum_x\rho_x^{ab;c}
    \bigl(\beta_x^{ab;c}-\iota_x^q(\lambda_x)\bigr)=0
 \quad\Longrightarrow\quad
 [X_c]R^{[2]}q={1\over4}\sum_x
                  \Gamma_x(\lambda_x)_{ab}.            \tag{6a}
\]

Condition (6a) need not lift any individual incidence vector.  In
general the exact new datum relative to the known pullback \(\Gamma_x\)
is the one extension scalar in the augmented map

\[
 \widetilde\Gamma_x(e,t)_{ab}
  :=\rho_x^{ab;c}(\iota_x^q(e)+t\beta_x^{ab;c})
   =\Gamma_x(e)_{ab}+t\nu_x,
 \qquad
 \nu_x:=\rho_x^{ab;c}(\beta_x^{ab;c}).                 \tag{7}
\]

The obstruction to lifting the **incidence vector itself** is exactly the
quotient class

\[
 [\beta_x^{ab;c}]\in
 \operatorname {coker}\!\left(
  \iota_x^q:E_x\longrightarrow({\cal A}_{W\setminus x})_1
                         \right).                       \tag{8}
\]

Here \(E_x\simeq\mathbb C^3\) is the physical label space.  If this class
is nonzero, \(\nu_x\) is one extra extension scalar beyond
\(\Gamma_x=\rho_x\circ\iota_x^q\).  The class is not an if-and-only-if
obstruction to accidentally matching the single scalar \(\nu_x\):
\(\rho_x\) may kill a nonliftable difference, as in the aggregate
condition (6a).

This is a genuine second-response-order operation: one first takes the
first-response-order polar \(\rho_x\), then reinserts the tagged local
response incidence \(\beta_x\).  A cofactor-weighted linear combination
of top rows, including the usual degree-two or degree-three cap-minor
identities, remains first order in \(R\) and does not perform this
reinsertion.

Independently of whether (6) or (6a) holds, the cancellation gate is the
single exact equation

\[
 \boxed{
 \alpha\sum_{x\in W}\nu_x
       =-24 (u^{\{3\}})^{\mathsf T}J_3v^{\{3\}}.}       \tag{9}
\]

Indeed

\[
 \chi_c={\alpha\over4}\sum_x\nu_x
          +6(u^{\{3\}})^{\mathsf T}J_3v^{\{3\}}.       \tag{10}
\]

Neither a sitewise lift nor the weaker aggregate recovery proves (9);
they only express its second-response-order left side through physical
\(\Gamma\)-data.  Conversely, a new source identity could prove (9)
directly without lifting any \(\beta_x\).  The cited Hamming-one
trichotomy, two-chart synchronization, and one selected nonzero curvature
currently supply none of these three conclusions.  They leave low-rank
spoke alternatives; even on the synchronized routed-\(\Gamma\) branch
they prescribe (5), not the appended value \(\nu_x\).  This identifies
the missing map without asserting that the complete physical equations
cannot force cancellation by a new overlap argument.

## 2. The marked-site functional

Fix \(x\in W\), put \(D_x=W\setminus\{x\}\), and scalarize every site of
\(D_x\) at \(c\).  Let \(E_x\simeq\mathbb C^3\) be the physical label
space at \(x\), with its three coordinate-label basis vectors.  In the
five-site square-zero algebra write, first on those basis vectors,

\[
\begin{aligned}
 U_x&=\sum_{y\in D_x}u_yz_y,
 &V_x&=\sum_{y\in D_x}v_yz_y,\\
 Q_x&=\sum_{\{y,z\}\subset D_x}Q_{yz}z_yz_z,
 &L_x(e)&=\sum_{y\in D_x}q_{xy}(e,c)z_y .              \tag{11}
\end{aligned}
\]

Extend \(L_x\) linearly to \(E_x\), and likewise extend
\(e\mapsto\Gamma_x(e)\) linearly from the three complete Hamming-one
rows.  Thus

\[
 \iota_x^q=L_x:E_x\longrightarrow({\cal A}_{D_x})_1    \tag{11a}
\]

is the physical \(q\)-incidence map at the labelled site \(x\).  The
selected response has the exact decomposition

\[
 R_c=U_xV_x+z_x\beta_x^{ab;c},\qquad
 \boxed{\beta_x^{ab;c}=u_xV_x+v_xU_x.}                 \tag{12}
\]

Define

\[
 \rho_x^{ab;c}(\ell)
       =[\ell U_xV_xQ_x]_{z^{D_x}}.                    \tag{13}
\]

The definition of the Hamming-one polar in the routing theorem gives
immediately

\[
 \Gamma_x(e)_{ab}
   =[L_x(e)U_xV_xQ_x]_{z^{D_x}}
   =\rho_x^{ab;c}(L_x(e)),                             \tag{14}
\]

which proves (5) while retaining all three roles:

* \(e\) is the physical label at the marked residual site \(x\);
* \(a,b\) are the two exposed endpoint labels of the selected row; and
* \(c\) is the fixed physical label at every off-\(x\) site.

The new value is explicitly

\[
\begin{aligned}
 \nu_x
  &=[(u_xV_x+v_xU_x)U_xV_xQ_x]_{z^{D_x}}\\
  &=u_x[U_xV_x^{\,2}Q_x]_{z^{D_x}}
    +v_x[U_x^{\,2}V_xQ_x]_{z^{D_x}}.                  \tag{15}
\end{aligned}
\]

The repeated \(V_x\) or repeated \(U_x\) in (15) is the essential tagged
reinsertion.  In contrast, (14) has one star from each of the three
distinct exposed-site roles.  Permuting those three roles, as in
cross-site synchronization, does not create either repeated-star term in
(15).

## 3. Proof of the \(1/4\) and \(1/8\) factors

Let

\[
 C_2=[X_c]R^{[2]}q.
\]

Every monomial contributing to \(C_2\) is a perfect matching with two
response edges and one \(Q\)-edge.  It therefore has exactly four sites
occupied by \(R\).  Mark one of those four sites \(x\).  Once \(x\) is
marked, (12) says that its response edge contributes
\(z_x\beta_x^{ab;c}\); the other response edge is \(U_xV_x\), and the
remaining edge is \(Q_x\).  The marked coefficient is exactly \(\nu_x\).
Every unmarked monomial has four possible marks, with its coefficient
unchanged.  Hence

\[
                         \sum_x\nu_x=4C_2,              \tag{16}
\]

which proves (2).

For completeness, expanding the two response edges into their \(u/v\)
orientations gives

\[
 C_2=2\!\!\sum_{\substack{|I|=|J|=2\\I\cap J=\varnothing}}
 u_Iv_JQ_{W\setminus(I\cup J)}.                         \tag{17}
\]

For a fixed disjoint pair \((I,J)\), the factor \(2=2!\) is the number of
bijections pairing the two \(u\)-sites with the two \(v\)-sites.  Equations
(16)--(17) prove (3)--(4), without a case classification.

There is a useful companion marking identity.  Put

\[
 \sigma_x(\ell)=[\ell(U_xV_x)^{[2]}]_{z^{D_x}}.         \tag{18}
\]

Then, for every fixed site \(x\),

\[
\begin{aligned}
 C_2&=\rho_x(\beta_x)+\sigma_x(L_x(c)),\\
 [X_c]R^{[3]}&=\sigma_x(\beta_x)
       =6(u^{\{3\}})^{\mathsf T}J_3v^{\{3\}}.        \tag{19}
\end{aligned}
\]

The first line separates whether the fixed site is occupied by a response
edge or by the \(Q\)-edge.  The second has only the response occupation.
This \(2\times2\) polar square makes clear that (14) is one corner,
whereas the compound and cubic require the normal column.

## 4. What the complete Hamming-one row does know

The distinction is visible before invoking the routing trichotomy.  For
an arbitrary physical defect label \(e\), define the full response
incidence

\[
 \beta_x^{ab}(e)
   =p_{a,x}(e)V_x+s_{b,x}(e)U_x                         \tag{20}
\]

and the first-hafnian functional

\[
 \eta_x(\ell)=[\ell Q_x^{[2]}]_{z^{D_x}}.              \tag{21}
\]

The coefficient of the complete selected off-diagonal row at the literal
word \(e_xc^{D_x}\) is

\[
 \boxed{
 \alpha\eta_x(L_x(e))
  +\eta_x(\beta_x^{ab}(e))
  +\Gamma_x(e)_{ab}=0.}                                \tag{22}
\]

The three summands respectively place \(x\) on a direct \(q\)-edge, on a
response edge, and on a \(q\)-edge in the response term.  Equation (22)
uses the complete all-word row and has no cancelled matching power.

It determines the contraction of \(\beta_x^{ab}(e)\) against
\(Q_x^{[2]}\).  The four-hole layer instead needs its contraction against
\(U_xV_xQ_x\):

\[
 \eta_x(\beta_x^{ab}(c))
 \quad\hbox{versus}\quad
 \rho_x(\beta_x^{ab;c})=\nu_x.                         \tag{23}
\]

These are different response grades.  Under the bookkeeping scaling
\(R\mapsto tR\), the Hamming polar \(\Gamma_x\) is of order \(t\), the
tagged value \(\nu_x\) is of order \(t^2\), and
\([X_c]R^{[3]}\) is of order \(t^3\).  Thus a linear span of the top rows
or their cofactor-weighted cap-minor combinations cannot become (9)
without an explicit response-dependent reinsertion such as (6), or an
equivalent nonlinear overlap identity.

## 5. The incidence-lift and quotient branches

Let

\[
 T_x=\operatorname {im}\iota_x^q
       \subset({\cal A}_{D_x})_1.                       \tag{24}
\]

If \(\beta_x^{ab;c}\in T_x\), choose \(\lambda_x\) with
\(L_x(\lambda_x)=\beta_x^{ab;c}\).  Equations (14) and (16) give (6).
If two lifts differ, their difference lies in \(\ker L_x\), and (14)
vanishes on that difference, so the contraction is canonical.

If \(\beta_x^{ab;c}\notin T_x\), the existing \(\Gamma_x\) gives only
\(\rho_x|_{T_x}\).  Adjoining \(\beta_x\) increases the incidence domain
by one dimension and requires one extra scalar \(\nu_x\) to specify
\(\rho_x\) on the enlarged span in (7).  This is the exact
normal-incidence quotient branch.  Notice that \(E_x\) has
dimension three while \(({\cal A}_{D_x})_1\) has dimension five; neither
goodness of the two endpoint stars nor a three-site endpoint selector is
a surjectivity statement for \(\iota_x^q\).

For the pure colour \(c\), define the two fixed-label channel sets

\[
\begin{aligned}
 I&=\{i:p_{i,y}(c)\ne0\text{ for some }y\in W\},\\
 J&=\{j:s_{j,y}(c)\ne0\text{ for some }y\in W\},
\end{aligned}                                             \tag{24a}
\]

and put

\[
 F_c=[q^{[3]}]_{c^W},\qquad M_c=E_{cc}-F_ca.             \tag{24b}
\]

Under the routing antecedent

\[
                         a_{I^c,J^c}\ne0,                \tag{24c}
\]

the complete Hamming-one theorem adds the sitewise trichotomy

\[
 \operatorname {rank}P_x\le |I|,\qquad
 \operatorname {rank}S_x\le |J|,\qquad\text{or}\qquad
 \Gamma_x(e)=\delta_{ec}M_c.                            \tag{25}
\]

The first two alternatives are separate low-rank exits.  The last fixes
the pullback (5), but contains no conclusion that (8) vanishes.  More
sharply, on the high-rank route used to prove the third alternative, the
Taylor identity

\[
 M_{x,e}=P_x(e)h^{\mathsf T}+gS_x(e)^{\mathsf T}
                +\Gamma_x(e)                            \tag{25a}
\]

has \(g=h=0\).  The Hamming-one equation then literally forgets the
local endpoint coefficients \(p_{a,x}(c),s_{b,x}(c)\), while (12) uses
exactly those coefficients to form \(\beta_x\).  On two
charts, cross-site synchronization compares coefficients
\([t_ex_iy_jz]_{c^D}\), again the distinct-star corner (14).  Its common-site
consequence \([\Theta z]=0\) is an alternating difference-channel
constraint.  The selected curvature makes the displayed change of normal
forms invertible, but the sharp local guard in the synchronization note
shows that it does not permit cancellation of \(z\).  Likewise, the
[adjacent \(h=3\) transgression audit](adjacent_full_nine_h3_cycle_transgression.md)
identifies the unresolved curvature **sum** channel.  Neither registered
result supplies the repeated-star normal value (15) or its aggregate (9).

Therefore the present exact branch ledger is:

1. close every low-rank spoke exit needed to reach the routed-\(\Gamma\)
   branch;
2. if the chosen route is to recover the compound from physical
   \(\Gamma\)-data, prove the sufficient sitewise lifts (6), or only the
   strictly weaker aggregate scalar equality (6a); and
3. separately prove the cancellation (9), either after such a recovery
   by comparing with the cubic response term, or directly from a new
   source identity without any incidence lift.

In particular, sitewise incidence lifts alone do not imply (9), and
direct cancellation does not logically require them.

This does not assert that all complete full-nine equations leave (8)
free.  It says that the cited trichotomy, synchronization, and curvature
outputs stop exactly before the map which evaluates it.

## 6. A tiny exact grade-separation mutation

The distinction between (22) and (23) already has a six-site monomial
model.  Use scalar sites \(x,0,1,2,3,4\) and put

\[
 q=z_xz_0+z_3z_4,\qquad
 U_t=z_0+t z_x,\qquad V=z_1+z_2,\qquad R_t=U_tV.         \tag{26}
\]

At the tagged site \(x\), allow the three physical \(q\)-incidence rows
to span

\[
 T_x=\operatorname {span}\{z_0,z_3,z_4\}.              \tag{27}
\]

For every \(t\),

\[
 q^{[3]}=0,\qquad R_tq^{[2]}=0,                         \tag{28}
\]

and every selected component \(\Gamma_y(e)_{ab}\) is zero: every possible
monomial repeats a site.  Thus the complete selected off-diagonal
all-word row on this support fibre and its Hamming-one polar data are
unchanged by \(t=0\rightsquigarrow1\).  At \(x\), however,

\[
 \beta_x(0)=0,\qquad
 \beta_x(1)=z_1+z_2\notin T_x,                          \tag{29}
\]

and

\[
 [X_c]R_0^{[2]}q=0,\qquad
 [X_c]R_1^{[2]}q=2,qquad
 \rho_x(\beta_x(1))=2.                                \tag{30}
\]

The six marked values at \(t=1\) are \((2,2,2,2,0,0)\), so their sum is
\(8=4\cdot2\), while the four-hole sum in the normalization of (3) is
one.  This is the promised exact check of both factors.

The mutation can be padded by unused coordinate columns so that both
endpoint star triples remain injective, and a scalar curvature
\(AU-BF=1\) may be chosen on disjoint exposed entries.  It is **not** a
complete nine-row GHZ source: only the selected all-word support fibre and
the polar/grade inference are being guarded.  Its force is correspondingly
narrow: bare \(\Gamma\), goodness, and the numerical fact of nonzero
curvature do not themselves perform the tagged response reinsertion.

## 7. Audit and scope

The dependency-free
[checker](../computations/verify_h3_hamming_one_normal_incidence_compound_transgression.py)
enumerates several deterministic integer pure data sets to verify (2)--(4), (16)--(19),
and (10), then verifies the exact mutation (26)--(30), including the
\(1/4\) and \(1/8\) normalizations and the nonzero incidence-cokernel
class.  It derives the three physical incidence rows from the decorated
\(q\)-blocks, checks the exact rank jump \(3\to4\) after adjoining
\(\beta_x\), and verifies that a physical-incidence mutant replacing one
label row by \(\beta_x\) is correctly recognized as a lift.

The positive theorem here is the marked-site identity and its exact
incidence-lift criterion.  The cancellation (9) remains a required
physical overlap theorem; no conjecture claim is made.
