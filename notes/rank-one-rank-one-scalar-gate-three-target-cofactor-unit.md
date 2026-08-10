# The rank-\((1,1)\) scalar gate cannot retain all three dark target labels

Research evidence only. Krenn's conjecture remains open,
**SP-CLEAN-BRIDGE** is not closed, and no certified dependency changes.

## Outcome

Continue from the exact diagonal classification in
[`rank-one-rank-one-scalar-gate-diagonal-cycle.md`](rank-one-rank-one-scalar-gate-diagonal-cycle.md).
On the rank-three part of the maximal \(b=3\), rank-\((1,1)\) scalar gate,
the diagonal map from the clean double-annihilator plane is surjective.
This note proves the following uniform strengthening.

> **Three-target cofactor theorem.**  Let \(A\) be the large dark shore and
> \(B\) its three-site complement.  At least one fixed target functional
> \(\beta_{A,i}\) vanishes identically.  Equivalently, for some physical
> label \(i\) there is a site \(x\in A\) such that
> \[
>                    e_i^{(x)}\in\operatorname {span}(U_x,V_x). \tag{1}
> \]

Thus the fully label-visible scalar gate is empty.  The remaining scalar
gate is forced into a literal fixed-coordinate blocker on the large shore,
so it joins the existing coordinate/one-bright overlap problem rather than
remaining an independent adjacent-power branch.

The theorem is uniform in \(h\ge3\), uses the actual common cofactor
\(q^{[h-1]}\), and retains arbitrary complex cancellation.

## 1. Rank-one diagonal lifts

Write

\[
 H_\lambda=\ker\lambda^{\mathsf T},\qquad
 H_\mu=\ker\mu^{\mathsf T},\qquad
 {\cal Q}=H_\lambda\otimes H_\mu.                         \tag{2}
\]

When the diagonal map \(\delta:{\cal Q}\to\mathbb C^3\) has rank three,
each coordinate target has a rank-one lift.  After multiplying each lift by
a nonzero scalar (which only rescales its nonzero target coefficient), write
the three responses as \(L_iM_i\).  The zero patterns of
\(\lambda,\mu\) give exactly the following normal forms, up to endpoint
transpose and physical-label permutation:

\[
\begin{array}{c|ccc}
 A&L_0M_0&L_1M_1&(L_0+L_1)(M_0+M_1)\\
 B&LM_0&LM_1&N(M_0+M_1)\\
 D&LM&LV&NM.
\end{array}                                                \tag{3}
\]

Form \(A\) occurs when both \(\lambda,\mu\) have full support.  Form
\(B\) occurs when exactly one has a missing coordinate.  Form \(D\)
occurs when both have different missing coordinates.  If they have the
same missing coordinate, the diagonal map has rank two and belongs to the
separate packet already isolated in the preceding note.

The normalization in (3) is projective, not an extra equation.  Three
distinct lines in a two-space admit representatives summing to zero.
Multiplying the three cap equations by independent nonzero scalars absorbs
the remaining line weights into their target coefficients.

## 2. The common cofactor has a diagonal three-site normalization

Assume for contradiction that all three \(\beta_{A,i}\) are nonzero.
The coefficient space

\[
                 {\cal K}_A=\bigotimes_{x\in A}K_x         \tag{4}
\]

is a complex vector space.  Finite-hyperplane avoidance gives one
\(\theta\in{\cal K}_A\) with
\(\beta_{A,0}(\theta)\beta_{A,1}(\theta)
\beta_{A,2}(\theta)\ne0\).  Put

\[
                         E=E_A(\theta)=\iota_\theta q^{[h-1]}
                         \in({\cal R}_B)_1.                \tag{5}
\]

Contracting the three rank-one cap rows gives

\[
                 L_iM_iE=b_iX_i^B,
                 \qquad b_i\ne0.                           \tag{6}
\]

There is a useful elementary normalization lemma.  Write
\(E=E_0+E_1+E_2\) by its local components on the three sites of \(B\).
Multiplication by \(E\) has image

\[
 E_0\otimes V_1\otimes V_2
 +V_0\otimes E_1\otimes V_2
 +V_0\otimes V_1\otimes E_2.                              \tag{7}
\]

Tensoring the quotient maps \(V_s\to V_s/\mathbb CE_s\) kills (7).
If \(X_i^B\) lies in (7), at least one local factor
\(e_i^{(s)}\) must lie on \(\mathbb CE_s\).  Apply this to all three
distinct pure tensors in (6).  One local vector cannot be proportional to
two different fixed axes, so the three sites are used bijectively.  After a
site permutation and invertible diagonal site scalings,

\[
                  E=e_0^{(0)}+e_1^{(1)}+e_2^{(2)}.          \tag{8}
\]

The same scalings preserve (3); they merely replace the already arbitrary
nonzero scalars \(b_i\).

## 3. Exact coefficient unit

For each of the three normal forms in (3), expand every coefficient of the
three equations (6) after (8).  There are \(81\) literal coefficient rows.
Adjoin one localization row

\[
                         z b_0b_1b_2-1=0.                  \tag{9}
\]

Over \(\mathbb Q\), the resulting ideal is the unit ideal for each of
\(A,B,D\).  The exact reduced standard basis is `[1]` in both degree-reverse
lexicographic and lexicographic orders.  The same independently generated
systems give `[1]` over \(\mathbb F_2\) and \(\mathbb F_{32003}\).
Therefore (6) has no complex solution with all \(b_i\ne0\), contradicting
the chosen dark coefficient.

Consequently some \(\beta_{A,i}=0\).  Since

\[
 \beta_{A,i}=\bigotimes_{x\in A}
       \epsilon_i^{(x)}\big|_{K_x},                        \tag{10}
\]

one factor vanishes.  For that site,
\(\epsilon_i^{(x)}|_{K_x}=0\), equivalently the physical vector
\(e_i^{(x)}\) lies in the span of the two local shore forms \(U_x,V_x\).
This proves (1).

## Scope

This closes the fully label-visible rank-three scalar gate.  It does not
close:

1. the rank-two common-missing-coordinate packet;
2. the rank-three packet after the forced blocker (1); or
3. the separate coordinate gate of the clean quotient plane.

The latter two now share the same one-bright fixed-coordinate input, so the
next proof obligation is the literal four-site overlap equation, not another
scalar adjacent-power interpolation.

## Exact audit

The checker
[`verify_rank_one_rank_one_scalar_gate_three_target_cofactor_unit.py`](../computations/verify_rank_one_rank_one_scalar_gate_three_target_cofactor_unit.py)
pins the preceding diagonal-cycle dependency, enumerates all sixteen pairs
of endpoint support patterns (one \(A\), six \(B\), six \(D\), and three
rank-two exceptions), constructs all \(82\) generators in each normal form,
and invokes exact Singular standard bases in the four coefficient/order
settings stated above.  Generator and output ledgers are SHA-256 pinned.
