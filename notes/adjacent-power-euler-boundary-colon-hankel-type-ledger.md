# The adjacent-power bracket is an Euler boundary, while the 27-row pair is a colon class

## 1. Outcome

Put \(D=2h-1\), \(h\geq3\), and let \(A\) be a graded
site-square-zero algebra over a characteristic-zero field.  For
\(z\in A_2\), consider the uniform two-step complex

\[
 A_1\mathop{\longrightarrow}^{b_h}A_3\oplus A_1
 \mathop{\longrightarrow}^{d_h}A_D,                    \tag{1}
\]

where

\[
 b_h(a)=(az,-(h-1)a),\qquad
 d_h(C,\Gamma)=Cz^{[h-2]}+\Gamma z^{[h-1]}.             \tag{2}
\]

The divided-power identity \(zz^{[h-2]}=(h-1)z^{[h-1]}\)
gives \(d_hb_h=0\).  If \(x\in A_1\) is an ordered endpoint
factor, then the curvature/direct-double bracket

\[
 x\kappa\bigl(zz^{[h-2]}-(h-1)z^{[h-1]}\bigr)          \tag{3}
\]

has coefficient pair \((x\kappa z,-(h-1)x\kappa)\), which is exactly the
boundary \(b_h(x\kappa)\).  The evaluated expression (3) is
\(d_hb_h(x\kappa)=0\).  The lower
connection/normal bracket in the newly exposed overlap identity is the
same Euler boundary one layer down.  Thus the complete adjacent-power
identity is a sum of two Euler boundaries after the direct/star/internal
source grading is forgotten.

The completed 27-row cycle is different.  In the notation of
`full-27-colon-cycle-macaulay-transfer-gap.md`, set

\[
 C_b=x_b\omega,
 \qquad
 \zeta_h=(C_b,\Gamma_b).                                \tag{4}
\]

Its literal equation is \(d_h(\zeta_h)=0\).  But

\[
 \boxed{
 [\zeta_h]=0\text{ in }H_1((1))
 \quad\Longleftrightarrow\quad
 (h-1)x_b\omega+\Gamma_bz=0.}                           \tag{5}
\]

Indeed the second coordinate of \(b_h(a)=\zeta_h\) forces
\(a=-\Gamma_b/(h-1)\), and the first coordinate then gives exactly the
right side of (5).

The exact scalar shadow of the all-27-row suspended guard has

\[
 d_h(\zeta_h)=0,
 \qquad
 (h-1)x_b\omega+\Gamma_bz_h\ne0                         \tag{6}
\]

for every \(h\geq3\).  Hence in this guard the colon cycle is not the
endpoint multiple of the Euler bracket.  This is an all-order separation,
not just a mismatch of displayed formulas.

Consequently, in this guard, an ordinary chain comparison which factors
through the static complex (1) cannot turn the coefficient boundary behind
(3) into the nonzero class (4): a chain map sends boundaries to
boundaries.  This does **not** rule out the hoped-for construction.  It
shows that any construction using the extra literal-source information
must be secondary.  A cap-filtration
extension or cross-chart mapping cone must have a connecting morphism
which turns the source-filtered lift of the Euler boundary into the colon
class.  No such connecting morphism is supplied by the adjacent-power
identity alone.

There is a second, independent obstruction after that connecting map.  The
selector conic, the clean Macaulay line, and the transverse tilted line are
three a priori different binary parameter spaces.  The ordered transverse
endpoint contracts the curvature factor to a scalar; it does not produce
the odd clean-line covariant of order \(2h-3\) needed to turn the quadratic
selector covector into a degree-\(D\) Hankel functional.  A physical site
factor \(x_b\) also raises site degree, not binary parameter order.

Thus the adjacent-power syzygy, the scalar-zero cap relation, and an
ordered endpoint factor do not yet canonically give the common Hankel
annihilator.  The exact missing data are stated in Sections 4--5.  Krenn's
conjecture remains open.

## 2. Exact comparison of the two cycles

Write

\[
 Z_0=z^{[h-1]},\qquad Z_1=z^{[h-2]},\qquad
 Z_2=z^{[h-3]}.
\]

The source overlap calculation gives

\[
 \sigma_h=
 \kappa(zZ_1-(h-1)Z_0)
 +\delta v(zZ_2-(h-2)Z_1)=0.                            \tag{7}
\]

After multiplying by an ordered site factor \(x\), its three coefficient
layers are

