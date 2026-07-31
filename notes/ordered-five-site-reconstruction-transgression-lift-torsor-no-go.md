# Ordered five-site reconstruction does not define the radial transgression

## 1. Outcome

Let \(h\geq3\).  In the notation of the
[five-exposed-site ledger](five-exposed-site-yoneda-cup-obstruction.md), put

\[
 C_4=W\setminus\{r,s\},\qquad
 D_5=W\setminus\{r,s,x\},\qquad
 D_x=W\setminus\{x\}.                                    \tag{1}
\]

Thus \(|C_4|=2h-2\), \(|D_5|=2h-3\), and \(|D_x|=2h-1\).
Retain the ledger's oriented coefficients \(D,v,\kappa\), and fix a routed
colour \(c\).  Whenever the intended output is called nonzero below, the
standing branch assumptions are

\[
                  \kappa\ne0,\qquad
 \widehat\zeta_c:=-\overline Y_c\ne0.                   \tag{1a}
\]

This note tests the most literal proposed restriction--insertion
correspondence

\[
 \bigoplus_{k,\ell}\mathcal R_{2h-2}(C_4)
   \mathop{\longrightarrow}^{\partial_{x,c}}
 \bigoplus_{k,\ell}\mathcal R_{2h-3}(D_5)
   \mathop{\longrightarrow}^{I_{r,s}}
 \mathcal R_{2h-1}(D_x).                                 \tag{2}
\]

For each fixed pair of cap-row labels \((i,j)\), the first arrow acts
componentwise.  Suppressing these direct sums would mistype the second
arrow: insertion reconstructs a physical target only from the complete
\((k,\ell)\)-array.

The result is a precise no-go, not a proof of Krenn's conjecture.

Relative to the fixed physical colour bases, there is a unique literal
ordered insertion on the complete all-label coefficient array:

\[
 \boxed{
 I_{r,s}\bigl((F_{k\ell})_{k,\ell}\bigr)
   =\sum_{k,\ell}e_k^{(r)}e_\ell^{(s)}F_{k\ell}.}         \tag{3}
\]

It is simply the inverse of simultaneous coefficient extraction on the
component which occupies both sites \(r,s\).  It uses no inverse star,
matching power, direct entry, or quotient map.  It also retains endpoint
order: \(k\) belongs to the named \(r\)-slot and \(\ell\) to the named
\(s\)-slot.

Applied to the complete five-site comparison, (3) gives zero.  Indeed the
literal source identity is componentwise

\[
 {\cal A}_{pq}^{ij;k\ell c}
      ={\cal A}_{pr}^{ik;j\ell c},                       \tag{4}
\]

so

\[
 I_{r,s}\left(
   ({\cal A}_{pq}^{ij;k\ell c}
       -{\cal A}_{pr}^{ik;j\ell c})_{k,\ell}
 \right)=0.                                             \tag{5}
\]

Before top-degree evaluation, the curvature/direct-double pair and the
connection/normal pair are the two Euler boundaries in the static
adjacent-power complex

\[
 \begin{aligned}
  b_h(\xi\kappa)&=(\xi\kappa z,-(h-1)\xi\kappa),\\
  b_{h-1}(\xi Dv)&=(\xi Dvz,-(h-2)\xi Dv).
 \end{aligned}                                          \tag{6}
\]

Consequently every **strict chain lift** of the literal coefficient
restriction and reconstruction which intertwines the displayed source and
target differentials sends the adjacent-power carrier to a boundary.  The
polynomial correspondence (2) by itself has no chain degree and does not
assert that such a lift exists.  If a strict lift does exist, it cannot send
the carrier to the nonzero odd class

\[
                         \kappa\widehat\zeta_c.           \tag{7}
\]

This is stronger than the site-degree obstruction to ordinary
multiplication and narrower than a no-go for all secondary operations.  It
shows that the natural restriction--insertion map itself is not the missing
transgression.

The diagonal target is also rigid.  If \(Y_c^{D_5}\) denotes the constant
colour-\(c\) word on \(D_5\), then its all-label two-site target array is

\[
 T^{(c)}_{k\ell}=\delta_{kc}\delta_{\ell c}Y_c^{D_5},
\]

and (3) gives

\[
 \boxed{
 I_{r,s}\bigl((T^{(c)}_{k\ell})_{k,\ell}\bigr)
    =e_c^{(r)}e_c^{(s)}Y_c^{D_5}=Y_c^{D_x}.}             \tag{8}
\]

