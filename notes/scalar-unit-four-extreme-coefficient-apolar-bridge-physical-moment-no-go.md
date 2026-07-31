# The four-extreme apolar separator is physical at top occupancy but is not a clean-cap bridge

## 1. Outcome

Work over a characteristic-zero field, and over \(\mathbb C\) when roots
and colour rescalings are used.  For \(h\geq3\), put

\[
 \begin{aligned}
 u(t)&=(1+t)^h-1-ht,\\
 w(t)&=\frac{(1+t)^{h-1}-1}{t},\\
 v(t)&=(t-2)w(t),\\
 x(t)&=1+ht,
 \end{aligned}                                                   \tag{1}
\]

where the displayed quotient defining \(w\) is a polynomial.  The proposed
functional is correct:

\[
 \boxed{
 L_h(f)=(3h-7)[t^0]f-6[t^1]f
       +4(h-1)[t^{h-1}]f-4h(h-1)[t^h]f }
                                                                  \tag{2}
\]

satisfies, uniformly,

\[
 \boxed{L_h(u)=L_h(v)=L_h(tv)=0,
        \qquad L_h(x)=-(3h+7)\ne0.}                              \tag{3}
\]

Thus \(L_h\) is a four-coordinate dual certificate for the universal
carrier module.  It is not, by itself, a clean-point or target
contradiction.

There are two exact reasons.

First, the four displayed coefficients of the literal full normal polynomial
are orders in the affine cap variables \((z,D)\); their response terms are
written in \((G,R_D)\), with \(G=Q+R\).  They are not the formal \(Q/R\)
bidegrees selected by (2).  Even an equality \(R_D=R\) does not identify the
two ledgers by coefficient naming: the change \(Q=G-R\) mixes the source
grades across the full normal-order ledger.
More decisively, in a **full exact source**, if

\[
 D_{aa}=0,\qquad D_{bb}D_{cc}\ne0,\qquad R_D=R_{aa},              \tag{4}
\]

then \(K=D-E_{aa}\) is already an active response-free clean cap.  Hence
the no-active-clean branch cannot contain (4).  A top-apolar equality
modulo \(\operatorname {Ann}(q^{[h-1]})\) is weaker and does not license
this response cancellation.

Second, top physical occupancy does not repair the gap.  Section 5 gives,
for every \(h\geq3\), a literal site-square-zero packet with all of the
following properties:

* \(R=p_as_a\) is a genuine rank-one endpoint-star carrier;
* both endpoint-star triples are injective;
* there is a target-visible normal matrix \(D\) with
  \(D_{aa}=0\), \(D_{bb}=D_{cc}=-1\), and \(R_D=R\);
* one pure full-occupancy coefficient realizes all four weights in (2);
* after ordinary-power normalization,

  \[
       u_h(Q,R)=Qv_{h-1}(Q,R)=Rv_{h-1}(Q,R)=0,
       \qquad x_h(Q,R)=-(3h+7)X_a\ne0;                  \tag{5}
  \]

* the intrinsic unary row can be normalized exactly, its unary cap is
  clean, and its adjacent comparison survives:

  \[
                 U_a=0,
       \qquad R\Theta_a\ne0.                              \tag{6}
  \]

This packet is deliberately **not** a full exact ternary source: the explicit
extension in Section 5 makes every one of the other eight pair rows fail.
If those rows held, (4) would give the clean cap above.  The construction
therefore does not contradict the exact cap lemma, the radial-cap root sieve,
or Krenn's conjecture.  Those results use the contracted identities supplied
by all nine rows, which this packet does not have.  The packet proves
something narrower and useful:
rank-one carrier provenance, endpoint injectivity, the exceptional target
row, clean unary data, and all degree-\(h\) prolongations used by the
four-coefficient separator do not supply the missing full-nine bridge.

The minimal additional input is consequently an annihilator-lifting or
filtered comparison statement.  It must either lift an exposed/top
identity to an actual quadratic equality such as \(R_D=R\), where the
response-free cap closes immediately, or retain the lower-degree oriented
four-cut class before multiplication by \(Q\) and \(R\), with the
exceptional target and zero indeterminacy in the same source filtration.
Separating formal \(Q/R\) grades after evaluation is not such a statement.

