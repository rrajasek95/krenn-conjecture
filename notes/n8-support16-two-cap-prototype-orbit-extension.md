# Support 16: reach of the two-cap prototype

The exact checker is
[`verify_n8_support16_two_cap_prototype_orbit_extension.py`](../computations/verify_n8_support16_two_cap_prototype_orbit_extension.py).

## Result

Among the 281 stabilizer orbits in the corrected directed source-star
register, exactly 22 orbits, representing 25 directed incidences, have a
forced distinct-direct-colour cover by two cap faces of the shared-`20`
prototype.  Conditional on the same mutual-coordinate companion anchor chart
as the prototype theorem, all 22 therefore land an arbitrary noncoordinate
near vector in an active clean cap.

```text
all stabilizer orbits / incidences             281 / 376
forced distinct two-cap cover                   22 / 25
global same-colour completion guard            259 / 351
prototype-compatible representative caps             144
```

The forced set consists of one shared orbit—the original `2 -> 02` case—and
21 never-private orbits.  Their incidence weights are one and 24.  Twenty
orbits have exactly two prototype faces and two have three.

## 1. What counts as the same prototype

For a directed source incidence `X_vw` and a cap `vq`, expand every residual
factor through

\[
 R_{ij}^{vq}(K)=K\mathbin{\lrcorner}(X_{vi}\otimes X_{qj})
                +K\mathbin{\lrcorner}(X_{vj}\otimes X_{qi}).  \tag{1}
\]

A cap is called prototype-compatible when its complete oriented response has
exactly

```text
2 expanded monomials through X_vw
2 expanded companion monomials.
```

For every one of the 144 compatible representative caps, the checker proves
that the two companion monomials use the same two source-star edges on both
cap shores, with the pairings crossed.  In a mutual-coordinate anchor chart
their coefficient is therefore the same complementary `2x2` permanent as in
the shared-`20` theorem.  This is checked from contraction slots, not inferred
from residual `R_ab` labels.

The number of compatible faces per stabilizer orbit is

```text
faces per orbit              0     1     2    3
stabilizer orbits          162    96    21    2
directed incidences        216   134    24    2
```

## 2. Forced distinct direct colours

Declare the selected source edge `X_vw` nonanchor.  Let `d` be the degree of
the directed endpoint `v`, and let `m` be the number of prototype cap edges
at its star.  If all prototype caps had the same direct colour, then the
remaining `d-1-m` non-target edges could contribute at most that many further
colours.  Hence the exact three-anchor condition forces two distinct
prototype colours whenever

\[
                         d-1-m\leq 1.                  \tag{2}
\]

Every orbit satisfying (2) has `d=4`, so after removing the nonanchor target
the other three edges are necessarily the three distinct coordinate anchors.
The shared-`20` construction tests the noncoordinate near vector against two
of those direct colours.  It cannot vanish on both without becoming a
coordinate vector; one cap therefore supplies the denominator-cleared active
rank-two zero.

The checker imports and rechecks all twelve symbolic rank charts from the
prototype theorem before applying this count.

## 3. The 259 sharp guards

Condition (2) fails on the other 259 orbits.  This is not merely a weak local
count.  For every residual orbit the checker constructs a full colouring of
the entire 16-edge support representative such that

* the selected edge is the sole declared nonanchor;
* every other support edge is a mutual-coordinate anchor;
* every vertex sees all three anchor colours; and
* every prototype cap at the directed star has direct colour zero.

Thus graph-wide anchor compatibility does not rescue the two-colour argument.
Of the 259 residual orbits, 258 have at most one prototype face.  One
degree-five orbit has two prototype faces, but the two remaining non-target
star edges carry the other two colours, allowing the prototype faces to
coincide in colour.  This single orbit is the exact same-colour collision
guard with two surviving tests.

These colourings are not asserted to satisfy the complete mixed GHZ rows.
They are sharp global guards against extending the two-cap lemma from anchor
coverage alone.  Progress on the 259 must use a response with more companion
terms, a three-cap/higher-rank construction, or a complete mixed-row exit.

## Reproduction

```sh
python3 computations/verify_n8_support16_two_cap_prototype_orbit_extension.py
python3 -O computations/verify_n8_support16_two_cap_prototype_orbit_extension.py
python3 -I -S computations/verify_n8_support16_two_cap_prototype_orbit_extension.py
```

Pinned ledger SHA-256:

```text
cb0f94826af7d3119eb11f4b59022797951b18767efae1095d417426d8d89be2
```
