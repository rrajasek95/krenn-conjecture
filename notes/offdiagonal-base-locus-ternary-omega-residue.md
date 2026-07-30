# Off-diagonal inactive endpoints have a universal ternary Omega residue

## 1. Outcome

Let a canonical physical cap line be selected at an off-diagonal entry

\[
             a\ne b,\qquad \alpha=A_{pq}(a,b)\ne0,
             \qquad K_0=E_{ab}.
\]

Write \(\tau=\operatorname {tr}A_{pq}\) and let

\[
                         K_1=\tau E_{ab}-\alpha I              \tag{1}
\]

be its scalar-zero point.  Suppose at least one of the two inactive
endpoints is clean.  Then the clean error on their joining pencil has one
of the exact factorizations

\[
 \begin{array}{c|c}
 K_0\text{ clean}&{\cal E}(tK_0+uK_1)=u\Psi_0(t,u)\\
 K_1\text{ clean}&{\cal E}(tK_0+uK_1)=t\Psi_1(t,u),
 \end{array}
 \qquad \deg\Psi_0=\deg\Psi_1=h-1.                            \tag{2}
\]

After exposing one residual site and passing to the usual odd-site
quotient, the boundary-polar defect of the scalar-zero response is

\[
                  \boxed{\operatorname {res}_{q_0}(r;t_c)
                            =-\alpha\,\overline Y_c}
                 \qquad(c=0,1,2).                              \tag{3}
\]

Thus every surviving colour has the chart-independent normalized class

\[
                  \boxed{\widehat\zeta_c
                    :=\alpha^{-1}\operatorname {res}_{q_0}(r;t_c)
                     =-\overline Y_c.}                         \tag{4}
\]

For two overlapping off-diagonal charts with the same odd complement,
the two normalized classes in (4) agree literally.  No diagonal selected
entry, trace equation, unary target, or complementary binary target is
needed for this transport.  Hence the previously studied
unary--complementary Omega interface extends, on this precise subbranch,
to the base-locus--ternary endpoints supplied by an off-diagonal canonical
line.

If the line has no active clean point, whichever residual in (2) is
available has no zero on \(D(tu)\).  The existing bounded binary Bezout
theorem gives, for \(\nu=0\) or \(1\),

\[
 H\in V^*\otimes\mathbb C[t,u]_{h-1},\qquad
                    \langle H,\Psi_\nu\rangle=(tu)^{h-1}.      \tag{5}
\]

Tensoring (5) with (4) therefore reaches exactly the same one-dimensional
torus--Koszul middle residue as in the diagonal packet.  The remaining
source problem is again to construct the filtered curvature-normal
correction with middle coefficient \(-\widehat\zeta_c\).

If both endpoints are clean, then \(\Psi_0=t\Omega\) and
\(\Psi_1=u\Omega\), with
\(\deg\Omega=h-2\), and (5) sharpens to the familiar certificate

\[
 H'\in V^*\otimes\mathbb C[t,u]_{h-2},\qquad
                    \langle H',\Omega\rangle=(tu)^{h-2}.       \tag{5a}
\]

The two cases in (2) are exhaustive on an all-inactive off-diagonal line.
Its nonconstant coordinate gcd is supported at \(K_0,K_1\), so at least
one of them is clean; arbitrary higher multiplicity is harmless because
only one endpoint factor is removed before applying the bounded theorem.
Thus the off-diagonal **routing into the coefficient residue is complete**.
This is not proof closure: the diagonal selected line, survival of a
nonzero odd target class, and the source-filtered correction remain open.
The conjecture remains open.

## 2. The two off-diagonal endpoint packets

Let the cap leave \(2h\) residual sites, \(h\ge3\), and let \(q\) be the
internal quadratic.  For a cap matrix \(K\), use

\[
 s=s(K),\qquad r=r(K),\qquad F=sq+r,
 \qquad T(K)=\sum_iK_{ii}X_i.                                \tag{6}
\]

