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

## 5. Proof impact and remaining incidence packet

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
   (13); the residual non-plane release has at most one live label.

The remaining scalar-shore gate is consequently a genuine **two-site
blocker-incidence packet**.  This includes both a multiple blocker for one
label and two singleton blockers for different labels.  Their compatibility
must either produce an active clean cap, enter a coordinate/endpoint-dark
descent, or construct the source-valid assignment-sum comparison detected by
the provenance quotient.  The physical dark-cut theorem remains available,
but its differential has not yet been identified with that source
comparison.

## 6. Exact audit

[`verify_n8_rank11_scalar_released_site_three_target_closure.py`](../computations/verify_n8_rank11_scalar_released_site_three_target_closure.py)
pins the arbitrary-superposition and common-power dependencies and audits all
54 endpoint-coloured quadratic columns.  Exactly 27 columns avoid \(x\) and
vanish; the other 27 split into three disjoint nine-column blocks according
to their fixed \(x\)-colour.  It also checks the conditional
three-nonzero-factor ledger of (10) and exhausts the two-target containment
ledgers behind (13).  The proof above is uniform over \(\mathbb C\); the
checker is a deterministic regression audit, not a finite substitute.