Thus the \((c,c)\) insertion component is unavoidable.  Deleting it makes
the reconstructed target zero, and no off-diagonal insertion cell can
replace it.  In the intrinsic scalar-unit packet, the complete five-site
target has coefficient \(h\mathbf1_{i=j=k=\ell=c}Y_i^{D_5}\).  Thus the
choice \(c=a\) simultaneously requires the \((k,\ell)=(a,a)\) insertion
component and the exceptional selected cap row \((i,j)=(a,a)\).
Independently, the
[full normal-jet ledger](scalar-unit-full-normal-jet-unary-anchor-ledger.md)
contains the ordered square

\[
                         R_{ia}R_{aj}H_a.                \tag{9}
\]

Any proposed comparison which claims to act on this first normal jet must
retain those ordered factors, while its target-bearing five-site component
must retain the \((a,a)\) row.  The current identities do not identify an
arbitrary \(R_{ia}R_{aj}H_a\) with that target row; transposing the factors
or suppressing the exceptional component is not source-faithful.

Even after that row is retained, the current identities determine only the
target of a putative filtered nullhomotopy, not its lower odd-response
coordinate.  This residual freedom is an explicit affine torsor.  Record a
source row by the pair, with \(T=\Delta\) in the off-diagonal packet and
\(T=X_a\) in the normalized intrinsic unary packet,

\[
        (\text{coefficient of }T,\quad
          \text{coefficient of }\widehat\zeta_c).         \tag{10}
\]

The normalized target-bearing cap row has pair

\[
                            e_c=(-1,+1).                  \tag{11}
\]

In the off-diagonal packet this is the normalized scalar-zero cap.  In the
intrinsic packet the same coordinates describe the negative of the
normalized unary cap.  This distinction changes the source provenance, not
the target--response arithmetic below.

The
[same-power target--residue lock](offdiagonal-same-power-target-residue-lock.md)
forces every literal target companion with target \(+T\) to have pair

\[
                            u_{\rm sp}=(+1,-1),            \tag{12}
\]

and \(e_c+u_{\rm sp}=(0,0)\).  A secondary target
nullhomotopy which retained the response would instead have to have

\[
                            u_{\rm sec}=(+1,0),            \tag{13}
\]

so that \(e_c+u_{\rm sec}=(0,+1)\).

Equations (11)--(13) are not merely a picture.  Section 5 constructs, for
every \(\lambda\in\mathbb C\), a filtered chain completion whose new target
cell has lower response \(\lambda\widehat\zeta_c\).  All these completions
have the same associated-graded target row, the same ordered coefficient
reconstruction, the same cap cycle, the same adjacent-power Euler
boundaries, and the same scalar-unit unary-anchor identity.  Their
target-cancelled residuals are

\[
                         (1+\lambda)\widehat\zeta_c.       \tag{14}
\]

At the target--response coordinate level, the literal same-power cell is
the point \(\lambda=-1\) and gives zero; this does not identify its source
grade with the grade of a new cell.  The desired normalization would be
\(\lambda=0\).  Hence the listed source identities do not select the
desired value or the relative chain grade in which it should be read.

For this literal restriction--insertion architecture, the exact extra
datum is consequently a filtered five-site cell
\(H_{r,s;x,c}\) whose leading boundary is the exceptional diagonal target,
whose lower odd coordinate is zero, and whose connection/normal part is a
literal boundary.  For a single-valued operation one must also prove that
the odd residue vanishes on the difference of any two such cells.  This is
the missing existence and zero-indeterminacy statement; it is not implied
by coefficient reconstruction, endpoint order, the adjacent-power
identity, or the unary-anchor ledger.

## 2. The ordered reconstruction lemma

For each site \(v\), let \(E_v\) be the three-dimensional colour space with
basis \(e_1^{(v)},e_2^{(v)},e_3^{(v)}\).  The site-square-zero algebra has a
multigrading by occupied sites.  Its component occupying every site of a
set \(S\) is canonically

\[
                  {\cal R}_{\mathbf1_S}(S)
                    \simeq\bigotimes_{v\in S}E_v.        \tag{15}
\]

The order used to display the tensor product is bookkeeping only; the
site algebra itself is commutative.  What remains ordered are the named
physical slots.

Put \(S=D_5\sqcup\{r,s\}\).  Simultaneous coefficient extraction gives an
isomorphism

\[
 \operatorname {Coeff}_{r,s}:
 {\cal R}_{\mathbf1_S}(S)
  \longrightarrow
 \bigoplus_{k,\ell}{\cal R}_{\mathbf1_{D_5}}(D_5),
 \qquad
 F\longmapsto
  (\partial_{s,\ell}\partial_{r,k}F)_{k,\ell}.           \tag{16}
\]

