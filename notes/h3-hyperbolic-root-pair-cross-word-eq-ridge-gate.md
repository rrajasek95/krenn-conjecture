# The paired root transport first fails on word placement, then on mixed reduced Eq

## Verdict

The local Pfaffian `SL3` root squares, the response `D4` cube, the signed
Weyl telescope, and the flat cap graph do **not** construct a physical map

```text
11:110000  ->  01211222
```

for either hyperbolic return.  Their coefficient shadows are compatible,
but their source idempotents are not: `D4` and signed Weyl preserve the
operation matching, matching index, repeated-edge label and second-Hasse
direction tag, while the cap graph is a spectator in a separate
word/fine/repeated grade.

There are also two already certified obstructions before this word map:

1. each incomplete root on the complete response leaves a signed `24`-term
   collision splitter in a `45`-term missing/doubled sector;
2. after granting those four response-naturality cells, the two root
   squares contribute the same unary order defect, hence
   `2*q01*H2345`, not zero.

After granting both earlier faces, the forward lower cofactor still has the
unavailable `DSQ` operation type.  After additionally granting that lower
type and the degree-zero word/fine section, the first augmented obstruction
is the **mixed reduced-Eq naturality-square incidence**.  The shifted ridge
is a second, independent obstruction after that mixed cell is supplied.

Pairing the two roots cancels neither one.

Exact checker:
[`verify_h3_hyperbolic_root_pair_cross_word_eq_ridge_gate.py`](../computations/verify_h3_hyperbolic_root_pair_cross_word_eq_ridge_gate.py).

## The `24`-term residual is not a Weyl marginal

This comparison can be made on literal operation monomials.  The signed
Weyl telescope is matching-constant and remains on the `105` squarefree
perfect-matching coordinates.  The four complete collision rows occupy four
disjoint `45`-coordinate missing/doubled sectors.  Thus the combined literal
space has

```text
105 + 4*45 = 285 coordinates.
```

The telescope marginal together with the four symmetric collision rows has
rank `5`.  Adjoining the four signed `24`-term root residuals raises the rank
to `9`.

For root `i`, let `R_i` be its residual and put

\[
                         \lambda_i=R_i/24.
\]

Then exactly

\[
 \lambda_i(\text{Weyl matching constant})=0,
 \qquad \lambda_i(C_j)=0,
 \qquad \lambda_i(R_j)=\delta_{ij}.                 \tag{1}
\]

So the answer is unambiguously:

```text
the 24-term collision residual is a pure-Weyl/Cartan marginal: NO;
it is operation-idempotent disjoint and centered inside its collision sector.
```

The local Pfaffian identity does not contradict (1).  It is a genuine
symmetry of the signed operation `K4`; (1) appears when that six-coordinate
root is inserted into the complete unsigned `105`-matching response without
the omitted cross-edge root directions.

## The degree-zero word section is absent

In full augmented-site order `(P,S,0,1,2,3,4,5)`, the response and cap words
are

```text
response  11110000 = 11:110000
cap       01211222.
```

They differ at sites `P,0,2,3,4,5`, a Hamming distance of six.  The known
response path is

```text
110000  ->  111111  ->  112112
   D4          tail Cartan/Weyl,
```

whereas the cap multiplier has letters `(2,1,1,2)` at the four `D4` sites.
The literal `0 -> 1` `D4` action therefore does not even start on the cap
object.  The endpoint transpose completes an associated-symbol half, but
moves the repeated component from `Lambda` to a disjoint `Lambda^T`.

The flat cap theorem only says that a cap copy, once physically placed at a
vertex, has no further curvature or holonomy.  Declaring such a copy at
every response vertex is the enriched tensor model, not a physical
cross-word section.

In the primitive two-word quotient retain response/cap coordinates for each
root.  The old block-diagonal inventory has cross-word rank `0`; one paired
diagonal arrow has rank `1`; two root-labelled arrows have rank `2`.
Hence a paired cell could carry one diagonal section, but rootwise
naturality still requires both labelled arrows.

## Conditional Eq-versus-ridge test

Now grant every earlier obligation as strongly as possible:

- all four `24`-term response splitters;
- the selected unary Cartan return;
- the missing forward `DSQ` lower cell;
- both response-to-cap word/fine/repeated sections;
- both `D4` private returns; and
- both clean central Koszul reduced-Eq edges.

For each root retain rows

```text
(R, E, kappa, gamma)
```

where `R` is the `D4`/private return, `E` is the clean reduced-Eq edge,
`kappa` is the mixed naturality-square incidence, and `gamma` is the shifted
ridge.  On two root labels the strongly granted base has rank `4`.

The required paired comparison has

```text
root 1: (1,1,1,0)
root 2: (1,1,1,0).
```

Its sum raises the rank

```text
4 -> 5.
```

The normalized diagonal mixed-incidence covector, with value `1/2` on each
`kappa` coordinate, kills all granted edges and reads `1` on this paired
comparison.  This is the same primitive mapping-square `H1` which is lost
when source idempotents are forgotten: coefficientwise `D4 + K_Eq` has the
right `(R,E)` shadow, but objectwise edge data do not supply the mixed
two-cell.

After granting the paired mixed cell, the two shifted ridge faces raise the
rank again:

```text
5 -> 6.
```

Their normalized diagonal detector likewise reads `1`.  Formal cap/ridge
flatness proves zero mixed curvature and fixes the connection face
`-d(q_xv^01)`; it does not put either labelled `gamma` into the cap source
module.

If the two mixed cells and two ridge faces are kept rootwise rather than
only diagonally, the ranks are

```text
base 4 -> mixed 6 -> full mixed+ridge 8.
```

## Why pairing cannot cancel

In the labelled module the two `kappa` coordinates and the two `gamma`
coordinates are independent.  Every sign choice `(+-1,+-1)` therefore
raises the mixed rank from `4` to `5` and the subsequent ridge rank to `6`.

Forgetting the root label does not help the orientation that constructs
`z`.  The two returns are

\[
                  A-B,\qquad A-C,
\]

with the same sign, so their sum is

\[
                 z=(A-B)+(A-C)=2A-B-C.              \tag{2}
\]

Under the same forgetting map the paired mixed-Eq coefficient is `2`, and
the paired ridge coefficient is also `2`, rather than zero.  Choosing
opposite signs could cancel an unlabelled face, but it changes (2) to
`C-B` or `B-C` and no longer fills the balanced class.

## Shortest remaining construction

The positive target is one root-labelled paired collision mapping
bicomplex which simultaneously contains:

1. the four response collision splitters and their unary-order coherence;
2. the forward `DSQ` and reverse `PQQ` proper faces;
3. two physical `11:110000 -> 01211222` word/fine/repeated arrows;
4. the diagonal mixed `K_Eq` two-cell; and
5. both shifted ridges with their `-d(q_xv^01)` connection faces.

Only after items 1--3 exist is reduced Eq the first relevant augmented
test; only after item 4 exists does the ridge become first.  The existing
graphs solve all coefficient signs and formal curvature, but none of these
source placements can be inferred by composing their shadows.

## Scope

This is exact for the canonical `h=3` fixed-window root pair, the complete
`105`-matching response, all four `45`-term collision sectors, and the
committed D4/Weyl/cap/Koszul interfaces.  It is a conditional quotient
no-go for the paired cancellation, not an all-resolution or all-`h` no-go.

Run normally, optimized, and isolated/no-site.  Frozen ledger SHA-256:

```text
af131bf8e657a0ba49cf2a8a0fb8f109698ea239e2d76408551117d4a29efb51
```
