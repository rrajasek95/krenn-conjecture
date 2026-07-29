# The three-color block-diagonal ansatz at `n=8` is impossible

This note settles the following finite subproblem.  Split the eight binary
sites into the four canonical pairs

\[
 P_i=\{i0,i1\}\qquad(0\leq i<4),
\]

and let `B_uv` be an arbitrary tensor in `V_u ⊗ V_v`, where every `V_u`
is two-dimensional.  Suppose `B_i0,i1=0` and

\[
 H_B(P_I)=0\quad(\varnothing\ne I\subsetneq\{0,1,2,3\}),
 \qquad H_B(P_0\cup P_1\cup P_2\cup P_3)=\Delta_{8,2}.       \tag{1}
\]

Here `H_B(S)` is the sum of the tensor products belonging to the perfect
matchings of `S`, and

\[
 \Delta_{8,2}=e_0^{\otimes8}+e_1^{\otimes8}.                \tag{2}
\]

We prove that (1) has no solution.  Consequently one cannot obtain a
three-color `n=8` example by adjoining a scalar color supported only on the
canonical matching `01|23|45|67` to an arbitrary binary block.

## 1. The two crossing-product facts

We use the following elementary tensor observation repeatedly.

**Crossing-product lemma.**  Suppose two nonzero products of two-site
tensors, supported on two different perfect matchings, are equal.  Delete
the common matching edges.  On every remaining alternating cycle, every
two-site tensor has matrix rank one, and the resulting one-site factor
lines agree at each vertex on the two sides of the equality.

Indeed, take two adjacent vertices which form an edge of the first
matching.  The first product has Schmidt rank one across this two-vertex
set versus its complement.  In the second product exactly two matching
edges cross that cut, so its Schmidt rank is the product of the ranks of
those two edge tensors.  Both ranks are therefore one.  Moving around the
alternating cycle proves the assertion.  Equality of the resulting fully
decomposable tensors then identifies their factor lines at every site.

We will also use the immediate two-term version: if a zero hafnian has two
nonzero matching terms, cancel their common nonzero tensor product and apply
the lemma to the residual matchings.

## 2. The five maximal K2,2 components

For two canonical blocks `P_i,P_j`, the four-site equation is

\[
 B_{i0,j0}\otimes B_{i1,j1}
 +B_{i0,j1}\otimes B_{i1,j0}=0,                              \tag{3}
\]

with the tensor factors put back in site order.  If precisely one summand
is nonzero, (3) is impossible.  If both vanish, the nonzero support contains
neither pair of opposite edges of the four-cycle.  It is therefore contained
in one of the four two-edge stars.

If both summands are nonzero, the crossing-product lemma gives nonzero
one-site vectors and scalars such that

\[
 B_{ia,jb}=\lambda_{ab}u_{ia}^{j}\otimes u_{jb}^{i},
 \qquad
 \lambda_{00}\lambda_{11}+\lambda_{01}\lambda_{10}=0.       \tag{4}
\]

All four scalars are nonzero.  In particular

\[
 \det(\lambda_{ab})=2\lambda_{00}\lambda_{11}\ne0.          \tag{5}
\]

After absorbing row and column scalars into the endpoint vectors, its
scalar matrix is

\[
 W=\begin{pmatrix}1&1\\1&-1\end{pmatrix}.                   \tag{6}
\]

We call this the **dense** component.  Thus the exact possibilities for a
layer are: empty support, one of four singletons, one of four full stars, or
the dense component.  Their bit masks in edge order `00,01,10,11` are

\[
 0;\quad1,2,4,8;\quad3,5,10,12;\quad15.                     \tag{7}
\]

## 3. The six-site promotion lemmas

Call a corner `(i;j,k)` coherent if, at both sites of `P_i`, the rank-one
incidence line toward `P_j` equals the incidence line toward `P_k`.

**Lemma 3.1 (two terms).**  In a two-term six-site identity, every edge left
after canceling the common matching edges has rank one, and the two residual
incidence lines agree at every residual vertex.

This is exactly the two-term crossing-product lemma above.

**Lemma 3.2 (four terms with a dense layer).**  Suppose a block triangle has
four supported matching terms and at least one dense layer.  Every edge in
those four terms has rank one.  Moreover:

1. if two layers are dense, their common block and the noncenter block of
   the remaining star are coherent corners;
2. if one layer is dense, its two endpoint blocks are coherent corners.

