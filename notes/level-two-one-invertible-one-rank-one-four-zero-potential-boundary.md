# The \(1I+1R+4Z\) potential boundary has rank at most \(44\)

Research evidence only. Krenn's conjecture remains open,
**SP-CLEAN-BRIDGE** is untouched, and no certified dependency changes.

## Outcome

Let a binary six-site packet satisfy

\[
 X_uJX_v^{\mathsf T}=(\nu_u+\nu_v)M_{uv},\qquad
 J=\begin{pmatrix}0&1\\1&0\end{pmatrix},                     \tag{1}
\]

with endpoint ranks

\[
                   (\operatorname{rank}X_0,\ldots,
                    \operatorname{rank}X_5)=(2,1,0,0,0,0).    \tag{2}
\]

The full potential/support stratum closes with a large margin:

> **\(1I+1R+4Z\) potential theorem.** Every packet satisfying (1)--(2)
> obeys
> \[
>                         \operatorname{rank}d\Psi_M\le44.     \tag{3}
> \]

An exhaustive signed-partition census gives \(675\) labelled support
envelopes, or \(85\) modulo the natural \(S_4\) action on the zero sites.
Eighty-four quotient envelopes have at most eleven active tangent edges,
which proves (3) directly. The sole twelve-edge quotient envelope has an
inactive three-edge shore. Its twelve scalar coordinate tangents and five
universal vertex gauges span sixteen kernel directions because their
intersection is one-dimensional, again proving (3).

Thus no rank-\(55\) selected/R2 residue exists in this endpoint-rank
stratum. L0, L1, and literal residual R2 are not needed.

## 1. Support reduction

Write the sole rank-one endpoint matrix as

\[
                              X_1=h_1b_1^{\mathsf T}.          \tag{4}
\]

Since \(X_0\) is invertible and \(X_1\ne0\), equation (1) forces

\[
                              \nu_0+\nu_1\ne0.                 \tag{5}
\]

Broaden the two-site core \(Q=\{0,1\}\) to its single complete-graph
edge. Every other edge has at least one zero endpoint matrix, so its
numerator in (1) vanishes. It can be nonzero only when the two endpoint
potentials sum to zero. The broadened support graph is

\[
 H=\{01\}\ \cup\
   \{uv:uv\ne01,\ \nu_u+\nu_v=0\}.                            \tag{6}
\]

A tangent block \(\dot M_{uv}\) contributes only if the four-site
complement of \(\{u,v\}\) has a perfect matching in \(H\). If \(a(H)\)
is the number of active tangent edges, then

\[
                         \operatorname{rank}d\Psi_M
                              \le4a(H).                         \tag{7}
\]

## 2. Exact potential census

Canonical signed partitions enumerate zero and every nonzero negation
orbit \(\{\alpha,-\alpha\}\), hence every possible zero-sum graph over
the complex potentials. Of \(4088\) signed partitions on six labelled
sites, \(3440\) satisfy (5). They induce \(675\) distinct graphs (6).

The active-edge histograms are

\[
\begin{array}{c|rrrrrrrrrrrrr}
a(H)&0&1&2&3&4&5&6&7&8&9&10&11&12\\ \hline
\text{labelled}&35&72&96&131&98&87&59&49&24&4&14&2&4\\
S_4\text{ quotient}&10&8&8&16&10&9&8&7&2&1&3&2&1.
\end{array}                                                     \tag{8}
\]

Thus \(671\) labelled envelopes, or \(84\) quotient envelopes, have
\(a(H)\le11\) and satisfy (3) directly. No support envelope has thirteen,
fourteen, or fifteen active tangent edges.

## 3. The unique maximal support orbit

The four labelled envelopes with \(a(H)=12\) form one quotient orbit. Up
to relabelling the zero sites, its potentials are

\[
           (\nu_0,\ldots,\nu_5)
             =(\lambda,\lambda,\lambda,-\lambda,-\lambda,-\lambda),
             \qquad\lambda\ne0.                               \tag{9}
\]

The zero site \(2\) shares the core potential, while sites \(3,4,5\)
have the opposite potential. The base-support graph is

\[
 H=\{01\}\ \cup\ K_{\{0,1,2\},\{3,4,5\}}.                  \tag{10}
\]

The three tangent edges

\[
                              D=\{01,02,12\}                  \tag{11}
\]

are inactive. For edge \(01\), its complement contains site \(2\) and
the three opposite-shore sites, so no perfect matching exists. The same
argument applies to \(02\) and \(12\). Every other tangent edge is active.

