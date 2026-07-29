# The two-deletion quotient is a nilpotent two-step algebra, not `C^3`

## Outcome

The nine two-deletion caps do have a natural associative quotient, but its
associativity goes in the opposite direction from the hoped-for semisimple
argument.  If

\[
 h=q^{m-2},\qquad I=\operatorname {Ann}(h),\qquad
 \mathcal A=\mathcal R_W/I,
\]

then multiplication by `h` identifies `A_2` with the image of the source
Hessian.  However, `h` already has degree two below the top degree, so

\[
 \mathcal A=\mathbb C\oplus\mathcal A_1\oplus\mathcal A_2,
 \qquad \mathcal A_1\mathcal A_2=0,
 \qquad (\mathcal A_+)^3=0.                               \tag{1}
\]

Thus every associator involving the cap classes vanishes tautologically.
The nine equations give, modulo the line spanned by the internal quadratic,
a diagonal **three-space isotope**.  They do not identify the two degree-one
spaces and the degree-two output space as one algebra, and the actual
quotient has no nontrivial idempotents at all.

This is sharp at the abstract quotient level.  There is an eight-dimensional
commutative associative model of Hilbert function `(1,3,4)` with nonzero
`Q` independent of the three target lifts, full colour symmetry,
deleted-endpoint reflection symmetry, and all nine cap equations.  It is a
local algebra whose radical has cube zero.  A universal eleven-dimensional
version realizes every asymmetric direct-pair matrix `a_cd` and transforms
to its transpose under endpoint reversal.

Consequently the quotient/image algebra cannot yield a uniform
semisimple-`C^3` contradiction.  A successful use of the two-deletion
system must retain additional physical information discarded by this
quotient: the site multigrading, the relations `V_i^2=0` at specified sites,
and especially that `h` is the power `q^(m-2)` of the same distinguished
quadratic.

## 1. The full nine-cap system

Let `|B|=2m`, delete vertices `u,v`, and put

\[
 W=B\setminus\{u,v\},\qquad |W|=N=2m-2.
\]

Work in the site-square-zero algebra

\[
 \mathcal R_W=\bigotimes_{w\in W}(\mathbb C\oplus V_w),
 \qquad V_wV_w=0,                                        \tag{2}
\]

graded by the number of occupied sites.  Write the full quadratic as

\[
 Q_{\rm full}=q+\sum_cx_{v,c}p_c+\sum_dx_{u,d}s_d
                 +\sum_{c,d}a_{cd}x_{v,c}x_{u,d}.        \tag{3}
\]

Here `q in R_2`, while `p_c,s_d in R_1`; endpoint order is retained, so the
matrix `(a_cd)` is arbitrary and need not be symmetric.  Put

\[
 \mathcal H_q:\mathcal R_2\longrightarrow\mathcal R_N,
 \qquad \mathcal H_q(Z)=Zq^{m-2}.                         \tag{4}
\]

Harmless factorial normalizations can be included in (4).  With the
normalization in `source-derivative-hessian-dichotomy.md`, extracting the
nine colour pairs at `u,v` gives

\[
 \boxed{\quad
 \mathcal H_q\bigl(a_{cd}q+(m-1)p_cs_d\bigr)
      =(m-1)!\,\delta_{cd}X_c,
 \quad c,d=0,1,2,\quad}                                  \tag{5}
\]

where `X_c=product_(w in W)x_(w,c)`.  Rescaling (4) or the `X_c` removes
the displayed factorial; none of the conclusions below depends on it.  For
clarity, Sections 2--5 absorb it into `X_c` and write

\[
 \mathcal H_q\bigl(a_{cd}q+\kappa p_cs_d\bigr)
      =\delta_{cd}X_c,
 \qquad \kappa=m-1.                                      \tag{6}
\]

All nine equations for one fixed deleted pair determine every coefficient
of the original matching tensor.  Therefore an actual physical
`q,p,s,a` countermodel to (6) would already be a full ternary source, not a
mere local gadget.  The countermodels below concern the proposed
**quotient-algebra inference** from (6), not physical realizability.

