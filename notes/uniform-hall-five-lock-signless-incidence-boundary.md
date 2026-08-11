# Common-provenance opposite locks form a signless incidence module

## Conditional closure theorem

The sole `M3` interface in `f127fd7` has a finite exact closure once its
opposite crossed companions have literal common matching provenance.

Group the lock columns by their common nonzero matching tail.  Assume each
such complete coefficient contains exactly two opposite lock columns with
the same cofactor and no additional term.  After localizing that cofactor,
the row is

\[
                            z_u+z_v=0.                \tag{1}
\]

Let `G` have one vertex for each lock column and one edge for each row (1).
The full critical block is the signless incidence matrix of `G`.

For every connected component there are exactly two outcomes.

1. If `G` is bipartite, assign signs `+1,-1` on its two parts.  The
   resulting vertex vector lies in the exact lock kernel, because every row
   sees `+1-1=0`.  The same-star square-zero theorem makes this a finite
   source switch, and entry-minimality scales it to delete a blocker.
2. If `G` is not bipartite, choose an odd cycle.  Alternately add and subtract
   its rows.  Every intermediate column cancels and the root column occurs
   twice:

   \[
       (z_0+z_1)-(z_1+z_2)+\cdots +(z_{2r}+z_0)=2z_0. \tag{2}
   \]

   The lock pivot `z0` is already localized and nonzero.  Over the complex
   source field, (2) is an ordinary source unit.

Thus a common-provenance critical component cannot remain both injective
and unit-free.

Checker:
`computations/verify_uniform_hall_five_lock_signless_incidence_boundary.py`.

## Exact role of entry-minimality

The graph theorem supplies the datum missing in the prior argument.  On a
bipartite component it explicitly constructs a vector in the kernel of all
five complete rows.  Because the participating directions share the same
physical star, their square is zero and the switch is exact.  Only then is
entry-minimality invoked to remove one nonzero blocker.

This avoids the invalid inference “minimum support implies a kernel.”  The
kernel comes from the signless incidence structure; minimum support only
turns it into a contradiction.

## What common matching provenance must mean

The hypothesis is coefficient-level, not merely graph-theoretic.  For each
edge of `G`:

* the two columns must occur in one literal full-output coefficient;
* their remaining source matching must be identical;
* hence their cofactor multiplier and sign must agree; and
* no third lock column or unmatched source term may occur in that coefficient;
  and
* a bipartite component used for descent must lie in one physical same-star
  switch space, so the alternating direction has square zero and its finite
  source change is exactly linear.

The checker freezes two sharp counterguards.

* A signless four-cycle has the alternating kernel `(1,-1,1,-1)`.  Adding
  one unmatched row `[1,0,0,0]` raises the rank from three to four and kills
  that kernel.
* Replacing one row `[1,1,0,0]` by `[1,2,0,0]` also raises the rank to four.
  The physical incidence is unchanged, but unequal tail weights destroy the
  signless relation.

Therefore “opposite companions exist” is insufficient.  Their exact common
matching class and the absence of extra columns are load-bearing.

## Interface with the two new landing theorems

When the common-provenance hypothesis fails in a controlled way, two routes
are already certified.

* A new endpoint/direct cell carrying the missing anchor label enters the
  finite two-shared-anchor migration of `07a1f02`; it yields reselection, an
  off-anchor escape, a unit, or the pure third-colour direct label.
* The canonical pair of opposite third-colour companions enters `242a91c`;
  it repairs all four deleted-star ranks and either invokes complete
  exchange or has a nonzero distinct-head transition minor.

The genuinely remaining `M3` obligation is consequently exact:

```text
prove that every unmatched full-row term is one of those two routed cells,
or prove that all residual opposite companions share the literal tail and
therefore form the signless incidence module above.
```

No physical full-row counterpacket violating that statement is known.  The
weighted and unmatched matrices are coefficient guards showing why the
common-tail audit cannot be skipped; they are not Krenn sources.

## Verification

Run

```text
python3 computations/verify_uniform_hall_five_lock_signless_incidence_boundary.py
python3 -O computations/verify_uniform_hall_five_lock_signless_incidence_boundary.py
python3 -I -S computations/verify_uniform_hall_five_lock_signless_incidence_boundary.py
```

The checker verifies cycle certificates of lengths `3,...,9`, connected
tree/cycle-with-tail representatives, and both sharp provenance guards.  The
proof for arbitrary connected graphs is the spanning-tree sign propagation
and odd-cycle identity above.

Frozen ledger SHA-256:

```text
fbbb3079756c1b7b163936715686ee5dffc5727f0ea87442f7db9e6efdea045d
```
