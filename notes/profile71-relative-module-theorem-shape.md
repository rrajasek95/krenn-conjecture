# The `7+1` packet is an equation module, not a cellular boundary

## Exact outcome

Let `M_71` be the source-word space on words with colour multiplicities
`7+1`.  A basis element is equivalently a triple `(i; a -> b)`: the
exceptional site `i`, the majority colour `a`, and the distinct minority
colour `b`.  Hence, before any quotient,

```
M_71 = Q[{0,...,7}] tensor Q[{ordered distinct colour pairs}]
     = (1 + S^(7,1)) external_tensor (1 + sign + 2 standard_S3).
```

It has dimension 48.  Each literal amplitude row has 105 decorated matching
monomials, and the 48 supports are pairwise disjoint (5,040 monomials total).
Thus the literal `7+1` packet has rank 48.  It is not a family of relations
among matchings, much less the boundary image in the usual signed
matching-exchange/Pluecker complex.  Its rows also have augmentation 105,
whereas an oriented cellular boundary has augmentation zero.

## What the joint projection does

After forgetting edge-colour incidence and retaining only the 28 physical
edge multiplicities plus the nine global ordered-colour-pair counts, the
48 rows have rank 42.  The kernel has the six exact relations, one for every
ordered pair of distinct colours `(a,b)`,

```
3 X_(b a a a a a a a)
- X_(a b a a a a a a) - ... - X_(a a a a a a b a)
+ 3 X_(a a a a a a a b) = 0                         (projected only).
```

These are not literal source identities.  More sharply, swapping sites 0
and 1 in the displayed coefficient vector maps it to a nonzero projected
vector with 30 terms (15 coefficients `+4`, 15 coefficients `-4`).  The
projection kernel is therefore not `S8`-stable.  The current joint quotient
does not carry the source `S8 x S3` action and cannot support an equivariant
cellular exactness argument.  The eight `7+1` words already in closure22 are
independent in the projection, so completing their orbit adds only 34 new
degree-four projected directions, despite adding 40 literal equations.

## Effect on the terminal dual

The completed orbit certainly kills the frozen 100-column dual: seven of
its words supply 87 crossing translations, and `00000200` alone supplies
four crossings of pairing `-1`.  This removes that one relative cokernel
class (and, in a genuinely equivariant literal model, its symmetry orbit).
It does **not** show that the enlarged complex is exact.

The completed one-generator control proves that the conservative warning is
real.  After adjoining only `00000200`, 100 CEGAR rounds terminate at rank
133,968 with the same 13,636-term target remainder and a new integral
156-column dual.  It has target pairing one and annihilates every abstract
translation of closure22 plus `00000200`: this is a genuine replacement
relative cokernel class in the joint semigroup module.  The replacement is
itself crossed by 133 translations from six still-missing `7+1` words, so the
full orbit kills it too.  Nothing, however, prevents the same phenomenon
from iterating after all 48 words are admitted.

## Actionable theorem test

Treat profile `7+1` as 40 additional source equations, not as a boundary
map.  The next decisive calculation is exactly one full-orbit CEGAR run:

1. adjoin all 48 `7+1` words;
2. require either target reduction to zero or an integral dual annihilating
   every translation of all 62 admitted words;
3. for any positive reduction, reconstruct literal decorated multipliers
   and characteristic zero before claiming ideal membership.

Any representation-theoretic promotion must instead be performed in the
252-cell exponent semigroup (or another quotient retaining edge-colour
incidence), where `S8 x S3` genuinely acts.  The existing 37-coordinate
joint projection is an obstruction/counterguard to such a promotion.

Exact replay:

```
python3 computations/unaudited-codex-rootless-fine-macaulay-2026-08-22/audit_profile71_module_shape.py --check-results
python3 -O computations/unaudited-codex-rootless-fine-macaulay-2026-08-22/audit_profile71_module_shape.py --check-results
python3 -I -S computations/unaudited-codex-rootless-fine-macaulay-2026-08-22/audit_profile71_module_shape.py --check-results
```
