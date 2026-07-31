# The full-nine target locks every scalar-unit radial locus to rank one

## 1. Outcome

Work in the exact intrinsic scalar-unit chart of the independently audited
[projective root sieve](scalar-unit-radial-cap-projective-root-sieve.md).
Thus, on \(2h\) residual sites with \(h\geq3\),

\[
 \alpha\delta_{ia}\delta_{ja}q^{[h]}
       +R_{ij}q^{[h-1]}=\delta_{ij}X_i,
 \qquad R_{ij}=p_i s_j,
 \qquad \alpha\ne0.                                      \tag{1}
\]

These rows force \(q\ne0\): if \(q=0\), either complementary diagonal
row would read \(0=X_i\).  Hence the functional \(\beta\) below is unique.

Put

\[
 Q=q^{[h]},\qquad
 D=\operatorname {span}\{X_0,X_1,X_2\},\qquad
 M(z)=zq^{[h-1]}.                                        \tag{2}
\]

For a cap matrix \(K\), retain

\[
 r(K)=\sum_{i,j}K_{ij}R_{ij},\qquad
 s(K)=\alpha K_{aa},\qquad
 T(K)=\sum_iK_{ii}X_i.                                  \tag{3}
\]

On the radial locus

\[
 {\cal L}=\{K:r(K)\in\mathbb Cq\},\qquad
 r(K)=\beta(K)q,                                        \tag{4}
\]

define the single linear form

\[
                         c=s+h\beta.                     \tag{5}
\]

The literal nine rows impose the following target lock.

> **Theorem 1.1 (full-nine radial target lock).**  On every exact
> intrinsic scalar-unit chart,
>
> \[
>                         \boxed{T(K)=c(K)Q\quad(K\in{\cal L}).}     \tag{6}
> \]
>
> Consequently
>
> \[
>                         \boxed{\operatorname {rank}(s,\beta)\leq1.} \tag{7}
> \]
>
> More precisely:
>
> * if \(Q\notin D\), then \(K_{00}=K_{11}=K_{22}=s=\beta=0\) on
>   \({\cal L}\);
> * if \(Q\in D\), write uniquely
>   \(Q=v_0X_0+v_1X_1+v_2X_2\).  Then on \({\cal L}\)
>
>   \[
>   \boxed{
>   K_{ii}=v_i c,\qquad
>   s=\alpha v_a c,\qquad
>   \beta={1-\alpha v_a\over h}\,c.}                    \tag{8}
>   \]
>
>   This includes \(Q=0\), where \(v_0=v_1=v_2=0\), all three
>   diagonal restrictions and \(s\) vanish, and only the one form
>   \(\beta=c/h\) may survive.

Thus the rank-two hypothesis in the conditional projective sieve is not
something that goodness, support extremality, or four-cut provenance still
has to prove.  It is incompatible with the same literal target row used by
that sieve.  This does not invalidate the conditional theorem; it shows
that its rank-two premise has empty intersection with an exact full-nine
scalar-unit chart.

There is a positive replacement for that route.  Exactly one of the
following holds.

1. \(Q\in D\) and all three \(v_i\) are nonzero.  Then \(q\) itself is an
   exact three-colour source on the residual sites, after one invertible
   diagonal endpoint rescaling.  This is already the order descent.
2. There are a label \(i\) and a literal top functional \(\nu\) such that

   \[
   \nu(Q)=0,\qquad \nu(X_j)=\delta_{ij}.                 \tag{9}
   \]

   The physical matching-power catalecticant

   \[
   \boxed{\lambda_i(z)=\nu\bigl(zq^{[h-1]}\bigr)}        \tag{10}
   \]

   then satisfies

   \[
   \boxed{
   \lambda_i(q)=0,\qquad
   \lambda_i(R_{jk})=\delta_{ij}\delta_{ik}.}            \tag{11}
   \]

   Hence

   \[
                            {\cal L}\subseteq\{K_{ii}=0\}. \tag{12}
   \]

Formula (10) realizes one of the mod-\(\mathbb Cq\) pure response
selectors left abstract in the root-sieve note.  Its direction of
construction is important: first multiply by the actual physical
\(q^{[h-1]}\), then apply a literal top coefficient functional.  No
quadratic dual is extended by hand and pushed through a matching power.