The physical row and the denominator-cleared clean error are

\[
 sq^{[h]}+rq^{[h-1]}=T(K),\qquad
                  {\cal E}(K)=F^{[h]}-s^{h-1}T(K).             \tag{7}
\]

At \(K_0=E_{ab}\), off-diagonality gives

\[
 s_0=\alpha,\qquad T_0=0,\qquad
                  F=\alpha q+p_as_b.                          \tag{8}
\]

Cleanliness at this point is equivalent to the exact matching-base-locus
equation

\[
                              F^{[h]}=0.                       \tag{9}
\]

At \(K_1\), direct contraction is zero by its definition.  Since
\(E_{ab}\) has zero diagonal, all three diagonal entries of \(K_1\) are
\(-\alpha\), and \(E_{ab}^2=0\) gives

\[
 \det K_1=(-\alpha)^3\ne0,\qquad
 T_1=-\alpha\Delta_{2h,3}.                                  \tag{10}
\]

Write \(R=r(K_1)\).  The physical equation at this endpoint is always

\[
              Rq^{[h-1]}=-\alpha\Delta_{2h,3}.                 \tag{11}
\]

Thus \(R\ne0\), and no target label has been discarded.  If \(K_1\) is
also clean, its additional equation is

\[
                              R^{[h]}=0.                       \tag{11a}
\]

Only in that specialization is this a ternary nilpotent response packet.

On the ordered pencil \(K(t,u)=tK_0+uK_1\), equations (8)--(10) give

\[
 s(t,u)=\alpha t,\qquad F(t,u)=tF+uR,qquad
 T(t,u)=-\alpha u\Delta_{2h,3}.                              \tag{12}
\]

The activity product is a nonzero scalar multiple of

\[
                               tu^3.                          \tag{13}
\]

Consequently \(D(tu)\) is exactly the active locus on this pencil.

## 3. Exact two-orientation factorization and boundary polar

Without assuming either endpoint clean, expand the clean error using
divided powers:

\[
 \begin{aligned}
 {\cal E}(t,u)
  &=(tF+uR)^{[h]}-(\alpha t)^{h-1}
                         (-\alpha u\Delta_{2h,3})\\
  &=\sum_{j=0}^{h}t^{h-j}u^jE_j,                             \tag{14}
 \end{aligned}
\]

where

\[
\boxed{
\begin{aligned}
E_0&=F^{[h]},\\
E_1&=RF^{[h-1]}+\alpha^h\Delta_{2h,3},\\
E_j&=R^{[j]}F^{[h-j]}\qquad(2\le j\le h).
\end{aligned}}                                             \tag{15}
\]

The coefficient \(E_1\), independent of which endpoint is clean, has the
boundary-polar difference

\[
\boxed{
RF^{[h-1]}-E_1
   =-\alpha^h\Delta_{2h,3}
   =\alpha^{h-1}Rq^{[h-1]}.}                                 \tag{16}
\]

This is the same identity used in the diagonal Omega packet, now with all
three target colours on the scalar-zero side.  It follows only from the
physical scalar-zero row; cleanliness of neither endpoint is used in
(16), and no common matching power has been cancelled.  Relative to
\(K_0\), it is the first inward polar.  Relative to \(K_1\), it is the
order-\((h-1)\) inward jet.  This observation is what makes the two
orientations share one defect.

If \(K_0\) is clean, (9) gives \(E_0=0\), and

\[
 \Psi_0(t,u)=\sum_{j=1}^{h}t^{h-j}u^{j-1}E_j,
 \qquad {\cal E}=u\Psi_0.                                   \tag{16a}
\]

If \(K_1\) is clean, (11a) gives \(E_h=0\), and

\[
 \Psi_1(t,u)=\sum_{j=0}^{h-1}t^{h-1-j}u^jE_j,
 \qquad {\cal E}=t\Psi_1.                                   \tag{16b}
\]

