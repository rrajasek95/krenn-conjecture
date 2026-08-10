# N=8 one-bad whole-packet Macaulay frontier

## Scope

This note records a bounded exact feasibility calculation for the two sharp
coordinate-monomial star orbits in the normalized one-bad packet.  It does
not restrict the support of the residual source: all 135 endpoint-coloured
cells of the six-site source `q` remain independent variables.

After fixing the four star rows, the packet is exactly

```
H_0124(q) = X_0^4,       H_0135(q) = X_1^4,
H_U(q)    = 0,           H_V(q)    = 0,
H_012345(q) = X_2^6.
```

For sharp orbit 0, `(U,V)=(0125,0134)`; for sharp orbit 1,
`(U,V)=(0145,0123)`.  Thus the scalar coefficient ideal has 324 quadratic
four-site generators and 729 cubic six-site generators.  The site
permutation `(2 4)` carries the first ideal to the second, so it is enough to
compute one of them.

## Exact bounded result

The checker builds the ordinary degree-`D` Macaulay matrix, but only its
fine-multidegree incidence component containing the constant monomial.  Rows
outside that component cannot participate in a unit certificate.  Exact
ranks over `QQ` are:

| `D` | columns | rows | rank | rank after adjoining `1` |
|---:|---:|---:|---:|---:|
| 3 | 22 | 7 | 7 | 8 |
| 4 | 112 | 65 | 57 | 58 |
| 5 | 1,320 | 1,105 | 921 | 922 |
| 6 | 2,160 | 2,016 | 1,586 | 1,587 |

Consequently `1` is not in the degree-at-most-six Macaulay row space.  This
is a rigorous lower bound on the degree of any Nullstellensatz certificate;
it is **not** a rational point and does not prove that the ideal is proper.

At degree seven the same exact component construction jumps to 70,398
columns and 110,898 rows (68,238 columns are new in degree seven).  Naive
sparse modular elimination was capped without a rank result.  This is the
current whole-packet computational frontier; no claim is made about the
degree-seven rank.

## Consequence and next useful computation

The earlier sparse-support exclusions do not extend automatically to the
unrestricted packet, and a low-degree unit certificate does not settle it.
The next bounded attack should exploit a structural hafnian
flattening/condensation identity, or branch on a nonzero target matching in
each of the two diagonal fibres and perform source-faithful localized
elimination.  Repeating naive degree-seven Gaussian elimination is not a
useful next step.

## Reproduction

```bash
.venv/bin/python computations/verify_n8_one_bad_whole_packet_macaulay.py
.venv/bin/python -O computations/verify_n8_one_bad_whole_packet_macaulay.py
```

The checker constructs every hafnian coefficient from literal physical
matchings, verifies the orbit isomorphism, computes the four exact ranks over
`QQ`, and guards the degree-seven component ledger without attempting its
rank.
