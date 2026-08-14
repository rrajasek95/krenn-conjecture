# The canonical direct-free feature selector is quadratic, but still relative

## Exact indexing correction

The canonical `h=3` direct-free response packet consists of the 90 perfect
matchings of

```text
P,S,0,1,2,3,4,5
```

which avoid `PS`.  Every such matching has unique partners `p` of `P` and
`s` of `S`; deleting `Pp` and `Ss` leaves a perfect matching of the other
four numbered sites.  Hence there is a canonical bijection

```text
direct-free matching  <->  (ordered endpoints p,s, residual K4 matching).
```

This is the parameter `h=2` occurrence set in the uniform Gram checker:

```text
|Omega_2|=90.
```

The parameter `h=3` Gram set has 840 occurrences and belongs to the next
order.  Consequently, for

```text
f=P0|S1|23|45,
```

the relevant nonlinear feature identity is quadratic:

```text
Q_(0,1) X_23 = Q_(0,1) X_45 = e_f.                 (1)
```

Within the ordered-endpoint fibre `(0,1)`, either residual edge forces its
complement.  The exact supports are

```text
Q_(0,1): 3,    X_23: 12,    X_45: 12,    e_f: 1.
```

Checker:
[`verify_h3_direct_free_feature_selector_index_gate.py`](../computations/verify_h3_direct_free_feature_selector_index_gate.py).

## Why this does not shorten the physical cube automatically

The four-edge Euler formula is

```text
E_P0 E_S1 E_23 E_45(R)=f.
```

Coefficientwise, (1) is the same top projector because

```text
Q_(0,1)=E_P0 E_S1
```

on occurrences and one tail edge forces the other after that endpoint
selection.  Physically, however, the four proper faces remain distinct:

```text
P0:15,    S1:15,    23:12,    45:12.
```

The endpoint fibre `Q_(0,1)` is itself the selected response block whose
termwise PP lift is open, and `X_23=X_45` is false before restricting to
that fibre.  Replacing the four labelled operators by the quadratic
indicator therefore forgets the endpoint product-rule faces and the two
separate tail reinsertion labels.  The exact relative-carrier dual from the
Boolean-cube audit still applies.

This also separates two uses of the word “cubic.”  The physical association
projector is cubic in the endpoint adjacency operator; the feature selector
for the 90-term canonical packet has degree two.  The cubic feature monomial
from the uniform Gram theorem acts on the distinct 840-occurrence packet.

## Proof consequence

The nonlinear Gram-feature escape is real, but at canonical `h=3` it lands
precisely on the already isolated interface:

1. construct the selected endpoint-fibre comparison with its `P0/S1`
   faces;
2. make the residual restriction/reinsertion maps chain-natural; and
3. retain the pointed carrier rather than killing it in `H0`.

Thus the feature algebra supplies no new cap or response-to-`AugP2` arrow.
It gives a smaller coefficient formula for the same pointed class.
