# Anchor hybrids either reselect to goodness or form a finite interference cycle

## Result

Fix selected pure matchings `Q_0,Q_1,Q_2` in an exact ternary source, and
let `e=uv` carry a nonzero off-diagonal cell `x_e^(a,b)`, `a != b`.  Suppose
the physical pair `e` belongs to at least one `Q_i`.

For every such colour `i`, split the complete hybrid zero row according to
whether its matching retains `e`:

\[
       0=G_{w_i}=x_e^{a,b}H_e^i+O_e^{a,b}.             \tag{1}
\]

The corresponding pure target row is

\[
       1=x_e^{i,i}H_e^i+P_e^i.                         \tag{2}

Here `H_e^i` is the all-`i` hafnian on the other sites, `O_e` is the sum of
mixed matchings omitting the physical pair `e`, and `P_e` is the analogous
pure avoiding sum.

There is an exact alternative.

1. If `O_e=0` for every selected colour whose matching uses `e`, then (1)
   gives `H_e^i=0`, and (2) gives `P_e^i=1`.  Reselect a nonzero pure
   matching omitting `e` in every such colour.  The physical pair `e` is now
   outside all three selected anchors and enters the rank-`(3,3)` nonanchor
   active route.
2. If some `O_e != 0`, one nonzero omitting matching contains a new
   off-diagonal endpoint arm on a physical pair `f != e`.  If `f` is outside
   `Q_0 union Q_1 union Q_2`, it is rank-good.  Otherwise repeat the hybrid
   split at `f`, keeping the selected pure matchings fixed.

The fixed anchor union has at most `3N/2` physical pairs and each pair has
six ordered ternary off-diagonal decorations.  Therefore bright propagation
either exits to a good pair or repeats an actual decorated anchor cell after
at most `9N` strict moves.  In the latter case the complete source rows give
a literal anchor-contained interference cycle.  This proves occurrence and
finite component entry without a `C4/C6/C8` support census.

Checker:
[`verify_uniform_anchor_hybrid_propagation_cycle.py`](../computations/verify_uniform_anchor_hybrid_propagation_cycle.py).

## 1. The retain/omit equations are coefficient-exact

In the hybrid word, sites `u,v` have colours `a,b` and every other site has
colour `i`.  A matching retaining `uv` uses the fixed cell `x_e^(a,b)`;
the remaining matching is entirely in colour `i`.  Summing all such terms
gives the first product in (1).  Every other matching belongs to `O_e`.
The pure row partitions identically, giving (2).

No termwise noncancellation is assumed.  If the aggregate `O_e` vanishes,
the nonzero mixed cell forces `H_e^i=0` numerically at the exact source.
Then `P_e^i=1`, so at least one literal pure avoiding monomial is nonzero.

## 2. A bright avoiding mate always changes the off-diagonal pair

Take a nonzero term of `O_e`.  It pairs `u` and `v` away from one another.
The incident cells have endpoint colours `(a,i)` and `(b,i)`.  Since
`a != b`, at least one differs from `(i,i)` and is off-diagonal.  Its
physical pair is not `e` because the matching omits `uv`.

If one of `a,b` equals `i`, every avoiding matching has exactly one such
off-diagonal arm.  If neither equals `i`, it has two.  The exact `N=8`
audit reconstructs all `28*3*6*90` edge/colour/matching records and freezes
the `1/2`-arm split.  This census only checks the uniform sentence; the
proof is the endpoint-colour observation.

## 3. Why the process terminates in a component

On a bright step no pure matching is reselected, so the physical anchor
union remains fixed.  Each step either leaves that union or moves to another
one of its at most `9N` ternary decorated off-diagonal cells.  A longer walk
repeats the full decorated-cell state, not merely its physical pair.  Every
directed step is source-labelled by the actual hybrid complete row and an
actual nonzero omitting monomial.

The repeated-pair branch is not yet declared a binomial cycle.  Complete
rows can have further matching terms.  After private terms are peeled, the
reachable finite row/matching hypergraph contains a critical component.  Its
odd signed holonomy gives a source unit.  On coherent even holonomy, the
rank-one adjugate theorem reduces the component to the anchor and physical
Cartan amplitudes; a dark Cartan amplitude is an exact internal potential.

Thus the remaining source theorem is now precisely:

> lift a component-exact potential to a same-row support dependence, or use
> one of its contaminating complete-row terms to enlarge/leave the component.

There is no longer a separate theorem asking whether the selected
off-diagonal cell occurs in a useful source row or whether a longer even
cycle is reachable.

## 4. Relation to minimum support and rank landing

The dark reselection branch changes only the chosen pure matching witnesses;
it does not modify the source.  Once `e` is absent from all selected
matchings, their three pure coordinate heads survive deletion of `e` at
both endpoints, so the pinned nonanchor theorem applies.

The bright exit likewise supplies an off-diagonal cell, not automatically a
clean cap.  The generic active-minor route can still have a same-head
`(2,2,3,3)` profile.  Transverse physical landing remains downstream of the
present source-exhaustivity theorem.

## Scope

The argument is valid for every even order and arbitrary complex weights,
endpoint asymmetry, and aggregated parallel sources.  A repeated physical
pair produces a finite literal source component, but the theorem does not
force that component to be binomial, give it nonzero Fitting holonomy, turn
its exact potential into deletion, or produce an active clean overlap.

Run:

```text
python3 computations/verify_uniform_anchor_hybrid_propagation_cycle.py
python3 -O computations/verify_uniform_anchor_hybrid_propagation_cycle.py
python3 -I -S computations/verify_uniform_anchor_hybrid_propagation_cycle.py
```

Frozen ledger SHA-256:

```text
daf610c29166befd149168a497061175a70e93e466493aa69de5a69d711f7137
```
