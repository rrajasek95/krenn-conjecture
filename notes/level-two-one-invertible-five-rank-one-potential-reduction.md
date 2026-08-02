# The \(1I+5R\) potential frontier reduces to \(K_{1,4}\) and \(K_{2,3}\)

Research evidence only. Krenn's conjecture remains open,
**SP-CLEAN-BRIDGE** is untouched, and no certified dependency changes.

## Outcome and scope

Let a binary six-site packet satisfy the generic-kernel equations

\[
                 X_iJX_j^{\mathsf T}=(\nu_i+\nu_j)M_{ij},
 \qquad J=\begin{pmatrix}0&1\\1&0\end{pmatrix}.                 \tag{1}
\]

Assume \(X_0\) is invertible and \(X_1,\ldots,X_5\) are nonzero of rank
one. Impose residual R2 in the original physical coordinates. This note
gives the first potential/support reduction of that endpoint-rank stratum:

> **\(1I+5R\) potential reduction.** If
> \(\operatorname{rank}d\Psi_M=55\), then, after relabelling the five
> rank-one sites, their potentials have one of the two forms
> \[
> \begin{array}{c|cc}
> &A&B\\ \hline
> K_{1,4}&|A|=1,\ \nu_A=\lambda&
>          |B|=4,\ \nu_B=-\lambda\\
> K_{2,3}&|A|=2,\ \nu_A=\lambda&
>          |B|=3,\ \nu_B=-\lambda,
> \end{array}
> \qquad\lambda\ne0.                                           \tag{2}
> \]
> Writing \(X_i=h_ib_i^{\mathsf T}\), the \(b_i\) on each shore share a
> line:
> \[
> b_i\parallel b_A\ (i\in A),\qquad
> b_j\parallel b_B\ (j\in B),\qquad
> b_A^{\mathsf T}Jb_B=0.                                      \tag{3}
> \]
> Both lines are nonisotropic. Every cross-shore block is free; all
> within-shore blocks are fixed nonzero rank-one blocks; and the five
> \(0\)-spokes are constant on each of the two shores after the harmless
> rank-one scales are absorbed. In physical selected coordinates the two
> pencil slopes are antipodal. Moreover, R2 at root \(0\) forces two
> distinct rank-one sites \(i,j\) with \(h_i\parallel e_0\) and
> \(h_j\parallel e_1\).

Every other potential graph has differential rank at most \(51\):

\[
\begin{array}{c|cccc}
\text{potential graph}&\text{has an isolate}&K_5&
K_3\sqcup K_2&K_{1,2}\sqcup K_2\\ \hline
\operatorname{rank}d\Psi_M&\le42&\le42&\le51&\le49.
\end{array}                                                     \tag{4}
\]

The two connected bipartite forms in (2) are exact covariant residual
normal forms, not closures. Since their lines are nonisotropic, every
rank-one endpoint has both selected columns nonzero. Literal R2 therefore
uses its two-internal-witness alternative at every one of the six roots.

This note uses no L0 or L1 equation. The bounds in (4) are support bounds
and do not use R2.

## Pair-pencil form of the generic-kernel equation

Write

\[
                         X_i=h_ib_i^{\mathsf T}
                         \qquad(i=1,\ldots,5).                  \tag{5}
\]

Then

\[
 X_iJX_j^{\mathsf T}
   =(b_i^{\mathsf T}Jb_j)\,h_ih_j^{\mathsf T}.                  \tag{6}
\]

At the invertible root,

\[
 X_0JX_i^{\mathsf T}=(X_0Jb_i)h_i^{\mathsf T}\ne0,             \tag{7}
\]

so

\[
                              \nu_0+\nu_i\ne0                   \tag{8}
\]

for every rank-one site.

On the rank-one sites, define the scalar zero-sum graph

\[
 E=\{ij:\nu_i+\nu_j=0\}.                                      \tag{9}
\]

For \(ij\in E\), equation (1) forces

\[
                         b_i^{\mathsf T}Jb_j=0,                 \tag{10}
\]

and leaves \(M_{ij}\) arbitrary. For \(ij\notin E\), the block is fixed:

\[
 M_{ij}=\frac{b_i^{\mathsf T}Jb_j}{\nu_i+\nu_j}
                         h_ih_j^{\mathsf T},                   \tag{11}
\]