## 2. Uniform proof of the four coefficient identities

The only coefficients of \(u\) used by (2) are

\[
 [t^0]u=[t^1]u=0,
 \qquad [t^{h-1}]u=h,
 \qquad [t^h]u=1.                                      \tag{7}
\]

Therefore

\[
                         L_h(u)=4h(h-1)-4h(h-1)=0.       \tag{8}
\]

Write

\[
                 w(t)=\sum_{k=0}^{h-2}{h-1\choose k+1}t^k.         \tag{9}
\]

The four needed coefficients of \(v=(t-2)w\) are

\[
 \begin{aligned}
 [t^0]v&=-2(h-1),\\
 [t^1]v&=(h-1)-2{h-1\choose2}=(h-1)(3-h),\\
 [t^{h-2}]v&={h-1\choose h-2}-2=h-3,\\
 [t^{h-1}]v&=1.
 \end{aligned}                                                   \tag{10}
\]

Substitution gives

\[
 \begin{aligned}
 L_h(v)
  &=(h-1)\bigl[-2(3h-7)-6(3-h)+4\bigr]=0,\\
 L_h(tv)
  &=(h-1)\bigl[12+4(h-3)-4h\bigr]=0.                  \tag{11}
 \end{aligned}
\]

Finally,

\[
                    L_h(x)=(3h-7)-6h=-(3h+7).           \tag{12}
\]

No finite-range calculation is used here.  Characteristic zero ensures
that the last scalar is nonzero.

## 3. What the literal full normal polynomial actually exposes

Use the full-nine scalar-unit notation

\[
 Q=\alpha q,\qquad R=R_{aa},\qquad G=Q+R,
\]

and let \(D_{aa}=0\).  Clearing divided-power factorials in the full
normal-jet formula gives

\[
 \boxed{
 \begin{aligned}
 h!\,{\cal E}(zE_{aa}+D)
   ={}&z^h u_h(Q,R)+h z^{h-1}R_D Rw_{h-2}(Q,R)\\
     &+\sum_{m=2}^h {h\choose m}z^{h-m}
          R_D^mG^{h-m}.
 \end{aligned}}                                                  \tag{13}
\]

Here

\[
 \begin{aligned}
 u_h(Q,R)&=(Q+R)^h-Q^h-hRQ^{h-1},\\
 w_{h-2}(Q,R)&=\frac{(Q+R)^{h-1}-Q^{h-1}}R,
 \end{aligned}                                                   \tag{14}
\]

with the second expression interpreted as its polynomial expansion.

The \(D\)-orders \(m=0,1,h-1,h\), equivalently the coefficients of
\(z^h,z^{h-1},z,1\), in (13) are

\[
 u_h,qquad hR_D Rw_{h-2},qquad
 hR_D^{h-1}G,qquad R_D^h.                               \tag{15}
\]

The index \(m\) counts insertions of the fixed normal direction \(D\)
(or, equivalently, descending powers of \(z\)); it does not count formal
copies of the selected response \(R\).  In particular, the target
subtractions turn the raw orders \(G^h\) and \(hR_DG^{h-1}\) into the
first two expressions in (15).

They are not the four formal source-grade monomials

\[
          Q^h,\quad Q^{h-1}R,\quad QR^{h-1},\quad R^h.          \tag{16}
\]

If \(R_D=R\), the normal basis is \((G,R)\), and
\(Q=G-R\).  Expanding \((G-R)^{h-k}R^k\) uses response orders from \(k\)
through \(h\).  The dual change is explicitly dense.  The response monomial
\(G^{h-j}R^j\) has source dehomogenization \(t^j(1+t)^{h-j}\), and direct
substitution gives

\[
 L_h\bigl(t^j(1+t)^{h-j}\bigr)=
 \begin{cases}
  -(3h+7),&j=0,\\
  -(4h+2),&j=1,\\
  -4j(h-1),&2\leq j\leq h.
 \end{cases}                                             \tag{16a}
\]

Thus the pullback of \(L_h\) uses every \((G,R)\) response order.  For
\(h\geq4\) this includes all intermediate orders omitted by a four-extreme
normal extraction.  For \(h=3\) there are only four orders, but their
transformed weights are still not the four source weights in (2).  A
two-parameter Rees lift could retain the \(Q/R\) grade before this change of
basis, but the evaluated equation at \(Q,R\) does not provide a section of
that lift.

