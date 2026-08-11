# The opposite Hall-star orientation has one unary-bridge crossed row

## Result

In the opposite-side residual of the Hall-star theorem, normalize the
selected diagonal holes as

```text
colour 1:  p1(c), s1(a),
colour 2:  p2(b), s2(c).
```

Let `M0` be a selected pure-zero matching in the genuine unary top.  If
`M0` uses the residual edge `a-b`, the crossed `21` row contains the literal
nonzero product

\[
               p_2(b,2)s_1(a,1)(M_0/(a b)).           \tag{1}

The crossed `12` centre-centre product `p1(c)s2(c)` is zero by
site-square-freeness.  Thus the apparently silent opposite orientation has
one load-bearing crossed row, exactly as suggested by the selected unary
edge.

Keeping complete coefficients rather than one matching term gives a sharp
family reduction:

1. if the pure-zero two-hole cofactor pairing is nonzero on some effective
   leaf pair `(a,b)`, the complete `21` coefficient has a nonzero bridge and
   requires a cancellation mate;
2. a mate outside the selected centre/leaf sites exposes an off-anchor
   off-diagonal endpoint cell and enters the certified good-active route;
3. if no free mate occurs, the entire coefficient is one three-block
   triangle lock; and
4. if no effective leaf pair has a bridge, the pure-zero cofactor pairing
   vanishes on the product of the two effective leaf spans.

The checker is
`computations/verify_uniform_multisite_hall_star_triangle_bridge_boundary.py`.

## Literal source pivot

On residual sites `c,a,b,d,e,f`, choose

```text
M0 = ab | cd | ef.
```

Restoring the two outer endpoints gives the three selected pure matchings

```text
Q0: outer-direct | ab | cd | ef,
Q1: p-c | s-a | (two colour-1 residual edges),
Q2: p-b | s-c | (two colour-2 residual edges).
```

For the output word with outer colours `(2,1)`, residual colours `1` at
`a`, `2` at `b`, and `0` elsewhere, (1) is a full perfect matching.  The
checker constructs the physical eight-site cells and verifies that it is
the unique selected-support term with coefficient one.  Swapping the outer
labels gives the `12` candidate, but both stars then occupy `c`, so no
matching exists.

This selected-support calculation is only the source label for the general
identity.  In an arbitrary source, write

\[
 T_{ab}=p_2(b,2)s_1(a,1)
       [q^{[h-1]}]_{U\setminus\{a,b\},0}.              \tag{2}

The bridge branch is `T_ab!=0`; the bridge-dark branch is the exact
statement that (2) vanishes for every pair of effective leaves.  It is not
the weaker assertion that one chosen matching term is absent.

## Free mate or three-block lock

Fix a nonzero bridge word.  Expand its complete crossed coefficient by the
sites of `p2` and `s1`.  Any term using

```text
p2(u) with u outside {b,c},
or s1(v) with v outside {a,c},
```

contains an off-diagonal endpoint cell on a physical pair outside the three
selected anchors at that endpoint.  That pair has deleted-star ranks
`(3,3)` by the selected-matching argument, and the private-site theorem
supplies the exact active-minor/free-companion alternative.

If no such term occurs, the possible site pairs are

```text
(b,a), (b,c), (c,a), (c,c).
```

The last repeats `c` and vanishes.  Consequently the whole source row is

\[
                   B_{ab}+A_{R c}+A_{P c}=0.           \tag{3}

Here `B_ab` is the unary bridge, while the other two terms are corrections
on the selected diagonal anchor edges.  Equation (3) is genuinely
coefficient-feasible as a scalar relation—for example `(2,-3,1)`—so the
crossed row alone does not close it.

## Exact remaining obligation

The opposite Hall-star normal form is therefore no longer an unspecified
site collision.  Its two residuals are

```text
bridge-dark:  T|_(effective leaf1 x effective leaf2) = 0,
triangle lock: B_ab + A_Rc + A_Pc = 0.
```

A proof of affine line-hitting must use the unary and diagonal equations to
exclude the bridge-dark cofactor block or straighten the two anchor
corrections in (3).  A free term already routes to the pinned active-pair
machinery.  This theorem uses complete source coefficients and arbitrary
multisite support; it is not a family-subset census and does not assert a
full one-bad counterexample.

Run

```text
python3 computations/verify_uniform_multisite_hall_star_triangle_bridge_boundary.py
python3 -O computations/verify_uniform_multisite_hall_star_triangle_bridge_boundary.py
python3 -I -S computations/verify_uniform_multisite_hall_star_triangle_bridge_boundary.py
```

Frozen ledger SHA-256:

```text
eea4c3d2bd81eecdfc228c59f0c72b1422487b331a5ff774f7b59154cf06a124
```
