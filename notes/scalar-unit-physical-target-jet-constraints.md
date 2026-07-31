# Physical scalar-unit target jets share a four-site carrier, but need not have rank one

## 1. Outcome

Work in the intrinsic scalar-unit chart on \(2h\) residual sites,
\(h\geq3\):

\[
 \alpha\delta_{ia}\delta_{ja}q^{[h]}
      +R_{ij}q^{[h-1]}=\delta_{ij}X_i,
 \qquad R_{ij}=p_i s_j,
 \qquad \alpha\ne0.                                      \tag{1}
\]

On the clean unary branch put

\[
 Q=q^{[h]},\qquad
 G=\alpha q+R_{aa},\qquad
 \Theta_a=G^{[h-1]}-\alpha^{h-1}q^{[h-1]}=R_{aa}H_a,     \tag{2}
\]

where

\[
 H_a=\sum_{m=0}^{h-2}{1\over m+1}
       \alpha^{h-2-m}q^{[h-2-m]}R_{aa}^{[m]}.             \tag{3}
\]

For the complementary labels \(C=\{b,c\}\), write

\[
                         Z_{jk}=R_{jk}\Theta_a
                                  \qquad(j,k\in C).       \tag{4}
\]

At a good scalar-unit pair of a maximum-mutual-anchor representative this
packet is nonzero: if it vanished, the certified
[scalar-unit pivot](scalar-unit-pivot-global-potential-anchor-matching.md)
would raise the anchor potential.
Suppose, as in the target-resonance branch, that every \(Z_{jk}\) is in
\(D=\operatorname {span}\{X_a,X_b,X_c\}\), and put

\[
                 W_\ell=\bigl([X_\ell]Z_{jk}\bigr)_{j,k\in C}.
                                                                  \tag{5}
\]

Physical factorization adds one exact piece of structure which packet-level
linear algebra does not record.  For every target label \(\ell\), define
the bilinear form on residual one-site forms

\[
 \boxed{\quad
 {\mathfrak C}_\ell(u,v)
       =[X_\ell]\bigl(u\,s_a\,p_a\,v\,H_a\bigr).
 \quad}                                                           \tag{6}
\]

Then all four entries of one coefficient matrix are restrictions of the
same literal carrier form:

\[
 \boxed{
                 (W_\ell)_{jk}={\mathfrak C}_\ell(p_j,s_k).
       }                                                          \tag{7}
\]

Moreover, a nonzero entry in (7) exposes four distinct physical sites and
one nonzero coefficient of the *same* \(H_a\)-complement.  This is a legal
common-carrier localization before top matching-power cancellation.

This structure does **not** imply that \(W_\ell\) has rank at most one.
Section 4 gives a six-site rational guard with good endpoint stars, the
clean unary equation, the exceptional \((a,a)\) full-nine row, and literal
\(R_{ij}=p_i s_j\), for which

\[
                         W_b=\begin{pmatrix}0&-1\\-1&0\end{pmatrix},
                         \qquad \det W_b=-1.              \tag{8}
\]

Thus Segre factorization and the full divided-difference carrier do not by
themselves force the \(GL_2\)-absorption ranks from the
[selector--jet criterion](scalar-unit-selector-jet-resonance-generalized-pivot.md),
a monomial packet, or a rank-one target jet.  The guard is deliberately
weaker than (1): it keeps the exceptional row but not the other eight
tensor rows.

There is nevertheless a useful maximum-anchor consequence when the target
packet is already coordinate-monomial.  At a good scalar-unit pair, if all
nine rows hold and

\[
 Z_{bc}=Z_{cb}=0,\qquad
 Z_{bb}=\lambda_bX_b,\qquad Z_{cc}=\lambda_cX_c,          \tag{9}
\]

with no \(X_a\)-leakage, then maximum-anchor extremality forces

\[
 \boxed{
  \bigl(1+\alpha^{1-h}\lambda_b\bigr)
  \bigl(1+\alpha^{1-h}\lambda_c\bigr)=0.}               \tag{10}
\]

