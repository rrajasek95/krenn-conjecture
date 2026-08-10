# A scalar-shore release cannot expose all three targets

Research progress only.  This closes the all-three-target released-site
subcase of the maximal rank-\((1,1)\) scalar shore.  It does **not** close a
singleton blocker for one fixed label: another label may remain blocked on
one of the two unreleased sites.  Krenn's conjecture and
`SP-CLEAN-BRIDGE` remain open.

## 1. Result

Use the notation of
[`n8-rank11-scalar-unique-blocker-common-power-packet.md`](n8-rank11-scalar-unique-blocker-common-power-packet.md).
Thus

\[
 A=\{x,y,z\},\qquad C=B\cup\{x\},\qquad |B|=3,
\tag{1}
\]

and \(x\) is released from the dark shore.  The scalar
gate chooses full-support \(u\in\ker\lambda^{\mathsf T}\) and
\(v\in\ker\mu^{\mathsf T}\).  Put

\[
 T=P_B(u),\qquad V=S_B(v).
\tag{2}
\]

As in the preceding scalar-gate notes, this is the branch away from the
original coefficient-vector gates
\(\lambda\parallel e_i\) and \(\mu\parallel e_i\); those are already
separate coordinate-gate outputs.  That assumption is exactly what permits
the simultaneous full-support choice of \(u,v\).

Both \(T\) and \(V\) are supported on \(B\); in particular

\[
                         T_x=V_x=0.                         \tag{3}
\]

The contracted literal full-nine row is

\[
 TVE_x(\theta)=\sum_{c=0}^2
   u_cv_c\,\beta_{A\setminus\{x\},c}(\theta)X_c^C .        \tag{4}
\]

If all three functionals on the right are nonzero, finite hyperplane
avoidance gives one \(\theta\) on which all three values are simultaneously
nonzero.  The new observation is that (3) makes this impossible: a
four-site multiplier with one common zero site cannot produce a diagonal
tensor having all three target colours nonzero.

Consequently every release retains a blocker for at least one target label
on the two unreleased sites.  Equivalently, the union of all target blocker
sets on the three-site dark shore cannot be a singleton.  A blocker set for
one particular label may still be a singleton; it then forces a companion
blocker for another label at a different site.

## 2. The zero-site splitting lemma

Let \(C=B\sqcup\{x\}\), \(|B|=3\), and work in the site-square-zero
algebra on \(C\).  Let \(T,V\) be arbitrary local linear forms satisfying
\(T_x=V_x=0\), and let

\[
 \mu_{T,V}:({\cal R}_C)_2\longrightarrow({\cal R}_C)_4,
 \qquad Q\longmapsto TVQ .                                \tag{5}
\]

Write \(D=\operatorname{span}\{X_0^C,X_1^C,X_2^C\}\).

**Lemma 2.1.**  The intersection \(\operatorname{im}\mu_{T,V}\cap D\)
is a coordinate subspace.  More explicitly, if

\[
                  TVQ=\sum_c a_cX_c^C,                    \tag{6}
\]

then \(X_c^C\in\operatorname{im}\mu_{T,V}\) for every \(c\) with
\(a_c\ne0\).

**Proof.**  A quadratic component of \(Q\) avoiding \(x\) is supported on
two sites of the three-set \(B\).  Its complementary multiplier block must
use \(x\), so it vanishes by (3).  Hence only components meeting \(x\)
survive.  Write their sum uniquely as

\[
                         Q_x=\sum_c e_c^{(x)}L_c,           \tag{7}
\]

with \(L_c\) a linear form on \(B\).  Then

\[
                         TVQ=\sum_c e_c^{(x)}TVL_c.         \tag{8}
\]

The three vectors \(e_c^{(x)}\) are independent.  Comparing (8) with (6)
gives

\[
                         TVL_c=a_cX_c^B.                   \tag{9}
\]

For \(a_c\ne0\), multiplication of \(a_c^{-1}e_c^{(x)}L_c\)
by \(TV\) is exactly \(X_c^C\).  This proves the lemma. \(\square\)

The lemma is special to the literal released-site support.  It is false for
a general four-site multiplier with no common zero site; no unsupported
classification of arbitrary two-dimensional diagonal intersections is
being used.

## 3. Contradiction for an all-three-target release

The already proved
[`four-site arbitrary-superposition obstruction`](four-site-arbitrary-superposition-dressed-packet-obstruction.md)
says that one multiplier \(TV\) contains at most two individual pure targets
in its image.  If the three
\(\beta_{A\setminus\{x\},c}\) are nonzero, choose \(\theta\) in (4)
outside their kernels.  Full support of \(u,v\) makes all three coefficients

