# The `(c,t,c)` companion has exactly six quadratic cancellation mates

Date: 2026-08-11

Checker: `computations/verify_h3_one_bad_companion_quadratic_mate_partition.py`

## Verdict

At the concentrated normal form `C=Q1=0` from `1dea1fa`, the mandatory
mixed coefficient `21000121` has 105 perfect-matching monomials.  Filtering
by the number of cells outside the normal-form support gives exactly

```text
normal degree       1    2    3    4
number of terms     1    6   30   68.
```

The sole linear term is the pivot `C=12:10`.  The six quadratic mates split
into two source grades:

```text
D_cc^(pr) Q_t q^[2]                     four terms,
P_c Q_t R_c q                            two terms.
```

No `pq`- or `qr`-direct mate appears before cubic normal degree.  Thus the
first arbitrary-support escape from the literal companion closure is a
finite six-pair problem, not an uncontrolled support face.

## The six pairs

With the normalized nonzero cells understood, the four diagonal-companion
pairs are

```text
(01:21, Q_t@2:0),    (02:20, Q_t@1:1),
(13:10, 24:00),      (14:10, 23:00).
```

The two common-hole pairs are

```text
(P_c@1:1, R_c@2:0),
(R_c@1:1, P_c@2:0).
```

The checker obtains this list directly from the 105 K8 matchings and the
literal endpoint-colour word; the labels are not abstract jet variables.

## Complete tangent audit of the four retained rows

The first derivative of the two diagonal tensor rows and the `ca`/`tt`
tensor rows uses all

```text
90 internal q cells + 5*15 star cells + 2 direct scalars = 167 columns
```

and has 150 occupied coefficient rows.  Four q directions from the first
grade expose genuinely unique forbidden coordinates:

```text
01:21 -> Ra row 21000,
13:10 -> Qc row 11101,
14:10 -> Qc row 11220,
23:00 -> tt row 22002.
```

The remaining two have only the following apparent first-order repairs:

```text
02:20 -> ca row 22000, also hit by Qc@0:2;
24:00 -> Qc row 11010, also hit by -Qc@4:0.
```

But those star columns carry new tails respectively in `Qc:21111` and
`Qc:00220`.  Hence none of the four `Dpr*Qt*q^[2]` quadratic monomials is a
closed two-cell tangent by itself.  Each demands an additional physical
face already at first order.

By contrast, the `P_c/R_c` cells do not occur in these four selected outer
labels, so both of their products are tangent-invisible through first order.
They are the genuine quadratic attaching candidates.

## Exact route split and remaining hypotheses

For `(P_c@1,R_c@2)`, both new colours use the same holes as the existing
`P_t@1,R_a@2`.  The two endpoint `2x2` minors are `(0,0)`, while the
quadratic response is supported on the single physical hole-pair `{1,2}`.
Thus the one-edge support demanded by the intrinsic Component-II theorem
is automatic.  What is **not** automatic from this mate alone is the
scalar-zero pure-target cap normalization; that source-labelled relation
must still be extracted from the surrounding rows.

For `(R_c@1,P_c@2)`, the new holes are crossed.  The two endpoint minors
are `(1,-1)`, so goodness on the selected two-dimensional endpoint slices
is automatic.  What is **not** yet certified is full endpoint activity/span
and the curved two-chart hypothesis required by the OO theorem.  Therefore
the calculation identifies the crossed-good route but does not invoke the
curved theorem unconditionally.

This is the sharp quadratic dichotomy.  Cubic support expansion is not
justified until the missing scalar-zero normalization and the missing
activity/curvature hypotheses are checked on these two literal pairs.

## Scope

This is a complete degree-two matching and four-row tangent classification
at the concentrated literal normal form.  It does not inspect the thirty
cubic or sixty-eight quartic terms, and it is not a full arbitrary-support
one-bad theorem.  Its value is that it replaces the vague phrase
"cancellation mates" by six physical pairs and two precisely stated
proof obligations.
