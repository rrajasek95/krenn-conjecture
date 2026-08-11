# A dark Hall unary escape has an exact response-visibility gate

## Result

In the bridge-dark Hall triangle, unary recursion forces a nonzero literal
escape

\[
                     q_{ad}^{00}H^0_{ad}\ne0,
                     \qquad d\notin B.                 \tag{1}
\]

There are two source-valid ways for (1) to become the desired good active
carrier.

1. If a second nonzero pure-zero matching pairs `a` somewhere other than
   `d`, and `a-d` is absent from the two selected diagonal matchings, use
   that matching after deleting `a-d`.  It restores the lost colour-zero
   column at both ends; the two diagonal matchings restore colours one and
   two.  Hence the active internal pair `a-d` has deleted-star ranks
   `(3,3)`.
2. Attach the selected cell `s1(a,1)` to (1).  Every endpoint cell
   `p_i(d,gamma)` gives the literal response term

   \[
       p_i(d,\gamma)s_1(a,1)H^0_{ad}.                  \tag{2}
   \]

   If `d` is outside the two selected `P`-neighbours, `P-d` belongs to none
   of the three selected pure matchings.  The term (2) makes it
   support-active, while those three matchings give deleted-star ranks
   `(3,3)`.  Thus any nonzero `P`-star evaluation at an external escape is
   already a free good active arm.

For the centre escape `d=c`, (2) is automatic: the selected
`p1(c,1)s1(a,1)` contribution is nonzero and lies in the mixed diagonal
word which is one at `c,a` and zero elsewhere.  The complete diagonal zero
row must therefore supply another endpoint-star site or an anchored
correction.

Checker:
`computations/verify_uniform_hall_triangle_bridge_dark_coloured_escape.py`.

## Common-tail proof

The perfect matchings in `H0_ad` are exactly the tails left after deleting
`a,d`.  Multiplying such a tail by `q_ad:00` gives its unary term;
multiplying the same tail by `p_i(d,gamma)s1(a,1)` gives its response term.
This is a literal term-preserving bijection, valid for every residual order.
No division, genericity, or support enumeration is involved.

For the external pair `P-d`, the three selected target matchings avoid that
physical edge: the unary matching uses `P-R`, while the diagonal matchings
use the two normalized `P`-neighbours.  After deleting `P-d`, their three
surviving endpoint columns have target colours `0,1,2` at both ends.
Consequently they are independent even when two physical neighbours
coincide.  The nonzero cofactor in (2) supplies activity.

The internal-pair repair is equally literal.  A second unary matching which
pairs `a` away from `d` avoids the entire edge `a-d`, so it supplies colour
zero at both deleted stars.  This argument stops exactly when `a-d` is a
unary support coloop, or when another selected target matching also uses the
same physical edge and loses a second colour column.

## Sharp boundary

The response attachment is not automatic at an external escape.  On
residual sites

```text
c=0, a=1, b=2, d=4,
pure 0: 03 | 14 | 25,
pure 1: 23 | 45       (holes c,a),
pure 2: 13 | 45       (holes b,c),
```

the complete unary tensor is exactly `X0`, the two displayed diagonal
cofactor monomials are nonzero, and `H0_ab=0`.  The escape `a-d=1-4` is the
unique pure-zero edge at `a`, so deleting it leaves selected ranks `(2,2)`.
Moreover the selected `P` rows occur only at `c` and `b`; both vanish at
`d=4`.  Thus (1) has neither an alternate unary rank repair nor a response
attachment at its external endpoint.

This is a physical common-`q` guard, not a formal assignment of cofactors.
It is deliberately not a full one-bad packet: its omitted mixed response
coefficients are load-bearing.  It proves that the next positive statement
must use one of those complete response mates to break the unary coloop or
to make an endpoint row hit the escape site.  Unary recursion plus selected
diagonal monomials alone cannot do so.

## Exact remaining interface

The bridge-dark route is therefore reduced to

\[
\boxed{\begin{array}{c}
\text{a repaired active internal edge, or a free active }P\!-
d\text{ arm},\\
\text{or a unary/multiply-used coloop at }a\!-
d\text{ with both }P\text{ rows zero at }d.
\end{array}}
\]

The last line is the precise coloured-response coupling still required; it
is not another unrestricted Hall family or support layer.

Run

```text
python3 computations/verify_uniform_hall_triangle_bridge_dark_coloured_escape.py
python3 -O computations/verify_uniform_hall_triangle_bridge_dark_coloured_escape.py
python3 -I -S computations/verify_uniform_hall_triangle_bridge_dark_coloured_escape.py
```

Frozen ledger SHA-256:

```text
e55dd3b1b74a68fa6d6e881083c980e5010960436584f3f37048653632a370cb
```