\[
                a_c=u_cv_c\beta_{A\setminus\{x\},c}(\theta)\ne0.
\tag{10}
\]

Lemma 2.1 turns (4) into membership of all three \(X_c^C\), contradicting
that obstruction.  Notice that no recombination of three different
coefficients \(\theta\), no rank-three hypothesis, and no independent
relaxation of \((E_x,F_x)\) is involved.

## 4. Two live released labels force a coordinate plane

The sharp equality case also has a useful source-faithful normal form.
Suppose exactly two released labels \(a,b\) are live.  Lemma 2.1 and (9)
give linear forms \(L_a,L_b\) on the three-set \(B\) such that, after
nonzero rescaling,

\[
                         TVL_a=X_a^B,\qquad TVL_b=X_b^B.    \tag{11}
\]

For \(s\in B\), put \(S_s=\operatorname{span}(T_s,V_s)\).  Apply the
quotient maps \(V_r\to V_r/S_r\) and \(V_s\to V_s/S_s\) at any two
distinct sites \(r,s\in B\).  Every term of \(TVL_c\) assigns \(T,V\) to
two of the three sites and \(L_c\) to the third.  At least one of the two
quotiented sites therefore carries \(T\) or \(V\), so the double quotient
kills the entire left side of (11).  It cannot kill \(X_c^B\) unless

\[
                         e_c\in S_r\quad\hbox{or}\quad e_c\in S_s.
\tag{12}
\]

Thus each of the two axes \(e_a,e_b\) belongs to at least two of the three
local spaces \(S_s\).  These are four containment incidences on three
sites.  If no site contained both axes, there would be at most three.
Consequently some \(s\in B\) satisfies

\[
                         S_s=\operatorname{span}(e_a,e_b). \tag{13}
\]

So the equality boundary is not an arbitrary binary four-site packet: it
exports a literal coordinate endpoint plane on the physical three-site
complement.  The remaining one-live case has no such conclusion from the
multiplier alone.

## 5. The blocker incidence forces some coordinate plane

Return to all three blocker sets

\[
 Z_c=\{s\in A:e_c^{(s)}\in\operatorname{span}(U_s,V_s)\}.
\tag{14}
\]

The scalar cofactor theorem says that their union is nonempty.  Suppose
first that some dark site belongs to two sets, say \(s\in Z_a\cap Z_b\).
Then its two-dimensional-or-smaller local span contains the independent
axes \(e_a,e_b\), so

\[
                  \operatorname{span}(U_s,V_s)
                    =\operatorname{span}(e_a,e_b).         \tag{15}
\]

This is already a literal coordinate plane.  Assume no such dark plane.
Then every dark site carries at most one blocker incidence.

If some release has two live labels, (13) gives a coordinate plane on the
physical complement \(B\).  Assume this does not happen either.  A globally
unblocked label is live after every release.  It would force each of the
other two blocker sets to have size at least two; that is at least four
incidences on three dark sites, contradicting the no-dark-plane assumption.
Thus every label is blocked.  There are at least three incidences, and at
most one per site, so equality holds: after relabelling,

\[
                         Z_0=\{x_0\},\quad
                         Z_1=\{x_1\},\quad
                         Z_2=\{x_2\},                      \tag{16}
\]

with \(x_0,x_1,x_2\) distinct.

This rainbow is impossible.  Release \(x_c\) and choose a dark coefficient
on the other two sites for which the restored \(c\)-target is nonzero.
Equation (9) supplies a linear form \(L_c\) on the **same** three-site
complement \(B\) with

\[
                              TVL_c=X_c^B.                 \tag{17}
\]

Doing this for \(c=0,1,2\) puts all three pure targets in the image of the
same multiplier \(TV\).  Adjoin any one common zero site \(x\) and use
\(e_c^{(x)}L_c\) as the three quadratic preimages.  This is a four-site
multiplier containing all three \(X_c\), contrary to the arbitrary-
superposition theorem.

We have therefore proved the uniform scalar-shore alternative

\[
 \boxed{\text{some physical local multiplier span is a target coordinate
 plane}.}                                                   \tag{18}
\]

The plane occurs either in \(\operatorname{span}(U_s,V_s)\) on the dark
shore or in \(\operatorname{span}(T_s,V_s)\) on the three-site physical
complement after a two-live release.  This is not automatically the
original coefficient-vector gate \(\lambda\parallel e_i\) or
\(\mu\parallel e_i\); transporting (18) into an active clean cap remains
the next source problem.

## 6. The moving complement plane becomes a fixed-label identity