Using the dense transformed functional would not fix the logical issue.
The polynomial in (13) is the cap error, not a polynomial identity equal to
zero for every \(z\).  Unary cleanliness kills its leading coefficient at
one cap, while absence of another clean cap is a common-root avoidance
statement.  Neither condition permits coefficientwise annihilation of
(13).

There is nevertheless an exact and stronger conclusion when the collision
in (4) holds in the physical quadratic algebra.

**Lemma 3.1 (response-free collision cap).**  Assume \(\alpha\ne0\), the
three pure targets are nonzero, and all nine exact rows

\[
 \alpha\delta_{ia}\delta_{ja}q^{[h]}
       +R_{ij}q^{[h-1]}=\delta_{ij}X_i,                 \tag{17}
\]

and let \(D\) satisfy (4).  Then \(K=D-E_{aa}\) is active and clean.

**Proof.**  Contracting (17) against \(D\), and separately taking its
\((a,a)\)-row, gives

\[
 \begin{aligned}
 D_{bb}X_b+D_{cc}X_c&=R_Dq^{[h-1]},\\
 X_a-\alpha q^{[h]}&=Rq^{[h-1]}.
 \end{aligned}                                                   \tag{18}
\]

Since \(R_D=R\),

\[
 D_{bb}X_b+D_{cc}X_c-X_a=-\alpha q^{[h]}.               \tag{19}
\]

For \(K=D-E_{aa}\), the direct scalar, response, target, and residual
quadratic are therefore

\[
 \begin{aligned}
 s(K)&=-\alpha,\\
 r(K)&=R_D-R=0,\\
 T(K)&=-\alpha q^{[h]},\\
 F(K)&=-\alpha q.
 \end{aligned}                                                   \tag{20}
\]

Consequently

\[
 {\cal E}(K)=(-\alpha q)^{[h]}
       -(-\alpha)^{h-1}(-\alpha q^{[h]})=0.             \tag{21}
\]

The three diagonal target coordinates of \(K\) are
\((-1,D_{bb},D_{cc})\), and its direct scalar is nonzero.  Hence (4)
makes \(K\) active.  \(\square\)

This lemma uses the actual quadratic equality \(R_D=R\).  Replacing it by

\[
       (R_D-\lambda R-\mu Q)q^{[h-1]}=0                 \tag{22}
\]

only gives a top-apolar statement.  The exact rows imply

\[
 D_{bb}X_b+D_{cc}X_c
   =\lambda X_a+\alpha(h\mu-\lambda)q^{[h]}.            \tag{23}
\]

If the stronger quadratic equality
\(R_D=\lambda R+\mu Q\) held, the two cap parameters would give

\[
 F(xE_{aa}+yD)=(x+\mu y)Q+(x+\lambda y)R,               \tag{23a}
\]

which is a genuine \(Q/R\) pencil exactly when \(\lambda\ne\mu\).
Equation (22) does not imply (23a); lifting it is precisely the
annihilator problem.

This gives a sharp boundary classification.  If
\(D_{bb}D_{cc}\lambda\ne0\), then either
\(h\mu=\lambda\), which contradicts independence of the three pure
targets, or \(q^{[h]}\) has all three pure target coefficients nonzero.
After independent colour rescaling it is a smaller exact ternary source.
On a minimal-order branch that is impossible.  If \(\lambda=0\) and
\(\mu\ne0\), (23) instead makes \(q^{[h]}\) an exact binary target after
rescaling; exact binary sources are a genuine boundary and cannot be
discarded.  The remaining case \(\lambda=\mu=0\) is impossible, because
(23) would equate the nonzero independent combination
\(D_{bb}X_b+D_{cc}X_c\) to zero.  Thus a weaker apolar carrier plane
neither supplies the response-free cap nor gives a uniform ternary
contradiction.

## 4. Endpoint-star injectivity does not produce or exclude the direction

The condition \(R_D=R\) says that the product map

