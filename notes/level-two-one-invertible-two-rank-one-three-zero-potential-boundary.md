# The \(1I+2R+3Z\) potential boundary closes before R2

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
                    \operatorname{rank}X_5)=(2,1,1,0,0,0).    \tag{2}
\]

An exhaustive signed-potential census closes this entire stratum:

> **\(1I+2R+3Z\) potential theorem.** There are \(376\) labelled
> potential-support envelopes satisfying (1), or \(73\) modulo the
> natural \(S_2\times S_3\) action on the rank-one and zero sites.
> Seventy-one quotient envelopes satisfy
> \[
>                         \operatorname{rank}d\Psi_M\le52.     \tag{3}
> \]
> The other two quotient envelopes each have one inactive tangent edge.
> Its four scalar tangent cells, together with the five universal vertex
> gauges, give
> \[
>                         \operatorname{rank}d\Psi_M\le51.     \tag{4}
> \]
> Consequently no rank-\(55\) packet has endpoint ranks (2).

All \(376\) labelled envelopes close before L0, L1, or literal residual
R2. In particular there is no rank-\(55\) selected/R2 residue to
calibrate on this endpoint-rank stratum. The argument is a differential
support-and-gauge theorem; it does not assert that the displayed bounds
are sharp.

## 1. Potential support

Write

\[
                         X_i=h_ib_i^{\mathsf T}
                         \qquad(i=1,2).                        \tag{5}
\]

Invertibility of \(X_0\) and nonvanishing of \(X_1,X_2\) imply

\[
                         \nu_0+\nu_1\ne0,
                 \qquad  \nu_0+\nu_2\ne0.                    \tag{6}
\]

Broaden the core \(Q=\{0,1,2\}\) to a complete graph. This forgets the
rank-one factors of its fixed blocks and can only increase differential
support. Every block incident with a zero endpoint \(z\in\{3,4,5\}\)
has zero numerator in (1), so it can be nonzero only when its endpoint
potentials sum to zero. The broadened support graph is therefore

\[
 H=K_Q\ \cup\
   \{uz:z\in\{3,4,5\},\ \nu_u+\nu_z=0\}.                    \tag{7}
\]

A tangent block \(\dot M_{uv}\) is active only if the four-site
complement of \(\{u,v\}\) has a perfect matching in \(H\). If \(a(H)\)
is the number of active tangent edges, its four binary cells give

\[
                         \operatorname{rank}d\Psi_M
                              \le4a(H).                         \tag{8}
\]

Thus \(a(H)\le13\) proves (3).

## 2. Exact signed-partition census

Canonical signed partitions enumerate zero and every nonzero negation
orbit \(\{\alpha,-\alpha\}\), so they enumerate all possible zero-sum
relations over arbitrary complex potentials. Of \(4088\) signed
partitions on six labelled sites, \(2908\) satisfy (6). They induce
\(376\) distinct graphs (7).

The active-edge histograms are

\[
\begin{array}{c|rrrrrrrrrrrrrrr}
a(H)&0&1&2&3&4&5&6&7&8&9&10&11&12&13&14\\ \hline
\text{labelled}&1&21&9&33&60&48&21&69&27&52&6&12&10&3&4\\
S_2\times S_3\text{ quotient}&1&5&2&7&7&10&6&11&4&9&1&3&3&2&2.
\end{array}                                                     \tag{9}
\]

Hence \(372\) labelled envelopes, or \(71\) quotient envelopes, have
\(a(H)\le13\). No envelope has all fifteen tangent edges active.

## 3. The two dense support types

The four labelled envelopes with \(a(H)=14\) form two quotient types:

\[
\begin{array}{c|c|c|c|c}
\text{type}&(\nu_0,\ldots,\nu_5)&H\setminus K_Q&
\text{inactive edge}&\text{labelled count}\\ \hline
\text{five-site zero clique}&
(\lambda,0,0,0,0,0)&
K_{\{1,2,3,4,5\}}\setminus\{12\}&12&1\\
\text{split }K_{4,2}\text{ zero boundary}&
(\lambda,\lambda,\lambda,\lambda,-\lambda,-\lambda)&
K_{\{0,1,2,3\},\{4,5\}}&45&3.
\end{array}                                                     \tag{10}
\]

Here \(\lambda\ne0\). In the second row, one of the three zero endpoints
has potential \(\lambda\), while the other two have potential
\(-\lambda\); the three labelled envelopes record that choice. Core edge
\(12\) is already included in \(K_Q\), which explains its removal from
the optional graph in the first row.

For the zero clique, the complement of tangent edge \(12\) is
\(\{0,3,4,5\}\). Root \(0\) has no supported edge to the three zero
sites, so that complement has no perfect matching. For the split type,
the complement of edge \(45\) is \(\{0,1,2,3\}\), and site \(3\) has no
base edge to the core. These are the unique inactive tangent edges.

## 4. Four zero columns plus five gauges

For any inactive edge \(e\), all four coordinate tangents supported on
the cells of \(e\) lie in \(\ker d\Psi_M\). Let their span be \(U_e\), so

\[
                              \dim U_e=4.                       \tag{11}
\]

Independently, for

\[
 W=\{\mu\in\mathbb C^6:\sum_u\mu_u=0\},
\]

the universal vertex-gauge tangent

\[
             K^\mu_{uv}=(\mu_u+\mu_v)M_{uv}                  \tag{12}
\]

lies in \(\ker d\Psi_M\). The space \(W\) has dimension five.

