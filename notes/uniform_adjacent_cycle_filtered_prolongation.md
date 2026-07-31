# A uniform adjacent-cycle prolongation is a horizontal splitting, not a suspension

## 1. Outcome

Assume, at the first residual boundary \(h=3\), that the two adjacent
all-label full-nine systems really supply the grade-preserving row proposed
in
[`separating-three-three-opposite-shore-leakage-bianchi-boundary.md`](separating-three-three-opposite-shore-leakage-bianchi-boundary.md):
after the target, normal, direct, and internal companions are retained and
cancelled in their literal grades, its residual is a specified two- or
three-colour projection of

\[
       H_{XX}\dot S_X+\dot P_Y^{\mathsf T}H_{YY},
\]

and its remaining scalar coefficient is

\[
                         \lambda(AU-BF),\qquad \lambda\ne0.       \tag{1}
\]

This hypothesis is stronger than the one-chart identities currently
proved.  Granting it still does **not** determine a uniform filtered
prolongation.  There are two logically independent readouts:

1. on a rootless clean line, one nonzero common functional in
   \((\operatorname {Sym}^{2h-1}U^*)^*\) annihilating every clean
   coordinate and all \(h\) shifts; and
2. on an all-inactive line, a target-zero correction whose torus--Koszul
   middle coefficient is the negative of the surviving odd residue.

The second readout has no remaining high-degree interpolation problem:
the certificate--bracket prolongation theorem constructs the full
degree-\(2d\) correction once one source-filtered radial-to-response value
is available.  The first readout remains a separate decorated
colon-to-Hankel comparison.

This note proves an abstract lift-torsor lemma which gives the exact common
zero-indeterminacy condition for both readouts.  It then shows that literal
site suspension of the hypothetical \(h=3\) row does not prove that
condition:

* site suspension has clean-line parameter degree zero and cannot naturally
  promote a degree-five Macaulay functional to degree (2h-1);
* the activity polynomial
  \(s^{2h-6}\kappa _0\kappa _1\kappa _2\) has the right numerical
  degree, but has the wrong variance until a determinant line is
  trivialized, and the current raw anchor cuts do not identify the
  selector conic with the clean cap line;
* abstract based-loop deformations in a freely completed path-lift model
  preserve the adjacent row, its endpoints, and its associated graded, but
  move all required weighted moments independently;
* evaluated divisibility at a diagonal third boundary gives principal
  parts only in the evaluation kernel, not in the literal boundary module;
  and
* the intrinsic scalar-unit branch already needs the first weighted
  horizontal row at \(h=3\).

There are two exact ways to remove indeterminacy.  If the operation is
reconstructed from its evaluated row, the first missing source identity is
the **vertical-homology annihilation**

\[
 \boxed{
 H(\mathfrak R_h)\bigl(\ker H(\pi_h)\bigr)=0,}                   \tag{2}
\]

for the actual adjacent full-nine filtered complex when the combined
readout kills ambient boundaries.  Here \(\ker H(\pi_h)=\operatorname{im}
H(i)\), not necessarily all of \(H(\mathscr V_h)\); for a readout defined
only modulo vertical boundaries, the stronger domain
\(H(\mathscr V_h)\) must replace it, as Lemma 2.1 records.  The map \(\pi_h\)
is the combined constraint map recording literal reinsertion/evaluation,
the fixed target component, the prescribed associated-graded data, and the
chosen literal connection/normal boundary certificate;
\(\mathfrak R_h\) is the combined Macaulay, odd-middle, principal-parts,
and intrinsic-unary readout defined below.  Equation (2) says only that
the desired operation is independent of its filtered nullhomotopy.  A
positive theorem must additionally construct one horizontal lift with the
normalized nonzero values.  No existing named lemma proves either
assertion.

Alternatively, one can define the operation as a literal raw fixed-block
coefficient cut before selector normalization.  Such a cut is canonical
and excludes the abstract based-loop deformations by definition, but it
must satisfy the still-unproved **grade-split landing identity**

\[
 \boxed{
  \operatorname {pr}_{\rm bad}{\mathscr X}_h=dB_h,
  \qquad \operatorname {tar}{\mathscr X}_h=0,
  \qquad \operatorname {pr}_{\rm low}{\mathscr X}_h={\cal N}_h.}       \tag{2a}
\]

Here \({\mathscr X}_h\) extracts every exposed-site coefficient in the
literal fixed-block polynomial, \(\operatorname {pr}_{\rm bad}\) denotes
the direct/internal/normal companions which must be killed as boundaries,
and \({\cal N}_h\) is the required lower carrier.  At \(h=3\), (2a)
contains the grade-split sum-channel relation whose addition raises the
known source-row rank.  Thus the raw route removes the torsor only by
replacing (2) with a new, currently independent, source identity.

Thus the attempted construction yields a precise conditional sufficiency
theorem and a sharp obstruction, not an active-clean theorem or a proof of
Krenn's conjecture.

## 2. The filtered cone and its lift torsor

Let \(\mathscr C_h\) denote the literal all-label two-chart source complex,
filtered by the connection, normal, curvature, direct-double, cap, and
target grades.  This is notation for the complex which a positive proof
must construct; the existing evaluated identities do not by themselves
define it.  Let