\[
 \mathbb C^3\otimes\mathbb C^3
       \longrightarrow({\cal A}_W)_2,
 \qquad e_i\otimes e_j\longmapsto p_i s_j              \tag{24}
\]

has a kernel tensor with nonzero \((a,a)\)-entry.  Goodness says only that
the two linear maps \(e_i\mapsto p_i\) and \(e_j\mapsto s_j\) are
injective.  It does not make (24) injective.

There is a uniform construction.  Start with arbitrary nonzero and
linearly independent carrier rows \(P,S\).  Choose linear site forms
\(\eta,\zeta\) such that \(P,\eta,\zeta\) are independent, and choose
\(\eta',\zeta'\) such that \(S,\eta',\zeta'\) are independent.  Require
only that \(\zeta\) and \(\zeta'\) lie at the same physical site, so
\(\zeta\zeta'=0\).  Define

\[
 \begin{array}{lll}
 p_a=P,&p_b=\eta,&p_c=\zeta-P-\eta,\\
 s_a=S,&s_b=\eta',&s_c=\zeta'-S-\eta'.
 \end{array}                                                   \tag{25}
\]

Both star triples are injective, while

\[
 \sum_{i,j}R_{ij}
   =\left(\sum_i p_i\right)\left(\sum_j s_j\right)
   =\zeta\zeta'=0.                                      \tag{26}
\]

Let \(J\) be the all-ones \(3\)-by-\(3\) matrix and put

\[
                         D=E_{aa}-J.                      \tag{27}
\]

Then

\[
 D_{aa}=0,qquad D_{bb}=D_{cc}=-1,qquad
 R_D=R_{aa}-\sum_{i,j}R_{ij}=R_{aa}.                    \tag{28}
\]

This construction is only a star/product packet.  By Lemma 3.1, it cannot
also satisfy all nine exact rows on a no-active-clean branch.  Its purpose
is to show precisely why endpoint injectivity cannot be used either to
infer or to forbid the needed carrier direction; the full source rows do
the decisive work.

## 5. A literal rank-one physical moment realization of \(L_h\)

The following countermodel upgrades the formal coefficient guard to the
site-square-zero algebra while retaining the rank-one carrier shape.

**Theorem 5.1 (physical degree-\(h\) carrier countermodel).**  For every
\(h\geq3\), there are \(2h\) three-colour physical sites, quadratics
\(Q,R\) with \(R=p_as_a\), and a pure target word \(X_a\) such that

\[
                  Q^{h-k}R^k=\ell_kX_a\quad(0\leq k\leq h),          \tag{28a}
\]

where the \(\ell_k\) are the four weights of \(L_h\).  The selected
endpoint stars extend to injective triples admitting the normal direction
(4).  After a nonzero scalar normalization, the exceptional \((a,a)\)
row, unary cleanliness, and the nonzero adjacent comparison all hold, as
do the three top relations in (5).  The complementary eight full-nine
rows do not hold.

Let

\[
 \ell_0=3h-7,qquad \ell_1=-6,qquad
 \ell_{h-1}=4(h-1),qquad
 \ell_h=-4h(h-1),                                      \tag{29}
\]

and put \(\ell_k=0\) at all other indices.  Thus

\[
                         L_h(f)=\sum_{k=0}^h\ell_k[t^k]f.            \tag{30}
\]

Take \(2h\) physical sites in ordered pairs
\((L_i,R_i)\), and retain only the selected colour \(a\) for the moment.
Write \(l_i=e_a^{(L_i)}\), \(r_i=e_a^{(R_i)}\), and

\[
                         X_a=\prod_{i=1}^h l_ir_i.         \tag{31}
\]

Set

\[
 C=\frac{\ell_0}{h!},
 \qquad
 \epsilon_k=\frac{\ell_k}
  {C\,(h-k)!\,(k!)^2}\quad(0\le k\le h).               \tag{32}
\]

Then \(\epsilon_0=1\) and \(\epsilon_h\ne0\).  Over \(\mathbb C\),
choose \(z_1,\ldots,z_h\) with elementary symmetric functions

\[
                         e_k(z_1,\ldots,z_h)=\epsilon_k.  \tag{33}
\]

This is simply the root factorization of the monic polynomial with the
prescribed elementary coefficients.  Choose nonzero \(q_i\) with
\(\prod_iq_i=C\), and define

\[
 Q=\sum_{i=1}^h q_i l_ir_i,qquad
 P=\sum_{i=1}^h l_i,qquad
 S=\sum_{i=1}^h z_iq_i r_i,qquad
 R=PS.                                                   \tag{34}
\]

Thus \(R\) is literally \(p_as_a\).  A direct full-occupancy count gives

\[
 \boxed{Q^{h-k}R^k=\ell_kX_a\qquad(0\le k\le h).}       \tag{35}
\]

Indeed, choose the \(h-k\) diagonal \(Q\)-edges on the complement of a
set \(I\) of size \(k\).  The factors \(P^kS^k\) must occupy exactly the
left and right sites indexed by \(I\).  Their coefficient is

\[
 (h-k)!(k!)^2
   \left(\prod_iq_i\right)\prod_{i\in I}z_i.            \tag{36}
\]

Summing (36) over \(I\) and using (32)--(33) proves (35).  Since all
forms use only colour \(a\), there is no other degree-\(2h\) word.  For
\(f(t)=\sum_{k=0}^h a_kt^k\), write
\(f^{\rm hom}(Q,R)=\sum_{k=0}^h a_kQ^{h-k}R^k\).  Then coefficient
extraction of the literal pure word \(X_a\) satisfies

\[
 [X_a]f^{\rm hom}(Q,R)=L_h(f).                          \tag{37}
\]

This is a legal evaluated physical coefficient, not a declaration that
formal \(Q/R\) grades are independent after evaluation.

Homogenize \(v\) to degree \(h-1\).  Equations (3), (35), and (37) give

\[
 \begin{aligned}
 u_h(Q,R)&=0,\\
 Qv_{h-1}(Q,R)&=0,\\
 Rv_{h-1}(Q,R)&=0,\\
 x_h(Q,R)&=-(3h+7)X_a\ne0.
 \end{aligned}                                                   \tag{38}
\]

Moreover the adjacent comparison is visibly nonzero.  With

\[
 \theta_{\rm ord}=(Q+R)^{h-1}-Q^{h-1},                  \tag{39}
\]

only the \(R^{h-1}Q\) and \(R^h\) moments contribute to
\(R\theta_{\rm ord}\), so

\[
 \begin{aligned}
 R\theta_{\rm ord}
  &=\bigl((h-1)\ell_{h-1}+\ell_h\bigr)X_a\\
  &=-4(h-1)X_a\ne0.                                    \tag{40}
 \end{aligned}
\]

Choose \(\alpha\ne0\) with

\[
                         h!\alpha^{h-1}=-(3h+7),         \tag{41}
\]

and put \(q=Q/\alpha\).  Then (38) is exactly the exceptional scalar-unit
row

\[
                         \alpha q^{[h]}+Rq^{[h-1]}=X_a,  \tag{42}
\]

and its unary clean error is zero.  More precisely, with
\(G_a=\alpha q+R=Q+R\),

\[
 U_a=\frac1{h!}u_h(Q,R)=0,\qquad
 \Theta_a=\frac1{(h-1)!}\theta_{\rm ord},\qquad
 R\Theta_a=-\frac4{(h-2)!}X_a\ne0.                       \tag{42a}
\]

The extension (25)--(28) can be made explicit without adding sites.  Use
the two pairs with indices \(1,2\) and set

\[
 \eta=e_b^{(L_1)},\qquad \eta'=e_b^{(R_1)},\qquad
 \zeta=e_b^{(L_2)},\qquad \zeta'=e_c^{(L_2)}.             \tag{43}
\]

Then \(\zeta\zeta'=0\), while \(P,\eta,\zeta\) and
\(S,\eta',\zeta'\) are independent.  Thus both ordered endpoint stars are
injective and \(D=E_{aa}-J\) has \(R_D=R\), exactly as in (28).

This same choice visibly fails every complementary row, not merely their
conjunction.  Put \(d_i=q_i/\alpha\),
\(\sigma_i=z_iq_i\), and
\(\rho_i=\prod_{r\ne i}d_r\).  All three kinds of scalars are nonzero:
\(\prod_iq_i=C\ne0\), \(\alpha\ne0\), and
\(\prod_i z_i=e_h(z)=\epsilon_h\ne0\).  Let \(W_i^{cd}\) denote the
full word which has colours \(c,d\) at \(L_i,R_i\) and colour \(a\) at
every other site.  In the indicated top response, the following
coefficients are respectively

\[
\begin{array}{c|cccccccc}
 (i,j)&ab&ac&ba&bc&ca&cb&bb&cc\\ \hline
 \text{word}&W_1^{ab}&W_1^{ab}&W_1^{ba}&W_1^{bb}
             &W_2^{ba}&W_1^{ab}&W_1^{bb}&W_2^{ba}\\
 [W]\,R_{ij}q^{[h-1]}
     &\rho_1&-\rho_1&\sigma_1\rho_1&-\rho_1
     &\sigma_2\rho_2&-\rho_1&\rho_1&-\sigma_2\rho_2 .
\end{array}                                                   \tag{44}
\]

The six off-diagonal rows therefore have nonzero left sides instead of
zero.  The last two displayed words are not the pure words \(X_b,X_c\),
so both complementary diagonal rows fail as well.  Only the exceptional
\((a,a)\)-row (42) is imposed.

Consequently the packet is explicitly not a full exact source.  In
particular, although its quadratic direction makes
\(r(D-E_{aa})=0\), the absent companion rows do not identify
\(T(D-E_{aa})\) with \(-\alpha q^{[h]}\).  Thus neither Lemma 3.1 nor the
radial-cap root sieve declares this response-free cap clean.

The scope of (38) is also exact.  It realizes the degree-\(h\)
prolongations \(Qv\) and \(Rv\); it does not assert that the lower-degree
tensor \(v\) itself vanishes on every two-site complement.  A literal
four-cut theorem which proves that stronger compatible family would add
new information and would exclude this packet.  Merely multiplying an
exposed relation back to top occupancy, or summing its occupancies before
retaining provenance, does not.

## 6. The minimal missing bridge

The four-extreme functional can be used safely in either of two ways, but
neither is currently supplied by the scalar-unit ledger.

1. **Actual normal lift.**  Construct a target-visible \(D\) in the
   physical quadratic algebra with \(R_D=R\).  Lemma 3.1 then gives an
   active clean cap immediately.  It is not necessary to apply \(L_h\).
   A statement only after multiplication by \(q^{[h-1]}\) is insufficient;
   the required new assertion is an annihilator/colon lifting theorem.
2. **Filtered four-cut lift.**  Retain the lower-degree oriented carrier
   before its \(Q\)- and \(R\)-prolongations, prove compatibility on every
   complementary occupancy, and carry the exceptional \((a,a)\) target
   through the same source filtration.  Different Rees lifts must have
   zero residue difference.  This is the existence and zero-indeterminacy
   datum absent from a formal grade split.

The packet in Section 5 is a sharp unit test for either proposal.  Any
claimed theorem based only on endpoint injectivity, the exceptional row,
unary cleanliness, and top prolonged carrier equations must also apply to
that packet and is therefore false.  A valid theorem must visibly use one
of the omitted full-nine or lower-degree source-provenance hypotheses.

## 7. Audit

The dependency-free checker
[`verify_scalar_unit_four_extreme_coefficient_apolar_bridge_physical_moment_no_go.py`](../computations/verify_scalar_unit_four_extreme_coefficient_apolar_bridge_physical_moment_no_go.py)
checks (3) for \(3\le h\le128\), the factorial-normalized physical moment
construction (32)--(38), the surviving adjacent comparison (40), the
literal site-square-zero count for \(h=3,4\), the dense basis change
\(Q=G-R\), the response-free cap algebra, and the injective-star
construction (25)--(28) together with all eight witnesses in (44).  It uses
explicit exceptions rather than Python assertions, runs unchanged under
`python -O`, and rejects independent mutations of every extreme weight,
the source/normal grade identification, the moment and \(\alpha\)
factorials, the shifted carrier generator, the target sign, the endpoint
order, and the normal matrix sign.

The checker audits exact algebra and Vieta data.  Existence of the
\(z_i\) in (33) and of \(\alpha\) in (41) uses algebraic closure of
\(\mathbb C\), not numerical root finding.
