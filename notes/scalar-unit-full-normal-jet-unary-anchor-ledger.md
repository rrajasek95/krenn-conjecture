# The scalar-unit full normal jet retains one unavoidable comparison class

## 1. Outcome

Fix a minimum-entry-support exact ternary aggregate source, a good physical
pair \(p,q\), and \(2h\) residual sites, with \(h\geq3\).  Suppose that the
direct block at this pair is the intrinsic diagonal scalar unit

\[
                         A_{pq}=\alpha E_{aa},\qquad \alpha\ne0.       \tag{1}
\]

Write the complete nine physical rows as

\[
 \alpha\delta_{ia}\delta_{ja}q^{[h]}
       +R_{ij}q^{[h-1]}=\delta_{ij}X_i,
 \qquad R_{ij}=p_i s_j.                                      \tag{2}
\]

Put

\[
 \begin{aligned}
 G_a&=\alpha q+R_{aa},\\
 U_a&=G_a^{[h]}-\alpha^{h-1}X_a,\\
 \Theta_a&=G_a^{[h-1]}-\alpha^{h-1}q^{[h-1]}.
 \end{aligned}                                                \tag{3}
\]

Here \(U_a={\cal E}(E_{aa})\) is the unary-cap error.  The class
\(\Theta_a\) is the first adjacent-power comparison at that cap.  For an
arbitrary full-nine normal direction \(D=(D_{ij})\) with \(D_{aa}=0\), set

\[
             R_D=\sum_{i,j}D_{ij}R_{ij},\qquad
             T_D=\sum_iD_{ii}X_i.                            \tag{4}
\]

Then the exact clean error on the whole affine normal space is

\[
\boxed{
 \begin{aligned}
 {\cal E}(xE_{aa}+D)
   ={}&x^hU_a+x^{h-1}R_D\Theta_a\\
     &+\sum_{m=2}^h x^{h-m}R_D^{[m]}G_a^{[h-m]} .
 \end{aligned}}                                               \tag{5}
\]

No support choice, isotropic contraction, localization, or cancellation of
a matching power is used in (5).  All nine rows in (2), including the
exceptional \((a,a)\) target row, are retained.

The first normal jet has a literal four-cut factorization.  Define

\[
 H_a=\sum_{\ell=0}^{h-2}{1\over \ell+1}
       \alpha^{h-2-\ell}q^{[h-2-\ell]}R_{aa}^{[\ell]} .       \tag{6}
\]

Then

\[
 \boxed{\Theta_a=R_{aa}H_a,\qquad
 R_{ij}\Theta_a=R_{ia}R_{aj}H_a.}                           \tag{7}
\]

In particular the two complementary diagonal jets are

\[
 R_{bb}\Theta_a=R_{ba}R_{ab}H_a,\qquad
 R_{cc}\Theta_a=R_{ca}R_{ac}H_a.                            \tag{8}
\]

Thus the scalar-unit collision does not erase the first normal datum.  It
moves it into the two-step off-diagonal squares through the selected colour.
This is precisely the level at which a four-cut overlap, rather than another
same-power cap row, has to act.

There is also a uniform order-\(h\) unary-anchor identity:

\[
 \boxed{
 G_a\Theta_a
    =hU_a+(h-1)\alpha^{h-1}R_{aa}q^{[h-1]}.}                 \tag{9}
\]

Consequently

\[
 \Theta_a=0
 \quad\Longrightarrow\quad
 U_a=-{h-1\over h}\alpha^{h-1}R_{aa}q^{[h-1]}.              \tag{10}
\]

The strongest rigidity conclusion is source-level:

\[
 \boxed{(U_a,\Theta_a)\ne(0,0)}                              \tag{11}
\]

at a minimum-entry-support good pair.  Indeed, simultaneous vanishing would
give

\[
                  q^{[h]}=\alpha^{-1}X_a,qquad
                  R_{aa}q^{[h-1]}=0.                         \tag{12}
\]

