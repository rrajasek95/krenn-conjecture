# Full-orbit low-degree contraction screen

Status: **exact rational nonmembership PASS**.  Degree-zero and degree-one
`B4 x S3` contraction identities cannot kill the remote tail factor.  No
coefficient solve or Gröbner basis is used.

## Orbit ansatz

The `B4 x S3` closure of the fixed 380 rows is

```text
profile 7+1       48 rows      1 orbit
profile 6+1+1    144 rows      1 orbit
profile 3+3+2  1,680 rows      5 orbits (96,144,288,576,576)
```

Thus the full mixed-row set has 1,872 rows in seven source orbits.  Pairing
every row with all 252 literal edge-cell linear multipliers gives 471,744
objects.  Exact orbit quotienting before monomial expansion gives 463
multiplier orbits:

```text
7+1       12,096 objects    39 orbits
6+1+1     36,288 objects    56 orbits
3+3+2    423,360 objects   368 orbits
```

## Vertex-colour grading and exact solve

Every `F_w` is homogeneous for the 24-component vertex-colour grading

```text
deg(F_w) = sum_v e_(v,w_v).
```

A linear edge-cell multiplier adds one colour degree at each endpoint.  This
splits the global orbit ansatz into independent small rational blocks.

A useful vector target is `T_uv^ij H_k`: if it belonged to the mixed-row
span, the pure equation `H_k=1` would imply the individual tail cell.  The
504 such targets have four symmetry orbits, according to same/cross physical
edge and whether `k` is an endpoint or the third colour.  Their exact blocks
are:

```text
target orbit            candidates x columns    rank -> augmented rank
same-block, endpoint           1 x 195                 1 -> 2
same-block, third              2 x 300                 2 -> 3
cross-block, endpoint          1 x 195                 1 -> 2
cross-block, third             3 x 390                 3 -> 4
```

All four memberships fail over `Q`.  Each block has an explicit monomial
whose coefficient is one in `T H_k` and zero in every grade-compatible
mixed row times multiplier.  These dual witnesses are frozen in the result
JSON.  The candidate profiles contain only 71 rows, plus one 611 row in the
cross-block/third block.  No 332 row can enter: after one multiplier a 332
base word still differs from the pure colour at more than the two multiplier
endpoints.

The degree-zero pure-H target fails even earlier: its grade block contains no
mixed row, so the matrix has shape `0 x 105` and rank rises from zero to one
when the target is adjoined.

## Scalar target guard

A single “positive” scalar is not an algebraic zero-tail certificate here.
The product of all 168 tail cells vanishes whenever any one cell vanishes.
A sum of squares has nonzero isotropic zeros after algebraic closure, while
conjugate squares are not source polynomials.  More generally, one
nonconstant polynomial in `A^168` defines a hypersurface and cannot have only
the origin as its zero set.  A vector/ideal target is necessary.

## Degree-two stop

There are 31,878 quadratic cell monomials with repetition.  The degree-two
ansatz would contain 59,675,616 literal row-multiplier objects and at least
25,901 `B4 x S3` orbits.  This is not the requested small follow-up, and no
audited quadratic localizer would turn such an identity into the individual
tail equations, so it was not launched.

The exact dual witnesses retire degree-zero/one Euler-contraction machinery.
The remaining route is the boundary-valued substituted 332 system or a
higher-degree identity with an explicit unit/localizer.

## Replay

```sh
python3 computations/unaudited-codex-tail-remote-orbit-contraction-2026-08-21/audit_tail_remote_orbit_contraction.py --write-results
python3 -O computations/unaudited-codex-tail-remote-orbit-contraction-2026-08-21/audit_tail_remote_orbit_contraction.py --write-results
python3 -I -S computations/unaudited-codex-tail-remote-orbit-contraction-2026-08-21/audit_tail_remote_orbit_contraction.py --write-results
```

