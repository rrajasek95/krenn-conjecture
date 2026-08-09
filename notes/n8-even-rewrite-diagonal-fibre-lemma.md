# N=8 even-complement diagonal fibre lemma and sharp guards

The proposed global statement

> every three-one-factor state with a diagonal endpoint-colour cell has an
> even-complement rewrite with fewer diagonal cells

is false as written.  Chart 26 is already a counterexample: it has twelve
diagonal cells, while both of its mixed factors have odd complement type
`(5,3)`.  It admits no even-complement rewrite at all.

## The exact fibre-local theorem

Fix a mixed output word with colour counts `(n0,n1,n2)`, summing to eight.
Among all 105 compatible physical perfect matchings, the minimum possible
number of same-colour (diagonal) pairs is

```text
max(0,max(n0,n1,n2)-4).
```

Indeed, if the largest colour class has more than four vertices, exactly
`nmax-4` pairs must remain inside it; otherwise all vertices can be paired
across colour classes.  The checker independently enumerates all
`3^8-3=6,558` mixed words and all 105 matchings per word.

Consequently, for a selected mixed matching `R` with even complementary
two-factor, a strict diagonal-decreasing rewrite exists exactly when
`R` has more diagonal pairs than this word-fibre minimum.  The complement
is unchanged, and a minimum matching supplies the required mate.  This is
the structural content behind every observed decrease; the remaining
global problem is to prove that a suitable nonminimal even factor exists.

Among the 31 pure roots, chart 26 is the unique state with no even factor.
Each of the other thirty has a factor strictly above its fibre minimum.
The same criterion succeeds on all 505 exact nonroot states in the first
rewrite layer.  The latter is a bounded counterguard, not an all-state proof.

## All-offdiagonal bottom fibres

In an all-offdiagonal 24-port state, let `x01,x02,x12` be the numbers of
cells joining each unordered pair of endpoint colours.  Port balance forces

```text
x01=x02=x12=4.
```

Every contained selected matching already has zero diagonal pairs, so no
strict decrease is possible.  A word admits such a matching precisely when
every colour count is at most four.  Up to colour permutation the possible
mixed partitions and the numbers of labelled zero-diagonal matchings are

| word partition | matchings |
|---|---:|
| `(4,4)` | 24 |
| `(4,3,1)` | 24 |
| `(4,2,2)` | 24 |
| `(3,3,2)` | 36 |

For counts `(n0,n1,n2)`, put

```text
e01=4-n2, e02=4-n1, e12=4-n0.
```

The count is

```text
n0!*n1!*n2!/(e01!*e02!*e12!).
```

At the lowest diagonal filtration, one mixed hafnian fibre therefore gives
one all-`+1` signed incidence row on 24 or 36 labelled bottom states.  Fibre
locally this leaves cokernel dimension at least 23 or 35.  Any contraction
must use gluing between different fibres and their Laurent/source signs; a
single bottom fibre cannot provide an acyclic pivoting.

This classifies the possible bottom **fibre types**, not the global
`S8 x S3` orbits of all-offdiagonal three-factor states.  That orbit gluing
and its signed homology are the remaining finite problem.

The exact checker is
`computations/verify_n8_even_rewrite_diagonal_fibre_lemma.py`.
Its frozen ledger SHA-256 is
`f60104bf038b76a97f49edb62c18600c2f21357ce493f8605a25c4c6d6ffbbb6`.
