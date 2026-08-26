# Source-relative Hermitian least-star trace audit

Status: **the strongest available Hermitian identity distinguishes the two
controls, but its GHZ specialization is an exact cancellation rather than a
positive SOS remainder.  This scalar route is terminal without a new sign
theorem for the pure dual trace.**

## Candidate survey

Only three genuinely source-relative candidates survived the archive screen.

1. **Canonical least-star pseudoinverse trace.**  On an injective star chart,
   it uses the Hermitian minimum-norm dual rather than an arbitrary conormal
   representative.  This is the strongest candidate and is audited exactly
   below.
2. **Global conormal Euler trace.**  At a regular norm minimum,
   `A=J_A^* lambda` and homogeneity gives
   `||A||^2=m <lambda,F(A)>`.  Multiplier nonuniqueness and the absence of a
   sign on the mixed pairing leave the same obstruction as the star trace.
3. **Matching-Gram/Fischer--Bombieri SOS.**  Pure normalization gives
   `||F||^2=3+sum_mixed |F_w|^2`.  The archived doubled-norm screen shows that
   only the trivial perfect-matching association-scheme sector contributes,
   so this restates the mixed equations and has no source-relative remainder.

The archived least-star overlap/Laplacian candidate is not a fourth live
route: its restricted overlap complex is surjective on both injective-star
controls (ranks `54/54` at `n=4` and `135/135` at `n=6`).  It supplies no
cohomological positive term distinguishing them.

## Exact scalar identity

Fix a vertex `v`.  Let `A_v` be the vector of the coloured cells on its full
star and let

```text
L_v : A_v -> F(A)
```

be the literal derivative/reconstruction map with all other edge blocks held
fixed.  Every perfect matching uses exactly one edge at `v`, hence

```text
L_v A_v = F(A).                                           (1)
```

When `L_v` is injective, its canonical Hermitian least dual is

```text
Lambda_v = L_v (L_v^* L_v)^(-1) A_v,
L_v^* Lambda_v = A_v.                                    (2)
```

Pairing (1) with (2) gives

```text
||A_v||^2 = <Lambda_v,F(A)>.
```

Every source cell belongs to two vertex stars, so summing produces the exact
trace identity

```text
2 ||A||^2 = sum_v <Lambda_v,F(A)>.                        (3)
```

For a normalized ternary GHZ output, pairing and summing all mixed equations
is exactly

```text
sum_v sum_(w mixed) conjugate(Lambda_v[w]) F_w = 0,        (4)
```

and (3) reduces to

```text
2 ||A||^2 = sum_(v,c) conjugate(Lambda_v[c^n]).            (5)
```

Thus this is genuinely a Hermitian identity available at the least-star
normal point, and (4) genuinely uses the simultaneous mixed zero equations.

## Exact controls

The checker works over `Q(omega)`, `omega^2+omega+1=0`, builds every matching
amplitude and every literal star matrix, solves the Hermitian Gram systems,
and verifies `L_v^* Lambda_v=A_v` exactly.

For the exact `n=4` GHZ global minimum,

```text
||A||^2=6,
sum_v <Lambda_v,F>=12,
pure pairing=12,
mixed pairing=0.
```

Each of its four star norms is `3`, and each least dual has support only on
the three pure output words.

For the phased `n=6` block-injective local minimum of its own non-GHZ output,

```text
||A||^2=63,
sum_v <Lambda_v,F>=126,
Re(pure pairing)
  = 8000216223841636996444963448570591902755427032162298889105712222020
    / 9575973051879024764702612475549368094296999685843777897287986422387
  ~= 0.8354468,
Re(mixed pairing)
  = 1198572388312915483356084208470649787978666533384153716169180576998742
    / 9575973051879024764702612475549368094296999685843777897287986422387
  ~= 125.1645532.
```

The two `omega` coefficients cancel exactly, and the exact full values are in
the result JSON.  Hence the least-star trace does distinguish the controls:
the GHZ mixed pairing is zero, whereas the phased block-injective mixed
pairing is nonzero.

## Terminal interpretation

The useful-looking positivity is only positivity of the *total*
pseudoinverse quadratic form.  Its decomposition into pure and mixed output
coordinates contains cross terms and is indefinite.  On GHZ, the mixed
piece vanishes because the mixed equations already vanish; what remains is
the unconstrained pure-dual trace (5), which is identically `2||A||^2`.
There is therefore no positive source-faithful remainder and no contradiction.

The global Euler trace and matching-Gram identity fail for the same structural
reason.  A further Hermitian attack would need genuinely new information,
such as a sign or rigidity theorem for the three pure coordinates of every
canonical least dual; none of the archived adjoint-star, overlap-Laplacian, or
Gram identities provides it.

## Replay

```sh
python3 computations/unaudited-codex-hermitian-star-sos-2026-08-22/audit_hermitian_star_trace.py --write-results
python3 -O computations/unaudited-codex-hermitian-star-sos-2026-08-22/audit_hermitian_star_trace.py
python3 -I -S computations/unaudited-codex-hermitian-star-sos-2026-08-22/audit_hermitian_star_trace.py
```

The hostile `--mutate-n4-mixed` run must fail.  All three valid modes return
logical SHA-256
`bc84ae853342c5ede955e2e11e9bb258f1b33a1107527709755081f1b81090d9`.
