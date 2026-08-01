# A zero four-site cofactor forces differential rank at most \(51\)

Research evidence only. Krenn's conjecture remains open,
**SP-CLEAN-BRIDGE** is untouched, and no certified dependency changes.

## 1. Outcome

Let \(M\) be a binary packet on six vertices \(R\), and let
\(C_{uv}\) be the four-site matching tensor on \(R\setminus\{u,v\}\).

> **Cofactor-zero rank-drop theorem.** Suppose
> \[
>                         C_{uv}\equiv0,              \tag{1}
> \]
> and the live block graph of \(M\) on \(R\setminus\{u\}\) is connected
> and nonbipartite. Then
> \[
>                         \operatorname{rank}d\Psi_M\le51.           \tag{2}
> \]

The bound is sharp over \(\mathbb Q\). An integral packet in the checker has
exactly one zero four-site cofactor tensor, a \(K_5\) endpoint deletion, and
differential rank exactly \(51\).

This quantifies the cofactor boundary isolated by the zero-star theorem. In
particular, if \(\operatorname{rank}d\Psi_M\ge52\) and \(C_{uv}=0\), neither
endpoint deletion \(R\setminus\{u\}\) nor \(R\setminus\{v\}\) can remain
connected and nonbipartite.

## 2. Four literal edge-block kernels

The differential column belonging to the cell \(M_{uv}[a,b]\) is supported
on words with \(w_u=a,w_v=b\), and on such a word it is exactly the
complementary cofactor:

\[
 \frac{\partial\Psi(M)(w)}{\partial M_{uv}[a,b]}
   =
 \begin{cases}
 C_{uv}(w|_{R\setminus\{u,v\}}),&(w_u,w_v)=(a,b),\\
 0,&\text{otherwise}.
 \end{cases}                                         \tag{3}
\]

Under (1), all four columns belonging to the \(2\times2\) block \(M_{uv}\)
are zero. Hence the four-dimensional coordinate space

\[
 E_{uv}=\{K:K_{xy}=0\text{ for }xy\ne uv\}            \tag{4}
\]

lies in \(\ker d\Psi_M\).

## 3. Transversality to the five gauges

There are also the universal trace-zero vertex gauges

\[
 G=\left\{
 K^\mu_{xy}=(\mu_x+\mu_y)M_{xy}:
 \sum_{x\in R}\mu_x=0
 \right\}.                                           \tag{5}
\]

They have dimension five under the deletion hypothesis. Indeed, if
\(K^\mu=0\), then \(\mu_x+\mu_y=0\) on every live edge of the connected
nonbipartite graph \(R\setminus\{u\}\). An odd cycle and connectivity force
\(\mu_x=0\) for every \(x\ne u\), and the trace condition gives
\(\mu_u=0\).

The same argument proves

\[
                              E_{uv}\cap G=0.          \tag{6}
\]

If a gauge is supported only on \(uv\), it vanishes on every deletion edge,
so the preceding propagation again gives \(\mu=0\). Therefore

\[
                  \dim\ker d\Psi_M\ge4+5=9,
\]

and the \(64\times60\) differential has rank at most \(51\), proving (2).

## 4. Sharp integral witness

Take \(uv=01\). On the complementary vertices \(2,3,4,5\), choose vertex
vectors

\[
 x_2=(1,2),\quad x_3=(2,3),\quad
 x_4=(3,5),\quad x_5=(5,7),
\]

and rank-one blocks

\[
                         M_{ij}=t_{ij}x_ix_j^{\mathsf T},
\]

with

\[
 t_{23}=t_{45}=t_{24}=t_{35}=t_{25}=1,\qquad
 t_{34}=-2.                                          \tag{7}
\]

For every binary word on these four vertices, the matching tensor factors as

\[
 \left(t_{23}t_{45}+t_{24}t_{35}+t_{25}t_{34}\right)
 \prod_{i=2}^5x_i(w_i)
 =(1+1-2)\prod_{i=2}^5x_i(w_i)=0.                    \tag{8}
\]

Thus \(C_{01}\equiv0\), although all six complementary edges are live and
their graph is \(K_4\). The remaining nine blocks, including \(M_{01}\), are
the small integral matrices recorded in the checker. They make the full live
graph \(K_6\).

Exact row reduction gives

\[
                         \operatorname{rank}d\Psi_M=51
\]

modulo both \(101\) and \(1{,}000{,}003\). All other fourteen four-site
cofactor tensors are nonzero. The nine displayed kernel directions are
independent modulo both primes, so the upper and lower bounds match over
\(\mathbb Q\).

## 5. Audit

[verify_level_two_cofactor_zero_rank_drop.py](../computations/verify_level_two_cofactor_zero_rank_drop.py)
checks the literal cofactor columns, all five gauge kernels, independence of
the combined nine directions, the exact zero-cofactor set, the \(K_5\)
deletion graph, and the sharp rank \(51\) at two primes. It is
standard-library only and passes normal, optimized, and isolated Python.

## 6. Revised frontier

The cofactor-vanishing and graph-degenerate alternatives are not independent
soft exceptions. At ranks \(52\) through \(55\), every zero cofactor edge
forces graph degeneration at both endpoint deletions. Consequently the
remaining rank-\(55\) boundary consists of:

1. nonzero four-site cofactors together with the forced singular internal
   blocks from R2; or
2. a coupled graph-degenerate packet in which every zero cofactor has two
   bad endpoint deletions.

This removes the cofactor-zero/connected-deletion branch completely and
leaves the at-most-three-invertible R2 incidence patterns as the generic
two-sided target.
