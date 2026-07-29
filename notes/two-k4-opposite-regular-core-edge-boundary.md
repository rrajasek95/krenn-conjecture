# Opposite-regular core-edge boundary and its exact sector residual

> **Status.**  The literal-zero theorem and the sector calculations in this
> note are complete.  The arbitrary-map core-edge statement is supported by
> exact normal-form and unrelated-basis computations, but still needs an
> invariant coefficient proof.  No exact-ten support census or exact-ten
> obstruction is claimed here.

## 1. Outcome

There is a sharp local boundary behind the proposed exact-ten calculation.
Two pulled-back stars may have two common exceptional sites, while the two
remaining sites carry opposite regular legs.  Eight-cell erasure appears to
determine exactly the quadratic block joining the common exceptional sites.

The strongest tempting version is false.  When all exceptional maps vanish,
the erased Hessian has rank (9), not (54): its kernel is the literal sum
of the other five edge-block spaces and has dimension (45).  Thus no
argument may silently replace the core-edge conclusion by full injectivity,
incident-edge vanishing, or a small determinant-line residual.

For the displayed ten-position mask, even the core-edge conclusion on both
shores is insufficient.  An exact literal-zero example with all six required
nonsingular blocks invertible satisfies both core-sector equations.  At least
one further constant-cell or mixed-sector identity is therefore necessary.

The exact audit is
[`verify_two_k4_opposite_regular_core_edge.py`](../computations/verify_two_k4_opposite_regular_core_edge.py).

## 2. The local pattern

Work in

\[
 \mathcal R=\bigotimes_{i=0}^3(\mathbb F\oplus V_i),
 \qquad V_i^2=0,\qquad \dim V_i=3.                    \tag{1}
\]

Let (U,W) be three-spaces, let (K\subset U) and (L\subset W) be
planes, and put

\[
 p_x=\sum_iP_ix,\qquad s_y=\sum_iS_iy.                \tag{2}
\]

Assume only

\[
                         P_3\text{ and }S_2
                         \text{ are isomorphisms}.     \tag{3}
\]

The six maps

\[
                  P_0,P_1,P_2,S_0,S_1,S_3             \tag{4}
\]

are arbitrary.  In the two-(K_4) application they are singular, but the
local computation does not appear to need that hypothesis.

The eight-cell erasure equations are

\[
 q p_xs_y=0
       \qquad(x\in K\text{ or }y\in L),\qquad q\in\mathcal R_2. \tag{5}
\]

The sharp statement suggested by every exact calculation is the following.

**Candidate core-edge lemma.**  Under (3)--(5),

\[
                              q_{01}=0.                 \tag{6}
\]

The word *candidate* is essential.  The checker proves (6) for all
(3^6=729) simultaneous zero/rank-one/rank-two diagonal normal forms and
for eighteen exact specializations with unrelated kernels and images.  It
also survived direct finite-field searches in characteristics (2,3,5)
and exact Gaussian-rational degeneracy tests.  Those tests rule out many
plausible exceptional loci, but a finite family of simultaneous normal
forms is not an invariant proof for six arbitrary maps.

The remaining proof obligation is precise: after normalizing (P_3=S_2=I),
perform coefficient elimination in (5) without simultaneously normalizing
any two of the six maps in (4), and show that cancellation by the five
straddling edge blocks cannot mask a nonzero (q_{01}).

## 3. A proved literal-zero branch

There is a useful uniform branch that does not require the missing
elimination.

**Lemma 3.1 (zero common sites).**  Suppose

\[
                        P_0=P_1=S_0=S_1=0.             \tag{7}
\]

The maps (P_2,S_3) remain arbitrary and (P_3,S_2) remain invertible.
Then (5) forces (q_{01}=0).

**Proof.**  Every block of (q) other than (q_{01}) has a complementary
inserted factor at site (0) or (1), so its contribution to (qp_xs_y)
vanishes under (7).  The surviving response is

\[
 q_{01}\otimes
 \bigl(P_2x\otimes S_3y+S_2y\otimes P_3x\bigr).       \tag{8}
\]

Fix nonzero (x\in K).  If the parenthesis in (8) vanished for every
(y\in W), put (a=P_2x) and (b=P_3x\ne0).  If (a=0), then
(S_2y\otimes b=0) for every (y), contradicting the invertibility of
(S_2).  If (a\ne0), the equality would put the three-dimensional space

\[
                         V_2\otimes\mathbb Fb
\]

inside (\mathbb Fa\otimes V_3).  Their intersection is only
(\mathbb Fa\otimes\mathbb Fb), a line.  This is again impossible.  Thus
the parenthesis is nonzero for some (y), and (5) gives (q_{01}=0).
\(\square\)

If in addition (P_2=S_3=0), the response of (q_{01}) is simply

