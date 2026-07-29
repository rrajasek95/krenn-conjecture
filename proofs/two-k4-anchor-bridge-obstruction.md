# Two standard `K_4` equality blocks cannot be synchronized by an anchor-free bridge

This note rules out the most direct eight-site counterexample architecture,
including arbitrary endpoint colors, parallel sources, and signed complex
weights on the bridge.

Let `C={0,1,2}`.  The left four-site block has vertices

\[
                         L_*,L_0,L_1,L_2
\]

and the right block has vertices `R_*,R_0,R_1,R_2`.  In each block put the
standard three one-factor realization of four-site ternary equality: the
color-`r` one-factor is

\[
 L_*L_r\mid L_iL_k,
 \qquad \{i,k\}=C\setminus\{r\},                         \tag{1}
\]

and similarly on the right.  The two weights in each one-factor may be
arbitrary nonzero complex numbers whose product is one.  Add arbitrary
two-endpoint tensors

\[
             B_{ij}\in V_{L_i}\otimes V_{R_j}
             \qquad (i,j\in C)                            \tag{2}
\]

between the six nonanchor vertices, but no bridge incident with `L_*` or
`R_*`.  Parallel sources in (2) are allowed and are aggregated into
`B_{ij}`.

We prove that the resulting eight-site matching tensor cannot be

\[
               \Delta_{8,3}=e_0^{\otimes8}
                 +e_1^{\otimes8}+e_2^{\otimes8}.          \tag{3}
\]

## 1. The required six-terminal signature

Every full matching uses zero or two bridge edges.  With zero bridge edges,
the two `K_4` blocks give all nine block-constant tensors, each with
coefficient one.  If two bridge edges are used, the anchors must use
`L_*L_r` and `R_*R_s` for unique `r,s`; the bridge then near-perfectly
matches

\[
       \{L_i:i\ne r\}\quad\hbox{to}\quad\{R_j:j\ne s\}.
\]

Write `K_rs` for the four-site tensor obtained by summing the two bridge
matchings on this `K_{2,2}`.  The colors at the two anchor edges isolate
the nine pairs `(r,s)`, so (3) would force

\[
 K_{rr}=0,
 \qquad
 K_{rs}=\kappa_{rs}
   \bigotimes_{i\ne r}e_r^{(L_i)}
   \bigotimes_{j\ne s}e_s^{(R_j)}\ne0
       \quad(r\ne s),                                    \tag{4}
\]

where every `kappa_rs` is nonzero.  With unit anchor-edge weights it is
`-1`; allowing arbitrary weights only rescales it and will not matter.

Thus the proposed synchronization is exactly a six-terminal
``not-equal'' near-perfect signature.

## 2. Its support is necessarily all of `K_{3,3}`

Let

\[
                         S=\{(i,j):B_{ij}\ne0\}.           \tag{5}
\]

For `r != s`, the nonzero identity in (4) says that at least one of the two
perfect matchings of the complementary `K_{2,2}` is contained in `S`.
For `r=s`, the two matching products sum to zero.  A tensor product of
nonzero tensors is nonzero, so those two matchings are either both
supported or both unsupported.  These nine Boolean conditions force

\[
                              S=C\times C.                \tag{6}
\]

Here is a direct proof.  Write `z_ij` for the indicator of `(i,j) in S`.
Simultaneous permutation of rows and columns and transposition leave the
conditions invariant, so a missing edge may be taken to be `z_00` or
`z_01`.

If `z_00=0`, the off-diagonal complement `(r,s)=(1,2)` forces
`z_01=z_20=1`.  The diagonal complements `r=2` and `r=1` then force,
respectively, `z_10=0` and `z_02=0`.  But the two matching bits for the
off-diagonal complement `(2,1)` are

\[
                  z_{00}z_{12},\qquad z_{02}z_{10},
\]

both zero, a contradiction.  If `z_01=0`, the complement `(1,2)` forces
`z_00=z_21=1`; the diagonal complement `r=2` then forces `z_11=0`.
The two bits for complement `(2,0)` are now

\[
                  z_{01}z_{12},\qquad z_{02}z_{11},
\]

again both zero.  Thus no edge is missing and (6) follows.  The
accompanying checker also exhausts the full `2^9` truth table.  The lemma
is independent of coefficients or genericity.

## 3. The three zero squares collapse every endpoint to one line

Fix `r`, and write `C\setminus{r}={i,k}`.  Since all nine bridge tensors
are nonzero, the diagonal equation `K_rr=0` is an equality of two nonzero
products on different perfect matchings:

\[
              B_{ii}B_{kk}+B_{ik}B_{ki}=0,                \tag{7}
\]

with tensor factors restored to their four physical sites.  The standard
crossing-product lemma applies: all four edge tensors in this square have
matrix rank one, and the two incidence factor lines agree at every corner
of the square.

