# Genus-two Kasteleyn/Pfaffian terminal crosswalk

Status: **UNAUDITED exact terminal no-go**.  The requested 16-Pfaffian survey
was already completed through the first two physical attachment layers.  It
is source-faithful as a wordwise rewrite, but Pfaffian Pluecker/Jacobi/BE
identities yield no new clean-pair or cofactor relation beyond the existing
Laplace/carrier rows.

## Exact expansion and deletion scope

The pinned cellular `K8` embedding has 16 triangular and two quadrilateral
faces, hence genus two.  Its four independent cocycles give 16 spin sectors.
The quadratic refinement has rank four and Gauss sum `-4`, so Fourier
inversion gives coefficients `c_eta=+/-1/4`.  Exact enumeration verifies

```text
haf(K8) = sum_eta c_eta Pf(K^eta)
```

matching by matching: all 105 resulting coefficients are `+1`.

Principal deletion is valid inside every Pfaffian sector, but it does not in
general descend through the same Arf aggregate.  Differentiating/deleting a
physical edge `e` twists the coefficient vector by its four-bit spin
character `ell(e)`.  In the pinned gauge 12 edges are trivial and 16 are
nontrivial, realizing nine distinct nonzero characters.  A nontrivial
character takes both signs on the sectors and is never proportional to the
original Arf vector.  Thus deletion is source-faithful without sector-resolved
equations only on the 12 trivial-character edges.

## First Pluecker/Jacobi and BE layers

The 70 empty-base principal-Pfaffian quadrics are squarefree.  All
`70*16=1120` sector identities survive exactly, but they are merely the
four-site Pfaffian expansion.  Their 210 squarefree complement lifts per
decorated word remain wordwise Laplace tautologies and never couple either
pure anchor to the crossed row.

Every nonempty-base Pluecker relation has a doubled physical site.  A
nonnegative source multiplier cannot return it to the squarefree K8 grade.
Odd-principal Buchsbaum--Eisenbud rows have the same obstruction.  The exact
one-step census checks 14,112 insertions and finds no squarefree row; 4,480
contractions give 1,792 duplicate-free lower cofactors, but no squarefree
eight-site row and no common decorated grade.

The unique two-step degree repair was also exhausted.  There are 336
contraction/reinsertion paths.  Of these, 82 have zero net Arf twist and 254
are twisted.  Nevertheless every one of all 5,376 sector rows and 145,152
decorated rows is the zero identity: its 30 raw terms pair into 15 matching
monomials with opposite signs.  Even the 82 untwisted paths carry no target,
anchor, residual, or response value.

## Controls and verdict

The expansion itself is universal in the edge variables, so it automatically
replays the `n=4` witness and invisible-chord controls without adding a
constraint.  The exact `n=6` theorem uses source equations not supplied by a
single Arf/Pfaffian sector; there is no equality-case transfer from it to
`K8`.

The genus-two construction is therefore only a 16-fold coordinate rewrite at
the literal squarefree source grade.  A viable Pfaffian continuation would
need a new target-augmented, cross-word attaching map that both removes the
doubled-site grade and descends nontrivial Arf characters.  That is precisely
the missing provenance problem, not a consequence of standard Pfaffian ideal
theory.

## Frozen artifacts

```text
note, direct probe      338a2510...  / 06c8aebe...
note, one-step          3285e07c...  / dbb6b47e...
note, two-step          ce66a70d...  / 0b914886...
```

The three standard replays pass with logical digests respectively
`5e6a7a702c8f8e633424628d87252418ed477703160c64d1d1f3e837360e77c8`,
`fbf8d2003280d9a0d909dba8291bd1ea2d8b37842cf1e53682759331bd92796a`,
and `0693e4e9e49f1dcaf3e2c790fa53d23506a1a98f6e93eb4a1976cafaadf6c437`.
