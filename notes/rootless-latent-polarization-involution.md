# The rank-six full-nine shadow is a latent involution problem

## Result

Let `L` be the six-dimensional latent space of a rank-six response, let `J`
be its nondegenerate symmetric response form, and let

\[
             C:\operatorname{Sym}^2L\longrightarrow T
\]

be the tensor-valued polarization supplied by the common quadratic block.
Fix the target subspace

\[
 W=\operatorname{span}\{q^{[3]},X_0,X_1,X_2\}\subseteq T.
\]

The following two conditions are equivalent over a field of characteristic
different from two.

1. There is a direct sum `L=P+S`, with `dim P=dim S=3`, such that

   \[
   J(P,P)=J(S,S)=0,\qquad C(P,S)\subseteq W.             \tag{1}
   \]

2. There is an endomorphism `R` of `L` satisfying

   \[
   R^2=1,\quad \operatorname{tr}R=0,\quad
   R^{\mathsf T}J+JR=0,                                 \tag{2}
   \]

   and, for every `lambda` annihilating `W`,

   \[
   A_\lambda R+RA_\lambda=0,
   \qquad A_\lambda=J^{-1}(\lambda\circ C).             \tag{3}
   \]

This gives a small, intrinsic and basis-invariant necessary test for the
rank-six rootless branch.  The exact checker is
`computations/verify_rootless_latent_polarization_involution.py`.

The physical logical direction is important:

\[
 \text{literal full-nine equations}
 \Longrightarrow (1) \Longleftrightarrow (2),(3).        \tag{4}
\]

The reverse implication in (4) is not asserted.  Equations (2),(3) recover
only the coarse target-span containment (1); they do not recover the common
direct coefficient matrix, the prescribed diagonal pattern of the nine
rows, or their word, fine, occurrence and source labels.

## Proof

Assume (1).  Define `R=+1` on `P` and `R=-1` on `S`.  It is an involution
of trace zero.  Because `P` and `S` are `J`-isotropic,

\[
                  J(Rx,y)+J(x,Ry)=0,
\]

so `R` is `J`-skew.  For `lambda` in `W`-perp, (1) says that the symmetric
form `C_lambda=lambda o C` has no `P`-by-`S` block.  Since `J` has only a
nondegenerate `P`-by-`S` block, `A_lambda=J^{-1}C_lambda` is off-diagonal.
That is exactly (3).

Conversely, let `R` satisfy (2),(3).  In characteristic different from two,
`L` is the direct sum of the `+1` and `-1` eigenspaces.  The trace condition
makes both dimensions three.  If `x,y` lie in the same eigenspace, the
`J`-skew identity gives `2J(x,y)=0`; both eigenspaces are therefore maximal
`J`-isotropic.  Anticommutation sends each eigenspace through `A_lambda` to
the other.  Hence, for `p` in the plus eigenspace and `s` in the minus
eigenspace,

\[
 C_\lambda(p,s)=J(A_\lambda p,s)=0.
\]

This holds for every `lambda` annihilating `W`, so `C(P,S)` lies in `W`.

## What this buys us

The other eight uncontracted physical pair rows were previously an unwieldy
collection of cross-word tensor equations.  In the full-rank latent branch,
their first unavoidable shadow is now the finite polynomial system (2),(3)
in the 36 entries of one endomorphism `R`.  It is invariant under a change of
latent basis:

```text
J,C  -> g^T (J,C) g,
R    -> g^-1 R g.
```

This is a useful rootless certificate target.  To exclude a proposed packet
it is enough to prove that (2),(3) have no solution.  For example, if one
projected polarization form equals `J`, then `A_lambda=1`; (3) becomes
`2R=0`, which is incompatible with `R^2=1`.

For a positive proof, however, solving (2),(3) is only a first stage.  One
must still impose the literal common-direct-matrix and nine-row diagonal
conditions.  Any argument which silently promotes a solution of the
involution system to a physical factorization repeats the same loss of
source labels that invalidated the direct six-site reduction.

## Rank-deficient branch

This theorem deliberately assumes `dim(P+S)=6`.  If the two injective
three-dimensional endpoint stars overlap, they do not form complementary
eigenspaces of an involution on `L`.  That branch is geometrically different
and must be classified before this test can be called exhaustive.  The
checker includes a rank-four overlap guard to prevent accidental use of the
rank-six equivalence there.

## Consequence for the proof strategy

The highest-value intrinsic rootless attack now has two finite stages.

1. Split by `dim(P+S)`.  Classify the overlapping-star branch directly.
2. In the rank-six branch, eliminate the involution system (2),(3) together
   with the remaining literal nine-row constraints and the activity
   saturation.

An inconsistency gives an EqSystem-level rootless contradiction without any
duplicated `B/Eq`, `AugP2`, or mapping-cylinder choices.  A solution gives a
sharply structured candidate which can be tested against the literal source
rows rather than another auxiliary presentation.
