# H3 C6 E14 unary S-pair first-reduction boundary

## Finite orbit/factor theorem

The 228 private target occurrences from `6e5878e` have canonical unary
cycle-breakers in only nine word orbits:

| unary word | maximum multiplied tail degree | occurrences |
|---|---:|---:|
| `000011` | 4 | 36 |
| `000101` | 4 | 36 |
| `001001` | 4 | 48 |
| `001010` | 4 | 24 |
| `001100` | 4 | 24 |
| `010001` | 4 | 18 |
| `011000` | 4 | 18 |
| `010010` | 3 | 12 |
| `100100` | 3 | 12 |

Writing the selected unary row as `U=p A+B`, where the linear pivot `p`
divides no monomial of `B`, gives exactly three factor types:

- 156 times: `A` has degrees `(0,1)` and `B` has ten quadratics plus two
  cubics;
- 48 times: `A` has degrees `(0,2)` and `B` has eight quadratics plus four
  cubics;
- 24 times: `A` is constant and `B` has twelve quadratics.

In every case `A(0)` is nonzero, so `A` is a unit in the local/Rees
completion.  After multiplying by the missing factor of the private quadratic,
all 2,736 terms of `B` have a literal complete-`G11` zero-row divisor.  Of
these, 432 are divisible by a nonprivate target-row occurrence and 2,304 by
another complete zero-row occurrence.  Thus there is no support or incidence
obstruction at this stage.

The return factors themselves use only the two missing chord coordinates
`v04_00` and `v13_00`.  After normalizing their constant term they are

```text
1                                      (24),
1-v04,  1-v04/5,  1+v04/3             (54,24,18),
1-v13,  1+v13/3                        (24,36),
1-v04*v13/7                            (48).
```

Thus the return graph has no cross-orbit edge: these are self-loops on the
private generator.  On the strict silent-C6 branch the *whole physical edge
tables* `q04,q13` vanish, so `v04_00=v13_00=0` and every loop factor is the
unit `1`.  Conversely every nonconstant singular locus makes at least one
missing chord nonzero and exits to the crossed-C4 response landing of
`h3-four-base-silent-c6-response-lock.md`; it is not a hidden flat holonomy
inside the chordless chart.

## The first reduction does not close

For the lexicographically first chart `(1,1)` occurrence,

```
endpoint = p1_0_1 s1_1_1,
private  = u35_11 v24_11,
U-word   = 000101,
p        = u35_11,
A        = -1 + v04_00.
```

The checker forms every complete unary or `G11` row, with its exact `q`
multiplier and target readout, that directly hits one of the twelve multiplied
`B` tails.  There are 269 distinct target-augmented columns, each an independent
first-hit pivot (exact rational rank 269).  The `B` target is not in their
span.  Exact echelon reduction is

```
(p1_0_1 s1_1_1) u35_11 v24_11
  - (p1_0_1 s1_1_1) u35_11 v04_00 v24_11
= (p1_0_1 s1_1_1) u35_11 v24_11 (1-v04_00).
```

So the complete first reductions return precisely to the original private
generator multiplied by the unary local unit.  A rational cokernel functional
of support 22 kills all 269 columns and pairs `-1` with `B`; after clearing
denominators its primitive integral pairing is `-30`.

The two canonical specializations make the algebraic split precise.  At
`v04_00=0`, the specialized first-hit module has rank 224 and the `B`
remainder equals the nonzero private-generator remainder.  At `v04_00=1`,
the rank is 257 and `B` reduces to zero, but the private generator still has
nonzero remainder.  Hence neither branch alone closes the source problem:
on `D(1-v04)` the two classes are identified, while on `V(1-v04)` the unary
pivot disappears and leaves the private class free.

`G22` cannot directly change this result: its endpoint-star grade is distinct
from the displayed `p1/s1` private module.  It may enter only after an
endpoint-word-changing attachment.

## Exact next datum

The next source row must enter through one of the first-hit companion
coordinates killed by neither the displayed residual nor its dual.  In
Buchberger language this is the next S-pair/endpoint-word-change layer, not a
fourth internal support face.  The present checker deliberately stops before
the recursively expanding companion closure; it proves the finite first-hit
cokernel, not a completed Gröbner calculation or a full-source counterexample.

Verified by
`computations/verify_h3_c6_e14_unary_spair_first_reduction_boundary.py`.