Then every response slice whose \(p\)-endpoint colour is \(a\) is zero.
Deleting the complete star row \(p_a\) preserves the exact matching tensor
but strictly decreases aggregate entry support, since goodness makes
\(p_a\ne0\).  This contradicts the selected representative.

In particular, if the unary cap \(E_{aa}\) is clean, then

\[
                         U_a=0\quad\Longrightarrow\quad
                         \Theta_a\ne0.                        \tag{13}
\]

This rules out a tempting closing move.  Cleanliness of the unary endpoint
does **not** make its first normal comparison vanish; on the actual selected
source it forces that comparison to survive.

Absence of an active clean cap does not by itself add a relation to (5).
It only says that, for every \(D\) with \(D_{bb}D_{cc}\ne0\), the
vector-valued polynomial obtained from (5) has no common nonzero root in
the corresponding affine line.  A rootless vector polynomial need not
have any vanishing Taylor coefficient.  Hence no order-\(h\) anchor
null-homotopy, smaller ternary source, or source contradiction follows from
root avoidance alone.

The first genuinely missing datum is now explicit: a source-faithful
four-cut/adjacent-power comparison must act on

\[
                         R_{ia}R_{aj}H_a                    \tag{14}
\]

before the common power is collapsed, and relate that class to the terminal
unary anchor \(U_a\) in (5).  The nine same-power rows determine (5), but do
not provide that comparison.  Injectivity of the endpoint stars also does
not make multiplication by the rows faithful on \(H_a\).

This is a reduction, not a proof of the conjecture.

## 2. Derivation of the full normal form

For a cap \(K\), use

\[
 \begin{aligned}
 s(K)&=\langle K,A_{pq}\rangle,\\
 r(K)&=\sum_{i,j}K_{ij}R_{ij},\\
 T(K)&=\sum_iK_{ii}X_i,\\
 F(K)&=s(K)q+r(K),\\
 {\cal E}(K)&=F(K)^{[h]}-s(K)^{h-1}T(K).
 \end{aligned}                                                \tag{15}
\]

Take \(K=xE_{aa}+D\), with \(D_{aa}=0\).  The scalar-unit hypothesis gives

\[
       s(K)=\alpha x,\qquad r(K)=xR_{aa}+R_D,
       \qquad T(K)=xX_a+T_D,\qquad F(K)=xG_a+R_D.            \tag{16}
\]

Contracting (2) against (D) gives the literal identity

\[
                         R_Dq^{[h-1]}=T_D.                    \tag{17}
\]

Expand the first term of (15) in divided powers:

\[
 (xG_a+R_D)^{[h]}
       =\sum_{m=0}^h x^{h-m}R_D^{[m]}G_a^{[h-m]}.             \tag{18}
\]

The \(m=0\) term minus the \(x^hX_a\) target is \(x^hU_a\).
The \(m=1\) term minus the \(x^{h-1}T_D\) target is

\[
 \begin{aligned}
 x^{h-1}\left(R_DG_a^{[h-1]}-\alpha^{h-1}T_D\right)
  &=x^{h-1}R_D
       \left(G_a^{[h-1]}-\alpha^{h-1}q^{[h-1]}\right)\\
  &=x^{h-1}R_D\Theta_a,
 \end{aligned}                                                \tag{19}
\]

where (17) is used without cancelling \(q^{[h-1]}\).  The remaining terms
are exactly the sum in (5).

Formula (5) also gives every mixed normal polar.  For
\(D^{(1)},\ldots,D^{(m)}\) with zero \(aa\)-entry, the multilinear
coefficient in normal order \(m\ge2\) is, with the usual divided-power
polar normalization,

\[
 R_{D^{(1)}}\cdots R_{D^{(m)}}G_a^{[h-m]}.                    \tag{20}
\]

At order one it is \(R_D\Theta_a\).  Thus no information is lost by
restricting (5) to a line, but the full affine form shows that the same
class controls all eight normal directions simultaneously.

## 3. The two-step square in the first jet

The divided-power binomial formula gives