\[
 \bigl(x\delta vz,
       x(\kappa z-(h-2)\delta v),
       -(h-1)x\kappa\bigr)                              \tag{8}
\]

against \((Z_2,Z_1,Z_0)\).  The first and last two entries are respectively
the embedded boundaries

\[
 \begin{aligned}
 b_{h-1}^{\rm low}(x\delta v)
    &=(x\delta vz,-(h-2)x\delta v),\\
 b_h(x\kappa)&=(x\kappa z,-(h-1)x\kappa).
 \end{aligned}                                         \tag{9}
\]

Here \(b_{h-1}^{\rm low}\) is (2) shifted from the
\((Z_1,Z_0)\)-layers to the \((Z_2,Z_1)\)-layers.  Formula (9) is the
precise sense in which (7) has Bockstein *shape* but is an ordinary Euler
boundary after passing to the static site algebra.

By contrast, the full-27 pair is the two-layer vector

\[
                    (x_b\omega,\Gamma_b)                \tag{10}
\]

against \((Z_1,Z_0)\).  Its cycle equation says only that

\[
 (x_b\omega)Z_1+\Gamma_bZ_0=0.                          \tag{11}
\]

It does not allow cancellation of \(Z_1\).  Boundary membership would be
the strictly stronger coefficient identity in (5).  This distinction is
exactly the residual colon torsion.

For completeness, in the rational guard take

\[
\begin{aligned}
 z_0&=4u_1u_2+u_1u_3+u_2u_4,\\
 x_b&=\tfrac12u_3,\\
 \omega&=u_0u_4+u_2u_4+u_1u_2-u_1u_3-u_1u_4,\\
 \Gamma_b&=-2u_0+2u_1-\tfrac52u_2+\tfrac12u_3+2u_4.
                                                               \tag{12}
\end{aligned}
\]

For \(h>3\), adjoin disjoint matching variables and put
\(z_h=z_0+q_h\) as in the full-27 note.  The suspension proof there gives
(11) for every \(h\).  On the other hand, the coefficient of
\(u_0u_3u_4\) in the defect from (5) is

\[
 [u_0u_3u_4]\bigl((h-1)x_b\omega+\Gamma_bz_h\bigr)
 ={h-1\over2}\ne0.                                     \tag{13}
\]

The first summand gives the displayed coefficient, while no edge of
\(z_h\) can pair a term of \(\Gamma_b\) to produce \(u_0u_3u_4\).
This proves (6) uniformly.  Notice that the guard is still only a scalar
projection of target purity.  It proves nonboundary status in the static
complex; it does not obstruct a genuinely decorated connecting map.
Reversing the ordered pair \((e,a)\) in the weighted full-27 residual sends
both \(\omega\) and \(\Gamma_b\) to their negatives.  Thus the cycle and
the defect both change by one common sign; the witness in (13) becomes
\(-(h-1)/2\), while nonboundary status is unchanged.  The complementary
colour \(b\), and hence the factor \(x_b\), is not exchanged in this
orientation reversal.

## 3. What the scalar-zero extension would still have to do

For the off-diagonal selected cap, the legal normalized scalar-zero datum
is the response--target pair

\[
 \epsilon_*=
       (\alpha^{-1}R,-\Delta_{2h,3}),                   \tag{14}
\]

and its ordinary odd residue is

\[
 \rho_c(\alpha^{-1}R)=-\overline Y_c
                      =\widehat\zeta_c.                 \tag{15}
\]

The adjacent-power signs force the conditional normalization

\[
 \mathfrak B_c(\kappa,\epsilon_*)
       =\kappa\widehat\zeta_c.                          \tag{16}
\]

But (16) names a desired connecting value; it does not construct it.
There are two exact reasons it cannot be inserted into (9) as a
coefficient replacement.

1. The object (14) has nonzero target.  Its response coordinate alone is
   not a literal targetless row.
2. On the same \(q^{[h-1]}\)-complement, every companion cancelling that
   target has the opposite residue, so it cancels (15) as well.

In particular, there is no legal operation in the static complex which
simply sends the radial \(z\) in \(b_h(x\kappa)\) to \(R\).  A positive
construction needs a short exact sequence of **source-filtered** complexes
or a cross-chart cone in which the target of (14) is null-homotoped in a
different filtration degree.  Its connecting morphism must retain (15)
and must send the connection/normal part of (7) to a boundary.

