# The common-coloop corner is a flat odd-site residue

## 1. Outcome

The diagonal curvature corner left in
[the common-coloop reduction](common-coloop-full-nine-residual-coupling.md)
has a canonical lower-degree interpretation. On an odd set \(K\) of
\(2h-1\) sites, put

\[
 A=q_0^{[h-1]},\qquad B=q_0^{[h-2]},\qquad
 C_{q_0}={\cal R}_{2h-1}(K)\big/{\cal R}_1(K)A .        \tag{1}
\]

For a quadratic \(Z\) and a linear form \(T\), define the **odd residue**

\[
             \operatorname {res}_{q_0}(Z;T)
                    =[TZB]\in C_{q_0}.                         \tag{2}
\]

This note proves four exact facts.

1. The residue kills every vertex-gauge quadratic. Thus it is insensitive
   to the genuine source gauge, without cancelling a common power.
2. For a canonical physical pair cap, its residue against a third star is
   exactly its constant-colour target class. All 24 nonconstant triple
   rows have zero residue, while the three constant rows do not.
3. The power-free pair-chart connection transports this residue exactly.
   Both sides are the same constant-colour target; the overlap equation is
   flat rather than contradictory.
4. At a common coloop, the scalar-zero contraction has residue

   \[
      \operatorname {res}_{q_0}(\overline R_*;t_c)
             =-\alpha\,\overline Y_c .                         \tag{3}
   \]

   Consequently every remaining singleton corner, and each of the one or
   two unary corners, is a nonzero gauge-invariant residue class.

This exports the corner from an endpoint-ordered Taylor table to a
canonical overlap class. It does **not** close the conjecture: the
displayed exact connection carries the class unchanged. Therefore the
crossed zero row and the direct connection/Bianchi transport do not kill
it. The next lemma must couple (3) to a branch-specific nonlinear
condition: the clean-error/Omega equations on an inactive-root branch, or
the saturated Macaulay obstruction on a rootless branch. A precise
sufficient interface is stated in Section 7.

## 2. The odd residue and vertex-gauge invariance

Work in the site-square-zero algebra on \(K\), and let

\[
 \mathfrak t_K=\bigoplus_{y\in K}\mathbb C\epsilon_y.
\]

For \(\beta\in\mathfrak t_K\), write \(Z_{q_0}^{\beta}\) for the
vertex-gauge quadratic whose \(yz\)-block is

\[
        (Z_{q_0}^{\beta})_{yz}=(\beta_y+\beta_z)(q_0)_{yz}.
                                                                  \tag{4}
\]

The near-perfect gauge identity gives, for every
\(T\in{\cal R}_1(K)\),

\[
 Z_{q_0}^{\beta}Tq_0^{[h-2]}
   =\left(\left(\sum_{y\in K}\beta_y\right)T
                     -\beta\mathbin\cdot T\right)q_0^{[h-1]}.
                                                                  \tag{5}
\]

Here \((\beta\mathbin\cdot T)_y=\beta_yT_y\). Equation (5) is a
coefficientwise matching identity: after \(T\) fills the unmatched site,
sum the endpoint weights over the \(h-1\) matching edges. Their sum is
\(\sum_y\beta_y-\beta_{\operatorname {site}(T)}\).

The right side of (5) belongs to \({\cal R}_1(K)A\). Hence

\[
 \boxed{\quad
   \operatorname {res}_{q_0}(Z_{q_0}^{\beta};T)=0
   \quad\text{for all }\beta,T.
 \quad}                                                         \tag{6}
\]

Equivalently, (2) defines a linear map

\[
 \Theta_{q_0}:
   {{\cal R}_2(K)\over\Gamma_{q_0}(\mathfrak t_K)}
       \longrightarrow
   \operatorname {Hom}({\cal R}_1(K),C_{q_0}),
 \qquad [Z]\longmapsto(T\longmapsto[TZB]).                     \tag{7}
\]

No injectivity of \(\Theta_{q_0}\) is asserted. Only its exact
gauge-invariance will be used.

## 3. Every physical cap residue is a constant-word selector

Let a pair \(p,q\) be deleted from an exact source, leaving \(2h\) sites.
For endpoint colours \(i,j\), the canonical unnormalized pair cap is

\[
             {\cal P}_{pq}^{ij}=h p_i s_j+a_{ij}q,              \tag{8}
\]

and the complete pair row is

\[
       {\cal P}_{pq}^{ij}q^{[h-1]}
               =h\delta_{ij}X_i.                               \tag{9}
\]

Choose a third site \(x\), let \(K\) be the remaining odd set, and write

\[
 \begin{aligned}
 q&=q_0+\sum_c e_c^{(x)}t_c,\\
 {\cal P}_{pq}^{ij}
   &=P_{pq}^{ij}+\sum_c e_c^{(x)}L_c^{ij}.
 \end{aligned}                                                  \tag{10}
\]

The coefficient at \(e_c^{(x)}\) in (9) is

\[
       L_c^{ij}A+P_{pq}^{ij}t_cB
          =h\delta_{ij}\delta_{ic}Y_i.                         \tag{11}
\]

