# A unique scalar-shore blocker has a literal four-site common-power packet

Research evidence only.  Krenn's conjecture and `SP-CLEAN-BRIDGE` remain
open, and no certified dependency changes.

> **Scope correction and additive sharpening.**  A singleton blocker for
> one fixed label does not imply that the other two released target
> functionals are nonzero.  The released-site splitting theorem in
> [`n8-rank11-scalar-released-site-three-target-closure.md`](n8-rank11-scalar-released-site-three-target-closure.md)
> proves the exact replacement: at most two released target labels are
> live, so a singleton blocker forces a companion blocker for another label
> on one of the two unreleased sites.  If two labels remain live, one
> physical complement site has their literal coordinate plane as its
> multiplier span.  The common-power formulas below remain the exact
> provenance audit.

## Outcome

The maximal rank-\((1,1)\) scalar shore now always loses at least one fixed
target label.  Let (i) be such a label and put

\[
 Z_i=\{x\in A:e_i^{(x)}\in\operatorname {span}(U_x,V_x)\}.
\tag{1}
\]

This note separates the two exact possibilities.

* If \(|Z_i|=1\), freeing its unique site restores the (i)-th target.
  At (N=8), the resulting one-bright four-site tensors have the explicit
  common-power form (5).  The zero-site splitting theorem forces at least
  one other target label to remain blocked on the unreleased pair.
* If \(|Z_i|\ge2\), every one-site release still misses label (i).  This
  is a genuinely different multiple-blocker branch and must be handled by a
  two-site compatibility or a fixed-axis descent.

Thus the highest-impact remaining scalar-shore problem is a two-site
blocker-incidence packet: either one label has multiple blockers or two
labels have blockers at distinct sites.  The scalar gate no longer needs a
separate resultant or support census.

## 1. Why the blocker set is exact

On the rank-\((1,1)\) shore,

\[
 K_x=\ker(P_x^*\oplus S_x^*)
     =\operatorname {ann}\langle U_x,V_x\rangle .
\tag{2}
\]

The fixed target functional factors sitewise:

\[
 \beta_{A,i}=\bigotimes_{x\in A}
      \epsilon_i^{(x)}\big|_{K_x}.
\tag{3}
\]

Consequently \(\beta_{A,i}=0\) exactly when (Z_i\ne\varnothing).  If
(Z_i=\{x\}), then
\(\beta_{A\setminus\{x\},i}\ne0\).  Moreover any other target functional
which survived on (A) also survives after deleting (x).  Finite
hyperplane avoidance chooses a decomposable dark coefficient on the other
shore sites for which all these surviving target values are simultaneously
nonzero.

The two scalar-shore unit theorems prove that some (Z_i) is nonempty in
every scalar packet.  They do not prove that it is a singleton; that
quantifier is the only reason the multiple-blocker boundary is retained.

## 2. Exact consecutive-power provenance at eight sites

At (N=8), after deleting the selected physical pair the residual set has
six sites.  In the unique-blocker case write

\[
 A=\{x,y,z\},\qquad C=B\cup\{x\}=W\setminus\{y,z\}.
\tag{4}
\]

Choose dark covectors at (y,z) with the required nonzero target values.
For the literal residual quadratic (q), let

* (d) be its contracted (yz)-cell;
* (r_y,r_z) be the contracted (y)- and (z)-stars restricted to (C);
* (q_C) be the restriction of (q) to the four sites (C).

Direct matching separation gives

\[
\boxed{
\begin{aligned}
 E_x&=\iota_y\iota_z q^{[2]}=d q_C+r_yr_z,\\
 F_x&=\iota_y\iota_z q^{[3]}
     =d q_C^{[2]}+r_yr_zq_C.
\end{aligned}}
\tag{5}
\]

There are only two matching types.  Either (y,z) are paired together,
giving the (d)-term, or they meet two distinct sites of (C), giving the
(r_yr_z)-term.  No coefficient is hidden and no division or localization
is used.

Substituting (5) into the literal one-bright equations (61)--(63) of
[`endpoint-dark-shore-consecutive-power-jet.md`](endpoint-dark-shore-consecutive-power-jet.md)
produces the smallest honest scalar-shore closure problem.  In particular,
allowing independent (E_x,F_x) is an unsound relaxation: formal four-site
response packets exist which do not come from consecutive powers of one
quadratic.