\[
 \begin{aligned}
 \Theta_a
 &=\sum_{k=1}^{h-1}\alpha^{h-1-k}
       q^{[h-1-k]}R_{aa}^{[k]}\\
 &=R_{aa}\sum_{k=1}^{h-1}{1\over k}\alpha^{h-1-k}
       q^{[h-1-k]}R_{aa}^{[k-1]}\\
 &=R_{aa}H_a.
 \end{aligned}                                                \tag{21}
\]

The factor \(1/k\) is forced by
\(R_{aa}R_{aa}^{[k-1]}=kR_{aa}^{[k]}\).  Characteristic zero is used only
in these displayed nonzero integers.

The response quadratics retain their endpoint order, but commute in the
site-square-zero algebra.  Therefore

\[
 R_{ij}R_{aa}
   =(p_is_j)(p_as_a)
   =(p_is_a)(p_as_j)
   =R_{ia}R_{aj}.                                           \tag{22}
\]

Equations (21)--(22) prove (7)--(8).  The equality is literal before any
matching power is used.  Its value may vanish because of physical-site
collisions or cancellation; the statement does not replace it by a formal
nonzero product.

This identifies exactly why the full nine top rows stop one grade too
late.  They determine \(R_{ij}q^{[h-1]}\), while (7) contains all lower
adjacent powers

\[
 R_{ia}R_{aj}q^{[h-2-\ell]}R_{aa}^{[\ell]},
                    \qquad0\le\ell\le h-2.                  \tag{23}
\]

Multiplying a top target row by a positive-degree factor merely kills the
already full-support target.  It does not recover (23).  One must expose a
physical coefficient before top degree, which is precisely a four-cut
overlap operation.

## 4. Euler transport of the unary anchor

Multiply the definition of \(\Theta_a\) by \(G_a\).  Since

\[
                         G_aG_a^{[h-1]}=hG_a^{[h]},            \tag{24}
\]

and the exceptional row of (2) says

\[
                 \alpha q^{[h]}+R_{aa}q^{[h-1]}=X_a,         \tag{25}
\]

one has

\[
 \begin{aligned}
 G_aq^{[h-1]}
 &=\alpha hq^{[h]}+R_{aa}q^{[h-1]}\\
 &=X_a+(h-1)\alpha q^{[h]}.
 \end{aligned}                                                \tag{26}
\]

Substituting (24)--(26) gives

\[
 \begin{aligned}
 G_a\Theta_a
 &=hG_a^{[h]}
       -\alpha^{h-1}\bigl(X_a+(h-1)\alpha q^{[h]}\bigr)\\
 &=hU_a+(h-1)\alpha^{h-1}
       \bigl(X_a-\alpha q^{[h]}\bigr)\\
 &=hU_a+(h-1)\alpha^{h-1}R_{aa}q^{[h-1]},
 \end{aligned}                                                \tag{27}
\]

which is (9).  This calculation is where the exceptional scalar-unit row
is essential.  An isotropic packet that suppresses the \((a,a)\) target
cannot derive (27).

## 5. Simultaneous vanishing contradicts minimal goodness

Assume \(U_a=\Theta_a=0\).  Equation (27), characteristic zero, and
\(\alpha\ne0\) give

\[
                         R_{aa}q^{[h-1]}=0.                   \tag{28}
\]

Equation (25) then gives \(q^{[h]}=\alpha^{-1}X_a\).  The other eight rows
of (2) say

\[
                  R_{aj}q^{[h-1]}=0\quad(j\ne a),
                  \qquad
                  R_{ia}q^{[h-1]}=0\quad(i\ne a).            \tag{29}
\]

Every matching of the original source either uses the direct edge \(pq\),
or uses one \(p\)-star and one \(q\)-star.  Its endpoint-colour-\((i,j)\)
response is exactly \(R_{ij}q^{[h-1]}\).  Equations (28)--(29) therefore
show that every response with \(p\)-endpoint colour \(a\) is the zero
tensor.