**Proof.**  There are only two support configurations.

First let `AB` and `AC` be dense and let the `BC` star be centered at `B0`.
Use (6) on both dense layers.  Put

\[
 X=u_{A0}^{B}\otimes u_{A1}^{C},\qquad
 Y=u_{A0}^{C}\otimes u_{A1}^{B}.                            \tag{8}
\]

Grouping the four matching terms by which star edge uses `C0` or `C1`
turns the zero identity, up to nonzero scalar factors, into

\[
 -(X+Y)\otimes(S_0\otimes u_{C1}^{A})
 +(X-Y)\otimes(u_{C0}^{A}\otimes S_1)=0.                    \tag{9}
\]

The omitted fixed factor at `B1` is common.  Neither `X+Y` nor `X-Y` can
vanish: if one vanished, the other would be twice a nonzero tensor, leaving
one nonzero summand in (9).  Hence the two factors on each side of (9) are
proportional.  Proportionality of `X+Y` and `X-Y` makes `X` and `Y`
proportional, which is coherence at `A`.  Applying the crossing-product
lemma to the other proportionality makes `S_0,S_1` rank one, identifies
their factors at the star center, and aligns their factors at `C0,C1` with
the dense factors.  This is coherence at `C`.

Second let `AB` be dense, and let the two other stars be centered at the two
different sites `C0,C1`.  (This is the only one-dense star configuration
with four supported matchings.)  If their edge tensors are `S_a` on
`A_a C0` and `T_b` on `B_b C1`, define

\[
 P_a=S_a\otimes u_{A,1-a}^{B},\qquad
 Q_b=T_b\otimes u_{B,1-b}^{A}.                              \tag{10}
\]

The identity is

\[
 \sum_{a,b=0}^1 W_{1-a,1-b}P_a\otimes Q_b=0.                \tag{11}
\]

Since `W` is invertible, (11) cannot vanish if either of the two maps
sending `a` to `P_a` and `b` to `Q_b` has rank two.  Both pairs are therefore
proportional.  Applying the crossing-product lemma to these two
proportionalities makes all four star matrices rank one and gives coherence
at `A` and `B`.  This proves the lemma. `QED`

**Lemma 3.3 (eight dense terms).**  In an all-dense block triangle,
`H_6=0` forces at least two of its three corners to be coherent.

**Proof.**  For each block `i`, let

\[
 L_i:\mathbb C^2\longrightarrow V_{i0}\otimes V_{i1}       \tag{12}
\]

send its two orientation states to the products of its two incidence
vectors toward the other two blocks.  With the dense scalar weights (6),
the six-site tensor is

\[
 (L_i\otimes L_j\otimes L_k)\Omega.                         \tag{13}
\]

Every mode flattening of the `2 by 2 by 2` tensor `Omega` has rank two: the
ratio of its two rows changes sign when either of the other orientation bits
is flipped.  If all three `L` maps are injective, (13) is nonzero.  If just
one has rank one, contracting the corresponding full-rank mode flattening
by its nonzero two-coordinate row is still nonzero, and the other two maps
are injective.  Thus at least two maps have rank one.  The two columns of
`L_i` are decomposable and nonzero, so `rank(L_i)=1` is exactly coherence of
the corner at block `i`. `QED`

## 4. Formal matching relations and the finite support audit

The remaining step is finite and exact.  For a fixed exact support, attach
a formal basis vector to each supported full perfect matching.  A proper
zero identity with supported matchings `M_1,...,M_r` may have a common
matching `C`.  Its tensor product is nonzero, so it can be canceled, giving

\[
 \sum_s \prod_{e\in M_s\setminus C}B_e=0.                  \tag{14}
\]

Multiplying (14) by any matching product on the complementary vertices
gives a linear relation among full matching products.

Exact rational row reduction has two immediate certificates.

* If the all-ones full-hafnian coefficient vector reduces to zero, then
  `H_8=0`.
* If the reduced terms have no edge crossing a nontrivial vertex cut and
  their coefficient matrix across that cut has rank one, then `H_8` is a
  product tensor across the cut.

Either conclusion contradicts (2), whose Schmidt rank across every
nontrivial cut is two.

The checker
[`computations/verify_block_diagonal_type_obstruction.py`](../computations/verify_block_diagonal_type_obstruction.py)
performs the following exhaustive audit using only integer set operations,
union-find, and rational Gaussian elimination.