## 3. The released target has rank at most two

There is a further uniform consequence at (N=8).  Stay on the scalar gate
away from the original coordinate gates.  Choose

\[
 u\in\ker\lambda^{\mathsf T},\qquad
 v\in\ker\mu^{\mathsf T}
\tag{6}
\]

with every fixed coordinate nonzero, and put (K=uv^{\mathsf T}).  Finite
hyperplane avoidance makes this choice possible.  The scalar gate gives
\(\sigma(K)=0\), while the two annihilator equations make the response on
the released four sites

\[
 r(K)=P_B(u)S_B(v)=TV.                                    \tag{7}
\]

Contracting the literal full-nine row on the remaining dark coefficient
space gives

\[
 TVE_x(\theta)=\sum_{c=0}^2u_cv_c
       \beta_{A\setminus\{x\},c}(\theta)X_c^C.             \tag{8}
\]

If \(\beta_{A\setminus\{x\}}\) had rank three, three choices of
\(\theta\), followed by an invertible (3\times3) scalar recombination,
would produce quadratics (Q_c\) satisfying

\[
                         TVQ_c=X_c^C\qquad(c=0,1,2).        \tag{9}
\]

This contradicts the proved
[`four-site arbitrary-superposition obstruction`](four-site-arbitrary-superposition-dressed-packet-obstruction.md),
which allows at most two pure targets in the image of one multiplier (TV).
Therefore

\[
 \boxed{\operatorname {rank}\beta_{A\setminus\{x\}}\le2.} \tag{10}
\]

Conditionally, if all three individual target functionals in (10) were
nonzero, write them on the two remaining shore sites as

\[
 a_c\otimes b_c,qquad c=0,1,2.                            \tag{11}
\]

Three nonzero rank-one tensors spanning a space of dimension at most two
have one of the following exact forms:

1. two of (11) are proportional, so the same two fixed labels are
   proportional on both remaining sites; or
2. no two are proportional, in which case all (a_c\)'s are proportional
   or all (b_c\)'s are proportional.

For the second statement, express the third tensor as a linear combination
of the first two.  Every (2\times2) minor of that sum is the product of a
left wedge and a right wedge.  Rank one forces one complete wedge family to
vanish.  Since the restrictions of the three coordinate evaluations span
the dual dark kernel, the second alternative says that one remaining dark
kernel is one-dimensional.  Thus (10) leaves only a rank-two local endpoint
plane or a repeated two-label alignment at both remaining sites.  The
released-site splitting theorem now excludes this conditional three-live
subcase outright.  It does not exclude one or two live released labels.

## 4. Proof impact

The repo-wide proof spine is

\[
 \text{physical active line}
 \dashrightarrow\text{active clean cap}
 \longrightarrow N\mapsto N-2
 \longrightarrow\text{the proved six-site contradiction}.
\]

The dashed arrow remains the only conjecture-level gap.  Within the maximal
rank-\((1,1)\) shore, the rank-three and common-missing rank-two unit
theorems route every scalar packet to (1), and the zero-site splitting
theorem forces blocker incidences onto at least two shore sites.  Therefore
the next useful local theorem is exactly their two-site compatibility: turn
either a same-label multiple blocker or two different-label singleton
blockers into an active clean cap, a fixed-axis descent, or the source-valid
assignment-sum comparison detected by the scalar provenance quotient.

This would also meet the fixed-label input left by the coordinate and
endpoint-dark shore reductions.  By contrast, another orbit plateau,
support-only face census, or higher Hasse/Spencer enumeration would not
touch this source-faithful packet.

## Exact audit

[`verify_n8_rank11_scalar_unique_blocker_common_power_packet.py`](../computations/verify_n8_rank11_scalar_unique_blocker_common_power_packet.py)
expands both sides of (5) in all independent endpoint-coloured cells of a
generic six-site quadratic and independent contraction coefficients.  It
also checks all eight local live/blocker patterns for each target label,
audits the distinct three-point Segre-line classification on 169 exact
projective rank-one tensors, and pins the four-site obstruction and the two
scalar-shore dependencies.  The common-power audit is symbolic, uses the
standard library only, and makes no random specialization.