Indeed, if both factors were nonzero, the transformed coefficient matrices
would be two transverse nonzero matrix units, so the monomial generalized
pivot would raise the anchor potential.  Thus a diagonal physical
resonance which avoids cross-channel transport must exactly cancel at
least one original target row.  Equation (10) does not exclude that exact
cancellation boundary.

Section 5 gives the sharp row audit.  On six residual sites there is a
good-star, clean-unary, physically factorized packet satisfying **eight of
the nine tensor equations coefficientwise**, with sole residual

\[
                             0-X_c=-X_c.                 \tag{11}
\]

It has

\[
 Z_{bb}=X_b,\qquad Z_{bc}=Z_{cb}=Z_{cc}=0,               \tag{12}
\]

and hence, before the missing row is supplied,

\[
 A_a=0,\qquad A_b=2E_{bb},\qquad A_c=0.                 \tag{13}
\]

This target-only packet is not \(GL_2\)-absorbable.  The missing row cannot
be appended as an abstract target declaration: its physical left side is
literally zero.  If it could be appended without changing the data, then
\(A_c=E_{cc}\), and (13) would become a monomial absorbable packet.  Hence
the complementary diagonal row is exactly the first full-source identity
which this guard omits and which any positive proof must use.  The guard
does not prove that this row alone is sufficient; after it is restored,
the exact-cancellation alternative in (10), target leakage, or a
nonmonomial cross packet can remain.

The net result is a concrete theorem and a sharp no-go, not a clean-cap
theorem or a proof of Krenn's conjecture.

## 2. The common physical carrier

The Segre square is literal in the site-square-zero algebra:

\[
 \begin{aligned}
 R_{jk}R_{aa}
   &=(p_js_k)(p_as_a)\\
   &=(p_js_a)(p_as_k)=R_{ja}R_{ak}.                     \tag{14}
 \end{aligned}
\]

Combining (2), (4), and (14) gives

\[
                         Z_{jk}=p_js_ap_as_kH_a.          \tag{15}
\]

Taking the \(X_\ell\)-coefficient proves (7).  Notice what (7) does and
does not say.  It is a simultaneous factorization of all four entries
through one physical bilinear form, but a restriction of a bilinear form
to two two-dimensional spaces can have rank two.  There is no outer-product
factorization of \(W_\ell\) unless one separately proves that
\({\mathfrak C}_\ell\) has rank one on these star spaces.

The coefficient localization is also exact.  Write \(x_r^d\) for the
colour-\(d\) coordinate at residual site \(r\), and expand the one-site
forms in this basis.  Formula (15) gives

\[
 \begin{aligned}
 [X_\ell]Z_{jk}
   =\sum_{\substack{r,s,t,u\\\text{pairwise distinct}}}
      &(p_j)_{r,\ell}(s_a)_{s,\ell}
        (p_a)_{t,\ell}(s_k)_{u,\ell}\\
      &\mathbin{\cdot}
       [X_\ell/(x_r^\ell x_s^\ell x_t^\ell x_u^\ell)]H_a.
                                                                  \tag{16}
 \end{aligned}
\]

There is no hidden sign or factorial in (16): the four roles are ordered,
while multiplication in the algebra is commutative.  Terms with a repeated
physical site vanish before coefficient restriction.  If the left side is
nonzero, not every scalar summand on the right can be zero.  Therefore some
ordered four-site choice has all four star coefficients nonzero and has a
nonzero \(H_a\)-coefficient on the common complement.

This inference does not select a nonzero curvature coefficient.  A
curvature contains a difference such as
\(\alpha q_{rs}-(p_a)_r(s_a)_s\), whereas (16) only sources the two
transition assignments and the carrier.  Complex cancellation can make
the curvature difference zero even when both assignments in (16) are
nonzero.  Nor does (16) turn a top selector into a lower annihilator.  It
is exactly a carrier localization, no more.

In particular, if a surviving entry is radial,
\(Z_{jk}=\lambda Q\ne0\), choose any nonzero top-word coefficient of
\(Q\) and apply the same expansion as (16).  This still produces a
literal four-site carrier term.  It cannot produce a sourced-selector
detection: every admissible top selector kills \(Q\), and hence also kills
\(Z_{jk}\).  Physical factorization therefore converts radial blindness
into common-carrier localization, not into selector visibility.

