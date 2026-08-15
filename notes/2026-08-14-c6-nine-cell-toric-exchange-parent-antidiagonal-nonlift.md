# The nine-cell parent anti-diagonal is toric but not a physical EqSystem row

## Outcome

The exact nine-cell escape guard has the shortest possible unlabelled matching
exchange chain:

```text
M0 = 05|12|34  --C4(0125), tail 34-->  M1 = 01|25|34
M1 = 01|25|34  --C4(2345), tail 01-->  N  = 01|23|45.      (1)
```

It is the unique two-step `C4` chain whose three matching monomials are live
in the nine-cell support.  There is also a one-step primitive `C6` toric
binomial from `M0` to `N`.

This does **not** generate the parent anti-diagonal source-naturally.  The
first toric edge is

\[
                              M_0-M_1,                     \tag{2}
\]

while both physical mixed EqSystem rows contain the signless hafnian sum

\[
                              M_0+M_1.                     \tag{3}

On the exact rational guard the weighted contributions are

\[
                       (M_0,M_1,N)=(2,-2,1),              \tag{4}

\]

so (3) vanishes and (2) evaluates to `4`.  The toric exchange is not a
physical row.  The second exchange `M1-N` evaluates to `-3`, and the direct
`C6` exchange `M0-N` evaluates to `1`.  Hence the chain fails before any
parent selector or cap descent is constructed.

The checker exhausts the full degree-three and degree-four edge-incidence
toric fibres, all 729 EqSystem word rows, and all word/fine/operation labels:
`computations/verify_c6_nine_cell_toric_exchange_parent_antidiagonal_nonlift.py`.

## 1. The exact labelled guard

Use cap `34` and coefficients

```text
34;0=34;1=34;2=1,
05;1=2, 12;1=1,
01;1=-2, 25;1=1,
23;1=-1/2, 45;1=1.                                      (5)
```

Complete expansion of all fifteen `K6` perfect matchings in every output word
has only three nonempty left sides:

```text
coefficient:111001   M1(-2)+M0(2)        = 0,
coefficient:111111   N(1)+M1(-2)+M0(2)   = 1,
coefficient:111221   M1(-2)+M0(2)        = 0.             (6)
```

In occurrence coordinates `(M0,M1,N)`, the physical row module is spanned by

\[
                 (1,1,0),\qquad (1,1,1).                  \tag{7}

Its rank is two.  Adjoining either the parent anti-diagonal `(1,-1,0)` or the
short-tail selector `(0,1,1)` raises the rank to three.  Thus neither is a
linear combination of complete physical rows.

This remains false with arbitrary polynomial row multipliers in the local
occurrence algebra.  The quotient map

\[
       M_0\mapsto t,\qquad M_1\mapsto-t,\qquad N\mapsto1  \tag{8}

kills the two physical equations

\[
                   M_0+M_1,\qquad M_0+M_1+N-1,            \tag{9}

but sends `M0-M1` to `2t`, which is nonzero.  Equation (8) is an exact ideal
nonmembership certificate, not only a row-rank calculation.

## 2. Minimal exchange chains

Join two perfect matchings when their symmetric difference is one `C4`, or
equivalently when they share one matching edge.  In the resulting graph on
the fifteen `K6` matchings, `M0` and `N` have distance two.  There are exactly
three shortest paths:

```text
M0 -> 01|25|34 -> N,
M0 -> 03|12|45 -> N,
M0 -> 05|14|23 -> N.                                    (10)
```

Only the first lies in the nine-cell support, and its intermediate is `M1`.
The complete labelled steps are:

1. `M0 -> M1`: common cap/tail `34`, alternating window `0125`, both parents
   cap-containing.  It occurs in the same mixed word, but EqSystem supplies
   the even sum (3), not the odd orientation (2).
2. `M1 -> N`: common tail `01`, alternating window `2345`.  It changes the
   cap status from `contains:34` to `avoids:34`.  The two occurrences coexist
   only in pure word `111111`; restricting that row to tail `01` gives the
   signless sub-sum `M1+N`, not a coefficient operation and not `M1-N`.

The direct pair `M0,N` has no common tail and symmetric difference the entire
six-cycle.  Its edge-monomial difference is a primitive degree-three toric
binomial, but the complete pure row also contains `M1` and the target.

Therefore the first nonlift is already Step 1.  No later exchange can repair
its missing sign/operation provenance.

## 3. Complete degree-three toric census

Map every `K6` edge variable by

\[
                             x_{uv}\longmapsto t_ut_v.      \tag{11}

Degree-three edge monomials split into incidence fibres.  Exact enumeration
gives

```text
680 monomials, 336 fibres, 121 nontrivial fibres,
825 binomial pairs,
fibre sizes 1:215, 3:90, 6:30, 15:1.                      (12)
```

The size-fifteen fibre is precisely the perfect-matching fibre of site degree
`(1,1,1,1,1,1)`, with `C(15,2)=105` toric binomials.

At the guard point only `M0,M1,N` have nonzero matching monomials.  Among the
105 binomials, 66 vanish because both terms are absent.  None is incident to
one of the three live parents.  In fact every toric binomial incident to a
live parent is pointwise nonzero: the three live values `2,-2,1` are distinct
and all other matching values are zero.

This is stronger than saying the chosen two-step chain fails.  Even the very
permissive rule “accept a toric exchange if it happens to vanish at this
source point” supplies no first edge out of a live parent.

## 4. Degree-four exchanges do not repair the lift

The complete degree-four incidence census is

```text
3060 monomials, 951 fibres, 486 nontrivial fibres,
8955 binomial pairs,
fibre sizes 1:465, 3:270, 6:135, 10:66, 21:15.            (13)
```

For each of the three live parents and each of the seven live colour-one
edge cells, the checker examines the fibre of the degree-four monomial
`x_e M`.  None of these 21 terms has another term of equal value in its
fibre, so there is again no pointwise-vanishing exchange incident to the
labelled parent.

More fundamentally, `x_eM` has site multidegree

\[
                  (2,2,1,1,1,1)                           \tag{14}

up to permutation.  A literal six-site coefficient word has squarefree site
degree `(1,1,1,1,1,1)`.  Thus every degree-four exchange is off the physical
EqSystem word grade.  Since the edge toric ideal is homogeneous in total
edge degree, degree-four generators cannot produce the degree-three parent
anti-diagonal without division by an edge cell.  Such localization would be
another unsupported occurrence selector.

## 5. Why “full EqSystem ideal membership” needs care

The checker enumerates all 729 EqSystem words.  On the nine-cell coordinate
subspace, pure words `000000` and `222222` have zero left side but target one.
Their specialized equations are `-1`.  Therefore the target-inhomogeneous
**full** specialized ideal is the unit ideal, and every polynomial—including
the parent anti-diagonal—belongs to it vacuously.

This cannot be used as a lift: the nine-cell packet is an exact guard for the
three rows (6), not a full GHZ source.  A genuine completion must supply the
missing pure anchors rather than use their failure as `1=0`.  The meaningful
tests are consequently:

1. membership in the local physical row ideal (disproved by (8));
2. membership in a fixed word/fine/operation row module (disproved by (7));
   or
3. a source-provenant identity on an actual full completion.

The third possibility is not excluded globally here, but the toric chain
does not construct it: its very first generator is nonzero on the exact guard
and has the wrong physical operation.

## 6. Exact verdict and next datum

Unlabelled toric membership is tautological: adjoining the toric generator
`M0-M1` supplies the desired parent anti-diagonal by definition.  The desired
physical claim is false on the guard:

```text
toric operation       edge-incidence-kernel binomial,
physical operation    coefficient:word (signless hafnian),
toric parent face     M0-M1,
physical parent face  M0+M1.                              (15)
```

The minimum additional datum is an actual source operation whose boundary is
the oriented matching exchange while preserving the word, fine parent, cap
window, and companion rows.  Neither the degree-three/degree-four toric ideal
nor the full unlabelled EqSystem row span provides that operation.

## Scope

This is exact for the rational nine-cell guard, all `3^6` word rows, all
degree-three and degree-four `K6` edge-incidence toric fibres, and the literal
matching path labels.  It does not exclude a new oriented exchange operation
on a larger full-source completion, nor does it prove the missing pure anchors
can be completed.

Run:

```text
python3 computations/verify_c6_nine_cell_toric_exchange_parent_antidiagonal_nonlift.py --mode structural
python3 -O computations/verify_c6_nine_cell_toric_exchange_parent_antidiagonal_nonlift.py --mode full
python3 -I -S computations/verify_c6_nine_cell_toric_exchange_parent_antidiagonal_nonlift.py --mode exhaustive
```

Frozen ledger SHA-256:

```text
967ae124bd1b980010110386590a5bd4fa82f4dfdc086341f7a9f915f6d7deeb
```
