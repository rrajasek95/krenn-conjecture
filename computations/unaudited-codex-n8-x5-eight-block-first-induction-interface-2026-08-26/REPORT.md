# First exact eight-block induction interface

## Outcome

The first unproved step after the sealed zero-through-six theorem and the
seven-block boundary is the **eight-added-block layer**.  It does not follow
monotonically from closing the 64 seven-block loci.

The exact support census is:

```text
C(20,8) supports                              125,970
fixed-identity triangle/star closed            66,752
fixed-identity structural evaders              59,218
guard-stable eight-block supports                1,268
stable coefficient strata (x16)                20,288
fixed-identity closed strata                    16,427
nonidentity hyperplane-avoidance closed          3,245
coefficient-dependent unresolved strata            616
guard-symmetry orbits                              308
```

Among the 616 unresolved strata, 472 have one unresolved seven-block deletion
parent and 40 have two.  Crucially, **104 have no unresolved seven-block
parent at all**.  These 104 are new eight-block phenomena, so a theorem that
only closes and deletes from the historical 64 sparse loci is insufficient.

## Unconditional lemma

For a two-response carrier

```text
L(K) = (U^T K B1, U^T K B2),
P = Col(U),  Q = ColSpan(B1,B2),  W = P tensor Q,
```

there exists `K in ker(L)` with all `K00,K11,K22,<K,C>` nonzero exactly when
`E00,E11,E22,C` all lie outside `W`.  This is unconditional over `Q`:
trace cyclicity gives `im(L*)=W`; a functional vanishes on the kernel exactly
when it is in `W`; and four proper hyperplanes cannot cover a rational vector
space.  No historical sparse certificate is used.

## Smallest new class

Lexicographically by supported matching count, nonzero variable-family count,
and total response-edge load, the smallest no-parent class has rank
`(8,1,66)`: four records in two exact guard-symmetry orbits.  A representative
support is

```text
fixed:   03,16,27,45 = I3
nonzero: 01,06,15,17,23,26,35,46,47
```

and its guard mate replaces the `06` geometry by `07`.  In both orbits the
base matching `03|16|27|45` is the four-pair equality tensor: it agrees with
GHZ on the three pure words but has 78 additional mixed base words.  Thus the
6,561 full-X5 equations say that the seven alternative matching tensors equal
`GHZ - base`, whose value is `-1` on those 78 mixed words and zero elsewhere.
For the `06` orbit this source-labelled tensor polynomial factors as

```text
(A01*A35 + A03*A15)*(A26*A47 + A27*A46)
 + A06*A23*(A15*A47 + A17*A45)
 + A03*A17*A26*A45 = 0.
```

For the `07` orbit, the middle term is
`A07*A23*(A15*A46 + A16*A45)`.  The product signs denote the literal matching
tensor factors with entry convention `Auv[c_u,c_v]`; the package expands them
back to the exact seven supported matchings.

Both representatives have a minimal cap01/star3 carrier with only two
nonzero forbidden response products.  In the `06` orbit it is

```text
L(K)=(A06^T K A15, A06^T K A17),
```

while in the `07` orbit it is

```text
L(K)=(A07^T K A15, A07^T K A16),  A16=I3.
```

The lemma reduces each orbit to four explicit exact-Q failure systems: one
cap-pairing incidence and three diagonal incidences.  Nonzero matrices are
encoded without chart explosion by witness equations
`sum w_ij A_ij=1`.  Per orbit the pairing system has 180 variables/6,579
generators and each diagonal system 171/6,576.  Thus eight exact-Q unit-ideal
certificates would close the four smallest records.  A nonunit point would
only show failure of this selected carrier and is not a conjecture
counterexample without checking all other carriers and guards.

## Scope

This package proves the exact census, the failure of deletion monotonicity,
the unconditional two-sandwich activity lemma, and the finite source-labelled
interface.  It does **not** close any of the 616 coefficient loci, the full
eight-block layer, rep2/rep5, or the conjecture.  No Singular, CEGAR, D12 read,
or other heavy solver ran.
