# The private p5 row completes the localized Rees landing

Date: 2026-08-11

Checker:
`computations/verify_n8_one_bad_axis_pure_global_killer_p5_weierstrass.py`

## Literal missing row

Keep all `90` mixed q cells symbolic in the localized axis-pure chart.  One
complete response coefficient not used among the 54 carrier-killer rows is

```text
11 @ 011011
 = p5*s1*(A*z03 + m02:01*m34:01 + m04:01*m23:10).
```

This is an original source row, not a declared graph equation.  The factors
`A`, `s1`, and `z03` are units: `A,s1` come from the diagonal response anchor
and `z03` from the exact pure-chart identity of `260bb94`.  All four mixed
cells in the two quadratic tails belong to the 54-variable standard-basis
block of `1aec4da`.

Consequently the parenthesized cofactor is a unit in the completed mixed
graph.  The row forces

```text
p5 = 0.
```

Equivalently, with the common source valuation its initial term is the unit
`A*s1*z03*p5`, while both tails have exact weight two higher.  Thus this row
adds a 55th unit-linear initial, `p5`, pairwise coprime to the 54 carrier
initials.  No maximum-support argument is actually needed to derive the
vanishing; maximum-support minimality merely interprets the vanished entry
as source-removable.

## Coefficient-ring and homogeneity audit

The checker replays the stronger carrier-only inequalities for the original
54 rows: arbitrary pure coefficients and star factors are left in the base
ring, and every contaminant still has carrier weight at least one above its
selected carrier.  Hence the 54 equations define their formal graph over the
whole localized pure coefficient ring, not just at a specialization where
the other pure coefficients vanish.

It also checks target-character homogeneity for every coefficient of the
unary tensor and all four response tensors.  Under the separator of
`1aec4da`:

```text
54 graph carriers have target weight 0,
36 graph parameters have weights 1 (32 cells) or 2 (4 cells),
p5 has weight -1 but is zero in the completed quotient.
```

The graph functions for the 54 weight-zero carriers vanish at the origin and
are target-homogeneous over a weight-zero pure base.  Since every remaining
parameter has positive weight, those functions are identically zero.  The
target-compatible cocharacter therefore contracts every nonzero mixed graph
parameter and keeps all endpoint data finite.

At the limit all mixed q cells vanish.  The exact pure-chart theorem
`260bb94` says the five source equations then contain a unit; equivalently
`9070e22` gives a unit degree-zero crossed response germ.  Completeness and
Nakayama lift that unit back to the localized mixed graph.  Thus the
completed localized full-mixed chart is empty.

## Scope

This closes the exact Rees prerequisite exposed by `aaed0f5` for the pinned
axis-pure endpoint packet.  It is a completed-local statement.  It does not
assert that the cofactor bracket cannot vanish at a distant affine point,
nor does it supply the separate upstream theorem that an arbitrary exact
source lands in this normalized axis-pure packet.