## 2. The canonical annihilator quotient

Set

\[
 h=q^{m-2}\in\mathcal R_{N-2},\qquad
 I=\operatorname {Ann}_{\mathcal R_W}(h)
   =\{z:zh=0\},\qquad
 \mathcal A=\mathcal R_W/I.                              \tag{7}
\]

The diagonal equations in (6) have nonzero right sides, so `h != 0`.
Consequently `I cap R_0=0` and `A_0=C`.

**Theorem 2.1 (two-step quotient theorem).**  The ideal `I` is homogeneous,

\[
 I_2=\ker\mathcal H_q,\qquad
 \overline{\mathcal H}_q:\mathcal A_2
          \mathbin{\mathop{\longrightarrow}^{\sim}}
          \operatorname {im}\mathcal H_q,                \tag{8}
\]

and

\[
 \mathcal A_k=0\quad(k\ge3),\qquad
 \mathcal A_1\mathcal A_2=0,qquad
 (\mathcal A_+)^3=0.                                    \tag{9}
\]

In particular `A` is a local commutative associative algebra with residue
field `C`, and it contains no semisimple algebra `C^r` for any `r>1`.

**Proof.**  The annihilator of any element is an ideal.  Since `h` is
homogeneous, its annihilator is homogeneous, and (8) is the first
isomorphism theorem applied in degree two.

The maximum nonzero degree of the site-square-zero algebra is `N`.  If
`z in R_k` with `k>=3`, then `zh` has degree

\[
                         k+(N-2)>N,
\]

so it is zero.  Thus `R_k subset I` for every `k>=3`, proving (9).
The positive-degree ideal `A_+=A_1 direct-sum A_2` is nilpotent, and the
quotient by it is `C`, so `A` is local.

For completeness, a local algebra with nilpotent maximal ideal has only
the idempotents zero and one.  If `e=alpha+n`, with `n in A_+`, then
`e^2=e` first gives `alpha in {0,1}`.  For `alpha=0`, an idempotent which is
nilpotent is zero.  For `alpha=1`, the equation is
`n(1+n)=0`; the element `1+n` is invertible, so again `n=0`.  Since
`C^r` has nontrivial idempotents for `r>1`, it cannot embed as a unital
subalgebra. `QED`

Theorem 2.1 applies to every `q`, including every Hessian degeneracy.  It
also identifies the precise mistake in quotienting only the degree-two
vector space and then guessing a semisimple product: the genuine
associative quotient exists, but it is a two-step graded local algebra.
Its degree-two part lies in the socle; in degenerate charts the socle may
also contain degree-one classes.

## 3. What the nine caps actually force

Use capital letters for classes in `A`:

\[
 Q=[q],\qquad P_c=[p_c],\qquad S_d=[s_d].                 \tag{10}
\]

Each `X_c` belongs to `im H_q` by its diagonal cap.  Let `Y_c in A_2` be
its unique inverse under (8).  Since the three top tensors `X_c` are
linearly independent, so are `Y_0,Y_1,Y_2`.  Equations (6) become the nine
exact identities

\[
 \boxed{\quad
 a_{cd}Q+\kappa P_cS_d=\delta_{cd}Y_c.
 \quad}                                                   \tag{11}
\]

This is the complete quotient/image content of the caps.

Let `Y=span{Y_0,Y_1,Y_2}` and project `A_2` modulo `C Q`.  Denote images by
bars.  Then

\[
 \kappa\,\overline{P_cS_d}=\delta_{cd}\overline{Y_c}.     \tag{12}
\]

If `Q notin Y`, the three barred target lifts remain independent.  In that
case both triples `(P_c)` and `(S_d)` are linearly independent.  Indeed, if
`sum_c lambda_cP_c=0`, multiply by `S_d` and reduce modulo `Q`; (12) gives
`lambda_d bar(Y_d)=0`, hence `lambda_d=0`.  The argument for the `S_d` is
identical.

