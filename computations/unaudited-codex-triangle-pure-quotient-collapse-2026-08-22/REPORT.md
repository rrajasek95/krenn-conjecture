# Triangle pure-word quotient collapse

Status: **UNAUDITED exact theorem plus two-prime profile PASS**. This is a
strict reduction of the triangle-blocker branch. It is not a proof of the
eight-site conjecture.

## The identity

Fix a cap pair `pq`, its six residual sites `R`, a residual triangle `T`, and
a colour `c`. For a cap matrix `K`, write

```text
d(K)       = <K,A_pq>,
kappa_c(K) = K_cc,
H_c        = Haf(A_R[c,c]).
```

Partitioning the 105 matchings according to whether they use `pq` gives the
literal `15+90` identity

```text
F_(i,j,c^6) = H_c A_pq[i,j]
              + sum_(ab subset R) h_(ab,c) rho_ab^(cc)[i,j].       (1)
```

The Rust checker reconstructs (1) for all nine endpoint colours, all 28 cap
pairs, all three pure residual colours, every stored source, and both audit
primes. No Groebner or interpolation step is used.

At a normalized exact `X5` point, the left side of (1) is the matrix unit
`E_cc`. Contracting with `K` therefore gives

```text
kappa_c(K) = H_c d(K) + sum_(ab subset R) h_(ab,c) R_ab^(cc)(K).   (2)
```

On the simultaneous cyclic five-set rank-nine open proved in the upstream
response-surjectivity artifact, all nine coordinate functionals of each of
the three internal triangle responses belong to `rowspan L_T`. The other
twelve residual-edge responses are literal rows of `L_T`. Hence (2) descends
to the exact quotient identity

```text
[kappa_c] = H_c [d]  in Mat_3^* / rowspan(L_T),  c=0,1,2.          (3)
```

## Consequence

On `H_0 H_1 H_2 != 0`, the direct blocker and all three diagonal blockers
are equivalent modulo `rowspan L_T`. Thus the four-way triangle-blocker
disjunction collapses to one quotient condition: if any one blocker is in
`rowspan L_T`, all four are. If `H_c=0`, equation (3) instead makes the
corresponding diagonal blocker automatic; this is the explicit boundary
divisor.

The remaining problem is therefore no longer four unrelated branches. It
is the union of:

1. the common-blocker branch on the simultaneous five-set and pure-cofactor
   open; and
2. the five-set determinantal or pure-cofactor boundary.

The identity does **not** say that either branch is empty. In particular,
full carrier rank blocks all four forms vacuously. A finishing argument must
combine (3) with a source-derived defect (`E1/E2`, a fixed-label full-nine
relation, or an equivalent rank loss), rather than treating blocker
membership alone as restrictive.

## Two-prime census

The profile enumerates

```text
28 cap pairs * 3 colours * 20 residual triangles = 1,680 groups/source.
```

The exact source-universal identity is checked `28*3*9=756` times per source
and prime. At primes 1009 and 1013 the full ledgers agree. The key controls
are:

| source | simultaneous open | `H_c=0` there | carrier corank there |
|---|---:|---:|---:|
| dense | 1680 | 0 | 0 |
| W40/X4 | 8 | 4 | 8 |
| W25/X3 | 157 | 62 | 131 |
| dense-support E1 block | 48 | 0 | 48 |
| good-star E1 block | 1608 | 0 | 48 |

The last control is load-bearing: it exhibits exactly 48 open groups with
full response rank eight, nonzero `H_c`, and an inactive kernel. It is not
an exact `X5` point, so it identifies the next missing ingredient rather
than refuting (3): the full-nine/fixed-label equations must exclude this
defect-one hostile model.

## Replay

```sh
python3 computations/unaudited-codex-triangle-pure-quotient-collapse-2026-08-22/check_results.py
```

The checker invokes the dependency-free Rust implementation twice, checks
the complete ledgers, and pins the exact source and implementation hashes.