\[
 \pi_h:\mathscr C_h\longrightarrow
   \mathscr E_h\oplus\mathscr T_h\oplus\mathscr G_h
       \oplus\mathscr Q_h^{\rm cn}                                      \tag{3}
\]

be the combined chain map which (i) reinserts the exposed sites and
evaluates the literal row in the site-square-zero matching algebra,
(ii) records its target grade, and (iii) records every associated-graded
component fixed in the definition of an allowed lift.  The fourth
component explicitly records condition 4: enlarge the cone by a
connection/normal primitive \(b_{\rm cn}\), and let its
\(\mathscr Q_h^{\rm cn}\)-coordinate be

\[
             \operatorname {cn}(H_h)-d b_{\rm cn}.                      \tag{3a}
\]

Thus that coordinate is zero exactly when the connection/normal part has
a **literal chosen boundary certificate**.  It is not merely evaluation
of that part.  This enlargement is essential: the kernel of evaluation
alone could still change the target or condition 4.  Replace the displayed
codomain by the image subcomplex of \(\pi_h\), so that \(\pi_h\) is
degreewise surjective.  From now on \(\mathscr C_h\) denotes this enlarged
cone and \(H_h\) denotes its full cone cell, including \(b_{\rm cn}\).  Put

\[
                         \mathscr V_h=\ker\pi_h.                         \tag{4}
\]

The hypothetical adjacent row determines a fixed evaluated cone cell
\(g_h\) only after an all-order construction is supplied.  An **allowed
horizontal lift** includes the primitive in (3a) and is a chain
\(H_h\in\mathscr C_{h,1}\) satisfying:

1. \(\pi_h(H_h)\) is the fixed evaluated coefficient row together with
   its prescribed target and associated-graded data;
2. \(dH_h\) is the prescribed adjacent curvature/cap cone boundary;
3. its total target is zero, with the exceptional diagonal target retained
   until this nullhomotopy; and
4. its \(\mathscr Q_h^{\rm cn}\)-constraint (3a) is zero.

The precise differential signs depend on the chosen cone convention and
are immaterial for the following elementary statement.

Write \(Z_1(\mathscr V_h)=\ker(d:\mathscr V_{h,1}\to
\mathscr V_{h,0})\) and
\(B_1(\mathscr V_h)=d(\mathscr V_{h,2})\), and let
\(i:\mathscr V_h\hookrightarrow\mathscr C_h\) be inclusion.

> **Lemma 2.1 (horizontal lift torsor).**  If the allowed-lift set
> \(\mathcal L_h\) is nonempty, define
> \[
> H_h\sim_{\mathscr V}H'_h
>       \quad\Longleftrightarrow\quad
> H_h-H'_h\in B_1(\mathscr V_h).
> \]
> Then \(\mathcal L_h/\!\sim_{\mathscr V}\) is an affine torsor under
> \(H_1(\mathscr V_h)\).  If instead allowed lifts are identified whenever
> their difference lies in \(B_1(\mathscr C_h)\), the effective acting
> group is
> \[
> \operatorname {im}i_*
>   \simeq {H_1(\mathscr V_h)\over\ker i_*}
>   =\ker H_1(\pi_h).                                      \tag{5}
> \]
> Hence a readout which kills ambient boundaries is independent of the
> lift exactly when its induced homology map annihilates
> \(\operatorname {im}i_*=\ker H_1(\pi_h)\).  A merely source-relative
> readout which is known only to kill \(B_1(\mathscr V_h)\) must instead
> annihilate all of \(H_1(\mathscr V_h)\).

