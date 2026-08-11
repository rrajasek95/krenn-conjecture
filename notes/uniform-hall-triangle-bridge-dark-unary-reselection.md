# A bridge-dark Hall leaf has an active unary escape

## Result

Let `U` be the even residual site set and let `Z=(q_uv^{00})` be the
pure-zero slice of the common internal quadratic.  Write

\[
 H^0_{uv}=\operatorname{haf}(Z|_{U\setminus\{u,v\}}).
\]

In the exact unary target `q^[h]=X0`, the pure-zero coefficient is one.
Expansion at a fixed site `a` gives the literal source identity

\[
             1=\operatorname{haf}(Z)
              =\sum_{d\ne a}q_{ad}^{00}H^0_{ad}.       \tag{1}
\]

Consequently, if the Hall-triangle bridge is dark on two effective leaf
sets,

\[
                    H^0_{ab}=0\qquad(a\in A,b\in B),  \tag{2}
\]

then every `a in A` has an **active unary escape**

\[
       q_{ad}^{00}H^0_{ad}\ne0\quad\hbox{for some }d\notin B. \tag{3}
\]

Over the integral coefficient domain, both factors in (3) are nonzero.
Choose a nonzero perfect-matching monomial in `H0_ad` and adjoin the edge
`a-d`.  This reselects the pure-zero target matching through an edge which
leaves the opposite effective leaf set.  Thus bridge-darkness is a cut
escape condition, not a dead unary leaf.

Checker:
`computations/verify_uniform_hall_triangle_bridge_dark_unary_reselection.py`.

## Exact matching proof

The perfect matchings of `U` partition according to the mate `d` of `a`.
The block with mate `d` is exactly

```text
q_ad^00 times the perfect matchings of U minus {a,d}.
```

This proves (1) without division or a genericity assumption.  Under (2),
all summands indexed by `B` vanish.  Since their total is one, at least one
remaining summand is nonzero.  A nonzero cofactor sum has a nonzero
matching monomial, giving the claimed source witness.  The checker audits
the disjoint matching partition for residual sizes `2,4,6,8,10`.

The argument applies one leaf at a time.  It does not assert that the
separately selected escapes for all leaves occur in one common matching.
That stronger simultaneous selection would need an additional Hall or
source-exchange argument.

## Why the unary row does not force a bridge

The conclusion cannot be strengthened to `H0_ab!=0` using the unary target
and selected diagonal monomials alone.  On residual sites

```text
c=0, a=1, b=2, and 3,4,5,
```

take the common internal support

```text
pure 0: 03 | 14 | 25,
pure 1: 23 | 45          (selected cofactor with holes c,a),
pure 2: 13 | 45          (selected cofactor with holes b,c).
```

Give every displayed cell coefficient one.  Literal expansion has exactly
one nonzero six-site output:

```text
q^[3] : 000000 -> 1.
```

Thus the **complete** unary tensor is `X0`, and both displayed diagonal
cofactor monomials are nonzero.  Nevertheless

```text
H0_ab = H0_12 = 0,
```

because the complement `{0,3,4,5}` has no pure-zero perfect matching.  The
selected unary matching instead uses the escapes `a-4` and `b-5`.

This guard is deliberately not a one-bad packet.  Its `11`, `22`, and
crossed `21` cofactors have additional mixed outputs.  Those complete
response rows—not the unary equation again—are the next load-bearing
input.  In particular, a proof must couple the escape matching to the
diagonal/crossed rows or use the non-dark three-term lock

\[
                    B_{ab}+A_{Rc}+A_{Pc}=0.
\]

## Scope

This is a uniform, source-labelled hafnian recursion theorem and a sharp
six-site guard.  It neither closes the bridge-dark Hall triangle nor gives
an arbitrary-star concentration.  It replaces the vague dark alternative
by the exact condition that every effective leaf has an active unary edge
escaping the opposite set; the remaining theorem must transport that edge
through the other four response rows.

Run

```text
python3 computations/verify_uniform_hall_triangle_bridge_dark_unary_reselection.py
python3 -O computations/verify_uniform_hall_triangle_bridge_dark_unary_reselection.py
python3 -I -S computations/verify_uniform_hall_triangle_bridge_dark_unary_reselection.py
```

Frozen ledger SHA-256:

```text
6c58ee37e2e6ea798df02e9c25dc535ec4e2e8e9af8cb78acfd4dabe25522fdf
```