Reducing modulo \({\cal R}_1(K)A\) removes the normal-row term and gives

\[
 \boxed{\quad
  \operatorname {res}_{q_0}(P_{pq}^{ij};t_c)
       =h\delta_{ij}\delta_{ic}\,\overline Y_i.
 \quad}                                                         \tag{12}
\]

Thus the residue sees precisely the three constant triples
\((0,0,0),(1,1,1),(2,2,2)\). This is an exact full-row statement, not a
selected-word inference. In particular, every nonconstant triple is
already residue-flat.

There is a useful dual scalar form. If \(\overline Y_c\ne0\), choose
\(\lambda\in C_{q_0}^*\) with \(\lambda(\overline Y_c)=1\). Then

\[
       \mathscr T_\lambda(T,U,V)=\lambda(TUVB)                 \tag{13}
\]

is a symmetric, source-provenant trilinear functional. Equation (6)
says that it vanishes whenever the quadratic \(UV\) is replaced by a
vertex gauge. Equation (12) normalizes its constant-word value.

## 4. The power-free connection transports, rather than kills, the residue

Expose three sites \(p,q,x\), with colours \(i,j,c\), and use the same
odd complement \(K\). Let \(y_j\) be the colour-\(j\) star of \(q\) into
\(K\). The literal pair-cap connection is

\[
 P_{pq}^{ij}t_c-P_{px}^{ic}y_j
       =(a_{pq}^{ij}t_c-a_{px}^{ic}y_j)q_0.                    \tag{14}
\]

Multiplying (14) by \(B=q_0^{[h-2]}\) gives on the right

\[
 (h-1)(a_{pq}^{ij}t_c-a_{px}^{ic}y_j)A,
\]

which is zero in \(C_{q_0}\). Therefore

\[
 \boxed{\quad
  \operatorname {res}_{q_0}(P_{pq}^{ij};t_c)
      =\operatorname {res}_{q_0}(P_{px}^{ic};y_j).
 \quad}                                                         \tag{15}
\]

By (12), both sides equal

\[
                  h\delta_{ij}\delta_{ic}\overline Y_i.       \tag{16}
\]

This identifies the precise effect of source-faithful overlap on the
corner. The connection does not impose a second equation on it. It
reindexes the same constant-colour target. The triangle connection and
its first Bianchi relation remain flat for the same reason.

The conclusion is unchanged after adding a vertex-gauge representative
to either cap, by (6). Hence (15) is a genuine quotient transport law,
not a choice of the relative two-label torus gauge.

## 5. Identification with the common-coloop curvature corner

Return to the full-nine common-coloop notation. Thus

\[
 q=q_0+\rho,\qquad
 \rho=\sum_c e_c^{(x)}t_c,
\]

and put

\[
 K_*=\tau E_{ab}-\alpha I,\qquad
 \overline R_*=\sum_{i,j}(K_*)_{ij}\overline p_i\overline s_j,
 \qquad a\ne b,\quad\alpha\ne0.                              \tag{17}
\]

The direct scalar of \(K_*\) is zero. Summing (8) against \(K_*\) and
restricting away from \(x\) gives

\[
             P_{pq}^{K_*}=h\overline R_*.                      \tag{18}
\]

Equations (12) and (18) now give, for each colour \(c\),

\[
 \boxed{\quad
   \operatorname {res}_{q_0}(\overline R_*;t_c)
       =(K_*)_{cc}\overline Y_c
       =-\alpha\overline Y_c.
 \quad}                                                         \tag{19}
\]

Equivalently,

\[
 [\rho\overline R_*B]
       =-\alpha\sum_{c=0}^2e_c^{(x)}\otimes\overline Y_c
       \quad\text{in }V_x\otimes C_{q_0}.                     \tag{20}
\]

Labels in the two kernel supports have \(Y_c\in I\), so their terms in
(20) vanish. What remains is exactly

\[
       -\alpha\sum_{c\in M}
          e_c^{(x)}\otimes\overline Y_c,                        \tag{21}
\]

the curvature quotient in the common-coloop note.

In the disjoint singleton normalization

\[
       \ker P_{\bar x}=\mathbb Ce_r,\qquad
       \ker S_{\bar x}=\mathbb Ce_s,\qquad r\ne s,             \tag{22}
\]

let \(t\) be the third label. The restriction of the off-diagonal term
\(\tau\overline p_a\overline s_b\) in (17), if nonzero, is one of the
three cells

\[
 \overline p_s\overline s_r,\qquad
 \overline p_s\overline s_t,\qquad
 \overline p_t\overline s_r.                                  \tag{23}
\]

The \(q_0\)-term in a canonical cap has zero residue because
\([t_cq_0B]=(h-1)[t_cA]=0\). Thus (12) says that all three products in
(23) have zero residue. Hence the scalar-zero contraction
does not mix the sole corner with an untracked entry:

\[
    \operatorname {res}_{q_0}(\overline R_*;t_t)
       =-\alpha\operatorname {res}_{q_0}
            (\overline p_t\overline s_t;t_t)
       =-\alpha\overline Y_t.                                  \tag{24}
\]

