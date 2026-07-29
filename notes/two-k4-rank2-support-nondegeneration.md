# Rank-two singularity does not force a transversal-support degeneration

## 1. The audit result

The determinantal-boundary theorem in
[`two-k4-dead-slice-determinantal-boundary.md`](two-k4-dead-slice-determinantal-boundary.md)
shows that a putative full two-`K_4` realization has a singular cross block.
It is tempting to contract a kernel direction and invoke either the
low-matching theorem or the unique-perfect-matching theorem.  Singularity
alone does not justify that step.

**Theorem 1.1 (support nondegeneration).**  For every pair of colours
`z,c`, there is an exact system of cross matrices with the following
properties.

1. `B_00` has rank exactly two, zero row `z`, zero column `c`, and otherwise
   full support.  The other fifteen blocks are invertible and have all nine
   cells nonzero.
2. Every one of the `3^8` coordinate words has at least eighteen supported
   cross-sector matching monomials.  In particular, all six off-diagonal
   block-constant words have a supported correction, and no zero-target
   fibre is a singleton.
3. Contracting the left kernel of `B_00`, the right kernel, or both, while
   taking generic vectors at the other sites leaves the scalar transversal
   graph `K_(4,4)-L_0R_0`.  It has eighteen perfect matchings.

Thus a rank-two singular block does not force either matching number at most
three or a unique transversal perfect matching, even after the natural
kernel contractions.  This is a limitation theorem, not a weighted solution
of the target equations.  It says that the remaining proof must use
coefficient or projective-incidence information beyond cell support.

The exact audit is
[`verify_two_k4_rank2_support_nondegeneration.py`](../computations/verify_two_k4_rank2_support_nondegeneration.py).

## 2. An explicit rank pattern

After permuting rows and columns, take

\[
 B_{00}=
 \begin{pmatrix}
 0&0&0\\
 0&1&1\\
 0&1&2
 \end{pmatrix},
 \qquad
 B_{ij}=I_3+J_3=
 \begin{pmatrix}
 2&1&1\\
 1&2&1\\
 1&1&2
 \end{pmatrix}quad((i,j)\ne(0,0)).                     \tag{1}
\]

The lower-right minor of `B_00` has determinant one, so its rank is two.
The second matrix has determinant four and full coordinate support.  Moving
the zero row and column gives all nine pairs `(z,c)`.

For a coordinate shore word `a|b`, the scalar support graph seen by the
four-cross sector is

\[
 \begin{cases}
 K_{4,4},&a_0\ne z\text{ and }b_0\ne c,\\
 K_{4,4}-L_0R_0,&a_0=z\text{ or }b_0=c.
 \end{cases}                                             \tag{2}
\]

These graphs have respectively 24 and 18 perfect matchings.  Therefore the
four-cross sector alone already prevents a singleton in every coordinate
fibre.  Adding the compatible two-cross matchings gives the exact histogram

\[
\begin{array}{c|rrrrrrrrrr}
\text{supported terms}&18&19&20&21&22&24&25&26&28&32\\ \hline
\text{number of words}&2200&320&960&80&80&1760&5&1024&128&4.
\end{array}                                               \tag{3}
\]

This histogram is the same for all nine choices `(z,c)`.  In particular,
the minimum is eighteen, not merely two.

## 3. Kernel contraction still leaves eighteen transversals

Let `ell=e_z` be the left kernel row and `r=e_c` the right kernel column of
`B_00`.  Use `ell` at `L_0`, `r` at `R_0`, and the all-ones vector at the
other six sites.  Then

\[
             \ell^{\mathsf T}B_{00}r=0.                 \tag{4}
\]

Every other contracted cross edge is nonzero: on an edge incident with one
kernel endpoint the value is four, and away from those endpoints it is
twelve.  Hence the contracted support is exactly `K_(4,4)-L_0R_0`.  The
same conclusion holds if only `ell` or only `r` is imposed.  Since the
nonvanishing conditions on the other fifteen bilinear evaluations are
Zariski open, this is also the generic behaviour of either kernel
contraction, not an artefact of the displayed positive matrices.

The remaining graph has eighteen transversal perfect matchings and many
alternating cycles.  Nothing in the rank-two kernel by itself selects one
of them.

## 4. Sharp deletion thresholds

There is also a simple graph-theoretic reason the desired degeneration
cannot follow from one forced zero edge.

* A bipartite graph on `4+4` vertices with a unique perfect matching has at
  most ten edges.  After normalizing that matching, contraction gives an
  acyclic digraph, and a topological order embeds it in the ten-edge upper
  triangular graph.  Thus at least six edges must be deleted from `K_(4,4)`
  to leave a unique perfect matching.
* At least four edges must be deleted to destroy all perfect matchings.  Four
  suffice by isolating a vertex, while Hall's theorem, or direct extension
  of a partial permutation, shows that three do not.

The checker exhausts all `2^16` bipartite supports and verifies both sharp
thresholds.  Consequently a local-contraction reduction from the singular
boundary to the already excluded graph strata must propagate at least three
additional forced edge zeros to lose matching number four, or at least five
additional zeros to retain exactly one perfect matching.

## 5. Consequence for the rank-two program

The support countermodel satisfies every usual constant-nonempty and
mixed-no-singleton condition, yet it is not claimed to satisfy any matching
coefficient equation.  The useful conclusion is methodological and strict:
dead-slab permanent identities must force extra proportionalities or
cancellations before a singleton Hamilton contraction can emerge.  A proof
that jumps directly from `det B_00=0` to a low/unique transversal graph is
invalid without such a propagation lemma.

In particular, the oriented-triangle incidence mechanism from the
determinantal-boundary analysis is genuinely stronger than support.  It can
choose projective covectors adapted to several columns at once; the raw
left/right kernel of one rank-two block cannot.
