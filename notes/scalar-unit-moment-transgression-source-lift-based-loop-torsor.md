# The scalar-unit moment lift has a based-loop torsor

## 1. Outcome

Work over a characteristic-zero field \(\mathbb K\).  Fix \(h\geq3\), put
\(n=h-2\), and use the certified scalar-unit orientation

\[
 u_h=\sum_{k=2}^h q^{[h-k]}r^{[k]},\qquad
 x_h=q^{[h]}+q^{[h-1]}r.                                  \tag{1}
\]

For \(s\geq0\), set

\[
 H_s=\int_0^1t^s(q+tr)^{[n]}\,dt,\qquad
 c_s=(r-2q)H_s.                                           \tag{2}
\]

The required index set is

\[
 S_h=\{0,\ldots,m\},\qquad
 m=\begin{cases}1,&h=3,\\h-3,&h\geq4.\end{cases}          \tag{3}
\]

The target-side integral in (2) is canonical once the ordered affine
segment \(q\to q+r\) is chosen.  It has a Bernstein endpoint formula, and
its honest one-form pullback is invariant under every endpoint-fixing
polynomial reparameterization.  Thus the denominators and the affine
parameter are not the missing lemma.

The obstruction is a source-lift ambiguity.  Define the based Rodrigues
loops for all \(j\geq1\)

\[
 \eta_j(t)=\frac{d^{j-1}}{dt^{j-1}}
              \bigl(t^j(1-t)^j\bigr),\qquad j\geq1,       \tag{4}
\]

and take the following required higher-moment block:

\[
 \Delta_{sj}=\int_0^1t^s\,d\eta_j(t),
                         \qquad1\leq s,j\leq m.           \tag{5}
\]

Every \(\eta_j\) vanishes at both endpoints, every unweighted integral
\(\int d\eta_j\) is zero, and \(\Delta\) is triangular with

\[
 \Delta_{sj}=0\quad(s<j),\qquad
 \Delta_{jj}=(-1)^j\frac{(j!)^3}{(2j+1)!}\ne0.            \tag{6}
\]

Consequently based vertical source loops valued in the evaluation kernel
preserve both endpoints, the unweighted divided difference, and every
evaluated or associated-graded row, but can shift the required higher
moments independently.  Honest pullback preserves this ambiguity.

The main result is a sharp filtered countermodel.

> **Based-loop source-lift torsor theorem.**  For every \(h\geq3\), there
> is a two-step filtered differential graded \(\mathbb K[q,r]\)-module
> \(C_h\) with the following properties.
>
> 1. \(u_h=0\) in chain degree zero, \(c_0\) is an exact total source
>    class, and multiplication by \(q,r\) is defined in the module and
>    commutes with the differential.
> 2. In the associated graded, the stronger coefficientwise polynomial
>    \((r-2q)(q+tr)^{[n]}\) is the boundary of one ordered polynomial
>    carrier cell.  Hence all \(c_s\), \(s\in S_h\), come from the same
>    leading source lift.
> 3. In the total complex, the lower differential is a universal based
>    vertical one-form and the exceptional class satisfies
>    \([x_h]\ne0\).
> 4. Filtered lifts with the same associated graded form an affine torsor
>    under based vertical loops.  The residue map from the smallest
>    relevant loop space onto the \(m\) higher moments is an isomorphism.

This countermodel grants more leading data than any currently proved
physical four-cut statement.  It is also a genuine graded module, so it
does not multiply an evaluated coefficient illegally.  The desired lift
is the zero point of the torsor; endpoint order, reparameterization
invariance, higher coefficient extraction, Rees data, and Koszul
multiplication do not select that point.

This is a universal logical countermodel, not a physical matching source
and not a counterexample to Krenn's conjecture.  At the level of logical
independence, a complex carrying any already-certified physical rows may
be adjoined as a disjoint direct summand, which preserves those rows.  This
bookkeeping neither identifies \(C_h\) with, nor makes it a countermodel
of, the physical matching source.  A positive proof must add a
source-provenant horizontal/nullhomotopy cell and prove that every
competing lift has zero moment residue.