## 3. Target matrices and the diagonal-cancellation fork

Put \(q^\sharp=\alpha^{-1}G\).  On the clean unary branch,

\[
                   \alpha(q^\sharp)^{[h]}=X_a.           \tag{17}
\]

For \(j,k\in C\), the full rows and the adjacent-power identity give

\[
 \begin{aligned}
 T_{jk}:=R_{jk}(q^\sharp)^{[h-1]}
   &=R_{jk}q^{[h-1]}+\alpha^{1-h}Z_{jk}\\
   &=\delta_{jk}X_j+\alpha^{1-h}Z_{jk}.                 \tag{18}
\end{aligned}
\]

There is an exact two-form way to display what the full rows add.  Define

\[
 \begin{aligned}
 {\mathfrak B}_\ell(u,v)&=[X_\ell](uvq^{[h-1]}),\\
 {\mathfrak C}_\ell(u,v)&=[X_\ell](u\,s_a\,p_a\,v\,H_a).
 \end{aligned}                                                 \tag{18a}
\]

On the complementary star spaces, the complete top rows say

\[
 \boxed{
 \bigl({\mathfrak B}_\ell(p_j,s_k)\bigr)_{j,k\in C}
       =E_{\ell\ell}^{C},}
                                                               \tag{18b}
\]

while physical factorization says that the adjacent form restricts to
\(W_\ell\).  Hence the target matrix is exactly

\[
 \boxed{
 A_\ell=
   \bigl({\mathfrak B}_\ell+\alpha^{1-h}{\mathfrak C}_\ell\bigr)
       \big|_{\operatorname {span}(p_b,p_c)
                   \times\operatorname {span}(s_b,s_c)}.}          \tag{18c}
\]

The sole \(cc\)-row is the nonzero cofactor pairing

\[
                         {\mathfrak B}_c(p_c,s_c)=1.       \tag{18d}
\]

It does not, by itself, prescribe
\({\mathfrak C}_c(p_c,s_c)\).  Relating the two bilinear forms would be a
genuine adjacent-power transgression; cancelling \(q^{[h-1]}\) does not
provide it.

If the packet is target-valued and
\(T_{jk}=\sum_\ell(A_\ell)_{jk}X_\ell\), then

\[
 \boxed{
 A_\ell=E_{\ell\ell}^{C}+\alpha^{1-h}W_\ell,}          \tag{19}
\]

where \(E_{aa}^{C}=0\), and \(E_{bb}^{C},E_{cc}^{C}\) are
the two complementary diagonal units.  The baseline units in (19) are
precisely where the two complementary diagonal rows of (1) enter.  They
cannot be inferred from factorization (7).

Under (9), equation (19) becomes

\[
 A_a=0,\qquad
 A_b=(1+\alpha^{1-h}\lambda_b)E_{bb},\qquad
 A_c=(1+\alpha^{1-h}\lambda_c)E_{cc}.                  \tag{20}
\]

If both displayed scalars are nonzero, these matrices satisfy the
potential-compatible monomial criterion: endpoint permutations and
diagonal rescalings restore \(E_{bb},E_{cc}\), preserve the coordinate
support graph, and the new direct \(aa\)-edge raises the mutual-anchor
potential.  This contradicts maximum-anchor extremality and proves (10).

A physical collision gives a useful one-hole specialization.  If

\[
                         R_{cc}R_{aa}=0,                 \tag{21}
\]

then (2) gives \(Z_{cc}=0\) without testing or cancelling \(H_a\).  If the
other three entries have the form in (12), the full \(cc\)-row supplies
the untouched matrix unit \(A_c=E_{cc}\).  Hence a noncancelling
\(Z_{bb}=\lambda X_b\) is immediately the monomial case.  The eight-row
guard below realizes (21) literally and shows why dropping just that row
removes this conclusion.

Nothing here rules out

\[
                         \lambda_b=-\alpha^{h-1},         \tag{22}
\]

which makes \(A_b=0\).  Excluding (22), forcing a second target channel,
or producing a cross entry requires an additional lower-carrier/full-row
comparison.  Equation (7) by itself supplies none of these.

