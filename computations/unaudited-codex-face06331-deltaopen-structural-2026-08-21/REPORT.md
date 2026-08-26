# k5 full interior `0:63:31`, branch `d1-d2 != 0`

Status: **UNAUDITED exact three-mode structural PASS; no solver launched**.

Let

```
delta = d1-d2,
K = a2*b5^2*d1-a2*b5^2*d2+a5*b5*d1+a5*b5*d2-b5^2-2*b5+1.
```

Raw row 8 solves exactly as `a1=-K/delta`.  Fraction-free substitution into
the other fifteen literal rows introduces no denominator except `delta`.
The transformed live product correctly retains `K` (the numerator of `a1`),
`delta-K*d1` (the numerator of `1+a1*d1`), and the `delta` guard.  Its
expanded form has 41,414 terms.

The shortest new irreducible row is raw 9 (`t_123`), with nine terms and
degree six.  Put

```
P = b3*d4-b4*d3,
Q = b3*d4+b4*d3,
W = b3^2*b5^2+2*b3*b4*b5-b4^2.
```

It has the exact split

```
raw9 = P*(a3*b4+a4*b3*b5^2) - a5*b3*b4*b5*Q + W,
Q = 2*b4*d3 + P.
```

Thus `P!=0` gives a linear solve for `a3` (with `b4` already live), while
`P=0` leaves the four-term consistency row

```
-2*a5*b3*b4^2*b5*d3 + b3^2*b5^2 + 2*b3*b4*b5 - b4^2 = 0.
```

No component is claimed empty.  Standard, `-O`, and isolated `-I -S` runs
all return logical digest
`22b78f4e2c7d6333c89244b96c74f65d730b782e211e2ed6397359e3606d6dbe`.