The remaining obstruction is now narrower.  The functional (10) is a
global \((h-1)\)-matching cofactor.  A physical four-cut exposes a lower
adjacent-power layer, typically with \(q^{[h-2]}\).  The nine top rows do
not transgress (10) to that lower layer, and neither good-star injectivity
nor minimum-support/maximum-anchor extremality supplies such a
transgression.  Thus this note gives an exact target-lock theorem and a
source-provenant selector, but not a clean cap in the selector branch.

## 2. The one-line proof of the target lock

The divided-power convention gives

\[
                         q q^{[h-1]}=h q^{[h]}=hQ.        \tag{13}
\]

Contracting (1) by \(K\) gives the literal row

\[
                         s(K)Q+r(K)q^{[h-1]}=T(K).       \tag{14}
\]

For \(K\in{\cal L}\), substitute \(r(K)=\beta(K)q\) and use (13):

\[
 T(K)=\bigl(s(K)+h\beta(K)\bigr)Q=c(K)Q.                \tag{15}
\]

This proves (6).  It also makes the normal form immediate.  If
\(Q\notin D\), then the two lines \(\mathbb CQ\) and \(D\) meet only at
zero.  Since \(T(K)\in D\), equation (15) forces \(c(K)=0\) and
\(T(K)=0\).  Independence of the three target words gives all three
diagonal entries zero.  Hence \(s=0\), and \(c=s+h\beta=0\) gives
\(\beta=0\).

If \(Q\in D\), write \(Q=\sum_i v_iX_i\).  Comparing the independent
\(X_i\)-coordinates in (15) gives

\[
                         K_{ii}=v_i c.                   \tag{16}
\]

The scalar-unit identity \(s=\alpha K_{aa}\) and the definition of \(c\)
then give the other two formulas in (8).  Both \(s\) and \(\beta\) are
multiples of the one form \(c\), proving (7).

This proof uses no cancellation of \(Q\), \(q\), or \(q^{[h-1]}\).  It
remains valid when \(Q=0\), when multiplication by \(q^{[h-1]}\) has a
large kernel, and under arbitrary complex cancellation in every response.

There is also an exact visibility ledger.  When \(Q\in D\), the diagonal
functional \(K_{ii}|_{\cal L}\) is nonzero exactly when both

\[
                         v_i\ne0\quad\hbox{and}\quad c|_{\cal L}\ne0. \tag{17}
\]

When \(Q\notin D\), no diagonal is visible.  Thus both complementary
diagonals can be visible, but only on the same one-dimensional target
coordinate \(c\); their visibility can never turn \((s,\beta)\) into a
rank-two pair.

There is an equivalent exact quotient formulation which keeps radial
equality separate from matching-power torsion.  Let

\[
 {\cal N}=\operatorname {span}\{R_{ij}:(i,j)\ne(a,a)\}
       \subset{\cal A}_2,\qquad
 u=[R_{aa}],\quad v=[q]\quad\hbox{in }{\cal A}_2/{\cal N}. \tag{17a}
\]

If \(x=K_{aa}\), then an actual equality \(r(K)=\beta q\) is equivalent,
after choosing the eight other entries of \(K\), to

\[
                              xu=\beta v.                \tag{17b}
\]

Consequently

\[
 \operatorname {rank}(s,\beta)
   =\dim\{(\alpha x,\beta):xu=\beta v\}.                 \tag{17c}
\]

This dimension is two exactly when \(u=v=0\), namely when both
\(R_{aa}\) and \(q\) belong to the actual response span \({\cal N}\).
The target lock proves that this simultaneous killing cannot occur in an
exact full-nine chart.  No quotient by
\(\operatorname {Ann}(q^{[h-1]})\) appears in (17a)--(17c).

Two boundary readings are useful.  If \(q\in{\cal N}\), take an actual
representation \(r(K)=q\) with \(K_{aa}=0\).  Equations (8) and (15) force
\(Q\in D\) with \(v_a=0\): its top power is supported on the two
complementary target colours.  If instead
\(R_{aa}-\mu q\in{\cal N}\), the corresponding direct-bearing radial cap
has the one fixed response coefficient \(\beta/K_{aa}=\mu\); (15), not a
relation modulo an annihilator, produces the fixed target ratio used in
(23).

## 3. An active radial cap is already a raw order descent

Suppose \(K\in{\cal L}\) has all three diagonal entries nonzero.  Equation
(15) shows that \(c(K)\ne0\), \(Q\in D\), and

\[
                  Q={1\over c(K)}\sum_iK_{ii}X_i.        \tag{18}
\]

Every coefficient on the right is nonzero.  Thus

