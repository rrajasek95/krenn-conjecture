# Doubly-good curved OO overlap survives two diagonal anchors

## 1. Outcome

Adding one differently labelled diagonal anchor to the
[`one-anchor OO counterguard`](oo-doubly-good-one-anchor-counterguard.md)
still does not close the overlap.  There is an integral eight-site packet
with

* matching tensor exactly `X_0+X_2`;
* all six off-diagonal rows equal to zero in every pair chart;
* rank-one OO arms with distinct heads `0,1`;
* four good-star ranks `(3,3,3,3)`;
* nonzero curvature `kappa=-1`; and
* complete target-`2` right-ruling alignment in both charts.

It fails only the third diagonal target `X_1`.  Therefore even two
differently labelled diagonal rows, all off-diagonal rows, doubly-good OO
provenance, curvature, and the common alignment ledger do not imply a dark
cut or the missing target.  The complete three-diagonal sector is genuinely
indispensable on this route.

This is not a ternary source or a Krenn counterexample; it is an exact
two-colour source embedded in the ternary aggregate space.

## 2. Alternating cycle plus forbidden shore triangle

Label the vertices cyclically by `0,...,7` and put

\[
                         p=0,\qquad q=2,\qquad r=4.          \tag{1}
\]

On the four cycle edges

\[
                  01,\ 23,\ 45,\ 67                         \tag{2}
\]

put `E_00`, and on

\[
                  12,\ 34,\ 56,\ 70                         \tag{3}
\]

put `E_22`.  The alternating cycle has exactly its two colour-class
perfect matchings, giving `X_0+X_2`.

The vertices `0,2,4` lie in one bipartition shore.  Add the three cells

\[
                  A_{02}=E_{10},\qquad
                  A_{04}=E_{11},\qquad
                  A_{24}=E_{11}.                            \tag{4}
\]

No perfect matching can use an edge internal to one shore unless it also
uses an edge internal to the opposite shore.  There are no such opposite
shore edges, so every cell in (4) is globally matching-forbidden.  It can
alter local ranks and curvature but cannot change the tensor.  Hence

\[
                              H_8(A)=X_0+X_2.                \tag{5}
\]

This is the clean combinatorial reason all mixed rows remain zero; no
coefficient cancellation or genericity is involved.

## 3. OO structure

The first two cells in (4) are rank-one outgoing arms at `p=0`, with
heads `0` at `q=2` and `1` at `r=4`.  After either arm is deleted, the two
cycle neighbours supply endpoint rows `0,2`, while the other shore-triangle
edge supplies row `1`.  The opposite endpoints have the same structure,
using `A_24` for their missing row.  Thus all four deleted-star maps are
injective.

Choose the fourth site `3`.  Its cycle blocks are

\[
                         A_{23}=E_{00},\qquad A_{43}=E_{22}.
\]

With shared `p`-row `1`, the curvature coefficient is

\[
 A_{02}(1,0)A_{43}(1,0)-A_{04}(1,1)A_{23}(0,0)
                         =0-1=-1.                           \tag{6}

For target `2`, every local `pq` wedge matrix is zero.  In the `pr` chart
the sole nonzero wedge is at site `q`, and it lies in column `1`, the right
head of `A_pr`.  Hence all six residual sites belong to the appropriate RR
alignment set in each chart.

## 4. Consequence for the full-nine gate

Equation (5) satisfies the complete `00` and `22` tensor rows and all six
off-diagonal rows.  It disproves any proposed two-anchor transport identity
derived only from the currently forced OO rank/alignment/curvature data.
The smallest honest local target is no longer a proper row subset: it must
use all three diagonal anchors together with the off-diagonal provenance.

This matches the complementary older guards from the other direction:
discarding all off-diagonal rows leaves a three-anchor curved packet, while
discarding even one diagonal label now leaves the present curved OO packet.
The exact remaining lemma is therefore genuinely **full nine**, not
seven- or eight-row.

## 5. Reproduction

```sh
python3 computations/verify_oo_doubly_good_two_anchor_counterguard.py
python3 -O computations/verify_oo_doubly_good_two_anchor_counterguard.py
```

The checker enumerates all 105 physical perfect matchings and all endpoint
colour choices, verifies that exactly the two alternating matchings survive,
then audits both direct heads, all four star ranks, the literal curvature
minor, and every target-`2` RR wedge matrix.