Formula (3) is its inverse.  In particular,

\[
 \partial_{s,\ell}\partial_{r,k}
 I_{r,s}((F_{uv})_{u,v})=F_{k\ell}.                     \tag{17}
\]

This proves existence and uniqueness relative to the displayed colour
bases.  More precisely, the construction is covariant under simultaneous
changes of those bases: (3) is the coordinate expression of the canonical
tensor identification

\[
 E_r\otimes E_s\otimes{\cal R}_{\mathbf1_{D_5}}(D_5)
       \simeq{\cal R}_{\mathbf1_S}(S).                   \tag{18}
\]

Swapping the named sites replaces \(E_r\otimes E_s\) by
\(E_s\otimes E_r\) and simultaneously swaps \((k,\ell)\); it does not
silently transpose a physical block.  The orientation of the chart
comparison is separate.  Replacing the oriented comparison \(pq-pr\) by
\(pr-pq\) negates \(D,\kappa\), the adjacent-power chain, and any correctly
normalized secondary output together.

Now let \((F_{k\ell})\) be a complete all-label family on \(C_4\).
The literal correspondence of bidegree \((-1,+2)\) is

\[
 \mathfrak C_{r,s;x,c}((F_{k\ell}))
   =I_{r,s}\bigl((\partial_{x,c}F_{k\ell})_{k,\ell}\bigr).
                                                               \tag{19}
\]

It has net site degree \(+1\), as required.  Formula (19) is fully defined
only on the all-label array.  A single fixed-\((k,\ell)\) coefficient is
not enough to reconstruct the physical target on \(D_x\).

Applying (19) to a literal equality preserves that equality.  In
particular, (4) proves (5).  The fifteen/ten/one direct-star split in the
five-site formula is essential for identifying the entries of the array,
but after all entries are retained it does not create a new homology class.
The result is exact reconstruction of the already-zero comparison row.

## 3. The adjacent-power carrier is a strict boundary

Let \(A\) be any characteristic-zero graded site algebra with divided
powers.  For every \(m\geq2\), set

\[
 \begin{aligned}
 b_m(a)&=(az,-(m-1)a),\\
 d_m(C,\Gamma)&=Cz^{[m-2]}+\Gamma z^{[m-1]}.
 \end{aligned}                                           \tag{20}
\]

Then

\[
 d_mb_m(a)
  =a\bigl(zz^{[m-2]}-(m-1)z^{[m-1]}\bigr)=0.            \tag{21}
\]

The high pair in (6) is evaluated by \(d_h\); the low pair is evaluated by
\(d_{h-1}\).  In particular, the second line is defined at \(h=3\), where
its lower divided power is \(z^{[0]}\).

The oriented four-cut ledger is

\[
 \begin{aligned}
 \sigma_h={}&
 \kappa\bigl(zZ_1-(h-1)Z_0\bigr)\\
 &+Dv\bigl(zZ_2-(h-2)Z_1\bigr),\\
 Z_0={}&z^{[h-1]},\quad Z_1=z^{[h-2]},\quad
 Z_2=z^{[h-3]}.
 \end{aligned}                                          \tag{22}
\]

In the static degree-shift model, adjoin an ordered linear site factor
\(\xi\).  Its three coefficient layers are

\[
 \bigl(\xi Dvz,\ \xi\kappa z-(h-2)\xi Dv,\ -(h-1)\xi\kappa\bigr).
                                                               \tag{23}
\]

This is exactly the sum of the low embedded boundary and the high boundary
in (6).  This static model is not a construction of the physical
restriction--insertion chain lift.  If such a chain map \(\Phi\) has been
specified, then it satisfies

\[
 [\Phi(\sigma_h)]=0                                     \tag{24}
\]

in target homology.  This statement is uniform in \(h\), including
\(h=3\), where \(Z_2=z^{[0]}\); no negative power is introduced.

The literal radial carrier also remains invisible after the odd
restriction.  On the common odd quadratic \(q_0\), with
\(A=q_0^{[h-1]}\), \(B=q_0^{[h-2]}\), one has

\[
 \rho_c(q_0)=[t_cq_0B]
   =(h-1)[t_cA]=0                                      \tag{24a}
\]

in \({\cal R}_{2h-1}/({\cal R}_1A)\).  Thus neither applying the
ordinary odd residue to the radial coordinate nor first regarding its
adjacent-power coefficient pair as a strict boundary produces the desired
response.

