# First-unmatched-tail attachment boundary on the normalized rootless C5

## Result

The residual `R_v-R_w` terms have an exact conditional attachment theorem,
but normalized C5 tail data alone do not supply its endpoint hypothesis.
The earliest missing statement is therefore response-hole accessibility,
not another internal matching switch.

Checker:
`computations/verify_h3_rootless_c5_first_unmatched_tail_attachment_boundary.py`.

## Literal tail algebra

Write the five off-cycle chords as

```text
A=q13, B=q14, C=q24, D=q25, E=q35.
```

After the selected C5 edges are normalized to one, the five deletion-face
companions are

```text
R1 = C*E + D,
R2 = A   + B*E,
R3 = B*D + C,
R4 = E   + A*D,
R5 = A*C + B.
```

The ten displayed monomials are pairwise distinct: five linear and five
quadratic.  Moreover, consecutive faces in order `1,3,5,2,4` have disjoint
tail supports.  Thus every term in every adjacent `R_v-R_w` is literally a
first unmatched tail; no equal-tail cancellation is hidden in the
normalized C5 algebra.

## Conditional complete-row lemma

Fix one literal tail matching `N` in `R_v`.  If an endpoint product at the
forced response hole `(x,v)` is nonzero, its complete coefficient has six
terms:

1. the selected orientation and tail;
2. the opposite endpoint orientation on the same decorated tail; and
3. four terms obtained from the other two four-site matchings, in both
   endpoint orientations.

Every different tail differs from `N` by one literal alternating C4.  Hence
exactness gives the exhaustive routing:

```text
no active mate        -> localized ordinary source unit;
same-tail opposite    -> proportional finite deletion or Fitting carrier;
different-tail C4     -> offanchor typed attachment, or anchor Hall/lock.
```

Across the ten tail occurrences this is ten same-tail opposite terms and
forty C4 terms.  This is the desired first-unmatched-tail lemma under one
sharp hypothesis: a nonzero endpoint product at `(x,v)`.

The Fitting outcome is not automatically a four-good landing.  Deleted-star
rank completion and termination remain separate.

## Sharp obstruction

The endpoint hypothesis does not follow from normalized internal C5 data.
For example, at

```text
A=2, B=C=D=E=1
```

some adjacent `R_v-R_w` are nonzero.  Setting every endpoint product on
holes `(x,1),...,(x,5)` to zero makes all complete attachment columns dark
without changing those internal tail values.

This is a source-typing counterguard, not a full rootless coefficient point:
it omits the full unary and four-response target constraints.  Its purpose
is to isolate the exact missing implication:

> the full common-q source packet must turn a response-dark unmatched C5
> tail into a hole hit, an offanchor carrier, or a Hall relation.

This is the same affine line-hitting issue as Theorem A's multisite
concentration gate.  The selected internal matching proves no endpoint-star
coordinate by itself.

## Relation to the recent E14 units

`e35b24c` and `414f4c6` show that one or two internal contaminants cannot
survive on the canonical E14 fibre.  They support the proposed attachment
mechanism locally, but they do not prove response-hole accessibility for the
rootless C5 chart and are not used to infer it.

## Verification

```text
python3 computations/verify_h3_rootless_c5_first_unmatched_tail_attachment_boundary.py
python3 -O computations/verify_h3_rootless_c5_first_unmatched_tail_attachment_boundary.py
python3 -I -S computations/verify_h3_rootless_c5_first_unmatched_tail_attachment_boundary.py
```

Frozen ledger SHA-256:

```text
7d0d402c01bd9862235b568068a418009220f344247d48ca4c8f48b683c12578
```