On the dense locus where every allowed block of \(H\) is nonzero, both
gauge maps are injective and disjoint from \(U_e\). The graph reason is
elementary. If \(K^\mu\) vanishes on a nonzero block \(uv\), then

\[
                              \mu_u+\mu_v=0.                   \tag{13}
\]

Along a connected graph these equations alternate signs; an odd cycle
forces every \(\mu_u\) to vanish. Moreover, if a gauge lies in \(U_e\),
then (13) holds on every edge outside \(e\). Thus it is enough that
\(H\setminus\{e\}\) be connected and nonbipartite.

Both dense graphs have this property:

- for the zero clique, delete \(12\) from the \(K_5\) shore; the shore
  remains connected with triangles, and root \(0\) is attached through
  \(01,02\);
- for the split type, edge \(45\) is absent already, while the core
  triangle \(012\) is connected to every remaining site.

Consequently

\[
 \dim\ker d\Psi_M\ge\dim U_e+dim W=4+5=9,
 \qquad \operatorname{rank}d\Psi_M\le60-9=51               \tag{14}
\]

on the dense nonzero-block locus of either type. Every \(52\)-minor is a
polynomial in the packet entries. Since those minors vanish on the dense
open locus, they vanish identically and (14) extends to every
specialization, including packets with further zero or singular blocks.
This proves (4).

## 5. Isotropic refinement of the zero clique

For the first row of (10), the rank-one pair equation gives

\[
 X_1JX_2^{\mathsf T}
  =(b_1^{\mathsf T}Jb_2)h_1h_2^{\mathsf T}=0,
 \qquad b_1^{\mathsf T}Jb_2=0.                               \tag{15}
\]

If \(b_1,b_2\) are proportional, their common line is isotropic. The two
nonzero root spokes then share the left factor \(X_0Jb_1\), while
\(M_{03}=M_{04}=M_{05}=0\). Root \(0\) is fixed, and the existing
fixed-root theorem sharpens (14) to

\[
                         \operatorname{rank}d\Psi_M\le42.      \tag{16}
\]

If the two lines are distinct, both are nonisotropic and orthogonal. The
gauge proof above still gives the uniform rank-51 closure, so no residual
pair-pencil branch remains.

## 6. Exact calibrations

The checker includes deterministic rational packets on both dense types.
For the zero clique, take

\[
\begin{aligned}
X_0&=\begin{pmatrix}2&3\\5&7\end{pmatrix},&
X_1&=\binom23(1\ \ 1),&
X_2&=\binom57(1\ \ {-1}),&
X_3&=X_4=X_5=0,
\end{aligned}                                                  \tag{17}
\]

with potentials \((1,0,0,0,0,0)\). Every block inside
\(\{1,2,3,4,5\}\) is free. For the split type, use the same \(X_0\),

\[
 X_1=\binom23(1\ \ 2),\qquad
 X_2=\binom57(2\ \ 3),\qquad X_3=X_4=X_5=0,                 \tag{18}
\]

and potentials \((1,1,1,1,-1,-1)\). Its eight
\(K_{\{0,1,2,3\},\{4,5\}}\) blocks are free. On every free edge put

\[
 M_{uv}=\begin{pmatrix}k&k+1\\k+2&k+4\end{pmatrix},
 \qquad k=11+7u+13v,                                         \tag{19}
\]

and determine every nonzero-multiplier block from (1).

Both packets satisfy all \(60\) scalar generic-kernel equations and all
\(64\) selected level-two rows with \(z=-\sum_u\nu_u\). Their exact
differential ranks are

\[
\begin{array}{c|ccc}
&\mathbb Q&\mathbb F_{101}&\mathbb F_{1000003}\\ \hline
\text{five-site zero clique}&48&48&48\\
\text{split }K_{4,2}\text{ boundary}&43&43&43.
\end{array}                                                     \tag{20}
\]

For each calibration, the checker constructs the four inactive coordinate
tangents and five trace-zero gauges, verifies all nine are kernel vectors,
and proves their combined rank is nine. The ranks in (20) are calibrations,
not claimed sharp uniform bounds.

## Consequence

The adjacent \(1I+3R+2Z\) stratum had one sharp rank-55 all-spokes
residue. Setting a third rank-one endpoint to zero removes one core bridge:
the resulting split \(K_{4,2}\) packet loses the entire \(45\) tangent
block. On the other dense potential type, the five-site zero clique loses
the \(12\) tangent block instead. In both cases the four new zero columns
are independent of the universal gauges, so rank \(55\) is impossible.

Therefore the descending endpoint-rank map has no \(1I+2R+3Z\)
generic-kernel/R2 frontier. Any rank-55 packet with one invertible selected
matrix must lie in a different endpoint-rank stratum.

## Exact audit

The standard-library checker
[verify_level_two_one_invertible_two_rank_one_three_zero_potential_boundary.py](../computations/verify_level_two_one_invertible_two_rank_one_three_zero_potential_boundary.py)

- enumerates all signed partitions, enforces (6), and reconstructs the
  \(376\) labelled and \(73\) quotient support envelopes;
- audits every complement perfect matching and both histograms in (9);
- identifies the two dense quotient types and their four labelled forms;
- verifies the connected nonbipartite deletion criterion behind (14);
- constructs the exact dense calibrations, all generic-kernel and selected
  level-two rows, the nine independent kernel directions, and the ranks in
  (20); and
- imports and pins the fixed-root bound used in (16).

It passes normal, optimized, and isolated Python.
