# The rank-\((1,1)\) scalar gate has one canonical diagonal-zero cycle

Research evidence only. Krenn's conjecture remains open,
**SP-CLEAN-BRIDGE** is not closed, and no certified dependency changes.

## Outcome

Continue with the maximal three-site rank-\((1,1)\) shore of
[`rank-one-rank-one-shore-clean-quotient-plane.md`](rank-one-rank-one-shore-clean-quotient-plane.md).
Thus

\[
 p_i^A=\lambda_iU,\qquad s_j^A=\mu_jV,
 \qquad
 {\cal Q}=\{K:\lambda^{\mathsf T}K=0,\ K\mu=0\},
 \tag{1}
\]

and assume the direct scalar vanishes on the whole clean plane \({\cal Q}\).
Suppose first that neither endpoint is on a coordinate gate:
\(\lambda\not\parallel e_i\) and \(\mu\not\parallel e_i\) for every
physical label \(i\).  The three diagonal functionals are not merely
individually nonzero.  Their joint map

\[
 \delta:{\cal Q}\longrightarrow\mathbb C^3,
 \qquad K\longmapsto(K_{00},K_{11},K_{22})                 \tag{2}
\]

has the exact rank classification

\[
 \boxed{
 \operatorname {rank}\delta=
 \begin{cases}
 2,&\lambda_k=\mu_k=0\text{ for one common }k,\\
 3,&\text{otherwise.}
 \end{cases}}                                               \tag{3}
\]

The exceptional case in (3) is a new sharply named boundary: both endpoint
stars have the same missing colour on the large shore.  Outside it,
\(\delta\) is surjective and its kernel is one-dimensional.

Contracting the complete physical rows gives

\[
 r(K)q^{[h-1]}=\sum_iK_{ii}X_i\qquad(K\in{\cal Q}),        \tag{4}
\]

where every \(r(K)\) is supported on the three-site shore.  Hence in the
rank-three case there are nonzero literal shore quadratics \(R_i\) and a
canonical cycle response \(R_*\) satisfying

\[
 \boxed{
 R_iq^{[h-1]}=X_i\quad(i=0,1,2),
 \qquad R_*q^{[h-1]}=0.}                                   \tag{5}
\]

All four arise by contracting the same nine physical rows; no abstract
target splitting or independently normalized chart is used.  This replaces
the four-dimensional scalar gate by one fixed four-row source packet.

If every coordinate of \(\lambda,\mu\) is nonzero, put

\[
 C=(\lambda_0\lambda_1\lambda_2)
   (\mu_0\mu_1\mu_2).
\]

The unique diagonal-zero cap has the explicit entries

\[
 (K_*)_{ij}=
 \begin{cases}
  C/(\lambda_i\mu_j),&(i,j)=(0,1),(1,2),(2,0),\\
 -C/(\lambda_i\mu_j),&(i,j)=(1,0),(2,1),(0,2),\\
 0,&i=j.
 \end{cases}                                                \tag{6}
\]

Writing \(\widehat p_i=p_i^B/\lambda_i\) and
\(\widehat s_j=s_j^B/\mu_j\), its response is the alternating triangle

\[
 \frac{R_*}{C}=
 \widehat p_0\widehat s_1+\widehat p_1\widehat s_2
 +\widehat p_2\widehat s_0
 -\widehat p_1\widehat s_0-\widehat p_2\widehat s_1
 -\widehat p_0\widehat s_2.                                \tag{7}
\]

Equivalently,

\[
 \frac{R_*}{C}=
 (\widehat p_0-\widehat p_2)(\widehat s_1-\widehat s_2)
 -(\widehat p_1-\widehat p_2)(\widehat s_0-\widehat s_2).  \tag{8}
\]

Thus the remaining generic scalar gate has a literal affine Segre-cycle
annihilator, not an unspecified element of a response kernel.  The cycle
response may itself vanish; that is a distinguished degeneration of the
packet, not a contradiction.  The next uniform input is correspondingly
precise: combine (5)--(8) with one freed shore-site row to show that the
three nonzero pure lifts cannot coexist with either this cycle annihilator
or its zero-response degeneration.  The endpoint-dark one-bright equations
(57)--(63) are already exactly that source level.

This note does not prove that the four-row packet (5) is impossible.  It
also does not eliminate the common-missing-coordinate case of (3).  Those
are the two residual scalar-gate packets.

## Proof of the rank classification

Put \(H_\lambda=\ker\lambda^{\mathsf T}\) and
\(H_\mu=\ker\mu^{\mathsf T}\).  The clean plane is canonically
\(H_\lambda\otimes H_\mu\).  Let \(a_i\) and \(b_i\) be the restrictions
of the \(i\)-th coordinate functionals to these two-dimensional spaces.
The dual of (2) sends the \(i\)-th basis vector to

\[
                         a_i\otimes b_i.                    \tag{9}
\]

The no-coordinate-gate hypothesis says that none of the six factors in
(9) is zero.  For distinct \(i,j\), the two left factors are proportional
exactly when \(\lambda_k=0\), where \(\{i,j,k\}=\{0,1,2\}\); the analogous
right statement uses \(\mu_k=0\).

Three nonzero decomposable tensors in a tensor product of two
two-dimensional spaces are dependent here only if one pair is
proportional.  Indeed, if the first two left factors and first two right
factors are both independent, their span is the diagonal subspace in
suitable bases and contains no third rank-one tensor with both coordinates
nonzero.  If exactly one pair of left factors is proportional, a dependence
forces the corresponding right pair to be proportional as well; all three
left factors cannot be proportional because the coordinate restrictions
span \(H_\lambda^*\), and similarly on the right.  Therefore the tensors
in (9) are dependent exactly when the same pair is proportional on both
sides, equivalently when \(\lambda_k=\mu_k=0\).  In that case precisely two
of (9) are proportional and the rank is two.  Otherwise the rank is three.

Since \(\dim{\cal Q}=4\), surjectivity leaves a one-dimensional kernel.
Formula (6) is checked directly against
\(\lambda^{\mathsf T}K_*=K_*\mu=0\) and the zero diagonal.  Equations
(4)--(5) then follow by linearity and the full physical contraction.

## Exact audit

The standard-library checker
[`verify_rank_one_rank_one_scalar_gate_diagonal_cycle.py`](../computations/verify_rank_one_rank_one_scalar_gate_diagonal_cycle.py)
enumerates all rational hyperplane vectors with at least two nonzero
coordinates over \(\{-3,-1,0,1,2\}\).  For every ordered pair it constructs
the four-dimensional double-annihilator plane, computes the exact diagonal
rank and kernel over `Fraction`, verifies (3), reconstructs three diagonal
lifts whenever the rank is three, and compares the full-support kernel with
(6).  It also verifies the factorization (8) coefficientwise.  The frozen
ledger is deterministic and standard-library only.