**Proof.**  If \(H_h,H'_h\in\mathcal L_h\), their fixed differentials
agree and every component of (3) agrees, so
\(H_h-H'_h\in Z_1(\mathscr V_h)\).  Conversely, adding any element of
\(Z_1(\mathscr V_h)\) preserves the differential and all four constraints.
Quotienting the differences by \(B_1(\mathscr V_h)\) gives the free and
transitive \(H_1(\mathscr V_h)\)-action.  Passing further to ambient
homology identifies two acting classes precisely when their difference
lies in \(\ker i_*\).  Finally, degreewise surjectivity of \(\pi_h\) gives
the short exact sequence
\(0\to\mathscr V_h\to\mathscr C_h\to\operatorname {im}\pi_h\to0\);
exactness of its homology sequence gives
\(\operatorname {im}i_*=\ker H_1(\pi_h)\).  The two readout criteria are
then immediate.  \(\square\)

The lemma is deliberately relative: it neither assumes \(i_*\) injective
nor requires all vertical homology to vanish.  Only the effective action
seen by the chosen readout must be killed.

### 2.2 Canonical raw cuts bypass the torsor only after a landing theorem

Coefficient extraction from a literal fixed-block polynomial is a
canonical linear operator and commutes with polynomial equality.  If
\({\mathscr X}_h\) in (2a) were proved to land in the desired lower
carrier, then its full dependence on the cap parameter would be fixed.
The abstract based loops in Section 6.6 would not be alternative
representatives of that raw operation, so every weighted moment would be
determined without proving (2).

The current raw-anchor theorem stops one step earlier.  It computes the
target coefficient before normalization and its frame defect after
normalization, but the raw source cut still has components in several
literal grades.  Coefficient extraction is division-free; **projection to
the lower carrier is not yet legal**, because the unwanted companions
have not been shown to be boundaries.  Equation (2a), rather than
canonicity of coefficient extraction, is the missing desuspension.  The
rank calculation in Section 6.3 proves that it is not a linear consequence
of the currently named \(h=3\) rows.

## 3. The four components of the combined readout

Define

\[
 \mathfrak R_h=
   \mathfrak M_h\oplus\mathfrak T_{c,h}\oplus
   \mathfrak P_{\ell,r,h}\oplus\mathfrak U_{a,h}.               \tag{6}
\]

These summands are used on different branches; packaging them in one map
does not identify their target spaces.

### 3.1 Rootless Macaulay readout

Let \(U\) be the canonical binary clean-line parameter space and let
\(\mathcal E_h\subseteq\operatorname {Sym}^hU^*\) be the span of the
scalar clean-error coordinates.  Write

\[
  \mathfrak M_h(H_h)=\Theta_h=(\theta_0,\ldots,\theta_{2h-1})
       \in(\operatorname {Sym}^{2h-1}U^*)^*.                    \tag{7}
\]

For

\[
 f_\alpha(s,t)=\sum_{k=0}^h c_{\alpha,k}s^{h-k}t^k,
\]

the required chain property is the single common Hankel system

\[
 \boxed{
   \sum_{k=0}^h c_{\alpha,k}\theta_{k+j}=0
   \quad\text{for every }\alpha\text{ and }0\le j\le h-1.}     \tag{8}
\]

Equivalently,

\[
                         \mu_{\mathcal E_h}^*(\Theta_h)=0.       \tag{9}
\]

The readout must also satisfy \(\Theta_h\ne0\).  The residual-Macaulay
gcd theorem then turns (9) into a common clean root.  On the rootless
branch this is an immediate contradiction.

This is one functional across all coordinates and shifts.  A separate
functional for each anchor, chart, or shift is insufficient.

### 3.2 Inactive middle-coefficient readout

On a routed inactive binary line let

\[
 \Omega\in V\otimes\mathbb C[t,u]_d,
 \qquad H\in V^*\otimes\mathbb C[t,u]_d,
 \qquad\langle H,\Omega\rangle=(tu)^d,                         \tag{10}
\]

and let \(0\ne\widehat\zeta_c\in C\) be the normalized odd residue.
The required value is

\[
                    \boxed{\mathfrak T_{c,h}(H_h)
                                      =-\widehat\zeta_c.}       \tag{11}
\]

More invariantly, the horizontal lift must first give the order-zero
source-filtered normal value

\[
                 \tau_h(\gamma z)=\gamma\widehat\zeta_c,        \tag{12}
\]

with the target nullhomotoped in a different filtration grade.  If
\(\ell\) is the ordered complementary transverse form and
\([\gamma,\ell]\ne0\), the already proved certificate--bracket theorem
then gives

\[
 G_c=-[\gamma,\ell]^{-1}[\tau_h(\gamma z),\ell]
                  \langle H,\Omega\rangle
     =-\widehat\zeta_c(tu)^d.                                  \tag{13}
\]

This is the full coefficient correction, not just its middle term.  It is
independent of the Bezout certificate.  Therefore no additional Hermite
interpolation is needed after (12).

### 3.3 Diagonal Rees principal parts

On a generic diagonal line let \(\ell\) be the third boundary factor and
write a filtered residual representative as

\[
            \widetilde\Omega=
              \sum_{j=0}^d\ell^jw^{d-j}P_j.                    \tag{14}
\]

If the evaluated coordinate gcd contains \(\ell^r\), then
\(P_0,\ldots,P_{r-1}\in\ker\epsilon\).  Literal division is legal only if

\[
            \boxed{P_0,\ldots,P_{r-1}\in N_{\rm lit}.}          \tag{15}
\]

The principal-parts readout is therefore

\[
 \mathfrak P_{\ell,r,h}(H_h)=
  [\widetilde\Omega\bmod\ell^r]
   \in {\ker\epsilon\over N_{\rm lit}}
            \otimes(\mathbb C[\ell,w]/(\ell^r))_d.             \tag{16}
\]

Its required value is zero.  The literal principal-parts criterion then
gives the filtered quotient by tail extraction, after which (11)--(13)
apply to the two-boundary packet.

### 3.4 Intrinsic order-\(h\) unary readout

At \(A_{pq}=\alpha E_{aa}\), the full normal-jet theorem supplies

\[
 \mathcal E(xE_{aa}+D)=x^hU_a+x^{h-1}R_D\Theta_a
       +\sum_{m=2}^h x^{h-m}R_D^{[m]}G_a^{[h-m]},       \qquad
 \Theta_a=R_{aa}H_a.                                           \tag{17}
\]

On the clean unary branch \(U_a=0\), one has \(\Theta_a\ne0\) at the
chosen minimum-support good pair.  A legal filtered comparison must retain
the exceptional target and desuspend the ordered squares

\[
                         R_{ia}R_{aj}H_a.                        \tag{18}
\]

The Hermite source-path calculation shows that the necessary target-side
moments are fixed, but in the abstract path-lift completion a horizontal
source lift can be changed by based loops.  The intrinsic readout
\(\mathfrak U_{a,h}\) records the resulting moment residues.  Its required
value is zero on every vertical cycle that is actually realized in
\(\mathscr V_h\).  At \(h=3\), the first nontrivial component is already

\[
 \boxed{
 \mathfrak o_1([z\,d(t(1-t))])
   =-{1\over6}\bigl[(R-2Q)\chi_{jk}(z)\bigr]=0,}                \tag{19}
\]

where \(\chi_{jk}\) is the still-unconstructed source desuspension map.
The stronger relative-saturation identity

\[
                H(\chi_{jk})(\ker H(\pi_{jk}))=0                \tag{20}
\]

implies (19) and all higher moment vanishings at once.

## 4. Conditional rootless and routed-inactive exclusions

The preceding definitions isolate branchwise sufficient statements, not
an exhaustive active-clean theorem.  The displayed version uses the
reconstructive mapping-cone route.  In a raw-cut version, hypotheses 1--2
are replaced by a canonical \({\mathscr X}_h\) satisfying (2a); the
branch readout and comparison hypotheses remain unchanged.

For an already routed inactive branch \(b\), let
\(\mathscr D_{b,h}\) be its literal source cone (after the Rees quotient,
when one is required), let \(\mathscr K_{b,h}\) be the target-coefficient
complex, and let \(m=m(b,h)\) be the residue degree.  These names do not
assert a comparison: the chain map and its homological faithfulness are
part of hypothesis 7 below.

> **Theorem 4.1 (conditional rootless and routed-inactive exclusion).**
> Suppose, for every relevant \(h\ge3\), the actual adjacent all-label
> source packet admits:
>
> 1. an allowed horizontal lift \(H_h\) of the cycle--curvature row with
>    nonzero coefficient (1);
> 2. the zero-indeterminacy identity (2);
> 3. on a rootless branch, the nonzero common Hankel value (7)--(9);
> 4. on an already routed off-diagonal inactive branch, the normalized
>    value (11)--(12);
> 5. on an already routed generic diagonal branch, the vanishing
>    principal-parts value (16), followed on the literal Rees quotient by
>    the normalized value in hypothesis 4;
> 6. on an already routed intrinsic scalar-unit branch with the unary cap
>    clean, \(U_a=0\), the exceptional target and ordered carrier (18),
>    with (19) equal to zero (or the stronger (20)); and
> 7. for each branch claimed in the second conclusion, an explicit chain
>    comparison
>    \[
>       \Phi_{b,h}:\mathscr D_{b,h}\longrightarrow\mathscr K_{b,h},
>    \]
>    a physical cycle \(\widehat\zeta_b\) whose nonzero class spans
>    \(L_{b,h}=\mathbb C[\widehat\zeta_b]
>       \subset H_m(\mathscr D_{b,h})\), and a literal corrected
>    target-zero chain \(G_{b,h}\in\mathscr K_{b,h,m+1}\) satisfying
>    \[
>       dG_{b,h}=\Phi_{b,h}(\widehat\zeta_b),
>       \qquad
>       H_m(\Phi_{b,h})|_{L_{b,h}}\text{ is injective}.           \tag{20a}
>    \]
>
> Then hypotheses 1--3 exclude the rootless branch.  Moreover,
> hypotheses 1--2, the relevant one of 4--6, and hypothesis 7 exclude that
> already routed inactive branch.

**Proof.**  On the rootless branch, (8)--(9) give a nonzero element of the
dual kernel of the clean Macaulay map.  Rootlessness makes the Macaulay map
surjective, so its dual kernel is zero, a contradiction.

For an off-diagonal routed branch, minimum-order survival supplies the
nonzero physical class \([\widehat\zeta_b]\), while (11)--(13) construct
the corrected chain in (20a).  Hence
\(H_m(\Phi_{b,h})([\widehat\zeta_b])=0\); injectivity on \(L_{b,h}\)
contradicts its nonvanishing.  On a generic diagonal branch, (15)--(16)
first make the tail extraction a literal source quotient, and the same
argument applies there.  On the clean-unary intrinsic branch,
(17)--(20), together with the explicitly assumed comparison (20a), gives
the identical homology contradiction. \(\square\)

The chain map, bounding equation, and restricted homology injection in
hypothesis 7 are essential: cancellation of a displayed coefficient alone
does not kill a physical source class.  In particular, no existing result
constructs the intrinsic unary map \(\Phi_{b,h}\) into the same exact
coefficient mechanism as the off-diagonal residue.

The theorem is deliberately silent about the nonintrinsic diagonal
trace-collision branch \(\beta=0\), where a one-chart adaptive line is
available but no source-faithful two-chart comparison has been constructed.
It is also silent about the intrinsic dirty target-plane branch
\(A_{pq}=\alpha E_{aa}\) with \(U_a\ne0\).  Thus these alternatives are not
claimed to be exhausted, and Theorem 4.1 has no active-clean-point
conclusion.

## 5. Which existing lemmas suffice after the missing identity

The positive downstream algebra is already available.

| Required step | Existing named result | Exact role |
|---|---|---|
| Static colon cycle and site suspension | `full-27-colon-cycle-macaulay-transfer-gap` | Supplies \((x_b\omega,\Gamma_b)\) and tensors it by a disjoint matching word; it does not define a Hankel map. |
| Rootless contradiction from one common dual | `residual-macaulay-quotient-is-the-common-divisor` | A nonzero element of \(\ker\mu_{\mathcal E_h}^*\) is exactly a common divisor/root. |
| Minimal odd Cartan slot and its coefficient equations | `odd-covariant-filtered-hankel-naturality-obstruction` | Shows that the auxiliary order is \(2h-3\), gives the exact Cartan convolution, and proves that correct degree and nonvanishing do not imply the Hankel cut. |
| Physical odd cofactor type | `pure-target-one-site-polarization-and-odd-cofactor-gap`, Section 4 | Supplies the \(2h-3\) residual target factors, conditional on still-missing local maps \(\phi_x:V_x\to U_{\rm cl}^*\); it proves neither those maps nor their common Hankel equations. |
| Raw anchor-frame readout | `diagonal-anchor-four-cut-leakage-holonomy-transgression` | Recovers the selector connection modulo reciprocal diagonal gauge from three labelled four-cuts; it does not compare the selector conic with the cap line. |
| Aggregate/source-grade admissibility | `hessian-pullback-filtered-source-provenance`, Propositions 2.1 and 4.1 | Tests whether the four-cut pullback is represented by top rows plus literal graded overlap rows. |
| Nonzero inactive class | `odd-residue-minimality-survival` | Supplies a surviving colour on a minimum-order forbidden source. |
| Unique inactive obstruction | `inactive-omega-torus-koszul-overlap-residue` | Reduces the coefficient complex to its single middle class. |
| All-order coefficient correction | `residue-chain-map-radial-transgression`, Theorem 5.1 | Turns (12) into (13), independently of the certificate. |
| Same-power exclusion | `offdiagonal-same-power-target-residue-lock` | Proves the target nullhomotopy must be cross-quotient/filtered. |
| Generic diagonal quotient | `diagonal-rees-saturation-cap-jet-bockstein`, Lemma 4.1 | Turns (15) into a canonical filtered quotient at every multiplicity. |
| Intrinsic surviving datum | `scalar-unit-full-normal-jet-unary-anchor-ledger` | Supplies (17)--(18) and \(\Theta_a\ne0\) on the clean unary branch. |
| First intrinsic moment obstruction | `scalar-unit-hermite-source-path-first-moment-lift-obstruction` | Identifies (19)--(20); \(H_1\) is already indispensable at \(h=3\). |

The negative ledgers explain why these results cannot themselves establish
(2): the adjacent-power class is an Euler boundary while the completed row
is a colon class; ordinary Yoneda/cup multiplication sends the relevant
product to zero; ordered reconstruction leaves an affine lower-response
torsor; and based-loop deformations in the free path-lift completion move
the higher moments without changing the associated graded.

## 6. Attempted prolongation of the hypothetical \(h=3\) row

### 6.1 What literal suspension proves

Adjoin \(2h-6\) sites in disjoint pairs and let \(V_h\) be their complete
matching word.  The divided-power suspension calculation gives

\[
 \zeta_h=\zeta_3\otimes V_h,\qquad d\zeta_h=0.                  \tag{21}
\]

The same tensoring applies to any hypothetical grade-preserving adjacent
row whose old-site terms occupy every old site.  Thus (21) is a genuine
all-order **static** cycle on the specially suspended packet.

It proves neither naturality for an arbitrary order-\(h\) source nor
compatibility with the binary clean-line parameter.  The word \(V_h\) has
clean-line parameter degree zero.

### 6.2 Rootless suspension stops before the Hankel shifts

Suppose optimistically that the \(h=3\) row produces a quintic functional
\(\Theta_3\in(\operatorname {Sym}^5U^*)^*\).  For \(h>3\), there is no
nonzero \(SL(U)\)-natural linear map

\[
              \operatorname {Sym}^5U
                 \longrightarrow\operatorname {Sym}^{2h-1}U,            \tag{22}
\]

because the two irreducible representations have different highest
weights.  A Cartan-product prolongation needs an additional source-derived
even covariant

\[
                          \rho_{2h-6}\in\operatorname {Sym}^{2h-6}U.     \tag{23}
\]

The static matching word \(V_h\) does not supply (23).  Even if a form
\(\rho_{2h-6}\) is chosen, one must still prove

\[
             \mu_{\mathcal E_h}^*(\Theta_3\rho_{2h-6})=0.               \tag{24}
\]

No representation-theoretic or divided-power identity implies (24).
The exact pure-axis test

\[
                         \mathcal E_h=\langle s^h,t^h\rangle             \tag{25}
\]

has \(\mathcal E_h\operatorname {Sym}^{h-1}U^*
=\operatorname {Sym}^{2h-1}U^*\), so its dual kernel is zero.  Hence no
rule depending only on the suspended static row can produce the required
nonzero functional for arbitrary clean coordinates.

### 6.3 The activity covariant is degree-correct but does not satisfy the cut

Let the homogeneous clean cap line be

\[
                         K(u,v)=uK_0+vK_1,
\]

and let \(U_{\rm cl}\) be its two-dimensional parameter space.  The
direct and target contractions are genuine source-derived linear forms

\[
 s,\kappa _0,\kappa _1,\kappa _2\in U_{\rm cl}^*.
\]

Generic activity says that their product is not the zero polynomial.
Consequently

\[
 \boxed{
 a_h:=s^{\,2h-6}\kappa _0\kappa _1\kappa _2
       \in\operatorname {Sym}^{2h-3}U_{\rm cl}^*\setminus\{0\}}          \tag{25a}
\]

does close the numerical degree gap.  On the canonical off-diagonal line
\(K(u,v)=uE_{ab}+vI\), \(a\ne b\), it is

\[
 s=\alpha u+\tau v,\qquad \kappa _0=\kappa _1=\kappa _2=v,
 \qquad a_h=(\alpha u+\tau v)^{2h-6}v^3.                       \tag{25b}
\]

At \(h=3\) this is exactly \(v^3\).  On a diagonal canonical line the
corresponding product is
\((\alpha u+\tau v)^{2h-6}(u+v)v^2\), after naming its selected colour
first.

There are nevertheless two typing conditions before (25a) can be used.
First, the selector cycle supplies
\(\Psi_C=\vartheta _2\in\operatorname {Sym}^2U_{\rm sel}\), not on
\(U_{\rm cl}\); one needs a source-derived projective comparison
\(\iota:U_{\rm sel}\simeq U_{\rm cl}\).  Second, (25a) is covariant,
whereas the Cartan auxiliary lies in
\(\operatorname {Sym}^{2h-3}U_{\rm cl}\).  The canonical two-dimensional
variance identity is

\[
 U_{\rm cl}^*\simeq U_{\rm cl}\otimes(\det U_{\rm cl})^{-1},             \tag{25c}
\]

so raising (25a) introduces the twist
\((\det U_{\rm cl})^{-(2h-3)}\).  A volume form removes it under
\(SL(U_{\rm cl})\), but a \(GL(U_{\rm cl})\)-natural construction must
carry or trivialize this line explicitly.

Even granting both choices, the candidate

\[
 \Theta_h=C\bigl(\iota_*\Psi_C,a_h^\sharp\bigr)                         \tag{25d}
\]

is merely a nonzero element of the correct target representation.  The
full-nine equations currently proved do not imply

\[
                  \boxed{\mu_{\mathcal E_h}^*(\Theta_h)=0.}             \tag{25e}
\]

At \(h=3\), write \(\Psi_C=(q_0,q_1,q_2)\) in divided-differential
coordinates.  Cartan multiplication by the off-diagonal target cubic
\(v^3\) gives

\[
                 \Theta_3=(0,0,0,q_0,4q_1,10q_2).                       \tag{25f}
\]

For the exact pure-axis test
\(\mathcal E_3=\langle u^3,v^3\rangle\), the six Macaulay shifts form
the coordinate basis of \(\operatorname {Sym}^5U_{\rm cl}^*\).
Therefore (25f) has Hankel residual
\((q_0,4q_1,10q_2)\), and (25e) forces \(\Psi_C=0\).  This is a formal
coefficient guard, not a physical Krenn counterexample; it proves that
activity, correct degree, and a nonzero selector cycle do not perform the
missing coefficient cut.

The retained \(h=3\) source grades sharpen this failure.  In the exact
rational packet, set

\[
 \begin{aligned}
 F_0&=\operatorname {Haf}_6(q)=4,\\
 \Psi_C&=a_{12}a_{20}\Phi_{01}
       +a_{20}a_{01}\Phi_{12}+a_{01}a_{12}\Phi_{20},\\
 \chi_C&=[e_0e_1e_2e_3]z^{[2]}=1,\\
 \kappa&=AU-BF,\qquad \Theta=F_0\Psi_C.
 \end{aligned}
\]

The full source presentation uses coordinates

\[
                  (\Theta,\Xi,\kappa,C,D,L,N),
\]

where \(\Xi\) is the cycle-projected crossed coefficient and
\(C,D,L,N\) are the curvature, direct, connection, and normal top
components.  Its anchor-reconstruction row, crossed target-zero row, two
high Euler rows, and low Euler row have rank five.  Adjoining the missing
division-free transgression

\[
 \boxed{\Theta-\chi_C\kappa
       =F_0\Psi_C-\chi_C(AU-BF)=0}                                     \tag{25g}
\]

raises the full rank to six.  The curvature Euler row is
\(C=2\chi_C\kappa\), so (25g) is equivalently

\[
                         F_0\Psi_C-\tfrac12C=0.
\]

In the reduced grade-only presentation, \(\Theta\) is retained as the
external anchor datum while the auxiliary \(\Xi\)-coordinate and the two
independent anchor-reconstruction/crossed bookkeeping rows are suppressed.
The remaining three Euler rows have rank three, and adjoining the same row
(25g) raises that rank to four.  Thus the reduced \(3\to4\) and full
\(5\to6\) statements are the same one-row rank jump in two presentations,
not competing audits.

On the displayed full coordinates, the separating witness is

\[
                         (0,0,1,2,-2,-1/4,1/4).
\]

Every retained row annihilates it, whereas (25g) evaluates to \(-1\): in
particular \(F_0\Psi_C=0\) and \(\chi_C(AU-BF)=1\).  Thus even at \(h=3\)
a new **grade-split sum-channel row** is required; neither suspension nor
the activity cubic repairs the static rank jump.  The exact audit is
[`verify_adjacent_full_nine_h3_cycle_transgression.py`](../computations/verify_adjacent_full_nine_h3_cycle_transgression.py).

### 6.4 The physical-factor product is better typed locally, but is not constructed

Section 4 of
`pure-target-one-site-polarization-and-odd-cofactor-gap` removes two
distinct pure-anchor sites and leaves the physical tensor

\[
             \bigotimes_{x\notin S}e_c^{(x)},
             \qquad |D_h\setminus S|=2h-3.
\]

If the same adjacent source supplied local maps

\[
             \phi_x:V_x\longrightarrow U_{\rm cl}^*,
             \qquad
 \widetilde a_h=\prod_{x\notin S}\phi_x(e_c^{(x)}),                   \tag{25h}
\]

then \(\widetilde a_h\) would be a much more source-sensitive candidate
than (25a).  It still has the variance twist (25c), and it still must
satisfy (25e) after Cartan multiplication.

The raw diagonal-anchor four-cuts do not yet define the maps in (25h).
They live on a residual **probe path**, not on the cap-covector line.  For
one label they give only

\[
 {\mathscr C}_c{\cal D}(t)=g_c(t)E_{cc},\qquad
 g_c(t)=u_{x_c,c}(t)u_{y_c,c}(t),
\]

and their normalized-minus-raw derivative recovers
\(-X^{\mathsf T}E_{cc}-E_{cc}Y\).  Hence they provide a pair product and
a target-frame connection modulo reciprocal diagonal gauge.  They do not
provide a linear map on every \(V_x\), a map
\(U_{\rm sel}\to U_{\rm cl}\), or the \(h\) common Macaulay shifts.
The rotating-frame guard shows that all raw cofactors may even stay
constant while these frame defects are nonzero.

Nor is (25h) identified with (25a).  The forms \(s,\kappa_c\) are global
contractions on the deleted cap slots, while the \(\phi_x\) would be local
maps on the odd complement.  Their equality would itself be a new
factorization identity.  Already at \(h=3\), the off-diagonal activity
candidate is \(v^3\), whereas a physical pure-site candidate may be a
product of three distinct lines \(\ell_e\ell_a\ell_b\).

### 6.5 Pure carriers do not make reinsertion injective without retained tags

The pure-factor lemma gives existence, not uniqueness, of a witness site.
Even in the most favourable linear model, for a fixed label \(c\) and a
set \(W_c\) of possible witness sites put

\[
 P_c=\bigoplus_{x\in W_c}\mathbb C\mathbf e_{c,x},\qquad
 \pi_c(\mathbf e_{c,x})=X_c.
\]

Then

\[
 \ker\pi_c=\left\{(a_x)_{x\in W_c}:\sum_xa_x=0\right\}.                \tag{25i}
\]

Thus reinsertion is injective on each individual summand but not on their
direct sum unless the source has selected a unique witness.  Different
labels cannot cancel because the \(X_c\) are independent; different sites
for the same label do cancel because reinsertion forgets the witness tag.

The existing anchor lemmas do not supply uniqueness.  The two anchors
with a common factor force an \(e\)-pure and an \(a\)-pure site to be
distinct, but they do not make either witness set a singleton.  Moreover,
Section 5 of the pure-target note gives three labelled anchor
factorizations whose witnesses occupy only two sites.  Hence complete
anchor labels alone do not force a direct sum of three distinct fixed-site
carriers.

If one replaces \(\pi_c\) by a fully tagged raw-cut map
\(\mathbf e_{c,x}\mapsto E_{c,x}\), injectivity is tautological.  What is
not proved is that all relevant vertical cycles land in this tagged pure
submodule, that the complete family of tags is retained by a chain map,
or that \(\chi_{jk}\) factors through it.  The concrete remaining
witness-exchange identity is

\[
 \boxed{
   [\chi_{jk}(\mathbf e_{c,x}-\mathbf e_{c,y})]=0
   \quad(x,y\in W_c),}                                           \tag{25j}
\]

together with vanishing on the non-pure vertical complement.  Proving
that every exchange is a literal boundary would establish the desired
relative injectivity without killing all vertical homology.  No current
pure-factor or raw-four-cut lemma proves it.

### 6.6 Inactive coefficient prolongation is formal; its source lift is not

Once (12) is granted at a fixed \(h\), equation (13) proves every
coefficient and the correct middle sign.  This is the maximal positive
uniform statement available from the current algebra.

However, in the freely completed polynomial path-lift model used to test
the reconstructive route of Lemma 2.1, two lifts with the same adjacent row
may differ by an abstract based loop.  Let

\[
 \eta_j(t)={d^{j-1}\over dt^{j-1}}\bigl(t^j(1-t)^j\bigr),\qquad j\ge1.
\]

For the weighted moments needed through (m=h-3) (and through (m=1)
at \(h=3\)), their changes are

\[
 \Delta_{sj}=\int_0^1t^s\,d\eta_j(t),\qquad
 \Delta_{sj}=0\ (s<j),\qquad
 \Delta_{jj}=(-1)^j{(j!)^3\over(2j+1)!}\ne0.                  \tag{26}
\]

Thus the moment map from this abstract based-loop space is triangular and
invertible.  Every required higher moment can be shifted while preserving
the endpoints, unweighted lift, and associated-graded row.  At \(h=3\),
the first shift is already \(-1/6\), exactly (19).  These \(\eta_j\) are
conditional ambiguity probes: no current lemma realizes them as physical
vertical cycles in the actual adjacent complex \(\mathscr V_h\).  They
therefore show that evaluated endpoints and associated-graded data do not
by themselves prove lift uniqueness; they do **not** prove that a physical
raw fixed-block lift has this ambiguity.

This abstract guard does not obstruct a literal raw fixed-block cut
satisfying (2a): such a cut chooses its parameter polynomial before
evaluation and admits no loop mutation.  What is missing for that
alternative is lower-carrier landing, not moment uniqueness.

### 6.7 Rees saturation also fails before division

The two-dimensional principal-parts guard

\[
 M=\langle z,r\rangle,\qquad N=0,\qquad
 \epsilon(z)=0,\quad\epsilon(r)=1,\qquad P=wz+\ell r              \tag{27}
\]

has \(\epsilon(P)=\ell\), but \(P\) is not divisible by \(\ell\) in
\(M\otimes\mathbb C[\ell,w]\).  Its literal remainder modulo \(\ell\) is
\(wz\), giving the nonzero principal part
\([z]\otimes w\in(\ker\epsilon/N)\otimes\mathbb C[w]\).  Tensoring an
\(h=3\) adjacent row by extra matching
sites does not put \([z]\) in the literal boundary module.  Thus (15),
not coordinate divisibility, is the first diagonal source statement.

## 7. The first genuinely missing identities

Existence and uniqueness must be separated, but a canonical raw operation
changes which one comes first.

* **Raw-cut route.**  The first missing source identity is the
  grade-split landing (2a).  Its \(h=3\) scalar shadow is (25g), which is
  rank-independent of every currently named row.  If (2a) is proved,
  coefficient extraction canonically fixes the lift and all weighted
  moments.  One must still prove the separate rootless coefficient cut
  (25e), or the inactive normalization (11)--(12), on its lower carrier.
* **Reconstructive mapping-cone route.**  Construct one actual full-nine
  horizontal lift whose branch readouts have the prescribed values, and
  prove (2), so every vertical difference has zero image.  The first
  nontrivial coefficient of this zero-indeterminacy condition occurs
  already at \(h=3\):

\[
 \boxed{
 [(R-2Q)\chi_{jk}(z)]=0
 \quad\text{for every }[z]\in\ker H(\pi_{jk}).}                 \tag{28}
\]

The stronger and cleaner mapping-cone statement is (20).  For the
diagonal quotient,
the same identity appears as \([P_0]=\cdots=[P_{r-1}]=0\) in
\(\ker\epsilon/N_{\rm lit}\).  For the rootless readout, it says that the
common Hankel functional assigned to a horizontal lift is unchanged by
every filtered source boundary and vertical cycle.

No current row identity proves (2a), (25e), or (28).  The one-chart cycle
formula, power-free Bianchi rows, static full-27 cycle, target-residue
lock, and Hermite endpoint interpolation all factor through \(\pi_h\),
so they are blind to \(\ker H(\pi_h)\).  The pure-carrier shortcut would
prove (28) if it established the witness-exchange relation (25j) and
killed the non-pure vertical complement, but the present anchors do
neither.

Thus the earliest missing algebra for a canonical construction is the
grade-split sum-channel (2a); for an abstract lift construction it is the
vertical saturation (28).  Even after either source problem is solved,
the rootless branch still needs the common Hankel equation (25e).  The
named lemmas in Section 5 perform the downstream coefficient algebra only
after these new identities and a nonzero normalization are supplied.

## 8. Exact audit scope

The dependency-free checker
[`verify_uniform_adjacent_cycle_filtered_prolongation.py`](../computations/verify_uniform_adjacent_cycle_filtered_prolongation.py)
audits the finite-dimensional algebra used in the obstruction:

* the pure-axis Macaulay map has rank \(2h\) for each tested \(h\);
* the activity candidate has order \(2h-3\), specializes to \(v^3\) at
  the off-diagonal \(h=3\) boundary, and has the nonzero Cartan--Hankel
  residual (25f);
* reinsertion on two same-label pure witness summands has a one-dimensional
  exchange kernel, while a fully tagged cut is injective;
* the abstract based-loop moment matrix is triangular with the diagonal
  (26), and its \(h=3\) entry is \(-1/6\);
* the required auxiliary clean-line order is (2h-6); and
* direct arithmetic in \(M\otimes\mathbb C[\ell,w]\) gives evaluated
  divisibility but the nonzero literal remainder \(wz\bmod\ell\).

The proof of Lemma 2.1, the representation-theoretic observation (22),
the pure-axis span, the triangular moment formula, and the principal-parts
guard are uniform.  The checker is only an exact arithmetic audit.  It
does not construct \(\mathscr C_h\), \({\mathscr X}_h\), \(\chi_{jk}\), a
horizontal lift, or any of (2a), (25e), and (28).
