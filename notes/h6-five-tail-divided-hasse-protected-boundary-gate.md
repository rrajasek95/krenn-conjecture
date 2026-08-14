# The (h=6) response deletion cell exists, but target and (q) do not promote it

## Verdict

The five-tail class from `8ec7f1c` has a canonical positive realization in
the **complete matching-response polynomial**.  For distinguished tail edge
`0`, set

\[
 \Theta_{0;ijk}
 =T_{ijk}+Q_{0ijk}^{0}-Q_{0ijk}^{1}+Q_{0ijk}^{2}.
\]

Then the primitive third simplicial/divided-Hasse deletion cell satisfies

\[
\begin{aligned}
 dK_0^{\rm del}
   &=\Theta_{0;234}-\Theta_{0;134}
     +\Theta_{0;124}-\Theta_{0;123}\\
   &=B_0.                                             \tag{1}
\end{aligned}
\]

Thus (B_0) is not an unexplained abstract Johnson relation.  It is the
ordinary oriented boundary of the deletion simplex on the four tail edges
complementary to `0`, corrected on each four-support by the three existing
pairwise Beck--Chevalley squares.

This does **not** yet give a physical `PP/AugP2` comparison cell.  The
complete target equations and the pointwise identity
\(q=M-a_{\rm inc}\) make (1) compatible with every checked protected row,
but they do not manufacture the operation-changing tensor
\(K_0^{\rm del}\otimes\Phi\) or force cross-face Hasse-linearity.  The exact
alternatives are:

- construct the normalized physical cell
  \(K_0^\Phi=(1/30)(K_0^{\rm del}\otimes\Phi)\), with
  \(dK_0^\Phi=(1/30)B_0\); or
- retain the terminal covector \(\chi(T_{123})=1\), zero on every other
  face and protected/label row, which evaluates \(-1/30\) on the requested
  normalized boundary.

Exact certificate:
[`verify_h6_five_tail_divided_hasse_protected_boundary_gate.py`](../computations/verify_h6_five_tail_divided_hasse_protected_boundary_gate.py).

## 1. Source-provenant deletion on the complete response

Take ten labelled tail sites and the complete hafnian

\[
                H_{10}=\sum_{M\in\operatorname {PM}(10)}q_M.
\]

It has (9!!=945) terms.  Fix the disjoint edges

```text
0=(0,1), 1=(2,3), 2=(4,5), 3=(6,7), 4=(8,9).
```

For every subset (S) of these five edges, restrict to matchings containing
(S) and delete the edges and their endpoints.  The result is literally the
complete hafnian on the remaining sites, every coefficient still one.  Its
term count by (|S|=0,\ldots,5) is

```text
945, 105, 15, 3, 1, 1.
```

The checker tests all 32 subsets and every deletion order.  All orders agree.
This proves the required coassociative deletion structure in the complete
matching-response species, not only on an isolated fixed monomial.

For a four-subset `0ijk`, the three order-interchange homotopies are exactly
the signed combination

\[
                    Q_{0ijk}^{0}-Q_{0ijk}^{1}+Q_{0ijk}^{2}.
\]

Adding it to the inherited triangle gives \(\Theta_{0;ijk}\).  The ordinary
oriented simplex formula

\[
 \partial[1,2,3,4]=[2,3,4]-[1,3,4]+[1,2,4]-[1,2,3]
\]

is precisely (1).  Its sixteen coefficients have gcd one.  Signed
relabeling gives five cells (K_a); their boundaries span rank four and
sum to zero, realizing \(\operatorname {sgn}\otimes\operatorname {Std}_5\).

This explains the earlier square-only rank jump.  An ordinary fixed-window
cube sees only the (Q) coordinates.  The primitive deletion simplex mixes
four inherited triangles with twelve squares and is therefore outside that
grammar while remaining canonical in the full deletion species.

## 2. Literal word/fine/repeated cancellation

The ten two-edge window objects retain the labels

\[
  w_W,qquad T_{W^c}q_{(v,W)},qquad
  (W;\text{ removed/reinserted }W^c),qquad P_3+K_2,
\]

with three labelled spectator (K_2) factors and the prolonged
`Phi` operation parent.  The boundary of every `T` or `Q` face is a cycle of
literal connectors between these window objects.

There are 30 connectors in \(J(5,2)\).  In \(B_0\), every connector occurs
exactly twice with opposite signs.  The executable ledger records, for all
30, its two endpoint words, its two fine labels, its removed/reinserted
edges, repeated labels, operation parent, and the two incident faces.  The
two contributions cancel in the **same** labelled connector.  No word,
fine, or repeated coarsening is used.

