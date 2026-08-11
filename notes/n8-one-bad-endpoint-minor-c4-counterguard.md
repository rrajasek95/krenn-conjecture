# Endpoint minors have a cofactor-invisible branch

Date: 2026-08-11

Checker:
`computations/verify_n8_one_bad_endpoint_minor_c4_counterguard.py`

## Exact verdict

The four genuine common-`q` response rows

\[
 p_i s_j q^{[2]}=\delta_{ij}X_i,\qquad i,j\in\{1,2\},
\]

do not force either proportional endpoint stars or an active alternating
`C4`.  There is a third exact branch: a coloured-port minor can be nonzero
while its corresponding common hafnian cofactor is identically invisible at
the reference colour.

This is the sharp limitation of the private-site formula from `14b8b07`.
For two endpoint labels and a fixed residual word it reads

\[
 p_uH_q-q_uH_p=\sum_{s\ne u,v}
       (p_uq_s-q_up_s)C_s.
\]

A nonzero abstract endpoint minor does not activate the right side unless
the same residual word supports `C_s`.

## Literal common-q packet

On residual sites `0,...,5`, take

```text
q  = 24:11 + 35:11 + 05:22 + 14:22,
p1 = e1@0 + e1@5,       p2 = e2@2,
s1 = e1@1,              s2 = e2@3.
```

Perfect-matching expansion over `Q` gives exactly

```text
p1*s1*q^[2] = X1,       p1*s2*q^[2] = 0,
p2*s1*q^[2] = 0,        p2*s2*q^[2] = X2.
```

The two coloured-port matrices have rank two.  Their nonzero unordered
minors are

```text
P endpoint: ((0,1),(2,2)) = +1,
            ((2,2),(5,1)) = -1,
Q endpoint: ((1,1),(3,2)) = +1.
```

For both orientations of each minor, the checker computes the literal common
cofactor after deleting the endpoint and alternate site.  There are six
oriented tests.  In every one, the cofactor is either zero or its only word
has the wrong colour at the reference site.  Thus the number of compatible
alternating-`C4` terms is exactly `0/6`.

This is not cancellation in an abstract cofactor module: all cofactors come
from the displayed single physical quadratic `q`, with all site, colour, and
matching labels retained.

## Why neither advertised endpoint conclusion follows

The endpoint rows are not proportional because both port matrices have rank
two.  The first determinant obstruction is not active because all nonzero
minors are cofactor-invisible.  On the unreduced packet, the canonical
permanent-null cap moreover has the literal defect

```text
R^[2] q = 2 * [111211].
```

No displayed physical arm is doubly good, and both defect matchings use the
inactive arm `P5`.  Hence this packet does not enter the certified active
curved-OO gate through the proposed first-`C4` route.

## Exact missing input

The packet is the committed eight-of-nine frontier.  It has

```text
q^[3] = 0
```

instead of the unary target `X0`; equivalently the sole failed full-nine
coefficient is the pure `00` row.  Also, `e1@5` in `p1` is invisible to all
four responses: deleting it preserves the responses and removes the cap
defect.  Therefore this is not a full one-bad packet and not a Krenn
counterexample.

The source-valid dichotomy must use at least one of those two missing
mechanisms.  A correct next statement is:

```text
proportional endpoint rows
  OR active determinant/cofactor route
  OR cofactor-invisible minors removable by a source modification.
```

Eliminating the third branch in a minimum-support full packet requires the
unary top/common-cofactor provenance; it does not follow from crossed-zero
and the two diagonal response rows alone.

## Reproduction

```sh
python3 computations/verify_n8_one_bad_endpoint_minor_c4_counterguard.py
python3 -O computations/verify_n8_one_bad_endpoint_minor_c4_counterguard.py
```

The checker pins both the private-site identity and the existing exact
common-`q` response packet, reconstructs all four response tensors, computes
the complete endpoint-minor lists and all six oriented compatible cofactors,
and rechecks the raw cap/OO failure data.
