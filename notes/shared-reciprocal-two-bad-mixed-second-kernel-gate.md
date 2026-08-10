# The minimal second tilted kernel loses a bright class

## 1. The only private-pivot collision

Continue in the repaired primitive-cycle chart.  Keep the five nonzero
parameters

```text
z=04:tt, y=14:at, b=04:at, w=13:aa, v=03:ta.
```

The three load-bearing cofactors are

```text
K2 = CCCC +(y+bw) AAAT +(vy+zw) TAAT,
K3 = (z+y) TAAT +b AAAT,
K4 = AAAA +(w+v) TAAA.                                (1)
```

The old eleven monomial columns and the three `K3` columns give the
rank-14 chart.  With all selected cells nonzero, the first possible second
relation is the collision

```text
e_a@3 K3 = b e_t@4 K4.                                (2)
```

Direct `a`- and `c`-bright purity and (2) force

```text
v=-w, y=-z, bw=z.
```

Substitution into the remaining `TAAT` coefficient of `K2` gives

```text
vy+zw = 2zw != 0.                                     (3)
```

Thus over characteristic zero no second kernel exists on the old support.
The factor `2` is the two same-sign matching routes, not a numerical-grid
artifact.

## 2. Smallest new support and its private rows

The only unused physical matching for the `TAAT` word of `K2` is

```text
01:ta * 34:at.
```

It requires two new cells; one new coordinate cannot contribute a matching
monomial.  Write their weights `r,s`.  Equation (3) forces

```text
rs=-2zw.                                               (4)
```

This does create the second independent kernel.  But the two new cells
cross with the already present `01:cc` and `34:cc` cells.  Literal matching
expansion gives

```text
K2 = CCCC +s CCAT +r TACC.                             (5)
```

After inserting `c` at hole `2`, the pure word and both mixed words in (5)
occur in the same unique column `(2,c)`.  The pure row forces that column's
coefficient to one, while the two private mixed rows force `r=s=0`,
contrary to (4).  Hence

```text
X_c notin im(Phi).                                     (6)
```

This is the exact determinant/private-row exclusion for the minimal second
kernel support.

## 3. Rational two-kernel packet

For reproducibility choose

```text
z=1, y=-1, b=1, w=1, v=-1, r=1, s=-2.
```

The literal cofactors are

```text
K0 = AACC -2 AAAT,
K1 = TACC -2 TAAT,
K2 = CCCC -2 CCAT +TACC,
K3 = AAAT,
K4 = AAAA.                                             (7)
```

The cofactor map has rank `13` and exactly the two independent kernels

```text
U=e_t@0-e_a@1,
V=e_a@3-e_t@4.                                         (8)
```

Adjoining every product `P*U'*V'*q` for the full two-dimensional kernel
raises the rank to `24`, but `X_t` remains outside.  In fact the only
`tt` cell is `04:tt`, while the target components of (8) occur at sites
`0` and `4`; the residual edge overlaps them and cannot appear in a pure
product monomial.

The packet has `X_a` in `im(Phi)` but not `X_c` or `X_t`.  It is therefore
not a local seed for the two-bad source and not a Krenn counterexample.

## 4. Scope and next boundary

This closes the smallest second-kernel realization inside the canonical
repaired primitive-cycle chart.  It does not exclude a larger path-switch
network which mates the two private words in (5), nor a different
multi-centre bright chart.  Any true local seed must now repair both private
bright rows while retaining two kernel directions and a `tt` residual edge
disjoint from their target supports.

## 5. Reproduction

```sh
uv run python computations/verify_shared_reciprocal_two_bad_mixed_second_kernel_gate.py
uv run python -O computations/verify_shared_reciprocal_two_bad_mixed_second_kernel_gate.py
```

Both modes reproduce

```text
8d5f4c3d0b076402176048178e44701f5b28f346c6d9108f096d060897c2f39c
```