\[
                         q_{01}\otimes S_2y\otimes P_3x. \tag{9}
\]

It is injective, while all other five edge blocks are invisible.  Hence

\[
 \ker(5)=\bigoplus_{ij\ne01}V_i\otimes V_j,
 \qquad \dim\ker(5)=45.                               \tag{10}
\]

This proves both sharpness and the literal-zero case exactly.

## 4. Pullback for the diagnostic ten-position mask

Consider the singular-position set

\[
\begin{aligned}
 \mathcal S={}&\{00,01,02\}\cup\{10,11,13\}\\
              &\cup\{22,23\}\cup\{32,33\}.          \tag{11}
\end{aligned}
\]

Thus rows (0,1) have common exceptional columns (0,1), column (2)
is regular only for row (1), and column (3) is regular only for row
(0).  The four blocks

\[
                    B_{20},B_{21},B_{30},B_{31}        \tag{12}
\]

are all invertible.

Fix rows (2,3) to their internal factor color

\[
                         c=\kappa(23)=\kappa(01),      \tag{13}
\]

and let rows (0,1) have colors (x,y).  As in the earlier exact-eight
calculation, exact grouping of the two- and four-cross matchings gives

\[
 q_{\mathrm{eff}}=\lambda_{23}q_R+p_{2,c}p_{3,c},     \tag{14}
\]

and

\[
 q_{\mathrm{eff}}p_{0,x}p_{1,y}
   =\text{the complete two-/four-cross coefficient}.  \tag{15}
\]

For ((x,y)\ne(c,c)), the left word is nonconstant and (23) is its
unique compatible internal edge.  The target and zero-cross sectors vanish,
so a genuine realization would give all eight erasures (5).  The candidate
core-edge lemma would then give

\[
                       (q_{\mathrm{eff}})_{01}=0.      \tag{16}
\]

Write

\[
 z_i=\operatorname{row}_c(B_{2i})^{\mathsf T},\qquad
 w_i=\operatorname{row}_c(B_{3i})^{\mathsf T}.         \tag{17}
\]

In the unit chart, (16) is exactly

\[
                 E_{cc}+z_0w_1^{\mathsf T}
                         +w_0z_1^{\mathsf T}=0.        \tag{18}
\]

For arbitrary nonzero shore weights, the first term is merely multiplied by
a nonzero scalar.  Transposing the construction gives the analogous equation
for the (c)-th columns of the same four invertible matrices (12).

Unlike the three-incident-block conclusions used at exact six and exact
eight, (18) gives only one coordinate line.  A two-dimensional correction
space can absorb one line, so there is no endpoint-plane contradiction.

## 5. An exact countermodel to a core-sector closure

The failure is not merely dimensional.  Put every block in (11) literally
equal to zero and set

\[
 B_{03}=B_{12}=B_{20}=B_{21}=B_{30}=I,
 \qquad B_{31}=-2I.                                   \tag{19}
\]

These are exactly the six nonsingular positions of the mask.  At color
(c), the correction on edge (01) is

\[
       I\cdot(-2I)+I\cdot I=-E_{cc},                  \tag{20}
\]

where (20) means the corresponding two outer products of the (c)-th rows.
It cancels the standard block (E_{cc}), so (16) holds.  The same calculation
with (c)-th columns proves the transposed core equation.

Moreover, rows (0,1) are supported only at sites (3,2), respectively.
Consequently (q_{\mathrm{eff}}p_{0,x}p_{1,y}) sees only the already-zero
block ((q_{\mathrm{eff}})_{01}), and vanishes for all nine cells, not only
the erased eight.  The transposed assertion also holds for all nine cells.

This is not asserted to satisfy the full eight-site target equations.  It is
an exact countermodel to any proof using only the two shorewise core-edge
conclusions and their erased sectors.  The minimal residual is therefore:

\[
 \boxed{\text{derive and use at least one additional constant-cell or mixed
 sector identity.}}                                   \tag{21}
\]

## 6. Exact audit

Run

```text
python computations/verify_two_k4_opposite_regular_core_edge.py
```

The checker verifies:

1. the exact rank-(9), nullity-(45) literal-zero kernel (10), with the
   five residual edge blocks supported literally;
2. the nine-dimensional core-column rank increment in all (729)
   simultaneous rank normal forms;
3. eighteen exact unrelated-basis specializations;
4. all (729) coefficients of the sector identity (15) on a rank-two
   realization of (11); and
5. both shorewise all-nine-cell cancellations in the exact countermodel
   (19).

Its output is

```text
opposite-regular literal-zero kernel: rank 9, residual dimension 45
opposite-regular normal forms: 729 core projections of dimension 9; ...
opposite-regular unrelated-basis audits: 18 exact cases
displayed ten-position 2/4-cross sector identity: 729 coefficients
literal-zero two-shore core-sector countermodel: PASS
```