## 2. The maximal canonical target-side construction

Algebraic integration is the \(\mathbb K\)-linear map

\[
 \int_0^1\left(\sum_k a_kt^k\right)dt
       =\sum_k\frac{a_k}{k+1}.                            \tag{7}
\]

The ordered endpoints give

\[
                         q+tr=(1-t)q+t(q+r).
\]

Expanding in divided powers and integrating the beta densities yields

\[
 \boxed{
 H_s=\sum_{j=0}^{n}
       \frac{(s+j)!(n-j)!}{(s+n+1)!}
       q^{[n-j]}(q+r)^{[j]}.}                            \tag{8}
\]

Thus the entire target-side tower is a canonical algebraic divided
difference.  Reversing the endpoint order replaces \(t^s\) by
\((1-t)^s\); order chooses which moment tower is meant.

If \(\phi(0)=0\) and \(\phi(1)=1\), the honest pullback of (2) is

\[
 \phi(\tau)^s(q+\phi(\tau)r)^{[n]}\,d\phi(\tau).          \tag{9}
\]

The polynomial fundamental theorem of calculus proves that (9) has the
same integral as (2), without assuming that \(\phi\) is invertible or
that its endpoint derivatives are nonzero.  A raw
\(\tau^s\,d\tau\) or endpoint-speed jet is not this pullback.

Formula (8) remains in the formal target ring.  Its endpoint powers are
not automatically objects in one physical restriction module.  It
therefore neither constructs a common source carrier nor licenses
multiplication of an evaluated four-cut coefficient by \(q\) or \(r\).

## 3. The uniform based-loop ambiguity

Each function in (4) retains a factor \(t(1-t)\).  Integration by parts
gives

\[
 \Delta_{sj}=-s\int_0^1t^{s-1}\eta_j(t)\,dt.             \tag{10}
\]

If \(s<j\), integrate the definition of \(\eta_j\) by parts \(j-1\)
times.  All boundary terms vanish and the \((j-1)\)-st derivative of
\(t^{s-1}\) is zero.  On the diagonal,

\[
\begin{aligned}
 \int_0^1t^{j-1}\eta_j(t)\,dt
   &=(-1)^{j-1}(j-1)!\int_0^1t^j(1-t)^j\,dt\\
   &=(-1)^{j-1}(j-1)!\frac{(j!)^2}{(2j+1)!}.
\end{aligned}                                            \tag{11}
\]

Equations (10)--(11) prove (6).  This is a triangular Rodrigues proof,
not a repetition of the Hilbert--Cauchy carrier-span theorem.

Let \(Z\) be a space of vertical source cycles killed by the evaluated
row map.  Adding

\[
                 \nu(t)=\sum_{j=1}^m z_j\,d\eta_j(t),
                 \qquad z_j\in Z,                        \tag{12}
\]

to a source lift changes no endpoint and has zero unweighted integral.
Its higher-moment residue is

\[
 \mathfrak m(\nu)=
   \left(\sum_{j=1}^m\Delta_{sj}z_j\right)_{s=1}^m.       \tag{13}
\]

By (6), (13) realizes arbitrary higher-moment residues.  Under an
endpoint-fixing reparameterization,

\[
 \int_0^1\phi(\tau)^s
       d\bigl(\eta_j(\phi(\tau))\bigr)
       =\int_0^1t^s\,d\eta_j(t)=\Delta_{sj}.              \tag{14}
\]

Both sides are endpoint evaluations of the same polynomial primitive.
Thus honest pullback preserves the ambiguity rather than removing it.

Put

\[
                         B_m=t(1-t)\mathbb K[t]_{\leq m-1}.
\]

The \(\eta_j\)'s form a basis of \(B_m\), and

\[
 B_m\otimes Z\longrightarrow Z^m,\qquad
 \eta\otimes z\longmapsto
       \left(\int_0^1t^s\,d\eta\;z\right)_{s=1}^m        \tag{15}
\]