## 4. A clean physical rank-two jet

This guard shows sharply that the common bilinear carrier in (7) need not
have rank one.  Take \(h=3\), \(\alpha=1\), labels
\(a=0,b=1,c=2\), and six residual sites \(0,1,\ldots,5\).  Write

\[
 e_{rs}^{d}=x_r^dx_s^d,
 \qquad X_d=x_0^dx_1^d\cdots x_5^d.                     \tag{23}
\]

Set

\[
 \begin{aligned}
 q={}&e_{01}^{a}+e_{23}^{a}+e_{45}^{a}
       -2e_{05}^{b}+e_{25}^{b}+e_{35}^{b},\\
 p_a={}&-x_1^b,&p_b={}&x_0^b,&p_c={}&x_4^b,\\
 s_a={}& x_3^b,&s_b={}&x_0^b,&s_c={}&x_4^b.              \tag{24}
 \end{aligned}
\]

Both star triples are linearly independent.  Put
\(R=R_{aa}=-e_{13}^b\).  The three \(b\)-cells of \(q\) all meet site
\(5\), so their second divided power is zero.  None is an edge of the
\(a\)-matching.  Consequently

\[
 q^{[3]}=X_a,\qquad Rq^{[2]}=0,\qquad R^{[2]}=0.          \tag{25}
\]

Thus the exceptional full-nine row and the clean unary equation both hold:

\[
 q^{[3]}+Rq^{[2]}=X_a,
 \qquad (q+R)^{[3]}=X_a.                                \tag{26}
\]

At adjacent power,

\[
 \Theta_a=(q+R)^{[2]}-q^{[2]}=Rq
          =R\left(q+\tfrac12R\right)=RH_a.              \tag{27}
\]

The two off-diagonal complementary products use four sites and leave the
cell \(e_{25}^b\):

\[
 Z_{bc}=Z_{cb}=-X_b,
 \qquad Z_{bb}=Z_{cc}=0.                                \tag{28}
\]

Their old \(q^{[2]}\)-responses are zero, so the transformed packet is
target-only with

\[
 A_b=\begin{pmatrix}0&-1\\-1&0\end{pmatrix},
 \qquad A_a=A_c=0.                                      \tag{29}
\]

This proves (8).  It also displays the localization (16): for \(Z_{bc}\),
the four star sites are \(0,3,1,4\), in the order
\(p_b,s_a,p_a,s_c\), and the \(H_a\)-complement is the supported cell
\(e_{25}^b\).  The \(cb\)-entry uses the same four sites in the other
endpoint order.

The guard does not satisfy the other eight rows of (1), and no such claim
is made.  It proves exactly that physical Segre factorization, good stars,
clean unary data, and the exceptional row do not force a rank-one target
jet.  It is not a Krenn counterexample.

## 5. The eight-of-nine good-star guard

The stronger row guard again has \(h=3\), \(\alpha=1\), and the notation
(23).  Put

\[
 \begin{aligned}
 q={}&e_{01}^{a}+e_{23}^{a}+e_{45}^{a}
       +e_{14}^{b}+e_{35}^{b},\\
 p_a={}&x_1^b,&p_b={}&x_0^b,&p_c={}&x_1^c,\\
 s_a={}&x_4^b,&s_b={}&x_2^b,&s_c={}&x_3^c.              \tag{30}
 \end{aligned}
\]

The two star triples are linearly independent: \(p_a,p_c\) share a
physical site but use different residual colour coordinates.  Let
\(R=R_{aa}=e_{14}^b\).  The only perfect matching in the support of \(q\)
is the three \(a\)-edges.  Also no pair of \(q\)-cells covers the four
sites complementary to \(R\).  Hence

\[
 q^{[3]}=X_a,\qquad Rq^{[2]}=0,\qquad R^{[2]}=0,          \tag{31}
\]

and therefore

\[
 (q+R)^{[3]}=X_a,qquad
 \Theta_a=Rq=R\left(q+\tfrac12R\right).                 \tag{32}
\]

We now audit all nine tensor rows, not merely their target coefficients.
For \(R_{bb}=x_0^bx_2^b\), the complement is matched uniquely by
\(e_{14}^b,e_{35}^b\), so