\[
                         q^{[h]}=\sum_i v_iX_i,\qquad
                         v_0v_1v_2\ne0.                  \tag{19}
\]

Choose one residual site \(u\).  Apply the diagonal map

\[
                         e_i^{(u)}\longmapsto v_i^{-1}e_i^{(u)}     \tag{20}
\]

to the \(u\)-endpoint of every aggregate block of \(q\) incident with
\(u\).  Every residual perfect matching uses exactly one such endpoint, so
the matching tensor in (19) becomes

\[
                              X_0+X_1+X_2.               \tag{21}
\]

Expanding the transformed aggregate cells gives a finite decorated source
on \(2h=N-2\) sites.  Thus, in the minimum-order contradiction setup, the
radial locus contains no active cap at all.  The finite-union lemma then
also says directly that \({\cal L}\) is contained in one of the three
diagonal hyperplanes.  The catalecticant construction below identifies a
source-provenant such hyperplane without appealing only to that abstract
finite-union argument.

Outside the minimum-order setup, the clean condition on a visible radial
line becomes a fixed scalar test rather than a projective family.  Assume
\(Q\in D\), \(c|_{\cal L}\ne0\), and put

\[
                         x=\alpha v_a.                   \tag{22}
\]

If \(x\ne0\), every radial point with \(s\ne0\) has the one response ratio

\[
                         {\beta\over s}={1-x\over hx}.   \tag{23}
\]

The root-sieve polynomial \(P_h(t)=(1+t)^h-1-ht\) therefore reduces to

\[
 \boxed{
 ((h-1)x+1)^h-h^h x^{h-1}=0.}                            \tag{24}
\]

Indeed the left side of (24) is
\((hx)^hP_h((1-x)/(hx))\).  If \(x=0\), the selected diagonal and \(s\)
vanish on the entire radial locus.  Thus the full-nine row replaces a
movable projective ratio by one target coefficient \(x\); it supplies no
root-counting freedom.

## 4. The exact matching-power selector criterion

The nine rows can be rewritten as the multiplication table

\[
 \boxed{
 M(q)=hQ,\qquad
 M(R_{jk})=\delta_{jk}X_j
       -\alpha\delta_{ja}\delta_{ka}Q.}                  \tag{25}
\]

Fix a label \(i\).  A top functional \(\nu\) obeying (9) gives, by
(10),

\[
 \begin{aligned}
 \lambda_i(q)&=h\nu(Q)=0,\\
 \lambda_i(R_{jk})
   &=\delta_{jk}\nu(X_j)
      -\alpha\delta_{ja}\delta_{ka}\nu(Q)
     =\delta_{ij}\delta_{ik}.
 \end{aligned}                                           \tag{26}
\]

This proves (11).  Conversely, suppose a selector with the values (11)
factors through the literal multiplication map as \(\nu M\).  The value on
\(q\) gives \(\nu(Q)=0\), since \(h\ne0\).  The three diagonal rows in
(25) then give \(\nu(X_j)=\delta_{ij}\).  Hence (9) is also necessary.

It follows that the exact criterion is

\[
 \boxed{
 \lambda_i\text{ factors through the full-nine matching-power row}
 \iff
 \begin{cases}
 Q\notin D, &\text{or}\\
 Q=\sum_jv_jX_j\text{ with }v_i=0.
 \end{cases}}                                             \tag{27}
\]

For \(Q\in D\), necessity follows by applying \(\nu\) to
\(Q=\sum_jv_jX_j\): one gets \(0=v_i\).  If \(v_i=0\), the ordinary
physical coefficient functional \(\pi_i\), which selects the constant word
\(X_i\), is already a suitable \(\nu\).

If \(Q\notin D\), choose a standard top word \(Y\notin\{X_0,X_1,X_2\}\)
whose coefficient \(\pi_Y(Q)\) is nonzero and put

\[
       \nu=\pi_i-{\pi_i(Q)\over\pi_Y(Q)}\pi_Y.            \tag{28}
\]

Then (9) holds.  Formula (28) is a finite linear combination of two
literal physical coefficient restrictions.  It is not an arbitrary
functional on the quadratic response space.

Finally, if the first alternative of Section 1 fails, then either
\(Q\notin D\), when every label works in (27), or \(Q\in D\) has a zero
coordinate, when that label works.  This proves the stated direct-descent
or source-provenant-selector dichotomy.  Equation (12) follows without a
factorization argument: for \(K\in{\cal L}\),

