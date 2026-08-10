# One extra coupled channel cannot restore the second kernel

## 1. Complete one-coordinate boundary

Start from any of the four minimal simultaneous mate charts in
[`the private-row mate theorem`](shared-reciprocal-two-bad-mixed-private-row-mates.md).
After localizing the mate equations, write

```text
xy=2,   pq=-1,
y=2/x,  q=-1/p,              x,p !=0.                  (1)
```

Each chart has `16` occupied endpoint-colour coordinates.  There are `74`
unused coordinates, and the checker adjoins every one of them with an
independent nonzero weight `h`.  Thus the theorem covers

```text
4*74=296
```

coefficient-exact one-extra charts.  This includes an extra cell on an
already occupied physical edge as well as a new physical edge; parallel
aggregate cells and endpoint order are retained.

## 2. Maximal-minor certificate

Delete the duplicate cofactor-map column supplied by the old kernel

```text
U=e_t@0-e_a@1.
```

This leaves a `243x14` matrix over the Laurent ring

```text
Q[x^+-1,p^+-1,h^+-1].                                 (2)
```

For `65` of the `74` extra coordinates in each mate type, the original
`14x14` minor remains the Laurent unit `+-16/p^2`.  Only nine coordinates
can change that pivot minor.

For each of those nine exceptions the checker extracts complementary
maximal minors and saturates by `xph`.  Equivalently it adjoins inverses
`xi,pi,hi` and computes the exact Gröbner basis of

```text
<all selected minors, x*xi-1, p*pi-1, h*hi-1>.
```

All `4*9=36` exceptional ideals are the unit ideal.  Hence no common zero
of the maximal minors exists anywhere on the coefficient torus.

The exact census is

```text
260 charts: original Laurent-unit minor,
 36 charts: complementary saturated minor ideal = (1). (3)
```

Therefore every one-extra chart satisfies

```text
rank(Phi)>=14,             dim ker(Phi)<=1.             (4)
```

The bound allows some extra cells to break the old kernel and raise the
rank to `15`; it is deliberately stronger than checking only the displayed
second-kernel vector.

## 3. Consequence

A two-bad local seed requires two independent cofactor-kernel rows before
its nonlinear product can represent the missing pure class.  Equation (4)
shows that no single additional shared mate or cancellation cell beyond a
minimal four-cell repair can restore that prerequisite.  Thus a rational
seed does not occur on the complete one-extra boundary, regardless of
whether a special coefficient choice repairs one bright row.

The next possible escape is genuinely coupled: at least two further
endpoint-colour coordinates must be added together so that their matching
product can change the saturated rank ideal.  This note does not classify
that two-extra boundary.

## 4. Reproduction

```sh
uv run python computations/verify_shared_reciprocal_two_bad_mixed_one_extra_channel.py
uv run python -O computations/verify_shared_reciprocal_two_bad_mixed_one_extra_channel.py
```

Both modes reproduce

```text
909703d990302ed5e5fcda5b15ed9f2c3ecbdf7ace575f4fdd2ff8c5d313d8ca
```