The three choices of `r` cover all nine bridge edges.  At a fixed left
vertex `L_i`, the two squares indexed by the two values `r != i` identify
the incidence line on each pair of columns sharing column `i`; hence all
three incidence lines agree.  The same holds at every right vertex.
Consequently there are nonzero one-site vectors `u_i,v_j` and nonzero
scalars `lambda_ij` such that

\[
                         B_{ij}=\lambda_{ij}u_i\otimes v_j
                         \quad(i,j\in C).                 \tag{8}
\]

This conclusion also covers every degenerate intersection of the three
crossing-product strata: (6) already excludes zero edge tensors.

## 4. Two off-diagonal signatures give incompatible colors

Substituting (8) into an off-diagonal `K_rs`, its two matching terms have
the same one-site factors.  Equation (4), being nonzero, therefore implies

\[
                 \mathbb C u_i=\mathbb C e_r
                 \quad\hbox{for every }i\ne r,            \tag{9}
\]

and analogously `C v_j=C e_s` for every `j != s`.

Take `i=0`.  The pair `(r,s)=(1,0)` in (9) gives
`C u_0=C e_1`, while `(r,s)=(2,0)` gives
`C u_0=C e_2`.  These coordinate lines are distinct, a contradiction.
Therefore the anchor-free bridge architecture cannot realize (3).

## 5. A coordinate-pure anchor endpoint still cannot repair it

The obstruction survives the smallest anchor-incident enlargement.  Add an
edge `L_*R_*` whose aggregate tensor is supported in one coordinate row or
one coordinate column,

\[
             D=e_p\otimes v\quad\hbox{or}\quad u\otimes e_q,
             \qquad D\ne0.                               \tag{10}
\]

Every matching using this edge contributes only to the anchor-color slice
coordinates in the exact support of `D`.  Therefore every other equation
in (4) remains unchanged; the tensor on the six nonanchor sites contributed
by such matchings may be completely arbitrary for the following argument.

First consider the monomial special case
`D=d e_p\mathbin\otimes e_q`.  Up to
simultaneous color permutation and transposition, the omitted equation is
`(0,0)` or `(0,1)`.  Impose on the other eight complementary squares the
same necessary support conditions used in Section 2.  If `(0,0)` is
omitted, the only surviving bridge supports have respectively seven,
eight, eight, and nine edges:

\[
 C^2\setminus\{12,21\},\quad
 C^2\setminus\{21\},\quad
 C^2\setminus\{12\},\quad C^2.                            \tag{11}
\]

If `(0,1)` is omitted, the only survivors are

\[
 \{00,01,02,10,11,21\},\qquad C^2.                        \tag{12}
\]

Each is already contradictory by the following two elementary
consequences of an unchanged equation.

* A supported diagonal zero square promotes its four edge tensors to
  rank one and identifies the two endpoint lines at each corner.
* If exactly one matching supports a nonzero off-diagonal pure signature,
  its two edge tensors are rank one and their endpoint lines are the
  prescribed coordinate lines.  If both matchings are supported but their
  two incidence lines at a vertex have already been identified, that
  common line must likewise be the prescribed coordinate line.

Applying these implications to (11)--(12) always labels one identified
endpoint line by two distinct colors.  For example, on the full support in
(11), the unchanged diagonal squares `r=1,2` identify all three incidence
lines at `L_0`; the unchanged signatures `K_10` and `K_20` label that line
by `e_1` and `e_2`.  On the six-edge support in (12), the unique terms of
`K_02` and `K_10` both use `B_21`, labeling its left endpoint by `e_0` and
`e_1` directly.  The other three sparse masks are the row/column symmetric
versions of the same line conflict.  The checker exhausts all `512`
supports and audits every implication, so no genericity is hidden here.

The same exact audit proves the stronger statement (10).  There are `34`
possible exact coordinate supports contained in at most one row or at most
one column (including the empty support).  For each of them and each of the
`512` bridge-edge supports, the untouched square equations either fail the
necessary matching-support condition or the preceding rank-one line
implications give two different color labels on one line.  This is a
finite `34*512` truth-table proof; the checker implements the implications
directly rather than using numerical rank tests.

Thus an arbitrary signed complex vector `v` or `u` in (10), and in
particular one arbitrary-weight monomial anchor cell, cannot repair the
two-block construction.  This extension does not claim the same for a
matrix on `L_*R_*` having at least two active coordinate rows and columns;
such a matrix contaminates several anchor slices simultaneously and is a
genuinely larger ansatz.

The exact audit
[`computations/verify_two_k4_anchor_bridge_obstruction.py`](../computations/verify_two_k4_anchor_bridge_obstruction.py)
enumerates the 27 anchor-free underlying full matchings (and all 42 after
adding `L_*R_*`), checks the reduction to the nine signatures (4),
exhausts the `512` bridge supports, and audits the endpoint-line
propagation and final color conflicts.
