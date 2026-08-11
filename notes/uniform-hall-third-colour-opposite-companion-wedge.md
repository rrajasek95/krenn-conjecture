# Opposite third-colour companions close the paired Hall path

## Result

The four active decorations left by the paired bridge-dark path are not an
independent wrong-colour web.  They repair one another and produce the
existing active four-good overlap.

In the canonical residual

```text
M0 = 03 | 14 | 25,
M1 = 24 | 35,
M2 = 15 | 34,
```

the trapped mates are

```text
24:02, 35:20        on the pure-one edges,
15:01, 34:10        on the pure-two edges.
```

Consider the adjacent central arms `35` and `34`, sharing site `3`.

* After deleting `35`, the pure-zero and pure-two matchings supply rows zero
  and two.  The opposite decorations `34:10` and `15:01` supply row one at
  sites `3` and `5`.  Both deleted stars therefore have rank three.
* After deleting `34`, the pure-zero and pure-one matchings supply rows zero
  and one.  The opposite decorations `35:20` and `24:02` supply row two at
  sites `3` and `4`.  Again both deleted stars have rank three.

Both arms belong to nonzero selected diagonal target matchings, so their
deleted cofactors are nonzero.  Thus they are active good arms, not merely
rank witnesses.

Checker:
`computations/verify_uniform_hall_third_colour_opposite_companion_wedge.py`.

## The shared-site transition

At the common site `3`, the two central corrections are

```text
35:20 -> head e2, remote colour 0,
34:10 -> head e1, remote colour 0.
```

Their heads are distinct.  In the sharp residual, the entries which could
cancel their two-by-two wedge are exactly

```text
35:10,       34:20.
```

Those are the missing anchor-labelled companions: the first has the
pure-one row on the colour-one arm, and the second has the pure-two row on
the colour-two arm.  Consequently there is an exact dichotomy.

1. If either such companion occurs, apply the complete decorated-anchor
   mixed-word exchange theorem to that `k`-labelled decoration.  It gives a
   pure-anchor reselection, an avoiding matching/off-anchor escape, or the
   corresponding localized row unit.  Thus the packet leaves the
   third-colour residual for an already certified landing; mere presence of
   the cell is not being treated as activity by itself.
2. If neither occurs, the transition minor is

   \[
                    \kappa=-q_{35}^{20}q_{34}^{10}\ne0. \tag{1}
   \]

Together with the four rank-three deleted stars and the two nonzero
cofactors, (1) is precisely the distinct-head active four-good overlap.
No same-star deletion theorem is needed in this last branch.

## Uniformity and scope

The proof is local and works at every residual order `h>=3`.  Append the
same disjoint diagonal factor edges to `M0,M1,M2`; they multiply the two
activity cofactors by nonzero factors and leave the four local ranks and
the minor (1) unchanged.

Combining this with the complete exchange alternatives from the preceding
reduction gives

```text
pure-Qk reselection,
off-anchor active escape,
anchor-safe lock-kernel deletion or localized unit,
or the active distinct-head four-good overlap above.
```

This closes the four-decoration paired-path residual as a landing theorem.
It does not reprove the downstream curved full-nine obstruction, and it
does not claim that an arbitrary longer Hall path has already been reduced
to this four-decoration local packet.

Run

```text
python3 computations/verify_uniform_hall_third_colour_opposite_companion_wedge.py
python3 -O computations/verify_uniform_hall_third_colour_opposite_companion_wedge.py
python3 -I -S computations/verify_uniform_hall_third_colour_opposite_companion_wedge.py
```

Frozen ledger SHA-256:

```text
9f18f9a1266df4f0ff1a406bd14b05c42bc8dd62ff9e13f31e432a1911a46cb7
```
