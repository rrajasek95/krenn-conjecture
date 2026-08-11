# The minimal torus-opposing pair is killed by two unary-top rows

Date: 2026-08-11

Checker:
`computations/verify_n8_one_bad_axis_pure_opposing_pair_top_elimination.py`

## Exact coefficient theorem

Start with the arbitrary fifteen-cell pure-zero chart from `260bb94`, keep
all old coloured q and endpoint-star coefficients symbolic, and adjoin only
the minimal torus-opposing pair isolated by `9913c00`:

```text
x = q01:02,       y = q34:02.
```

The checker expands the complete unary top and all four response tensors.
The pair changes seven top words and `2,2,2,1` words in response sectors
`11,12,21,22`, respectively.  No abstract row or support shadow is used.

One mixed unary word is the single monomial

```text
q^[3] @ 021111 = A*B*x.
```

The colour-1 diagonal response anchor is `A*B*p0*s1=1`, so `A` and `B` are
units.  The required mixed top coefficient is zero; hence `x=0`.

After setting `x=0`, every one of the nine old arbitrary-pure top equations
is unchanged.  The exact ideal certificate of `260bb94` therefore still
gives

```text
z03*z12*z45 = 1.
```

In particular `z12` is a unit.  A second mixed unary word is

```text
q^[3] @ 200022 = C*y*z12.
```

The colour-2 diagonal anchor makes `C` a unit, so `y=0`.  Thus the complete
top equations eliminate both members of the opposing pair; the response
rows need no additional clean/curved routing.

## Consequence and scope

The character circuit in `9913c00` is a genuine obstruction to deriving
pure-chart accessibility from axis purification alone, but it is not a
coefficient-feasible counterpacket on this chart.  Literal source equations
supply precisely the non-toric carrier elimination that the weight audit
could not.

This theorem allows all fifteen pure `z_ij`, the old four coloured q cells,
and the pinned five star coefficients, but exactly two new mixed q cells.
Additional mixed carriers can create cancellation mates for the two private
top words and are not covered.  No broader support conclusion is claimed.
