# Every outside strict-shore endpoint component reaches the four-good wedge

## Result

Work in the opposite-shore strict `K2,2` chart.  Besides the unary direct
arm, the chosen diagonal target matchings use the four residual ports
`0,1,2,3` at each outer endpoint.  Thus the remaining ports `4,5` give
physical arms outside the selected anchor union.

Let `z=e_i@u` be one occupied component of one endpoint row, with
`u in {4,5}`.  Hold the common `q` and both opposite endpoint rows fixed and
form its complete two-response column

\[
       \mathcal C(z)=\bigl(zs_1q^{[h-1]},zs_2q^{[h-1]}\bigr)
\]

for a `p` component, or the transposed column for an `s` component.  Then:

1. if `C(z)=0`, deleting `z` is an exact finite joint-kernel modification;
2. if `C(z)!=0`, one literal coefficient and then one literal matching
   summand is nonzero, so the outside arm has an active cofactor witness;
3. pairing that arm with either selected opposite-colour core arm at the
   same outer endpoint gives a distinct-head four-good active wedge.

Consequently support minimality excludes the first alternative.  Every
occupied outside component enters the already certified four-good interface.
If its pure diagonal target coefficient is nonzero, it is additionally a
new effective Hall hole, so the conclusion also refines the requested
effective-hole alternative.

Checker:
[`verify_uniform_hall_k22_outside_endpoint_component_wedge.py`](../computations/verify_uniform_hall_k22_outside_endpoint_component_wedge.py).

## Exact complete-column argument

Changing one component of `p_i` affects exactly the complete rows `i1` and
`i2`; the unary top and the other three responses do not depend on it.
Therefore

```text
B(z,s1)=B(z,s2)=0
    => B(p_i-z,sj)=B(p_i,sj),  j=1,2,
```

by bilinearity.  This is an exact deletion, not a tangent statement.  The
same proof applies to an `s_i` component after transposing the two endpoints.
Because the arm lies outside the selected anchor union, deleting it also
preserves every chosen anchor.

If the complete column is nonzero, choose one of its nonzero output
coefficients.  That coefficient is a finite sum of literal matching
monomials, so over the source field at least one summand is nonzero.  Removing
the outside arm from that matching leaves its nonzero complete cofactor.
This supplies the activity witness without assuming termwise uniqueness or
restricting the rest of the source support.

## Why the selected opposite arm is four-good

Use the five selected pure matchings

```text
Q0 : PS | 01 | 24 | 35,
Q1 : P0 | S1 | 23 | 45,     P3 | S2 | 01 | 45,
Q2 : P2 | S0 | 13 | 45,     P1 | S3 | 02 | 45.
```

The outside arm `P-u` (or `S-u`) belongs to none of them, so all three
colour columns survive at both deleted endpoints.  For a selected
opposite-colour arm, deleting its first core matching removes one column,
but the second disjoint core matching of the same colour restores it.  The
unary and the other diagonal colour supply the remaining two rows.  Hence
both physical pairs have deleted-star ranks `(3,3)`.

At their common outer endpoint the outside component has head `e_i`, while
the selected mate has head `e_j`, `i!=j`.  Their `2 x 2` minor is a nonzero
coordinate minor.  The checker audits both outer endpoints, both colours,
both outside ports, and both possible opposite-colour core mates: `16`
source-labelled wedges, all with ranks `(3,3,3,3)`.

## Scope

This closes the endpoint-support gap identified after the strict terminal
return: components outside the four displayed K4 shore ports cannot be
unmatched lock columns at a support-minimal source.  It does not classify a
new component on an already displayed core port, and it does not reprove the
downstream curved/full-nine overlap theorem.

Run

```text
python3 computations/verify_uniform_hall_k22_outside_endpoint_component_wedge.py
python3 -O computations/verify_uniform_hall_k22_outside_endpoint_component_wedge.py
python3 -I -S computations/verify_uniform_hall_k22_outside_endpoint_component_wedge.py
```

Frozen ledger SHA-256:

```text
70577f179dc8a789c1857625764519f820d086ed2079bd0180f7ecb4b168eac4
```