\[
                         R_{bb}q^{[2]}=X_b.              \tag{33}
\]

For each of the six off-diagonal \(R_{ij}\), its four-site complement has
no pair of disjoint supported \(q\)-cells.  Thus every off-diagonal tensor
is zero coefficientwise.  The exceptional row is (31).  Finally,
\(R_{cc}=x_1^cx_3^c\) leaves sites \(0,2,4,5\), on which \(q\) has no
two-cell matching.  Therefore

\[
 \begin{array}{c|c}
 (i,j)&\delta_{ia}\delta_{ja}q^{[3]}+R_{ij}q^{[2]}\\ \hline
 (a,a)&X_a\\
 (b,b)&X_b\\
 i\ne j&0\\
 (c,c)&0.
 \end{array}                                             \tag{34}
\]

Equation (34) is an exhaustive polynomial identity in the coloured
site-square-zero basis.  The sole full-nine residual is exactly \(-X_c\),
as asserted in (11).

The physical jet is equally sparse.  In \(Z_{bb}\), the four star factors
occupy sites \(0,4,1,2\), and the only possible carrier cell on the
complement is \(e_{35}^b\).  Thus

\[
                         Z_{bb}=X_b.                     \tag{35}
\]

The other three products vanish by a site collision or by absence of the
last complementary cell.  This proves (12)--(13).

The missing row cannot be treated as an independent packet-level source.
Here

\[
 R_{cc}q^{[2]}=0,
 \qquad R_{cc}R_{aa}=0,
 \qquad Z_{cc}=0.                                       \tag{36}
\]

The middle equality is literal because both \(p_c\) and \(p_a\) occupy
site \(1\).  If the absent identity

\[
                         R_{cc}q^{[2]}=X_c               \tag{37}
\]

were available on these same data, (18) and (35)--(36) would give

\[
 T_{bb}=2X_b,\qquad T_{cc}=X_c,
 \qquad T_{bc}=T_{cb}=0,                                \tag{38}
\]

which is the potential-compatible monomial pivot.  But (36) makes (37)
the contradiction \(0=X_c\).  This is why a packet-level target guard
must not be called a physical exact source, and why the omitted \(cc\)-row
is the minimal additional full-source identity exposed by this example.

## 6. What remains after the row is restored

The two conclusions should not be conflated.

1. Formula (7) is unconditional physical structure.  It gives a common
   four-star carrier and the exact localization (16), but no rank-one or
   curvature conclusion.
2. Formula (10) closes the noncancelling coordinate-monomial subcase at a
   maximum-anchor representative.  It is a real target-matrix constraint
   supplied by the two diagonal baselines in the full rows.
3. The rank-two guard proves that clean unary and the exceptional row do
   not control the carrier rank.
4. The eight-row guard proves that even goodness, physical factorization,
   clean unary data, and every other tensor row do not reconstruct the
   missing complementary target unit.

Accordingly, the minimal next identity must use the restored complementary
diagonal row together with the common carrier to rule out the exact
cancellation boundary (22), force a second/cross target coefficient, or
produce an oriented curvature class on the same four-site restriction.
The top row by itself only supplies the baseline in (19); cancelling a
matching power or declaring the packet coefficient to be an exact source
would be invalid.

## 7. Exact audit

The dependency-free checker
[`verify_scalar_unit_physical_target_jet_constraints.py`](../computations/verify_scalar_unit_physical_target_jet_constraints.py)
implements the coloured site-square-zero algebra over `Fraction`.  It
verifies:

* all nine tensor residuals of (34), including every off-target word;
* both star ranks, the exceptional row, clean unary equation, and exact
  divided-power carrier in both guards;
* the Segre squares in all nine ordered cells;
* the target matrices (13) and (29), including the rank-two determinant;
* literal four-site carrier localization for every stated nonzero jet; and
* sign, direct-coefficient, and divided-power mutations.

Every check raises an explicit runtime error and remains active under
`python -O`.  The six-site guards are smallest in the standing scalar-unit
range \(h\geq3\).  They are exact local guards, not exact ternary sources.