There is no need to retain a plane depending on the particular generic cap.
Let

\[
 H_\lambda=\ker\lambda^{\mathsf T},\qquad
 H_\mu=\ker\mu^{\mathsf T},                               \tag{19}
\]

and vary \((u,v)\) over the dense open subset on which all six fixed
coordinates are nonzero.  The product \(H_\lambda\times H_\mu\) is
irreducible.  The dark-shore alternatives (15) are independent of
\((u,v)\).  If one occurs, the plane is already fixed.

Assume none occurs.  For every generic \((u,v)\), equation (13) gives a
site \(s\in B\) and a missing coordinate \(k\) such that

\[
 P_s(u),\ S_s(v)\in \Pi_k:=\operatorname{span}\{e_i:i\ne k\}.
\tag{20}
\]

There are only nine choices \((s,k)\).  For each one, (20) is a Zariski
closed linear condition on \(H_\lambda\times H_\mu\).  Their finite union
covers a dense open subset, hence covers the whole irreducible product.
An irreducible variety cannot be a finite union of proper closed subsets,
so one fixed pair \((s,k)\) obeys (20) identically.  Equivalently,

\[
 e_k^*P_s\big|_{H_\lambda}=0,qquad
 e_k^*S_s\big|_{H_\mu}=0.                                \tag{21}
\]

The annihilator of \(H_\lambda\) is \(\mathbb C\lambda^{\mathsf T}\),
and similarly for \(\mu\).  Thus there are scalars \(c,d\) such that the
literal fixed-label cells satisfy

\[
 \boxed{
   p_{i,s}(k)=c\lambda_i,\qquad
   s_{j,s}(k)=d\mu_j
   \quad(0\le i,j\le2).}                                 \tag{22}
\]

Combining the two alternatives, every maximal scalar gate away from the
original coefficient-vector coordinate gate produces either

1. a fixed dark-site plane (15), or
2. a fixed complement site and target coordinate satisfying (22).

Unlike a cap-dependent rank count, (22) is a source-labelled row identity.
It is the correct input for the next two-chart assignment-sum comparison.

## 7. Proof impact and remaining incidence packet

The earlier common-power note correctly proved
\(\operatorname{rank}\beta_{A\setminus\{x\}}\le2\), but its subsequent
sentence that a singleton blocker for one label makes all three released
functionals nonzero was not automatic.  The support split above supplies
the exact replacement: the set of nonzero released target functionals has
size at most two, and equality forces (13).  Thus the maximal scalar shore
now routes as follows.

1. The scalar unit theorem supplies a fixed lost target label.
2. Its blocker set is nonempty.
3. Releasing any one site cannot make all three target functionals live.
4. Therefore blocker incidences occupy at least two distinct shore sites.
5. A release with two live labels enters the coordinate-plane boundary
   (13).
6. If every release has at most one live label, the only plane-free blocker
   ledger is the rainbow (16), and its three common-multiplier rows are
   impossible.

The scalar shore has therefore been routed to a fixed literal local
coordinate plane, with the complement case sharpened to (22).  What remains
is to identify (15) or (22) with an existing coordinate/endpoint-dark
descent, or to use the fixed-label proportionality to construct the
source-valid assignment-sum comparison detected by the provenance quotient.
The physical dark-cut theorem remains available, but its differential has
not yet been identified with that source comparison.

On the rank-three complement-plane branch, this last comparison has now
been bypassed.  The
[fixed-plane provenance closure](n8-rank11-scalar-fixed-plane-provenance-closure.md)
shows that (22) makes the unique target-free cap response vanish, so the
scalar provenance quotient is already zero.  The still-live cases are the
rank-two common-missing packet and the alternative fixed plane on the dark
shore.

## 8. Exact audit

[`verify_n8_rank11_scalar_released_site_three_target_closure.py`](../computations/verify_n8_rank11_scalar_released_site_three_target_closure.py)
pins the arbitrary-superposition and common-power dependencies and audits all
54 endpoint-coloured quadratic columns.  Exactly 27 columns avoid \(x\) and
vanish; the other 27 split into three disjoint nine-column blocks according
to their fixed \(x\)-colour.  It also checks the conditional
three-nonzero-factor ledger of (10) and exhausts the two-target containment
ledgers behind (13).  It also exhausts the blocker-set incidence: away from
the two coordinate-plane exits there are exactly six rainbow ledgers, all
of which feed the same three-target multiplier contradiction.  The proof
above is uniform over \(\mathbb C\).  The checker also audits the nine
finite plane labels and the elementary hyperplane-annihilator implication
behind (22).  It is a deterministic regression audit, not a finite
substitute.