including the possibility that it vanishes. Thus only an edge of \(E\)
can break the fixed factor \(h_i\) at a rank-one root \(i\).

If \(i\) is isolated in \(E\), all five blocks incident with \(i\) have
the fixed \(i\)-factor \(h_i\). After normalizing that factor to \(e_0\),
all nonincident tangent columns lie in the \(32\)-dimensional
\(i=0\) output slice, while the five incident edges contribute at most ten
transverse cells. Hence

\[
                         \operatorname{rank}d\Psi_M
                              \le32+5\cdot2=42.                 \tag{12}
\]

More precisely, rank \(55\) requires every rank-one root to have an
incident edge of \(E\) whose actual free block breaks its \(h_i\)-factor.
In particular \(E\) has no isolated vertex.

## Five scalar graphs have no isolated vertex

The form of (9) is rigid. All zero-potential vertices form one clique.
For each nonzero value \(\mu\), its value classes \(C_\mu,C_{-\mu}\)
form one complete bipartite component; an unpaired class is isolated.
Distinct zero or signed-value components have no edges between them.

On five vertices, no isolated vertex leaves exactly

\[
 K_5,\qquad K_{1,4},\qquad K_{2,3},\qquad
 K_3\sqcup K_2,\qquad K_{1,2}\sqcup K_2.                       \tag{13}
\]

Indeed, a component has at least two vertices. The only size partitions
are \(5\) and \(3+2\). A five-vertex component is the zero clique or a
complete bipartite graph with shores \(1+4\) or \(2+3\). In a \(3+2\)
partition, the three-vertex component is either the zero clique \(K_3\)
or \(K_{1,2}\), while the two-vertex component is \(K_2\).

This classification also covers several distinct scalar realizations of
the same graph. For example, \(K_{1,2}\sqcup K_2\) may use two different
nonzero signed magnitudes, or one nonzero \(K_{1,2}\) component together
with a two-vertex zero clique.

## The complete graph fixes the invertible root

The graph \(K_5\) forces

\[
                              \nu_1=\cdots=\nu_5=0.             \tag{14}
\]

Equations (10) make five nonzero vectors pairwise \(J\)-orthogonal. In
dimension two they share one isotropic line. To see this, start with
\(b=(x,y)\). Its orthogonal line is generated by

\[
                              b^\perp=(x,-y),
\]

and

\[
                         (b^\perp)^{\mathsf T}Jb^\perp=-2xy.   \tag{15}
\]

Two nonzero vectors in that line must also be mutually orthogonal, so
\(xy=0\). The line is then isotropic and equals its own orthogonal line.
Absorb the five nonzero proportionality constants into the \(h_i\), and
write every \(b_i=b\).

By (7), (8), and (14),

\[
                         M_{0i}=\nu_0^{-1}
                                  (X_0Jb)h_i^{\mathsf T}.       \tag{16}
\]

All five blocks incident with site \(0\) have the same nonzero root
\(X_0Jb\). The fixed-root bound (12), now at the invertible site, proves
the \(K_5\) entry of (4). Notice that the relaxed support class with ten
arbitrary rank-one-to-rank-one blocks could have rank \(55\); the
pair-pencil relation (10) is what creates the fixed root at site \(0\).

## The disconnected graphs are coordinate shores

For \(K_{1,2}\sqcup K_2\), take the three-vertex \(K_{1,2}\) component as
a shore. Its two zero-multiplier blocks form an exceptional path. Every
cross block from \(0\) or the other \(K_2\) component has the fixed factor
\(h_t\) at its shore endpoint, while the remaining internal shore block is
a scalar multiple of \(h_th_u^{\mathsf T}\). Independent local shore
bases therefore put the packet in the coordinate-shore path envelope, and

\[
                         \operatorname{rank}d\Psi_M\le49.       \tag{17}
\]

For \(K_3\sqcup K_2\), the \(K_3\) component is the zero-potential clique.
Its three pair-pencil vectors are pairwise orthogonal, so they share one
isotropic line as above. After their scales are absorbed, each of the three
inner sites—site \(0\) and the two vertices of the other component—has
the same spoke to all three \(K_3\) shore sites. The three internal shore
blocks are arbitrary. This is exactly the constant-cross triangle
envelope, giving

\[
                         \operatorname{rank}d\Psi_M\le51.       \tag{18}
\]

