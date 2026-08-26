# X5 triangle Hermitian degree-four audit

## Verdict

The proposed low-degree positive identity does **not** exist in the natural
triangle-sensitive ansatz.  This is a source-faithful, scoped no-go, not a
claim against higher-degree or localized X5 certificates.

The load-bearing X5 data were used literally: the 6,558 mixed word rows split
under `S8 x S3` into the nine profiles

`710, 620, 611, 530, 521, 440, 431, 422, 332`

of sizes `48,168,168,336,1008,210,1680,1260,1680`.  Thus the test uses the
full nine-dimensional diagonal X5 norm span, rather than the superseded five
off-count trace screen.

## Exact obstruction

Each mixed amplitude has holomorphic source degree four, so `P_mixed` has
bidegree `(4,4)`.  Each literal entry of the `108 x 9` triangle response matrix
`L_T` has degree two, so the natural quartic spectral moments of `L_T` also
have bidegree `(4,4)`.  In contrast:

- the fixed-`K` clean-cap error `s r^2 x/2 + r^3/6` has degree six, hence its
  norm square has bidegree `(6,6)`;
- the first polynomial rank-nine detector `det(L_T)` has degree 18, hence its
  norm square has bidegree `(18,18)`.

Consequently neither the actual cap-error square nor a rank-drop detector can
occur in a polynomial `(4,4)` identity.

The complete output-Hermitian census has 12,870 ordered contingency tables,
2,180 `S8 x S3` ordered-pair orbits, and 1,188 real Hermitian orbits after
transpose.  Output quadratics alone therefore form a large space but do not
encode source response rank.

## Interpolation certificate

On 21 deterministic dense signed sources, every site-colour port has squared
weighted degree 21, so every source is exactly moment-balanced.  At both
primes 1009 and 1013:

- the nine literal X5 profile norms have rank 9;
- the seven triangle spectral moments plus pure norm and source norm have
  rank 9;
- their joint rank is 18, so their spans intersect trivially;
- adjoining `P_mixed` to the triangle/control span raises rank 9 to 10.

Each modular rank jump exhibits a nonzero integer minor, proving the stated
nonmembership over characteristic zero.

There is also a stronger positivity guard: the pinned exact balanced strict
local minimum `f281d19d...` has every one of the 560 matrices `L_T` of rank 9
and all 6,558 mixed amplitudes nonzero.  Hence every nonnegative expression
indexed by `ker(L_T)` is zero there while `P_mixed>0`; a universal
kernel-response/cap-error sum-of-squares identity is impossible.

## Scope

This closes constant-coefficient coupling of the full nine X5 profile norms
to the listed natural `(4,4)` triangle moments, and all universal positive
kernel-square identities.  It does not exclude identities modulo the X5
ideal with source-dependent multipliers, rational identities after inverting
response minors, higher-degree Positivstellensatz certificates, or an
identity elsewhere in the full 1,188-orbit Hermitian output space.

Replay:

```sh
python3 audit_triangle_hermitian_degree4.py --check-results
python3 -O audit_triangle_hermitian_degree4.py --check-results
python3 -I -S audit_triangle_hermitian_degree4.py --check-results
python3 audit_triangle_hermitian_degree4.py --check-results --mutate  # must fail
```

Logical result SHA-256: `892016178e40538f6d2f624a846e942bc343b4c4df70d8a412d1e33b061b453e`.