We obtain the strongest valid positive conclusion.

**Proposition 3.1 (diagonal-isotope theorem).**  If `Q notin Y`, the
restricted bilinear tensor

\[
 \operatorname {span}(P_0,P_1,P_2)\times
 \operatorname {span}(S_0,S_1,S_2)
 \longrightarrow (Y+\mathbb C Q)/\mathbb C Q            \tag{13}
\]

is, after three *independent* choices of bases, the diagonal tensor

\[
                         (e_c,e_d)\longmapsto
                         \delta_{cd}e_c.                  \tag{14}
\]

It is therefore an isotope of coordinatewise multiplication on `C^3`.
It is not a subalgebra of `A`, and no associativity statement for (14) is
inherited from `A`.

**Proof.**  Independence was proved above, and (12) is exactly the table
(14) after mapping `P_c`, `S_c`, and `bar Y_c` independently to the three
standard bases.  But the first two spaces lie in degree one and the third
lies in degree two.  By (9), multiplying any output of (13) by another
positive-degree element gives zero.  There is no canonical identification
of the three spaces, so transported associativity of (14) is external data,
not an identity in `A`. `QED`

If `0 != Q in Y`, then `Y/CQ` has dimension two, not three.  If `Q=0`, it
has dimension three.  These are still diagonal quotient tables, but they
give even less basis rigidity.  In every branch, multiplying (11) by any
`P_e` or `S_e` gives only `0=0`, because both sides lie in `A_2` before the
extra multiplication.  Thus associativity supplies no hidden cubic
compatibility among the nine caps.

There is a useful physical interpretation of the exceptional branch.

**Proposition 3.2 (internal diagonal-power dichotomy).**  One has
`Q in Y` if and only if

\[
 q^{m-1}=\lambda_0X_0+\lambda_1X_1+\lambda_2X_2.         \tag{14a}
\]

If all three scalars are nonzero, the internal quadratic `q` itself gives
a three-colour realization on the `|W|=|B|-2` remaining sites, after a
diagonal normalization at one site.  Thus in an order-minimal hypothetical
source of order at least eight, the branch `Q in Y` can occur only with at
least one `lambda_c=0`.

**Proof.**  The isomorphism (8) sends `Q=[q]` to
`q h=q^(m-1)` and sends `Y_c` to `X_c`.  This proves the equivalence.  If
all `lambda_c` are nonzero, the matching tensor of `q` has coefficients
`lambda_c/(m-1)!`.  Apply at one remaining site the diagonal map with
entries `(m-1)!/lambda_c`.  Equivariance of the matching tensor under local
linear maps normalizes (14a) to `sum_c X_c`. `QED`

## 4. The smallest generic abstract countermodel

Fix any nonzero `kappa`; for the eight-site normalization one may take
`kappa=3`.  Define a graded vector space

\[
 \mathcal A_0=\mathbb C1,
 \qquad \mathcal A_1=\operatorname {span}\{e_0,e_1,e_2\},
 \qquad
 \mathcal A_2=\operatorname {span}\{Y_0,Y_1,Y_2,Q\}.      \tag{15}
\]

Make `1` the identity and set

\[
 e_ce_d={\delta_{cd}\over\kappa}Y_c,
 \qquad \mathcal A_1\mathcal A_2=0,
 \qquad \mathcal A_2^2=0.                               \tag{16}
\]

This is a commutative associative algebra: every product of three
positive-degree elements is zero.  Put

\[
                         P_c=S_c=e_c,qquad a_{cd}=0.      \tag{17}
\]

Then (11) holds exactly, `Q notin Y`, endpoint reversal fixes the model,
and every simultaneous permutation of the three colours is an algebra
automorphism.  Define the abstract image map by

\[
 \overline{\mathcal H}(Y_c)=X_c,qquad
 \overline{\mathcal H}(Q)=T,                             \tag{18}
\]

where `T,X_0,X_1,X_2` are independent.  This makes the image and quotient
identities (8), (11) exact.