This is an exact labelled boundary statement conditional on the connector
being a physical `Phi` connector.  Equality of the requested labels does
not construct the still-missing operation-changing connector.

## 3. Complete target projection

The four literal words in this five-tail packet are

```text
01211222222222
01212212222222
01212222122222
01212222221222.
```

They all retain the mixed prefix `0121`.  Deleting any subset of the five
tail pairs leaves that prefix, so every one of the `4*32=128` restricted
words is mixed and its GHZ target coefficient is zero **before** word or
fine coarsening.

Conversely, each of the three pure length-14 target words remains pure under
all 32 tail deletions.  Hence the target is group-like on the pure sector.
The sum of the sixteen coefficients in (B_0) is zero; separately, its four
triangle coefficients and twelve square coefficients each sum to zero.
Thus the complete target projection of (1) is zero on both the literal mixed
packet and every normalized pure target.

## 4. Protected projections

Normalize the local comparison by \(\mu=1/30\).  The already certified cap
first-face signature is

\[
\begin{array}{c|rrrrrrr}
 &B&Eq&\text{target}&M&a_{\rm inc}&q&P_f\\ \hline
 &\mu&\mu&\mu&-\mu&-\mu&0&\mu,
\end{array}                                          \tag{2}
\]

and the transported cap/Cartan bridge signature is

\[
\begin{array}{c|rrrrrr}
 &\text{target}&q&a_{\rm inc}&\operatorname {ores}&W&\text{ridge}\\ \hline
 &-\mu&0&0&\mu&-\mu&\mu.
\end{array}                                          \tag{3}
\]

Tensoring a **natural** normalized `Phi` with the deletion cell transports
these values constantly across the sixteen faces.  Since
\(\sum_f(B_0)_f=0\), the alternating projections of

```text
B, Eq, target, M, ainc, q, P_f, ores, W, ridge
```

all vanish exactly.  In particular, (q=0) termwise in (2), not merely
after summing.

Equations (2)--(3) are conditional physical readouts: the cap and Cartan
rows are certified, but their placement on the response-to-cap `Phi` is the
open local theorem.  The calculation proves that no new scalar obstruction
appears at (h=6) once natural `Phi` exists.

## 5. Why target plus (q=M-a_{\rm inc}) is not enough

The (q) identity is pointwise.  It does not relate different `T/Q` faces.
For example, assign

\[
 M=e_{T_{123}},\qquad a_{\rm inc}=0,
 \qquad q=M-a_{\rm inc}=e_{T_{123}}.
\]

This satisfies (q=M-a_{\rm inc}) on every face and changes no target row,
but

\[
                     \langle B_0,q\rangle=-1.        \tag{4}
\]

Thus complete target plus the (q) definition does not imply the required
cross-face Hasse identity.  Natural deletion covariance of (M) and
(a_{\rm inc}), or equivalently the physical cell itself, is additional
input.

## 6. Exact filler-or-terminal alternative

Use the 25 literal `T/Q` face coordinates and append every protected,
word, fine, repeated, and operation row.  Make the deliberately stronger
grant of arbitrary unit fillers on **every** augmented coordinate except the
literal `T123` `Phi`-presentation face.  The resulting ranks are

```text
augmented row dimension                              64
strong grant rank                                    63
rank after adjoining (1/30)B0                        64.
```

The unique displayed detector is

\[
 \chi(T_{123})=1,
 \qquad \chi=0\quad\text{on every other face and external row}. \tag{5}
\]

It kills all ordinary cube/square directions, all complete target and
pointwise (q) corrections, and arbitrary `B/Eq/W/ores/ridge` and label-row
corrections.  Yet

\[
                      \chi((1/30)B_0)=-1/30.         \tag{6}
\]

Therefore an objectwise target or protected correction cannot be the
filler.  The shortest positive datum is one triangle-bearing normalized
cell (K_0^\Phi).  Signed (S_5)-naturality supplies the other four
instances and their single sum relation.

## Scope

The coefficient deletion cell is constructed in the complete ten-tail
matching response.  The word/fine/repeated boundary, complete GHZ target,
and conditional normalized protected projections are exact.  The result
does not construct the source-labelled response-to-cap `Phi`, prove that
`PP/AugP2` is a module over this higher deletion cell, or complete the
separate 945-tail matching-cover descent.  Consequently (1) is a positive
source-side construction and (5) is the exact terminal alternative for the
current physical comparison grammar.
