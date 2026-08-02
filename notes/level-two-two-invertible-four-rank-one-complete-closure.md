# The full (2I+4R) generic-kernel stratum has rank at most (53)

Research evidence only. Krenn's conjecture remains open,
**SP-CLEAN-BRIDGE** is untouched, and no certified dependency changes.

## Outcome and scope

Let a binary six-site packet satisfy the generic-kernel equations

\[
                 X_uJX_v^{\mathsf T}=(\nu_u+\nu_v)M_{uv}.        \tag{1}
\]

Suppose (X_0,X_1) are invertible and (X_2,X_3,X_4,X_5) are nonzero
of rank one. Then

> **Complete (2I+4R) closure.** Every such packet satisfies
> \[
>                         \operatorname{rank}d\Psi_M\le53.       \tag{2}
> \]

Consequently the entire (2I+4R) generic-kernel stratum misses
differential rank (55). This conclusion uses only (1): it does not need
L0, L1, R2, or a physical target equation.

The bound combines four existing no-isolated support theorems with one
uniform isolated-vertex reduction. The latter is the new step here.

## The zero-sum graph has only five branches

On the four rank-one sites (R=\{2,3,4,5\}), put

\[
 E=\{tu\in\tbinom R2:\nu_t+\nu_u=0\}.                           \tag{3}
\]

This graph has a rigid scalar structure. All vertices with potential zero
form one clique. For every nonzero value (\lambda), the value classes
(C_\lambda) and (C_{-\lambda}) form a complete bipartite component;
an unpaired value class contributes isolated vertices. Distinct zero or
signed-value components have no edges between them.

If (E) has no isolated vertex, four vertices leave exactly four options:

\[
                  2K_2,\qquad K_{1,3},\qquad K_{2,2},\qquad K_4. \tag{4}
\]

Indeed, the zero clique is either absent, a two-vertex component, or all
four vertices. With no zero vertices, every component is a nontrivial
complete bipartite graph, so the only size partitions are (2+2) and
(4), with bipartitions (1+1), (1+3), or (2+2).

There is one easily missed realization of (2K_2): besides two distinct
nonzero opposite pairs, it can be

\[
                         (0,0,\lambda,-\lambda),\qquad\lambda\ne0. \tag{5}
\]

The disjoint-pair rank proof applies to (5) without change. Its covariant
reduction uses only that the two graph edges leave arbitrary (2\times2)
blocks while every nonedge among rank-one sites is a scalar multiple of
(a_ta_u^{\mathsf T}). The formal matching factorization and its four
effective kernel directions are statements on that graph-defined support
class; they do not use nonzero values for the two exceptional pairs.

If (E) is not one of (4), it has an isolated vertex. These cases are
handled uniformly below.

## An isolated vertex produces a three-site coordinate shore

Write

\[
                         X_t=a_tb_t^{\mathsf T}\qquad(t\in R).   \tag{6}
\]

Choose an isolated vertex (r\in R), and use the other three rank-one
sites (T=R\setminus\{r\}) as a shore. For an invertible site
(i\in\{0,1\}) and (t\in T),

\[
 X_iJX_t^{\mathsf T}=(X_iJb_t)a_t^{\mathsf T}\ne0.              \tag{7}
\]

Thus (\nu_i+\nu_t\ne0), and the determined block (M_{it}) has fixed
right factor (a_t^{\mathsf T}). Isolation gives
(\nu_r+\nu_t\ne0), while

\[
 X_rJX_t^{\mathsf T}
   =(b_r^{\mathsf T}Jb_t)a_ra_t^{\mathsf T}.                    \tag{8}
\]

Hence (M_{rt}), including the possibility that it vanishes, has the same
fixed shore factor. On an internal shore nonedge, (1) gives a scalar
multiple of (a_ta_u^{\mathsf T}); an edge of (E[T]) leaves its entire
(2\times2) block free.

Independent local output bases at the three shore sites send every
(a_t) to (e_0). These bases preserve differential rank. The packet is
therefore in the coordinate-shore support class with inner sites
(\{0,1,r\}). The coordinate-shore matching proof is a block-support
argument and does not require those three inner endpoint matrices to be
invertible; the rank-one inner site is a specialization of the same support
class.

