# Four-port balance eliminates the residual defect-one chart

## 1. Outcome

Let an exact ternary aggregate source on an even set \(B\) satisfy

\[
                         H_B(A)=\Delta_{B,3}.
\]

Fix a good deleted pair. Use the notation of
[the escape-chart descent theorem](good-pair-fan-escape-chart-descent-theorem.md):
\(W\) is the even internal set, \(q\) is its quadratic, the chart is
gauge-rigid, and

\[
 \nu=\#\{\text{nontrivial bipartite components of }G_3(q)\}
       +\#\{\text{isolated vertices of }G_3(q)\}.
\]

The only residual defect-one chart in that theorem was **(E3)**:
\(\nu=1\), with a proper bipartite component \(K_0\), a nonempty
nonbipartite remainder, and two-site-supported deleted-star rows.

**Theorem 1.1 (four-port defect-one elimination).** Chart (E3) is
empty, for every even order and every shore size. Consequently every
good pair of a hypothetical exact source lies in exactly one of

* **(E1)** the internal Hessian has a non-gauge kernel direction; or
* **(E2)** the rank-three graph has defect at least two.

In particular all at least \(N(N-7)/2\) good pairs, and every pair in a
good fan of size at least \(N-7\), lie in (E1) or (E2), for every even
\(N\ge8\).

The proof is support-theoretic only after the exact mixed pair equations
have produced one physical four-port window. It does not select a term
from a cancelling coefficient, cap the common power, assume endpoint
symmetry, or restrict invisible blocks.

## 2. Imported defect-one structure

Write the proper bipartite component as

\[
                         K_0=A\mathbin{\dot\cup}B_0,
 \qquad O=W\setminus K_0\ne\varnothing,
\]

and let \(\zeta\) be \(+1\) on \(A\), \(-1\) on \(B_0\), and zero on
\(O\). The defect-one theorem supplies, for every off-diagonal colour
pair \(c\ne d\),

\[
 p_cs_d=\beta_{cd}Z^\zeta,
 \qquad a_{cd}=-\beta_{cd}\Delta,
 \qquad
 (Z^\zeta)_{ij}=(\zeta_i+\zeta_j)q_{ij}.               \tag{1}
\]

At least one \(\beta_{cd}\) is nonzero. Fix one and put

\[
 P=\operatorname{supp}(p_c),\qquad
 S=\operatorname{supp}(s_d),\qquad U=P\cup S.          \tag{2}
\]

Every row is nonzero and supported on at most two physical sites, so

\[
                         |U|\le4.                       \tag{3}
\]

Every nonzero \(\zeta\)-visible block of \(q\) is a block of the product
in (1). Hence both of its endpoints belong to \(U\). The live-interface
lemma from the escape theorem says that some such block joins \(K_0\) to
\(O\); therefore

\[
                         U\cap O\ne\varnothing.          \tag{4}
\]

The invisible blocks are exactly the \(A\)-to-\(B_0\) blocks and the
\(O\)-internal blocks. They remain completely arbitrary below.

## 3. Every two-site complement has a supported matching

Put \(|W|=2t\). For a physical pair \(D=\{x,y\}\subset W\), write
\(q_{W\setminus D}\) for the restriction of \(q\) to its complement.

**Lemma 3.1 (pair-complement activity).** On a gauge-rigid chart,

\[
             q_{W\setminus D}^{[t-1]}\ne0
             \qquad\text{for every }D\in\binom W2.      \tag{5}
\]

**Proof.** If the divided power in (5) vanished, every one of the nine
matrix-unit variations supported on the block \(D\) would be killed by
\(Z\mapsto Zq^{[t-1]}\). Thus a nine-dimensional block space would lie
in the Hessian kernel. A vertex-gauge quadratic supported in that block
has its \(D\)-block in the line

\[
                         \mathbb Cq_D,
\]

because every gauge block is \((\alpha_x+\alpha_y)q_D\). The gauge
intersection therefore has dimension at most one, including when
\(q_D=0\). The other at least eight block directions are non-gauge,
contrary to rigidity. \(\square\)

Nonvanishing in (5) implies the existence of at least one supported
perfect matching of \(W\setminus D\). This implication is safe under
complex cancellation: a nonzero tensor coefficient must have at least
one nonzero matching monomial, but no particular monomial is selected in
the argument.

## 4. The two-shore balance contradiction

Let

\[
 a=|A|,\qquad b=|B_0|,
 \qquad u_A=|U\cap A|,\quad u_B=|U\cap B_0|,
 \quad u_O=|U\cap O|.
\]

For a supported perfect matching \(M\) of \(W\setminus D\), let \(F_A\)
be the number of \(A\setminus D\) vertices which \(M\) matches either
inside \(A\) or to \(O\). Define \(F_B\) symmetrically. Every remaining
vertex of \(A\) or \(B_0\) is matched across the two shores, so

