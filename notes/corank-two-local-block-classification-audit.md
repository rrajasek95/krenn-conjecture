# Audit of the corank-two local block classification

## Outcome

The dimension arguments, the pairwise-distinct rank-two branch, the
rank-three classification, and the connected-graph propagation in
[`corank-two-local-block-classification.md`](corank-two-local-block-classification.md)
are valid.  The first version did omit one coordinate family in the
repeated-row-line rank-two branch: when the repeated line is alternating,
the outputs `v_02` and `v_12` need not vanish.  This was a real gap in the
written proof but not a counterexample.  In the omitted family `B=-A`, so
the entire physical image is skew-symmetric and cannot contain the
required invertible matrix.  The proof and exact verifier now include
this family.

## 1. Dimension and avoidance checks

Let `T=T_(A,B)` and let `D` be the four-plane of relations.  From
`T(D) subset C H` and `dim(Z_0/D)=2`,

\[
                         \operatorname {rank}T\le 3.
\]

In the dead case, rank two would give `D=ker T`.  Avoidance makes every
restriction `T|R_c` injective, hence every `T(R_c)` equals the common
two-dimensional image.  That image would lie in all three `X_c`, whose
intersection is zero.  Thus the dead image has rank at most one.

In the live rank-two case, `K_0=ker T intersection D` has dimension
three.  A row-plane restriction can have neither rank zero (by the
dimension formula inside the four-space `ker T`) nor rank two (its image
would contain the invertible `H` while lying in `X_c`).  The three row
images are therefore nonzero lines spanning the two-dimensional image.
This validates the split into pairwise-distinct lines and one repeated
line.

In live rank three,

\[
             \dim T^{-1}(\mathbb C H)=4=\dim D,
             \qquad D\subseteq T^{-1}(\mathbb C H),
\]

so equality holds.  This supplies both facts used later: `T` is
injective on every row and column plane, and its image on each such plane
avoids `C H`.

## 2. The corrected repeated-line branch

After permuting colours, write the repeated row line as

\[
                         N=xE_{01}+yE_{10}.
\]

If `x+y != 0`, the four conditions
`v_01,v_02,v_10,v_12 in C N` force `v_02=v_12=0` and give the normal
form already displayed in equation (22) of the main note.  The two
determinant identities there show that the full image pencil is singular.

If `x+y=0`, scale to `x=1,y=-1`.  Direct entry comparison instead gives

\[
 A=\begin{pmatrix}
 t_{10}&-u&t_{12}\\-v&-t_{01}&-t_{02}\\0&0&0
 \end{pmatrix},\qquad B=-A.
\]

Here `v_02=t_02 N` and `v_12=t_12 N` can both be nonzero, so the earlier
claim that they vanish was false.  Nevertheless

\[
                         T(M)=AM^{\mathsf T}-MA^{\mathsf T}
\]

is skew-symmetric for every `M`.  Every odd-dimensional skew-symmetric
matrix is singular, excluding the invertible line.  This closes the only
missed rank-two case.

## 3. Pairwise-distinct and rank-three branches

For three pairwise-distinct row lines, scaling their unique dependence
gives the three pair-supported matrices in equation (20).  They have zero
diagonal, hence `A_cd=-B_cd` off diagonal.  Therefore every component of
`v_cd` on the unordered pair joining its first colour to the third colour
is alternating.  If one of the three pair lines were nonalternating, the
two relevant outputs vanish; the resulting zero column and the remaining
two nonzero row outputs force that same pair line to be alternating after
all.  If all three pair lines are alternating, the entire image consists
of skew matrices.  Both alternatives contradict invertibility.

For rank three, the three two-planes `U_c=U intersection X_c` must be
distinct.  Their pairwise intersections are disjointly supported lines
on `01`, `02`, and `12`, so they span `U` and force every matrix in `U`
to have zero diagonal.  Any off-diagonal entry of `A` or `B` then makes
one pair line alternating.  If the corresponding diagonal column is
nonzero, the displayed three-line pencil has identically zero determinant;
if it is zero, a column-plane restriction has rank at most one.  Thus
`A,B` are diagonal.  Column-plane injectivity and the three pair-line
determinants then force all diagonal entries nonzero and `A=B`; the other
sign gives only skew matrices.  No orientation or sign case is missing.

## 4. Propagation and orthogonal closure

On an internal rank-three edge, left-right normalization really gives

\[
 P_i^{-1}\mathcal L_{ij}(M)P_j^{-\mathsf T}
   =M(P_j^{-1}S_j)^{\mathsf T}+(P_i^{-1}S_i)M^{\mathsf T}.
\]

Thus a live edge has the same invertible diagonal endpoint matrix, while
a dead edge has rank-at-most-one endpoint matrices with the same unique
column support.  A live and dead edge cannot meet.  Connectedness hence
makes all edges live or all dead.  The dead case globally kills two star
rows; the live case propagates one diagonal matrix `D` and makes
`T_D(D)` one fixed invertible symmetric zero-diagonal line.  Applying the
relation inclusion to every internal pair then forces every normalized
block `q_ij` onto that same line, including pairs outside the original
rank-three graph.

Finally, for the simultaneous group `SO(H)`, the invariant decomposition

\[
            \operatorname {Sym}^2\mathbb C^3
              =\mathbb C H\oplus\operatorname {Sym}^2_0
\]

is the trivial line plus the irreducible five-dimensional summand.  The
off-diagonal coordinate space contains `H` and a nonzero trace-free
part, so its invariant span is the full symmetric square.  Hence the six
off-diagonal pair equations annihilate the whole equivariant Hessian map
modulo `C Q`, and the three diagonal targets would all lie in `C Q`.
The global contradiction is therefore unaffected by the corrected local
case.

## 5. Computational checks

[`verify_corank_two_local_block_classification.py`](../computations/verify_corank_two_local_block_classification.py)
now checks the omitted alternating family symbolically, including
`B=-A`, all four repeated-line outputs, skew-symmetry of all six outputs,
and their zero determinants.  The full exact verifier passes.  As an
additional non-certifying stress test, 300,000 random pairs `(A,B)` over
`F_3` were screened for rank-two or rank-three block maps and then for an
invertible image line and a four-plane satisfying all six avoidance
conditions; no unclassified instance was found.
