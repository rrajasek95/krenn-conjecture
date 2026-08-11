# A two-block word either reselects the pure anchor or exposes activity

## The complete-cofactor identity

Fix an edge `e=uv` and two distinct colours `k,l`.  Consider the complete
output word

```text
k at u,v;        l at every other site.                    (1)
```

Every perfect matching is in exactly one of two classes.

* If it contains `e`, its contribution belongs to the complete factor

  ```text
  q_e^{kk} H_e^l.
  ```

* If it avoids `e`, both `u` and `v` must be matched into the complementary
  site set.  It therefore contains exactly two endpoint cells of type
  `(k,l)`.

Hence the exact mixed-zero coefficient is

```text
0 = q_e^{kk} H_e^l + R_cross.                           (2)
```

This is a literal partition of the full hafnian row, not a support-shadow
or matching-cardinality inference.

Checker:
`computations/verify_uniform_two_block_word_cofactor_reselection.py`.

## The block-diagonal branch

If every cancellation mate is block-diagonal, then `R_cross=0`.  Localize
the selected cell `q_e^{kk}`.  Equation (2) gives

```text
H_e^l = 0.                                               (3)
```

The pure-`l` target coefficient uses the *same complete cofactor*:

```text
1 = q_e^{ll} H_e^l + R_pure,avoid e.                    (4)
```

Substituting (3) gives `R_pure,avoid e=1`.  Thus some nonzero pure-`l`
matching avoids `e`.  This is the required anchor-safe pure-anchor
reselection.  No comparison of unequal tail classes is needed.

If `H_e^l!=0` while `R_cross=0`, (2) is instead the ordinary localized
source unit.

## The crossing branch

Every term in `R_cross` has exactly two off-diagonal `(k,l)` endpoint
cells.  There are only six ordered ternary types, all covered by the pinned
target-augmented private-site identity:

```text
sum_s Delta_us C_s = -q_u.                              (5)
```

Therefore each nonzero cross cell forces a nonzero determinant/cofactor
product.  If its physical edge leaves the selected anchor union, this is
the immediate off-anchor active landing.  If both cross edges remain in
the union, their typed active products feed the existing complete-exchange,
two-shared migration, and opposite-companion path interfaces.  The theorem
does not claim that (5) alone supplies all four deleted-star ranks.

## Consuming the first transfer debt

For the six-site winding guard of `3c4faa2`, the first unmet full word is

```text
001111.
```

Its existing singleton matching is `P1`, which contains `e=01`.  Inside the
three selected-anchor physical union there are exactly three matching
classes.

* A `P0` mate also contains `01`, so it joins the complete
  `q01_00 H01^11` factor.  If there is no avoiding class, (3)--(4) reselect
  the pure-one matching away from `01`.
* A `P2` mate avoids `01`, so it contains exactly two `01` cross-colour
  cells and enters (5).
* The displayed Hamilton winding mate of the guard already uses a physical
  edge outside the selected anchor union, hence is itself the off-anchor
  landing rather than a residual provenance obstruction.

Thus `001111` does not create another untyped omitted word.  It terminates
at common-class cofactor/reselection or at typed activity/off-anchor escape.
The signless SCC theorem remains necessary only after those typed routes
have been factored into a genuine common tail class.

## Uniform audit

The checker verifies the exact through/avoiding partition through ten
sites, all six ordered ternary colour pairs, and all `72` labelled six-site
avoiding matchings.  It also reloads the frozen physical guard and checks
its three anchor-contained matching classes and its `001111` singleton
coefficient.

## Scope

This is a uniform source-polynomial theorem over an integral domain after
localizing the selected `q_e^{kk}`.  It consumes the first full-row debt and
proves a pure-anchor reselection or an active/off-anchor interface.  The
final conversion of an anchor-contained active determinant to a four-good
overlap remains governed by the already pinned rank/path theorems.

Run

```text
python3 computations/verify_uniform_two_block_word_cofactor_reselection.py
python3 -O computations/verify_uniform_two_block_word_cofactor_reselection.py
python3 -I -S computations/verify_uniform_two_block_word_cofactor_reselection.py
```

Frozen ledger SHA-256:

```text
17e895985a56b5f32a1c2bb30726c3d2199f458d5f0079a5704d4fce5eb08c68
```
