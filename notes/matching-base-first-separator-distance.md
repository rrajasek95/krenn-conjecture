# A first unjoined matching base is one chordless alternating cycle

## Result

Fix one literal output word and one connected component `J` of already
certified typed matching-base exchanges.  Every vertex records the complete
source occurrence—row, word, endpoint ports, physical perfect matching, and
decorated tail—not merely its unlabelled matching.

For two physical perfect matchings define

\[
 \delta(M,N)=\sum_{C\subset M\triangle N}
                   \left(\frac{|C|}{2}-1\right),       \tag{1}
\]

where the sum runs over the alternating-cycle components.  Choose a nonzero
same-word occurrence `N` outside `J` and `M in J` minimizing `delta(M,N)`.
Then:

1. `M triangle N` is one alternating cycle;
2. if that cycle has length at least six, no supported same-word
   distance-three shortening chord can occur; and
3. consequently the first separator is either a physical `C4` whose source
   typing has not been certified, or one chordless `C_(2r)`, `r>=3`.

This is the exact global-to-local topology reduction needed by the current
Theorem-A attack.  Its checker is
`computations/verify_matching_base_first_separator_distance.py`.

## Proof

Suppose `M triangle N` has at least two alternating components.  Switch one
proper component from `M` to `N`.  The resulting matching `K` uses only
decorated cells already nonzero in `M` or `N`, so its monomial is nonzero in
the same literal word.

If `K` belongs to `J`, then

\[
                         \delta(K,N)<\delta(M,N).
\]

If `K` does not belong to `J`, then

\[
                         \delta(M,K)<\delta(M,N).
\]

Either inequality contradicts the chosen pair.  Hence there is one cycle.

Write it in the standard form

```text
M = 01 | 23 | 45 | ...,
N = 12 | 34 | 56 | ... | (2r-1)0.
```

If the decorated chord `03` is supported in the same word, the matching

```text
K = 03 | 12 | 45 | 67 | ...
```

has `M triangle K=C4` and `K triangle N=C_(2r-2)`.  According as `K` is in
`J` or outside it, one of these two smaller distances contradicts
minimality.  Thus the first long separator is chordless relative to the
supported same-word inventory.

The proof is valid at every order.  The checker freezes the complete `h=3`
and `h=4` topology counts and audits component switching and the shortening
formula through `C20`.

## What this eliminates

No new graph census is needed to reduce multiple alternating components or
supported long-cycle chords.  The topological part of the proposed
connectivity induction is therefore easy.  The first hard steps are source
typing and transgression selection:

1. At `delta=1`, a physical `C4` is not automatically a certified exchange
   cell.  The opposite determinant orientation must retain the same
   decorated complementary tail in a complete source row.
2. At `delta=2`, a chordless `C6` is the first genuine topology.  The
   universal punctured-face functional has one pure-target term and three
   distinct mixed faces.  Those mixed faces can cancel the desired chord
   even when its pure monomial is nonzero
   (`h3-punctured-face-even-cycle-transgression-boundary.md`).
3. The committed silent-`C6` bright theorem closes one special fixed-port
   packet by private response words.  It does not yet select a
   transgression for a generic chordless `C6`.

Thus the next positive theorem should not be called a chord-existence
theorem.  It is a **source-labelled first-transgression theorem**: in the
full unary-plus-four-response packet, route or kill the three mixed faces of
one shortening base, or turn them into an off-anchor/Hall/lock witness.

## Scope guards

- Membership in `J` means connection by certified typed exchanges, not
  physical `C4` adjacency.
- Switching a whole component proves that a same-word matching monomial is
  nonzero; it does not manufacture an opposite determinant orientation.
- A chord is useful only when its decorated cell is supported in the same
  word.
- The lemma supplies no active-rank landing and no global termination
  potential after a carrier or Hall witness is produced.

## Verification

```text
python3 computations/verify_matching_base_first_separator_distance.py
python3 -O computations/verify_matching_base_first_separator_distance.py
python3 -I -S computations/verify_matching_base_first_separator_distance.py
```

Frozen ledger SHA-256:

```text
eccd682b613d3932f43d06b37d169c9173634962d47c6477fd172c1491078ba0
```
