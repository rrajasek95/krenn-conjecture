# Hybrid-to-pure Cartan rectangles cancel in the complete source row

## Result

Let a selected pure-`i` matching `mu` contain a physical edge `xy`, and
replace its pure cell on that edge by an off-diagonal cell with endpoint
colours `a,b`, `a!=b`.  Its mixed word is

\[
                         z=(a,b,i,\ldots,i).            \tag{1}
\]

For every even `N>=6`, the occurrence `(mu,z)` has a four-corner Cartan
rectangle with the pure target word `i^N`:

\[
       (\mu,i^N)-(\mu,z)-(s\mu,i^N)+(s\mu,z).          \tag{2}
\]

But (2) is not an independently available physical source row.  In the
complete matching sum, the transposition `s` permutes all perfect matchings,
and every rectangle cancels with its transposed mate.  The full degree-zero
boundary is zero.

Checker:
[`verify_uniform_hybrid_to_pure_cartan_rectangle_cancellation.py`](../computations/verify_uniform_hybrid_to_pure_cartan_rectangle_cancellation.py).

## Occurrencewise construction

Use independent local Weyl elements at `x,y`, sending `a,b` respectively to
`i`; their product sends (1) to `i^N`.  Choose `p,q` on two different
complementary matching edges and put `s=(p q)`.  Both sites are residual and
have colour `i` in both words, so `s` fixes `z` and `i^N`, while
`s mu != mu`.  The four labelled corners in (2) are therefore distinct.

Independent local colour actions are physical source symmetries, and the
target defect of their product is invariant under the disjoint
transposition.  Endpoint oddization thus makes the **sum** of these
rectangles a physical Cartan cycle in the principal-parts source resolution.

## Complete-row cancellation

For fixed `s`, the map `mu -> s mu` permutes the entire perfect-matching set.
Summing (2) gives

\[
 \sum_\mu[(\mu,i^N)-(\mu,z)-(s\mu,i^N)+(s\mu,z)]=0.  \tag{3}
\]

The checker verifies (3) for every exceptional-site pair, residual
transposition, and ordered ternary hybrid decoration at orders six and
eight.  Thus selecting only the rectangle through a marked occurrence would
project a complete physical cycle to a partial matching sum; it would not
construct a source generator.

## Component consequence

Projecting (3) to a proper matching component can expose a boundary across
the component cut.  That projected boundary becomes physical exactly when a
chain projector or complement primitive splits the complete Cartan cycle in
the augmented source resolution.  This is the component-splitting gate
already isolated by the Cartan placement and dark-potential theorems.

The result therefore rules out the tempting shortcut

```text
one target-touching occurrence rectangle => typed component exit.
```

It does not obstruct asymmetric placements where the endpoint transposition
changes the source word: those have a nonzero complete-row projection and
give the valid marked-component placement theorem.  Nor does it obstruct a
genuine higher component splitter.

## Verification

```text
python3 computations/verify_uniform_hybrid_to_pure_cartan_rectangle_cancellation.py
python3 -O computations/verify_uniform_hybrid_to_pure_cartan_rectangle_cancellation.py
python3 -I -S computations/verify_uniform_hybrid_to_pure_cartan_rectangle_cancellation.py
```

Frozen ledger SHA-256:

```text
318a56ddb051b910ebab2cd3669ef1f167f266761cefb8cbb9c7a27a7adfb78e
```
