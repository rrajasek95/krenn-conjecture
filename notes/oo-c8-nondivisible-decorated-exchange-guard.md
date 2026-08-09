# The 12 nondivisible Ward profiles are decorated exchange guards

## Exact verdict

The proposed `2x2` C4 exchange does not uniformly close the 12 profiles whose
active leader does not divide the pure anchor monomial.

- Seven profiles have one physical C4, but their missing ratio also changes a
  colour cell on a physical edge common to both matchings.
- Two profiles have one C6 and the same common-edge colour-cell obstruction.
- Two profiles have two disjoint C4 components and no common-edge change.
- One profile has one C8 and no common-edge change.

Thus only three profiles are pure symmetric-difference-cycle problems, and
even those require a `C4+C4` or `C8` compound relation rather than the single
two-edge exchange proposed for all 12.  The other nine require a genuinely
decorated common-edge colour transport in addition to any cycle minor.

This classifies the fixed sparse regressions.  It does not rule out a larger
full-nine identity that supplies the missing colour transport.

## Census

The exact physical cycle census is

```text
C4       7
C4+C4    2
C6       2
C8       1
```

Nine profiles have exactly one common physical matching edge whose endpoint
colour cell changes; three have none.  Keeping the support-variable location
of every active-only and pure-only factor gives four signatures:

```text
count  cycles  changed common edges  active-only                 pure-only
7      C4      1                     common recolour              cycle + common recolour
2      C6      1                     common recolour              cycle + common recolour + cycle
2      C4+C4   0                     exchange cycle               three exchange-cycle factors
1      C8      0                     exchange cycle               three exchange-cycle factors
```

Unsigned physical matching incidence would merge data that the source
coefficient equations distinguish.

## Smallest decorated guard

Take

```text
support = 03:11, 15:00, 15:11, 67:11
mixed word = 10022011.
```

The selected and pure matchings are

```text
M_active = 02|15|34|67,
M_pure   = 03|15|24|67.
```

Their physical symmetric difference is the C4

```text
02,34  <->  03,24.                                      (1)
```

But the common physical edge `15` uses different source cells:

```text
M_active uses 15:00,
M_pure   uses 15:11.                                    (2)
```

In support-mask notation,

```text
active mask     = 10 = (15:00)(67:11),
pure mask       = 13 = (03:11)(15:11)(67:11),
active-only     = 15:00,
pure-only       = (03:11)(15:11).
```

A minor using only the four physical edges in (1) does not see the ratio in
(2).  This is the smallest missing provenance cell.

## Exact two-parameter guard

Set the four displayed support weights to

```text
(03:11, 15:00, 15:11, 67:11) = (2,x,5,7).
```

The checker compares `x=3` and `x=11`.  In both specializations:

- the two rank-one direct arms are unchanged;
- all four deleted-star ranks remain three;
- curvature remains `-1`;
- the physical C4 cells and their products are unchanged; and
- the pure coefficient remains `70`.

But the selected mixed coefficient changes from `21` to `77`.  Hence the
rank-one arms, good-star ranks, curvature, physical C4 data, and pure anchor
do not determine the active coefficient.  A proof must use a full-nine row
that transports `15:00` to `15:11`, or an equivalent source-labelled
decorated exchange; a physical matching minor alone is insufficient.

These rational packets are structural/source-relaxation guards, not exact
GHZ sources: their selected mixed coefficient is nonzero.  Their purpose is
to identify the hypothesis missing from the proposed local exchange lemma.

## Determinant-clearing scope

On any fixed torus support, one can cross-multiply arbitrary nonzero
monomials.  For the guard,

```text
(15:00) * M_pure = (03:11)(15:11) * M_active.
```

That tautological chart identity recovers the known sparse monomial unit
certificate.  It is not a uniform source theorem: its multiplier explicitly
uses the remote decorated cells in (2), and future cancellation mates change
both coefficient polynomials.  The desired all-source statement must derive
those multipliers from the source equations rather than read them from a
fixed monomial support.

## Reproduction

```text
python3 computations/verify_oo_c8_nondivisible_exchange_guard.py
python3 -O computations/verify_oo_c8_nondivisible_exchange_guard.py
```
