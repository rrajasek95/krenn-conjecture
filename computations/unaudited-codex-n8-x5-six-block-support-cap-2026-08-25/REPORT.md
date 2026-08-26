# Every six-added-block support closes under the formal guard

Status: **all 38,760 six-added-block supports are closed.**  Of these,
34,124 have an immediate fixed-identity triangle or star cap; 4,524 exact
guard reductions land in the sealed zero-through-five-block theorem; and the
remaining 112 supports have a direct nonidentity cap certificate.

## Exact six-load classification

For six additions chosen from the twenty off-family site edges, the complete
support census is

```text
C(20,6)                                      38,760
fixed identity triangle/star certificate    34,124
fixed identity structural evaders            4,636
```

Iterating the parent's unit-minor guard injections reduces the 4,636 evaders
by final added-support size as follows:

```text
size 2: 96,  size 3: 1,080,  size 4: 2,244,
size 5: 1,104,                         size 6: 112.
```

The first 4,524 cases are therefore inherited from an already closed layer.
The 112 stable supports form 57 exact orbits under `(1 2)(6 7)`: two singleton
orbits and 55 doubletons.

## General no-outside-edge criterion

For any support size, suppose no supported source edge joins cap site `6` or
`7` to an outside site `3,4,5`.  A response monomial of cap `67` on residual
pair `ab` uses one edge incident to `6` and one incident to `7`.  If `ab` is
not contained in triangle `012`, at least one of those source edges is
outside-cap-adjacent and is absent.  Therefore every forbidden response is
the zero polynomial for every `K`.

Exact classification shows that **all 112 stable six-block evaders satisfy
this general criterion**.  Their possible cap-`67` response edges are subsets
of `01,02,12`.

If `A67 != 0`, the response kernel is all nine-dimensional `M3`.  The three
diagonal activity failures and `<K,A67>=0` are four proper hyperplanes, whose
union cannot cover `M3(Q)`.  Constructively `K(t)_ij=t^(3i+j)` works for some
`t` in `1,...,9`.

If `A67=0`, every one of the 112 supports has a fixed-identity certificate at
maximal remaining variable support.  The exact support census is

```text
cap16/star: 60,  cap16/triangle: 48,  cap27/star: 4.
```

Taking `K=I3` gives `kappa=(1,1,1)` and cap pairing `3`; further zero
specializations only remove responses.  Thus every coefficient stratum is
active clean, with no response-minor elimination needed.

The audit includes a 257-sample exact rational replay covering all 112 stable
supports in both the nonzero- and zero-`A67` strata.  It uses neither pure-row
nor residual/source equations and reads no CEGAR or D12 artifact.

## Scope

Together with the parent chain, all zero-through-six-added-block layers are
closed under the formal guard.  The no-outside-edge criterion is valid at any
support size, but seven-or-more-block supports may contain complete switched
partner patterns and remain unclassified.  This is not the full support
dichotomy or a full-conjecture proof.

Parent manifest:
`119ec632645202f973c89c3381e85113a902c4066e627ba7c6d051fa729d49fb`.