is an isomorphism.  On this smallest moment-visible loop space, zero
indeterminacy is equivalent to eliminating the based vertical loop.

## 4. The coefficientwise filtered DGM countermodel

Regard divided powers as factorial-normalized homogeneous polynomials in

\[
                         S=\mathbb K[q,r]
\]

and put \(\overline S=S/(u_h)\).  Write

\[
 C(t)=(r-2q)(q+tr)^{[n]}=\sum_{\ell=0}^n C_\ell t^\ell,
 \qquad
 D_{\ell j}=[t^\ell]\eta_j'(t).                          \tag{16}
\]

For the coefficientwise construction use the full based-loop space
\(B_n\).  Give symbols \(z_1,\ldots,z_n\) internal degree \(h-1\), and set

\[
 (C_h)_0=\overline S\oplus
          \bigoplus_{j=1}^n\overline S z_j,\qquad
 (C_h)_1=\bigoplus_{\ell=0}^n\overline S a_\ell.         \tag{17}
\]

The subscripts in (17) are chain degrees; the homogeneous polynomial
degree is a separate internal grading.  Every \(a_\ell\) has internal
degree \(h-1\).  Define \(d:(C_h)_1\to(C_h)_0\), put
\(d(C_h)_0=0\), and extend the following rule \(S\)-linearly:

\[
 d a_\ell=\left(\overline C_\ell,
        \sum_{j=1}^nD_{\ell j}z_j\right)
                         \quad(0\leq\ell\leq n).         \tag{18}
\]

Thus \(d^2=0\), and

\[
 d(qa_\ell)=q\,da_\ell,\qquad
 d(ra_\ell)=r\,da_\ell.                                  \tag{19}
\]

All degree-\(h\) consequences are legal operations in this one source
module.  No evaluated four-cut equality is multiplied.

If \(A(t)=\sum_{\ell=0}^na_\ell t^\ell\), (18) is the single
coefficientwise equation

\[
 dA(t)=\overline C(t)+\sum_{j=1}^nz_j\eta_j'(t).         \tag{20}
\]

Its moment cells

\[
 e_s=\int_0^1t^sA(t)\,dt
       =\sum_{\ell=0}^n\frac{a_\ell}{s+\ell+1}           \tag{21}
\]

satisfy

\[
 de_0=(\overline c_0,0),\qquad
 de_s=\left(\overline c_s,
       \sum_{j=1}^n\left(\int_0^1t^s\,d\eta_j\right)z_j
       \right)\quad(s\geq1).                            \tag{22}
\]

In particular \(c_0\) is an unambiguous total boundary.  On the required
higher moments, the first \(m\) loop directions give the invertible
matrix (6).

Filter \((C_h)_0\) by

\[
 F_0(C_h)_0=\bigoplus_j\overline S z_j,\qquad
 F_1(C_h)_0=(C_h)_0,
\]

and put \(F_0(C_h)_1=0\), \(F_1(C_h)_1=(C_h)_1\).  The lower term in
(20) disappears in the associated graded:

\[
                 \operatorname{gr}(d)A(t)=\overline C(t). \tag{23}
\]