In either case, absence of an active clean point and (13) say precisely
that the available \(\Psi_\nu\) has no zero on \(D(tu)\).  The bounded
certificate theorem at degree \(h-1\) proves (5).  If that residual were
zero, every point would be clean and (13) would supply an active one.

When both (9) and (11a) hold, both endpoint factors occur:

\[
 \Psi_0=t\Omega,\qquad\Psi_1=u\Omega,\qquad
 \Omega=\sum_{j=1}^{h-1}t^{h-1-j}u^{j-1}E_j.                 \tag{16c}
\]

The same argument at degree \(h-2\) proves (5a).

## 4. Odd-site residue and normalization

Expose a residual site \(x\), let \(D\) be the remaining \(2h-1\) sites,
and write

\[
 \begin{aligned}
 q&=q_0+\sum_c e_c^{(x)}t_c,\\
 R&=r+\sum_c e_c^{(x)}n_c.
 \end{aligned}                                               \tag{17}
\]

Put

\[
 A=q_0^{[h-1]},\qquad B=q_0^{[h-2]},\qquad
 C_{q_0}={{\cal R}_{2h-1}(D)\over {\cal R}_1(D)A}.             \tag{18}
\]

For a quadratic \(Z\) and a linear form \(T\), recall

\[
                 \operatorname {res}_{q_0}(Z;T)=[TZB]
                                  \in C_{q_0}.                 \tag{19}
\]

Taking the \(e_c^{(x)}\)-coefficient of (11) gives

\[
                         n_cA+rt_cB=-\alpha Y_c.               \tag{20}
\]

The first term vanishes in (18), so (20) proves (3).  Equivalently,
taking the same coefficient in (16) gives the intrinsic boundary-polar
form

\[
 \boxed{
 \alpha^{h-1}\operatorname {res}_{q_0}(r;t_c)
  =\pi_{q_0}\partial_{x,c}
       \bigl(RF^{[h-1]}-E_1\bigr)
  =-\alpha^h\overline Y_c.}                                  \tag{21}
\]

Division in (4) is only by the nonzero scalar \(\alpha\).  No site form,
quadratic, or divided power is divided out.

## 5. Two-chart transport and exact scope

Take two overlapping off-diagonal physical charts and expose their
respective extra sites so that both use the same odd internal quadratic
\(q_0\) and the same quotient (18).  Let their selected nonzero direct
entries be \(\alpha_0,\alpha_1\).  Formula (3) in the two charts gives

\[
 \alpha_0^{-1}\operatorname {res}_{q_0}(r_0;t_{0,c})
   =-\overline Y_c
   =\alpha_1^{-1}\operatorname {res}_{q_0}(r_1;t_{1,c}).      \tag{22}
\]

This equality is in the unchanged physical target label \(c\); it is not
obtained by independently relabelling the two endpoints.  It is also
compatible with the power-free cap connection, which transports the same
constant-colour residue.

The positive gain is exact: every all-inactive off-diagonal line has one
of the one-sided certificates and the same normalized boundary defect,
without diagonal routing.  When an overlapping off-diagonal chart is
compared, that defect obeys the flat transport law (22).  Combined with
the torus--Koszul reduction at \(d=h-1\), only one middle coefficient of
the source-filtered curvature-normal correction remains inside the routed
coefficient model.  If both endpoints are clean, the same statement uses
the sharper value \(d=h-2\).

Three limitations must remain explicit.

1. This exhausts only the off-diagonal selected line.  The diagonal line
   has unequal scalar-zero target coefficients and a separate trace gate.
2. A colour contributes a nonzero obstruction only when
   \(\overline Y_c\ne0\) in (18); a separate physical routing lemma must
   supply one surviving label.
3. Equations (5) and (22) transport the defect but do not construct the
   filtered overlap correction which cancels its torus--Koszul middle
   coefficient.

Accordingly this note removes a normalization obstacle; it does not modify
the certified proof spine and does not resolve the conjecture.
