# OO colour-raising Ward identity: direct-coordinate provenance guard

## Verdict

The localized site-`r` colour operation `2 -> 1` is an exact Ward identity,
but it does **not** transport the active mixed `E_12` Hessian through its own
physical half-edge column.  On every one of the 47 main active profiles, the
same-column Ward coefficient is zero.  The differentiated diagonal term is
instead supplied by the existing direct `pr:(1,1)` cell acting on the absent
off-diagonal direct coordinate `pr:(1,2)`.

Consequently the Ward identity relates two mixed full-nine rows.  All four
corners of the common-word face are mixed, so its target derivative is zero;
no diagonal-anchor constant occurs.  A bare localized Ward/Koszul operation
therefore does not repair the pure/mixed grade gate found by the star-inverse
audit.

This is a counterguard to that proposed proof step, not an exact GHZ source
or a counterexample to Krenn.

## Universal source identity

At `r=4`, index a physical half-edge column by

```text
alpha = (partner site, partner endpoint colour).
```

Write `a_(j,alpha)` for the source cell with colour `j` at `r`.  Once the
`r` edge is removed, let `C_alpha(w)` be the matching cofactor for the
remaining six sites and residual word `w`.  The complete source coefficient
is

```text
F_j(w) = sum_alpha a_(j,alpha) C_alpha(w).                 (1)
```

This includes the direct neighbour `p`, every deleted-star neighbour, and
coordinates that vanish at the sparse packet.  The column-local source Ward
derivation

```text
W_(2->1) = sum_alpha a_(1,alpha) d/d a_(2,alpha)           (2)
```

satisfies, identically and matching by matching,

```text
W_(2->1) F_2(w) = F_1(w).                                 (3)
```

Thus good-star inversion cannot change the physical column in (2).  Any
column change must come from a separate source-provenant relation.

## Canonical exact ledger

For the canonical profile

```text
support = 01:21, 03:11, 17:11, 56:11
face    = 12111, 10111, 02111, 00111
```

fix `p=1` and `q=0`, and take the alternating second difference on the face.
Only three of the 21 universal cofactor columns survive:

```text
nabla^2 C_(p,1) = -m
nabla^2 C_(3,0) = -m
nabla^2 C_(3,2) =  m
m = x_17:11 x_56:11                              (mask 12).
```

After specializing the actual source star, the complete rows are

```text
nabla^2 F_2 = a_(2,(3,2)) C_(3,2) =  m,
nabla^2 F_1 = a_(1,(p,1)) C_(p,1) = -m.                   (4)
```

The tempting transport would differentiate the active first term in (4),
but

```text
a_(1,(3,2)) = A_r3(1,2) = 0.                              (5)
```

Instead, (3) obtains `-m` from

```text
A_pr(1,1) * d/d A_pr(1,2)                                (6)
```

acting on the *formal absent-coordinate term*
`A_pr(1,2) C_(p,1)` of `F_2`.  Equation (6) is the smallest surviving Ward
provenance grade.  Omitting absent incident cells, or differentiating only
the selected `K` block, misses it and gives an unsound transport statement.

The deleted-star pivot determinant is one throughout this calculation, so
determinant clearing does not alter (5) or (6).

## Why no anchor appears

Let `R_j(w)=F_j(w)-Delta_j(w)` be the full source equation.  From (3),

```text
W_(2->1) R_2(w) = R_1(w) + Delta_1(w).                    (7)
```

The extra target term in (7) is nonzero only for the pure residual word
`w=1^6`.  Every corner used in the audited Hessian is mixed.  Its alternating
target term is therefore zero, and (7) reduces only to another mixed-ideal
row.  In the canonical packet this is exactly the pair `m` and `-m` in (4),
not `m` and a pure-anchor constant.

This residual-word fact is independent of the star rank.  To obtain the
desired identity

```text
unit * nabla^2(E_12) = diagonal anchor + mixed rows,
```

one still needs a second operation that changes the residual word grade and
retains source provenance.  The one-site Ward derivation changes only the
colour at `r`.

## Complete 47-profile census

For every committed clean `(q,r)=(0,2)` profile, the checker reconstructs all
21 cofactor columns, all actual incident source coefficients, and both full
source rows.  It verifies (1) directly against the complete matching tensor.
The exact census is

```text
active leader transported by the same physical column       0 / 47
active leader supplied by the direct absent-coordinate term 47 / 47
nonzero specialized r=1 Ward columns per profile             exactly 1
pure target corners on the Ward face                         0 / 188
```

So the direct-coordinate provenance guard is not peculiar to the displayed
representative.

## Reproduction

```text
python3 computations/verify_oo_c8_color_raising_ward.py
python3 -O computations/verify_oo_c8_color_raising_ward.py
```

The checker uses exact rational matching expansion only; there is no finite
field, coefficient grid, or floating-point rank decision.