This grants the coefficientwise sufficient identity, not just its moment
shadow.  The previously audited
[formal moment theorem](scalar-unit-carrier-moment-tower-hilbert-cauchy.md#1-outcome-orientation-and-the-degree-correction)
implies that \(x_h\) is a boundary in this associated graded.  That span
proof is not repeated here.

In the total complex, however,

\[
                            [x_h]\ne0.                    \tag{24}
\]

Suppose \((\overline x_h,0)\) were the boundary of a homogeneous
internal-degree-\(h\) chain \(\sum_{\ell=0}^n b_\ell a_\ell\).  Since
each \(a_\ell\) has internal degree \(h-1\), every
\(b_\ell\in\overline S_1\).  The \(z_j\)-coordinates give

\[
             \sum_{\ell=0}^n b_\ell D_{\ell j}=0
                         \quad(1\leq j\leq n).            \tag{25}
\]

The derivative map

\[
 B_n\longrightarrow\mathbb K[t]_{\leq n},\qquad
                         \eta\longmapsto\eta'            \tag{26}
\]

is injective, and its image lies in the kernel of \(\int_0^1\).
Both spaces have dimension \(n\), so its image is exactly that kernel.
The left kernel in (25) is therefore the line spanned by

\[
                         (1,1/2,\ldots,1/(n+1)).
\]

There is a single \(b\in\overline S_1\) with

\[
                         b_\ell=\frac b{\ell+1}.          \tag{27}
\]

The polynomial component of the alleged boundary is then \(bc_0\).
Because \(h\geq3\), the quotient has no relation in degree one, so
\(\overline S_1=S_1\) and \(b\) has a unique linear lift.  Equality of
the polynomial components in \(\overline S\) says
\(x_h-bc_0\in(u_h)_h=\mathbb K u_h\).  Thus

\[
                x_h\in\operatorname{span}_{\mathbb K}
                       \{u_h,qc_0,rc_0\}.                \tag{28}
\]

The uniform nonmembership proved in the
[carrier-torsion obstruction](scalar-unit-carrier-torsion-obstruction.md#3-exact-polynomial-module-nonmembership)
rules out (28).  In the cleared normalization used there,
\(u_h^{\rm clr}=h!u_h\), \(v_{h-1}^{\rm clr}=(h-1)!c_0\), and
\(x_h^{\rm clr}=h!x_h\), so these nonzero rescalings do not change the
span test.  This proves (24).  The argument is uniform in \(h\) and uses
chain direction, internal degrees, and every possible degree-\(h\)
boundary explicitly.

More generally, replace \(D\) in (18) by \(D\Lambda\), for any
\(n\)-by-\(n\) matrix \(\Lambda\).  Every resulting filtered complex has
the same associated graded (23).  With
\(Z=\operatorname{span}_{\mathbb K}\{z_1,\ldots,z_n\}\), these are
coordinate points of the coefficientwise lift torsor

\[
                         B_n\otimes_{\mathbb K}Z.        \tag{29}
\]

Restricting the loop factor to \(B_m\) gives the moment-visible torsor
(15).
The point \(\Lambda=0\) is the desired zero-lower-term lift.  There the
coefficientwise identity is a total boundary, all \(c_s\)'s are total
boundaries, and the formal moment theorem kills \(x_h\).  The point
\(\Lambda=I\) is the countermodel above and retains \(x_h\).

In Rees notation, (18) is

\[
 d_\Lambda a_\ell=\overline C_\ell+\rho
             \sum_j(D\Lambda)_{\ell j}z_j.               \tag{30}
\]

Every \(\Lambda\) has the same special fibre at \(\rho=0\).  A Rees
module records the extension but does not choose its splitting.  A flat
connection in one base direction does not choose it either: one-variable
flatness is automatic, while the vertical connection coefficient is the
free parameter in (29).

## 5. Why the proposed physical constructions stop at the torsor

### 5.1 Multivariate site scalings and higher cuts

Independent physical site scalings produce a multigraded polynomial, and
higher \(2k\)-cut extraction records its face coefficients.  Diagonal
pullback can reproduce (8).  But coefficients obtained after exposing
different sites live in different restriction modules.  Adding them as
one \(H_s\) requires coherent all-label insertion maps which commute with
the source differential, every face map, and \(q,r\)-multiplication.

A vertical cycle times the multivariate bubble
\(\prod_v t_v(1-t_v)\) vanishes on every boundary face.  Its evaluated
coefficients vanish as well because the cycle lies in the evaluation
kernel, while its diagonal pullback is a based loop.  Thus more faces or
higher cuts do not remove (29) unless a new source
injectivity/saturation theorem makes that vertical cycle a literal
boundary.  Coefficient reconstruction alone reconstructs an already-zero
evaluated row.

### 5.2 Endpoint order and the common carrier

Endpoint order fixes the sign in (9), the left endpoint \(t=0\), and the
oriented curvature sum \(r-2q\).  It does not identify the two restricted
oriented four-cut carriers.  Occupancy can remove different monomials on
the two sides, and evaluated cancellation can kill either restriction.
A common carrier needs a chain-level base-change square in which
restriction, ordered insertion, and horizontal transport commute before
evaluation.  No current endpoint row provides that square.

### 5.3 Koszul multiplication

The countermodel already has the strongest formal remedy to the grading
problem: it is an \(S\)-module and (19) holds.  The vertical degree-\(h\)
classes \(qz_j,rz_j\) are free.  Their ordinary Koszul relation occurs
one degree later and does not make either class zero.  A Koszul
presentation therefore does not erase the lower term in (18); it needs a
source contraction or a colon theorem for the actual physical module.

### 5.4 Exceptional-target retention

The exceptional class is not discarded, evaluated away, or divided by a
carrier.  Equation (24) retains it in total homology while (23) grants
the entire proposed coefficientwise leading identity.  The exceptional
target detects the filtered extension.  Suppressing its diagonal
insertion cell would hide the obstruction rather than solve it.

## 6. The exact extra datum

A positive source lift must construct, in one all-label filtered
differential graded \(S\)-module \(Q\), an ordered polynomial one-form
cell \(E(t)\,dt\) satisfying

\[
 d_Q(E(t)\,dt)=(r-2q)(q+tr)^{[n]}\,dt                    \tag{31}
\]

as a literal source identity, not merely after evaluation.  It must also
satisfy all of the following.

1. **Common physical carrier.**  A chain-level
   restriction--insertion/base-change map compares the two oriented
   restrictions before they are added to give \(r-2q\).
2. **Naturality.**  Pullback by \(t=\phi(\tau)\) sends (31) to its honest
   one-form pullback and preserves its class.
3. **Legal module structure.**  \(Q\) is an \(S\)-module and its
   differential commutes with \(q,r\).
4. **Exceptional row.**  The \((a,a)\) target cell and \(x_h\) remain in
   the same filtered complex until the final contradiction.
5. **Zero indeterminacy.**  If \(E,E'\) are allowed lifts, their vertical
   based-loop difference has zero image under (15).  Equivalently, the
   allowed lift torsor has a distinguished zero section modulo
   moment-null literal boundaries.

Then

\[
                         e_s=\int_0^1t^sE(t)\,dt          \tag{32}
\]

satisfies \(d_Qe_s=c_s\) for every \(s\in S_h\).
Multiplication by \(q,r\) is legal in \(Q\), and the audited algebraic
theorem gives \(x_h=0\).  Conversely, (4)--(30) show that omitting item 5
permits a reparameterization-invariant filtered lift with the same
coefficientwise associated graded and with \(x_h\ne0\).

The minimal new datum is therefore a source-provenant horizontal
splitting/nullhomotopy together with vanishing of its based-loop moment
residue.  A source-specific saturation theorem proving that the relevant
vertical cycle space is zero is an equivalent route.

## 7. Exact audit and scope

The dependency-free checker
[verify_scalar_unit_moment_transgression_source_lift_based_loop_torsor.py](../computations/verify_scalar_unit_moment_transgression_source_lift_based_loop_torsor.py)
uses exact rational arithmetic.  It audits the Bernstein identity (8),
endpoint conditions, the triangular residues (6), honest
reparameterization (14), coefficientwise derivative-kernel identity
(26), legal divided-power multiplication, associated-graded closure, and
survival of \(x_h\) in the total filtered countermodel.  It includes
deterministic failures for a wrong Rodrigues order, a missing pullback
Jacobian, a shifted moment denominator, a missing vertical loop, and
incorrect divided-power multiplier weights.  It uses explicit exceptions
and therefore runs unchanged under optimized Python.

This note proves a source-lift obstruction and identifies the exact extra
datum.  It does not assert that the filtered module is a physical matching
source, does not multiply an evaluated four-cut row, does not repeat the
Hilbert--Cauchy span proof, and does not modify the certified proof
frontier.
