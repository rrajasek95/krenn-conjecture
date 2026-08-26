# Other diagonal `P=2` orbit: leakage, carriers, and exact lift

## Terminal verdict

The elementary two-cell energy-to-cap statement holds on the second diagonal
equality orbit, but its multi-ray extension fails at the first four-cell
level.  The first full-carrier-evading zero Hessian direction nevertheless
integrates to a strictly upward exact arc:

```text
P(r) = 6 - 8 r^4 + 4 r^8 = 2 + 4 (r^4-1)^2.
```

Thus this orbit supplies a sharp quartic-flat control, not a descending
counterfamily.  The inequivalent six-leakage Laurent-orbit family remains the
live descending no-carrier family.

## Canonical source and elementary rays

The three diagonal matching layers are

```text
M0 = 01 23 45 67
M1 = 02 13 46 57
M2 = 03 14 27 56.
```

Literal matching enumeration gives the three pure amplitudes and exactly two
mixed amplitudes, `00001111` and `11110000`, all with coefficient one.  Hence
`P=2`.  The matching triple has stabilizer order eight.

Among 240 off-support endpoint-coloured cells there are 72 minimal two-cell
rays admitting the unique diagonal second-order port-balance correction.
Exact phase minimization gives

```text
P2 distribution: 0^12, 1^4, 2^8, 3^40, 4^8.
```

The 12 nonpositive rays are all zero rays, in three stabilizer orbits of size
four.  Every literal ray has an active support-separated `K=I` response-star
cap; activity includes the exact direct-trace constant-one check.  This proves
the same elementary local energy-to-cap statement already known at the other
diagonal equality orbit.

## Minimal multi-ray obstruction

Every single balanced ray retains a frozen clean cap.  At four cells, unions
of two disjoint rays give 192 literal / 36 stabilizer-orbit supports that
destroy all 12 frozen support-separated caps.  Their exact continuous phase
minima are

```text
0^8, 1^2, 2^2, 3^8, 5^2, 6^14.
```

For every orbit, the triangle-inequality lower bound on the Hermitian and
holomorphic pair interactions is attained by a Gaussian phase assignment, so
the displayed values are exact continuous minima, not a phase-grid bound.

Seven zero orbits have a minimizing phase with no `K=I` response star or
triangle.  The lexicographically first is

```text
support = {04^(0,1), 07^(1,0), 16^(0,1), 26^(1,0)}
phases  = (+,+,-,-)
P2      = 4 + 2 Re(y04*y16) + 2 Re(y07*y26) = 0.
```

For this source, fraction-free row reduction over `Q(t)` audits all 168 star
and 560 triangle carriers.  For each carrier it tests membership of the three
diagonal blockers and the direct-pair blocker in the outside-response
rowspace.  There are 64 rank/membership profile bins and zero active carriers:
every one of the 728 masks is nonzero.  This terminally refutes the multi-ray
energy-to-cap implication at tangent order.

## Exact balanced and pure-normalized integration

The leakage degrees on the four anchors in colours zero and one are
`(1,0,0,1)` and `(1,0,1,0)`; colour two has `(0,0,0,0)`.  Put

```text
s=t^2=r^2-r^-2,   C=r^2,   C(C-s)=1.
```

On a degree-zero anchor put `r`, on a degree-one anchor put `r^-1`, keep
colour two unit, and put the four leakage cells equal to `(+t,+t,-t,-t)`.
Then every port moment in each active colour is exactly `r^2`, while the four
anchor product in every colour is exactly one.  Literal amplitude enumeration
gives

```text
P-2 = 4 t^4 + 4 t^6 + 2 t^8 + (1/2)t^10 - (1/32)t^14 + O(t^18),
P   = 2 + 4(r^4-1)^2 exactly.
```

The positive real branch is `1 <= r < infinity`.  It has unique minimum two
at the equality source and is coercive.  At its projective boundary, four
degree-zero anchors and four leakage cells survive after `r^-1` rescaling;
the reciprocal anchors and the colour-two unit anchors vanish.  Exact finite
quadratic-field audits at `r=101/100` and `r=2` again find zero active
carriers among all 728.

This is different from the Laurent-orbit six-cell family: that family uses
six leakage cells across three colours, has 17 outputs, stays no-carrier, and
begins `P-2=(-51/200)s^2+O(s^4)`.  The present four-cell family is globally
harmless along its canonical exact integration.

## Scope and replay

The exact lift uses no new higher-order off-support cells.  Positivity along
this lift does not prove that every formal integration of the same tangent is
positive after arbitrary new higher-order source directions.

All three checkers pass under standard Python, `python3 -O`, and
`python3 -I -S`.  The elementary cap-ledger mutation, the multi-ray lower-bound
mutation, and the integrated curvature-sign mutation each fail as expected.

Logical digests:

```text
elementary rays: 7187799b8fcf5926333e92f543ad7a27eca4676191b378d03c2fefb38b68ab6a
multi-ray:       060577e16f0c9cdad76cda669f5d30fb80d994926621ab099f98711252a647f8
exact lift:      921dae0e78b24675007f9075a541f85fa04be44311ce19f2ceaa276413dc5b64
```