Let \(U_D\) be the coordinate tangent space on the twelve binary cells of
the three edges in (11). Then

\[
                         U_D\subseteq\ker d\Psi_M,
                 \qquad  \dim U_D=12.                         \tag{12}
\]

## 4. The gauge intersection is one-dimensional

For

\[
 W=\{\mu\in\mathbb C^6:\sum_u\mu_u=0\},
\]

the five-dimensional universal gauge space is

\[
                         K^\mu_{uv}=(\mu_u+\mu_v)M_{uv},
                 \qquad  K^\mu\in\ker d\Psi_M.               \tag{13}
\]

On the dense locus where every block in (10) is nonzero, the gauge map is
injective. Indeed, equations \(\mu_u+\mu_v=0\) on the \(K_{3,3}\) edges
make \(\mu\) constant with value \(t\) on \(\{0,1,2\}\) and with value
\(-t\) on \(\{3,4,5\}\). The additional nonzero edge \(01\) forces
\(2t=0\), hence \(t=0\).

A gauge tangent lies in \(U_D\) precisely when it vanishes on all nine
\(K_{3,3}\) blocks. Those equations leave the single bipartite sign line

\[
 \mu_0=\mu_1=\mu_2=t,
 \qquad \mu_3=\mu_4=\mu_5=-t.                                \tag{14}
\]

Its coordinate sum is automatically zero, and its only nonzero block
component is on \(01\), inside \(U_D\). Therefore

\[
 \dim(U_D\cap K^W)=1,
 \qquad \dim(U_D+K^W)=12+5-1=16.                              \tag{15}
\]

It follows that

\[
                         \operatorname{rank}d\Psi_M
                              \le60-16=44                     \tag{16}
\]

on the dense locus. Every \(45\)-minor is polynomial in the packet
entries, so its vanishing extends to all specializations of (10), including
packets with additional zero or singular blocks. This proves (3) on the
last quotient envelope.

## 5. Exact calibration

For an exact rational packet in the maximal orbit, take

\[
 X_0=\begin{pmatrix}2&3\\5&7\end{pmatrix},\qquad
 X_1=\binom23(1\ \ 2),\qquad X_2=X_3=X_4=X_5=0,              \tag{17}
\]

with potentials (9) at \(\lambda=1\). Put

\[
 M_{uv}=\begin{pmatrix}k&k+1\\k+2&k+4\end{pmatrix},
 \qquad k=11+7u+13v,                                         \tag{18}
\]

on every \(K_{3,3}\) edge in (10), and determine every
nonzero-multiplier block from (1). In particular, \(M_{01}\) is nonzero
rank one, while \(M_{02}=M_{12}=0\).

Since \(\sum_u\nu_u=0\), the selected direct parameter is \(z=0\).
The checker verifies all \(60\) scalar generic-kernel equations and all
\(64\) selected level-two rows. It constructs the twelve inactive
coordinate tangents and five gauges explicitly and finds their combined
rank to be sixteen. The differential ranks are

\[
 \operatorname{rank}_{\mathbb Q}d\Psi_M
 =\operatorname{rank}_{\mathbb F_{101}}d\Psi_M
 =\operatorname{rank}_{\mathbb F_{1000003}}d\Psi_M=43.        \tag{19}
\]

Thus the uniform rank-44 theorem is within one dimension of this exact
dense calibration. Rank 44 is not claimed sharp.

## Consequence

The endpoint-rank descent becomes strictly easier after the
\(1I+3R+2Z\) sharp residue. The full \(1I+2R+3Z\) stratum already has
rank at most \(52\); with only one nonzero rank-one endpoint left, the
support graph loses at least three whole tangent blocks at its densest
point. The gauge intersection calculation lowers the global bound to
\(44\).

Hence generic kernel and differential rank alone exclude every
\(1I+1R+4Z\) packet from the rank-55 frontier. Residual R2 cannot restore
the missing dimensions.

## Exact audit

The standard-library checker
[verify_level_two_one_invertible_one_rank_one_four_zero_potential_boundary.py](../computations/verify_level_two_one_invertible_one_rank_one_four_zero_potential_boundary.py)

- enumerates all signed partitions, enforces (5), and reconstructs the
  \(675\) labelled and \(85\) quotient support envelopes;
- audits every complement perfect matching and both histograms in (8);
- identifies the unique maximal quotient orbit and its four labelled
  potential forms;
- verifies the twelve inactive cell directions, five gauges, and their
  one-dimensional intersection; and
- checks the exact calibration, all generic-kernel and selected level-two
  rows, and the three ranks in (19).

It passes normal, optimized, and isolated Python.
