# Every anchor hybrid has a physical Cartan rectangle to the pure target

## Result

Let a selected pure-`i` matching `mu` contain a physical edge `xy`, and
replace its pure cell on that edge by a nonzero off-diagonal cell with endpoint
colours `a,b`, `a!=b`.  Its complete mixed word is

\[
                            z=(a,b,i,\ldots,i).          \tag{1}

At every even order `N>=6`, the occurrence `(mu,z)` belongs to a
source-provenant physical Cartan rectangle whose other word is the pure
target word `i^N`:

\[
     (\mu,i^N)-(\mu,z)-(s\mu,i^N)+(s\mu,z).            \tag{2}

Here `s` transposes sites on two distinct complementary edges of `mu`.
All four labelled corners are distinct and have coefficients `+1,-1,-1,+1`.

Checker:
[`verify_uniform_hybrid_to_pure_cartan_rectangle.py`](../computations/verify_uniform_hybrid_to_pure_cartan_rectangle.py).

## Construction

Use independent local Weyl elements at `x` and `y`, sending `a` and `b`
respectively to `i`.  Their product `w` sends (1) to `i^N`.  Choose `p,q`
on two different complementary matching edges and put `s=(p q)`.  Since
`p,q` are residual sites, both have colour `i` in (1) and in `i^N`; hence
`s` fixes both words.  But it switches two matching edges, so

\[
                           s\mu\ne\mu.                 \tag{3}

The principal boundary `(1-s)(w-1)` is exactly (2).

Independent local colour actions are physical source symmetries: every
perfect matching has one incident edge at each acted-on site.  The target
defect of `w` is invariant under the disjoint transposition `s`, because the
two transposed sites remain monochromatic.  Thus endpoint oddization kills
the target defect and (2) is a genuine physical Cartan prism in the complete
principal-parts source resolution.

## Component consequence

Let a fine-label-saturated critical component contain `(mu,z)`.  The other
three corners of (2) have literal labels.  Therefore either

1. one lies outside the component and is a typed word-changing/matching
   exit; or
2. the complete component also contains the two pure-target corners.

This is stronger than merely knowing that some Cartan connector projects
nontrivially: every anchor-hybrid component is connected by a physical
four-corner interference pattern to its own pure target colour.

It also identifies the remaining dark-potential issue.  If the complete
lift residual `R=G-Cy` is nonzero, saturation makes it a typed exit.  If it
vanishes, the potential has canceled a target-touching rectangle and must be
promoted either to an occupied anchor-safe kernel move or to the complete
augmented generator/annihilator alternative.  Bare matching holonomy alone
cannot make that promotion.

## Scope

The theorem does not assert that keeping the pure corners forces a nonzero
Schur charge, nor that a zero complete residual consists of occupied scalar
cells in one endpoint row.  It removes the possibility of a physically
isolated anchor-hybrid component and supplies the precise target boundary
which any terminal dark component must cancel.

## Verification

```text
python3 computations/verify_uniform_hybrid_to_pure_cartan_rectangle.py
python3 -O computations/verify_uniform_hybrid_to_pure_cartan_rectangle.py
python3 -I -S computations/verify_uniform_hybrid_to_pure_cartan_rectangle.py
```

Frozen ledger SHA-256:

```text
45a1bf5e123e97920a6da56cef8476172d4a396002cd4bfce7d7de76164fe93b
```