Set the complete aggregate row \(p_a\) to zero and leave every other
aggregate block unchanged.  The direct contribution is unchanged, every
response with \(i\ne a\) is unchanged, and every removed response with
\(i=a\) was already zero.  These are tensor equalities after all arbitrary
complex cancellations inside each response slice; no individual matching
summand is being set to zero.  Hence the new aggregate source still has
matching tensor \(\Delta_{B,3}\).

Because \(pq\) is good, the deleted \(p\)-star map is injective.  In
particular \(p_a\ne0\), so setting it to zero removes at least one nonzero
aggregate matrix entry.  This contradicts minimum entry support.  This
proves (11)--(13).

Notice the exact conclusion of the intermediate power identity: (12) is a
unary source on the residual sites, not a smaller ternary source.  It is
the global minimal-support/good-pair condition, rather than unary
impossibility, that yields the contradiction.

## 6. What no-active cleanliness does and does not imply

Suppose first that \(K_0=E_{aa}\) is clean, so \(U_a=0\).  For any normal
direction with \(D_{bb}D_{cc}\ne0\), every \(K_0+zD\), \(z\ne0\), is
active.  Formula (5) becomes

\[
 {\cal E}(K_0+zD)
 =zR_D\Theta_a+
   \sum_{m=2}^hz^mR_D^{[m]}G_a^{[h-m]}.                     \tag{30}
\]

Absence of an active clean cap says only that the coordinates of the
right side have no common root in \(\mathbb C^*\).  It does not say that
its coefficient of \(z\), or any other coefficient, is zero.  Even the
formal vector polynomial \((z,z^2)\) has this root pattern.  Equation (13)
in fact says that the source comparison \(\Theta_a\) itself is nonzero.

If \(E_{aa}\) is dirty, \(U_a\ne0\) remains as the terminal coefficient
of normal order \(h\) when (5) is expanded from the scalar-zero boundary
\(x=0\).  The ordinary collision jets of order at most \(h-1\) cannot see
or remove it.  Formula (9) relates it to \(\Theta_a\) and the exceptional
target row, but it is not a null-homotopy of either term.

Therefore the desired closing implication cannot be

\[
 \text{no active clean cap}\Longrightarrow\Theta_a=0.
                                                                    \tag{31}
\]

Root avoidance supplies a Macaulay/Bezout coefficient certificate, not a
Taylor-coefficient vanishing theorem.  Lifting that certificate through
the source filtration still requires a relation coupling the terms in
(23) to \(U_a\).

A minimal candidate is a literal four-cut chain comparison which, after
one physical coefficient is exposed,

1. retains both endpoint orders in \(R_{ia}R_{aj}\);
2. compares the adjacent powers in \(H_a\) before multiplying to top
   degree;
3. carries the exceptional \((a,a)\) target in (27); and
4. has zero indeterminacy in the relevant odd/source quotient.

Neither star injectivity nor the isotropic dressed rows provide these four
properties.  The existing scalar-unit isotropic guard suppresses the
exceptional row used in (27), and the 80-of-81 guard shows that injective
stars can still miss exactly that coefficient.  Those guards are
consistent with, but do not prove, the full normal ledger above.

## 7. Scope and audit

The theorem assumes only the exact full-nine pair rows until Section 5.
Minimum entry support and goodness are used solely for the non-simultaneous
vanishing statement (11).  No determinant of the cap matrix is used;
activity depends only on its direct scalar and three diagonal target
coordinates.

The dependency-free checker
[`verify_scalar_unit_full_normal_jet_unary_anchor_ledger.py`](../computations/verify_scalar_unit_full_normal_jet_unary_anchor_ledger.py)
verifies (5) symbolically in the formal commuting divided-power algebra,
checks the factor \(1/(\ell+1)\) in (6), audits the Segre square (22) in
all nine ordered cells, and verifies the Euler identity (9) for every
\(2\le h\le64\).  The source-deletion argument in Section 5 is exact prose
reasoning; the checker audits its algebraic input (27) and the scalar-unit
row pattern behind (28)--(29), not
minimum support itself.