Local bases in (17)--(18) are used only for differential rank. No physical
GHZ or R2 axis is inferred from them.

## The two connected residual normal forms

It remains to analyze a connected complete bipartite graph
\(K_{a,b}\) with \((a,b)=(1,4)\) or \((2,3)\). Its potential is (2) with
\(\lambda\ne0\). If one shore contains two vertices, their common
orthogonal neighbor and the two-dimensionality of the pencil force their
\(b_i\)'s onto one line. Applying the same argument across the graph gives
(3).

If that line were isotropic, it would equal its orthogonal line, so all
five \(b_i\)'s would share one line. Equation (7) would again fix all five
blocks at site \(0\), and (12) would apply. Thus a rank-\(55\) residue has
two distinct nonisotropic orthogonal lines.

In the original selected coordinates, write \(b_A=(p,q)\). Nonisotropy
means \(pq\ne0\), and its unique \(J\)-orthogonal line is generated by
\((p,-q)\). Consequently

\[
                         b_B\parallel(p,-q),                  \tag{19}
\]

so the two selected projective slopes are antipodal. This is a statement
in the physical selected basis, not a local normalization.

Absorb the shorewise scalar multiples of \(b_A,b_B\) into the \(h_i\).
Then:

- every block in \(A\times B\) is free;
- every within-\(A\) and within-\(B\) block is a fixed nonzero multiple of
  \(h_ih_j^{\mathsf T}\), because
  \(b_A^{\mathsf T}Jb_A\) and \(b_B^{\mathsf T}Jb_B\) are nonzero; and
- the \(0\)-spokes have the two constant forms
  \[
  M_{0i}=g_Ah_i^{\mathsf T}\ (i\in A),\qquad
  M_{0j}=g_Bh_j^{\mathsf T}\ (j\in B),                         \tag{20}
  \]
  up to nonzero shorewise scalars, where \(g_A,g_B\) are independent.

This is the promised covariant residual normal form. It has four arbitrary
blocks for \(K_{1,4}\) and six for \(K_{2,3}\).

For \(J=\left(\begin{smallmatrix}0&1\\1&0\end{smallmatrix}\right)\), a
nonisotropic line has both coordinates nonzero. Hence every rank-one
\(X_i=h_ib_i^{\mathsf T}\) has both selected endpoint columns nonzero.
The invertible root does as well. At all six roots, the outside selected
column makes R2 preservation fail, and neither selected endpoint edge can
be a pure binary-column witness. Literal residual R2 therefore requires
two distinct **internal** edges at every root, one pure in each physical
binary output column.

At root \(0\), the internal edges are precisely the five \(0\)-spokes.
Since \(g_A,g_B\ne0\), the block \(M_{0i}=g_Sh_i^{\mathsf T}\) is pure
in physical output column \(c\) exactly when \(h_i\parallel e_c\).
Thus the two witnesses demanded by R2 at root \(0\) give the concrete,
coordinate-covariant restriction

\[
 \exists i\ne j:\qquad h_i\parallel e_0,qquad h_j\parallel e_1. \tag{21}
\]

No normalization is used in (21); the two axes are the original physical
binary output columns.

This R2 witness condition is retained as part of the open \(K_{1,4}\) and
\(K_{2,3}\) residue. No normalized \(h_i\) or \(g_A,g_B\) line is called a
physical pure column.

## Exact audit

The standard-library checker
[verify_level_two_one_invertible_five_rank_one_potential_reduction.py](../computations/verify_level_two_one_invertible_five_rank_one_potential_reduction.py)

- verifies 625 exact instances of the rank-one pair-pencil identity (6)
  and the nonvanishing invertible-root images (7);
- exhausts all \(5^5\) signed-value assignments needed to realize every
  graph in (13), including distinct-magnitude component realizations;
- imports the exact \(32+10=42\) fixed-root theorem and its sharp integral
  rank-\(42\) calibration;
- audits the two-dimensional complete-orthogonal-pencil argument on an
  exact projective grid;
- imports all 64 coordinate-shore path identities behind (17) and all 64
  constant-cross triangle identities behind (18);
- checks the two connected covariant normal forms, their nonisotropic
  antipodal paired-pencil representative, their free-block counts, and
  the exact root-\(0\) pure-column criterion; and
- records the literal two-internal-witness R2 alternative at all six
  remaining roots.

It passes normal, optimized, and isolated Python.