It must also explain the actual coefficients of the colon pair.  Even in
the guard, \(\Gamma_b\) is not a scalar multiple of \(x_b\), and
\(\omega\) is not a scalar multiple of \(z_h\).  Thus neither component of
(10) is the coefficientwise image of the corresponding component of
\(b_h(x\kappa)\).  The cap extension has to produce this transverse
coefficient defect, not merely reproduce the divided-power identity.

## 4. The three parameter spaces do not collapse

Let

\[
 U_{\rm cl},\qquad U_{\rm sel},\qquad U_{\perp}
\]

denote respectively the canonical clean-line parameter space, the
selector-conic parameter space, and the tilted-overlap parameter space.
The presently available types are:

| datum | \(U_{\rm cl}\) | \(U_{\rm sel}\) | \(U_\perp\) |
|---|---:|---:|---:|
| selector covector \(\vartheta_2\) before contraction | \(0\) | \(2\) | \(0\) |
| colon cycle after applying \(\vartheta_2\) | \(0\) | \(0\) | \(0\) |
| curvature carrier \(\gamma=\kappa a+\lambda b\) | \(0\) | \(0\) | \(1\) |
| ordered complementary form \(\ell=b/\kappa\) | \(0\) | \(0\) | \(1\) |
| bracket \([\gamma,\ell]=1\) | \(0\) | \(0\) | \(0\) |
| physical ordered site factor \(x_b\) | \(0\) | \(0\) | \(0\) |
| chosen clean-line lift \(k_{\rm sz}\) of the scalar-zero point, if supplied | \(1\) | \(0\) | \(0\) |
| required Hankel functional \(\Theta_D\) | \(D\) | \(0\) | \(0\) |

The entries record symmetric binary order, not site degree.  They suppress
dual variance and determinant characters: the statement here is under the
three independent \(SL(2)\) actions.  Under \(GL(U_\perp)\), the bracket
carries the expected determinant character, which the ordered transverse
coordinates may trivialize.  Subject to that convention, the bracket is
the unique natural transverse contraction affecting the middle certificate
line.  It removes the two odd \(U_\perp\)-factors and leaves an
\(SL(U_\perp)\)-scalar; it does not transport either factor to
\(U_{\rm cl}\).  Likewise \(x_b\)
raises the site degree of (3) from \(2h-2\) to \(2h-1\), but its clean-line
order stays zero.

Before any comparison \(U_{\rm sel}\simeq U_{\rm cl}\), naturality under
\(SL(U_{\rm cl})\times SL(U_{\rm sel})\) already forbids using the
quadratic selector as a clean binary functional.  After granting such a
comparison, the smallest irreducible auxiliary which can combine
bilinearly with \(\operatorname {Sym}^2U_{\rm cl}\) to reach
\(\operatorname {Sym}^DU_{\rm cl}\) is

\[
                  \operatorname {Sym}^{D-2}U_{\rm cl}
                  =\operatorname {Sym}^{2h-3}U_{\rm cl}. \tag{17}
\]

This is the auxiliary for the Cartan-product summand, and it is odd.  The
transverse bracket does not supply (17).  Even a chosen parameter lift
\(k_{\rm sz}\in U_{\rm cl}\) of the scalar-zero point would supply only one
clean linear factor.  Such a lift is additional data and is not the
scalar-zero contraction matrix conventionally denoted \(K_*\).  Replacing
\(k_{\rm sz}\) by its \((D-2)\)-nd Veronese power would be an additional
nonlinear construction, not the linear cap extension or the adjacent-power
chain map.  Even if that power and a projective line comparison were
granted, the further coefficient identity

\[
 \mu_{\mathcal E}^*
   \bigl(\iota_*(\vartheta_2)k_{\rm sz}^{D-2}\bigr)=0    \tag{18}
\]

is not a consequence of types or of the cycle equations above.  In the
rootless branch it is precisely the contradiction one still has to prove.

If an “ordered endpoint factor” means one Segre factor \(u\) or \(v\) of
a rank-one selector, endpoint ordering distinguishes the two tautological
lines but does not remove the reciprocal gauge
\((u,v)\mapsto(\lambda u,\lambda^{-1}v)\).  Choosing one factor is therefore
not a canonical odd covariant without an additional source trivialization.

## 5. The exact uniform maps still missing

There are two logically separate maps.

First, one needs a source-filtered extension, schematically

\[
 0\longrightarrow\mathscr K_h^{\rm colon}
  \longrightarrow\widetilde{\mathscr C}_h
  \longrightarrow\mathscr C_h^{\rm adj}
  \longrightarrow0,                                    \tag{19}
\]