\[
                         K_{ii}=\lambda_i(r(K))
                                =\beta(K)\lambda_i(q)=0. \tag{29}
\]

## 5. What “source-provenant” means here

Let \({\cal A}_1\) be the direct sum of the residual one-site colour
spaces.  The functional in (10) induces the honest physical cofactor
pairing

\[
                         B_\nu(u,v)=\nu\bigl(uvq^{[h-1]}\bigr),
                         \qquad u,v\in{\cal A}_1.         \tag{30}
\]

Since \(R_{jk}=p_js_k\), equation (11) is the small matrix identity

\[
                         \boxed{B_\nu(p_j,s_k)=
                                \delta_{ij}\delta_{ik}.} \tag{31}
\]

For a coordinate \(\nu\), every coefficient of \(B_\nu\) is a literal
\((h-1)\)-matching cofactor of \(q\); for (28) it is the displayed linear
combination of two such cofactors.  Thus (31) survives endpoint order,
parallel aggregate cells, and arbitrary complex cancellation.  It is a
legal catalecticant of the actual source.

There is one legal Euler descent from this global table.  Expand the
actual residual quadratic in its decorated aggregate-cell basis,

\[
                              q=\sum_e q_e e,             \tag{31a}
\]

and define the four-form cofactor matrices

\[
                 C_e(j,k)=\nu\bigl(p_js_k\,e\,q^{[h-2]}\bigr).       \tag{31b}
\]

Since \(q q^{[h-2]}=(h-1)q^{[h-1]}\), equations (30)--(31) give

\[
                         \boxed{\sum_e q_e C_e=(h-1)E_{ii}.}         \tag{31c}
\]

Every summand in (31b) is literal: after expanding \(p_j,s_k,e\), it
exposes four residual sites and leaves the actual
\((h-2)\)-matching complement.  In particular some supported cell \(e\)
has \(C_e(i,i)\ne0\).  Thus the full-nine selector forces nonzero physical
four-cut **detection** in the selected channel; it cannot hide entirely in
the top matching power.

Equation (31c) is not the missing transgression.  It is a weighted sum,
permits cancellation in every other entry, and does not identify the
detected star--star coefficient with an oriented
direct--internal curvature coefficient on a common carrier.  In
particular it gives neither an annihilating lower selector nor a value on
the adjacent-power normal class.

This is stronger than the abstract quotient statement

\[
 \widetilde\lambda_i(q)=0,\qquad
 \widetilde\lambda_i(R_{jk})=\delta_{ij}\delta_{ik},     \tag{32}
\]

obtained merely by factoring \(K_{ii}\) through the response quotient.
For a *specified* trapped label, (32) need not factor through \(M\): (27)
is the exact obstruction.  The direct-descent-or-selector theorem succeeds
because it chooses a zero coordinate of \(Q\), rather than insisting on an
arbitrary boundary label furnished by finite-union duality.

The conclusion must nevertheless stop at (31).  It is not legitimate to
rewrite

\[
 \nu(R_{jk}q^{[h-1]})
 \quad\hbox{as}\quad
 \widetilde\lambda_i(R_{jk})\,q^{[h-1]},                 \tag{33}
\]

whose two sides even live in different spaces.  Nor does (31) define the
value of the same functional on \(R_{jk}H\), on an adjacent divided power,
or on a four-cut carrier.  The selector is sourced precisely because the
matching power was applied before \(\nu\); that fact cannot then be
reversed into cancellation of the matching power.

## 6. Why the other exact hypotheses do not restore rank two

The target lock (15) is an equality in the actual full-support tensor
space.  Additional hypotheses cannot turn two proportional functionals
in (8) into independent ones.

* **Good-star injectivity.**  It says that the triples
  \((p_0,p_1,p_2)\) and \((s_0,s_1,s_2)\) are injective endpoint maps.  An
  injective pair is fully compatible with the rank-one cross-pairing
  (31): already \(P=S=I_3\) and \(B=E_{ii}\) give
  \(P^{\mathsf T}BS=E_{ii}\).  Injectivity supplies no lower bound on the
  rank of a particular catalecticant restriction.
* **Minimum aggregate-entry support.**  The known deletion argument uses
  simultaneous vanishing of the unary error and its first normal jet.
  It does not make multiplication by \(q^{[h-1]}\) injective and does not
  alter (15).  Support counts also do not force the global pairing
  \(B_\nu\) to be supported on one exposed four-cut.