\[
 |A\setminus D|-|B_0\setminus D|=F_A-F_B.              \tag{6}
\]

Every edge counted by \(F_A\) or \(F_B\) is \(\zeta\)-visible. Its
endpoints lie in \(U\), and consequently

\[
                         F_A\le u_A,\qquad F_B\le u_B.  \tag{7}
\]

Assume first that \(a,b\ge2\), and interchange the shores so that
\(a\ge b\). Put \(\delta=a-b\ge0\). Delete two \(B_0\)-vertices and
use Lemma 3.1. Equations (6)--(7) give

\[
                         u_A\ge\delta+2.                 \tag{8}
\]

If \(\delta\ge2\), (4) and (8) already give
\(|U|\ge u_A+u_O\ge5\), contradicting (3). If \(\delta=1\), deleting
two \(A\)-vertices gives \(u_B\ge1\); then
\(u_A+u_B+u_O\ge3+1+1=5\). If \(\delta=0\), the same deletion gives
\(u_B\ge2\), and again \(u_A+u_B+u_O\ge2+2+1=5\).

Thus no residual chart has two shores of size at least two.

## 5. Singleton shores

It remains to take \(A=\{x\}\) and \(B_0=\{b_1,\ldots,b_r\}\), after
possibly swapping shores. Suppose first that \(r\ge2\). For every
\(b_j\), delete \(\{x,b_j\}\). In a supported matching of the
complement, every remaining \(B_0\)-vertex must use a same-shore or an
interface edge. Those edges are visible, so

\[
                         B_0\setminus\{b_j\}\subset U.
\]

Varying \(j\) gives \(B_0\subset U\). Together with (4), this first
forces \(r\le3\).

The component \(K_0\) is connected, so every \(xb_j\) is a rank-three
edge. It is invisible in (1), hence

\[
 p_{c,x}\otimes s_{d,b_j}+s_{d,x}\otimes p_{c,b_j}=0. \tag{9}
\]

If \(x\in U\), then for each \(b_j\in U\) equation (9) cannot contain
exactly one nonzero simple tensor. If it contains both, cancellation of
two nonzero simple tensors forces both sites into both supports. If it
contains neither, the membership of \(b_j\) forces \(x\) and \(b_j\)
into the same one of \(P,S\). Applying this to at least two distinct
\(b_j\)'s puts at least three sites in one of the two supports, contrary
to their size bound. Therefore

\[
                         x\notin U.                     \tag{10}
\]

If \(r=2\), (10) leaves \(x\) with only its two \(B_0\)-partners: every
\(x\)-to-\(O\) block is visible and hence zero outside \(U\). This
contradicts the minimum block-degree-three Lemma R.

If \(r=3\), equations (3)--(4) and \(B_0\subset U\) force

\[
                         U=B_0\mathbin{\dot\cup}\{o\}
\]

for one \(o\in O\). The two supports are disjoint two-sets partitioning
\(U\); otherwise their union could not have four elements. A live
interface edge splits \(o\) from one \(B_0\)-site. By the pigeonhole
principle two of the three \(B_0\)-sites lie in the same support, so their
visible block is zero. Delete \(x\) and the third \(B_0\)-site. The two
retained sites cannot meet each other and can use no interface site except
the single \(o\); they cannot both be matched. This contradicts Lemma
3.1.

Finally, \(r=1\) is the \(K_2\) component already excluded, uniformly in
the remainder, by Theorem E of the escape-chart theorem: its two opposite
interface signs give an explicit non-gauge collision kernel.

This exhausts all shore sizes and proves Theorem 1.1. \(\square\)

## 6. Consequences and scope

The former escape taxonomy is now the two-way alternative (E1)/(E2).
The conclusion is stronger than merely eliminating the zero-block part of
(E3). In particular, Corollary G's induced-zero-shore alternative cannot
occur, because its shore-forming fan pairs were zero-block defect-one
pairs. The literal \(k=1\) bound would already give at least \(N-13\)
(E1)/(E2) pairs in one fan for even \(N\ge14\); Theorem 1.1 instead puts
all at least \(N-7\) good fan pairs there, for every even \(N\ge8\).

The proof retains:

* arbitrary endpoint-ordered \(3\times3\) aggregate blocks;
* parallel decorated sources after exact aggregation;
* zero blocks and arbitrary rank-zero, rank-one, and rank-two invisible
  blocks;
* arbitrary complex cancellation inside every matching coefficient; and
* the literal common internal quadratic and all nine pair equations.

The lightweight exact audit is
[verify_good_pair_defect_one_four_port_elimination.py](../computations/verify_good_pair_defect_one_four_port_elimination.py).
An independent reconstruction is recorded in
[good-pair-defect-one-four-port-elimination-independent-audit.md](good-pair-defect-one-four-port-elimination-independent-audit.md).