Under (1a), the intended odd response is nonzero.  Therefore a strict chain
lift cannot satisfy (7).  Calling the leading part of (22) a class requires
a relative Rees quotient in which the displayed static boundary acquires a
connecting symbol.  That quotient is additional structure, not a new
formula for (19).

This proof does not use ordinary cup or Yoneda multiplication.  It only
uses the defining property of a chain map and the two literal Euler
boundaries.

## 4. The exceptional diagonal cannot be reconstructed from the other cells

The top-occupancy decomposition (16) is a direct sum.  For a fixed colour
\(c\), the constant target word on \(D_x\) has coefficient array

\[
 \partial_{s,\ell}\partial_{r,k}Y_c^{D_x}
   =\delta_{kc}\delta_{\ell c}Y_c^{D_5}.                 \tag{25}
\]

Equations (8) and (25) prove both existence and uniqueness of its
insertion.  In particular,

\[
 I_{r,s}\bigl((T_{k\ell}^{(c)})_{(k,\ell)\ne(c,c)}\bigr)=0.
                                                               \tag{26}
\]

This is a direct-sum statement, so it is unaffected by arbitrary complex
cancellation in the source coefficients.

For the intrinsic scalar-unit block \(A_{pq}=\alpha E_{aa}\), the full
normal-jet ledger identifies

\[
 \Theta_a=R_{aa}H_a,\qquad
 R_{ij}\Theta_a=R_{ia}R_{aj}H_a.                         \tag{27}
\]

The factor order in (27) names the endpoint path \(i\to a\to j\):

\[
 R_{ia}R_{aj}=(p_i s_a)(p_a s_j).
\]

Commutativity proves the Segre equality with \(R_{ij}R_{aa}\), but does
not exchange the named \(p\)- and \(q\)-endpoint slots.  Formula (19) acts
on the \((k,\ell)\)-array separately for each fixed outer \((i,j)\); a full
comparison must therefore retain those outer slots as well.

The exceptional row enters the exact Euler identity

\[
 G_a\Theta_a
   =hU_a+(h-1)\alpha^{h-1}R_{aa}q^{[h-1]}.               \tag{28}
\]

Equation (28) is indispensable, but it is still an equality in the
literal source/target grade.  It specifies no map from the comparison
class (27) to the odd response quotient.  In particular, it neither gives
a lift of the \((a,a)\) target through a new comparison degree nor proves
multiplication by \(G_a\) faithful on that degree.  The lift-torsor
countercomplex below remains compatible with (28) for every value of its
lower parameter.

## 5. The filtered lift-torsor countercomplex

The ambiguity can be isolated over one copy of \(\mathbb C\).  Start with
any fixed literal complex containing the already fixed degree-zero cycles
\(T\), the required diagonal target, and \(Z=\widehat\zeta_c\), the odd
response.  Adjoin a new comparison cell \(H\) in degree one without
changing any old differential.  For each
\(\lambda\in\mathbb C\), define

\[
                 d_\lambda H=T+\lambda Z,
                 \qquad d_\lambda T=d_\lambda Z=0.      \tag{29}
\]

Plainly \(d_\lambda^2=0\).  Give this complex the increasing filtration

\[
 F_0=\mathbb C Z,\qquad
 F_1=\mathbb C Z\oplus\mathbb C T\oplus\mathbb C H.     \tag{30}
\]

Here (30) describes the three displayed directions; any other summands of
the fixed complex retain their old filtration.

The associated-graded differential is

\[
                      \operatorname {gr}(d_\lambda)H=T  \tag{31}
\]

for every \(\lambda\).  Thus endpoint reconstruction and every leading
target equation see the same cell.  The parameter occurs only in the
unprescribed filtration-lowering response component.

The fixed target-bearing cap cycle is

\[
                             e=-T+Z.                     \tag{32}
\]

Combining it with the new target cell gives

\[
                        e+d_\lambda H=(1+\lambda)Z.      \tag{33}
\]

At \(\lambda=-1\), (29) is the same-power target companion and (33) is
zero, exactly as required by the target--residue lock.  At
\(\lambda=0\), (29) is the desired filtered target nullhomotopy and (33)
is \(Z\).  Every other \(\lambda\) gives a different response.
Multiplication by the oriented curvature scalar gives

\[
              \kappa e+\kappa d_\lambda H
                   =(1+\lambda)\kappa\widehat\zeta_c.    \tag{34}
\]

Reversing the chart orientation negates both sides.  No trace, direct
entry, site form, or matching power is divided out.