1. It enumerates the `10^6` patterns from (7).
2. It deletes patterns with fewer than two full matchings, or exactly one
   matching on a proper union of canonical pairs.  A unique proper matching
   is a nonzero tensor and cannot give the required zero; a unique full
   matching factors across one of its matched pairs and cannot equal (2).
   There remain `73,749`.
3. It quotients by the group `S_4 semidirect (C_2)^4`, of order `384`,
   leaving `501` exact-support orbits.
4. Relations (14) close `123` orbits by zero and `318` by a product cut.
5. On the remaining `60`, it applies Lemmas 3.1--3.3.  For every allowed
   choice of the two or three coherent corners in every all-dense triangle,
   it takes the transitive closure of the forced endpoint-line equalities.
   In `58` orbits, some physical vertex has one common rank-one factor in
   every full matching term.  Thus `H_8` has mode rank at most one there.

All statements used in step 5 are one-way necessary implications, so the
audit is valid on degenerate intersections of components as well as on
generic points.  Enumerating exact masks, rather than only the five maximal
components, is essential here.

## 5. The first exceptional sparse cycle

The first of the two remaining representatives is

\[
 (0,3,12,15,15,0),                                        \tag{15}
\]

in block-pair order `01,02,03,12,13,23`.  Thus `02,03` are
stars centered at the two different sites of block zero, `12,13` are dense,
and `01,23` are empty.  There are no supported six-site matchings.

Let `c,d` select the two star edges, and let `a` say which site of block one
goes to block two.  After grouping sites as

\[
 G_1=P_1,\qquad G_2=\{00\}\cup P_2,\qquad
 G_3=\{01\}\cup P_3,                                      \tag{16}
\]

the full tensor has the form

\[
 (L\otimes P\otimes Q)\Omega_3,\qquad
 (\Omega_3)_{a,c,d}=W_{a,1-c}W_{1-a,1-d}.                  \tag{17}
\]

All eight coefficients in (17) are nonzero, and each mode flattening has
rank two.  Equality with (2), whose three grouped mode ranks are two, forces
all three maps `L,P,Q` to be injective and forces each of their images to be

\[
 \operatorname{span}\{e_0^{\otimes |G_i|},
                         e_1^{\otimes |G_i|}\}.             \tag{18}
\]

Every column of `L`, `P`, or `Q` has a product factor at at least one
physical site.  A nonzero tensor
\(\alpha e_0^{\otimes m}+\beta e_1^{\otimes m}\) has Schmidt rank one at
such a site only if \(\alpha\beta=0\).  Hence the two columns of each map
must be the two pure constant rays, in some order.  Only rescalings and swaps
of the three binary indices are possible.  They cannot change the
eight-point support of `Omega_3` into the two-point support of the grouped
GHZ tensor.  This contradicts (2).

## 6. The second exceptional sparse cycle

The last representative is

\[
 (0,15,15,15,15,0).                                       \tag{19}
\]

The four nonempty block layers form the cycle `0-2-1-3-0` and are all
dense.  Full matchings using two doubled block layers sum to products of
the corresponding four-site hafnians and hence vanish.  The remaining
cycle tensor is

\[
 (L_0\otimes L_1\otimes L_2\otimes L_3)\Omega_4,           \tag{20}
\]

where each `L_i` is the two-orientation map for block `i`.  If some `L_i`
has rank one, (20) has block-mode rank at most one, contrary to (2).
Otherwise all four maps are injective.

For the orientation convention used by the checker, the flattening of the
Hadamard-sign core across `{0,2}|{1,3}` is

\[
 \begin{pmatrix}
 -1&-1& 1&-1\\
 -1&-1&-1& 1\\
  1&-1&-1&-1\\
 -1& 1&-1&-1
 \end{pmatrix},                                            \tag{21}
\]

whose determinant is `-16`.  Injective local maps preserve this Schmidt
rank four, whereas (2) has Schmidt rank two across the same block cut.  This
is the final contradiction.

Running

```text
uv run python computations/verify_block_diagonal_type_obstruction.py
```

prints

```text
exact supports: admissible=73749, orbits=501, formal_outcomes={'open': 60, 'product': 318, 'zero': 123}
promotion/coherence audit closes 58 of the 60 formal open orbits
two sparse cycle cores close the final 2 orbits
all 501 admissible exact-support orbits are obstructed
```

This completes the exact obstruction to (1).
