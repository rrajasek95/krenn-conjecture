# The universal normalized-C5 tail quotient has rank four

## Result

On the target-preserving normalized `C5` chart, retain the two off-cycle
matching occurrences in every face separately.  In the universal
endpoint-typed polynomial module,

\[
 Q_{\rm tail}=
 {\operatorname{span}_{\mathbb Q}\{R_v-R_{\rm next}\}\over
  \operatorname{im}J_{\rm tail}}
 \cong \mathbb Q^4.                                    \tag{1}
\]

The reason is source grading, not a support assumption.  Every complete
unary or response term containing one of the ten tails also contains a
nonempty endpoint attachment.  Hence all those rows have zero projection
to the bare-tail grade before localization.

Checker:
`computations/verify_h3_rootless_c5_universal_ten_tail_typed_quotient.py`.

This is not a full-source counterexample.  It identifies the exact columns
which a positive response-hole accessibility theorem must activate.

## 1. Exact ten-tail basis

Let the normalized selected cycle be

```text
12, 23, 34, 45, 15
```

with internal word `m=12112`.  Each deletion face has three perfect
matchings, exactly one on the selected cycle and two off it.  The ten
off-cycle decorated monomials are

```text
v=1: q24^21*q35^12, q25^22*q34^11
v=2: q13^11*q45^12, q14^11*q35^12
v=3: q14^11*q25^22, q15^12*q24^21
v=4: q12^12*q35^12, q13^11*q25^22
v=5: q13^11*q24^21, q14^11*q23^21.
```

They are pairwise distinct.  Write their face sums as `R_v`.  In cyclic
face order

```text
1, 3, 5, 2, 4
```

the five columns `R_v-R_next` have rank four and their unique relation is
their oriented sum zero.

The checker freezes two exact dual presentations.  An integral sparse dual
for the first four cyclic edges chooses one occurrence from each successive
prefix of the face order.  A face-symmetric representative puts coefficient
`1/2` on both occurrences in the same prefixes.  Their pairing with the
first four differences is the identity matrix; every one reads `-1` on the
closing edge.  Thus the rank-four quotient has explicit primitive sparse
separators, not merely a numerical rank certificate.

## 2. Complete rows containing the occurrences

There is one relevant unary coefficient.  Its output word is

```text
012112
```

on `x,D`.  Its fifteen perfect matchings are uniquely a spoke `(x,v)` times
one of the three matchings of the deleted face.  Exactly ten are off-cycle,
and each has the typed form

\[
                     q_{xv}^{0m_v}N.                  \tag{2}
\]

Thus (2) gives ten unary spoke occurrences, but no bare `N` column.

For every `v` and every response label `ij` in
`11,12,21,22`, the complete coefficient at the forced hole `(x,v)` has six
terms: three face matchings in each of the two endpoint orientations.  An
off-cycle tail `N` occurs as the complete bracket

\[
 B_{ij}^{xv}N=
 (p_i@x\,s_j@v+p_i@v\,s_j@x)N.                       \tag{3}
\]

Consequently the complete inventory is

```text
21 relevant coefficients = 1 unary + 5 holes * 4 responses
135 matching terms        = 15 unary + 20 * 6 response
10 unary off-cycle spokes
40 off-cycle response brackets = 80 oriented endpoint columns.
```

All relevant face words contain both colours `1` and `2`, so these selected
coefficients have target readout zero.  The checker retains the deletion
face, internal decorated matching, endpoint orientation, response label,
endpoint word, and target readout for every term.

## 3. Endpoint-grade separation

Give every endpoint attachment its literal nonnegative source grade.  The
ten unary occurrences have endpoint degree one; the eighty oriented
response occurrences have endpoint degree two.  None has endpoint degree
zero.  Therefore every complete row projects to zero in the bare ten-tail
summand, and

\[
                    \operatorname{rank}J_{\rm tail}=0 \tag{4}
\]

in that universal typed grade.  Polynomial multiplication can only add
endpoint degree, so it does not change (4).  Dividing by a spoke or by the
bracket (3) would change the conclusion, but that is a localization and
requires its factor to be active.

This is exactly compatible with commit `8771755`: once one bracket in (3)
is active, its complete six-term row gives the unit/same-tail/C4 routing
dichotomy.  The present theorem says that activity is an additional physical
input and cannot be silently supplied by forgetting endpoint grades.

## Scope

Equation (1) is a finite exact `h=3` theorem for the normalized selected-C5
chart and the universal endpoint-typed polynomial rows.  It does not exhibit
a full source satisfying all equations with dark brackets, prove that every
bracket is dark, or refute a source-level accessibility theorem.  The missing
positive input is precisely one of the ten spokes (2), or one of the forty
complete brackets (3), with source-valid localization/routing.

Run:

```text
python3 computations/verify_h3_rootless_c5_universal_ten_tail_typed_quotient.py
python3 -O computations/verify_h3_rootless_c5_universal_ten_tail_typed_quotient.py
python3 -I -S computations/verify_h3_rootless_c5_universal_ten_tail_typed_quotient.py
```

Frozen ledger SHA-256:

```text
f5998c8c56459323e0fb9f56158d0785ba1841654b7737415748407cb84c675d
```