whose connecting morphism has the source-provenant value

\[
 \boxed{
 \partial_{\epsilon_*}
   ([\sigma_h]\otimes x_b)=[(x_b\omega,\Gamma_b)]\ne0.} \tag{20}
\]

Here \([\sigma_h]\) must mean the class in the appropriate filtered
quotient, not its zero class in the static Euler complex.  The lift must
use the literal curvature, direct-double, normal, connection, and cap rows;
it must null-homotope the target in (14); and changing any representative
by a literal source boundary must change (20) by a boundary.  Formulae
(5)--(16) fix the necessary normalization and show why this is a genuine
Bockstein/Yoneda datum rather than an ordinary chain map.

Second, one needs the decorated filtered-to-Hankel comparison

\[
 \boxed{
 \operatorname {Tr}_h:
 H_1(\mathscr K_h^{\rm colon,dec})
       \longrightarrow
 \ker\!\left(
   \mu_{\mathcal E}^{*}:(\operatorname {Sym}^{D}U_{\rm cl}^*)^*
       \to(\mathcal E\otimes
                 \operatorname {Sym}^{h-1}U_{\rm cl}^*)^*
            \right),}                                  \tag{21}
\]

with

\[
 \operatorname {Tr}_h([(x_b\omega,\Gamma_b)])\ne0.      \tag{22}
\]

Explicitly, if
\[
 f_\alpha(s,t)=\sum_{k=0}^{h}c_{\alpha,k}s^{h-k}t^k
       \in\mathcal E
\]
and \(\operatorname {Tr}_h([\zeta_h])
=(\theta_0,\ldots,\theta_D)\), then (21) requires the one common system
\[
 \sum_{k=0}^{h}c_{\alpha,k}\theta_{k+j}=0
 \qquad\text{for every }\alpha\text{ and }0\leq j\leq h-1. \tag{22a}
\]
Rootlessness makes the corresponding Macaulay multiplication map
surjective, so its dual kernel is zero.  A nonzero value in (22) is
therefore exactly the desired contradiction, not merely a low-rank
surrogate.

One Cartan-factorized realization of (21) would consist of a
source-derived projective comparison
\(\iota:U_{\rm sel}\simeq U_{\rm cl}\), together with a linear lift (whose
overall scalar is harmless here), and an odd covariant

\[
 \Phi_h([(x_b\omega,\Gamma_b)])
       =\kappa_{2h-3}\in\operatorname {Sym}^{2h-3}U_{\rm cl} \tag{23}
\]

such that

\[
 0\ne\iota_*(\vartheta_2)\kappa_{2h-3}
       \in\ker\mu_{\mathcal E}^*.                       \tag{24}
\]

Equations (21)--(24) require one functional which annihilates every clean
coordinate and all \(h\) shifts, not chartwise or anchorwise functionals.
The ordered transverse bracket can normalize (20), but it constructs
neither (23) nor the Hankel cut (24).

If both (20) and (21) existed, their composite would produce the desired
nonzero common Hankel annihilator and contradict rootlessness.  Presently
neither map is constructed.  The first missing map is source-homological;
the second is the clean-line parameter and coefficient comparison.

## 6. Checker and scope

The dependency-free checker
[`verify_adjacent_power_euler_colon_hankel_type.py`](../computations/verify_adjacent_power_euler_colon_hankel_type.py)
verifies over exact rationals:

* both adjacent divided-power brackets as Euler boundaries;
* the suspended colon equation extracted from the full-27 guard for
  \(3\leq h\leq9\), including its two nonzero summands;
* the uniform nonzero boundary defect (13), including its sign;
* reversal of the \((e,a)\) orientation, including the common sign change
  of \(\omega\), \(\Gamma_b\), and the defect;
* the symmetric orders and central-character ledger for the three
  independent binary parameter spaces; and
* the Clebsch--Gordan minimal auxiliary order \(D-2=2h-3\).

The proof of (5), the coefficient proof (13), and the representation
argument are uniform in \(h\); the finite checker loop is only an audit.
The checker does not re-audit all 27 literal rows, ranks, kernels, or target
normalizations; those are the scope of
[verify_full_27_colon_cycle_guard.py](../computations/verify_full_27_colon_cycle_guard.py).
Here only the derived two-coordinate cycle and its suspension are used.
This note does not claim that every filtered or decorated chain map is
impossible.  It isolates exactly why the newly exposed adjacent-power
identity is not already the full-27 class and why the available ordered
endpoint does not already land on the clean Hankel line.
