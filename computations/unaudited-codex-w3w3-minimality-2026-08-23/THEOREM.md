# Ten coloured sources are necessary and sufficient for `W3 x W3`

Let the six vertices be `0,...,5`, with binary endpoint colours.  A coloured
source coordinate is `(u,v;a,b)` with `u<v`.  For a word `c` and perfect
matching `M`, its occurrence monomial is the product of the three coordinates
`(u,v;c_u,c_v)` for `uv` in `M`.

The target support is

```text
001001  001010  001100
010001  010010  010100
100001  100010  100100.
```

## Theorem

In the postselected pair-source/perfect-matching model, an exact
`W3 tensor W3` state requires at least ten nonzero coloured source
coordinates.  Ten suffice, even with every nonzero weight equal to one.

## Certified proof

Suppose a complex-weighted realization has support `S`.

Every target word must have at least one supported occurrence; otherwise its
coefficient is zero.  The frozen CNF encodes only these nine target-cover
conditions together with `|S| <= 9`.  It has 654 variables and 1,509 clauses.
The accompanying 7,614-addition deletion-free DRUP trace derives the empty
clause.  The repository checker replays every addition by reverse unit
propagation, using CaDiCaL rather than the Glucose instance that generated the
proof.

For sharpness, the public PyTheus ten-coordinate solution has one occurrence
for each of the nine target words and none for any of the other 55 words.
Thus setting every listed weight to one produces the target exactly.  The
independent SAT boundary audit also finds and directly checks a second
ten-coordinate support.

This lower bound is stronger than either a singleton or phase-sensitive
obstruction: nine coordinates cannot even cover the nine desired basis
words.  It holds before forbidden outputs or complex weights are considered.