The old literal complex already contains a same-power cell \(S\), in its
own source grade, with

\[
                             dS=T-Z=-e.                  \tag{35}
\]

If one forgets the source filtration and adjoins \(H\) in the same total
complex, then

\[
                  d_\lambda(H-S)=(1+\lambda)Z.           \tag{36}
\]

In particular, at the desired value \(\lambda=0\), the putative response
\(Z\) is an ordinary total boundary.  Thus merely adjoining the
zero-response target lift does not work: one must construct a relative
filtered quotient in which \(H\) has the proposed comparison provenance
while the same-power cell \(S\) is not an allowed indeterminacy for that
secondary value.  Equation (36) is the exact algebraic form of the
zero-indeterminacy requirement.

The attachment (29) is not asserted to be physical.  Its purpose is
sharper:
it proves that the axioms currently available for a *new* filtered target
cell--chain condition, correct leading target, ordered endpoint support,
and compatibility with all fixed literal identities--do not determine its
lower response.  More formally, this is the filtered extension of the
fixed complex by the single generator \(H\) with the displayed
differential.  Since the extension changes no old differential, all
connection, curvature, direct-double, cap, and scalar-unit identities
remain unchanged.  The two values \(\lambda=-1,0\) nevertheless give
different projected responses.

Equivalently, after fixing the coefficient of \(T\) to be one, the set of
allowed lower differentials is an affine torsor under
\(\operatorname {Hom}(\mathbb C H,\mathbb C Z)\cong\mathbb C Z\).  The
same-power lock selects the wrong target--response point for the desired
normalization.  The literal rows provide no source-graded second point.

## 6. Exact additional datum and scope

A successful construction along the literal route (19) must add all of the
following.

1. A relative filtered/Rees quotient in which the static Euler boundary
   (22) defines the intended adjacent-power connecting symbol.
2. A literal all-label five-site cell \(H_{r,s;x,c}\) whose ordered
   coefficient support is (19), including the \((c,c)\) target component
   and, in the scalar-unit packet, the ordered factors
   \(R_{ia}R_{aj}H_a\).
3. A target-nullhomotopy equation whose filtration-lowering odd component
   is zero--the source-provenant analogue of \(\lambda=0\) in (29)--and
   whose connection/normal part is a literal boundary.
4. Zero indeterminacy: if \(H,H'\) satisfy the same three requirements,
   then the odd residue of the lower component of \(H-H'\) must vanish.
   In particular, the relative quotient must not admit the old
   same-power cell \(S\) as a competing lift of \(H\), since (36) gives
   exactly the nonzero response as their difference at \(\lambda=0\).

Items 3--4 are exactly what distinguishes the desired lift from the
same-power lift \(\lambda=-1\) and from the rest of the torsor.  The full
five-site formula verifies the raw coefficient array but supplies no such
cell.  The scalar-unit Euler identity verifies the exceptional target but
supplies no such lower normalization.  Endpoint ordering fixes signs and
slots, but it does not select \(\lambda\).

Accordingly, the proved no-go is:

> **Ordered reconstruction / lift-torsor lemma.**  For every \(h\ge3\),
> the unique literal restriction--insertion reconstruction (19) sends the
> complete five-site comparison to zero.  The adjacent-power carrier is
> already a static boundary, so every strict chain lift of (19) sends it to
> a boundary.  The exceptional diagonal target is
> supported only in its matching diagonal endpoint cell.  After adjoining
> a target-cancelling filtered cell, its lower odd coordinate is an
> unconstrained response-line torsor; the existing same-power cell selects
> the zero-output point.  Therefore the displayed source identities alone
> neither construct nor uniquely determine a nonzero radial-to-response
> transgression.

This lemma does not rule out a physical secondary comparison with the four
properties above.  It identifies the exact datum that such a comparison
must contribute and prevents the canonical coefficient reconstruction,
the adjacent-power ledger, or the exceptional unary anchor from being
mistaken for that datum.

The dependency-free checker
[verify_ordered_five_site_reconstruction_transgression_lift_torsor_no_go.py](../computations/verify_ordered_five_site_reconstruction_transgression_lift_torsor_no_go.py)
audits ordered extraction/reinsertion, the unique diagonal target cell,
the two Euler-boundary normalizations, orientation reversal, and the
\(\lambda=-1,0\) filtered countercomplex, including adversarial endpoint,
sign, and normalization mutations, under normal Python and python -O.  The
proofs above, not its finite range of orders, are uniform in \(h\).
