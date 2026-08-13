# Cut-swap support tail lift and the shared-loop gate

## Result

On the normalized canonical (h=3), faces-((3,5)), repeated
(P_3+K_2) component, the cut-swap lower packet has a source-valid shifted
site-collapse realization on all twelve of its nonzero physical collision
labels.  After the forced rational normalization it lands on the literal
360-feature aggregate

\[
                 B_0+B_2-B_3-B_5.
\]

This is exactly an `alpha=(-1,+1,+1,-1)` four-corner boundary in the order
`(5,0,2,3)`.  Together with the already constructed endpoint-odd Cartan
ridge, it is the literal output-side (M_v=-O_\alpha+K).

The same construction cannot extend to all fifteen physical collision
labels inside the natural one-double-fibre site-collapse class.  All three
shared labels contain the repeated edge (02), and every successful support
map identifies source sites (0,2) at target site (4).  Their image would
therefore contain the forbidden coefficient loop (44).  The shared packet
is one fixed \(\rho\)-label and one \(\rho\)-pair.  Thus the smallest missing
interface is exactly two equivariant shared-loop repair images.

## Canonical target symmetry

The complete faces-((3,5)) fine degree has 288 full-nine columns and six
pure multiplier columns.  Forgetting decorations, their graphs in the
checker order are

```text
0: 12 34 45
1: 13 24 45
2: 14 23 45
3: 14 24 35
4: 14 25 34
5: 15 24 34
```

Exhausting every site permutation and every global colour permutation that
preserves the complete fine degree, the direct-free pair, and these six
physical multipliers gives four automorphisms.  The optional endpoint swap
acts trivially on this inventory.  The only nontrivial odd-site action is

\[
                    s=(2\ 5),
\]

which acts on the pure multiplier indices as

\[
                    (0\ 5)(2\ 3),
\]

with 1 and 4 fixed.  Hence the odd four-multiplier direction is not chosen
ad hoc: it is selected by the physical target grade.

## Twelve-label construction

Let `rho=(1 4)` on the six collision sites and let the signed lower be the
`024-only` labels minus the `012-only` labels.  There are fifteen physical
labels, three shared labels, and twelve labels in this signed support.

Enumerate every surjection

\[
        \phi:\{0,\ldots,5\}\longrightarrow\{1,\ldots,5\}
\]

with one double fibre, all other fibres singleton, and

\[
                    \phi\rho=s\phi.
\]

Exactly four maps take every one of the twelve support matchings to one of
the six pure multiplier graphs:

```text
(4,2,4,1,5,3)
(4,2,4,3,5,1)
(4,5,4,1,2,3)
(4,5,4,3,2,1)
```

Their signed pushforwards are

\[
       \pm 2(B_0+B_2-B_3-B_5).
\]

Over the physical rational coefficient field, multiplying the chosen
orientation by (1/2) gives

\[
       a=(1,0,1,-1,0,-1).
\]

The target involution sends (a\) to (-a).  The four selected complete
full-nine boundaries are disjoint 90-feature rows, so the boundary has
exactly 360 literal decorated seven-edge features.  It is the corner order
`(5,0,2,3)` with coefficients `(-1,+1,+1,-1)`.

Also

\[
                     \sum_j a_j=0.
\]

Consequently the pure (r_0) target and physical `ainc` rows cancel.  The
old-cap tail has no `W` or `D` output, while the reduced-Eq corners retain
the stated alpha coefficients.  The physical Cartan term (K) then cancels
ordinary residue and supplies the eta/sigma terminal ridge, as proved by the
literal (M_v=-O_\alpha+K) theorem.

## The exact extension obstruction

There are no equivariant one-double-fibre maps that lift all fifteen labels.
For each of the four support maps,

\[
                     \phi(0)=\phi(2)=4.
\]

The three shared labels all have repeated edge (02).  Their other two
edges map to one of

```text
12+35, 13+25, 15+23,
```

but in every case the third edge is (44).  Such a loop is absent from the
physical coefficient algebra and from every pure multiplier graph.

Nor can the shared labels simply be sent to zero.  Forgetting their repeated
edge sends them to three distinct unit matching coordinates.  A zero
extension would therefore fail even the occurrence-shadow chain square.

Under \(\rho\), the three shared labels split as one fixed orbit and one
two-element orbit.  A full physical comparison needs only:

1. one image for the fixed shared label;
2. one image for a representative of the shared pair, with its mate forced
   by equivariance.

The correct next source type is thus a diagonal/loop-resolution relative
cell with these two image directions and zero protected output.  This is the
whole remaining Gate-I input problem in this construction.

## Scope

This result constructs the desired map on the signed twelve-label packet and
proves a minimal obstruction within the one-double-fibre site-collapse
class.  It does not exclude an arbitrary linear or relative comparison on
the shared labels, and it does not claim a general-(Y) or inactive-grade
extension.

## Verification

Run:

```text
python3 computations/verify_h3_cut_swap_support_tail_lift_shared_loop_gate.py
python3 -O computations/verify_h3_cut_swap_support_tail_lift_shared_loop_gate.py
python3 -I -S computations/verify_h3_cut_swap_support_tail_lift_shared_loop_gate.py
```

Frozen ledger digest:

```text
8c255624f436b4685df302b0237855fc3b1156731235a322f5c07bc40828fefb
```
