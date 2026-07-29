# Color-sensitive combinations of all star expansions

The scalar averaging identity can be strengthened by using the full
diagonal infinitesimal stabilizer of the target.  This retains asymmetric
endpoint colors and can delete an edge coordinate-by-coordinate.

Let (H_B(A)=\Delta_{B,q}).  Choose scalars
(\alpha_{v,r}) satisfying

\[
 \sum_{v\in B}\alpha_{v,r}=1\qquad(r=1,\ldots,q),            \tag{1}
\]

and let (D_v e_r=\alpha_{v,r}e_r).  Since each constant-color target
summand acquires the scalar in (1),

\[
 \Delta_{B,q}=\sum_vD_v^{(v)}\Delta_{B,q}.                  \tag{2}
\]

Apply the right side to the matching expansion and group by the edge on
which the local operator acts.  One obtains the exact identity

\[
 \Delta_{B,q}=\sum_{u<v}B_{uv}^{(\alpha)}\otimes
 H_{B\setminus\{u,v\}}(A),                                 \tag{3}
\]

where

\[
 B_{uv}^{(\alpha)}=(D_u\otimes I+I\otimes D_v)A_{uv},
 \qquad
 B_{uv}^{(\alpha)}(i,j)
   =(\alpha_{u,i}+\alpha_{v,j})A_{uv}(i,j).                 \tag{4}
\]

Every nonzero term in (3) has partition rank one.  Consequently

\[
 q\le
 \min_{\sum_v\alpha_{v,r}=1\ (\forall r)}
 \#\{uv:B_{uv}^{(\alpha)}\ne0,
       H_{B\setminus\{u,v\}}(A)\ne0\}.                     \tag{5}
\]

For an entry-minimal realization every nonzero underlying matrix has a
nonzero complementary tensor, so the second condition in (5) can be
omitted.  An edge is killed precisely when the linear equations

\[
 \alpha_{u,i}+\alpha_{v,j}=0
 \quad\text{hold for every }(i,j)\in\operatorname{supp}A_{uv}. \tag{6}
\]

Taking all three color coordinates of (\alpha_v) equal recovers the
earlier scalar identity.  Taking one vertex vector equal to
((1,\ldots,1)) and all others zero recovers the ordinary star expansion.
The gain is that (6) sees endpoint-color support and can kill asymmetric
rank-one anchors without killing every matrix on the same underlying
support pattern.

The diagonal operators used here are the full infinitesimal local
stabilizer relevant to this construction when (|B|\ge3): an off-diagonal
entry at one site sends a constant target summand to a basis coloring with a
unique exceptional vertex, so it cannot be canceled by an operator at a
different site.  The diagonal entries are constrained exactly by (1).

The remaining task is an equality/linear-matroid analysis of (5).  If an
(\alpha) leaves only three edges for (q=3), (3) is a minimal
three-term partition decomposition and should be combined with its precise
cut pattern.  Dense full-support matrices impose all nine equations in
(6), whereas a forced rank-one anchor imposes only the equations on its
one-dimensional coordinate support; thus the identity is especially
compatible with `notes/slice-cover.md`.
