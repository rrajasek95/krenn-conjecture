# Lowest crossing-tail response on the aligned diagonal chart

Status: **UNAUDITED exact three-mode PASS; local response certificate, with
an explicit global-lift scope blocker.**

## Literal 90-to-45 interface

For the raw source row `00000011` and tail pair `67`, the 105 perfect
matchings split into 15 using the common tail and 90 not using it.  Every
one of the latter has two `0/1` crossing edges and two residual `0/0` fine
edges.  Group by

```text
unordered residual pair {a,b} + a perfect matching of the other four sites.
```

There are exactly 45 groups: 15 residual pairs times three fines.  Each
contains exactly the two raw endpoint orientations `(6a,7b)` and `(6b,7a)`.
The JSON result stores every matching index, matching, raw endpoint-ordered
cell, fine, and orientation.

Writing the twelve crossing-tail cells as

```text
y_a = a_{a6}^{01},    z_a = a_{a7}^{01},    0 <= a < 6,
```

the complete degree-two tail is

```text
R(y,z) = y^T C z,
C_aa = 0,
C_ab = Hafnian of the diagonal graph on {0,...,5}\{a,b}.
```

Each off-diagonal `C_ab` is the sum of the three fine groups; symmetry gives
the two endpoint-ordered occurrences.  Thus this formula is a collection of
all 90 literal terms, not a spectator-tail replacement.

## Exact support-six certificate

On the frozen aligned support-six point over `Q(z), z^2+2z-1=0`, with
anchors `01,23,45,67` normalized to one, the response matrix is

```text
[ 0       0       0      -z-3     0       z-1 ]
[ 0       0       z-1     0      -z-3     0   ]
[ 0       z-1     0       0       0       1-z ]
[-z-3     0       0       0       z+3     0   ]
[ 0      -z-3     0       z+3     0       0   ]
[ z-1     0       1-z     0       0       0   ].
```

It has

```text
rank(C) = 6,       ker(C) = 0,       det(C) = -64.
```

The unique maximal minor is therefore the full determinant.  The artifact
stores an explicit `C^{-1}` and checks both `C^{-1}C=I` and `CC^{-1}=I` in
the quadratic number field.

The same literal matrix was evaluated symbolically on the four-parameter
weight-zero diagonal family over
`Q(sqrt(2),sqrt(65))(u,v,w,t)`.  All six permanent rows, four triangle rows,
twelve branch-51 selected cofactor rows, and `H=4` were independently
replayed.  The same minor is identically

```text
det(C(u,v,w,t)) = -64.
```

Thus `adj(C)/(-64)` is a symbolic left inverse over that whole family, not
just at its support-six specialization `t=0,u=v=w=1`.

## What the inverse does—and does not—prove

The twelve polar coefficients of the quadratic response are

```text
Py = dR/dy = C z,       Pz = dR/dz = C y.
```

The stored exact identities

```text
z = C^{-1} Py,          y = C^{-1} Pz
```

force all twelve crossing-tail cells to vanish **if** all twelve polar
coefficients occur in the lowest source initial ideal.  The `12x12` Hessian
has rank 12, determinant 4096, and zero kernel.  After quotienting the two
endpoint orientations under `6<->7`, the symmetric and antisymmetric blocks
are `C` and `-C`; both still have zero kernel.

The fixed literal row alone is insufficient.  Its equation is only the
single quadric `R=0`; for example `y=e0,z=e0` is nonzero and satisfies it
because `C_00=0`.  Hence invertibility of `C` proves nondegeneracy of the
pairing, not deletion of the twelve star cells unless the source supplies
the polar rows separately.  Establishing that source-initial-ideal inclusion
is the next honest global diagonal-to-full lift gate.

The response construction was replayed under all 384 elements of the
anchor stabilizer `C2^4 semidirect S4`, allowing the tail anchor to move.
Each transform gives `P C P^T` and determinant `-64`.  This establishes the
required B4 covariance.

## Controls and scope

Deleting one occurrence changes the literal census from 90 to 89.  Changing
one physical response coefficient changes the determinant from `-64` to
`-36`; both mutation controls fire.

This is a local degree-two response certificate on one support-six chart and
one aligned positive-dimensional component.  It is not a full 240-variable
initial-ideal theorem, and no higher tail weight was expanded.

Standard, `-O`, and `-I -S` runs share logical digest
`c539050f19006735039b263ce6f73d041e16d71fb310eb948a29554e4941608b`.
The mutation runs share logical digest
`c389523e3eb2c1600c1322030aca94a3436ac500e60a6e4a195f36a9922a4e3b`.
The checker SHA-256 is
`955f20530ad6256a350992eae117205bd632d2f3956c5b09e3bdf6bd22606fb4`.