On three shore vertices, (E[T]) is determined by its edge count:

\[
\begin{array}{c|cccc}
E[T]&\varnothing&\text{one edge}&\text{two-edge path}&\text{triangle}\\ \hline
\operatorname{rank}d\Psi_M&\le35&\le42&\le49&\le51.
\end{array}                                                       \tag{9}
\]

The first three entries are the empty-, one-edge-, and path-shore support
bounds. It remains only to justify the constant-cross hypothesis behind
the triangle entry.

## The triangle shore has constant cross spokes

If (E[T]) is a triangle, the three equations
(\nu_t+\nu_u=0) have full rank in characteristic zero. Therefore

\[
                              \nu_t=0\qquad(t\in T).              \tag{10}
\]

Equation (1) also gives

\[
                              b_t^{\mathsf T}Jb_u=0
                              \qquad(t\ne u\text{ in }T).        \tag{11}
\]

For (J=\left(\begin{smallmatrix}0&1\\1&0\end{smallmatrix}\right)),
three nonzero pairwise (J)-orthogonal vectors share one isotropic line.
Concretely, if (b_0=(x,y)), its orthogonal line is spanned by
((x,-y)). The other two factors lie on that line, and their mutual
pairing is a nonzero scalar multiple of (-2xy). It follows that (xy=0),
so the orthogonal line is the line of (b_0). Absorb the three nonzero
scales into the (a_t)'s and write (b_t=b) on all of (T).

After (a_t=e_0), the two invertible inner sites have

\[
 M_{it}=\nu_i^{-1}(X_iJb)e_0^{\mathsf T}
                         \qquad(i=0,1,\ t\in T),                \tag{12}
\]

because (7) also forces (\nu_i\ne0). Since (r) is isolated from the
zero-potential triangle, (\nu_r\ne0), and

\[
 M_{rt}=\nu_r^{-1}(b_r^{\mathsf T}Jb)a_re_0^{\mathsf T}
                         \qquad(t\in T).                         \tag{13}
\]

Thus each inner site's three spokes are genuinely constant, including
when the vector in (13) is zero. The constant-cross factorization gives
the last bound (51) in (9). Every isolated-vertex graph is therefore
bounded by (51).

## Combining all graph types

The existing graph-defined support bounds and the isolated result are

\[
\begin{array}{c|ccccc}
\text{graph branch}&2K_2&K_{1,3}&K_{2,2}&K_4&\text{has an isolate}\\ \hline
\operatorname{rank}d\Psi_M&\le48&\le47&\le53&\le52&\le51.
\end{array}                                                       \tag{14}
\]

The four no-isolated entries are respectively the
[disjoint-pair](level-two-two-invertible-four-rank-one-disjoint-pair-closure.md),
[star](level-two-two-invertible-four-rank-one-k13-closure.md),
[balanced-bipartite](level-two-two-invertible-four-rank-one-balanced-k22-closure.md),
and [all-zero](level-two-two-invertible-four-rank-one-all-zero-closure.md)
theorems. The maximum in (14) is (53), proving (2).

No new exact packet is introduced here. Earlier physical-coordinate
calibrations and their literal R2 audits remain evidence only inside their
stated graph branches; no local rank-normalizing basis is used to infer a
new physical target statement.

## Exact audit

The standard-library checker
[verify_level_two_two_invertible_four_rank_one_complete_closure.py](../computations/verify_level_two_two_invertible_four_rank_one_complete_closure.py)

- exhausts all (9^4) signed-value assignments needed to model every
  abstract four-vertex zero/opposition pattern;
- verifies that the no-isolated signatures are exactly (4), including both
  realizations of (2K_2);
- imports the exact (35/42/49/51) coordinate-shore identities and audits
  the isolated triangle's common source line and constant spokes; and
- reruns the formal factorization and kernel-dimension audits giving the
  four no-isolated bounds in (14).

It passes normal, optimized, and isolated Python.