* **Maximum-anchor extremality.**  The anchor potential constrains exact
  same-order scalar-unit pivots.  It does not vary \(Q=q^{[h]}\), create a
  second radial target coordinate, or factor the cofactor pairing (30)
  through a lower carrier.
* **Physical four-cut provenance.**  A literal four-cut operation exposes
  sites before top degree and retains a coefficient paired with a lower
  power such as \(q^{[h-2]}\).  Euler expansion (31c) proves that at least
  one such layer detects the selected channel, but it does not supply the
  oriented curvature/adjacent-power comparison.  Polarizing in \(K\) adds
  nothing because (14) is linear in \(K\).  Polarizing \(q\) beyond the
  literal Euler insertion would require an actual source deformation with
  compatible nine rows; none is supplied by (1).

Accordingly the exact missing positive statement is not radial rank two.
It is a **cofactor-to-four-cut transgression**: a source-valid operation
must take the pure global table (31) to a nonzero lower adjacent-power
class while retaining the exceptional \((a,a)\) row and the oriented
four-cut carrier.  The site-square-zero algebra has matching-power torsion,
so this cannot be inferred by cancellation or formal differentiation.

## 7. Sharp response-module guards

The normal form is an identity for every physical source, so no
counterexample is needed to establish it.  Two exact response modules show
that its boundaries and the catalecticant criterion are sharp.  They are
same-power algebraic guards, not Krenn counterexamples and not claimed
physical good-star realizations.

First take \(a=0\), choose \(v_2\ne0\), set

\[
 Q=v_0X_0+v_1X_1+v_2X_2,\qquad
 \beta_0={1-\alpha v_0\over h},                          \tag{34}
\]

and let \(q,R_{00},R_{11}\), and the six off-diagonal responses be
independent.  Define

\[
 R_{22}={\beta_0q-v_0R_{00}-v_1R_{11}\over v_2}.         \tag{35}
\]

Give multiplication by \(q^{[h-1]}\) the table

\[
 \begin{aligned}
 M(q)&=hQ,&M(R_{00})&=X_0-\alpha Q,\\
 M(R_{11})&=X_1,&M(R_{jk})&=0\quad(j\ne k).
 \end{aligned}                                           \tag{36}
\]

Equation (35) then gives \(M(R_{22})=X_2\), so all nine rows hold.  The
radial locus is exactly the line generated by

\[
                         K=\operatorname {diag}(v_0,v_1,v_2),
                         \qquad r(K)=\beta_0q.            \tag{37}
\]

When \(v_0v_1v_2\ne0\), all three diagonal functionals are visible but
\((s,\beta)\) still has rank one.  Taking \(v_1=0\) gives the exact
zero-coordinate boundary and the literal selector \(\pi_1M\).

For the second guard, take \(Q=X_0-2X_1\), make \(q\), the three diagonal
responses, and five off-diagonal response symbols independent, and impose
only

\[
                              R_{01}=R_{02}.              \tag{38}
\]

Use the table (25).  Then

\[
                         {\cal L}=\mathbb C(E_{01}-E_{02}),
                         \qquad \beta=0,                  \tag{39}
\]

so all three diagonal boundaries contain \({\cal L}\).  Abstract quotient
selectors (32) exist for all three labels.  Criterion (27), however, says
that only the label \(2\), the zero coordinate of \(Q\), factors through
the literal matching-power row.  This proves that “some source-provenant
selector” is sharp: the full-nine equations do not source every abstract
selector attached to every containing boundary.

## 8. Scope and exact audit

The target-lock theorem uses only the literal nine rows, divided-power
multiplication, and independence of the three constant-colour words.  It
therefore applies unchanged to a good pair in a minimum-support or
maximum-anchor representative and with all existing physical four-cut data
retained.  Those hypotheses matter only for a continuation from the
selector branch.

The dependency-free
[checker](../computations/verify_scalar_unit_radial_locus_full_nine_target_lock.py)
reconstructs the radial locus as the exact nullspace of
\([R_{ij}\mid-q]\), verifies (6)--(8) in the visible, boundary, transverse,
and \(Q=0\) regimes, audits the fixed-ratio polynomial (24), and solves the
factorization problem (27) by exact rational row reduction.  It includes
response-sign, divided-power-factor, selector-\(q\), and clean-polynomial
mutations.  Every failure is explicit and remains active under
“python -O”.

This is a structural reduction and a legal selector construction.  It is
not a clean-cap theorem, a four-cut transgression, or a proof of Krenn's
conjecture.
