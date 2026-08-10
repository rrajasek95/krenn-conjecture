# The common-missing-coordinate scalar gate also loses a dark target label

Research evidence only. Krenn's conjecture remains open,
**SP-CLEAN-BRIDGE** is not closed, and no certified dependency changes.

## Outcome

The joint-diagonal theorem
[`rank-one-rank-one-scalar-gate-diagonal-cycle.md`](rank-one-rank-one-scalar-gate-diagonal-cycle.md)
left one rank-two exception: both endpoint coefficient vectors have the same
missing fixed coordinate.  This note proves that the exception also cannot
retain all three dark target labels.

Combined with the rank-three theorem
[`rank-one-rank-one-scalar-gate-three-target-cofactor-unit.md`](rank-one-rank-one-scalar-gate-three-target-cofactor-unit.md),
the conclusion is now uniform across the entire maximal rank-\((1,1)\)
scalar gate:

\[
 \boxed{\text{some }\beta_{A,i}=0,
 \text{ hence }e_i^{(x)}\in\operatorname {span}(U_x,V_x)
 \text{ at some }x\in A.}                                 \tag{1}
\]

Thus every scalar gate routes to a literal fixed-label shore blocker.  The
remaining work is the same one-bright overlap required by the coordinate
gate; there is no longer a fully label-visible scalar branch.

## 1. Exact four-row normal form

Relabel the common missing coordinate as \(2\).  Then

\[
 \lambda=(\lambda_0,\lambda_1,0),\qquad
 \mu=(\mu_0,\mu_1,0),                                    \tag{2}
\]

with the four displayed nonzero coefficients.  Put

\[
 x=(\lambda_1,-\lambda_0,0),\qquad
 y=(\mu_1,-\mu_0,0).                                     \tag{3}
\]

The double-annihilator plane has rank-one basis

\[
 xy^{\mathsf T},\quad xe_2^{\mathsf T},\quad
 e_2y^{\mathsf T},\quad e_2e_2^{\mathsf T}.              \tag{4}
\]

Its diagonal images are respectively

\[
 (\lambda_1\mu_1,\lambda_0\mu_0,0),\quad0,\quad0,
 \quad(0,0,1).                                             \tag{5}
\]

The scalar-gate hypothesis kills every direct term in these four
contractions.  Contract a dark coefficient \(\theta\) and put
\(E=E_A(\theta)\).  Writing the four literal shore forms as \(L,M,N,V\),
the complete rows are

\[
\begin{aligned}
 LME&=aX_0+bX_1,\\
 LVE&=0,\\
 NME&=0,\\
 NVE&=cX_2,
\end{aligned}                                              \tag{6}
\]

where \(a,b,c\ne0\) whenever all three
\(\beta_{A,i}(\theta)\ne0\).

## 2. Normalizing the forced cofactor component

Assume all three \(\beta_{A,i}\) are nonzero functionals.  Finite
hyperplane avoidance again chooses \(\theta\) with \(abc\ne0\).  The last
row of (6) puts the pure tensor \(X_2\) in the image of multiplication by
\(E\).  Tensoring the three local quotients
\(V_s\to V_s/\mathbb CE_s\) shows that at one site the local component of
\(E\) is a nonzero multiple of the fixed \(e_2\)-axis.  Permute the three
shore sites and rescale that axis to obtain

\[
                         E_2=e_2^{(2)}.                    \tag{7}
\]

No restriction is placed on the other two local components \(E_0,E_1\).
This is strictly weaker than the full diagonal normalization used in the
rank-three packet.

## 3. Exact unit

Expand all four tensor equations (6) after (7).  Their \(108\) literal
three-site coefficients, together with

\[
                         zabc-1=0,                          \tag{8}
\]

generate the unit ideal over \(\mathbb Q\).  Exact Singular returns the
reduced basis `[1]` in both degree-reverse lexicographic and lexicographic
orders.  Independently generated runs over \(\mathbb F_2\) and
\(\mathbb F_{32003}\) give the same verdict.

Therefore the four-row packet (6) has no complex point with \(abc\ne0\), a
contradiction.  Some \(\beta_{A,i}\) is identically zero, and the tensor
factorization of \(\beta_{A,i}\) gives (1) exactly as in the rank-three
case.

## Scope

This removes the last fully label-visible scalar-gate packet.  It does not
close the fixed-label blocker (1), nor the original coordinate gate.  Both
now enter the same bounded one-bright four-site system.  Closing that system
would finish the entire maximal \(b=3\), rank-\((1,1)\) shore.

## Exact audit

The checker
[`verify_rank_one_rank_one_scalar_gate_rank2_common_missing_unit.py`](../computations/verify_rank_one_rank_one_scalar_gate_rank2_common_missing_unit.py)
pins the rank-three dependency, constructs the \(109\) exact generators,
and reproduces the four standard-basis unit calculations.  Generator and
output ledgers are SHA-256 pinned; the two unconstrained local components of
\(E\) remain fully symbolic.
