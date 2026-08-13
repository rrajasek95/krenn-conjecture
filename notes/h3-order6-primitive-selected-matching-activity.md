# The primitive Cartan interference closes all but a double coloop

## Corrected signed activity theorem

The literal primitive `A0^2` polynomial has signed support `167`, not `79`.
The old verifier accidentally used unary `+Counter`, which retained the 79
positive coefficients and discarded 88 negative ones.  After the signed
correction, exactly two of the 90 direct-free pure matching tori carry a
nonzero primitive coefficient:

```text
02 | 13 | 47 | 56     -> -4,
02 | 16 | 35 | 47     -> -2.
```

The first is the universal selected-activity normal form.  Let `u` be a
candidate target-full site outside the selected `S`-neighbour of one bright
matching.  If `u` is not that matching's `P`-neighbour, physical relabelling
fixing `P,S` sends

```text
u -> 0,       neighbour(u) -> 2,
neighbour(S) -> 4,          neighbour(P) -> 5,
```

and the remaining two sites to `1,3`.  The selected matching becomes
`02|13|47|56`, so the physical primitive Cartan coefficient is `-4`.
The global bright-colour symmetry gives the same theorem from either selected
bright matching.

Checker:
[`verify_h3_order6_primitive_selected_matching_activity.py`](../computations/verify_h3_order6_primitive_selected_matching_activity.py).

## Complete packet consequence

The earlier selected-arm theorem and this activity theorem split all 461,700
selected matching/full-site packets exactly:

```text
selected target-full arm repairs the quotient       310,500
selected pure-matching Cartan activity               150,930
double-coloop residual                                   270.
```

Thus 461,430 packets now produce the rank-`(3,3)` active overlap directly.
The former 151,200 activity frontier has collapsed to 270 packets.

## Exact residual

Every residual packet has one form.  The two bright matchings share both
their selected endpoint neighbours:

```text
S--n in colours 1 and 2,
P--p in colours 1 and 2,
F={n,p}.
```

The remaining four internal sites carry two-edge tails.  There are only two
physical orbit types:

```text
same two-edge tail                         90 packets,
tails differ by one alternating C4        180 packets.
```

The primitive selected-matching coefficient is dark here for a transparent
reason: either target-full candidate is the `P`- or `S`-coloop of both bright
matchings.  The next row must couple the two endpoint-colour channels or
produce a dependence; searching the other 35 general incidence orbits is no
longer necessary.

This is the interference pattern suggested by the Cartan construction.  A
single matching channel is active except when two colours align on the same
two endpoint coloops.  Only their residual same-tail/C4 phase relation can
still cancel.

## Scope

This closes selected physical activity after the local Cartan comparison.  It
does not yet eliminate the 270 double-coloop packets, prove uniform entry from
an arbitrary minimum counterexample, or construct the inactive `Yw -> W`
comparison.

Verification:

```text
python3 computations/verify_h3_order6_primitive_selected_matching_activity.py
python3 -O computations/verify_h3_order6_primitive_selected_matching_activity.py
python3 -I -S computations/verify_h3_order6_primitive_selected_matching_activity.py
```

Frozen ledger SHA-256:

```text
9578425a3b572da1f2809f0ae353b8dc7d955b9ec52f01d916b78b7bba5e6e63
```