The unary one- and two-corner branches obey the same formula separately
for each missing label. Since the local axes \(e_c^{(x)}\) are
independent, distinct nonzero terms in (21) cannot cancel each other.

It follows from (6) and (19) that every missing label certifies

\[
         [\overline R_*]\ne0
       \quad\text{in}\quad
       {\cal R}_2(K)/\Gamma_{q_0}(\mathfrak t_K).               \tag{25}
\]

This is only a non-gauge conclusion; no injectivity of (7) is needed.

## 6. An actual consecutive-power one-chart guard at \(h=3\)

The odd source and the two known lifts do not themselves exclude the sole
corner. Here is a five-site literal example. Write \(z_{yc}=e_c^{(y)}\)
and take

\[
 \begin{aligned}
 q_0={}&z_{00}z_{10}+z_{20}z_{30}
       +z_{01}z_{21}+z_{11}z_{41}+z_{32}z_{42},\\
 A={}&q_0^{[2]},\qquad B=q_0.
 \end{aligned}                                                  \tag{26}
\]

The only matching in \(A\) which leaves site \(4\) is
\((01)_0(23)_0\), and the only one which leaves site \(3\) is
\((02)_1(14)_1\). Therefore

\[
                  z_{40}A=Y_0,\qquad z_{31}A=Y_1.              \tag{27}
\]

There is no all-colour-2 two-edge matching in \(q_0\), so every element
of \({\cal R}_1A\) has zero coefficient at \(Y_2\). Hence

\[
                         \overline Y_2\ne0.                    \tag{28}
\]

Add a sixth site \(x\), and set

\[
 \begin{array}{lll}
 \rho=e_2^{(x)}z_{02},
 &\overline p_0=0,&\overline p_1=z_{01},
 \quad\overline p_2=z_{12},\\
 &&\\[-1.5ex]
 &\overline s_1=0,&\overline s_0=z_{00},
 \quad\overline s_2=z_{22}.
 \end{array}                                                    \tag{29}
\]

The two endpoint restrictions have rank two, with singleton kernels
\(e_0\) and \(e_1\). Every curvature cell in the quotient rectangle
\(\{1,2\}\times\{0,2\}\) vanishes except the \(22\)-cell: the first row
and first column collide with \(\rho\) at site \(0\), while

\[
 \rho\overline p_2\overline s_2B
     =e_2^{(x)}z_{02}z_{12}z_{22}z_{32}z_{42}=X_2.             \tag{30}
\]

Thus (26)--(30) use one actual quadratic and its literal consecutive
powers, put the two kernel labels in the lift image, and realize exactly
one missing diagonal corner. They are not a full-nine physical source:
no local endpoint rows and direct matrix satisfying all nine equations
are supplied. The example has one purpose. It rules out a proof from
odd-source realizability, rank-two endpoint restrictions, and the two
known lifts alone.

## 7. The sharpened remaining lemma

Equations (15)--(16) show that the direct linear overlap transport is flat
on the corner. A sufficient genuinely new statement is the following.

> **Common-coloop residue--second-polar detection lemma.** Take two
> overlapping source-provenant full-nine charts with nonzero physical
> curvature \(AU-BF\). Impose the simultaneous no-active bad locus in the
> relevant branch: the residual Omega bad locus for inactive roots, or the
> activity-saturated Macaulay bad locus for rootless lines. If a
> common-coloop scalar-zero cap occurs, then on at least one odd overlap it
> satisfies
> \[
>       \operatorname {res}_{q_0}(\overline R_*;t_c)=0
> \]
> for one target colour \(c\) whose monochromatic class is not in
> \({\cal R}_1q_0^{[h-1]}\).

Equation (19) would contradict this conclusion immediately. A stronger,
often easier sufficient conclusion is that the corresponding
\(\overline R_*\) is a vertex-gauge quadratic, because (6) then gives the
displayed vanishing automatically.

At the first inactive-root boundary, where the unary and scalar-zero
endpoints are both clean, its no-active hypothesis says exactly that each
Omega pair is independent or has exactly one zero member. On a rootless
line the Omega formulation is unavailable and must not be inserted by
analogy; the required input is instead the saturated Macaulay
nonexistence condition.

The lemma is not proved here. It is not the conjecture under a new name:
it is restricted to the already-reduced common-coloop scalar-zero stratum
and asks only for the vanishing of one explicit odd-overlap quotient class
from the branch-specific nonlinear equations. Its formulation identifies
exactly what a successful two-chart calculation must add:

* it must use the branch-specific nonlinear bad-locus equations, not only
  the power-free connection or its Bianchi identity;
* it must retain a diagonal constant-word row, since all nonconstant rows
  already have zero residue by (12);
* it may work modulo genuine vertex gauges, by (6), without selecting a
  relative label-torus normalization; and
* it compares literal consecutive-power representatives, so neither the
  abstract Taylor-table guard nor cancellation of \(q_0^{[h-2]}\) enters.

This is the smallest source-faithful interface currently visible between
the common-coloop corner and the two-chart Omega obstruction.