The model has Hilbert function `(1,3,4)`, radical cube zero, and only the
idempotents zero and one.  It is the smallest abstract model in the generic
branch `Q notin Y`: the independent target lifts and `Q` require
`dim A_2>=4`; Proposition 3.1 requires `dim A_1>=3`; and the identity adds
one more dimension.  Equations (15)--(18) attain the lower bound eight.

This is a countermodel to the proposed implication

\[
 \text{nine diagonal caps + associativity}
 \quad\Longrightarrow\quad
 \text{a semisimple coordinatewise }\mathbb C^3
 \text{ inside the quotient}.                            \tag{19}
\]

The diagonal isotope is present, but the containing algebra is maximally
nonsemisimple.

## 5. Universal completion with arbitrary endpoint asymmetry

The preceding model used `a=0` and the strongest reflection symmetry
`P_c=S_c`.  Endpoint asymmetry adds no quotient constraint.  Let

\[
 \mathcal A_1=P\oplus S,
 \quad P=\operatorname {span}\{P_0,P_1,P_2\},
 \quad S=\operatorname {span}\{S_0,S_1,S_2\},             \tag{20}
\]

retain `A_2=span{Y_0,Y_1,Y_2,Q}`, and, for an arbitrary complex matrix
`a=(a_cd)`, define

\[
 P_cS_d={\delta_{cd}Y_c-a_{cd}Q\over\kappa},qquad
 PP=SS=0,qquad A_1A_2=A_2^2=0.                           \tag{21}
\]

Again this is automatically commutative and associative, and (11) holds
for all nine ordered pairs.  No symmetry of `(a_cd)` was introduced.
Reversing the deleted endpoints sends

\[
 P_c\longleftrightarrow S_c,qquad a\longmapsto a^{\mathsf T},
 \qquad Y_c\longmapsto Y_c,qquad Q\longmapsto Q,         \tag{22}
\]

and is an isomorphism between the two corresponding algebras.  Thus the
universal model retains exactly the covariance required by arbitrary
ordered endpoint colours.

More generally, any prescribed symmetric bilinear values on `P times P`
and `S times S` may be added to (21), with values in `A_2`, without
affecting associativity: every ensuing triple product still vanishes.  The
nine caps therefore impose no universal constraints on those missing
products.

## 6. Exact scope and route consequence

The abstract models in Sections 4--5 are not claimed to be
`R_W/Ann(q^(m-2))` for a physical site quadratic.  If they were realized
together with all nine caps, Section 1 would turn them into a full source.
Their role is more precise: they satisfy every identity retained by the
bare quotient/image-algebra argument—grading, commutativity, associativity,
top-degree annihilation, target-lift independence, direct-edge asymmetry,
and endpoint reversal—while violating the proposed semisimple conclusion.

Therefore a continuation cannot use only the abstract multiplication table
(11).  It must reintroduce at least one discarded physical constraint, for
example:

* the decomposition `A_1=direct-sum_(w in W)V_w` and the individual
  same-site square-zero relations;
* the fact that the bilinear products `p_cs_d` have the polarized site form
  `p_(c,i) tensor s_(d,j)+s_(d,i) tensor p_(c,j)` on every pair;
* compatibility of the annihilator ideal with the distinguished element
  `q`, beyond merely retaining its degree-two class `Q`; or
* a relation comparing different physical pair deletions before passing to
  their separate annihilator quotients.

Without such data, the most that survives is the diagonal isotope of
Proposition 3.1, and that structure is fully compatible with a cube-zero
local algebra.

The exact checker
[`computations/verify_two_deletion_quotient_level_algebra.py`](../computations/verify_two_deletion_quotient_level_algebra.py)
audits all structure constants and associators in the eight-dimensional
model, verifies its colour automorphisms and trivial idempotents, realizes a
dense asymmetric rational `(a_cd)` in the universal model, checks all nine
cap equations, and verifies endpoint reversal as the isomorphism
`a -> a^T`.
